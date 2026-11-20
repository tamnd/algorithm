---
title: Each step of the variational kernel estimate maximizes the free energy exactly, so the free energy never decreases, while joint MAP with a Laplace prior prefers no blur
proves: [correctness]
status: full
---

**Setting.** On a periodic grid of $n$ points, $d = Kg + e$ with $e \sim N(0, \sigma^2 I)$, where $K$ is the circulant matrix of the kernel $k$, $(Kg)_r = \sum_s k_s g_{r-s}$. The kernel lies in $\mathcal K = \{k \ge 0,\ k = 0 \text{ outside } T,\ \sum k = 1\}$ for a support set $T$ of $m$ offsets. Each $g_i$ has a hidden label $z_i \in \{1, \dots, J\}$ with $P(z_i = j) = \pi_j$ and $g_i \mid z_i = j \sim N(0, v_j)$, all independent. For a distribution $q(g, z) = q(g)\,q(z)$ the free energy is

$$\mathcal F(q, k) = \mathbb E_q[\log p(d, g, z \mid k)] + H[q] = \log p(d \mid k) - \mathrm{KL}\big(q \,\Vert\, p(g, z \mid d, k)\big).$$

The second form follows from $p(d, g, z \mid k) = p(d \mid k)\,p(g, z \mid d, k)$. So $\mathcal F \le \log p(d \mid k)$, with equality exactly when $q$ is the posterior. The algorithm is lines L1 to L8 of the page.

**Claim 1 (the step for $q(g)$).** For fixed $q(z)$ with $r_{ij} = q(z_i = j)$ and fixed $k$, the maximizer of $\mathcal F$ over all densities $q(g)$ is $N(\mu, S)$ with

$$S^{-1} = K^TK/\sigma^2 + \operatorname{diag}(w), \qquad w_i = \sum_j r_{ij}/v_j, \qquad \mu = S K^T d/\sigma^2.$$

*Proof.* The terms of $\mathcal F$ that depend on $q(g)$ are $\mathbb E_{q(g)}[\phi(g)] + H[q(g)]$ with $\phi(g) = \mathbb E_{q(z)}[\log p(d, g, z \mid k)]$. This equals $-\mathrm{KL}(q(g) \Vert e^{\phi}/Z) + \log Z$, which is largest exactly at $q(g) \propto e^{\phi}$. Up to terms free of $g$, $\phi(g) = -\lVert d - Kg\rVert^2/(2\sigma^2) - \sum_i \sum_j r_{ij}\,g_i^2/(2v_j)$, a concave quadratic whose Hessian is $-S^{-1}$ and whose maximum is at $\mu$. So $e^{\phi}$ is proportional to the density of $N(\mu, S)$. $S^{-1}$ is positive definite because $w_i > 0$. $\square$

**Claim 2 (the step for $q(z)$).** For fixed $q(g) = N(\mu, S)$ and $k$, the maximizer over all $q(z)$ is the product over $i$ of $r_{ij} \propto \pi_j\, v_j^{-1/2}\exp\big(-(\mu_i^2 + S_{ii})/(2v_j)\big)$.

*Proof.* The same argument with $\phi(z) = \mathbb E_{q(g)}[\log p(g, z)] = \sum_i \big(\log \pi_{z_i} - \tfrac12\log(2\pi v_{z_i}) - \mathbb E[g_i^2]/(2v_{z_i})\big)$ and $\mathbb E[g_i^2] = \mu_i^2 + S_{ii}$. The sum over $i$ makes $e^{\phi}$ a product, so the optimal $q(z)$ factors over the pixels. $\square$

**Claim 3 (the step for $k$).** For fixed $q$, $\mathcal F$ depends on $k$ only through $-\mathbb E_q\lVert d - Kg\rVert^2/(2\sigma^2)$, and

$$\mathbb E_q\lVert d - Kg\rVert^2 = \lVert d - K\mu\rVert^2 + \operatorname{tr}(KSK^T) = \lVert d\rVert^2 - 2b^Tk_T + k_T^TAk_T,$$

where $k_T$ lists the values of $k$ on $T$, $A_{st} = \sum_r (\mu_{r-s}\mu_{r-t} + S_{r-s,\,r-t})$ and $b_s = \sum_r d_r\mu_{r-s}$ for $s, t \in T$. $A$ is positive semidefinite, so line L7 solves a convex quadratic program over the simplex.

*Proof.* With $g = \mu + u$, $\mathbb E u = 0$ and $\mathbb E uu^T = S$, $\mathbb E\lVert d - K\mu - Ku\rVert^2 = \lVert d - K\mu\rVert^2 + \mathbb E\lVert Ku\rVert^2$, and $\mathbb E\lVert Ku\rVert^2 = \operatorname{tr}(KSK^T)$. Writing $(Kg)_r = \sum_{s \in T} k_s g_{r-s}$ and expanding gives the stated $A$ and $b$. For any vector $c$ on $T$, $c^TAc = \sum_r \big((\sum_s c_s\mu_{r-s})^2 + \operatorname{Var}(\sum_s c_s u_{r-s})\big) \ge 0$. $\square$

