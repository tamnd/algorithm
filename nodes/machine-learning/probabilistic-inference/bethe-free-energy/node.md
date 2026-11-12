---
tag: QK8KM6
kind: definition
slug: bethe-free-energy
name: Bethe free energy
aliases:
- Bethe approximation
- Bethe variational problem
- Bethe entropy approximation
area: machine-learning/probabilistic-inference
level: advanced
summary: "F_Bethe(b) = sum_a sum b_a log(b_a/f_a) - sum_i (d_i - 1) sum b_i log b_i on the local polytope. Exact on trees, not convex in general; loopy BP fixed points are its stationary points."
prereqs: [factor-graph, partition-function, belief-propagation, shannon-entropy]
see_also: [loopy-belief-propagation, generalized-belief-propagation, tree-reweighted-belief-propagation, mean-field-approximation, evidence-lower-bound, marginal-inference, ising-model, convex-function]
sources:
  - paper: doi:10.1098/rspa.1935.0122
    title: "Hans A. Bethe, Statistical theory of superlattices, Proceedings of the Royal Society of London A 150(871), 1935"
    locator: the approximation of the configurations of an alloy lattice that treats each site with its nearest neighbors exactly and ignores longer correlations
  - paper: doi:10.1109/TIT.2005.850085
    title: "Jonathan S. Yedidia, William T. Freeman and Yair Weiss, Constructing free-energy approximations and generalized belief propagation algorithms, IEEE Transactions on Information Theory 51(7), 2005, pages 2282 to 2312"
    locator: "the Bethe free energy of a factor graph, its exactness on trees, and the equivalence of its stationary points with the fixed points of belief propagation"
  - paper: "Jonathan S. Yedidia, William T. Freeman and Yair Weiss, Generalized belief propagation, Advances in Neural Information Processing Systems 13 (NIPS 2000), MIT Press, 2001"
    title: Yedidia, Freeman and Weiss 2001
    locator: the Bethe free energy for pairwise Markov random fields and the link to BP fixed points
  - paper: doi:10.1561/2200000001
    title: "Martin J. Wainwright and Michael I. Jordan, Graphical models, exponential families, and variational inference, Foundations and Trends in Machine Learning 1(1-2), 2008"
    locator: "Chapter 4 (the Bethe variational problem, the local polytope and the Bethe entropy approximation)"
  - paper: "Tom Heskes, Stable fixed points of loopy belief propagation are local minima of the Bethe free energy, Advances in Neural Information Processing Systems 15 (NIPS 2002), MIT Press, 2003"
    title: Heskes 2003
    locator: stable BP fixed points are local minima of the Bethe free energy
  - paper: "Nicholas Ruozzi, The Bethe partition function of log-supermodular graphical models, Advances in Neural Information Processing Systems 25 (NIPS 2012)"
    title: Ruozzi 2012
    locator: for log-supermodular (attractive) binary pairwise models the Bethe partition function is a lower bound on Z
---

The Bethe free energy is a function of a set of local beliefs, one table for each factor and one for each variable of a [factor graph](/factor-graph/). It approximates the exact variational free energy, whose minimum is $-\log Z$, by an expression that uses only these local tables. On a tree it is exact: at the true marginals it equals $-\log Z$. On a graph with cycles it is an approximation, it need not be convex, and its minimum can be on either side of $-\log Z$. Its stationary points are exactly the fixed points of [loopy belief propagation](/loopy-belief-propagation/), which turns a message-passing rule into an optimization problem. Hans Bethe used it in 1935 for alloys on a lattice; Yedidia, Freeman and Weiss linked it to belief propagation.

## Definition

**The model.** A positive distribution on a factor graph with variables $x_1, \ldots, x_n$ (each with finitely many states) and factors $f_1, \ldots, f_m$:

$$p(x) = \frac{1}{Z} \prod_a f_a(x_a), \qquad f_a > 0,$$

where $x_a$ is the vector of the variables of factor $a$ and $Z$ is the [partition function](/partition-function/). Let $d_i$ be the number of factors that contain $x_i$.

**The exact free energy.** For any distribution $q$ over all of $x$, the variational (Gibbs) free energy is

