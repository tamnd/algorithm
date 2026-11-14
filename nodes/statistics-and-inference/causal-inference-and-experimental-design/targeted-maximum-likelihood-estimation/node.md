---
tag: SKN7EC
kind: algorithm
slug: targeted-maximum-likelihood-estimation
name: Targeted maximum likelihood estimation
aliases:
- TMLE
- targeted minimum loss-based estimation
area: statistics-and-inference/causal-inference-and-experimental-design
level: research
summary: Van der Laan's estimator that fits an initial outcome model and then updates it along the efficient influence function, giving a doubly robust plug-in estimate.
model: real-ram
complexity:
  vars: {n: "the number of units", k: "the number of Newton-Raphson steps for the fluctuation"}
  time: {worst: Θ(k n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, doubly_robust: true, plug_in: true, stays_in_outcome_range: true, solves_efficient_score_equation: true, needs_positivity: true}
history:
  year: 2006
  people: [Mark J. van der Laan, Daniel Rubin]
  note: Van der Laan and Rubin introduced targeted maximum likelihood learning in 2006. Gruber and van der Laan gave the logistic fluctuation for bounded continuous outcomes in 2010, and van der Laan and Rose wrote the textbook in 2011.
prereqs: [augmented-inverse-probability-weighting, influence-function]
see_also: [double-machine-learning, inverse-probability-weighting, propensity-score, average-treatment-effect, m-estimator, newton-raphson-method, cross-validation, random-forest]
sources:
  - paper: doi:10.2202/1557-4679.1043
    title: Mark J. van der Laan and Daniel Rubin, Targeted maximum likelihood learning, The International Journal of Biostatistics 2(1), 2006
    locator: the whole article (the targeting step along a submodel whose score is the efficient influence function, and its double robustness)
  - paper: doi:10.2202/1557-4679.1260
    title: Susan Gruber and Mark J. van der Laan, A targeted maximum likelihood estimator of a causal effect on a bounded continuous outcome, The International Journal of Biostatistics 6(1), 2010
    locator: the whole article (scaling the outcome to [0, 1] and using the logistic fluctuation)
  - book: isbn:9781441997814
    title: Mark J. van der Laan and Sherri Rose, Targeted Learning, Causal Inference for Observational and Experimental Data, Springer, 2011
    locator: Chapter 4 (introduction to TMLE, pp. 67 to 82) and Chapter 5 (understanding TMLE)
  - paper: doi:10.1111/j.1541-0420.2005.00377.x
    title: Heejung Bang and James M. Robins, Doubly robust estimation in missing data and causal inference models, Biometrics 61(4), 2005
    locator: pp. 962 to 973 (the regression on the clever covariate, an earlier form of the targeting step)
  - paper: doi:10.2307/2998560
    title: Jinyong Hahn, On the role of the propensity score in efficient semiparametric estimation of average treatment effects, Econometrica 66(2), 1998
    locator: pp. 315 to 331 (the efficiency bound for the ATE)
---

Targeted maximum likelihood estimation (TMLE) estimates the [average treatment effect](/average-treatment-effect/) as a plug-in: it predicts $Y(1)$ and $Y(0)$ for every unit with an outcome model and averages the difference. Before averaging, it moves the outcome model by one fitted number $\varepsilon$ in the direction of the clever covariate $H = T/e(X) - (1 - T)/(1 - e(X))$, which is built from the [propensity score](/propensity-score/). After this update the residuals, weighted by $H$, add up to zero, so the plug-in estimate equals the [AIPW](/augmented-inverse-probability-weighting/) estimate at the updated model. It is therefore doubly robust in the same way as AIPW, and with a logistic update it keeps the estimate inside the range of the outcome, which AIPW does not.

## In plain words

Start with a model that predicts each person's outcome with and without treatment, and average the predicted differences. If the model is wrong, the answer is biased. AIPW fixes this by adding weighted prediction errors to the answer, but that addition can push the answer to impossible values, such as a probability above one.

TMLE puts the fix into the model instead of into the answer. It nudges every prediction by a small amount, more for people with a low chance of the treatment they got, and picks the size of the nudge so that the weighted prediction errors cancel out. Then it averages the nudged predictions. The answer has the same protection as AIPW, but since it is an average of predictions, it always makes sense.

## The problem

**Identification.** This is the same as for [IPW](/inverse-probability-weighting/) and AIPW. The estimand is $\tau = \mathbb{E}[Y(1) - Y(0)]$. Under consistency with [SUTVA](/sutva/), [ignorability](/ignorability/) $(Y(0), Y(1)) \perp T \mid X$ and positivity $0 < e(X) < 1$, it is identified by the g-formula $\tau = \mathbb{E}[\mu_1(X) - \mu_0(X)]$ with $\mu_t(x) = \mathbb{E}[Y \mid T = t, X = x]$. The efficient influence function of $\tau$ in the nonparametric model is

$$D(Y, T, X) = H(T, X)\big(Y - \mu_T(X)\big) + \mu_1(X) - \mu_0(X) - \tau, \qquad H(T, X) = \frac{T}{e(X)} - \frac{1 - T}{1 - e(X)}.$$

Ignorability and SUTVA cannot be checked from the observed data; positivity can be checked in part from the estimated propensities.

**Estimation.** The input is $n$ units with treatment $T_i$, outcome $Y_i$ in a known range $[a, b]$, a propensity value $e_i \in (0, 1)$, and initial predictions $Q_{1i}$ and $Q_{0i}$ of $\mu_1(X_i)$ and $\mu_0(X_i)$ strictly inside $(a, b)$. The outcome and the predictions are scaled to $[0, 1]$ by $u \mapsto (u - a)/(b - a)$; for a binary outcome no scaling is needed. The initial predictions can come from any learner: a [logistic regression](/logistic-regression/) in each arm, or an ensemble chosen by [cross-validation](/cross-validation/) (the super learner of van der Laan and Rose). The output is the estimate $\hat\tau$, its parts $\hat\mu_1$ and $\hat\mu_0$, the fitted $\hat\varepsilon$, and a standard error.

## The algorithm

```pseudo id=main
TMLE-ATE(T, Y, e, Q1, Q0)             ▷ Y, Q1, Q0 scaled to [0, 1]; 0 < e_i < 1; 0 < Q < 1
L1  for i ← 1 to n do H_i ← T_i / e_i - (1 - T_i) / (1 - e_i);  o_i ← logit Q_{T_i, i}
L2  ε ← 0
L3  repeat
L4      U ← Σ_i H_i (Y_i - expit(o_i + ε H_i));  I ← Σ_i H_i² q_i (1 - q_i)   ▷ q_i = expit(o_i + ε H_i)
L5      δ ← U / I;  halve δ while the log-likelihood at ε + δ is below the one at ε
L6      ε ← ε + δ
L7  until |δ| < tol (1 + |ε|)
L8  for i ← 1 to n do Q1*_i ← expit(logit Q1_i + ε / e_i);  Q0*_i ← expit(logit Q0_i - ε / (1 - e_i))
L9  μ1 ← mean(Q1*);  μ0 ← mean(Q0*);  return (μ1 - μ0, μ1, μ0, ε)
```

Line L1 builds the clever covariate and the offset, the initial prediction for the arm each unit was in, on the logit scale. Lines L2 to L7 fit the one-parameter logistic regression of $Y$ on $H$ with that offset and no intercept, by [Newton-Raphson](/newton-raphson-method/) on its score $U$, with step halving so that no step lowers the log-likelihood. The log-likelihood is strictly concave in $\varepsilon$, so the root of $U$ is the unique maximizer. The code uses $\mathrm{tol} = 10^{-12}$ and at most 100 steps. If $H$ separates the outcome (every unit with $H > 0$ has $Y = 1$ and every unit with $H < 0$ has $Y = 0$, or the reverse), no maximizer exists and the code raises an error. Line L8 updates both predictions of every unit, not only the observed one, and line L9 averages them. Multiply by $b - a$ to return to the original scale.

**Variance.** The influence-function variance is

$$v = \frac{1}{n(n - 1)}\sum_{i=1}^n \hat D_i^2, \qquad \hat D_i = H_i(Y_i - Q^*_{T_i i}) + Q^*_{1i} - Q^*_{0i} - \hat\tau,$$

and $\hat\tau \pm z_{1 - \alpha/2}\sqrt v$ is a normal [confidence interval](/confidence-interval/) of approximate level $1 - \alpha$ when both working models are consistent. This is cited (van der Laan and Rose 2011), not proved here.

**Linear fluctuation.** For an unbounded outcome with squared loss, the update is $Q^*_t = Q_t + \varepsilon H(t, X)$, and $\hat\varepsilon = \sum_i H_ir_i/\sum_i H_i^2$ with $r_i = Y_i - Q_{T_i i}$ is one least squares step. It solves the score equation exactly but loses the range guarantee.

## Example

Take the eight units of the [IPW page](/inverse-probability-weighting/) with a binary outcome: $Y = 1$ for the five mild units and $Y = 0$ for the three severe ones. The design propensity is $1/4$ for $x = 0$ and $3/4$ for $x = 1$, and the initial outcome model ignores $x$: $Q_1 = 1/2$ (the treated mean) and $Q_0 = 3/4$ (the control mean).

| unit | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $x$ | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| $T$ | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 |
| $Y$ | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| $H$ | 4 | 4 | $-4/3$ | $-4/3$ | $-4/3$ | $4/3$ | $4/3$ | $-4$ |
| residual $r = Y - Q_T$ | 1/2 | 1/2 | 1/4 | 1/4 | 1/4 | $-1/2$ | $-1/2$ | $-3/4$ |

The initial plug-in is $1/2 - 3/4 = -1/4$, and AIPW at the initial model gives $1/3$. The linear fluctuation is easy to follow by hand: $\sum_i H_ir_i = 4 - \tfrac43 - 1 + 3 = 14/3$ and $\sum_i H_i^2 = 32 + \tfrac{32}9 + \tfrac{48}9 + 16 = 512/9$, so $\hat\varepsilon = 21/256$. The updated treated predictions are $\tfrac12 + 4\hat\varepsilon = 53/64$ for $x = 0$ and $\tfrac12 + \tfrac43\hat\varepsilon = 39/64$ for $x = 1$; the control predictions are $\tfrac34 - \tfrac43\hat\varepsilon = 41/64$ and $\tfrac34 - 4\hat\varepsilon = 27/64$. Averaging over the five mild and three severe units, $\hat\mu_1 = 191/256$, $\hat\mu_0 = 143/256$ and $\hat\tau = 48/256 = 3/16$. AIPW evaluated at the updated predictions also gives $3/16$, since the weighted residuals now add to zero.

The logistic fluctuation of lines L2 to L7 gives $\hat\varepsilon \approx 0.3736$ and $\hat\tau \approx 0.1892$, with $\hat\mu_1 \approx 0.7437$ and $\hat\mu_0 \approx 0.5545$. The stratified estimate is 0, since all units in a stratum have the same outcome. The propensities are the true design values, so all three estimates are consistent, but eight units are far too few for them to agree: the answers $1/3$, $3/16$ and $0.189$ differ by terms that shrink only in large samples. The example shows the arithmetic, not the accuracy.

## Correctness

The proofs establish:

- the log-likelihood of the fluctuation is strictly concave in $\varepsilon$; a maximizer exists unless $H$ separates the outcome, and it solves the score equation $\sum_i H_i(Y_i - Q^*_{T_i i}) = 0$;
- any predictions that solve this score equation make the plug-in estimate equal to the AIPW estimate at those predictions (exactly; the tests check it with fractions for the linear fluctuation and to $10^{-10}$ for the logistic one);
- with the logistic fluctuation every updated prediction, and so the estimate, lies inside the range of the outcome;
- if the propensity is constant within each arm and the initial fits are logistic regressions with an intercept in each arm, the update is $\hat\varepsilon = 0$;
- the population limit $\bar\tau$ of the procedure equals $\tau$ if either the propensity or the initial outcome model is right.

The convergence of the estimate to that limit, its asymptotic normality and efficiency, and the coverage of the interval are cited from van der Laan and Rubin (2006) and van der Laan and Rose (2011), not proved. The simulation numbers are measured.

## Complexity

Each Newton-Raphson step does $\Theta(n)$ work (two sums, and a log-likelihood evaluation per halving), so with $k$ steps the fluctuation costs $\Theta(kn)$; $k$ is small in practice, since the problem is one-dimensional and concave. Lines L1, L8 and L9 are $\Theta(n)$. The code keeps the offsets and the updated predictions, $\Theta(n)$ extra space. The initial fits dominate the cost when flexible learners are used. The linear fluctuation needs one pass and no iteration.

## Properties

- **Plug-in.** The estimate is $\frac1n\sum_i(Q^*_{1i} - Q^*_{0i})$, an average of predictions that obey the model's range. In a near-positivity example with four units ($T = 1, 1, 0, 0$; $Y = 1, 0, 0, 1$; $e = 0.05, 0.5, 0.5, 0.5$; all initial predictions 0.2), AIPW estimates $\Pr[Y(1) = 1]$ as 4.1 and the ATE as 3.6; TMLE gives $\hat\mu_1 = 0.424$ and $\hat\tau = 0.270$.
- **Doubly robust.** In a simulation with $X$ uniform on $[0, 1]$, $e(x) = \operatorname{expit}(-2 + 4x)$, $\Pr[Y = 1 \mid T, X] = \operatorname{expit}(-1 + 2X + T(1 - X))$, true ATE $\log((1 + \mathrm{e})/2) - 1/2 \approx 0.1201$, $n = 1000$ and 200 samples (seed 2026), with logistic models in $1, x$ as the right models and constants as the wrong ones:

| working models | mean of $\hat\tau$ | SD | 95% coverage | largest $\lvert\mathrm{TMLE} - \mathrm{AIPW}\rvert$ |
|---|---|---|---|---|
| both right | 0.1169 | 0.0371 | 0.940 | 0.0009 |
| outcome wrong | 0.1171 | 0.0371 | 0.945 | 0.0065 |
| propensity wrong | 0.1173 | 0.0352 | 0.895 | 0 |
| both wrong | 0.2151 | 0.0309 | 0.130 | 0 |

The two estimators agree to the third decimal on the same fits. With a constant propensity the update is exactly 0 (the last proved property above), so the last two rows equal AIPW. These numbers are measured.

- **Same asymptotics as AIPW.** When the nuisance estimates converge fast enough, TMLE and AIPW have the same influence function and so the same limiting variance, which reaches Hahn's (1998) efficiency bound if both models are right. Their difference is of second order.
- **Many parameters, one framework.** The same recipe (a submodel through the initial fit whose score at $\varepsilon = 0$ contains the efficient influence function, then a plug-in) gives estimators of the ATT, of risk ratios, of survival curves and of effects of time-varying treatments.

## Variants and improvements

- **Super learner for the initial fit.** Van der Laan and Rose recommend fitting $Q$ and $e$ by a cross-validated ensemble of learners, so that both are likely to be consistent.
- **Cross-validated TMLE.** Fit the nuisances on other folds than the ones used in the update, as in [double machine learning](/double-machine-learning/), to drop the Donsker conditions that flexible learners may break.
- **Collaborative TMLE.** Chooses the propensity model in steps, guided by the fit of the targeted outcome model, to avoid weights that add variance without removing bias.
- **Iterated and one-step versions.** For parameters whose clever covariate depends on $Q$ itself, the fluctuation is repeated until the score equation holds. The one-step estimator is AIPW: it adds the mean influence function to the plug-in without changing the model.
- **Weighted fluctuation.** Fitting $\varepsilon$ with covariate $T - (1 - T)$ and weights $1/\tilde e$ or $1/(1 - \tilde e)$ solves the same score equation and is often more stable when the weights are large.

## When to use it

Use TMLE when you would use AIPW and the outcome is bounded, especially binary, and the propensities come near 0 or 1, since the plug-in form keeps the estimate in range, which Gruber and van der Laan (2010) found also makes it more stable in finite samples. It is also the natural choice for parameters beyond the ATE, such as survival probabilities, where an average of predictions is easier to keep valid than a weighted correction. For a continuous outcome with no natural bounds, AIPW or the linear fluctuation is simpler and gives almost the same answer.

## Pitfalls

- **The bounds of the outcome.** The logistic fluctuation needs a known range $[a, b]$, and the initial predictions must be strictly inside it. Taking $a$ and $b$ as the sample minimum and maximum is common; truncate predictions a little inside, such as to $[0.001, 0.999]$ on the scale of $[0, 1]$.
- **Truncating the propensities.** Bounding $\tilde e$ to an interval such as $[0.025, 0.975]$ stabilizes $H$ but changes the target slightly; report the bound.
- **Not a fix for confounding.** Like every method that uses only $X$, TMLE assumes [ignorability](/ignorability/); targeting improves the estimate of a statistical quantity, not its causal meaning.
- **Overfitting.** A learner that interpolates the data makes $Y_i - Q_{T_i i}$ nearly 0, so the update does nothing and the bias of the initial fit stays. Use cross-validated fits.
- **A separated update.** With very few units, $H$ can separate a binary outcome and the fluctuation has no maximum. The code reports this rather than returning a huge $\varepsilon$.
- **Coverage with a wrong model.** In the table above, coverage was 0.895 with the wrong propensity model, below the nominal 0.95. The influence-function variance assumes both models are consistent.

## Implementations

## History

Van der Laan and Rubin (2006) introduced targeted maximum likelihood learning as a general way to turn an initial density estimate into an estimator that solves the efficient influence function equation for a chosen parameter, and so is doubly robust and efficient when the nuisances are well estimated. The clever covariate had appeared before as a regression term in the doubly robust estimators of Scharfstein, Rotnitzky and Robins (1999) and Bang and Robins (2005). Gruber and van der Laan (2010) showed that the logistic fluctuation on a scaled outcome keeps estimates in range for bounded continuous outcomes. Van der Laan and Rose (2011) wrote the book that made the method widely used, with the super learner for the initial fits. The method was later renamed targeted minimum loss-based estimation, keeping the abbreviation, because the update can use any loss function.

## References
