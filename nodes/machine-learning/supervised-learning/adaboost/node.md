---
tag: F7R3H9
kind: algorithm
slug: adaboost
name: AdaBoost
aliases:
- adaptive boosting
- discrete AdaBoost
area: machine-learning/supervised-learning
level: core
summary: "Boosting that reweights the training examples after each round and combines weak learners by a weighted vote. Its training error falls like exp(-2 sum of squared edges)."
solves: [classification]
model: real-ram
complexity:
  vars: {n: the number of training examples, d: the number of features, T: the number of rounds}
  time: {worst: "O(d n log n + T d n)"}
  space: {extra: "Θ(d n + T)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1995
  people: [Yoav Freund, Robert Schapire]
  note: Freund and Schapire presented AdaBoost at EuroCOLT 1995 and published the journal version in 1997.
prereqs: [boosting, decision-stump]
see_also: [weak-learnability-equivalence, gradient-boosting, margin-generalization-bound, multiplicative-weights-update, weighted-majority, logistic-loss, multiclass-classification, bagging]
sources:
  - paper: doi:10.1006/jcss.1997.1504
    title: Yoav Freund and Robert E. Schapire, A decision-theoretic generalization of on-line learning and an application to boosting, Journal of Computer and System Sciences 55(1), 1997
    locator: Section 4 (the algorithm AdaBoost and its training error bound, Theorem 6)
  - paper: doi:10.1023/A:1007614523901
    title: Robert E. Schapire and Yoram Singer, Improved boosting algorithms using confidence-rated predictions, Machine Learning 37(3), 1999
    locator: the bound of the training error by the product of the normalizers Z_t, and the choice of alpha_t that minimizes Z_t
  - paper: doi:10.1214/aos/1016218223
    title: Jerome Friedman, Trevor Hastie and Robert Tibshirani, Additive logistic regression, a statistical view of boosting, Annals of Statistics 28(2), 2000
    locator: Discrete AdaBoost as forward stagewise additive modeling with the exponential loss, and the population minimizer of that loss
  - paper: doi:10.4310/SII.2009.v2.n3.a8
    title: Ji Zhu, Hui Zou, Saharon Rosset and Trevor Hastie, Multi-class AdaBoost, Statistics and Its Interface 2(3), 2009
    locator: the algorithm SAMME and its link to a multiclass exponential loss
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 10.1 (Algorithm 10.1, AdaBoost.M1) and Sections 10.4 to 10.6 (the exponential loss and its robustness)
  - book: isbn:9780262017183
    title: Robert E. Schapire and Yoav Freund, Boosting, Foundations and Algorithms, MIT Press, 2012
    locator: Chapter 1 (the algorithm and a toy example) and Chapter 3 (the training error)
  - paper: doi:10.1214/aos/1024691352
    title: Robert E. Schapire, Yoav Freund, Peter Bartlett and Wee Sun Lee, Boosting the margin, a new explanation for the effectiveness of voting methods, Annals of Statistics 26(5), 1998
    locator: the bound on the fraction of training examples with margin at most theta, and the margin bound on the test error
  - paper: doi:10.1007/BF00116037
    title: Robert E. Schapire, The strength of weak learnability, Machine Learning 5(2), 1990
    locator: the first boosting algorithm
  - paper: doi:10.1006/inco.1995.1136
    title: Yoav Freund, Boosting a weak learning algorithm by majority, Information and Computation 121(2), 1995
    locator: boost by majority
  - paper: doi:10.1023/A:1007607513941
    title: Thomas G. Dietterich, An experimental comparison of three methods for constructing ensembles of decision trees, bagging, boosting, and randomization, Machine Learning 40(2), 2000
    locator: the experiments with added classification noise
  - paper: doi:10.1007/s10994-009-5165-z
    title: Philip M. Long and Rocco A. Servedio, Random classification noise defeats all convex potential boosters, Machine Learning 78(3), 2010
    locator: the main theorem on convex potential boosters under random classification noise
---

AdaBoost is the first practical [boosting](/boosting/) algorithm, by Freund and Schapire. It calls a weak learner, such as a [decision stump](/decision-stump/), $T$ times on reweighted copies of the training set, and after each round it raises the weight of the examples that the last weak hypothesis got wrong. The output is the weighted vote $\operatorname{sign}(\sum_t \alpha_t h_t(x))$ with $\alpha_t = \frac12 \ln((1 - \varepsilon_t)/\varepsilon_t)$. If each weak hypothesis has weighted error $\varepsilon_t = \frac12 - \gamma_t$, the training error of the vote is at most $\exp(-2\sum_t \gamma_t^2)$, so it falls exponentially fast. This bound gives the constructive half of the [equivalence of weak and strong learnability](/weak-learnability-equivalence/).

## In plain words

You have a learner that is only a little better than a coin flip. AdaBoost makes it strong by asking it many questions in a row. Each example in the training set has a weight, and at the start all weights are equal. In each round, the weak learner builds a rule that does well on the weighted examples. Then AdaBoost makes the examples that this rule got wrong heavier, and the ones it got right lighter, so that the next rule must pay attention to the hard cases. At the end, all the rules vote. A rule that made fewer weighted mistakes gets a larger say in the vote. Even if each rule is weak, the vote becomes correct on all training examples after enough rounds.

## The problem

The input is a training set $S = ((x_1, y_1), \ldots, (x_n, y_n))$ with $x_i \in \mathbb{R}^d$ and labels $y_i \in \{-1, +1\}$, a number of rounds $T$, and a weak learner. Given a distribution $D$ on the indices $1, \ldots, n$, the weak learner returns a hypothesis $h : \mathbb{R}^d \to \{-1, +1\}$. Its weighted error is $\varepsilon = \sum_i D(i) [h(x_i) \ne y_i]$ and its edge is $\gamma = \frac12 - \varepsilon$. The output is a classifier $H$ for binary [classification](/classification/). The training error bound below holds for every training set, with no assumption on how it was drawn. To say anything about the error on new data, assume that the examples are drawn i.i.d. from an unknown distribution $D$ over $\mathbb{R}^d \times \{-1, +1\}$, with the 0-1 loss.

## The algorithm

```pseudo id=main
ADABOOST(S = ((x_1, y_1), .., (x_n, y_n)), T, WEAK-LEARNER)
L1  for i ← 1 to n do D_1(i) ← 1/n
L2  for t ← 1 to T do
L3      h_t ← WEAK-LEARNER(S, D_t)
L4      ε_t ← Σ_i D_t(i) · [h_t(x_i) ≠ y_i]
L5      if ε_t ≥ 1/2 then stop the loop and keep rounds 1 .. t − 1
L6      if ε_t = 0 then return h_t
L7      α_t ← ½ ln((1 − ε_t) / ε_t)
L8      for i ← 1 to n do D_{t+1}(i) ← D_t(i) · exp(−α_t y_i h_t(x_i))
L9      Z_t ← Σ_i D_{t+1}(i); divide each D_{t+1}(i) by Z_t
L10 return H(x) = sign(Σ_t α_t h_t(x))
```

Line L8 multiplies the weight of a correct example by $e^{-\alpha_t}$ and the weight of a wrong one by $e^{\alpha_t}$. With $\alpha_t$ of line L7, the new weights split in two equal halves: after line L9 the correct examples hold total weight $\frac12$ and the wrong ones hold $\frac12$. So the wrong examples of round $t$ get weight $D_t(i)/(2\varepsilon_t)$ and the correct ones get $D_t(i)/(2(1 - \varepsilon_t))$. Line L5 stops when the weak learner has no edge. Line L6 handles a perfect hypothesis, where $\alpha_t$ would be infinite. A weak learner that can also return the negation $-h$ never has $\varepsilon_t > \frac12$, since one of $h$ and $-h$ has error at most $\frac12$.

The weak learner of the code is the stump of least weighted error. A stump $(f, \theta, s)$ predicts $s$ when $x_f > \theta$ and $-s$ otherwise. For each feature, one sweep over the sorted values tries every threshold between two distinct values and both signs.

## Example

Take ten points on a line, $x = 1, 2, \ldots, 10$, with labels $+ + - - - + + + - -$. No single stump is right on more than 7 points, so no single stump has error below $0.3$. The table runs AdaBoost with stumps. The stump "$x > \theta$ gives $s$" is written $(\theta, s)$, and ties go to the first threshold found.

| round $t$ | stump | wrong points | $\varepsilon_t$ | $\alpha_t$ | $Z_t$ | training error | $\prod Z_s$ | $\exp(-2\sum \gamma_s^2)$ |
|---|---|---|---|---|---|---|---|---|
| 1 | $(2.5, -)$ | 6, 7, 8 | $3/10$ | 0.4236 | 0.9165 | 0.3 | 0.9165 | 0.9231 |
| 2 | $(8.5, -)$ | 3, 4, 5 | $3/14$ | 0.6496 | 0.8207 | 0.3 | 0.7521 | 0.7841 |
| 3 | $(5.5, +)$ | 1, 2, 9, 10 | $2/11$ | 0.7520 | 0.7714 | 0 | 0.5802 | 0.6403 |

After round 1 the three wrong points get weight $0.1/(2 \cdot 0.3) = 1/6$ each, and the seven correct points get $0.1/(2 \cdot 0.7) = 1/14$ each. The stump of round 2 says $+$ for $x \le 8.5$. It is wrong on points 3, 4 and 5, which now weigh only $3/14$ in total. After round 3 the score $F(x) = \sum_t \alpha_t h_t(x)$ is $0.321$ on points 1 and 2, $-0.526$ on points 3 to 5, $0.978$ on points 6 to 8 and $-0.321$ on points 9 and 10. Its sign is right on all ten points. In each round the training error is below $\prod Z_s$, and $\prod Z_s$ is below $\exp(-2\sum \gamma_s^2)$.

## Correctness

AdaBoost is a heuristic for the test error, but it has an exact guarantee on the training error.

**Theorem (Freund and Schapire 1997).** If AdaBoost runs $T$ rounds with $0 < \varepsilon_t < \frac12$ and $\gamma_t = \frac12 - \varepsilon_t$, then

$$\frac1n \left|\{i : H(x_i) \ne y_i\}\right| \le \prod_{t=1}^{T} 2\sqrt{\varepsilon_t (1 - \varepsilon_t)} = \prod_{t=1}^{T} \sqrt{1 - 4\gamma_t^2} \le \exp\left(-2\sum_{t=1}^{T} \gamma_t^2\right).$$

The key fact is the form of the weights after $T$ rounds: $D_{T+1}(i) = \exp(-y_i F_T(x_i)) / (n \prod_t Z_t)$ with $F_T = \sum_t \alpha_t h_t$. These weights sum to 1, and $\exp(-y_i F_T(x_i)) \ge 1$ on each training mistake. So the training error is at most $\prod_t Z_t$. The choice of $\alpha_t$ minimizes $Z_t = (1 - \varepsilon_t)e^{-\alpha} + \varepsilon_t e^{\alpha}$, with the minimum $2\sqrt{\varepsilon_t(1 - \varepsilon_t)}$. If every edge is at least $\gamma > 0$, the training error is 0 after $T > \ln(n)/(2\gamma^2)$ rounds. The full proof is below.

### The exponential loss view

Friedman, Hastie and Tibshirani (2000) showed that AdaBoost is forward stagewise additive modeling with the exponential loss $\ell(y, F(x)) = \exp(-y F(x))$. In round $t$, among all terms $\alpha h$ with $\alpha > 0$, the term that most reduces $\sum_i \exp(-y_i (F_{t-1}(x_i) + \alpha h(x_i)))$ is a hypothesis $h$ of least weighted error under $D_t$, with $\alpha = \alpha_t$. The weights $D_t(i)$ are the normalized losses $\exp(-y_i F_{t-1}(x_i))$. The minimizer of the expected exponential loss at a point $x$ is $F^*(x) = \frac12 \ln(\Pr[y = 1 \mid x] / \Pr[y = -1 \mid x])$, half the log-odds. This view links AdaBoost to [logistic regression](/logistic-regression/), and it leads to [gradient boosting](/gradient-boosting/) with other losses.

## Complexity

Count the operations in $n$, $d$ and $T$. Lines L4, L8 and L9 take $\Theta(n)$ time per round, plus one evaluation of $h_t$ on each example. The weak learner dominates. For stumps, sort each feature once at the start, in $O(d n \log n)$ time. Then each round sweeps each feature in the sorted order and updates the error in $O(1)$ per point, so a round costs $O(d n)$. The total time is $O(d n \log n + T d n)$ in the worst case. The sorted orders take $\Theta(d n)$ memory, the weights $\Theta(n)$ and the model $\Theta(T)$. To classify a new point costs $O(T)$ stump evaluations. The code of this page sorts again in each round for clarity, so it takes $O(T d n \log n)$ time.

## Properties

- **Adaptive.** AdaBoost needs no bound on the edges in advance. A round with a larger edge gets a larger $\alpha_t$ and reduces the bound more.
- **Deterministic.** With a deterministic weak learner, the output is a function of the training set. Some weak learners sample from $D_t$ instead of using the weights; then the output is random.
- **No zero error in one round.** By line L9, the hypothesis $h_t$ has weighted error exactly $\frac12$ under $D_{t+1}$. So round $t + 1$ never picks $h_t$ again with a positive edge, but a later round can.
- **Margins grow after the training error is 0.** The bound of the theorem also holds for the fraction of examples with normalized margin $y_i F(x_i) / \sum_t \alpha_t$ at most $\theta$, with a factor $2^T \prod_t \sqrt{\varepsilon_t^{1-\theta}(1 - \varepsilon_t)^{1+\theta}}$ in place of $\prod_t Z_t$. This is why the test error often keeps falling after the training error is 0; see the [margin generalization bound](/margin-generalization-bound/).
- **Noise sensitivity.** Each round multiplies the weight of a mislabeled example by $e^{\alpha_t} > 1$ whenever the weak hypothesis gives it the true label, so these examples take a large part of the weight. Dietterich (2000) observed that with added label noise, bagging often beat AdaBoost on decision trees. Long and Servedio (2010) proved that every boosting algorithm that minimizes a convex potential, AdaBoost included, can fail under random classification noise on some data, where a noise-tolerant booster succeeds.

## Variants and improvements

- **Real AdaBoost.** The weak hypothesis returns a real number whose sign is the class and whose size is the confidence. Schapire and Singer (1999) choose each round to minimize $Z_t$ directly.
- **LogitBoost and gradient boosting.** Replace the exponential loss with the [logistic loss](/logistic-loss/), which grows only linearly for large negative margins. Friedman, Hastie and Tibshirani (2000) fit it by Newton steps. [Gradient boosting](/gradient-boosting/) does the same for any differentiable loss.
- **SAMME for $k$ classes.** Zhu, Zou, Rosset and Hastie (2009) use $\alpha_t = \ln((1 - \varepsilon_t)/\varepsilon_t) + \ln(k - 1)$, multiply the weight of each wrong example by $e^{\alpha_t}$, and predict $\arg\max_c \sum_t \alpha_t [h_t(x) = c]$. It needs only $\varepsilon_t < 1 - 1/k$, which is better than random guessing among $k$ classes. For $k = 2$ it is AdaBoost with each $\alpha_t$ doubled, which gives the same vote. See [multiclass classification](/multiclass-classification/) for the other ways to reduce $k$ classes to two.
- **Shrinkage and early stopping.** Multiply each $\alpha_t$ by a factor $\nu < 1$, and choose $T$ on held-out data. This often lowers the test error, at the cost of more rounds.

## When to use it

Use AdaBoost with shallow trees or stumps on clean data of moderate size, when you want a simple method with few parameters and a proof for the training error. Its only parameters are $T$ and the weak learner. On data with label noise or many outliers, prefer a booster with a bounded or linear-tail loss, such as [gradient boosting](/gradient-boosting/) with the logistic loss, or [bagging](/bagging/), which does not concentrate weight on hard examples.

## Pitfalls

- **Taking $\alpha_t$ with the wrong sign or base.** Line L7 is $\frac12 \ln((1 - \varepsilon_t)/\varepsilon_t)$ with the natural logarithm. With $\ln(\varepsilon_t / (1 - \varepsilon_t))$ the update raises the weight of correct examples, and the training error grows.
- **Forgetting the normalization in line L9.** Without it the weights shrink or grow without bound, $\varepsilon_t$ is no longer a weighted error, and $\alpha_t$ is wrong.
- **Not handling $\varepsilon_t = 0$ or $\varepsilon_t \ge \frac12$.** Line L7 divides by zero when $\varepsilon_t = 0$, and gives $\alpha_t \le 0$ when $\varepsilon_t \ge \frac12$. Lines L5 and L6 must come first.
- **Ties at $F(x) = 0$.** A score of exactly 0 must count as a mistake in a test of the bound, because the proof uses $\exp(-y F) \ge 1$ only for $y F \le 0$.
- **Reading the bound as a test error bound.** The theorem is about the training set. The error on new data needs a capacity argument, by the [VC dimension](/vc-dimension/) of weighted votes or by margins, and it holds only with high probability over an i.i.d. sample.

## Implementations

## History

Schapire (1990) and Freund (1995) gave the first boosting algorithms, which needed a known lower bound on the edge; the question they answered is on the page on [weak learnability](/weak-learnability-equivalence/). Freund and Schapire presented AdaBoost, which adapts to the edges, at EuroCOLT 1995, and the journal version appeared in 1997. Schapire and Singer (1999) gave the form with labels in $\{-1, +1\}$ and the analysis by the normalizers $Z_t$ used here. Friedman, Hastie and Tibshirani (2000) gave the exponential loss view, and Zhu, Zou, Rosset and Hastie (2009) gave SAMME for many classes.

## References
