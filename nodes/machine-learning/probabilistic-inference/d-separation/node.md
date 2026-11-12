---
tag: WVXXR3
kind: concept
slug: d-separation
name: d-separation
aliases:
- directional separation
- directed separation
area: machine-learning/probabilistic-inference
level: core
summary: "A test on a DAG: Z d-separates X from Y when Z blocks every trail between them. Then X and Y are independent given Z in every distribution that factorizes over the DAG."
prereqs: [bayesian-network, conditional-independence, directed-acyclic-graph]
see_also: [d-separation-query, bayes-ball, markov-blanket, markov-property, backdoor-criterion, do-calculus, bayesian-network-structure-learning, structural-causal-model]
sources:
  - book: isbn:9781558604797
    title: Judea Pearl, Probabilistic Reasoning in Intelligent Systems, Networks of Plausible Inference, Morgan Kaufmann, 1988
    locator: "Chapter 3 (Markov and Bayesian networks): the d-separation criterion and its use as the independence semantics of a Bayesian network"
  - paper: doi:10.1002/net.3230200504
    title: Dan Geiger, Thomas Verma and Judea Pearl, Identifying independence in Bayesian networks, Networks 20(5), 1990, pages 507 to 534
    locator: soundness and completeness of d-separation, and a linear-time algorithm
  - paper: "Christopher Meek, Strong completeness and faithfulness in Bayesian networks, Proceedings of the 11th Conference on Uncertainty in Artificial Intelligence (UAI 1995), pages 411 to 418"
    title: Meek 1995
    locator: the parameters of a discrete or linear Gaussian network that are not faithful to the DAG have measure zero
  - paper: doi:10.1002/net.3230200503
    title: Steffen L. Lauritzen, A. Philip Dawid, Birgitte N. Larsen and Hanns-Georg Leimer, Independence properties of directed Markov fields, Networks 20(5), 1990, pages 491 to 505
    locator: the directed global Markov property by separation in the moral graph of the smallest ancestral set, and its equivalence with d-separation
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 3, Section 3.3 (independencies in graphs: d-separation, soundness and completeness, Algorithm 3.1, I-equivalence)"
  - book: isbn:9780198522195
    title: Steffen L. Lauritzen, Graphical Models, Oxford University Press, 1996
    locator: "Chapter 3, Section 3.2.2 (Markov properties on directed acyclic graphs)"
---

d-separation is a test on a [directed acyclic graph](/directed-acyclic-graph/) that tells when a set of nodes $Z$ blocks every trail between two sets $X$ and $Y$. Judea Pearl introduced it in the 1980s as the independence rule of a [Bayesian network](/bayesian-network/): if $Z$ d-separates $X$ from $Y$, then $X$ and $Y$ are [conditionally independent](/conditional-independence/) given $Z$ in every distribution that factorizes over the graph. The converse holds for almost all choices of the conditional tables. A [d-separation query](/d-separation-query/) takes linear time, for example with [Bayes-Ball](/bayes-ball/).

## In plain words

Information can flow between two variables along any route of arrows, whatever their direction. Each variable in the middle of a route acts like a valve. If the route goes through a variable as a chain or splits there, the valve is open until you observe that variable; then it closes. If two arrows on the route meet head to head at a variable, the valve is closed until you observe that variable or something caused by it; then it opens. Two sets are separated when every route has at least one closed valve. Separated variables cannot inform each other, whatever the numbers in the model.

## The idea

**Trails and the three patterns.** Let $G = (V, E)$ be a DAG. A *trail* is a sequence of distinct nodes in which each consecutive pair is joined by an edge in either direction. An interior node $v$ of a trail, with neighbours $a$ and $b$ on the trail, is in one of three patterns:

| pattern | shape | blocked by $Z$ when |
|---|---|---|
| chain | $a \to v \to b$ or $a \leftarrow v \leftarrow b$ | $v \in Z$ |
| fork | $a \leftarrow v \to b$ | $v \in Z$ |
| collider | $a \to v \leftarrow b$ | $v \notin Z$ and no descendant of $v$ is in $Z$ |

