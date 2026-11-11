---
title: Shamir's scheme reconstructs the secret from any t shares and reveals nothing to t - 1
proves: [correctness]
status: full
---

Let $\mathbb{F}$ be a finite field, $1 \le t \le n < |\mathbb{F}|$, and let the share points $x_1, \ldots, x_n$ be distinct and nonzero (on the page $x_i = i$). The dealer's polynomial is $f(X) = s + a_1 X + \cdots + a_{t-1} X^{t-1}$ with $a_1, \ldots, a_{t-1}$ uniform and independent. Line numbers refer to the pseudocode on the page.

**Lemma 1 (uniqueness).** For distinct $u_1, \ldots, u_k \in \mathbb{F}$ and any $v_1, \ldots, v_k \in \mathbb{F}$ there is exactly one polynomial $g$ of degree less than $k$ with $g(u_j) = v_j$ for all $j$.

*Proof.* Existence: $g = \sum_j v_j \ell_j$ with $\ell_j(X) = \prod_{m \ne j} (X - u_m)/(u_j - u_m)$, which has degree $k - 1$, $\ell_j(u_j) = 1$ and $\ell_j(u_m) = 0$ for $m \ne j$. The denominators are nonzero because the $u_j$ are distinct, and $\mathbb{F}$ is a field, so they can be inverted. Uniqueness: the difference of two such polynomials has degree less than $k$ and $k$ roots. A nonzero polynomial over a field has at most as many roots as its degree, so the difference is zero. $\square$

**Lemma 2 (correctness).** For any $t$ shares $(x_j, f(x_j))$, line L5 returns $s$.

*Proof.* By Lemma 1 with $k = t$, $f = \sum_j f(x_j) \ell_j$, since $f$ has degree less than $t$ and agrees with the right side at the $t$ points. Evaluate at 0: $\ell_j(0) = \prod_{m \ne j} (0 - x_m)/(x_j - x_m) = \prod_{m \ne j} x_m / (x_m - x_j) = \lambda_j$, the value of line L4. So $\sum_j \lambda_j f(x_j) = f(0) = s$. $\square$

**Lemma 3 (perfect secrecy).** Let $B$ be a set of $t - 1$ of the share points. For each secret $s$, the vector $(f(x))_{x \in B}$ is uniform in $\mathbb{F}^{t-1}$. So its distribution does not depend on $s$.

*Proof.* Fix $s$. For each target vector $(v_x)_{x \in B}$, apply Lemma 1 with $k = t$ to the $t$ distinct points $\{0\} \cup B$ (distinct because the share points are nonzero) and the values $s$ at 0 and $v_x$ at $x$. There is exactly one polynomial of degree less than $t$ through them, and it has constant term $s$, so exactly one choice of $(a_1, \ldots, a_{t-1}) \in \mathbb{F}^{t-1}$ gives the shares $(v_x)$. The map from coefficients to shares is therefore a bijection of $\mathbb{F}^{t-1}$, and a uniform input gives a uniform output. For fewer than $t - 1$ shares, take the marginal of a uniform vector, which is again uniform. $\square$

**Lemma 4 (linearity).** If $(x_i, f(x_i))$ and $(x_i, g(x_i))$ are shares of $s$ and $s'$ with threshold $t$, then $(x_i, f(x_i) + g(x_i))$ are shares of $s + s'$, and $(x_i, c f(x_i))$ are shares of $c s$, with threshold $t$.

*Proof.* $f + g$ and $c f$ have degree less than $t$ and constant terms $s + s'$ and $c s$. Lemma 2 applies to them. $\square$

**Corollary 5 (refresh).** Let $g$ be a uniform polynomial of degree less than $t$ with $g(0) = 0$, independent of $f$. The refreshed shares $f(x_i) + g(x_i)$ are shares of $s$ by Lemma 4. Their joint distribution is that of a fresh sharing of $s$, independent of $f$ beyond $s$: the coefficients of $f + g$ above degree 0 are $a_k + b_k$ with $b_k$ uniform and independent, so they are uniform and independent of $(a_1, \ldots, a_{t-1})$.

**Remark (wrong shares).** If share $j$ is replaced by $f(x_j) + \delta$, then line L5 returns $s + \lambda_j \delta$, by linearity of the sum. Since $\lambda_j \ne 0$, the result is wrong whenever $\delta \ne 0$, and nothing in the computation shows it. With $t + 1$ shares, interpolate $f$ from $t$ of them and test the last one; by Lemma 1 a single wrong share among the $t + 1$ always fails this test, because the $t + 1$ values then do not lie on one polynomial of degree less than $t$. $\blacksquare$
