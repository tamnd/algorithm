---
tag: EFBPVW
kind: concept
slug: post-selection-inference
name: Post-selection inference
aliases:
- selective inference
area: statistics-and-inference/regression-and-diagnostics
level: research
summary: Valid tests and intervals for a model chosen from the same data, by conditioning on the selection event or by simultaneous inference over all models.
prereqs: [p-value, confidence-interval, multiple-comparisons-problem, stepwise-regression]
see_also: [polyhedral-lemma, lasso-regression, scheffe-method, bonferroni-correction, false-discovery-rate, knockoff-filter, leaps-and-bounds, akaike-information-criterion]
sources:
  - paper: doi:10.1214/12-AOS1077
    title: "Richard Berk, Lawrence Brown, Andreas Buja, Kai Zhang and Linda Zhao, Valid post-selection inference, Annals of Statistics 41(2), 2013, pp. 802 to 837"
    locator: "The whole paper (the target beta_{j.M}, the PoSI constant, its bounds between the orthogonal case and Scheffe)"
  - paper: doi:10.1073/pnas.1507583112
    title: "Jonathan Taylor and Robert J. Tibshirani, Statistical learning and selective inference, Proceedings of the National Academy of Sciences 112(25), 2015, pp. 7629 to 7634"
    locator: The whole paper (selective type I error, conditioning on the selection event, examples for forward stepwise and the lasso)
  - paper: doi:10.1214/15-AOS1371
    title: "Jason D. Lee, Dennis L. Sun, Yuekai Sun and Jonathan E. Taylor, Exact post-selection inference, with application to the lasso, Annals of Statistics 44(3), 2016, pp. 907 to 927"
    locator: Sections 3 to 5 (the selection event of the lasso as a union of polyhedra and the truncated normal pivot)
  - paper: doi:10.1080/01621459.2015.1108848
    title: "Ryan J. Tibshirani, Jonathan Taylor, Richard Lockhart and Robert Tibshirani, Exact post-selection inference for sequential regression procedures, Journal of the American Statistical Association 111(514), 2016, pp. 600 to 620"
    locator: The whole paper (selective tests and intervals after forward stepwise regression and least angle regression)
  - paper: doi:10.1017/S0266466605050036
    title: "Hannes Leeb and Benedikt M. Pötscher, Model selection and inference: facts and fiction, Econometric Theory 21(1), 2005, pp. 21 to 59"
    locator: The whole paper (the distribution of post-model-selection estimators and why naive inference after selection fails)
  - paper: doi:10.1080/01621459.2020.1732989
    title: "Danijel Kivaranovic and Hannes Leeb, On the length of post-model-selection confidence intervals conditional on polyhedral constraints, Journal of the American Statistical Association 116(534), 2021, pp. 845 to 857"
    locator: The whole paper (the conditional intervals from the polyhedral method have infinite expected length)
  - paper: doi:10.1214/17-AOS1564
    title: "Xiaoying Tian and Jonathan Taylor, Selective inference with a randomized response, Annals of Statistics 46(2), 2018, pp. 679 to 710"
    locator: The whole paper (adding noise to the selection step for more power after selection)
  - paper: doi:10.1214/13-AOS1175
    title: "Richard Lockhart, Jonathan Taylor, Ryan J. Tibshirani and Robert Tibshirani, A significance test for the lasso, Annals of Statistics 42(2), 2014, pp. 413 to 468"
    locator: The whole paper (the covariance test along the lasso path)
---

Post-selection inference, also called selective inference, is the set of methods that give valid tests and confidence intervals when the hypotheses or the model were chosen by looking at the same data. A regression chosen by [stepwise regression](/stepwise-regression/), by the [lasso](/lasso-regression/) or by an analyst who looked at plots does not have the usual t and F laws, because the data that pass the selection are not a random sample of all data. The classical tests, applied after selection, reject too often and their intervals cover too rarely. There are three exact remedies: use fresh data for the inference, cover all models at the same time, or condition on the event that the given model was selected.

## In plain words

If you throw many darts and draw the target around the one that landed best, the throw looks excellent. A test applied only to the winner of a search is the same: the winner is the result that looked strongest, partly by luck, so the usual test overrates it. One fix is to search on one half of the data and test on the other half. A second fix is to use a stricter test that would be fair for every result you could have picked. A third fix asks a narrower question: among all data sets that would have made you pick this same winner, how unusual is yours? That question has an exact answer for many common search rules, and it gives honest p-values and intervals for the result you actually chose.

