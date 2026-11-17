---
tag: JXS149
kind: model
slug: lotka-volterra-predator-prey
name: Lotka-Volterra predator-prey model
aliases:
- predator-prey equations
area: biology/epidemic-and-ecological-models
level: intro
summary: Prey grow and are eaten in proportion to encounters, and predators grow from what they eat, which gives closed neutral cycles.
history:
  year: 1925
  people: [Alfred J. Lotka, Vito Volterra]
  note: Lotka gave the equations in his 1925 book, and Volterra found them on his own in 1926 to explain the fish catches of the Adriatic.
prereqs: [ode-initial-value-problem, jacobian-linearization]
see_also: [lotka-volterra-competition, holling-functional-response, logistic-growth-model, lyapunov-function, limit-cycle, poincare-bendixson-theorem, classical-runge-kutta-4, kermack-mckendrick-sir-model]
sources:
  - book: "Alfred J. Lotka, Elements of Physical Biology, Williams and Wilkins, Baltimore, 1925"
    title: Lotka 1925
    locator: the equations for a species that feeds on another, and their periodic solutions
  - paper: doi:10.1038/118558a0
    title: Vito Volterra, Fluctuations in the abundance of a species considered mathematically, Nature 118(2972), 1926
    locator: pages 558 to 560 (the equations, the periodic fluctuations, the law of the averages and the effect of fishing)
  - book: isbn:9780387952239
    title: James D. Murray, Mathematical Biology I, An Introduction, third edition, Springer, 2002
    locator: Chapter 3, Models for Interacting Populations (the Lotka-Volterra system, its first integral, and realistic predator-prey models)
---

The Lotka-Volterra predator-prey model is the pair of differential equations $\dot x = a x - b x y$, $\dot y = c x y - d y$ for the densities of a prey $x$ and a predator $y$. Prey grow exponentially when alone and are eaten at a rate proportional to the number of encounters. Predators grow from what they eat and die at a constant rate. Lotka (1925) and Volterra (1926) found the model on their own. Every positive solution is periodic: the populations cycle on closed curves around one equilibrium, and the size of the cycle depends only on the start.

## The machine

**The state.** $x(t) \ge 0$ is the prey density and $y(t) \ge 0$ is the predator density, as numbers or biomass per unit of area. Both are real numbers.

**The parameters.** All four are positive.

- $a$, in 1 per time: the growth rate of the prey with no predators.
- $b$, in 1 per (predator density times time): the rate at which one predator kills prey, per unit of prey density.
- $c$, in 1 per (prey density times time): the growth of the predator per unit of prey density. If a fraction $e$ of the eaten prey is turned into predators, then $c = e b$ when both are counted in the same unit.
- $d$, in 1 per time: the death rate of the predator with no prey.

**The equations.**

$$\frac{dx}{dt} = a x - b x y, \qquad \frac{dy}{dt} = c x y - d y.$$

**The assumptions.** Without predators the prey grow without bound, at the rate $a$. Without prey the predators die out, at the rate $d$. Prey and predators meet at random, so the kill rate is proportional to $x y$ (mass action). Each predator eats $b x$ prey per unit of time, without limit, so there is no satiation and no handling time; this is the type I response of the [Holling functional response](/holling-functional-response/). Births follow kills at once, with no delay. Both populations are well mixed, have no age structure and are large enough for a deterministic description.

**A numerical solution.** The equations have no closed form in elementary functions. The implementation uses fixed-step [RK4](/classical-runge-kutta-4/) and checks the conserved quantity $V$ below.

```pseudo id=main
LV-RK4(x0, y0, dt, steps)              ▷ F(x, y) = (a x - b x y, c x y - d y)
L1  (x, y) ← (x0, y0)
L2  repeat steps times
L3      k1 ← F(x, y)
L4      k2 ← F((x, y) + dt k1 / 2)
L5      k3 ← F((x, y) + dt k2 / 2)
L6      k4 ← F((x, y) + dt k3)
L7      (x, y) ← (x, y) + dt (k1 + 2 k2 + 2 k3 + k4) / 6
L8  return the list of states
```

