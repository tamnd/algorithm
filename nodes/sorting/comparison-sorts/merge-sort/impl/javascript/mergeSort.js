// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

/**
 * Sorts a in place, in non-decreasing order, and returns it. The sort is stable.
 * @template T
 * @param {T[]} a
 * @returns {T[]}
 */
export function mergeSort(a) {
  sort(a, 0, a.length);
  return a;
}

function sort(a, lo, hi) {
  if (hi - lo <= 1) return; // @line L1
  const mid = lo + ((hi - lo) >> 1); // @line L2
  sort(a, lo, mid); // @line L3
  sort(a, mid, hi); // @line L4
  merge(a, lo, mid, hi); // @line L5
}

function merge(a, lo, mid, hi) {
  const b = a.slice(lo, mid); // @line L6
  let i = 0, j = mid, k = lo; // @line L7
  while (i < b.length && j < hi) { // @line L8
    if (b[i] <= a[j]) { // @line L9
      a[k] = b[i++];
    } else {
      a[k] = a[j++]; // @line L10
    }
    k++; // @line L11
  }
  while (i < b.length) { // @line L12
    a[k++] = b[i++]; // @line L13
  }
}
