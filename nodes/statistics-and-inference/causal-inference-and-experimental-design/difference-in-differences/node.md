---
tag: XKDP5H
kind: technique
slug: difference-in-differences
name: Difference in differences
aliases:
- DiD
- diff-in-diff
area: statistics-and-inference/causal-inference-and-experimental-design
level: core
summary: Estimates an effect by the change over time in the treated group minus the change in a control group, valid under parallel trends.
prereqs: [potential-outcomes-framework, average-treatment-effect, welch-t-test]
see_also: [synthetic-control-method, cluster-robust-standard-errors, ordinary-least-squares, regression-discontinuity-design, cuped, inverse-probability-weighting, permutation-test, block-bootstrap]
sources:
  - paper: "David Card and Alan B. Krueger, Minimum wages and employment: a case study of the fast-food industry in New Jersey and Pennsylvania, American Economic Review 84(4), 1994, pp. 772-793"
    title: David Card and Alan B. Krueger, Minimum wages and employment, a case study of the fast-food industry in New Jersey and Pennsylvania, American Economic Review 84(4), 1994
    locator: pp. 772 to 793, the table of mean full-time-equivalent employment by state and wave (general locator, the table number was not checked)
  - paper: doi:10.2307/1924810
    title: Orley Ashenfelter and David Card, Using the longitudinal structure of earnings to estimate the effect of training programs, The Review of Economics and Statistics 67(4), 1985
    locator: the article starting on p. 648 (comparison of earnings changes of trainees and a comparison group)
  - paper: doi:10.1162/003355304772839588
    title: Marianne Bertrand, Esther Duflo and Sendhil Mullainathan, How much should we trust differences-in-differences estimates?, The Quarterly Journal of Economics 119(1), 2004
    locator: pp. 249 to 275 (serial correlation and the over-rejection of placebo laws; clustering and collapsing as fixes)
  - paper: doi:10.1111/0034-6527.00321
    title: Alberto Abadie, Semiparametric difference-in-differences estimators, The Review of Economic Studies 72(1), 2005
    locator: pp. 1 to 19 (parallel trends conditional on covariates, propensity score weighting)
  - paper: doi:10.1016/j.jeconom.2021.03.014
    title: Andrew Goodman-Bacon, Difference-in-differences with variation in treatment timing, Journal of Econometrics 225(2), 2021
    locator: pp. 254 to 277 (the two-way fixed effects estimate as a weighted average of all two-group two-period comparisons)
  - paper: doi:10.1257/aer.20181169
    title: Clément de Chaisemartin and Xavier D'Haultfœuille, Two-way fixed effects estimators with heterogeneous treatment effects, American Economic Review 110(9), 2020
    locator: pp. 2964 to 2996 (the weights on the cell effects and the possibility of negative weights)
  - paper: doi:10.1016/j.jeconom.2020.12.001
    title: Brantly Callaway and Pedro H. C. Sant'Anna, Difference-in-differences with multiple time periods, Journal of Econometrics 225(2), 2021
    locator: pp. 200 to 230 (group-time average treatment effects and their aggregation)
  - paper: doi:10.1016/j.jeconom.2020.09.006
    title: Liyang Sun and Sarah Abraham, Estimating dynamic treatment effects in event studies with heterogeneous treatment effects, Journal of Econometrics 225(2), 2021
    locator: pp. 175 to 199 (contamination of event-study coefficients by other relative periods)
---

Difference in differences estimates the effect of a treatment that some units get at some time and others do not. It takes the change in the mean outcome of the treated units from before to after, and subtracts the change of the untreated units over the same period. The first difference removes fixed differences between the groups, the second removes the common change over time, and what is left is the effect of the treatment if the treated group would have followed the same trend as the control group without it. That assumption, parallel trends, is weaker than random assignment, because the groups may differ in level. It is untestable for the period after treatment. With two groups and two periods the estimate is exactly the interaction coefficient of an OLS regression, so the usual regression tools apply. With many groups adopting at different times, the common two-way fixed effects regression is a weighted average of cell effects with weights that can be negative, and newer estimators avoid this.

## In plain words

New Jersey raised its minimum wage in 1992 and Pennsylvania did not. Employment in New Jersey fast-food shops changed by some amount over the year. Part of that change would have happened anyway, because of the season, the economy and so on. Pennsylvania shops next door felt the same season and economy but not the new wage, so their change estimates the part that would have happened anyway. Subtract it, and the rest is the effect of the wage.

