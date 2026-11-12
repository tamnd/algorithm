---
tag: YPNGR6
kind: model
slug: dynamic-bayesian-network
name: Dynamic Bayesian network
aliases:
- DBN
- dynamic belief network
area: machine-learning/probabilistic-inference
level: advanced
summary: "A Bayesian network that repeats over time slices, given by a prior net and a two-slice net. HMMs and linear dynamical systems are special cases."
history:
  year: 1989
  people: [Thomas Dean, Keiji Kanazawa, Kevin P. Murphy]
  note: Dean and Kanazawa (1989) used a Bayesian network repeated over time to reason about persistence and causation. Murphy's 2002 thesis gave the 2TBN form and the frontier and interface algorithms in one framework.
prereqs: [bayesian-network, hidden-markov-model]
see_also: [state-space-model, kalman-filter, hidden-semi-markov-model, forward-algorithm, junction-tree-algorithm, variable-elimination, particle-filter, treewidth]
sources:
  - paper: doi:10.1111/j.1467-8640.1989.tb00324.x
    title: Thomas Dean and Keiji Kanazawa, A model for reasoning about persistence and causation, Computational Intelligence 5, 1989, pages 142 to 150
    locator: a Bayesian network with one copy of the state variables for each time point
  - paper: "Kevin P. Murphy, Dynamic Bayesian Networks: Representation, Inference and Learning, PhD thesis, University of California, Berkeley, 2002"
    title: Murphy 2002
    locator: "Chapter 2 (the DBN as a prior network and a 2TBN, with HMMs, factorial HMMs, HSMMs and linear dynamical systems as DBNs), Section 3.3 (the frontier algorithm, from Zweig 1996), Section 3.4 (the interface algorithm) and Section 4.2.1 (the Boyen-Koller approximation)"
  - paper: doi:10.1023/A:1007425814087
    title: Zoubin Ghahramani and Michael I. Jordan, Factorial hidden Markov models, Machine Learning 29, 1997, pages 245 to 273
    locator: the factorial HMM, and the cost of exact inference, O(T K N^(K+1)) for K chains of N states
  - paper: "Xavier Boyen and Daphne Koller, Tractable inference for complex stochastic processes, Proceedings of the 14th Conference on Uncertainty in Artificial Intelligence (UAI), 1998, pages 33-42"
    title: Boyen and Koller 1998
    locator: the belief as a product of cluster marginals, and the bound on the error over time
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 6 (template models, the 2-TBN and its unrolling) and Chapter 15 (inference in temporal models, and entanglement)"
---

A dynamic Bayesian network (DBN) is a [Bayesian network](/bayesian-network/) for a process that goes on in time. Each time step, or slice, has the same set of variables, and the same small network connects each slice to the one before it. So two pieces define a model of any length: a network for the first slice and a two-slice network for the step from $t - 1$ to $t$. A [hidden Markov model](/hidden-markov-model/) is the DBN with one hidden variable and one observed variable per slice. A DBN can have many hidden variables per slice, each with few parents, so the model needs far fewer numbers than the HMM on the joint state. Exact filtering does not get this saving in general: after a few steps the hidden variables of a slice are all dependent, and the exact belief needs a table that is exponential in their number.

## The machine

**Variables.** Each slice $t$ has the variables $Z_t = (Z_t^1, \ldots, Z_t^n)$. Some are hidden and some are observed. In the implementation on this page there are $K$ binary hidden chains $X_t^0, \ldots, X_t^{K-1}$, and each chain $k$ has one observed child $Y_t^k$.

**The 2TBN.** As in Murphy (2002, Chapter 2), a DBN is a pair $(B_1, B_\to)$.

- $B_1$ is a Bayesian network over $Z_1$. It gives the prior $P(Z_1)$.
- $B_\to$, the two-slice temporal Bayesian network (2TBN), gives each variable of slice $t$ parents in slice $t - 1$ or in slice $t$, and a [conditional probability table](/conditional-probability-table/):

$$P(Z_t \mid Z_{t-1}) = \prod_{i=1}^{n} P\bigl(Z_t^i \mid \operatorname{Pa}(Z_t^i)\bigr).$$

The arcs inside a slice must form a DAG. The 2TBN is the same for every $t$, and the process is first-order Markov in $Z_t$.

**Unrolling.** For $T$ slices, copy $B_1$ once and $B_\to$ $T - 1$ times. The result is an ordinary Bayesian network with $n T$ variables, and its joint is

$$P(Z_1, \ldots, Z_T) = P(Z_1) \prod_{t=2}^{T} P(Z_t \mid Z_{t-1}).$$

Any inference method for Bayesian networks works on the unrolled network. The special methods below use the fact that its shape repeats.

**Filtering.** The main task is the belief $P(X_t \mid y_1, \ldots, y_t)$ for each $t$, plus the likelihood $P(y_1, \ldots, y_T)$. One correct method forms the flat HMM: its states are the $2^K$ joint values of the hidden chains, its transition matrix is the product of the CPTs, and its emission is the product of the $P(Y^k \mid X^k)$. The [forward algorithm](/forward-algorithm/) on this HMM costs $O(T \, 4^K)$ time after the $2^K \times 2^K$ matrix is built.

**The frontier algorithm.** The frontier algorithm (Zweig 1996; Murphy 2002, Section 3.3) never builds that matrix. It keeps one table, the frontier, over a set of variables that separates the past from the future. To go from slice $t - 1$ to slice $t$:

