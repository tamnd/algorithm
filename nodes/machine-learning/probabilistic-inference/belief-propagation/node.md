---
tag: 5AZ02P
kind: algorithm
slug: belief-propagation
name: Belief propagation
aliases:
- sum-product algorithm
- Pearl's belief propagation
- sum-product message passing
area: machine-learning/probabilistic-inference
level: core
summary: "Exact marginals on a tree-shaped factor graph by sum-product messages: one pass to a root and one back, two messages per edge."
solves: [marginal-inference]
model: real-ram
complexity:
  vars: {N: the number of edges of the factor graph, d: the largest domain size, k: the largest scope size, D: the largest number of factors on one variable}
  time: {worst: "O(N (k d^k + D d))"}
  space: {extra: "O(N d)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1982
  people: [Judea Pearl]
  note: "Pearl gave local message passing for trees in 1982 and for polytrees in his 1988 book; Kschischang, Frey and Loeliger (2001) stated it on factor graphs."
prereqs: [factor-graph, marginal-inference, message-passing]
see_also: [loopy-belief-propagation, max-product, junction-tree-algorithm, variable-elimination, forward-backward-algorithm, belief-propagation-decoding, bcjr-algorithm, gaussian-belief-propagation]
sources:
  - paper: "Judea Pearl, Reverend Bayes on inference engines: a distributed hierarchical approach, Proceedings of the National Conference on Artificial Intelligence (AAAI-82), 1982, pages 133 to 136"
    title: Pearl 1982
    locator: belief updating by messages between the nodes of a tree
  - book: isbn:9781558604797
    title: Judea Pearl, Probabilistic Reasoning in Intelligent Systems, Morgan Kaufmann, 1988
    locator: "Chapter 4, belief propagation in trees and in singly connected networks (polytrees)"
  - paper: doi:10.1109/18.910572
    title: "Frank R. Kschischang, Brendan J. Frey and Hans-Andrea Loeliger, Factor graphs and the sum-product algorithm, IEEE Transactions on Information Theory 47(2), 2001, pages 498 to 519"
    locator: the sum-product update rules on a factor graph and their exactness on trees
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Chapter 8, Section 8.4.4 (the sum-product algorithm)"
---

Belief propagation, also called the sum-product algorithm, computes the exact [marginals](/marginal-inference/) of a model whose [factor graph](/factor-graph/) is a tree. Each variable and each factor sends a *message* to each neighbour: a table over one variable that sums up its side of the tree. A factor sends the sum, over its other variables, of its table times the messages it got from them. A variable sends the product of the messages it got from its other factors. With a pass from the leaves to a root and a pass back, each edge carries two messages, and the product of the messages into a variable is its marginal. The same updates run on graphs with cycles are [loopy belief propagation](/loopy-belief-propagation/), which has no guarantee.

## In plain words

Think of a tree of people, where each person knows only a part of the facts. To find out what everyone knows together, each person sends a short note to each neighbour. The note sums up what that side of the tree knows.

A note is sent once a person has the notes from all the other neighbours. So the leaves start, the notes travel to a root, and then they travel back.

When a person has notes from all neighbours, they know how the whole tree sees them. In a model, this is the probability of each value of a variable, given all the evidence.

This works because a tree has one path between any two places, so no fact arrives twice.

## The problem

**Input.** Discrete variables $X_1, \ldots, X_n$, a set of factors $f$ with nonnegative tables over their scopes, and evidence $e$ (values for some variables). The factor graph, with an edge between each factor and each variable of its scope, must be a tree or a forest. A [Bayesian network](/bayesian-network/) whose graph has no cycle when the directions are ignored (a polytree) gives such a factor graph, with one factor $P(X \mid \mathrm{Pa}(X))$ per variable.

**Output.** $P(X_i \mid e)$ for each variable, the marginal of the scope of each factor, and $Z(e)$, the sum of the product of the factors over the assignments that agree with $e$. For a Bayesian network, $Z(e) = P(e)$.

## The algorithm

Let $\lambda_x$ be the evidence indicator of $x$: 1 on the observed value, 0 on the others, and 1 everywhere if $x$ is not observed.

```pseudo id=main
BELIEF-PROPAGATION(factor tree, e)
L1  pick a variable as root; list the nodes in breadth-first order from it
L2  for each node u except the root, in reverse order: SEND(u, parent(u))    ▷ collect
L3  for each node u except the root, in order: SEND(parent(u), u)            ▷ distribute
L4  for each variable x: b_x(x) ← λ_x(x) · Π over f in N(x) of μ_{f→x}(x)
L5  return b_x / Σ b_x for each x, and Z = Σ b_x

SEND(u, w)
L6  if u is a variable x: μ_{x→w}(x) ← λ_x(x) · Π over g in N(x) \ {w} of μ_{g→x}(x)
L7  else u is a factor f: μ_{f→w}(x_w) ← Σ over the other variables of f of f(x_f) · Π over y in N(f) \ {w} of μ_{y→f}(x_y)
```

Line L6 is the product step and line L7 the sum step, which gives the name. The order of lines L2 and L3 makes sure a node sends to a neighbour only after it has received from all its other neighbours. Any order with this rule gives the same messages; the two passes are one such order. On a forest, run the lines on each tree; $Z$ is the product over the trees.

The marginal of the scope of a factor is $f(x_f) \prod_{y \in f} \mu_{y \to f}(x_y)$, divided by $Z$.

## Example

Let $X_0$ and $X_1$ be binary with $P(X_0{=}1) = 1/4$, $P(X_1{=}1 \mid X_0{=}0) = 1/2$ and $P(X_1{=}1 \mid X_0{=}1) = 9/10$. The factor graph is $f_0 - X_0 - f_1 - X_1$, with $f_0 = P(X_0)$ and $f_1 = P(X_1 \mid X_0)$. The evidence is $X_1 = 1$, so $\lambda_{X_1} = (0, 1)$. The root is $X_0$, and the breadth-first order is $X_0, f_0, f_1, X_1$.

| pass | message | value at 0 | value at 1 |
|---|---|---|---|
| collect | $\mu_{X_1 \to f_1} = \lambda_{X_1}$ | 0 | 1 |
| collect | $\mu_{f_1 \to X_0}(x_0) = \sum_{x_1} P(x_1 \mid x_0)\, \mu_{X_1 \to f_1}(x_1)$ | 1/2 | 9/10 |
| collect | $\mu_{f_0 \to X_0} = P(X_0)$ | 3/4 | 1/4 |
| distribute | $\mu_{X_0 \to f_0} = \mu_{f_1 \to X_0}$ | 1/2 | 9/10 |
| distribute | $\mu_{X_0 \to f_1} = \mu_{f_0 \to X_0}$ | 3/4 | 1/4 |
| distribute | $\mu_{f_1 \to X_1}(x_1) = \sum_{x_0} P(x_1 \mid x_0)\, \mu_{X_0 \to f_1}(x_0)$ | 2/5 | 3/5 |

The factor graph has three edges and six messages. At $X_0$, $b(x_0) = (3/4 \cdot 1/2,\ 1/4 \cdot 9/10) = (3/8, 9/40)$, with sum $Z = 3/5 = P(X_1{=}1)$. So $P(X_0{=}1 \mid X_1{=}1) = (9/40)/(3/5) = 3/8$. At $X_1$, $b = (0 \cdot 2/5,\ 1 \cdot 3/5) = (0, 3/5)$, with the same sum $3/5$.

## Correctness

Remove an edge between $u$ and $w$. The tree falls into two parts. The message from $u$ to $w$ is the sum, over the variables on the side of $u$ other than the variable of the edge, of the product of the factors and indicators on that side. This holds by induction on the size of the side. The side of a variable is the variable with the sides of its other factors, and these share nothing else, so the sum splits into the product of line L6. The side of a factor is the factor with the sides of its other variables, each of which meets the scope in one variable only, which gives line L7. At a variable, the sides of all its factors cover the tree, so the product of line L4 is the sum of the whole product over all the other variables, the marginal times $Z$. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

The costs are in the [real RAM](/real-ram/) model, worst case. The factor graph has $N = \sum_f |\mathrm{scope}(f)|$ edges, and the algorithm sends $2N$ messages.

- A message from a factor with $k$ variables reads its table of up to $d^k$ entries and multiplies $k - 1$ messages into each, so it costs $O(k d^k)$. A factor sends $k$ messages, so the factors cost $O(N k d^k)$ in total.
- A message from a variable with $D$ factors multiplies $D - 1$ tables of size $d$, $O(D d)$, and it sends $D$ of them, so the variables cost $O(N D d)$ in total. Prefix and suffix products bring this to $O(N d)$.

Space is $O(N d)$ for the messages. For a pairwise model on a tree with $n$ variables, $N = 2(n - 1)$ plus the unary factors, and the cost is $O(n d^2)$, the same as one run of [variable elimination](/variable-elimination/) on the tree, but it gives all $n$ marginals.

## Properties

- **Exact on trees.** With exact arithmetic the result equals the sum over all joint assignments. The order of the messages does not matter, as long as each node waits for its other neighbours.
- **Two messages per edge.** No iteration and no convergence test is needed on a tree.
- **Local.** Each message uses only the table of one node and the messages into it, so the updates can run in parallel, one node per processor.
- **Generic in the operations.** Only the sum, the product and the rule that the product distributes over the sum are used. With the maximum in place of the sum it becomes [max-product](/max-product/); see [message passing](/message-passing/) for the general form.

## Variants and improvements

- **Pearl's form on polytrees.** Pearl's original algorithm works on the Bayesian network itself, with $\pi$ messages from parents to children and $\lambda$ messages from children to parents. On a polytree it computes the same marginals as the factor graph form.
- **Normalized messages.** Scaling each message so that it sums to 1 changes no marginal and avoids underflow; keep the logarithms of the scale factors to get $\log Z$. In log space, the sum of line L7 becomes a [log-sum-exp](/log-sum-exp-trick/).
- **Loopy belief propagation.** On a graph with cycles, the same updates can be run again and again until the messages stop changing. This is [loopy belief propagation](/loopy-belief-propagation/). It may not converge, and when it does, the results are approximations, related to the stationary points of the [Bethe free energy](/bethe-free-energy/).
- **Gaussian models.** For jointly Gaussian variables, the messages are Gaussian and are passed as means and precisions: [Gaussian belief propagation](/gaussian-belief-propagation/).
- **Junction trees.** For a graph with cycles, exact inference groups the variables into cliques and runs the same passes on a [junction tree](/junction-tree-algorithm/).
- **Chains and codes.** On a chain, the two passes are the [forward-backward algorithm](/forward-backward-algorithm/); on the trellis of a convolutional code they are the [BCJR algorithm](/bcjr-algorithm/). [Belief propagation decoding](/belief-propagation-decoding/) runs the loopy form on the graph of an LDPC code.

## When to use it

Use belief propagation when the factor graph is a tree, such as a chain, a tree-structured Markov random field or a polytree Bayesian network, and you need all the marginals. It is simple, exact and linear in the size of the tree. When the graph has cycles, use the [junction tree algorithm](/junction-tree-algorithm/) if the width is small, or loopy belief propagation as a fast approximation.

## Pitfalls

- **Running on a graph with cycles and trusting the result.** A message can return to its sender, and evidence is counted more than once. The two-pass schedule needs a tree; check this first.
- **Sending too early.** A message sent before all the other neighbours have sent is wrong, and the error spreads. Use the two passes, or count the messages each node has received.
- **Forgetting the evidence.** The evidence indicator must enter at the variable, in line L6 and in line L4. A factor that already fixes the value is another way.
- **Underflow.** On long chains the products of many small numbers become 0 in floating point. Normalize the messages.
- **A polytree is not a tree.** In a polytree, a node can have several parents. The factor graph is still a tree, but the moral graph is not, so pairwise belief propagation on the moral graph is not the right method.

## Implementations

## History

Pearl (1982) gave belief updating by messages between the nodes of a tree, as a model of distributed reasoning. His 1988 book extended it to singly connected networks (polytrees). Gallager's decoding of low-density parity-check codes (1962) used the same kind of updates, and later work showed that it, the forward-backward algorithm, the Viterbi algorithm and turbo decoding are all cases of one algorithm. Kschischang, Frey and Loeliger (2001) stated this algorithm on factor graphs, under the name sum-product algorithm. Aji and McEliece (2000) gave the same unification as the generalized distributive law.

## References
