---
tag: 67E45Z
kind: problem
slug: model-order-reduction
name: Model order reduction
aliases:
- model reduction
- MOR
area: control/state-space-control
level: core
summary: "Given a linear system with many states, find one with far fewer states whose input-output behavior is close to it in a stated norm, such as the H-infinity or H2 norm."
prereqs: [linear-time-invariant-system, state-space-representation, transfer-function]
see_also: [balanced-truncation, iterative-rational-krylov, hankel-singular-values, balanced-truncation-error-bound, balanced-realization, singular-perturbation-method, krylov-subspace, pade-approximation]
sources:
  - book: isbn:9780898715293
    title: Athanasios C. Antoulas, Approximation of Large-Scale Dynamical Systems, SIAM, 2005
    locator: Chapter 7, Balancing and balanced approximations; the later chapters on Krylov and moment matching methods
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 7, Model Reduction by Balanced Truncation; Chapter 8, Hankel Norm Approximation
  - paper: doi:10.1109/TAC.1981.1102568
    title: B. C. Moore, Principal component analysis in linear systems, controllability, observability, and model reduction, IEEE Transactions on Automatic Control 26(1), 17-32, 1981
    locator: balanced realizations and the truncation of weakly controllable and weakly observable states
  - paper: doi:10.1080/00207178408933239
    title: Keith Glover, All optimal Hankel-norm approximations of linear multivariable systems and their L-infinity error bounds, International Journal of Control 39(6), 1115-1193, 1984
    locator: the optimal Hankel-norm approximation, the lower bound by the Hankel singular values, and the L-infinity error bounds
  - paper: doi:10.1137/060666123
    title: S. Gugercin, A. C. Antoulas and C. Beattie, H2 model reduction for large-scale linear dynamical systems, SIAM Journal on Matrix Analysis and Applications 30(2), 609-638, 2008
    locator: the interpolation conditions for H2 optimality and the iterative rational Krylov algorithm
---

Model order reduction (MOR) replaces a large model of a dynamical system by a small one that gives almost the same outputs for the same inputs. Large linear models appear when a physical system is described in fine detail: a finite element model of a bridge, a circuit model of the wires on a chip, or a discretized heat or fluid equation can have $10^4$ to $10^7$ state variables, far too many to simulate many times or to design a controller for. A reduced model with $r$ states, often $r$ between 5 and 100, can be simulated and analysed quickly. The question is how to choose it so that the error in the outputs is small and, where possible, provably small. For linear time-invariant systems the error is measured by a norm of the difference of the [transfer functions](/transfer-function/), usually the $H_\infty$ norm (the worst gain over all frequencies) or the $H_2$ norm (the energy of the impulse response error). The main methods are [balanced truncation](/balanced-truncation/), which has an a priori error bound in terms of the [Hankel singular values](/hankel-singular-values/), and interpolation methods such as the [iterative rational Krylov algorithm](/iterative-rational-krylov/), which scale to very large sparse models. Every asymptotically stable model of order $r$ has an $H_\infty$ error of at least the $(r+1)$th Hankel singular value, so these values also say how far any reduction can go.

## In plain words

A detailed computer model of a machine can have millions of numbers in its state, because it describes every small piece. But the engineer only cares about a few inputs, such as forces or voltages, and a few outputs, such as a position or a current. Most of the internal detail has almost no effect on what goes from those inputs to those outputs. Model reduction finds a much smaller model that has nearly the same effect from the inputs to the outputs. A good method also says how large the error can be, for every input. The small model is then used for fast simulation, for control design, or inside an optimization that must run the model many times.

## Definition

**Data.** A [linear time-invariant system](/linear-time-invariant-system/) in [state-space form](/state-space-representation/)

$$\dot x = A x + B u, \qquad y = C x + D u, \qquad A \in \mathbb{R}^{n \times n},\ B \in \mathbb{R}^{n \times m},\ C \in \mathbb{R}^{p \times n},$$

with transfer function $G(s) = C (sI - A)^{-1} B + D$, usually with $A$ [Hurwitz](/hurwitz-matrix/), and a target order $r < n$.

**Problem.** Find $A_r \in \mathbb{R}^{r \times r}$, $B_r$, $C_r$ and $D_r$ such that $G_r(s) = C_r (sI - A_r)^{-1} B_r + D_r$ is close to $G$ in a stated norm, and such that $G_r$ keeps the properties that matter, above all that $A_r$ is Hurwitz. The usual norms are

- the [H-infinity norm](/h-infinity-norm/) $\|G - G_r\|_\infty = \sup_\omega \sigma_{\max}(G(i\omega) - G_r(i\omega))$, the worst ratio of output error energy to input energy;
- the [H2 norm](/h2-norm/) $\|G - G_r\|_{H_2} = \left(\frac{1}{2\pi}\int_{-\infty}^{\infty} \|G(i\omega) - G_r(i\omega)\|_F^2\, d\omega\right)^{1/2}$, the energy of the impulse response error, and the worst peak output error for unit energy inputs of a system with one output;
- the Hankel norm $\|G - G_r\|_H$, the gain from past inputs to future outputs, which equals the largest Hankel singular value of $G - G_r$.