## The idea

**What goes wrong.** Let $y = \mu + \varepsilon$ with $\varepsilon \sim N(0, \sigma^2 I)$ and $\sigma$ known, and let a rule $\hat M(y)$ choose a model or a hypothesis. A classical test of a fixed hypothesis $H$ has $P(\text{reject } H) \le \alpha$. After selection we test $H_{\hat M}$, and the guarantee is lost, for two reasons. First, multiplicity: the rule looked at many candidates. Second, the selection and the test use the same noise, and a candidate that was picked because its noise was large will have a large test statistic. In the simplest case, $y \sim N(\mu, I_m)$, the rule picks the largest $|y_j|$ and the analyst reports the usual 95% interval $y_j \pm 1.96$. If $\mu = 0$, the interval covers the selected mean only when all $m$ values have $|y_j| < 1.96$, which has probability $0.95^m$: 0.774 for $m = 5$ and 0.599 for $m = 10$.

**What the target is.** In regression, the coefficient of a variable depends on which other variables are in the model. Berk et al. (2013) make this explicit: for a model $M \subseteq \{1, \dots, m\}$ and $j \in M$, the target $b_{j \cdot M}$ is the $j$-th coefficient of the least squares projection of $\mu = E[y]$ on the columns $X_M$. It is defined whether or not the model is "true". After selection the target is $b_{j \cdot \hat M}$, a random quantity, and a valid interval must cover it with the stated probability.

**Remedy 1: split the sample.** Select $\hat M$ on one part of the observations and test on the other part. If the rows are independent, the second part is independent of $\hat M$, and every classical method is exact on it. The cost is power, because both steps use only part of the data, and the selected model depends on the random split.

**Remedy 2: simultaneous inference (PoSI).** Find a constant $K$ such that, with probability $1 - \alpha$, every $t$ statistic of every target $b_{j \cdot M}$ over all models $M$ and all $j \in M$ is at most $K$ in absolute value. Then the intervals $\hat b_{j \cdot M} \pm K \cdot \mathrm{se}$ cover their targets for every model at the same time, so they are valid after any selection rule, including an informal one. The PoSI constant depends only on $X$ and $\alpha$. For orthogonal columns each $\hat b_{j \cdot M}$ is the same for all $M$ that contain $j$, so $K$ is the constant for the maximum of $m$ independent $|z|$ values. For every design, $K$ is at most the [Scheffé](/scheffe-method/) constant $\sqrt{\chi^2_{m, 1-\alpha}}$, because every $t$ statistic is a unit contrast in the $m$-dimensional column space of the centered design. With $\sigma$ known and $\alpha = 0.05$:

| $m$ | orthogonal design | [Bonferroni](/bonferroni-correction/) over $m$ | Scheffé bound |
|---|---|---|---|
| 1 | 1.960 | 1.960 | 1.960 |
| 5 | 2.569 | 2.576 | 3.327 |
| 10 | 2.800 | 2.807 | 4.279 |
| 20 | 3.016 | 3.023 | 5.605 |

The orthogonal value grows like $\sqrt{2\log m}$ and the Scheffé bound like $\sqrt m$. Berk et al. show that some designs need a constant of order $\sqrt m$. Computing $K$ for a general design means a search over all $m 2^{m-1}$ pairs $(j, M)$, which limits PoSI to about $m \le 20$.

**Remedy 3: conditional (selective) inference.** Test $H_{\hat M}$ with a test that is valid given the event that $\hat M$ was selected:

$$P\bigl(\text{reject } H_M \mid \hat M = M\bigr) \le \alpha \quad \text{for every } M \text{ with } H_M \text{ true}.$$

