---
title: Two-pointer pair search finds a pair with sum t if and only if one exists
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The array $A[0 \ldots n-1]$ is sorted, $A[0] \le \cdots \le A[n-1]$. A *solution* is a pair of indices $(i, j)$ with $0 \le i < j \le n-1$ and $A[i] + A[j] = t$. Write $\mathrm{Sol}(a, b)$ for the set of solutions $(i, j)$ with $a \le i < j \le b$.

**Claim.** PAIR-SEARCH$(A, t)$ stops after at most $\max(n-1, 0)$ iterations of the loop of line L2. It returns a solution if a solution exists, and NIL otherwise.

*Proof.* We use this invariant, checked each time the test of line L2 is about to run:

> **(P)** $0 \le lo$, $hi \le n - 1$, $lo \le hi + 1$, and if $\mathrm{Sol}(0, n-1) \ne \emptyset$ then $\mathrm{Sol}(lo, hi) \ne \emptyset$.

*Initialization.* Line L1 sets $lo = 0$ and $hi = n - 1$. Then $lo \le hi + 1$ because $n \ge 0$, and $\mathrm{Sol}(lo, hi) = \mathrm{Sol}(0, n-1)$, so the last part holds.

*Maintenance.* Assume (P) and $lo < hi$. Line L3 sets $s = A[lo] + A[hi]$; both indices are in $[0, n-1]$ by (P). If $s = t$, line L4 returns $(lo, hi)$, which is a solution because $lo < hi$. Otherwise there are two cases.

- *Case $s < t$ (line L5).* Take any $(lo, j)$ with $lo < j \le hi$. Because $A$ is sorted and $j \le hi$, $A[j] \le A[hi]$, so $A[lo] + A[j] \le A[lo] + A[hi] = s < t$. So no solution in $\mathrm{Sol}(lo, hi)$ has first index $lo$, and $\mathrm{Sol}(lo, hi) = \mathrm{Sol}(lo + 1, hi)$. Line L5 sets $lo$ to $lo + 1$, so the last part of (P) still holds. The bounds hold because the new $lo$ is at most $hi$.
- *Case $s > t$ (line L6).* Take any $(i, hi)$ with $lo \le i < hi$. Because $i \ge lo$, $A[i] \ge A[lo]$, so $A[i] + A[hi] \ge A[lo] + A[hi] = s > t$. So no solution in $\mathrm{Sol}(lo, hi)$ has second index $hi$, and $\mathrm{Sol}(lo, hi) = \mathrm{Sol}(lo, hi - 1)$. Line L6 sets $hi$ to $hi - 1$, and (P) holds as before; the new $hi$ is at least $lo \ge 0$.

In both cases no solution of the old range is lost: this is the statement that a pointer move never skips an answer.

*Termination.* Let $d = hi - lo$. Each iteration that does not return runs exactly one of lines L5 and L6, and each of them decreases $d$ by exactly 1. At the start $d = n - 1$, and the loop runs only while $d \ge 1$. So there are at most $n - 1$ iterations when $n \ge 1$, and none when $n = 0$.

*Result.* If line L4 returns, the result is a solution, as shown. Otherwise the loop stops with $lo \ge hi$, so $lo = hi$ or $lo = hi + 1$ by (P). Then no pair $(i, j)$ with $lo \le i < j \le hi$ exists, and $\mathrm{Sol}(lo, hi) = \emptyset$. By the contrapositive of the last part of (P), $\mathrm{Sol}(0, n-1) = \emptyset$, so NIL is the right answer. $\blacksquare$

**Exact count on a no-answer input.** If no solution exists, line L4 never returns, so each iteration decreases $d$ by 1 from $n - 1$ to 0, and the loop runs exactly $n - 1$ times for $n \ge 1$.

**Remark on the order of solutions.** The proof shows only that *some* solution stays in the range. A specific solution can leave the range: on $A = [1, 2, 3, 4]$ with $t = 5$, the algorithm returns $(0, 3)$ and never looks at the solution $(1, 2)$. To list all solutions, use the variant of the page that skips the blocks of equal items after a match.
