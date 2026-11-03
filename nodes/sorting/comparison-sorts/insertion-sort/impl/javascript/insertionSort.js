// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

/**
 * Sorts a in place, in non-decreasing order, and returns it. The sort is stable.
 * @template T
 * @param {T[]} a
 * @returns {T[]}
 */
export function insertionSort(a) {
  for (let i = 1; i < a.length; i++) { // @line L1
    const key = a[i]; // @line L2
    let j = i - 1; // @line L3
    while (j >= 0 && a[j] > key) { // @line L4
      a[j + 1] = a[j]; // @line L5
      j--; // @line L6
    }
    a[j + 1] = key; // @line L7
  }
  return a;
}
