---
tag: RX173Z
kind: theorem
slug: sequential-composition-theorem
name: Basic composition theorem
aliases:
- sequential composition
area: security-and-privacy/differential-privacy
level: intro
summary: "If k mechanisms, each (epsilon_i, delta_i)-DP, run on the same data, even adaptively, the k outputs together are (sum of epsilon_i, sum of delta_i)-DP."
history:
  year: 2006
  people: [Cynthia Dwork, Frank McSherry, Kobbi Nissim, Adam Smith]
  note: "The additive rule was in use from the first papers on differential privacy in 2006. McSherry (2009) named it sequential composition and made it the privacy budget of the PINQ system."
prereqs: [differential-privacy-definition, approximate-differential-privacy]
see_also: [parallel-composition-theorem, advanced-composition-theorem, optimal-composition-theorem, post-processing-theorem, group-privacy-theorem, randomized-response, privacy-loss-random-variable, renyi-differential-privacy]
sources:
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), pages 211 to 407, 2014"
    locator: "Section 3.5, Theorem 3.14 (two pure mechanisms), Corollary 3.15 (k pure mechanisms) and Theorem 3.16 (k mechanisms with (epsilon_i, delta_i)); Appendix B (the proof of Theorem 3.16)"
  - paper: doi:10.1145/1559845.1559850
    title: "Frank McSherry, Privacy integrated queries: an extensible platform for privacy-preserving data analysis, SIGMOD 2009, pages 19 to 30"
    locator: "the section on sequential and parallel composition"
  - paper: doi:10.1109/TIT.2017.2685505
    title: "Peter Kairouz, Sewoong Oh and Pramod Viswanath, The composition theorem for differential privacy, IEEE Transactions on Information Theory 63(6), pages 4037 to 4049, 2017"
    locator: "the exact privacy region of k-fold composition, which shows when the sum of the deltas can be improved"
---

The basic composition theorem says that privacy loss adds up. If $k$ mechanisms run on the same dataset, and mechanism $i$ is $(\varepsilon_i, \delta_i)$-differentially private, then the tuple of all $k$ outputs is $(\sum_i \varepsilon_i, \sum_i \delta_i)$-differentially private. This holds when each mechanism may depend on the outputs of the ones before it. The theorem is the reason that [differential privacy](/differential-privacy-definition/) can be managed as a budget: an analyst gets a total $\varepsilon$ and spends part of it on each query. The bound on $\varepsilon$ is tight for a worst-case mechanism. For many queries with small $\varepsilon_i$ the [advanced composition theorem](/advanced-composition-theorem/) gives a much smaller total, at the cost of a small extra $\delta$.

## Statement

Fix a set of datasets and a symmetric neighbor relation $x \sim x'$. The theorem holds for any such relation, for example add/remove or replace, because it is a statement about one pair at a time. A randomized mechanism $M$ is $(\varepsilon, \delta)$-differentially private ([approximate DP](/approximate-differential-privacy/)) if for every pair $x \sim x'$ and every event $S$ of outputs,

