---
tag: 6W3JT5
kind: technique
slug: message-passing
name: Message passing
aliases:
- local message passing
- generalized distributive law
area: machine-learning/probabilistic-inference
level: core
summary: "Compute a global sum of products by local messages on a graph. On a tree, each edge carries one message each way, and the operations can be any commutative semiring."
prereqs: [factor-graph, graphical-model]
see_also: [belief-propagation, max-product, junction-tree-algorithm, loopy-belief-propagation, variable-elimination, forward-backward-algorithm, floyd-warshall, kleene-algebra]
sources:
  - paper: doi:10.1109/18.825794
    title: "Srinivas M. Aji and Robert J. McEliece, The generalized distributive law, IEEE Transactions on Information Theory 46(2), 2000, pages 325 to 343"
    locator: the marginalize a product function problem over a commutative semiring, solved by messages on a junction tree
  - paper: doi:10.1109/18.910572
    title: "Frank R. Kschischang, Brendan J. Frey and Hans-Andrea Loeliger, Factor graphs and the sum-product algorithm, IEEE Transactions on Information Theory 47(2), 2001, pages 498 to 519"
    locator: the sum-product algorithm on factor graphs, its schedules, and the change of semiring
  - book: isbn:9781558604797
    title: Judea Pearl, Probabilistic Reasoning in Intelligent Systems, Morgan Kaufmann, 1988
    locator: "Chapter 4, local message passing in trees and polytrees"
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 10 (message passing in clique trees) and Chapter 11 (message passing on graphs with cycles, and schedules)"
---

Message passing is a technique for computing a global quantity of a model, such as a marginal, a normalizing constant or a best assignment, by local computation. Each node of a graph keeps a part of the model, and each node sends to each neighbour a *message*: a small table that sums up what its side of the graph knows about the variables they share. A message is computed from the node's own table and the messages from its other neighbours. On a tree, two passes give exact results, with one message per edge in each direction. The only property used is that one operation distributes over the other, so the same template works in any commutative semiring: sum and product give [belief propagation](/belief-propagation/), max and product give [max-product](/max-product/), and min and plus give shortest paths. Aji and McEliece (2000) called this the *generalized distributive law*.

## In plain words

A big sum of products has an exponential number of terms. But if each factor touches only a few variables, many terms share parts, and you can add up the parts first. Message passing does this in an order given by a graph.

Each node does a small job. It waits until all but one of its neighbours have sent it a note, then it combines its own table with those notes and sends a short note to the last neighbour. When the graph is a tree, no note ever comes back to where it started, so nothing is counted twice.

The same plan works for adding, for taking the best, and for other pairs of operations, as long as the multiplication spreads over the addition, as in $a(b + c) = ab + ac$.

## When it applies

Use it when:

- the quantity is a "sum" of a "product" of local functions, $\bigoplus_{x \setminus x_Q} \bigotimes_f f(x_f)$, where each function has a small scope;
- $(\oplus, \otimes)$ is a commutative semiring: both operations are associative and commutative, and $\otimes$ distributes over $\oplus$;
- the functions can be arranged on a tree whose nodes hold sets of variables, with the running intersection property: a [factor graph](/factor-graph/) that is a tree, or a [junction tree](/junction-tree/) of the cliques.

If the graph has cycles, the technique still runs (loopy message passing), but it is not exact in general. If it needs division, as in the Hugin form, the semiring must allow it.

## The template

Let $T$ be a tree whose node $i$ holds a set of variables $C_i$ and a local function $\psi_i$, the $\otimes$-product of the functions assigned to it. For an edge $\{i, j\}$ let $S_{ij} = C_i \cap C_j$.

```pseudo id=main
MESSAGE-PASSING(T, ψ, ⊕, ⊗)
L1  pick a root; order the nodes breadth-first from it
L2  for each node i except the root, in reverse order: SEND(i, parent(i))   ▷ collect
L3  for each node i except the root, in order: SEND(parent(i), i)           ▷ distribute
L4  for each node i: β_i ← ψ_i ⊗ (⊗ over k in N(i) of m_{k→i})
L5  return β

SEND(i, j)
L6  m_{i→j} ← ⊕ over the variables of C_i \ S_ij of ( ψ_i ⊗ (⊗ over k in N(i) \ {j} of m_{k→i}) )
```

After the two passes, $\beta_i(x_{C_i}) = \bigoplus_{x \setminus x_{C_i}} \bigotimes_f f(x_f)$ for every node: the "marginal" of the whole product on $C_i$, in the semiring. The proof is the one of [belief propagation](/belief-propagation/), with $(\oplus, \otimes)$ in place of $(+, \times)$: by the running intersection property, the variables on the two sides of an edge meet only in the separator, so the $\oplus$ over one side can be done before the $\otimes$ with the other side.