Each step costs four evaluations of $F$, so a run to time $T$ costs $O(T/dt)$ operations. With $dt = 0.01$ the value of $V$ changes by less than $10^{-9}$ over 4 periods in the example below.

## What it counts

- The equilibria: the extinction point $(0, 0)$ and the coexistence point $(x^*, y^*) = (d/c,\ a/b)$.
- The orbit through a start point, which is the level curve of $V$ through it, and its period.
- The time averages of $x$ and $y$ over one period.
- The response of the averages to a harvest of both species.

**An example.** Take $a = 1$, $b = 0.1$, $c = 0.02$ and $d = 0.5$, in arbitrary time units. The coexistence point is $(25, 10)$. The orbit from $(40, 10)$ has $V = -2.347025$, against the minimum $V(25, 10) = -2.412023$. On this orbit $x$ moves between $14.32$ and $40$ and $y$ between $6.81$ and $14.05$. Prey peak first, and predators peak about a quarter of a cycle later. The period depends on the size of the orbit:

| start $(x_0, 10)$ | 25.5 | 30 | 40 | 60 | 100 |
|---|---|---|---|---|---|
| period | 8.886 | 8.905 | 9.031 | 9.477 | 10.751 |

The small orbits have the period $2\pi/\sqrt{ad} = 8.886$ of the linearization. The orbit from $(100, 10)$ takes the prey down to $1.98$ and the predators down to $2.01$, values at which a real population of a few individuals can die out by chance.

## Relation to other models

- **Prey with a carrying capacity.** Replace $a x$ by $a x (1 - x/K)$, the [logistic growth model](/logistic-growth-model/). If $d/c < K$, the cycles disappear and every positive solution spirals into one equilibrium (proof below). The closed orbits of the classical model are fragile.
- **Predators with satiation.** Replace $b x y$ by a type II [Holling functional response](/holling-functional-response/) $b x y / (1 + b h x)$. With logistic prey this gives a model in which a stable [limit cycle](/limit-cycle/) can appear: an isolated cycle whose amplitude does not depend on the start. The [Poincaré-Bendixson theorem](/poincare-bendixson-theorem/) is the usual tool to prove that such a cycle exists.
- **[Lotka-Volterra competition](/lotka-volterra-competition/).** It uses the same quadratic interaction terms with negative signs on both, for two species that harm each other. It has no closed orbits.
- **The SIR model.** The [Kermack-McKendrick SIR model](/kermack-mckendrick-sir-model/) has the same mass-action product $S I$, with the susceptibles as the prey that are not replaced. Without births, it has one epidemic wave and no cycles.
- **Many species.** The generalized Lotka-Volterra equations $\dot x_i = x_i (r_i + \sum_j a_{ij} x_j)$ hold both cases above for $n$ species.
- **Stochastic versions.** In a model with individual births, deaths and kills, the quantity $V$ is no longer conserved. Nothing pulls the state back to one cycle, so the amplitude drifts at random. A large cycle takes a species down to a few individuals, where it can die out by chance.

## Known results in the model

**The first integral.** The function

$$V(x, y) = c x - d \ln x + b y - a \ln y$$

is constant along each solution with $x, y > 0$.

*Proof.* By the chain rule, $\frac{dV}{dt} = \left(c - \frac{d}{x}\right)\dot x + \left(b - \frac{a}{y}\right)\dot y$. Since $\dot x = x(a - b y)$ and $\dot y = y(c x - d)$, this is $(c x - d)(a - b y) + (b y - a)(c x - d) = 0$. $\square$

**Every positive solution is periodic.** If $x_0, y_0 > 0$ and $(x_0, y_0) \ne (x^*, y^*)$, the solution is periodic, and its orbit is the closed curve $\{V = V(x_0, y_0)\}$.

