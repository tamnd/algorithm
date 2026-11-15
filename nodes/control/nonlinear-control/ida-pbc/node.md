---
tag: ST8SKY
kind: algorithm
slug: ida-pbc
name: Interconnection and damping assignment
aliases:
- IDA-PBC
area: control/nonlinear-control
level: research
summary: A passivity-based method that solves matching equations to give the closed loop a chosen port-Hamiltonian form with a minimum at the target.
model: real-ram
complexity:
  vars: {n: the dimension of the state, m: the number of inputs}
  time: {worst: "O(n^2 m + m^3)"}
  space: {extra: "O(n m + m^2)"}
properties: {deterministic: true, exact: true, recursive: false, online: true}
history:
  year: 2002
  people: [Romeo Ortega, Arjan van der Schaft, Bernhard Maschke, Gerardo Escobar]
  note: "Ortega, van der Schaft, Maschke and Escobar (2002) introduced the method for port-controlled Hamiltonian systems: choose the interconnection and damping of the closed loop, solve the matching equations for the energy, and use LaSalle for convergence."
prereqs: [port-hamiltonian-system, passivity-based-control, lasalle-invariance-principle]
see_also: [lyapunov-direct-method, hamiltonian-systems, passivity, dissipativity, pd-control-with-gravity-compensation, computed-torque-control, backstepping, feedback-linearization]
sources:
  - paper: doi:10.1016/S0005-1098(01)00278-3
    title: "Romeo Ortega, Arjan van der Schaft, Bernhard Maschke and Gerardo Escobar, Interconnection and damping assignment passivity-based control of port-controlled Hamiltonian systems, Automatica 38(4), 585-596, 2002"
    locator: "Proposition 1 and Section 3.1 (the matching equation and the conditions on the target system), Section 3.2 (the matching PDE), and the condition for asymptotic stability by LaSalle"
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.2, the invariance principle
---

Interconnection and damping assignment (IDA-PBC) is an algorithm of [passivity-based control](/passivity-based-control/) for plants written as a [port-Hamiltonian system](/port-hamiltonian-system/) $\dot x = (J - R) \nabla H + g u$. The designer does not choose the closed-loop energy directly. Instead, the designer chooses how energy should flow and be lost in the closed loop, the matrices $J_d$ and $R_d$, and then solves the matching equations, a set of partial differential equations, for an energy $H_d$ that has its minimum at the target. The control is the solution of a linear equation at each point. The closed loop is again port-Hamiltonian, its energy $H_d$ can only decrease, and the [LaSalle invariance principle](/lasalle-invariance-principle/) gives convergence. It handles systems with fewer actuators than states, such as electromechanical systems, where the energy cannot be changed in every direction.

## In plain words

A machine has an energy, and the energy flows between its parts and is lost in friction and resistance. You want the machine to rest at a new point. You cannot simply say what the new energy should be, because with few motors you cannot push in every direction. So you first decide how you would like the parts to pass energy to each other, and where you would like it to be lost. Then you look for an energy that fits this plan, using only the pushes your motors can make, and that has its lowest point where you want the machine to rest. If you find one, the controller makes the machine behave like a new machine with that energy, and the new machine slides down to the lowest point.

## The problem

**Input.** A plant $\dot x = (J(x) - R(x)) \nabla H(x) + g(x) u$ with $J = -J^T$, $R = R^T \succeq 0$, and $g(x)$ of full column rank $m$. A target point $x^*$. A choice of $J_d(x) = -J_d^T$ and $R_d(x) = R_d^T \succeq 0$, and an energy $H_d$ that solves the matching PDE

$$g^\perp(x) \left( (J_d - R_d) \nabla H_d - (J - R) \nabla H \right) = 0,$$

where $g^\perp$ is a full rank left annihilator of $g$, with $\nabla H_d(x^*) = 0$ and $\nabla^2 H_d(x^*) \succ 0$.

**Output.** The state feedback $u(x)$ such that the closed loop is $\dot x = (J_d - R_d) \nabla H_d$, or a report that the matching equation fails at $x$.

The hard part, solving the PDE, is a design step done once, by hand or with a computer algebra system. The algorithm below is what runs in the controller.

## The algorithm

```pseudo id=main
IDA-PBC-CONTROL(J - R, ∇H, g, J_d - R_d, ∇H_d, tol)
L1  a ← (J - R) ∇H
L2  c ← (J_d - R_d) ∇H_d
L3  w ← c - a
L4  u ← (gᵀ g)⁻¹ gᵀ w
L5  ρ ← w - g u
L6  if some |ρ_i| > tol then fail: the matching equation has no solution at x
L7  return u
```

