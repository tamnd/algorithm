---
tag: 638X2J
kind: algorithm
slug: tree-reweighted-belief-propagation
name: Tree-reweighted belief propagation
aliases:
- TRW
- TRW-S
- tree-reweighted sum-product
- TRW-BP
area: machine-learning/probabilistic-inference
level: research
summary: "Message passing with edge weights from a distribution over spanning trees. It maximizes a concave function on the local polytope whose maximum is an upper bound on log Z."
solves: [marginal-inference]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of edges, k: the largest number of states of a variable, d: the largest degree, t: the number of iterations}
  time: {worst: "O(n^3 + t m k (k + d))"}
  space: {extra: "O(n^2 + m k^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2005
  people: [Martin J. Wainwright, Tommi S. Jaakkola, Alan S. Willsky]
  note: "Wainwright, Jaakkola and Willsky wrote log Z of a graph with cycles as bounded by a convex combination of tree-structured problems, and derived the tree-reweighted sum-product messages that compute the best such bound. A max-product version for MAP followed, and Kolmogorov (2006) made it convergent as TRW-S."
prereqs: [loopy-belief-propagation, bethe-free-energy, spanning-tree]
see_also: [matrix-tree-theorem, uniform-spanning-tree-sampling, generalized-belief-propagation, mean-field-approximation, max-product, map-inference, convex-function, ising-model]
sources:
  - paper: "Martin J. Wainwright, Tommi S. Jaakkola and Alan S. Willsky, A new class of upper bounds on the log partition function, IEEE Transactions on Information Theory 51(7), 2005"
    title: Wainwright, Jaakkola and Willsky 2005
    locator: "the convex combination of tree-structured parameters, the edge appearance probabilities, the tree-reweighted entropy and its variational upper bound, and the tree-reweighted message updates"
  - paper: doi:10.1561/2200000001
    title: "Martin J. Wainwright and Michael I. Jordan, Graphical models, exponential families, and variational inference, Foundations and Trends in Machine Learning 1(1-2), 2008"
    locator: "Chapter 7 (convex relaxations and upper bounds, including the tree-reweighted Bethe problem and its message-passing algorithm)"
  - paper: "Martin J. Wainwright, Tommi S. Jaakkola and Alan S. Willsky, MAP estimation via agreement on trees: message-passing and linear programming, IEEE Transactions on Information Theory 51(11), 2005"
    title: Wainwright, Jaakkola and Willsky 2005 (MAP)
    locator: "tree-reweighted max-product and its link to the linear programming relaxation"
  - paper: "Vladimir Kolmogorov, Convergent tree-reweighted message passing for energy minimization, IEEE Transactions on Pattern Analysis and Machine Intelligence 28(10), 2006"
    title: Kolmogorov 2006
    locator: "TRW-S, a sequential schedule of tree-reweighted max-product under which a lower bound on the energy never decreases"
---

Tree-reweighted belief propagation (TRW) is a change to [loopy belief propagation](/loopy-belief-propagation/) that makes its objective concave and its result an upper bound on the log partition function $\log Z$. Each edge gets a weight $\rho_{st}$, the probability that it lies in a spanning tree drawn from a fixed distribution over the spanning trees of the graph. The messages are sum-product messages with these weights put in at three places. At a fixed point, the pseudomarginals maximize a concave function on the local polytope, and the maximum value is at least $\log Z$. With $\rho = 1$ on every edge, which is the only choice on a tree, TRW is ordinary BP, and on a tree it is exact. It was introduced by Wainwright, Jaakkola and Willsky.

## In plain words

On a graph with loops, loopy belief propagation can give answers that are too sure, it can settle at different answers from different starts, and its estimate of the total weight of all states can be too high or too low.

A tree has no such problems. TRW looks at the graph as a mix of all its spanning trees. Each edge counts in proportion to how often it appears in a random spanning tree. Edges that most trees use count almost fully, and edges that few trees use count less. The messages are those of belief propagation with these counts put in. The problem it solves has no false local answers, and its estimate of the total weight is never too low: it is a guaranteed upper bound. On a tree, every edge is in the only spanning tree, and TRW is exactly belief propagation.

## The problem

**The model.** A pairwise [Markov random field](/markov-random-field/) on a connected graph $G = (V, E)$:

$$p(x) = \frac{1}{Z} \exp\Big(\sum_{s \in V} \theta_s(x_s) + \sum_{(s,t) \in E} \theta_{st}(x_s, x_t)\Big).$$

The queries are an upper bound on $\log Z$ and approximate marginals.

**The variational principle.** For the vector $\mu$ of true single and pairwise marginals, $\log Z = \langle \theta, \mu \rangle + H(p)$, where $\langle \theta, \mu \rangle$ is the expected value of the exponent. Loopy BP replaces the entropy by the Bethe entropy, which is neither a bound nor concave in general.

**The tree-reweighted entropy.** Let $\rho(T)$ be a probability distribution over the spanning trees of $G$, and let $\rho_{st}$ be the probability that the edge $(s,t)$ is in the tree. For a tree, the entropy of the tree-structured distribution with given marginals is $H_T = \sum_s H(\tau_s) - \sum_{(s,t) \in T} I_{st}(\tau_{st})$, with the mutual information $I_{st}(\tau_{st}) = \sum \tau_{st} \log \frac{\tau_{st}}{\tau_s \tau_t}$. Averaging over the trees gives

$$B(\tau) = \langle \theta, \tau \rangle + \sum_{s} H(\tau_s) - \sum_{(s,t) \in E} \rho_{st}\, I_{st}(\tau_{st}).$$

TRW computes $\max B(\tau)$ over the local polytope $\mathbb{L}$ of normalized, locally consistent pseudomarginals. Because each tree entropy is at least the true entropy, $\max_{\mathbb{L}} B \ge \log Z$. The vector $\rho$ must lie in the spanning tree polytope, and every $\rho_{st}$ must be positive.

**Choosing $\rho$.** For the uniform distribution over spanning trees, $\rho_{st}$ is the effective resistance between $s$ and $t$ when every edge is a unit resistor (Kirchhoff). It comes from the inverse of the Laplacian with one node removed, as in the [matrix-tree theorem](/matrix-tree-theorem/). On a cycle of length $L$ it is $(L-1)/L$, on the complete graph $K_n$ it is $2/n$, and on any graph the values add up to $n - 1$.

## The algorithm

The message from $t$ to $s$ is a function of $x_s$:

$$M_{ts}(x_s) \propto \sum_{x_t} \exp\Big(\frac{\theta_{st}(x_s, x_t)}{\rho_{st}} + \theta_t(x_t)\Big) \frac{\prod_{v \in N(t) \setminus s} M_{vt}(x_t)^{\rho_{vt}}}{M_{st}(x_t)^{1 - \rho_{st}}}.$$

The pairwise potential is divided by $\rho_{st}$, the incoming messages are raised to the power $\rho_{vt}$, and the message on the reverse edge is not left out, as in BP, but divided out to the power $1 - \rho_{st}$. With $\rho_{st} = 1$ all three changes vanish. The pseudomarginals are

$$\tau_s(x_s) \propto e^{\theta_s(x_s)} \prod_{v \in N(s)} M_{vs}(x_s)^{\rho_{vs}}, \qquad \tau_{st}(x_s, x_t) \propto e^{\theta_{st}/\rho_{st}}\, P_s(x_s)\, P_t(x_t),$$

with $P_s(x_s) = e^{\theta_s(x_s)} \prod_{v \in N(s) \setminus t} M_{vs}(x_s)^{\rho_{vs}} / M_{ts}(x_s)^{1 - \rho_{st}}$ and $P_t$ the same with $s$ and $t$ swapped.

```pseudo id=main
TRW(G, θ, λ, ε, T)
L1  ρ_st ← the edge appearance probabilities of a distribution over spanning trees (uniform: the effective resistances)
L2  log M_ts ← 0, for every edge in both directions
L3  for iteration i ← 1 to T do
L4      for every directed edge (t, s): M'_ts ← the TRW update, from the messages of iteration i − 1
L5      M_ts ← normalize(M'_ts^(1 − λ) M_ts^λ); δ ← the largest change of a message
L6      if δ < ε then break
L7  compute τ_s and τ_st from the messages
L8  return B(τ), τ
```

The messages are kept as logarithms, and damping is done on the logarithms. The returned $B(\tau)$ is an upper bound on $\log Z$ only if the run converged.

## Example

Take the 4-cycle $0 - 1 - 2 - 3 - 0$ with spins $x_s \in \{-1, +1\}$, $\theta_s = h_s x_s$ with $h = (0.2, -0.1, 0.3, 0)$, and $\theta_{st} = x_s x_t$ on all four edges. The cycle has four spanning trees, each without one edge, so the uniform distribution gives $\rho_{st} = 3/4$. The sum over the 16 states gives $\log Z = 4.87295$.

TRW with damping $\lambda = 0.5$ converges in 165 iterations to $B = 4.96432$, an upper bound with a gap of $0.091$. Loopy BP ($\rho = 1$) converges to $-F_{\mathrm{Bethe}} = 4.64550$, which is below $\log Z$ here.

| spin | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| exact $p(x_s = +1)$ | 0.6766 | 0.6667 | 0.6828 | 0.6732 |
| TRW $\tau_s(+1)$ | 0.6609 | 0.6478 | 0.6693 | 0.6564 |
| loopy BP | 0.7977 | 0.7810 | 0.8081 | 0.7920 |

Loopy BP counts the positive coupling of the loop again and again and is too sure. TRW counts each edge with weight $3/4$ and is a little too unsure. On the $3 \times 3$ grid, the uniform spanning tree weights are $17/24$ on the boundary edges and $7/12$ on the four edges that touch the center, which add up to $8$. On six seeded grids with fields in $[-0.5, 0.5]$ and couplings in $[-2, 2]$, the gap $B - \log Z$ was between $0.18$ and $1.38$.

## Correctness

The bound has a short proof. For any spanning tree $T$, the tree-structured distribution with the true marginals has entropy $H_T(\mu)$, and the true distribution has smaller entropy, because the gap is a [Kullback-Leibler divergence](/evidence-lower-bound/). Averaging over $\rho(T)$ gives $H(p) \le \sum_s H(\mu_s) - \sum \rho_{st} I_{st}(\mu_{st})$, so $B(\mu) \ge \log Z$ at the true marginals, and the maximum over the local polytope is at least as large.

At a fixed point, the pseudomarginals are locally consistent: summing $\tau_{st}$ over $x_t$ gives $\tau_s$. Wainwright, Jaakkola and Willsky proved more: $B$ is concave on $\mathbb{L}$, and the fixed points of the messages are exactly its maximizers. So a converged run returns $\max_{\mathbb{L}} B \ge \log Z$. When $B$ is strictly concave, the maximizer is unique, and the fixed point does not depend on the start. On a tree, $\rho = 1$, the messages are those of BP, and the result is exact. The proofs of the bound, the consistency and the tree case are in the correctness proof.

The message iteration itself has no general guarantee of convergence on a graph with cycles.

## Complexity

The costs are in the [real RAM](/real-ram/) model.

- **The weights.** The effective resistances need the inverse of an $(n-1) \times (n-1)$ matrix: $O(n^3)$ arithmetic operations. This is done once.
- **One message.** The product of the incoming messages costs $O(d k)$ and the sum over $x_t$ for each $x_s$ costs $O(k^2)$.
- **One iteration.** $2m$ messages: $O(m k (k + d))$.
- **Iterations.** Not bounded in general. In the example, 165.
- **Memory.** $O(m k)$ for the messages, $O(m k^2)$ for the pairwise pseudomarginals, and $O(n^2)$ for the inverse.

## Properties

- **An upper bound on $\log Z$.** At convergence, for any valid $\rho$. Loopy BP gives no bound, and [mean field](/mean-field-approximation/) gives a lower bound; together they bracket $\log Z$.
- **Concave objective.** Every fixed point is a global maximizer of $B$, and all of them give the same bound. When $B$ is strictly concave, there is one fixed point, whatever the start.
- **Reduces to BP.** With $\rho = 1$, which on a tree is forced.
- **Not exact on graphs with cycles.** Even the marginals at the best $\rho$ are not the true ones.
- **Optimizing $\rho$.** The bound is convex in $\rho$, so $\rho$ can be tuned over the spanning tree polytope to make it tighter.

## Variants and improvements

- **Optimized weights.** Wainwright, Jaakkola and Willsky minimize the bound over $\rho$ with a conditional gradient method, where each step solves a maximum weight spanning tree problem.
- **Tree-reweighted max-product.** The same reweighting applied to [max-product](/max-product/) gives a method for [MAP inference](/map-inference/) whose fixed points relate to the linear programming relaxation over the local polytope (Wainwright, Jaakkola and Willsky 2005, MAP paper).
- **TRW-S.** Kolmogorov's sequential schedule for tree-reweighted max-product, under which a lower bound on the minimum energy never decreases. The alias TRW-S names this MAP method, not the sum-product method of this page.
- **Other convex free energies.** Any counting numbers that make the free energy convex give a unique fixed point; the tree-reweighted ones are the ones with a proof of the upper bound.

## When to use it

Use TRW when you need a guaranteed upper bound on $\log Z$, for example to bracket the true value with a [mean field](/mean-field-approximation/) lower bound, or when loopy BP has several fixed points or depends on the start. For MAP problems in vision, the max-product form TRW-S is a standard tool. If you only need good marginals on a graph with few short loops, loopy BP is often more accurate.

## Pitfalls

- **Weights outside the spanning tree polytope.** Arbitrary $\rho$ give no bound. Take them from a distribution over spanning trees.
- **A zero weight.** The update divides $\theta_{st}$ by $\rho_{st}$. Every edge must lie in some tree of the distribution.
- **Reading a non-converged run.** The value $B(\tau)$ is a bound only at the maximizer. Before convergence, it can be below $\log Z$.
- **Loose bounds.** On dense frustrated models the local polytope allows pseudomarginals that no distribution has. On $K_4$ with all couplings $-2$ and no fields, $\log Z = 5.816$ but the TRW bound is $12.694$.
- **TRW-S is not this algorithm.** The alias is common, but TRW-S is the max-product method for MAP.

## Implementations

## History

The idea of bounding $\log Z$ by convex combinations of tractable problems goes back to the convexity of $\log Z$ as a function of the parameters. Wainwright, Jaakkola and Willsky applied it with spanning trees as the tractable problems in their 2005 paper in the IEEE Transactions on Information Theory, after conference versions from 2002, and showed that the best bound for fixed edge appearance probabilities is found by a reweighted form of the sum-product messages. The same authors gave the max-product form and its link to linear programming for MAP estimation. Kolmogorov (2006) changed the schedule of the max-product form so that it converges in a weak sense, and TRW-S became a standard method for energy minimization in computer vision.

## References
