---
tag: KQP2ZG
kind: model
slug: markov-random-field
name: Markov random field
aliases:
- Markov network
- undirected graphical model
area: machine-learning/probabilistic-inference
level: core
summary: "An undirected graph with a nonnegative potential on each clique; p(x) is their product over Z. Graph separation gives independence; for positive p this is Hammersley-Clifford."
history:
  year: 1974
  people: [John M. Hammersley, Peter Clifford, Julian Besag, John Moussouris]
  note: Hammersley and Clifford proved in an unpublished 1971 manuscript that positive Markov fields are Gibbs distributions. Besag published a proof in 1974, and Moussouris showed that positivity is needed.
prereqs: [graphical-model, conditional-independence, clique]
see_also: [partition-function, ising-model, potts-model, gibbs-sampling, factor-graph, bayesian-network, conditional-random-field, gaussian-graphical-model]
sources:
  - paper: doi:10.1111/j.2517-6161.1974.tb00999.x
    title: "Julian Besag, Spatial Interaction and the Statistical Analysis of Lattice Systems, Journal of the Royal Statistical Society B 36(2), 1974"
    locator: pp. 192-225 (the Hammersley-Clifford theorem with a proof, and models built from local conditional distributions)
  - paper: "Peter Clifford, Markov random fields in statistics, in G. R. Grimmett and D. J. A. Welsh (eds.), Disorder in Physical Systems, Oxford University Press, 1990"
    locator: pp. 19-32 (history of the Hammersley-Clifford theorem)
  - paper: doi:10.1007/BF01011714
    title: "John Moussouris, Gibbs and Markov Random Systems with Constraints, Journal of Statistical Physics 10(1), 1974"
    locator: pp. 11-33 (a Markov field on a 4-cycle with zeros that is not a Gibbs field)
  - book: isbn:9780198522195
    title: "Steffen L. Lauritzen, Graphical Models, Oxford University Press, 1996"
    locator: Chapter 3, Section 3.2 (Markov properties on undirected graphs and factorization)
  - book: isbn:9780262013192
    title: "Daphne Koller and Nir Friedman, Probabilistic Graphical Models, MIT Press, 2009"
    locator: Chapter 4 (Markov networks, Gibbs distributions, the Hammersley-Clifford theorem and log-linear models)
---

A Markov random field (MRF) is a [graphical model](/graphical-model/) given by an undirected graph over random variables $X_1, \ldots, X_n$ and a nonnegative function, called a potential, on each [clique](/clique/) of the graph. The joint distribution is the product of the potentials divided by a normalizing constant $Z$, the [partition function](/partition-function/). Whenever a set $S$ separates $A$ from $B$ in the graph, $X_A$ is [conditionally independent](/conditional-independence/) of $X_B$ given $X_S$. For strictly positive distributions, the Hammersley-Clifford theorem gives the converse: every distribution with these independences factorizes over the cliques. Without positivity the converse fails.

## The machine

**Data.** An undirected graph $H = (V, E)$ with $V = \{1, \ldots, n\}$; a list $\mathcal{C}$ of cliques of $H$ (often the maximal cliques, or the edges for a pairwise MRF); for each $C \in \mathcal{C}$ a potential $\psi_C(x_C) \ge 0$.

**The Gibbs distribution.**

$$
p(x) = \frac{1}{Z}\prod_{C \in \mathcal{C}} \psi_C(x_C), \qquad Z = \sum_{x} \prod_{C \in \mathcal{C}} \psi_C(x_C) .
$$

For positive potentials, write $\psi_C = e^{-E_C}$ and $p(x) = e^{-E(x)}/Z$ with energy $E(x) = \sum_C E_C(x_C)$. A log-linear model sets $\log \psi_C(x_C) = \sum_k w_k f_k(x_C)$ for features $f_k$ and weights $w_k$. Potentials are not probabilities: they need not sum to 1 and are not the marginals of the cliques.

**Example.** Take the chain $A - B - C$ of binary variables with $\psi_{AB} = \psi_{BC}$ equal to 3 when the two values agree and 1 when they differ. Then

