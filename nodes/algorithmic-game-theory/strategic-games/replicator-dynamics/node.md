---
tag: DA7ATV
kind: model
slug: replicator-dynamics
name: Replicator dynamics
aliases:
- replicator equation
area: algorithmic-game-theory/strategic-games
level: advanced
summary: A differential equation in which the share of each strategy in a population grows at a rate equal to its payoff minus the average payoff.
prereqs: [evolutionarily-stable-strategy, ode-initial-value-problem]
see_also: [mutation-selection-balance, prisoners-dilemma, classical-runge-kutta-4, lyapunov-function, multiplicative-weights-update, lotka-volterra-competition, logistic-growth-model, jacobian-linearization]
sources:
  - paper: doi:10.1016/0025-5564(78)90077-9
    title: "Peter D. Taylor and Leo B. Jonker, Evolutionarily stable strategies and game dynamics, Mathematical Biosciences 40(1-2) (1978), 145-156"
    locator: the replicator equation for a population playing a symmetric game, and the asymptotic stability of a regular evolutionarily stable strategy
  - book: isbn:9780521625708
    title: Josef Hofbauer and Karl Sigmund, Evolutionary Games and Population Dynamics, Cambridge University Press, 1998
    locator: Chapter 7 (the replicator equation, Nash equilibria as rest points, and Theorem 7.2.4, every evolutionarily stable state is asymptotically stable)
  - paper: doi:10.1038/246015a0
    title: "John Maynard Smith and George R. Price, The logic of animal conflict, Nature 246 (1973), 15-18"
    locator: evolutionarily stable strategies, the static notion that the dynamics makes precise
---

The replicator dynamics is a differential equation for the shares of the types in a large population: the share of a type grows when its fitness is above the mean fitness of the population and shrinks when it is below, at a rate equal to its share times the difference. In evolutionary game theory, the fitness of a type is its expected payoff in random encounters with the population, so it depends on the shares of all types; this is frequency-dependent selection. With fitnesses that do not depend on the shares it is the haploid selection equation, and with a symmetric payoff matrix it is the continuous-time selection equation at one diploid locus, for which Fisher's fundamental theorem holds. Taylor and Jonker (1978) introduced it as the dynamic counterpart of the [evolutionarily stable strategy](/evolutionarily-stable-strategy/), which is a static test, and every such strategy is an asymptotically stable rest point of the equation.

## The machine

**The state.** A population has $n$ types, or pure strategies, $1, \ldots, n$. The state is the vector of shares $x = (x_1, \ldots, x_n)$ in the simplex $\Delta_n = \{x : x_i \ge 0,\ \sum_i x_i = 1\}$. A strategy here is a fixed behaviour of an individual, inherited by its offspring; nobody chooses.

**The payoffs.** An $n \times n$ matrix $A$ gives the payoff $A_{ij}$ of type $i$ when it meets type $j$. Individuals meet in random pairs, so the fitness of type $i$ is $f_i(x) = (Ax)_i$, and the mean fitness is $\bar f(x) = x^{\mathsf T} A x = \sum_i x_i f_i(x)$. Payoffs are increments of the growth rate over a common background rate.

**The equation.**

$$\dot x_i = x_i \big( (Ax)_i - x^{\mathsf T} A x \big), \qquad i = 1, \ldots, n.$$

It follows from the growth of the absolute numbers: if type $i$ has $N_i$ individuals and grows at the rate $\beta + f_i$, then $x_i = N_i / \sum_j N_j$ satisfies this equation, and the background rate $\beta$ cancels.

**Standing assumptions.** The population is infinite, so there is no drift; it is well mixed, with random pairing; time is continuous and generations overlap; reproduction is asexual or the types are alleles at one locus with no other effects. For finite populations with random sampling, see the [Wright-Fisher model](/wright-fisher-model/).

**Basic properties.**

- The simplex is invariant, and so is each face: a type with share 0 stays at 0, so the equation cannot create a new type. Each vertex is a rest point.
- The rest points are the states $x$ at which every type in the support of $x$ has the same fitness.
- Adding a constant to a column of $A$ does not change the orbits in $\Delta_n$, since it adds the same number to every $f_i$ and to $\bar f$.
- The right-hand side is a polynomial, so by the theory of the [initial value problem](/ode-initial-value-problem/) each start has a unique solution, defined for all times.

