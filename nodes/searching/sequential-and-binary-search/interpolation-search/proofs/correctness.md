---
title: Interpolation search returns an index of x, or NIL, after at most n probes
proves: [correctness, termination]
status: full
---

Let $A[0 \ldots n-1]$ be numbers sorted in non-decreasing order, $n \ge 0$, and let $x$ be a number. We prove that INTERPOLATION-SEARCH$(A, x)$ stops after at most $n$ executions of line L4, and that it returns an index $i$ with $A[i] = x$ when $x$ occurs in $A$, and NIL otherwise.

**Invariant.** Before each test of line L2: $0 \le lo$, $hi \le n - 1$, and $A[j] \ne x$ for every $j < lo$ and every $j > hi$.

At the start $lo = 0$ and $hi = n - 1$, and the statement about $j$ is empty.

**The interpolation stays in the range.** Suppose that the loop body runs. Then $lo \le hi$ and $A[lo] \le x \le A[hi]$. If line L3 does not return, then $A[lo] \ne A[hi]$, so $A[lo] < A[hi]$ because the array is sorted and $lo \le hi$; in particular $lo < hi$. Let $t = (x - A[lo])/(A[hi] - A[lo])$. Then $0 \le t \le 1$, so $0 \le t \cdot (hi - lo) \le hi - lo$, and since $hi - lo$ is an integer, $0 \le \lfloor t (hi - lo) \rfloor \le hi - lo$. So line L4 gives $lo \le pos \le hi$, and $A[pos]$ is a valid read.

**The step keeps the invariant.** If $A[pos] < x$, then $A[j] \le A[pos] < x$ for every $j \le pos$, so no $j < pos + 1$ holds $x$, and the new $lo = pos + 1$ keeps the invariant. If $A[pos] > x$, then $A[j] \ge A[pos] > x$ for every $j \ge pos$, so the new $hi = pos - 1$ keeps it. The bounds $0 \le lo$ and $hi \le n - 1$ are kept, because $lo$ only grows and $hi$ only shrinks.

**Returns are correct.** Line L7 returns $pos$ only when $A[pos] = x$. Line L3 returns $lo$ only when $A[lo] = A[hi]$, and then $A[lo] \le x \le A[hi] = A[lo]$ gives $A[lo] = x$.

**NIL is correct.** Line L8 runs when the test of line L2 fails. If $lo > hi$, the invariant says that no index $j$ with $0 \le j < lo$ or $hi < j \le n - 1$ holds $x$, and these are all the indices. If $lo \le hi$ and $x < A[lo]$, then every $j$ in $[lo, hi]$ has $A[j] \ge A[lo] > x$; with the invariant, $x$ is not in $A$. The case $x > A[hi]$ is the same.

**Termination.** Each execution of line L4 is followed by a return or by a step that makes $hi - lo$ smaller by at least 1, since $lo \le pos \le hi$ and either $lo$ becomes $pos + 1 \ge lo + 1$ or $hi$ becomes $pos - 1 \le hi - 1$. The value $hi - lo + 1$ starts at $n$ and the loop body runs only while it is at least 1, so line L4 runs at most $n$ times. $\blacksquare$
