---
title: The Robbins-Monro iteration converges in mean square under the step conditions, at the rate O(1/n) with steps of order 1/n
proves: [correctness, convergence-rate]
status: full
---

**Setting.** $X \subseteq \mathbb{R}^d$ is closed and convex, and $P$ is the Euclidean projection onto $X$ (with $X = \mathbb{R}^d$ and $P$ the identity when there is no constraint). The field is $h(x) = \mathbb{E}_\xi H(x, \xi)$, and $x^* \in X$ is a point with $h(x^*) = 0$. The iteration is $x_{n+1} = P(x_n - a_nY_n)$ with $Y_n = H(x_n, \xi_n)$, fresh independent samples $\xi_n$ and fixed steps $a_n > 0$. Let $\mathcal{F}_n$ be the history up to $x_n$, so $\mathbb{E}[Y_n \mid \mathcal{F}_n] = h(x_n)$. Write $e_n = \mathbb{E}\lVert x_n - x^*\rVert^2$.

**Assumptions.** For all $x \in X$:

- (A1) strong monotonicity at the root: $\langle h(x), x - x^*\rangle \ge \mu\lVert x - x^*\rVert^2$ with $\mu > 0$;
- (A2) growth of the second moment: $\mathbb{E}\lVert H(x, \xi)\rVert^2 \le A + B\lVert x - x^*\rVert^2$ with $A, B \ge 0$.

The field $h$ need not be a gradient. (A1) makes $x^*$ the only root in $X$: if $h(y) = 0$ then $\mu\lVert y - x^*\rVert^2 \le 0$.

**Lemma 1 (one step).** $e_{n+1} \le (1 - 2\mu a_n + Ba_n^2)\,e_n + Aa_n^2$.

*Proof.* The projection does not increase distances and $P(x^*) = x^*$, so $\lVert x_{n+1} - x^*\rVert^2 \le \lVert x_n - x^*\rVert^2 - 2a_n\langle Y_n, x_n - x^*\rangle + a_n^2\lVert Y_n\rVert^2$. Take $\mathbb{E}[\cdot \mid \mathcal{F}_n]$. The middle term becomes $-2a_n\langle h(x_n), x_n - x^*\rangle \le -2\mu a_n\lVert x_n - x^*\rVert^2$ by (A1), and the last term is at most $a_n^2(A + B\lVert x_n - x^*\rVert^2)$ by (A2). Take the full expectation. $\square$

**Lemma 2 (a deterministic sequence).** Let $u_n \ge 0$ satisfy $u_{n+1} \le (1 - b_n)u_n + c_n$ for $n \ge N$, with $0 \le b_n \le 1$, $\sum_n b_n = \infty$, $c_n \ge 0$ and $\sum_n c_n < \infty$. Then $u_n \to 0$.

*Proof.* Write $\Pi_{j,m} = \prod_{i=j}^{m-1}(1 - b_i)$, which is at most $\exp(-\sum_{i=j}^{m-1}b_i)$ and so tends to $0$ as $m \to \infty$ for each fixed $j$. Unrolling gives, for $m > M \ge N$,

$$u_m \le \Pi_{N,m}u_N + \sum_{j=N}^{M-1}\Pi_{j+1,m}c_j + \sum_{j=M}^{m-1}\Pi_{j+1,m}c_j \le \Pi_{N,m}u_N + \Pi_{M,m}\sum_{j\ge N}c_j + \sum_{j\ge M}c_j,$$

since every factor of a product is in $[0, 1]$ and $\Pi_{j+1,m} \le \Pi_{M,m}$ for $j < M$. Given $\varepsilon > 0$, choose $M$ with $\sum_{j\ge M}c_j < \varepsilon$. As $m \to \infty$ the first two terms tend to $0$, so $\limsup u_m \le \varepsilon$. $\square$

**Theorem 1 (mean-square convergence).** Under (A1) and (A2), if $\sum_n a_n = \infty$ and $\sum_n a_n^2 < \infty$, then $\mathbb{E}\lVert x_n - x^*\rVert^2 \to 0$.

