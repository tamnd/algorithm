---
tag: BV262Y
kind: concept
slug: loss-function
name: Loss function
aliases:
area: machine-learning/supervised-learning
level: intro
summary: "A loss scores one prediction against its label. Learning minimizes the mean loss; convex surrogates stand in for the 0-1 loss when they are classification calibrated."
prereqs: [expected-value, conditional-expectation]
see_also: [empirical-risk-minimization, generalization-error, mean-squared-error, cross-entropy-loss, logistic-loss, hinge-loss, bayes-optimal-classifier, convex-function]
sources:
  - paper: doi:10.1198/016214505000000907
    title: Peter L. Bartlett, Michael I. Jordan and Jon D. McAuliffe, Convexity, classification, and risk bounds, Journal of the American Statistical Association 101(473), 138-156, 2006
    locator: Section 2 (classification calibration, the psi-transform and Theorem 1) and Section 3.1 (convex losses are calibrated if and only if differentiable at 0 with a negative derivative)
  - paper: doi:10.1198/016214506000001437
    title: Tilmann Gneiting and Adrian E. Raftery, Strictly proper scoring rules, prediction, and estimation, Journal of the American Statistical Association 102(477), 359-378, 2007
    locator: Section 2 (proper scoring rules and their convex characterization) and Section 3 (the logarithmic, Brier and spherical scores for categorical outcomes)
  - paper: doi:10.1214/aos/1079120130
    title: Tong Zhang, Statistical behavior and consistency of classification methods based on convex risk minimization, The Annals of Statistics 32(1), 56-85, 2004
    locator: the conditional risk of convex margin losses and its link to the excess 0-1 risk
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 10.6 (loss functions and robustness) and Section 12.3.2 (Table 12.1, the margin losses and the functions that minimize them)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Chapter 2 (the loss and the risk), Section 12.3 (surrogate loss functions)
---

A loss function $\ell(\hat y, y) \ge 0$ gives the cost of the prediction $\hat y$ when the true label is $y$. The *risk* of a predictor is its expected loss on a new example, and [empirical risk minimization](/empirical-risk-minimization/) picks the predictor with the smallest mean loss on the training set. In [classification](/classification/) the loss that we care about is the 0-1 loss, but it is hard to minimize, so learners minimize a convex *surrogate* such as the [hinge loss](/hinge-loss/) or the [logistic loss](/logistic-loss/). Classification calibration (Bartlett, Jordan and McAuliffe 2006) is the exact condition under which this does no harm in the limit.

## In plain words

A model makes a guess, and the data gives the right answer. A loss function is a rule that turns the gap between the two into one number: zero for a perfect guess, larger for a worse guess. Training a model means finding the settings that make the average of this number small on the training data.

The choice of the rule decides what the model learns. If big errors cost much more than small ones, the model aims at the average answer. If all errors cost the same per unit, it aims at the middle answer. For yes or no questions, the natural rule counts each mistake as one, but a computer cannot search well with that rule, because it is flat almost everywhere. So we use a smooth bowl-shaped rule instead, and we check that the bowl leads to the same yes or no answers in the end.

## The idea

**Setting.** Examples $(x, y)$ are drawn i.i.d. from an unknown distribution $D$ on $\mathcal X \times \mathcal Y$. A predictor $h$ maps an input to a prediction in a set $\hat{\mathcal Y}$. A loss is a function $\ell : \hat{\mathcal Y} \times \mathcal Y \to [0, \infty)$. For a training set of $n$ examples and a model with parameters $\theta$,

$$R(h) = \mathbb{E}_{(x, y) \sim D}\, \ell(h(x), y), \qquad L(\theta) = \frac1n \sum_{i=1}^{n} \ell(h_\theta(x_i), y_i).$$

$R$ is the risk (the [generalization error](/generalization-error/)) and $L$ is the empirical risk. The *conditional risk* at an input $x$ is $C_x(\hat y) = \mathbb{E}[\ell(\hat y, y) \mid x]$. Because $R(h) = \mathbb{E}_x\, C_x(h(x))$, a predictor that minimizes $C_x$ at each $x$ minimizes $R$. That pointwise minimizer is the Bayes predictor for the loss, and its risk is the Bayes risk $R^*$.

