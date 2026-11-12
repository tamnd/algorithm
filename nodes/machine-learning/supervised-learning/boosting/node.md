---
tag: 1DCZMK
kind: technique
slug: boosting
name: Boosting
area: machine-learning/supervised-learning
level: core
summary: "Train weak learners one after another, each on data reweighted or relabeled to fix the errors of the sum so far, and combine them by a weighted vote or sum."
prereqs: [ensemble-learning, weak-learnability-equivalence]
see_also: [bagging, decision-stump, margin-generalization-bound, multiplicative-weights-update, early-stopping, logistic-loss, learning-to-rank, overfitting]
sources:
  - paper: doi:10.1007/BF00116037
    title: Robert E. Schapire, The strength of weak learnability, Machine Learning 5(2), 1990
    locator: the first boosting algorithm and the proof that weak learnability implies strong learnability
  - paper: doi:10.1006/inco.1995.1136
    title: Yoav Freund, Boosting a weak learning algorithm by majority, Information and Computation 121(2), 1995
    locator: boost by majority
  - paper: doi:10.1006/jcss.1997.1504
    title: Yoav Freund and Robert E. Schapire, A decision-theoretic generalization of on-line learning and an application to boosting, Journal of Computer and System Sciences 55(1), 1997
    locator: Section 4 (AdaBoost and the bound on its training error, Theorem 6)
  - paper: doi:10.1214/aos/1016218223
    title: Jerome Friedman, Trevor Hastie and Robert Tibshirani, Additive logistic regression, a statistical view of boosting, Annals of Statistics 28(2), 2000
    locator: boosting as forward stagewise additive modeling, AdaBoost and the exponential loss, and LogitBoost
  - paper: doi:10.1214/aos/1013203451
    title: Jerome H. Friedman, Greedy function approximation, a gradient boosting machine, Annals of Statistics 29(5), 2001
    locator: boosting as gradient descent in function space for any differentiable loss
  - paper: doi:10.1214/aos/1024691352
    title: Robert E. Schapire, Yoav Freund, Peter Bartlett and Wee Sun Lee, Boosting the margin, a new explanation for the effectiveness of voting methods, Annals of Statistics 26(5), 1998
    locator: the margin explanation of why the test error can keep falling after the training error is 0
  - book: isbn:9780262017183
    title: Robert E. Schapire and Yoav Freund, Boosting, Foundations and Algorithms, MIT Press, 2012
    locator: Chapter 1 (the boosting setting), Chapter 3 (the training error), Chapter 5 (margins) and Chapter 7 (loss minimization)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Chapter 10 (boosting and additive trees, forward stagewise additive modeling in Algorithm 10.2, the loss functions and their robustness)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, from Theory to Algorithms, Cambridge University Press, 2014
    locator: Chapter 10 (boosting, weak learnability, AdaBoost and its VC dimension)
  - paper: doi:10.1007/s10994-009-5165-z
    title: Philip M. Long and Rocco A. Servedio, Random classification noise defeats all convex potential boosters, Machine Learning 78(3), 2010
    locator: the main theorem on convex potential boosters under random classification noise
---

Boosting is a family of ensemble methods that build a strong predictor from many weak ones trained in sequence. In each round, a weak learner is trained on a version of the data that stresses what the ensemble so far gets wrong: examples with larger weights, or new targets equal to the residual errors. The new member is added to the ensemble with a weight. The result is a weighted vote for classification or a weighted sum for regression. The question that started the field, whether a learner that is only slightly better than chance can be made arbitrarily accurate, has a positive answer, the [equivalence of weak and strong learnability](/weak-learnability-equivalence/). [AdaBoost](/adaboost/) is the classic boosting algorithm, and [gradient boosting](/gradient-boosting/) extends the idea to any differentiable loss.

## In plain words

Train a simple model and look at its mistakes. Train a second simple model that pays more attention to those mistakes. Add it to the first, look at the mistakes of the pair, and train a third model to fix them. Keep going. Each model on its own is weak, maybe only a little better than a guess, but each one fixes part of what the others got wrong, so the sum gets better and better. At the end, all the models vote, and the better ones get a larger say.

