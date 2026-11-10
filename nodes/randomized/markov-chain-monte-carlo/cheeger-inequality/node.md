---
tag: VBEAG1
kind: theorem
slug: cheeger-inequality
name: Cheeger inequality for Markov chains
aliases:
- Cheeger bound
- Jerrum-Sinclair bound
area: randomized/markov-chain-monte-carlo
level: advanced
summary: For a reversible chain with conductance Φ* and spectral gap γ = 1 − λ2, Φ*²/2 ≤ γ ≤ 2Φ*. So the gap is small exactly when the chain has a bottleneck.
prereqs: [conductance, spectral-gap, detailed-balance]
see_also: [conductance, spectral-gap, canonical-paths, mixing-time, rapid-mixing, graph-conductance, laplacian-matrix, rayleigh-quotient]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 13.2, The Dirichlet Form and the Bottleneck Ratio (Lemma 13.7, Remark 13.8, Theorem 13.10, equation (13.6), Examples 13.11 and 13.12); Notes to Chapter 13
  - paper: doi:10.1016/0890-5401(89)90067-9
    title: Alistair Sinclair and Mark Jerrum, Approximate counting, uniform generation and rapidly mixing Markov chains, Information and Computation 82(1), 1989
    locator: pages 93 to 133 (the bound of the spectral gap by the conductance)
  - paper: doi:10.1090/S0002-9947-1988-0930082-9
    title: Gregory F. Lawler and Alan D. Sokal, Bounds on the L2 spectrum for Markov chains and Markov processes, a generalization of Cheeger's inequality, Transactions of the American Mathematical Society 309(2), 1988
    locator: pages 557 to 580
  - paper: doi:10.1007/BF02579166
    title: Noga Alon, Eigenvalues and expanders, Combinatorica 6(2), 1986
    locator: pages 83 to 96 (inequalities of this kind for graphs)
  - paper: "Jeff Cheeger, A lower bound for the smallest eigenvalue of the Laplacian, in Problems in Analysis, a symposium in honor of Salomon Bochner, Princeton University Press, 1970"
    locator: the original inequality for Riemannian manifolds
---

The Cheeger inequality for Markov chains says that a reversible chain has a small [spectral gap](/spectral-gap/) exactly when it has a bottleneck, a set of states that is hard to leave. In numbers, the gap $\gamma = 1 - \lambda_2$ and the [conductance](/conductance/) $\Phi_*$ satisfy $\Phi_*^2/2 \le \gamma \le 2\Phi_*$. The upper bound is a one-line test function argument. The lower bound is the useful one for algorithms: it turns a combinatorial bound on bottlenecks into a bound on the [mixing time](/mixing-time/).

## Statement

Let $P$ be a transition matrix on a finite set $\mathcal X$, reversible with respect to $\pi$ (see [detailed balance](/detailed-balance/)), with $\pi(x) > 0$ for all $x$. Let $Q(x, y) = \pi(x)P(x, y)$, $Q(A, B) = \sum_{x \in A, y \in B}Q(x, y)$,
$$
\Phi_* = \min_{S : 0 < \pi(S) \le 1/2}\frac{Q(S, S^c)}{\pi(S)},
$$
and let $\gamma = 1 - \lambda_2$, where $\lambda_2$ is the second largest eigenvalue of $P$.

**Theorem (LPW Theorem 13.10; Sinclair and Jerrum 1989, Lawler and Sokal 1988).**
$$
\frac{\Phi_*^2}{2} \le \gamma \le 2\Phi_*.
$$

The theorem is about $\gamma$, not the absolute gap $\gamma_* = 1 - \max_{j \ge 2}|\lambda_j|$. A chain can have a large $\gamma$ and still not mix because of an eigenvalue near $-1$; for lazy chains the two gaps are equal. The notation for mixing is $d(t) = \max_x\|P^t(x, \cdot) - \pi\|_{TV}$, $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$ and $t_{mix} = t_{mix}(1/4)$.

## In plain words

A chain can be slow for only one reason that matters here: some large group of states has little traffic to the rest. The theorem says that this reason is also the only one. If no group of states is hard to leave, the chain cannot be slow by much, and if some group is hard to leave, the chain must be slow. The two directions are not equally sharp. A bottleneck slows the chain by about the size of the bottleneck. The absence of bottlenecks guarantees speed only up to a square: if the worst door lets through a fraction of one percent, the chain could be as slow as that fraction squared.

## Proof

Both directions use the variational form of the gap (LPW Lemma 13.7 and Remark 13.8, proved on [spectral gap](/spectral-gap/)): with $\langle f, g\rangle_\pi = \sum_x\pi(x)f(x)g(x)$, $\|f\|_2^2 = \langle f, f\rangle_\pi$ and the Dirichlet form
$$
\mathcal E(f) = \langle(I - P)f, f\rangle_\pi = \frac12\sum_{x, y}Q(x, y)\big(f(x) - f(y)\big)^2,
$$
$$
\gamma = \min\Big\{\frac{\mathcal E(f)}{\operatorname{Var}_\pi(f)} : f \text{ not constant}\Big\}.
$$
The second expression for $\mathcal E$ uses the symmetry $Q(x, y) = Q(y, x)$ and $\sum_yQ(x, y) = \pi(x)$.