The two states need not have the same employment level. They only need the same change without the law.

## When it applies

Two groups, treated ($G = 1$) and control ($G = 0$), are seen before ($t = 0$) and after ($t = 1$) the treated group gets the treatment. Each unit has potential outcomes $Y_t(0)$ and $Y_t(1)$ in each period. The target is the average effect on the treated in the after period,

$$\tau_{\text{ATT}} = \mathbb{E}[Y_1(1) - Y_1(0) \mid G = 1].$$

**Identification.** Assume:

1. **No anticipation.** Before the treatment, the outcome is the untreated one: $Y_0 = Y_0(0)$ for every unit.
2. **Parallel trends.** $\mathbb{E}[Y_1(0) - Y_0(0) \mid G = 1] = \mathbb{E}[Y_1(0) - Y_0(0) \mid G = 0]$.

Then

$$\tau_{\text{ATT}} = \big(\mathbb{E}[Y_1 \mid G = 1] - \mathbb{E}[Y_0 \mid G = 1]\big) - \big(\mathbb{E}[Y_1 \mid G = 0] - \mathbb{E}[Y_0 \mid G = 0]\big).$$

*Proof.* The treated show $Y_1 = Y_1(1)$ after, and the controls show $Y_t = Y_t(0)$ in both periods. So $\tau_{\text{ATT}} = \mathbb{E}[Y_1 \mid G = 1] - \mathbb{E}[Y_1(0) \mid G = 1]$. Write the unseen term as $\mathbb{E}[Y_0(0) \mid G = 1] + \mathbb{E}[Y_1(0) - Y_0(0) \mid G = 1]$. The first part is $\mathbb{E}[Y_0 \mid G = 1]$ by no anticipation, and the second is $\mathbb{E}[Y_1 - Y_0 \mid G = 0]$ by parallel trends. Substituting gives the formula. $\blacksquare$

