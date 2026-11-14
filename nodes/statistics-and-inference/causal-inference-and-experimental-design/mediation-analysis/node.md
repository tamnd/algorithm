---
tag: EGAEMH
kind: technique
slug: mediation-analysis
name: Mediation analysis
aliases:
- natural direct and indirect effects
- causal mediation analysis
area: statistics-and-inference/causal-inference-and-experimental-design
level: advanced
summary: Splits a total effect into the part that goes through a mediator and the part that does not, defined by nested counterfactuals and identified under strong assumptions.
prereqs: [potential-outcomes-framework, ignorability, average-treatment-effect]
see_also: [front-door-criterion, structural-causal-model, do-calculus, ordinary-least-squares, delta-method, rosenbaum-sensitivity-analysis, local-average-treatment-effect, simpsons-paradox]
sources:
  - paper: doi:10.1037/0022-3514.51.6.1173
    title: Reuben M. Baron and David A. Kenny, The moderator-mediator variable distinction in social psychological research, conceptual, strategic, and statistical considerations, Journal of Personality and Social Psychology 51(6), 1986
    locator: pp. 1173 to 1182 (the regression steps for mediation and the product of coefficients)
  - paper: doi:10.1097/00001648-199203000-00013
    title: James M. Robins and Sander Greenland, Identifiability and exchangeability for direct and indirect effects, Epidemiology 3(2), 1992
    locator: pp. 143 to 155 (the nested counterfactual definitions of direct and indirect effects and their identification problems)
  - paper: "Judea Pearl, Direct and indirect effects, Proceedings of the 17th Conference on Uncertainty in Artificial Intelligence, 2001, pp. 411-420"
    title: Judea Pearl, Direct and indirect effects, Proceedings of the Seventeenth Conference on Uncertainty in Artificial Intelligence, 2001
    locator: pp. 411 to 420 (natural direct and indirect effects and the mediation formula)
  - paper: doi:10.1037/a0020761
    title: Kosuke Imai, Luke Keele and Dustin Tingley, A general approach to causal mediation analysis, Psychological Methods 15(4), 2010
    locator: pp. 309 to 334 (sequential ignorability, the estimation algorithm by simulation, sensitivity analysis)
  - paper: doi:10.1214/10-STS321
    title: Kosuke Imai, Luke Keele and Teppei Yamamoto, Identification, inference and sensitivity analysis for causal mediation effects, Statistical Science 25(1), 2010
    locator: pp. 51 to 71 (the identification theorem under sequential ignorability and the sensitivity parameter)
  - paper: doi:10.1093/oso/9780199754649.003.0011
    title: James M. Robins and Thomas S. Richardson, Alternative graphical causal models and the identification of direct effects, in Causality and Psychopathology, Oxford University Press, 2010
    locator: the whole chapter (cross-world independence, why no experiment identifies natural effects; general locator, the page numbers were not checked)
  - paper: doi:10.4310/SII.2009.v2.n4.a7
    title: Tyler J. VanderWeele and Stijn Vansteelandt, Conceptual issues concerning mediation, interventions and composition, Statistics and Its Interface 2(4), 2009
    locator: pp. 457 to 468 (the regression formulas for natural effects with an exposure-mediator interaction)
  - book: isbn:9780199325870
    title: Tyler J. VanderWeele, Explanation in Causal Inference, Methods for Mediation and Interaction, Oxford University Press, 2015
    locator: Chapters 2 and 3 on mediation with regression and on sensitivity analysis (general locator, the section numbers were not checked)
---

Mediation analysis asks how a treatment $A$ has its effect on an outcome $Y$: how much of the effect goes through an intermediate variable $M$, the mediator, and how much goes by other paths. A training program may raise wages partly because it raises skills and partly because the certificate signals something to employers. The natural indirect effect is the change in $Y$ when the mediator is moved from the value it would have without treatment to the value it would have with treatment, holding the treatment fixed. The natural direct effect is the change in $Y$ when the treatment changes but the mediator is held at its untreated value. Both are defined by nested potential outcomes such as $Y(1, M(0))$, which no unit can ever show, since it combines the treated world for $Y$ with the untreated world for $M$. They add up to the total effect. They can be estimated by the mediation formula, but only under sequential ignorability, which includes an assumption that no experiment can check. In linear models without interaction the indirect effect is the product of two regression coefficients, and that product equals the difference between the total and the direct coefficient exactly.

