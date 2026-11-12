---
tag: 251C6Y
kind: technique
slug: bagging
name: Bagging
aliases:
- bootstrap aggregating
area: machine-learning/supervised-learning
level: core
summary: "Fit one learner on many bootstrap resamples of the data and average or vote. It lowers the variance of unstable learners, and the left-out examples give a free error estimate."
prereqs: [ensemble-learning, bias-variance-tradeoff]
see_also: [random-forest, extremely-randomized-trees, cart, boosting, stacking, cross-validation, jensens-inequality, random-sampling]
sources:
  - paper: doi:10.1007/BF00058655
    title: Leo Breiman, Bagging predictors, Machine Learning 24(2), 1996
    locator: the definition of bagging, the experiments with bagged classification and regression trees, and the section on why bagging works (the aggregated predictor, the inequality from Jensen and the role of instability)
  - paper: doi:10.1214/aos/1176344552
    title: Bradley Efron, Bootstrap methods, another look at the jackknife, Annals of Statistics 7(1), 1979
    locator: the bootstrap resample of n points drawn with replacement
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 8.7 (bagging, its effect on squared error and on classification) and Section 15.3.1 (out-of-bag samples)
  - paper: doi:10.1023/A:1010933404324
    title: Leo Breiman, Random forests, Machine Learning 45(1), 2001
    locator: Section 3 (out-of-bag estimates of the error, the strength and the correlation)
  - paper: doi:10.1214/aos/1031689014
    title: Peter Bühlmann and Bin Yu, Analyzing bagging, Annals of Statistics 30(4), 2002
    locator: bagging as a smoother of hard decisions, its variance reduction for indicator predictors, and subagging
  - paper: "Leo Breiman, Heuristics of instability and stabilization in model selection, Annals of Statistics 24(6), 1996"
    locator: unstable procedures such as subset selection and trees, and stable ones such as ridge regression
---

Bagging, short for bootstrap aggregating, is a technique of Breiman (1996) that turns one learning algorithm into an ensemble. It draws $B$ bootstrap samples of the training set, each of $n$ examples drawn with replacement, fits the same learner on each, and combines the $B$ predictors by the average for regression or by a majority vote for classification. The average has a smaller variance than one fit, and the reduction is large when the learner is unstable, that is when small changes of the data change the fit a lot, as with deep [decision trees](/cart/). Each bootstrap sample leaves out about $1/e \approx 36.8\%$ of the examples, and these out-of-bag (OOB) examples give an estimate of the error with no extra fitting.

## In plain words

Some learners give quite different answers when the data changes a little. Bagging uses this. Make many new data sets from the one you have, by drawing examples at random and putting each one back after you draw it, so that some appear twice and some not at all. Train the learner on each new data set. To predict, take the average of all the answers, or the answer that most of them give. The jumps of the single learners partly cancel. Each learner never saw about a third of the examples, so you can test each example on the learners that never saw it.

## When it applies

- The data model is a training set $S = \{(x_1, y_1), \ldots, (x_n, y_n)\}$ drawn i.i.d. from a distribution, with labels that are classes or real numbers, and a deterministic learner $A$ that maps a training set to a predictor.
- The learner is unstable: its prediction at a point has a large [variance](/variance/) over training sets. Deep trees, subset selection and neural networks are unstable. [k-nearest neighbors](/k-nearest-neighbors/) with large $k$, [ridge regression](/ridge-regression/) and linear discriminant analysis are stable, and bagging gives them little.
- The learner has a low bias, so that the average of its fits is close to the target. Bagging does not reduce bias.
- For classification by vote, the base classifier must be right at a point more often than any other class over training sets. Where it is usually wrong, the vote makes it always wrong.
- The cost of $B$ fits is acceptable. The fits are independent, so they run in parallel.

## The template

```pseudo id=main
BAGGING(S, A, B)
L1  for b ← 1 to B do
L2      S_b ← n examples drawn from S uniformly with replacement      ▷ a bootstrap sample
L3      f_b ← A(S_b)
L4  return f(x) = (1/B) Σ_b f_b(x) for regression, or the majority vote of f_1(x), ..., f_B(x) for classification

OUT-OF-BAG(S, f_1, ..., f_B)
L5  for i ← 1 to n: f_oob(x_i) ← the average (or vote) of the f_b with (x_i, y_i) ∉ S_b
L6  return the average loss of f_oob(x_i) against y_i, over the i that have at least one such b
```

**The size of a bootstrap sample.** Example $i$ is missing from $S_b$ when all $n$ draws miss it, with probability $(1 - 1/n)^n$. By [linearity of expectation](/linearity-of-expectation/), the expected number of distinct examples in $S_b$ is $n\,(1 - (1 - 1/n)^n)$. Since $\ln(1 - 1/n) \le -1/n$ and $\ln(1 - 1/n) \ge -1/(n - 1)$,

$$\frac1e\left(1 - \frac1n\right) \le \left(1 - \frac1n\right)^n \le \frac1e,$$

