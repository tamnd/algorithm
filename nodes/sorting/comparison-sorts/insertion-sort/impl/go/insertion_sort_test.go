// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

package insertionsort

import (
	"math/rand/v2"
	"slices"
	"testing"
)

func TestExample(t *testing.T) {
	a := []int{5, 2, 4, 6, 1, 3}
	Sort(a)
	if !slices.Equal(a, []int{1, 2, 3, 4, 5, 6}) {
		t.Errorf("got %v", a)
	}
}

func TestEdges(t *testing.T) {
	for _, a := range [][]int{{}, {1}, {2, 1}, {1, 1, 1}, {3, 2, 1}} {
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
		a := make([]int, r.IntN(41))
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
