---
tag: WQMH2F
kind: theorem
slug: group-privacy-theorem
name: Group privacy
aliases:
- group privacy theorem
area: security-and-privacy/differential-privacy
level: core
summary: "An epsilon-DP mechanism protects any group of k records with parameter k times epsilon; with delta the additive term grows to about k e^((k-1) epsilon) delta."
prereqs: [differential-privacy-definition, approximate-differential-privacy]
see_also: [post-processing-theorem, sequential-composition-theorem, packing-lower-bound, laplace-mechanism, gaussian-mechanism, gaussian-differential-privacy, hamming-distance, induction]
sources:
  - paper: doi:10.1561/0400000042
    title: "Cynthia Dwork and Aaron Roth, The Algorithmic Foundations of Differential Privacy, Foundations and Trends in Theoretical Computer Science 9(3-4), 2014, pages 211 to 407"
    locator: "Section 2.3, Definition 2.3 (distance between databases), Theorem 2.2 (group privacy for delta = 0) with its proof, and the footnote to Theorem 2.2 (the form with delta)"
  - paper: doi:10.1007/11681878_14
    title: "Cynthia Dwork, Frank McSherry, Kobbi Nissim and Adam Smith, Calibrating noise to sensitivity in private data analysis, TCC 2006, LNCS 3876, pages 265 to 284"
    locator: the original definition for datasets that differ in one row, from which the group bound follows by a chain of neighbors
  - url: "https://arxiv.org/abs/1805.06530"
    title: "Borja Balle and Yu-Xiang Wang, Improving the Gaussian mechanism for differential privacy: analytical calibration and optimal denoising, ICML 2018, PMLR 80"
    locator: "Theorem 8 (the exact privacy profile of the Gaussian mechanism), used here for a group as a query with k times the sensitivity"
---

The group privacy theorem extends a guarantee for one record to a group of records. If a mechanism is $\varepsilon$-differentially private, then for two datasets that differ in $k$ records, the probability of every set of outputs changes by at most the factor $e^{k\varepsilon}$. So a family, a household or one person with $k$ records is protected with parameter $k\varepsilon$. For $(\varepsilon, \delta)$-DP the multiplicative part also becomes $k\varepsilon$, but the additive part grows faster, to $\delta(e^{k\varepsilon} - 1)/(e^{\varepsilon} - 1)$, which is at most $k e^{(k-1)\varepsilon}\delta$. Dwork and Roth (2014) state the pure form as Theorem 2.2 and the form with $\delta$ in a footnote to it. Both bounds can be reached, so they cannot be improved in general.

## Statement

