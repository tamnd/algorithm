---
tag: B8ZFXM
kind: theorem
slug: cover-hart-theorem
name: Cover-Hart theorem
aliases:
- nearest neighbor error bound
- Cover-Hart inequality
- Cover and Hart bound
area: machine-learning/supervised-learning
level: advanced
summary: "As the sample grows, the 1-nearest-neighbor error R satisfies R* ≤ R ≤ R*(2 - M R*/(M - 1)) for M classes, so it is at most twice the Bayes error R*."
prereqs: [k-nearest-neighbors, bayes-optimal-classifier]
see_also: [k-nearest-neighbors, bayes-optimal-classifier, metric-space, jensens-inequality, curse-of-dimensionality, classification]
sources:
  - paper: doi:10.1109/TIT.1967.1053964
    title: Thomas M. Cover and Peter E. Hart, Nearest neighbor pattern classification, IEEE Transactions on Information Theory 13(1), 1967
    locator: pp. 21 to 27 (the lemma on the convergence of the nearest neighbor, Theorem 1 for two classes, its extension to M classes, and the k-NN rule)
  - paper: "Luc Devroye, On the inequality of Cover and Hart in nearest neighbor discrimination, IEEE Transactions on Pattern Analysis and Machine Intelligence 3(1), 1981"
    locator: the bound for all distributions on R^d, without continuity conditions
  - book: isbn:9780387946184
    title: Luc Devroye, László Györfi and Gábor Lugosi, A Probabilistic Theory of Pattern Recognition, Springer, 1996
    locator: Chapter 5 (nearest neighbor rules, the asymptotic 1-NN error E[2η(X)(1 - η(X))] and its bounds)
  - book: isbn:9780471056690
    title: Richard O. Duda, Peter E. Hart and David G. Stork, Pattern Classification, second edition, Wiley, 2001
    locator: Section 4.5 (the nearest neighbor rule, its error rate and the error bounds)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Chapter 19, Section 19.2 (a finite sample bound for 1-NN when η is Lipschitz on the unit cube)
---

The Cover-Hart theorem compares the error of the 1-nearest neighbor rule with the best possible error. As the number of training examples $n \to \infty$, the error $R$ of [1-NN](/k-nearest-neighbors/) satisfies $R^\ast \le R \le R^\ast (2 - M R^\ast/(M - 1))$, where $R^\ast$ is the [Bayes risk](/bayes-optimal-classifier/) and $M$ is the number of classes. For two classes this is $R \le 2R^\ast(1 - R^\ast) \le 2R^\ast$. Cover and Hart proved it in 1967 for a separable metric space, under a mild continuity condition.

## Statement

**Setting.** Let $(\mathcal{X}, \rho)$ be a separable [metric space](/metric-space/) and let the classes be $\{1, \ldots, M\}$ with $M \ge 2$. The pair $(X, Y)$ has prior probabilities $\pi_i = \Pr[Y = i]$ and class conditional densities $f_i$ with respect to a common measure on $\mathcal{X}$, so that the posterior is
$$ \eta_i(x) = \Pr[Y = i \mid X = x] = \frac{\pi_i f_i(x)}{\sum_{j} \pi_j f_j(x)}. $$
The training set $(X_1, Y_1), \ldots, (X_n, Y_n)$ is i.i.d. with the law of $(X, Y)$ and is independent of $(X, Y)$. Let $X'_n$ be the training point nearest to $X$, with ties broken by any rule that does not look at the labels, and let $Y'_n$ be its label. The 1-NN rule predicts $Y'_n$, and its risk under the 0-1 loss is $R_n = \Pr[Y'_n \ne Y]$, over the training set and the test pair. The Bayes risk is $R^\ast = \mathbb{E}[1 - \max_i \eta_i(X)]$.

**Theorem (Cover and Hart 1967).** Assume that, with probability one, $X$ is either

1. a point of continuity of each of $f_1, \ldots, f_M$, or
2. a point of nonzero probability, $\Pr[X = x] > 0$.

