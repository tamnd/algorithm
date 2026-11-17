---
tag: V9BBX4
kind: definition
slug: holling-functional-response
name: Holling functional response
aliases:
- Holling type II response
area: biology/epidemic-and-ecological-models
level: core
summary: 'The rate at which a predator eats as a function of prey density: linear, saturating or sigmoid, for types I, II and III.'
history:
  year: 1959
  people: [Crawford S. Holling]
  note: Holling (1959) classified the responses from data on small mammals that eat sawfly cocoons, and derived the saturating form from search and handling time in an experiment with sandpaper discs.
prereqs: [lotka-volterra-predator-prey]
see_also: [lotka-volterra-predator-prey, michaelis-menten-kinetics, hill-equation, limit-cycle, poincare-bendixson-theorem, competitive-exclusion-principle, logistic-growth-model, jacobian-linearization]
sources:
  - paper: doi:10.4039/Ent91293-5
    title: Crawford S. Holling, The components of predation as revealed by a study of small-mammal predation of the European pine sawfly, The Canadian Entomologist 91(5), 1959
    locator: pages 293 to 320 (the functional and numerical responses, and the three shapes of the functional response)
  - paper: doi:10.4039/Ent91385-7
    title: Crawford S. Holling, Some characteristics of simple types of predation and parasitism, The Canadian Entomologist 91(7), 1959
    locator: pages 385 to 398 (the experiment with discs and the equation for the saturating response from search and handling time)
  - book: isbn:9780387952239
    title: James D. Murray, Mathematical Biology I, An Introduction, third edition, Springer, 2002
    locator: Chapter 3, Models for Interacting Populations (realistic predator-prey models with a saturating predation term)
---

A functional response is the rate at which one predator eats prey, written as a function $f(N)$ of the prey density $N$. Holling (1959) sorted the responses that are seen in data into three types: type I rises linearly, type II rises and then saturates, and type III has an S shape. The saturating type II follows from one assumption: a predator that handles a prey cannot search for the next one. The type changes the dynamics of a predator-prey model. A linear response gives the neutral cycles of the [Lotka-Volterra model](/lotka-volterra-predator-prey/); a saturating response can turn a stable equilibrium into a [limit cycle](/limit-cycle/).

## Definition

**Functional response.** Let one predator live among prey at the constant density $N \ge 0$, in prey per unit of area. Its **functional response** $f(N)$ is the long-run number of prey it eats per unit of time. It is a property of the predator alone, at a fixed prey density. The term is separate from the **numerical response**, which is the change in the number of predators (by births, deaths or movement) as the prey density changes.

The three Holling types use two parameters:

- the **attack rate** $a > 0$, in area per time: the area that a searching predator clears of prey per unit of time;
- the **handling time** $h > 0$, in time per prey: the time to catch, eat and digest one prey, during which the predator does not search.

**Type I (linear).**

$$f_{\mathrm{I}}(N) = a N.$$

In some uses the line is cut off at a maximum rate. This is the term $b x$ per predator of the Lotka-Volterra model.

**Type II (saturating).**

$$f_{\mathrm{II}}(N) = \frac{a N}{1 + a h N}.$$

**Type III (sigmoid).** The attack rate itself grows with prey density, as $a N$ in place of $a$, for example because the predator learns to find the prey or switches to it from other food. Here $a$ has the unit area squared per (prey times time). Then

$$f_{\mathrm{III}}(N) = \frac{a N^2}{1 + a h N^2}.$$

**Derivation of type II from the time budget.** Watch one predator for a time $T$. Split it into the search time $T_s$ and the handling time $T_h$, so $T = T_s + T_h$. While it searches, the predator meets prey at the rate $a N$, so it catches $C = a N T_s$ prey. Each catch takes the time $h$, so $T_h = h C$. Then

$$T = \frac{C}{a N} + h C, \qquad \text{so} \qquad \frac{C}{T} = \frac{a N}{1 + a h N}.$$

This is Holling's disc equation. In his experiment, a blindfolded person searched for sandpaper discs on a table by touch and put each disc aside after it was found, and the number of discs found in a fixed time fitted this curve.

**The same result as a renewal process.** Let the search time to the next prey be random with the mean $1/(aN)$, and let each handling take the time $h$. One cycle of search and handling takes the mean time $1/(aN) + h$ and gives one prey. By the renewal reward theorem, the long-run rate is $1 / (1/(aN) + h) = aN/(1 + ahN)$. So the formula also holds when the search times are random.

**Properties.**

| | type I | type II | type III |
|---|---|---|---|
| $f(N)$ for small $N$ | $a N$ | $\approx a N$ | $\approx a N^2$ |
| limit as $N \to \infty$ | no limit | $1/h$ | $1/h$ |
| half of the maximum at | | $N = 1/(ah)$ | $N = 1/\sqrt{ah}$ |
| risk per prey $f(N)/N$ | constant $a$ | falls: $a/(1 + ahN)$ | rises for $N < 1/\sqrt{ah}$, then falls |
| shape | line | concave | convex, then concave |