All quantities are evaluated at the current state $x$. Lines L1 and L2 compute the plant and the target vector fields without input. Line L3 is what the input must supply. Line L4 is the least squares solution of $g u = w$, which is the exact solution when one exists. Lines L5 and L6 check the part of $w$ that the input cannot reach; it is zero exactly when $H_d$ solves the matching PDE at $x$. With exact data use $tol = 0$.

## Example

**Magnetic levitation.** A ball hangs under an electromagnet. The state is the flux $\lambda$, the height $\theta$ of the ball (up is positive, the coil is at $\theta = 1$) and the momentum $p$. The energy is $H = (1 - \theta) \lambda^2 / (2k) + p^2 / (2m) + m g_0 \theta$, the coil has resistance $r$, and the input is the voltage, so $J - R$ has rows $(-r, 0, 0)$, $(0, 0, 1)$, $(0, -1, 0)$ and $g = (1, 0, 0)^T$. The magnetic force $\lambda^2 / (2k)$ pulls the ball up; at rest it balances gravity, so $\lambda^* = \sqrt{2 k m g_0}$.

The plant has no input on $\theta$ and $p$, and no term that couples $\lambda$ to $p$ directly: the current changes the force only through $\lambda$. Choose $J_d - R_d$ with rows $(-r_d, 0, -\alpha)$, $(0, 0, 1)$, $(\alpha, -1, 0)$: the new term $\alpha$ couples flux and momentum. The matching PDE has two rows, and its solutions are

$$H_d = \frac{p^2}{2m} + \frac{\lambda^3}{6 k \alpha} - \frac{m g_0}{\alpha} \lambda + \Phi\left( \theta + \frac{\lambda}{\alpha} \right)$$

for any function $\Phi$. Choosing $\Phi(z) = (b/2)(z - z^*)^2$ with $z^* = \theta^* + \lambda^* / \alpha$ puts the minimum at $(\lambda^*, \theta^*, 0)$, and the first row gives

$$u = \frac{r (1 - \theta) \lambda}{k} - \frac{\alpha p}{m} - r_d \frac{\partial H_d}{\partial \lambda}.$$

Take $k = m = r = 1$, $g_0 = 2$, $\theta^* = 0.5$ (so $\lambda^* = 2$ and $u^* = 1$), and $\alpha = 2$, $b = 1$, $r_d = 2$. Start at rest with the flux of the target but the ball too low, $x(0) = (2, 0.3, 0)$, where $H_d - H_d^* = 0.02$. The simulation uses 4th order Runge-Kutta with step $0.01$, and the feedback is evaluated inside the right side.

| $t$ | $\lambda$ | $\theta$ | $p$ | $H_d - H_d^*$ | $u$ |
|---|---|---|---|---|---|
| 0 | 2 | 0.3 | 0 | 0.02 | 1.6 |
| 0.5 | 2.04738 | 0.30602 | 0.03189 | 0.01614 | 1.43149 |
| 1 | 2.03087 | 0.33331 | 0.07436 | 0.01468 | 1.29427 |
| 2 | 1.97975 | 0.41852 | 0.07840 | 0.007474 | 1.12631 |
| 4 | 1.99471 | 0.48943 | 0.00642 | 0.0001219 | 1.02937 |
| 10 | 1.99998 | 0.49982 | 0.00011 | 2.427e-8 | 1.00035 |

$H_d$ never increases (measured), and $H_d(T) - H_d(0) = -r_d \int_0^T (\partial_\lambda H_d)^2 dt$ holds within $10^{-8}$ (measured). The ball rises to $\theta^* = 0.5$ without overshoot, and the distance to $x^*$ stays below $0.01$ from $t = 4.34$ on. Theorem 6 of the proof shows that every motion that starts in the set $\{\lambda \ge 0, H_d - H_d^* \le c\}$ with $c < 4/3$ converges to $x^*$.

## Correctness

The full proof is in proofs/correctness.md. Its main steps:

- **Theorem (matching).** $g u = w$ has a solution if and only if $\rho = 0$ at line L5, because $g (g^T g)^{-1} g^T$ is the orthogonal projection onto the range of $g$. The solution is unique and is the $u$ of line L4. Then the closed loop equals the target system.
- **Theorem (energy decrease).** Since $J_d$ is skew, $\dot H_d = -\nabla H_d^T R_d \nabla H_d \le 0$. With a strict minimum of $H_d$ at $x^*$, this gives Lyapunov stability by the [Lyapunov direct method](/lyapunov-direct-method/).
- **Theorem (convergence).** On a compact positively invariant set where the only solution with $\nabla H_d^T R_d \nabla H_d \equiv 0$ is $x^*$, every motion converges to $x^*$ (LaSalle; Ortega et al. 2002, Proposition 1).
- **The example.** The proof solves the matching PDE by characteristics, shows the Hessian of $H_d$ has determinant $b \lambda / (k \alpha) \cdot (1/m)$ and is positive definite for $\lambda > 0$, builds the compact invariant set from convexity, and checks the LaSalle condition: $\partial_\lambda H_d \equiv 0$ forces $\frac{d}{dt} \partial_\lambda H_d = -\lambda p / (k m) = 0$, so $p = 0$ and then $x = x^*$. The tests check the matching, the energy identity and the LaSalle identity exactly in Fraction.

