---
tag: 5JS87D
kind: algorithm
slug: h-infinity-loop-shaping
name: H-infinity loop shaping
aliases:
- Glover-McFarlane loop shaping
- normalized coprime factor robust stabilization
area: control/robust-and-adaptive-control
level: advanced
summary: Shapes the open loop with weights and then robustly stabilizes the shaped plant against normalized coprime factor uncertainty.
solves: [h-infinity-control-problem]
model: real-ram
complexity:
  vars: {n: the number of states of the shaped plant, m: the number of plant inputs, p: the number of plant outputs, c: the number of Newton steps of one matrix sign function}
  time: {total: "O(c n^3 + n^2 (m + p))"}
  space: {extra: "O(n^2 + n (m + p))"}
properties: {deterministic: true, exact: false, recursive: false, iterative: false}
history:
  year: 1992
  people: [Duncan McFarlane, Keith Glover]
  note: "Glover and McFarlane (1989) solved robust stabilization against normalized coprime factor uncertainty in closed form. McFarlane and Glover (1992) turned it into a design procedure with loop shaping weights."
prereqs: [loop-shaping, coprime-factorization, continuous-algebraic-riccati-equation, h-infinity-norm]
see_also: [dgkf-h-infinity-synthesis, mixed-sensitivity-design, nu-gap-metric, h-infinity-control-problem, small-gain-theorem, model-uncertainty, lqg-control, model-order-reduction]
sources:
  - paper: doi:10.1109/9.29424
    title: Keith Glover and Duncan McFarlane, Robust stabilization of normalized coprime factor plant descriptions with H-infinity-bounded uncertainty, IEEE Transactions on Automatic Control 34(8), 821-830, 1989
    locator: the closed form of the largest stability margin and the controllers that reach it
  - paper: doi:10.1109/9.256330
    title: Duncan McFarlane and Keith Glover, A loop-shaping design procedure using H-infinity synthesis, IEEE Transactions on Automatic Control 37(6), 759-769, 1992
    locator: the design procedure with pre and post weights and the bounds on how much the robust controller changes the shaped loop
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Section 9.4, H-infinity loop-shaping design (the two Riccati equations, gamma_min and the central controller for positive feedback)
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 18, H-infinity Loop Shaping
  - paper: doi:10.1109/9.237648
    title: Glenn Vinnicombe, Frequency domain uncertainty and the graph topology, IEEE Transactions on Automatic Control 38(9), 1371-1383, 1993
    locator: the nu-gap metric and the robust stability result in terms of b(G, K)
---

H-infinity loop shaping, also called Glover-McFarlane loop shaping, is a design method for linear multivariable feedback in two steps. First the designer picks weights $W_1$ and $W_2$ so that the shaped plant $G_s = W_2 G W_1$ has a good open loop shape: high gain at low frequency, low gain at high frequency and a moderate slope near crossover, as in classical [loop shaping](/loop-shaping/). Then a robust controller $K_s$ stabilizes $G_s$ with the largest possible margin against perturbations of a normalized [coprime factorization](/coprime-factorization/) of $G_s$. The final controller is $K = W_1 K_s W_2$. The second step is a special [H-infinity control problem](/h-infinity-control-problem/) whose optimal level has a closed form from two Riccati equations, so no search on $\gamma$ is needed.

## In plain words

Classical loop shaping tells you what the loop gain should look like, but it does not tell you how to make the loop stable with good margins for a plant with many inputs and outputs. This method lets you shape the gain first, with simple weights, and then adds a controller that fixes stability and robustness near crossover. The robust step is cheap: two Riccati equations give the best margin in closed form. If the best margin is very small, the shape you asked for is not compatible with the plant, and you change the weights. If the margin is good, the robust step changes the shaped loop only a little.

## The problem