This is the selective type I error (Taylor and Tibshirani 2015). Averaging over the selected $M$ shows that the long-run rate of false rejections among the hypotheses actually tested is also at most $\alpha$, whatever the selection rule does. For normal $y$ with known covariance and a selection event that is a polyhedron $\{Ay \le b\}$, the [polyhedral lemma](/polyhedral-lemma/) gives an exact pivot: a linear contrast $\eta^\top y$, given the event and the part of $y$ independent of $\eta^\top y$, has a normal law truncated to an interval that can be computed from $y$. The lasso with fixed $\lambda$, forward stepwise regression, least angle regression and the rule "pick the largest $|y_j|$" all have polyhedral selection events (Lee et al. 2016; Tibshirani et al. 2016). Conditioning uses only the information that the selection did not use, so it is exact in finite samples under its assumptions, with no multiplicity correction over the models that were not chosen.

**Costs and limits.** Selective intervals can be very long when the observed value is close to the edge of the selection region, because then the data barely passed the selection and say little. Kivaranovic and Leeb (2021) proved that the polyhedral intervals have infinite expected length in common settings. Conditioning on more than the selection (for example on the signs of the lasso, or on the full part of $y$ orthogonal to $\eta$) is simpler but loses power. Adding a small amount of random noise to $y$ before selection (Tian and Taylor 2018) leaves more information for the inference, at the price of a slightly worse selection. Leeb and Pötscher (2005) showed a different limit: the distribution of an estimator after a data-driven model choice cannot be estimated uniformly well, so "fix the naive standard error" methods such as a [bootstrap](/bootstrap-method/) of the whole procedure have no uniform guarantee.

**Assumptions.** The exact results of remedies 2 and 3 assume normal errors with known variance, or a $t$ version with an independent estimate of $\sigma^2$ for PoSI. With unknown $\sigma^2$, non-normal errors or a non-polyhedral rule, the selective tests are only approximately valid, and their validity is proved only under extra conditions.

## Examples

**Testing the winner.** Take $m = 5$ independent $N(\mu_j, 1)$ values, select $j$ with the largest $|y_j|$, and form a 95% interval for $\mu_j$. In 4000 simulated data sets (seed 20261114), the naive interval $y_j \pm 1.96$ covered the selected mean 77.2% of the time when $\mu = 0$ and 87.2% of the time when $\mu = (1, 0.5, 0, 0, -2)$. The selective interval from the polyhedral lemma covered 95.1% in both cases. The coverage of the selective interval is proved to be exactly 95% given each selection; the two simulated rates are measurements. The polyhedral lemma page works one data set of this kind by hand.

**Forward selection on noise.** On the [stepwise regression](/stepwise-regression/) page, forward selection on pure noise picks a first variable whose naive test is significant far more often than 5% of the time. The selective test of Tibshirani et al. (2016) for the same first step conditions on the variable and sign that were chosen, and by the polyhedral lemma its rate of false rejection given each choice is exactly the nominal rate.

**Sample splitting with a large data set.** With $n = 10\,000$ independent rows, select variables with the lasso on 5000 rows and fit ordinary least squares with the selected variables on the other 5000. With normal errors, the t intervals on the second half are exact for the targets $b_{j \cdot \hat M}$ of the selected model, at the cost of standard errors about $\sqrt 2$ times as large as those of a fit on all rows.

**Non-example: a model fixed in advance.** If the model and the hypotheses were registered before the data were seen, there is no selection, and the classical tests are valid as they are. Selection with a fixed set of hypotheses tested together is a [multiple comparisons](/multiple-comparisons-problem/) problem, handled by the [family-wise error rate](/family-wise-error-rate/) or the [false discovery rate](/false-discovery-rate/).

**Non-example: a selection that ignores $y$.** Choosing variables from $X$ alone, for example by dropping one of two highly correlated columns, does not change the law of $y$ given $X$, so classical inference given $X$ stays valid.

## Where it is used

- Regression after variable selection by stepwise methods, [best subset search](/leaps-and-bounds/), the lasso or an [information criterion](/akaike-information-criterion/), when the analyst wants p-values and intervals for the chosen coefficients.
- Genomics and other screening studies, to give intervals for the effect sizes of the top hits that are not inflated by the selection (the "winner's curse").
- Exploratory data analysis, where PoSI protects against an informal search.
- Changepoint detection and clustering, where the hypothesis (a change at the detected time, a difference between the found clusters) is formed from the data, and tests that condition on the selection event give valid p-values.
- Variable selection with error control is a separate aim: the [knockoff filter](/knockoff-filter/) controls the false discovery rate of the selected set, but it does not give intervals for the coefficients.

## References
