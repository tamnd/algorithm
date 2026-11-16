---
tag: HPRR7C
kind: theorem
slug: graph-representable-energies
name: Kolmogorov-Zabih representability theorem
aliases:
- graph-representable energies
- regularity condition for graph cuts
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: Only regular (submodular) binary energies can be represented by a cut. With terms of at most three variables, regularity is also sufficient, so one min cut minimizes them exactly.
prereqs: [max-flow-min-cut-theorem, submodular-function, markov-random-field]
see_also: [alpha-expansion, alpha-beta-swap, qpbo, boykov-kolmogorov-max-flow, graph-cut-stereo, image-segmentation-graph-cuts, min-cut-problem, potts-model]
sources:
  - paper: doi:10.1109/TPAMI.2004.1262177
    title: Vladimir Kolmogorov and Ramin Zabih, What energy functions can be minimized via graph cuts?, IEEE Transactions on Pattern Analysis and Machine Intelligence 26(2), 2004, 147-159
    locator: Definition 3.1 (graph-representable functions), Theorem 4.1 (the class F2), Section 4.1 (the construction for F2), Theorem 4.2 (NP-hardness of nonregular F2), Theorem 5.3 and Section 5.1 (the class F3), Theorem 6.1 (regularity is necessary)
  - paper: doi:10.1111/j.2517-6161.1989.tb01764.x
    title: D. M. Greig, B. T. Porteous and A. H. Seheult, Exact maximum a posteriori estimation for binary images, Journal of the Royal Statistical Society Series B 51(2), 1989, 271-279
    locator: the reduction of the MAP estimate of a binary image with an Ising prior to a minimum cut
  - paper: doi:10.1016/j.dam.2009.07.001
    title: Stanislav Živný, David A. Cohen and Peter G. Jeavons, The expressive power of binary submodular functions, Discrete Applied Mathematics 157(15), 2009, 3347-3358
    locator: the result that some submodular functions of four variables cannot be expressed by binary submodular functions with extra variables
  - paper: doi:10.1016/S0166-218X(01)00341-9
    title: Endre Boros and Peter L. Hammer, Pseudo-Boolean optimization, Discrete Applied Mathematics 123(1-3), 2002, 155-225
    locator: the parts on quadratic pseudo-Boolean functions, the multilinear form and the network flow methods for the submodular case
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 4, Model fitting and optimization (Markov random fields and their minimization by graph cuts)
---

The Kolmogorov-Zabih theorem says which energies of binary variables a [minimum cut](/min-cut-problem/) can minimize exactly. An energy is graph-representable if there is a directed graph with nonnegative capacities, a source, a sink and one node for each variable, such that the energy of every assignment equals, up to a constant, the cheapest cut that puts the nodes of the variables with value 0 on the source side and the others on the sink side. Such an energy is minimized by one max-flow computation, by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/). The theorem says that a graph-representable energy must be regular: every restriction of it to two variables, with the other variables fixed, satisfies $E(0,0) + E(1,1) \le E(0,1) + E(1,0)$. For energies that are sums of terms of at most two variables (the class $\mathcal{F}^2$) and at most three variables ($\mathcal{F}^3$), this condition is also sufficient. Regularity is the same as [submodularity](/submodular-function/) of the energy seen as a set function. The theorem is the base of the move algorithms [alpha-expansion](/alpha-expansion/) and [alpha-beta swap](/alpha-beta-swap/), and [QPBO](/qpbo/) is the method for energies that are not regular.

## Statement

Let $E : \{0,1\}^n \to \mathbb{R}$ be a function of binary variables $x_1, \ldots, x_n$.

**Graph-representable** (Kolmogorov and Zabih, Definition 3.1). $E$ is graph-representable if there is a directed graph $G$ with nonnegative edge capacities, terminals $s$ and $t$, nodes $v_1, \ldots, v_n$ and possibly more nodes, and a constant $K$, such that for every $x \in \{0,1\}^n$

$$E(x) = K + \min \{\, c(S) : s \in S,\ t \notin S,\ v_i \in S \text{ if } x_i = 0,\ v_i \notin S \text{ if } x_i = 1 \,\},$$

where $c(S)$ is the total capacity of the edges from $S$ to the other nodes. The extra nodes may be on either side.

