---
tag: 3V7ENF
kind: concept
slug: generalization-error
name: Generalization error
aliases:
- true risk
- test error
- out-of-sample error
- generalization gap
area: machine-learning/supervised-learning
level: intro
summary: "The expected loss L_D(h) of a hypothesis on new examples from the data distribution, and its gap to the training error. Hoeffding bounds the gap for a fixed h, not for a learned one."
prereqs: [expected-value, hoeffding-inequality, loss-function]
see_also: [empirical-risk-minimization, pac-learning, vc-dimension, rademacher-complexity, overfitting, bias-variance-tradeoff, cross-validation, union-bound]
sources:
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Section 2.1 (the true error and the training error), Chapter 4 (uniform convergence, finite classes) and Section 5.2 (the error decomposition into approximation and estimation error)
  - book: isbn:9780262039406
    title: Mehryar Mohri, Afshin Rostamizadeh and Ameet Talwalkar, Foundations of Machine Learning, second edition, MIT Press, 2018
    locator: Chapter 2 (generalization error and empirical error; finite hypothesis sets) and Section 4.1 (estimation and approximation errors)
  - paper: doi:10.1080/01621459.1963.10500830
    title: Wassily Hoeffding, Probability inequalities for sums of bounded random variables, Journal of the American Statistical Association 58(301), 1963
    locator: Theorem 2 (the bound for sums of independent bounded variables)
  - book: isbn:9780387987804
    title: Vladimir N. Vapnik, The Nature of Statistical Learning Theory, second edition, Springer, 2000
    locator: Chapter 1 (the risk functional and the empirical risk) and Chapter 2 (uniform convergence)
---

