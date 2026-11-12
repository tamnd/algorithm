---
tag: HPED45
kind: problem
slug: classification
name: Classification
aliases:
- supervised classification
- statistical classification
area: machine-learning/supervised-learning
level: intro
summary: "Learn from labeled examples a rule that maps each input to one of finitely many classes, with small expected 0-1 loss. The Bayes classifier sets the floor."
prereqs: [loss-function]
see_also: [multiclass-classification, bayes-optimal-classifier, confusion-matrix, pac-learning, logistic-regression, support-vector-machine, k-nearest-neighbors, decision-tree]
sources:
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Chapters 2 to 6 (the statistical learning framework, PAC and agnostic PAC learning, and Theorem 6.8, the quantitative fundamental theorem) and Section 12.3 (hardness of 0-1 loss minimization and surrogate losses)
  - book: isbn:9780387946184
    title: Luc Devroye, Laszlo Gyorfi and Gabor Lugosi, A Probabilistic Theory of Pattern Recognition, Springer, 1996
    locator: Chapter 2 (the Bayes error and plug-in decisions) and Chapter 7 (no universal rate of convergence)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 2.4 (statistical decision theory and the Bayes classifier)
  - paper: "C. K. Chow, On optimum recognition error and reject tradeoff, IEEE Transactions on Information Theory 16(1), 41-46, 1970"
    locator: the optimal rule with a reject option
---

Classification is the problem of learning, from $n$ labeled examples, a rule that maps each input to one of finitely many classes so that the expected 0-1 loss on new examples is small. Its best possible rule, for a known distribution, is the [Bayes classifier](/bayes-optimal-classifier/), which picks the most probable class; learning algorithms try to approach it from data. The task has binary, [multiclass](/multiclass-classification/) and multilabel forms, and it is judged with the [confusion matrix](/confusion-matrix/) and the metrics built on it.

## In plain words

You have a pile of examples, each with a label from a short fixed list: emails marked spam or not spam, photos marked cat, dog or bird. You want a rule that labels new examples that you have not seen. A rule is good if it makes few mistakes on new examples, not only on the pile.

Even the perfect rule can make mistakes, because two examples can look the same and still have different labels. The best you can do is to pick, for each kind of example, the label that is most often right. A learning method tries to find a rule close to that best rule while it sees only the pile.

## Definition

**Data model.** An input space $\mathcal X$ (often $\mathbb{R}^d$) and a finite label set $\mathcal Y = [k] = \{1, \ldots, k\}$ with $k \ge 2$. An unknown distribution $D$ on $\mathcal X \times \mathcal Y$. The training set $S = ((x_1, y_1), \ldots, (x_n, y_n))$ is drawn i.i.d. from $D$.

**Output.** A classifier $h : \mathcal X \to \mathcal Y$ chosen from $S$ (by a learning algorithm $A$, so $h = A(S)$).

**Criterion.** The risk under the 0-1 loss,

$$R(h) = P_{(x, y) \sim D}\big(h(x) \ne y\big).$$

Write $\eta_j(x) = P(y = j \mid x)$. The Bayes classifier $h^*(x) \in \arg\max_j \eta_j(x)$ (ties broken in any fixed way) minimizes $R$ over all measurable classifiers, and its risk is the Bayes error

$$R^* = \mathbb{E}_x\big[1 - \max_j \eta_j(x)\big].$$

The proof is pointwise: given $x$, the rule that predicts $j$ is wrong with probability $1 - \eta_j(x)$. See [Bayes optimal classifier](/bayes-optimal-classifier/).

**Goals.** Two standard ways to state what a learner must achieve:

- *Consistency:* $\mathbb{E}_S R(A(S)) \to R^*$ as $n \to \infty$, for a given $D$ or for every $D$ (universal consistency).
- *PAC learning relative to a class $H$* ([PAC learning](/pac-learning/), [agnostic PAC learning](/agnostic-pac-learning/)): with probability at least $1 - \delta$ over $S$, $R(A(S)) \le \min_{h \in H} R(h) + \varepsilon$, once $n$ is large enough as a function of $\varepsilon$, $\delta$ and $H$. The setting is *realizable* if some $h \in H$ has $R(h) = 0$, and *agnostic* otherwise.

## Variants

