---
tag: 5K8746
kind: technique
slug: canonical-paths
name: Canonical paths method
aliases:
- canonical path argument
area: randomized/markov-chain-monte-carlo
level: advanced
summary: Route a path of transitions between each pair of states so that no transition carries too much weight. If the congestion is B, the spectral gap is at least 1/B.
prereqs: [spectral-gap, conductance, detailed-balance]
see_also: [spectral-gap, conductance, cheeger-inequality, rapid-mixing, mixing-time, counting-perfect-matchings, permanent-computation, path-coupling]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 13.4, The Path Method (Theorem 13.20, Corollary 13.21, Section 13.4.1 on averaging over paths); Notes to Chapter 13
  - paper: doi:10.1137/0218077
    title: Mark Jerrum and Alistair Sinclair, Approximating the permanent, SIAM Journal on Computing 18(6), 1989
    locator: the canonical path argument for the matching chain
  - paper: doi:10.1214/aoap/1177005980
    title: Persi Diaconis and Daniel Stroock, Geometric bounds for eigenvalues of Markov chains, Annals of Applied Probability 1(1), 1991
    locator: pages 36 to 61 (the Poincaré inequality with path lengths)
  - paper: doi:10.1017/S0963548300000390
    title: Alistair Sinclair, Improved bounds for mixing rates of Markov chains and multicommodity flow, Combinatorics, Probability and Computing 1(4), 1992
    locator: pages 351 to 370 (the bound with path length and multicommodity flows)
  - book: isbn:9783764369460
    title: Mark Jerrum, Counting, Sampling and Integrating, Algorithms and Complexity, Birkhäuser, 2003
    locator: Chapter 5, Canonical paths and applications
---

The canonical paths method bounds the [spectral gap](/spectral-gap/) of a reversible [Markov chain](/markov-chain/) from below, and so its [mixing time](/mixing-time/) from above. For each ordered pair of states $(x, y)$ one chooses a path of allowed transitions from $x$ to $y$. If no transition is used by too many heavy paths, the chain has no bottleneck, and the gap is at least the inverse of the worst load. The method was introduced by Jerrum and Sinclair (1989) to prove rapid mixing of a chain on matchings, and Diaconis and Stroock (1991) gave it the form used here.

## In plain words

To show that a road network has no traffic jam, plan a route for every trip from every town to every other town, and add up how much traffic each road must carry. If every road carries only a modest load compared with its width, there is no narrow pass where traffic must squeeze through. For a Markov chain, the towns are the states, the roads are the allowed moves, and the width of a road is how often the chain uses it at equilibrium. A good set of routes proves that the chain has no bottleneck, and that proves that it mixes fast. The work is in choosing the routes cleverly and then counting how many of them pass through each road, which is often done by an encoding trick that maps routes to states.

## When it applies

- The chain is reversible with respect to $\pi$, so that the gap $\gamma = 1 - \lambda_2$ controls mixing (see [detailed balance](/detailed-balance/)).
- There is a natural way to turn any state into any other by allowed moves, for example by fixing positions one at a time.
- One can bound, for each transition, the total stationary weight of the pairs whose paths use it. Usually this is done with an injective or few-to-one map from those pairs to states.
- To get a mixing bound, the gap is passed to LPW Theorem 12.4, which needs the absolute gap. So the chain should be lazy, or its smallest eigenvalue should be controlled separately.

The method gives lower bounds on $\gamma$ only. To show that a chain is slow, use the bottleneck bound on [conductance](/conductance/) instead.

## The template

Let $P$ be reversible and irreducible on a finite set $\mathcal X$ with stationary distribution $\pi$. Let $E = \{(z, w) : P(z, w) > 0, z \ne w\}$ be the set of directed edges, with $Q(z, w) = \pi(z)P(z, w)$. For each ordered pair $x \ne y$ choose a path $\Gamma_{xy}$ from $x$ to $y$ that uses edges of $E$, with length $|\Gamma_{xy}|$. Define the *congestion*
$$
B = \max_{e \in E}\frac1{Q(e)}\sum_{(x, y) : e \in \Gamma_{xy}}\pi(x)\pi(y)|\Gamma_{xy}|.
$$

**Theorem (LPW Corollary 13.21; Diaconis and Stroock 1991).** $\gamma \ge 1/B$.

