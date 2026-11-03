// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

#include <algorithm>
#include <cassert>
#include <iostream>
#include <random>
#include <string>
#include <utility>
#include <vector>

#include "merge_sort.hpp"

struct Item {
    int key;
    char tag;
    bool operator<(const Item& o) const { return key < o.key; }
};

int main() {
    std::vector<int> a{38, 27, 43, 3, 9, 82, 10};
    algo::merge_sort(std::span<int>(a));
    assert((a == std::vector<int>{3, 9, 10, 27, 38, 43, 82}));

    std::vector<Item> s{{2, 'a'}, {1, 'b'}, {2, 'c'}, {1, 'd'}, {2, 'e'}};
    algo::merge_sort(std::span<Item>(s));
    std::string tags;
    for (const auto& x : s) tags += x.tag;
    assert(tags == "bdace");

    std::mt19937 rng(2150);
    for (int t = 0; t < 500; t++) {
        std::vector<int> b(rng() % 61);
        for (auto& v : b) v = static_cast<int>(rng() % 101) - 50;
        auto want = b;
        algo::merge_sort(std::span<int>(b));
        std::ranges::sort(want);
        assert(b == want);
    }
    std::cout << "ok\n";
}