The generalization error of a hypothesis $h$ is its expected [loss](/loss-function/) on a new example drawn from the same distribution as the training data. It is also called the true risk $L_D(h)$. The training error $L_S(h)$ is the mean loss on the sample, and the difference $L_D(h) - L_S(h)$ is the generalization gap. For one hypothesis fixed before the sample is seen, [Hoeffding's inequality](/hoeffding-inequality/) makes the gap small with high probability; for a hypothesis that the learner picked using the sample, it does not, and one needs a [union bound](/union-bound/) or uniform convergence over the class.

## In plain words

A model is trained on some examples, and then it meets new examples from the same source. Its generalization error is the average loss it will make on those new examples. Nobody can compute this number exactly, because the source is unknown. The training error is easy to compute, but it is an optimistic guess: the learner chose the model because it looks good on exactly those examples. A model that memorizes the training set has no training error and can still be wrong half of the time on new data. The gap between the two errors is what learning theory tries to bound. A fresh test set, which the learner never saw, gives an honest estimate.

## The idea

**Setting and notation.** Examples $z = (x, y)$ are drawn i.i.d. from an unknown distribution $D$ over $X \times Y$. A sample $S = (z_1, \ldots, z_n)$ has $n$ examples. A hypothesis $h : X \to Y$ comes from a [hypothesis class](/hypothesis-class/) $H$, and a loss $\ell(h, z) \ge 0$ says how bad $h$ is on $z$; for classification, $\ell$ is the zero-one loss $\mathbf{1}[h(x) \ne y]$. A learner $A$ maps $S$ to a hypothesis $h_S = A(S)$.

**Definitions.**

$$L_D(h) = \mathbb{E}_{z \sim D}[\ell(h, z)], \qquad L_S(h) = \frac{1}{n} \sum_{i=1}^{n} \ell(h, z_i), \qquad \mathrm{gap}(A, S) = L_D(h_S) - L_S(h_S).$$

$L_D(h)$ is the true risk, or generalization error, of $h$. $L_S(h)$ is the empirical risk, or training error. For a fixed $h$, $L_S(h)$ is a random variable with mean $L_D(h)$. The gap of a learner is a random variable too, because $h_S$ depends on $S$. The *test error* of $h$ is $L_T(h)$ on a separate test sample $T$ drawn after $h$ is fixed; it is an estimate of $L_D(h)$, not the same number.

**Three quantities that are often confused.** Let $L^\ast = \inf_h L_D(h)$ over all measurable $h$ (the Bayes risk) and $h^\ast \in \arg\min_{h \in H} L_D(h)$ (the best in class, assumed to exist).

1. The *generalization gap* $L_D(h_S) - L_S(h_S)$ compares the learned hypothesis with its own training error.
2. The *excess risk* compares it with a benchmark: $L_D(h_S) - L^\ast$ against the Bayes risk, or $L_D(h_S) - L_D(h^\ast)$ against the best in class.
3. The *error decomposition* of Shalev-Shwartz and Ben-David (Section 5.2) splits the true risk as $L_D(h_S) = \varepsilon_{\mathrm{app}} + \varepsilon_{\mathrm{est}}$, with the approximation error $\varepsilon_{\mathrm{app}} = \min_{h \in H} L_D(h)$ and the estimation error $\varepsilon_{\mathrm{est}} = L_D(h_S) - \min_{h \in H} L_D(h)$. Their $\varepsilon_{\mathrm{app}}$ contains the Bayes risk; other books subtract it and write $L_D(h_S) - L^\ast = (L_D(h^\ast) - L^\ast) + (L_D(h_S) - L_D(h^\ast))$.

A small gap does not mean a small risk: a constant classifier has a tiny gap and a large risk. A large class lowers the approximation error and tends to raise the estimation error. The [bias-variance decomposition](/bias-variance-tradeoff/) is a related split for squared loss, taken at each input and over training sets.

**One fixed hypothesis.** Let the loss take values in $[0, 1]$ and let $h$ be fixed before $S$ is drawn. Then the values $\ell(h, z_i)$ are i.i.d. in $[0, 1]$ with mean $L_D(h)$, and Hoeffding's inequality gives, for every $\varepsilon > 0$,

$$\Pr_S\big[\,|L_S(h) - L_D(h)| > \varepsilon\,\big] \le 2 e^{-2 n \varepsilon^2}.$$

Set the right side to $\delta$: with probability at least $1 - \delta$, $|L_S(h) - L_D(h)| \le \sqrt{\ln(2/\delta)/(2n)}$. This is the bound behind a test set. With $n = 1000$ test examples and $\delta = 0.05$, the test error is within $0.043$ of the true risk.

**Why a learned hypothesis needs more.** Hoeffding's inequality needs the summands to be independent with a fixed mean. For $h_S$, the values $\ell(h_S, z_i)$ depend on all of $S$ through the choice of $h_S$, so the inequality does not apply. The extreme case is a learner that memorizes $S$ and outputs label 0 at all other points: when the labels are fair coins that do not depend on $x$ and $X$ is large, $L_S(h_S) = 0$ while $L_D(h_S) = 1/2$.

**Theorem (uniform convergence for a finite class).** Let $H$ be finite and the loss take values in $[0, 1]$. For every $\varepsilon > 0$,

$$\Pr_S\big[\,\exists h \in H : |L_S(h) - L_D(h)| > \varepsilon\,\big] \le 2 |H| e^{-2 n \varepsilon^2}.$$

*Proof.* The event on the left is the union over $h \in H$ of the events $|L_S(h) - L_D(h)| > \varepsilon$. Each $h \in H$ is fixed before $S$ is drawn, so each event has probability at most $2 e^{-2n\varepsilon^2}$ by Hoeffding's inequality. The union bound adds these $|H|$ bounds. $\blacksquare$

So with probability at least $1 - \delta$, every $h \in H$, and therefore every $h_S$ that a learner picks from $H$, has $|L_D(h) - L_S(h)| \le \sqrt{\ln(2|H|/\delta)/(2n)}$. It suffices that $n \ge \ln(2|H|/\delta)/(2\varepsilon^2)$. Uniform convergence also bounds the estimation error of [empirical risk minimization](/empirical-risk-minimization/): if every $h \in H$ has $|L_D(h) - L_S(h)| \le \varepsilon$ and $h_S$ minimizes $L_S$ over $H$, then

$$L_D(h_S) \le L_S(h_S) + \varepsilon \le L_S(h^\ast) + \varepsilon \le L_D(h^\ast) + 2\varepsilon.$$

For an infinite class, the size $|H|$ is replaced by a measure of capacity: the [VC dimension](/vc-dimension/), the growth function of the [Sauer-Shelah lemma](/sauer-shelah-lemma/), or the [Rademacher complexity](/rademacher-complexity/). The [fundamental theorem of statistical learning](/fundamental-theorem-of-statistical-learning/) says that for binary classification, uniform convergence holds exactly when the VC dimension is finite.

## Examples

**Selection breaks the fixed-hypothesis bound.** Take $X = \{0, \ldots, 4095\}$ with $x$ uniform, and a label $y$ that is a fair coin independent of $x$. Every classifier has true risk exactly $1/2$. Let $H$ hold $k = 200$ classifiers, each a random table of 4096 bits drawn once with `random.Random(1)`. Draw samples of $n = 50$ examples, and use $\delta = 0.05$.

- The fixed-hypothesis bound is $\varepsilon_1 = \sqrt{\ln 40 / 100} \approx 0.192$. A training error below $0.5 - 0.192 = 0.308$ means at most 15 mistakes out of 50. For one fixed $h$ the probability of that is $\Pr[\mathrm{Bin}(50, \frac12) \le 15] \approx 0.0033$.
- The ERM choice, the $h$ with the fewest training mistakes, is the minimum of 200 such counts. If the counts were independent, the probability of 15 or fewer would be $1 - (1 - 0.0033)^{200} \approx 0.484$. In 400 simulated samples on the fixed class, the ERM choice had a gap above $\varepsilon_1$ in 49.25 percent of them, and $h_0$ (fixed in advance) in 0.25 percent.
- The union bound gives $\varepsilon_{200} = \sqrt{\ln 8000 / 100} \approx 0.300$. In the same 400 samples, some $h \in H$ had $|L_S(h) - \frac12| > 0.300$ in 0.5 percent of them, within $\delta$.

So the training error of the selected classifier is a biased estimate of its true risk, while the training error of a classifier fixed in advance is not.

**Sample size for a finite class.** For $|H| = 200$, $\varepsilon = 0.1$ and $\delta = 0.05$, uniform convergence needs $n \ge \ln(8000)/0.02 \approx 449.4$, so 450 examples. One fixed hypothesis needs only $\ln(40)/0.02 \approx 184.4$, so 185 examples.

**Non-example: a test set reused for selection.** If a test set is used to choose among models, the chosen model depends on it, and its test error is again a training error of the selection step. The fixed-hypothesis bound then holds for each model, but not for the chosen one, unless one pays the union bound over the candidates.

## Where it is used

- **[PAC learning](/pac-learning/) and [agnostic PAC learning](/agnostic-pac-learning/)** ask that $L_D(h_S)$, or the excess risk over the best in class, be at most $\varepsilon$ with probability $1 - \delta$.
- **Generalization bounds** (VC, Rademacher, [margin](/margin-generalization-bound/), stability, compression and description length bounds) are bounds on the gap or on the estimation error. See [Occam's razor](/occams-razor/) for a bound that grows with the description length of $h$.
- **Model selection and evaluation.** A held-out test set or [cross-validation](/cross-validation/) estimates the generalization error. [Structural risk minimization](/structural-risk-minimization/) trades the training error against a bound on the gap.
- **Diagnosis.** A small training error with a large validation error is the signature of [overfitting](/overfitting/).

### Pitfalls

- **Training error is not an estimate of the true risk** for a hypothesis chosen on the same data.
- **The gap is not the excess risk.** A learner can have zero gap and a large excess risk (it underfits), or a large gap and a small excess risk.
- **Approximation error in two senses.** Some texts include the Bayes risk in it (Shalev-Shwartz and Ben-David), others subtract it. Say which one you use.
- **The i.i.d. assumption.** All the bounds above assume that the test examples come from the same distribution $D$ as the training examples. Under a distribution shift, they say nothing.

## References