**What the loss decides.** The Bayes predictor depends only on the loss and on the law of $y$ given $x$:

| loss $\ell(\hat y, y)$ | name | Bayes predictor |
|---|---|---|
| $(\hat y - y)^2$ | [squared loss](/mean-squared-error/) | $\mathbb{E}[y \mid x]$, the [conditional mean](/conditional-expectation/) |
| $\lvert \hat y - y \rvert$ | absolute loss | a conditional [median](/median/) |
| $\max(\tau(y - \hat y), (\tau - 1)(y - \hat y))$ | pinball loss | a conditional $\tau$-quantile ([quantile regression](/quantile-regression/)) |
| $\mathbb{1}[\hat y \ne y]$ | 0-1 loss | $\arg\max_j P(y = j \mid x)$, the [Bayes classifier](/bayes-optimal-classifier/) |
| $-\log p_y$ for a distribution $p$ | log loss ([cross-entropy](/cross-entropy-loss/)) | $p = P(y = \cdot \mid x)$ |

**Margin losses.** In binary classification take $y \in \{-1, +1\}$ and a real score $f(x)$; predict $\operatorname{sign} f(x)$. The *margin* is $m = y f(x)$, and a margin loss has the form $\ell = \varphi(y f(x))$:

| $\varphi(m)$ | name | used by |
|---|---|---|
| $\mathbb{1}[m \le 0]$ | 0-1 | the target |
| $\max(0, 1 - m)$ | [hinge](/hinge-loss/) | [support vector machines](/support-vector-machine/) |
| $\log(1 + e^{-m})$ | [logistic](/logistic-loss/) | [logistic regression](/logistic-regression/) |
| $e^{-m}$ | exponential | [AdaBoost](/adaboost/) |
| $(1 - m)^2$ | squared | least squares on $\pm 1$ targets |

The 0-1 loss is not convex and its gradient is zero almost everywhere. Minimizing the empirical 0-1 loss over halfspaces in the agnostic setting is computationally hard (Shalev-Shwartz and Ben-David, Section 12.3). The other four are [convex](/convex-function/) in $m$, so for a linear score $f(x) = w \cdot x$ the empirical risk is convex in $w$.

**Classification calibration.** Let $\eta = P(y = 1 \mid x)$. The conditional $\varphi$-risk of a score $\alpha$ is

$$C_\eta(\alpha) = \eta\, \varphi(\alpha) + (1 - \eta)\, \varphi(-\alpha).$$

Let $H(\eta) = \inf_\alpha C_\eta(\alpha)$, and let $H^-(\eta) = \inf \{ C_\eta(\alpha) : \alpha (2\eta - 1) \le 0 \}$ be the best risk with a score of the wrong sign (or zero). Bartlett, Jordan and McAuliffe call $\varphi$ *classification calibrated* if $H^-(\eta) > H(\eta)$ for each $\eta \ne 1/2$. So a score of the wrong sign always costs strictly more than the best score. Their main results:

- **Convex case.** A convex $\varphi$ is classification calibrated if and only if $\varphi$ is differentiable at 0 and $\varphi'(0) < 0$.
- **Risk transfer.** There is a nondecreasing function $\psi$ with $\psi(0) = 0$ such that, for each measurable $f$ and each $D$, $\psi\big(R_{01}(f) - R_{01}^*\big) \le R_\varphi(f) - R_\varphi^*$. For a convex calibrated $\varphi$, $\psi(\theta) = \varphi(0) - H\big(\tfrac{1 + \theta}{2}\big)$, and $\psi(\theta) > 0$ for $\theta > 0$. So a sequence of scores whose $\varphi$-risk tends to the best $\varphi$-risk has a 0-1 risk that tends to the Bayes risk.

For the hinge loss $H(\eta) = 2 \min(\eta, 1 - \eta)$, which gives $\psi(\theta) = \lvert \theta \rvert$. For the exponential loss $H(\eta) = 2\sqrt{\eta(1 - \eta)}$, which gives $\psi(\theta) = 1 - \sqrt{1 - \theta^2}$.

