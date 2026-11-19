---
title: MLPG returns the unique maximizer of the Gaussian log likelihood, and the banded factorization has no fill
proves: [correctness]
status: full
---

Fix $T \ge 1$ frames and $D$ windows $w^{(0)}, \ldots, w^{(D-1)}$, each a finite map from offsets $\tau$ to coefficients, with $|\tau| \le L$ for every offset. The matrix $W$ has $DT$ rows indexed by $(t, d)$ and $T$ columns. Row $(t, d)$ has the entry $\sum w^{(d)}_\tau$ in column $u$, where the sum runs over the offsets with $\kappa(t + \tau) = u$; for the clamp rule $\kappa(x) = \min(\max(x, 0), T - 1)$, and for the zero rule $\kappa(x) = x$ and the offsets with $t + \tau$ outside $0 \ldots T-1$ are dropped. Let $U = \mathrm{diag}(\sigma^2_{t,d})$ with every $\sigma^2_{t,d} > 0$, and let $\mu$ be the vector of the means $\mu_{t,d}$. Define

$$\ell(c) = -\tfrac12 (Wc - \mu)^\top U^{-1} (Wc - \mu), \qquad P = W^\top U^{-1} W, \qquad r = W^\top U^{-1} \mu.$$

The log density $\log \mathcal{N}(Wc; \mu, U)$ is $\ell(c)$ plus a constant that does not depend on $c$.

## The maximizer

**Lemma 1.** If one window is the static window $\{0 \mapsto 1\}$, then $P$ is symmetric positive definite.

*Proof.* $P^\top = W^\top U^{-\top} W = P$ because $U$ is diagonal. For any $x$, $x^\top P x = \sum_{t,d} (W x)_{t,d}^2 / \sigma^2_{t,d} \ge \sum_t x_t^2 / \sigma^2_{t,0}$, keeping only the static rows, whose entries are $(Wx)_{t,0} = x_t$ under both edge rules. This is positive for $x \ne 0$. $\square$

**Theorem 1.** If $P$ is positive definite, $\ell$ has the unique maximizer $c^* = P^{-1} r$.

*Proof.* Expanding, $\ell(c) = -\tfrac12 c^\top P c + c^\top r - \tfrac12 \mu^\top U^{-1} \mu$. For any $c$, write $c = c^* + x$. Then $\ell(c) = \ell(c^*) - \tfrac12 x^\top P x + x^\top (r - P c^*) = \ell(c^*) - \tfrac12 x^\top P x$, which is less than $\ell(c^*)$ for $x \ne 0$. $\square$

If $P$ is only positive semidefinite, for example with no static window, then $\ell$ is constant along the null space of $W$ and the maximizer is not unique. The code finds a pivot that is not positive and raises an error in that case (Lemma 3).

## Lines L1 to L5 build P and r

Line L4 adds $a\,c / \sigma^2_{t,d}$ to entry $(u, v)$ for every pair of entries $(u, a)$ and $(v, c)$ of row $(t, d)$, and line L5 adds $a\, \mu_{t,d} / \sigma^2_{t,d}$ to $r_u$. Summed over the rows, these are $\sum_{t,d} W_{(t,d),u} W_{(t,d),v} / \sigma^2_{t,d} = P_{uv}$ and $\sum_{t,d} W_{(t,d),u}\, \mu_{t,d} / \sigma^2_{t,d} = r_u$. The code stores only $u \ge v$, which is enough because $P$ is symmetric.

**Lemma 2 (band).** $P_{uv} = 0$ when $|u - v| > 2L$.

*Proof.* Every nonzero entry of row $(t, d)$ is in a column $\kappa(t + \tau)$ with $|\tau| \le L$. Under both rules this column lies in $[t - L, t + L]$, because clamping moves a column toward $t$. A term of $P_{uv}$ needs $u$ and $v$ in the same row, so $|u - v| \le 2L$. $\square$

So $P$ has half-bandwidth $b = 2L$.

## Lines L6 to L8: the banded LDL factorization

**Lemma 3.** Let $P$ be symmetric with half-bandwidth $b$. If $P$ is positive definite, lines L6 to L8 compute a unit lower triangular $L$ with $L_{ij} = 0$ for $i - j > b$ and positive $D_1, \ldots, D_T$ with $P = L\, \mathrm{diag}(D)\, L^\top$. If $P$ is singular, some pivot $D_j$ is not positive and the code raises an error.

*Proof.* Equating the entries of $P = L\,\mathrm{diag}(D)\,L^\top$ on and below the diagonal gives, column by column,

$$D_j = P_{jj} - \sum_{k<j} L_{jk}^2 D_k, \qquad L_{ij} = \Bigl(P_{ij} - \sum_{k<j} L_{ik} L_{jk} D_k\Bigr) / D_j \quad (i > j).$$

These are the formulas of the dense factorization. By induction on $j$, the entries $L_{ik}$ with $i - k > b$ are 0: for $i - j > b$, $P_{ij} = 0$ by the band, and every term $L_{ik} L_{jk}$ with $k < j$ has $i - k > b$, so it is 0 by the induction hypothesis. So the dense formulas reduce to the sums over $k \ge \max(0, i - b)$ of the code, and the code computes the same $L$ and $D$ as the dense formulas, with no fill outside the band.

The leading $j \times j$ block satisfies $P_{[j]} = L_{[j]}\,\mathrm{diag}(D_1, \ldots, D_j)\,L_{[j]}^\top$ with $\det L_{[j]} = 1$, so $D_1 \cdots D_j = \det P_{[j]}$. If $P$ is positive definite, every leading minor is positive (Sylvester's criterion), so by induction every $D_j = \det P_{[j]} / \det P_{[j-1]} > 0$ and the division is safe. If $P$ is not positive definite, some leading minor is not positive, again by Sylvester's criterion. Take the first such $j$. The pivots before it are positive, so $D_j = \det P_{[j]} / \det P_{[j-1]} \le 0$, and line L7 raises an error. In exact arithmetic this test is exact; in floating point a nearly singular $P$ can give a tiny positive pivot instead. $\square$

## Lines L9 to L12: the solves

Line L9 solves $L y = r$ by forward substitution, line L10 sets $z = \mathrm{diag}(D)^{-1} y$, and line L11 solves $L^\top c = z$ by back substitution, each using only the entries inside the band. Then $L\,\mathrm{diag}(D)\,L^\top c = r$, so $Pc = r$ and $c = c^*$ by Theorem 1.

**Theorem 2.** If one window is static, MLPG returns the unique $c$ that maximizes $\log \mathcal{N}(Wc; \mu, U)$. Every step uses only $+$, $-$, $\times$ and $/$, so with Fraction inputs the result is exact.

*Proof.* Lemma 1, Theorem 1, Lemma 3 and the solves above. $\square$

## Cost

Building $P$ and $r$ costs $\sum_{t,d} s_d^2 = O(T \sum_d s_d^2)$ operations, where $s_d \le 2L + 1$ is the number of offsets of window $d$. The factorization does at most $b$ inner steps for each of the at most $b$ entries of each of the $T$ columns, so $O(T b^2)$, and the solves cost $O(T b)$. The storage is $O(T b)$. For fixed windows, the whole computation is $\Theta(T)$.
