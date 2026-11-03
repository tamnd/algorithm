// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

//! Merge sort.

/// Sorts `a` in place, in non-decreasing order. The sort is stable.
pub fn merge_sort<T: Ord + Clone>(a: &mut [T]) {
    let mut buf = Vec::with_capacity(a.len().div_ceil(2));
    sort(a, &mut buf);
}

fn sort<T: Ord + Clone>(a: &mut [T], buf: &mut Vec<T>) {
    let n = a.len();
    if n <= 1 {
        // @line L1
        return;
    }
    let mid = n / 2; // @line L2
    sort(&mut a[..mid], buf); // @line L3
    sort(&mut a[mid..], buf); // @line L4
    merge(a, mid, buf); // @line L5
}

fn merge<T: Ord + Clone>(a: &mut [T], mid: usize, buf: &mut Vec<T>) {
    buf.clear();
    buf.extend_from_slice(&a[..mid]); // @line L6
    let (mut i, mut j, mut k) = (0, mid, 0); // @line L7
    while i < buf.len() && j < a.len() {
        // @line L8
        if buf[i] <= a[j] {
            // @line L9
            a[k] = buf[i].clone();
            i += 1;
        } else {
            a[k] = a[j].clone(); // @line L10
            j += 1;
        }
        k += 1; // @line L11
    }
    while i < buf.len() {
        // @line L12
        a[k] = buf[i].clone(); // @line L13
        i += 1;
        k += 1;
    }
}