Then the limit $R = \lim_{n \to \infty} R_n$ exists and equals $\mathbb{E}\big[1 - \sum_{i=1}^M \eta_i(X)^2\big]$, and
$$ R^\ast \le R \le R^\ast \left(2 - \frac{M}{M - 1} R^\ast\right). $$
For $M = 2$ this is Theorem 1 of the paper: $R^\ast \le R \le 2R^\ast(1 - R^\ast)$. Both bounds are attained, for each value of $R^\ast$ in $[0, (M - 1)/M]$.

## In plain words

Even with endless data, no rule can beat the best rule that knows the true probabilities of the classes, because some inputs are truly ambiguous. The theorem says that the simplest rule, "copy the label of the closest stored example", comes close to that best rule. With very much data, its error is at most about twice the best error. When the best error is small, the closest example is almost always right. The price of copying one neighbor is that its label is itself a random draw, so two random draws must agree, and that happens a little less often than the best guess is right.

## Proof

We use the notation of the statement and write $\mu$ for the law of $X$. The proof has three steps: the nearest neighbor converges to $X$, the conditional risk converges, and an inequality on the posteriors bounds the limit.

**Lemma 1 (the nearest neighbor converges).** With probability one, $\rho(X'_n, X) \to 0$.

*Proof.* Let $B(x, r)$ be the open ball, and let $S$ be the set of points $x$ with $\mu(B(x, r)) > 0$ for each $r > 0$. First, $\mu(S) = 1$. Let $\{z_1, z_2, \ldots\}$ be a countable dense set. If $x \notin S$, then $\mu(B(x, r)) = 0$ for some $r > 0$. Choose $z_j$ with $\rho(x, z_j) < r/3$ and a rational $q$ with $r/3 < q < 2r/3$. Then $x \in B(z_j, q) \subseteq B(x, r)$, so $\mu(B(z_j, q)) = 0$. So the complement of $S$ is covered by countably many balls $B(z_j, q)$ of measure 0, and has measure 0. Second, fix $x \in S$ and $r > 0$. The event $\rho(X'_n, x) \ge r$ means that no training point is in $B(x, r)$, so its probability is $(1 - \mu(B(x, r)))^n \to 0$. The distance $\rho(X'_n, x)$ does not increase with $n$, so its limit $L$ exists, and $\Pr[L \ge r] \le (1 - \mu(B(x, r)))^n$ for each $n$, so $\Pr[L \ge r] = 0$. Taking $r = 1, 1/2, 1/3, \ldots$ gives $L = 0$ with probability one. Since $X$ is independent of the training set and $\mu(S) = 1$, the same holds for the random point $X$. $\square$

**Lemma 2 (the conditional risk).** Given $X = x$ and $X'_n = x'$, the labels $Y$ and $Y'_n$ are independent, and
$$ \Pr[Y'_n \ne Y \mid X = x, X'_n = x'] = 1 - \sum_{i=1}^M \eta_i(x)\, \eta_i(x'). $$

*Proof.* The index of the nearest neighbor is a function of $X, X_1, \ldots, X_n$ and of a tie rule that does not use the labels. Given all the points, the labels $Y, Y_1, \ldots, Y_n$ are independent, and $Y_j$ has the law $\eta(X_j)$, because the pairs are independent. So given $X = x$ and $X'_n = x'$, $Y$ has the law $\eta(x)$ and $Y'_n$ has the law $\eta(x')$, independently. The labels agree with probability $\sum_i \eta_i(x)\eta_i(x')$. $\square$

**Step 3 (the limit).** Let $x$ satisfy condition 1 or 2, and $\sum_j \pi_j f_j(x) > 0$. The set where the mixture density is 0 has probability 0, so this holds for $X$ with probability one.

- Under condition 1, each $\eta_i$ is a ratio of functions that are continuous at $x$, with a denominator that is not 0 at $x$. So $\eta_i$ is continuous at $x$, and Lemma 1 gives $\eta_i(X'_n) \to \eta_i(x)$ with probability one.
- Under condition 2, the probability that no training point equals $x$ is $(1 - \mu(\{x\}))^n \to 0$, and these events decrease in $n$. So with probability one some training point equals $x$ from some $n$ on. Then the nearest distance is 0, and in a metric space distance 0 means $X'_n = x$. So $\eta_i(X'_n) = \eta_i(x)$ for all large $n$.

By Lemma 2, the conditional risk $r_n = 1 - \sum_i \eta_i(X)\eta_i(X'_n)$ converges with probability one to
$$ r(X) = 1 - \sum_{i=1}^M \eta_i(X)^2. $$
Since $0 \le r_n \le 1$, the dominated convergence theorem gives $R_n = \mathbb{E}[r_n] \to \mathbb{E}[r(X)] = R$.

**Step 4 (the bounds at one point).** Fix $x$, write $\eta_i = \eta_i(x)$, let $j$ be an index of a largest $\eta_i$, and let $r^\ast(x) = 1 - \eta_j$ be the conditional Bayes risk at $x$.

- *Lower bound.* $\sum_i \eta_i^2 \le \eta_j \sum_i \eta_i = \eta_j$, so $r(x) \ge 1 - \eta_j = r^\ast(x)$.
- *Upper bound.* The other $M - 1$ posteriors sum to $r^\ast(x)$. By the Cauchy-Schwarz inequality, $\sum_{i \ne j} \eta_i^2 \ge r^\ast(x)^2/(M - 1)$. So
$$ r(x) \le 1 - (1 - r^\ast(x))^2 - \frac{r^\ast(x)^2}{M - 1} = 2 r^\ast(x) - \frac{M}{M - 1}\, r^\ast(x)^2. $$

**Step 5 (take expectations).** The lower bound gives $R = \mathbb{E}[r(X)] \ge \mathbb{E}[r^\ast(X)] = R^\ast$. For the upper bound, $\mathbb{E}[r^\ast(X)^2] \ge (\mathbb{E}[r^\ast(X)])^2 = (R^\ast)^2$, because the variance of $r^\ast(X)$ is not negative ([Jensen's inequality](/jensens-inequality/)). So
$$ R \le 2R^\ast - \frac{M}{M - 1}\mathbb{E}[r^\ast(X)^2] \le 2R^\ast - \frac{M}{M - 1}(R^\ast)^2 = R^\ast\left(2 - \frac{M}{M - 1}R^\ast\right). $$

**The two-class case in one line.** For $M = 2$, write $\eta = \eta_1(x)$. Then $r(x) = 1 - \eta^2 - (1 - \eta)^2 = 2\eta(1 - \eta)$ and $r^\ast(x) = \min(\eta, 1 - \eta)$, so $r(x) = 2 r^\ast(x)(1 - r^\ast(x))$ exactly. Taking expectations,
$$ R = 2R^\ast(1 - R^\ast) - 2\operatorname{Var}(r^\ast(X)). $$
This gives $R \le 2R^\ast(1 - R^\ast)$ at once. It also gives $R \ge R^\ast$, because $2r^\ast(1 - r^\ast) \ge r^\ast$ when $r^\ast \le 1/2$, and $r^\ast(x) \le 1/2$ for two classes. $\blacksquare$

## Consequences

- **Half the information is in one neighbor.** Since $R \le 2R^\ast$, the label of the single nearest neighbor of an infinite sample is worth at least half of what full knowledge of the posterior is worth, in this sense. Cover and Hart made this remark in their paper.
- **The noise-free case.** If $R^\ast = 0$ then $R = 0$: with deterministic labels, 1-NN is asymptotically perfect.
- **1-NN is not consistent.** For two classes, $R = R^\ast$ only when $r^\ast(X) \in \{0, 1/2\}$ with probability one. Otherwise $R > R^\ast$, even with infinite data. To reach $R^\ast$ the number of neighbors $k$ must grow, with $k/n \to 0$, as in Stone's theorem on the [k-nearest neighbors](/k-nearest-neighbors/) page.
- **An interval for the Bayes risk.** For two classes, solving $R \le 2R^\ast(1 - R^\ast)$ for $R^\ast$ gives $\frac{1}{2}\big(1 - \sqrt{1 - 2R}\big) \le R^\ast \le R$. A good estimate of the 1-NN error on a large sample thus brackets the best possible error. For $R = 1/3$ the interval is $[0.2113, 0.3333]$.
- **A worked example.** Let $X$ be uniform on $[0, 1]$ and $\eta_1(x) = x$, with two classes. Then $R^\ast = \mathbb{E}[\min(X, 1 - X)] = 1/4$, $R = \mathbb{E}[2X(1 - X)] = 1/3$, and the upper bound is $2 \cdot \frac14 \cdot \frac34 = 3/8$. The density is continuous on $(0, 1)$, so the theorem applies. In a simulation with seed 1, five training sets of size $n$ and 20000 test points each gave a mean 1-NN error of 0.3379 for $n = 100$, 0.3337 for $n = 1000$ and 0.3331 for $n = 10000$.
- **A three-class example with atoms.** Let $X$ take three values with probability $1/3$ each, with posteriors $(0.7, 0.2, 0.1)$, $(0.2, 0.6, 0.2)$ and $(1/3, 1/3, 1/3)$. Then $R^\ast = 41/90 \approx 0.4556$, $R = 253/450 \approx 0.5622$, and the bound is $3239/5400 \approx 0.5998$, below $2R^\ast \approx 0.9111$. Condition 2 holds at each point. Over 4000 training sets of size 50 (seed 2), the mean exact risk of the trained 1-NN rule was within 0.01 of $253/450$.
- **No rate.** The theorem is a limit and gives no rate of convergence. With no condition on the distribution, the convergence of $R_n$ can be arbitrarily slow (Devroye, Györfi and Lugosi). When $\mathcal{X} = [0, 1]^d$ and $\eta$ is $c$-Lipschitz, Shalev-Shwartz and Ben-David prove $\mathbb{E}[R_n] \le 2R^\ast + 4c\sqrt{d}\, n^{-1/(d+1)}$ for two classes, and the exponent $1/(d+1)$ is one form of the [curse of dimensionality](/curse-of-dimensionality/).
- **The k-NN rule for fixed k.** Cover and Hart also treat the k-NN rule with $k$ fixed. Its asymptotic risk $R_k$ lies between $R^\ast$ and the 1-NN limit for two classes and odd $k$, and decreases toward $R^\ast$ as $k$ grows.

## Tightness

Both bounds are attained, for each value of the Bayes risk.

- **Upper bound.** Fix $R^\ast \in [0, (M - 1)/M]$ and let the posterior be the same at every $x$: $\eta = (1 - R^\ast, \frac{R^\ast}{M - 1}, \ldots, \frac{R^\ast}{M - 1})$. Then the Cauchy-Schwarz step is an equality, because the other posteriors are equal, and the Jensen step is an equality, because $r^\ast(X)$ is constant. So $R = R^\ast(2 - M R^\ast/(M - 1))$. For two classes with $\eta \equiv 0.7$, $R^\ast = 0.3$ and $R = 2 \cdot 0.3 \cdot 0.7 = 0.42$.
- **Lower bound.** $R = R^\ast$ exactly when, with probability one, the posterior at $X$ is either a unit vector or the uniform vector $(1/M, \ldots, 1/M)$, because these are the cases of equality in $\sum_i \eta_i^2 \le \max_i \eta_i$. For example, with half the mass noise free and half uniform over three classes, $R = R^\ast = 1/3$.
- **The factor 2.** As $R^\ast \to 0$, the upper bound is $2R^\ast - O((R^\ast)^2)$, so no constant smaller than 2 works in a bound of the form $R \le c R^\ast$.
- **The conditions.** Separability is used in Lemma 1. In $\mathbb{R}^d$ with the Euclidean distance, Devroye (1981) showed that the same limit and bounds hold for every distribution, with no continuity condition. In general separable metric spaces of infinite dimension, the consistency results for k-NN can fail, and extra conditions are needed.

## History

Fix and Hodges (1951) introduced nearest neighbor discrimination and proved the consistency of the k-NN rule when $k \to \infty$ and $k/n \to 0$. Thomas Cover and Peter Hart studied the opposite regime, with $k$ fixed, and published the bound for the 1-NN rule in the IEEE Transactions on Information Theory in January 1967. Their proof assumed a separable metric space and continuity of the class densities almost everywhere, or atoms. Devroye (1981) removed the continuity condition in $\mathbb{R}^d$. The theorem is the standard reason why 1-NN is a strong baseline when data is plentiful.

## References
