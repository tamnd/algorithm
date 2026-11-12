---
tag: SMKERH
kind: algorithm
slug: max-product
name: Max-product algorithm
aliases:
- max-sum algorithm
- min-sum algorithm
- max-product belief propagation
area: machine-learning/probabilistic-inference
level: core
summary: "Belief propagation with max in place of sum. On a factor tree, one pass of messages and a backtracking pass give a most probable assignment."
solves: [map-inference]
model: real-ram
complexity:
  vars: {N: the number of edges of the factor graph, d: the largest domain size, k: the largest scope size, D: the largest number of factors on one variable}
  time: {worst: "O(N (k d^k + D d))"}
  space: {extra: "O(N d)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1988
  people: [Judea Pearl]
  note: "Pearl's belief revision computed the most probable explanation by local messages with maxima; the Viterbi algorithm (1967) is the case of a chain."
prereqs: [belief-propagation, map-inference]
see_also: [viterbi-algorithm, loopy-belief-propagation, junction-tree-algorithm, variable-elimination, message-passing, affinity-propagation, min-plus-matrix-multiplication, maximum-a-posteriori-estimation]
sources:
  - book: isbn:9781558604797
    title: Judea Pearl, Probabilistic Reasoning in Intelligent Systems, Morgan Kaufmann, 1988
    locator: "Chapter 5, belief revision: the most probable explanation by local propagation in trees and polytrees"
  - paper: doi:10.1109/18.910572
    title: "Frank R. Kschischang, Brendan J. Frey and Hans-Andrea Loeliger, Factor graphs and the sum-product algorithm, IEEE Transactions on Information Theory 47(2), 2001, pages 498 to 519"
    locator: the max-product and min-sum forms of the sum-product algorithm as a change of semiring
  - paper: doi:10.1109/18.910585
    title: "Yair Weiss and William T. Freeman, On the optimality of solutions of the max-product belief-propagation algorithm in arbitrary graphs, IEEE Transactions on Information Theory 47(2), 2001, pages 736 to 744"
    locator: fixed points of max-product on graphs with cycles are optimal in a large neighbourhood of assignments
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 13 (MAP inference): max-product variable elimination, max-product in clique trees, and decoding with ties"
---

The max-product algorithm finds a most probable assignment of a model whose [factor graph](/factor-graph/) is a tree. This is [MAP inference](/map-inference/). It is [belief propagation](/belief-propagation/) with each sum replaced by a maximum. A factor sends to a neighbour, for each value of the shared variable, the largest value of its table times the incoming messages. One pass from the leaves to a root gives the maximum probability. A *backtracking* pass from the root then picks the values: each factor picks its best row, given the value that its parent variable already has. In log space, the products become sums, and the algorithm is called max-sum, or min-sum for negative logs. On a chain it is the [Viterbi algorithm](/viterbi-algorithm/).

## In plain words

Belief propagation adds up all the ways a variable can take a value. Max-product keeps only the best way. Each message says: if my neighbour takes this value, the best my side of the tree can do is this much.

When the messages reach the root, the root knows the best total score for each of its values, and it picks the best one. Then it tells its neighbours its choice. Each of them picks the best values that fit that choice, and passes its own choices on, down to the leaves.

The backtracking matters when there are ties. If each variable picked its own best value alone, two tied choices could come from two different best answers that do not fit together.

## The problem

**Input.** Discrete variables $X_1, \ldots, X_n$, factors $f$ with nonnegative tables, and evidence $e$. The factor graph must be a tree or a forest.

**Output.** An assignment $x^*$ that agrees with $e$ and maximizes $\tilde p(x) = \prod_f f(x_f)$, the maximum $M = \tilde p(x^*)$, and, after a second pass, the max-marginals $\max \{\tilde p(x) : X_i = v\}$ for each variable and value. For a [Bayesian network](/bayesian-network/), $x^*$ is the most probable explanation of $e$, $M = P(x^*)$, and $P(x^* \mid e) = M / P(e)$.

## The algorithm

Let $\lambda_x$ be the evidence indicator of $x$: 1 on the observed value and 0 elsewhere, or 1 everywhere if $x$ is not observed.

```pseudo id=main
MAX-PRODUCT(factor tree, e)
L1  pick a variable r as root; list the nodes in breadth-first order from it
L2  for each node u except r, in reverse order, send to parent(u) ▷ a variable x sends λ_x(x) · Π μ_{g→x}(x) over its child factors g
L3      a factor f sends μ_{f→w}(x_w) ← max over the other variables of f of f(x_f) · Π over y in N(f) \ {w} of μ_{y→f}(x_y)
L4  b(x) ← λ_r(x) · Π over f in N(r) of μ_{f→r}(x); x*_r ← a maximizer of b; M ← b(x*_r)
L5  for each factor f, in breadth-first order, with parent variable p do
L6      a ← a row of f with a_p = x*_p that maximizes f(a) · Π over child variables y of μ_{y→f}(a_y)
L7      x*_y ← a_y for each child variable y of f
L8  return x*, M
```

Line L2 is the collect pass of belief propagation with line L3 in place of the sum. Lines L5 to L7 are the backtracking: they store no pointers, but look again at the table of each factor with the value of its parent fixed. Storing, at line L3, the row that reached each maximum gives the same result with more memory.

A distribute pass, as in belief propagation, gives the max-marginals at every variable. It is not needed for $x^*$.

**Max-sum.** With $\theta_f = \log f$ and $\log 0 = -\infty$, replace each product by a sum. Line L3 becomes $\max_{x_f \setminus x_w} \big(\theta_f(x_f) + \sum_y \nu_{y \to f}(x_y)\big)$. Sums of logs do not underflow, so this is the form used in practice. Min-sum uses $-\log f$, as costs or energies, and minimum in place of maximum.

## Example

Take a chain $A - B - C$ of binary variables, with a factor $\phi(A) = (1, 2)$ and two pairwise factors
$$\psi_1(A, B) = \begin{pmatrix} 3 & 1 \\ 1 & 2 \end{pmatrix}, \qquad \psi_2(B, C) = \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix},$$
where the row is the first variable. The root is $A$.

