#include "prelude.h"
#include "main.h"
#include "rand.h"
#include "test_util.h"

const int TL = 3;

Random rnd;

void checker(istream& in, istream& out, istream& ans) {
    testutil::compareStreams(out, ans);
}

%%SAMPLE_REGION%%

namespace stress_test {
    const int ITERS = 0;

    void solve(istream &in, ostream& out) {
    }

    void getInput(ostream& out) {
    }
}

TEST(%%PROBLEM_NAME%%, stress) {
    FOR(iter, stress_test::ITERS) {
        ostringstream out_for_input;
        stress_test::getInput(out_for_input);
        const string input = out_for_input.str();
        istringstream sin(input);
        ostringstream out;
        stress_test::solve(sin, out);
        const string output = out.str();
        testutil::testSolutionGcj<TL>(solve, checker, input, output);
    }
}


