---
tag: M3TQK5
kind: algorithm
slug: basis-pursuit
name: Basis pursuit
aliases:
- L1 minimisation
area: graphics-and-signals/signal-processing
level: advanced
summary: Recovers sparse solutions by minimising the L1 norm subject to linear constraints.
solves: [sparse-signal-recovery]
model: real-ram
complexity:
  vars: {m: the number of measurements, n: the number of unknowns, L: the bit length of the input}
  time: {worst: O(n^3.5 L)}
  space: {extra: Θ(m n)}
properties: {deterministic: true, recursive: false, in_place: false, exact: true}
history:
  year: 1998
  people: [Scott Shaobing Chen, David Donoho, Michael Saunders]
  note: Chen, Donoho and Saunders (1998) proposed the smallest l1 norm of the coefficients as the principle for decomposing a signal in an overcomplete dictionary, and solved it as a linear program.
prereqs: [sparse-signal-recovery, linear-programming-problem]
see_also: [restricted-isometry-property, orthogonal-matching-pursuit, iterative-shrinkage-thresholding, compressed-sensing, lasso-regression, simplex-method, interior-point-method, convex-relaxation]
sources:
  - paper: doi:10.1137/S1064827596304010
    title: Scott Shaobing Chen, David L. Donoho and Michael A. Saunders, Atomic decomposition by basis pursuit, SIAM Journal on Scientific Computing 20(1), 1998
    locator: pages 33 to 61 (the principle, its reduction to a linear program, and its denoising form)
  - paper: doi:10.1073/pnas.0437847100
    title: David L. Donoho and Michael Elad, Optimally sparse representation in general (nonorthogonal) dictionaries via l1 minimization, Proceedings of the National Academy of Sciences 100(5), 2003
    locator: pages 2197 to 2202 (exact recovery by l1 minimization when the sparsity is below (1 + 1/mu)/2)
  - paper: doi:10.1016/j.crma.2008.03.014
    title: Emmanuel J. Candès, The restricted isometry property and its implications for compressed sensing, Comptes Rendus Mathématique 346(9-10), 2008
    locator: pages 589 to 592, Theorem 1.2 (exact recovery when the restricted isometry constant of order 2s is below the square root of 2 minus 1)
  - book: isbn:9780817649470
    title: Simon Foucart and Holger Rauhut, A Mathematical Introduction to Compressive Sensing, Birkhäuser, 2013
    locator: Chapter 4 (basis pursuit and the null space property), Chapter 5 (coherence) and Chapter 15 (algorithms for l1 minimization)
---

Basis pursuit finds a vector $x$ that solves the underdetermined system $Ax = y$ and has the smallest $\ell_1$ norm $\|x\|_1 = \sum_j |x_j|$. The $\ell_1$ norm is the closest convex function to the count of nonzero entries, so this replaces the NP-hard search for the sparsest solution of [sparse signal recovery](/sparse-signal-recovery/) by a [linear program](/linear-programming-problem/) with $2n$ variables. The answer is exactly the sparsest solution if and only if $A$ has the null space property, which holds when the columns are incoherent or when the [restricted isometry constants](/restricted-isometry-property/) are small. The minimizer found by the simplex method has at most $m$ nonzero entries, even when the recovery fails.

## In plain words

You have fewer equations than unknowns, so many answers fit, and you want the one with the fewest nonzero numbers. Checking every choice of nonzero places is far too slow. Instead, look for the answer whose numbers have the smallest total size, counting each number by how far it is from zero. This is a much easier task: a standard method for linear problems with a cost to minimize solves it, step by step, with no guessing.

The smallest total size tends to sit at a corner where many numbers are exactly zero. For many systems, in particular random ones, that corner is the sparsest answer. For others it is not, and you get a different answer that still fits the equations and is still fairly sparse.

## The problem

**Input.** A matrix $A \in \mathbb R^{m \times n}$ with $m < n$ and a vector $y \in \mathbb R^m$. The columns $a_1, \ldots, a_n$ should have norm $1$, or the same norm, because the $\ell_1$ cost weights each column by its scale.

**Output.**

$$(P_1) \qquad \hat x \in \arg\min \{ \|x\|_1 : Ax = y \},$$

or a report that $Ax = y$ has no solution.

**Goal.** For $y = Ax_0$ with $x_0$ $s$-sparse, return $\hat x = x_0$.

**Cost model.** The [real RAM](/real-ram/). With rational $A$ and $y$, the simplex method in exact rational arithmetic returns the exact minimizer.

## The algorithm

Write $x = u - v$ with $u, v \ge 0$. Then $(P_1)$ is the standard form linear program

$$\text{minimize } \mathbf 1^{\mathsf T} u + \mathbf 1^{\mathsf T} v \quad \text{subject to } [\,A \;\; {-A}\,] \begin{pmatrix} u \\ v \end{pmatrix} = y, \quad u, v \ge 0.$$

