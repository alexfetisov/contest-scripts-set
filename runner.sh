#!/bin/bash

export CONTEST_SCRIPTS="$HOME/contest-scripts-set"

contest() {
    if [ -n $1 ]; then
        echo "preparing contest..."
        # TODO: implement
    else
        echo "usage: number of problems, prefix. Example: contest 5 cf_"
    fi
}


problem() {
    if [ -n $1 ]; then
        echo "preparing problem $1 with $2 tests"
        echo `$CONTEST_SCRIPTS/env/bin/python $CONTEST_SCRIPTS/main.py --name $1 --tests $2`
    else
        echo "usage: problem name, number of tests or gcj or empty for 0 tests. Example: problem a gcj; problem b 3; problem c"
    fi
}

test() {
    # TODO: make sure terminal in IDE has better line breaks
    # TODO: add manual instant test with adding that to testsuite
    if [ -n $1 ]; then
        echo `$CONTEST_SCRIPTS/env/bin/python $CONTEST_SCRIPTS/tester.py --name $1`
    else
        echo "usage: problem name, test number (or all if undefined)"
    fi
}

gen() {
    if [ -n $1 ]; then
        echo `$CONTEST_SCRIPTS/env/bin/python $CONTEST_SCRIPTS/tester.py --name $1 --generate`
    else
        echo "usage: problem name, test number (or all if undefined)"
    fi
}

gcj() {
    echo "preparing GCJ problem $1"
    echo `$CONTEST_SCRIPTS/env/bin/python $CONTEST_SCRIPTS/main.py --name $1 --gcj`
}

gcjt() {
    if [ -n $1 ]; then
        if [ -n $3 ]; then
            echo `$CONTEST_SCRIPTS/env/bin/python $CONTEST_SCRIPTS/tester.py --name $1 --input_file $2`
        else
            echo `$CONTEST_SCRIPTS/env/bin/python $CONTEST_SCRIPTS/tester.py --name $1 --input_file $2 --parallel`
        fi
    else
        echo "usage: problem name, input_file, n (if not parallel)" 
    fi
}

gcjg() {
    echo `$CONTEST_SCRIPTS/env/bin/python $CONTEST_SCRIPTS/tester.py --name $1 --gcj --generate`
}
