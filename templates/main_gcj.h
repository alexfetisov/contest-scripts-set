#pragma once

#include "prelude.h"
#include "io.h"

void solveTest(istream& in, ostream& out) {

}

void inputData(istream& in) {

}

void solve(istream& in, ostream& out, const int test_id = -1) {
    int test = next<int>(in);
    FOR(t, test) {
        inputData(in);
        if (t == test_id || test_id == -1) {
            out << "Case #" << t << ": ";
            solveTest(in, out);
        }
    }
}