Parallel trends holds, for example, if $Y_t(0) = \alpha_i + \lambda_t + \varepsilon_{it}$ with $\mathbb{E}[\varepsilon_{i1} - \varepsilon_{i0} \mid G] = 0$: any unit effect $\alpha_i$, even one correlated with $G$, cancels. It is a statement about the scale of $Y$: parallel trends in levels and in logs cannot both hold unless the groups have the same baseline. The groups need not be formed at random, but the treatment must not be timed to a shock that hits only the treated, such as a dip in earnings just before a training program (Ashenfelter's dip).

The technique does not apply when there is no untreated group observed over the same periods, when the treatment spreads to the controls (a SUTVA failure), or when the groups were on different trends before the treatment.

## The template

**Estimation.** For a panel of $n$ units seen in both periods:

```pseudo id=main
DID(Y_pre, Y_post, G)                   ▷ two periods, G_i = 1 for treated units
L1  ΔY_i ← Y_post,i - Y_pre,i for each unit
L2  τ̂ ← mean of ΔY over treated units - mean of ΔY over control units
L3  se ← √(s₁²/n₁ + s₀²/n₀)             ▷ s_g² the sample variance of ΔY in group g
L4  return (τ̂, se)
```

The cost is $\Theta(n)$. Working with unit changes makes the standard error valid for any correlation between a unit's two outcomes, which is what clustering by unit does. If treatment was assigned to groups of units, such as states, the changes must be averaged or [clustered](/cluster-robust-standard-errors/) by that group, and with few groups the large-sample interval is not reliable; a [permutation test](/permutation-test/) over the groups or a [block bootstrap](/block-bootstrap/) is an alternative.

**The regression form is exact.** For repeated cross-sections, possibly with different units and different counts in each of the four cells, fit by [OLS](/ordinary-least-squares/)

$$Y = \beta_0 + \beta_1 G + \beta_2 P + \beta_3 G P + e,$$

with $P$ the after-period indicator. The four regressors span the indicators of the four cells, so the fitted value in each cell is its mean $\bar y_{gp}$, and solving the four equations gives

$$\beta_0 = \bar y_{00}, \quad \beta_1 = \bar y_{10} - \bar y_{00}, \quad \beta_2 = \bar y_{01} - \bar y_{00}, \quad \beta_3 = (\bar y_{11} - \bar y_{10}) - (\bar y_{01} - \bar y_{00}).$$

For a balanced panel the cell means are the means of the units, so $\beta_3$ is also the output of DID, and it equals the two-way fixed effects coefficient with unit dummies. The tests check all three equalities exactly in fractions, on 100 unbalanced cross-sections and 50 panels.

**Worked example.** Three treated and three control units:

| unit | group | before | after | change |
| --- | --- | --- | --- | --- |
| 1, 2, 3 | treated | 10, 12, 14 | 15, 16, 20 | 5, 4, 6 |
| 4, 5, 6 | control | 8, 9, 13 | 10, 10, 16 | 2, 1, 3 |

The mean changes are 5 and 2, so $\hat\tau = 3$. Both groups have $s^2 = 1$, so $\mathrm{se} = \sqrt{1/3 + 1/3} = 0.82$. The regression on the 12 observations gives $(\beta_0, \beta_1, \beta_2, \beta_3) = (10, 2, 2, 3)$: control before 10, treated before 12, control after 12, treated after $10 + 2 + 2 + 3 = 17$. The after-period difference $17 - 12 = 5$ would include the level gap of 2 that was already there.

**Staggered adoption and two-way fixed effects.** With many periods and groups that start treatment at different times, the common practice is the regression $Y_{it} = \alpha_i + \lambda_t + \beta D_{it} + e_{it}$. By the Frisch-Waugh-Lovell theorem, in a balanced panel $\hat\beta = \sum_{it}\tilde d_{it}Y_{it}/\sum_{it}\tilde d_{it}D_{it}$, where $\tilde d_{it} = D_{it} - \bar D_{i\cdot} - \bar D_{\cdot t} + \bar D_{\cdot\cdot}$ is the double-demeaned treatment. If $Y_{it} = \alpha_i + \lambda_t + \tau_{it}D_{it}$, the unit and time terms vanish because $\tilde d$ has zero row and column sums, so

$$\hat\beta = \sum_{(i, t): D_{it} = 1} w_{it}\,\tau_{it}, \qquad w_{it} = \frac{\tilde d_{it}}{\sum_{js}\tilde d_{js}D_{js}}, \qquad \sum w_{it} = 1.$$

This is exact, and the weights depend only on the treatment pattern. They can be negative (de Chaisemartin and D'Haultfœuille 2020). Take two units and three periods, unit E treated from period 2 and unit L from period 3. The treated cells get weights $w_{E2} = 1$, $w_{E3} = -1/2$ and $w_{L3} = 1/2$. If the effect grows with time in treatment, say $\tau_{E2} = 1$, $\tau_{E3} = 4$ and $\tau_{L3} = 1$, then $\hat\beta = 1 - 2 + 1/2 = -1/2$, although every effect is positive. Goodman-Bacon (2021) explains why: the estimate averages all two-group comparisons, and one of them uses the already treated unit E as the control for L between periods 2 and 3, so E's growing effect is subtracted. Here $\hat\beta = \frac12\tau_{E2} + \frac12(\tau_{L3} - (\tau_{E3} - \tau_{E2}))$.

The fix is to compare only with units that are not treated. The group-time effect of Callaway and Sant'Anna (2021) for the units first treated in period $g$, at period $t \ge g$, is a 2-by-2 difference in differences with base period $g - 1$ and the never-treated units as controls. The code computes it, and a test with effects that grow with exposure checks that it recovers every effect exactly while the two-way fixed effects estimate (11/5 against an average cell effect of 16/5) does not.

**Simulation.** Unit effects with mean 3 higher in the treated group, a common shock of 1.5, a true effect of 2, 40 units per group, normal noise of variance 1 in each period, 1000 samples (seed 2026). Measured: mean estimate 2.010, standard deviation 0.318 (the model value is $\sqrt{0.1} = 0.316$), coverage of the 95% interval 0.948, and the after-period difference in means 5.004, biased by the level gap of 3.

## Classic examples

- **Cholera in London.** John Snow (1855) compared cholera deaths in the 1840s and 1850s between districts whose water company moved its intake upstream and districts whose company did not, an early form of the design.
- **Training programs.** Ashenfelter and Card (1985) compared earnings changes of trainees and a comparison group, and showed that trainees' earnings fell just before they entered, which biases a simple before-and-after comparison.
- **Minimum wage.** Card and Krueger (1994) surveyed fast-food restaurants in New Jersey and eastern Pennsylvania before and after New Jersey's 1992 minimum wage rise. Mean full-time-equivalent employment per store went from 20.44 to 21.03 in New Jersey and from 23.33 to 21.17 in Pennsylvania. The difference in differences is $0.59 - (-2.16) = 2.75$ from these rounded means; the paper reports 2.76 with a standard error of 1.36. Employment did not fall.
- **Policy rollouts.** Laws adopted by different states in different years are the typical staggered case, and the typical place where the two-way fixed effects problem shows up.
- **Product experiments with a holdout region.** When a feature is turned on in one market at a time, the other markets serve as the control, and [CUPED](/cuped/)-like adjustment with the pre-period outcome is a close relative.

## Variations

- **Covariates.** If parallel trends holds only given covariates $X$, regress the changes on $X$ within the controls, or weight the controls by the [propensity score](/propensity-score/) odds as in Abadie (2005), or combine both (doubly robust difference in differences).
- **Event study.** Replace $D_{it}$ by indicators of periods relative to the treatment start. The coefficients before the start test for pre-trends, and those after trace the dynamic effect. With staggered adoption the plain version mixes relative periods (Sun and Abraham 2021); estimate group-time effects first.
- **Group-time effects and aggregation.** Callaway and Sant'Anna (2021): compute the effect for each adoption group and period against never-treated or not-yet-treated units, then average with weights chosen by the analyst.
- **Triple differences.** Add a third contrast, such as an age group the policy does not affect, to remove trends specific to the treated region.
- **Changes in changes.** Athey and Imbens replace parallel trends in means by an assumption on the whole distribution and estimate quantile effects.
- **Synthetic control.** With one treated unit and many possible controls, choose a weighted mix of controls that fits the treated unit's pre-period path; see the [synthetic control method](/synthetic-control-method/).

## Pitfalls

- **Testing pre-trends and then trusting the result.** Parallel pre-trends make the assumption plausible but do not prove it for the after period, and a test with low power passes violations that matter. Conditioning on passing the test also distorts later inference.
- **Standard errors that ignore serial correlation.** Bertrand, Duflo and Mullainathan (2004) found that with many periods and state-level laws, standard errors that treat each state-year as independent reject a placebo law far too often. Cluster at the level of assignment.
- **Few treated groups.** With one treated state, clustering does not help, because the treated state's own shock cannot be separated from the effect.
- **Two-way fixed effects with staggered timing and changing effects.** Negative weights can make the estimate the wrong sign. Use group-time estimators or check the weights.
- **Choosing the scale after the fact.** Parallel trends in logs and in levels are different assumptions.
- **Composition changes.** In repeated cross-sections, if the treatment changes who is sampled after, such as people moving across the border, the cell means compare different populations.

## Exercises

1. Solve the four normal equations of the saturated regression and confirm the formula for $\beta_3$.
   <details><summary>Answer</summary>The fitted values are the cell means, so $\beta_0 = \bar y_{00}$, $\beta_0 + \beta_1 = \bar y_{10}$, $\beta_0 + \beta_2 = \bar y_{01}$, $\beta_0 + \beta_1 + \beta_2 + \beta_3 = \bar y_{11}$. Subtracting gives $\beta_3 = \bar y_{11} - \bar y_{10} - \bar y_{01} + \bar y_{00}$.</details>
2. Suppose the treated group has its own linear trend $\delta t$ in $Y_t(0)$ in addition to the common trend. What does the 2-by-2 estimate converge to?
   <details><summary>Answer</summary>$\tau_{\text{ATT}} + \delta$. The extra trend is not removed.</details>
3. In the three-period example with E treated from period 2 and L from period 3, compute the double-demeaned treatment and confirm the weights $1, -1/2, 1/2$.
   <details><summary>Answer</summary>The treatment rows are $(0, 1, 1)$ and $(0, 0, 1)$. Row means $2/3$, $1/3$, column means $0, 1/2, 1$, grand mean $1/2$. Then $\tilde d_{E2} = 1/3$, $\tilde d_{E3} = -1/6$, $\tilde d_{L3} = 1/6$, and $\sum \tilde d D = 1/3$.</details>
4. Show that in a balanced two-period panel, the regression of $\Delta Y_i$ on $(1, G_i)$ has the same slope as the interaction coefficient in the pooled regression.
   <details><summary>Answer</summary>The slope on a 0/1 regressor is the difference of the group means of $\Delta Y$, that is $(\bar y_{11} - \bar y_{10}) - (\bar y_{01} - \bar y_{00})$ when each group has the same units in both periods, and this is $\beta_3$ by Exercise 1.</details>
5. A treatment starts in period 5, but people learn of it in period 4 and change behaviour. Which assumption fails, and how can the analysis be repaired?
   <details><summary>Answer</summary>No anticipation. Use period 3 as the base period.</details>

## References
