import os
import re
import markdown2
from subprocess import Popen, STDOUT, PIPE
import contextlib


@contextlib.contextmanager
def temp_chdir(path):
    starting_directory = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(starting_directory)


def run_command(args, failure_str):
    p = Popen(args, stdout=PIPE, stderr=STDOUT)
    output, err = p.communicate()
    if err:
        raise Exception(failure_str.format(err))
    return output.decode('utf-8')


def refresh_repository(repo_path):
    if not os.path.exists(repo_path):
        raise Exception("No initialized repository at {}".format(repo_path))
    with temp_chdir(repo_path):
        args = ['git', 'fetch']
        run_command(args, "Failed to fetch repository: {}")


def prepare_repository(repo_url, repo_path):
    if not os.path.exists(repo_path):
        print("No repository detected at {}".format(repo_path))
        print("Pulling {}...".format(repo_url))
        os.makedirs(repo_path)
        with temp_chdir(repo_path):
            args = ['git', 'init']
            run_command(args, "Failed to initialize repository: {}")

            args = ['git', 'remote', 'add', 'origin', repo_url]
            run_command(args, "Failed to fetch repository: {}")

            refresh_repository(repo_path)


def branch_list(working_tree_dir):
    with temp_chdir(working_tree_dir):
        args = ['git', 'branch', '-r']
        p = Popen(args, stdout=PIPE, stderr=STDOUT)
        output, err = p.communicate()
        if err:
            raise Exception("Failed git call: %s" % str(err))
        output = output.decode('utf-8').replace('* ', '')
        return output.split("\n")


def diff_from_sha(repo_dir, ref_a, ref_b, word_diff=False):
    with temp_chdir(repo_dir):
        args = ['git', 'diff', ref_a, ref_b, '--unified=2000']
        if word_diff:
            args.append('--word-diff')
        p = Popen(args, stdout=PIPE, stderr=STDOUT)
        output, err = p.communicate()
        if err:
            raise Exception("Failed git call: %s" % str(err))
        return output.decode('utf-8').split("\n")


def diff_replace(diff):
    outlines = []
    # Read in the lines of the diff and remove the metadata
    for idx, line in enumerate(diff):
        if line.startswith("diff --git"):
            break
    else:
        raise Exception("Invalid diff")
    diff = diff[idx:]

    # Now, find every "diff --git ..." line and replace it (and all others
    # leading to the line that starts with "@@") with a special div that
    # indicates a new file
    regex = re.compile("^diff --git a/(\S+)")
    cur_line = 0
    while cur_line < len(diff):
        m = regex.match(diff[cur_line])
        # We've found a git line.
        if m:
            end_line = cur_line
            while not diff[end_line].startswith("@@ "):
                end_line += 1
                if end_line >= len(diff):
                    raise Exception("No end for last diff file")
            print("found %s from lines %d to %d" % (m.group(1), cur_line, end_line))

            # Ugly ugly, but it works. Remove all of the git lines and replace with a div
            if cur_line == 0:
                diff = diff[end_line+1:]
            else:
                diff = diff[:cur_line] + diff[end_line+1:]
            diff.insert(cur_line, "<div class=\"file\">File: %s</div>\n" % m.group(1))
        else:
            cur_line += 1

    # Find and replace dif elements with the html span tags
    replacements = {
        "[-": "<span class='removed'>",
        "-]": "</span>",
        "{+": "<span class='added'>",
        "+}": "</span>"
    }

    # For each line, replace and write out
    for line in diff:
        for k, v in replacements.items():
            line = line.replace(k, v)

        if line:
            if line[0] == "-":
                line = "<span class='removed'>%s</span><br>" % line[1:]

            if line[0] == "+":
                line = "<span class='added'>%s</span><br>" % line[1:]
        outlines.append(line.strip())

    return outlines


def generate_diff_markdown(diff, word_diff=False):

    outlines = diff_replace(diff)

    text = "\n".join(outlines)
    markdown_text = markdown2.markdown(text)

    # Condition code to include proper html escapes
    escapes = {
        u"\u2026": "&hellip;",
        u"\u011b": "&#283;",
        u"\xe0":   "&agrave;",
        u"\xf3":   "&oacute;",
        u"\u2012": "&#8210;",
        u"\u2013": "&ndash;",
        u"\u2018": "'"
    }
    for k, v in escapes.items():
        html = markdown_text.replace(k, v)

    # Finally, write out the results. We're done!
    return markdown_text