$$G(q) = \sum_x q(x) \log q(x) - \sum_x q(x) \log \prod_a f_a(x_a) = \mathrm{KL}(q \,\|\, p) - \log Z.$$

So $G(q) \ge -\log Z$, with equality only at $q = p$. The second term needs only the factor marginals of $q$, but the first, $-H(q)$, needs all of $q$. The KL divergence is defined on the [evidence lower bound](/evidence-lower-bound/) page; $H$ is [Shannon entropy](/shannon-entropy/) in nats.

**The local polytope.** The Bethe approach replaces $q$ by local beliefs $b = (\{b_a\}, \{b_i\})$, where $b_a$ is a table over the states of $x_a$ and $b_i$ is a table over the states of $x_i$, with

$$b_a \ge 0, \quad b_i \ge 0, \quad \sum_{x_i} b_i(x_i) = 1, \quad \sum_{x_a} b_a(x_a) = 1, \quad \sum_{x_a \setminus x_i} b_a(x_a) = b_i(x_i) \ \text{ for all } i \in a.$$

This set is the *local polytope* $\mathcal{L}$. Its points are *pseudomarginals*: they agree on their overlaps, but on a graph with cycles there may be no joint distribution that has them as marginals.

**The Bethe free energy.** For $b \in \mathcal{L}$,

$$F_{\mathrm{Bethe}}(b) = \sum_a \sum_{x_a} b_a(x_a) \log \frac{b_a(x_a)}{f_a(x_a)} - \sum_i (d_i - 1) \sum_{x_i} b_i(x_i) \log b_i(x_i),$$

with $0 \log 0 = 0$. Equivalently $F_{\mathrm{Bethe}} = U - H_{\mathrm{Bethe}}$, with the average energy $U(b) = -\sum_a \sum_{x_a} b_a \log f_a$ and the Bethe entropy

$$H_{\mathrm{Bethe}}(b) = \sum_a H(b_a) - \sum_i (d_i - 1) H(b_i) = \sum_i H(b_i) - \sum_a I_a(b_a),$$

where $I_a = \sum_{i \in a} H(b_i) - H(b_a)$ is the multi-information of $b_a$. In the second form, each variable adds its entropy once, and each factor removes the dependence among its variables. The entropy of variable $i$ is counted in $d_i$ factor terms, and the term $-(d_i - 1) H(b_i)$ removes the extra $d_i - 1$ copies.

The **Bethe variational problem** is to minimize $F_{\mathrm{Bethe}}$ over $\mathcal{L}$, and the **Bethe approximation** of the log partition function is $\log Z_{\mathrm{Bethe}} = -\min_{b \in \mathcal{L}} F_{\mathrm{Bethe}}(b)$, or the value at a chosen stationary point.

**The facts that make it useful.**

- **Exact on trees.** If the factor graph is a tree, then for every $b \in \mathcal{L}$ the function $q_b(x) = \prod_a b_a(x_a) / \prod_i b_i(x_i)^{d_i - 1}$ is a distribution with the marginals $b$, and $F_{\mathrm{Bethe}}(b) = G(q_b) \ge -\log Z$. At the true marginals $q_b = p$, so $F_{\mathrm{Bethe}} = -\log Z$, the minimum. Every point of $\mathcal{L}$ is then a true set of marginals.
- **BP fixed points.** On any factor graph, the beliefs of a fixed point of loopy belief propagation are a stationary point of $F_{\mathrm{Bethe}}$ on $\mathcal{L}$, and each stationary point with positive beliefs comes from a fixed point (Yedidia, Freeman and Weiss 2001, 2005). The proof, by Lagrange multipliers, is on the loopy BP page. Stable fixed points are local minima (Heskes 2003).
- **Not convex in general.** $U$ is linear in $b$, and $H(b_a)$ is concave, but $-(d_i - 1) H(b_i)$ is convex for $d_i \ge 2$, so on graphs with cycles $H_{\mathrm{Bethe}}$ can fail to be concave and $F_{\mathrm{Bethe}}$ can fail to be convex. Then $F_{\mathrm{Bethe}}$ can have several local minima, and loopy BP can have several fixed points.
- **No bound in general.** On a graph with cycles, $\log Z_{\mathrm{Bethe}}$ can be below or above $\log Z$. For attractive binary pairwise models (all couplings positive), it is a lower bound (Ruozzi 2012).

