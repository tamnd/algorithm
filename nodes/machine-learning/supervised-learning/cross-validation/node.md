---
tag: 1RKJ3F
kind: technique
slug: cross-validation
name: Cross-validation
aliases:
- k-fold cross-validation
- leave-one-out
- stratified k-fold cross-validation
- nested cross-validation
area: machine-learning/supervised-learning
level: intro
summary: "Estimate the risk of a learning procedure by partitioning the data into K folds, training on K - 1 of them, testing on the rest, and averaging over the folds."
prereqs: [generalization-error]
see_also: [hyperparameter-tuning, overfitting, bias-variance-tradeoff, ridge-regression, sherman-morrison-formula, stratified-sampling, early-stopping, ordinary-least-squares]
sources:
  - paper: "M. Stone, Cross-validatory choice and assessment of statistical predictions, Journal of the Royal Statistical Society, Series B 36(2), 111-147, 1974"
    locator: cross-validation for choosing a predictor and for assessing it
  - paper: "Ron Kohavi, A study of cross-validation and bootstrap for accuracy estimation and model selection, Proceedings of the 14th International Joint Conference on Artificial Intelligence, 1137-1143, 1995"
    locator: the comparison of K-fold, stratified and leave-one-out estimates, and the recommendation of stratified 10-fold
  - paper: "Yoshua Bengio and Yves Grandvalet, No unbiased estimator of the variance of K-fold cross-validation, Journal of Machine Learning Research 5, 1089-1105, 2004"
    locator: Corollary 3, equation (7) (the variance in terms of sigma^2, omega and gamma) and Theorem 6 (no universal unbiased estimator of that variance)
  - paper: "Sudhir Varma and Richard Simon, Bias in error estimation when using cross-validation for model selection, BMC Bioinformatics 7, 91, 2006"
    locator: the optimistic bias of the cross-validated error of a tuned classifier, and nested cross-validation
  - paper: "Gavin C. Cawley and Nicola L. C. Talbot, On over-fitting in model selection and subsequent selection bias in performance evaluation, Journal of Machine Learning Research 11, 2079-2107, 2010"
    locator: over-fitting of the model selection criterion and the bias of the reported performance
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 7.10 (7.10.1, K-fold cross-validation, the leave-one-out formula for linear fitting and generalized cross-validation; 7.10.2, the wrong and the right way to do cross-validation)
---

Cross-validation estimates the expected loss of a learning procedure on new data from the data set alone. It partitions the $n$ examples into $K$ folds, trains the procedure on $K - 1$ folds, measures the loss on the held-out fold, and averages over the $K$ choices, so that every example is tested exactly once by a model that did not see it (Stone 1974). $K = n$ is leave-one-out; stratified $K$-fold keeps the class proportions in each fold. It is the standard tool to choose hyperparameters and to compare models, and its two classic failures are leakage of the test folds into training and the use of one cross-validated score both to select and to report.

## In plain words

You want to know how well a method will do on data it has not seen, but you only have one data set. If you test on the same examples you trained on, the score is too good. So you hide part of the data, train on the rest, and test on the hidden part.

One split wastes data and depends on luck. Cross-validation cuts the data into a few equal parts. Each part takes one turn as the hidden test part while the others train the method. Every example is tested once, and you average all the test results.

The rule that matters most: everything the method learns, including how it picks features or settings, must happen inside the training part of each turn.

## When it applies

- The examples are exchangeable: drawn i.i.d., or at least with no dependence that crosses folds. Grouped or time-ordered data need a split that respects the groups or the time order.
- The procedure $A$ can be run $K$ times. Each run costs one training, so cross-validation costs $K$ trainings plus one final fit.
- You want one of two things: the [generalization error](/generalization-error/) of a procedure trained on about $n(K-1)/K$ examples, or a ranking of several procedures or hyperparameter values ([hyperparameter tuning](/hyperparameter-tuning/)).
- A separate test set is too expensive. With plenty of data, one large held-out set is simpler and has a known variance.

## The template

The data is $S = ((x_1, y_1), \ldots, (x_n, y_n))$. The holes are the learner `A` (the whole pipeline, including preprocessing, feature selection and tuning), the loss `ℓ`, the number of folds `K`, and the rule `SPLIT` that makes the folds.

```pseudo id=main
CROSS-VALIDATE(S, A, ℓ, K, SPLIT)                ▷ returns an estimate of the risk of A
L1  (F_1, ..., F_K) ← SPLIT(n, K)                ▷ disjoint, and their union is {1, ..., n}
L2  total ← 0
L3  for k ← 1 to K do
L4      h_k ← A({ (x_i, y_i) : i ∉ F_k })        ▷ every fitted step of A sees only these examples
L5      for each i ∈ F_k do
L6          total ← total + ℓ(y_i, h_k(x_i))
L7  return total / n
```

