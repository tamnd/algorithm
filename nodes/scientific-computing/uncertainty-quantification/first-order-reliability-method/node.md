---
tag: B2CCS2
kind: algorithm
slug: first-order-reliability-method
name: First-order reliability method
aliases:
- Hasofer-Lind method
- FORM
- HL-RF algorithm
area: scientific-computing/uncertainty-quantification
level: core
summary: Estimates a failure probability by finding the most probable failure point in standard normal space and linearizing the limit state there.
solves: [forward-uncertainty-propagation]
model: real-ram
complexity:
  vars: {d: "the number of random inputs", K: "the number of HL-RF iterations", C: "the cost of one evaluation of the limit state function"}
  time: {worst: O(K d C)}
  space: {extra: O(d)}
properties: {deterministic: true, intrusive: false, exact: false}
history:
  year: 1974
  people: [Abraham M. Hasofer, Niels C. Lind, Rudiger Rackwitz, Bernd Fiessler, Karl Breitung]
  note: Hasofer and Lind defined the reliability index as the distance to the limit state in standard normal space in 1974. Rackwitz and Fiessler gave the iteration for non-normal inputs in 1978, and Breitung the second-order correction in 1984.
prereqs: [random-variable, inverse-transform-sampling, kkt-conditions]
see_also: [subset-simulation, importance-sampling, monte-carlo-integration, newton-raphson-method, adjoint-sensitivity-analysis, automatic-differentiation, forward-uncertainty-propagation, cross-entropy-method]
sources:
  - paper: doi:10.1061/JMCEA3.0001848
    title: Abraham M. Hasofer and Niels C. Lind, Exact and invariant second-moment code format, Journal of the Engineering Mechanics Division (ASCE) 100(1), 1974, 111-121
    locator: the reliability index as the distance from the origin to the limit state surface in the space of standardized variables, and its invariance under reformulation of the limit state
  - paper: doi:10.1061/(ASCE)0733-9399(1984)110:3(357)
    title: Karl Breitung, Asymptotic approximations for multinormal integrals, Journal of Engineering Mechanics 110(3), 1984, 357-366
    locator: the asymptotic formula Phi(-beta) times the product of (1 + beta kappa_i)^(-1/2) over the principal curvatures at the design point
  - paper: doi:10.1016/0167-4730(91)90041-7
    title: Pei-Ling Liu and Armen Der Kiureghian, Optimization algorithms for structural reliability, Structural Safety 9(3), 1991, 161-177
    locator: the comparison of algorithms for the design point problem, the failure of plain HL-RF to converge in some cases, and the modified HL-RF method with a merit function
  - book: isbn:9780471960867
    title: Ove Ditlevsen and Henrik O. Madsen, Structural Reliability Methods, Wiley, 1996
    locator: Chapter 5 (the geometric reliability index of Hasofer and Lind) and the later chapters on non-normal inputs and second-order corrections
---