$$\Pr[M(x) \in S] \le e^{\varepsilon} \Pr[M(x') \in S] + \delta.$$

**Adaptive composition.** For $i = 1, \ldots, k$, let $M_i(x; y_1, \ldots, y_{i-1})$ be a mechanism that reads the dataset $x$ and the earlier outputs $y_1, \ldots, y_{i-1}$. The composed mechanism $M$ draws $Y_1 \sim M_1(x)$, then $Y_2 \sim M_2(x; Y_1)$, and so on, and outputs $(Y_1, \ldots, Y_k)$. The coins of the steps are independent given the earlier outputs.

**Theorem (basic composition).** If for each $i$ and each fixed prefix $(y_1, \ldots, y_{i-1})$ the mechanism $M_i(\cdot\,; y_1, \ldots, y_{i-1})$ is $(\varepsilon_i, \delta_i)$-DP, then $M$ is $\left(\sum_{i=1}^k \varepsilon_i, \sum_{i=1}^k \delta_i\right)$-DP.

The non-adaptive case, where each $M_i$ ignores the earlier outputs, is a special case. For pure DP ($\delta_i = 0$ for all $i$) the result is $(\sum_i \varepsilon_i)$-DP.

## In plain words

Each private answer leaks a little about each person. If you ask a second question, the second answer leaks a little more, and the two leaks add up. This stays true when you choose the second question after you see the first answer.

So a data holder can give an analyst a fixed privacy budget. Each question costs part of the budget. When the budget is spent, the data holder stops answering. The total leak about any one person is then at most the budget.

The rule is simple, and it is safe in the worst case. It can be too careful when you ask many small questions; a sharper rule exists for that case.

## Proof

All probabilities below are for one fixed pair $x \sim x'$. Write $P$ and $Q$ for the laws of the output under $x$ and under $x'$.

**Lemma 1.** If $P(S) \le e^{\varepsilon} Q(S) + \delta$ for every event $S$, then $E_P[h] \le e^{\varepsilon} E_Q[h] + \delta$ for every measurable function $h$ with values in $[0, 1]$.

*Proof.* By the layer-cake formula, $E_P[h] = \int_0^1 P(h > t)\,dt \le \int_0^1 \left(e^{\varepsilon} Q(h > t) + \delta\right) dt = e^{\varepsilon} E_Q[h] + \delta$.

**Two steps.** Let $P_1, Q_1$ be the laws of $Y_1$ under $x$ and $x'$, and let $P_2^{y}, Q_2^{y}$ be the laws of $M_2(x; y)$ and $M_2(x'; y)$. Fix an event $S$ of pairs, and write $S_{y} = \{y_2 : (y, y_2) \in S\}$. Then

$$\Pr[(Y_1, Y_2) \in S \mid x] = E_{y \sim P_1}\left[P_2^{y}(S_{y})\right].$$

For each $y$, the step-2 guarantee gives $P_2^{y}(S_y) \le e^{\varepsilon_2} Q_2^{y}(S_y) + \delta_2$. A probability is also at most 1, so $P_2^{y}(S_y) \le g(y) + \delta_2$ with $g(y) = \min\left(1, e^{\varepsilon_2} Q_2^{y}(S_y)\right)$. The function $g$ takes values in $[0, 1]$, so Lemma 1 applies to it with the step-1 guarantee:

$$\Pr[(Y_1, Y_2) \in S \mid x] \le E_{P_1}[g] + \delta_2 \le e^{\varepsilon_1} E_{Q_1}[g] + \delta_1 + \delta_2.$$

Now $g(y) \le e^{\varepsilon_2} Q_2^{y}(S_y)$, so $E_{Q_1}[g] \le e^{\varepsilon_2} E_{y \sim Q_1}[Q_2^{y}(S_y)] = e^{\varepsilon_2} \Pr[(Y_1, Y_2) \in S \mid x']$. This gives

$$\Pr[(Y_1, Y_2) \in S \mid x] \le e^{\varepsilon_1 + \varepsilon_2} \Pr[(Y_1, Y_2) \in S \mid x'] + \delta_1 + \delta_2.$$

**Induction on $k$.** The case $k = 1$ is the hypothesis. For $k \ge 2$, the first $k - 1$ steps form one mechanism with output $(Y_1, \ldots, Y_{k-1})$. By the induction hypothesis it is $(\sum_{i<k} \varepsilon_i, \sum_{i<k} \delta_i)$-DP. Step $k$ is a mechanism that reads this output as its prefix, and it is $(\varepsilon_k, \delta_k)$-DP for each prefix. The two-step argument, with the first $k - 1$ steps as step 1, gives the claim. $\blacksquare$

## Consequences

- **The privacy budget.** A system can keep a running sum of the $\varepsilon_i$ and $\delta_i$ that it has spent and refuse queries past a limit. PINQ did this. The [sparse vector technique](/sparse-vector-technique/) and [report noisy max](/report-noisy-max/) are ways to pay less than the sum for special query patterns.
- **Building blocks.** Many algorithms are a sequence of private steps, for example a [Laplace mechanism](/laplace-mechanism/) per query, or one noisy gradient per step of [DP-SGD](/dp-sgd/). Basic composition gives a first bound for each of them. With [post-processing](/post-processing-theorem/), any function of the outputs keeps the bound.
- **Parallel composition.** When the mechanisms read disjoint parts of the data, the [parallel composition theorem](/parallel-composition-theorem/) replaces the sum by the maximum. Its proof uses the theorem above for each pair of neighbors.
- **Sharper rules.** The [advanced composition theorem](/advanced-composition-theorem/) and the [optimal composition theorem](/optimal-composition-theorem/) improve the sum when $k$ is large. [Renyi DP](/renyi-differential-privacy/) and [zCDP](/zero-concentrated-differential-privacy/) compose by a plain sum of their own parameters, and the conversion to $(\varepsilon, \delta)$ is done once, at the end.
- **A rule of thumb, not a theorem.** Splitting a budget evenly, $\varepsilon_i = \varepsilon/k$, is common. It is a choice of the analyst. The theorem gives the same total for any split.

## Tightness

**The sum of the epsilons.** Take [randomized response](/randomized-response/) with $\varepsilon = \ln 3$: a person with bit $b$ reports $b$ with probability $3/4$ and $1 - b$ with probability $1/4$. Use replace neighbors on a dataset of one person: $x$ has bit 1 and $x'$ has bit 0. Run it twice with fresh coins. The outputs $(1,1), (1,0), (0,1), (0,0)$ have probabilities $(9, 3, 3, 1)/16$ under $x$ and $(1, 3, 3, 9)/16$ under $x'$. At the output $(1, 1)$ the ratio is $9 = e^{2 \ln 3}$. So the pair is not $(\varepsilon', 0)$-DP for any $\varepsilon' < 2 \ln 3$, and the bound $\varepsilon_1 + \varepsilon_2$ is exact. The same computation with $k$ runs gives the ratio $3^k = e^{k \ln 3}$.

**The sum of the deltas.** Let $M_\delta$ output the whole dataset with probability $\delta$ and a fixed symbol $\perp$ otherwise. It is $(0, \delta)$-DP. Run $k$ independent copies on $x$, and let $S$ be the event that some copy outputs $x$. Then $\Pr[S \mid x] = 1 - (1 - \delta)^k$ and $\Pr[S \mid x'] = 0$. So the composition is not $(\varepsilon', \delta')$-DP for any $\varepsilon'$ when $\delta' < 1 - (1 - \delta)^k = k\delta - O(k^2 \delta^2)$. The sum $k\delta$ is tight up to the second-order term.

The two parts are not tight at the same time for all parameters. Kairouz, Oh and Viswanath found the exact set of pairs $(\varepsilon', \delta')$ that k-fold composition reaches; see the [optimal composition theorem](/optimal-composition-theorem/).

## History

The additive rule appears in the first papers on differential privacy, by Dwork, McSherry, Nissim and Smith (2006) and by Dwork, Kenthapadi, McSherry, Mironov and Naor (2006), as the way to answer several queries. McSherry (2009) named it sequential composition, together with parallel composition, and made it the privacy budget of the PINQ query system. Dwork and Roth (2014) give the pure case as Theorem 3.14 and Corollary 3.15 and the $(\varepsilon, \delta)$ case as Theorem 3.16. Dwork, Rothblum and Vadhan (2010) set up the adaptive model, in which an adversary picks each mechanism after it sees the earlier outputs, that this page uses.

## References
