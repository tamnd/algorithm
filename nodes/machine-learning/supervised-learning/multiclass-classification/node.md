---
tag: TK6JHM
kind: problem
slug: multiclass-classification
name: Multiclass classification
aliases:
- multi-class classification
- multinomial classification
area: machine-learning/supervised-learning
level: intro
summary: "Classification with k >= 3 classes and one label per input. Solved directly with k scores and an argmax, or by reduction to binary problems (OvR, OvO, ECOC)."
prereqs: [classification]
see_also: [classification, one-vs-rest, one-vs-one, error-correcting-output-codes, softmax-regression, cross-entropy-loss, hinge-loss, confusion-matrix]
sources:
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Chapter 17 (multiclass prediction, the one-versus-all and all-pairs reductions, linear multiclass predictors) and Chapter 29 (the Natarajan dimension and multiclass learnability)
  - paper: "Erin L. Allwein, Robert E. Schapire and Yoram Singer, Reducing multiclass to binary: a unifying approach for margin classifiers, Journal of Machine Learning Research 1, 113-141, 2000"
    locator: code matrices in {-1, 0, +1} that cover one-against-all, all-pairs and random codes, and Theorem 1 (the training error bound for loss-based decoding)
  - paper: "Ryan Rifkin and Aldebaro Klautau, In defense of one-vs-all classification, Journal of Machine Learning Research 5, 101-141, 2004"
    locator: experiments in which one-vs-all with well-tuned binary classifiers is as accurate as the other reductions
  - paper: "Ambuj Tewari and Peter L. Bartlett, On the consistency of multiclass classification methods, Journal of Machine Learning Research 8, 1007-1025, 2007"
    locator: which multiclass surrogate losses are classification calibrated
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 4.2 (linear regression of an indicator matrix, and the masking of a class when k >= 3)
---

Multiclass classification is [classification](/classification/) with $k \ge 3$ classes and exactly one correct class per input. The goal is a rule $h : \mathcal X \to [k]$ with small expected 0-1 loss; the best rule picks the class with the largest conditional probability. There are two ways to solve it: a single model with $k$ scores $f_1(x), \ldots, f_k(x)$ that predicts $\arg\max_j f_j(x)$, fitted with a multiclass loss such as the [cross-entropy](/cross-entropy-loss/) of [softmax regression](/softmax-regression/), or a reduction to binary problems: [one-vs-rest](/one-vs-rest/), [one-vs-one](/one-vs-one/) and [error-correcting output codes](/error-correcting-output-codes/).

## In plain words

A binary classifier answers a yes-or-no question. Many real tasks have more answers: which digit is this, which language is this text, which of a hundred species is this bird. Each example has one right answer from the list.

You can build one model that gives a score to every answer and picks the highest. Or you can build many yes-or-no models and combine their votes. One model per answer asks "this answer or another one?". One model per pair of answers asks "this one or that one?". A code design asks a few cleverly chosen questions, so that a few wrong answers can still be corrected.

## Definition

**Input.** A training set $S = ((x_1, y_1), \ldots, (x_n, y_n))$ drawn i.i.d. from an unknown distribution $D$ on $\mathcal X \times [k]$, with $k \ge 3$.

**Output.** A classifier $h : \mathcal X \to [k]$. Often $h(x) = \arg\max_j f_j(x)$ for a score vector $f(x) \in \mathbb{R}^k$, with ties broken by a fixed rule.

**Criterion.** The 0-1 risk $R(h) = P(h(x) \ne y)$. With $\eta_j(x) = P(y = j \mid x)$, the [Bayes classifier](/bayes-optimal-classifier/) $h^*(x) = \arg\max_j \eta_j(x)$ is optimal, and the Bayes error is $R^* = \mathbb{E}_x[1 - \max_j \eta_j(x)]$. Since $\max_j \eta_j \ge 1/k$, $R^* \le 1 - 1/k$, the error of a uniform random guess.

A largest $\eta_j$ need not exceed $\frac12$: with three classes, a plurality is enough, and a rule that waits for a majority can be far from optimal.

## Variants

- **Probabilistic.** Output the vector $\eta(x)$, judged by the cross-entropy (the log loss) or the Brier score.
- **Top-$m$ prediction.** Output $m$ classes; the error is $P(y \notin \hat Y(x))$. The Bayes rule outputs the $m$ largest $\eta_j(x)$.
- **Cost-sensitive.** A $k \times k$ cost matrix $c(i, j)$; the Bayes rule is $\arg\min_j \sum_i c(i, j)\, \eta_i(x)$.
- **Ordinal.** The classes are ordered (ratings 1 to 5), and errors between far classes cost more.
- **Hierarchical.** The classes are leaves of a tree, and errors within a subtree cost less.
- **Extreme classification.** $k$ in the thousands or millions, where even $O(k)$ prediction time is too much.
- **Multilabel** is a different problem: there each input has a *set* of labels (see [classification](/classification/)).

## Examples

**A small Bayes computation.** Let $\mathcal X = \{a, b\}$ with $P(a) = 0.6$, $P(b) = 0.4$, $\eta(a) = (0.5, 0.3, 0.2)$ and $\eta(b) = (0.2, 0.35, 0.45)$.

