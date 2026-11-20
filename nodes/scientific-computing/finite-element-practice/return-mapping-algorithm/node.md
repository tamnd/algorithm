---
tag: PD9SMC
kind: algorithm
slug: return-mapping-algorithm
name: Return mapping algorithm
aliases:
- radial return algorithm
- radial return mapping
area: scientific-computing/finite-element-practice
level: advanced
summary: Integrates elastoplastic laws at each quadrature point by an elastic trial stress followed by a projection back to the yield surface.
model: real-ram
complexity:
  vars: {q: the number of quadrature points, n: the number of strain increments}
  time: {worst: "Θ(n q)"}
  space: {extra: "Θ(q)"}
properties: {deterministic: true, iterative: false, closed_form_for_linear_hardening: true, exact_for_backward_euler_equations: true, order_of_accuracy: "first order in the strain increment for nonproportional paths", consistent_tangent: true}
history:
  year: 1964
  people: [M. L. Wilkins, R. D. Krieg, J. C. Simo, R. L. Taylor, T. J. R. Hughes]
  note: Wilkins in 1964 brought the stress back to the von Mises surface along the radius. Simo and Taylor in 1985 derived the tangent that is consistent with the discrete map, which gives quadratic convergence of the global Newton method.
prereqs: [backward-euler-method, newton-method-for-systems, finite-element-method]
see_also: [arc-length-method, newmark-beta-method, finite-element-assembly, gaussian-quadrature, proximal-operator, differential-algebraic-equations]
sources:
  - book: isbn:9780387975207
    title: J. C. Simo and T. J. R. Hughes, Computational Inelasticity, Springer, 1998
    locator: Chapter 1 (the one-dimensional return mapping) and Chapter 3 (radial return for J2 flow theory and its consistent tangent)
  - paper: doi:10.1016/0045-7825(85)90070-2
    title: J. C. Simo and R. L. Taylor, Consistent tangent operators for rate-independent elastoplasticity, Computer Methods in Applied Mechanics and Engineering 48(1) (1985) 101-118
    locator: the tangent obtained by linearizing the discrete return map, and the quadratic convergence of the global Newton method
  - paper: doi:10.1115/1.3454568
    title: R. D. Krieg and D. B. Krieg, Accuracies of numerical solution methods for the elastic-perfectly plastic model, Journal of Pressure Vessel Technology 99(4) (1977) 510-515
    locator: the accuracy of radial return and of other integration methods for von Mises plasticity
  - paper: doi:10.1002/nme.1620230303
    title: M. Ortiz and J. C. Simo, An analysis of a new class of integration algorithms for elastoplastic constitutive relations, International Journal for Numerical Methods in Engineering 23(3) (1986) 353-366
    locator: the cutting plane variant, which needs no second derivatives of the yield function
---

The return mapping algorithm computes the stress at one quadrature point of a finite element model with elastoplastic material. It gets the total strain at the end of a load step and the plastic state at the start of the step. First it assumes that the step is elastic and computes a trial stress. If the trial stress is inside the yield surface, the step is elastic and the trial stress is the answer. If not, it moves the stress back onto the yield surface and updates the plastic strain and the hardening variables. The result is the exact solution of the [backward Euler](/backward-euler-method/) equations of the flow rule for this step. For von Mises (J2) plasticity with linear hardening the projection is along the radius of the yield cylinder, so the map is in closed form. The derivative of the map is the consistent tangent. With it, the global [Newton iteration](/newton-method-for-systems/) converges quadratically.

## In plain words

Think of a metal bar that you stretch in small steps. In each step, first pretend that the bar is a spring and compute the force from the stretch. If this force is below what the metal can carry, it is the right answer. If it is above, the metal must have flowed. Then pull the force back down to what the metal can carry, and record how much of the stretch became permanent. In three dimensions, the pull back goes straight toward the centre of a circle of allowed stresses, so one division gives the answer. The method also tells the solver how the force changes when the stretch changes. This lets the solver of the whole structure converge in very few steps.

## The problem