The first-order reliability method (FORM) estimates the probability that a system fails, $P_f = \mathbb{P}[g(X) \le 0]$, where $g$ is the limit state function of the random inputs $X$. It maps $X$ to a vector $u$ of independent standard normal variables, finds the point $u^*$ of the limit state surface $g = 0$ closest to the origin, and replaces the surface by its tangent plane there. The distance $\beta = \|u^*\|$ is the Hasofer-Lind reliability index, and $P_f \approx \Phi(-\beta)$. The design point $u^*$ is the most probable failure point, because the standard normal density falls with the distance from the origin. FORM needs only a few dozen evaluations of $g$ and its gradient, no matter how small $P_f$ is, which is why structural engineers use it for probabilities of $10^{-3}$ to $10^{-7}$. The result is exact for a linear limit state of normal variables and an approximation otherwise; the [second-order correction](#variants-and-improvements) of Breitung uses the curvature of the surface.

## In plain words

You want the chance that a load beats the strength of a part, when both are uncertain. First, rescale every uncertain quantity so that it becomes a standard bell curve variable; then all directions in this new space are alike, and the chance of a point falls off with its distance from the center. The border between safe and failed is a surface in this space. The failure point that is easiest to reach is the point of the border closest to the center. Find it by a simple iteration that steps toward the border along its slope. Its distance $\beta$ tells you the answer: if the border were flat, the chance of failure would be exactly the chance that a bell curve variable exceeds $\beta$.

## The problem

The inputs $X = (X_1, \ldots, X_d)$ are independent with continuous marginal CDFs $F_k$. The map $x_k = F_k^{-1}(\Phi(u_k))$ sends a standard normal vector $u$ to $X$, by [inverse transform sampling](/inverse-transform-sampling/); write $x = T(u)$. The limit state function $g$ is differentiable, with failure for $g(x) \le 0$. In standard normal space the limit state is $G(u) = g(T(u))$. Find the design point

$$u^* = \arg\min \{\|u\| : G(u) = 0\},$$

the reliability index $\beta = \pm \|u^*\|$, positive when the origin is safe ($G(0) > 0$), and the estimate $P_f \approx \Phi(-\beta)$. Also return the unit normal $\alpha = -\nabla G(u^*)/\|\nabla G(u^*)\|$, whose squared entries $\alpha_k^2$ measure the importance of each input.

## The algorithm

```pseudo id=main
FORM(g, T, tol)
L1  u ← 0                                                     ▷ the mean point
L2  repeat
L3      G ← g(T(u));  ∇G ← gradient of g(T(·)) at u
L4      u_new ← ((∇G^T u - G) / ‖∇G‖^2) ∇G                   ▷ HL-RF step
L5  until ‖u_new - u‖ ≤ tol · max(1, ‖u_new‖);  u ← u_new
L6  β ← sign(G(0)) ‖u‖
L7  return β, P_f ≈ Φ(-β), u* = u, x* = T(u), α = -∇G / ‖∇G‖
```

Line L1 starts at the origin of standard normal space, which maps to the medians of the inputs. Line L3 evaluates the limit state and its gradient; the reference code uses central differences with step $10^{-6}$, which costs $2d$ evaluations, while large models use an [adjoint](/adjoint-sensitivity-analysis/) or [automatic differentiation](/automatic-differentiation/). Line L4 is the Hasofer-Lind-Rackwitz-Fiessler (HL-RF) step: it replaces $G$ by its linearization $G(u) + \nabla G^{\mathsf T}(v - u)$ and jumps to the point of the plane $\{v : \text{linearization} = 0\}$ closest to the origin. For a linear $G$ this is the answer after one step. Line L5 stops when the step is small; the reference code raises an error after 100 iterations. Line L6 gives $\beta$ its sign, and line L7 evaluates $\Phi(-\beta) = \frac{1}{2} \operatorname{erfc}(\beta / \sqrt{2})$, which keeps full relative accuracy in the far tail, where $1 - \Phi(\beta)$ would lose all digits.

## Example

**Lognormal resistance against a normal load.** Let $g = R - S$ with $\ln R \sim N(\ln 10, 0.2^2)$ and $S \sim N(5, 1.5^2)$. The exact value is $P_f = \int \phi_S(s) F_R(s)\, ds = 1.289177 \times 10^{-2}$, by a one dimensional integral. The HL-RF iterates are deterministic:

| step | $u_1$ ($R$) | $u_2$ ($S$) | $\|u\|$ | $G(u)$ |
|---|---|---|---|---|
| 1 | -1.600000 | 1.200000 | 2.0000000 | $4.6 \times 10^{-1}$ |
| 2 | -1.527591 | 1.577766 | 2.1961060 | $7.7 \times 10^{-4}$ |
| 3 | -1.539187 | 1.566886 | 2.1964124 | $2.0 \times 10^{-5}$ |
| 4 | -1.537375 | 1.568675 | 2.1964203 | $4.8 \times 10^{-7}$ |
| 6 | -1.537614 | 1.568440 | 2.1964205 | $2.9 \times 10^{-10}$ |

The first step is the exact answer for normal $R$; the rest corrects for the lognormal shape. At the design point $R = S = 7.353$, and $\alpha^2 = (0.490, 0.510)$, so both inputs matter about equally. FORM gives $\Phi(-2.196420) = 1.403 \times 10^{-2}$, 8.8 percent too high, and Breitung's formula gives $1.305 \times 10^{-2}$, 1.2 percent too high. A Monte Carlo estimate with the same 10 percent error would need about 8000 samples; FORM used 11 iterations of 5 evaluations each.

**A curved limit state.** Let $G(u) = 3 - u_1 + \frac{k}{2} u_2^2$ with standard normal $u$. For every $k \ge 0$ the design point is $(3, 0)$ and $\beta = 3$, so FORM always returns $\Phi(-3) = 1.349898 \times 10^{-3}$. The curvature of the surface at $u^*$ is $k$. The exact values come from a one dimensional integral; they are deterministic.

| $k$ | exact $P_f$ | FORM | error | Breitung | error |
|---|---|---|---|---|---|
| 0 | $1.349898 \times 10^{-3}$ | $1.349898 \times 10^{-3}$ | 0 | $1.349898 \times 10^{-3}$ | 0 |
| 0.05 | $1.250308 \times 10^{-3}$ | $1.349898 \times 10^{-3}$ | +8.0% | $1.258786 \times 10^{-3}$ | +0.7% |
| 0.1 | $1.168962 \times 10^{-3}$ | $1.349898 \times 10^{-3}$ | +15.5% | $1.183939 \times 10^{-3}$ | +1.3% |
| 0.2 | $1.043599 \times 10^{-3}$ | $1.349898 \times 10^{-3}$ | +29.4% | $1.067188 \times 10^{-3}$ | +2.3% |
| 0.5 | $8.208174 \times 10^{-4}$ | $1.349898 \times 10^{-3}$ | +64.5% | $8.537505 \times 10^{-4}$ | +4.0% |

FORM cannot see the curvature, so its error grows with $k$. Breitung's factor $(1 + 3k)^{-1/2}$ removes most of it.

## Correctness

Three statements are theorems; the proof file proves them. First, a fixed point of the HL-RF step with $G(u) = 0$ satisfies the optimality conditions of the design point problem: $u = \lambda \nabla G(u)$, the [KKT conditions](/kkt-conditions/) of $\min \frac{1}{2}\|u\|^2$ subject to $G(u) = 0$. Conversely, every regular point that satisfies them, with $G = 0$, is a fixed point. Second, if $G(u) = a_0 + a^{\mathsf T} u$ is linear, then one step from any start lands on $u^* = -a_0 a / \|a\|^2$, and $\Phi(-\beta)$ with $\beta = a_0 / \|a\|$ is the exact failure probability, because $a^{\mathsf T} u \sim N(0, \|a\|^2)$. Third, $\beta$ depends only on the failure set $\{G \le 0\}$, not on how $g$ is written: $g = R - S$, $\ln R - \ln S$ and $R/S - 1$ give the same $\beta$, which the tests check. This invariance is what Hasofer and Lind added over the earlier mean value indices.

Two statements are not theorems for general $g$. The HL-RF iteration need not converge: for strongly curved surfaces it can cycle, as Liu and Der Kiureghian showed, and a step size control on a merit function fixes this. And $\Phi(-\beta)$ is only a first-order approximation. Breitung proved that $P_f \sim \Phi(-\beta) \prod_{i=1}^{d-1} (1 + \beta \kappa_i)^{-1/2}$ as $\beta \to \infty$ with the products $\beta \kappa_i$ held fixed, which describes the error of FORM: it is small when $\beta \kappa_i$ is small. When the limit state has several design points of similar distance, FORM finds one of them and misses the others.

## Complexity

In the [real RAM](/real-ram/) model, each HL-RF iteration costs one evaluation of $g$ and a gradient. With central differences the gradient costs $2d$ evaluations, so the total is $O(K d C)$ for $K$ iterations; with an adjoint gradient it is $O(K C)$. The extra space is $O(d)$. $K$ is typically 5 to 20 for smooth problems, and it does not depend on the size of $P_f$, while [Monte Carlo integration](/monte-carlo-integration/) needs about $1/(P_f \varepsilon^2)$ samples for relative error $\varepsilon$. Breitung's correction adds a Hessian at the design point, $O(d^2)$ evaluations by differences, and an $O(d^3)$ determinant.

## Properties

- **Deterministic.** No sampling error; the error is the linearization error.
- **Cost independent of $P_f$.** The work does not grow as the failure probability shrinks.
- **Exact for linear limit states (theorem).** For $G$ linear in standard normal space, $\Phi(-\beta)$ is exact.
- **Invariant (theorem).** $\beta$ depends only on the failure set.
- **Sensitivities for free.** The entries $\alpha_k^2$ sum to 1 and rank the inputs; $\partial \beta / \partial \theta$ for a parameter $\theta$ follows from the gradient at $u^*$.
- **Local.** It sees the limit state only near one point.
- **Needs gradients.** $g$ must be differentiable near the design point.

## Variants and improvements

- **Second-order reliability method (SORM).** Fit a quadratic at $u^*$ and use Breitung's formula, or the later exact or improved formulas for a paraboloid. The reference code computes the curvature matrix in the tangent plane from a finite difference Hessian.
- **Improved HL-RF.** Use the HL-RF direction with a line search on a merit function, which makes the method converge for curved surfaces (Liu and Der Kiureghian).
- **General optimizers.** The design point problem is a constrained minimization; sequential quadratic programming or a [Newton](/newton-raphson-method/) method on the KKT system also work.
- **Dependent inputs.** Use the Rosenblatt or Nataf transform instead of the separate map of each marginal.
- **Importance sampling at the design point.** Sample from a normal law centered at $u^*$; the [importance sampling](/importance-sampling/) estimate corrects the FORM error at a modest cost.
- **System reliability.** For several failure modes, find a design point for each and combine the linearized events with a multinormal integral.

## When to use it

Use FORM when $P_f$ is small, each evaluation of $g$ is expensive, $g$ is smooth with gradients available, and the failure domain has one dominant design point. It is the standard method of structural reliability and of reliability based design. Check its answer with Breitung's correction or with importance sampling around $u^*$. Use [subset simulation](/subset-simulation/) when the limit state is strongly nonlinear, has several design points, or has no usable gradient, and plain [Monte Carlo](/monte-carlo-integration/) when $P_f$ is not small.

## Pitfalls

- **Curvature.** A curved limit state can make $\Phi(-\beta)$ wrong by a large factor, as the second table shows. Compute the SORM correction.
- **Several design points.** A failure domain with two regions of similar distance is underestimated by half or more. Restart from different points, or use a sampling method.
- **Non-convergence.** Plain HL-RF can oscillate. Monitor $G(u)$ and $\|u\|$, and switch to a line search.
- **Noisy gradients.** Finite differences of a model with solver noise give wrong directions. The stopping tolerance must be larger than the gradient noise; the reference code uses a relative $10^{-8}$ because its differences carry errors near $10^{-9}$.
- **Tail arithmetic.** Compute $\Phi(-\beta)$ with erfc, not as $1 - \Phi(\beta)$, which is 0 in double precision for $\beta$ above about 8.3.
- **Wrong transform.** Dependent inputs mapped as if independent give a wrong $\beta$. Use a transform that respects the joint law.

## Implementations

## History

Early reliability indices used the mean and standard deviation of $g$ and changed when $g$ was written in another form. Hasofer and Lind fixed this in 1974 by measuring the distance to the limit state surface in the space of standardized variables, which made the index depend only on the failure set. Rackwitz and Fiessler extended the method to non-normal inputs in 1978, with an equivalent normal transform and the iteration now called HL-RF. Breitung derived the asymptotic second-order formula in 1984. Liu and Der Kiureghian compared optimization algorithms for the design point in 1991 and gave a modified HL-RF method that converges where the plain one cycles. Ditlevsen and Madsen collected the theory in their 1996 book.

## References