*Proof.* The axes are invariant: $x = 0$ gives $\dot x = 0$, and $y = 0$ gives $\dot y = 0$. So a positive solution stays positive. Write $V(x, y) = g(x) + h(y)$ with $g(x) = c x - d \ln x$ and $h(y) = b y - a \ln y$. The function $g$ is strictly convex on $(0, \infty)$, with its only minimum at $x = d/c$, and $g(x) \to \infty$ as $x \to 0$ or $x \to \infty$; the same holds for $h$ with its minimum at $y = a/b$. So $V$ is strictly convex with one minimum at $(x^*, y^*)$, and each level set $\{V = v\}$ with $v > V(x^*, y^*)$ is a closed bounded convex curve. Each vertical line meets it in at most two points, and so does each horizontal line. The solution stays on this curve, and the curve holds no equilibrium, because the only positive equilibrium is the minimum point. The speed $|(\dot x, \dot y)|$ is continuous and positive on the compact curve, so it has a positive minimum, and the solution moves around the whole curve in finite time. When it comes back to its start, it repeats, because the equation is autonomous. $\square$

**The linearization is a center.** The [Jacobian](/jacobian-linearization/) at $(x^*, y^*)$ is

$$J = \begin{pmatrix} 0 & -b d / c \\ a c / b & 0 \end{pmatrix},$$

with the eigenvalues $\pm i \sqrt{a d}$. So small orbits are close to ellipses with the period $2\pi/\sqrt{a d}$. The linearization alone does not prove that the orbits are closed, because a center of the linear system can be a spiral of the nonlinear one; the first integral proves it.

**The period grows with the amplitude.** The table above shows it for the example: the period increases from $8.886$ for small orbits to $10.751$ for the orbit from $(100, 10)$. This is a measurement with RK4 and $dt = 0.01$, not a closed form.

**The law of the averages (Volterra).** Over one period $T$ of any positive solution, the time averages are the equilibrium values:

$$\frac{1}{T}\int_0^T x\,dt = \frac{d}{c}, \qquad \frac{1}{T}\int_0^T y\,dt = \frac{a}{b}.$$

*Proof.* $\frac{d}{dt}\ln x = a - b y$. Integrate from 0 to $T$. The left side is $\ln x(T) - \ln x(0) = 0$, because the solution is periodic. So $0 = a T - b \int_0^T y\,dt$. The same step with $\frac{d}{dt}\ln y = c x - d$ gives the average of $x$. $\square$

**Harvesting raises the prey (Volterra's principle).** Remove both species at the same per capita rate $\varepsilon$, with $0 < \varepsilon < a$. The equations become $\dot x = (a - \varepsilon) x - b x y$ and $\dot y = c x y - (d + \varepsilon) y$, so the averages become $(d + \varepsilon)/c$ for the prey and $(a - \varepsilon)/b$ for the predator. Harvest increases the mean prey and decreases the mean predator. Volterra used this to explain why the share of predatory fish in the Adriatic catches rose when fishing stopped during the First World War.

**With logistic prey, the coexistence point attracts.** Take $\dot x = a x (1 - x/K) - b x y$ and $\dot y = c x y - d y$ with $x^* = d/c < K$. Then $y^* = \frac{a}{b}\left(1 - \frac{x^*}{K}\right) > 0$, and every solution with $x_0, y_0 > 0$ tends to $(x^*, y^*)$.

*Proof.* Let $W(x, y) = c x - d \ln x + b y - b y^* \ln y$. As above, $\frac{dW}{dt} = (c x - d)\left(a - \frac{a x}{K} - b y\right) + (b y - b y^*)(c x - d) = (c x - d)\left(a - \frac{a x}{K} - b y^*\right)$. Since $a - b y^* = a x^*/K$, the last factor is $\frac{a}{K}(x^* - x)$, and $\frac{dW}{dt} = -\frac{a}{cK}(c x - d)^2 \le 0$. So $W$ is a [Lyapunov function](/lyapunov-function/). Its sublevel sets in the open quadrant are compact, as in the proof above, so each solution is bounded and stays away from the axes. By LaSalle's invariance principle, the solution tends to the largest invariant set inside $\{\dot W = 0\} = \{x = x^*\}$. On the line $x = x^*$, $\dot x = 0$ forces $y = y^*$. So that set is the point $(x^*, y^*)$. $\square$

In the example with $K = 100$, the solution from $(40, 10)$ spirals into $(25, 7.5)$.

**Structural instability.** The two results above show that the closed orbits are not robust. A small self-limitation of the prey, of any size $1/K > 0$ with $d/c < K$, turns every cycle into a spiral. Cycles that are seen in real predator and prey data need a model in which they are robust, such as a limit cycle.

## References