**Input.** At one quadrature point: the total strain $\varepsilon_{n+1}$ at the end of the step, the plastic state at the start of the step (plastic strain $\varepsilon^p_n$, equivalent plastic strain $\alpha_n$, back stress $\beta_n$), the bulk modulus $\kappa$, the shear modulus $\mu$, the initial yield stress $\sigma_y > 0$, the isotropic hardening modulus $K \ge 0$ and the kinematic hardening modulus $H \ge 0$.

**Output.** The stress $\sigma_{n+1}$, the new state $(\varepsilon^p_{n+1}, \alpha_{n+1}, \beta_{n+1})$ and the tangent $C_{n+1} = \partial \sigma_{n+1} / \partial \varepsilon_{n+1}$, such that the backward Euler equations hold:

$$\sigma_{n+1} = \kappa\,(\mathrm{tr}\,\varepsilon_{n+1})\,I + 2\mu\,(\mathrm{dev}\,\varepsilon_{n+1} - \varepsilon^p_{n+1}), \qquad \varepsilon^p_{n+1} = \varepsilon^p_n + \Delta\gamma\,\hat n,$$

$$\alpha_{n+1} = \alpha_n + \sqrt{2/3}\,\Delta\gamma, \qquad \beta_{n+1} = \beta_n + \tfrac23 H\,\Delta\gamma\,\hat n, \qquad \hat n = \frac{\xi_{n+1}}{|\xi_{n+1}|}, \quad \xi_{n+1} = \mathrm{dev}\,\sigma_{n+1} - \beta_{n+1},$$

with the yield function $f = |\xi| - \sqrt{2/3}\,(\sigma_y + K\alpha)$ and the loading conditions

$$\Delta\gamma \ge 0, \qquad f_{n+1} \le 0, \qquad \Delta\gamma\,f_{n+1} = 0.$$

Here $|\cdot|$ is the Frobenius norm. The flow rule is a differential equation with an inequality constraint in time. Backward Euler replaces it by the equations above, which have one unknown scalar $\Delta\gamma$ after the elimination of the others. The one-dimensional model is the same with $\sigma = E(\varepsilon - \varepsilon^p)$, $f = |\sigma - q| - (\sigma_y + K\alpha)$ and no factors $\sqrt{2/3}$ and $\tfrac23$.

## The algorithm

```pseudo id=main
RADIAL-RETURN(eps, eps_p, alpha, beta, kappa, mu, sigma_y, K, H)
L1  s_tr <- 2 mu (dev eps - eps_p); xi_tr <- s_tr - beta          ▷ elastic trial stress
L2  f_tr <- |xi_tr| - sqrt(2/3) (sigma_y + K alpha)
L3  if f_tr <= 0 then
L4      return sigma = s_tr + kappa (tr eps) I, the old state, the elastic tangent
L5  dgamma <- f_tr / (2 mu + 2/3 (K + H)); n <- xi_tr / |xi_tr|
L6  sigma <- s_tr - 2 mu dgamma n + kappa (tr eps) I                ▷ radial return
L7  eps_p <- eps_p + dgamma n; alpha <- alpha + sqrt(2/3) dgamma; beta <- beta + 2/3 H dgamma n
L8  C <- kappa I (x) I + 2 mu theta I_dev - 2 mu theta_bar n (x) n; return sigma, the new state, C
```

In line L8, $\theta = 1 - 2\mu\,\Delta\gamma/|\xi_{\rm tr}|$ and $\bar\theta = 1/(1 + (K + H)/(3\mu)) - (1 - \theta)$, $I \otimes I$ maps a strain to its trace times $I$, and $I_{\rm dev}$ maps a symmetric strain to its deviator.

The pressure $\kappa\,\mathrm{tr}\,\varepsilon$ is always elastic, because the plastic strain is deviatoric. In the one-dimensional map (`return_map_1d`), line L5 is $\Delta\gamma = f_{\rm tr}/(E + K + H)$, line L6 is $\sigma = \sigma_{\rm tr} - E\,\Delta\gamma\,\mathrm{sign}(\xi_{\rm tr})$ and the tangent of line L8 is $E(K + H)/(E + K + H)$.

The finite element code calls this map at every quadrature point in every global Newton iteration. Each call starts from the state of the last converged load step, never from the state of the last iteration. The state is stored only when the global iteration converges.

