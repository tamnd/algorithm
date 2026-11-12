---
tag: RT2GC9
kind: algorithm
slug: junction-tree-algorithm
name: Junction tree algorithm
aliases:
- Hugin algorithm
- Lauritzen-Spiegelhalter algorithm
- Shafer-Shenoy algorithm
- clique tree propagation
area: machine-learning/probabilistic-inference
level: advanced
summary: "Exact inference: build a junction tree of the moral graph, then pass messages to a root and back. Every clique then holds its exact joint marginal."
solves: [marginal-inference]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of factors, d: the largest domain size, w: the induced width of the order}
  time: {worst: "O(n^3 + (n + m) d^(w+1))"}
  space: {extra: "O(n d^(w+1))"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1988
  people: [Steffen L. Lauritzen, David J. Spiegelhalter]
  note: "Local computation on the cliques of the triangulated moral graph; the Hugin and Shafer-Shenoy forms followed in 1990."
prereqs: [junction-tree, variable-elimination, bayesian-network]
see_also: [belief-propagation, message-passing, elimination-ordering, max-product, loopy-belief-propagation, generalized-belief-propagation, forward-backward-algorithm, bucket-elimination]
sources:
  - paper: doi:10.1111/j.2517-6161.1988.tb01721.x
    title: "Steffen L. Lauritzen and David J. Spiegelhalter, Local computations with probabilities on graphical structures and their application to expert systems, Journal of the Royal Statistical Society, Series B 50(2), 1988, pages 157 to 224"
    locator: moralization, triangulation, the cliques with the running intersection property, and the propagation of evidence between cliques
  - paper: "Finn V. Jensen, Steffen L. Lauritzen and Kristian G. Olesen, Bayesian updating in causal probabilistic networks by local computations, Computational Statistics Quarterly 4, 1990, pages 269 to 282"
    title: Jensen, Lauritzen and Olesen 1990
    locator: the Hugin architecture with separator tables, and the collect and distribute passes
  - paper: doi:10.1007/BF01531015
    title: "Glenn Shafer and Prakash P. Shenoy, Probability propagation, Annals of Mathematics and Artificial Intelligence 2, 1990, pages 327 to 351"
    locator: propagation in join trees with messages and no division
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 10, Sections 10.2 (sum-product message passing in clique trees) and 10.3 (belief update with separator division)"
---

The junction tree algorithm computes exact [marginals](/marginal-inference/) of a [Bayesian network](/bayesian-network/) or a [Markov random field](/markov-random-field/), for all variables at once. It joins the variables that share a factor (for a Bayesian network this is the moral graph), triangulates this graph along an [elimination ordering](/elimination-ordering/), and builds a [junction tree](/junction-tree/) of its cliques. Each factor goes into one clique. Then one pass of messages goes from the leaves to a root and one pass goes back. After the two passes, the table of each clique $C$ is $P(C, e)$, the exact joint marginal of the clique with the evidence $e$. The cost is $O((n + m)\, d^{w+1})$ for an order of induced width $w$, the same as one run of [variable elimination](/variable-elimination/), but it gives the marginals of all the cliques.

## In plain words

Variable elimination answers one question at a time. When you ask about a different variable, it does most of the work again. The junction tree algorithm saves that work.

First it groups the variables into overlapping groups, arranged in a tree, so that two groups that share a variable agree along the whole path between them. Each probability table goes into a group that holds all its variables.

Then the groups talk. In the first pass, each group tells its parent what it knows, starting at the leaves. In the second pass, each group tells its children what the rest of the tree knows. Each message is about the shared variables only.

After the two passes, each group knows the exact probabilities of its own variables, given the evidence.

## The problem

**Input.** Factors $\Phi$ over discrete variables $X_1, \ldots, X_n$ with nonnegative tables, evidence $e$ (values for some variables), and an elimination order $\pi$. For a Bayesian network, $\Phi$ holds one table $P(X_i \mid \mathrm{Pa}(X_i))$ for each variable.

**Output.** For each clique $C_i$ of the junction tree, the table $P(C_i, e)$, and from it $P(e)$ and $P(X \mid e)$ for every variable $X$. For a Markov random field the tables are the marginals of the unnormalized product, and their sum is the [partition function](/partition-function/) with the evidence fixed.

## The algorithm

The pseudocode is the Hugin form: each tree edge keeps a separator table $\mu_{ij}$ over $S_{ij} = C_i \cap C_j$, and a pass divides by the old separator table.

```pseudo id=main
JUNCTION-TREE-ALGORITHM(Φ, e, π)
L1  G ← the graph with an edge between each two variables in a common factor
L2  (C_1..C_k, tree edges) ← BUILD-JUNCTION-TREE(G, π)
L3  φ_i ← 1 for each clique; μ_ij ← 1 for each tree edge
L4  for each factor f in Φ and each evidence indicator [X_v = e_v]: multiply f into one clique that holds its scope
L5  for each non-root clique i, leaves first: PASS(i, parent(i))      ▷ collect
L6  for each non-root clique i, root first: PASS(parent(i), i)        ▷ distribute
L7  return φ_1..φ_k                                                    ▷ φ_i = P(C_i, e); P(e) = Σ φ_i

PASS(i, j)
L8  μ* ← Σ over C_i \ S_ij of φ_i
L9  φ_j ← φ_j · μ* / μ_ij                                             ▷ with 0/0 = 0
L10 μ_ij ← μ*
```

Line L1 gives the moral graph for a Bayesian network: the scope of $P(X \mid \mathrm{Pa}(X))$ is $X$ and its parents, so the parents are joined. Line L2 triangulates along $\pi$, keeps the maximal cliques and joins them by a maximum weight spanning tree, as on the [junction tree](/junction-tree/) page. Line L4 puts each factor into one clique only; a factor put into two cliques would be counted twice. Lines L5 and L6 use a breadth-first order from the root, read backward and then forward.

In the collect pass every old separator table is 1, so line L9 only multiplies. In the distribute pass the division removes from the message what the child itself sent in the collect pass, so no information is counted twice.

**The Shafer-Shenoy form** keeps the clique tables $\psi_i$ fixed and stores one message per direction of each edge:
$$m_{i \to j} = \sum_{C_i \setminus S_{ij}} \psi_i \prod_{c \in N(i) \setminus \{j\}} m_{c \to i}, \qquad \phi_i = \psi_i \prod_{c \in N(i)} m_{c \to i}.$$
It never divides, so it also works where division is not defined, at the cost of more multiplications at cliques with many neighbours. Both forms are in the implementation.

## Example

Take the sprinkler network with $C$ (cloudy), $S$ (sprinkler), $R$ (rain) and $W$ (wet grass): $P(C{=}1) = 0.5$; $P(S{=}1 \mid C) = 0.5, 0.1$ for $C = 0, 1$; $P(R{=}1 \mid C) = 0.2, 0.8$; $P(W{=}1 \mid S, R) = 0, 0.9, 0.9, 0.99$ for $(S, R) = (0,0), (0,1), (1,0), (1,1)$. The evidence is $W = 1$.

The moral graph has the edges $CS, CR, SR, SW, RW$. The order $(W, C, S, R)$ gives the cliques $C_1 = \{S, R, W\}$ and $C_2 = \{C, S, R\}$ with the separator $\{S, R\}$. Line L4 puts $P(W \mid S, R)$ and the indicator $[W = 1]$ into $C_1$, and $P(C)$, $P(S \mid C)$, $P(R \mid C)$ into $C_2$. The root is $C_1$.

**Collect.** $C_2$ sends $\mu^*(S, R) = \sum_C P(C) P(S \mid C) P(R \mid C) = P(S, R)$:

| $(S, R)$ | (0, 0) | (0, 1) | (1, 0) | (1, 1) |
|---|---|---|---|---|
| $\mu^* = P(S, R)$ | 0.29 | 0.41 | 0.21 | 0.09 |
| $\phi_1 = P(S, R, W{=}1)$ | 0 | 0.369 | 0.189 | 0.0891 |

The second row is $\mu^*$ times $P(W{=}1 \mid S, R)$; the rows of $\phi_1$ with $W = 0$ are 0. The sum is $P(W{=}1) = 0.6471$. So $P(R{=}1 \mid W{=}1) = (0.369 + 0.0891)/0.6471 = 509/719 \approx 0.708$ and $P(S{=}1 \mid W{=}1) = (0.189 + 0.0891)/0.6471 = 309/719 \approx 0.430$.

**Distribute.** $C_1$ sends $\mu^* = \sum_W \phi_1 = (0, 0.369, 0.189, 0.0891)$. The old separator table is $P(S, R)$, so line L9 multiplies $\phi_2(C, S, R)$ by $\mu^*/\mu = (0, 0.9, 0.9, 0.99)$, which is $P(W{=}1 \mid S, R)$. Now $\phi_2 = P(C, S, R, W{=}1)$, and $P(C{=}1 \mid W{=}1) = 414/719 \approx 0.576$. Both tables give the same $P(S, R, W{=}1)$ on the separator. Two messages were sent, $2(k - 1)$ for $k = 2$ cliques.

## Correctness

Root the tree. Let $\Psi_i$ be the product of the factors put into the subtree below clique $i$. The running intersection property gives two facts. The variables below $i$ that also occur elsewhere are in the separator to the parent. The subtrees of the children of $i$ share no variable outside $C_i$. So a sum over the variables below $i$ splits into a product of sums, one for each child. By induction from the leaves, the message that $i$ sends in the collect pass is $\sum \Psi_i$ over all the variables below $i$ that are not in the separator. The root then holds the full marginal of its clique.

In the distribute pass, write the joint as $\Psi_i \cdot R$, where $R$ uses only the separator and the variables outside the subtree. Then the marginal of $C_i$ is the old table of $i$ times a function $\rho$ of the separator. The new message divided by the old one is exactly $\rho$, so line L9 makes the table of $i$ its marginal. Where the old separator entry is 0, the matching entries of $C_i$ are also 0, and the rule $0/0 = 0$ is exact. The full proof, with the Shafer-Shenoy form, is in [the proof page](proofs/correctness.md).

## Complexity

The costs are in the [real RAM](/real-ram/) model, one arithmetic operation per step, worst case. Let $k \le n$ be the number of cliques; each has at most $w + 1$ variables.

| step | time |
|---|---|
| L1, L2: moral graph and junction tree | $O(n^3 + m\, w^2)$ |
| L3, L4: tables and factors | $O((n + m)\, d^{w+1})$ |
| L5, L6: $2(k - 1)$ passes | $O(k\, d^{w+1})$ |
| total | $O(n^3 + (n + m)\, d^{w+1})$ |

A pass from $i$ to $j$ reads $\phi_i$ once and $\phi_j$ once, so it costs $O(d^{|C_i|} + d^{|C_j|})$, and each clique takes part in as many passes as it has edges, twice. Space is $O(n\, d^{w+1})$ for the clique tables; the separator tables are smaller.

The term $d^{w+1}$ dominates. The least $w$ over all orders is the [treewidth](/treewidth/) of the graph of line L1, and finding it is NP-hard, so line L2 uses a heuristic order such as min-fill. No exact method avoids this in general: exact inference is NP-hard by [Cooper's theorem](/cooper-theorem/). Compared with $n$ separate runs of variable elimination, the junction tree algorithm gives all the marginals for about twice the cost of one run.

## Properties

- **Exact.** With exact arithmetic, the result equals the sum over all joint assignments, and it does not depend on the order $\pi$, the tree, or the root.
- **Calibrated.** After the two passes, two neighbouring cliques give the same marginal on their separator.
- **Reuse.** Lines L1 to L3 depend only on the graph. A new set of evidence needs only lines L4 to L7 again. A change of evidence in one clique needs only a distribute pass from that clique, after a collect pass to it.
- **Two passes are enough.** Unlike [loopy belief propagation](/loopy-belief-propagation/), there are no iterations and no convergence test.

## Variants and improvements

- **Lauritzen-Spiegelhalter form.** In the original architecture, a clique divides its own table by the message it sends in the collect pass, so that after the pass the tables hold conditional distributions given the separators. The distribute pass then only multiplies.
- **Max-product.** Replace the sums of line L8 by maxima to get the most probable assignment, as in [max-product](/max-product/); the division of line L9 stays valid with the rule $0/0 = 0$.
- **Other semirings.** The passes only need a sum and a product that distribute, so the same tree computes other quantities, as described on [message passing](/message-passing/).
- **Chains and trees.** When the model is a chain, the cliques are the pairs of neighbours and the algorithm is the [forward-backward algorithm](/forward-backward-algorithm/). When the model is a tree, it is [belief propagation](/belief-propagation/) on that tree.
- **Approximate forms.** When the cliques are too large, [generalized belief propagation](/generalized-belief-propagation/) runs similar passes on a graph of regions that need not be a tree, and the results are approximate.

## When to use it

Use the junction tree algorithm when the induced width of a good order is small (a table of $d^{w+1}$ entries must fit in memory), and when you need many marginals or the same model with many sets of evidence. Expert systems in medicine and diagnosis were the first use. For one marginal, variable elimination is simpler. For a tree-shaped model, belief propagation needs no triangulation. When the width is large, use approximate methods: [loopy belief propagation](/loopy-belief-propagation/), [variational inference](/variational-inference/), or sampling such as [Gibbs sampling](/gibbs-sampling/).

## Pitfalls

- **Forgetting to moralize.** The graph of line L1 must join each two variables in a common factor. A tree built from the directed edges only can have no clique for $P(X \mid \mathrm{Pa}(X))$.
- **A factor in two cliques.** Each factor goes into exactly one clique, or its values are counted twice. The evidence indicators also go into one clique each.
- **Division by zero.** With zeros in the tables, line L9 can meet $0/0$. The rule $0/0 = 0$ is correct here; $x/0$ with $x \ne 0$ does not happen.
- **Underflow.** The products of many small numbers underflow in floating point. Normalize each message and keep the scale factors in log space, or use exact arithmetic for small models.
- **Wrong order of passes.** A clique must send in the collect pass only after all its children have sent, and in the distribute pass only after it has received from its parent. Another order gives tables that are not marginals.

## Implementations

## History

Lauritzen and Spiegelhalter (1988) showed how to do exact inference in Bayesian networks by local computation on the cliques of the triangulated moral graph, ordered with the running intersection property. Jensen, Lauritzen and Olesen (1990) gave the Hugin architecture, with separator tables and the collect and distribute passes; it became the base of the Hugin software. Shafer and Shenoy (1990) gave the architecture without division, in the general setting of valuations. The algorithm extends Pearl's belief propagation on trees (Pearl 1982 and 1988) to all graphs, at a cost exponential in the width.

## References
