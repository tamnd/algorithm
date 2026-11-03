// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

#include "merge_sort.h"

#include <stdlib.h>
#include <string.h>

static void merge(int64_t *a, size_t lo, size_t mid, size_t hi, int64_t *b) {
    size_t m = mid - lo;
    memcpy(b, a + lo, m * sizeof *b);           // @line L6
    size_t i = 0, j = mid, k = lo;              // @line L7
    while (i < m && j < hi) {                   // @line L8
        if (b[i] <= a[j]) {                     // @line L9
            a[k] = b[i++];
        } else {
            a[k] = a[j++];                      // @line L10
        }
        k++;                                    // @line L11
    }
    while (i < m) {                             // @line L12
        a[k++] = b[i++];                        // @line L13
    }
}

static void sort(int64_t *a, size_t lo, size_t hi, int64_t *b) {
    if (hi - lo <= 1) return;                   // @line L1
    size_t mid = lo + (hi - lo) / 2;            // @line L2
    sort(a, lo, mid, b);                        // @line L3
    sort(a, mid, hi, b);                        // @line L4
    merge(a, lo, mid, hi, b);                   // @line L5
}

bool merge_sort(int64_t *a, size_t n) {
    if (n <= 1) return true;
    int64_t *b = malloc((n + 1) / 2 * sizeof *b);
    if (b == NULL) return false;
    sort(a, 0, n, b);
    free(b);
    return true;
}
