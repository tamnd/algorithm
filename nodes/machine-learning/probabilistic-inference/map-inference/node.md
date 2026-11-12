---
tag: VQER59
kind: problem
slug: map-inference
name: MAP inference
aliases:
- most probable explanation
- MPE
- marginal MAP
area: machine-learning/probabilistic-inference
level: core
summary: "Find a most probable assignment given evidence. Over all hidden variables (MPE) it is NP-hard; over a subset (marginal MAP) it is NP^PP-complete."
prereqs: [marginal-inference, bayesian-network]
see_also: [max-product, viterbi-algorithm, maximum-a-posteriori-estimation, variable-elimination, junction-tree-algorithm, image-segmentation-graph-cuts, depth-first-branch-and-bound, cooper-theorem]
sources:
  - paper: doi:10.1016/0004-3702(94)90072-8
    title: "Solomon Eyal Shimony, Finding MAPs for belief networks is NP-hard, Artificial Intelligence 68(2), 1994, pages 399 to 410"
    locator: the most probable assignment of all the variables (MPE) is NP-hard, by a reduction from satisfiability
  - paper: doi:10.1613/jair.1236
    title: "James D. Park and Adnan Darwiche, Complexity results and approximation strategies for MAP explanations, Journal of Artificial Intelligence Research 21, 2004, pages 101 to 133"
    locator: MAP over a subset of the variables is NP^PP-complete, and stays NP-hard in cases where marginals and MPE are easy
  - book: isbn:9781558604797
    title: Judea Pearl, Probabilistic Reasoning in Intelligent Systems, Morgan Kaufmann, 1988
    locator: "Chapter 5, belief revision and the most probable explanation"
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 13 (MAP inference), including the complexity of MAP and marginal MAP"
---

MAP inference is the problem of finding a most probable assignment of the unobserved variables of a graphical model, given evidence $e$. There are two problems under this name, and they have different answers and different complexity. The **most probable explanation** (MPE) maximizes $P(x_H, e)$ over all the unobserved variables $H$. **Marginal MAP** (also called partial MAP, or just MAP in parts of the literature) maximizes $P(x_M, e) = \sum_{x_S} P(x_M, x_S, e)$ over a chosen subset $M$, after summing out the rest $S$. MPE is NP-hard (Shimony 1994) and is solved on trees by [max-product](/max-product/). Marginal MAP is NP^PP-complete (Park and Darwiche 2004), and it can be hard even where marginals and MPE are easy.

## In plain words

A model says how likely each full combination of values is. You see some values, and you want the single best guess for the rest.

If you guess every unseen value at once, you want the one full combination that is most likely. That is MPE.

Often you care about only some of the unseen values. Then the best guess for those must count every way the other values could be, not only the best one. That is marginal MAP. A value that is part of the single best combination can lose when all the other ways are counted, so the two guesses can differ.

Both are hard for large general models; marginal MAP is harder.

## Definition

**Input.** Discrete variables $X_1, \ldots, X_n$, factors $\psi_c \ge 0$ that define $P(x) \propto \prod_c \psi_c(x_c)$ (for a [Bayesian network](/bayesian-network/), the conditional tables), and evidence $E = e$. Let $H$ be the unobserved variables.

**MPE.** Output
$$x_H^* \in \arg\max_{x_H} P(x_H, e) = \arg\max_{x_H} \prod_c \psi_c(x_H, e).$$
Dividing by $P(e) > 0$ does not change the maximizer, so this is also $\arg\max P(x_H \mid e)$.

**Marginal MAP.** Given also a partition $H = M \cup S$, output
$$x_M^* \in \arg\max_{x_M} \sum_{x_S} P(x_M, x_S, e).$$
With $S = \emptyset$ it is MPE. With $|M| = 1$ it is the most probable value of one variable, which needs only its [marginal](/marginal-inference/).

**Decision versions.** Given a rational $p$: is there $x_H$ with $P(x_H, e) > p$ (MPE)? Is there $x_M$ with $P(x_M, e) > p$ (marginal MAP)?

**Names.** Shimony (1994) and some of the early literature call the MPE problem MAP. Park and Darwiche (2004) and most later work use MPE for the full assignment and MAP for the subset. This page says MPE and marginal MAP.

## Variants

- **Energy minimization.** With $E(x) = -\sum_c \log \psi_c(x_c)$, MPE is the minimization of $E$. In vision and coding this is the usual form.
- **The $k$ best assignments.** List the $k$ most probable full assignments, not only the first.
- **Max-marginals.** For each variable and value, the largest probability of a full assignment with that value. They come from max-product with a second pass.
- **Posterior marginal decoding.** Pick, for each variable alone, its most probable value. This is not MPE and not marginal MAP over all variables; it maximizes the expected number of correct variables, not the chance that all are correct.
- **Continuous variables.** For Gaussian models MPE is the mean and is found by linear algebra. This page is about discrete models.

