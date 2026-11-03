// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

#pragma once

#include <cstddef>
#include <optional>
#include <span>

namespace algo {

// binary_search returns an index i with a[i] == x, or nothing when x is not in a. The span must be sorted.
template <typename T>
std::optional<std::size_t> binary_search(std::span<const T> a, const T& x) {
    std::size_t lo = 0, hi = a.size();          // @line L1
    while (lo < hi) {                           // @line L2
        std::size_t mid = lo + (hi - lo) / 2;   // @line L3
        if (a[mid] < x) {                       // @line L4
            lo = mid + 1;                       // @line L5
        } else if (x < a[mid]) {                // @line L6
            hi = mid;                           // @line L7
        } else {
            return mid;                         // @line L8
        }
    }
    return std::nullopt;                        // @line L9
}

}  // namespace algo
