---
tag: 4XYDN6
kind: theorem
slug: competitive-exclusion-principle
name: Competitive exclusion principle
aliases:
- Gause's law
area: biology/epidemic-and-ecological-models
level: core
summary: In consumer-resource models with linear uptake, n species on fewer than n resources cannot all persist; on one resource, the species that needs the least resource wins.
history:
  year: 1934
  people: [Georgii F. Gause, Garrett Hardin]
  note: Gause (1934) tested the competition equations with protozoa and yeasts, and Hardin (1960) gave the principle its name.
prereqs: [lotka-volterra-competition, ode-initial-value-problem]
see_also: [lotka-volterra-competition, levins-metapopulation-model, holling-functional-response, lotka-volterra-predator-prey, limit-cycle, lasalle-invariance-principle, rank-nullity-theorem, logistic-growth-model]
sources:
  - book: "Georgii F. Gause, The Struggle for Existence, Williams and Wilkins, Baltimore, 1934"
    title: Gause 1934
    locator: the experiments on competition between two species of Paramecium and between two yeasts
  - paper: "Garrett Hardin, The competitive exclusion principle, Science 131(3409), 1292-1297, 1960"
    title: Hardin 1960
    locator: the statement that complete competitors cannot coexist, and the name of the principle
  - paper: doi:10.1086/282171
    title: G. Evelyn Hutchinson, The paradox of the plankton, The American Naturalist 95(882), 1961
    locator: pages 137 to 145 (many plankton species on few resources, and a changing environment as an explanation)
  - paper: doi:10.1086/283553
    title: Robert A. Armstrong and Richard McGehee, Competitive exclusion, The American Naturalist 115(2), 1980
    locator: pages 151 to 170 (n species on m resources, and coexistence on fewer resources through nonequilibrium dynamics)
  - book: isbn:9780387952239
    title: James D. Murray, Mathematical Biology I, An Introduction, third edition, Springer, 2002
    locator: Chapter 3, Models for Interacting Populations (competition models and the principle of competitive exclusion)
---

The competitive exclusion principle says that species that compete for the same limiting resources cannot all coexist. As a statement about nature it has many exceptions. As a theorem it holds inside a stated model. This page proves two such theorems. In a consumer-resource model where each species grows linearly in the resource levels, $n$ species that are limited by $k < n$ resources cannot all persist, whatever the resources do in time. On one resource, every species except the one that can live on the lowest resource level dies out. In the two-species [Lotka-Volterra competition model](/lotka-volterra-competition/), one species excludes the other when it can invade and the other cannot.

## Statement

**The consumer-resource model.** There are $n$ consumer species with densities $N_1(t), \ldots, N_n(t) > 0$ and $k$ resources with levels $R(t) = (R_1(t), \ldots, R_k(t))$. The consumers follow

$$\frac{dN_i}{dt} = N_i \left( b_i \cdot R(t) - d_i \right), \qquad i = 1, \ldots, n,$$

where $b_i \in \mathbb{R}^k$ has entries $b_{i1}, \ldots, b_{ik} \ge 0$ (the gain of species $i$ per unit of each resource) and $d_i > 0$ is its death rate. The resources $R(t)$ can be any continuous functions of time: they can follow equations that depend on the consumers, cycle, or be forced from outside. Let $B$ be the $n \times k$ matrix with the rows $b_i$ and let $d = (d_1, \ldots, d_n)$.

**Theorem 1 (exclusion on few resources).** Suppose that the linear system $B \rho = d$ has no solution $\rho \in \mathbb{R}^k$, and that there is a bound $M$ with $N_i(t) \le M$ for all $i$ and all $t \ge 0$. Then there are numbers $c_1, \ldots, c_n$, not all zero, and $\gamma > 0$ with

$$\prod_{i=1}^{n} N_i(t)^{c_i} = \prod_{i=1}^{n} N_i(0)^{c_i} \, e^{-\gamma t} \quad \text{for all } t \ge 0,$$

