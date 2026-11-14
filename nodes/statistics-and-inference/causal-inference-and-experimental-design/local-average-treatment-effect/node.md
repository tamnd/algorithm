---
tag: 545YHW
kind: theorem
slug: local-average-treatment-effect
name: Local average treatment effect theorem
aliases:
- LATE
- complier average causal effect
- Imbens-Angrist theorem
area: statistics-and-inference/causal-inference-and-experimental-design
level: advanced
summary: Under monotonicity, the instrumental variables estimand equals the average effect among compliers, the units whose treatment the instrument changes.
prereqs: [instrumental-variables-estimation, potential-outcomes-framework, sutva]
see_also: [two-stage-least-squares, average-treatment-effect, randomized-experiment, regression-discontinuity-design, ignorability, mediation-analysis, delta-method]
sources:
  - paper: doi:10.2307/2951620
    title: Guido W. Imbens and Joshua D. Angrist, Identification and estimation of local average treatment effects, Econometrica 62(2), 1994
    locator: the article starting on p. 467 (the monotonicity condition and the theorem that the instrumental variables estimand is the average effect for the units the instrument moves)
  - paper: doi:10.1080/01621459.1996.10476902
    title: Joshua D. Angrist, Guido W. Imbens and Donald B. Rubin, Identification of causal effects using instrumental variables, Journal of the American Statistical Association 91(434), 1996
    locator: pp. 444 to 455 (the potential outcomes statement, the names complier, always-taker, never-taker and defier, and the bias without monotonicity or exclusion)
  - paper: doi:10.1177/0193841X8400800205
    title: Howard S. Bloom, Accounting for no-shows in experimental evaluation designs, Evaluation Review 8(2), 1984
    locator: pp. 225 to 246 (dividing the effect of assignment by the share treated, the one-sided case)
  - paper: doi:10.1111/j.0006-341X.2002.00021.x
    title: Constantine E. Frangakis and Donald B. Rubin, Principal stratification in causal inference, Biometrics 58(1), 2002
    locator: pp. 21 to 29 (strata defined by the joint potential values of a post-treatment variable)
  - paper: doi:10.3982/ECTA11974
    title: Toru Kitagawa, A test for instrument validity, Econometrica 83(5), 2015
    locator: pp. 2043 to 2063 (the testable implication that the implied complier outcome densities are nonnegative)
---

The local average treatment effect theorem says what the instrumental variables ratio estimates when the treatment effect differs from unit to unit. With a binary instrument and a binary treatment, the units fall into four groups by how their treatment responds to the instrument. If no unit responds in the wrong direction (monotonicity), then the Wald ratio, the effect of the instrument on the outcome divided by its effect on the treatment, equals the average effect of the treatment among the compliers, the units that take the treatment when the instrument is on and not when it is off. The theorem is due to Imbens and Angrist (1994). The estimand it names is called the local average treatment effect (LATE) in their work and the complier average causal effect in the statistics literature that grew from Angrist, Imbens and Rubin (1996). The theorem turns [instrumental variables estimation](/instrumental-variables-estimation/) from a method that needs a constant effect into one with a clear target, at the price that the target concerns a subgroup that we cannot list.

## Statement

**Setting.** Each unit has a binary instrument $Z$, potential treatments $D(0), D(1) \in \{0, 1\}$ (the treatment it would take with the instrument off and on), and potential outcomes $Y(d, z)$ for $d, z \in \{0, 1\}$, as in the [potential outcomes framework](/potential-outcomes-framework/) with [SUTVA](/sutva/). We observe $Z$, $D = D(Z)$ and $Y = Y(D, Z)$. The pair $(D(0), D(1))$ puts each unit in one of four principal strata:

| stratum | $D(0)$ | $D(1)$ | meaning |
| --- | --- | --- | --- |
| always-taker (A) | 1 | 1 | takes the treatment either way |
| never-taker (N) | 0 | 0 | refuses it either way |
| complier (C) | 0 | 1 | takes it if and only if the instrument is on |
| defier (F) | 1 | 0 | takes it if and only if the instrument is off |

