---
title: The auction algorithm runs in O(n^3 C + n^2) time
proves: [time.worst]
status: full
---

Let $A$ be an $n \times n$ matrix of integers with no forbidden pairs, and let $C = \max_{i,j} a_{ij} - \min_{i,j} a_{ij}$. Each arithmetic operation and comparison on the scaled benefits and prices costs $O(1)$ on the [word RAM](/word-ram/); by the argument of Claim 4 of the correctness proof every price stays between 0 and $2(n + 1)C + 2$, so prices and scaled benefits fit in $O(1)$ words when $n$ and the benefits do.

**Setup.** Lines L1 to L3 cost $O(n^2)$, for the scaled matrix, and so does finding the smallest and largest benefit.

**Number of iterations.** With no forbidden pairs, $\bar A = A$ and $\bar C = C$ in Claim 4 of the correctness proof, so the loop of line L4 runs at most $n((n + 1)C + 1) + 1 = O(n^2 C + n)$ times. For $n = 0$ it runs zero times.

**One iteration.** Lines L5 and L6 scan the $n$ entries of row $i$ and the $n$ prices twice, $O(n)$. Lines L7 to L9 and the queue operations cost $O(1)$. So an iteration costs $O(n)$.

**Line L10** checks $n$ pairs and sums $n$ benefits, $O(n)$.

**Total.** $O(n^2) + O(n^2 C + n) \cdot O(n) = O(n^3 C + n^2)$ time. The extra space is the scaled matrix, $\Theta(n^2)$, plus $O(n)$ for the prices, the two assignment arrays and the queue.

**Forbidden pairs.** The replacement entry $F$ widens the range to $\bar C = (n + 1)(h - \ell) + 1$, so the same count gives $O(n^4 C' + n^2)$ time, with $C' = h - \ell$ the range of the allowed benefits. $\blacksquare$