*Proof.* For a function $f$ and an edge $e = (z, w)$ let $\nabla f(e) = f(w) - f(z)$. Along the path $\Gamma_{xy}$ the increments add up: $f(y) - f(x) = \sum_{e \in \Gamma_{xy}}\nabla f(e)$. By the Cauchy-Schwarz inequality,
$$
(f(y) - f(x))^2 \le |\Gamma_{xy}|\sum_{e \in \Gamma_{xy}}\nabla f(e)^2.
$$
Multiply by $\pi(x)\pi(y)$, sum over all ordered pairs, and change the order of summation:
$$
2\operatorname{Var}_\pi(f) = \sum_{x, y}\pi(x)\pi(y)(f(y) - f(x))^2 \le \sum_{e \in E}\nabla f(e)^2\sum_{(x, y) : e \in \Gamma_{xy}}\pi(x)\pi(y)|\Gamma_{xy}| \le B\sum_{e \in E}Q(e)\nabla f(e)^2 = 2B\,\mathcal E(f),
$$
where $\mathcal E(f) = \frac12\sum_{z, w}Q(z, w)(f(z) - f(w))^2$ is the Dirichlet form. So $\mathcal E(f)/\operatorname{Var}_\pi(f) \ge 1/B$ for each non-constant $f$, and the variational form of the gap on [spectral gap](/spectral-gap/) gives $\gamma \ge 1/B$. $\square$

**The steps in practice.**

1. Choose the paths $\Gamma_{xy}$.
2. Fix a transition $e = (z, w)$, and describe the set $\mathrm{cp}(e)$ of pairs $(x, y)$ whose path uses it.
3. Bound $\sum_{(x, y) \in \mathrm{cp}(e)}\pi(x)\pi(y)$, often by an injection $\eta_e : \mathrm{cp}(e) \to \mathcal X$ with $\pi(x)\pi(y) \le c\,\pi(z)\pi(\eta_e(x, y))$. Then the sum is at most $c\,\pi(z)$.
4. Bound $|\Gamma_{xy}| \le L$, and conclude $B \le cL/\min_eP(e)$.
5. For a lazy chain, use $t_{rel} \le B$ in LPW Theorem 12.4: $t_{mix}(\varepsilon) \le \lceil B(\tfrac12\log\frac1{\pi_{min}} + \log\frac1{2\varepsilon})\rceil$.

**The two older forms.** Let $\bar\rho = \max_e\frac1{Q(e)}\sum_{e \in \Gamma_{xy}}\pi(x)\pi(y)$, the congestion without the lengths, and $L = \max|\Gamma_{xy}|$.

- *Jerrum and Sinclair (1989): $\Phi_* \ge 1/(2\bar\rho)$, hence $\gamma \ge 1/(8\bar\rho^2)$ by the [Cheeger inequality](/cheeger-inequality/).* Proof: for $S$ with $\pi(S) \le 1/2$, each path from $S$ to $S^c$ crosses an edge from $S$ to $S^c$, so $\pi(S)\pi(S^c) = \sum_{x \in S, y \notin S}\pi(x)\pi(y) \le \sum_{e \in E(S, S^c)}\bar\rho\,Q(e) = \bar\rho\,Q(S, S^c)$. With $\pi(S^c) \ge 1/2$, $Q(S, S^c)/\pi(S) \ge 1/(2\bar\rho)$. $\square$
- *Sinclair (1992): $\gamma \ge 1/(\bar\rho L)$*, because $B \le \bar\rho L$.

## Classic examples

### The hypercube with bit fixing

Take the lazy walk on $\{0, 1\}^n$: pick a coordinate $i$ uniformly and set it to a fair bit. Then $\pi(x) = 2^{-n}$ and $Q(e) = 2^{-n}/(2n)$ for each edge $(z, z \oplus e_i)$. Let $\Gamma_{xy}$ fix the differing bits from left to right.

A path uses the edge $(z, z \oplus e_i)$ exactly when $x$ agrees with $z$ on the bits $i, \ldots, n$ and $y$ agrees with $z \oplus e_i$ on the bits $1, \ldots, i$. So $x$ is free on $i - 1$ bits and $y$ on $n - i$ bits: $2^{n-1}$ pairs. Hence $\bar\rho = 2^{n-1}2^{-2n}\cdot 2n\,2^n = n$, and Jerrum-Sinclair gives $\Phi_* \ge 1/(2n)$, which is the exact value. For $B$, the path length is the Hamming distance, which is on average $1 + \frac{i - 1}2 + \frac{n - i}2 = \frac{n + 1}2$ over these pairs, so $B = n(n+1)/2$ and $\gamma \ge 2/(n(n + 1))$.

