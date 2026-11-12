---
tag: 1ASVXZ
kind: technique
slug: ensemble-learning
name: Ensemble learning
aliases:
- ensemble methods
- multiple classifier systems
area: machine-learning/supervised-learning
level: intro
summary: "Train several predictors and combine them by vote, average or a learned rule. The combination helps when the members are accurate and make different errors."
prereqs: [classification, variance]
see_also: [bias-variance-tradeoff, binomial-distribution, hoeffding-inequality, weak-learnability-equivalence, generalization-error, overfitting, cross-validation]
sources:
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 15.2 (Eq. 15.1, the variance of an average of identically distributed variables with pairwise correlation rho) and Chapter 16 (ensemble learning)
  - paper: doi:10.1007/3-540-45014-9_1
    title: Thomas G. Dietterich, Ensemble methods in machine learning, Multiple Classifier Systems, Lecture Notes in Computer Science 1857, 2000
    locator: the condition that the members be accurate and diverse, and the statistical, computational and representational reasons why ensembles work
  - paper: doi:10.1109/34.58871
    title: Lars Kai Hansen and Peter Salamon, Neural network ensembles, IEEE Transactions on Pattern Analysis and Machine Intelligence 12(10), 1990
    locator: the majority vote of networks with independent errors and its binomial error rate
  - paper: "Anders Krogh and Jesper Vedelsby, Neural network ensembles, cross validation, and active learning, Advances in Neural Information Processing Systems 7, 1995"
    locator: the ambiguity decomposition of the squared error of a weighted average
  - paper: "Marie Jean Antoine Nicolas de Caritat, marquis de Condorcet, Essai sur l'application de l'analyse à la probabilité des décisions rendues à la pluralité des voix, Imprimerie Royale, Paris, 1785"
    locator: the probability that a majority of independent voters, each right with probability above one half, is right, and its limit 1
  - paper: doi:10.1007/BF00058655
    title: Leo Breiman, Bagging predictors, Machine Learning 24(2), 1996
    locator: the aggregated predictor and the gain of averaging an unstable learner
  - paper: doi:10.1006/jcss.1997.1504
    title: Yoav Freund and Robert E. Schapire, A decision-theoretic generalization of on-line learning and an application to boosting, Journal of Computer and System Sciences 55(1), 1997
    locator: Section 4 (AdaBoost, an ensemble whose members are trained in sequence)
---

Ensemble learning is the technique of training several predictors, the members, and combining their outputs into one prediction, by a majority vote, an average, a weighted sum, or a second learned model. The members can be trained independently on different versions of the data, as in [bagging](/bagging/) and [random forests](/random-forest/), in sequence with each one correcting the earlier ones, as in [boosting](/boosting/), or as different algorithms combined by a learned rule, as in [stacking](/stacking/). An ensemble is better than its members when the members are accurate and their errors differ. Two exact facts show why: the variance of an average of $m$ predictors with pairwise correlation $\rho$ is $\rho\sigma^2 + (1 - \rho)\sigma^2/m$, and a majority of independent voters that are each right with probability $p > 1/2$ is right with a probability that tends to 1.

## In plain words

Ask one expert and you get one opinion, with its own mistakes. Ask many experts and take the most common answer, or the average, and many of the mistakes cancel out. This works only if two things are true. Each expert must be better than a guess. And the experts must not all make the same mistakes: if they all think alike, asking more of them adds nothing. So ensemble methods train many models that are each good but different from each other, for example by giving each model a different sample of the data, or by making each model focus on what the others got wrong.

## When it applies

- The data model is a training set $S = \{(x_1, y_1), \ldots, (x_n, y_n)\}$ drawn i.i.d. from a distribution, for [classification](/classification/) or regression, and a way to build $m$ members from it: several learners, or one learner with different data, weights, features or random seeds.
- Each member is better than chance: for a vote, right with probability above $1/2$ on two classes; for an average, with a small bias.
- The members are diverse: their errors are not strongly positively correlated. The gain of averaging falls to 0 as the correlation $\rho$ goes to 1.
- The cost of training and evaluating $m$ members is acceptable.

## The template

```pseudo id=main
ENSEMBLE(S, A_1, ..., A_m, combine)
L1  for j ← 1 to m do
L2      S_j ← a training set made from S: S itself, a resample, a reweighting, or a subset of the features
L3      f_j ← A_j(S_j)                ▷ S_j may depend on f_1, ..., f_{j-1} (boosting) or not (bagging)
L4  return x ↦ combine(f_1(x), ..., f_m(x))      ▷ a vote, an average, a weighted sum, or a learned combiner
```

**Averaging lowers the variance.** Let $f_1(x), \ldots, f_m(x)$ be identically distributed over the randomness of the training, each with variance $\sigma^2$, and each pair with correlation $\rho$. The variance of their average is the sum of all the covariances divided by $m^2$: $m$ variances $\sigma^2$ and $m(m - 1)$ covariances $\rho\sigma^2$. So

$$\mathrm{var}\Big(\frac1m \sum_{j=1}^{m} f_j(x)\Big) = \frac{m\sigma^2 + m(m - 1)\rho\sigma^2}{m^2} = \rho\sigma^2 + \frac{1 - \rho}{m}\,\sigma^2,$$

which is Eq. 15.1 of Hastie, Tibshirani and Friedman. More members remove only the second term. The first term stays, so lowering $\rho$, that is diversity, matters as much as adding members. The bias of the average is the bias of one member, so averaging does not lower the bias (see the [bias-variance tradeoff](/bias-variance-tradeoff/)).