| message | value at 0 | value at 1 |
|---|---|---|
| $\mu_{C \to \psi_2}$ | 1 | 1 |
| $\mu_{\psi_2 \to B}(b) = \max_c \psi_2(b, c)$ | 2 | 3 |
| $\mu_{B \to \psi_1}$ | 2 | 3 |
| $\mu_{\psi_1 \to A}(a) = \max_b \psi_1(a, b)\, \mu_{B \to \psi_1}(b)$ | $\max(6, 3) = 6$ | $\max(2, 6) = 6$ |
| $\mu_{\phi \to A}$ | 1 | 2 |

At the root, $b(A) = (6, 12)$, so $x^*_A = 1$ and $M = 12$. Backtracking: $\psi_1$ with $A = 1$ has the scores $1 \cdot 2 = 2$ for $B = 0$ and $2 \cdot 3 = 6$ for $B = 1$, so $x^*_B = 1$. Then $\psi_2$ with $B = 1$ has the scores 1 and 3, so $x^*_C = 1$. The result is $(1, 1, 1)$ with $\phi(1)\, \psi_1(1, 1)\, \psi_2(1, 1) = 2 \cdot 2 \cdot 3 = 12$. The next best assignment, $(0, 0, 0)$, has $1 \cdot 3 \cdot 2 = 6$. The collect pass sent 5 messages, one per edge of the factor graph.

**Ties.** For one factor $f(x, y) = [x \ne y]$ on two binary variables, both max-marginals are $(1, 1)$. Choosing each variable alone, with the smaller value on ties, gives $(0, 0)$, which has value 0. Backtracking fixes $x = 0$ first and then picks $y = 1$, a correct answer.

## Correctness

For nonnegative numbers, the product distributes over the maximum: $a \cdot \max(b, c) = \max(ab, ac)$. So the proof of belief propagation goes through with max in place of the sum: the message from $u$ to its parent is the maximum of the product of the factors on the side of $u$, with the variable of the edge fixed. At the root, $\max b = M$.

