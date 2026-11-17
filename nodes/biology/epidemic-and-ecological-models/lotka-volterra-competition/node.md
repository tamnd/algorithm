---
tag: 8SQFG6
kind: model
slug: lotka-volterra-competition
name: Lotka-Volterra competition model
aliases:
- competitive Lotka-Volterra equations
area: biology/epidemic-and-ecological-models
level: core
summary: Two species with logistic growth that reduce each other's growth, whose outcome depends on the competition coefficients.
history:
  year: 1925
  people: [Alfred J. Lotka, Vito Volterra, Georgii F. Gause]
  note: Lotka (1925) and Volterra (1926) wrote the equations, and Gause (1934) fitted them to experiments with yeasts and protozoa.
prereqs: [logistic-growth-model, jacobian-linearization]
see_also: [competitive-exclusion-principle, lotka-volterra-predator-prey, lyapunov-function, lyapunov-stability, levins-metapopulation-model, classical-runge-kutta-4, eigenvalue]
sources:
  - book: "Alfred J. Lotka, Elements of Physical Biology, Williams and Wilkins, Baltimore, 1925"
    title: Lotka 1925
    locator: the equations for species that compete for the same food
  - book: "Georgii F. Gause, The Struggle for Existence, Williams and Wilkins, Baltimore, 1934"
    title: Gause 1934
    locator: the competition equations and the experiments with two species of Paramecium and with yeasts
  - book: isbn:9780387952239
    title: James D. Murray, Mathematical Biology I, An Introduction, third edition, Springer, 2002
    locator: Chapter 3, Models for Interacting Populations (the section on competition models and the principle of competitive exclusion)
---

The Lotka-Volterra competition model is a pair of [logistic equations](/logistic-growth-model/) in which each species also lowers the growth of the other: $\dot N_1 = r_1 N_1 (1 - (N_1 + \alpha_{12} N_2)/K_1)$ and $\dot N_2 = r_2 N_2 (1 - (N_2 + \alpha_{21} N_1)/K_2)$. The outcome depends only on the carrying capacities and the competition coefficients. The two species coexist at a stable equilibrium when each species limits itself more than it limits the other. Otherwise one species wins, or the winner depends on the start. This is the model behind the theorem form of the [competitive exclusion principle](/competitive-exclusion-principle/).

## The machine

**The state.** $N_1(t) \ge 0$ and $N_2(t) \ge 0$ are the sizes or densities of two species that use the same resources.

**The parameters.** All are positive.

- $r_i$, in 1 per time: the growth rate of species $i$ when it is rare and alone.
- $K_i$, in individuals (or density) of species $i$: its carrying capacity when alone.
- $\alpha_{12}$, without unit: the effect of one individual of species 2 on the growth of species 1, measured in individuals of species 1. $\alpha_{12} = 0.5$ means that two individuals of species 2 crowd species 1 as much as one individual of species 1 does. $\alpha_{21}$ is the reverse.

**The equations.**

$$\frac{dN_1}{dt} = r_1 N_1 \left(1 - \frac{N_1 + \alpha_{12} N_2}{K_1}\right), \qquad \frac{dN_2}{dt} = r_2 N_2 \left(1 - \frac{N_2 + \alpha_{21} N_1}{K_2}\right).$$

**The assumptions.** Each species alone follows the logistic model. The competition is not explicit: the resources are not in the state, and each species feels the other only through a linear term in the per capita growth rate. The coefficients are constant. The populations are well mixed and large. Some books write $\beta_{12}$ or $a_{12}$ for $\alpha_{12}$, or put the coefficients in the form $b_{ij} = r_i \alpha_{ij}/K_i$; this page uses the form above.

**The isoclines.** The per capita growth of species 1 is zero on the line $L_1 : N_1 + \alpha_{12} N_2 = K_1$, and that of species 2 on the line $L_2 : \alpha_{21} N_1 + N_2 = K_2$. The relative position of the two lines in the positive quadrant gives the outcome. Two numbers decide it:

- $\Delta_1 = K_1 - \alpha_{12} K_2$. It is positive if species 1, when rare, can grow in a population of species 2 at its capacity $K_2$.
- $\Delta_2 = K_2 - \alpha_{21} K_1$. It is positive if species 2 can invade species 1 at $K_1$.