**Claim 4 (the quadratic program is solved exactly).** Let $A$ be symmetric positive semidefinite and $\Delta$ the simplex. The routine `simplex_qp` returns a minimizer of $Q(k) = k^TAk - 2b^Tk$ over $\Delta$ (with $A$ replaced by $A + \varepsilon I$, $\varepsilon = 10^{-12}$, which makes it strictly convex and the minimizer unique).

*Proof.* $Q$ is strictly convex, so it has one minimizer $k^\ast$ on the compact convex set $\Delta$. Let $U$ be the set of coordinates where $k^\ast > 0$. Then $k^\ast$ lies in the relative interior of the face $\Delta_U$, and it minimizes $Q$ over the affine set $\{k : k_i = 0 \text{ for } i \notin U,\ \sum k = 1\}$: if some point of that affine set had a lower value, the segment from $k^\ast$ toward it would stay in $\Delta_U$ for a short distance and, by convexity, lower $Q$ there. The minimizer over the affine set is the solution of the KKT system that the routine solves for $U$, and it is unique by strict convexity. So $k^\ast$ is one of the candidates. Every candidate that the routine keeps is a point of $\Delta$, so its value is at least $Q(k^\ast)$, and the routine returns the candidate of least value, which is $k^\ast$. $\square$

**Claim 5 (the free energy never decreases).** Along lines L4, L5 and L7, the value of $\mathcal F$ never decreases, and it is bounded above by $\max_{k \in \mathcal K}\log p(d \mid k)$. So the values converge.

*Proof.* By Claims 1 to 4 each line replaces one block of $(q(g), q(z), k)$ by a maximizer of $\mathcal F$ over that block with the others fixed; a maximizer is at least as good as the current value. The bound is $\mathcal F \le \log p(d \mid k)$. $\log p(d \mid k)$ is continuous in $k$ on the compact set $\mathcal K$ (it is a finite mixture of Gaussian densities whose covariances $KV_zK^T + \sigma^2 I$ are at least $\sigma^2 I$), so it has a maximum. A nondecreasing sequence that is bounded above converges. $\square$

This is a statement about the values of $\mathcal F$; it does not say that the kernels converge, or that they converge to the kernel of largest evidence. The tests check the monotone values on a run.

**Claim 6 (the bound is tight for a Gaussian prior).** If $J = 1$, the step of Claim 1 makes $\mathcal F = \log p(d \mid k) = \log N(d;\, 0,\ v KK^T + \sigma^2 I)$.

*Proof.* With one component $z$ is fixed and $p(g \mid d, k)$ is the Gaussian of Claim 1, so the KL term is $0$. Integrating $g \sim N(0, vI)$ out of $d = Kg + e$ gives the stated Gaussian. $\square$

**Claim 7 (joint MAP with a Laplace prior prefers no blur).** For $k \in \mathcal K$ and every $g$, $\lVert Kg\rVert_1 \le \lVert g\rVert_1$. So if $d = Kg$ without noise, the joint MAP cost $C(g, k) = \lVert d - Kg\rVert^2/(2\sigma^2) + \lambda\lVert g\rVert_1$ satisfies $C(d, \delta) \le C(g, k)$: the pair "the data are sharp and there is no blur" is at least as good as the true pair.

*Proof.* $\lVert Kg\rVert_1 = \sum_r |\sum_s k_s g_{r-s}| \le \sum_r\sum_s k_s|g_{r-s}| = \sum_s k_s \sum_r |g_{r-s}| = \lVert g\rVert_1$, by the triangle inequality, $k \ge 0$ and $\sum k = 1$. Then $C(d, \delta) = \lambda\lVert d\rVert_1 = \lambda\lVert Kg\rVert_1 \le \lambda\lVert g\rVert_1 = C(g, k)$. $\square$

The inequality is strict as soon as the blur mixes values of opposite sign, for example at a thin bar.

**Claim 8 (what the covariance term adds).** If $S = cI$, then $\operatorname{tr}(KSK^T) = c\,n\lVert k\rVert^2$. On $\mathcal K$, $\lVert k\rVert^2 \le 1$, with equality only at the vertices, the delta kernels.

*Proof.* $\operatorname{tr}(KK^T)$ is the sum of the squares of all entries of the circulant $K$, and each of its $n$ rows holds the values of $k$ once. On the simplex $\sum k_s^2 \le (\sum k_s)^2 = 1$, with equality only when one entry is $1$. $\square$

So in the simplest case the covariance term of Claim 3 is a penalty on $\lVert k\rVert^2$, which is largest at the delta kernels. The "naive" estimate of the code sets $S = 0$ in lines L5 and L6, which removes this penalty and also uses $\mu_i^2$ in place of $\mathbb E[g_i^2]$. For a general $S$ the term is not a multiple of $\lVert k\rVert^2$, and its effect is a heuristic explanation, not a theorem; the tests record, as a measurement, one run where the naive estimate ends at the delta kernel and the variational one does not.
