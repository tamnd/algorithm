---
tag: NMJ67K
kind: technique
slug: path-coupling
name: Path coupling
aliases:
- Bubley-Dyer path coupling
area: randomized/markov-chain-monte-carlo
level: advanced
summary: If a coupling of each pair of neighboring states shrinks a path metric by a factor e^(-α) per step, then d(t) ≤ e^(-αt) diam. Only neighbors need checking (Bubley and Dyer 1997).
prereqs: [coupling-method, coupling-inequality, mixing-time]
see_also: [coupling-method, coupling-inequality, glauber-dynamics, rapid-mixing, counting-graph-colorings, mixing-time, canonical-paths, hard-core-model]
sources:
  - paper: doi:10.1109/SFCS.1997.646111
    title: Russ Bubley and Martin Dyer, Path coupling, a technique for proving rapid mixing in Markov chains, Proceedings of the 38th Annual Symposium on Foundations of Computer Science (FOCS), 1997
    locator: pages 223 to 231
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 14.1, The Transportation Metric (Lemma 14.3); Section 14.2, Path Coupling (Theorem 14.6, Remark 14.7, Corollary 14.8); Section 14.3, Rapid Mixing for Colorings (Theorem 14.10)
  - paper: doi:10.1002/rsa.3240070205
    title: Mark Jerrum, A very simple algorithm for estimating the number of k-colorings of a low-degree graph, Random Structures and Algorithms 7(2), 1995
    locator: pages 157 to 165
  - paper: doi:10.1063/1.533196
    title: Eric Vigoda, Improved bounds for sampling colorings, Journal of Mathematical Physics 41(3), 2000
    locator: pages 1555 to 1569
---

Path coupling is a way to build and analyze a [coupling](/coupling-method/) of a [Markov chain](/markov-chain/) by looking only at pairs of states that are neighbors in some graph. If, for each such pair, one step of a coupling shrinks the expected distance by a factor $e^{-\alpha}$, then the same holds for every pair of states and every pair of distributions, and the [mixing time](/mixing-time/) is at most about $\alpha^{-1}\log(\mathrm{diam}/\varepsilon)$. Bubley and Dyer introduced it in 1997. It reduced Jerrum's proof that [Glauber dynamics](/glauber-dynamics/) for colorings mixes rapidly to a few lines.

## In plain words

Two copies of a chain can start very far apart, and a direct coupling must say what to do in every case. That is often too complicated to analyze. Path coupling uses a shortcut. Connect the two starting states by a chain of small steps, each step changing only one small part, such as the color of one vertex. Now show that for two states that differ in only one place, one move of the chain, done cleverly in both copies, brings them closer on average. Because distance along the chain of small steps adds up, the same shrinking holds for the far-apart pair. Repeat the move many times, and the distance becomes so small that the copies must agree. Checking only the simple case of one difference is what makes the method so effective.

## When it applies

- The state space $\mathcal X$ can be made the vertex set of a connected graph $G$ with edge lengths at least 1, and $\rho$ is the shortest path metric of $G$. The graph $G$ need not be the graph of transitions of the chain (LPW Remark 14.5).
- For each edge $\{x, y\}$ of $G$ there is a coupling $(X_1, Y_1)$ of $P(x, \cdot)$ and $P(y, \cdot)$ with $\mathbb E_{x, y}[\rho(X_1, Y_1)] \le e^{-\alpha}\rho(x, y)$ for one $\alpha > 0$.
- The typical case is a spin system with single-site updates, with $\rho$ the Hamming distance and neighbors that differ at one site.

The chain may need to be extended to a larger set first. For colorings, the chain is defined on all $q^n$ assignments of colors, not only on proper colorings, so that any two states are joined by a path that changes one vertex at a time.

## The template

The mixing notation is $d(t) = \max_x\|P^t(x, \cdot) - \pi\|_{TV}$, $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$ and $t_{mix} = t_{mix}(1/4)$, and $\mathrm{diam} = \max_{x, y}\rho(x, y)$.

**The transportation metric.** For distributions $\mu, \nu$ on $\mathcal X$, let $\rho_K(\mu, \nu) = \min\{\mathbb E\rho(X, Y) : (X, Y) \text{ a coupling of } \mu, \nu\}$. The minimum exists, because the couplings form a compact set and the expectation is linear in the coupling. Three facts are needed.

1. $\rho_K(\delta_x, \delta_y) = \rho(x, y)$.
2. $\|\mu - \nu\|_{TV} \le \rho_K(\mu, \nu)$, because $\rho(x, y) \ge \mathbf 1\{x \ne y\}$, so $\Pr[X \ne Y] \le \mathbb E\rho(X, Y)$ for each coupling, and the [coupling inequality](/coupling-inequality/) applies.
3. $\rho_K$ satisfies the triangle inequality (LPW Lemma 14.3). *Proof.* Take optimal couplings $\eta_1$ of $(\mu, \nu)$ and $\eta_2$ of $(\nu, \lambda)$. Glue them along the common middle: $\Pr[X = x, Y = y, Z = z] = \eta_1(x, y)\eta_2(y, z)/\nu(y)$ for $\nu(y) > 0$. Then $(X, Z)$ couples $\mu$ and $\lambda$, and $\mathbb E\rho(X, Z) \le \mathbb E\rho(X, Y) + \mathbb E\rho(Y, Z)$. $\square$