## What it counts

The model predicts the shares $x(t)$ over time, and in particular where they end: at which rest points, cycles or other limit sets, and from which starts. The questions are the stability of rest points, the size of their basins, the mean fitness $\bar f$ along the way, and how these compare with the static notions of game theory: [Nash equilibrium](/nash-equilibrium/) and [ESS](/evolutionarily-stable-strategy/).

**A closed form.** For two types with $A = \begin{pmatrix} 1 & 1 \\ 0 & 0 \end{pmatrix}$, type 1 always earns 1 more, and $\dot x_1 = x_1 (1 - x_1)$. This is the [logistic equation](/logistic-growth-model/), with the solution $x_1(t) = x_1(0) e^t / (1 - x_1(0) + x_1(0) e^t)$.

**Numerical solution.** In general the equation has no closed form, and it is solved with a fixed step by the [classical Runge-Kutta method](/classical-runge-kutta-4/) of order 4:

```pseudo id=main
REPLICATOR-RK4(A, x, h, T)            ▷ T steps of size h from the shares x
L1  for t ← 1 to T
L2      k1 ← F(x)
L3      k2 ← F(x + (h/2) k1)
L4      k3 ← F(x + (h/2) k2)
L5      k4 ← F(x + h k3)
L6      x ← x + (h/6)(k1 + 2 k2 + 2 k3 + k4)
L7  return x
F(x)                                  ▷ the right-hand side
L8  f ← A x
L9  φ ← (Σ_i x_i f_i) / (Σ_i x_i)
L10 return (x_i (f_i - φ))_i
```

Each step costs 4 evaluations of $F$, each $O(n^2)$. On the simplex the denominator in L9 is 1, so this is the equation above. Off the simplex it makes the entries of $F$ sum to exactly 0, so $\sum_i x_i$ stays 1 up to rounding. Without it, rounding errors in $\sum_i x_i$ grow like $e^{-\bar f t}$ near a rest point with $\bar f < 0$. The global error of the method is $O(h^4)$ on a fixed time interval. The implementation is in float. Its tests check the logistic closed form to $10^{-9}$, the order 4 (halving $h$ divides the error by about 16), and each example below.

## Relation to other models

- **Population genetics.** With constant fitnesses, $f_i$ not depending on $x$, the equation is the selection equation for haploid types, whose solution moves all weight to the fittest of the types present at the start. With a symmetric matrix $A$ of genotype fitnesses at one locus, $x$ is the vector of allele frequencies under random mating ([Hardy-Weinberg proportions](/hardy-weinberg-principle/)), and the equation is the continuous-time selection equation. Adding mutation gives the replicator-mutator equation, whose rest points describe a [mutation-selection balance](/mutation-selection-balance/).
- **Lotka-Volterra equations.** The replicator equation for $n$ types is equivalent, by a change of variables and of the time scale, to a [Lotka-Volterra](/lotka-volterra-competition/) equation for $n - 1$ species (Hofbauer and Sigmund 1998). So results move between the two.
- **Learning.** The update $x_i \leftarrow x_i e^{\eta f_i(x)} / \sum_j x_j e^{\eta f_j(x)}$ of [multiplicative weights](/multiplicative-weights-update/) has the first-order expansion $x_i + \eta x_i (f_i - \bar f)$, so the replicator equation is its limit as the step $\eta \to 0$.
- **Two populations.** For a bimatrix game $(A, B)$, one population plays rows and another columns: $\dot x_i = x_i((Ay)_i - x^{\mathsf T} A y)$ and $\dot y_j = y_j((B^{\mathsf T} x)_j - x^{\mathsf T} B y)$.
- **Discrete time.** The map $x_i \leftarrow x_i f_i(x) / \bar f(x)$, for positive payoffs, is the discrete-time replicator dynamics. Its stability properties can differ from those of the continuous equation.

## Known results in the model