1. Start with the belief over the hidden variables of slice $t - 1$.
2. Add the variables of slice $t$ one at a time. To add $X_t^k$, multiply the table by $P(X_t^k \mid \operatorname{Pa}(X_t^k))$ and by the evidence $P(y_t^k \mid X_t^k)$. Its parents are already in the frontier.
3. As soon as all children of an old variable $X_{t-1}^i$ are in the frontier, sum $X_{t-1}^i$ out.
4. At the end the table covers slice $t$ only. Its total is $P(y_t \mid y_1, \ldots, y_{t-1})$. Divide by it to get the new belief.

The implementation runs this in exact arithmetic or in floats. The tests compare it with the sum over all trajectories of the unrolled network, and with the forward algorithm on the flat HMM for $T = 200$.

**The interface algorithm.** The outgoing interface of slice $t$ is the set of its variables that have children in slice $t + 1$. This set separates the past from the future, so a filter only needs the joint over the interface. The interface algorithm (Murphy 2002, Section 3.4) builds a junction tree for one and a half slices, the interface of slice $t - 1$ together with all of slice $t$, and passes messages from slice to slice through a clique that holds the interface.

**Example.** Take two binary chains with no useful observations. $X^0$ keeps its value with probability $0.9$. $X^1_t$ copies $X^0_{t-1}$ with probability $0.9$ and does not depend on its own past. In slice 1 both are uniform and independent. In slice 2 both are still uniform, but

$$P(X_2^0 = 1, X_2^1 = 1) = \tfrac{1}{2}(0.9 \cdot 0.9) + \tfrac{1}{2}(0.1 \cdot 0.1) = 0.41 \ne 0.25,$$

because both depend on $X_1^0$. The belief over slice 2 does not factor, even though no variable of slice 2 is a parent of the other. The tests check this table exactly.

## What it counts

The size measures are $T$, the number of slices, $K$, the number of hidden variables per slice, here binary, and $F$, the largest number of variables in the frontier. One step is one arithmetic operation, as on the [real RAM](/real-ram/).

- **Model size.** The 2TBN needs one table per variable, with $2^{|\operatorname{Pa}|}$ rows. With at most $p$ parents each, that is $O(K 2^p)$ numbers, against $4^K$ for the flat transition matrix.
- **The flat HMM.** $O(T \, 4^K)$ time and $O(2^K)$ memory for filtering.
- **The frontier algorithm.** Adding one variable to a frontier of size $f$ costs $O(2^{f+1})$, so a slice costs $O(K 2^F)$ and filtering costs $O(T K 2^F)$. The frontier holds all $K$ old variables at the start of each slice, so $F \ge K$.
  - If each chain has only itself as a parent, as in a factorial HMM with one observation per chain, then $F = K + 1$ and the cost is $O(T K 2^{K+1})$, far less than $O(T 4^K)$.
  - If each variable has all of the previous slice as parents, no old variable can leave until all new ones are in, so $F = 2K$, and the frontier algorithm is no better than the flat HMM.
  - The order of addition matters. The tests show a model with $K = 3$ in which one order gives $F = 4$ and the other gives $F = 5$.
- **Smoothing** with a backward pass has the same cost as filtering.

## Relation to other models

- **Hidden Markov models.** One discrete hidden variable and one observed child per slice. Every DBN with discrete hidden variables is an HMM on the joint hidden state; the DBN gives a compact form of its transition matrix.
- **Linear dynamical systems.** Real hidden and observed vectors with linear Gaussian CPTs. Exact filtering is the [Kalman filter](/kalman-filter/). See [state-space models](/state-space-model/).
- **Factorial and coupled HMMs.** Several hidden chains, each with its own transitions, that share one observation (Ghahramani and Jordan 1997), or whose chains have arcs between them.
- **Hidden semi-Markov models.** A second hidden variable that counts the steps left in the current segment turns an [HSMM](/hidden-semi-markov-model/) into a DBN with two hidden variables per slice.
- **Bayesian networks.** A DBN unrolled for $T$ slices is a Bayesian network. Exact methods for Bayesian networks, such as [variable elimination](/variable-elimination/) and the [junction tree algorithm](/junction-tree-algorithm/), apply to it, with a cost set by the [treewidth](/treewidth/) of the unrolled graph.

## Known results in the model

- **Entanglement.** Even when the 2TBN is sparse, the hidden variables of one slice become dependent after a few steps through their common ancestors, or through an observation they share. So the exact belief over a slice in general needs a table over all hidden variables of the slice, of size exponential in their number. Koller and Friedman (Chapter 15) call this entanglement. The example above shows it after one step.
- **Cost of exact filtering.** Both the frontier and the interface algorithms take time exponential in the number of hidden variables per slice for most DBNs (Murphy 2002, Sections 3.3.4 and 3.4.4). For a factorial HMM with $K$ chains of $N$ states, exact inference costs $O(T K N^{K+1})$ (Ghahramani and Jordan 1997).
- **Chains that do not interact stay independent.** If each hidden chain has only itself as a parent and its own observations, the belief stays a product of one-chain beliefs. The tests check this exactly.
- **Approximate filtering.** The Boyen-Koller algorithm keeps the belief as a product of marginals over small clusters and projects onto this form after each step. Boyen and Koller (1998) show that the error does not grow without bound over time, because the process forgets its past. The factored frontier algorithm (Murphy 2002, Section 4.2.2) and [particle filters](/particle-filter/) are other approximations.
- **History.** Dean and Kanazawa (1989) used a network with one copy of the state variables per time point to reason about how facts persist and change. Murphy (2002) defined the DBN by the pair $(B_1, B_\to)$ and studied exact and approximate inference and learning for it.

## References