**Theorem (Bubley and Dyer 1997; LPW Theorem 14.6).** Under the conditions above, $\rho_K(\mu P, \nu P) \le e^{-\alpha}\rho_K(\mu, \nu)$ for all distributions $\mu, \nu$.

*Proof.*

1. *All pairs of states.* Fix $x, y$ and a shortest path $x = x_0, x_1, \ldots, x_r = y$ in $G$. By the triangle inequality for $\rho_K$ and the edge hypothesis,
$$
\rho_K(P(x, \cdot), P(y, \cdot)) \le \sum_{k=1}^r\rho_K(P(x_{k-1}, \cdot), P(x_k, \cdot)) \le e^{-\alpha}\sum_{k=1}^r\ell(x_{k-1}, x_k) = e^{-\alpha}\rho(x, y).
$$
The last equality holds because the path is a shortest one.
2. *All pairs of distributions.* Let $(X_0, Y_0)$ be an optimal coupling of $\mu$ and $\nu$. Given $(X_0, Y_0) = (x, y)$, draw $(X_1, Y_1)$ from an optimal coupling of $P(x, \cdot)$ and $P(y, \cdot)$. Then $X_1 \sim \mu P$, $Y_1 \sim \nu P$, and by step 1, $\mathbb E\rho(X_1, Y_1) \le e^{-\alpha}\mathbb E\rho(X_0, Y_0) = e^{-\alpha}\rho_K(\mu, \nu)$. $\square$

**Corollary (LPW Corollary 14.8).** $d(t) \le e^{-\alpha t}\,\mathrm{diam}$, so
$$
t_{mix}(\varepsilon) \le \Big\lceil\frac{\log\mathrm{diam} - \log\varepsilon}{\alpha}\Big\rceil.
$$

*Proof.* The theorem shows that $\mu \mapsto \mu P$ is a contraction for $\rho_K$, so there is exactly one stationary distribution $\pi$: two stationary laws $\pi, \pi'$ satisfy $\rho_K(\pi, \pi') \le e^{-\alpha}\rho_K(\pi, \pi')$, so $\rho_K(\pi, \pi') = 0$. Iterating the theorem with $\mu = \delta_x$ and $\nu = \pi = \pi P^t$, and using facts 1 and 2,
$$
\|P^t(x, \cdot) - \pi\|_{TV} \le \rho_K(\delta_xP^t, \pi P^t) \le e^{-\alpha t}\rho_K(\delta_x, \pi) \le e^{-\alpha t}\,\mathrm{diam}. \quad\square
$$

Irreducibility is not assumed, and $\pi$ may live on a proper subset of $\mathcal X$ (LPW Remark 14.7). That is what allows the extension to improper colorings.

**The steps in practice.**

1. Choose the graph $G$ and the lengths. Usually $G$ joins states that differ at one site, all lengths are 1, and $\rho$ is the Hamming distance, with $\mathrm{diam} = n$.
2. For two neighbors $x, y$, which differ at one site $v$, couple one step so that the two copies make the same move whenever the move does not depend on $v$.
3. Compute $\mathbb E\rho(X_1, Y_1)$: the chance that $v$ is fixed, minus 1, plus the chance that a new difference appears.
4. Find $\alpha$ with $\mathbb E\rho(X_1, Y_1) \le 1 - \alpha \le e^{-\alpha}$, and apply the corollary.

## Classic examples

### Glauber dynamics for colorings, q > 2Δ

Let $G$ have $n$ vertices and maximum degree $\Delta$, and let $q > 2\Delta$. Glauber dynamics picks a uniform vertex $w$ and gives it a uniform color from $A_w(x)$, the colors not used by the neighbors of $w$. Define it on all $q^n$ colorings; $A_w(x)$ has at least $q - \Delta \ge 1$ elements. Its stationary distribution is uniform on proper colorings. Let $\rho$ be the Hamming distance, and let $x, y$ differ only at $v$ (LPW Theorem 14.10).

- If $w = v$, probability $1/n$: $A_v(x) = A_v(y)$, the copies take the same color, and $\rho$ drops to 0.
- If $w$ is neither $v$ nor a neighbor of $v$: again $A_w(x) = A_w(y)$, and $\rho$ stays 1.
- If $w$ is a neighbor of $v$, probability $\deg(v)/n$: the sets $A_w(x)$ and $A_w(y)$ differ by at most the colors $x(v)$ and $y(v)$. Draw the color for $y$ uniformly from $A_w(y)$ and use it for $x$ unless it is $x(v)$, in which case use a correction that keeps the law of $x$ uniform on $A_w(x)$. The copies disagree at $w$ with probability at most $1/|A_w(y)| \le 1/(q - \Delta)$.

