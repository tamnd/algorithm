---
tag: Q3KGA9
kind: algorithm
slug: chow-liu-algorithm
name: Chow-Liu algorithm
aliases:
- Chow-Liu tree
- Chow-Liu dependence tree
area: machine-learning/probabilistic-inference
level: core
summary: "Learns the maximum-likelihood tree-shaped Bayesian network from discrete data: a maximum weight spanning tree under empirical mutual information weights."
solves: [bayesian-network-structure-learning]
model: real-ram
complexity:
  vars: {n: the number of variables, s: the number of samples, r: the largest number of states of a variable}
  time: {worst: "O(n^2 (s + r^2 + log n))"}
  space: {extra: "O(n^2 + n r^2)"}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1968
  people: [C. K. Chow, C. N. Liu]
  note: Chow and Liu showed that the best tree approximation of a discrete distribution, in Kullback-Leibler divergence, is a maximum weight spanning tree under mutual information weights, and that the same tree built from data is the maximum likelihood estimate.
prereqs: [maximum-spanning-tree, maximum-likelihood-estimation, bayesian-network]
see_also: [kruskal, prim, conditional-entropy, shannon-entropy, edmonds-arborescence, bayesian-network-structure-learning, disjoint-set, belief-propagation]
sources:
  - paper: doi:10.1109/TIT.1968.1054142
    title: C. K. Chow and C. N. Liu, Approximating discrete probability distributions with dependence trees, IEEE Transactions on Information Theory 14(3), 1968, pages 462 to 467
    locator: the product approximation by a dependence tree, the reduction to a maximum weight spanning tree under mutual information, and the maximum likelihood property of the tree built from samples
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 18 (structure learning in Bayesian networks): learning tree-structured networks by a maximum weight spanning tree"
  - paper: doi:10.1023/A:1007465528199
    title: Nir Friedman, Dan Geiger and Moises Goldszmidt, Bayesian network classifiers, Machine Learning 29, 1997, pages 131 to 163
    locator: the tree-augmented naive Bayes classifier, a Chow-Liu tree under mutual information conditional on the class
  - paper: doi:10.1090/S0002-9939-1956-0078686-7
    title: Joseph B. Kruskal, On the shortest spanning subtree of a graph and the traveling salesman problem, Proceedings of the American Mathematical Society 7(1), 1956, pages 48 to 50
    locator: the greedy spanning tree algorithm used in lines L3 to L7
---

The Chow-Liu algorithm learns the best tree-shaped [Bayesian network](/bayesian-network/) from discrete data. It weights each pair of variables by their empirical mutual information, takes a [maximum spanning tree](/maximum-spanning-tree/) of the complete graph under these weights, points the edges away from any root, and fills in the tables with the observed conditional frequencies. C. K. Chow and C. N. Liu proved in 1968 that this tree has the largest likelihood among all trees. It is the one case of [Bayesian network structure learning](/bayesian-network-structure-learning/) with an exact polynomial-time algorithm, and it costs about $n^2$ passes over the data for $n$ variables.

## In plain words

You have a table of observations of many variables and want a simple model in which each variable depends on at most one other variable. For each pair of variables, measure how much knowing one tells you about the other. Then build a tree that links all the variables and uses the strongest links possible: take the strongest link first, then the next strongest one that does not close a loop, and so on. Pick any variable as the top of the tree, let every link point away from it, and record how often each value of a variable follows each value of the variable above it. No other tree explains the data better.

## The problem

The input is a data set of $s$ samples of $n$ discrete variables $X_1, \dots, X_n$, where variable $X_v$ takes at most $r$ values. Here $n$ counts variables, the nodes of the network, and $s$ counts samples. A *tree-shaped network* is a Bayesian network whose DAG is a directed tree: one root with no parent, and every other node with exactly one parent. Its tables give $P(x_v \mid x_{\mathrm{pa}(v)})$. The output is the tree and the tables that maximize the likelihood $\prod_t P(x^{(t)})$ of the data.

The weight of a pair is the empirical *mutual information*

$$\hat I(X_u; X_v) = \sum_{a, b} \hat P(a, b) \log \frac{\hat P(a, b)}{\hat P(a)\, \hat P(b)},$$

where $\hat P$ are the observed frequencies. It is zero exactly when the observed frequencies of $X_u$ and $X_v$ are independent, and it is never negative. It equals $\hat H(X_v) - \hat H(X_v \mid X_u)$, with the [Shannon entropy](/shannon-entropy/) and the [conditional entropy](/conditional-entropy/) of $\hat P$.

