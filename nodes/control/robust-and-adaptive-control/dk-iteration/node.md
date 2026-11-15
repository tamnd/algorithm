---
tag: QSHHP3
kind: algorithm
slug: dk-iteration
name: D-K iteration
aliases:
- mu-synthesis by D-K iteration
area: control/robust-and-adaptive-control
level: advanced
summary: Designs a controller for robust performance. It alternates H-infinity synthesis with the scalings fixed and a fit of the scalings with the controller fixed.
solves: [h-infinity-control-problem]
model: real-ram
complexity:
  vars: {n: the number of plant states, q: the larger of the number of outputs z and inputs w, f: the number of grid frequencies, k: the number of bisection steps on gamma, c: the number of Newton steps of one matrix sign function, g: the number of golden section steps, t: the number of D-K iterations}
  time: {per-iteration: "O(k (c n^3 + n^2 q) + f (n^3 + n^2 q) + g f q^3)", total: "O(t (k (c n^3 + n^2 q) + f (n^3 + n^2 q) + g f q^3))"}
  space: {extra: "O(n^2 + n q + f q^2)"}
properties: {deterministic: true, exact: false, recursive: false, iterative: true}
history:
  year: 1985
  people: [John C. Doyle]
  note: "Doyle (1982) defined the structured singular value. Doyle (1985) is usually cited for mu-synthesis, where the controller and the scalings are improved in turn."
prereqs: [dgkf-h-infinity-synthesis, structured-singular-value, golden-section-search]
see_also: [mu-analysis, lmi-h-infinity-synthesis, h-infinity-control-problem, mixed-sensitivity-design, linear-fractional-transformation, model-uncertainty, small-gain-theorem, gain-scheduling]
sources:
  - paper: doi:10.1049/ip-d.1982.0053
    title: John C. Doyle, Analysis of feedback systems with structured uncertainties, IEE Proceedings D 129(6), 242, 1982
    locator: the definition of the structured singular value and the upper bound by diagonal scalings
  - paper: doi:10.1109/cdc.1985.268842
    title: John C. Doyle, Structured uncertainty in control system design, Proceedings of the 24th IEEE Conference on Decision and Control, 260-265, 1985
    locator: the design of controllers against structured uncertainty with the structured singular value
  - paper: doi:10.1016/0005-1098(93)90175-S
    title: Andrew Packard and John C. Doyle, The complex structured singular value, Automatica 29(1), 71-109, 1993
    locator: the upper bound by D scales, the cases where it is exact, and the main loop theorem
  - paper: doi:10.1109/9.45196
    title: R. S. Sezginer and Michael L. Overton, The largest singular value of e^X A e^-X is convex on convex sets of commuting matrices, IEEE Transactions on Automatic Control 35(2), 229-230, 1990
    locator: the convexity of the scaled largest singular value in the logarithm of the scaling
  - paper: doi:10.1109/9.284879
    title: Richard D. Braatz, Peter M. Young, John C. Doyle and Manfred Morari, Computational complexity of mu calculation, IEEE Transactions on Automatic Control 39(5), 1000-1002, 1994
    locator: the NP-hardness of computing mu
  - paper: doi:10.1049/ip-d.1982.0054
    title: Michael G. Safonov, Stability margins of diagonally perturbed multivariable feedback systems, IEE Proceedings D 129(6), 251, 1982
    locator: the multivariable stability margin for diagonal perturbations
  - paper: doi:10.1109/9.62265
    title: Michael K. H. Fan, Andre L. Tits and John C. Doyle, Robustness in the presence of mixed parametric uncertainty and unmodeled dynamics, IEEE Transactions on Automatic Control 36(1), 25-38, 1991
    locator: the upper bound for mixed real and complex uncertainty with D and G scalings
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 11, Structured Singular Value
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Section 8.12, mu-synthesis and DK-iteration
---

D-K iteration is the usual method for mu-synthesis: the design of a controller $K$ that makes the peak over frequency of the [structured singular value](/structured-singular-value/) $\mu$ of the closed loop small. The exact problem is hard, because $\mu$ itself is NP-hard to compute (Braatz et al. 1994). The method replaces $\mu$ by its upper bound with diagonal scalings $D$, and it minimizes $\|D\,\mathcal{F}_l(P, K)\,D^{-1}\|_\infty$ over $K$ and $D$. This joint problem is not convex. But with $D$ fixed it is an [H-infinity synthesis](/dgkf-h-infinity-synthesis/) problem (the K-step), and with $K$ fixed it is a convex problem in $\log D$ at each frequency (the D-step). The method does the two steps in turn. Each step can only lower the bound, up to the tolerances, so the bound decreases. But the iteration can stop at a point that is not the global optimum, and no guarantee of the global optimum is known.