A trail is *active* given $Z$ if none of its interior nodes is blocked. The node $v$ is a collider only relative to the trail: the same node can be a collider on one trail and a chain on another.

**Definition.** For pairwise disjoint $X, Y, Z \subseteq V$, the set $Z$ *d-separates* $X$ from $Y$, written $X \perp_G Y \mid Z$, if no trail from a node of $X$ to a node of $Y$ is active given $Z$. Otherwise $X$ and $Y$ are *d-connected* given $Z$.

**Why colliders are different.** In a chain or a fork, the end variables are linked through $v$, and fixing $v$ cuts the link. At a collider, the two ends are separate causes of $v$. They are independent until $v$ is observed; then one cause can explain away the other. A descendant of $v$ is a noisy copy of $v$, so observing it also opens the collider.

**Soundness.** Say that a distribution $P$ on discrete variables $(x_v)_{v \in V}$ *factorizes* over $G$ if $P(x) = \prod_{v \in V} P(x_v \mid x_{\mathrm{Pa}(v)})$.

> **Theorem (soundness; Geiger, Verma and Pearl 1990).** If $X \perp_G Y \mid Z$, then $X \perp Y \mid Z$ in every $P$ that factorizes over $G$.

*Proof.* We use the moral graph criterion of Lauritzen, Dawid, Larsen and Leimer (1990): let $A$ be the smallest set that holds $X \cup Y \cup Z$ and all their ancestors, and let $(G_A)^m$ be the undirected graph on $A$ with an edge for each edge of $G_A$ and an edge between each two parents of a common child. They prove that $X \perp_G Y \mid Z$ if and only if $Z$ separates $X$ from $Y$ in $(G_A)^m$, that is, each path from $X$ to $Y$ in $(G_A)^m$ meets $Z$. Given that, two steps finish the proof.