```pseudo id=main
LV-COMPETITION-OUTCOME(K1, K2, α12, α21)
L1  Δ1 ← K1 - α12 K2                     ▷ can species 1 invade species 2 alone?
L2  Δ2 ← K2 - α21 K1                     ▷ can species 2 invade species 1 alone?
L3  if Δ1 > 0 and Δ2 > 0 then return "coexist at (N1*, N2*)"
L4  if Δ1 > 0 and Δ2 < 0 then return "species 1 wins"
L5  if Δ1 < 0 and Δ2 > 0 then return "species 2 wins"
L6  if Δ1 < 0 and Δ2 < 0 then return "bistable: the start decides"
L7  return "degenerate (an isocline passes through an equilibrium)"
```

The rule costs $O(1)$ arithmetic operations. The growth rates $r_1$ and $r_2$ do not enter it: they change how fast the outcome comes, and the path, but not the outcome. The implementation checks the rule against RK4 runs from four start points for 30 random parameter sets.

## What it counts

- The four equilibria $(0, 0)$, $(K_1, 0)$, $(0, K_2)$ and, when it is positive, the coexistence point

$$N_1^* = \frac{K_1 - \alpha_{12} K_2}{1 - \alpha_{12}\alpha_{21}} = \frac{\Delta_1}{1 - \alpha_{12}\alpha_{21}}, \qquad N_2^* = \frac{\Delta_2}{1 - \alpha_{12}\alpha_{21}}.$$

- The stability of each equilibrium, and so the long-run outcome: coexistence, the exclusion of one species, or two outcomes that depend on the start.
- The rate of approach, from the eigenvalues of the [Jacobian](/jacobian-linearization/).

**Three examples.** All have $r_1 = r_2 = 1$ per unit of time.

| $K_1$ | $K_2$ | $\alpha_{12}$ | $\alpha_{21}$ | $\Delta_1$ | $\Delta_2$ | outcome |
|---|---|---|---|---|---|---|
| 100 | 100 | 0.5 | 0.5 | 50 | 50 | coexistence at $(66.67, 66.67)$, eigenvalues $-1/3$ and $-1$ |
| 100 | 100 | 1.5 | 1.5 | $-50$ | $-50$ | saddle at $(40, 40)$, eigenvalues $0.2$ and $-1$; the start decides |
| 100 | 80 | 0.6 | 1.5 | 52 | $-70$ | species 1 wins and goes to $(100, 0)$ |

In the second case, the start $(45, 35)$ ends at $(100, 0)$ and the start $(35, 45)$ ends at $(0, 100)$. In the third case, species 1 wins from $(1, 50)$, although it starts 50 times rarer.

## Relation to other models

- **[Logistic growth](/logistic-growth-model/).** With $N_2 = 0$, species 1 follows the logistic model and goes to $K_1$.
- **[Lotka-Volterra predator-prey](/lotka-volterra-predator-prey/).** The same quadratic terms with opposite signs on the two species. The predator-prey model has neutral cycles; the competition model has no periodic orbits, because it is a competitive system in the plane (each species lowers the growth of the other), and in such a system every bounded solution tends to an equilibrium.
- **Resource models.** In a model with explicit resources, such as consumers that eat from a pool that is renewed, the coefficients $\alpha_{ij}$ come out of the overlap in the resource use, when the resources are fast and stay near their equilibrium. The Lotka-Volterra form is then a linear approximation near the equilibrium. The [competitive exclusion principle](/competitive-exclusion-principle/) page gives a resource model and its theorem.
- **More species.** The generalized form $\dot N_i = r_i N_i (1 - \sum_j \alpha_{ij} N_j / K_i)$ for $n$ species, with $\alpha_{ii} = 1$, can have cycles and more complex behaviour for $n \ge 3$. For two species, the outcome is always one of the four cases above.
- **Space and patches.** In a landscape of patches, a weaker competitor that colonizes faster can persist next to a stronger one. The [Levins metapopulation model](/levins-metapopulation-model/) is the one-species base of these models.

## Known results in the model

