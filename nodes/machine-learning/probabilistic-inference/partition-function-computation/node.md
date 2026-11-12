---
tag: 4FZ51R
kind: problem
slug: partition-function-computation
name: Partition function computation
aliases:
- computing the partition function
area: machine-learning/probabilistic-inference
level: advanced
summary: "Compute Z, the sum of a product of factors over all configurations. Elimination takes time exponential in the induced width; in general it is #P-hard."
prereqs: [partition-function, variable-elimination]
see_also: [marginal-inference, junction-tree-algorithm, belief-propagation, kasteleyn-method, ising-model, model-counting, fpras, treewidth]
sources:
  - paper: doi:10.1016/0004-3702(94)00092-1
    title: "Dan Roth, On the hardness of approximate reasoning, Artificial Intelligence 82(1-2), 1996, pages 273 to 302"
    locator: exact probabilistic inference is #P-complete, by a reduction from counting satisfying assignments
  - paper: doi:10.1016/0031-8914(61)90063-5
    title: "Pieter W. Kasteleyn, The statistics of dimers on a lattice, I. The number of dimer arrangements on a quadratic lattice, Physica 27(12), 1961, pages 1209 to 1225"
    locator: counting the perfect matchings of a planar lattice by a Pfaffian
  - paper: doi:10.1103/PhysRev.124.1664
    title: "Michael E. Fisher, Statistical mechanics of dimers on a plane lattice, Physical Review 124(6), 1961, pages 1664 to 1672"
    locator: the dimer method on plane lattices, which also gives the partition function of the planar Ising model without a field
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 9, Sections 9.1 to 9.4 (complexity of inference, and variable elimination applied to the unnormalized measure)"
---

Partition function computation is the problem of finding $Z = \sum_x \prod_c \psi_c(x_c)$, the sum over all configurations of a product of nonnegative factors. It gives the normalization of a [Markov random field](/markov-random-field/), the probability of evidence in a [Bayesian network](/bayesian-network/), and the free energy in statistical physics; see [partition function](/partition-function/) for its meaning. Exact computation by [variable elimination](/variable-elimination/) takes $O(n\, d^{w+1})$ time for an elimination order of induced width $w$, so it is fast on trees and on graphs of small [treewidth](/treewidth/). In general the problem is #P-hard (Roth 1996): it includes counting the satisfying assignments of a formula. Some special families are easy for other reasons: the Ising model on a planar graph without an external field has a partition function computable in polynomial time by the Pfaffian method of Kasteleyn (1961) and Fisher (1961).

## In plain words

You have a model that gives a score to each full configuration, and you want the total of all scores.

Adding them one by one takes too long: with 100 yes or no variables there are more than a million million million million million configurations. When each score is a product of small parts, you can add up in a better order, one variable at a time. This is fast when the variables form a tree or something close to a tree.

For some models no fast method is known. The problem contains the problem of counting the solutions of a logic formula, which is believed to be very hard. A few models are easy for a special reason, like a flat grid of magnets with no outside field.

## Definition

**Input.** Discrete variables $X_1, \ldots, X_n$ with domains of size at most $d$, and factors $\psi_c$ given as tables of nonnegative rationals over small scopes $c$.

**Output.** The number $Z = \sum_{x} \prod_c \psi_c(x_c)$, exactly as a rational, or $\log Z$.

**Evidence.** With some variables fixed to $e$, the sum over the other variables is $Z(e)$. For a Bayesian network $Z(e) = P(e)$.

**Approximate versions.** Output $\hat Z$ with $(1 - \varepsilon) Z \le \hat Z \le (1 + \varepsilon) Z$ (relative error), or $\log \hat Z$ within an additive $\varepsilon$, with probability at least $1 - \delta$ for randomized methods.

## Variants

- **Counting.** With 0 and 1 factors, $Z$ is the number of configurations that satisfy all constraints: [model counting](/model-counting/) for formulas, the number of independent sets, of proper colourings, or of perfect matchings.
- **Weighted counting.** Weights on literals or on variables give weighted model counting, which can encode any discrete model.
- **Physics models.** The [Ising model](/ising-model/) and the Potts model, with or without an external field, ferromagnetic or not.
- **Gaussian models.** For $\tilde p(x) = \exp(-\frac12 x^\top J x + h^\top x)$ with $J$ positive definite, $Z = (2\pi)^{n/2} \det(J)^{-1/2} \exp(\frac12 h^\top J^{-1} h)$, a determinant: polynomial time.
- **Bounds.** Upper and lower bounds on $\log Z$, as given by variational methods.

## Examples

**An Ising cycle.** Four binary spins on a cycle $x_1 x_2 x_3 x_4$, each edge with the factor $\psi(a, b) = 2$ if $a = b$ and 1 otherwise. Count by the number of disagreeing edges, which is even on a cycle: 0 (2 configurations, product 16), 2 (12 configurations, product 4), 4 (2 configurations, product 1). So $Z = 32 + 48 + 2 = 82$.