- **Binary classification.** $k = 2$, often with labels $\{-1, +1\}$ and a real score $f$ with $h = \operatorname{sign} f$. The [hinge loss](/hinge-loss/) and [logistic loss](/logistic-loss/) are its surrogates.
- **Multiclass classification.** $k \ge 3$ with exactly one label per input. See [multiclass classification](/multiclass-classification/).
- **Multilabel classification.** Each input has a *set* of labels $Y \subseteq [k]$. The output is a vector in $\{0, 1\}^k$. Common losses are the Hamming loss $\frac1k \sum_j \mathbb{1}[\hat Y_j \ne Y_j]$ and the subset 0-1 loss $\mathbb{1}[\hat Y \ne Y]$. Under the Hamming loss the Bayes rule decides each label separately ($j \in \hat Y$ iff $P(j \in Y \mid x) > \frac12$); under the subset loss it picks the most probable whole set, which can differ.
- **Cost-sensitive classification.** A cost $c(i, j) \ge 0$ for predicting $j$ when the truth is $i$. The Bayes rule is $\arg\min_j \sum_i c(i, j)\, \eta_i(x)$. In the binary case with costs $c_{\mathrm{FP}}$ and $c_{\mathrm{FN}}$ it predicts positive iff $\eta_1(x) > c_{\mathrm{FP}} / (c_{\mathrm{FP}} + c_{\mathrm{FN}})$.
- **Probabilistic classification.** Output the vector $\eta(x)$ itself, judged by a proper scoring rule such as the [cross-entropy loss](/cross-entropy-loss/).
- **Classification with a reject option.** The rule may abstain at cost $c < \frac12$. Chow's rule predicts the most probable class if $\max_j \eta_j(x) \ge 1 - c$ and abstains otherwise.
- **Ranking and scoring.** Only the order of the scores matters; this is judged by [ROC AUC](/roc-auc/). See also [learning to rank](/learning-to-rank/).

## Examples

**A finite input space.** Let $\mathcal X = \{a, b, c\}$ with $P(a) = 0.5$, $P(b) = 0.3$, $P(c) = 0.2$, labels $\{0, 1\}$ and $\eta_1(a) = 0.9$, $\eta_1(b) = 0.4$, $\eta_1(c) = 0.5$.

| rule | $h(a)$ | $h(b)$ | $h(c)$ | risk |
|---|---|---|---|---|
| Bayes | 1 | 0 | 0 or 1 | $0.5 \cdot 0.1 + 0.3 \cdot 0.4 + 0.2 \cdot 0.5 = 0.27$ |
| always 1 | 1 | 1 | 1 | $0.05 + 0.18 + 0.10 = 0.33$ |
| always 0 | 0 | 0 | 0 | $0.45 + 0.12 + 0.10 = 0.67$ |

No rule has risk below $R^* = 0.27$, and at $c$ the two choices tie.

**The same data with costs.** Let a missed positive cost 4 and a false alarm cost 1. The threshold becomes $1/(1 + 4) = 0.2$, so the rule predicts 1 at $b$ too. Its expected cost is $0.5 \cdot 0.1 + 0.3 \cdot 0.6 + 0.2 \cdot 0.5 = 0.33$; predicting 0 at $b$ would cost $0.05 + 0.3 \cdot 0.4 \cdot 4 + 0.10 = 0.63$.

**Multilabel losses.** A news item has the true labels $\{\text{sport}, \text{economy}\}$ out of $\{\text{sport}, \text{politics}, \text{economy}\}$, and the prediction is all three. The Hamming loss is $1/3$; the subset 0-1 loss is 1.

## Known algorithms