## Example

**One dimension, exact numbers.** Take $E = 100$, $\sigma_y = 1$, $K = 10$, $H = 0$, the virgin state and the strain $\varepsilon = 0.03$. Line L1 gives $\sigma_{\rm tr} = 3$ and line L2 gives $f_{\rm tr} = 3 - 1 = 2 > 0$, so the step is plastic. Line L5 gives $\Delta\gamma = 2/110 = 1/55$. Line L6 gives $\sigma = 3 - 100/55 = 13/11$. The new state is $\varepsilon^p = \alpha = 1/55$, and the new yield stress is $1 + 10/55 = 13/11$, so the stress is on the yield surface. The tangent is $100 \cdot 10/110 = 100/11$. The bilinear stress strain curve has yield strain $0.01$ and slope $100/11$ after yield, so it gives $\sigma = 1 + (100/11)(0.02) = 13/11$. The reference code returns exactly these fractions (`test_1d_exact_fractions`). For monotone loading the one-dimensional map gives the exact curve for any number of steps.

**Kinematic hardening and the Bauschinger effect.** With $K = 0$ and $H > 0$, the elastic range keeps its width $2\sigma_y$ and moves with the back stress. After loading to $\sigma_{\max}$ the bar unloads elastically until $\sigma_{\max} - 2\sigma_y$ and then yields in compression. The tests check this.

**Three dimensions, a path that turns.** Take $\kappa = 160$, $\mu = 80$, $\sigma_y = 0.25$, $K = 10$ and $H = 5$. The strain has the fixed normal part $\mathrm{diag}(0.004, -0.002, -0.002)$ and a shear part $\varepsilon_{12} = 0.006\,t$, and it is sampled at $t = k/m$ for $k = 1, \ldots, m$, starting from the virgin state. The direction of the deviatoric stress turns during the path, so the result depends on the number of steps $m$. The table gives the largest stress error against $m = 20480$ steps, where $\sigma_{12} = 0.20929$.

| steps $m$ | $\sigma_{12}$ | largest error |
|---|---|---|
| 1 | 0.17412 | 0.10 |
| 20 | 0.20778 | $1.75 \times 10^{-3}$ |
| 40 | 0.20852 | $7.91 \times 10^{-4}$ |
| 80 | 0.20890 | $3.91 \times 10^{-4}$ |
| 160 | 0.20909 | $1.96 \times 10^{-4}$ |

The error halves when the step halves, so the map is first order on this path. On a proportional path, where the direction $\hat n$ stays fixed, one step and 40 steps give the same stress to $10^{-12}$.

**A bar in series.** Four bar elements with areas $1, 0.8, 1.2, 1$ and length 1 are fixed at one end and pulled $0.02$ at the other, with $E = 200$ and the same yield data. All four yield. Newton's method with the consistent tangent converges in 2 iterations: the response is piecewise linear, so one iteration finds the right branch in every element and the next is exact. With the elastic modulus as the tangent the same tolerance needs 361 iterations.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md).

- **The map solves the backward Euler equations, and the solution is unique (theorem).** Elimination shows that $\xi_{n+1}$ is a positive multiple of $\xi_{\rm tr}$, so $\hat n = \xi_{\rm tr}/|\xi_{\rm tr}|$ and $f_{n+1} = f_{\rm tr} - (2\mu + \tfrac23(K + H))\Delta\gamma$. The loading conditions then leave one choice: $\Delta\gamma = 0$ if $f_{\rm tr} \le 0$ and line L5 if not.
- **The stress is the closest point (theorem, perfect plasticity).** For $K = H = 0$ the deviatoric stress of line L6 is the point of the ball $|s - \beta| \le \sqrt{2/3}\,\sigma_y$ that is closest to $s_{\rm tr}$.
- **The tangent of line L8 is the exact derivative of the map (theorem).** At a plastic point with $f_{\rm tr} > 0$, differentiating lines L1, L5 and L6 gives $C$. A finite difference test in the reference code agrees with it.
- **This is exactness for the discrete equations, not for the flow rule.** The backward Euler equations differ from the continuum law on paths where $\hat n$ turns. Then the error is first order in the step (measured above). On proportional paths and for monotone loading in one dimension, the map is exact for the continuum law.

