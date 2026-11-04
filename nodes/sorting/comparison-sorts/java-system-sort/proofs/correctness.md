---
title: Both paths of the Java system sort sort the array, and the object path is stable
proves: [correctness, termination]
status: full
---

Line L1 picks one of two paths. We prove each path correct. In both, each change of $A$ is an exchange, a move inside a range, or a merge of two neighbouring ranges, so $A$ always holds a permutation of the input.

## The primitive path

**Claim P.** SORT-PRIMITIVE$(A, lo, hi, depth)$ stops and leaves $A[lo \ldots hi]$ sorted, and it changes no item outside the range.

*Proof.* By induction on $hi - lo$, and for equal lengths on $depth$. If $hi - lo < 47$, line L3 calls insertion sort, which is correct. If $depth = 0$, line L4 calls heapsort, which is correct. Otherwise $hi - lo \ge 47$.

*Line L5.* The five sample indices $e_3 - 2s, \ldots, e_3 + 2s$ with $s = \lfloor (hi - lo + 1)/7 \rfloor \ge 6$ and $e_3 = \lfloor (lo + hi)/2 \rfloor$ lie strictly between $lo$ and $hi$ and are distinct. Sorting them by insertion and exchanging the second with $A[lo]$ and the fourth with $A[hi]$ gives $p = A[lo] \le q = A[hi]$.

*Line L6.* The loop keeps the invariant

> **(D)** $A[lo+1 \ldots lt-1] < p$, $\; p \le A[lt \ldots k-1] \le q$, $\; A[gt+1 \ldots hi-1] > q$, $\; lo + 1 \le lt \le k \le gt + 1 \le hi$.

It holds at the start with $lt = k = lo + 1$ and $gt = hi - 1$, since the three parts are empty. Consider one step with $k \le gt$ and $x = A[k]$.

- If $x < p$, exchanging $A[k]$ and $A[lt]$ moves $x$ to the end of the left part, and the item at $lt$, which was in the middle part or was $x$ itself when $lt = k$, moves to $k$. Then $lt$ and $k$ both grow by 1, and (D) holds.
- If $x > q$, the inner loop moves $gt$ left past the items greater than $q$, but not below $k$. These items join the right part. If it stops with $k < gt$, then $A[gt] \le q$, and the exchange puts $x$ at $gt$, at the left end of the right part, and $A[gt]$ at $k$. If it stops with $k = gt$, the exchange does nothing and $x$ at $gt$ joins the right part. In both cases $gt$ drops by 1. The new item at $k$ is at most $q$, or $k > gt$. If it is less than $p$, it goes to the left part as in the first case. Then $k$ grows by 1, and (D) holds.
- Otherwise $p \le x \le q$, and $k$ grows by 1, which adds $x$ to the middle part.

Each step raises $k$ or lowers $gt$ (in fact raises $k$), so the loop stops with $k = gt + 1$.

*Line L7.* At the end, $lt - 1$ is the last index of the left part, or $lo$ if it is empty, and $gt + 1$ is the first index of the right part, or $hi$. After $lt \leftarrow lt - 1$ and $gt \leftarrow gt + 1$, exchanging $A[lo]$ with $A[lt]$ puts $p$ at $lt$ and an item less than $p$, or $p$ itself, at $lo$. Exchanging $A[hi]$ with $A[gt]$ puts $q$ at $gt$ and an item greater than $q$, or $q$ itself, at $hi$. Now $A[lo \ldots lt-1] < p = A[lt] \le A[lt+1 \ldots gt-1] \le q = A[gt] < A[gt+1 \ldots hi]$, with $lt < gt$.

*Lines L8 and L9.* The three ranges are strictly shorter than $A[lo \ldots hi]$, because each misses at least the two pivots. By the induction hypothesis the calls stop and sort them. If $p = q$, every item of the middle part is from $p$ to $q$, so equal to $p$, and the part is sorted without a call. Each item of a part is at most each item of the parts to its right, by the inequalities above, so $A[lo \ldots hi]$ is sorted. $\square$

Line L1 calls SORT-PRIMITIVE on the whole array, so by Claim P the array is sorted.

## The object path

**Invariant (R).** At the start of each step of the loop of line L10, with $i$ the start of the next run, the stack holds runs $[s_1, \ell_1], \ldots, [s_m, \ell_m]$ with $s_1 = 0$, $s_{t+1} = s_t + \ell_t$ and $s_m + \ell_m = i$, each $A[s_t \ldots s_t + \ell_t - 1]$ is sorted, and the items of each run are the items that the input held at the same positions, in an order that keeps equal items in their input order.

*Initialization.* The stack is empty and $i = 0$.

*Line L10.* The run at $i$ is ascending, or strictly descending and then reversed. A reversal of a strictly descending sequence gives an ascending sequence, and it has no equal items, so stability is kept. Binary insertion of each later item $x$ finds the first index whose item is greater than $x$, so $x$ goes after all items equal to it, which came before it in the input, and the prefix stays sorted. So the new run is sorted and stable, and it starts at $i$.

*Lines L11 and L12.* The push keeps (R). A merge of the runs $k$ and $k + 1$ takes two neighbouring sorted runs and writes their items into the same positions in sorted order. It takes the item of the left run when the two items are equal, so it keeps equal items in the order of the runs, which is their input order by (R). The two runs become one run with the start of the first and the sum of the lengths, so (R) holds.

**Termination.** Each step of the loop of line L10 adds a run of length at least 1, so $i$ grows, and the loop stops when $i = n$. Each merge removes one run from the stack, so the loops of line L11 and line L12 stop.

**Correctness at the end.** Line L12 merges until one run is left. By (R), it starts at 0, has length $n$, is sorted, and keeps equal items in their input order. So the array is sorted, and the sort is stable. If $n = 0$ the stack stays empty and there is nothing to sort. $\blacksquare$

The stack invariant of line L11 is not needed for correctness, only for the bound of $O(\log n)$ runs on the stack and for the cost of $O(n \log n)$.