Variable elimination gets the same in two steps. Summing out $x_1$ gives $\tau_1(x_2, x_4) = \sum_{x_1} \psi(x_1, x_2)\, \psi(x_1, x_4)$, which is $2 \cdot 2 + 1 \cdot 1 = 5$ when $x_2 = x_4$ and $2 \cdot 1 + 1 \cdot 2 = 4$ when they differ. Summing out $x_3$ gives the same table $\tau_3(x_2, x_4)$. Then $Z = \sum_{x_2, x_4} \tau_1 \tau_3 = 2 \cdot 25 + 2 \cdot 16 = 82$. The largest table had two variables: the induced width of this order is 2.

**A chain.** For a chain with $n$ variables and pairwise factors, $Z = \mathbf{1}^\top M_1 M_2 \cdots M_{n-1} \mathbf{1}$ for the matrices $M_i = [\psi_i(a, b)]$. This is the transfer matrix method of physics and costs $O(n d^2)$.

## Known algorithms

Exact:

- **Enumeration**: $O(d^n)$ products. A test reference.
- **[Variable elimination](/variable-elimination/)**: sum out all the variables. $O(n\, d^{w+1})$ for an [elimination ordering](/elimination-ordering/) of induced width $w$.
- **[Junction tree algorithm](/junction-tree-algorithm/)** and **[belief propagation](/belief-propagation/)** on trees: the sum of any calibrated clique table is $Z$, and all marginals come with it.
- **Pfaffian method**: for the Ising model on a planar graph without a field, $Z$ is a weighted count of the perfect matchings of a related planar graph, and these are counted by the Pfaffian of a skew matrix ([Kasteleyn's method](/kasteleyn-method/)), in polynomial time.
- **Gaussian elimination** for Gaussian models, and **knowledge compilation**: compile the model to a circuit in which $Z$ is one pass.

Approximate:

- **Monte Carlo**: estimate a chain of ratios $Z(\beta_{i+1})/Z(\beta_i)$ by [Markov chain Monte Carlo](/gibbs-sampling/) along a path of models (annealing), or use [importance sampling](/importance-sampling/). For the ferromagnetic Ising model, Jerrum and Sinclair (1993) gave a fully polynomial randomized approximation scheme ([FPRAS](/fpras/)).
- **Variational**: [mean field](/mean-field-approximation/) gives a lower bound on $\log Z$; [loopy belief propagation](/loopy-belief-propagation/) gives the Bethe approximation; tree-reweighted methods give an upper bound.

## Bounds

- **Upper bound.** $O(n\, d^{w^*+1})$ with an order of width $w^*$, the treewidth of the graph that joins the variables of each factor. So the problem is fixed-parameter tractable in the treewidth.
- **#P-hardness.** Computing $Z$ exactly is #P-hard in general. With 0 and 1 factors it counts the satisfying assignments of a CNF formula, which is #P-complete; Roth (1996) gave this reduction for inference in Bayesian networks. It stays #P-hard for simple models such as counting independent sets.
- **Hardness of approximation.** Deciding $Z > 0$ is already NP-hard for 0 and 1 factors (satisfiability), so no relative approximation exists in polynomial time unless P = NP; see the [Dagum-Luby theorem](/dagum-luby-theorem/) for the probabilistic form.
- **Easy special cases.** Bounded treewidth; the planar Ising model without a field; Gaussian models; models whose factor graph is a tree.

## Reductions

- **From #SAT.** For a CNF formula, one 0 and 1 factor per clause gives $Z = $ the number of satisfying assignments.
- **To and from marginals.** $P(x_Q \mid e) = Z(x_Q, e)/Z(e)$, so marginals reduce to partition functions. Conversely, for any $x$ with $\tilde p(x) > 0$, $Z = \tilde p(x) / P(x)$, and $P(x) = \prod_i P(x_i \mid x_1, \ldots, x_{i-1})$ is a product of $n$ marginals: [marginal inference](/marginal-inference/) and $Z$ are equally hard, and so are their approximations up to the factor lost in $n$ steps.
- **From counting perfect matchings.** A 0 and 1 model with one variable per edge and one factor per vertex has $Z$ equal to the number of perfect matchings, a #P-complete count in general graphs and a polynomial one in planar graphs ([counting perfect matchings](/counting-perfect-matchings/)).

## Applications

- Normalizing and comparing undirected models, and training them: the gradient of $\log Z$ is the vector of feature means.
- The probability of evidence in Bayesian networks, used to compare explanations and models.
- Statistical physics: free energy, phase diagrams, and exact solutions on planar lattices.
- Counting combinatorial objects, through the counting examples above.

## References