- [Logistic regression](/logistic-regression/) and [softmax regression](/softmax-regression/): linear scores fitted with the [logistic](/logistic-loss/) or [cross-entropy](/cross-entropy-loss/) loss; they estimate $\eta$.
- [Support vector machines](/support-vector-machine/): a maximum-margin linear rule in a kernel feature space, fitted with the [hinge loss](/hinge-loss/).
- [Perceptron](/perceptron/): online mistake-driven updates; at most $(R/\gamma)^2$ mistakes on data separable with margin $\gamma$.
- [k-nearest neighbors](/k-nearest-neighbors/): a majority vote of the nearest training points; universally consistent when $k \to \infty$ and $k/n \to 0$.
- [Naive Bayes](/naive-bayes-classifier/) and [quadratic discriminant analysis](/quadratic-discriminant-analysis/): generative models of $p(x \mid y)$ turned into $\eta$ by Bayes' rule.
- [Decision trees](/decision-tree/), [random forests](/random-forest/) and [boosting](/boosting/) such as [AdaBoost](/adaboost/) and [gradient boosting](/gradient-boosting/).
- Neural networks with a softmax output, trained by [stochastic gradient descent](/stochastic-gradient-descent/) on the cross-entropy loss.

## Bounds

- **The Bayes error is a floor.** For every classifier $h$, $R(h) \ge R^*$. It is positive exactly when $\max_j \eta_j(x) < 1$ on a set of inputs with positive probability, that is, when the input does not fix the label almost surely.
- **Sample complexity relative to a class.** For binary $H$ with [VC dimension](/vc-dimension/) $d < \infty$ the [fundamental theorem](/fundamental-theorem-of-statistical-learning/) (Shalev-Shwartz and Ben-David, Theorem 6.8) gives constants $C_1, C_2$ with: in the realizable case $C_1 \frac{d + \log(1/\delta)}{\varepsilon} \le m_H(\varepsilon, \delta) \le C_2 \frac{d \log(1/\varepsilon) + \log(1/\delta)}{\varepsilon}$, and in the agnostic case $C_1 \frac{d + \log(1/\delta)}{\varepsilon^2} \le m_H(\varepsilon, \delta) \le C_2 \frac{d + \log(1/\delta)}{\varepsilon^2}$. A class with infinite VC dimension is not PAC learnable.
- **No universal rate.** A universally consistent rule exists, but for every rule and every sequence of numbers tending to 0 slowly there is a distribution on which its risk converges more slowly (Devroye, Gyorfi and Lugosi, Chapter 7). See also the [no free lunch theorem](/no-free-lunch-theorem-learning/).
- **Computation.** Minimizing the empirical 0-1 loss over halfspaces in the agnostic setting is NP-hard in general (Shalev-Shwartz and Ben-David, Section 12.3). This is why practical algorithms minimize convex surrogates.

## Reductions

- **Classification to probability estimation.** Plug an estimate $\hat\eta$ into the Bayes rule. In the binary case, with $\hat h(x) = \mathbb{1}[\hat\eta(x) > \frac12]$,

  $$R(\hat h) - R^* = \mathbb{E}_x\big[\lvert 2\eta(x) - 1 \rvert\, \mathbb{1}[\hat h(x) \ne h^*(x)]\big] \le 2\, \mathbb{E}_x \lvert \hat\eta(x) - \eta(x) \rvert.$$

  *Proof.* At a point where $\hat h$ and $h^*$ differ, the conditional error of $\hat h$ exceeds that of $h^*$ by $\lvert 2\eta - 1 \rvert$. There $\eta$ and $\hat\eta$ lie on opposite sides of $\frac12$ (or $\hat\eta = \frac12$), so $\lvert \eta - \frac12 \rvert \le \lvert \eta - \hat\eta \rvert$. $\blacksquare$
- **Classification to convex surrogate minimization.** Minimize a classification calibrated loss instead of the 0-1 loss; the excess 0-1 risk is controlled by the excess surrogate risk (see [loss function](/loss-function/)).
- **Multiclass to binary.** [One-vs-rest](/one-vs-rest/) uses $k$ binary problems, [one-vs-one](/one-vs-one/) uses $k(k - 1)/2$, and [error-correcting output codes](/error-correcting-output-codes/) use one per column of a code matrix.
- **Multilabel to binary.** Binary relevance trains one binary classifier per label; it is exact for the Hamming loss when each classifier is Bayes optimal.

## Applications

Spam filtering, medical diagnosis from tests or images, credit approval, fraud detection, image and speech recognition, document categorization, and quality control. In each, the costs of the two kinds of error differ, so the choice of the threshold and of the metric ([precision and recall](/precision-and-recall/), [ROC AUC](/roc-auc/)) matters as much as the choice of the algorithm. [Cross-validation](/cross-validation/) estimates the risk and selects the hyperparameters.

## References