## The algorithm

```pseudo id=main
CHOW-LIU(D, n, root)
L1  for each pair i < j of variables do
L2      w(i, j) ← the mutual information of X_i and X_j in the counts of D
L3  sort the pairs by w in decreasing order
L4  make a singleton set for each variable ;  T ← no edges
L5  for each pair (i, j) in this order do
L6      if FIND(i) ≠ FIND(j) then
L7          add the edge ij to T ;  UNION(i, j)
L8  orient every edge of T away from root by a graph search
L9  for each variable v do
L10     θ_v(a | b) ← N(x_v = a, x_pa(v) = b) / N(x_pa(v) = b)   (for root, θ(a) ← N(x_root = a) / s)
L11 return the directed tree and the tables θ
```

Lines L3 to L7 are [Kruskal's algorithm](/kruskal/) for a maximum spanning tree, with a [disjoint-set](/disjoint-set/) structure for FIND and UNION. Any other maximum spanning tree algorithm, such as [Prim's](/prim/), gives a tree of the same weight and the same likelihood. Line L10 counts with $N(\cdot)$ the samples that match.

## Example

Take four binary variables $A, B, C, D$ and the eight samples

| $A$ | $B$ | $C$ | $D$ | count |
|---|---|---|---|---|
| 0 | 1 | 1 | 0 | 3 |
| 0 | 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 | 2 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 1 | 0 | 1 |

Lines L1 and L2 give the weights, in nats, rounded to four places:

| pair | $AB$ | $BC$ | $AC$ | $AD$ | $BD$ | $CD$ |
|---|---|---|---|---|---|---|
| $\hat I$ | 0.3804 | 0.3236 | 0.2158 | 0.0956 | 0.0640 | 0.0388 |

The loop of lines L5 to L7 goes through the pairs in this order:

| step | pair | sets before | action |
|---|---|---|---|
| 1 | $AB$ | $\{A\}, \{B\}, \{C\}, \{D\}$ | add $AB$ |
| 2 | $BC$ | $\{A, B\}, \{C\}, \{D\}$ | add $BC$ |
| 3 | $AC$ | $\{A, B, C\}, \{D\}$ | skip: $A$ and $C$ are in one set, so $AC$ closes a loop |
| 4 | $AD$ | $\{A, B, C\}, \{D\}$ | add $AD$ |
| 5, 6 | $BD$, $CD$ | $\{A, B, C, D\}$ | skip |

With root $A$, line L8 gives $A \to B$, $B \to C$ and $A \to D$, and line L10 gives $P(A = 1) = 1/2$, $P(B = 1 \mid A = 0) = 1$, $P(B = 1 \mid A = 1) = 1/4$, $P(C = 1 \mid B = 1) = 1$, $P(C = 1 \mid B = 0) = 1/3$, $P(D = 1 \mid A = 0) = 1/4$ and $P(D = 1 \mid A = 1) = 0$. The likelihood of the data is $27 / 2^{22}$, with log-likelihood $-11.953$. Of the $4^2 = 16$ spanning trees on four nodes, the next best one, with edges $AB$, $BC$, $BD$, has log-likelihood $-12.206$, and the model with no edges has $-18.351$.

## Correctness

**Theorem (Chow and Liu 1968).** The output has the largest likelihood among all tree-shaped Bayesian networks on the $n$ variables.

The proof has two steps. First, for a fixed tree, the best tables are the observed conditional frequencies of line L10, by Gibbs' inequality. With these tables the log-likelihood is

$$\ell^*(T) = s \sum_{uv \in T} \hat I(X_u; X_v) - s \sum_v \hat H(X_v).$$

The second sum is the same for all trees, and the first depends only on the undirected edges, since mutual information is symmetric. So the best tree is a maximum weight spanning tree, whatever the root. Second, lines L3 to L7 find a maximum weight spanning tree, by the exchange argument for Kruskal's algorithm. The full proof is below. The tests compare the likelihood of the output, in exact rational arithmetic, with the likelihood of all $n^{n-2}$ spanning trees ([Cayley's formula](/cayley-formula/)) for $n \le 5$.

## Complexity

