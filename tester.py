import subprocess

import click
import shutil

CONTEST_DIR = '/Users/alf/acm/alf/_'
ARCHIVE_DIR = '/Users/alf/acm/alf/archive'
SOURCES = ['codeforces', 'timus', 'opencup', 'atcoder', 'gcj', 'other']
MAIN_DIR = '/Users/alf/acm/alf'
SUBMIT_DIR = '/Users/alf/submit'
TEMPLATES_DIR = '/Users/alf/contest-scripts-set/templates'
DEBUG_DIR = '/Users/alf/acm/cmake-build-debug'
RELEASE_DIR = '/Users/alf/acm/cmake-build-release'
PARALLEL_COMMAND = 'parallel --results outdir --bar'

PATH_TO_EXEC_MAIN = './alf/_/{!s}/_{!s}_main'
PATH_TO_EXEC_TEST = './alf/_/{!s}/_{!s}_tests'

MAKE_MAIN = 'make _{!s}_main'
MAKE_TESTS = 'make _{!s}_tests'
MAKE_OUT = 'make _{!s}_out'


def verify_results(test_count):
    all_ok = True
    with open(RELEASE_DIR + "/out.txt", "r") as f:
        lines = f.readlines()
        cases_lines = []
        for line in lines:
            if line.startswith("Case #"):
                cases_lines.append(int(line.split(':')[0][6:]))
        if len(cases_lines) != test_count:
            print "Not all tests are presented!!!"
            all_ok = False
        for i in xrange(1, test_count + 1):
            if cases_lines[i-1] != i:
                print "Tests are not in the right order!!!"
                print "...test {!s}".format(i)
                all_ok = False
    return all_ok


def get_test_count():
    with open(RELEASE_DIR + "/in.txt", "r") as f:
        line = f.readline()
        try:
            test_count = int(line)
            return test_count
        except TypeError:
            print("Cannot read test number!!!")


def run_tests(name, test_id=None):
    """
    Build and run tests.
    If test_id is None run all tests in test file.
    If test_id is -1, runs stress test.
    Otherwise calls sample{test_id} test.
    """
    p = subprocess.Popen(MAKE_TESTS.format(name).split(' '), cwd=RELEASE_DIR)
    p.wait()
    if test_id is None:
        p = subprocess.Popen([PATH_TO_EXEC_TEST.format(name, name)],
                             cwd=RELEASE_DIR)
        p.wait()
    # TODO: finish test call for other test_id cases


@click.command()
@click.option('--name', help='Name of the problem')
@click.option('--test', default=None,
              help='if not set then all tests, or specify test mask')
@click.option('--generate',
              is_flag=True,
              help='generate output and copies it to folder')
@click.option('--main_only',
              is_flag=True,
              help='generate only main file to run')
@click.option('--gcj', is_flag=True,
              help='Executes solution against given test and moves it with code'
              'to folder')
@click.option('--input_file', default=None, help='Input file (for GCJ only)')
@click.option('--parallel', is_flag=True,
              help='If set executes tests in parallel')
def entry_point(name, test, generate, main_only, gcj, input_file, parallel):
    if generate:
        if main_only or gcj:
            command = MAKE_MAIN.format(name).split(' ')
            p = subprocess.Popen(command, cwd=RELEASE_DIR)
            p.wait()
            if main_only:
                return
        if test:
            run_tests(name)
        # Generates output now
        p = subprocess.Popen(MAKE_OUT.format(name).split(' '), cwd=RELEASE_DIR)
        p.wait()
        shutil.copyfile(CONTEST_DIR + "/" + name + "/out.cpp",
                        SUBMIT_DIR + "/out.cpp")
    elif gcj:
        # Executes gcj (we should have input_file set)
        shutil.copyfile(input_file, RELEASE_DIR + "/in.txt")
        test_count = test if test is not None else get_test_count()
        if parallel:
            # command_tokens = [
            #     PARALLEL_COMMAND, PATH_TO_EXEC_MAIN.format(name), {}, ":::",
            #     "{0.." + str(test_count - 1) + "}"
            # ]
            # command = " ".join(command_tokens)

            command = [PARALLEL_COMMAND + " ./alf/_/" +
                       name + "/_" + name + "_main {} ::: {0.." +
                       str(test_count-1) + "}"]
            p = subprocess.Popen(command, cwd=RELEASE_DIR, shell=True)
            p.wait()
            # Combine results
            with open(RELEASE_DIR + "/out.txt", "w") as out_file:
                for test_id in xrange(test_count):
                    with open("{!s}/outdir/1/{!s}/stdout".format(
                            RELEASE_DIR, str(test_id))) as f:
                        out_file.write(f.read())

            # Verify results
            if verify_results(test_count):
                # Copy results if everything is ok
                shutil.copyfile(RELEASE_DIR + "/out.txt",
                                SUBMIT_DIR + "/out.txt")
            # TODO: remove when verified
            # command2 = [PARALLEL_COMMAND + " ./alf/_/" +
            #            name + "/_" + name + "_main {} ::: {0.." +
            # str(test_count-1) + "}"]
        else:
            command = MAKE_MAIN.format(name).split(' ')
            p = subprocess.Popen(command, cwd=RELEASE_DIR)
            p.wait()
            # command = ["./alf/_/{!s}/_{!s}_main".]
            command = [" < ".join([PATH_TO_EXEC_MAIN.format(name, name),
                                   "{!s}/in.txt".format(RELEASE_DIR)])]
            p = subprocess.Popen(command, cwd=RELEASE_DIR, shell=True)
            p.wait()
            # TODO: output param here
            # if verify_results(test_count):
            #     # Copy results if everything is ok
            #     shutil.copyfile(RELEASE_DIR + "/out.txt",
            #                     SUBMIT_DIR + "/out.txt")
    elif test is not None:
        if test == "stress":
            run_tests(name, -1)
        else:
            run_tests(name, test)
    else:
        run_tests(name)


if __name__ == '__main__':
    entry_point()
