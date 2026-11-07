---
title: The eight block products add up to the matrix product
proves: [correctness, termination]
status: full
---

Let $R$ be a ring, or a semiring (commutativity of the multiplication is not used). A *view* is a block of an array given by a row range and a column range. For a call DC-MULTIPLY-ADD$(A, B, C)$ with $A$ of shape $n \times m$, $B$ of shape $m \times p$ and $C$ of shape $n \times p$, write $C^{\text{old}}$ for $C$ at the start of the call. Let $\mathcal{T} = \{(i, j, k) : 0 \le i < n,\ 0 \le j < p,\ 0 \le k < m\}$ be its set of index triples.

**Claim.** The call stops. When it returns, $C[i][j] = C^{\text{old}}[i][j] + \sum_{k=0}^{m-1} A[i][k] B[k][j]$ for all $i, j$, where the products are added one at a time in increasing order of $k$. No entry of the arrays outside the view $C$ changes, and $A$ and $B$ do not change. Line L3 runs exactly $|\mathcal{T}| = nmp$ times.

**Termination.** Let $\mu = n + m + p$. If the call reaches line L5, then it did not return at line L1 or L4, so $n, m, p \ge 1$ and at least one side is at least 2. A side $d \ge 2$ splits into $\lceil d/2 \rceil < d$ and $\lfloor d/2 \rfloor < d$. A side $d = 1$ splits into $1$ and $0$. So each of the eight calls of lines L8 and L9 has its three sides at most the old ones, and the side that was at least 2 is strictly smaller. So $\mu$ drops by at least 1 in each call, and $\mu \ge 0$, so the recursion is finite.

**Proof of the claim.** By strong induction on $\mu$.

*Base cases.* If $n = 0$ or $p = 0$, there are no entries of $C$ and line L1 returns, so the claim holds. If $m = 0$, each sum is empty and line L1 returns with $C = C^{\text{old}}$. If $n = m = p = 1$, line L3 adds $A[0][0] B[0][0]$ to $C[0][0]$, which is the claim with one term, and $|\mathcal{T}| = 1$.

*Step.* Let $n, m, p \ge 1$ with one side at least 2, and assume the claim for all calls with a smaller $\mu$. Line L5 splits the row range $[0, n)$ into $I_1 = [0, n_1)$ and $I_2 = [n_1, n)$ with $n_1 = \lceil n/2 \rceil$, the inner range into $K_1 = [0, m_1)$ and $K_2 = [m_1, m)$, and the column range into $J_1$ and $J_2$. The view $A_{rt}$ has rows $I_r$ and columns $K_t$, the view $B_{ts}$ has rows $K_t$ and columns $J_s$, and the view $C_{rs}$ has rows $I_r$ and columns $J_s$. The views $C_{11}, C_{12}, C_{21}, C_{22}$ are disjoint and cover $C$.

Fix $(r, s)$ and an entry $(i, j)$ with $i \in I_r$, $j \in J_s$. Only the two calls with this $(r, s)$ change $C_{rs}$, because each call changes only its own view of $C$ by the hypothesis. The call of line L8 has a smaller $\mu$, so by the hypothesis it adds $\sum_{k \in K_1} A[i][k] B[k][j]$, in increasing order of $k$. Then the call of line L9 adds $\sum_{k \in K_2} A[i][k] B[k][j]$, in increasing order of $k$. Every element of $K_1$ is less than every element of $K_2$, and $K_1 \cup K_2 = [0, m)$. So after both calls,

$$C[i][j] = C^{\text{old}}[i][j] + \sum_{k=0}^{m-1} A[i][k] B[k][j],$$

with the terms added in increasing order of $k$. The calls for other pairs $(r', s')$ do not touch $C_{rs}$. This holds for each entry, so the claim holds for $C$. The calls read $A$ and $B$ and never write them.

*Count.* The eight sets $I_r \times J_s \times K_t$ for $r, s, t \in \{1, 2\}$ are disjoint and their union is $\mathcal{T}$. By the hypothesis, the call for $(r, s, t)$ runs line L3 exactly $|I_r| |J_s| |K_t|$ times. The sum over the eight calls is $|\mathcal{T}|$. $\blacksquare$

**Corollary.** DC-MULTIPLY-ADD$(A, B, 0)$ gives $AB$, with each entry computed by the same sequence of additions as the triple loop with $s$ starting at $0$.