- **Weights.** Each of the $\binom{n}{2}$ pairs needs one pass over the $s$ samples to count the joint values, and $O(r^2)$ work to sum the terms. That is $O(n^2 (s + r^2))$ time.
- **Tree.** Sorting the pairs takes $O(n^2 \log n)$ time, and the union-find loop takes $O(n^2 \alpha(n))$. Prim's algorithm on the dense graph takes $O(n^2)$, which removes the logarithm.
- **Tables.** Line L10 is one more pass over the data per variable, $O(n s)$ time, and the tables hold $O(n r^2)$ numbers.
- **Total.** $O(n^2 (s + r^2 + \log n))$ time and $O(n^2 + n r^2)$ extra space for the weights and the tables. The weights are the main cost when $s$ is large.

## Properties

- **Exact and polynomial.** It finds a global optimum. Over general DAGs, even with at most two parents per node, the same problem is NP-hard (see [structure learning](/bayesian-network-structure-learning/)).
- **Root free.** All orientations of the tree have the same likelihood and are Markov equivalent: a directed tree has no v-structures.
- **Always a spanning tree.** Mutual information is never negative, so adding an edge never lowers the likelihood. With a penalty such as BIC, the best structure is a forest.
- **Consistent.** If the data come from a distribution that is Markov to a tree, and the true mutual informations on the tree edges are strictly larger than the ones that compete with them, the algorithm finds the true tree with probability tending to one as $s$ grows.
- **Fast inference.** The result is a tree, so exact inference by [belief propagation](/belief-propagation/) takes linear time.

## Variants and improvements

- **Penalized trees and forests.** Replace $\hat I(X_u; X_v)$ by $\hat I(X_u; X_v)$ minus a penalty for the extra parameters of the edge, as in BIC, and drop the edges with negative weight. Kruskal's algorithm then stops with a forest.
- **Bayesian scores and branchings.** With a decomposable score, the gain of each directed edge $u \to v$ can be computed. If the score gives the same value to Markov equivalent networks, the gain is symmetric and a maximum spanning tree is optimal. If not, the best directed tree is a maximum branching, found by [Edmonds' algorithm](/edmonds-arborescence/) (Heckerman, Geiger and Chickering 1995).
- **Tree-augmented naive Bayes.** For classification, Friedman, Geiger and Goldszmidt (1997) use the mutual information of $X_u$ and $X_v$ given the class, build the tree over the features, and add the class as a parent of every feature.
- **Gaussian data.** For jointly normal variables, $I(X_u; X_v) = -\tfrac12 \log(1 - \rho_{uv}^2)$, so the tree is a maximum spanning tree under the absolute correlations.
- **Mixtures of trees.** Meila and Jordan (2000) fit a mixture of Chow-Liu trees by expectation maximization, with one weighted Chow-Liu step per component.

## When to use it

Use it when you want a fast, exact baseline structure, a model with cheap exact inference, or the first step of a search over richer structures. It also serves as a density estimator and as a classifier through tree-augmented naive Bayes. Do not use it when the variables have strong dependences among three or more of them that a tree cannot express. Then use a score-based or constraint-based method for general DAGs, at a much higher cost.

## Pitfalls

- **Treating the root as meaningful.** The direction of the edges is arbitrary. It does not say which variable causes which.
- **Reading a missing edge as independence.** The tree always has $n - 1$ edges and drops the others, even if they are strong. A missing edge only says that the tree had a better use for its edges.
- **Estimating mutual information from few samples.** The plug-in estimate is biased upward, and every pair gets a positive weight from noise. With small $s$, prefer a penalized score, or smoothed counts.
- **Zero counts in the tables.** The maximum likelihood tables can contain zeros, as $P(D = 1 \mid A = 1) = 0$ in the example. A new sample with that pattern gets probability zero. Add pseudo-counts if the model will score new data.
- **Using a minimum spanning tree routine.** Negate the weights, or sort in decreasing order. A minimum spanning tree under mutual information gives the worst tree.

## Implementations

## History

C. K. Chow and C. N. Liu (1968) asked how to approximate a distribution of many discrete variables by a product of second order terms. They showed that the best such approximation in Kullback-Leibler divergence is a dependence tree built on a maximum weight spanning tree under mutual information, found with Kruskal's 1956 algorithm, and that the tree built from sample frequencies is the maximum likelihood estimate. Later work used the tree as a learning method for Bayesian networks, extended it to Bayesian scores and branchings (Heckerman, Geiger and Chickering 1995), to classifiers (Friedman, Geiger and Goldszmidt 1997) and to mixtures (Meila and Jordan 2000).

## References