## Examples and non-examples

**A tree.** Take three spins $s_i \in \{-1, +1\}$ on a chain, with $p(s) \propto \exp(0.5 s_1 - 0.3 s_3 + s_1 s_2 - 0.5 s_2 s_3)$, written as unary factors $e^{h_i s_i}$ and pair factors $e^{J s_i s_j}$. Then $\log Z = 2.8441$. At the exact marginals ($p(s_i = +1) = 0.7696, 0.7323, 0.2833$), the average energy is $U = -1.4557$ and the Bethe entropy is $H_{\mathrm{Bethe}} = 1.3884$, so $F_{\mathrm{Bethe}} = -2.8441 = -\log Z$. This is the exact entropy of $p$, because $p$ itself factors along the tree.

**A 4-cycle.** On the cycle $1 - 2 - 4 - 3 - 1$ with $J = 0.5$ and $h = (0.3, -0.2, 0.1, 0)$, $\log Z = 3.3433$. At the exact marginals, $F_{\mathrm{Bethe}} = -3.2901$, which is not $-\log Z$. At the fixed point of loopy BP it is $-3.3028$, lower than at the exact marginals, since BP finds a stationary point and the exact marginals are not one. So $\log Z_{\mathrm{Bethe}} = 3.3028$, a slight underestimate here.

**Not convex.** On the complete graph $K_4$ with $J = 1$ on every edge and no fields, take beliefs with $b_i(s) = (1 + m s)/2$ and $b_{ij}(s, t) = (1 + m s + m t + c\, s t)/4$. With $c = 0.913$, the points $m = 0.9$ and $m = -0.9$ both give $F_{\mathrm{Bethe}} = -5.9082$, but their midpoint $m = 0$ gives $-5.1652$, which is larger than the average. A convex function cannot do this. The two points are near the two magnetized fixed points of loopy BP, one for each sign.

**Non-example: a pseudomarginal.** On a triangle of spins with $J = -1$ on every edge and no fields, let $b_i$ be uniform and let each $b_{ij}$ put mass $\frac12$ on each of the two disagreeing pairs. This point is in $\mathcal{L}$, but no distribution on three spins has all three pairs always disagreeing. Its Bethe entropy is $3 \log 2 - 3 \log 2 = 0$ and $F_{\mathrm{Bethe}} = -3$, which is below $-\log Z = -\log(2e^{-3} + 6e) = -2.7978$. So on a graph with cycles, the minimum of $F_{\mathrm{Bethe}}$ can be below $-\log Z$, and $\log Z_{\mathrm{Bethe}}$ can overestimate $\log Z$.

**Non-example: the mean-field free energy.** If $q$ is a product distribution, $G(q)$ is computed exactly from the single-variable marginals, and $-\min G$ over product distributions is a lower bound on $\log Z$. This is the [mean-field approximation](/mean-field-approximation/), not the Bethe one: it restricts $q$ instead of approximating the entropy.

## Related definitions

- **Kikuchi free energy.** The generalization to larger regions, with counting numbers in place of $1$ and $-(d_i - 1)$; its stationary points are the fixed points of [generalized belief propagation](/generalized-belief-propagation/). The Bethe free energy is the case where the regions are the factors and the single variables.
- **Tree-reweighted free energy.** Replace each $I_a$ by $\rho_a I_a$ with edge appearance probabilities $\rho_a$ from a distribution over spanning trees. The result is convex, and its minimum gives an upper bound on $\log Z$; see [tree-reweighted belief propagation](/tree-reweighted-belief-propagation/).
- **Marginal polytope.** The set of marginals of real distributions. It is contained in $\mathcal{L}$, and equal to it on trees.
- **Evidence lower bound.** $-G(q)$ is the ELBO of an unnormalized model; the Bethe free energy approximates its negative without a full $q$.
- **Bethe lattice.** A tree in which every node has the same degree; on it the Bethe approximation of Bethe (1935) is exact, which gave the name.

## References
