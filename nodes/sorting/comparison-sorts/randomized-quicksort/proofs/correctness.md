---
title: Randomized quicksort sorts the array on each run
proves: [correctness]
status: full
---

Fix any sequence of values returned by the random choices of line L2, each with $lo \le r < hi$ in its call. We prove that the run with these values sorts the array. Then the algorithm is correct with probability 1.

We write $S$ for the multiset of the items of $A[lo \ldots hi-1]$ at the start of a call.

**Lemma (PARTITION).** Assume $hi - lo \ge 2$. Then PARTITION$(A, lo, hi)$ returns an index $p$ with $lo \le p \le hi - 1$. After it, $A[lo \ldots hi-1]$ holds the same items, $A[p] = x$ where $x$ is the old $A[hi-1]$, each item of $A[lo \ldots p-1]$ is at most $x$, and each item of $A[p+1 \ldots hi-1]$ is larger than $x$. Items outside the range do not change.

*Proof.* This is the [Lomuto partition](/lomuto-partition/). Its loop keeps the invariant: $lo \le i \le j$, each item of $A[lo \ldots i-1]$ is at most $x$, each item of $A[i \ldots j-1]$ is larger than $x$, and $A[hi-1] = x$. It holds at the start with $i = j = lo$. A step with $A[j] > x$ grows the second part. A step with $A[j] \le x$ swaps $A[j]$ with the first item of the second part, or with itself if that part is empty, and then grows the first part. The loop ends with $j = hi - 1$, and the last swap puts $x$ at index $i$ and a larger item, if there is one, at index $hi - 1$. All moves are swaps inside the range. $\square$

**Theorem.** For each choice of the random values, after RANDOMIZED-QUICKSORT$(A, lo, hi)$ the range $A[lo \ldots hi-1]$ is sorted and holds $S$, and no item outside the range changes.

*Proof.* By strong induction on $k = hi - lo$.

*Base.* If $k \le 1$, line L1 returns, and a range of at most one item is sorted.

*Step.* Let $k \ge 2$ and assume the claim for all shorter ranges. Line L2 gives $r$ with $lo \le r < hi$, so the swap of line L3 is inside the range and keeps $S$. By the lemma, line L4 gives $p$ with $lo \le p \le hi - 1$, the items at most $x = A[p]$ in $A[lo \ldots p-1]$, and the items larger than $x$ in $A[p+1 \ldots hi-1]$. The ranges of lines L5 and L6 have lengths $p - lo$ and $hi - p - 1$, both at most $k - 1$. By the hypothesis, line L5 sorts $A[lo \ldots p-1]$ and changes nothing else; it permutes that part, so its items are still at most $x$. Line L6 does the same for $A[p+1 \ldots hi-1]$, whose items stay larger than $x$. So the range is a sorted part with items at most $x$, then $x$, then a sorted part with items larger than $x$. It is sorted, and since all moves were swaps inside the range, it holds $S$. $\blacksquare$

**Termination.** Each call on $k \ge 2$ items makes two calls on at most $k - 1$ items each, for each choice of the random values. So each run stops after at most $2n + 1$ calls.