Fix a neighbor relation $\sim$ (add/remove or replace). The **distance** $d(x, x')$ between two datasets is the smallest $k$ such that there is a chain $x = x_0 \sim x_1 \sim \cdots \sim x_k = x'$. Under add/remove on histograms it is $\lVert x - x' \rVert_1$ (Dwork-Roth Definition 2.3); under replace on datasets of the same size it is the [Hamming distance](/hamming-distance/).

**Theorem (group privacy).** Let $M$ be $(\varepsilon, \delta)$-[DP](/approximate-differential-privacy/) under $\sim$, and let $k \ge 1$ be an integer.

(a) (Dwork-Roth Theorem 2.2.) If $\delta = 0$, then for all $x, x'$ with $d(x, x') \le k$ and all sets $S$ of outputs,
$$\Pr[M(x) \in S] \le e^{k\varepsilon}\Pr[M(x') \in S].$$

(b) In general, for all $x, x'$ with $d(x, x') \le k$ and all $S$,
$$\Pr[M(x) \in S] \le e^{k\varepsilon}\Pr[M(x') \in S] + \delta_k, \qquad \delta_k = \delta\sum_{i=0}^{k-1} e^{i\varepsilon} = \delta\,\frac{e^{k\varepsilon} - 1}{e^{\varepsilon} - 1} \le k e^{(k-1)\varepsilon}\delta,$$
where the fraction is read as $k\delta$ when $\varepsilon = 0$. The last bound is the form in the footnote to Dwork-Roth Theorem 2.2.

## In plain words

Change the $k$ records one at a time. Each step changes the probability of any output set by at most the factor $e^{\varepsilon}$, so $k$ steps change it by at most $e^{\varepsilon}$ multiplied $k$ times. With $\delta$, each step also adds $\delta$, but the $\delta$ added at an early step is then multiplied by the factors of the later steps. That is why the additive part grows like $e^{k\varepsilon}$ and not like $k$.

## Proof

Let $d(x, x') = j \le k$ and take a chain $x = x_0 \sim x_1 \sim \cdots \sim x_j = x'$. Write $P_i(S) = \Pr[M(x_i) \in S]$ and fix $S$. We show by [induction](/induction/) on $i$ that

$$P_0(S) \le e^{i\varepsilon}P_i(S) + \delta_i \quad \text{for } i = 0, 1, \ldots, j, \qquad \delta_i = \delta\sum_{l=0}^{i-1} e^{l\varepsilon}, \quad \delta_0 = 0.$$

The case $i = 0$ is $P_0(S) \le P_0(S)$. For the step, $x_{i-1} \sim x_i$, so the definition gives $P_{i-1}(S) \le e^{\varepsilon}P_i(S) + \delta$. With the hypothesis for $i - 1$,

$$P_0(S) \le e^{(i-1)\varepsilon}P_{i-1}(S) + \delta_{i-1} \le e^{(i-1)\varepsilon}\big(e^{\varepsilon}P_i(S) + \delta\big) + \delta_{i-1} = e^{i\varepsilon}P_i(S) + \delta_{i-1} + e^{(i-1)\varepsilon}\delta,$$

and $\delta_{i-1} + e^{(i-1)\varepsilon}\delta = \delta_i$. At $i = j$ this gives $P_0(S) \le e^{j\varepsilon}\Pr[M(x') \in S] + \delta_j$. Both $e^{j\varepsilon} \le e^{k\varepsilon}$ and $\delta_j \le \delta_k$ hold because $j \le k$, which proves (b). The sum of the geometric series gives the closed form, and each of its $k$ terms is at most $e^{(k-1)\varepsilon}$, which gives $\delta_k \le k e^{(k-1)\varepsilon}\delta$. Part (a) is the case $\delta = 0$, where every $\delta_i$ is 0. $\square$

## Consequences

- **From add/remove to replace.** A replace step is a removal and then an addition, so two datasets that are neighbors under replace are at distance 2 under add/remove. So $\varepsilon$-DP under add/remove gives $2\varepsilon$-DP under replace, and $(\varepsilon, \delta)$-DP gives $(2\varepsilon, (1 + e^{\varepsilon})\delta)$-DP.
- **Households and repeated records.** If one person can contribute up to $k$ records, the person is protected with $k\varepsilon$. To get $\varepsilon$ for each person, either run the mechanism with $\varepsilon/k$, or bound the contribution of each person so that the unit of privacy is the person.
- **A numeric example.** With $\varepsilon = 0.1$, $\delta = 10^{-6}$ and $k = 10$, a group gets $k\varepsilon = 1$ and $\delta_{10} = 10^{-6}(e - 1)/(e^{0.1} - 1) = 1.6338 \times 10^{-5}$. The looser form gives $10e^{0.9} \times 10^{-6} = 2.4596 \times 10^{-5}$. Both are about 16 to 25 times $\delta$, so $\delta$ must be small enough to survive this growth.
- **Lower bounds.** The theorem is the main tool of the [packing lower bound](/packing-lower-bound/): an $\varepsilon$-DP mechanism must give every one of many datasets at distance $k$ from a fixed one a probability of at least $e^{-k\varepsilon}$ times its own, which limits how accurate it can be.
- **A direct analysis can be better.** For a mechanism with a known form, the group of $k$ is often analysed better by hand. The [Gaussian mechanism](/gaussian-mechanism/) with sensitivity $\Delta$ is, for a group of $k$, a Gaussian mechanism for a query with sensitivity $k\Delta$, and its exact profile follows from Balle and Wang (2018, Theorem 8). With $\Delta = 1$ and $\sigma = 3.730632$, which gives $(1, 10^{-5})$-DP, the exact value for $k = 10$ at $\varepsilon = 10$ is $\delta = 0.0040547$, while part (b) gives $0.12818$ and the looser form gives $0.81031$. In the language of [Gaussian DP](/gaussian-differential-privacy/), $\mu$-GDP gives $k\mu$-GDP for groups of $k$.
- **Post-processing and composition.** The group bound is a bound on $M$ itself, so it survives [post-processing](/post-processing-theorem/), and the group bounds of mechanisms run in sequence add up as in the [sequential composition theorem](/sequential-composition-theorem/).

## Tightness

**Part (a) is exact.** The [Laplace mechanism](/laplace-mechanism/) on a count with noise $\mathrm{Lap}(1/\varepsilon)$ is $\varepsilon$-DP. Two datasets whose counts differ by $k$ give densities $\frac{\varepsilon}{2}e^{-\varepsilon|y - c|}$ and $\frac{\varepsilon}{2}e^{-\varepsilon|y - c - k|}$. For every $y \le c$ the ratio of the densities is exactly $e^{k\varepsilon}$, so the set $S = (-\infty, c]$ reaches the bound of (a).

**Part (b) is exact.** Let each record be a bit, let $c(x) = \min(k, \text{number of ones in } x)$, and note that one add/remove or replace step changes $c$ by at most 1. Let $M(x)$ output the symbol $s$ with probability $\delta_{k - c(x)}$ and the symbol $t$ otherwise, and assume $\delta_k + \delta_{k-1} \le 1$. Write $a = \delta_{k-c-1}$ and $b = \delta_{k-c} = e^{\varepsilon}a + \delta$ for the probabilities of $s$ at the counts $c + 1$ and $c$.

- From count $c$ to count $c + 1$, the excess on $s$ is $b - e^{\varepsilon}a = \delta$, and on $t$ it is $(1 - b) - e^{\varepsilon}(1 - a) \le 0$ because $1 - b \le 1 - a$.
- From count $c + 1$ to count $c$, the excess on $s$ is $a - e^{\varepsilon}b \le 0$. On $t$ it is $(1 - a) - e^{\varepsilon}(1 - b)$, which is at most $\delta$ exactly when $a(e^{\varepsilon} + 1) + \delta \le 1$ (for $\varepsilon > 0$, divide by $e^{\varepsilon} - 1$). This holds because $a(e^{\varepsilon} + 1) + \delta \le \delta_{k-1}(e^{\varepsilon} + 1) + \delta = \delta_k + \delta_{k-1} \le 1$.

So $M$ is $(\varepsilon, \delta)$-DP under both relations. For a dataset $x$ with no ones and a dataset $x'$ with $k$ ones, at distance $k$, take $S = \{s\}$: then $\Pr[M(x) \in S] = \delta_k$ and $\Pr[M(x') \in S] = \delta_0 = 0$, so the additive part must be at least $\delta_k$, and part (b) holds with equality. With $\varepsilon = 0.1$, $\delta = 10^{-6}$ and $k = 10$, every pair of neighbors has the hockey-stick divergence $10^{-6}$ and the pair at distance 10 has $1.6338 \times 10^{-5}$.

So the bound $k e^{(k-1)\varepsilon}\delta$ of Dwork and Roth is not tight, but the sum $\delta_k$ is. For $\varepsilon = 0$ the bound is $k\delta$, and a mechanism that publishes each record with probability $\delta$ reveals some member of a group of $k$ with probability $1 - (1 - \delta)^k$, which is close to $k\delta$ when $k\delta$ is small; for $\delta = 10^{-5}$ and $k = 10$ it is $9.9996 \times 10^{-5}$.

## History

Group privacy follows directly from the first definition of differential privacy, by Dwork, McSherry, Nissim and Smith (2006): a bound for one row gives a bound for datasets that differ in more rows by a chain of neighbors. Dwork and Roth (2014) state it as Theorem 2.2 for $\delta = 0$, with the proof by a chain of neighbors, and give the form $k e^{(k-1)\varepsilon}\delta$ for $(\varepsilon, \delta)$-DP in a footnote. The exact sum $\delta(e^{k\varepsilon} - 1)/(e^{\varepsilon} - 1)$ is what the same induction gives when the terms are not bounded one by one.

## References
