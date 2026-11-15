---
tag: P106V2
kind: algorithm
slug: iterative-rational-krylov
name: Iterative rational Krylov algorithm
aliases:
- IRKA
area: control/state-space-control
level: research
summary: "Finds a reduced model that meets the H2 optimality conditions by interpolating at the mirrored poles of the current reduced model, repeated to a fixed point."
solves: [model-order-reduction]
model: floating-point-model
complexity:
  vars: {n: the number of states, r: the reduced order, k: the number of iterations}
  time: {worst: "O(k r n^3)"}
  space: {extra: "O(n^2 + n r)"}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 2008
  people: [Serkan Gugercin, Athanasios C. Antoulas, Christopher Beattie]
  note: "Gugercin, Antoulas and Beattie proposed the iteration in 2008; the interpolation conditions for H2 optimality go back to Meier and Luenberger in 1967."
prereqs: [model-order-reduction, krylov-subspace, hermite-interpolation]
see_also: [balanced-truncation, h2-norm, arnoldi-iteration, lanczos-algorithm, pade-approximation, rational-approximation, fixed-point-iteration, newton-raphson-method]
sources:
  - paper: doi:10.1137/060666123
    title: S. Gugercin, A. C. Antoulas and C. Beattie, H2 model reduction for large-scale linear dynamical systems, SIAM Journal on Matrix Analysis and Applications 30(2), 609-638, 2008
    locator: the interpolation conditions for H2 optimality and the iterative rational Krylov algorithm
  - paper: doi:10.1109/TAC.1967.1098680
    title: L. Meier and D. G. Luenberger, Approximation of linear constant systems, IEEE Transactions on Automatic Control 12(5), 585-588, 1967
    locator: the first-order necessary conditions for an H2 optimal approximation, as interpolation of G and G' at the mirrored reduced poles
  - paper: doi:10.1016/j.sysconle.2012.03.005
    title: G. Flagg, C. Beattie and S. Gugercin, Convergence of the iterative rational Krylov algorithm, Systems and Control Letters 61(6), 688-691, 2012
    locator: the local convergence of the iteration for state-space-symmetric systems
---

The iterative rational Krylov algorithm, IRKA, makes a small model of a large linear system that is close in the $H_2$ norm, the root of the energy of the error impulse response (see [H2 norm](/h2-norm/)). It needs only solves with matrices $sI - A$, so it applies to systems with very many states, where the Gramians of [balanced truncation](/balanced-truncation/) are too costly. The idea is interpolation. A projection onto a [Krylov subspace](/krylov-subspace/) built from the vectors $(s_i I - A)^{-1} b$ gives a reduced model that matches the transfer function $G$ and its derivative at the chosen points $s_i$, as in [Hermite interpolation](/hermite-interpolation/). Meier and Luenberger (1967) showed that an $H_2$ optimal model of order $r$ must match $G$ and $G'$ at the mirror images $-\lambda_i$ of its own poles. IRKA, proposed by Gugercin, Antoulas and Beattie (2008), turns this condition into a [fixed-point iteration](/fixed-point-iteration/): interpolate at the current points, compute the poles of the new model, mirror them, and repeat. A fixed point satisfies the first-order conditions for a local minimum of the $H_2$ error. The iteration usually converges in tens of steps, but there is no general proof that it converges.

## In plain words

A large model can be summarized by how it responds at a few chosen test frequencies. One can build a small model that copies the large model exactly at those test frequencies, both the value and its slope. The question is which test frequencies to choose. The best small model, measured by the total energy of the error, has a property that helps: its test frequencies are the mirror images of its own natural frequencies. So the method guesses test frequencies, builds the small model, reads off its natural frequencies, mirrors them to get new test frequencies, and repeats. When the test frequencies stop moving, the small model has the property that the best one must have.

## The problem

Input: $A \in \mathbb{R}^{n \times n}$ Hurwitz, $b \in \mathbb{R}^n$, $c \in \mathbb{R}^{1 \times n}$, an order $r \le n$, initial shifts $s_1, \dots, s_r$ in the open right half plane and closed under conjugation, a tolerance and a maximum number of iterations. The system is $G(s) = c(sI - A)^{-1}b$, with one input and one output. Output: $A_r \in \mathbb{R}^{r \times r}$, $b_r$, $c_r$ with $G_r(s) = c_r(sI - A_r)^{-1}b_r$, the final shifts, the number of iterations and a flag that says whether the shifts converged. On convergence, with $\lambda_i$ the eigenvalues of $A_r$,

