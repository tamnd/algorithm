// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

#include "binary_search.h"

ptrdiff_t binary_search(const int64_t *a, size_t n, int64_t x) {
    size_t lo = 0, hi = n;                 // @line L1
    while (lo < hi) {                      // @line L2
        size_t mid = lo + (hi - lo) / 2;   // @line L3
        if (a[mid] < x) {                  // @line L4
            lo = mid + 1;                  // @line L5
        } else if (a[mid] > x) {           // @line L6
            hi = mid;                      // @line L7
        } else {
            return (ptrdiff_t)mid;         // @line L8
        }
    }
    return -1;                             // @line L9
}
