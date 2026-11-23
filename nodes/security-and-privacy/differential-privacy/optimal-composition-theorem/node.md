---
tag: D8BAGQ
kind: theorem
slug: optimal-composition-theorem
name: Optimal composition theorem
aliases:
- Kairouz-Oh-Viswanath composition
area: security-and-privacy/differential-privacy
level: research
summary: "Gives the exact set of (epsilon', delta') that k-fold adaptive composition of (epsilon, delta)-DP mechanisms satisfies, through a hypothesis testing view and one worst-case mechanism."
history:
  year: 2015
  people: [Peter Kairouz, Sewoong Oh, Pramod Viswanath]
  note: "Kairouz, Oh and Viswanath gave the exact region at ICML 2015, with the journal version in IEEE Transactions on Information Theory in 2017. Murtagh and Vadhan showed in 2016 that the case of different epsilons is #P-complete."
prereqs: [advanced-composition-theorem, neyman-pearson-lemma, type-i-and-type-ii-errors]
see_also: [sequential-composition-theorem, advanced-composition-theorem, privacy-loss-random-variable, gaussian-differential-privacy, numerical-privacy-accounting, randomized-response, binomial-distribution, counting-problem]
sources:
  - paper: doi:10.1109/TIT.2017.2685505
    title: "Peter Kairouz, Sewoong Oh and Pramod Viswanath, The composition theorem for differential privacy, IEEE Transactions on Information Theory 63(6), pages 4037 to 4049, 2017"
    locator: "the hypothesis testing view of DP, the worst-case mechanism and the optimal composition theorem; this page relies on the journal version"
  - url: "https://proceedings.mlr.press/v37/kairouz15.html"
    title: "Peter Kairouz, Sewoong Oh and Pramod Viswanath, The composition theorem for differential privacy, ICML 2015, PMLR 37"
    locator: "the conference version of the same results"
  - paper: doi:10.1007/978-3-662-49096-9_7
    title: "Jack Murtagh and Salil Vadhan, The complexity of computing the optimal composition of differential privacy, TCC 2016-A, LNCS 9562, pages 157 to 175"
    locator: "the formula for different (epsilon_i, delta_i), the #P-completeness result and the polynomial time approximation"
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), pages 211 to 407, 2014"
    locator: "Section 3.5.2, Definition 3.7 (k-fold adaptive composition), which this page uses"
---

The optimal composition theorem gives the exact privacy of $k$ private steps. For $k$ mechanisms that are each $(\varepsilon, \delta)$-differentially private, chosen adaptively, Kairouz, Oh and Viswanath found the full set of pairs $(\varepsilon', \delta')$ for which the composition is $(\varepsilon', \delta')$-DP, and showed that no smaller set is true. The key idea is the hypothesis testing view of privacy: a mechanism is $(\varepsilon, \delta)$-DP exactly when no test that tries to tell two neighbors apart from the output does too well, as in the [Neyman-Pearson lemma](/neyman-pearson-lemma/). One simple mechanism, a four-output version of [randomized response](/randomized-response/), is the worst case for this test, so the composition of $k$ copies of it gives the exact answer. The [basic](/sequential-composition-theorem/) and [advanced](/advanced-composition-theorem/) composition theorems are upper bounds on this exact value.

## Statement

Fix a symmetric neighbor relation, and use the $k$-fold adaptive composition experiment of the [advanced composition](/advanced-composition-theorem/) page, in which an adversary picks each pair of neighbors and each mechanism after it sees the earlier outputs.

**The worst-case pair.** For $\varepsilon \ge 0$ and $\delta \in [0, 1]$, let $\tilde P_{\varepsilon,\delta}$ and $\tilde Q_{\varepsilon,\delta}$ be the laws on the outputs $\{0, 1, 2, 3\}$ with

$$\tilde P = \left(\delta,\ \frac{(1-\delta)e^{\varepsilon}}{1+e^{\varepsilon}},\ \frac{1-\delta}{1+e^{\varepsilon}},\ 0\right), \qquad \tilde Q = \left(0,\ \frac{1-\delta}{1+e^{\varepsilon}},\ \frac{(1-\delta)e^{\varepsilon}}{1+e^{\varepsilon}},\ \delta\right).$$

