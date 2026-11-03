// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

package mergesort

import (
	"math/rand/v2"
	"slices"
	"testing"
)

func TestExample(t *testing.T) {
	a := []int{38, 27, 43, 3, 9, 82, 10}
	Sort(a)
	if !slices.Equal(a, []int{3, 9, 10, 27, 38, 43, 82}) {
		t.Errorf("got %v", a)
	}
}

func TestEdges(t *testing.T) {
	for _, a := range [][]int{{}, {1}, {2, 1}, {1, 1, 1}, {3, 2, 1}, {1, 2, 3}} {
		b := slices.Clone(a)
		Sort(b)
		if !slices.IsSorted(b) {
			t.Errorf("Sort(%v) = %v", a, b)
		}
	}
}

func TestRandom(t *testing.T) {
	r := rand.New(rand.NewPCG(2150, 0))
	for range 500 {
		a := make([]int, r.IntN(61))
		for i := range a {
			a[i] = r.IntN(101) - 50
		}
		b, want := slices.Clone(a), slices.Clone(a)
		Sort(b)
		slices.Sort(want)
		if !slices.Equal(b, want) {
			t.Fatalf("Sort(%v) = %v", a, b)
		}
	}
}
