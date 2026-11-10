---
title: P-STRASSEN has work Θ(n^(lg 7)) and span Θ(log^2 n), with exact counts
proves: [time.worst, depth.worst, space.extra]
status: full
---

**The cost model.** An add, a subtract or a product of two entries costs 1. A group of $k$ tasks run in parallel, a spawn group or a [parallel loop](/parallel-for/) over $k$ items, adds $k - 1$ to the work and $\lceil \lg k \rceil$ to the span. Taking a block of a matrix is index arithmetic and costs nothing. Let $n = 2^L$, $m = n/2$, and $\lg = \log_2$. This is the model that the implementation counts in, and the tests check the counts below with equality.

**Lemma 1 (a block sum).** Two nested parallel loops over an $m \times m$ block with a body of $c$ unit steps have work $(c + 1)m^2 - 1$ and span $2\lceil \lg m \rceil + c$.

*Proof.* The inner loop has work $mc + m - 1$ and span $\lceil \lg m \rceil + c$. The outer loop runs $m$ of them, with work $m(mc + m - 1) + m - 1 = (c+1)m^2 - 1$ and span $\lceil \lg m \rceil$ more. $\blacksquare$

**Theorem 2 (the recurrences).** For $n \ge 2$,

$$W(n) = 7W(n/2) + 8n^2 + 4, \qquad S(n) = S(n/2) + 4L + 9,$$

with $W(1) = S(1) = 1$.

*Proof.* Line L2 costs 1 for $n = 1$. For $n \ge 2$ the three steps run in sequence.

- Line L4 is a group of ten sums with $c = 1$. By Lemma 1 each has work $2m^2 - 1$ and span $2\lceil \lg m \rceil + 1$, and the group adds $9$ to the work and $\lceil \lg 10 \rceil = 4$ to the span: work $20m^2 - 1$, span $2(L - 1) + 5$.
- Line L5 is a group of seven calls: work $7W(m) + 6$ and span $S(m) + \lceil \lg 7 \rceil = S(m) + 3$.
- Line L7 is a group of four block sums, with $c = 3, 1, 1, 3$ steps per entry. By Lemma 1 their works add up to $(4 + 2 + 2 + 4)m^2 - 4 = 12m^2 - 4$, the largest span is $2\lceil \lg m \rceil + 3$, and the group adds 3 to the work and 2 to the span: work $12m^2 - 1$, span $2(L - 1) + 5$.

So $W(n) = 7W(m) + 6 + 32m^2 - 2 = 7W(n/2) + 8n^2 + 4$, and $S(n) = S(m) + 3 + 2\big(2(L - 1) + 5\big) = S(n/2) + 4L + 9$. $\blacksquare$

**Theorem 3 (closed forms).** For $n = 2^L$,

$$W(n) = \frac{37 \cdot 7^L - 32n^2 - 2}{3} = \frac{37 n^{\lg 7} - 32 n^2 - 2}{3}, \qquad S(n) = 2L^2 + 11L + 1.$$

So $W = \Theta(n^{\lg 7})$, $S = \Theta(\log^2 n)$, and the parallelism is $\Theta(n^{\lg 7} / \log^2 n)$.

*Proof.* For $L = 0$ both formulas give 1. For the span, unroll: $S(2^L) = 1 + \sum_{\ell = 1}^{L} (4\ell + 9) = 1 + 2L(L + 1) + 9L = 2L^2 + 11L + 1$. For the work, put the formula for $L - 1$ into the recurrence. With $(n/2)^2 = n^2/4$ and $7^L = 7 \cdot 7^{L - 1}$,

$$7 \cdot \frac{37 \cdot 7^{L-1} - 8n^2 - 2}{3} + 8n^2 + 4 = \frac{37 \cdot 7^L - 56n^2 - 14 + 24n^2 + 12}{3} = \frac{37 \cdot 7^L - 32n^2 - 2}{3}.$$

Since $7^L = n^{\lg 7}$ and $n^2 = o(n^{\lg 7})$, the work is $\Theta(n^{\lg 7})$; the leading constant is $37/3 \approx 12.3$. The span is a quadratic in $L = \lg n$. These are exact counts, so the bounds hold for every input, not only in the worst case. $\blacksquare$

The same result follows from the [master theorem](/master-theorem/): $W(n) = 7W(n/2) + \Theta(n^2)$ is its first case, since $n^2 = O(n^{\lg 7 - \epsilon})$, and $S(n) = S(n/2) + \Theta(\log n)$ is the extended second case with $a = 1$, $b = 2$, which gives $\Theta(\log^2 n)$.

**Theorem 4 (space).** A run on one processor holds at most $\tfrac{17}{3} n^2$ entries of temporary matrices at a time, which is $\Theta(n^2)$.

*Proof.* A call of size $n \ge 2$ allocates the ten sums and the seven products, each with $(n/2)^2$ entries, which is $\tfrac{17}{4}n^2$, and holds them until it returns. On one processor the calls of line L5 run one at a time, so at most one call of each size is active, and the total is at most $\tfrac{17}{4}(n^2 + n^2/4 + n^2/16 + \cdots) < \tfrac{17}{4} \cdot \tfrac43 n^2 = \tfrac{17}{3}n^2$. $\blacksquare$