## In plain words

A drug lowers heart attacks. Part of the reason is that it lowers cholesterol, and part may be something else, like lower inflammation. To split the effect, imagine giving each patient the drug but somehow keeping their cholesterol where it would have been without the drug. The change from no drug to this strange situation is the direct effect. The change from this situation to the plain drug, which lets cholesterol fall, is the indirect effect. The two pieces add to the whole effect.

The strange situation is never observed, not even in an ideal experiment, because a patient's cholesterol without the drug and their outcome with the drug come from two different worlds. So the split needs assumptions that are stronger than for the total effect.

## When it applies

A binary treatment $A$, a mediator $M$ that occurs after $A$ and before $Y$, an outcome $Y$, and pre-treatment covariates $X$. The potential mediator is $M(a)$ and the potential outcome is $Y(a, m)$; consistency says $M = M(A)$ and $Y = Y(A, M)$. The effects are, for the average over the population:

- **Total effect.** $\mathrm{TE} = \mathbb{E}[Y(1, M(1)) - Y(0, M(0))]$, the usual [average treatment effect](/average-treatment-effect/).
- **Controlled direct effect.** $\mathrm{CDE}(m) = \mathbb{E}[Y(1, m) - Y(0, m)]$, the effect of $A$ when $M$ is set to $m$ for everyone.
- **Natural direct effect.** $\mathrm{NDE} = \mathbb{E}[Y(1, M(0)) - Y(0, M(0))]$.
- **Natural indirect effect.** $\mathrm{NIE} = \mathbb{E}[Y(1, M(1)) - Y(1, M(0))]$.

Adding the last two, the middle terms cancel: $\mathrm{NDE} + \mathrm{NIE} = \mathrm{TE}$. The other order of the telescoping sum, $\mathbb{E}[Y(1, M(1)) - Y(0, M(1))] + \mathbb{E}[Y(0, M(1)) - Y(0, M(0))]$, gives a second split, and the two differ when $A$ and $M$ interact.

**Identification.** Sequential ignorability (Imai, Keele and Yamamoto 2010) assumes, for all $a, a', m$:

