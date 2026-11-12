---
tag: 2W5J8D
kind: technique
slug: stacking
name: Stacking
aliases:
- stacked generalization
- stacked regressions
area: machine-learning/supervised-learning
level: advanced
summary: "Fit a level-1 learner on the out-of-fold predictions of several level-0 learners. In-sample predictions leak the labels and give an over-optimistic combination."
prereqs: [ensemble-learning, cross-validation]
see_also: [bagging, boosting, ridge-regression, k-nearest-neighbors, least-squares-problem, quadratic-programming, overfitting, logistic-regression]
sources:
  - paper: doi:10.1016/S0893-6080(05)80023-1
    title: David H. Wolpert, Stacked generalization, Neural Networks 5(2), 1992
    locator: the level-0 and level-1 spaces, the partition of the learning set into held-out parts, and the use of the guesses on held-out points as the inputs of the level-1 learner
  - paper: doi:10.1007/BF00117832
    title: Leo Breiman, Stacked regressions, Machine Learning 24(1), 1996
    locator: stacking by cross-validated predictions with a linear level-1 combination, the non-negativity constraint on the weights, and the experiments with trees and subset regressions
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 8.8 (model averaging and stacking, with leave-one-out predictions as the inputs of the combination)
  - paper: doi:10.1613/jair.594
    title: Kai Ming Ting and Ian H. Witten, Issues in stacked generalization, Journal of Artificial Intelligence Research 10, 1999
    locator: class probabilities as level-1 inputs and multi-response linear regression as the level-1 learner for classification
  - paper: doi:10.2202/1544-6115.1309
    title: Mark J. van der Laan, Eric C. Polley and Alan E. Hubbard, Super learner, Statistical Applications in Genetics and Molecular Biology 6(1), 2007
    locator: stacking with V-fold cross-validation and an oracle inequality for the cross-validated selection of the combination
  - book: isbn:9780898713565
    title: Charles L. Lawson and Richard J. Hanson, Solving Least Squares Problems, SIAM, 1995
    locator: Chapter 23 (the active set algorithm for non-negative least squares)
---

Stacking, or stacked generalization, is a technique of Wolpert (1992) that combines several learners with a second learner. The first-level, or level-0, learners are fitted on folds of the training data, and their predictions on the examples that each fit did not see form a new data set. A level-1 learner, also called the meta-learner, is fitted on this data set to map the level-0 predictions to the label. For prediction, the level-0 learners are refitted on all the data, and the level-1 learner combines their outputs. Breiman (1996) studied stacked regressions, where the level-1 learner is a linear combination with non-negative weights fitted by least squares. The key rule is that the level-1 inputs must be out-of-fold predictions: in-sample predictions favor the learners that overfit most.

## In plain words

You have several models, and you want to know how much to trust each one. Ask each model to predict examples it was not trained on: split the data into parts, train on all parts but one, and predict the part that was left out, for each part in turn. Now each example has one honest prediction from each model. Train a small second model that takes these predictions as input and gives the final answer. It learns which models to trust, and how to mix them. Finally, train the first models again on all the data, and feed their predictions to the second model.

## When it applies

- The data model is a training set $S = \{(x_1, y_1), \ldots, (x_n, y_n)\}$ drawn i.i.d. from a distribution, with $L$ level-0 learners $A_1, \ldots, A_L$ that each map a training set to a predictor, and a level-1 learner $M$.
- The level-0 learners are different, so that their errors are not too correlated. Stacking copies of one learner gives little.
- There are enough examples for $K$-fold [cross-validation](/cross-validation/), and $K$ fits of each level-0 learner are affordable.
- The level-1 learner is simple: a linear combination, often with non-negative weights, or a [logistic regression](/logistic-regression/) on class probabilities. A flexible level-1 learner can overfit the $n$ level-1 examples.

## The template

```pseudo id=main
STACKING(S, A_1, ..., A_L, M, K)
L1  split {1, ..., n} at random into K folds F_1, ..., F_K of nearly equal size
L2  for k ← 1 to K do
L3      for l ← 1 to L: g ← A_l(S without the examples of F_k); z_il ← g(x_i) for each i ∈ F_k
L4  h ← M fitted on the level-1 data (z_i, y_i), i = 1, ..., n      ▷ z_i = (z_i1, ..., z_iL)
L5  for l ← 1 to L: f_l ← A_l(S)
L6  return the predictor x ↦ h(f_1(x), ..., f_L(x))
```

**Why the level-1 inputs must be out of fold.** In line L3, each $z_{il}$ comes from a fit that did not see example $i$, so $z_{il}$ behaves like the prediction of $A_l$ on a new example, and the level-1 learner sees how each level-0 learner does on unseen data. If instead each $A_l$ is fitted on all of $S$ and predicts its own training examples, the level-1 data reward memorization. A [1-nearest-neighbor](/k-nearest-neighbors/) learner predicts each training label exactly, so a least squares combination puts all the weight on it and reports zero error, whatever its error on new data.

**Breiman's combination.** For regression, Breiman takes $h(z) = \sum_l w_l z_l$ with

$$w = \arg\min_{w \ge 0} \sum_{i=1}^{n} \Big(y_i - \sum_{l=1}^{L} w_l z_{il}\Big)^2,$$