**Upper bound, $\gamma \le 2\Phi_*$.** Take $S$ with $0 < \pi(S) \le 1/2$ and let $f = 1_S$. The term $(f(x) - f(y))^2$ is 1 when exactly one of $x, y$ is in $S$ and 0 otherwise, so $\mathcal E(f) = \frac12\big(Q(S, S^c) + Q(S^c, S)\big) = Q(S, S^c)$. Also $\operatorname{Var}_\pi(f) = \pi(S)(1 - \pi(S)) \ge \pi(S)/2$. So
$$
\gamma \le \frac{Q(S, S^c)}{\pi(S)/2} = 2\,\frac{Q(S, S^c)}{\pi(S)}.
$$
Minimize over $S$. $\square$

**Lower bound, $\gamma \ge \Phi_*^2/2$.** Let $f_2$ be a real eigenfunction with $Pf_2 = \lambda_2f_2$. It is orthogonal to the constants, so $\sum_x\pi(x)f_2(x) = 0$, and it takes both signs. Replacing $f_2$ by $-f_2$ if needed, assume $\pi(\{f_2 > 0\}) \le 1/2$. Let $\psi = \max(f_2, 0)$; it is not 0.

*Step 1: $\mathcal E(\psi) \le \gamma\|\psi\|_2^2$.* Since $\psi \ge f_2$ and $P$ has non-negative entries, $P\psi \ge Pf_2 = \lambda_2f_2$. So at each $x$ with $\psi(x) > 0$,
$$
(I - P)\psi(x) \le f_2(x) - \lambda_2f_2(x) = \gamma\psi(x).
$$
Multiply by $\pi(x)\psi(x) \ge 0$ and sum over $x$; the points with $\psi(x) = 0$ add nothing. This gives $\mathcal E(\psi) = \langle(I - P)\psi, \psi\rangle_\pi \le \gamma\|\psi\|_2^2$.

*Step 2: $\Phi_*\|\psi\|_2^2 \le \sqrt{2\mathcal E(\psi)}\,\|\psi\|_2$.* Let
$$
I = \sum_{(x, y) : \psi(x) > \psi(y)}Q(x, y)\big(\psi(x)^2 - \psi(y)^2\big).
$$
For $t > 0$ let $S_t = \{x : \psi(x)^2 > t\}$. Each $S_t$ lies inside $\{f_2 > 0\}$, so $\pi(S_t) \le 1/2$, and by the definition of $\Phi_*$, $Q(S_t, S_t^c) \ge \Phi_*\pi(S_t)$. Write $\psi(x)^2 - \psi(y)^2 = \int_0^\infty 1\{\psi(y)^2 \le t < \psi(x)^2\}\,dt$ and exchange the sum and the integral:
$$
I = \int_0^\infty Q(S_t, S_t^c)\,dt \ge \Phi_*\int_0^\infty\pi(S_t)\,dt = \Phi_*\sum_x\pi(x)\psi(x)^2 = \Phi_*\|\psi\|_2^2.
$$
For the upper bound, factor $\psi(x)^2 - \psi(y)^2 = (\psi(x) - \psi(y))(\psi(x) + \psi(y))$ and use the Cauchy-Schwarz inequality:
$$
I \le \Big(\sum_{\psi(x) > \psi(y)}Q(x, y)(\psi(x) - \psi(y))^2\Big)^{1/2}\Big(\sum_{\psi(x) > \psi(y)}Q(x, y)(\psi(x) + \psi(y))^2\Big)^{1/2}.
$$
The first sum is $\mathcal E(\psi)$, because by symmetry of $Q$ each unordered pair with $\psi(x) \ne \psi(y)$ appears once here and twice in $\frac12\sum_{x, y}$. For the second, $(a + b)^2 \le 2a^2 + 2b^2$, and each unordered pair appears at most once, while $\sum_{x, y}Q(x, y)(\psi(x)^2 + \psi(y)^2) = 2\|\psi\|_2^2$ counts it twice; so the second sum is at most $2\|\psi\|_2^2$. Hence $I \le \sqrt{\mathcal E(\psi)}\cdot\sqrt2\,\|\psi\|_2$.

*Step 3.* Steps 1 and 2 give $\Phi_*\|\psi\|_2 \le \sqrt{2\mathcal E(\psi)} \le \sqrt{2\gamma}\,\|\psi\|_2$, so $\Phi_*^2 \le 2\gamma$. $\square$

## Consequences

