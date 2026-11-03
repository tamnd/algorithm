// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

#include "insertion_sort.h"

void insertion_sort(int64_t *a, size_t n) {
    for (size_t i = 1; i < n; i++) {         // @line L1
        int64_t key = a[i];                  // @line L2
        size_t j = i;                        // @line L3: j is one more than in the pseudocode, so it stays unsigned
        while (j > 0 && a[j - 1] > key) {    // @line L4
            a[j] = a[j - 1];                 // @line L5
            j--;                             // @line L6
        }
        a[j] = key;                          // @line L7
    }
}
