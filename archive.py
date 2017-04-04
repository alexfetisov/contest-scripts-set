import click
import os
import shutil

CONTEST_DIR = '/Users/alf/cpp-contests/alf/_'
ARCHIVE_DIR = '/Users/alf/cpp-contests/alf/archive'
SOURCES = ['codeforces', 'timus', 'opencup', 'atcoder', 'gcj', 'other']


@click.command()
@click.option('--name', help='Name of the competition/problem')
@click.option('--source',
              help='If put contest under specific source. Current sources: '
                   '[codeforces, timus, opencup, atcoder, gcj, other]')
@click.option('--contest',
              is_flag=True,
              help='Was that a contest or single problem')
@click.option('--remove',
              is_flag=True,
              help='If remove the content of _ after archive')
def entry_point(name, source, contest, remove):
    if source not in SOURCES:
        raise Exception('Source is not in allowed sources')

    all_problems = os.listdir(CONTEST_DIR)
    if not len(all_problems):
        print "Nothing to archive!"
        return

    archive_prefix = '/'.join([ARCHIVE_DIR, source, name])
    if not os.path.isdir(ARCHIVE_DIR):
        os.mkdir(ARCHIVE_DIR)
    if not os.path.isdir('/'.join([ARCHIVE_DIR, source])):
        os.mkdir('/'.join([ARCHIVE_DIR, source]))

    if os.path.isdir(archive_prefix):
        raise Exception(
            'Archive already contains this problem! Chose other name')
    os.mkdir(archive_prefix)
    single_problem = (len(all_problems) == 1 and not contest)
    for problem_name in all_problems:
        if single_problem:
            problem_dir = archive_prefix
        else:
            problem_dir = '/'.join([archive_prefix, problem_name])
            os.mkdir(problem_dir)
        # We copy main.h and tests.cpp. Later we can restore or update
        # problem name in Makefile via tests info
        main_h = '/'.join([CONTEST_DIR, problem_name, 'main.h'])
        tests_cpp = '/'.join([CONTEST_DIR, problem_name, 'tests.cpp'])
        shutil.copy(main_h, problem_dir)
        try:
            shutil.copy(tests_cpp, problem_dir)
        except:
            pass
        if remove:
            shutil.rmtree('/'.join([CONTEST_DIR, problem_name]))

if __name__ == '__main__':
    entry_point()
