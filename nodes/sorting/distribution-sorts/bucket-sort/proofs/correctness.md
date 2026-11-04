---
title: Bucket sort sorts keys in [0, 1) and is stable
proves: [correctness, stability]
status: full
---

Let $A[0 \ldots n-1]$ hold keys with $0 \le A[i] < 1$, and let $\beta(x) = \lfloor n x \rfloor$. For each key, $0 \le n x < n$, so $\beta(x) \in \{0, \ldots, n-1\}$ and line L3 appends to an existing list.

**Lemma 1 (the buckets are ordered).** If $\beta(x) < \beta(y)$, then $x < y$. Equivalently, if $x \le y$ then $\beta(x) \le \beta(y)$.

*Proof.* If $x \le y$, then $n x \le n y$, and the floor function is non-decreasing, so $\beta(x) \le \beta(y)$. The first form is the contrapositive. $\square$

**Lemma 2 (the scatter).** After the loop of lines L2 and L3, each index $i$ appears in exactly one list, the list $B[\beta(A[i])]$, and each list holds its keys in increasing order of input index.

*Proof.* By induction on the loop: before step $i$, the keys $A[0], \ldots, A[i-1]$ are each in their own bucket list, in order of index. Step $i$ appends $A[i]$ to the end of the list $B[\beta(A[i])]$ and changes no other list. So the claim holds before step $i + 1$, and for $i = n$ it is the lemma. $\square$

**Theorem.** BUCKET-SORT returns the keys of $A$ in non-decreasing order. If INSERTION-SORT is stable, keys that are equal appear in their input order.

*Proof.* After line L5, each list $B[j]$ holds the same keys as before, in non-decreasing order, by the correctness of insertion sort. Let $C$ be the concatenation of line L6, and let $p < q$ be positions in $C$ with keys $x$ at $p$ and $y$ at $q$.

1. If both come from the same list $B[j]$, then $x \le y$, because $B[j]$ is sorted.
2. If they come from different lists $B[j]$ and $B[j']$, then $j < j'$, because the concatenation puts the lists in order of their index. So $\beta(x) < \beta(y)$, and Lemma 1 gives $x < y$.

So $C$ is non-decreasing. By Lemma 2 it holds each key of $A$ exactly once.

For stability, let $A[i] = A[i']$ with $i < i'$. By Lemma 1 (with $x \le y$ and $y \le x$) both keys have the same bucket. By Lemma 2, $A[i]$ is in front of $A[i']$ in that list after line L3. A stable insertion sort keeps equal keys in their order, so $A[i]$ is still in front after line L5, and also in $C$. $\blacksquare$