**Projection and regularity.** A projection of $E$ to two variables $x_i, x_j$ is the function $F(a, b)$ of two binary variables that $E$ gives when $x_i = a$, $x_j = b$ and all other variables have fixed values. $E$ is regular if every projection to two variables satisfies

$$F(0,0) + F(1,1) \le F(0,1) + F(1,0).$$

A function of one variable has no such condition. $\mathcal{F}^2$ is the class of functions $E(x) = \sum_i E^i(x_i) + \sum_{i<j} E^{i,j}(x_i, x_j)$ and $\mathcal{F}^3$ adds terms $E^{i,j,k}(x_i, x_j, x_k)$.

**Theorem.**

1. (Necessity, Theorem 6.1 of the paper.) Every graph-representable function is regular.
2. (Class $\mathcal{F}^2$, Theorem 4.1.) $E \in \mathcal{F}^2$ is graph-representable if and only if every pairwise term satisfies $E^{i,j}(0,0) + E^{i,j}(1,1) \le E^{i,j}(0,1) + E^{i,j}(1,0)$.
3. (Class $\mathcal{F}^3$, Theorem 5.3.) $E \in \mathcal{F}^3$ is graph-representable if and only if it is regular.

In parts 2 and 3 the graph has $O(n + T)$ nodes and edges for $T$ terms, so a regular $E$ in $\mathcal{F}^3$ is minimized exactly in polynomial time by one max-flow computation: a minimum cut $S$ gives the minimizer $x_i = [v_i \notin S]$.

## In plain words

Think of each yes or no variable as a node that must go to one of two sides, the source side or the sink side. Cutting the graph into two sides costs the sum of the edges that cross from the source side to the sink side. If you can build a graph where this cost always equals your energy, then the cheapest cut tells you the best answer, and there are fast programs for the cheapest cut. The theorem says when such a graph exists. Look at any two variables. Agreeing in both ways must cost no more in total than disagreeing in both ways. If some pair breaks this rule, no graph can do it. If every pair keeps the rule and each term has at most three variables, a graph always exists.

## Proof

Write $c(S)$ for the capacity of the cut with source side $S$.

**Lemma (cuts are submodular).** For any two node sets $S_1, S_2$ that contain $s$ and not $t$, $c(S_1) + c(S_2) \ge c(S_1 \cap S_2) + c(S_1 \cup S_2)$.

*Proof.* Look at one edge $(u, w)$ of capacity $\gamma \ge 0$. It counts in $c(S)$ when $u \in S$ and $w \notin S$. Let $a_k = [u \in S_k]$ and $b_k = [w \notin S_k]$. The edge adds $\gamma(a_1 b_1 + a_2 b_2)$ to the left side and $\gamma(a_1 a_2 \max(b_1, b_2) + \max(a_1, a_2)\, b_1 b_2)$ to the right side. If both right terms are 1, then $a_1 = a_2 = b_1 = b_2 = 1$ and the left side is 2. If only the first is 1, then $a_1 = a_2 = 1$ and some $b_k = 1$, so the left side is at least 1. If only the second is 1, then $b_1 = b_2 = 1$ and some $a_k = 1$, so again the left side is at least 1. Sum over the edges. $\square$

**Part 1 (necessity).** Let $G$ and $K$ represent $E$. Fix a projection $F$ to $x_i, x_j$, with the other variables at fixed values $\bar x$. Let $S_{01}$ be a cheapest cut for the assignment with $x_i = 0$, $x_j = 1$ and $\bar x$, and let $S_{10}$ be a cheapest cut for $x_i = 1$, $x_j = 0$ and $\bar x$. Then $v_i \in S_{01}$, $v_j \notin S_{01}$, $v_i \notin S_{10}$ and $v_j \in S_{10}$. Every other variable node $v_k$ is in both sets or in neither, because both use the values $\bar x$. So $S_{01} \cap S_{10}$ is a cut for $x_i = x_j = 1$ and $\bar x$, and $S_{01} \cup S_{10}$ is a cut for $x_i = x_j = 0$ and $\bar x$; both contain $s$ and not $t$. By the definition and the lemma,

$$F(0,1) + F(1,0) - 2K = c(S_{01}) + c(S_{10}) \ge c(S_{01} \cap S_{10}) + c(S_{01} \cup S_{10}) \ge F(1,1) - K + F(0,0) - K.$$