Common choices for `SPLIT`:

- *K-fold:* shuffle $1, \ldots, n$ and cut it into $K$ blocks whose sizes differ by at most 1.
- *Stratified K-fold:* shuffle within each class, list the classes one after another, and deal the list to the folds in turn. Each class count, and each fold size, then differs by at most 1 across the folds (see [stratified sampling](/stratified-sampling/)).
- *Leave-one-out (LOO):* $K = n$ and $F_i = \{i\}$.
- *Grouped:* all examples of one patient, user or session go to the same fold.

**What it estimates.** Fix $k$. The model $h_k$ depends only on the examples outside $F_k$, so for $i \in F_k$, $\mathbb{E}[\ell(y_i, h_k(x_i))] = \mathbb{E}_{S'}[R(A(S'))]$ with $\lvert S' \rvert = n - \lvert F_k \rvert$. With equal fold sizes the estimate is unbiased for the expected risk of $A$ trained on $n(K-1)/K$ examples. A learner usually improves with more data, so this is slightly pessimistic for the final model trained on all $n$; the bias shrinks as $K$ grows. The estimate is about the *procedure* $A$, not about the one model that you deploy.

**The variance has no unbiased estimator.** Let $e_i$ be the loss of example $i$ and $m = n/K$ the fold size. Bengio and Grandvalet (2004, Corollary 3) show that the variance of the $K$-fold estimate is

$$\theta = \frac{\sigma^2}{n} + \frac{m - 1}{n}\, \omega + \frac{n - m}{n}\, \gamma,$$

where $\sigma^2 = \operatorname{Var}(e_i)$, $\omega$ is the covariance of two errors in the same fold, and $\gamma$ the covariance of two errors in different folds. The term $\gamma$ is not zero, because the training sets of different folds overlap. Their Theorem 6: no estimator computed from the $n$ errors of one $K$-fold run is unbiased for $\theta$ under all distributions. The usual "standard error over the folds", which treats the $K$ fold scores as independent, ignores $\gamma$ and is usually too small.

**Cost, and the leave-one-out shortcut for least squares.** In general LOO costs $n$ trainings. For a linear least squares or [ridge](/ridge-regression/) fit, one fit is enough. Let $A = X^\top X + \lambda I$, the fitted values $\hat y = H y$ with the hat matrix $H = X A^{-1} X^\top$, and the leverages $h_{ii} = x_i^\top A^{-1} x_i$. If $h_{ii} < 1$, the residual of the model refitted without example $i$ is

$$y_i - \hat y_{(i)} = \frac{y_i - \hat y_i}{1 - h_{ii}}.$$

*Proof.* Without example $i$ the matrix is $A - x_i x_i^\top$, and the right side is $X^\top y - x_i y_i$. The [Sherman-Morrison formula](/sherman-morrison-formula/) gives $(A - x_i x_i^\top)^{-1} = A^{-1} + \frac{A^{-1} x_i x_i^\top A^{-1}}{1 - h_{ii}}$, so $x_i^\top (A - x_i x_i^\top)^{-1} = \frac{x_i^\top A^{-1}}{1 - h_{ii}}$. Hence $\hat y_{(i)} = \frac{x_i^\top A^{-1}(X^\top y - x_i y_i)}{1 - h_{ii}} = \frac{\hat y_i - h_{ii} y_i}{1 - h_{ii}}$, and $y_i - \hat y_{(i)} = \frac{y_i - \hat y_i}{1 - h_{ii}}$. $\blacksquare$

So the LOO mean squared error is $\frac1n \sum_i \big(\frac{y_i - \hat y_i}{1 - h_{ii}}\big)^2$, at the cost of one fit and the diagonal of $H$. Generalized cross-validation replaces each $h_{ii}$ by the mean $\operatorname{tr}(H)/n$ (ESL Section 7.10.1). For [ordinary least squares](/ordinary-least-squares/) with $p$ independent columns, $\operatorname{tr}(H) = p$.

**Worked example.** Fit a line to $(0, 1), (1, 2), (2, 2), (4, 5)$. The fit is $\hat y = 0.8 + \frac{34}{35}x$, the residuals are $\frac15, \frac{8}{35}, -\frac{26}{35}, \frac{11}{35}$, and the leverages are $\frac35, \frac{11}{35}, \frac{9}{35}, \frac{29}{35}$ (they sum to 2, the number of parameters). The LOO residuals are $\frac12, \frac13, -1, \frac{11}{6}$. For the last point, the line through the first three is $\hat y = \frac76 + \frac12 x$, which predicts $\frac{19}{6}$ at $x = 4$, and $5 - \frac{19}{6} = \frac{11}{6}$, as the formula says. The training MSE is $0.186$, the LOO MSE is $85/72 = 1.181$, and GCV gives $0.743$; the high-leverage point at $x = 4$ dominates LOO.

