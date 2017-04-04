#include <fstream>
#include "main.h"

using namespace std;

int main() {
    ifstream in(%%IN_FILE_NAME%%);
    ofstream out(%%OUT_FILE_NAME%%);
    solve(in, out);
    return 0;
}