1. $\{Y(a', m), M(a)\}$ is independent of $A$ given $X$: no unmeasured confounding of the treatment, as in [ignorability](/ignorability/);
2. $Y(a', m)$ is independent of $M(a)$ given $A = a$ and $X$: no unmeasured confounding of the mediator and the outcome, including the case $a' \ne a$;

and positivity, $\Pr[M = m \mid A = a, X = x] > 0$ where needed. Then the mediation formula of Pearl (2001) holds:

$$\mathbb{E}[Y(a, M(a^*))] = \sum_x\sum_m\mathbb{E}[Y \mid A = a, M = m, X = x]\,\Pr[M = m \mid A = a^*, X = x]\,\Pr[X = x],$$

with integrals in place of sums for continuous variables.

*Proof.* Fix $x$ and condition on $X = x$ throughout. Then $\mathbb{E}[Y(a, M(a^*))] = \sum_m\mathbb{E}[Y(a, m) \mid M(a^*) = m]\Pr[M(a^*) = m]$. For the second factor, assumption 1 gives $\Pr[M(a^*) = m] = \Pr[M(a^*) = m \mid A = a^*] = \Pr[M = m \mid A = a^*]$. For the first factor,

$$\mathbb{E}[Y(a, m) \mid M(a^*) = m] \overset{1}{=} \mathbb{E}[Y(a, m) \mid M(a^*) = m, A = a^*] \overset{2}{=} \mathbb{E}[Y(a, m) \mid A = a^*] \overset{1}{=} \mathbb{E}[Y(a, m) \mid A = a] \overset{2}{=} \mathbb{E}[Y(a, m) \mid M(a) = m, A = a],$$

and the last term is $\mathbb{E}[Y \mid A = a, M = m]$ by consistency. The first step uses the joint independence in 1, the second uses 2 with $A = a^*$, the third uses 1, and the fourth uses 2 with $A = a$. Averaging over $x$ gives the formula. $\blacksquare$

The second step, with $a \ne a^*$, is the cross-world part: it relates $Y(a, m)$ to $M(a^*)$, two quantities that never coexist. Robins and Richardson (2010) point out that no experiment, even one that randomizes both $A$ and $M$, can test it, so the natural effects are identified only under an assumption that is not testable in principle. The controlled direct effect needs only the same-world parts and is identified by $\sum_x(\mathbb{E}[Y \mid 1, m, x] - \mathbb{E}[Y \mid 0, m, x])\Pr[x]$. The method does not apply when a variable affected by $A$ confounds $M$ and $Y$, since then assumption 2 fails for every choice of $X$ that excludes it, and the natural effects are not identified at all without further assumptions.

## The template

**Estimation.** The plug-in version of the mediation formula:

```pseudo id=main
MEDIATION(data, X)
L1  fit an outcome model μ(a, m, x) for E[Y | A = a, M = m, X = x]
L2  fit a mediator model p(m | a, x) for Pr[M = m | A = a, X = x]
L3  θ(a, a*) ← (1/n) Σᵢ Σ_m μ(a, m, Xᵢ) p(m | a*, Xᵢ)     ▷ for (a, a*) in {(0, 0), (1, 0), (1, 1)}
L4  NDE ← θ(1, 0) - θ(0, 0);  NIE ← θ(1, 1) - θ(1, 0)
L5  return (NDE, NIE), with intervals from the bootstrap or the delta method
```

For a continuous mediator, line L3 integrates over the fitted density of $M$, usually by drawing mediator values from it, as in the algorithm of Imai, Keele and Tingley (2010). For [OLS](/ordinary-least-squares/) models it has a closed form.

**Linear models.** Suppose $\mathbb{E}[M \mid A, X] = \alpha_0 + \alpha A + \alpha_x^\top X$ and $\mathbb{E}[Y \mid A, M, X] = \beta_0 + \gamma A + \beta M + \theta AM + \beta_x^\top X$. Plugging these into the mediation formula (VanderWeele and Vansteelandt 2009), with $\bar m_0 = \alpha_0 + \alpha_x^\top\mathbb{E}[X]$ the mean mediator without treatment:

$$\mathrm{NDE} = \gamma + \theta\,\bar m_0, \qquad \mathrm{NIE} = \alpha(\beta + \theta).$$

Without interaction, $\theta = 0$, these are the classical $\mathrm{NDE} = \gamma$ and $\mathrm{NIE} = \alpha\beta$, the product of coefficients of Baron and Kenny (1986).

**Product equals difference, exactly.** Let $\hat\tau$ be the OLS coefficient of $A$ in the regression of $Y$ on $(1, A)$, $\hat\alpha$ that of $M$ on $(1, A)$, and $\hat\gamma, \hat\beta$ those of $Y$ on $(1, A, M)$. Then in every sample

$$\hat\tau - \hat\gamma = \hat\alpha\hat\beta.$$

*Proof.* Write the long regression as $Y_i = \hat\beta_0 + \hat\gamma A_i + \hat\beta M_i + \hat e_i$, where the residuals $\hat e$ are orthogonal to $1$, $A$ and $M$. Take the sample covariance of both sides with $A$: $\widehat{\mathrm{Cov}}(A, Y) = \hat\gamma\,\widehat{\mathrm{Var}}(A) + \hat\beta\,\widehat{\mathrm{Cov}}(A, M) + 0$. Divide by $\widehat{\mathrm{Var}}(A)$: the left side is $\hat\tau$ and $\widehat{\mathrm{Cov}}(A, M)/\widehat{\mathrm{Var}}(A) = \hat\alpha$. $\blacksquare$

With the same covariates $X$ in all three regressions the identity still holds, by the Frisch-Waugh-Lovell theorem applied after removing $X$ from $A$, $M$ and $Y$. It is an algebraic fact, not a causal one: it holds for any variable $M$, mediator or not. It fails for logistic and other nonlinear models, where the two methods give different answers.

**Worked example.** No covariates, binary $A$ and $M$, and a population with

| | $\Pr[M = 1 \mid A]$ | $\mathbb{E}[Y \mid A, M = 0]$ | $\mathbb{E}[Y \mid A, M = 1]$ |
| --- | --- | --- | --- |
| $A = 0$ | 0.2 | 1 | 3 |
| $A = 1$ | 0.6 | 2 | 5 |

With $A$ randomized and sequential ignorability, the mediation formula gives

- $\theta(0, 0) = 1 \cdot 0.8 + 3 \cdot 0.2 = 1.4$,
- $\theta(1, 1) = 2 \cdot 0.4 + 5 \cdot 0.6 = 3.8$,
- $\theta(1, 0) = 2 \cdot 0.8 + 5 \cdot 0.2 = 2.6$,

so $\mathrm{TE} = 2.4$, $\mathrm{NDE} = 2.6 - 1.4 = 1.2$ and $\mathrm{NIE} = 3.8 - 2.6 = 1.2$. The linear formulas agree: the saturated outcome regression has $\beta_0 = 1$, $\gamma = 1$, $\beta = 2$, $\theta = 5 - 2 - 3 + 1 = 1$, and the mediator regression has $\alpha_0 = 0.2$, $\alpha = 0.4$, so $\mathrm{NDE} = 1 + 1 \cdot 0.2 = 1.2$ and $\mathrm{NIE} = 0.4 \cdot (2 + 1) = 1.2$. The other split uses $\theta(0, 1) = 1 \cdot 0.4 + 3 \cdot 0.6 = 2.2$: direct effect $3.8 - 2.2 = 1.6$ and indirect effect $2.2 - 1.4 = 0.8$, again summing to 2.4. The difference comes from the interaction $\theta = 1$. The controlled direct effects are $\mathrm{CDE}(0) = 1$ and $\mathrm{CDE}(1) = 2$.

## Classic examples

- **Psychology.** Baron and Kenny (1986) set the practice of testing whether $A$ affects $M$, whether $M$ affects $Y$ given $A$, and whether the effect of $A$ shrinks when $M$ is added. Their paper is among the most cited in the field; the causal assumptions behind it were made explicit only later.
- **Epidemiology.** How much of the effect of smoking on low birth weight goes through gestational age, or how much of the effect of education on health goes through income. Robins and Greenland (1992) gave the counterfactual definitions in this setting.
- **Genetics.** How much of the effect of a variant on disease goes through a measured gene expression or a biomarker.
- **Policy.** How much of the effect of a job training program on earnings goes through employment and how much through hourly wages.
- **Fairness.** Path-specific effects, a generalization, ask how much of the effect of a protected attribute on a decision goes through permitted and forbidden paths.

## Variations

- **Interventional effects.** Replace $M(a^*)$ by a random draw from the distribution of $M(a^*)$. The effects then need no cross-world assumption, and they are identified even with a treatment-induced confounder of $M$ and $Y$, but they no longer add up to the total effect in general.
- **Several mediators.** Joint natural effects through a set of mediators are identified like one; splitting between correlated mediators needs more assumptions or path-specific effects.
- **Sensitivity analysis.** Imai, Keele and Tingley (2010) index violations of assumption 2 by the correlation $\rho$ between the error terms of the mediator and outcome models and report the $\rho$ at which the indirect effect would vanish, in the spirit of [Rosenbaum's sensitivity analysis](/rosenbaum-sensitivity-analysis/).
- **Weighting and doubly robust estimators.** Inverse probability weighting by the mediator model, and estimators that combine weighting with the outcome model so that one correct model suffices.
- **Front-door adjustment.** If $M$ carries the whole effect and the treatment-outcome confounding does not touch $M$, the total effect is identified through $M$ even with unmeasured confounding of $A$ and $Y$. This is the front-door criterion of Pearl, listed under see also.
- **Principal stratification.** For effects within strata of $(M(0), M(1))$, as with compliers in the [local average treatment effect theorem](/local-average-treatment-effect/).

## Pitfalls

- **Assuming the mediator is randomized because the treatment is.** Randomizing $A$ gives assumption 1 for free but says nothing about assumption 2. A confounder of $M$ and $Y$ biases both natural effects, even in a perfect trial.
- **Adjusting for variables affected by the treatment.** Putting a post-treatment variable in $X$ breaks assumption 1; if it confounds $M$ and $Y$, the natural effects are not identified.
- **Using the Baron-Kenny steps as a causal test.** Requiring a significant total effect before looking for mediation has low power and is not needed; a significant product of coefficients is not evidence of a causal path unless the assumptions hold.
- **Ignoring the interaction.** With $A \times M$ interaction, $\gamma$ is a controlled direct effect at $M = 0$, not the natural direct effect, and $\alpha\beta$ is not the indirect effect.
- **Nonlinear models and the difference method.** In logistic regression, the change in the coefficient of $A$ when $M$ is added mixes mediation with the noncollapsibility of the odds ratio.
- **Measurement error in $M$.** In linear models, classical error in $M$ biases the indirect effect toward 0 and the direct effect away from it.
- **Reading the proportion mediated as a fraction of people.** $\mathrm{NIE}/\mathrm{TE}$ can be above 1 or negative when the two effects have opposite signs.

## Exercises

1. Show that $\mathrm{NDE} + \mathrm{NIE} = \mathrm{TE}$, and that the second split, with $\mathbb{E}[Y(1, M(1)) - Y(0, M(1))]$ as the direct part, also sums to $\mathrm{TE}$.
   <details><summary>Answer</summary>Both are telescoping sums: $Y(1, M(1)) - Y(0, M(0)) = [Y(1, M(1)) - Y(1, M(0))] + [Y(1, M(0)) - Y(0, M(0))] = [Y(1, M(1)) - Y(0, M(1))] + [Y(0, M(1)) - Y(0, M(0))]$. Take expectations.</details>
2. In the worked example, compute $\mathrm{NDE}$ and $\mathrm{NIE}$ from the linear formulas with $\bar m_0$ replaced by $\bar m_1 = 0.6$ and $\beta$ by $\beta$ alone, and say which split these numbers give.
   <details><summary>Answer</summary>$\gamma + \theta\bar m_1 = 1 + 0.6 = 1.6$ and $\alpha\beta = 0.4 \cdot 2 = 0.8$: the second split, direct effect with the mediator at its treated distribution and indirect effect under no treatment.</details>
3. Show that if $\theta = 0$ and there are no covariates, the plug-in NIE is $\hat\alpha\hat\beta$ and that it equals $\hat\tau - \hat\gamma$.
   <details><summary>Answer</summary>With linear models, $\theta(1, 1) - \theta(1, 0) = \hat\beta(\bar m_1 - \bar m_0) = \hat\beta\hat\alpha$ since $\hat\alpha$ is the difference of mediator means. The second part is the product-equals-difference identity.</details>
4. A trial randomizes both $A$ and $M$ (for example, a drug and a dose of a cholesterol-lowering agent). Which effects does it identify without further assumptions?
   <details><summary>Answer</summary>The total effect (from the arm where $M$ is not set) and the controlled direct effects $\mathrm{CDE}(m)$. Not the natural effects, since $Y(1, M(0))$ needs each unit's $M(0)$, which is not seen in the arm where $A = 1$.</details>
5. Give an example where $\mathrm{NIE}$ and $\mathrm{NDE}$ have opposite signs, and explain why the proportion mediated is then misleading.
   <details><summary>Answer</summary>A drug that lowers blood pressure (good) but causes weight gain that raises it (bad): $\mathrm{NDE} = -10$, $\mathrm{NIE} = +4$, $\mathrm{TE} = -6$, so the proportion mediated is $4/(-6) = -0.67$, which has no meaning as a share.</details>

## References
