---
title: Introsort sorts every input, in O(n log n) time
proves: [correctness, termination]
status: full
---

We use three facts proved on other pages. HEAPSORT$(A, lo, hi)$ ends and sorts $A[lo \ldots hi-1]$, changing nothing else. INSERTION-SORT$(A, lo, hi)$ does the same. HOARE-PARTITION$(A, p, r)$, for $r > p$, ends and returns $j$ with $p \le j < r$, after permuting $A[p \ldots r]$ so that each item of $A[p \ldots j]$ is at most each item of $A[j+1 \ldots r]$; see [Hoare partition](/hoare-partition/). Lines L11 to L15 are that procedure written with $<$ only: "until $A[j] \le x$" is "until not $x < A[j]$".

**Lemma 1.** For every range with $0 \le lo \le hi \le n$ and every $d \ge 0$, INTRO$(A, lo, hi, d)$ ends, changes only $A[lo \ldots hi-1]$, permutes it, and leaves it sorted.

*Proof.* By strong induction on $hi - lo$. Fix a call, and let $[lo_0, hi_0)$ be its first range. We claim that at the start of each pass of the loop of line L2:

(I) $[lo, hi) \subseteq [lo_0, hi_0)$; the items of $A[lo_0 \ldots hi_0-1]$ are a permutation of the original ones; $A[lo_0 \ldots lo-1]$ and $A[hi \ldots hi_0-1]$ are sorted; and each item of $A[lo_0 \ldots lo-1]$ is at most each item of $A[lo \ldots hi_0-1]$, and each item of $A[lo_0 \ldots hi-1]$ is at most each item of $A[hi \ldots hi_0-1]$.

At the first pass the two outer parts are empty, so (I) holds. Take a pass with $hi - lo > 16$ and $d > 0$. Lines L5 and L6 only exchange two items of the range. The positions $lo$, $\lfloor (lo+hi)/2 \rfloor$ and $hi - 1$ lie in the range, so $m$ does. Line L7 is called with $r = hi - 1 > lo = p$, so it returns $j$ with $lo \le j < hi - 1$, and each item of $A[lo \ldots j]$ is at most each item of $A[j+1 \ldots hi-1]$. Both parts $[lo, j+1)$ and $[j+1, hi)$ are non-empty and shorter than $hi - lo \le hi_0 - lo_0$.

In line L8, the recursive call sorts the left part by the induction hypothesis and touches nothing else. The left part now is sorted, its items are at least the items of $A[lo_0 \ldots lo-1]$ (they were in the range before), and at most the items of the right part, which were not moved. So setting $lo \leftarrow j + 1$ keeps (I). Line L9 is the same with the roles of the parts swapped. Each pass makes $hi - lo$ smaller, so the loop ends.

The loop ends in one of two ways. If $d = 0$ at line L3, HEAPSORT sorts $A[lo \ldots hi-1]$. If $hi - lo \le 16$, line L10 sorts it. Either way the middle part becomes sorted and keeps its set of items, so by (I) its items still lie between the two outer parts. Then $A[lo_0 \ldots hi_0-1]$ is the sorted left part, then the sorted middle, then the sorted right part, with each part at most the next, which is a sorted sequence. $\square$

**Theorem (correctness and termination).** INTROSORT$(A)$ ends and leaves $A$ sorted.

*Proof.* If $n \le 1$, the array is sorted and line L1 does nothing. Otherwise line L1 calls INTRO on the whole array, and Lemma 1 applies. $\square$

**Theorem (time).** INTROSORT makes $O(n \log n)$ comparisons and takes $O(n \log n)$ time.

*Proof.* Each call of INTRO receives a budget $d$ that is at most its caller's budget minus 1, and each pass of the loop lowers $d$ by 1 before it partitions. Call a partitioning step of depth $t$ one that runs with the budget $2\lfloor \lg n \rfloor - t$ after line L4. Then $0 \le 2 \lfloor \lg n \rfloor - t$, so $t \le 2 \lfloor \lg n \rfloor$. The ranges partitioned at one depth are disjoint, because a step only works inside the range left to it by the step one depth less, and the ranges of the two parts are disjoint. HOARE-PARTITION and the median of three cost $O(m)$ on $m$ items, so all the steps of one depth cost $O(n)$, and all depths cost $O(n \log n)$. The ranges given to HEAPSORT are disjoint, and with sizes $m_i$ they cost $O(\sum m_i \log m_i) = O(n \log n)$. The ranges given to INSERTION-SORT are disjoint with $m_i \le 16$, so they cost $O(\sum m_i^2) = O(16 n)$. $\blacksquare$