```pseudo id=main
BASIS-PURSUIT(A, y)                   ▷ A is m × n
L1  M ← [A, −A]                         ▷ m × 2n; the variables are z = (u, v)
L2  c ← the all-ones vector of length 2n
L3  phase 1: find a basic feasible z ≥ 0 with M z = y, or report that A x = y has no solution
L4  phase 2: run the simplex method from z to minimize c · z subject to M z = y, z ≥ 0
L5  return x ← u − v
```

Phase 1 adds an artificial variable to each row (after flipping the sign of rows with $y_i < 0$) and minimizes their sum; the system is feasible exactly when that minimum is $0$. Artificial variables that stay in the basis at the value $0$ are pivoted out, or their rows are dropped as redundant. Phase 2 starts from the resulting basis. Both phases use Bland's rule (the smallest eligible index enters and leaves), which rules out cycling on degenerate vertices. The phase 2 objective is bounded below by $0$, so phase 2 always ends at an optimal vertex. An [interior-point method](/interior-point-method/) can replace lines L3 and L4 and gives a polynomial time bound, but it returns a point near the center of the optimal face rather than a vertex.

## Example

**Recovery.** Let the columns be $e_1, e_2, e_3$ and $w = \tfrac1{11}(6, 6, 7)$, which has norm $1$, and let $x_0 = e_1 + e_2$, so $y = (1, 1, 0)$. Every solution of $Ax = y$ is

$$x(t) = \big(1 - \tfrac6{11}t,\; 1 - \tfrac6{11}t,\; -\tfrac7{11}t,\; t\big),$$

with $\|x(t)\|_1 = 2 + \tfrac6{11}t$ for $0 < t \le \tfrac{11}6$, $2 + \tfrac{30}{11}|t|$ for $t < 0$, and $\tfrac{30}{11}t - 2$ for larger $t$. The unique minimum is at $t = 0$, so basis pursuit returns $x_0$. In the linear program, the optimal vertex is $u = (1, 1, 0, 0)$, $v = 0$, with the value $2$. On this instance [orthogonal matching pursuit](/orthogonal-matching-pursuit/) fails: $|\langle w, y \rangle| = \tfrac{12}{11} > 1 = |\langle e_1, y \rangle|$, so its first step picks the wrong column $w$, and its two-step answer is $(0, 0, -\tfrac76, \tfrac{11}6)$, with $\ell_1$ norm $3$.

**Failure.** The reverse also happens. Let the columns be

$$a_1 = \tfrac19(7, 4, 4), \quad a_2 = \tfrac17(-3, 2, 6), \quad a_3 = \tfrac19(1, 8, 4), \quad a_4 = \tfrac19(8, 1, -4),$$

all of norm $1$, and $x_0 = (2, -1, 0, 0)$. Basis pursuit returns the unique minimizer

$$\hat x = \big(\tfrac{181}{140},\; 0,\; -\tfrac3{28},\; \tfrac{39}{35}\big), \qquad \|\hat x\|_1 = \tfrac{88}{35} < 3 = \|x_0\|_1,$$

which has three nonzero entries, one per row of $A$. Here orthogonal matching pursuit picks $a_1$ and then $a_2$ and returns $x_0$. Neither method is better on every instance.

## Correctness

Three facts make the method correct; the proofs are below.

1. **The linear program is $(P_1)$.** A feasible $x$ gives the feasible point $u = \max(x, 0)$, $v = \max(-x, 0)$ with cost $\|x\|_1$. A feasible $(u, v)$ gives $x = u - v$ with $Ax = y$ and $\|x\|_1 \le \mathbf 1^{\mathsf T}(u + v)$. So the two optimal values are equal, and line L5 maps an optimal $(u, v)$ to a minimizer of $(P_1)$.
2. **The output has at most $m$ nonzero entries.** The simplex method returns a basic solution, with at most $m$ nonzero $z_j$. At an optimum $u_j v_j = 0$, since otherwise lowering both by $\min(u_j, v_j)$ keeps $Mz = y$ and lowers the cost. So $x$ has at most $m$ nonzero entries.
3. **Exact recovery.** Basis pursuit returns $x_0$ as the unique minimizer for every $s$-sparse $x_0$ if and only if $A$ has the null space property of order $s$: $\|v_S\|_1 < \|v_{\bar S}\|_1$ for every nonzero $v$ with $Av = 0$ and every set $S$ of at most $s$ indices. For columns of norm $1$, the coherence condition $\mu < 1/(2s - 1)$ implies the null space property, and so does $\delta_{2s} < \sqrt 2 - 1$ (Candès 2008, Theorem 1.2).

## Complexity

The linear program has $m$ equality constraints and $2n$ variables. Each simplex pivot updates an $m \times (2n + m)$ tableau in $O(mn)$ time. The number of pivots is small in practice, but the simplex method with Bland's rule takes exponentially many pivots on some linear programs. Interior-point methods solve a linear program with $N$ variables and input bit length $L$ in $O(N^{3.5} L)$ arithmetic operations (Karmarkar's bound), which is $O(n^{3.5} L)$ here, and practical primal-dual methods need few iterations, each a linear solve of size $m$. The tableau needs $\Theta(mn)$ space. For large problems, first-order methods on the [lasso](/lasso-regression/) form, such as [iterative shrinkage-thresholding](/iterative-shrinkage-thresholding/), cost $O(mn)$ per iteration and only need products with $A$ and $A^{\mathsf T}$.

