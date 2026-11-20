---
tag: JVNKSY
kind: technique
slug: adjoint-state-method
name: Adjoint-state method
aliases:
- adjoint-state gradient
- adjoint method
area: imaging-and-inverse-problems/seismic-imaging
level: advanced
summary: "Compute the gradient of a misfit with respect to all model parameters at the cost of two wave simulations, one forward and one adjoint."
prereqs: [wave-equation, automatic-differentiation]
see_also: [adjoint-model, automatic-differentiation, backpropagation, full-waveform-inversion, reverse-time-migration, four-dimensional-variational-assimilation, gradient-checking, least-squares-migration]
sources:
  - paper: doi:10.1111/j.1365-246X.2006.02978.x
    title: R.-E. Plessix, A review of the adjoint-state method for computing the gradient of a functional with geophysical applications, Geophysical Journal International 167(2), 2006, 495 to 503
    locator: the Lagrangian derivation of the adjoint state and its use for the wave equation in the time and frequency domains
  - paper: "Guy Chavent, Identification of functional parameters in partial differential equations, in Identification of Parameters in Distributed Systems, R. E. Goodson and M. Polis (eds.), ASME, 1974, pages 31 to 48"
    locator: the adjoint-state computation of the gradient for parameter identification in partial differential equations
  - paper: doi:10.1190/1.1441754
    title: Albert Tarantola, Inversion of seismic reflection data in the acoustic approximation, Geophysics 49(8), 1984, 1259 to 1266
    locator: the gradient of the waveform misfit by back-propagation of the residuals
---

The adjoint-state method computes the gradient of an objective $J(m) = h(u(m))$, where the state $u$ depends on the parameters $m$ through an equation $F(u, m) = 0$, such as a wave equation whose coefficients are $m$. Instead of one simulation per parameter, it needs one forward solve for $u$ and one solve of the adjoint (transposed) equation for an adjoint state $\lambda$, and then $\nabla J = -\big(\partial F/\partial m\big)^{\mathsf T}\lambda$ (a theorem). The cost does not depend on the number of parameters. The [adjoint model](/adjoint-model/) of data assimilation is a special case of the same idea: there the transpose of the tangent linear forecast model, run backward in time, gives the gradient with respect to the initial state. The adjoint-state method is the general form, for any parameters of the equation; in seismic imaging the parameters are the coefficients of the wave equation, and the gradient is a [reverse-time migration](/reverse-time-migration/) of the residuals. Applied to the discrete equations, it is reverse-mode [automatic differentiation](/automatic-differentiation/) done by hand.

## In plain words

Suppose a simulation depends on a million numbers, such as the wave speed in each cell of the ground, and you want to know how a single score, the mismatch with the data, changes when each number changes. Trying each number one at a time would take a million simulations. The adjoint-state method gets all million answers from two runs. The first run is the normal simulation. The second run goes backward: it starts from the mismatch at the receivers and sends it back through the same physics, like playing the echoes in reverse. Where the backward run meets the forward run, it tells how much each cell is to blame for the mismatch.

## When it applies

**Setting.** A state $u \in \mathbb{R}^N$, parameters $m \in \mathbb{R}^P$, a state equation $F(u, m) = 0$ that has a unique solution $u(m)$ for each $m$ with $\partial F/\partial u$ invertible, and a smooth objective $h(u)$, for example $h(u) = \frac12\|Ru - d\|^2$ with a receiver operator $R$.

**The theorem.** Let $\lambda$ solve the adjoint equation
$$\Big(\frac{\partial F}{\partial u}\Big)^{\mathsf T}\lambda = \Big(\frac{\partial h}{\partial u}\Big)^{\mathsf T}.$$
Then $\nabla_m J = -\big(\partial F/\partial m\big)^{\mathsf T}\lambda$.

*Proof.* Differentiate $F(u(m), m) = 0$: $F_u\,u' = -F_m$. So $J' = h_u\,u' = -h_u F_u^{-1}F_m = -\lambda^{\mathsf T}F_m$ with $\lambda^{\mathsf T} = h_u F_u^{-1}$, which is the adjoint equation. $\square$

The same result follows from the Lagrangian $\mathcal{L}(u, \lambda, m) = h(u) - \lambda^{\mathsf T}F(u, m)$: at the state and adjoint solutions, $\nabla_m J = \partial\mathcal{L}/\partial m$.

**Time-dependent equations.** For a time-stepping scheme, $F_u$ is block lower triangular in time, so $F_u^{\mathsf T}$ is block upper triangular: the adjoint equation runs backward in time from a zero final state, with the data residuals as its source. For the wave equation $m\,u_{tt} - \Delta u = f$, $\partial F/\partial m$ applied to $\delta m$ is $\delta m\,u_{tt}$, so $\nabla_m J(x) = -\int \lambda(x, t)\,u_{tt}(x, t)\,dt$, a zero-lag correlation, the [imaging condition](/imaging-condition/).

**Conditions.** The method needs the transpose of the linearized state operator, so the equation must be differentiable in $u$ and $m$, and the forward states must be available during the backward run. It gives the gradient of one scalar objective; for $K$ objectives it needs $K$ adjoint solves.

## The template

```pseudo id=main
ADJOINT-STATE-GRADIENT(m)
L1  u ← solution of F(u, m) = 0      ▷ one forward simulation; keep the states needed in L3 and L4
L2  J ← h(u)
L3  λ ← solution of (∂F/∂u)ᵀ λ = (∂h/∂u)ᵀ      ▷ one adjoint simulation; backward in time for time stepping
L4  g ← -(∂F/∂m)ᵀ λ      ▷ for the wave equation, a correlation of λ with u_tt at every point
L5  return J, g
```

