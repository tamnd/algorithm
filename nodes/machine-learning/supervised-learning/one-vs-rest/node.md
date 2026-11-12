---
tag: 56YRRQ
kind: technique
slug: one-vs-rest
name: One-vs-rest
aliases:
- one-vs-all
- one-against-all
area: machine-learning/supervised-learning
level: intro
summary: "Reduce k-class classification to k binary problems, class j against all others, and predict the class whose binary score is largest."
prereqs: [multiclass-classification]
see_also: [multiclass-classification, one-vs-one, error-correcting-output-codes, logistic-regression, support-vector-machine, hinge-loss, softmax-regression, confusion-matrix]
sources:
  - paper: "Ryan Rifkin and Aldebaro Klautau, In defense of one-vs-all classification, Journal of Machine Learning Research 5, 101-141, 2004"
    locator: one-vs-all with well-tuned binary classifiers is as accurate as all-pairs and error-correcting codes in their experiments
  - paper: "Erin L. Allwein, Robert E. Schapire and Yoram Singer, Reducing multiclass to binary: a unifying approach for margin classifiers, Journal of Machine Learning Research 1, 113-141, 2000"
    locator: one-against-all as the k by k code matrix with +1 on the diagonal and -1 elsewhere, and Theorem 1 with l / rho = k / 2
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 4.1.2 (one-versus-the-rest and one-versus-one discriminants leave ambiguous regions; k linear scores with an argmax do not)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Section 17.1 (the one-versus-all and all-pairs reductions and their limitations)
---

One-vs-rest (OvR, also one-vs-all) reduces a $k$-class problem to $k$ binary problems. Problem $j$ uses all $n$ training examples, with class $j$ labeled $+1$ and every other class $-1$; a binary learner returns a real score $f_j$, and the prediction is $\arg\max_j f_j(x)$. It needs only $k$ classifiers and any binary learner, and with well-tuned binary classifiers it is often as accurate as the other reductions (Rifkin and Klautau 2004). Its weak points are that the $k$ scores are trained separately, so their scales need not be comparable, and that each binary problem is imbalanced, with about $1/k$ positives.

## In plain words

You have a good yes-or-no classifier and a problem with many classes. For each class, train one classifier that answers "is it this class?". To label a new example, ask all of them and take the class whose classifier is most confident.

Each classifier sees every example, but only a small part of them are "yes", so it can learn to say "no" too often. And each classifier learns alone, so one may give bigger numbers than another without being more sure. Both problems need care.

## When it applies

- You have a binary learner that outputs a real score or a probability, not only a sign. With signs only, the votes can be empty or tied (see Pitfalls).
- $k$ is moderate. Training costs $k$ runs of the binary learner on all $n$ examples, and prediction costs $k$ score evaluations.
- The binary scores are comparable across classes: probabilities from a [logistic](/logistic-regression/) model, or margins from classifiers trained with the same loss and regularization.

## The template

Classes are $1, \ldots, k$. The holes are the binary learner `BINARY`, which takes labeled examples in $\{-1, +1\}$ and returns a score function, and the tie rule in L5.

```pseudo id=main
ONE-VS-REST-TRAIN(S, k, BINARY)                  ▷ S = ((x_1, y_1), ..., (x_n, y_n))
L1  for j ← 1 to k do
L2      S_j ← ((x_i, +1 if y_i = j else −1) : i = 1, ..., n)
L3      f_j ← BINARY(S_j)                         ▷ a real-valued score
L4  return (f_1, ..., f_k)
ONE-VS-REST-PREDICT(f_1, ..., f_k, x)
L5  return the smallest j with f_j(x) = max_m f_m(x)
```

**When the reduction is exact.** If `BINARY` returns a strictly increasing function of the true conditional probability, the same function $g$ for every class, then $f_j(x) = g(\eta_j(x))$ with $\eta_j(x) = P(y = j \mid x)$, and the argmax of L5 is the [Bayes classifier](/bayes-optimal-classifier/) $\arg\max_j \eta_j(x)$. A binary learner fitted with a proper loss such as the [logistic loss](/logistic-loss/) estimates $\eta_j$ itself, so OvR with such learners is consistent when each binary estimate is. The estimates need not sum to 1; divide by their sum to get a distribution.