$$G_r(-\lambda_i) = G(-\lambda_i), \qquad G_r'(-\lambda_i) = G'(-\lambda_i), \qquad i = 1, \dots, r,$$

which are the necessary conditions for a local minimum of $\|G - G_r\|_{H_2}$ over real models of order $r$ with simple poles.

## The algorithm

```pseudo id=main
IRKA(A, b, c, r, s, tol, maxiter)
L1  s ← initial shifts s_1, ..., s_r, closed under conjugation, Re s_i > 0
L2  for it = 1 to maxiter do
L3      V ← basis of span{(s_i I - A)⁻¹ b};  W ← basis of span{(s_i I - Aᵀ)⁻¹ cᵀ}
L4      A_r ← (WᵀV)⁻¹ WᵀAV;  b_r ← (WᵀV)⁻¹ Wᵀb;  c_r ← cV
L5      s_new ← sorted −eig(A_r);  δ ← max_i |s_new,i − s_i| / |s_i|;  s ← s_new
L6      if δ < tol then
L7          return (A_r, b_r, c_r, s, it, converged)
L8  return (A_r, b_r, c_r, s, maxiter, not converged)
```

Line L1 takes the given shifts, or by default $r$ real shifts spread geometrically between $1/\|A^{-1}\|_\infty$ and $\|A\|_\infty$, which bound the moduli of the eigenvalues of $A$ from below and above. Line L3 solves $2r$ linear systems, one with $s_i I - A$ and one with $s_i I - A^T$ for each shift. For a conjugate pair only one complex solve per side is needed: its real and imaginary parts span the same space as the pair, so the basis and the reduced matrices are real. The implementation orthonormalizes both bases by Gram-Schmidt, done twice; this keeps the column spaces and so the reduced model. Line L4 is the Petrov-Galerkin projection, a two-sided oblique projection. Line L5 takes the eigenvalues of the small matrix $A_r$, mirrors them, sorts them, and measures how far they moved. Lines L6 and L7 stop at a fixed point, and line L8 reports a run that did not converge.

## Example

**The chain of four sections.** $G(s) = 1/((s+1)(s+2)(s+3)(s+4))$, realized with $A$ upper bidiagonal, $b = e_4$ and $c = e_1^T$, has $\|G\|_{H_2} = 0.0222718$. For $r = 2$ the default shifts are $0.58537$ and $4$. The table lists the shifts after $k$ updates and the $H_2$ error of the model projected at those shifts (measurements; the error is computed from the Gramian of the error system).

| $k$ | shifts | $\|G - G_r\|_{H_2}$ |
| --- | --- | --- |
| 0 | $0.58537$, $4$ | 0.0103772 |
| 1 | $0.25429 \pm 0.70058i$ | 0.00344639 |
| 2 | $0.86729 \pm 0.48197i$ | 0.00292236 |
| 3 | $0.63707 \pm 0.61264i$ | 0.0028312 |
| 4 | $0.72113 \pm 0.57036i$ | 0.0028203 |
| 6 | $0.70178 \pm 0.58019i$ | 0.0028186 |
| 10 | $0.69886 \pm 0.58167i$ | 0.00281857 |
| 25 | $0.69881 \pm 0.58170i$ | 0.00281857 |

The run stops after 25 iterations, with the reduced poles $-0.69881 \mp 0.58170i$, whose mirror images are the shifts. The error falls fast in the first steps, and the shifts then spiral into the fixed point at a linear rate. The final $H_2$ error is $0.00281857$, against $0.0028737$ for balanced truncation of the same order, and the $H_\infty$ error is $0.0020534$, against $0.0021479$ (measurements). For $r = 1$ the run takes 70 iterations and ends at the shift $0.28514$ with $H_2$ error $0.012742$; a brute-force search over all models $\phi/(s + \lambda)$ gives the same shift. For $r = 3$ it takes 13 iterations, ends at the shifts $0.87940$ and $1.65866 \pm 1.05175i$, and has $H_2$ error $0.00022340$. The [model order reduction](/model-order-reduction/) page compares both methods for each $r$.

