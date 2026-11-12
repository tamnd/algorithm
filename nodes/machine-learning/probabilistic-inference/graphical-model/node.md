---
tag: QJW75C
kind: model
slug: graphical-model
name: Graphical model
aliases:
- probabilistic graphical model
- PGM
area: machine-learning/probabilistic-inference
level: core
summary: "A family of joint distributions that factorize over a graph whose nodes are random variables. Missing edges are conditional independences; directed and undirected graphs differ."
history:
  year: 1988
  people: [Judea Pearl, Steffen L. Lauritzen, David J. Spiegelhalter]
  note: Pearl's 1988 book set out Bayesian networks and d-separation, and Lauritzen and Spiegelhalter gave exact inference by local computation on a junction tree in the same year.
prereqs: [conditional-independence, probability-distribution]
see_also: [bayesian-network, markov-random-field, factor-graph, d-separation, marginal-inference, variable-elimination, junction-tree, treewidth]
sources:
  - book: isbn:9780262013192
    title: "Daphne Koller and Nir Friedman, Probabilistic Graphical Models, MIT Press, 2009"
    locator: Chapter 3 (Bayesian networks, I-maps, d-separation and perfect maps), Chapter 4 (Markov networks and the relation between directed and undirected models) and Chapter 9 (variable elimination and its complexity)
  - book: isbn:9781558604797
    title: "Judea Pearl, Probabilistic Reasoning in Intelligent Systems, Morgan Kaufmann, 1988"
    locator: Chapter 3 (Markov and Bayesian networks as graphical representations of dependencies)
  - book: isbn:9780198522195
    title: "Steffen L. Lauritzen, Graphical Models, Oxford University Press, 1996"
    locator: Chapter 3 (conditional independence and Markov properties for undirected and directed graphs)
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: Chapter 8, in particular Section 8.3.4 (relation between directed and undirected graphs, with the v-structure and 4-cycle examples)
  - paper: doi:10.1111/j.2517-6161.1988.tb01721.x
    title: "S. L. Lauritzen and D. J. Spiegelhalter, Local Computations with Probabilities on Graphical Structures and Their Application to Expert Systems, Journal of the Royal Statistical Society B 50(2), 1988"
    locator: pp. 157-194
  - paper: doi:10.1214/088342304000000026
    title: "Michael I. Jordan, Graphical Models, Statistical Science 19(1), 2004"
    locator: pp. 140-155
---

A graphical model is a family of joint probability distributions over random variables $X_1, \ldots, X_n$, described by a graph with one node per variable. A distribution belongs to the family when it factorizes into local terms, one for each node and its parents in a directed graph, or one for each clique in an undirected graph. Missing edges then mean conditional independences that can be read off the graph. The two main kinds, [Bayesian networks](/bayesian-network/) and [Markov random fields](/markov-random-field/), express different sets of independences, and [factor graphs](/factor-graph/) describe the factorization of either kind exactly.

## The machine

A graphical model has three parts: a graph, a family of local functions on the graph, and the rule that multiplies them into a joint distribution.

**Directed (Bayesian network).** The graph $G$ is a [directed acyclic graph](/directed-acyclic-graph/). Each node has a conditional distribution given its parents $\mathrm{pa}(i)$, for discrete variables a [conditional probability table](/conditional-probability-table/), and

$$
p(x_1, \ldots, x_n) = \prod_{i=1}^n p(x_i \mid x_{\mathrm{pa}(i)}) .
$$

The product sums to 1 without any normalization. The independences are read off by [d-separation](/d-separation/).

**Undirected (Markov random field).** The graph $H$ is undirected. Each [clique](/clique/) $C$ carries a nonnegative potential $\psi_C$, and

$$
p(x) = \frac{1}{Z}\prod_{C} \psi_C(x_C), \qquad Z = \sum_x \prod_C \psi_C(x_C),
$$

where $Z$ is the [partition function](/partition-function/). The independences are read off by graph separation: $A \perp B \mid S$ when every path from $A$ to $B$ passes through $S$.

**Factor graph.** A [bipartite graph](/bipartite-graph/) with variable nodes and factor nodes, and $p(x) \propto \prod_a f_a(x_{N(a)})$. It shows exactly which variables share a factor, which the other two kinds do not always show.

**The graph as a list of independences.** Write $I(G)$ for the set of [conditional independence](/conditional-independence/) statements that the graph implies, and $I(p)$ for the set that hold in a distribution $p$. Then $G$ is an *I-map* of $p$ when $I(G) \subseteq I(p)$, and a *perfect map* when $I(G) = I(p)$. The complete graph is an I-map of every distribution and says nothing. A useful model has a sparse graph that is still an I-map.

**Queries.** Given evidence $E = e$, the standard questions are a [marginal](/marginal-inference/) $p(x_i \mid e)$, the most probable assignment ([MAP inference](/map-inference/)), the partition function or the probability of the evidence $p(e)$, samples from $p(x \mid e)$, and learning the local functions or the graph from data.

## What it counts