**The boundary equilibria.** At $(K_1, 0)$ the Jacobian is triangular, with the eigenvalues $-r_1$ and $r_2 \Delta_2 / K_2$. So $(K_1, 0)$ is stable if $\Delta_2 < 0$ and a saddle if $\Delta_2 > 0$. By symmetry, $(0, K_2)$ has the eigenvalues $-r_2$ and $r_1 \Delta_1 / K_1$. The origin has the eigenvalues $r_1$ and $r_2$, so it is always unstable.

*Proof for $(K_1, 0)$.* The partial derivatives of $\dot N_2$ at $N_2 = 0$ are $\partial \dot N_2 / \partial N_1 = 0$ and $\partial \dot N_2 / \partial N_2 = r_2 (1 - \alpha_{21} K_1 / K_2) = r_2 \Delta_2 / K_2$. The entry $\partial \dot N_1 / \partial N_1$ at $(K_1, 0)$ is $r_1(1 - 2K_1/K_1) = -r_1$. A triangular matrix has its diagonal entries as eigenvalues. $\square$

**The coexistence point.** If $\alpha_{12}\alpha_{21} \ne 1$, the isoclines meet in one point $(N_1^*, N_2^*)$ given above. It is positive if and only if $\Delta_1$ and $\Delta_2$ have the same sign as $1 - \alpha_{12}\alpha_{21}$. The Jacobian there is

$$J^* = \begin{pmatrix} -r_1 N_1^*/K_1 & -r_1 \alpha_{12} N_1^*/K_1 \\ -r_2 \alpha_{21} N_2^*/K_2 & -r_2 N_2^*/K_2 \end{pmatrix},$$

with the trace $\operatorname{tr} J^* < 0$ and the determinant $\det J^* = \frac{r_1 r_2 N_1^* N_2^*}{K_1 K_2}(1 - \alpha_{12}\alpha_{21})$.

*Proof.* At the point, $1 - (N_1^* + \alpha_{12} N_2^*)/K_1 = 0$, so the derivative of $\dot N_1$ with respect to $N_1$ is $-r_1 N_1^*/K_1$ and with respect to $N_2$ is $-r_1 \alpha_{12} N_1^*/K_1$. The second row is the same with the indices swapped. The determinant is $\frac{r_1 r_2 N_1^* N_2^*}{K_1 K_2}(1 - \alpha_{12}\alpha_{21})$. $\square$

So a positive coexistence point is a stable node (both eigenvalues are real and negative, because $(\operatorname{tr} J^*)^2 - 4\det J^* \ge (J^*_{11} - J^*_{22})^2 \ge 0$ when $\det J^* > 0$ and the off-diagonal entries have the same sign) when $\alpha_{12}\alpha_{21} < 1$, and a saddle when $\alpha_{12}\alpha_{21} > 1$.

**The four cases.** Let $\Delta_1, \Delta_2 \ne 0$.

1. $\Delta_1 > 0$ and $\Delta_2 > 0$: then $\alpha_{12}\alpha_{21} < 1$, because $K_1 > \alpha_{12} K_2 > \alpha_{12}\alpha_{21} K_1$. The coexistence point is positive and every solution with $N_1(0), N_2(0) > 0$ tends to it.
2. $\Delta_1 > 0$ and $\Delta_2 < 0$: every solution with $N_1(0) > 0$ tends to $(K_1, 0)$. Species 1 wins.
3. $\Delta_1 < 0$ and $\Delta_2 > 0$: species 2 wins, by symmetry.
4. $\Delta_1 < 0$ and $\Delta_2 < 0$: then $\alpha_{12}\alpha_{21} > 1$. The coexistence point is a positive saddle. Its stable manifold divides the open quadrant into two basins: one of $(K_1, 0)$ and one of $(0, K_2)$.

The condition of case 1 reads $\alpha_{21}/K_2 < 1/K_1$ and $\alpha_{12}/K_1 < 1/K_2$. The left side of the first inequality is the drop in the per capita growth of species 2 (divided by $r_2$) per individual of species 1, and the right side is the drop that one individual of species 1 causes to its own species (divided by $r_1$). So coexistence means: each species limits itself more than it limits the other.

*Proof of case 1 by a Lyapunov function.* Write $u_i = N_i - N_i^*$. Since $K_1 = N_1^* + \alpha_{12} N_2^*$, the first equation is $\dot N_1 = \frac{r_1}{K_1} N_1 (-u_1 - \alpha_{12} u_2)$, and the second is $\dot N_2 = \frac{r_2}{K_2} N_2 (-u_2 - \alpha_{21} u_1)$. Let