1. The marginal of $P$ on $A$ factorizes over $G_A$. Every node outside $A$ has all its descendants outside $A$, since a descendant in $A$ would make it an ancestor of $X \cup Y \cup Z$. So we can sum out the nodes of $V \setminus A$ one at a time, always a node with no child left. When $v$ has no child left, $x_v$ appears only in the factor $P(x_v \mid x_{\mathrm{Pa}(v)})$, and $\sum_{x_v} P(x_v \mid x_{\mathrm{Pa}(v)}) = 1$. What remains is $\prod_{v \in A} P(x_v \mid x_{\mathrm{Pa}(v)})$.
2. Each factor depends only on $\{v\} \cup \mathrm{Pa}(v)$, which is a complete set in $(G_A)^m$. Let $X'$ be the set of nodes of $A \setminus Z$ joined to $X$ by a path that avoids $Z$, and $Y' = A \setminus (X' \cup Z)$. Separation gives $Y \subseteq Y'$, and no edge of $(G_A)^m$ joins $X'$ to $Y'$. So each complete set lies inside $X' \cup Z$ or inside $Y' \cup Z$, and the marginal has the form $f(x_{X'}, x_Z)\, g(x_{Y'}, x_Z)$. A density of this form satisfies $X' \perp Y' \mid Z$: summing gives $P(x_{X'}, x_Z) = f \cdot \sum_{x_{Y'}} g$, $P(x_{Y'}, x_Z) = g \cdot \sum_{x_{X'}} f$ and $P(x_Z) = \sum f \cdot \sum g$, and then $P(x_{X'}, x_{Y'}, x_Z) P(x_Z) = P(x_{X'}, x_Z) P(x_{Y'}, x_Z)$. Summing out the parts of $X'$ and $Y'$ outside $X$ and $Y$ keeps the independence. $\blacksquare$

**Completeness.** If $X$ and $Y$ are d-connected given $Z$, then some $P$ that factorizes over $G$ has $X$ and $Y$ dependent given $Z$ (Geiger, Verma and Pearl 1990). Meek (1995) proved more: for discrete variables with any fixed numbers of states, the tables for which some d-connection is still an independence form a set of Lebesgue measure zero in the space of all tables. So for almost all parameters, the independences of $P$ are exactly the d-separations of $G$; such a $P$ is called *faithful* to $G$. Unfaithful parameters do exist, as the third example below shows.

**Equivalent forms.** The moral ancestral graph criterion above is one. Another is the directed global [Markov property](/markov-property/): a distribution satisfies all d-separation statements of $G$ if and only if it factorizes over $G$, with no positivity condition (Lauritzen 1996, Section 3.2.2). Two DAGs have the same d-separations if and only if they have the same skeleton and the same v-structures, which is the Markov equivalence used in [structure learning](/bayesian-network-structure-learning/).

## Examples

**A five node network.** Take $A \to B$, $A \to C$, $B \to D$, $C \to D$, $D \to E$. The trails between $B$ and $C$ are $B \leftarrow A \to C$ (a fork at $A$) and $B \to D \leftarrow C$ (a collider at $D$).

- Given $\emptyset$: the fork is open, so $B$ and $C$ are d-connected.
- Given $\{A\}$: the fork is blocked and the collider is closed, so $B \perp_G C \mid A$.
- Given $\{A, E\}$: the fork is blocked but $E$ is a descendant of the collider $D$, so the collider trail is active and $B$ and $C$ are d-connected.
- Given $\{D\}$: $A$ and $E$ are d-separated, since both trails from $A$ to $E$ pass through $D$ as a chain.

**Explaining away, with numbers.** Let a burglary $B$ and an earthquake $Q$ be independent causes of an alarm $L$, with $P(B = 1) = 0.1$, $P(Q = 1) = 0.2$, and $P(L = 1 \mid B, Q)$ equal to $0.01$, $0.3$, $0.9$ and $0.95$ for $(B, Q) = (0,0), (0,1), (1,0), (1,1)$. The collider $B \to L \leftarrow Q$ makes $B \perp_G Q$, and indeed $P(B = 1 \mid Q = 1) = 0.1 = P(B = 1)$. Given the alarm, the collider opens: $P(B = 1 \mid L = 1) = 455/761 \approx 0.598$, but $P(B = 1 \mid L = 1, Q = 1) = 19/73 \approx 0.260$. Learning of the earthquake explains the alarm away, so $B$ and $Q$ are dependent given $L$.

**An unfaithful network.** Take $A \to B \to C$ and $A \to C$ with $P(A = 1) = 1/2$, $P(B = 1 \mid A) = 1/4$ or $3/4$ for $A = 0$ or $1$, and $P(C = 1 \mid A, B) = 1/4$ when $A = B$ and $3/4$ when $A \ne B$. Then $P(C = 1 \mid A = 0) = P(C = 1 \mid A = 1) = 3/8$, so $A \perp C$, although $A$ and $C$ are adjacent and so d-connected. The direct effect and the effect through $B$ cancel. Meek's theorem says that such cancellations need exact equalities between the parameters.

## Where it is used

- **Queries and algorithms.** The [d-separation query](/d-separation-query/) is decided in linear time by the reachable set algorithm or by [Bayes-Ball](/bayes-ball/).
- **Markov blankets.** The [Markov blanket](/markov-blanket/) of a node in a DAG, its parents, children and co-parents, is the smallest set that d-separates it from all other nodes.
- **Markov properties.** The local directed [Markov property](/markov-property/) is a special case of d-separation.
- **Causal inference.** The [backdoor criterion](/backdoor-criterion/) and the three rules of the [do-calculus](/do-calculus/) are d-separation conditions in modified graphs of a [structural causal model](/structural-causal-model/).
- **Structure learning.** Constraint-based methods for [Bayesian network structure learning](/bayesian-network-structure-learning/), such as the PC algorithm, assume faithfulness and read the graph back from independence tests.
- **Inference.** Nodes d-separated from the query given the evidence can be dropped before [variable elimination](/variable-elimination/).

## References