## In plain words

You want a controller that keeps good performance for every plant in an uncertainty set. Such a set has structure: the uncertainty is a list of separate blocks. The structured singular value tests this, but it is hard to minimize. A simpler number is an upper bound that uses one scale factor per block. If you fix the scale factors, the best controller comes from standard H-infinity synthesis. If you fix the controller, the best scale factors come from a small convex search. Do the two steps in turn. The bound goes down at each step and soon stops changing. The result is usually good, but it can be a local optimum.

## The problem

The generalized plant $P$ has inputs $(w, u)$ and outputs $(z, y)$, with $u = K y$. The closed loop is the lower [linear fractional transformation](/linear-fractional-transformation/) $M = \mathcal{F}_l(P, K)$ from $w$ to $z$. The uncertainty $\Delta$ closes a loop from some outputs $z$ to some inputs $w$, and it has the block diagonal structure $\boldsymbol\Delta = \{\mathrm{diag}(\Delta_1, \ldots, \Delta_F)\}$ with full complex blocks. For robust performance, one extra full block $\Delta_P$ connects the performance outputs to the performance inputs. The design problem is

$$\min_{K \text{ stabilizing}} \ \sup_\omega \ \mu_{\boldsymbol\Delta}(M(j\omega)).$$

By the main loop theorem (Packard and Doyle 1993), if this peak is below $\beta$, then for every structured uncertainty of size below $1/\beta$ the loop is internally stable and the performance map has H-infinity norm below $\beta$. For each frequency, $\mu_{\boldsymbol\Delta}(M) \le \inf_D \bar\sigma(D M D^{-1})$, where $D = \mathrm{diag}(d_1 I, \ldots, d_F I, I)$ and every $d_i > 0$. With one $D$ for all frequencies, this gives the problem that D-K iteration attacks:

$$\min_{K,\ D} \ \|D\,\mathcal{F}_l(P, K)\,D^{-1}\|_\infty.$$

This page uses a constant $D$ in the K-step and in the D-step, which is the simplest case. The usual tools fit a rational $D(s)$ to values of $d_i(\omega)$ found frequency by frequency (see Variants).

The implementation treats one uncertainty block and one performance block, so $D = \mathrm{diag}(d I, I)$ with one scalar $d > 0$. The plant has the normalized form of the [two-Riccati page](/dgkf-h-infinity-synthesis/). The uncertainty channels must not touch $u$ or $y$ directly, that is, the rows of $D_{12}$ and the columns of $D_{21}$ for the uncertainty block are zero. Then the scaled plant is still normalized.

## The algorithm

```pseudo id=main
DK-ITERATION(P, grid, iters, delta, tol)
L1  d ← 1
L2  for it ← 1 to iters do
L3      P_d ← P with z1 ← d z1 and w1 ← w1 / d
L4      K ← central controller of P_d at (1 + delta) · gamma_opt(P_d)        ▷ K-step
L5      M(jw) ← closed loop F_l(P, K) at each w in grid
L6      search log d by golden section for the least max_w sigma_max(D M(jw) D^-1)   ▷ D-step
L7      v ← the least value, d ← its argument
L8      if v went down by less than tol · v since the last pass then stop
L9  return the K and d with the least v
```

**K-step.** Line L3 moves the scaling into the plant: it multiplies the rows of $C_1$ and $D_{12}$ for $z_1$ by $d$, and it divides the columns of $B_1$ and $D_{21}$ for $w_1$ by $d$. Then $\mathcal{F}_l(P_d, K) = D\,\mathcal{F}_l(P, K)\,D^{-1}$ for every $K$. Line L4 runs the two-Riccati synthesis on $P_d$: a bisection on $\gamma$ finds $\gamma_{\rm opt}(P_d)$, and the central controller at a level a little above it gives $K$. The code repeats the functions of the two-Riccati page, so that the file stands alone.

**D-step.** Lines L5 to L7 compute the frequency responses of the unscaled loop once and then minimize the function $\phi(t) = \max_\omega \bar\sigma(D_t M(j\omega) D_t^{-1})$ with $D_t = \mathrm{diag}(e^t I, I)$. Each term is convex in $t$ (Sezginer and Overton 1990), so the maximum is convex, and the golden section search on $[-8, 8]$ finds its minimum to the tolerance.