$$V = \sum_{i=1}^{2} w_i \left(N_i - N_i^* \ln N_i\right), \qquad w_1 = \frac{\alpha_{21} K_1}{r_1}, \quad w_2 = \frac{\alpha_{12} K_2}{r_2}.$$

Then $\dot V = \sum_i w_i \frac{u_i}{N_i}\dot N_i = -\alpha_{21} u_1(u_1 + \alpha_{12} u_2) - \alpha_{12} u_2 (u_2 + \alpha_{21} u_1) = -\left(\alpha_{21} u_1^2 + 2\alpha_{12}\alpha_{21} u_1 u_2 + \alpha_{12} u_2^2\right)$. This quadratic form is positive definite, because its discriminant is $4\alpha_{12}^2\alpha_{21}^2 - 4\alpha_{12}\alpha_{21} = 4\alpha_{12}\alpha_{21}(\alpha_{12}\alpha_{21} - 1) < 0$. So $\dot V < 0$ except at the coexistence point. Each term $N_i - N_i^* \ln N_i$ tends to infinity as $N_i \to 0$ or $N_i \to \infty$, so the sublevel sets of $V$ in the open quadrant are compact, and each solution stays in one of them. By the [Lyapunov](/lyapunov-function/) theorem with LaSalle's principle, each positive solution tends to the only point where $\dot V = 0$. $\square$

*Proof of case 2.* Here the line $L_2$ lies strictly below $L_1$ in the quadrant, because its intercepts $K_2/\alpha_{21} < K_1$ and $K_2 < K_1/\alpha_{12}$ are both smaller. So the quadrant splits into three regions: $A$ below $L_2$, where both species grow; $B$ between the lines, where $N_1$ grows and $N_2$ falls; $C$ above $L_1$, where both fall. On the boundary of $B$, the field points into $B$: on $L_1$ (above $L_2$), $\dot N_1 = 0$ and $\dot N_2 < 0$; on $L_2$ (below $L_1$), $\dot N_2 = 0$ and $\dot N_1 > 0$. So a solution that enters $B$ stays there. In $B$ the solution is monotone in each coordinate and bounded, so it converges, and the limit is an equilibrium in the closure of $B$ with $N_1 > 0$. The only one is $(K_1, 0)$. A solution in $A$ or $C$ is also monotone in each coordinate while it stays there. If it stays forever, it converges to an equilibrium in the closure of that region. For $A$ the candidates are $(0, 0)$ and $(0, K_2)$, and both are impossible, because $N_1$ is positive and increasing. For $C$ the only candidate is $(K_1, 0)$. Otherwise the solution enters $B$. With $N_2(0) = 0$, species 1 follows the logistic model to $K_1$. $\square$

*Proof of case 4.* The saddle has a one-dimensional stable manifold: two solution curves that tend to $(N_1^*, N_2^*)$. One comes from the region near the origin and one from far away, along the isoclines. Together with the saddle they form a curve that splits the quadrant. On each side, the argument of case 2 applies to the region between the isoclines that touches the axis: the region near $(K_1, 0)$ where $\dot N_1 > 0 > \dot N_2$ traps solutions and sends them to $(K_1, 0)$, and the region near $(0, K_2)$ sends them to $(0, K_2)$. A solution that is not on the stable manifold enters one of these two regions, because, as in case 2, it cannot converge to anything else while it is monotone. $\square$

**Speed of the outcome.** The time scale of the final approach is set by the eigenvalue of the stable equilibrium closest to zero. In the coexistence example it is $-1/3$, so a small deviation decays like $e^{-t/3}$, three times slower than in a single logistic population with $r = 1$.

**Degenerate cases.** If $\Delta_1 = 0$ or $\Delta_2 = 0$, the coexistence point lies on an axis and merges with a boundary equilibrium. If $\alpha_{12}\alpha_{21} = 1$ and $\Delta_1 = \Delta_2 = 0$, the two isoclines coincide and there is a whole line of equilibria. These cases need exact equalities between parameters, so small changes remove them; they are not robust predictions of coexistence.

## References