*Proof.* Since $\sum a_n^2 < \infty$, $a_n \to 0$, so there is $N$ with $Ba_n \le \mu$ and $\mu a_n \le 1$ for all $n \ge N$. For those $n$, $1 - 2\mu a_n + Ba_n^2 \le 1 - \mu a_n$, and Lemma 1 gives $e_{n+1} \le (1 - \mu a_n)e_n + Aa_n^2$. Apply Lemma 2 with $b_n = \mu a_n$ and $c_n = Aa_n^2$. $\blacksquare$

**Theorem 2 (rate).** Under (A1) and (A2), let $n_0 \ge \max(2, 2B/\mu^2)$ and $a_n = \frac{2}{\mu(n + n_0)}$. Then for every $n \ge 0$

$$\mathbb{E}\lVert x_n - x^*\rVert^2 \le \frac{\nu}{n + n_0}, \qquad \nu = \max\Big(n_0\lVert x_0 - x^*\rVert^2,\ \frac{4A}{\mu^2}\Big).$$

*Proof.* Write $t = n + n_0 \ge 2$. Then $2\mu a_n = 4/t$ and $Ba_n^2 = 4B/(\mu^2t^2) \le 2/t$, because $t \ge n_0 \ge 2B/\mu^2$. So Lemma 1 gives $e_{n+1} \le (1 - 2/t)e_n + 4A/(\mu^2t^2)$, with $1 - 2/t \ge 0$. The claim holds at $n = 0$ by the choice of $\nu$. If $e_n \le \nu/t$, then

$$e_{n+1} \le \frac{(t - 2)\nu}{t^2} + \frac{\nu}{t^2} = \frac{(t - 1)\nu}{t^2} \le \frac{\nu}{t + 1},$$

since $4A/\mu^2 \le \nu$ and $(t - 1)(t + 1) \le t^2$. $\blacksquare$

**Proposition 3 (the step conditions cannot be dropped).**

1. If $\sum a_n < \infty$ and $a_n < 1$, the method can fail without any noise. Take $h(x) = H(x, \xi) = x$ on $\mathbb{R}$ with $x^* = 0$. Then $x_n = x_0\prod_{j<n}(1 - a_j)$, and the product tends to a positive limit because $\sum_j a_j < \infty$. For $a_j = 1/(j + 2)^2$ the limit is $\prod_{i\ge2}(1 - 1/i^2) = 1/2$.
2. If $a_n = a$ is constant, so that $\sum a_n^2 = \infty$, the error need not go to $0$. Take $H(x, \xi) = M(x - x^*) + s\xi$ with $M = \begin{pmatrix}1 & 1\\ -1 & 1\end{pmatrix}$ and $\xi \sim N(0, I)$ in $\mathbb{R}^2$. With $T = I - aM$, the error $d_n = x_n - x^*$ satisfies $d_{n+1} = Td_n - as\xi_n$, so its covariance satisfies $C_{n+1} = TC_nT^\top + a^2s^2I$. Since $TT^\top = ((1 - a)^2 + a^2)I$, the fixed point is $C = cI$ with $c = a^2s^2/(1 - (1 - a)^2 - a^2) = as^2/(2(1 - a))$ for $0 < a < 1$. The mean $T^nd_0$ tends to $0$ because $\lVert T\rVert^2 = (1 - a)^2 + a^2 < 1$, so $e_n \to as^2/(1 - a) > 0$.

*Proof.* Both parts are direct computations given in the statement. For part 1, $\prod_{i=2}^{m}(1 - 1/i^2) = \frac{m + 1}{2m}$ telescopes to $1/2$. $\blacksquare$

**Remarks.** Theorems 1 and 2 hold with $P$ the identity, which is the original unconstrained iteration. Under the weaker condition $\langle h(x), x - x^*\rangle > 0$ for $x \ne x^*$, with (A2) and the same step conditions, $x_n \to x^*$ almost surely. That result needs the Robbins-Siegmund supermartingale convergence theorem and is not proved here. The test file checks Theorem 2 on the exact first and second moments of the linear field in Proposition 3, where Lemma 1 is not tight, and on the quantile problem by Monte Carlo over 400 seeds.