## When it applies

- The data model is a training set $S = \{(x_1, y_1), \ldots, (x_n, y_n)\}$, for binary or multiclass [classification](/classification/) or for regression, with a loss that measures the error of a real-valued score $F(x)$.
- A weak learner is available that accepts example weights or arbitrary real targets, and returns a simple hypothesis, such as a [decision stump](/decision-stump/) or a small tree.
- The weak learning assumption holds: on every weighting of the data, the weak learner does better than chance by a margin $\gamma > 0$. For two classes, its weighted error is at most $\frac12 - \gamma$.
- The labels are not too noisy. Boosting puts more and more weight on the examples it cannot fit, which are often the mislabeled ones.
- The rounds can run one after another. Unlike [bagging](/bagging/), the members depend on each other.

## The template

```pseudo id=main
BOOSTING(S, WEAK-LEARNER, T)
L1  F_0 ← 0 (or the best constant); D_1 ← the uniform weights on S
L2  for t ← 1 to T do
L3      h_t ← WEAK-LEARNER(S, D_t)        ▷ fitted to the weighted data, or to new targets such as residuals
L4      α_t ← the weight of h_t that most reduces the loss of F_{t-1} + α h_t
L5      F_t ← F_{t-1} + α_t h_t
L6      D_{t+1} ← weights (or targets) that stress the examples on which F_t does badly
L7  return F_T, or sign(F_T) for two classes
```

This is forward stagewise additive modeling (Friedman, Hastie and Tibshirani 2000; Hastie, Tibshirani and Friedman, Algorithm 10.2): each round adds one term to $F$ and never changes the earlier terms. The members of the family differ in the loss, the weak learner, and the rule of lines L4 and L6.

**AdaBoost.** With labels in $\{-1, +1\}$, the exponential loss $e^{-yF(x)}$, and weak hypotheses with values in $\{-1, +1\}$, line L4 gives $\alpha_t = \frac12 \ln((1 - \varepsilon_t)/\varepsilon_t)$, where $\varepsilon_t$ is the weighted error of $h_t$, and line L6 multiplies the weight of example $i$ by $e^{-\alpha_t y_i h_t(x_i)}$ and normalizes. If $\varepsilon_t = \frac12 - \gamma_t$, the training error of $\mathrm{sign}(F_T)$ is at most

$$\prod_{t=1}^{T} 2\sqrt{\varepsilon_t (1 - \varepsilon_t)} \le \exp\Big(-2 \sum_{t=1}^{T} \gamma_t^2\Big),$$

so under the weak learning assumption it is 0 after $O(\ln n / \gamma^2)$ rounds. The proof is on the page of [AdaBoost](/adaboost/).

**Gradient boosting.** For any differentiable loss $\ell(y, F)$, line L6 sets the new targets to the negative gradient $-\partial \ell(y_i, F_{t-1}(x_i))/\partial F$, line L3 fits a regression tree to them, and line L4 is a line search. For squared loss the targets are the residuals $y_i - F_{t-1}(x_i)$. See [gradient boosting](/gradient-boosting/) and its second-order form [XGBoost](/xgboost/).

**Why boosting can generalize.** The training error bound says nothing about new data. Two explanations are standard. First, the vote of $T$ base hypotheses from a class of [VC dimension](/vc-dimension/) $d$ lies in a class whose VC dimension grows like $O(T d \log(T d))$, so a small $T$ limits overfitting (Shalev-Shwartz and Ben-David, Chapter 10). Second, the margin view of Schapire, Freund, Bartlett and Lee bounds the test error by the fraction of training examples with a small normalized margin $y F(x) / \sum_t |\alpha_t|$, plus a term that does not grow with $T$; AdaBoost keeps raising the margins after the training error is 0 (see [margin bounds](/margin-generalization-bound/)).

## Classic examples

