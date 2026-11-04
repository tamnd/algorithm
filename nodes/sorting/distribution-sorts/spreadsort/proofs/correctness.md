---
title: Spreadsort sorts its input and terminates
proves: [correctness, termination]
status: full
---

Let $f$ be the key map, with $x < y \Leftrightarrow f(x) < f(y)$. Write $g(x) = f(x)$ for short. For a task $(lo, hi)$ with $mn$ and $mx$ the least and the greatest value of $g$ on the range, write $r$ for the number of bits of $mx - mn$.

**Fact 1.** In a pass with shift $s$, the bin $\beta(x) = (g(x) - mn) \gg s$ does not decrease when $g(x)$ grows. So if $\beta(x) < \beta(y)$ then $x < y$.

*Proof.* $\lfloor t / 2^s \rfloor$ does not decrease in $t$. If $\beta(x) < \beta(y)$, then $g(x) - mn < g(y) - mn$, since otherwise $\beta(x) \ge \beta(y)$. So $g(x) < g(y)$ and $x < y$. $\square$

**Fact 2.** Each bin of the pass has a spread less than $2^s$. If $s = 0$, all keys of a bin are equal.

*Proof.* Keys of bin $j$ have $j 2^s \le g(x) - mn < (j + 1) 2^s$, so two of them differ by less than $2^s$. For $s = 0$ the difference is 0, so $g$ and therefore the keys are equal. $\square$

**Fact 3.** The bins are in range: $\beta(x) < 2^b$ for each key.

*Proof.* $g(x) - mn \le mx - mn < 2^r = 2^{b + s}$, so $\beta(x) < 2^b$. $\square$

**Invariant.** (I1) The tasks on the stack have disjoint ranges. (I2) $A$ holds the input multiset. (I3) For indices $i < j$ that are not in the same task, $A[i] \le A[j]$.

**Initialization.** The stack has the one task $(0, n)$, and each pair of indices is in it, so (I1) to (I3) hold.

**Maintenance.** Pop the task $(lo, hi)$. The pairs with one index outside $[lo, hi)$ keep their relation, because the range keeps its multiset of keys.

- If $m < M$, insertion sort puts the range in order, so the pairs inside the range now satisfy (I3).
- If $mn = mx$, all keys of the range are equal, and (I3) holds inside it.
- Otherwise, line L10 counts the bins, which are valid by Fact 3, and line L11 permutes the range so that bin $j$ fills $start[j] \ldots start[j+1] - 1$. The permutation only swaps keys, so (I2) holds. Take $i < j$ inside the range in different bins. The bin of $A[i]$ is lower, so $A[i] < A[j]$ by Fact 1. If $s = 0$, keys in the same bin are equal by Fact 2, so (I3) holds for the whole range. If $s > 0$, line L13 pushes each bin with two or more keys as a task. Its range is inside $[lo, hi)$, so (I1) holds, and pairs in the same bin are in the same new task, so (I3) is not claimed for them. A bin with one key has no pair inside it.

**Termination.** For a task, let $\rho$ be the number of bits of its spread $mx - mn$, which is at most $K$. A task pushed by line L13 comes from a pass with $s = r - b \le r - 1$, since $b \ge 1$. Its spread is less than $2^s$ by Fact 2, so its $\rho \le s \le r - 1$. So along each chain of tasks, $\rho$ drops by at least one with each pass, and a chain has at most $K + 1$ passes. Each pass pushes at most $m$ tasks, with disjoint ranges of at least two keys. So the tasks at each depth have disjoint ranges, there are at most $n/2$ of them, and the total number of pops is at most $1 + (K + 1) n / 2$. The loop ends.

**Result.** When the stack is empty, (I3) holds for all pairs of indices, and (I2) says that $A$ holds the input. So $A$ is the input in non-decreasing order. $\blacksquare$
