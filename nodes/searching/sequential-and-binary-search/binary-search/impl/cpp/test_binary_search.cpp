// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

#include <algorithm>
#include <cassert>
#include <iostream>
#include <random>
#include <string>
#include <vector>

#include "binary_search.hpp"

int main() {
    const std::vector<int> a{2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
    std::span<const int> s(a);
    assert(algo::binary_search(s, 23) == 5);
    assert(algo::binary_search(s, 2) == 0);
    assert(algo::binary_search(s, 91) == 9);
    assert(!algo::binary_search(s, 30));
    assert(!algo::binary_search(s, 1));
    assert(!algo::binary_search(s, 100));
    assert(!algo::binary_search(std::span<const int>{}, 1));

    const std::vector<std::string> w{"ant", "bee", "cat"};
    assert(algo::binary_search(std::span<const std::string>(w), std::string("bee")) == 1);

    std::mt19937 rng(2150);
    for (int t = 0; t < 2000; t++) {
        std::vector<int> b(rng() % 31);
        for (auto& v : b) v = static_cast<int>(rng() % 41) - 20;
        std::ranges::sort(b);
        int x = static_cast<int>(rng() % 51) - 25;
        auto got = algo::binary_search(std::span<const int>(b), x);
        if (std::ranges::find(b, x) != b.end()) {
            assert(got && b[*got] == x);
        } else {
            assert(!got);
        }
    }
    std::cout << "ok\n";
}