## Properties

- **Convex.** $(P_1)$ is a convex problem, so every local minimizer is global, and the set of minimizers is a face of the feasible polyhedron.
- **Not always unique.** The minimizer can be a whole segment. For the four tetrahedron columns $(1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)$, which sum to $0$, the points $(1, 1, 0, 0)$ and $(0, 0, -1, -1)$ have the same measurements and the same $\ell_1$ norm, and so does every point between them.
- **Sparse vertices.** A vertex solution has at most $m$ nonzero entries, whatever $A$ is.
- **Recovery is uniform.** Under the null space property of order $s$, one matrix recovers every $s$-sparse vector, with no knowledge of the support.
- **Guarantee by coherence.** With $\mu$ the mutual coherence, recovery of every $s$-sparse vector holds when $s < \tfrac12(1 + 1/\mu)$, which is the same as $\mu < 1/(2s - 1)$ (Donoho and Elad 2003). For $A = [\,I_{16} \mid \tfrac14 H\,]$ with a $16 \times 16$ Hadamard matrix $H$, $\mu = \tfrac14$, so every $2$-sparse vector in $\mathbb R^{32}$ is recovered from $16$ measurements.
- **Dual certificate.** $x_0$ with support $S$ is a minimizer if there is $w$ with $(A^{\mathsf T} w)_j = \operatorname{sign}(x_{0,j})$ on $S$ and $|(A^{\mathsf T} w)_j| \le 1$ off $S$. This is [strong duality](/strong-duality/) for the linear program.

## Variants and improvements

- **Basis pursuit denoising.** For noisy data, minimize $\|x\|_1$ subject to $\|Ax - y\|_2 \le \varepsilon$. This is a second-order cone program. Under a small $\delta_{2s}$, its error in the $\ell_2$ norm is at most a constant times $\varepsilon$ plus a constant times $\sigma_s(x_0)_1/\sqrt s$, where $\sigma_s(x_0)_1$ is the $\ell_1$ error of the best $s$-term approximation (Candès 2008).
- **The lasso form.** Minimize $\tfrac12\|Ax - y\|_2^2 + \lambda\|x\|_1$. For each $\varepsilon$ there is a $\lambda$ with the same solution, and [iterative shrinkage-thresholding](/iterative-shrinkage-thresholding/) solves this form.
- **The Dantzig selector.** Minimize $\|x\|_1$ subject to $\|A^{\mathsf T}(Ax - y)\|_\infty \le \lambda$, again a linear program.
- **Weighted and reweighted $\ell_1$.** Give each entry a weight, and update the weights from the last solution, so that large entries cost less. This often recovers vectors that plain basis pursuit misses.
- **Homotopy.** Follow the solution of the lasso as $\lambda$ decreases to $0$. Each change of the support is one step, and for very sparse solutions there are few steps.
- **Other norms.** [Total variation denoising](/total-variation-denoising/) puts the $\ell_1$ norm on the gradient of an image instead of on its coefficients.

## When to use it

Use basis pursuit when the data has no noise or very little, when you want a guarantee that holds for every sparse vector, and when the problem is small enough for a linear program solver. It needs no knowledge of the sparsity $s$, unlike [orthogonal matching pursuit](/orthogonal-matching-pursuit/), and it often recovers vectors with more nonzero entries than greedy methods do. For noisy data use the denoising form, and for very large $A$ use a first-order method on the lasso form. When $s$ is very small and speed matters most, a greedy method is cheaper.

## Pitfalls

- **Column scale.** The $\ell_1$ cost prefers columns with large norms, since they reach $y$ with smaller coefficients. Normalize the columns first and rescale the answer.
- **Equality with noise.** With noisy $y$, the constraint $Ax = y$ forces the solution to fit the noise, and the result is not sparse. Use the denoising or lasso form.
- **A minimizer is not the sparsest solution.** When the null space property fails, the output can be a different, denser vector, as in the failure example. Check the residual and the sparsity, or use the theory to choose $m$.
- **Degenerate pivots.** Many sparse problems give degenerate vertices. Without an anti-cycling rule, the simplex method can cycle.
- **Rounding.** In floating point, entries that should be $0$ come out as small numbers. Threshold them, then refit by [least squares](/least-squares-problem/) on the support.

## Implementations

## History

Fits with the smallest sum of absolute values go back to the eighteenth century, and geophysicists used $\ell_1$ objectives to find sparse spike trains in the 1970s and 1980s. Chen, Donoho and Saunders (1998) named basis pursuit, proposed it as a principle for decompositions in overcomplete dictionaries of wavelets and other waveforms, and solved it by interior-point methods. Donoho and Huo (2001) and Donoho and Elad (2003) proved that it finds the sparsest representation when that representation is sparse enough compared with the coherence. Candès, Romberg and Tao (2006), Donoho (2006) and Candès and Tao (2005) showed that it recovers sparse vectors from random measurements, which started [compressed sensing](/compressed-sensing/).

## References