## Example

The plant is $\dot x = x + w_1 + w_2 + u$, with $z_1 = 0.5 x$, $z_2 = x$, $z_3 = u$ and $y = x + w_3$. The uncertainty block is $w_1 = \Delta z_1$: a complex scalar uncertainty that makes the pole $1 + 0.5\,\Delta$. The performance block maps $(w_2, w_3)$, a load and a sensor noise, to $(z_2, z_3)$. So $A = 1$, $B_1 = [1, 1, 0]$, $B_2 = 1$, $C_1 = [0.5; 1; 0]$, $D_{12} = [0; 0; 1]$, $C_2 = 1$ and $D_{21} = [0, 0, 1]$. The grid has 321 frequencies from $10^{-4}$ to $10^4$ and $\omega = 0$, and the K-step uses $1 + \delta = 1.02$.

| pass | $d$ in K-step | $\gamma_{\rm opt}(P_d)$ | $K(s)$ | peak at old $d$ | new $d$ | $v$ |
|---|---|---|---|---|---|---|
| 1 | 1 | 3.06155 | $-177.992/(s + 60.0728)$ | 3.12213 | 1.41421 | 3.09689 |
| 2 | 1.41421 | 3.00002 | $-173.692/(s + 59.7749)$ | 3.05938 | 1.41421 | 3.05938 |
| 3 | 1.41421 | 3.00002 | same | 3.05938 | 1.41421 | 3.05938 |

The third pass changes nothing, so the iteration stops. These are measurements of the code. The bound on the peak of $\mu$ goes from $3.09689$ for the plain H-infinity controller to $3.05938$. The closed loop poles of the final controller are $-56.768$ and $-2.007$.

Here the K-step optimum can be checked by hand. With $d = \sqrt 2$ the scaled plant has $B_1 B_1^T = C_1^T C_1 = 3/2$, so both Riccati equations are $(1 - 1.5\,\gamma^{-2}) X^2 - 2X - 1.5 = 0$. At $\gamma = 3$ this is $\tfrac56 X^2 - 2X - 1.5 = 0$, with the stabilizing root $X = Y = 3$, so $\rho(XY) = \gamma^2$ and $\gamma_{\rm opt}(P_{\sqrt 2}) = 3$. The plant is symmetric under $d \to 2/d$, and the scan of $\gamma_{\rm opt}(P_d)$ over $d$ has its least value at $d = \sqrt 2$. Since there are two full blocks, the scaled bound equals $\mu$ at each frequency (Packard and Doyle 1993). But a constant $d$ for all frequencies can still be conservative.

## Correctness

The method is a heuristic for the problem with $\mu$, and it is a descent method for the problem with constant scalings. Let $J(K, d) = \|D\,\mathcal{F}_l(P, K)\,D^{-1}\|_\infty$. Three facts give the descent:

1. **Scaling the plant.** $\mathcal{F}_l(P_d, K) = D\,\mathcal{F}_l(P, K)\,D^{-1}$, because $D$ acts only on the channels $z_1$ and $w_1$, which do not touch $u$ and $y$ directly. So the K-step minimizes $J(\cdot, d)$ over all stabilizing controllers, up to the bisection tolerance and the factor $1 + \delta$.
2. **Convex D-step.** $t \mapsto \bar\sigma(e^{tE} M e^{-tE})$ is convex for each fixed complex matrix $M$ and diagonal $E$ (Sezginer and Overton 1990). A maximum of convex functions is convex. So golden section search finds the minimum of the grid function to its tolerance, provided the minimum lies inside $[-8, 8]$.
3. **Descent.** Take the true norm in place of the grid maximum and exact arithmetic. Let $v_k = J(K_k, d_k)$ after pass $k$. The next K-step gives $\gamma_{\rm opt}(P_{d_k}) \le J(K_k, d_k) = v_k$, because $K_k$ is one of the candidates. The new controller has $J(K_{k+1}, d_k) < (1 + \delta)\,\gamma_{\rm opt}(P_{d_k})$, and the D-step can only lower this. So $v_{k+1} < (1 + \delta)\,v_k$. With $\delta \to 0$ and exact steps the sequence is nonincreasing, and since it is bounded below by 0 it converges.

A limit of the sequence is a point where neither step can improve. Such a point need not be a global optimum of $J$, because $J$ is not jointly convex in $K$ and $D$. The proofs are in [proofs/correctness.md](proofs/correctness.md); the convexity result and the two-Riccati theorem are cited.

