---
title: Radix exchange sort sorts non-negative integers
proves: [correctness, termination]
status: full
---

Keys are integers in $[0, 2^w)$. For $-1 \le b < w$, write $\mathrm{top}(x, b) = \lfloor x / 2^{b+1} \rfloor$, the bits of $x$ above bit $b$. A task $(lo, hi, b)$ is *valid* if all keys of $A[lo \ldots hi - 1]$ have the same value of $\mathrm{top}(\cdot, b)$.

**Fact 1.** If $\mathrm{top}(x, b) = \mathrm{top}(y, b)$ and $\mathrm{bit}(x, b) < \mathrm{bit}(y, b)$, then $x < y$. If $\mathrm{top}(x, -1) = \mathrm{top}(y, -1)$, then $x = y$.

*Proof.* Write $t = \mathrm{top}(x, b)$. Then $x = t \cdot 2^{b+1} + 0 \cdot 2^b + r$ and $y = t \cdot 2^{b+1} + 1 \cdot 2^b + r'$ with $0 \le r, r' < 2^b$, so $x < t \cdot 2^{b+1} + 2^b \le y$. For $b = -1$, $\mathrm{top}(x, -1) = x$. $\square$

**Lemma (partition).** Let lines L5 to L9 run on a range $[lo, hi)$ with $hi - lo \ge 2$. They end, permute the range, and at the end every key of $A[lo \ldots i - 1]$ has bit $b$ equal to 0 and every key of $A[i \ldots hi - 1]$ has bit $b$ equal to 1.

*Proof.* At each test of line L6 the following holds: all keys of $A[lo \ldots i-1]$ have bit 0, all keys of $A[j+1 \ldots hi-1]$ have bit 1, and $lo \le i \le j + 1 \le hi$. This is true at the start, with both parts empty. Line L7 moves $i$ only past keys with bit 0, and line L8 moves $j$ only past keys with bit 1, and both keep $i \le j + 1$, because they stop when $i > j$. If line L9 swaps, then $i < j$, and by the stops of L7 and L8, $A[i]$ has bit 1 and $A[j]$ has bit 0; after the swap $A[i]$ has bit 0 and $A[j]$ has bit 1, so both parts grow by one and $i \le j + 1$ still holds. Each turn of the loop of line L6 either moves $i$ or $j$ in L7 or L8, or swaps and moves both, because if neither L7 nor L8 moves, then $i \le j$ and the conditions of both scans fail, which means $A[i]$ has bit 1 and $A[j]$ has bit 0, so $i \ne j$ and line L9 runs. So $j - i$ decreases in each turn, and the loop ends with $i = j + 1$. Then the two parts cover the range. $\square$

**Correctness.** Call the state *good* if the tasks on $S$ have disjoint ranges and are valid, any two indices $p < q$ that are not in the same task have $A[p] \le A[q]$, and $A$ holds the input keys. The first task $(0, n, w - 1)$ is valid, because $\mathrm{top}(x, w - 1) = 0$ for all keys, so the state is good at the start.

Pop a task $(lo, hi, b)$. If $hi - lo \le 1$, there is no pair inside it. If $b < 0$, all its keys are equal by Fact 1, so all pairs inside it are in order. In both cases dropping the task keeps the state good. Otherwise the lemma splits the range into a part with bit $b = 0$ and a part with bit $b = 1$. Both parts agree on the bits above $b$ and on bit $b$, so they are valid at $b - 1$. A key of the first part and a key of the second part are in order by Fact 1. Pairs with one index outside the range keep their relation, because the range holds the same keys. So the state stays good after line L10.

**Termination.** Each task pushed by line L10 has a bit index one lower than the popped task, and tasks with $b < 0$ push nothing. So each task has $b \ge -1$, and the tasks form a binary tree of height at most $w + 1$. The tree is finite, so the loop ends.

**Result.** When $S$ is empty, every pair $p < q$ has $A[p] \le A[q]$, so $A$ is sorted, and it holds the input keys. $\blacksquare$
