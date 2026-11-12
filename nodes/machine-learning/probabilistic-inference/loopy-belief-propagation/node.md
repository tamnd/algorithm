---
tag: BP1TB7
kind: algorithm
slug: loopy-belief-propagation
name: Loopy belief propagation
aliases:
- loopy BP
- loopy sum-product
- iterative belief propagation on graphs with cycles
area: machine-learning/probabilistic-inference
level: advanced
summary: "Run the sum-product messages of belief propagation on a factor graph with cycles until they stop changing. No convergence guarantee; fixed points are Bethe stationary points."
solves: [marginal-inference]
model: real-ram
complexity:
  vars: {t: the number of iterations, m: the number of factors, r: the largest number of variables in a factor, k: the largest number of states of a variable}
  time: {worst: "O(t m r k^r)"}
  space: {extra: "O(m r k)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1988
  people: [Judea Pearl, Robert J. McEliece, David J. C. MacKay, Kevin P. Murphy, Yair Weiss, Michael I. Jordan]
  note: Pearl (1988) suggested running belief propagation on networks with loops. McEliece, MacKay and Cheng (1998) showed that turbo decoding is this algorithm, and Murphy, Weiss and Jordan (1999) studied its accuracy and convergence on other networks.
prereqs: [belief-propagation, factor-graph, marginal-inference]
see_also: [bethe-free-energy, residual-belief-propagation, generalized-belief-propagation, tree-reweighted-belief-propagation, gaussian-belief-propagation, mean-field-approximation, ldpc-code, junction-tree-algorithm]
sources:
  - book: isbn:9781558604797
    title: Judea Pearl, Probabilistic Reasoning in Intelligent Systems, Morgan Kaufmann, 1988
    locator: "Chapter 4 (belief updating by network propagation in trees and polytrees, and the discussion of networks with loops)"
  - paper: doi:10.1109/49.661103
    title: "Robert J. McEliece, David J. C. MacKay and Jung-Fu Cheng, Turbo decoding as an instance of Pearl's belief propagation algorithm, IEEE Journal on Selected Areas in Communications 16(2), 1998, pages 140 to 152"
    locator: turbo decoding is belief propagation on a Bayesian network with loops
  - paper: "Kevin P. Murphy, Yair Weiss and Michael I. Jordan, Loopy belief propagation for approximate inference: an empirical study, Proceedings of the 15th Conference on Uncertainty in Artificial Intelligence (UAI), 1999"
    title: Murphy, Weiss and Jordan 1999
    locator: accuracy on the PYRAMID, toyQMR and QMR-DT networks, the oscillations, and damping (momentum) as a remedy
  - paper: doi:10.1109/TIT.2005.850085
    title: "Jonathan S. Yedidia, William T. Freeman and Yair Weiss, Constructing free-energy approximations and generalized belief propagation algorithms, IEEE Transactions on Information Theory 51(7), 2005, pages 2282 to 2312"
    locator: "the Bethe free energy and the theorem that the fixed points of BP with positive messages are the stationary points of the Bethe free energy on the local polytope"
  - paper: "Jonathan S. Yedidia, William T. Freeman and Yair Weiss, Generalized belief propagation, Advances in Neural Information Processing Systems 13 (NIPS 2000), MIT Press, 2001"
    title: Yedidia, Freeman and Weiss 2001
    locator: first statement of the equivalence of BP fixed points and Bethe stationary points
  - paper: doi:10.1109/TIT.2007.909166
    title: "Joris M. Mooij and Hilbert J. Kappen, Sufficient conditions for convergence of the sum-product algorithm, IEEE Transactions on Information Theory 53(12), 2007, pages 4422 to 4437"
    locator: "the condition on the spectral radius of the matrix of tanh|J_ij| over directed edges for binary pairwise models, which gives a unique fixed point and convergence from any start"
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, MIT Press, 2009
    locator: "Section 11.3 (propagation-based approximation: loopy belief propagation on cluster graphs, convergence, damping and message scheduling)"
  - paper: "Tom Heskes, Stable fixed points of loopy belief propagation are local minima of the Bethe free energy, Advances in Neural Information Processing Systems 15 (NIPS 2002), MIT Press, 2003"
    title: Heskes 2003
    locator: stable fixed points of BP are local minima, not only stationary points, of the Bethe free energy
---

Loopy belief propagation runs the sum-product messages of [belief propagation](/belief-propagation/) on a [factor graph](/factor-graph/) that has cycles. Each message is recomputed from the others again and again, and when the messages stop changing, the beliefs are used as approximate marginals. On a tree the same rules give the exact marginals; on a graph with cycles the answer is approximate, the iteration may oscillate, and damping often helps. Its fixed points are exactly the stationary points of the [Bethe free energy](/bethe-free-energy/), which explains what it computes. It is the decoder of [LDPC codes](/ldpc-code/) and turbo codes, and a standard method for approximate [marginal inference](/marginal-inference/).

## In plain words

On a tree, belief propagation works like a careful gossip network: each node collects reports from all its other neighbors, sums them up, and passes one report on. A report never comes back to the node that started it, so nothing is counted twice, and the result is exact.

On a graph with loops, a report can travel around a loop and come back. Loopy belief propagation ignores this problem and keeps passing reports in rounds until they stop changing. Evidence is then counted more than once, so the answer is only approximate. The rounds might also never settle; they can swing back and forth. Mixing each new report with the old one, which is called damping, often calms them down. In practice the answers are often good, which is why the method is so widely used.

## The problem

**The model.** A positive distribution on a factor graph with variables $x_1, \ldots, x_n$, where $x_i$ has $k_i$ states, and factors $f_1, \ldots, f_m$:

$$p(x) = \frac{1}{Z} \prod_{a=1}^m f_a(x_a), \qquad f_a > 0,$$

where $x_a$ is the vector of the variables in the scope of factor $a$. Write $N(a)$ for the variables of factor $a$ and $N(i)$ for the factors that contain $x_i$. A [Bayesian network](/bayesian-network/) or a [Markov random field](/markov-random-field/) becomes a factor graph with one factor per conditional table or potential.

**The query.** The single-variable marginals $p(x_i)$ and the factor marginals $p(x_a)$. Exact marginals are #P-hard in general, and the [junction tree algorithm](/junction-tree-algorithm/) is exponential in the treewidth. Loopy BP gives approximate *beliefs* $b_i \approx p(x_i)$ and $b_a \approx p(x_a)$.

**The messages.** There are two kinds on each edge $(i, a)$ of the factor graph, each a vector over the states of $x_i$:

$$\nu_{i \to a}(x_i) \propto \prod_{c \in N(i) \setminus a} \mu_{c \to i}(x_i), \qquad \mu_{a \to i}(x_i) \propto \sum_{x_a \setminus x_i} f_a(x_a) \prod_{j \in N(a) \setminus i} \nu_{j \to a}(x_j),$$

and the beliefs are

$$b_i(x_i) \propto \prod_{a \in N(i)} \mu_{a \to i}(x_i), \qquad b_a(x_a) \propto f_a(x_a) \prod_{i \in N(a)} \nu_{i \to a}(x_i).$$

These are the equations of belief propagation. Loopy BP uses them on a graph with cycles, where they are no longer a finite recursion but a system of fixed point equations.

## The algorithm

The schedule here is synchronous (also called flooding): each round computes all new messages from the old ones. The damping factor $\lambda \in [0, 1)$ mixes each new message with the old one; $\lambda = 0$ is plain loopy BP.

```pseudo id=main
LOOPY-BP(factor graph, f, λ, ε, T)
L1  μ_{a→i} ← uniform, for every edge (a, i)
L2  for t ← 1 to T do
L3      ν_{i→a}(x_i) ← normalize(Π_{c ∈ N(i)∖a} μ_{c→i}(x_i)), for every edge
L4      μ'_{a→i}(x_i) ← normalize(Σ_{x_a∖x_i} f_a(x_a) Π_{j ∈ N(a)∖i} ν_{j→a}(x_j)), for every edge
L5      δ ← max over edges and states of |μ'_{a→i} − μ_{a→i}|
L6      μ_{a→i} ← normalize((1 − λ) μ'_{a→i} + λ μ_{a→i}), for every edge
L7      if δ < ε then return the beliefs b_i, b_a, "converged"
L8  return the beliefs b_i, b_a, "not converged"
```

The normalization does not change the beliefs; it keeps the numbers in range. For long runs or sharp factors, work with logarithms. The output must say whether the run converged: the beliefs after $T$ rounds of an oscillating run are not an approximation of anything.

## Example

**A 4-cycle.** Take an Ising model on spins $s_i \in \{-1, +1\}$ with unary factors $e^{h_i s_i}$ and pairwise factors $e^{J s_i s_j}$, on the cycle $1 - 2 - 4 - 3 - 1$, with $J = 0.5$ on each edge and $h = (0.3, -0.2, 0.1, 0)$. With $\lambda = 0$, the belief $b_1(+1)$ after rounds 1 to 8 is $0.6457, 0.6246, 0.6246, 0.6200, 0.6321, 0.6312, 0.6312, 0.6311$. The run reaches $\delta < 10^{-6}$ after 17 rounds and $\delta < 10^{-10}$ after 28.

| spin | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| loopy BP, $b_i(+1)$ | 0.6315 | 0.4981 | 0.5958 | 0.5357 |
| exact, $p(s_i = +1)$ | 0.6211 | 0.4982 | 0.5882 | 0.5329 |

The largest error is 0.0104. The exact values come from the sum over all 16 states. BP is too confident here: each belief is a little farther from $1/2$ than the exact marginal, because the evidence of each field returns around the cycle. The [mean-field approximation](/mean-field-approximation/) on the same model gives the means $\mathbb{E}[s_i] = (0.617, 0.297, 0.542, 0.397)$, which is far worse than BP's $(0.263, -0.004, 0.192, 0.071)$.

**A tree.** On a chain of 6 spins with random fields and couplings, the messages stop changing after at most 7 rounds, and the beliefs agree with the exact marginals to $10^{-10}$, as they must.

**A frustrated loop.** On the complete graph $K_4$ with $J = -2$ on every edge (each spin wants to differ from all three others, which is impossible) and $h = (0.5, 0, 0, 0)$, plain loopy BP does not converge. After a few rounds, all four beliefs $b_i(+1)$ swing between almost 0 and almost 1 at every round, a cycle of period 2. With $\lambda = 0.3$ it still does not converge in 5000 rounds; with $\lambda = 0.5$ it converges in 854 rounds and with $\lambda = 0.7$ in 273. The converged beliefs, $b_1(+1) = 0.508$ and $b_i(+1) = 0.498$ for the others, are poor: the exact marginals are $0.731$ and $0.425$. Damping changes whether the iteration converges, not the quality of the fixed point.

## Correctness

Loopy BP has no general guarantee of convergence or accuracy. What is proved:

- **Exact on trees.** If the factor graph is a tree, the synchronous schedule with $\lambda = 0$ reaches the exact messages after at most as many rounds as the longest path, and the beliefs are then the exact marginals. With damping, the unique fixed point is still the exact one.
- **Damping keeps the fixed points.** If $\mu = (1 - \lambda) F(\mu) + \lambda \mu$ with $\lambda < 1$, then $\mu = F(\mu)$.
- **Local consistency.** At a fixed point, $\sum_{x_a \setminus x_i} b_a(x_a) = b_i(x_i)$ for every edge. The beliefs are a point of the *local polytope*, even when no distribution has them as marginals.
- **The variational meaning.** The fixed points with positive messages are exactly the stationary points of the Bethe free energy $F_{\mathrm{Bethe}}(b)$ over the local polytope (Yedidia, Freeman and Weiss 2001, 2005), and the stable fixed points are local minima (Heskes 2003).
- **A sufficient condition for convergence.** For binary pairwise models $p \propto \exp(\sum_i h_i s_i + \sum_{ij} J_{ij} s_i s_j)$, let $A$ be the matrix over directed edges with $A_{i \to j,\, k \to i} = \tanh |J_{ki}|$ for $k \in N(i) \setminus j$ and 0 elsewhere. If the spectral radius of $A$ is below 1, BP has a unique fixed point and converges to it from any start (Mooij and Kappen 2007). It does not depend on the fields. For the 4-cycle above the radius is $\tanh 0.5 \approx 0.46$; for the frustrated $K_4$ it is $2 \tanh 2 \approx 1.93$, so the condition says nothing there.

The proofs of the first four points are in the correctness proof.

## Complexity

The costs are in the [real RAM](/real-ram/) model, with $m$ factors of at most $r$ variables with at most $k$ states each.

- **One round.** Line L4 for one factor sums over its $k^r$ joint states. Done naively for each of its $r$ edges, this costs $O(r^2 k^r)$ per factor; computing the product of all incoming messages once and dividing (or using prefix and suffix products) brings it to $O(r k^r)$. Line L3 costs $O(\deg(i)\, k)$ per edge with the same trick. So a round costs $O(m r k^r)$. For a pairwise model with $e$ edges, this is $O(e k^2)$.
- **Rounds.** The number $t$ of rounds is not bounded in general, and the method may never converge. On a tree, $t$ is at most the diameter of the factor graph. Under the Mooij-Kappen condition, the convergence is geometric.
- **Memory.** Two messages of $k$ numbers per edge: $O(m r k)$.

## Properties

- **Exact on trees, approximate on loops.** The error comes from evidence that travels around cycles. Loops that are long or weakly coupled give small errors; short, strongly coupled and frustrated loops give large ones.
- **Overconfidence.** On a loop of attractive (ferromagnetic) couplings, beliefs tend to be more extreme than the exact marginals, as in the 4-cycle example.
- **Many fixed points.** On strongly coupled graphs the Bethe free energy can have several minima, and the result depends on the start and the schedule.
- **No bound.** Unlike [mean field](/mean-field-approximation/) (a lower bound on $\log Z$) or [tree-reweighted BP](/tree-reweighted-belief-propagation/) (an upper bound), the Bethe approximation of $\log Z$ can be on either side.
- **Local and parallel.** Each message needs only its neighbors, so the method suits parallel hardware and very large sparse graphs.

## Variants and improvements

- **Schedules.** A sequential schedule, which updates one message at a time with the newest values, often converges faster than the synchronous one. [Residual belief propagation](/residual-belief-propagation/) updates first the message that would change most.
- **Damping in the log domain.** Damping $\log \mu$ instead of $\mu$ is also common; it has the same fixed points.
- **Max-product.** Replace the sum of line L4 by a maximum to get loopy [max-product](/max-product/), an approximation of [MAP inference](/map-inference/); [affinity propagation](/affinity-propagation/) is an example.
- **Larger regions.** [Generalized belief propagation](/generalized-belief-propagation/) passes messages between clusters of variables and finds stationary points of the Kikuchi free energy; it is often more accurate on grids.
- **Convex variants.** [Tree-reweighted belief propagation](/tree-reweighted-belief-propagation/) changes the entropy weights so that the free energy is convex, which gives a unique fixed point and an upper bound on $\log Z$.
- **Continuous variables.** [Gaussian belief propagation](/gaussian-belief-propagation/) passes means and precisions; if it converges, its means are exact on any graph. [Expectation propagation](/expectation-propagation/) projects messages onto an exponential family.

## When to use it

Use loopy BP for large sparse models where exact inference is out of reach and the loops are long or weak: error-correcting codes such as [LDPC codes](/ldpc-code/), low-level vision on grids, and sparse networks. Check convergence on each run. If it does not converge, damp it or change the schedule, and if it still fails or the couplings are strong and frustrated, use the junction tree algorithm on a small model, generalized BP, or [Gibbs sampling](/gibbs-sampling/).

## Pitfalls

- **Reading unconverged beliefs.** After $T$ rounds of an oscillating run, the beliefs depend on the parity of $T$. Report the convergence status, as line L8 does.
- **Too little damping.** On the frustrated $K_4$, $\lambda = 0.3$ is not enough. Raise $\lambda$ until the run converges, and accept the slower progress.
- **Trusting the fixed point.** Convergence does not mean accuracy: the frustrated example converges with damping to beliefs that are off by 0.22.
- **Zero entries.** Factors with zeros can make all messages zero at some state, and the normalization then divides by 0. Hard constraints, as in codes, need log-domain arithmetic and care.
- **Underflow.** Products of many messages underflow. Normalize at every step, or work with logs.
- **Double counting in a model that is almost a tree.** If a model has a few loops, exact methods on a [junction tree](/junction-tree-algorithm/) may cost little and remove the error.

## Implementations

## History

Pearl gave belief propagation for trees and polytrees in his 1988 book and noted that the same local rules could run on networks with loops, without a guarantee. Ten years later, McEliece, MacKay and Cheng showed that the decoder of the turbo codes of Berrou, Glavieux and Thitimajshima, which works far better than expected, is belief propagation on a graph with loops; Gallager's decoder for LDPC codes from 1963 is another instance. Murphy, Weiss and Jordan in 1999 tested loopy BP on other networks and found that it often converges to good marginals, that it can oscillate, and that damping can help. Yedidia, Freeman and Weiss in 2001 showed that the fixed points are the stationary points of the Bethe free energy of statistical physics, which led to generalized belief propagation. Mooij and Kappen in 2007 gave sufficient conditions for convergence.

## References