**Part 2 (sufficiency for $\mathcal{F}^2$).** Two facts make the construction modular. First, if $E_1$ and $E_2$ are represented by graphs on the same nodes $s, t, v_1, \ldots, v_n$, possibly with their own extra nodes, then $E_1 + E_2$ is represented by the union of the two graphs, with capacities added on shared edges and constants added: the extra nodes of the two graphs are disjoint, so the minimum over their placement splits into two independent minimums. Second, each term is representable alone:

- A unary term $\beta x_i$ with $\beta \ge 0$ is an edge $s \to v_i$ of capacity $\beta$: it is cut exactly when $v_i \notin S$, that is $x_i = 1$. With $\beta < 0$ write $\beta x_i = \beta + |\beta| (1 - x_i)$: an edge $v_i \to t$ of capacity $|\beta|$ and the constant $\beta$. A general unary term is $E^i(0) + (E^i(1) - E^i(0)) x_i$.
- A pairwise term with $A = E^{i,j}(0,0)$, $B = E^{i,j}(0,1)$, $C = E^{i,j}(1,0)$, $D = E^{i,j}(1,1)$ equals

$$A + (C - A)\, x_i + (D - C)\, x_j + (B + C - A - D)(1 - x_i)\, x_j,$$

which the four cases check. The last product is 1 exactly when $v_i \in S$ and $v_j \notin S$, so it is an edge $v_i \to v_j$ of capacity $B + C - A - D$. The capacity is nonnegative exactly when the term is regular. The other parts are unary terms and a constant.

For the converse, the projection of $E \in \mathcal{F}^2$ to $x_i, x_j$ is $E^{i,j}$ plus functions of one variable and a constant, which do not change $F(0,0) + F(1,1) - F(0,1) - F(1,0)$. So $E$ is regular exactly when every $E^{i,j}$ is regular, and Part 1 gives the "only if" direction.

**Part 3 (sufficiency for $\mathcal{F}^3$).** Write $E$ in its unique multilinear form

$$E(x) = a_0 + \sum_i a_i x_i + \sum_{i<j} a_{ij} x_i x_j + \sum_{i<j<k} a_{ijk} x_i x_j x_k.$$

For a projection to $x_i, x_j$, the value $F(0,0) + F(1,1) - F(0,1) - F(1,0)$ is the coefficient of $x_i x_j$ after the other variables are fixed, which is $a_{ij} + \sum_k a_{ijk} x_k$. The other variables take all values, so $E$ is regular if and only if

$$a_{ij} + \sum_{k} \max(a_{ijk}, 0) \le 0 \quad \text{for every pair } i < j. \tag{R}$$

Replace each cubic monomial with one extra binary variable $w$, using two identities that hold for all binary values (check the eight cases):

$$-P\, x_i x_j x_k = \min_{w} P\, w\,(2 - x_i - x_j - x_k), \qquad P\, x_i x_j x_k = P\,(x_i x_j + x_i x_k + x_j x_k) + \min_{w} P\, w\,(1 - x_i - x_j - x_k),$$

with $P \ge 0$. In both, the products $w x_i$ have the coefficient $-P \le 0$. A positive cubic monomial also adds $a_{ijk}$ to the coefficient of each of its three pairs, and a negative one adds nothing. After all replacements, $E(x) = \min_w E'(x, w)$ where $E'$ has only unary and pairwise terms, and the coefficient of $x_i x_j$ in $E'$ is the left side of (R). A pairwise term $\gamma x_i x_j$ has $F(0,0) + F(1,1) - F(0,1) - F(1,0) = \gamma$, so every pairwise term of $E'$ is regular. By Part 2, $E'$ is represented by a graph with nodes for $x$ and $w$. A minimum over cuts that fixes the nodes of $x$ is also a minimum over the placement of the nodes of $w$, so the same graph, with the nodes of $w$ as extra nodes, represents $E$. The converse is Part 1. $\square$

The proof of Part 3 is a little different from the construction in Section 5.1 of the paper, which builds the graph for each regular term of three variables after a regrouping of the terms (Theorem 5.4 of the paper). Both give a graph of $O(n + T)$ nodes and edges.

**The minimizer.** If $G$ represents $E$ and $S^*$ is a minimum cut, the assignment $x_i = [v_i \notin S^*]$ has $E(x) \le K + c(S^*)$, and every $x$ has $E(x) \ge K + c(S^*)$, so $x$ is a minimizer.

## Consequences