a non-negative least squares (NNLS) problem. Unconstrained weights are often large with opposite signs, because the level-0 predictions are highly correlated; the constraint $w \ge 0$ makes the combination stable. Breiman found that the weights need not be forced to sum to 1. NNLS is a convex [quadratic program](/quadratic-programming/). The active set method of Lawson and Hanson solves it; for a few learners, one can also solve the [least squares problem](/least-squares-problem/) on each support of $w$ and keep the best non-negative solution. A point $w \ge 0$ is optimal exactly when the gradient $Z^\top(Zw - y)$ is zero on the support of $w$ and not negative elsewhere.

**Cost.** $K L$ fits on about $n(K - 1)/K$ examples, $L$ fits on $n$ examples, one fit of the level-1 learner on $n$ examples with $L$ features, and $L$ predictions per query.

**Example.** Take $x = 1, \ldots, 6$ and $y = 1, 3, 2, 5, 4, 6$, the folds $\{1, 4\}$, $\{2, 5\}$ and $\{3, 6\}$, and three level-0 learners: 1-nearest neighbor (ties to the smaller $x$), the least squares line, and the mean of $y$. The out-of-fold predictions are:

| $x$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $y$ | 1 | 3 | 2 | 5 | 4 | 6 |
| 1-NN | 3 | 1 | 3 | 2 | 5 | 4 |
| line | 1.35 | 1.8846 | 3.25 | 3.75 | 5.1154 | 5.65 |
| mean | 3.75 | 3.5 | 3.25 | 3.75 | 3.5 | 3.25 |

Alone, the three columns have squared errors $23$, $5.8582$ and $18.75$. NNLS gives the weights $(0, 0.8854, 0.1188)$ with squared error $5.6358$. With in-sample predictions instead, the 1-NN column equals $y$, NNLS gives $(1, 0, 0)$ with squared error $0$, and the same weights on the out-of-fold predictions have squared error $23$.

## Classic examples

- **Stacked regressions.** Breiman stacked [regression trees](/cart/) of different sizes, and linear regressions on subsets of the variables of different sizes, with NNLS weights on cross-validated predictions.
- **Stacking classifiers by probabilities.** Ting and Witten feed the class probabilities of the level-0 classifiers, not their hard labels, to a level-1 linear model per class.
- **Super learner.** van der Laan, Polley and Hubbard use $V$-fold cross-validation to fit a convex combination of many learners, and prove that it does about as well as the best combination as $n$ grows.
- **Blending in competitions.** Many prediction competitions are won by a linear blend of very different models, such as [boosted trees](/gradient-boosting/), neural networks and [k-nearest neighbors](/k-nearest-neighbors/), fitted on held-out predictions.
- **Model selection as stacking.** Picking the single learner with the smallest cross-validation error is stacking with a level-1 learner restricted to weight vectors with one entry 1 and the others 0.

## Variations

- **Blending.** Fit the level-0 learners once on part of the data and fit the level-1 learner on their predictions on a held-out part. It is simpler and avoids $K$ refits, but uses fewer examples at each level.
- **Leave-one-out stacking.** With $K = n$, the level-1 inputs are leave-one-out predictions, as in Hastie, Tibshirani and Friedman, Section 8.8.
- **Feature-weighted stacking.** Let the weights depend on the input, for example through features of $x$ multiplied by the level-0 predictions.
- **Multi-level stacking.** Stack the stacked models again, with new folds at each level, at a growing risk of overfitting.
- **Regularized level-1 learners.** Use [ridge regression](/ridge-regression/), or a sum-to-one constraint, instead of or together with non-negativity.

## Pitfalls

- **Leakage through in-sample predictions.** Line L3 must predict only the fold that the fit did not see. In-sample predictions give the most flexible learner all the weight and an apparent error that is far too small.
- **Reusing the folds to judge the stack.** The level-1 learner was fitted on the out-of-fold predictions, so its error on them is itself optimistic. Estimate the error of the whole stack with an outer cross-validation or a separate test set.
- **Forgetting to refit.** Line L5 refits each level-0 learner on all of $S$. Using the $K$ fold models at prediction time is a valid variant (average them), but mixing the two by mistake gives inputs with a different scale than the level-1 learner saw.
- **A level-1 learner that is too flexible.** With $L$ correlated inputs and $n$ examples, unconstrained least squares can give huge weights of opposite signs. Non-negativity or a penalty prevents this.
- **Leaking through preprocessing.** Feature scaling, feature selection or target encoding fitted on all of $S$ before the folds also leaks the labels of the held-out fold.

## Exercises

1. Show that with in-sample predictions and a 1-nearest-neighbor learner among the level-0 learners (with distinct inputs), every minimizer of the NNLS problem has zero residual, and that $w = e_1$ is one of them.
2. Prove that $w \ge 0$ minimizes $\|Zw - y\|^2$ subject to $w \ge 0$ if and only if $g = Z^\top(Zw - y)$ satisfies $g_l = 0$ when $w_l > 0$ and $g_l \ge 0$ when $w_l = 0$.
3. Show that choosing the learner with the least cross-validation error is a special case of stacking, and name the level-1 hypothesis class.
4. Count the fits of the level-0 learners in $K$-fold stacking with $L$ learners, and with an outer $K'$-fold cross-validation to estimate the error of the stack.
5. Two level-0 learners have nearly equal out-of-fold predictions, $z_{i2} = z_{i1} + \varepsilon u_i$. Show that the unconstrained least squares weights can grow like $1/\varepsilon$ with opposite signs, and that the non-negative weights stay bounded as $\varepsilon \to 0$.

## References