The holes are the state equation and its discretization (L1), the objective (L2), the adjoint solver (L3), which uses the transpose of the same discrete operator, and the parameter derivative (L4). Line L4 costs about one pass over the stored forward states.

## Classic examples

**A small linear system by hand.** Let $F(u, m) = A(m)u - f$ with
$A(m) = \begin{pmatrix} m_1 & 0 \\ -1 & m_2 \end{pmatrix}$, $f = (1, 0)$, and $h(u) = \frac12 u_2^2$. At $m = (1, 2)$ the state is $u = (1, 0.5)$ and $J = 0.125$. The adjoint equation $A^{\mathsf T}\lambda = (0, u_2) = (0, 0.5)$ reads $m_2\lambda_2 = 0.5$ and $m_1\lambda_1 - \lambda_2 = 0$, so $\lambda = (0.25, 0.25)$. Since $\partial A/\partial m_1$ and $\partial A/\partial m_2$ pick the two diagonal entries, $g = (-\lambda_1 u_1, -\lambda_2 u_2) = (-0.25, -0.125)$. Directly, $J = \frac12(m_1 m_2)^{-2}$ gives $\partial J/\partial m_1 = -(m_1 m_2)^{-2}/m_1 = -0.25$ and $\partial J/\partial m_2 = -0.125$, the same.

**[Full-waveform inversion](/full-waveform-inversion/).** The state is the discrete wavefield, the parameters are $1/v^2$ in every cell, and $h$ is the least-squares data misfit. The adjoint run is the transposed time-stepping scheme with the residuals injected at the receivers. The test of that page checks the gradient against [finite differences](/gradient-checking/) to about $6 \times 10^{-8}$ (a measurement).

**[Reverse-time migration](/reverse-time-migration/).** With the misfit linearized about a background model, the gradient at $\delta m = 0$ is $-L^{\mathsf T}d$ for Born modeling $L$, which RTM computes. Migration is the first gradient of an inversion.

**[4D-Var](/four-dimensional-variational-assimilation/).** The parameters are the initial state of a forecast model; the adjoint state is computed by the [adjoint model](/adjoint-model/) backward over the assimilation window.

**[Backpropagation](/backpropagation/).** A layered network is a state equation $u_{k+1} = \sigma(W_k u_k)$; the backward pass is its adjoint, and the weight gradient is the product of the adjoint state and the forward activations.

## Variations

- **Discrete or continuous adjoint.** Transposing the discrete scheme (discretize, then optimize) gives the exact gradient of the discrete objective. Deriving the continuous adjoint equation and discretizing it (optimize, then discretize) gives an approximation that converges as the grid is refined, but may not pass a gradient check.
- **Frequency domain.** For the time-harmonic wave equation $A(\omega, m)u = f$, the adjoint is the conjugate transpose system, and one factorization of $A$ serves both the forward and the adjoint solves.
- **Checkpointing.** Store the forward states only at checkpoints and recompute between them during the backward run; with $O(\log s)$ checkpoints the recomputation cost grows by a factor $O(\log s)$ for $s$ time steps, the binomial schedule of automatic differentiation.
- **Second-order adjoints.** A second forward and adjoint pair gives a Hessian-vector product, for Newton and Gauss-Newton methods.
- **Many sources.** For several shots the objective is a sum, so the gradient is the sum of the gradients of each shot, each with its own forward and adjoint runs.

## Pitfalls

- **Mismatched discretizations.** Using a different scheme for the adjoint run than the transpose of the forward scheme in line L3 gives a gradient that is wrong by a discretization error, and line searches fail near the optimum. Check the gradient against finite differences on a small case.
- **The wrong end condition.** The adjoint of a time-stepping scheme starts from zero at the final time and runs backward. Starting it at time zero, or forward, gives nonsense.
- **Transpose of a variable coefficient.** For $u^{n+1} = 2u^n - u^{n-1} + (\Delta t^2/m)Lu^n$, the transpose of $(\Delta t^2/m)L$ is $L(\Delta t^2/m)$, so the adjoint state $\lambda$ gets $1/m$ before $L$. The scaled state $\mu = \lambda/m$ satisfies the same recursion with $1/m$ after $L$, as on the [full-waveform inversion](/full-waveform-inversion/) page. Mixing the two forms is exact only for constant $m$.
- **Memory.** Line L4 needs the forward field at every time of the backward run. Storing all of it is often too large in 3D; use checkpointing or boundary storage.
- **Nonsmooth objectives.** The method gives the gradient of a differentiable $h$; for an $\ell_1$ misfit or a shock in the state, the gradient is not defined everywhere.

## Exercises

1. Derive the adjoint equation for $F(u, m) = A(m)u - f$ from the Lagrangian $h(u) - \lambda^{\mathsf T}(A(m)u - f)$ and check it on the $2 \times 2$ example.
2. For the 1D scheme $u^{n+1} = 2u^n - u^{n-1} + \Delta t^2 m^{-1}(Lu^n + f^n)$, write all time steps as one block lower-triangular system and derive the backward recursion of the adjoint state.
3. Count the solves needed for the gradient of $J$ with $P$ parameters by forward finite differences, by forward sensitivities, and by the adjoint state.

## References