Hence
$$
\mathbb E_{x, y}\rho(X_1, Y_1) \le 1 - \frac1n + \frac{\Delta}{n(q - \Delta)} = 1 - \frac{c}{n}, \qquad c = \frac{q - 2\Delta}{q - \Delta} > 0,
$$
and the corollary with $\alpha = c/n$ and $\mathrm{diam} = n$ gives
$$
t_{mix}(\varepsilon) \le \Big\lceil\frac{q - \Delta}{q - 2\Delta}\,n(\log n - \log\varepsilon)\Big\rceil.
$$
This is the bound of Jerrum (1995), whose original proof was a longer direct coupling.

Exact values for small graphs, from the exact transition matrix on proper colorings and $\varepsilon = 1/4$:

| graph | $q$ | $\Delta$ | proper colorings | exact $t_{mix}$ | path coupling bound |
|---|---|---|---|---|---|
| one edge | 3 | 1 | 6 | 4 | 9 |
| path with 3 vertices | 5 | 2 | 80 | 6 | 23 |
| triangle | 5 | 2 | 60 | 7 | 23 |

### The lazy hypercube

Let neighbors differ in one coordinate, and couple by choosing the same coordinate and the same bit. For neighbors differing at coordinate $i$, the distance drops to 0 if $i$ is chosen and stays 1 otherwise, so $\mathbb E\rho = 1 - 1/n$. With $\alpha = 1/n$ and $\mathrm{diam} = n$, $t_{mix}(\varepsilon) \le \lceil n(\log n - \log\varepsilon)\rceil$, which is 8 for $n = 3$; the exact value is 3. Here path coupling recovers the direct coupling bound with no work on far-apart pairs.

## Variations

- **Non-contracting couplings.** If only $\mathbb E\rho(X_1, Y_1) \le \rho(x, y)$ holds, so $\alpha = 0$, Bubley and Dyer also gave a bound of order $\mathrm{diam}^2/\kappa$ times $\log(1/\varepsilon)$, provided the distance changes with probability at least $\kappa$ at each step. This is the analogue of Lemma B on [coupling method](/coupling-method/).
- **Other chains, then comparison.** Vigoda (2000) applied path coupling to a chain that recolors whole two-colored components (Kempe components) at once, and proved $O(n\log n)$ mixing for $q > \tfrac{11}6\Delta$. A comparison of Dirichlet forms then gave $O(n^2)$ mixing for Glauber dynamics in the same range. Chen, Delcourt, Moitra, Perarnau and Postle (2019) lowered the constant $\tfrac{11}6$ slightly.
- **Weighted metrics.** Lengths other than 1, or a weight per site, can turn a non-contracting coupling into a contracting one. The proof of the theorem is unchanged.
- **Several steps at once.** Apply the theorem to $P^T$ in place of $P$ when one step does not contract but $T$ steps do.

## Pitfalls

- **The metric must be a path metric.** Step 1 of the proof walks along a shortest path in $G$ and uses $\rho(x, y) = \sum\ell(x_{k-1}, x_k)$. For a metric that is not the path metric of the graph on which the edge couplings are defined, the argument fails.
- **Every edge must contract.** One edge with $\mathbb E\rho > e^{-\alpha}\rho$ breaks the theorem, even if the average edge contracts.
- **The state space may need extending.** With proper colorings only, two colorings at Hamming distance $k$ need not be joined by $k$ single-site changes through proper colorings. Working on all colorings avoids this, but then the chain must be defined there, and one must check that its unique stationary distribution is the intended one.
- **Correct marginals in the edge coupling.** In the coloring coupling, the copy with the smaller set of allowed colors needs a correction step, or its color is not uniform on its allowed set.
- **The bound is only an upper bound.** For the small cases in the table it is 2 to 4 times the true value.

## Exercises

1. Show that $\rho_K(\delta_x, \delta_y) = \rho(x, y)$ and that $\rho_K(\mu, \nu) = \|\mu - \nu\|_{TV}$ when $\rho(x, y) = \mathbf 1\{x \ne y\}$.
2. Complete the coloring coupling: when $|A_w(x)| < |A_w(y)|$ and the color $U$ drawn for $y$ equals $x(v)$, draw the color for $x$ uniformly from $A_w(x)$. Check that the color of $x$ is then uniform on $A_w(x)$.
3. For the lazy walk on a path with $n$ vertices and $\rho(x, y) = |x - y|$, show that every coupling of two interior neighbors has $\mathbb E\rho(X_1, Y_1) \ge 1$. So path coupling with this metric cannot give $\alpha > 0$.
4. Compute the path coupling bound for Glauber dynamics on 5-colorings of the path with 3 vertices at $\varepsilon = 1/4$, and confirm that it is 23.
5. Use the theorem to show that, for $q > 2\Delta$, Glauber dynamics on all $q^n$ colorings has exactly one stationary distribution, although it is not irreducible on that set.

## References