**The ambiguity decomposition.** For a weighted average $\bar f = \sum_j w_j f_j$ with $w_j \ge 0$ and $\sum_j w_j = 1$, and any target $y$, Krogh and Vedelsby showed

$$(\bar f - y)^2 = \sum_j w_j (f_j - y)^2 - \sum_j w_j (f_j - \bar f)^2.$$

The ensemble error equals the weighted error of the members minus their spread around the average, the ambiguity. It is never worse than the weighted member error, and the gain is exactly the diversity of the predictions.

**The Condorcet jury theorem.** Let $m$ be odd, and let $m$ voters be right independently, each with probability $p$. The majority is right with probability $P_m = \sum_{k > m/2} \binom{m}{k} p^k (1 - p)^{m - k}$, a [binomial](/binomial-distribution/) tail. Going from $m$ to $m + 2$ voters changes the result only when the first $m$ votes are split by one, which gives

$$P_{m+2} - P_m = \binom{m}{(m-1)/2} \big(p(1 - p)\big)^{(m+1)/2} (2p - 1).$$

So $P_m$ increases with $m$ when $p > 1/2$ and decreases when $p < 1/2$. By [Hoeffding's inequality](/hoeffding-inequality/), $1 - P_m \le e^{-2m(p - 1/2)^2}$, so $P_m \to 1$ when $p > 1/2$. For $p = 0.6$: $P_1 = 0.6$, $P_3 = 0.648$, $P_5 = 0.6826$, $P_{11} = 0.7535$, $P_{51} = 0.9265$ and $P_{101} = 0.9791$.

**Diversity in the vote.** Independence is a strong assumption, and the members of real ensembles are trained on the same data. With $m = 3$ members that are each right with probability $0.6$, the expected number of right votes is $1.8$. If they are always right or wrong together, the majority is right with probability $0.6$. If their errors never overlap, the majority is right whenever at least two are right, and the bound $2 P_3 \le 1.8$ is reached at $P_3 = 0.9$. If they are right together and wrong apart, $P_3$ falls to $0.4$, below a single member. The joint pattern of the errors, not only their rates, decides the result.

## Classic examples

- **Bagging.** [Bagging](/bagging/) trains one learner on bootstrap samples and averages, to lower the variance of an unstable learner.
- **Random forests and extra trees.** A [random forest](/random-forest/) adds random feature choices to bagged trees to lower $\rho$; [extremely randomized trees](/extremely-randomized-trees/) also draw the cut points at random.
- **Boosting.** [Boosting](/boosting/), with [AdaBoost](/adaboost/) and [gradient boosting](/gradient-boosting/), trains the members in sequence so that each one corrects the errors of the earlier ones, which lowers the bias. The [equivalence of weak and strong learnability](/weak-learnability-equivalence/) shows that this can turn slightly better than random learners into accurate ones.
- **Stacking.** [Stacking](/stacking/) combines different algorithms by a second learner fitted on their held-out predictions.
- **Neural network ensembles.** Hansen and Salamon averaged networks trained from different random starts; ensembles of networks remain a simple way to improve accuracy and calibration.

## Variations

- **Ways to make members differ.** Resample the examples, reweight them, choose subsets of the features, inject randomness into the learner, change its parameters, or use different algorithms.
- **Ways to combine.** A plain majority vote or average; a weighted vote with weights from the accuracy of each member, as in AdaBoost; an average of class probabilities; or a learned combiner, as in stacking.
- **Parallel and sequential ensembles.** Independent members (bagging, forests) can be trained in parallel and mainly lower the variance. Sequential members (boosting) depend on each other and can lower the bias too.
- **Selection and pruning.** Keep only a subset of the members, chosen on held-out data, to save prediction time or to drop poor members.
- **Bayesian model averaging.** Weight models by their posterior probability. It is related, but its aim is to average over uncertainty about one true model, not to build a richer model.

## Pitfalls

- **Correlated members.** Members trained on the same data with the same algorithm make the same errors. By the variance formula, a large $\rho$ leaves most of the variance, however many members there are.
- **Weak members in a vote.** If the members are right with probability below $1/2$ at some input, the Condorcet argument runs in reverse and the majority is wrong more often than one member.
- **Expecting averaging to fix bias.** An average of biased members has the same bias. Use boosting or richer members when the members underfit.
- **Assuming independence.** The binomial numbers above are an upper limit on what real, correlated members give, not a prediction.
- **Ignoring the cost.** An ensemble of $m$ members takes about $m$ times the memory and prediction time of one member, which matters in deployment.
- **Leaking labels into the combiner.** A learned combiner must be fitted on predictions for examples the members did not train on, as in [stacking](/stacking/).

## Exercises

1. Derive $\mathrm{var}(\frac1m \sum_j f_j) = \rho\sigma^2 + (1 - \rho)\sigma^2/m$, and show that $\rho \ge -1/(m - 1)$ is needed for the variance to be non-negative.
2. Prove the ambiguity decomposition by expanding $(f_j - y)^2 = ((f_j - \bar f) + (\bar f - y))^2$ and summing with the weights $w_j$.
3. Prove the formula for $P_{m+2} - P_m$ in the Condorcet theorem by looking at the cases where the two new votes change the majority.
4. Three classifiers on two classes are each right with probability $0.7$. Find the largest and the smallest possible accuracy of their majority vote over all joint distributions of their errors.
5. Use Hoeffding's inequality to find how many independent voters with $p = 0.55$ are enough for the majority to be right with probability at least $0.99$.

## References