- **Binary labeling.** Foreground and background segmentation and binary image restoration with an Ising or [Potts](/potts-model/) prior have regular pairwise terms, so they are solved exactly by one cut. This is the case of Greig, Porteous and Seheult (1989) and of [graph cut segmentation](/image-segmentation-graph-cuts/).
- **Move algorithms.** A multi-label energy is minimized approximately by a sequence of binary moves. A move is one cut when its binary energy is regular. The swap move is regular when the pairwise term is a semimetric, and the expansion move when it is a metric. See [alpha-beta swap](/alpha-beta-swap/) and [alpha-expansion](/alpha-expansion/).
- **Stereo with occlusions.** The uniqueness constraint of [graph cut stereo](/graph-cut-stereo/) is an infinite pairwise term. It is regular only after the move variables are chosen with care, and the theorem tells which choices work.
- **Nonregular energies.** For a pairwise energy that is not regular, [QPBO](/qpbo/) builds a regular energy on twice as many variables and gets a partial optimal labeling.
- **A test before building a graph.** To know whether a new energy can be minimized by one cut, check the inequality on every pairwise projection. If it fails anywhere, no graph exists, however many extra nodes it has.
- **Max-flow solvers.** In vision the graphs are grids with a few edges per node, and the [Boykov-Kolmogorov algorithm](/boykov-kolmogorov-max-flow/) is the usual solver (an observed speed, not a bound).

### A worked example

Take the pairwise term $E(0,0) = 0$, $E(0,1) = 3$, $E(1,0) = 2$, $E(1,1) = 1$. It is regular: $0 + 1 \le 3 + 2$. The formula of Part 2 gives $E = 2 x_i - x_j + 4 (1 - x_i) x_j$, and $-x_j = -1 + (1 - x_j)$. The graph has an edge $s \to v_i$ of capacity 2, an edge $v_j \to t$ of capacity 1, an edge $v_i \to v_j$ of capacity 4, and $K = -1$.

| $(x_i, x_j)$ | source side | cut edges | cut cost | $K + $ cost | $E$ |
|---|---|---|---|---|---|
| $(0, 0)$ | $s, v_i, v_j$ | $v_j \to t$ | 1 | 0 | 0 |
| $(0, 1)$ | $s, v_i$ | $v_i \to v_j$ | 4 | 3 | 3 |
| $(1, 0)$ | $s, v_j$ | $s \to v_i$, $v_j \to t$ | 3 | 2 | 2 |
| $(1, 1)$ | $s$ | $s \to v_i$ | 2 | 1 | 1 |

A non-example is the term that rewards disagreement, $E(0,0) = E(1,1) = 1$ and $E(0,1) = E(1,0) = 0$: here $1 + 1 > 0 + 0$, so by Part 1 no graph represents it, with any number of extra nodes.

## Tightness

- **Regularity is not enough for four variables.** Živný, Cohen and Jeavons (2009) showed that some submodular functions of four binary variables cannot be written as the minimum over extra variables of a sum of submodular functions of two variables. So the "if" direction of Part 3 does not extend to all orders. Submodular functions of any order are still minimized in polynomial time by general submodular minimization, but not by one cut of this kind.
- **Nonregular terms make the problem hard.** Theorem 4.2 of the paper shows that minimizing $E \in \mathcal{F}^2$ is NP-hard when one fixed nonregular pairwise term may be placed on any pairs, together with arbitrary unary terms. So, unless P = NP, the limit that regularity puts on cuts is also a limit for every polynomial method on such classes.
- **Representation is not the only route.** A single nonregular term of two variables is easy to minimize by trying the four cases. The theorem is about the cut construction, not about every polynomial method.

## History

Greig, Porteous and Seheult (1989) showed that the maximum a posteriori estimate of a binary image with an Ising prior is a minimum cut, and so can be computed exactly. Quadratic pseudo-Boolean functions with nonpositive quadratic coefficients were known to be minimized by network flows in operations research before that; the survey of Boros and Hammer (2002) collects these results. Boykov, Veksler and Zabih (2001) used cuts for the moves of multi-label energies and built a graph for each kind of move. Kolmogorov and Zabih (2004) gave the general answer: they defined graph-representable functions, proved that regularity is necessary, and gave constructions for $\mathcal{F}^2$ and $\mathcal{F}^3$. Živný, Cohen and Jeavons (2009) showed that the construction cannot cover all submodular functions of four variables.

## References
