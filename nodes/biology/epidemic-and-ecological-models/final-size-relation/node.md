---
tag: X9Y6S3
kind: theorem
slug: final-size-relation
name: Final size relation
aliases:
- final epidemic size equation
area: biology/epidemic-and-ecological-models
level: core
summary: In the SIR model the fraction z ever infected solves 1 - z = e^(-R0 z), which has a positive root exactly when R0 > 1.
history:
  year: 1927
  people: [W. O. Kermack, A. G. McKendrick]
  note: Kermack and McKendrick derived the relation for their general model with an infectivity that depends on the time since infection.
prereqs: [kermack-mckendrick-sir-model, basic-reproduction-number]
see_also: [herd-immunity-threshold, percolation, giant-component, erdos-renyi-model, stochastic-sir-model, reed-frost-model, seir-epidemic-model, fixed-point-iteration]
sources:
  - paper: doi:10.1098/rspa.1927.0118
    title: W. O. Kermack and A. G. McKendrick, A contribution to the mathematical theory of epidemics, Proceedings of the Royal Society of London A 115(772), 1927
    locator: pages 700 to 721 (the threshold density and the equation for the final number of susceptibles)
  - paper: doi:10.1007/s11538-005-9047-7
    title: Junling Ma and David J. D. Earn, Generality of the final size formula for an epidemic of a newly invading infectious disease, Bulletin of Mathematical Biology 68(3), 2006
    locator: pages 679 to 702 (the formula holds with a latent stage, any number of infectious stages with durations of any distribution, transmission rates that vary between individuals, and a general class of spatial contact structures; it fails with some kinds of heterogeneous mixing, such as a core group)
  - book: isbn:9780691116174
    title: Matt J. Keeling and Pejman Rohani, Modeling Infectious Diseases in Humans and Animals, Princeton University Press, 2008
    locator: Section 2.1.1, SIR model without demography (2.1.1.1 the threshold phenomenon, 2.1.1.2 epidemic burnout)
  - paper: doi:10.1103/PhysRevE.66.016128
    title: M. E. J. Newman, Spread of epidemic disease on networks, Physical Review E 66(1), 2002
    locator: the mapping of SIR epidemics on a contact network to bond percolation, and the outbreak size as the size of a giant cluster
---

The final size relation is the equation for the fraction $z$ of a population that is ever infected in an SIR epidemic. In the [Kermack-McKendrick model](/kermack-mckendrick-sir-model/), with homogeneous mixing and an epidemic that starts from a very small number of cases in a fully susceptible population, $z$ solves $z = 1 - e^{-R_0 z}$, where $R_0$ is the [basic reproduction number](/basic-reproduction-number/). The equation does not depend on any other parameter, it has no solution in closed form with elementary functions, and its positive root is always larger than the [herd immunity threshold](/herd-immunity-threshold/) $1 - 1/R_0$. The same equation gives the size of the giant component of an [Erdos-Renyi random graph](/erdos-renyi-model/), a link through [percolation](/percolation/).

## Statement

Consider the Kermack-McKendrick SIR model

$$
\frac{dS}{dt} = -\frac{\beta S I}{N}, \qquad \frac{dI}{dt} = \frac{\beta S I}{N} - \gamma I, \qquad \frac{dR}{dt} = \gamma I,
$$

with $R_0 = \beta / \gamma$ and the initial fractions $s_0 = S(0)/N > 0$, $i_0 = I(0)/N > 0$ and $r(0) = 0$, so that $s_0 + i_0 = 1$.

**Theorem.**
1. The limits $s_\infty = \lim_{t \to \infty} S(t)/N$ and $r_\infty = \lim_{t \to \infty} R(t)/N$ exist, $I(t) \to 0$, and $s_\infty \ge s_0 e^{-R_0} > 0$.
2. The limit $s_\infty$ is the only root in $(0, s_0)$ of the equation $\ln(s_0 / s_\infty) = R_0 (1 - s_\infty)$.
3. Let $z = 1 - s_\infty$, the fraction ever infected, and let $i_0 \to 0$. Then $z$ converges to the largest root in $[0, 1)$ of the equation $z = 1 - e^{-R_0 z}$. If $R_0 \le 1$, this root is $z = 0$. If $R_0 > 1$, it is the only root in $(0, 1)$, and it satisfies $1 - 1/R_0 < z < 1$.

## In plain words

Take a large town where nobody is immune, and let a few people bring in a new infection. Count, at the end, how many people ever caught it. That share depends only on one number: how many people one case infects in a town of people who can all catch it. If that number is at most one, almost nobody gets infected. If it is larger than one, a fixed share of the town is infected, and some people are never infected at all, because the infection runs out of new people to reach before it reaches everyone. The share infected is also always larger than the share that would have been enough to stop the spread. The epidemic overshoots, because many people are still sick when the spread begins to slow down, and each of them still infects others.

## Proof

**Step 1: an exact first integral.** From the equations for $S$ and $R$,

$$
\frac{d}{dt} \ln S = -\frac{\beta I}{N} = -\frac{R_0}{N} \frac{dR}{dt}.
$$