so the expected fraction of distinct examples is within $1/(en)$ of $1 - 1/e \approx 0.632$, from above. For $n = 3$, the $27$ equally likely samples have 3 distinct examples in 6 cases, 2 in 18 cases and 1 in 3 cases, so the expected fraction is $(18 + 36 + 3)/81 = 19/27 = 1 - (2/3)^3 \approx 0.704$.

**Why averaging helps for squared loss.** Breiman compares the predictor $f(x; S)$ with the aggregated predictor $f_A(x) = \mathbb{E}_S\, f(x; S)$, the average over training sets of size $n$. For a fixed $(x, y)$, [Jensen's inequality](/jensens-inequality/) gives

$$\mathbb{E}_S\,(y - f(x; S))^2 = (y - f_A(x))^2 + \mathrm{var}_S\, f(x; S) \ge (y - f_A(x))^2.$$

The gain is exactly the variance of the learner at $x$, so it is large for unstable learners and near zero for stable ones. Bagging replaces the unknown distribution by the empirical one: the bootstrap samples imitate fresh training sets, and line L4 approximates $f_A$. The same identity holds for the $B$ fitted predictors: the squared error of their average is the mean squared error of the members minus the spread of their predictions.

**Why the OOB estimate is honest.** In line L5 each $f_b$ used for example $i$ was fitted on a sample without $(x_i, y_i)$, so it predicts an unseen example. The OOB error is like a [cross-validation](/cross-validation/) error of an ensemble of about $B/e$ members, at no extra cost.

**Cost.** $B$ times the cost of the learner on $n$ examples, plus $B$ predictions per query. The OOB error costs about $nB/e$ predictions.

## Classic examples

- **Bagged decision trees.** Breiman's experiments bagged [CART](/cart/) trees and cut their test error on many data sets. Deep unpruned trees have low bias and high variance, the case where bagging helps most.
- **Random forests.** A [random forest](/random-forest/) is bagging of trees plus a random choice of features at each split, which lowers the correlation between the trees.
- **Extremely randomized trees.** [Extra trees](/extremely-randomized-trees/) drop the bootstrap and randomize the cut points instead; the randomization does the job of the resampling.
- **Bagging a stable learner.** Bagging [k-nearest neighbors](/k-nearest-neighbors/) with a large $k$, or [ordinary least squares](/ordinary-least-squares/) with many examples, changes little, since their variance is already small.
- **OOB error in practice.** The OOB error of a bagged ensemble replaces a separate validation set when choosing the number of trees or other parameters.

## Variations

- **Subagging.** Draw subsamples of size $n/2$ without replacement instead of bootstrap samples. Bühlmann and Yu (2002) show that it behaves much like bagging at a lower cost, and analyze how bagging smooths hard decisions such as the indicator of a split.
- **Averaging probabilities.** For classification, average the class probabilities of the members and take the largest, instead of counting votes. This gives a smoother and often better classifier (Hastie, Tibshirani and Friedman, Section 8.7).
- **Random subspaces and random patches.** Draw random subsets of features, of examples, or of both, for each member.
- **Bootstrap of residuals or smoothed bootstrap.** For regression, resample residuals of a fitted model, or add noise to the inputs, to make new training sets.
- **Bagging and boosting.** [Boosting](/boosting/) also builds an ensemble, but with weights that depend on earlier members. It reduces bias as well as variance, and its members cannot be fit in parallel.

## Pitfalls

- **Bagging a stable or biased learner.** The gain in the identity above is the variance of the learner. A linear model with many examples, or a very shallow tree, has little variance to remove.
- **Voting with a poor classifier.** If, at a point, the base classifier predicts the right class less often than another class over training sets, the vote predicts the wrong class with probability near 1. Bagging can make a classifier worse.
- **Using in-bag predictions as an error estimate.** A member fitted on example $i$ usually predicts it well. Line L5 must use only the members whose sample excludes $i$.
- **Expecting the members to be independent.** Each bootstrap sample holds about $63\%$ of the examples of $S$, so two samples have about $40\%$ of the examples in common, and the members are correlated. The variance of the average stays above $\rho \sigma^2$ however large $B$ is (see [ensemble learning](/ensemble-learning/)).
- **Losing interpretability.** The average of many trees is not a tree, and the simple reading of a single tree is lost.

## Exercises

1. Show that the number of distinct examples in a bootstrap sample of size $n$ has expectation $n(1 - (1 - 1/n)^n)$, and find its variance.
2. Prove $(1 - 1/n)^{n - 1} \ge 1/e$ for $n \ge 2$, and deduce the lower bound on $(1 - 1/n)^n$ used above.
3. For a regression predictor, prove the identity $\frac1B \sum_b (y - f_b)^2 = (y - \bar f)^2 + \frac1B \sum_b (f_b - \bar f)^2$, where $\bar f$ is the average of the $f_b$.
4. A classifier at a fixed $x$ predicts the right class with probability $0.4$ and each of two wrong classes with probability $0.3$ over training sets. What does the vote of many independent copies predict? What if the wrong classes have probabilities $0.5$ and $0.1$?
5. Explain why bagging ordinary least squares with $n$ much larger than $d$ gives nearly the same predictor as one least squares fit.

## References