Let $G_s = (A, B, C, 0)$ be a strictly proper shaped plant with $m$ inputs, $p$ outputs and $n$ states, with $(A, B)$ [stabilizable](/stabilizability/) and $(C, A)$ [detectable](/detectability/). A normalized left coprime factorization $G_s = M^{-1} N$ has $M$ and $N$ stable and $N N^* + M M^* = I$ on the imaginary axis. The perturbed plants are

$$G_\Delta = (M + \Delta_M)^{-1}(N + \Delta_N), \qquad \left\| \begin{bmatrix} \Delta_N & \Delta_M \end{bmatrix} \right\|_\infty < \varepsilon,$$

with $\Delta_N$ and $\Delta_M$ stable. The controller $K_s$ is connected in negative feedback, $u = -K_s y$. By the [small gain theorem](/small-gain-theorem/), $K_s$ stabilizes every such $G_\Delta$ if and only if it stabilizes $G_s$ internally and

$$\gamma(G_s, K_s) = \left\| \begin{bmatrix} K_s \\ I \end{bmatrix} (I + G_s K_s)^{-1} \begin{bmatrix} I & G_s \end{bmatrix} \right\|_\infty \le \frac{1}{\varepsilon}.$$

The stability margin of the loop is $b(G_s, K_s) = 1 / \gamma(G_s, K_s)$. The robust step asks for a controller with $b$ close to the largest value $\varepsilon_{\max}$.

**Theorem** (Glover and McFarlane 1989; Skogestad and Postlethwaite 2005, section 9.4). Let $Z \ge 0$ be the stabilizing solution of the filter Riccati equation and $X \ge 0$ that of the control Riccati equation:

$$A Z + Z A^T - Z C^T C Z + B B^T = 0, \qquad A^T X + X A - X B B^T X + C^T C = 0.$$

Then the smallest achievable value of $\gamma(G_s, K_s)$ over all internally stabilizing controllers is

$$\gamma_{\min} = \sqrt{1 + \rho(X Z)}, \qquad \varepsilon_{\max} = \frac{1}{\gamma_{\min}} = \sqrt{1 - \left\| \begin{bmatrix} N & M \end{bmatrix} \right\|_H^2},$$

where $\rho$ is the spectral radius and $\| \cdot \|_H$ is the Hankel norm. For every $\gamma > \gamma_{\min}$ a controller with $\gamma(G_s, K_s) \le \gamma$ is $K_s = (A_K, B_K, C_K, 0)$ with

$$L = (1 - \gamma^2) I + X Z, \quad B_K = \gamma^2 (L^T)^{-1} Z C^T, \quad A_K = A - B B^T X + B_K C, \quad C_K = -B^T X.$$

Skogestad and Postlethwaite (2005) write this controller for positive feedback, $u = K_s y$, with $C_K = B^T X$. This page uses negative feedback, so the sign of $C_K$ is changed once here and in the code.

## The algorithm

```pseudo id=main
LOOP-SHAPING-DESIGN(G, W1, W2, f)
L1  Gs ← W2 G W1                          ▷ shaped plant (A, B, C, 0)
L2  Z ← stabilizing solution of A Z + Z A^T - Z C^T C Z + B B^T = 0
L3  X ← stabilizing solution of A^T X + X A - X B B^T X + C^T C = 0
L4  γmin ← sqrt(1 + ρ(X Z))
L5  γ ← f · γmin                           ▷ f > 1, often 1.1
L6  L ← (1 - γ^2) I + X Z
L7  B_K ← γ^2 (L^T)^-1 Z C^T
L8  Ks ← (A - B B^T X + B_K C, B_K, -B^T X, 0)
L9  return γmin, γ, K = W1 Ks W2
```

The two Riccati equations are solved as on the [two-Riccati synthesis](/dgkf-h-infinity-synthesis/) page: the code takes the matrix sign function of the $2n \times 2n$ [Hamiltonian matrix](/hamiltonian-matrix/) by a scaled Newton iteration, reads off the stable invariant subspace, and accepts the solution only if the residual is small and the closed loop matrix is [Hurwitz](/hurwitz-matrix/). The designer then checks $\gamma_{\min}$: a value above about 4 ($\varepsilon_{\max}$ below 0.25) means the weights ask for a loop that this plant cannot give with good robustness. This is a rule of thumb from design practice (Skogestad and Postlethwaite 2005, section 9.4), not a theorem.

