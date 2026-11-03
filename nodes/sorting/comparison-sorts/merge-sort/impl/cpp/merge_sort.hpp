// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

#pragma once

#include <cstddef>
#include <span>
#include <utility>
#include <vector>

namespace algo {

namespace detail {

template <typename T>
void merge(std::span<T> a, std::size_t mid, std::vector<T>& b) {
    b.assign(std::make_move_iterator(a.begin()), std::make_move_iterator(a.begin() + mid));  // @line L6
    std::size_t i = 0, j = mid, k = 0;                       // @line L7
    while (i < b.size() && j < a.size()) {                   // @line L8
        if (!(a[j] < b[i])) {                                // @line L9: b[i] <= a[j], with only <
            a[k] = std::move(b[i++]);
        } else {
            a[k] = std::move(a[j++]);                        // @line L10
        }
        k++;                                                 // @line L11
    }
    while (i < b.size()) {                                   // @line L12
        a[k++] = std::move(b[i++]);                          // @line L13
    }
}

template <typename T>
void sort(std::span<T> a, std::vector<T>& b) {
    if (a.size() <= 1) return;                               // @line L1
    std::size_t mid = a.size() / 2;                          // @line L2
    sort(a.first(mid), b);                                   // @line L3
    sort(a.subspan(mid), b);                                 // @line L4
    merge(a, mid, b);                                        // @line L5
}

}  // namespace detail

// merge_sort sorts a in place, in non-decreasing order. The sort is stable.
template <typename T>
void merge_sort(std::span<T> a) {
    std::vector<T> b;
    b.reserve((a.size() + 1) / 2);
    detail::sort(a, b);
}

}  // namespace algo