## Complexity

Let $n$ be the number of plant states, $q$ the larger of the number of outputs $z$ and inputs $w$, and $f$ the number of grid frequencies. These bounds are for the real-RAM model with dense factorizations.

**Per iteration.** The K-step costs $O(k(c n^3 + n^2 q))$ as on the [two-Riccati page](/dgkf-h-infinity-synthesis/), with $k$ bisection steps and $c$ Newton steps per sign function. The closed loop has $2n$ states, so the frequency responses cost $O(f(n^3 + n^2 q))$. Each value of $\phi$ costs $f$ largest singular values of $q \times q$ matrices, $O(f q^3)$ with a bounded number of Jacobi sweeps. Golden section needs $g = O(\log(16/\text{tol}))$ values. The total per iteration is $O(k(c n^3 + n^2 q) + f(n^3 + n^2 q) + g f q^3)$.

**Number of iterations.** No useful bound on the number of passes $t$ is known. The convergence result above only says that the bounds decrease and converge, not how fast or to what. In practice a few passes are typical (rule of thumb); the example stops after three.

## Properties

- The bound $v_k$ is an upper bound on $\sup_\omega \mu_{\boldsymbol\Delta}(M(j\omega))$ only on the grid. Between grid points the true peak can be larger.
- With full complex blocks only and $2S + F \le 3$, where $S$ is the number of repeated scalar blocks and $F$ the number of full blocks, the scaled bound is equal to $\mu$ at each frequency (Packard and Doyle 1993). With more blocks it can be strictly larger.
- The controller order is the order of $P$ plus the order of the scalings. A constant $D$ adds no states, but a rational $D(s)$ of order $r$ adds $2r$ states per block, one copy on each side.
- The method is deterministic, and it depends on the start $d = 1$. A different start can give a different limit.

## Variants and improvements

- **Frequency-dependent scalings.** The standard method solves the D-step separately at each grid frequency, which gives values $d(\omega)$, then fits a stable, minimum phase rational $D(s)$ to them, and it puts $D(s)$ into the plant for the next K-step (Skogestad and Postlethwaite 2005, section 8.12). This is less conservative than a constant $D$ but the fit adds states and can break the descent property.
- **LMI K-step.** The K-step can use [LMI-based synthesis](/lmi-h-infinity-synthesis/), which needs no rank assumptions on the scaled plant.
- **Real uncertainty.** For real parametric blocks, the upper bound of Fan, Tits and Doyle (1991) adds a second scaling $G$. Synthesis methods use this bound in place of the D-scale bound, with a similar alternation.

## When to use it

Use D-K iteration when the uncertainty has a clear block structure, a robust performance specification is needed, and plain [mixed sensitivity design](/mixed-sensitivity-design/) is too conservative because it treats all uncertainty as one block. Check the result by [mu-analysis](/mu-analysis/) with both bounds on a fine grid. If the uncertainty is a single full block, plain H-infinity synthesis is enough, because then $\mu = \bar\sigma$.

## Pitfalls

- **Local optima.** The joint problem is not convex. Try other starting scalings, and compare with an upper bound from analysis.
- **Back off.** Near $\gamma_{\rm opt}$ the central controller has very fast poles. The factor $1 + \delta$ is a rule of thumb; it makes the descent hold only up to that factor, so do not stop on a single small rise.
- **Grid.** A coarse grid can miss a sharp peak. The bound $v$ is then too optimistic.
- **Fit order.** With frequency-dependent scalings, a high order fit gives a high order controller, and a low order fit can make the bound worse than the values $d(\omega)$ predict.
- **Scaling range.** If the best $d$ is near the end of the search interval, the uncertainty channel is almost decoupled from the performance channel. Then widen the interval or check the plant.
- **Sign conventions.** The controller is wired as $u = K y$. Convert from sources that use $u = -K y$ or positive feedback before you compare.

## Implementations

## History

Doyle (1982) defined the structured singular value and gave its upper bound with diagonal scalings. Safonov (1982) gave a related stability margin for diagonal perturbations. Doyle (1985) is usually cited as the start of mu-synthesis, where the controller and the scalings are improved in turn. Sezginer and Overton (1990) proved the convexity in the logarithm of the scaling that makes the D-step a convex problem. Packard and Doyle (1993) surveyed the complex structured singular value and the cases where the scaled bound is exact. Braatz, Young, Doyle and Morari (1994) proved that computing $\mu$ is NP-hard, which explains why synthesis works with the bound.

## References
