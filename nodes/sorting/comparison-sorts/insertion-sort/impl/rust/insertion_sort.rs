// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

//! Insertion sort.

/// Sorts `a` in place, in non-decreasing order. The sort is stable.
pub fn insertion_sort<T: Ord + Clone>(a: &mut [T]) {
    for i in 1..a.len() {
        // @line L1
        let key = a[i].clone(); // @line L2
        let mut j = i; // @line L3: j is one more than in the pseudocode, so it stays unsigned
        while j > 0 && a[j - 1] > key {
            // @line L4
            a[j] = a[j - 1].clone(); // @line L5
            j -= 1; // @line L6
        }
        a[j] = key; // @line L7
    }
}