## Correctness

The full proof is in proofs/correctness.md. Its steps are theorems:

1. **Projection.** With $M(s) = W^T(sI - A)V$, the reduced transfer function is $G_r(s) = cV M(s)^{-1} W^T b$. It depends only on the column spaces of $V$ and $W$, so the real basis and the orthonormalization of line L3 do not change it.
2. **Hermite interpolation.** For every shift with $M(s_i)$ invertible, $G_r(s_i) = G(s_i)$ and $G_r'(s_i) = G'(s_i)$. This holds after every pass of line L4, not only at the end.
3. **The $H_2$ inner product by residues.** For $H(s) = \sum_k \psi_k/(s - \mu_k)$ with poles in the open left half plane, $\langle G, H \rangle_{H_2} = \sum_k \psi_k G(-\mu_k)$.
4. **Meier and Luenberger conditions.** For $G_r$ with simple poles $\lambda_i$ and residues $\phi_i$, the partial derivatives of $J = \|G - G_r\|_{H_2}^2$ are $-2(G(-\lambda_i) - G_r(-\lambda_i))$ in $\phi_i$ and $2\phi_i(G'(-\lambda_i) - G_r'(-\lambda_i))$ in $\lambda_i$. So the gradient is zero if the interpolation conditions hold, and only then when every $\phi_i \ne 0$.
5. **Fixed points.** If the iteration reaches $s_i = -\lambda_i(A_r)$ with simple eigenvalues in the open left half plane and $W^T V$ invertible, then steps 2 and 4 show that $G_r$ is a stationary point of the $H_2$ error.

The tests check the interpolation at random shifts on 500 random projections, the equality of the real and complex bases, the conditions of step 5 on converged runs, the $r = 1$ result against a brute-force search, the chain example, that small perturbations of the converged model do not lower the error, and that $r = n$ reproduces $G$.

## Complexity

Each pass costs:

- Line L3: $2r$ linear solves of size $n$, which is $O(r n^3)$ with dense Gaussian elimination, as in the implementation, and much less with sparse factorizations, depending on the sparsity pattern. Conjugate pairs halve the count. The Gram-Schmidt step costs $O(n r^2)$.
- Line L4: $O(n^2 r)$ for $W^T A V$ with dense $A$, or $O(\text{nnz}(A)\, r)$ with sparse $A$, and $O(r^3)$ for the small solve.
- Line L5: $O(r^3)$ for the eigenvalues of $A_r$.

So $k$ passes cost $O(k r n^3)$ with dense matrices, and the extra space is $O(n^2 + nr)$ for one factorization and the two bases. The count $k$ is not bounded in advance, and the code stops at `maxiter`. Compared with balanced truncation, which needs $O(n^3)$ work for two Lyapunov equations and dense storage, IRKA needs only solves, so the sparse cost is what matters for large models.

**Rounding.** In the [floating-point model](/floating-point-model/), each solve of line L3 by Gaussian elimination with partial pivoting is backward stable in the infinity norm in practice (a rule of thumb; the growth factor is usually small). The basis vectors for nearby shifts are nearly parallel, which is why the bases are orthonormalized: the projection uses the subspaces, not the vectors. The eigenvalues of $A_r$ in line L5 are sensitive when $A_r$ is far from normal, and this limits how small `tol` can usefully be.

## Properties

- **Interpolation at every pass** (a theorem): the model of each pass matches $G$ and $G'$ at its shifts.
- **Stationary at a fixed point** (a theorem): a converged model with simple poles satisfies the Meier and Luenberger conditions. It is a local, not a global, optimum in general.
- **Convergence is not guaranteed.** Flagg, Beattie and Gugercin (2012) proved local convergence for state-space-symmetric systems, $A = A^T$ and $b = c^T$ (a theorem). For general systems the iteration usually converges in tens of passes (a rule of thumb), but it can cycle or diverge.
- **Asymptotic stability is not guaranteed** for the intermediate models; a pass can return an $A_r$ with an eigenvalue in the right half plane. Converged models of asymptotically stable systems are usually asymptotically stable in practice (a rule of thumb).
- **No a priori error bound.** Unlike balanced truncation, the error is known only after the model is computed.
- **Linear rate.** On the chain example the shifts approach the fixed point at a linear rate, with a spiral in the complex plane (a measurement).
- **Deterministic.** For fixed initial shifts the result is fixed, but different initial shifts can lead to different local optima.