**The minimizers of the conditional risk.** For $0 < \eta < 1$:

| $\varphi$ | $\alpha^*(\eta) = \arg\min_\alpha C_\eta(\alpha)$ | $H(\eta)$ |
|---|---|---|
| hinge | $\operatorname{sign}(2\eta - 1)$ (any $\alpha \in [-1, 1]$ when $\eta = 1/2$) | $2\min(\eta, 1 - \eta)$ |
| logistic | $\ln \dfrac{\eta}{1 - \eta}$ | $-\eta \ln \eta - (1 - \eta) \ln (1 - \eta)$ |
| exponential | $\tfrac12 \ln \dfrac{\eta}{1 - \eta}$ | $2\sqrt{\eta(1 - \eta)}$ |
| squared | $2\eta - 1$ | $4\eta(1 - \eta)$ |

*Derivations.* For the logistic loss, $\frac{d}{d\alpha} C_\eta = -\eta\, \sigma(-\alpha) + (1 - \eta)\, \sigma(\alpha)$ with $\sigma(t) = 1/(1 + e^{-t})$. Since $\sigma(-\alpha) = 1 - \sigma(\alpha)$, the derivative is $\sigma(\alpha) - \eta$, which is zero at $\sigma(\alpha) = \eta$, that is at the log-odds. $C_\eta$ is convex, so this stationary point is the minimum. For the exponential loss, $-\eta e^{-\alpha} + (1 - \eta) e^{\alpha} = 0$ gives $e^{2\alpha} = \eta / (1 - \eta)$. For the squared loss, $-2\eta(1 - \alpha) + 2(1 - \eta)(1 + \alpha) = 0$ gives $\alpha = 2\eta - 1$. The hinge case is on the [hinge loss](/hinge-loss/) page. In each case the sign of $\alpha^*$ is the sign of $2\eta - 1$, which is the Bayes decision. The logistic, exponential and squared minimizers are also invertible functions of $\eta$, so they give a probability estimate; the hinge minimizer does not.

**Proper scoring rules.** When the prediction is a probability distribution $p$ over the labels, a loss $S(p, y)$ is a *scoring rule*. It is *proper* if, for each true distribution $q$,

$$\mathbb{E}_{y \sim q}\, S(q, y) \le \mathbb{E}_{y \sim q}\, S(p, y) \quad \text{for all } p,$$

and *strictly proper* if equality holds only at $p = q$. Gneiting and Raftery write scores as rewards to be maximized; this page uses the loss sign. Two strictly proper rules:

