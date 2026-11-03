// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

/** Returns an index i with a[i] === x, or -1 when x is not in a. The array must be sorted. */
export function binarySearch<T>(a: readonly T[], x: T): number {
  let lo = 0, hi = a.length; // @line L1
  while (lo < hi) { // @line L2
    const mid = lo + ((hi - lo) >> 1); // @line L3
    if (a[mid] < x) { // @line L4
      lo = mid + 1; // @line L5
    } else if (a[mid] > x) { // @line L6
      hi = mid; // @line L7
    } else {
      return mid; // @line L8
    }
  }
  return -1; // @line L9
}
