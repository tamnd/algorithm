// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

// Package mergesort sorts a slice by merging.
package mergesort

import "cmp"

// Sort sorts a in place, in non-decreasing order. The sort is stable.
func Sort[T cmp.Ordered](a []T) {
	buf := make([]T, (len(a)+1)/2)
	sort(a, 0, len(a), buf)
}

func sort[T cmp.Ordered](a []T, lo, hi int, buf []T) {
	if hi-lo <= 1 { // @line L1
		return
	}
	mid := lo + (hi-lo)/2 // @line L2
	sort(a, lo, mid, buf)  // @line L3
	sort(a, mid, hi, buf)  // @line L4
	merge(a, lo, mid, hi, buf) // @line L5
}

func merge[T cmp.Ordered](a []T, lo, mid, hi int, buf []T) {
	b := buf[:mid-lo]
	copy(b, a[lo:mid])     // @line L6
	i, j, k := 0, mid, lo  // @line L7
	for i < len(b) && j < hi { // @line L8
		if b[i] <= a[j] { // @line L9
			a[k] = b[i]
			i++
		} else {
			a[k] = a[j] // @line L10
			j++
		}
		k++ // @line L11
	}
	for i < len(b) { // @line L12
		a[k] = b[i] // @line L13
		i++
		k++
	}
}