**Mixing time from conductance.** For a lazy reversible chain, $\gamma_* = \gamma \ge \Phi_*^2/2$, so $t_{rel} \le 2/\Phi_*^2$, and LPW Theorem 12.4 gives
$$
\frac1{4\Phi_*} \le t_{mix} \le \Big\lceil\frac2{\Phi_*^2}\Big(\frac12\log\frac1{\pi_{min}} + \log 2\Big)\Big\rceil,
$$
where the left side is the bottleneck bound of LPW Theorem 7.4 on [conductance](/conductance/).

**A characterization of rapid mixing.** Consider a family of lazy reversible chains with $\log(1/\pi_{min})$ polynomial in $\log|\mathcal X|$. By the two bounds above, $t_{mix}$ is polynomial in $\log|\mathcal X|$ if and only if $1/\Phi_*$ is. This is the form in which Sinclair and Jerrum stated [rapid mixing](/rapid-mixing/), and it reduced proofs of rapid mixing to lower bounds on $\Phi_*$, for example by [canonical paths](/canonical-paths/).

**Graphs.** For the simple random walk on a $d$-regular graph, $P = A/d$, where $A$ is the [adjacency matrix](/adjacency-matrix/) with eigenvalues $d = \mu_1 \ge \mu_2 \ge \cdots$. Then $\gamma = (d - \mu_2)/d$, where $d - \mu_2$ is the second smallest eigenvalue of the [Laplacian matrix](/laplacian-matrix/), and $\Phi(S) = h(S)/d$ with $h(S) = |E(S, S^c)|/|S|$. The theorem becomes
$$
\frac{h^2}{2d} \le d - \mu_2 \le 2h, \qquad h = \min_{0 < |S| \le n/2}h(S).
$$
Inequalities of this kind for graphs are due to Alon and Milman (1985) and Alon (1986). They are the reason that expansion and the eigenvalue gap of a graph are equivalent up to a square. See [graph conductance](/graph-conductance/).

**Spectral partitioning.** The proof of the lower bound is constructive. Run Step 2 with $\Phi_{min} = \min_t\Phi(S_t)$ in place of $\Phi_*$: it shows that some set $S_t = \{x : f_2(x) > \sqrt t\}$ has $\Phi(S_t) \le \sqrt{2\gamma}$. So sorting the states by $f_2$ and trying each prefix of the positive part finds a set with conductance at most $\sqrt{2\gamma} \le 2\sqrt{\Phi_*}$. This "sweep cut" is the basis of spectral graph partitioning.

## Tightness

Both sides of the theorem are attained in order, by different chains. The values below were found exactly, with $\Phi_*$ by trying all subsets.

| Chain | $\Phi_*$ | $\Phi_*^2/2$ | $\gamma$ | $2\Phi_*$ |
|---|---|---|---|---|
| Land of Oz | $1/2$ | $0.125$ | $0.75$ | $1$ |
| lazy path, 3 vertices | $1/2$ | $0.125$ | $0.5$ | $1$ |
| lazy hypercube, $n = 3$ | $1/6$ | $0.0139$ | $1/3$ | $1/3$ |
| lazy hypercube, $n = 4$ | $1/8$ | $0.0078$ | $1/4$ | $1/4$ |
| lazy cycle, 8 vertices | $1/8$ | $0.0078$ | $0.1464$ | $0.25$ |
| two triangles joined by an edge, lazy | $1/14$ | $0.00255$ | $0.1023$ | $0.1429$ |
| two copies of $K_4$ joined by an edge, lazy | $1/26$ | $0.00074$ | $0.0567$ | $0.0769$ |

- **The upper bound is exact for the hypercube (LPW Example 13.11).** For the lazy walk on $\{0, 1\}^n$, $\Phi_* = 1/(2n)$ and $\gamma = 1/n = 2\Phi_*$.
- **The lower bound has the right order for cycles (LPW Example 13.12).** For the lazy walk on a cycle with $n$ vertices, $n$ even, the worst set is an arc of $n/2$ vertices, with $\Phi_* = 1/n$, while $\gamma = (1 - \cos(2\pi/n))/2 \approx \pi^2/n^2$. So $\gamma$ is of order $\Phi_*^2$, and no bound of the form $\gamma \ge c\,\Phi_*$ can hold for all chains.
- **Reversibility is needed.** For a chain that is not reversible, $\lambda_2$ can be complex, and the variational form fails. The bottleneck bound $t_{mix} \ge 1/(4\Phi_*)$ still holds, because its proof does not use reversibility.

## History

Jeff Cheeger (1970) proved a lower bound on the first non-zero eigenvalue of the Laplacian of a compact Riemannian manifold in terms of an isoperimetric constant, which is why $\Phi_*$ is often called the Cheeger constant. Noga Alon and Vitali Milman (1985) and Alon (1986) proved inequalities of this type for graphs, in the study of expanders. Lawler and Sokal (1988), and Sinclair and Jerrum (1989), extended them to reversible Markov chains (LPW, Notes to Chapter 13). Jerrum and Sinclair used the lower bound, together with canonical paths, to prove that the chain on matchings mixes rapidly, which gave an [FPRAS](/fpras/) for the [permanent](/permanent-computation/) of dense 0-1 matrices.

## References