and $\min_i N_i(t) \to 0$ as $t \to \infty$. So the $n$ species cannot all stay above a fixed positive level.

If $n > k$, the system $B\rho = d$ has a solution only for a set of parameters $(B, d)$ of Lebesgue measure zero. So Theorem 1 applies to almost all models with more species than resources.

**Theorem 2 (the $R^*$ rule on one resource).** Let $k = 1$ and $b_i > 0$, and let $R_i^* = d_i / b_i$ be the resource level at which species $i$ just replaces itself. If $R_1^* < R_j^*$ and $N_1(t) \le M$ for all $t \ge 0$, then there is a constant $C$ with

$$N_j(t) \le C \, e^{-b_j (R_j^* - R_1^*)\, t} \quad \text{for all } t \ge 0.$$

So every species with a larger $R^*$ than the one with the smallest $R^*$ dies out, at an exponential rate.

**Theorem 3 (Lotka-Volterra).** In the model $\dot N_1 = r_1 N_1 (1 - (N_1 + \alpha_{12} N_2)/K_1)$, $\dot N_2 = r_2 N_2 (1 - (N_2 + \alpha_{21} N_1)/K_2)$ with positive parameters, suppose $K_1 > \alpha_{12} K_2$ and $K_2 < \alpha_{21} K_1$. Then every solution with $N_1(0) > 0$ and $N_2(0) \ge 0$ tends to $(K_1, 0)$.

**A hand example for Theorem 2.** Take $b_1 = 0.5$, $d_1 = 0.1$, so $R_1^* = 0.2$, and $b_2 = 1$, $d_2 = 0.3$, so $R_2^* = 0.3$. Then

$$\frac{d}{dt}\left(\ln N_1 - 0.5 \ln N_2\right) = (0.5 R - 0.1) - 0.5 (R - 0.3) = 0.05$$

for every resource level $R$, also when $R$ changes in time. If $N_1 \le M$, then $\ln N_2 \le 2 \ln M - 2 S(0) - 0.1\,t$ with $S = \ln N_1 - 0.5 \ln N_2$, so $N_2$ falls at least like $e^{-0.1\, t}$. This is the rate $b_2 (R_2^* - R_1^*) = 1 \cdot 0.1$ of the theorem.

**A hand example for Theorem 3.** With $K_1 = 100$, $K_2 = 80$, $\alpha_{12} = 0.6$ and $\alpha_{21} = 1.5$, the tests give $100 > 48$ and $80 < 150$, so species 1 wins, also from the start $(1, 50)$.

## In plain words

Each species needs a certain amount of food to replace its losses. If one food limits two species, the species that can live on less food keeps eating the food down to a level at which the other species loses more than it gains, and the other species dies out. With several foods, each species is a different mix of needs. If there are more species than foods, the needs of the species cannot all be met at the same time, and some species must lose. This holds even when the food supply goes up and down, as long as each species gains in proportion to the food. When species gain from food in a way that saturates, or when space, predators or a changing climate act as further limits, more species can live together.

## Proof

**A linear algebra step.** The system $B\rho = d$ has no solution if and only if there is a vector $c \in \mathbb{R}^n$ with $B^{\mathsf T} c = 0$ and $c \cdot d \ne 0$.

*Proof.* The column space of $B$ is the orthogonal complement of the null space of $B^{\mathsf T}$. If $d$ is not in the column space, its orthogonal projection $c$ onto the null space of $B^{\mathsf T}$ is not zero, and $c \cdot d = c \cdot c > 0$. Conversely, if $B\rho = d$, then $c \cdot d = c \cdot B\rho = (B^{\mathsf T} c)\cdot \rho = 0$ for each $c$ with $B^{\mathsf T}c = 0$. $\square$

**Proof of Theorem 1.** Take $c$ from the step above, with the sign chosen so that $\gamma = c \cdot d > 0$. Let $S(t) = \sum_i c_i \ln N_i(t)$. Then

$$\frac{dS}{dt} = \sum_{i} c_i \left( b_i \cdot R(t) - d_i \right) = \left(B^{\mathsf T} c\right) \cdot R(t) - c \cdot d = -\gamma.$$