| $n$ | $B$ | $1/B$ | true $\gamma$ | $1/(\bar\rho L) = 1/n^2$ | $1/(8\bar\rho^2)$ |
|---|---|---|---|---|---|
| 2 | 3 | 0.333 | 0.5 | 0.25 | 0.031 |
| 3 | 6 | 0.167 | 0.333 | 0.111 | 0.014 |
| 4 | 10 | 0.1 | 0.25 | 0.0625 | 0.0078 |

These values were computed exactly by listing all paths. The bound $1/B$ is off by the factor $(n + 1)/2$; the true gap is $1/n$.

### The lazy path

On the lazy walk on a path with $n$ vertices, the only paths are the direct ones. For $n = 5$, $B = 8$, so $\gamma \ge 0.125$, against the true $\gamma = 0.1464$. For $n = 7$, $B = 18$, so $\gamma \ge 0.0556$, against $0.0670$. Here the method is nearly tight.

### Matchings and the permanent

Jerrum and Sinclair (1989) studied a chain on all matchings of a graph, weighted by $\lambda^{|M|}$, with moves that add an edge, remove an edge, or swap one edge for another at a shared vertex. The canonical path from $M$ to $M'$ processes the components of the symmetric difference $M \oplus M'$, which are paths and cycles, one at a time in a fixed order, and unwinds each component edge by edge. For each transition, an encoding built from $M \oplus M'$ and the ends of the transition is nearly injective, and it bounds the congestion by a polynomial. This proved rapid mixing for the chain on matchings, and with more work an FPRAS for [counting perfect matchings](/counting-perfect-matchings/) in dense bipartite graphs, that is, for the [permanent](/permanent-computation/) of dense 0-1 matrices.

### Other uses

Jerrum and Sinclair (1993) used canonical paths for a chain on the subgraphs of a graph, which gives an FPRAS for the partition function of the ferromagnetic [Ising model](/ising-model/). The book of Jerrum (2003), Chapter 5, has further examples.

## Variations

- **Multicommodity flows (Sinclair 1992).** Instead of one path per pair, send the demand $\pi(x)\pi(y)$ along several paths, split in any way. The same proof works with the flow on each edge in place of the sum over paths, and spreading the load can remove the effect of a few overloaded edges.
- **Comparison of chains (LPW Theorem 13.20).** Route each transition of a chain $\tilde P$ with a known gap by paths in $P$. Then $\gamma \ge \tilde\gamma/B'$ for a congestion $B'$ of the routing. Canonical paths are the special case where $\tilde P(x, y) = \pi(y)$, whose gap is 1. Diaconis and Saloff-Coste used comparison for random walks on groups.
- **Weighted lengths.** Diaconis and Stroock (1991) allow each edge a length, which gives a family of bounds of the same shape.

## Pitfalls

- **Forgetting the absolute gap.** Corollary 13.21 bounds $\gamma = 1 - \lambda_2$. A chain with an eigenvalue near $-1$ can have a good bound and still mix slowly. Make the chain lazy, or bound $\lambda_{min}$ separately.
- **Counting ordered pairs.** $B$ sums over ordered pairs $(x, y)$, and the edges are directed. Mixing conventions changes the constant by a factor of 2.
- **The length factor.** The bound with $B$ includes $|\Gamma_{xy}|$, and the bound with $\bar\rho$ does not. Using $\bar\rho$ in $\gamma \ge 1/B$ is wrong; it needs the factor $L$ or the square from Cheeger.
- **Paths must use real transitions.** Each edge of $\Gamma_{xy}$ must have $P(z, w) > 0$. An edge with tiny $P(z, w)$ has tiny $Q(e)$ and can dominate $B$.
- **Loose bounds.** The method can lose a polynomial factor. For the hypercube it gives $1/B = 2/(n(n + 1))$ against the truth $1/n$. Coupling often gives sharper results when it applies.

## Exercises

1. For the lazy walk on a cycle with $n$ vertices, route each pair along the shorter arc. Show that $B$ is of order $n^2$, and compare with $\gamma \approx \pi^2/n^2$.
2. For the lazy walk on the complete graph $K_n$, use the direct edge as the path for each pair. Show that $1/B = n/(2(n - 1))$, which is the exact gap.
3. Prove the Jerrum-Sinclair bound $\Phi_* \ge 1/(2\bar\rho)$ for a chain that is not reversible, and explain why it does not then give a mixing bound through the Cheeger inequality.
4. For the lazy hypercube, show that every choice of paths, and every multicommodity flow, has $B \ge n(n + 1)/2$. (Hint: the total load over all $n2^n$ directed edges is at least $\sum_{x, y}\pi(x)\pi(y)H(x, y)^2$, where $H$ is the Hamming distance.) So the method cannot reach the true order $1/n$ here.

## References
