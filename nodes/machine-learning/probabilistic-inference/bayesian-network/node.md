---
tag: BFMEF2
kind: model
slug: bayesian-network
name: Bayesian network
aliases:
- belief network
- Bayes net
area: machine-learning/probabilistic-inference
level: core
summary: "A DAG over random variables with one conditional distribution per node given its parents. The joint is their product; each node is independent of its non-descendants given its parents."
history:
  year: 1988
  people: [Judea Pearl]
  note: Pearl's 1988 book set out Bayesian networks as a representation of uncertain knowledge, with d-separation and exact belief propagation on polytrees.
prereqs: [graphical-model, conditional-probability-table, directed-acyclic-graph, conditional-independence]
see_also: [d-separation, markov-blanket, ancestral-sampling, variable-elimination, cooper-theorem, bayesian-network-structure-learning, markov-random-field, factor-graph]
sources:
  - book: isbn:9781558604797
    title: "Judea Pearl, Probabilistic Reasoning in Intelligent Systems, Morgan Kaufmann, 1988"
    locator: Chapter 3, Section 3.3 (Bayesian networks, the factorization and d-separation) and Chapter 4 (belief propagation in trees and polytrees)
  - book: isbn:9780262013192
    title: "Daphne Koller and Nir Friedman, Probabilistic Graphical Models, MIT Press, 2009"
    locator: Chapter 3 (factorization, local independences, I-maps, d-separation, I-equivalence) and Chapter 9 (variable elimination and the NP-hardness of exact inference)
  - paper: doi:10.1016/0004-3702(90)90060-D
    title: "Gregory F. Cooper, The Computational Complexity of Probabilistic Inference Using Bayesian Belief Networks, Artificial Intelligence 42(2-3), 1990"
    locator: pp. 393-405
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: Section 8.1 (Bayesian networks and their parameter counts) and Section 8.2 (conditional independence and d-separation)
---

A Bayesian network is a [graphical model](/graphical-model/) given by a [directed acyclic graph](/directed-acyclic-graph/) over random variables $X_1, \ldots, X_n$ and, for each node, a conditional distribution of that variable given its parents. The joint distribution is the product of these local distributions. The graph encodes [conditional independences](/conditional-independence/): each variable is independent of its non-descendants given its parents. For discrete variables the local distributions are [conditional probability tables](/conditional-probability-table/), and the network stores $\sum_i (r_i - 1)\prod_{j \in \mathrm{pa}(i)} r_j$ numbers in place of the $\prod_i r_i - 1$ of a full joint table.

## The machine

**Data.** A DAG $G$ on nodes $1, \ldots, n$, with $\mathrm{pa}(i)$ the parents of node $i$; for each node a CPD $p(x_i \mid x_{\mathrm{pa}(i)})$. In the discrete case, $X_i$ has $r_i$ values and the CPD is a table with one row per parent setting.

**Factorization.** The network defines

$$
p(x_1, \ldots, x_n) = \prod_{i=1}^n p(x_i \mid x_{\mathrm{pa}(i)}) .
$$

*It sums to 1, and the CPDs are its conditionals.* List the nodes in a [topological order](/topological-sort/). The last node $x_n$ appears only in its own factor, so summing it out leaves the product over the first $n - 1$ nodes. Repeating gives a total of 1. The same argument shows that for any ancestral set $A$ (closed under taking parents), the marginal $p(x_A)$ is the product of the CPDs of the nodes in $A$.

**The local Markov property.** For each node $i$, with $\mathrm{nd}(i)$ its non-descendants,

$$
X_i \perp X_{\mathrm{nd}(i) \setminus \mathrm{pa}(i)} \mid X_{\mathrm{pa}(i)} .
$$

*Proof from the factorization.* The set $A = \mathrm{nd}(i) \cup \{i\}$ is ancestral: a parent of a non-descendant is a non-descendant, and the parents of $i$ are non-descendants. So $p(x_A) = p(x_i \mid x_{\mathrm{pa}(i)}) \cdot g(x_{\mathrm{nd}(i)})$, where $g$ is the product of the other CPDs in $A$. Dividing by $p(x_{\mathrm{nd}(i)}) = g(x_{\mathrm{nd}(i)})$ gives $p(x_i \mid x_{\mathrm{nd}(i)}) = p(x_i \mid x_{\mathrm{pa}(i)})$, which depends on the non-descendants only through the parents. Conversely, if $p$ has the local Markov property, the chain rule in topological order gives the factorization, because each $p(x_i \mid x_1, \ldots, x_{i-1})$ conditions on a set of non-descendants that contains the parents. So the two are equivalent.

**Global independences.** All the independences implied by the factorization are found by [d-separation](/d-separation/). In particular, a node is independent of all others given its [Markov blanket](/markov-blanket/): its parents, its children, and the other parents of its children.