## Example

Take $G_s = 1/s$, so $A = 0$ and $B = C = 1$. Both Riccati equations reduce to $1 - X^2 = 0$, so $X = Z = 1$ and

$$\gamma_{\min} = \sqrt{1 + 1} = 1.41421, \qquad \varepsilon_{\max} = 0.70711.$$

With $f = 1.1$, $\gamma = 1.55563$ and $\gamma^2 = 2.42$. Then $L = -0.42$, $B_K = 2.42 \cdot 1/(-0.42) = -5.76190$, $A_K = -1 - 5.76190 = -6.76190$ and $C_K = -1$. The controller for $u = -K_s y$ is

$$K_s(s) = \frac{5.76190}{s + 6.76190}.$$

The loop $G_s K_s$ gives the closed loop polynomial $s^2 + 6.76190 s + 5.76190 = (s + 1)(s + 5.76190)$, so the loop is internally stable. A frequency sweep of the $2 \times 2$ map in the definition of $\gamma$ gives a peak of $1.54183$, reached as $\omega \to 0$, so $b = 0.64858$. This is above $1/\gamma = 0.64282$ and below $\varepsilon_{\max}$, as the theorem says.

For this plant the static gain $K_s = 1$ already reaches $\varepsilon_{\max}$: the map is $\frac{s}{s + 1}\begin{bmatrix} 1 & 1/s \\ 1 & 1/s \end{bmatrix}$, which has rank one and largest singular value $\sqrt 2$ at every frequency. As $\gamma \to \gamma_{\min}$, $L$ becomes singular and the central controller degenerates; this is why the procedure backs off.

For $G_s = 1/(s + 1)$ the equations give $X = Z = \sqrt 2 - 1$, $\gamma_{\min} = \sqrt{4 - 2\sqrt 2} = 1.08239$ and $\varepsilon_{\max} = \cos(\pi/8) = 0.92388$. With the integral weight $W_1 = (s + 2)/s$ the shaped plant $(s + 2)/(s(s + 1))$ has $\gamma_{\min} = 1.55146$, and the final controller $K = W_1 K_s$ has three states, an integrator, and gives an internally stable loop with the plant.

## Correctness

The theorem above is cited; its proof combines three facts (Glover and McFarlane 1989; Zhou, Doyle and Glover 1996, chapter 18). First, the small gain theorem reduces robust stabilization against $[\Delta_N, \Delta_M]$ to the bound on $\gamma(G_s, K_s)$. Second, for a normalized coprime factorization this bound is a two-block problem that reduces to a Nehari problem, whose optimum is given by the Hankel norm of $[N\ M]$. Third, the state-space formulas for the normalized factors turn that Hankel norm into the gramians of a realization with the matrices $X$ and $Z$, which gives $\gamma_{\min}^2 = 1 + \rho(XZ)$.

The code is correct if it computes the stabilizing $X$ and $Z$, and then applies the formulas. The Riccati step is the one proved on the two-Riccati synthesis page. The proof file [proofs/correctness.md](proofs/correctness.md) checks the scalar cases in closed form, shows that the series connection gives $K = W_1 K_s W_2$, and explains why the sign change gives the same loop as the positive feedback formulas of the source. The tests check $\gamma_{\min}$ against a separate Hankel norm computation from two Lyapunov equations, and they check that no stabilizing static or first-order controller from a random sample has a margin above $\varepsilon_{\max}$.

## Complexity

Let $n$ be the number of states of the shaped plant, which is the plant order plus the weight orders. The method needs two Riccati equations of size $n$ and one eigenvalue problem for $XZ$. With $c$ Newton steps per matrix sign function, each step $O(n^3)$, the time is $O(c n^3 + n^2(m + p))$ and the extra space is $O(n^2 + n(m + p))$. There is no bisection on $\gamma$, unlike general H-infinity synthesis, because $\gamma_{\min}$ has a closed form. The final controller has $n$ states plus the states of $W_1$ and $W_2$, before any reduction.