**Theorem (Kairouz, Oh and Viswanath).** For all $\varepsilon \ge 0$, $\delta \in [0, 1]$, $k \ge 1$ and $\varepsilon' \ge 0$, the class of $(\varepsilon, \delta)$-DP mechanisms is $(\varepsilon', \delta')$-DP under $k$-fold adaptive composition if and only if $\delta' \ge \delta_k(\varepsilon')$, where

$$\delta_k(\varepsilon') = 1 - (1-\delta)^k + \frac{(1-\delta)^k}{(1+e^{\varepsilon})^k}\sum_{a=0}^{k}\binom{k}{a}\max\left(0,\ e^{a\varepsilon} - e^{\varepsilon'}e^{(k-a)\varepsilon}\right).$$

At the points $\varepsilon' = (k - 2i)\varepsilon$, for $i = 0, 1, \ldots, \lfloor k/2 \rfloor$, the sum is $\sum_{l=0}^{i-1}\binom{k}{l}\left(e^{(k-l)\varepsilon} - e^{(k-2i+l)\varepsilon}\right)$, which is the form in the paper. The bound is reached by $k$ independent copies of the pair $(\tilde P, \tilde Q)$.

**Different parameters (Murtagh and Vadhan).** For steps with parameters $(\varepsilon_i, \delta_i)$, the exact value is $1 - \prod_i(1-\delta_i)\left(1 - \frac{1}{\prod_i(1+e^{\varepsilon_i})}\sum_{S \subseteq [k]}\max\left(0, e^{\sum_{i \in S}\varepsilon_i} - e^{\varepsilon'}e^{\sum_{i \notin S}\varepsilon_i}\right)\right)$. Computing it exactly is #P-complete, and it can be approximated to any accuracy in polynomial time.

## In plain words

Think of an observer who sees all the outputs and must guess which of two neighboring datasets was used. A private mechanism is one for which every guessing rule makes many mistakes of one kind or the other.

Among all mechanisms with the same privacy level, one simple mechanism is the easiest to guess from. It sometimes tells the truth outright, and otherwise answers with a biased coin. Any other mechanism with the same level gives the observer less help than this one.

So, to know how much $k$ answers reveal in the worst case, you only need to study $k$ copies of this simple mechanism. Its outputs can be counted exactly, and the count gives the exact privacy of the combination.

## Proof

The proof has three steps. Step 3, the computation, is full. Steps 1 and 2 are a sketch, and the full proof is in Kairouz, Oh and Viswanath (IEEE Transactions on Information Theory 2017), in the proof of the composition theorem through the hypothesis testing view.

**The hockey-stick form.** For laws $P, Q$ and $\varepsilon' \ge 0$, the smallest $\delta'$ with $P(S) \le e^{\varepsilon'}Q(S) + \delta'$ for all $S$ is $H_{\varepsilon'}(P\|Q) = \sum_v \max(0, P(v) - e^{\varepsilon'}Q(v))$, the maximum being reached at $S = \{v : P(v) > e^{\varepsilon'}Q(v)\}$. So a pair is $(\varepsilon', \delta')$-DP if and only if $H_{\varepsilon'}$ is at most $\delta'$ in both orders.

**Step 1 (worst case, sketch).** A pair $(P, Q)$ is $(\varepsilon, \delta)$-DP if and only if every test of $P$ against $Q$ with type I error $a$ has type II error at least $\max(0, 1 - \delta - e^{\varepsilon}a, e^{-\varepsilon}(1 - \delta - a))$, as defined on the page on [type I and type II errors](/type-i-and-type-ii-errors/). The pair $(\tilde P, \tilde Q)$ reaches this bound for every $a$. By Blackwell's theorem on the comparison of experiments, every $(\varepsilon, \delta)$-DP pair is then the image of $(\tilde P, \tilde Q)$ under one randomized map, applied to both.

**Step 2 (composition, sketch).** Apply Step 1 to each step of the experiment, given the prefix. The adaptive view in both experiments is then the image of $k$ independent copies of $(\tilde P, \tilde Q)$ under one randomized map. A randomized map cannot increase the hockey-stick divergence (it is a post-processing). So the view is $(\varepsilon', \delta')$-DP whenever the $k$-fold product of $(\tilde P, \tilde Q)$ is.

**Step 3 (the computation).** Let $P^k, Q^k$ be the $k$-fold products. Split the outputs $v \in \{0, 1, 2, 3\}^k$ in three groups.

1. $v$ has a 0. Then $Q^k(v) = 0$, and $v$ adds $P^k(v)$ to $H_{\varepsilon'}$. These outputs have total mass $1 - (1-\delta)^k$ under $P^k$.
2. $v$ has no 0 and has a 3. Then $P^k(v) = 0$, and $v$ adds nothing.
3. $v \in \{1, 2\}^k$ with $a$ ones. Then $P^k(v) = (1-\delta)^k e^{a\varepsilon}/(1+e^{\varepsilon})^k$ and $Q^k(v) = (1-\delta)^k e^{(k-a)\varepsilon}/(1+e^{\varepsilon})^k$. There are $\binom{k}{a}$ such $v$.

The sum of the three groups is $\delta_k(\varepsilon')$. The pair is symmetric under the swap $0 \leftrightarrow 3$, $1 \leftrightarrow 2$, so the other order gives the same value. Thus the product is $(\varepsilon', \delta')$-DP if and only if $\delta' \ge \delta_k(\varepsilon')$. With Step 2, $\delta_k(\varepsilon')$ is enough for every adaptive composition.

**Necessity.** The pair $(\tilde P, \tilde Q)$ is $(\varepsilon, \delta)$-DP: on outputs 1 and 2 the ratio is at most $e^{\varepsilon}$, and outputs 0 and 3 hold mass $\delta$. A mechanism that outputs $\tilde P$ on a dataset $x$ and $\tilde Q$ on a neighbor $x'$, run $k$ times, has a view whose $H_{\varepsilon'}$ is exactly $\delta_k(\varepsilon')$ by Step 3. So no smaller $\delta'$ is true for the class. $\blacksquare$

## Consequences

- **Exact numbers.** For $k = 100$, $\varepsilon = 0.1$, $\delta = 0$ and $\delta' = 10^{-6}$, the exact value is $\varepsilon' = 4.7746$. Advanced composition gives $6.3082$, and basic composition gives 10. The value comes from a bisection on $\varepsilon'$, since $\delta_k$ decreases in $\varepsilon'$. This short script checks it:

```python
from math import comb, exp

def delta_k(k, eps, delta, eps_total):
    p = 1 / (1 + exp(eps))
    s = sum(comb(k, a) * max(0.0, exp(a * eps) - exp(eps_total + (k - a) * eps)) for a in range(k + 1))
    return 1 - (1 - delta) ** k + (1 - delta) ** k * s * p ** k

lo, hi = 0.0, 10.0
for _ in range(100):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if delta_k(100, 0.1, 0.0, mid) > 1e-6 else (lo, mid)
print(round(hi, 4))  # 4.7746
```

- **A small hand example.** With $k = 2$ and randomized response with $\varepsilon = \ln 3$ ($\delta = 0$), the sum has terms $\binom{2}{a}\max(0, 3^a - e^{\varepsilon'}3^{2-a})/16$. This gives $\delta_2(0) = 8/16 = 1/2$, $\delta_2(\ln 3) = 6/16 = 3/8$ and $\delta_2(2\ln 3) = 0$.
- **Hardness for different steps.** Murtagh and Vadhan reduce a #P-complete counting problem, close to counting the solutions of a [knapsack problem](/knapsack-problem/), to the formula with different $\varepsilon_i$. Their approximation algorithm is based on approximate counting for knapsack. In practice, [numerical accountants](/numerical-privacy-accounting/) compute such values to a stated accuracy.
- **The trade-off view.** The test bound in Step 1 is the trade-off function of [f-DP](/gaussian-differential-privacy/). Dong, Roth and Su build on it, and their central limit theorem says that the composition of many steps with small $\varepsilon$ is close to Gaussian DP.
- **A link to privacy loss.** $\delta_k(\varepsilon')$ is $E[\max(0, 1 - e^{\varepsilon' - L})]$ for the [privacy loss](/privacy-loss-random-variable/) $L$ of the $k$-fold worst-case pair. The loss is $\varepsilon(2A - k)$ with $A$ [binomial](/binomial-distribution/), plus the value $+\infty$ with probability $1 - (1-\delta)^k$.

## Tightness

The theorem is its own tightness statement: the $k$-fold worst-case pair reaches $\delta_k(\varepsilon')$ for every $\varepsilon'$, as shown in the last part of the proof. The exact region holds for the class of all $(\varepsilon, \delta)$-DP mechanisms. A given mechanism, such as the Gaussian mechanism, can have a smaller region; an accountant that uses the exact output laws of that mechanism gets the smaller value.

## History

Kairouz, Oh and Viswanath presented the theorem at ICML 2015, and the journal version appeared in IEEE Transactions on Information Theory in 2017. They took the hypothesis testing view of privacy from earlier work of Wasserman and Zhou (2010) and used Blackwell's theorem to reduce composition to one worst-case mechanism. Murtagh and Vadhan (TCC 2016) treated different parameters for each step, proved the #P-completeness of the exact value and gave an approximation algorithm. Dong, Roth and Su (2022) turned the testing view into the definition of f-DP.

## References