## Examples

**MPE and marginal MAP differ.** Let $A$ be binary with $P(A{=}0) = 0.6$, and $B \in \{0, 1, 2\}$ with $P(B \mid A{=}0)$ uniform and $P(B{=}0 \mid A{=}1) = 1$.

| $(a, b)$ | (0, 0) | (0, 1) | (0, 2) | (1, 0) | (1, 1) | (1, 2) |
|---|---|---|---|---|---|---|
| $P(a, b)$ | 0.2 | 0.2 | 0.2 | 0.4 | 0 | 0 |

The MPE is $(A, B) = (1, 0)$, with probability 0.4. Marginal MAP over $M = \{A\}$ compares $P(A{=}0) = 0.6$ with $P(A{=}1) = 0.4$ and returns $A = 0$. So the value of $A$ in the MPE is not the marginal MAP answer for $A$. The value $A = 0$ wins because its probability is spread over three values of $B$.

**Formulas.** For a CNF formula $\varphi$, build the network of [Cooper's theorem](/cooper-theorem/): fair coins for the variables, deterministic nodes for the clauses, and an output $Y$ that is 1 when all clauses are true. With the evidence $Y = 1$, the MPE has probability $2^{-n}$ if $\varphi$ is satisfiable, and its values of the coins are a satisfying assignment; otherwise $P(Y{=}1) = 0$.

## Known algorithms

Exact:

- **Max-product** on a factor tree: linear time, a MAP assignment by backtracking ([max-product](/max-product/)). On a chain it is the [Viterbi algorithm](/viterbi-algorithm/).
- **[Variable elimination](/variable-elimination/)** and the **[junction tree algorithm](/junction-tree-algorithm/)** with max in place of the sum: $O(n\, d^{w+1})$ for an order of induced width $w$, for MPE.
- **Marginal MAP by elimination**: the sum variables must be eliminated before the max variables, so the order is constrained, and the constrained width can be much larger than the treewidth.
- **Search**: [depth-first branch and bound](/depth-first-branch-and-bound/) and best-first search, with bounds from relaxed problems, for MPE and for marginal MAP.
- **Graph cuts**: for binary variables with pairwise factors whose energy is submodular, MPE reduces to a [minimum cut](/min-cut-problem/) and is polynomial, as in [image segmentation](/image-segmentation-graph-cuts/).

Approximate: loopy max-product and max-sum, linear programming relaxations and their duals, local search, and sampling with annealing.

## Bounds

- **MPE is NP-hard** (Shimony 1994). Its decision version is NP-complete: a certificate is the assignment, whose probability is a product of table entries. The formula example gives NP-hardness directly, even when every node has at most three parents.
- **Marginal MAP is NP^PP-complete** (Park and Darwiche 2004). Its decision version guesses $x_M$ (the NP part) and then must compare a sum with $p$ (a PP question).
- **Marginal MAP is hard on easy graphs.** Park and Darwiche show that it remains NP-hard on polytrees, where marginals and MPE take linear time, because the sum variables must be eliminated first.
- **Bounded width.** MPE takes $O(n\, d^{w+1})$ time given an order of width $w$, so it is polynomial for bounded treewidth.
- **Approximation.** With evidence, finding any assignment of positive probability is NP-hard for MPE, by the same reduction: such an assignment is a satisfying assignment. So an approximation within any factor is NP-hard too.

## Reductions

- **From SAT to MPE.** The formula example: $\varphi$ is satisfiable if and only if the MPE given $Y = 1$ has positive probability. With the reduction to 3SAT, each node has at most three parents.
- **From MPE to energy minimization and back.** Logs turn products into sums.
- **From marginal inference to marginal MAP.** With $M = \{X\}$ for one binary variable $X$, a marginal MAP oracle returns the more probable value, so it tells whether $P(X{=}1) \ge 1/2$. For the formula network this asks whether at least half of all assignments satisfy $\varphi$, a PP-complete question.
- **MPE to max-product.** On a factor tree, MPE is exactly what max-product computes; a junction tree reduces general MPE to a tree of cliques.

## Applications

- Decoding of codes and of hidden Markov models: the most likely sent word, or the most likely state sequence.
- Diagnosis: the most likely set of faults that explains the symptoms (MPE), or the most likely state of a few chosen faults (marginal MAP).
- Vision: stereo, segmentation and denoising as energy minimization on grids.
- Structured prediction: the prediction step of a [conditional random field](/conditional-random-field/) is an MPE problem.

## References