- **Nash equilibria and rest points (Hofbauer and Sigmund 1998, Chapter 7).** If $(x, x)$ is a symmetric Nash equilibrium, $x$ is a rest point; the converse fails, since every vertex is a rest point. A rest point that is Lyapunov stable is a Nash equilibrium, and so is the limit of an orbit that starts in the interior and converges. A strict equilibrium is asymptotically stable.
- **ESS are asymptotically stable.** Every evolutionarily stable state is an asymptotically stable rest point (Taylor and Jonker 1978 for regular ESS; Hofbauer and Sigmund 1998, Theorem 7.2.4). For an ESS $\hat x$, the relative entropy $\sum_{i : \hat x_i > 0} \hat x_i \log(\hat x_i / x_i)$ decreases along orbits near $\hat x$, so it is a [Lyapunov function](/lyapunov-function/). An interior ESS attracts every orbit that starts in the interior. In the Hawk-Dove game, $A = \begin{pmatrix} -1 & 2 \\ 0 & 1 \end{pmatrix}$, the share $q$ of Hawks follows $\dot q = q(1 - q)(1 - 2q)$, and every interior start goes to the ESS $q = 1/2$.
- **The converse is false.** For
$$A = \begin{pmatrix} 0 & 6 & -4 \\ -3 & 0 & 5 \\ -1 & 3 & 0 \end{pmatrix},$$
the centre $c = (1/3, 1/3, 1/3)$ has $Ac = (2/3, 2/3, 2/3)$, so it is a rest point and a Nash equilibrium. For $z = (1, 0, -1)$, $z^{\mathsf T} A z = 5 > 0$, so the mutant $y = c + \delta z$ gets $u(y, y) - u(c, y) = 5\delta^2 > 0$, and $c$ is not an ESS. Yet the [linearization](/jacobian-linearization/) at $c$, in the coordinates $(x_1, x_2)$, has trace $-2/3$ and determinant $1/3$, so its eigenvalues are $-1/3 \pm i\sqrt{2}/3$, and $c$ is asymptotically stable. The vertex $e_1$ is a strict equilibrium and attracts other orbits: the run from $(0.4, 0.3, 0.3)$ goes to $c$, and the run from $(0.8, 0.1, 0.1)$ goes to $e_1$.
- **Dominated strategies die out.** If type $i$ is strictly dominated by type $j$, then $x_i / x_j \to 0$ along every interior orbit, since $\frac{d}{dt} \log(x_i / x_j) = f_i - f_j$ stays below a negative constant. In the [prisoner's dilemma](/prisoners-dilemma/), the share of cooperators tends to 0.
- **Cycles.** In rock, paper, scissors, with 1 for a win, $-1$ for a loss and 0 for a tie, $\frac{d}{dt}\log(x_1 x_2 x_3) = \sum_i f_i - 3\bar f = 0$, because the columns of $A$ sum to 0 and $x^{\mathsf T} A x = 0$. So $x_1 x_2 x_3$ is constant along orbits, and every interior orbit other than the centre is a closed cycle. If each tie costs $\varepsilon$, so $A$ has $-\varepsilon$ on the diagonal, then $\frac{d}{dt}\log(x_1x_2x_3) = \varepsilon(3\lVert x \rVert^2 - 1)$. For $\varepsilon > 0$ the product rises and orbits go to the centre, which is then an ESS; for $\varepsilon < 0$ it falls and orbits spiral out toward the boundary.
- **Fisher's fundamental theorem.** If $A$ is symmetric, $\frac{d}{dt} \bar f = 2 \sum_i x_i (f_i - \bar f)^2$, twice the variance of the fitness, so the mean fitness never decreases and is a Lyapunov function. For a non-symmetric $A$ the mean fitness can fall, as in the prisoner's dilemma, where it drops from 3 to 1 as defectors take over.
- **Two populations.** In the two-population dynamics of a bimatrix game, an interior rest point is never asymptotically stable, because after a change of the time scale the flow keeps volumes in the interior (Hofbauer and Sigmund 1998). This is one reason the one-population and two-population models give different predictions.

## References