Integrate from 0 to $t$, and use the fractions $s = S/N$ and $r = R/N$ with $r(0) = 0$:

$$
\ln \frac{s(t)}{s_0} = -R_0\, r(t). \tag{1}
$$

**Step 2: the limits exist.** $S$ decreases and is bounded below by 0, and $R$ increases and is bounded above by $N$, so both have limits, and $I = N - S - R$ has a limit too. If $I(t) \to I_\infty > 0$, then $dR/dt = \gamma I$ would make $R$ grow without bound, which is impossible. So $I(t) \to 0$ and $r_\infty = 1 - s_\infty$. From (1) with $r(t) \le 1$, $s(t) \ge s_0 e^{-R_0}$, so $s_\infty > 0$: the epidemic ends with susceptibles left.

**Step 3: the equation for the limit.** Let $t \to \infty$ in (1) and use $r_\infty = 1 - s_\infty$. This gives $\ln(s_0 / s_\infty) = R_0 (1 - s_\infty)$. To show that the root is unique in $(0, s_0)$, let

$$
h(x) = \ln x - \ln s_0 + R_0 (1 - x).
$$

Then $h(s_\infty) = 0$. The function $h$ is strictly concave, $h(x) \to -\infty$ as $x \to 0$, and $h(s_0) = R_0 (1 - s_0) = R_0 i_0 > 0$. A strictly concave function that is negative near 0 and positive at $s_0$ crosses zero exactly once in $(0, s_0)$: after the first crossing it cannot fall below zero and rise again. Also $s_\infty < s_0$, because $S$ strictly decreases while $I > 0$. So $s_\infty$ is the only root in $(0, s_0)$.

**Step 4: the roots of $f(z) = 1 - e^{-R_0 z} - z$.** We have $f(0) = 0$, $f(1) = -e^{-R_0} < 0$, $f'(z) = R_0 e^{-R_0 z} - 1$ and $f''(z) = -R_0^2 e^{-R_0 z} < 0$, so $f$ is strictly concave.
- If $R_0 \le 1$, then $f'(0) \le 0$, and by concavity $f'(z) < 0$ for $z > 0$, so $f < 0$ on $(0, 1]$ and $z = 0$ is the only root in $[0, 1]$.
- If $R_0 > 1$, then $f'(0) > 0$, so $f > 0$ just to the right of 0. With $f(1) < 0$, $f$ has a root in $(0, 1)$, and a strictly concave function has at most two roots, so the root $z^*$ in $(0, 1)$ is unique.

**Step 5: the limit $i_0 \to 0$.** With $x = s_\infty$ and $s_0 = 1 - i_0$, the function $h$ converges to $h_0(x) = \ln x + R_0 (1 - x)$, uniformly on compact subsets of $(0, 1]$, and $h_0(1 - z) = 0$ is the same as $f(z) = 0$. If $R_0 > 1$, the root $1 - z^*$ of $h_0$ in $(0, 1)$ is a simple root, so the root of $h$ in $(0, s_0)$ converges to it. If $R_0 \le 1$, then $h_0 < 0$ on $(0, 1)$, so the root of $h$ in $(0, s_0)$ must converge to 1, which means $z \to 0$.

**Step 6: the bounds.** For $R_0 > 1$, $f(1 - 1/R_0) = 1/R_0 - e^{-(R_0 - 1)} > 0$, because $e^{y} > 1 + y$ for $y = R_0 - 1 > 0$ gives $e^{R_0 - 1} > R_0$. Since $f > 0$ exactly on $(0, z^*)$, the point $1 - 1/R_0$ lies left of $z^*$, so $z^* > 1 - 1/R_0$. And $z^* < 1$ because $f(1) < 0$. $\blacksquare$

## Consequences

**Values.** The positive root, found numerically:

| $R_0$ | 1.1 | 1.2 | 1.5 | 2 | 2.5 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|---|
| $z$ | 0.1761 | 0.3137 | 0.5828 | 0.7968 | 0.8926 | 0.9405 | 0.9802 | 0.9930 |
| $1 - 1/R_0$ | 0.0909 | 0.1667 | 0.3333 | 0.5 | 0.6 | 0.6667 | 0.75 | 0.8 |

You can check a value by hand: for $R_0 = 2$, $1 - e^{-2 \cdot 0.7968} = 1 - e^{-1.5936} = 1 - 0.2032 = 0.7968$.

**Overshoot.** The infection stops growing when the susceptible fraction falls below $1/R_0$, which is the herd immunity threshold. But at that moment many people are still infectious, and they keep infecting others. For $R_0 = 2$, $z \approx 0.797$ against $1 - 1/R_0 = 0.5$: an overshoot of about 30 percent of the population.

**Estimating $R_0$.** The relation can be inverted: $R_0 = -\ln(1 - z) / z$. If a serological survey after an epidemic finds that half of the population was infected, $R_0 = 2 \ln 2 \approx 1.386$. With pre-existing immunity in a fraction $r(0)$ of the population, the same proof gives $\ln(s_0 / s_\infty) = R_0 (1 - r(0) - s_\infty)$.