| rule | $h(a)$ | $h(b)$ | risk |
|---|---|---|---|
| Bayes | 1 | 3 | $0.6 \cdot 0.5 + 0.4 \cdot 0.55 = 0.52$ |
| always 1 | 1 | 1 | $0.6 \cdot 0.5 + 0.4 \cdot 0.8 = 0.62$ |
| uniform guess | | | $2/3 = 0.667$ |
| Bayes top-2 | $\{1, 2\}$ | $\{3, 2\}$ | $0.6 \cdot 0.2 + 0.4 \cdot 0.2 = 0.2$ |

At $b$ no class has a majority, but class 3 is still the right choice.

**Masking of the middle class.** Let $x \in [0, 3]$ with class 1 on $[0, 1)$, class 2 on $[1, 2)$ and class 3 on $[2, 3]$. The question "class 2 or not?" has no answer of the form $\operatorname{sign}(w x + b)$, because class 2 is an interval in the middle. But three linear scores with an argmax solve the whole problem: $f_j(x) = c_j x - c_j^2/2$ with centers $c = (0.5, 1.5, 2.5)$ gives $f_j(x) = \frac{x^2}{2} - \frac{(x - c_j)^2}{2}$, so the argmax is the nearest center, with boundaries at 1 and 2. Fitting each score separately by least squares on the class indicator can still lose class 2, because its fitted line can stay below the other two everywhere; ESL Section 4.2 calls this masking.

**Digit recognition.** Ten classes $0, \ldots, 9$. A softmax model gives ten scores; one-vs-one trains 45 binary classifiers; a 15-bit error-correcting code trains 15.

## Known algorithms

- [Softmax regression](/softmax-regression/): $k$ linear scores fitted with the cross-entropy loss; it estimates $\eta$, and its loss is calibrated.
- Multiclass [support vector machines](/support-vector-machine/) with the Crammer-Singer or Weston-Watkins [hinge loss](/hinge-loss/). Unlike the binary hinge, these losses are not classification calibrated for every distribution when $k \ge 3$ (Tewari and Bartlett 2007).
- Methods that handle $k$ classes natively: [k-nearest neighbors](/k-nearest-neighbors/) (a plurality vote), [naive Bayes](/naive-bayes-classifier/), [decision trees](/decision-tree/) and [random forests](/random-forest/) (class frequencies in the leaves), and [gradient boosting](/gradient-boosting/) with $k$ trees per round.
- Neural networks with a softmax output layer.
- Reductions to a binary learner: [one-vs-rest](/one-vs-rest/), [one-vs-one](/one-vs-one/) and [error-correcting output codes](/error-correcting-output-codes/).

## Bounds

- **The Bayes error** is at most $1 - 1/k$, and no rule beats $R^*$.
- **Learnability.** For a finite $k$, a class $H$ of functions $\mathcal X \to [k]$ is PAC learnable iff its Natarajan dimension is finite. The Natarajan dimension generalizes the [VC dimension](/vc-dimension/), and the sample complexity bounds that it gives have the binary form with an extra factor of order $\log k$ in the upper bound (Shalev-Shwartz and Ben-David, Chapter 29).
- **Reductions.** If each of the $\ell$ binary classifiers of a code matrix has average loss $\varepsilon$, loss-based decoding has training error at most $\ell \varepsilon / (\rho\, L(0))$, where $\rho$ is the minimum distance between rows (Allwein, Schapire and Singer 2000, Theorem 1). For one-vs-rest $\ell/\rho = k/2$, so the bound grows with $k$; for all-pairs and for random codes it is about 2.
- **Prediction cost.** Argmax over $k$ scores and one-vs-rest need $k$ score evaluations, one-vs-one needs $k(k - 1)/2$, a code with $\ell$ columns needs $\ell$, and a balanced tree of binary decisions needs $\lceil \log_2 k \rceil$.

## Reductions

- **To binary classification.** [One-vs-rest](/one-vs-rest/) trains $k$ classifiers, each on all $n$ examples. [One-vs-one](/one-vs-one/) trains $k(k - 1)/2$ classifiers, each on the examples of two classes only. [Error-correcting output codes](/error-correcting-output-codes/) train one classifier per column of a code matrix and decode to the nearest row. All three are cases of the $\{-1, 0, +1\}$ code matrices of Allwein, Schapire and Singer (2000).
- **To probability estimation.** Estimate $\eta(x)$ and take the argmax; the excess 0-1 risk is at most $2\, \mathbb{E}_x \max_j \lvert \hat\eta_j(x) - \eta_j(x) \rvert$.
- **To one binary problem over pairs.** Build a feature map $\Psi(x, j)$ and score $f_j(x) = w \cdot \Psi(x, j)$; with $\Psi(x, j)$ equal to $x$ placed in block $j$ of a $kd$-vector, this is $k$ independent linear scores (Shalev-Shwartz and Ben-David, Chapter 17). This is the starting point of [structured prediction](/structured-prediction/).
- **From multiclass to ranking.** A score vector also orders the classes, so top-$m$ prediction is a ranking problem.

## Applications

Handwritten digit and character recognition, object recognition in images (ImageNet has 1000 classes), speech and phoneme recognition, language identification, document topic labeling, intent detection in dialogue systems, species identification, and medical diagnosis with several possible conditions. The results are summarized with a $k \times k$ [confusion matrix](/confusion-matrix/), accuracy, and macro or micro [precision, recall and $F_1$](/precision-and-recall/).

## References