- **Log loss** $S(p, y) = -\ln p_y$. The gap is $\mathbb{E}_q[-\ln p_y] - \mathbb{E}_q[-\ln q_y] = \sum_y q_y \ln (q_y / p_y)$, the Kullback-Leibler divergence, which is $\ge 0$ with equality only at $p = q$ (Gibbs' inequality, see [cross-entropy loss](/cross-entropy-loss/)).
- **Brier score** $S(p, y) = \sum_j (p_j - \mathbb{1}[j = y])^2$. Expand: $\mathbb{E}_q S(p, y) = \sum_j p_j^2 - 2 \sum_j p_j q_j + 1$, so the gap is $\sum_j (p_j - q_j)^2 = \lVert p - q \rVert^2$.

A proper rule rewards an honest forecast, so minimizing it fits probabilities, not only decisions. Gneiting and Raftery characterize the proper rules through convex functions of the forecast (Savage's representation).

## Examples

**Margin losses at a few margins.**

| margin $m$ | 0-1 | hinge | logistic | exponential | squared |
|---|---|---|---|---|---|
| $-2$ | 1 | 3 | 2.1269 | 7.3891 | 9 |
| $-1$ | 1 | 2 | 1.3133 | 2.7183 | 4 |
| $0$ | 1 | 1 | 0.6931 | 1 | 1 |
| $0.5$ | 0 | 0.5 | 0.4741 | 0.6065 | 0.25 |
| $1$ | 0 | 0 | 0.3133 | 0.3679 | 0 |
| $2$ | 0 | 0 | 0.1269 | 0.1353 | 1 |

The exponential loss grows fastest on the wrong side, which makes AdaBoost sensitive to label noise. The squared loss rises again for $m > 1$: it penalizes a point that is *too* correct.

**One input with $\eta = 0.7$.** A grid search over $\alpha \in [-4, 4]$ in steps of $10^{-4}$ finds the minimizers $\alpha^* = 1$ (hinge), $0.8473$ (logistic, $= \ln(7/3)$), $0.4236$ (exponential) and $0.4$ (squared), with the values $H = 0.6$, $0.6109$, $0.9165$ and $0.84$. All four are positive, so all four predict the label $+1$, as the Bayes classifier does. The best scores with $\alpha \le 0$ cost $1$, $0.6931$, $1$ and $1$: in each case strictly more than $H$, as calibration demands.

**Non-example: the perceptron loss.** $\varphi(m) = \max(0, -m)$ is convex, but it has a kink at 0, so it is not calibrated. Indeed $C_\eta(0) = 0$ for each $\eta$, so the score 0 is optimal for every input, and $H^- = H = 0$. Minimizing this loss alone can return $f \equiv 0$. The [perceptron](/perceptron/) avoids this only because it updates on mistakes, not because it minimizes the loss.

**Non-example of a proper rule: the absolute error.** With $q = 0.7$ for the event $y = 1$, the expected loss $\mathbb{E}\lvert p - y \rvert = 0.7(1 - p) + 0.3p$ is $0.5$ at $p = 0.5$, $0.42$ at $p = 0.7$ and $0.3$ at $p = 1$. It is smallest at $p = 1$, not at the true $0.7$, so it rewards an overconfident forecast. For comparison, the Brier score is $0.5$, $0.42$, $0.5$ and $0.6$ at $p = 0.5, 0.7, 0.9, 1$, and the log loss is $0.6931$, $0.6109$ and $0.7645$ at $p = 0.5, 0.7, 0.9$ (and infinite at $p = 1$). Both proper rules are smallest at the true $p = 0.7$.

## Where it is used

- **Regression.** [Mean squared error](/mean-squared-error/) for [linear regression](/linear-regression/) and [ridge regression](/ridge-regression/); the pinball loss for [quantile regression](/quantile-regression/).
- **Probabilistic classification.** [Cross-entropy loss](/cross-entropy-loss/) for [softmax regression](/softmax-regression/) and neural networks; the [logistic loss](/logistic-loss/) is its binary case.
- **Margin classifiers.** The [hinge loss](/hinge-loss/) in [support vector machines](/support-vector-machine/), the exponential loss in [AdaBoost](/adaboost/), any differentiable loss in [gradient boosting](/gradient-boosting/).
- **Learning theory.** [Empirical risk minimization](/empirical-risk-minimization/), [PAC learning](/pac-learning/) and [agnostic PAC learning](/agnostic-pac-learning/) are stated for a fixed loss.
- **Evaluation.** The metric used to compare models, such as accuracy from the [confusion matrix](/confusion-matrix/), need not equal the training loss.

### Pitfalls

- **Calibration is a limit statement.** It says that driving the surrogate risk to its infimum over all measurable functions drives the 0-1 risk to the Bayes risk. With a small [hypothesis class](/hypothesis-class/) the surrogate minimizer can classify worse than the 0-1 minimizer in that class.
- **A calibrated loss need not give probabilities.** The hinge loss is calibrated, but its minimizer is $\pm 1$, so an SVM score is not a probability.
- **The scale of $y$ matters.** The margin forms need $y \in \{-1, +1\}$. With labels in $\{0, 1\}$ use the binary cross-entropy form; see [logistic loss](/logistic-loss/).
- **The training loss and the evaluation metric differ.** A model trained with log loss can be judged by accuracy, [precision and recall](/precision-and-recall/) or [ROC AUC](/roc-auc/); say which one you report.
- **"Objective function" is broader.** The training objective often adds a penalty, as in [regularization](/regularization/); the loss is only the data term.

## References