**Optimal versions.** For a fixed norm and order, minimize the error over all asymptotically stable $G_r$ of order $r$. For the Hankel norm the problem is solved exactly (Glover 1984). For the $H_2$ norm it is a nonconvex smooth problem with known first-order conditions. For the $H_\infty$ norm no finite algorithm for the optimum is known; the methods used give bounds, not the optimum.

## Variants

- **Projection methods.** Most methods choose $V, W \in \mathbb{R}^{n \times r}$ with $W^T V = I$ and set $A_r = W^T A V$, $B_r = W^T B$, $C_r = C V$, $D_r = D$. Balanced truncation and Krylov methods are of this kind; only the choice of $V$ and $W$ differs.
- **Structure-preserving reduction.** Second-order systems $M \ddot q + D \dot q + K q = F u$ from mechanics, port-Hamiltonian systems, and passive circuits need reduced models with the same structure, so that the reduced model is again passive or again mechanical.
- **Frequency-weighted reduction.** Minimize $\|W_o (G - G_r) W_i\|$ for weights that stress a frequency band. Enns (1984) gave a frequency-weighted version of balanced truncation. It is used for controller reduction, where the error that matters is the closed-loop error.
- **Unstable systems.** Keep the unstable part exactly and reduce the asymptotically stable part, or reduce a coprime factorization (see [coprime factorization](/coprime-factorization/)).
- **Parametric and nonlinear reduction.** For models with parameters, or nonlinear models, projection bases are built from samples. Proper orthogonal decomposition takes the bases from the [singular value decomposition](/singular-value-decomposition/) of a matrix of simulated states, the same computation as [principal component analysis](/principal-component-analysis/). [Dynamic mode decomposition](/dynamic-mode-decomposition/) fits a small linear model to data.
- **Discrete time.** The same problem for $x_{k+1} = A x_k + B u_k$, with $A$ Schur stable and the norms on the unit circle.

## Examples

- **First order to order 0.** $G(s) = 1/(s + 1)$ has one Hankel singular value $\sigma_1 = 1/2$. The best constant approximation in the $H_\infty$ norm is $G_0 = 1/2$, with $|G(i\omega) - 1/2| = \tfrac{1}{2}|1 - i\omega| / |1 + i\omega| = 1/2$ for every $\omega$: the lower bound $\sigma_1$ is attained. Balanced truncation to order 0 gives $G_0 = D = 0$ and the error $1 = 2\sigma_1$, which is its upper bound. This shows the factor 2 between the two bounds.
- **A chain of four first-order sections.** $G(s) = 1/((s+1)(s+2)(s+3)(s+4))$ has Hankel singular values $0.027988$, $0.0082179$, $0.0011269$ and $0.0000632855$. The table compares balanced truncation (BT) and IRKA, both computed by the implementations of their pages; the $H_\infty$ errors are maxima over a grid of about 1200 frequencies (a measurement).

| $r$ | lower bound $\sigma_{r+1}$ | BT error, $H_\infty$ | BT bound $2\sum_{k > r}\sigma_k$ | IRKA error, $H_\infty$ | BT error, $H_2$ | IRKA error, $H_2$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.0082179 | 0.014601 | 0.018816 | 0.014429 | 0.013113 | 0.012742 |
| 2 | 0.0011269 | 0.0021479 | 0.0023804 | 0.0020534 | 0.0028737 | 0.0028186 |
| 3 | 0.0000632855 | 0.00012657 | 0.00012657 | 0.00011394 | 0.00022450 | 0.00022340 |

The $H_\infty$ norm of $G$ is $1/24 = 0.041667$ and its $H_2$ norm is $0.0222718$, so a model with two states already has a relative $H_\infty$ error of about 5 percent. Every $H_\infty$ error lies between the lower bound and the BT bound, as the two theorems below require. IRKA, which targets the $H_2$ norm, has the smaller $H_2$ error, as it should; on this system it also has the smaller $H_\infty$ error, which is a measurement, not a rule.
- **No good reduction.** If all Hankel singular values are equal, the lower bound $\sigma_{r+1} = \sigma_1$ and the upper bound $\|G - D\|_\infty \le 2\sigma_1$ show that no model of lower order is better than the constant $G_r = D$ by more than a factor 2. This happens for a delay approximated by an all-pass Padé model (see [Padé approximation](/pade-approximation/)): a delay has no small accurate model.

## Known algorithms