**Queries.** Given evidence $E = e$, compute $P(X_q \mid e)$, the probability of the evidence $P(e)$, or the most probable assignment. The reference method enumerates all assignments:

$$
P(X_q = x \mid e) = \frac{\sum_{y} p(x, e, y)}{\sum_{x', y} p(x', e, y)},
$$

with $y$ ranging over the other variables. It costs $O(n \prod_i r_i)$ operations. [Ancestral sampling](/ancestral-sampling/) draws exact samples from $p$ by sampling the nodes in topological order.

## What it counts

**Parameters.** A node with $r_i$ values and parents with $r_j$ values needs $(r_i - 1)\prod_{j \in \mathrm{pa}(i)} r_j$ free numbers. For $n$ binary variables with at most $k$ parents each, that is at most $n\,2^k$, against $2^n - 1$ for the joint.

**Example: the sprinkler network.** Cloudy $C$ is a parent of Sprinkler $S$ and of Rain $R$, and both are parents of WetGrass $W$. With

- $P(C = 1) = 1/2$,
- $P(S = 1 \mid C = 0) = 1/2$ and $P(S = 1 \mid C = 1) = 1/10$,
- $P(R = 1 \mid C = 0) = 1/5$ and $P(R = 1 \mid C = 1) = 4/5$,
- $P(W = 1 \mid S, R) = 0, 9/10, 9/10, 99/100$ for $(S, R) = (0,0), (1,0), (0,1), (1,1)$,

the network has $1 + 2 + 2 + 4 = 9$ free numbers, against 15 for a joint table on four binary variables. Enumeration gives $P(W = 1) = 6471/10000$, $P(R = 1 \mid W = 1) = 509/719 \approx 0.708$ and $P(S = 1 \mid W = 1) = 309/719 \approx 0.430$. Also $P(S = 1 \mid W = 1, R = 1) = 99/509 \approx 0.195$. Learning that it rained lowers the belief that the sprinkler ran, because rain already explains the wet grass. This effect, called explaining away, comes from the v-structure $S \to W \leftarrow R$: $S \perp R \mid C$ holds, but $S \not\perp R \mid \{C, W\}$.

**Inference cost.** Enumeration is exponential in $n$. [Variable elimination](/variable-elimination/) and the [junction tree](/junction-tree/) method take time exponential only in the treewidth of the moral graph. On a polytree (a DAG whose undirected skeleton has no cycle), Pearl's [belief propagation](/belief-propagation/) is exact in time linear in the total size of the CPTs.

## Relation to other models

- **Markov random fields.** Moralizing (joining each pair of parents of a common child and dropping directions) turns a Bayesian network into a [Markov random field](/markov-random-field/) with the CPDs as clique potentials and $Z = 1$. The moral graph can lose independences such as $S \perp R \mid C$ above; v-structures have no undirected perfect map.
- **Factor graphs.** Each CPD becomes one factor joined to the node and its parents; see [factor graph](/factor-graph/).
- **Special cases.** [Hidden Markov models](/hidden-markov-model/) and linear Gaussian state space models (the [Kalman filter](/kalman-filter/)) are chain-shaped networks unrolled over time. The [naive Bayes classifier](/naive-bayes-classifier/) has the class as the only parent of every feature.
- **Markov equivalence.** Different DAGs can encode the same independences: $A \to B \to C$, $A \leftarrow B \leftarrow C$ and $A \leftarrow B \to C$ all say $A \perp C \mid B$. Two DAGs are equivalent exactly when they have the same skeleton and the same v-structures (Koller and Friedman, Chapter 3). So data alone cannot orient every arc, which limits [structure learning](/bayesian-network-structure-learning/).

## Known results in the model

- **Factorization, local Markov and global Markov are equivalent.** A distribution factorizes over $G$ if and only if it satisfies the local Markov property, if and only if every d-separation in $G$ is an independence of the distribution (Koller and Friedman, Chapter 3).
- **Inference is NP-hard.** Deciding whether $P(X_q = 1) > 0$ in a network with binary variables is NP-hard, by a reduction from 3-SAT: one root per propositional variable, one deterministic OR node per clause, and an AND node over the clauses, so the AND node has positive probability exactly when the formula is satisfiable ([Cooper's theorem](/cooper-theorem/), 1990). So no exact algorithm runs in polynomial time on all networks unless P = NP.
- **Tractable structure.** Exact inference takes time polynomial in the size of the CPTs for networks of bounded treewidth, and linear time on polytrees.
- **Learning.** With complete data, the log-likelihood is a sum of one term per CPT row, so the [maximum likelihood](/maximum-likelihood-estimation/) estimate is the table of conditional frequencies $N(x_i, u)/N(u)$. With hidden variables or missing data it is fitted by [expectation maximization](/expectation-maximization/).

## References
