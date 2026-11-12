---
tag: ZJC1JG
kind: algorithm
slug: variable-elimination
name: Variable elimination
aliases:
- VE
- sum-product variable elimination
area: machine-learning/probabilistic-inference
level: core
summary: "Exact inference: multiply the factors that hold a variable, sum the variable out, repeat. Time O(n d^(w+1)) for an order of induced width w."
solves: [marginal-inference]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of factors, d: the largest domain size, w: the induced width of the order}
  time: {worst: "O((n + m) d^(w+1))"}
  space: {extra: "O((n + m) d^w + d^(w+1))"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1994
  people: [Nevin L. Zhang, David Poole, Rina Dechter]
  note: Zhang and Poole described variable elimination for Bayesian networks in 1994. Dechter gave the same scheme as bucket elimination in 1996, for probabilistic queries and for optimization.
prereqs: [marginal-inference, bayesian-network, markov-random-field]
see_also: [elimination-ordering, bucket-elimination, junction-tree-algorithm, belief-propagation, max-product, partition-function-computation, treewidth, fill-in]
sources:
  - paper: "Nevin L. Zhang and David Poole, A simple approach to Bayesian network computations, Proceedings of the Tenth Canadian Conference on Artificial Intelligence, 1994, pages 171 to 178"
    title: Zhang and Poole 1994
    locator: the variable elimination algorithm for posterior probabilities in Bayesian networks
  - paper: "Rina Dechter, Bucket elimination: a unifying framework for probabilistic inference, Proceedings of the Twelfth Conference on Uncertainty in Artificial Intelligence (UAI 1996), pages 211 to 219"
    title: Dechter 1996
    locator: the bucket elimination algorithms for belief updating, MPE and MAP, and the bound exponential in the induced width
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 9, Sections 9.2 to 9.4 (the algorithm, evidence, and the complexity in terms of the induced graph)"
  - book: isbn:9780521884389
    title: Adnan Darwiche, Modeling and Reasoning with Bayesian Networks, Cambridge University Press, 2009
    locator: Chapter 6 (inference by variable elimination, elimination orders and their width)
---

Variable elimination (VE) is an exact algorithm for [marginal inference](/marginal-inference/) in a [Bayesian network](/bayesian-network/) or a [Markov random field](/markov-random-field/). It takes the variables that are not asked for one at a time, multiplies the factors that mention the variable, and sums the variable out of that product. The cost depends on the order: with $n$ variables, domains of size at most $d$ and an order of [induced width](/elimination-ordering/) $w$, it does $O(n d^{w+1})$ arithmetic operations on a Bayesian network. The minimum $w$ over all orders is the [treewidth](/treewidth/) of the graph, so VE is fast on graphs that are close to trees and exponential on graphs that are not.

## In plain words

A probability model is a product of many small tables. To get the chance of one variable, you must add up the product over all values of all the other variables. Done directly, that sum has one term for each full assignment, which is far too many.

Variable elimination adds up one variable at a time. To remove a variable, it collects only the tables that mention that variable, multiplies them, and adds over the values of the variable. The result is a new table that no longer mentions it. The other tables do not change, because they do not depend on that variable.

When all the other variables are gone, the tables that are left mention only the variable you asked about. You multiply them and scale the result so that it adds up to one.

## The problem

In this page $n$ is the number of variables, not the number of training examples, and $d$ is the largest domain size, not the input dimension. The model is a set $\Phi$ of $m$ nonnegative factors $\phi(X_\phi)$ over discrete variables $X_1, \ldots, X_n$, with
$$P(x) = \frac{1}{Z} \prod_{\phi \in \Phi} \phi(x_\phi).$$
For a Bayesian network the factors are the [conditional probability tables](/conditional-probability-table/) and $Z = 1$. The query is a set $Q$ of variables and evidence $E = e$. The output is the table $P(Q \mid E = e)$. This is the [marginal inference](/marginal-inference/) problem.

## The algorithm

The input also holds an order $\pi$ of the variables that are neither in $Q$ nor in $E$. Here $\phi[E = e]$ is the factor $\phi$ with the evidence variables fixed to their observed values (the rows that disagree with $e$ are dropped).

```pseudo id=main
VARIABLE-ELIMINATION(Φ, Q, e, π)
L1  Φ ← { φ[E = e] : φ ∈ Φ }                  ▷ reduce each factor by the evidence
L2  for each variable z in the order π do
L3      Ψ ← the factors of Φ whose scope holds z
L4      ψ ← ∏_{φ ∈ Ψ} φ                         ▷ a table over z and its neighbours
L5      τ ← Σ_z ψ                               ▷ sum z out
L6      Φ ← (Φ \ Ψ) ∪ {τ}
L7  φ* ← ∏_{φ ∈ Φ} φ                             ▷ a table over Q only
L8  return φ*(q) / Σ_{q'} φ*(q') for each q
```

Line L4 is the only expensive step. The product $\psi$ is a table over $z$ and every variable that shares a factor with $z$ at that time. Line L5 makes a table $\tau$ over these neighbours, and line L6 puts it back in place of the factors it came from. This $\tau$ links all the neighbours of $z$ to each other. In graph terms, eliminating $z$ adds *fill* edges between its neighbours and deletes $z$, the same step as in sparse [Gaussian elimination](/fill-in/). Line L8 divides by $\sum_{q'} \phi^*(q') = \tilde P(e)$, the unnormalized probability of the evidence. For a Bayesian network this is $P(e)$, so VE also gives the [probability of the evidence](/partition-function-computation/) for free.

## Example

The sprinkler network has four binary variables: cloudy $C$, sprinkler $S$, rain $R$ and wet grass $W$, with the edges $C \to S$, $C \to R$, $S \to W$, $R \to W$. Its tables are $P(C{=}1) = 0.5$; $P(S{=}1 \mid C{=}0) = 0.5$, $P(S{=}1 \mid C{=}1) = 0.1$; $P(R{=}1 \mid C{=}0) = 0.2$, $P(R{=}1 \mid C{=}1) = 0.8$; and $P(W{=}1 \mid S, R) = 0, 0.9, 0.9, 0.99$ for $(S, R) = 00, 01, 10, 11$.

The query is $P(R \mid W{=}1)$ with the order $\pi = (C, S)$.

| step | factors used | new factor | its values |
|---|---|---|---|
| L1 | $P(W \mid S, R)$ | $f(S, R) = P(W{=}1 \mid S, R)$ | $f(0,0) = 0$, $f(0,1) = 0.9$, $f(1,0) = 0.9$, $f(1,1) = 0.99$ |
| eliminate $C$ | $P(C)$, $P(S \mid C)$, $P(R \mid C)$ | $\tau_1(S, R) = \sum_c P(c) P(S \mid c) P(R \mid c)$ | $\tau_1(0,0) = 0.29$, $\tau_1(0,1) = 0.41$, $\tau_1(1,0) = 0.21$, $\tau_1(1,1) = 0.09$ |
| eliminate $S$ | $\tau_1(S, R)$, $f(S, R)$ | $\tau_2(R) = \sum_s \tau_1(s, R) f(s, R)$ | $\tau_2(0) = 0.189$, $\tau_2(1) = 0.4581$ |
| L8 | $\tau_2(R)$ | $P(R \mid W{=}1)$ | $0.189/0.6471 = 210/719$, $0.4581/0.6471 = 509/719$ |

So $P(R{=}1 \mid W{=}1) = 509/719 \approx 0.7079$, and $P(W{=}1) = 0.6471$. The same run with the query $S$ gives $P(S{=}1 \mid W{=}1) = 309/719 \approx 0.4298$. If we also observe $R = 1$, then $P(S{=}1 \mid W{=}1, R{=}1) = 99/509 \approx 0.1945$: the rain *explains away* the wet grass, and the belief in the sprinkler drops.

The largest product here has three variables ($C$, $S$, $R$ in the first step), so this order has induced width 2.

## Correctness

The invariant of the loop of line L2 is: the product of the factors in $\Phi$ equals the sum of the full unnormalized product over the variables already eliminated, with the evidence fixed. It holds at the start because of line L1. One step keeps it by the distributive law: the factors outside $\Psi$ do not depend on $z$, so they move out of the sum over $z$, and
$$\sum_z \prod_{\phi \in \Phi} \phi = \prod_{\phi \notin \Psi} \phi \cdot \sum_z \prod_{\psi \in \Psi} \psi.$$
At the end, the product is $\tilde P(Q, e)$, and line L8 turns it into $P(Q \mid e)$. A second induction shows that the scope of each factor is a clique of the current elimination graph, which bounds the size of each product by $w + 1$. Both proofs are in [the full proof](proofs/correctness.md).

## Complexity

The costs are arithmetic operations in the [real RAM](/real-ram/) model, in the worst case, for a fixed order of induced width $w$ on the interaction graph of the factors (the [moral graph](/bayesian-network/) for a Bayesian network).

- **Time.** The product of line L4 has at most $d^{w+1}$ entries, and each factor in $\Psi$ costs one multiplication per entry. Each factor, original or created, is used in exactly one step, and there are at most $m + n$ of them. So the loop costs $O((n + m) d^{w+1})$. For a Bayesian network $m = n$, which gives $O(n d^{w+1})$. A simple implementation also spends $O(w)$ time per entry on index arithmetic.
- **Space.** Each $\tau$ has at most $d^{w}$ entries and the current product at most $d^{w+1}$, so the extra space is $O((n + m) d^w + d^{w+1})$.
- **The final table.** Line L7 builds a table over $Q$, of size $d^{|Q|}$. For a single query variable this is $d$.
- **The order matters.** On a star with $k$ leaves, eliminating the centre first makes a product over all $k + 1$ variables, while eliminating the leaves first never makes a product over more than 2. Finding an order of minimum width is NP-hard; see [elimination ordering](/elimination-ordering/).
- **Lower bound.** No method is polynomial in general: [marginal inference](/marginal-inference/) is #P-hard, and its decision form is NP-hard by [Cooper's theorem](/cooper-theorem/).

## Properties

- **Exact.** With exact arithmetic (fractions), the result is exactly $P(Q \mid e)$.
- **One query at a time.** A run answers one query. To get the marginal of each of the $n$ variables, a naive use repeats the work $n$ times. The [junction tree algorithm](/junction-tree-algorithm/) and [belief propagation](/belief-propagation/) on a tree reuse the shared sums and give all marginals for about twice the cost of one.
- **Any commutative semiring.** The proof uses only the distributive law. With max in place of sum, the same loop computes the value of the most probable assignment ([MAP inference](/map-inference/)); with sum and no evidence, it computes the [partition function](/partition-function/).

## Variants and improvements

- **Bucket elimination.** Dechter's form puts each factor in the bucket of its first variable in the order, and processes the buckets in turn. It is the same computation, with a fixed place for each factor. The constraint form is [bucket elimination](/bucket-elimination/) for constraint networks.
- **Max-product and MPE.** Replace the sum of line L5 by a max and record the maximizing value of each $z$. A backward pass over the order then gives a most probable assignment. On a tree this is [max-product](/max-product/).
- **Marginal MAP.** Sum out the variables outside the MAP set first, then maximize the rest. The order is constrained, so the width can be much larger than the treewidth.
- **Pruning.** Before the run, delete each variable that is not an ancestor of $Q \cup E$ in a Bayesian network (a barren node). Its table sums to 1 and contributes nothing.
- **Logarithms and scaling.** On large tables, products of many small numbers underflow. Keep each factor scaled, or work with logs and the [log-sum-exp trick](/log-sum-exp-trick/).

## When to use it

Use VE when you need one marginal, or the probability of the evidence, on a model of small treewidth. It is short to write and easy to check. When you need the marginals of many variables, or the same model with many evidence sets, build a [junction tree](/junction-tree/) once and run the [junction tree algorithm](/junction-tree-algorithm/). When the treewidth is large, no exact method is practical; use [loopy belief propagation](/loopy-belief-propagation/), [variational inference](/variational-inference/) or [Gibbs sampling](/gibbs-sampling/).

## Pitfalls

- **A bad order.** The cost is exponential in the width of the order, not of the graph. Do not eliminate a variable of high degree early. Use the min-fill or min-degree heuristic of [elimination ordering](/elimination-ordering/).
- **Evidence left in the factors.** If line L1 is skipped and the evidence variables are summed out in the loop, the result is the prior $P(Q)$, not the posterior.
- **Forgetting to normalize.** For a Markov random field, or with evidence, the table of line L7 is not a distribution. Line L8 is needed, and it fails when the evidence has probability zero; check for this case.
- **Summing out a query variable.** The order must not hold a query variable. Then the table of line L7 has no variable left.
- **Underflow.** With floats and many factors, the entries can become 0. Rescale each $\tau$ or use logs.

## Implementations

## History

Zhang and Poole (1994) presented variable elimination as a simple way to compute posteriors in Bayesian networks, with the elimination of variables one by one in a chosen order. Dechter (1996) gave the same scheme as bucket elimination and showed one algorithm for belief updating, MPE and MAP, with a cost exponential in the induced width. The graph side of the method is the same as the vertex elimination of sparse Gaussian elimination, where the fill edges and the order play the same role.

## References
