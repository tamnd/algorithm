// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

//! Binary search in a sorted slice.

use std::cmp::Ordering;

/// Returns an index `i` with `a[i] == *x`, or `None` when `x` is not in `a`. The slice must be sorted.
pub fn binary_search<T: Ord>(a: &[T], x: &T) -> Option<usize> {
    let (mut lo, mut hi) = (0, a.len()); // @line L1
    while lo < hi {
        // @line L2
        let mid = lo + (hi - lo) / 2; // @line L3
        match a[mid].cmp(x) {
            Ordering::Less => lo = mid + 1,  // @line L4 L5
            Ordering::Greater => hi = mid,   // @line L6 L7
            Ordering::Equal => return Some(mid), // @line L8
        }
    }
    None // @line L9
}
