// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "binary_search.h"

static int cmp(const void *p, const void *q) {
    int64_t a = *(const int64_t *)p, b = *(const int64_t *)q;
    return (a > b) - (a < b);
}

int main(void) {
    const int64_t a[] = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
    assert(binary_search(a, 10, 23) == 5);
    assert(binary_search(a, 10, 2) == 0);
    assert(binary_search(a, 10, 91) == 9);
    assert(binary_search(a, 10, 30) == -1);
    assert(binary_search(a, 10, 1) == -1);
    assert(binary_search(a, 10, 100) == -1);
    assert(binary_search(NULL, 0, 1) == -1);

    srand(2150);
    int64_t b[30];
    for (int t = 0; t < 2000; t++) {
        size_t n = (size_t)(rand() % 31);
        for (size_t i = 0; i < n; i++) b[i] = rand() % 41 - 20;
        qsort(b, n, sizeof b[0], cmp);
        int64_t x = rand() % 51 - 25;
        ptrdiff_t got = binary_search(b, n, x);
        int found = 0;
        for (size_t i = 0; i < n; i++) found |= b[i] == x;
        if (found) {
            assert(got >= 0 && (size_t)got < n && b[got] == x);
        } else {
            assert(got == -1);
        }
    }
    puts("ok");
    return 0;
}