$$
Z = \sum_b \Big(\sum_a \psi(a, b)\Big)\Big(\sum_c \psi(b, c)\Big) = 2 \cdot 4 \cdot 4 = 32 .
$$

$P(A = C) = 20/32 = 5/8$, so $A$ and $C$ are dependent, but $A \perp C \mid B$, because $B$ separates them.

**Markov properties.** For a distribution $p$ on $X_V$ and the graph $H$:

- *Pairwise (P):* $X_u \perp X_v \mid X_{V \setminus \{u, v\}}$ for every non-adjacent pair $u, v$.
- *Local (L):* $X_v \perp X_{V \setminus (\{v\} \cup N(v))} \mid X_{N(v)}$ for every $v$, where $N(v)$ is the set of neighbors. $N(v)$ is the [Markov blanket](/markov-blanket/) of $v$.
- *Global (G):* $X_A \perp X_B \mid X_S$ whenever $S$ separates $A$ from $B$, that is, every path from $A$ to $B$ meets $S$.
- *Factorization (F):* $p$ is a Gibbs distribution with potentials on cliques of $H$.

**(F) implies (G).** Let $S$ separate $A$ from $B$. Let $\tilde A$ be the set of nodes connected to $A$ by paths that avoid $S$, and $\tilde B = V \setminus (\tilde A \cup S)$, so $B \subseteq \tilde B$. No edge joins $\tilde A$ to $\tilde B$, so every clique lies in $\tilde A \cup S$ or in $\tilde B \cup S$. Grouping the potentials gives $p(x) = f(x_{\tilde A}, x_S)\,g(x_{\tilde B}, x_S)$. By the factorization criterion this gives $X_{\tilde A} \perp X_{\tilde B} \mid X_S$, and by decomposition $X_A \perp X_B \mid X_S$.

**(G) implies (L) implies (P).** $N(v)$ separates $v$ from all non-neighbors, which gives (L). For a non-adjacent pair $u, v$, (L) gives $X_u \perp X_{V \setminus (\{u\} \cup N(u))} \mid X_{N(u)}$, and the set on the right contains $v$; weak union moves the other variables into the conditioning set, which gives (P).

## What it counts