**Near the threshold.** Expand $e^{-R_0 z} \approx 1 - R_0 z + R_0^2 z^2 / 2$ to get $z \approx 2 (R_0 - 1) / R_0^2$, so $z$ grows linearly in $R_0 - 1$ just above 1. For $R_0 = 1.1$ this gives 0.1653, against the exact 0.1761.

**The Lambert W form.** With the principal branch $W_0$ of the Lambert W function, the inverse of $w \mapsto w e^w$,

$$
z = 1 + \frac{W_0\left(-R_0 e^{-R_0}\right)}{R_0}.
$$

To check it, put $w = -R_0 (1 - z)$; then $z = 1 - e^{-R_0 z}$ becomes $w e^{w} = -R_0 e^{-R_0}$. The other real branch gives $w = -R_0$, which is $z = 0$.

**Computing the root.** The [fixed-point iteration](/fixed-point-iteration/) $z_{k+1} = 1 - e^{-R_0 z_k}$ from $z_0 = 1$ decreases monotonically to $z^*$, because the map is increasing and its value at 1 is below 1. Its rate is the derivative at the root, $R_0 e^{-R_0 z^*} = R_0 (1 - z^*) < 1$, which is about 0.41 for $R_0 = 2$. The [Newton-Raphson method](/newton-raphson-method/) on $f$ converges quadratically from the same start.

**Percolation.** The giant component of the Erdos-Renyi graph $G(n, c/n)$ holds a fraction $S$ of the nodes that solves $S = 1 - e^{-c S}$, the same equation with $c$ in place of $R_0$ (see [giant component](/giant-component/)). The match is exact in the limit: if each infectious period has the same fixed length, the stochastic SIR epidemic is equivalent to bond [percolation](/percolation/) on the complete graph with an edge probability of about $R_0 / N$, and the people infected in a major outbreak are the giant cluster that contains the first case (Newman 2002). The chain binomial [Reed-Frost model](/reed-frost-model/) is this case.

**The stochastic model.** In the Markov chain version, the [stochastic SIR model](/stochastic-sir-model/), an outbreak from one case either dies out early with a small final size or becomes a major outbreak. For large $N$ and $R_0 > 1$, a major outbreak has a final fraction close to $z^*$. The probability of a major outbreak is not given by this relation; it comes from the [branching process extinction theorem](/branching-process-extinction-theorem/), and it is $1 - 1/R_0$ for an exponential infectious period.

## Tightness

**The relation needs homogeneous mixing.** With groups that mix unevenly, each group has its own final size, and $z_i = 1 - \exp\left(-\sum_j K_{ij} z_j\right)$, where $K$ is the [next-generation matrix](/next-generation-matrix/). For two groups of equal size with $K = \begin{pmatrix} 3 & 1 \\ 1 & 0.5 \end{pmatrix}$, $R_0 = \rho(K) \approx 3.351$, and the final sizes are $z_1 \approx 0.974$ and $z_2 \approx 0.739$, so the overall fraction is about 0.857. A homogeneous population with the same $R_0$ has $z \approx 0.960$. So the single equation overestimates the final size in this example; $R_0$ alone does not decide it.

**On a contact network** the final size depends on the degree distribution, through the percolation equations of the [SIR model on networks](/sir-epidemic-model/), not only on $R_0$.

**The distribution of the infectious period.** The relation holds for any distribution of the infectious period, and also with a latent period, as in the [SEIR model](/seir-epidemic-model/), because the final size depends only on the total infectiousness of one case (Ma and Earn 2006). The same holds if individuals differ in infectiousness, for example with super-spreaders. The time course changes, the final size does not.

**Births and deaths.** With births, new susceptibles arrive, the infection can become endemic, and the question of a final size does not arise.

**The small initial condition.** Part 3 is a limit. For a finite initial fraction $i_0$, use the exact relation of part 2. For example, with $R_0 = 2$ and $i_0 = 0.001$ in a population of 10000, the exact relation gives a final number of 7971.5 infected, against $10000 \cdot 0.7968 = 7968$ from the limit equation.

**The threshold is sharp.** For $R_0 = 1$ exactly, $z = 0$ in the limit, and for $R_0 = 1 + \varepsilon$, $z \approx 2 \varepsilon$, so the final size is continuous in $R_0$ but not differentiable at 1.

## History

Kermack and McKendrick (1927) derived the threshold and the final size equation for a general model where the infectivity of an individual depends on the time since its infection; the SIR equations with constant rates are their special case. The equation became the standard result of the field and is in every textbook, for example Keeling and Rohani (2008, section 2.1.1). Ma and Earn (2006) showed how far it holds: for a latent stage, any number of infectious stages, stage durations of any distribution, individuals that differ in infectiousness, and a general class of spatial contact structures. It fails with some kinds of heterogeneous mixing, for example a core group of a sexually transmitted infection. The link with random graphs came later, through the mapping of SIR epidemics on networks to percolation (Newman 2002).

## References