- **[Balanced truncation](/balanced-truncation/)** (Moore 1981). Solve two [Lyapunov equations](/lyapunov-equation/) for the Gramians, change to the [balanced realization](/balanced-realization/), and drop the states with small Hankel singular values. $G_r$ is asymptotically stable when $\sigma_r > \sigma_{r+1}$, and the [error bound](/balanced-truncation-error-bound/) is $\|G - G_r\|_\infty \le 2 \sum$ of the distinct dropped values. Dense cost $O(n^3)$.
- **Balanced singular perturbation approximation.** In the balanced coordinates, set the derivative of the small states to zero instead of the states themselves (see [singular perturbation method](/singular-perturbation-method/)). It matches the gain at $s = 0$ exactly instead of at $s = \infty$, and it has the same error bound.
- **Optimal Hankel-norm approximation** (Glover 1984). It reaches the smallest possible Hankel norm error $\sigma_{r+1}$, and with a suitable constant term it has an $H_\infty$ error of at most the sum of the distinct tail values, half the bound of balanced truncation.
- **[Iterative rational Krylov algorithm](/iterative-rational-krylov/)** (Gugercin, Antoulas and Beattie 2008). It meets the first-order conditions of $H_2$ optimality by interpolation at mirrored reduced poles. It needs only solves with $sI - A$, so it works for sparse $A$ with millions of states. It has no a priori error bound.
- **Moment matching.** Match the Taylor coefficients of $G$ at one or more points with bases from a [Krylov subspace](/krylov-subspace/), computed by the [Arnoldi iteration](/arnoldi-iteration/) or the [Lanczos algorithm](/lanczos-algorithm/). At $s = \infty$ this matches the [Markov parameters](/markov-parameters/); the one-point version gives a [Padé approximation](/pade-approximation/) of $G$. Cheap, but neither asymptotic stability nor the error is guaranteed.
- **Modal truncation.** Keep the eigenvalues of $A$ nearest the imaginary axis, or those with the largest residues. It keeps asymptotic stability, but its error depends on the residues, and it can miss important states for non-normal $A$.
- **Low-rank Gramian methods.** For large sparse systems, balanced truncation is applied with low-rank factors of the Gramians, which iterative Lyapunov solvers compute; the cost is then a number of sparse solves.

## Bounds

- **Lower bound for every method.** For every asymptotically stable $G_r$ of order at most $r$, $\|G - G_r\|_\infty \ge \|G - G_r\|_H \ge \sigma_{r+1}$. This is a theorem (Glover 1984): the Hankel operator of $G_r$ has rank at most $r$, and the best approximation of rank $r$ of a compact operator has error $\sigma_{r+1}$.
- **Upper bound by balanced truncation.** $\|G - G_r\|_\infty \le 2(\sigma_{r+1} + \dots)$ with each distinct value counted once. This is a theorem; see the [error bound](/balanced-truncation-error-bound/) page. So the best $H_\infty$ error of order $r$ is between $\sigma_{r+1}$ and twice the sum of the distinct tail values.
- **Hankel-norm optimum.** The minimum of $\|G - G_r\|_H$ over asymptotically stable $G_r$ of order $r$ is exactly $\sigma_{r+1}$, and Glover (1984) describes all minimizers.
- **H2 norm.** No a priori bound of this kind is used in practice for the $H_2$ error of IRKA. The optimal $H_2$ problem has local minima, and the first-order conditions (Meier and Luenberger 1967) are what IRKA meets.
- **Cost.** Dense balanced truncation costs $O(n^3)$ operations and $O(n^2)$ memory. Krylov and IRKA methods cost a number of linear solves with $sI - A$; for sparse $A$ this is close to linear in $n$ per solve in many applications, a measurement that depends on the solver.

## Reductions

- **To Lyapunov equations and an SVD.** Balanced truncation reduces the problem to two [Lyapunov equations](/lyapunov-equation/) and a [singular value decomposition](/singular-value-decomposition/) of a product of Cholesky or square-root factors.
- **To rational interpolation.** $H_2$ optimality reduces to Hermite interpolation of $G$ at the mirror images of the reduced poles (see [Hermite interpolation](/hermite-interpolation/)). Moment matching is interpolation at fixed points.
- **To low-rank matrix approximation.** The Hankel-norm problem is a structured version of the best rank $r$ approximation of the Hankel operator; the unstructured version is solved by the SVD, and the structured one by Glover's all-pass construction.
- **From realization.** When the data are impulse response samples instead of a state-space model, the [Ho-Kalman algorithm](/ho-kalman-algorithm/) and the [eigensystem realization algorithm](/eigensystem-realization-algorithm/) truncate the SVD of a Hankel matrix of [Markov parameters](/markov-parameters/), which is a data-driven form of balanced truncation.

## Applications

- **Circuit simulation.** The interconnect of integrated circuits gives RLC networks with millions of elements. Krylov methods reduce them to small models that the circuit simulator can use.
- **Structural dynamics.** [Finite element](/finite-element-method/) models of vehicles, aircraft and buildings are reduced for vibration analysis and for active control.
- **Controller reduction.** An $H_\infty$ or LQG controller has the order of the plant model plus the weights. Balanced or frequency-weighted reduction gives a controller of low order that can run on a small processor.
- **Control of partial differential equations.** Heat, flow and acoustic models are discretized, reduced, and then used to design controllers and observers.
- **Many-query problems.** Optimization, uncertainty quantification and real-time digital twins run a model many times; the reduced model makes that affordable.

## References
