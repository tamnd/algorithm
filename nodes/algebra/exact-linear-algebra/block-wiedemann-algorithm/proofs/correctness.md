---
title: Block Wiedemann returns kernel vectors, and its generators are generators
proves: [correctness, termination]
status: full
---

Let $A$ be an $n \times n$ matrix over $\mathbb{F}_p$, $s \ge 1$ the block width, $X, Z \in \mathbb{F}_p^{n \times s}$, $Y = AZ$, $L = 2\lceil n/s \rceil + 4$ and $S_i = X^T A^i Y$ for $0 \le i < L$. Write $S(x) = \sum_{i < L} S_i x^i$, an $s \times s$ matrix of polynomials.

**Claim.** (1) The algorithm stops. (2) Every vector it returns is a nonzero $u$ with $Au = 0$; in particular, for a nonsingular $A$ it returns FAIL. (3) Every pair $(d, f)$ produced by line L5 satisfies $\sum_{j=0}^{d} S_{i+j} f_j = 0$ for $0 \le i < L - d$. (4) If a pair satisfies the stronger condition $\sum_j A^j Y f_j = 0$ and $u = \sum_{j \ge e} A^{j-e} Z f_j \ne 0$, where $e$ is the least index with $f_e \ne 0$, then lines L8 to L10 return a kernel vector.

**(1) Termination.** The loops of lines L3 and L5 have $L$ steps, M-Basis has $L$ rounds over $2s$ rows, there are at most $2s$ pairs in line L6, and the loop of line L8 has $e + 2$ steps.

**(2) Returned vectors.** Line L9 returns $u$ only after line L8 checked $u \ne 0$ and line L9 checked $Au = 0$. A nonsingular matrix has no such $u$.

**(3) The M-Basis invariant.** Let $G(x)$ be the $2s \times s$ matrix with $S(x)^T$ on top of $-I_s$, and let $P$ be the $2s \times 2s$ polynomial matrix of the method, with rows $P_i = (a_i \mid b_i)$, $a_i, b_i \in \mathbb{F}_p[x]^{1 \times s}$, and counters $\delta_i$. We show that before round $k$ (for $0 \le k \le L$):

- (I1) $P G \equiv 0 \pmod{x^k}$;
- (I2) $\deg a_i \le \delta_i$ and $\deg b_i \le \delta_i - 1$ for each $i$.

At $k = 0$, $P = I$ and $\delta = (0, \dots, 0, 1, \dots, 1)$: (I1) is empty, and row $i$ is a unit vector of degree $0$ in the part where its counter allows it. Assume (I1) and (I2) before round $k$, and let $\Delta$ be the coefficient of $x^k$ in $PG$. The rows are treated in increasing order of $\delta$. When row $i$ is reduced by a pivot row $j$, row $j$ came earlier, so $\delta_j \le \delta_i$, and $P_i - c P_j$ still satisfies (I2) with the counter $\delta_i$. The same operation applied to $\Delta$ keeps $\Delta$ equal to the coefficient of $x^k$ in the new $PG$, and it keeps (I1), since both rows satisfy it. After all rows are treated, the rows that are not pivots have zero rows in $\Delta$, so they satisfy $P_i G \equiv 0 \pmod{x^{k+1}}$. Each pivot row is multiplied by $x$ and its counter is increased by $1$, which keeps (I2). Its product with $G$ was $\equiv 0 \pmod{x^k}$ by (I1), so after the multiplication it is $\equiv 0 \pmod{x^{k+1}}$. So (I1) and (I2) hold before round $k + 1$.

At the end, (I1) with $k = L$ says $a_i S(x)^T - b_i \equiv 0 \pmod{x^L}$ for each row. Fix a row with $a_i \ne 0$, write $d = \delta_i$ and $a_i = \sum_{t \le d} \alpha_t x^t$, and set $f_j = \alpha_{d - j}^T$ for $0 \le j \le d$, as line L5 does. For $d \le t < L$, the coefficient of $x^t$ in $b_i$ is $0$ by (I2), so the coefficient of $x^t$ in $a_i S^T$ is $0$:

$$
0 = \sum_{k = 0}^{d} \alpha_k S_{t - k}^T = \Big( \sum_{j=0}^{d} S_{t - d + j}\, f_j \Big)^T,
$$

with $k = d - j$. All indices $t - k$ lie in $[t - d, t] \subseteq [0, L - 1]$. Putting $i = t - d$, which runs over $0 \le i < L - d$, gives (3).

**(4) Extraction.** Suppose $\sum_j A^j Y f_j = 0$. Since $Y = AZ$ and $f_j = 0$ for $j < e$,

$$
0 = \sum_{j \ge e} A^{j+1} Z f_j = A^{e+1} \sum_{j \ge e} A^{j - e} Z f_j = A^{e+1} u.
$$

Line L7 computes this $u$, by accumulating $Z f_j, A Z f_{j+1}, \dots$ with the block $A^{j-e} Z$ updated by one product per step. If $u \ne 0$, let $t \le e$ be the largest index with $A^t u \ne 0$; it exists because $A^0 u = u \ne 0$ and $A^{e+1} u = 0$. Then $A^{t+1} u = 0$. The loop of line L8 visits $u, Au, \dots$ in turn and returns the first $A^t u$ that is nonzero with $A^{t+1} u = 0$, which happens for some $t \le e$, within the $e + 2$ steps. $\blacksquare$

**What is not proved here.** Statement (3) is a condition on the projected sequence $X^T A^i Y$ only. That a generator of small degree also satisfies the stronger condition of (4), and that $u \ne 0$, holds with high probability over random $X$ and $Z$; this is the probabilistic analysis of Kaltofen (1995) for large fields and of Villard (1997) for small ones. The implementation does not rely on it, since it checks every candidate, and it repeats with new random blocks when all candidates fail.