**Schedules.** A node may send to $j$ as soon as it has received from all its other neighbours. On a tree, any order with this rule gives the same messages. Common orders:

- *two passes* to a root and back, as above: $2(|V| - 1)$ messages, the fewest possible for all marginals;
- *flooding*: every node sends to every neighbour at each round, from the messages of the round before. On a tree it reaches the exact messages after as many rounds as the diameter, and it is easy to run in parallel;
- *one pass* to a root: enough for a single marginal, or for a maximum followed by backtracking.

**Semirings.** Some pairs and what the template computes with them:

| $\oplus$ | $\otimes$ | values | result | page |
|---|---|---|---|---|
| $+$ | $\times$ | nonnegative reals | marginals and the partition function | [belief propagation](/belief-propagation/) |
| max | $\times$ | nonnegative reals | max-marginals, most probable assignment | [max-product](/max-product/) |
| max | $+$ | reals and $-\infty$ | the same in log space | [max-product](/max-product/) |
| min | $+$ | reals and $+\infty$ | least cost, shortest paths | [min-plus product](/min-plus-matrix-multiplication/) |
| or | and | true, false | whether a solution exists | [constraint satisfaction](/bucket-elimination/) |
| $+$ | $\times$ | integers | the number of solutions | [model counting](/model-counting/) |

## Classic examples

- **[Belief propagation](/belief-propagation/)** on a factor tree: the sum-product semiring, two passes, all marginals.
- **[Max-product](/max-product/)** and max-sum: the max semiring, one pass and backtracking for a MAP assignment.
- **[Junction tree algorithm](/junction-tree-algorithm/)**: the template on a tree of cliques of a triangulated graph, for any model, at a cost exponential in the width.
- **[Forward-backward algorithm](/forward-backward-algorithm/)** and the **[Viterbi algorithm](/viterbi-algorithm/)**: the template on a chain, with the sum and with the maximum. The [BCJR algorithm](/bcjr-algorithm/) is the forward-backward algorithm on the trellis of a code.
- **[Variable elimination](/variable-elimination/)** and **[bucket elimination](/bucket-elimination/)**: one collect pass, where each intermediate factor is a message.
- **Fast transforms.** Aji and McEliece showed that the fast Fourier transform on a finite abelian group also fits the template, with a suitable junction tree.

## Variations

- **Hugin form.** Keep a table on each edge and divide by it in the distribute pass, in place of the product over all but one neighbour. It needs division.
- **Loopy message passing.** On a graph with cycles, run the same updates in rounds until they stop changing. This is [loopy belief propagation](/loopy-belief-propagation/); it can fail to converge, and its fixed points are approximations. Schedules matter more here: sequential and residual schedules, which send the message that changed most, often converge where flooding does not.
- **Region graphs.** [Generalized belief propagation](/generalized-belief-propagation/) passes messages between sets of variables on a graph that need not be a tree.
- **Continuous variables.** For Gaussian models the messages are Gaussian and carry a mean and a precision: [Gaussian belief propagation](/gaussian-belief-propagation/). In general, messages can be approximated by samples or by members of a fixed family.
- **Normalized messages.** In the sum-product semiring, scaling a message by a constant changes no marginal. Normalizing each message avoids underflow.

## Pitfalls

- **Not a semiring.** The operations must distribute. Mixing max and sum in one pass, as in marginal MAP, breaks the template: max and sum do not commute.
- **Counting twice.** A message to $j$ must leave out what came from $j$. On a graph with cycles this rule is not enough, and evidence can come back to its source.
- **No running intersection property.** Putting cliques on an arbitrary tree, or skipping triangulation, gives wrong results without any error.
- **Underflow and overflow.** Products of many numbers leave the range of floating point. Use logs (max-sum, log-sum-exp) or normalize.
- **Assuming exactness on cycles.** The template is exact only on trees.

## Exercises

1. On a path of $n$ nodes, count the messages of the two-pass schedule and of flooding until all messages are final.
2. Show that on a tree, any schedule in which a node sends to $j$ only after it has received from all its other neighbours gives the same messages as the two passes.
3. Use the (min, +) semiring on a chain whose factors are edge weights to compute the shortest path from the first to the last node, and compare with dynamic programming.
4. With the (or, and) semiring on a tree-shaped constraint network, show that the root message is true exactly when a solution exists, and find a solution by backtracking.
5. Find a three-node graph with a cycle on which two rounds of flooding with the sum-product semiring give a wrong marginal.

## References
