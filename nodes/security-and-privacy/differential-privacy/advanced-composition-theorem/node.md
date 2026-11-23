---
tag: 0CAVYC
kind: theorem
slug: advanced-composition-theorem
name: Advanced composition theorem
aliases:
- strong composition theorem
- Dwork-Rothblum-Vadhan composition
area: security-and-privacy/differential-privacy
level: core
summary: "k-fold adaptive composition of (epsilon, delta)-DP mechanisms is (epsilon', k delta + delta')-DP with epsilon' = epsilon sqrt(2k ln(1/delta')) + k epsilon (e^epsilon - 1), so loss grows as sqrt(k)."
history:
  year: 2010
  people: [Cynthia Dwork, Guy N. Rothblum, Salil Vadhan]
  note: "Dwork, Rothblum and Vadhan proved the bound in their FOCS 2010 paper on boosting, with the adaptive k-fold composition experiment that later work uses."
prereqs: [sequential-composition-theorem, kullback-leibler-divergence, azuma-inequality]
see_also: [sequential-composition-theorem, optimal-composition-theorem, privacy-loss-random-variable, renyi-differential-privacy, zero-concentrated-differential-privacy, total-variation-distance, martingale, dp-sgd]
sources:
  - paper: doi:10.1109/FOCS.2010.12
    title: "Cynthia Dwork, Guy N. Rothblum and Salil Vadhan, Boosting and differential privacy, FOCS 2010, pages 51 to 60"
    locator: "the k-fold adaptive composition experiment and the composition theorem"
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), pages 211 to 407, 2014"
    locator: "Section 3.5.1, Lemma 3.17 (approximate max divergence as a statistical distance plus a max divergence), Lemma 3.18 (the KL bound) and Lemma 3.19 (Azuma); Section 3.5.2, Definition 3.7, Theorem 3.20 and its proof, and Corollary 3.21"
  - paper: doi:10.1109/TIT.2017.2685505
    title: "Peter Kairouz, Sewoong Oh and Pramod Viswanath, The composition theorem for differential privacy, IEEE Transactions on Information Theory 63(6), pages 4037 to 4049, 2017"
    locator: "the optimal composition theorem, which shows how far the bound is from exact"
---

The advanced composition theorem shows that the privacy loss of many private steps grows like the square root of their number, not linearly, if you accept a small failure probability. For $k$ mechanisms that are each $(\varepsilon, \delta)$-differentially private, chosen adaptively, and for any $\delta' > 0$, the composition is $(\varepsilon', k\delta + \delta')$-DP with

$$\varepsilon' = \sqrt{2k \ln(1/\delta')}\,\varepsilon + k\varepsilon(e^{\varepsilon} - 1).$$

For small $\varepsilon$ the second term is about $k\varepsilon^2$, and $\varepsilon'$ is about $\varepsilon\sqrt{2k\ln(1/\delta')}$. The [basic composition theorem](/sequential-composition-theorem/) gives $k\varepsilon$ instead. With $k = 100$ steps of $\varepsilon = 0.1$ and $\delta' = 10^{-6}$, the bound is $6.3082$ against 10. The proof views the total [privacy loss](/privacy-loss-random-variable/) as a sum of bounded terms with a small mean and applies the [Azuma inequality](/azuma-inequality/).

## Statement

Fix a symmetric neighbor relation. The **k-fold adaptive composition experiment** for a class $\mathcal F$ of mechanisms and an adversary $A$ runs, for a bit $b \in \{0, 1\}$, the steps $i = 1, \ldots, k$:

1. $A$ picks two neighboring datasets $x_i^0 \sim x_i^1$ and a mechanism $M_i \in \mathcal F$, as a function of its coins and of the outputs $y_1, \ldots, y_{i-1}$.
2. $A$ receives $y_i \sim M_i(x_i^b)$, with fresh coins.

Let $V^b$ be the view of $A$ (its coins and $y_1, \ldots, y_k$) in experiment $b$. The class $\mathcal F$ is $(\varepsilon', \delta')$-DP under $k$-fold adaptive composition if for every adversary $A$ and every event $S$, $\Pr[V^0 \in S] \le e^{\varepsilon'} \Pr[V^1 \in S] + \delta'$, and the same with $0$ and $1$ swapped. The case $x_i^b = x^b$ for all $i$ is the plain composition of $k$ mechanisms on one pair of neighbors.

**Theorem (Dwork, Rothblum and Vadhan 2010; Dwork-Roth Theorem 3.20).** For all $\varepsilon, \delta, \delta' \ge 0$, the class of $(\varepsilon, \delta)$-DP mechanisms is $(\varepsilon', k\delta + \delta')$-DP under $k$-fold adaptive composition, where

$$\varepsilon' = \sqrt{2k\ln(1/\delta')}\,\varepsilon + k\varepsilon(e^{\varepsilon} - 1).$$