**The estimand.** With the exclusion restriction below, write $Y(d)$ for $Y(d, 0) = Y(d, 1)$. The local average treatment effect, or complier average causal effect, is

$$\tau_C = \mathbb{E}[Y(1) - Y(0) \mid D(1) > D(0)] = \mathbb{E}[Y(1) - Y(0) \mid \text{C}].$$

It is an average over a subgroup defined by potential treatments, so it is a causal quantity, but no unit can be classified as a complier from data, because only one of $D(0), D(1)$ is seen.

**Assumptions.**

1. **Independence.** $Z$ is independent of $(Y(0, 0), Y(0, 1), Y(1, 0), Y(1, 1), D(0), D(1))$.
2. **Exclusion.** $Y(d, 0) = Y(d, 1)$ for $d = 0, 1$ and every unit.
3. **Monotonicity.** $D(1) \ge D(0)$ for every unit: there are no defiers.
4. **First stage.** $\Pr[\text{C}] > 0$, and $0 < \Pr[Z = 1] < 1$.

All expectations are assumed finite.

**Theorem (Imbens and Angrist 1994).** Under assumptions 1 to 4,

$$\frac{\mathbb{E}[Y \mid Z = 1] - \mathbb{E}[Y \mid Z = 0]}{\mathbb{E}[D \mid Z = 1] - \mathbb{E}[D \mid Z = 0]} = \tau_C,$$

and the denominator is $\Pr[\text{C}]$. Moreover the shares of the strata and the complier means of both potential outcomes are identified:

$$\Pr[\text{A}] = \mathbb{E}[D \mid Z = 0], \quad \Pr[\text{N}] = 1 - \mathbb{E}[D \mid Z = 1], \quad \Pr[\text{C}] = \mathbb{E}[D \mid Z = 1] - \mathbb{E}[D \mid Z = 0],$$

$$\mathbb{E}[Y(1) \mid \text{C}] = \frac{\mathbb{E}[YD \mid Z = 1] - \mathbb{E}[YD \mid Z = 0]}{\Pr[\text{C}]}, \qquad \mathbb{E}[Y(0) \mid \text{C}] = \frac{\mathbb{E}[Y(1 - D) \mid Z = 0] - \mathbb{E}[Y(1 - D) \mid Z = 1]}{\Pr[\text{C}]}.$$

So of the three aliases, LATE and complier average causal effect name the estimand $\tau_C$, and Imbens-Angrist theorem names the identification result.

## In plain words

An instrument can only tell us about the units it moves. Always-takers and never-takers have the same treatment whatever the instrument does, so by exclusion their outcome does not change with the instrument either, and they add nothing to the difference in mean outcomes between the two instrument arms. All of that difference comes from the compliers, whose treatment switches from 0 to 1. Dividing by the share of compliers turns the total into an average per complier. Defiers would spoil this, because their switch goes the other way and their effects would enter with a minus sign.

## Proof

By exclusion, $Y = Y(D(Z))$, and since $D(z) \in \{0, 1\}$,

$$Y(D(z)) = Y(0) + D(z)\,\Delta, \qquad \Delta = Y(1) - Y(0).$$

**Numerator.** Given $Z = z$, the observed $Y$ is $Y(0) + D(z)\Delta$. By independence, the law of $(Y(0), Y(1), D(0), D(1))$ given $Z = z$ is its unconditional law, so

$$\mathbb{E}[Y \mid Z = z] = \mathbb{E}[Y(0) + D(z)\Delta \mid Z = z] = \mathbb{E}[Y(0)] + \mathbb{E}[D(z)\Delta],$$

and the difference is $\mathbb{E}[(D(1) - D(0))\Delta]$. The factor $D(1) - D(0)$ is $1$ for compliers, $-1$ for defiers and $0$ for always-takers and never-takers. Therefore