- **Parameters.** A potential on a clique of $k$ variables with $r$ values each has $r^k$ entries, one of which is redundant up to scale. A pairwise binary MRF needs $O(n + |E|)$ numbers.
- **Normalization.** $Z$ is a sum over $\prod_i r_i$ assignments. Unlike a [Bayesian network](/bayesian-network/), where $Z = 1$, evaluating $p(x)$ for one $x$ needs $Z$. Ratios $p(x)/p(x')$ and local conditionals do not:

$$
p(x_v \mid x_{V \setminus v}) = \frac{\prod_{C \ni v} \psi_C(x_C)}{\sum_{x_v'} \prod_{C \ni v} \psi_C(x_v', x_{C \setminus v})},
$$

which uses only the potentials that contain $v$. [Gibbs sampling](/gibbs-sampling/) runs on these conditionals.
- **Inference cost.** Marginals and $Z$ by [variable elimination](/variable-elimination/) cost time exponential in the treewidth of $H$. For general graphs computing $Z$ is #P-hard; the [Ising model](/ising-model/) is the standard hard case.
- **Learning cost.** For a log-linear model, $\partial \log p(D)/\partial w_k$ is the data average of $f_k$ minus its expectation under the model. The second term needs inference, so each gradient step costs an inference call.

## Relation to other models

- **Bayesian networks.** The moral graph of a DAG, with the CPDs as potentials and $Z = 1$, is an MRF for the same distribution. Directed and undirected graphs express different independences: a v-structure has no undirected perfect map and a 4-cycle has no directed one; see [graphical model](/graphical-model/).
- **Factor graphs.** An MRF does not say whether a triangle carries one potential on three variables or three pairwise potentials. A [factor graph](/factor-graph/) does.
- **Special cases.** The [Ising model](/ising-model/), the [Potts model](/potts-model/) and the [hard-core model](/hard-core-model/) are MRFs on graphs. A [Gaussian graphical model](/gaussian-graphical-model/) is a Gaussian MRF: $X_u \perp X_v \mid X_{\text{rest}}$ exactly when the precision matrix has a zero in entry $(u, v)$. A [conditional random field](/conditional-random-field/) is an MRF over outputs whose potentials depend on observed inputs.

## Known results in the model

**Hammersley-Clifford theorem.** Let $p$ be strictly positive. Then $p$ satisfies the pairwise Markov property for $H$ if and only if it factorizes over the cliques of $H$. With the implications above, (F), (G), (L) and (P) are all equivalent for positive $p$ (Besag 1974; Lauritzen, Section 3.2).

*Proof that (P) implies (F) for positive $p$.* Take binary variables for notation; the general case is the same. For $B \subseteq V$, let $x^B$ agree with $x$ on $B$ and be 0 elsewhere, and let $H_B(x) = \log p(x^B)$, which is finite by positivity. Define

$$
\phi_A(x) = \sum_{B \subseteq A} (-1)^{|A \setminus B|} H_B(x) .
$$

Each $\phi_A$ depends only on $x_A$, and Möbius inversion on the lattice of subsets gives $\log p(x) = H_V(x) = \sum_{A \subseteq V} \phi_A(x)$. Now suppose $A$ contains two non-adjacent nodes $i, j$, and let $C = A \setminus \{i, j\}$. Grouping the terms by $D = B \cap C$,

$$
\phi_A(x) = \sum_{D \subseteq C} (-1)^{|C \setminus D|}\left[H_{D \cup \{i, j\}} - H_{D \cup \{i\}} - H_{D \cup \{j\}} + H_D\right](x) .
$$

Fix $D$ and write $w$ for the values of $x^D$ off $\{i, j\}$. The bracket is $\log \frac{p(x_i, x_j, w)\,p(0, 0, w)}{p(x_i, 0, w)\,p(0, x_j, w)}$. By (P), $p(a, b, w) = p(a \mid w)\,p(b \mid w)\,p(w)$, and the ratio is 1. So $\phi_A = 0$ unless $A$ is a clique, and $p = \prod_{A \text{ clique}} e^{\phi_A}$. The test file runs this construction in exact arithmetic on random positive MRFs and checks that every non-clique potential is 1.

**Positivity cannot be dropped (Moussouris 1974).** On the 4-cycle $1 - 2 - 3 - 4 - 1$, let $p$ be uniform on the eight assignments

$$
0000,\ 1000,\ 1100,\ 1110,\ 0001,\ 0011,\ 0111,\ 1111
$$

and 0 on the other eight. One checks by enumeration that $X_1 \perp X_3 \mid (X_2, X_4)$ and $X_2 \perp X_4 \mid (X_1, X_3)$, and that the global Markov property holds. But $p$ is not a product of edge potentials. If it were, then $p(0101) > 0$: its value pairs on the four edges are $(x_1, x_2) = (0, 1)$, which occurs in $0111$; $(x_2, x_3) = (1, 0)$, in $1100$; $(x_3, x_4) = (0, 1)$, in $0001$; and $(x_4, x_1) = (1, 0)$, in $0001$. Each of these assignments has positive probability, so each edge potential is positive at its pair, and the product at $0101$ would be positive. Yet $p(0101) = 0$.

**Other results.**

- For positive $p$, (P) implies (G) directly, by the intersection property of [conditional independence](/conditional-independence/); without positivity (P) does not even imply (L). For example, let $X_1 = X_2 = X_3$ be one fair coin and let the graph have the single edge $1 - 2$. Each non-adjacent pair is independent given the third variable, which fixes both, so (P) holds. But (L) at node 3, which has no neighbors, says $X_3$ is independent of $(X_1, X_2)$, which is false.
- Besag's 1974 paper also builds joint MRFs from families of local conditional distributions $p(x_v \mid x_{N(v)})$, such as auto-logistic models on lattices.
- Exact inference is exponential in the treewidth, and computing $Z$ is #P-hard in general, so large MRFs use [belief propagation](/belief-propagation/), sampling, or [mean-field](/mean-field-approximation/) and other variational approximations.

## References