**Corollary (Dwork-Roth Corollary 3.21).** For $0 < \varepsilon' < 1$ and $\delta' > 0$, it is enough that each step is $(\varepsilon, \delta)$-DP with $\varepsilon = \varepsilon' / (2\sqrt{2k\ln(1/\delta')})$ to get $(\varepsilon', k\delta + \delta')$-DP in total.

## In plain words

Each private answer moves the odds about one person up or down by a small amount. Basic composition assumes that every answer pushes the odds in the same direction by the full amount. That can happen, but it is very unlikely when there are many answers.

Most answers push the odds only a little, and some push them the other way. The pushes add up like the steps of a random walk. A random walk of many small steps usually ends near where its average drift takes it, plus a spread that grows like the square root of the number of steps.

So, except with a small probability that you choose, the total push stays far below the worst case. You pay for that small probability in the second privacy parameter.

## Proof

The proof below is full for $\delta = 0$. The extension to $\delta > 0$ is a marked sketch with the exact locator.

**Lemma 1 (KL bound).** Let $P, Q$ have densities $p, q$ with $|\ln(p/q)| \le \varepsilon$ everywhere. Then the [KL divergence](/kullback-leibler-divergence/) satisfies $D(P \| Q) \le \varepsilon(e^{\varepsilon} - 1)$.

*Proof.* Since $D(Q \| P) \ge 0$, we have $D(P \| Q) \le D(P\|Q) + D(Q\|P) = \int (p - q)\ln(p/q) \le \varepsilon \int |p - q|$. Let $S = \{p > q\}$, $a = P(S)$, $b = Q(S)$ and $t = a - b$, so $\int|p - q| = 2t$. The bound on the ratio gives $a \le e^{\varepsilon} b$ and $1 - b \le e^{\varepsilon}(1 - a)$. These say $t \le (e^{\varepsilon} - 1)b$ and $e^{\varepsilon} t \le (e^{\varepsilon} - 1)(1 - b)$. Adding them gives $t \le (e^{\varepsilon} - 1)/(e^{\varepsilon} + 1)$, which is the [total variation](/total-variation-distance/) bound. So $\varepsilon \int |p - q| \le 2\varepsilon(e^{\varepsilon} - 1)/(e^{\varepsilon} + 1) \le \varepsilon(e^{\varepsilon} - 1)$.

