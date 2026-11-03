// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "merge_sort.h"

static int cmp(const void *p, const void *q) {
    int64_t a = *(const int64_t *)p, b = *(const int64_t *)q;
    return (a > b) - (a < b);
}

int main(void) {
    int64_t a[] = {38, 27, 43, 3, 9, 82, 10};
    const int64_t want[] = {3, 9, 10, 27, 38, 43, 82};
    assert(merge_sort(a, 7));
    assert(memcmp(a, want, sizeof a) == 0);
    assert(merge_sort(NULL, 0));

    srand(2150);
    int64_t b[60], c[60];
    for (int t = 0; t < 500; t++) {
        size_t n = (size_t)(rand() % 61);
        for (size_t i = 0; i < n; i++) b[i] = c[i] = rand() % 101 - 50;
        assert(merge_sort(b, n));
        qsort(c, n, sizeof c[0], cmp);
        assert(n == 0 || memcmp(b, c, n * sizeof b[0]) == 0);
    }
    puts("ok");
    return 0;
}
