---
title: Shell sort sorts the array and keeps its items
proves: [correctness]
status: full
---

For a gap $h \ge 1$, the *chain* of a residue $r$ with $0 \le r < h$ is the list of the items at the indices $r, r + h, r + 2h, \ldots$ that are less than $n$. The array is *$h$-sorted* when each chain is sorted.

**Lemma (one pass).** One step of the loop of line L1, with the gap $h$, permutes the items of each chain among the indices of that chain, and after it the array is $h$-sorted.

*Proof.* Lines L3 to L8 only read and write the indices $i, i - h, i - 2h, \ldots$, which are all in the chain of $i \bmod h$. So the pass works on each chain apart from the others, and it does not move an item to another chain. For one chain, list its indices as $c_0 < c_1 < \cdots < c_{t-1}$. The step of line L2 for $i = c_s$ is the step of [insertion sort](/insertion-sort/) for position $s$ of this chain: line L5 compares with $A[c_{s-1}], A[c_{s-2}], \ldots$, line L6 shifts each larger item one place up in the chain, and line L8 writes the key into the gap that is left. We use this invariant, before the step for $i = c_s$:

> The items at $c_0, \ldots, c_{s-1}$ are the items that were there at the start of the pass, in sorted order.

It holds for $s = 1$, because one item is sorted. Assume it before the step for $c_s$. The loop of line L5 stops at the first index $c_q$, going down from $c_s$, with $q = 0$ or $A[c_{q-1}] \le key$. Each of $A[c_q], \ldots, A[c_{s-1}]$ is larger than $key$, and each moves one place up in the chain. Then line L8 puts $key$ at $c_q$. The items at $c_0, \ldots, c_{q-1}$ are at most $key$ and sorted, the items at $c_{q+1}, \ldots, c_s$ are larger than $key$ and sorted, so $c_0, \ldots, c_s$ hold the old items plus $key$ in sorted order. The steps for indices in other chains do not touch this chain. At the end of the pass, $s = t$, so each chain is sorted. The step for each $i$ ends because $j$ falls by $h \ge 1$ in each turn of line L5 and the loop stops at $j < h$. $\square$

**Theorem.** If $H$ is a finite list of positive gaps whose last gap is $1$, then SHELL-SORT$(A, H)$ stops, and after it $A$ holds the same items, in non-decreasing order.

*Proof.* Each line moves items only by the shift of line L6 and the write of line L8, and by the lemma each pass permutes the items of each chain. So the multiset of the items does not change. There are finitely many passes, and each pass has $n - h$ steps that each end, so the algorithm stops. The last pass has $h = 1$. With $h = 1$ there is one chain, the full array, so by the lemma the array is sorted after this pass. $\blacksquare$

The earlier passes are not needed for correctness. They only make the last pass fast, because they remove most of the [inversions](/inversion/) before it.
