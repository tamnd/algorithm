---
title: Correctness of the Sylvester matrix operations and the rank formula
proves: [correctness]
status: full
---

**Setting.** $R$ is an integral domain with field of fractions $F$. $f = \sum_{k=0}^{m} a_k x^k$ and $g = \sum_{k=0}^{n} b_k x^k$ have formal degrees $m, n \ge 0$, and $N = m + n$. Column $c$ of $\operatorname{Syl}(f, g)$ stands for $x^{N-1-c}$. For $d \ge 0$, $P_d$ is the $F$-space of polynomials of degree less than $d$, with the basis $x^{d-1}, \ldots, x, 1$.

**ENTRY.** Row $i < n$ is meant to be the coefficient vector of $x^{n-1-i} f = \sum_k a_k x^{k + n - 1 - i}$. Column $c$ stands for $x^{N - 1 - c}$, so the entry is $a_k$ with $k + n - 1 - i = N - 1 - c$, that is $k = m - (c - i)$, when $0 \le k \le m$, and $0$ otherwise. This is line E3. In the same way, row $n + j$ is $x^{m-1-j} g$, with the entry $b_{n - (c - j)}$, as on line E4. $\square$

**COMBINE.** Let $s = \sum_{i<n} s_i x^{n-1-i} \in P_n$ and $t = \sum_{j<m} t_j x^{m-1-j} \in P_m$. The row vector $(s_0, \ldots, s_{n-1}, t_0, \ldots, t_{m-1})$ times $\operatorname{Syl}(f, g)$ is $\sum_i s_i \, \text{row}_i + \sum_j t_j \, \text{row}_{n+j}$. By the claim on ENTRY, this is the coefficient vector of $\sum_i s_i x^{n-1-i} f + \sum_j t_j x^{m-1-j} g = s f + t g$, which has degree less than $N$. Lines C3 and C4 add $s_i a_{m-k}$ and $t_j b_{n-k}$ at position $i + k$ and $j + k$. Position $p$ stands for $x^{N-1-p}$, and $x^{n-1-i} \cdot x^{m-k} = x^{N-1-(i+k)}$, so these are exactly the terms of the two products. $\square$

So $\operatorname{Syl}(f, g)$ is the matrix of the $F$-linear map

$$\varphi : P_n \times P_m \to P_N, \qquad (s, t) \mapsto s f + t g,$$

acting on row vectors, and $\operatorname{rank} \operatorname{Syl}(f, g) = \dim \operatorname{im} \varphi = N - \dim \ker \varphi$.

**DET.** Lines L2 to L11 are the [Bareiss algorithm](/bareiss-algorithm/) on the dense matrix. Its correctness proof shows: after the step for pivot $k$, each entry $A[i][j]$ with $i, j > k$ equals the minor of the row-permuted input on the rows $0, \ldots, k, i$ and the columns $0, \ldots, k, j$, which is an element of $R$, and the division on line L9 is exact because $R$ is an integral domain and the divisor is the previous pivot minor, which is nonzero. If line L6 finds no pivot in column $k$, then the rows $k, \ldots, N-1$ of the current matrix are zero in column $k$, and the current matrix is upper block triangular with a zero column below the diagonal, so the determinant is 0. Otherwise, at the end $A[N-1][N-1]$ is the full determinant of the row-permuted input. Each swap on line L7 changes the sign of the determinant, and `sign` records this. Line L1 returns $\det$ of the empty matrix, which is 1. So DET returns $\det \operatorname{Syl}(f, g)$. $\square$

**Rank formula.** *Claim.* If $a_m \ne 0$ or $b_n \ne 0$, then $\operatorname{rank} \operatorname{Syl}(f, g) = m + n - \deg \gcd(f, g)$, where $\gcd(f, 0) = f$ and the gcd is taken in $F[x]$.

*Proof.* By symmetry (swapping $f$ and $g$ permutes the rows and does not change the rank) assume $a_m \ne 0$, so $\deg f = m$. If $g = 0$, then $\gcd(f, g) = f$ has degree $m$, and $\ker \varphi = \{(s, t) : s f = 0\} = \{0\} \times P_m$ has dimension $m$, so the rank is $n$, as claimed. Now let $g \ne 0$, $h = \gcd(f, g)$ of degree $e$, $f = h f_1$ and $g = h g_1$ with $\gcd(f_1, g_1) = 1$ and $\deg f_1 = m - e$.

Let $(s, t) \in \ker \varphi$. Then $s f_1 = -t g_1$. So $f_1$ divides $t g_1$, and since $f_1$ and $g_1$ are coprime, $f_1$ divides $t$: $t = q f_1$ for some $q \in F[x]$. Then $s f_1 = -q f_1 g_1$, so $s = -q g_1$. The condition $\deg t < m$ means $\deg q < m - \deg f_1 = e$ (or $q = 0$). Conversely, every $q \in P_e$ gives $t = q f_1$ with $\deg t < e + m - e = m$ and $s = -q g_1$ with $\deg s < e + \deg g_1 = \deg g \le n$, and $(s, t) \in \ker \varphi$. The map $q \mapsto (-q g_1, q f_1)$ is linear and injective, because $f_1 \ne 0$. So $\dim \ker \varphi = \dim P_e = e$, and the rank is $m + n - e$. $\square$

*Consequence.* When $a_m \ne 0$ or $b_n \ne 0$, $\operatorname{Res}_{m,n}(f, g) = \det \operatorname{Syl}(f, g) = 0$ if and only if the rank is below $N$, which is if and only if $\deg \gcd(f, g) \ge 1$. When $a_m = b_n = 0$, column 0 is zero, and the determinant is 0. $\blacksquare$
