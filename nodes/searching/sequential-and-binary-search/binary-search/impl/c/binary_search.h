// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

#ifndef BINARY_SEARCH_H
#define BINARY_SEARCH_H

#include <stddef.h>
#include <stdint.h>

// binary_search returns an index i with a[i] == x, or -1 when x is not in a[0..n-1]. The array must be sorted.
ptrdiff_t binary_search(const int64_t *a, size_t n, int64_t x);

#endif