For the backtracking, show from the leaves up that the product on the side of each node, at $x^*$, equals the message that node sent, at the value $x^*$ gives to the variable of the edge. A factor picks the row that reaches its message for the value of its parent, and its children reach their messages by induction. At the root this gives $\tilde p(x^*) = b(x^*_r) = M$. The argument holds for any choice among tied rows, because each choice is made with the parent fixed. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

The costs are in the [real RAM](/real-ram/) model, worst case, and are the same as for belief propagation. The collect pass sends $N$ messages, where $N = \sum_f |\mathrm{scope}(f)|$ is the number of edges. A factor message costs $O(k d^k)$ and a variable message $O(D d)$, so the pass costs $O(N(k d^k + D d))$. The backtracking reads each factor table once more, $O(\sum_f k d^k)$, and the optional distribute pass costs as much as the collect pass. Space is $O(N d)$ for the messages; storing argmax pointers adds $O(N d)$.

For a chain of $n$ variables with $d$ states and pairwise factors, the cost is $O(n d^2)$, the cost of the Viterbi algorithm.

## Properties

- **Exact on trees.** It returns an assignment of maximum value, for any choice among ties.
- **Semiring change.** Only the rule that the product distributes over the maximum is used. The pair (max, product) on nonnegative numbers, (max, +) on logs, and (min, +) on costs are all semirings, and the algorithm is the same in each. See [message passing](/message-passing/).
- **Max-marginals.** After both passes, each variable holds its max-marginal. Without ties, the maximizer of each max-marginal gives the MAP assignment directly.
- **Not the most probable value of each variable.** The MAP assignment can differ from the assignment that picks the most probable value of each variable from its marginal. They answer different questions.

## Variants and improvements

- **Viterbi.** On a chain, as in a [hidden Markov model](/hidden-markov-model/), max-product is the [Viterbi algorithm](/viterbi-algorithm/), with backpointers in place of the second look at each table.
- **Max-product on a junction tree.** For graphs with cycles, the [junction tree algorithm](/junction-tree-algorithm/) with max in place of the sum gives an exact MAP assignment, at a cost exponential in the width. Variable elimination with max does the same for one query.
- **Loopy max-product.** On a graph with cycles, the updates can be run until they stop changing. Weiss and Freeman (2001) showed that a fixed point is optimal among all assignments that differ from it on a set of variables whose subgraph is a tree or has at most one cycle per component. It need not be the global optimum, and it need not converge. [Affinity propagation](/affinity-propagation/) is an application of loopy max-sum.
- **The k best assignments.** Keeping the $k$ best values at each step, in place of the best only, gives the $k$ most probable assignments on a tree.
- **Marginal MAP.** Maximizing over some variables while summing over the others mixes the two operations, and they do not commute. Marginal MAP is harder; see [MAP inference](/map-inference/).

## When to use it

Use max-product when the factor graph is a tree and you need one most probable assignment: decoding a chain or a tree-shaped model, the best parse in a tree-structured model, or the most likely state sequence. Use max-sum in floating point. For models with cycles, use the junction tree algorithm when the width is small, or loopy max-product, linear programming relaxations, or local search as approximations.

## Pitfalls

- **Decoding each variable alone.** With ties, the maximizers of the max-marginals can be inconsistent, as in the example. Use backtracking.
- **Mixing max and sum.** Summing out a variable and maximizing over another in the wrong order computes a different quantity. Max and sum do not commute.
- **Underflow.** Products of many probabilities underflow to 0 in floating point, and then all values tie. Use max-sum.
- **Comparing floating point ties.** In log space, two equal products can get slightly different sums. This does not break optimality, but it can change which of the tied answers is returned.
- **Forgetting the evidence.** Fix the observed variables by the indicator $\lambda_x$, or the answer can disagree with the evidence.

## Implementations

## History

The Viterbi algorithm (1967) is the chain case, and dynamic programming on trees is older. Pearl (1988) gave belief revision, the computation of the most probable explanation of the evidence by local messages with maxima on trees and polytrees, as the companion of belief propagation. Kschischang, Frey and Loeliger (2001) and Aji and McEliece (2000) described max-product and min-sum as the sum-product algorithm over a different semiring. Weiss and Freeman (2001) studied the fixed points of max-product on graphs with cycles.

## References