**When it is not.** A learner fitted with the [hinge loss](/hinge-loss/) estimates only $\operatorname{sign}(2\eta_j(x) - 1)$. Where no class has $\eta_j(x) > \frac12$, for example $\eta(x) = (0.4, 0.35, 0.25)$, all $k$ Bayes-optimal hinge classifiers output $-1$, the same value, and the argmax carries no information. The practical scores of an SVM are not exactly $\pm 1$, so OvR with SVMs often works, but the guarantee is lost.

**Cost.** With a binary learner that costs $T(m)$ on $m$ examples, training costs $k\, T(n)$ and prediction costs $k$ score evaluations. Compare $\binom{k}{2}$ trainings on about $2n/k$ examples each for [one-vs-one](/one-vs-one/).

**As a code matrix.** OvR is the $k \times k$ code matrix with $+1$ on the diagonal and $-1$ elsewhere (Allwein, Schapire and Singer 2000). Two rows differ in exactly 2 columns, so the minimum row distance is 2, and Hamming decoding cannot correct even one wrong binary output; see [error-correcting output codes](/error-correcting-output-codes/).

## Classic examples

- Multiclass [logistic regression](/logistic-regression/) in many libraries ("ovr" mode), as an alternative to a joint [softmax regression](/softmax-regression/).
- Multiclass [support vector machines](/support-vector-machine/) built from $k$ binary SVMs (Rifkin and Klautau 2004).
- The [perceptron](/perceptron/) with one weight vector per class, trained independently.
- Multilabel classification with "binary relevance": the same $k$ binary problems, but every class with a positive score is output, not only the largest.

## Variations

- **Probability normalization.** With probability outputs $p_j(x)$, predict $\arg\max_j p_j(x)$ and report $p_j / \sum_m p_m$.
- **Class weights.** Weight the positives of problem $j$ by $(n - n_j)/n_j$, or resample, to counter the imbalance.
- **Calibration after training.** Fit a monotone map from each $f_j$ to a probability on held-out data, for example with [isotonic regression](/isotonic-regression/), so that the scores become comparable.
- **Joint training.** Train the $k$ scores together with a multiclass loss (softmax [cross-entropy](/cross-entropy-loss/), or the Crammer-Singer hinge). This is no longer a reduction, but it removes the scale problem.

## Pitfalls

- **Hard votes are ambiguous.** If each binary classifier outputs only a sign, a point can get no $+1$ at all, or several. Bishop (Section 4.1.2) shows these regions for linear classifiers. Use the real scores and the argmax.
- **Masking.** On a line with class 1 on $[0, 1)$, class 2 on $[1, 2)$ and class 3 on $[2, 3)$, the problem "class 2 against the rest" has no linear solution. With least-squares linear scores on 30 evenly spaced points, the class-2 score is the constant $-\frac13$, and it is never the largest: OvR predicts class 2 nowhere and gets 20 of 30 points right. Adding the feature $x^2$ gives 28 of 30. [One-vs-one](/one-vs-one/) with linear classifiers solves the original problem.
- **Imbalance.** With $k$ balanced classes each problem has $1/k$ positives. A binary learner that minimizes the error can predict $-1$ everywhere at error $1/k$, and then all scores tie.
- **Different scales.** Scores of separately regularized classifiers, or of different model types, are not comparable. Use one learner with the same settings for all $j$.
- **Confusion with "one-vs-one".** OvR trains on all $n$ examples each time; one-vs-one trains each classifier on two classes only.

## Exercises

1. Show that in the $k \times k$ OvR code matrix every pair of rows differs in exactly two columns, and conclude that Hamming decoding detects one error but corrects none.
2. Let each binary learner return $f_j(x) = \eta_j(x) + \epsilon_j(x)$ with $\lvert \epsilon_j \rvert \le \delta$. Show that OvR predicts a class $j$ with $\eta_j(x) \ge \max_m \eta_m(x) - 2\delta$.
3. Give a distribution with three classes where every Bayes-optimal hinge-loss binary classifier outputs $-1$ on a region of positive probability, and show that OvR with the smallest-index tie rule then has an excess risk that is positive.
4. Suppose the binary learner costs $T(m) = c\, m^2$ and the $k$ classes have $n/k$ examples each. Compare the training cost of OvR, $k c n^2$, with that of one-vs-one.

## References
