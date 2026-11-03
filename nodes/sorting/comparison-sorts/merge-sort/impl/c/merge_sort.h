// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

#ifndef MERGE_SORT_H
#define MERGE_SORT_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// merge_sort sorts a[0..n-1] in place, in non-decreasing order. The sort is stable.
// It returns false, and does not change a, when it cannot allocate the buffer.
bool merge_sort(int64_t *a, size_t n);

#endif