- **Parameters.** A full joint table over $n$ binary variables has $2^n - 1$ free numbers. A Bayesian network in which each node has at most $k$ parents has at most $n\,2^k$. A pairwise Markov random field with $|E|$ edges has $O(n + |E|)$ potential values for binary variables. The graph turns an exponential table into a sum of local sizes.
- **Inference cost.** Exact inference by [variable elimination](/variable-elimination/) along an ordering whose largest intermediate factor has $w + 1$ variables, each with at most $r$ values, takes $O(m\,r^{w+1})$ arithmetic operations for $m$ factors. The best $w$ over all orderings is the [treewidth](/treewidth/) of the moral or undirected graph. On a tree $w = 1$, and [belief propagation](/belief-propagation/) is exact in time linear in $n$.
- **Learning cost.** With complete data, the likelihood of a Bayesian network splits into one term per CPT, and each is fitted by counting. The likelihood of a Markov random field contains $\log Z$, which couples all potentials, so each gradient step needs inference.

## Relation to other models

**Directed and undirected graphs express different independences.**

*A v-structure has no undirected perfect map.* Take the DAG $A \to C \leftarrow B$, with $A$ and $B$ independent causes of $C$. In a typical distribution on it, the only independence among the three variables is $A \perp B$. Knowing $C$ couples the causes, so $A \not\perp B \mid C$. An undirected graph on $\{A, B, C\}$ must join $A$ to $C$ and $B$ to $C$, because those pairs are dependent given every set. If it also joins $A$ and $B$, it misses $A \perp B$. If it does not, separation gives $A \perp B \mid C$, which is false. The test file checks all 8 undirected graphs on three nodes against a distribution with $P(C = 1 \mid a, b) = 1/10, 6/10, 7/10, 9/10$.

*A 4-cycle has no directed perfect map.* Take the undirected cycle $A - B - C - D - A$ with generic pairwise potentials. Its independences are exactly $A \perp C \mid \{B, D\}$ and $B \perp D \mid \{A, C\}$. A DAG with these independences must have the same four edges and no chord, since adjacent pairs are dependent given every set. Any acyclic orientation of a cycle has a node whose two cycle edges both point into it. In a 4-cycle the two neighbors of that node are not adjacent, so they form a v-structure $B \to A \leftarrow D$ (up to names). Then conditioning on $\{A, C\}$ activates the path through $A$, and the DAG does not imply $B \perp D \mid \{A, C\}$. The test file checks all 543 DAGs on four labeled nodes against a distribution on the cycle.

**Where they agree.** Moralizing a DAG (joining every pair of parents of a common child and dropping directions) gives an undirected I-map of the same distribution, which may lose independences. It loses none exactly when the DAG has no v-structure whose two parents are non-adjacent. In the other direction, an undirected graph has a DAG with the same independences exactly when it is [chordal](/chordal-graph/) (Koller and Friedman, Chapter 4). Models on chordal graphs are called decomposable.

**Factor graphs** refine both. A triangle in an undirected graph may carry one factor on three variables or three pairwise factors; the factor graph shows which. Every Bayesian network and every Markov random field converts to a factor graph with the same joint distribution.

**Special cases.** [Hidden Markov models](/hidden-markov-model/) and the [Kalman filter](/kalman-filter/) are chain-structured Bayesian networks. The [Ising model](/ising-model/) and the [Potts model](/potts-model/) are pairwise Markov random fields on grids. A [conditional random field](/conditional-random-field/) is a Markov random field over outputs, conditioned on inputs. The [naive Bayes classifier](/naive-bayes-classifier/) is a Bayesian network in which the class is the only parent of each feature.

## Known results in the model

- **Directed Markov properties.** For a distribution on a DAG, factorization, the local Markov property (each node is independent of its non-descendants given its parents), and the global property (d-separation implies independence) are equivalent (Lauritzen, Chapter 3; Koller and Friedman, Chapter 3).
- **Completeness of d-separation.** d-separation finds every independence that holds in all distributions that factorize over the DAG; for a statement that it does not imply, some such distribution violates it (Koller and Friedman, Section 3.3).
- **Undirected Markov properties.** Factorization implies the global, local and pairwise Markov properties, in that order. For strictly positive distributions all four are equivalent: this is the Hammersley-Clifford theorem, treated on the [Markov random field](/markov-random-field/) page with its counterexample when positivity fails.
- **Hardness.** Exact marginal inference in Bayesian networks is NP-hard ([Cooper's theorem](/cooper-theorem/), 1990), and computing the partition function of a general Markov random field is #P-hard. So no exact method is fast on all graphs; the treewidth bound above is the main tractable case.
- **Exact algorithms.** Variable elimination and the [junction tree](/junction-tree/) method are exact, with cost exponential in the treewidth. Belief propagation is exact on trees and is used as an approximation on graphs with cycles. Sampling ([Gibbs sampling](/gibbs-sampling/)) and variational methods ([variational inference](/variational-inference/)) are the main approximate methods.

## References
