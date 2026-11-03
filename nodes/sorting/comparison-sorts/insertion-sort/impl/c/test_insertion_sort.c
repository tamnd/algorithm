// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "insertion_sort.h"

static int cmp(const void *p, const void *q) {
    int64_t a = *(const int64_t *)p, b = *(const int64_t *)q;
    return (a > b) - (a < b);
}

int main(void) {
    int64_t a[] = {5, 2, 4, 6, 1, 3};
    const int64_t want[] = {1, 2, 3, 4, 5, 6};
    insertion_sort(a, 6);
    assert(memcmp(a, want, sizeof a) == 0);
    insertion_sort(NULL, 0);

    srand(2150);
    int64_t b[40], c[40];
    for (int t = 0; t < 500; t++) {
        size_t n = (size_t)(rand() % 41);
        for (size_t i = 0; i < n; i++) b[i] = c[i] = rand() % 101 - 50;
        insertion_sort(b, n);
        qsort(c, n, sizeof c[0], cmp);
        assert(n == 0 || memcmp(b, c, n * sizeof b[0]) == 0);
    }
    puts("ok");
    return 0;
}