## Classic examples

- Choosing the penalty $\lambda$ of [ridge regression](/ridge-regression/) or the lasso over a grid, often with the LOO shortcut or GCV.
- Choosing $k$ in [k-nearest neighbors](/k-nearest-neighbors/); LOO is cheap there because removing one point only changes its own neighbor list.
- Pruning a [decision tree](/decision-tree/): CART picks the cost-complexity parameter by 10-fold cross-validation.
- The number of rounds of [gradient boosting](/gradient-boosting/), and the stopping epoch in [early stopping](/early-stopping/).
- The penalty $C$ and the kernel width of a [support vector machine](/support-vector-machine/).
- Comparing [logistic regression](/logistic-regression/) with a [random forest](/random-forest/) on the same folds, so that the fold-to-fold noise is shared.

## Variations

- **Repeated K-fold.** Run $K$-fold several times with new shuffles and average. This removes the dependence on one random split, but not the $\gamma$ term.
- **Nested cross-validation.** To report the performance of "tune, then fit", put the whole tuning loop inside `A`: an outer $K$-fold loop holds out test folds, and on each outer training part an inner cross-validation picks the hyperparameter (Varma and Simon 2006). The outer estimate is then honest for the tuned procedure. The hyperparameters chosen in the outer folds may differ; that is expected.
- **The one-standard-error rule.** Among models whose CV error is within one standard error of the best, take the simplest (ESL Section 7.10).
- **Grouped and time-series splits.** Keep groups whole; for time series, train on the past and test on the next block only.
- **Monte Carlo cross-validation.** Draw many random train and test splits. The test sets may overlap, so they do not partition the data.
- **Cross-validation for classification metrics.** Pool the predictions of all folds and compute one [confusion matrix](/confusion-matrix/) or one [ROC AUC](/roc-auc/), or average the per-fold values; for AUC the two can differ.

## Pitfalls

- **Leakage.** Any step fitted on all the data before the split (feature selection, scaling, imputation, oversampling, choosing a threshold) lets the test folds influence the model. ESL Section 7.10.2 shows the scale: with 50 samples, 5000 predictors independent of the labels, the 100 predictors most correlated with the labels chosen on all the data, and a 1-nearest-neighbor classifier, the cross-validated error was about 3 percent, though the true error is 50 percent. The fix is to put the selection inside `A`.
- **Selection bias.** The best of many cross-validated scores is optimistic for the model it selects, because the selection used the same folds (Cawley and Talbot 2010). Report a nested estimate or a fresh test set.
- **Duplicates and groups.** Near-identical examples split across folds make the test easy.
- **Leave-one-out can fail badly.** For a majority-class predictor on a data set with exactly half of each class, removing one example makes the other class the majority, so every LOO prediction is wrong and the LOO error is 1, while the true error is $\frac12$ (Kohavi 1995). LOO also has high variance for the 0-1 loss.
- **Over-trusting the fold spread.** The spread of the $K$ scores does not give an unbiased variance; see Bengio and Grandvalet above. Paired comparisons of two models on the same folds are more reliable than comparing two independent estimates.
- **Unstratified folds with rare classes.** A fold with no positives makes recall undefined; stratify.

## Exercises

1. Show that for $\lambda > 0$ every leverage of ridge regression satisfies $h_{ii} < 1$, so the LOO shortcut always applies. (Hint: write $H$ in the eigenbasis of $X^\top X$.)
2. Show that GCV and LOO give the same value when all leverages are equal, and that this holds for a model with only an intercept, where $h_{ii} = 1/n$ and the LOO residual is $\frac{n}{n - 1}(y_i - \bar y)$.
3. For the 1-nearest-neighbor classifier, show that LOO needs only the nearest other training point of each point, and give an $O(n^2 d)$ algorithm.
4. Prove that stratified dealing (list the examples class by class, then assign position $t$ to fold $t \bmod K$) gives class counts and fold sizes that each differ by at most 1 across the folds.
5. In the formula for $\theta$, suppose $\omega = \gamma$. Show that $\theta = \frac{\sigma^2 - \omega}{n} + \omega$, so the variance does not go to 0 as $n$ grows if $\omega$ stays at a fixed positive value.

## References