So $S(t) = S(0) - \gamma t$, which is the product formula. Split the sum into $P = \{i : c_i > 0\}$ and the rest. For $i \notin P$, the term $c_i \ln N_i(t)$ is at least $c_i \ln M$, since $c_i \le 0$ and $N_i \le M$. So $\sum_{i \in P} c_i \ln N_i(t) \le S(0) - \gamma t - \sum_{i \notin P} c_i \ln M \to -\infty$. The set $P$ is not empty, because otherwise the left side is zero. Each term in $P$ is at most $c_i \ln M$, so the smallest $N_i(t)$ with $i \in P$ tends to $0$. $\square$

**Proof of the measure-zero remark.** If $B\rho = d$, then the $n \times (k + 1)$ matrix $[B \mid d]$ has the nonzero vector $(\rho, -1)$ in its null space, so its rank is at most $k$ by the [rank-nullity theorem](/rank-nullity-theorem/). For $n \ge k + 1$, this forces the determinant of its first $k + 1$ rows to vanish. That determinant is a polynomial in the entries that is not identically zero, and the zero set of such a polynomial has Lebesgue measure zero. $\square$

**Proof of Theorem 2.** Let $S(t) = b_j \ln N_1(t) - b_1 \ln N_j(t)$. Then

$$\frac{dS}{dt} = b_j (b_1 R - d_1) - b_1 (b_j R - d_j) = b_1 d_j - b_j d_1 = b_1 b_j (R_j^* - R_1^*) = \beta > 0.$$

So $S(t) = S(0) + \beta t$, and $\ln N_j(t) = (b_j \ln N_1(t) - S(t)) / b_1 \le (b_j \ln M - S(0) - \beta t)/b_1$. Since $\beta / b_1 = b_j (R_j^* - R_1^*)$, this is the bound with $C = \exp((b_j \ln M - S(0))/b_1)$. $\square$

**Proof of Theorem 3.** Write $\Delta_1 = K_1 - \alpha_{12}K_2 > 0$ and $\Delta_2 = K_2 - \alpha_{21} K_1 < 0$. The per capita growth of species 1 is zero on the line $L_1 : N_1 + \alpha_{12} N_2 = K_1$, and that of species 2 on $L_2 : \alpha_{21} N_1 + N_2 = K_2$. The intercepts of $L_2$ are $K_2/\alpha_{21} < K_1$ and $K_2 < K_1/\alpha_{12}$, so in the closed quadrant $L_2$ lies strictly below $L_1$. This splits the quadrant into three regions:

- $A$, below $L_2$: both species grow.
- $B$, between the lines: $N_1$ grows and $N_2$ falls.
- $C$, above $L_1$: both species fall.

On the part of $L_1$ that bounds $B$, $\dot N_1 = 0$ and $\dot N_2 < 0$; on the part of $L_2$ that bounds $B$, $\dot N_2 = 0$ and $\dot N_1 > 0$. So the field points into $B$ on its boundary, and a solution that enters $B$ stays in it. In $B$ both coordinates are monotone and bounded, so the solution converges, and its limit is an equilibrium in the closure of $B$ with $N_1 > 0$. The only one is $(K_1, 0)$.

A solution in $A$ or in $C$ is also monotone in both coordinates while it stays there. If it stays forever, it converges to an equilibrium in the closure of that region. For $A$, the candidates are $(0, 0)$ and $(0, K_2)$, and neither can be the limit, because $N_1$ is positive and increases in $A$. For $C$, the only candidate is $(K_1, 0)$. Otherwise the solution enters $B$. If $N_2(0) = 0$, species 1 follows the logistic equation and tends to $K_1$. $\square$

## Consequences