The risk per prey is the column that matters for the prey. With type II, a prey is safer when there are many prey, so the predator cannot hold the prey at a low density. With type III, the risk rises with $N$ at low density, so predation pushes a rare prey back up.

## Examples and non-examples

**A worked example.** Take $a = 2$ and $h = 0.25$. The maximum rate is $1/h = 4$ prey per unit of time, and type II reaches half of it at $N = 1/(ah) = 2$.

| $N$ | 1 | 2 | 4 | 8 | 100 |
|---|---|---|---|---|---|
| $f_{\mathrm{II}}(N) = 2N/(1 + 0.5 N)$ | 1.333 | 2 | 2.667 | 3.2 | 3.922 |
| $f_{\mathrm{III}}(N) = 2N^2/(1 + 0.5 N^2)$ | 1.333 | 2.667 | 3.556 | 3.879 | 3.9992 |

At $N = 2$ type II gives $4/2 = 2$ and type III gives $8/3 = 2.667$. Both tend to 4.

**A saturating response destabilizes.** Put type II into a predator-prey model with logistic prey (the model of Rosenzweig and MacArthur):

$$\dot x = r x \left(1 - \frac{x}{K}\right) - f(x)\, y, \qquad \dot y = e f(x)\, y - m y, \qquad f(x) = \frac{a x}{1 + a h x},$$

where $e$ is the share of eaten prey that becomes predators and $m$ is the predator death rate. With $e > m h$, the equilibrium prey density is $x^* = m / (a (e - m h))$. The prey isocline is the parabola $y = g(x) = r (1 - x/K)(1 + a h x)/a$, with its top at $x_p = (K - 1/(ah))/2$.

**Claim.** If $0 < x^* < K$, the positive equilibrium $(x^*, g(x^*))$ is stable when $x^* > x_p$ and unstable when $x^* < x_p$.

*Proof.* Write $\dot x = f(x)(g(x) - y)$. At the equilibrium, $g(x^*) = y^*$ and $e f(x^*) = m$, so the [Jacobian](/jacobian-linearization/) is

$$J = \begin{pmatrix} f(x^*)\, g'(x^*) & -f(x^*) \\ e f'(x^*)\, y^* & 0 \end{pmatrix}.$$

Its determinant $e f(x^*) f'(x^*) y^*$ is positive, so the sign of the trace $f(x^*) g'(x^*)$ decides. The derivative $g'(x) = (r/a)(a h - 1/K - 2 a h x / K)$ is zero at $x_p$, positive to the left and negative to the right. $\square$

With $r = 1$, $a = 2$, $h = 0.25$, $e = 0.5$ and $m = 1$, the equilibrium is $x^* = 2$ and $x_p = (K - 2)/2$, so the equilibrium is stable for $K < 6$ and unstable for $K > 6$. For $K = 5$, an RK4 run with $dt = 0.01$ goes to $(2, 0.6)$. For $K = 8$, the runs from $(3, 0.5)$ and from $(2.05, 0.749)$ go to the same cycle, on which the prey moves between $0.31$ and $6.28$ and the predator between $0.11$ and $1.74$. More food for the prey ($K$ larger) makes the system cycle; this is often called the paradox of enrichment. With type I in the same model, $g$ is a falling line and the equilibrium is stable for every $K > x^*$.

**Non-examples and near cases.**

- **Not a Holling response: predator dependence.** A rate such as $a N / (1 + a h N + q P)$, which also falls with the predator density $P$ because predators get in each other's way, is a predator-dependent response. A ratio-dependent response $f(N/P)$ is another. The Holling types depend on $N$ only.
- **Not a Holling response: the numerical response.** The rate $e f(N)$ at which predators are born from food is a numerical response, not a functional response, even when it has the same shape.
- **A saturating curve of another form.** The curve $f(N) = f_{\max}(1 - e^{-cN})$ is also concave and saturating, so it is a type II shape in Holling's broad sense, but it is not the disc equation and it does not come from the time budget above.

## Related definitions

- **[Michaelis-Menten kinetics](/michaelis-menten-kinetics/).** The enzyme rate $V_{\max} S / (K_m + S)$ has the same form as type II, with $V_{\max} = 1/h$ and $K_m = 1/(ah)$. The derivations are parallel: an enzyme that holds one substrate molecule cannot bind the next one.
- **[Hill equation](/hill-equation/).** With the Hill coefficient 2, the curve $S^2/(K^2 + S^2)$ has the form of type III.
- **[Lotka-Volterra predator-prey model](/lotka-volterra-predator-prey/).** Its predation term is type I.
- **[Limit cycle](/limit-cycle/).** The attractor that appears in the example above when the equilibrium becomes unstable; the [Poincaré-Bendixson theorem](/poincare-bendixson-theorem/) proves that it exists when the solutions are bounded.
- **[Competitive exclusion principle](/competitive-exclusion-principle/).** With linear (type I) gains from a resource, $n$ species cannot all persist on fewer than $n$ resources. Saturating gains remove this bound, because they allow coexistence on a cycle.

## References
