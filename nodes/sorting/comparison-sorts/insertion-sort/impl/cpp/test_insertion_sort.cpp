// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

#include <algorithm>
#include <cassert>
#include <iostream>
#include <random>
#include <string>
#include <vector>

#include "insertion_sort.hpp"

int main() {
    std::vector<int> a{5, 2, 4, 6, 1, 3};
    algo::insertion_sort(std::span<int>(a));
    assert((a == std::vector<int>{1, 2, 3, 4, 5, 6}));

    std::vector<std::string> w{"pear", "fig", "apple"};
    algo::insertion_sort(std::span<std::string>(w));
    assert((w == std::vector<std::string>{"apple", "fig", "pear"}));

    std::mt19937 rng(2150);
    for (int t = 0; t < 500; t++) {
        std::vector<int> b(rng() % 41);
        for (auto& v : b) v = static_cast<int>(rng() % 101) - 50;
        auto want = b;
        algo::insertion_sort(std::span<int>(b));
        std::ranges::sort(want);
        assert(b == want);
    }
    std::cout << "ok\n";
}
