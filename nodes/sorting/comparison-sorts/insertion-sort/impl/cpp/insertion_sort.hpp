// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

#pragma once

#include <cstddef>
#include <span>
#include <utility>

namespace algo {

// insertion_sort sorts a in place, in non-decreasing order. The sort is stable.
template <typename T>
void insertion_sort(std::span<T> a) {
    for (std::size_t i = 1; i < a.size(); i++) {   // @line L1
        T key = std::move(a[i]);                    // @line L2
        std::size_t j = i;                          // @line L3: j is one more than in the pseudocode
        while (j > 0 && key < a[j - 1]) {           // @line L4
            a[j] = std::move(a[j - 1]);             // @line L5
            j--;                                    // @line L6
        }
        a[j] = std::move(key);                      // @line L7
    }
}

}  // namespace algo
