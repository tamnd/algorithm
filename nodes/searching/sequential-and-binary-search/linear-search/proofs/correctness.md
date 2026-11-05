---
title: Linear search returns the first index of x, or NIL when x is not in A
proves: [correctness, termination]
status: full
---

Let $A[0 \ldots n-1]$ be an array with $n \ge 0$ and let $x$ be a key. We prove that LINEAR-SEARCH$(A, x)$ stops, and that it returns the smallest index $i$ with $A[i] = x$, or NIL when there is no such index.

**Invariant.** Before the pass of the loop of line L1 with index $i$, and also when the loop ends with $i = n$, this statement holds:

$$ P(i): \quad 0 \le i \le n \text{ and } A[j] \ne x \text{ for each } j \text{ with } 0 \le j < i. $$

*Start.* The first pass has $i = 0$. The range $0 \le j < 0$ is empty, and $0 \le n$, so $P(0)$ holds. If $n = 0$ the loop does no pass, and $P(0)$ is the statement at the end.

*Step.* Assume $P(i)$ and that the pass with index $i$ runs, so $i \le n - 1$. Line L2 tests $A[i] = x$. If the test is true, the algorithm returns and the loop has no next pass. If the test is false, then $A[i] \ne x$. With $P(i)$, $A[j] \ne x$ for each $j < i + 1$, and $i + 1 \le n$. So $P(i + 1)$ holds before the next pass, or at the end of the loop when $i + 1 = n$.

**Termination.** The index $i$ starts at 0 and grows by exactly 1 in each pass that does not return. The loop has no pass with $i \ge n$. So it runs at most $n$ passes, and the algorithm stops after at most $n$ key tests.

**Result.** There are two ways to stop.

1. Line L2 returns $i$. Then $0 \le i \le n - 1$ and $A[i] = x$, so $i$ is an index of $x$. By $P(i)$, no index $j < i$ has $A[j] = x$. So $i$ is the smallest index of $x$.
2. Line L3 returns NIL. The loop ended after the pass with $i = n - 1$ or, when $n = 0$, without a pass. In both cases $P(n)$ holds: $A[j] \ne x$ for each $j$ with $0 \le j < n$. So $x$ is not in $A$ and NIL is correct.

$\blacksquare$

**The number of tests.** If $x$ first occurs at index $i$, the algorithm makes exactly $i + 1$ key tests: the passes $0, \ldots, i - 1$ fail by the minimality of $i$, and the pass $i$ succeeds. If $x$ is absent, it makes exactly $n$ key tests. These counts give the best, worst and average cases on the page.