$$\mathbb{E}[Y \mid Z = 1] - \mathbb{E}[Y \mid Z = 0] = \Pr[\text{C}]\,\mathbb{E}[\Delta \mid \text{C}] - \Pr[\text{F}]\,\mathbb{E}[\Delta \mid \text{F}]. \tag{1}$$

**Denominator.** In the same way $\mathbb{E}[D \mid Z = 1] - \mathbb{E}[D \mid Z = 0] = \mathbb{E}[D(1) - D(0)] = \Pr[\text{C}] - \Pr[\text{F}]$. $\quad (2)$

**Ratio.** Monotonicity gives $\Pr[\text{F}] = 0$, so (2) is $\Pr[\text{C}]$, which is positive by assumption 4, and (1) over (2) is $\mathbb{E}[\Delta \mid \text{C}] = \tau_C$.

**Shares.** $\mathbb{E}[D \mid Z = 0] = \Pr[D(0) = 1] = \Pr[\text{A}] + \Pr[\text{F}] = \Pr[\text{A}]$, and $1 - \mathbb{E}[D \mid Z = 1] = \Pr[D(1) = 0] = \Pr[\text{N}] + \Pr[\text{F}] = \Pr[\text{N}]$.

**Complier means.** $YD = Y(1)D(z)$ given $Z = z$, so by independence $\mathbb{E}[YD \mid Z = z] = \mathbb{E}[Y(1)D(z)]$. With no defiers, $D(1) = 1$ on A and C, and $D(0) = 1$ on A only, so the difference is $\mathbb{E}[Y(1); \text{C}] = \Pr[\text{C}]\,\mathbb{E}[Y(1) \mid \text{C}]$. In the same way $Y(1 - D) = Y(0)(1 - D(z))$ given $Z = z$; $1 - D(0) = 1$ on N and C, and $1 - D(1) = 1$ on N only, so $\mathbb{E}[Y(1 - D) \mid Z = 0] - \mathbb{E}[Y(1 - D) \mid Z = 1] = \Pr[\text{C}]\,\mathbb{E}[Y(0) \mid \text{C}]$. The difference of the two complier means is $\tau_C$ again, which checks the first claim. $\blacksquare$

**Example.** Ten units, with the instrument randomized so that independence holds by design. The table gives every unit's potential values; the effect is $\Delta = Y(1) - Y(0)$.

| unit | stratum | $D(0)$ | $D(1)$ | $Y(0)$ | $Y(1)$ | $\Delta$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1, 2 | A | 1 | 1 | 4, 6 | 7, 9 | 3, 3 |
| 3, 4, 5 | N | 0 | 0 | 1, 2, 3 | 2, 4, 3 | 1, 2, 0 |
| 6 to 10 | C | 0 | 1 | 2, 3, 1, 4, 0 | 5, 5, 4, 6, 5 | 3, 2, 3, 2, 5 |

With the instrument on, the always-takers show $Y(1)$, the never-takers $Y(0)$ and the compliers $Y(1)$: the mean outcome is $(7 + 9 + 1 + 2 + 3 + 5 + 5 + 4 + 6 + 5)/10 = 47/10$, and the treated share is $7/10$. With it off, the compliers show $Y(0)$ instead: the mean is $(7 + 9 + 1 + 2 + 3 + 2 + 3 + 1 + 4 + 0)/10 = 32/10$, and the treated share is $2/10$. In expectation over the randomization, the Wald ratio is

$$\frac{4.7 - 3.2}{0.7 - 0.2} = \frac{1.5}{0.5} = 3 = \frac{3 + 2 + 3 + 2 + 5}{5} = \tau_C.$$

The shares come out as stated: $\Pr[\text{A}] = 0.2$, $\Pr[\text{N}] = 1 - 0.7 = 0.3$, $\Pr[\text{C}] = 0.5$. The complier means are $\mathbb{E}[Y(1) \mid \text{C}] = (4.1 - 1.6)/0.5 = 5$ and $\mathbb{E}[Y(0) \mid \text{C}] = (1.6 - 0.6)/0.5 = 2$, which match $(5 + 5 + 4 + 6 + 5)/5$ and $(2 + 3 + 1 + 4 + 0)/5$. The average effect over all ten units is $(6 + 3 + 15)/10 = 2.4$, not 3: the ratio does not estimate it. Comparing the treated with the untreated inside the instrument-on arm gives $41/7 - 2 = 3.86$, which is biased because always-takers have high $Y(0)$.