## Variants and improvements

- **Several inputs and outputs.** The MIMO version uses tangential interpolation: each shift comes with a right direction and a left direction, which are updated from the eigenvectors of $A_r$ and the residues of $G_r$.
- **One-sided projection.** For a state-space-symmetric system, $W = V$ gives the same conditions with half the solves.
- **Data-driven IRKA.** The steps need only values of $G$ and $G'$ at the shifts, so the reduced model can be built from measurements of the transfer function, without $A$, by a Loewner matrix construction.
- **Rational Krylov at fixed points.** Without the iteration, one projection at chosen shifts is moment matching. With one shift at infinity it gives the [Padé approximation](/pade-approximation/) computed by the [Lanczos algorithm](/lanczos-algorithm/) or the [Arnoldi iteration](/arnoldi-iteration/).
- **Safer shifts.** Reflect a shift that falls into the left half plane back to the right half plane, or start from the mirrored poles of a balanced truncation model. Both are rules of thumb.
- **Faster convergence.** Treat the fixed-point equation as a nonlinear system and apply the [Newton-Raphson method](/newton-raphson-method/) or a trust-region method to the $H_2$ error.
- **Descriptor and discrete-time systems.** Use $sE - A$ in the solves, or the unit disk version of the conditions, where the mirror of a pole $\lambda$ is $1/\lambda$.

## When to use it

Use IRKA when the model is large and sparse, when solves with $sI - A$ are affordable but dense Gramians are not, and when the $H_2$ error matters, for example the energy of the impulse response error. Also use it for a medium-sized model when balanced truncation is not accurate enough and a local optimum in the $H_2$ norm is wanted. Start from shifts spread over the spectrum, or from the mirrored poles of a balanced truncation model. Check the converged flag, and check the error after the run, since no bound is known in advance. Use [balanced truncation](/balanced-truncation/) instead when a guaranteed $H_\infty$ error bound or guaranteed asymptotic stability is needed.

## Pitfalls

- **Line L1 with a set of shifts that is not closed under conjugation.** Then the reduced model is complex. The implementation raises an error. Give conjugate pairs together.
- **Line L1 with poor shifts.** Shifts far from the spectrum of $A$ give slow convergence: for the chain with $r = 1$ the default shift needs 70 passes. Spread the shifts over the scale of the eigenvalues of $A$.
- **Line L3 with nearly equal shifts.** The columns $(s_i I - A)^{-1} b$ are then nearly parallel, and a basis without orthonormalization is ill conditioned. The implementation orthonormalizes, and it raises an error if a column is lost.
- **Line L4 with $W^T V$ singular.** Then the Petrov-Galerkin model does not exist. This happens rarely, for special shifts; change the shifts.
- **Line L5 with an eigenvalue of $A_r$ in the right half plane.** Its mirror image is a shift in the left half plane, perhaps near an eigenvalue of $A$, and the next solve is ill conditioned. The implementation does not check this. Reflect such shifts into the right half plane.
- **Line L6 with shifts that are not matched.** The change must compare each new shift with the corresponding old one. The implementation sorts both lists the same way before the comparison. Without the sort, a reordering looks like a large change.
- **Line L8 ignored.** A run that hits `maxiter` returns the last model, which need not satisfy any optimality condition. Check the flag.

## Implementations

## History

Meier and Luenberger (1967) derived the first-order conditions for the $H_2$ optimal approximation of a system with one input and one output: the reduced model must interpolate $G$ and $G'$ at the mirror images of its poles. Many methods for $H_2$ optimal reduction followed, most based on Lyapunov or Sylvester equations. Gugercin, Antoulas and Beattie (2008) reformulated the conditions as interpolation by a rational Krylov projection and proposed the fixed-point iteration, which needs only linear solves and so applies to large systems. Flagg, Beattie and Gugercin (2012) proved local convergence for state-space-symmetric systems.

## References