## Complexity

In the [real-RAM model](/real-ram/), one call does a fixed number of operations: a deviator, one norm, one division and the 81 entries of the tangent. So $n$ strain increments at $q$ quadrature points cost $\Theta(n q)$ calls of constant cost, if each increment needs one global iteration. With $j$ global Newton iterations per increment the cost is $\Theta(n q j)$, and the consistent tangent keeps $j$ small. The history is three tensors and one scalar per point, so the extra space is $\Theta(q)$.

## Properties

- **No local iteration for linear hardening.** The scalar equation for $\Delta\gamma$ is linear. With nonlinear isotropic hardening it is a scalar nonlinear equation, which local Newton iterations solve.
- **Unconditionally stable.** Any step size gives a stress on or inside the yield surface, and the loading conditions hold exactly.
- **The consistent tangent is symmetric** for associative J2 plasticity, and it differs from the continuum elastoplastic tangent by the factor $\theta < 1$ on the deviatoric part. The two agree only as $\Delta\gamma \to 0$.
- **The volume change is elastic.** The pressure never needs a correction.

## Variants and improvements

- **Closest point projection.** For a general convex yield function, the same backward Euler equations need a local Newton iteration on $(\sigma, \Delta\gamma)$, with the second derivatives of the yield function.
- **Cutting plane (Ortiz and Simo 1986).** Iterate with explicit corrections that need only the gradient of the yield function. It is cheaper per iteration, but its tangent is not consistent.
- **Generalized midpoint rule.** Evaluate the flow direction at $\varepsilon_{n+\vartheta}$. With $\vartheta = \tfrac12$ it is second order on smooth paths, but each step needs a local iteration even for linear hardening.
- **Finite strain.** With a multiplicative split of the deformation gradient and logarithmic strains, the same radial return applies to the logarithms of the principal elastic stretches.
- **Viscoplasticity.** For the overstress law $\dot\gamma = f/\eta$ of Perzyna type, backward Euler adds $\eta/\Delta t$ to the denominator of line L5. As $\eta \to 0$ the plastic map comes back.

## When to use it

Use it in every implicit finite element code for metal plasticity, and as the model for other constitutive updates with an inequality constraint, such as damage, friction and Drucker Prager or Mohr Coulomb soil plasticity. With J2 plasticity and linear hardening the closed form is the standard choice. Use a closest point projection with local iterations for curved or anisotropic yield surfaces. In explicit dynamics the consistent tangent is not needed, but the return map itself is the same.

## Pitfalls

- **Updating the history during the global iteration.** The map must start every iteration from the converged state of the last step. If not, the plastic strain accumulates spurious increments and the solution depends on the number of iterations.
- **Using the continuum tangent.** It drops the factor $\theta$ and destroys quadratic convergence. With the elastic tangent the global iteration converges only linearly, as in the bar example.
- **Engineering shear strains.** Codes in Voigt notation store $2\varepsilon_{12}$. The norm and the tangent then need factors of 2, and a missing factor changes the yield point in shear.
- **A zero trial deviator.** If $\xi_{\rm tr} = 0$ the direction is not defined. The step is then elastic, because $f_{\rm tr} = -\sqrt{2/3}(\sigma_y + K\alpha) < 0$, so the code never divides by zero as long as $\sigma_y > 0$.
- **Large steps on turning paths.** The map is stable for any step, but the stress after a nonproportional path has a first order error. Exactness for the discrete equations does not mean accuracy for the material law.

## Implementations

## History

Wilkins in 1964 brought the stress back to the von Mises surface along the radius in his hydrodynamic codes, which gave radial return its name. Krieg and Krieg in 1977 compared the accuracy of radial return with other integration methods for perfect plasticity. Simo and Taylor in 1985 showed that the tangent must be the derivative of the discrete map, and that with this consistent tangent the global Newton method converges quadratically. Ortiz and Simo in 1986 analysed the cutting plane variant. Simo and Hughes in 1998 put the theory of return mapping, closest point projection and their tangents into one book.

## References
