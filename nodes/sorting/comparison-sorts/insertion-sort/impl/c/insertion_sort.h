// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

#ifndef INSERTION_SORT_H
#define INSERTION_SORT_H

#include <stddef.h>
#include <stdint.h>

// insertion_sort sorts a[0..n-1] in place, in non-decreasing order. The sort is stable.
void insertion_sort(int64_t *a, size_t n);

#endif
