---
title: Even expansion, extrapolation and order of the Gragg-Bulirsch-Stoer method
proves: [correctness]
status: full
---

**Setting.** $y' = f(t, y)$, $y \in \mathbb{R}^d$, with $f$ smooth. One big step from $(t, y)$ of size $H$ uses the modified midpoint values $T_{j,1} = z_{n_j}$, with substeps $h_j = H/n_j$ and even $n_1 < \dots < n_k$, and the Aitken-Neville table
$$T_{j,l} = T_{j,l-1} + \frac{T_{j,l-1} - T_{j-1,l-1}}{(n_j/n_{j-l+1})^2 - 1}.$$

## Theorem 1 (Gragg's expansion, cited)

Let $f$ be $C^{2m+2}$. There are functions $c_1, \dots, c_m$, the same for all even $n$, such that for even $n$,
$$z_n = y(t + H) + c_1(H)\,h^2 + \dots + c_m(H)\,h^{2m} + O(h^{2m+2}), \qquad h = H/n,$$
where $c_i(H) = O(H)$ because each $c_i$ vanishes at $H = 0$. This is Gragg's theorem (Gragg 1965; Hairer, Nørsett and Wanner, Section II.9). We do not reprove it here. The idea of the proof is as follows. Hairer, Nørsett and Wanner rewrite the midpoint rule, including its Euler start, as a one-step method with step $2h$ that acts on pairs of values, both starting at $y$. This one-step method is symmetric: replacing $h$ by $-h$ gives its inverse. A symmetric one-step method has a global error expansion that contains only even powers of $h$ (Section II.8), and the values $z_n$ can be read off from it. In fact the expansion has the form $\sum_ih^{2i}(a_i + (-1)^nb_i)$, so its coefficients depend on the parity of $n$. All $n_j$ must therefore have the same parity, and the method uses even $n_j$.

## Lemma 2 (Aitken-Neville computes the extrapolated polynomial)

Let $P_{j,l}$ be the polynomial in $x = h^2$ of degree at most $l - 1$ that takes the values $T_{i,1}$ at $x_i = h_i^2$ for $i = j - l + 1, \dots, j$. Then $T_{j,l} = P_{j,l}(0)$.

*Proof.* By induction on $l$. For $l = 1$ the statement is $P_{j,1} = T_{j,1}$. Neville's recursion for interpolating polynomials evaluated at $x = 0$ is
$$P_{j,l}(0) = \frac{(0 - x_{j-l+1})P_{j,l-1}(0) - (0 - x_j)P_{j-1,l-1}(0)}{x_j - x_{j-l+1}}.$$
Both sides are polynomials of degree at most $l - 1$ interpolating the right data, which is a standard identity. Dividing numerator and denominator by $x_j$ and using $x_{j-l+1}/x_j = (n_j/n_{j-l+1})^2$, this becomes $P_{j,l-1}(0) + (P_{j,l-1}(0) - P_{j-1,l-1}(0))/((n_j/n_{j-l+1})^2 - 1)$, which is the recursion of the table. $\square$

**Corollary (exactness).** If $T_{i,1} = a_0 + a_1h_i^2 + \dots + a_{l-1}h_i^{2(l-1)}$ for $i = j - l + 1, \dots, j$, then $T_{j,l} = a_0$ exactly. The tests check this in exact rational arithmetic for a polynomial of degree 3 in $h^2$ and $l = 4$, and that $l = 3$ is not exact.

## Theorem 3 (order $2k$)

Let $f$ be $C^{2k+2}$. Then $T_{k,k} = y(t + H) + O(H^{2k+1})$ and $T_{k,k-1} = y(t + H) + O(H^{2k-1})$.

*Proof.* Insert Theorem 1 with $m = k$ into Lemma 2. The value $P_{k,k}(0)$ is a linear combination $\sum_i w_iT_{i,1}$ with weights (the Lagrange weights at 0) that depend only on the ratios $n_i/n_j$, not on $H$. They satisfy $\sum_iw_i = 1$ and $\sum_iw_ih_i^{2q} = 0$ for $q = 1, \dots, k - 1$. So
$$T_{k,k} = y(t + H) + \sum_iw_i\big(c_k(H)h_i^{2k} + O(h_i^{2k+2})\big).$$
Since $h_i = H/n_i$ and $c_k(H) = O(H)$, the remainder is $O(H^{2k+1})$. The same argument for $T_{k,k-1}$ leaves the term with $c_{k-1}(H)h_i^{2k-2} = O(H^{2k-1})$. $\square$

So the local error of the step is $O(H^{2k+1})$, and the estimate $T_{k,k} - T_{k,k-1}$ equals the local error of $T_{k,k-1}$ up to $O(H^{2k+1})$. That is an asymptotic statement. The method is a one-step method whose increment is Lipschitz in $y$ when $f$ is Lipschitz: each midpoint run has a Lipschitz constant $1 + O(HL)$ in $y$, and the extrapolation weights are fixed. So the standard one-step convergence argument gives global error $O(H^{2k})$ for fixed $H$. The table on the page shows the orders 2, 4, 6 and 8.

## Proposition 4 (stability function)

On $y' = \lambda y$ with $z = H\lambda$, every $T_{j,1}$ is a polynomial in $z$ of degree $n_j$. Hence $T_{k,k}$ is a polynomial of degree at most $n_k = 2k$. By Theorem 3 it agrees with $e^z$ up to $O(z^{2k+1})$. A polynomial of degree at most $2k$ with that property is the Taylor polynomial $\sum_{q=0}^{2k}z^q/q!$. $\square$

The tests compare one step of the code with this polynomial at real and complex $z$, for $k = 2, 3, 4$.

## Cost and termination

The run with $n_j$ substeps evaluates $f$ at $z_0, \dots, z_{n_j - 1}$, and $f(t, z_0) = f(t, y)$ is shared by all runs. So an attempt costs $1 + \sum_j(n_j - 1) = 1 + \sum_{j=1}^k(2j - 1) = k^2 + 1$ evaluations. A rejected attempt has $\mathrm{err} > 1$, so $H$ is multiplied by $\min(1, 0.9\,\mathrm{err}^{-1/(2k-1)}) < 0.9$. With $\mathrm{atol} > 0$ and $\|\mathrm{est}\| \le KH^{2k-1}$ for small $H$, a step is accepted after finitely many rejections. Line L3 makes the last accepted point exactly $T$.

## Linear invariants

If $w^Tf = 0$ identically, each midpoint run keeps $w^Tz_m = w^Ty$. The extrapolation weights sum to 1, so $w^TT_{k,k} = w^Ty$ as well.