- **The first boosting algorithms.** Schapire (1990) combined three copies of a weak learner trained on filtered data, recursively; Freund's boost by majority (1995) improved its efficiency. Both needed to know $\gamma$ in advance.
- **AdaBoost.** [AdaBoost](/adaboost/) (Freund and Schapire 1997) adapts to the errors $\varepsilon_t$, needs no knowledge of $\gamma$, and is usually run with [decision stumps](/decision-stump/) or small trees.
- **Gradient tree boosting.** [Gradient boosting](/gradient-boosting/) with regression trees, shrinkage and subsampling is a standard method for tabular data, and [XGBoost](/xgboost/) is a widely used system for it.
- **LogitBoost.** Friedman, Hastie and Tibshirani fit the [logistic loss](/logistic-loss/) by Newton steps, one weighted least squares fit per round.
- **Boosting for ranking.** RankBoost and gradient-boosted trees with ranking losses are common methods for [learning to rank](/learning-to-rank/).

## Variations

- **Reweighting, resampling or filtering.** The weak learner can take the weights directly, or be trained on a sample drawn from $D_t$, or see a stream from which examples are kept with a probability that depends on their weight.
- **Shrinkage.** Multiply each $\alpha_t h_t$ by a learning rate $\nu < 1$. More rounds are needed, but the test error is often lower; together with [early stopping](/early-stopping/), it is the usual way to regularize boosting.
- **Confidence-rated predictions.** Let $h_t$ take real values, as in Real AdaBoost and the analysis of Schapire and Singer.
- **Multiclass boosting.** AdaBoost.M1 needs a weighted error below $\frac12$ on $k$ classes, which is hard for weak learners; AdaBoost.M2, AdaBoost.MH and SAMME weaken this requirement.
- **Noise-tolerant boosting.** Losses that grow slowly for badly misclassified examples, such as in BrownBoost or with the logistic or Huber losses, reduce the weight on outliers. Long and Servedio showed that no booster that minimizes a convex potential can tolerate random label noise in general.
- **Online and multiplicative weights.** The reweighting rule of AdaBoost is a case of the [multiplicative weights update](/multiplicative-weights-update/) method, played between the booster and the weak learner.

## Pitfalls

- **Label noise.** The weights of mislabeled examples grow exponentially under the exponential loss, and later rounds spend their effort fitting the noise. Use a more robust loss, shrinkage, or early stopping.
- **A weak learner that is too strong.** If the first hypothesis already fits the training data, its error is 0, the weights are undefined, and boosting stops with one overfitted member. Keep the base hypotheses simple.
- **A weak learner with no edge.** If $\varepsilon_t = \frac12$ on the reweighted data, the round adds nothing. With hypotheses that are too simple, such as stumps on data that needs interactions, boosting stalls at a high error.
- **Too many rounds.** Boosting often resists overfitting for a long time, but it can overfit, especially with noise and without shrinkage. Choose $T$ by [cross-validation](/cross-validation/) or a held-out set.
- **Confusing the two kinds of ensemble.** Boosting mainly reduces bias and needs sequential training; bagging reduces variance and runs in parallel. A boosted ensemble of deep trees and a bagged ensemble of stumps both work poorly.

## Exercises

1. Show that the weight update of AdaBoost gives the last hypothesis a weighted error of exactly $\frac12$ under the new weights $D_{t+1}$.
2. Use the bound $\prod_t 2\sqrt{\varepsilon_t(1 - \varepsilon_t)}$ to show that, if every $\gamma_t \ge \gamma$, the training error is 0 after more than $\ln(n) / (2\gamma^2)$ rounds.
3. Show that for squared loss, the forward stagewise template with a least squares weak learner fits the residuals $y_i - F_{t-1}(x_i)$ in each round.
4. Derive the step $\alpha_t = \frac12 \ln((1 - \varepsilon_t)/\varepsilon_t)$ by minimizing $\sum_i D_t(i)\, e^{-\alpha y_i h_t(x_i)}$ over $\alpha$.
5. Take the four points of XOR in the plane, with label $+1$ at $(0, 0)$ and $(1, 1)$ and label $-1$ at $(0, 1)$ and $(1, 0)$. Show that no weighted vote of decision stumps has zero training error on them, and find weights on the points under which every stump has weighted error $\frac12$.

## References
