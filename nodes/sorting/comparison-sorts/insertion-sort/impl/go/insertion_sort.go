// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

// Package insertionsort sorts a slice by insertion.
package insertionsort

import "cmp"

// Sort sorts a in place, in non-decreasing order. The sort is stable.
func Sort[T cmp.Ordered](a []T) {
	for i := 1; i < len(a); i++ { // @line L1
		key := a[i]                  // @line L2
		j := i - 1                   // @line L3
		for j >= 0 && a[j] > key {   // @line L4
			a[j+1] = a[j] // @line L5
			j--           // @line L6
		}
		a[j+1] = key // @line L7
	}
}