- **The number of species is at most the number of limiting resources.** Theorem 1 gives this bound for all consumer-resource models with linear gains, outside a set of parameters of measure zero. In such a model, if $n$ species are seen to persist, there are at least $n$ limiting factors.
- **One resource has one winner.** Theorem 2 gives a measurable prediction: grow each species alone, measure the resource level $R^*$ it leaves, and the species with the lowest $R^*$ wins in mixture. The winner is not the species that grows fastest, but the one that tolerates the lowest resource level.
- **The ecological principle (not a theorem).** The general rule "complete competitors cannot coexist", in the form that Hardin (1960) named, is a guide, not a result. It is true only in a model with stated assumptions. Gause (1934) found it in experiments: in mixed cultures of two Paramecium species, one species excluded the other.
- **Hutchinson's paradox of the plankton.** Many species of phytoplankton live together in a lake on a small number of nutrients, which seems to contradict the principle. Hutchinson (1961) proposed that the environment changes faster than exclusion can be completed, so that no equilibrium is reached.
- **Coexistence through nonequilibrium dynamics.** Armstrong and McGehee (1980) showed that the linear form of the gains is the key assumption. With saturating gains, as in a type II [Holling functional response](/holling-functional-response/), two species on one resource can coexist on a [limit cycle](/limit-cycle/): the resource level cycles, and each species does better at a different phase of the cycle. Theorem 1 does not apply, because its proof needs the per capita growth to be linear in the resources.
- **Space and other limits.** Predators, space and dispersal act as extra limiting factors. In a landscape of patches, a weaker competitor that colonizes empty patches faster can persist next to a stronger one; the [Levins metapopulation model](/levins-metapopulation-model/) is the base of these models.

## Tightness

- **The bound $n \le k$ is sharp.** Two species can coexist on two resources. Take $b_1 = (1, 0.2)$, $b_2 = (0.2, 1)$, $d_1 = d_2 = 0.6$, and resources that are supplied and eaten as $\dot R_l = (1 - R_l) - R_l \sum_i b_{il} N_i$. The system $B\rho = d$ has the solution $\rho = (0.5, 0.5)$, and the model has the positive equilibrium $N_1 = N_2 = 5/6$, $R = (0.5, 0.5)$. A simulation with explicit Euler and $dt = 0.01$ from $(N_1, N_2) = (0.1, 0.5)$ and from $(2, 0.01)$ reaches this equilibrium in both cases. Each species is limited more by the resource it eats more of, so each limits itself more than it limits the other.
- **The condition on $B\rho = d$ is needed.** If $R_1^* = R_2^*$ on one resource, then $N_1^{b_2} / N_2^{b_1}$ is constant in time, and neither species excludes the other. This is a neutral case: any small change in $d_1$ or $d_2$ breaks it.
- **Linearity is needed.** With saturating gains, the proof of Theorem 1 fails, and Armstrong and McGehee (1980) give coexistence of more species than resources on a cycle.
- **Theorem 3 needs both conditions.** If both species can invade ($\Delta_1 > 0$ and $\Delta_2 > 0$), they coexist at a stable equilibrium. If neither can ($\Delta_1 < 0$ and $\Delta_2 < 0$), the winner depends on the start. For $K_1 = K_2 = 100$, $r_1 = r_2 = 1$ and $\alpha_{12} = \alpha_{21} = 1.5$, the start $(45, 35)$ goes to $(100, 0)$ and the start $(35, 45)$ goes to $(0, 100)$.
- **Bounded densities are needed in Theorems 1 and 2.** If the resource grows without bound, the populations can all grow without bound, and $\min_i N_i(t) \to 0$ can fail. In a model where the resources are supplied at a finite rate, the bound holds.

## History

Lotka (1925) and Volterra (1926) wrote the competition equations of Theorem 3. Gause (1934) fitted them to experiments with yeasts and with Paramecium, and he found that one species excluded the other when both used the same food in the same way. Hardin (1960) called the rule the competitive exclusion principle and stated it as "complete competitors cannot coexist". Hutchinson (1961) asked why many species of plankton coexist on few resources. Armstrong and McGehee (1980) set the question in a model with $n$ species on $m$ resources, and showed that the exclusion result depends on the equilibrium or on the linear form of the gains.

## References
