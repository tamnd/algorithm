---
tag: 63EWRZ
kind: algorithm
slug: gaussian-belief-propagation
name: Gaussian belief propagation
aliases:
- Gaussian BP
- GaBP
- Gaussian loopy belief propagation
area: machine-learning/probabilistic-inference
level: research
summary: "Belief propagation for a Gaussian graphical model in information form. Exact on trees; on graphs with cycles, if it converges the means are exact but the variances are not."
solves: [marginal-inference]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of nonzero off-diagonal pairs of J, d: the largest degree, t: the number of iterations}
  time: {worst: "O(t m d)"}
  space: {extra: "O(n + m)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2001
  people: [Yair Weiss, William T. Freeman, Dmitry M. Malioutov, Jason K. Johnson, Alan S. Willsky]
  note: "Weiss and Freeman (2001) proved that Gaussian BP, when it converges on a graph with cycles, gives the exact means but not the exact variances. Malioutov, Johnson and Willsky (2006) proved that walk-summability is sufficient for convergence."
prereqs: [belief-propagation, gaussian-graphical-model, jacobi-method]
see_also: [gauss-seidel-method, conjugate-gradient-method, loopy-belief-propagation, positive-definite-matrix, spectral-radius, diagonally-dominant-matrix, kalman-filter, rauch-tung-striebel-smoother]
sources:
  - paper: "Yair Weiss and William T. Freeman, Correctness of belief propagation in Gaussian graphical models of arbitrary topology, Neural Computation 13(10), 2001"
    title: Weiss and Freeman 2001
    locator: "the information-form message updates, the result that the means are exact at a fixed point while the variances are not, and convergence for diagonally dominant models"
  - paper: "Dmitry M. Malioutov, Jason K. Johnson and Alan S. Willsky, Walk-sums and belief propagation in Gaussian graphical models, Journal of Machine Learning Research 7, 2006"
    title: Malioutov, Johnson and Willsky 2006
    locator: "walk-summability, the walk-sum interpretation of the means and variances computed by Gaussian BP, and convergence of Gaussian BP for walk-summable models"
---

Gaussian belief propagation (GaBP) is [belief propagation](/belief-propagation/) for a [Gaussian graphical model](/gaussian-graphical-model/). The joint density is $p(x) \propto \exp(-\tfrac12 x^\top J x + h^\top x)$, with a sparse precision matrix $J$. Every message is a Gaussian in one variable, so it is two numbers, and the sum-product integral has a closed form. On a tree, GaBP gives the exact means and variances. On a graph with cycles it may not converge, but Weiss and Freeman proved that if it converges, the means are exact, while the variances are in general wrong. Malioutov, Johnson and Willsky proved that walk-summability of $J$ is sufficient for convergence. Since the mean is the solution of $J x = h$, GaBP is also a distributed iterative solver for linear systems, like the [Jacobi method](/jacobi-method/) and the [Gauss-Seidel method](/gauss-seidel-method/).

## In plain words

Some problems have many quantities that are linked in pairs, each with uncertainty that follows a bell curve. Examples are positions in a sensor network or heights in a smooth surface. We want the best estimate of each quantity and how uncertain it is.

In Gaussian belief propagation, each quantity sends each neighbor a short note of two numbers: what it believes about the neighbor, and how sure it is. It forms the note from its own data and the notes it got from its other neighbors. Notes go back and forth until they stop changing. If the links form a tree, the result is exact. If the links have loops, the notes may never settle. If they do settle, the best estimates are exact, but the reported uncertainties are wrong.

## The problem

**The model.** A Gaussian density in information form,

$$p(x) \propto \exp\big(-\tfrac12 x^\top J x + h^\top x\big),$$

where $J$ is an $n \times n$ symmetric [positive definite](/positive-definite-matrix/) matrix. The mean is $\mu = J^{-1} h$ and the covariance is $J^{-1}$. The graph has an edge between $i$ and $j$ when $J_{ij} \ne 0$; a zero means that $x_i$ and $x_j$ are independent given the other variables.

**The query.** The marginal of each $x_i$, which is the Gaussian with mean $\mu_i$ and variance $(J^{-1})_{ii}$. A dense solve costs $O(n^3)$, and for a sparse $J$ with a large fill-in, even a sparse [Cholesky decomposition](/cholesky-decomposition/) can be too slow or too large.

**Walk-summability.** Scale $J$ to unit diagonal: $\tilde J = D^{-1/2} J D^{-1/2} = I - R$, with $D$ the diagonal of $J$. The matrix $J$ is *walk-summable* if the [spectral radius](/spectral-radius/) of $|R|$, the matrix of absolute values, is below 1. Then $(I - R)^{-1} = \sum_k R^k$ converges absolutely, and every entry of the covariance and the mean is an absolutely convergent sum over walks in the graph. Walk-summable models include the [diagonally dominant](/diagonally-dominant-matrix/) ones and the positive definite models with $R \ge 0$ (attractive models).

## The algorithm

The message from $i$ to $j$ is $\exp(-\tfrac12 P_{ij} x_j^2 + v_{ij} x_j)$, stored as the pair $(P_{ij}, v_{ij})$. The *cavity* values of $i$ without $j$ add the local terms and all incoming messages but the one from $j$:

$$J_{i \setminus j} = J_{ii} + \sum_{k \in N(i) \setminus j} P_{ki}, \qquad h_{i \setminus j} = h_i + \sum_{k \in N(i) \setminus j} v_{ki}.$$

Integrating $x_i$ out of $\exp(-\tfrac12 J_{i \setminus j} x_i^2 + h_{i \setminus j} x_i - J_{ij} x_i x_j)$ gives the new message

$$P_{ij} = -\frac{J_{ij}^2}{J_{i \setminus j}}, \qquad v_{ij} = -\frac{J_{ij}\, h_{i \setminus j}}{J_{i \setminus j}}.$$

The integral exists only if $J_{i \setminus j} > 0$.

```pseudo id=main
GaBP(J, h, ε, T)
L1  P_ij ← 0, v_ij ← 0, for every ordered pair with J_ij ≠ 0
L2  for iteration t ← 1 to T do
L3      for every ordered pair (i, j): J_{i\j} ← J_ii + Σ_{k ∈ N(i), k ≠ j} P_ki; h_{i\j} ← h_i + Σ_{k ∈ N(i), k ≠ j} v_ki (if J_{i\j} ≤ 0, stop: failed)
L4          P'_ij ← −J_ij² / J_{i\j}; v'_ij ← −J_ij h_{i\j} / J_{i\j}
L5      δ ← the largest change of a message; P ← P', v ← v'
L6      if δ < ε then break
L7  for each i: Ĵ_i ← J_ii + Σ_{k ∈ N(i)} P_ki; ĥ_i ← h_i + Σ_{k ∈ N(i)} v_ki
L8  return the means μ_i = ĥ_i / Ĵ_i and the variances σ_i² = 1 / Ĵ_i
```

The precision messages $P$ do not depend on $h$ or on $v$, so they converge or fail on their own. The schedule above is synchronous, which is like the Jacobi method; a sequential schedule that uses the newest messages is like the Gauss-Seidel method.

## Example

Take the $3 \times 3$ grid with $J_{ii} = 1$, $J_{ij} = -0.2$ on the 12 grid edges, and $h = (0.5, -0.2, 0.3, 0, 1, -0.4, 0.2, 0.1, -0.3)$, with the variables numbered row by row. Then $R \ge 0$, and its spectral radius is $0.2 \cdot 2\sqrt2 = 0.566$, so the model is walk-summable. GaBP converges in 28 iterations (largest change below $10^{-12}$).

The means agree with $J^{-1} h$ (from exact elimination) to $10^{-10}$: $\mu = (0.6309, 0.2230, 0.3136, 0.4317, 1.1706, -0.1552, 0.3570, 0.3535, -0.2604)$. The variances do not:

| variable | 0 (corner) | 1 (edge) | 4 (center) |
|---|---|---|---|
| exact $(J^{-1})_{ii}$ | 1.1023 | 1.1611 | 1.2353 |
| GaBP $1 / \hat J_i$ | 1.0961 | 1.1490 | 1.2115 |

All GaBP variances here are too small. The walk-sum view explains this: the variance of $x_i$ is the sum of the weights of all walks from $i$ back to $i$, and GaBP adds up only a subset of them (Malioutov, Johnson and Willsky 2006). With $R \ge 0$ every walk has a positive weight, so the subset gives less.

A model that is positive definite but not walk-summable can make GaBP fail. On the complete graph $K_4$ with $J_{ii} = 1$ and $J_{ij} = r$, the eigenvalues are $1 + 3r$ and $1 - r$, so $J$ is positive definite for $0 < r < 1$, and $\rho(|R|) = 3r$. By symmetry all precision messages are equal and satisfy $P = -r^2 / (1 + 2P)$, that is $2P^2 + P + r^2 = 0$, which has a real root only if $r^2 \le 1/8$. For $r = 0.3$ ($\rho(|R|) = 0.9$), GaBP converges to the exact means. For $r = 0.35$ the precisions converge but the means grow without bound, and for $r \ge 0.36$ the cavity precision becomes negative after a few iterations.

## Correctness

- **The update.** The message rule is the sum-product rule: the integral of a Gaussian in $x_i$ times $\exp(-J_{ij} x_i x_j)$ is a Gaussian in $x_j$ with the given $P_{ij}$ and $v_{ij}$.
- **Trees.** On a tree, the synchronous iteration stops changing after at most $D + 1$ iterations, where $D$ is the diameter, and the means and variances are exact, as for belief propagation.
- **Means at any fixed point (Weiss and Freeman).** If the messages are at a fixed point with positive cavity precisions, then $\mu = \hat h / \hat J$ solves $J \mu = h$. The proof uses only the fixed-point equations of one edge and a sum over the neighbors of each node.
- **Variances.** They are not exact in general on a graph with cycles, as the example shows.
- **Convergence.** Not guaranteed for a general positive definite $J$. Weiss and Freeman proved convergence for diagonally dominant $J$, and Malioutov, Johnson and Willsky for walk-summable $J$, which includes the diagonally dominant case.

The proofs of the first three points are in the correctness proof.

## Complexity

The costs are in the [real RAM](/real-ram/) model.

- **One message.** $O(d)$ to form the cavity sums, $O(1)$ for the update.
- **One iteration.** $2m$ messages: $O(m d)$. If each node first adds all its incoming messages and then subtracts the one from $j$, it is $O(n + m)$.
- **Iterations.** For a tree, at most $D + 1$. For a walk-summable model, the error falls roughly geometrically; the rate depends on the model.
- **Memory.** Two numbers per directed edge, $O(n + m)$.

For a sparse $J$, an iteration costs as much as one product of $J$ with a vector, the same as one step of the Jacobi method or of the [conjugate gradient method](/conjugate-gradient-method/).

## Properties

- **Exact on trees.** Means and variances.
- **Exact means at any fixed point.** Even on graphs with cycles.
- **Wrong variances on graphs with cycles.** Too small in attractive walk-summable models.
- **The precisions do not depend on $h$.** One run of the precision messages serves all right-hand sides.
- **Distributed.** Each node uses only its own row of $J$ and the messages of its neighbors.

## Variants and improvements

- **A linear solver.** GaBP solves $J x = h$ for a symmetric positive definite $J$; the mean messages alone can be run with fixed precisions.
- **Damping.** Mixing the new message with the old one can help on models near the edge of convergence.
- **Kalman smoothing.** On the chain of a linear Gaussian state space model, GaBP gives the same marginals as the [Kalman filter](/kalman-filter/) followed by the [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/).
- **Multivariate messages.** With vector variables, the messages are Gaussians in several dimensions, and the divisions become small matrix inversions.

## When to use it

Use GaBP for marginal means in a large sparse Gaussian model, when the model is walk-summable or diagonally dominant, and when a distributed method is useful, as in sensor networks. If you need the variances, use it only on trees, or use a method with exact variances. For a general symmetric positive definite system on one machine, the conjugate gradient method has a convergence guarantee that GaBP does not have.

## Pitfalls

- **Positive definite is not enough.** On $K_4$ with $J_{ij} = 0.4$, $J$ is positive definite but GaBP fails. Check walk-summability or diagonal dominance first.
- **Reading the variances as exact.** On a graph with cycles they are approximations, even when the means are exact.
- **Negative cavity precision.** Then the integral does not exist; the run must stop and report failure.
- **The precision loop converges but the means diverge.** On $K_4$ with $r = 0.35$, the precisions converge and the means grow without bound. Check the change of the $v$ messages as well.

## Implementations

## History

Belief propagation for Gaussian models on trees is as old as belief propagation, and on chains it is Kalman smoothing. Weiss and Freeman studied it on graphs with cycles in a paper published in Neural Computation in 2001 and proved that a fixed point gives the exact means, while the variances are in general wrong, and that diagonally dominant models converge. Malioutov, Johnson and Willsky (2006) expanded the covariance as a sum over walks in the graph, called $J$ walk-summable when these sums converge absolutely, and proved that GaBP converges for every walk-summable model, with means that sum all walks and variances that sum only part of them.

## References