## Complexity

Count real operations at unit cost, as in the real RAM. Lines L1 and L2 cost $O(n^2)$ each. Forming $g^T g$ costs $O(n m^2)$, $g^T w$ costs $O(n m)$, and solving the $m \times m$ system costs $O(m^3)$. Line L5 costs $O(n m)$. The total per evaluation is $O(n^2 + n m^2 + m^3)$, which is within $O(n^2 m + m^3)$, plus the cost of $\nabla H$ and $\nabla H_d$. The extra space is $O(n m + m^2)$. If $g$ is constant, $(g^T g)^{-1} g^T$ can be computed once. The design step, solving the matching PDE, has no general bound: it may have no useful solution.

## Properties

- **Structure kept.** The closed loop is port-Hamiltonian with energy $H_d$, so it is passive from a new input to the output $g^T \nabla H_d$, and further passive loops can be added.
- **Energy as Lyapunov function.** $H_d - H_d^*$ is a Lyapunov function by construction; no separate search is needed.
- **Underactuation handled.** The matching PDE has $n - m$ rows. With full actuation ($m = n$) it is empty, and any $H_d$ works.
- **Not unique.** Different choices of $J_d$, $R_d$ and of the free function $\Phi$ give different controllers. The free function sets the shape of the energy and so the region of attraction.
- **Local or global.** The guaranteed region is a compact sublevel set of $H_d$. In the example it is local, because $H_d$ has the cubic term $\lambda^3$, but large: any $c$ below $4/3$.

## Variants and improvements

- **Fixing $J_d$ and $R_d$ first (non-parameterized).** The usual approach, as in the example: choose the matrices, then solve the PDE.
- **Fixing $H_d$ first (algebraic).** Choose $H_d$, and solve the matching equation for $J_d$ and $R_d$, which is then algebraic.
- **Mechanical systems.** For underactuated mechanical systems, $H_d$ has a kinetic and a potential part, and the matching PDE splits into one for the inertia matrix and one for the potential energy. This covers the cart-pole, the ball and beam, and similar systems.
- **Adding integral action or adaptation.** Add states to the controller to reject constant disturbances or estimate parameters, keeping the port-Hamiltonian form.
- **Damping injection only.** If $H$ already has its minimum at $x^*$, take $J_d = J$, $H_d = H$ and only increase $R$: this is the damping injection of the [port-Hamiltonian system](/port-hamiltonian-system/) page.

## When to use it

Use it for physical systems that have a clear energy, such as electromechanical systems, power converters, motors and mechanical systems, especially when they are underactuated, so that simple energy shaping does not apply. It is useful when you want a controller that keeps the physical meaning and gives a Lyapunov function for free. If the matching PDE has no solution you can find, or the plant has no natural energy, use [backstepping](/backstepping/) or [feedback linearization](/feedback-linearization/) instead. For a fully actuated robot arm, [PD control with gravity compensation](/pd-control-with-gravity-compensation/) is the simple special case.

## Pitfalls

- **The PDE is the real work.** Line L6 only checks the matching at one point. If $H_d$ does not solve the PDE everywhere, the controller fails at some states, or the closed loop is not the target.
- **No minimum at the target.** A solution of the PDE is useless unless the free function can place a strict minimum at $x^*$. Check the Hessian.
- **A non-constant $J_d$ or $R_d$ must keep the signs.** $J_d$ must be skew and $R_d$ positive semidefinite at every $x$, or $\dot H_d \le 0$ fails.
- **The LaSalle condition.** $R_d$ is usually only positive semidefinite, so $\dot H_d = 0$ on a set larger than $\{x^*\}$. Check that no other solution stays there, as in the example.
- **Model validity.** The levitation model needs $\theta < 1$. The region from the theory is a statement about the model, and it may include states the real system cannot reach.
- **Numerical residual.** With floating point data, set a small $tol$ at line L6; with $tol = 0$, rounding makes the check fail.

## Implementations

## History

Passivity-based control of Euler-Lagrange systems was developed in the 1980s and 1990s, mainly for robots and electrical machines. Port-controlled Hamiltonian systems, introduced by Maschke and van der Schaft in the early 1990s, gave a model class with the energy, the interconnection and the dissipation as separate objects. Ortega, van der Schaft, Maschke and Escobar (2002) used this structure to make the design systematic: assign the interconnection and the damping of the closed loop, solve the matching equations for the energy, and prove convergence with LaSalle. Later work applied it to underactuated mechanical systems, power electronics and electrical machines.

## References
