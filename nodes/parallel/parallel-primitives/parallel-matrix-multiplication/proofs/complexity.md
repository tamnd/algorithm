---
title: Exact work and span of the three parallel matrix products
proves: [time.worst, depth.worst]
status: full
---

**The cost model.** A multiply-add step, a product of two entries, and an add of two entries each cost 1. A group of $k \ge 1$ tasks that run in parallel, either a spawn group or a [parallel loop](/parallel-for/) over $k$ items, is run as a balanced binary tree of forks with $k$ leaves. That tree has $k - 1$ forks and depth $\lceil \lg k \rceil$, so the group adds $k - 1$ to the work and $\lceil \lg k \rceil$ to the span: its work is $k - 1$ plus the sum of the works of the tasks, and its span is $\lceil \lg k \rceil$ plus the largest span of a task. Steps in sequence add their works and their spans. The implementation counts in this model, and the tests check each closed form below with equality. Let $n = 2^L$ for the two recursive products, and $\lg = \log_2$.

**Theorem 1 (the parallel loops).** The loop product has $W = n^3 + n^2 - 1$ and $S = 2\lceil \lg n \rceil + n$. So $W = \Theta(n^3)$ and $S = \Theta(n)$.

*Proof.* The body of iteration $(i, j)$ is a sequential loop of $n$ steps, with work and span $n$. For a fixed $i$, the inner loop is a group of $n$ such bodies, with work $n \cdot n + n - 1$ and span $\lceil \lg n \rceil + n$. The outer loop is a group of $n$ inner loops, with work $n(n^2 + n - 1) + n - 1 = n^3 + n^2 - 1$ and span $\lceil \lg n \rceil + \lceil \lg n \rceil + n$. $\blacksquare$

**Lemma 2 (the add of lines L8 to L10).** The two nested parallel loops that add an $n \times n$ matrix into another have work $2n^2 - 1$ and span $2\lceil \lg n \rceil + 1$.

*Proof.* As in Theorem 1 with a body of cost 1: the inner loop has work $2n - 1$ and span $\lceil \lg n \rceil + 1$, and the outer loop has work $n(2n - 1) + n - 1 = 2n^2 - 1$ and span $2\lceil \lg n \rceil + 1$. $\blacksquare$

**Theorem 3 (with a temporary matrix).** P-MATRIX-MULTIPLY-RECURSIVE has

$$W(n) = n^3 + 2n^2(n - 1) + \frac{6(n^3 - 1)}{7}, \qquad S(n) = L^2 + 5L + 1.$$

So $W = \Theta(n^3)$, $S = \Theta(\log^2 n)$, and the parallelism is $\Theta(n^3 / \log^2 n)$.

*Proof.* For $n = 1$, line L2 costs 1, so $W(1) = S(1) = 1$, and both formulas give 1. For $n \ge 2$, the eight calls of lines L5 and L6 form one group of eight, with work $8W(n/2) + 7$ and span $3 + S(n/2)$. Then comes the add of Lemma 2. So

$$W(n) = 8W(n/2) + 2n^2 + 6, \qquad S(n) = S(n/2) + 2L + 4.$$

For the span, unroll: $S(2^L) = 1 + \sum_{\ell = 1}^{L} (2\ell + 4) = 1 + L(L + 1) + 4L = L^2 + 5L + 1$. For the work, put the formula for $n/2$ into the recurrence. The three terms give $8 (n/2)^3 = n^3$, $8 \cdot 2 (n/2)^2 (n/2 - 1) = 2n^3 - 4n^2$, and $8 \cdot 6((n/2)^3 - 1)/7 = 6(n^3 - 8)/7$. Adding $2n^2 + 6$ gives $n^3 + 2n^3 - 2n^2 + (6n^3 - 48 + 42)/7$, which is the formula for $n$. The leading terms give $W \sim (3 + 6/7)n^3$, so $W = \Theta(n^3)$, and $S = \Theta(L^2) = \Theta(\log^2 n)$. $\blacksquare$

**Theorem 4 (with no temporary matrix).** P-MATRIX-MULTIPLY-ADD has

$$W(n) = n^3 + \frac{6(n^3 - 1)}{7}, \qquad S(n) = 5n - 4.$$

So $W = \Theta(n^3)$, $S = \Theta(n)$, and the parallelism is $\Theta(n^2)$.

*Proof.* For $n = 1$, line 1 costs 1, and both formulas give 1. For $n \ge 2$, each of the two phases is a group of four calls, with work $4W(n/2) + 3$ and span $2 + S(n/2)$, and the phases run in sequence. So $W(n) = 8W(n/2) + 6$ and $S(n) = 2S(n/2) + 4$. For the span, $2(5n/2 - 4) + 4 = 5n - 4$. For the work, $8\big((n/2)^3 + 6((n/2)^3 - 1)/7\big) + 6 = n^3 + (6n^3 - 48 + 42)/7$, which is the formula for $n$. $\blacksquare$

**Remark (lower bounds).** The formulas are exact, so the $\Theta$ bounds hold for every input of size $n$, not only for the worst one: the counts do not depend on the values of the entries.

**Theorem 5 (where the temporary matrix starts to pay).** The span of Theorem 3 is less than the span of Theorem 1 exactly when $n \ge 64$.

*Proof.* With $n = 2^L$, compare $L^2 + 5L + 1$ with $2L + 2^L$, that is $L^2 + 3L + 1$ with $2^L$. For $L = 0, \ldots, 5$ the left side is $1, 5, 11, 19, 29, 41$ and the right side is $1, 2, 4, 8, 16, 32$, so the left side is not smaller. For $L = 6$ they are $55 < 64$. If $L^2 + 3L + 1 < 2^L$ and $L \ge 6$, then $(L + 1)^2 + 3(L + 1) + 1 = (L^2 + 3L + 1) + 2L + 4 < 2^L + 2^L$, because $2L + 4 < 2^L$ for $L \ge 6$. $\blacksquare$