## Consequences

- **Two-stage least squares.** With one binary instrument, [2SLS](/two-stage-least-squares/) is the sample Wald ratio exactly, so it is a consistent estimator of $\tau_C$, and its robust standard error is valid for it. The sample analogues of the complier means are consistent, and their standard errors follow from the [delta method](/delta-method/).
- **One-sided noncompliance.** If the treatment is not available with the instrument off, $D(0) = 0$ for every unit, so monotonicity holds by design and there are no always-takers. The compliers are then exactly the treated units in the instrument-on arm, and by independence $\tau_C$ is the average effect on the treated. This is Bloom's (1984) correction for no-shows: divide the effect of assignment by the share that took the treatment.
- **Different instruments, different answers.** Each instrument has its own compliers. Two valid instruments can give two different estimates with no contradiction, and the overidentification test of 2SLS can then reject although both instruments are valid.
- **Describing the compliers.** Replacing $Y$ by a covariate $X$ in the formula for $\mathbb{E}[Y(1) \mid \text{C}]$ gives $\mathbb{E}[X \mid \text{C}]$ (since $X$ is not affected by $D$). So we can say how compliers differ from the population even though we cannot name them.
- **A testable implication.** The complier means come from complier distributions: for every set $B$, $\Pr[Y \in B, D = 1 \mid Z = 1] - \Pr[Y \in B, D = 1 \mid Z = 0] \ge 0$, and the same for $D = 0$ with the arms reversed. A negative value rejects the assumptions together (Kitagawa 2015).
- **More general instruments.** For a multi-valued instrument, Imbens and Angrist show that the ratio for any two values is the effect for the units moved between them, and that the 2SLS estimate with the instrument values as dummies is a weighted average of these effects with nonnegative weights.

## Tightness

- **Without monotonicity.** By (1) and (2) the ratio is $(\Pr[\text{C}]\,\tau_C - \Pr[\text{F}]\,\tau_F)/(\Pr[\text{C}] - \Pr[\text{F}])$, a combination with a negative weight on the defiers' effect. It can lie outside the range of all unit effects. With $\Pr[\text{C}] = 0.4$, $\tau_C = 1$, $\Pr[\text{F}] = 0.2$ and $\tau_F = 5$, every unit gains from the treatment, but the ratio is $(0.4 - 1)/0.2 = -3$.
- **Without exclusion.** If the instrument has a direct effect $\gamma$ on every unit's outcome, the numerator gains $\gamma$ and the ratio becomes $\tau_C + \gamma/\Pr[\text{C}]$. A small direct effect is divided by the complier share, so a weak first stage makes it large.
- **Without a first stage.** If $\Pr[\text{C}] = 0$, the ratio is $0/0$ and $\tau_C$ is not defined.
- **The average effect over everyone is not identified.** The data fix the law of $Y(1)$ for always-takers and of $Y(0)$ for never-takers, and nothing about $Y(0)$ for always-takers or $Y(1)$ for never-takers. Two populations that differ only in those unseen values give the same observed law and different average effects, so the average treatment effect has only bounds, which are finite only for a bounded outcome.

## History

Bloom (1984) divided the effect of random assignment by the share treated for programs that controls could not enter. Imbens and Angrist (1994) gave the monotonicity condition and proved the general result, naming the estimand the local average treatment effect. Angrist, Imbens and Rubin (1996) restated it in Rubin's potential outcomes notation, introduced the names complier, always-taker, never-taker and defier, and showed what goes wrong without each assumption. Frangakis and Rubin (2002) made the strata by joint potential values of a post-treatment variable a general tool, principal stratification. Kitagawa (2015) gave a test of the joint assumptions.

## References
