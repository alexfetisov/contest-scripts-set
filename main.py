"""
python main.py --name fb_b --gcj --tests 1
python tester.py --name fb_b --generate --gcj --test 1
"""

# TODO: move all path and settings to .ini file and put to gitignore

import click
import os
import shutil
import subprocess

MAIN_DIR = '/Users/alf/acm/alf'
TEMPLATES_DIR = '/Users/alf/contest-scripts-set/templates'
DEBUG_DIR = '/Users/alf/acm/cmake-build-debug'
RELEASE_DIR = '/Users/alf/acm/cmake-build-release'

# REGIONS
PROBLEM_NAME = "%%PROBLEM_NAME%%"
IN_FILE = "%%IN_FILE_NAME%%"
OUT_FILE = "%%OUT_FILE_NAME%%"
TESTS = "%%SAMPLE_REGION%%"
TEST_IN = "%%TEST_IN%%"
TEST_OUT = "%%TEST_OUT%%"
ID = "%%ID%%"
TEST_TYPE = "%%TEST_TYPE%%"

TEST_TEMPLATE = """
TEST(%%PROBLEM_NAME%%, sample%%ID%%) {
    string inString = testutil::trim(R"_TEST_(
%%TEST_IN%%
)_TEST_");
    string ansString = testutil::trim(R"_TEST_(
%%TEST_OUT%%
)_TEST_");
    testutil::%%TEST_TYPE%%<TL>(solve, checker, inString, ansString);
}
"""


def make_path(directory, file_name):
    return '/'.join([directory, file_name])


def replace_all_regions(line, name, tests, files, gcj=False):
    line = line.replace(PROBLEM_NAME, name)
    if files is not None:
        if files == 'io':
            line = line.replace(IN_FILE, 'input.txt')
            line = line.replace(OUT_FILE, 'output.txt')
        else:
            line = line.replace(IN_FILE, '%s.in'.format(files))
            line = line.replace(OUT_FILE, '%s.out'.format(files))

    test_type = "testSolutionGcj" if gcj else "testSolution"
    if TESTS in line:
        tests_as_str = ""
        idx = 1
        if not len(tests):
            cur_test = TEST_TEMPLATE
            cur_test = cur_test.replace(TEST_TYPE, test_type)
            cur_test = cur_test.replace(PROBLEM_NAME, name)
            cur_test = cur_test.replace(TEST_IN, "")
            cur_test = cur_test.replace(TEST_OUT, "")
            cur_test = cur_test.replace(ID, str(idx))
            tests_as_str += '\n' + cur_test + '\n'
            idx += 1
        else:
            for test_in, test_out in tests:
                cur_test = TEST_TEMPLATE
                cur_test = cur_test.replace(TEST_TYPE, test_type)
                cur_test = cur_test.replace(PROBLEM_NAME, name)
                cur_test = cur_test.replace(TEST_IN, test_in)
                cur_test = cur_test.replace(TEST_OUT, test_out)
                cur_test = cur_test.replace(ID, str(idx))
                tests_as_str += '\n' + cur_test + '\n'
                idx += 1
        return tests_as_str
    return line


def create_gcj_problem(name, path, tests, files):
    makefile = 'CMakeLists.txt'
    main_cpp = 'main_gcj.cpp'
    main_h = 'main_gcj.h'
    tests_cpp = 'tests_gcj.cpp'
    for f in [makefile, main_cpp, main_h, tests_cpp]:
        with open(make_path(TEMPLATES_DIR, f), 'r') as inf:
            with open(make_path(TEMPLATES_DIR, 'temp'), 'w') as temp:
                for line in inf:
                    temp.write(replace_all_regions(line, name, tests, files,
                                                   gcj=True))
        to = f
        if "_gcj" in to:
            to = to.replace("_gcj", "")
        shutil.move(make_path(TEMPLATES_DIR, 'temp'), make_path(path, to))


def create_simple_problem(name, path, tests, files):
    makefile = 'CMakeLists.txt'
    main_cpp = 'main.cpp'
    main_h = 'main.h'
    tests_cpp = 'tests.cpp'
    if files is not None:
        main_cpp = 'main_files.cpp'

    for f in [makefile, main_cpp, main_h, tests_cpp]:
        with open(make_path(TEMPLATES_DIR, f), 'r') as inf:
            with open(make_path(TEMPLATES_DIR, 'temp'), 'w') as temp:
                for line in inf:
                    temp.write(replace_all_regions(line, name, tests, files))
        shutil.move(make_path(TEMPLATES_DIR, 'temp'), make_path(path, f))


def update_cmake(name):
    p = subprocess.Popen(["cmake", "-DCMAKE_BUILD_TYPE=Release", "../"],
                         cwd=RELEASE_DIR)
    p.wait()

    p = subprocess.Popen(["cmake", "-DCMAKE_BUILD_TYPE=Debug", "../"],
                         cwd=DEBUG_DIR)
    p.wait()

    p = subprocess.Popen(["make", name + "_tests"], cwd=RELEASE_DIR)
    p.wait()


def prepare_problem(name, contest, tests=[], gcj=False, files=None, ):
    path = '/'.join([MAIN_DIR, contest, name])
    os.mkdir(path)
    name = '_' + name
    if not gcj:
        create_simple_problem(name, path, tests, files)
    else:
        create_gcj_problem(name, path, tests, files)
    update_cmake(name)


@click.command()
@click.option('--name', help='Name of the problem')
@click.option('--gcj', is_flag=True, help='If that is GCJ problem')
@click.option('--files', default=None, help='If problem needs files. Name of '
                                            'in/out or io if input/output')
@click.option('--url', default=None, help='If there is URL, then parse')
@click.option('--tests', default=0, help='Number of samples')
@click.option('--update', is_flag=True,
              help='If failed to compile, can compile again')
def entry_point(name, gcj, files, url, tests, update):
    if update:
        update_cmake(name)
        return
    test_values = []
    for i in xrange(tests):
        click.echo("Enter input for test #%s" % str(i))
        test_in = []
        line = raw_input("")
        while line:
            test_in.append(line)
            try:
                line = raw_input("")
            except Exception:
                break
        click.echo("Enter output for test #%s" % str(i))
        test_out = []
        line = raw_input("")
        while line:
            test_out.append(line)
            try:
                line = raw_input("")
            except Exception:
                break
        test_values.append(('\n'.join(test_in), '\n'.join(test_out)))
    prepare_problem(name, '_', test_values, gcj, files)

if __name__ == '__main__':
    entry_point()