## Properties

- $\gamma_{\min} \ge 1$ always, so $\varepsilon_{\max} \le 1$.
- The margin $b(G, K)$ is the same quantity that the [nu-gap metric](/nu-gap-metric/) theory uses: if $b(G, K) > \beta$, then $K$ stabilizes every plant whose $\nu$-gap from $G$ is at most $\beta$ (Vinnicombe 1993).
- The robust step changes the loop only where it must: McFarlane and Glover (1992) give bounds, in terms of $\varepsilon$, on the change of the loop gain at frequencies where the shaped loop gain is large or small. The bounds are theorems; how close the final loop stays to the shaped loop is a measurement on each design.
- $\gamma(G_s, K_s)$ bounds the four closed loop maps $(I + G_s K_s)^{-1}$, $(I + G_s K_s)^{-1} G_s$, $K_s (I + G_s K_s)^{-1}$ and $K_s (I + G_s K_s)^{-1} G_s$ at once, because each one is a block of the $2 \times 2$ block map in the definition. So $\gamma_{\min}$ also limits the peaks of the sensitivity and complementary sensitivity of the shaped loop.
- Like all H-infinity central controllers, $K_s$ is observer based and has the order of the shaped plant.

## Variants and improvements

- **Nonzero D.** If the shaped plant has $D \ne 0$, the Riccati equations get extra terms with $R = I + D^T D$ and $S = I + D D^T$ (Skogestad and Postlethwaite 2005, section 9.4). This code needs $D = 0$.
- **Observer form.** The controller can be written in observer form, which makes gain scheduling and [anti-windup](/anti-windup/) easier (Skogestad and Postlethwaite 2005, section 9.4).
- **Two degrees of freedom.** A reference model can be added to the robust step to improve tracking, as in Skogestad and Postlethwaite (2005, section 9.4).
- **Discrete time.** The same procedure works with discrete Riccati equations.
- **Weight choice by optimization.** Some methods tune the weights to meet given margins; the second step stays the same.

## When to use it

Use it for multivariable plants when you can say what the loop gain should look like, and you want a robust controller without building a weighted generalized plant as in [mixed sensitivity design](/mixed-sensitivity-design/). It is a good first design because it needs only the two weights and one number, $\gamma_{\min}$, tells you if they are reasonable. It is less direct when the specifications are about particular closed loop maps, or when there is structured uncertainty; then use mixed sensitivity or [D-K iteration](/dk-iteration/).

## Pitfalls

- **Bad weights.** If $\gamma_{\min}$ is large, the robust step changes the loop a lot near crossover and the final loop is not the one you shaped. Fix the weights; do not accept the result.
- **Unscaled plants.** The robustness measure mixes all inputs and outputs, so scale the plant to sensible units before you shape it.
- **Sign conventions.** Formulas from books on this method are often for positive feedback. A controller with the wrong sign makes the loop unstable even though the numbers look right.
- **Integrators.** A pure integrator in $W_1$ gives a shaped plant with a pole at 0. The Riccati equations still work, but a frequency sweep at $\omega = 0$ fails; sweep over positive frequencies.
- **Controller order.** The controller has as many states as the shaped plant. Use [model order reduction](/model-order-reduction/) and check the margin again after the reduction.

## Implementations

## History

Glover and McFarlane (1989) solved the robust stabilization problem for normalized coprime factor perturbations and found that the optimal level has a closed form, unlike general H-infinity problems. McFarlane and Glover (1992) built the loop shaping design procedure on it, with weights that carry the performance goals and a robust step that needs no tuning. Vinnicombe (1993) linked the stability margin $b(G, K)$ to the $\nu$-gap metric, which gave the margin a clear meaning in terms of plant uncertainty.

## References