**Lemma 2 (tail to DP).** Let $L(v) = \ln(\Pr[V^0 = v]/\Pr[V^1 = v])$. If $\Pr[L(V^0) > \varepsilon'] \le \delta'$, then $\Pr[V^0 \in S] \le e^{\varepsilon'}\Pr[V^1 \in S] + \delta'$ for every $S$.

*Proof.* Let $B = \{v : L(v) > \varepsilon'\}$. Then $\Pr[V^0 \in S] \le \Pr[V^0 \in S \setminus B] + \Pr[V^0 \in B] \le e^{\varepsilon'}\Pr[V^1 \in S \setminus B] + \delta'$.

**The case $\delta = 0$.** Fix an adversary. The coins $r$ of $A$ have the same law in both experiments. Given $r$ and a prefix $y_1, \ldots, y_{i-1}$, the adversary's choices $x_i^0, x_i^1, M_i$ are fixed. So the log ratio splits into a sum:

$$L(r, y_1, \ldots, y_k) = \sum_{i=1}^k c_i, \qquad c_i = \ln\frac{\Pr[M_i(x_i^0) = y_i]}{\Pr[M_i(x_i^1) = y_i]}.$$

Run experiment 0 and condition on $r$ and the prefix. Then $|c_i| \le \varepsilon$, because $M_i$ is $\varepsilon$-DP, and $E[c_i \mid \text{past}] = D(M_i(x_i^0) \| M_i(x_i^1)) \le \beta$ with $\beta = \varepsilon(e^{\varepsilon} - 1)$, by Lemma 1. Let $Z_i = c_i - E[c_i \mid \text{past}]$. The $Z_i$ form a [martingale](/martingale/) difference sequence, and given the past, $Z_i$ lies in an interval of length $2\varepsilon$. The Azuma-Hoeffding inequality gives $\Pr[\sum_i Z_i \ge t] \le \exp(-2t^2/(k(2\varepsilon)^2))$. Take $t = \varepsilon\sqrt{2k\ln(1/\delta')}$. Then the bound is $\delta'$, and since $\sum_i c_i \le k\beta + \sum_i Z_i$,

$$\Pr\left[L > k\varepsilon(e^{\varepsilon} - 1) + \varepsilon\sqrt{2k\ln(1/\delta')}\right] \le \delta'.$$

Lemma 2 gives the inequality from experiment 0 to experiment 1. The class is closed under the swap of $x_i^0$ and $x_i^1$, so the same argument gives the other direction.

**The case $\delta > 0$ (sketch).** By Dwork-Roth Lemma 3.17, an $(\varepsilon, \delta)$-DP pair of output laws is within statistical distance $\delta$ of a pair of laws whose log ratio is bounded by $\varepsilon$. Replace each step by such a pair. By the triangle inequality for statistical distance, the view changes by at most $k\delta$. The $\delta = 0$ argument applies to the replaced experiment and gives $(\varepsilon', \delta')$, and the change of the view adds $k\delta$. The full proof is in Dwork and Roth, Section 3.5.2, in the proof of Theorem 3.20. $\blacksquare$

## Consequences

- **More queries for the same budget.** With a fixed total budget, each of $k$ queries can get noise for $\varepsilon \approx \varepsilon'/\sqrt{k}$ instead of $\varepsilon'/k$. Dwork and Roth use this to answer close to $n^2$ counting queries with error $o(n)$ on a dataset of size $n$.
- **Crossover with basic composition.** For $\varepsilon = 0.1$ and $\delta' = 10^{-6}$ the bound is below $k\varepsilon$ only for $k \ge 35$:

| $k$ | basic, $k\varepsilon$ | advanced, $\varepsilon'$ |
|---|---|---|
| 10 | 1.0 | 1.7674 |
| 20 | 2.0 | 2.5611 |
| 50 | 5.0 | 4.2428 |
| 100 | 10.0 | 6.3082 |
| 1000 | 100.0 | 27.1397 |

- **The first sqrt(k) accountant.** The analysis of private learning by many noisy steps, for example [DP-SGD](/dp-sgd/), first used this theorem. Abadi et al. (2016) showed that tracking the moments of the privacy loss gives much less; see the [moments accountant](/moments-accountant/).
- **A heuristic, not a theorem.** The simple form "$\varepsilon\sqrt{k}$" is only a guide. It drops the factor $\sqrt{2\ln(1/\delta')}$ and the term $k\varepsilon(e^{\varepsilon} - 1)$, and it is wrong when $\varepsilon$ is not small.

## Tightness

The square root growth cannot be removed. Take $k$ runs of [randomized response](/randomized-response/) with parameter $\varepsilon$. The privacy loss is $\varepsilon(2A - k)$ with $A$ binomial with $k$ trials and success probability $e^{\varepsilon}/(1 + e^{\varepsilon})$. Its mean is $k\varepsilon\tanh(\varepsilon/2) \approx k\varepsilon^2/2$, and its standard deviation is about $\varepsilon\sqrt{k}$. By the [central limit theorem](/central-limit-theorem/), the $\varepsilon'$ needed for a fixed small $\delta'$ grows like $\varepsilon\sqrt{k}$ times a factor that grows with $\ln(1/\delta')$.

The constants are not exact. For $k = 100$, $\varepsilon = 0.1$ and total $\delta = 10^{-6}$, the exact optimum of Kairouz, Oh and Viswanath is $\varepsilon' = 4.7746$, against the bound $6.3082$. The [optimal composition theorem](/optimal-composition-theorem/) gives the exact value for every $k$. The term $k\delta$ is needed up to second-order terms: the example in the Tightness section of the [basic composition](/sequential-composition-theorem/) page loses $1 - (1 - \delta)^k$.

## History

Dwork, Rothblum and Vadhan (2010) proved the theorem in a paper on boosting for queries. They also set up the adaptive experiment above, in which an adversary picks the datasets and the mechanisms one step at a time, and showed that the bound holds there. Dwork and Roth (2014) give it as Theorem 3.20, with the proof through the KL bound and Azuma's inequality. Kairouz, Oh and Viswanath (2015) found the exact optimum for identical steps, and Murtagh and Vadhan (2016) showed that the exact optimum for different steps is hard to compute. Later work moved to divergences that compose by a plain sum, such as [Renyi DP](/renyi-differential-privacy/) and [zCDP](/zero-concentrated-differential-privacy/), and to numerical accountants.

## References
