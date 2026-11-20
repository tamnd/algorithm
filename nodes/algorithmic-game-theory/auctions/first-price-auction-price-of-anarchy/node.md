---
tag: Z6E38R
kind: theorem
slug: first-price-auction-price-of-anarchy
name: Price of anarchy of first-price auctions
aliases:
- 1 - 1/e bound for first-price auctions
area: algorithmic-game-theory/auctions
level: advanced
summary: "Every Bayes-Nash equilibrium of a first-price auction with independent values has expected welfare at least 1 - 1/e^2 (about 0.865) of the optimum, a ratio of at most 1.157. The old bound was 1 - 1/e."
prereqs: [price-of-anarchy, bayes-nash-equilibrium, first-price-auction, independent-private-values, first-price-auction-equilibrium]
see_also: [price-of-anarchy, price-of-stability, smoothness-framework, first-price-auction, first-price-auction-equilibrium, vickrey-auction, bayes-nash-equilibrium, independent-private-values]
sources:
  - paper: doi:10.1145/3617902
    title: "Yaonan Jin and Pinyan Lu, First price auction is 1 - 1/e^2 efficient, Journal of the ACM 70(5) (2023), article 36"
    locator: the main theorem, that the price of anarchy of the first-price auction with independent values is 1 - 1/e^2 and that this bound is tight, and an example of an inefficient equilibrium with two bidders
  - paper: doi:10.1137/1.9781611977554.ch14
    title: "Yaonan Jin and Pinyan Lu, The price of stability for first price auction, Proceedings of SODA 2023, 332-352"
    locator: the result that with independent values the price of stability of the first-price auction is also 1 - 1/e^2, and the price of stability for correlated values
  - paper: doi:10.1145/3699804.3699810
    title: "Yaonan Jin and Pinyan Lu, Settling the efficiency of the first-price auction, ACM SIGecom Exchanges 20(2)"
    locator: a survey of the bounds 1 - 1/e, 0.743 and 1 - 1/e^2 and of the proof ideas
  - paper: doi:10.1145/2488608.2488635
    title: "Vasilis Syrgkanis and Eva Tardos, Composable and efficient mechanisms, Proceedings of STOC 2013, 211-220"
    locator: the smoothness bound 1 - 1/e for the Bayes-Nash equilibria of the first-price auction, which holds also for correlated values
  - paper: doi:10.1145/3188745.3188944
    title: "Darrell Hoy, Samuel Taggart and Zihe Wang, A tighter welfare guarantee for first-price auctions, Proceedings of STOC 2018, 132-137"
    locator: the bound of about 0.743 for independent values, and the worst example known at the time, with ratio about 0.869
  - paper: "Tim Roughgarden, Vasilis Syrgkanis and Eva Tardos, The price of anarchy in auctions, Journal of Artificial Intelligence Research 59 (2017), 59-101"
    locator: Theorem 2.2 (the bound 1 - 1/e for first-price auctions with correlated values) and the discussion of its tightness
---

The price of anarchy of the [first-price auction](/first-price-auction/) measures how much welfare its equilibria can lose. With symmetric bidders the equilibrium is efficient, because all bidders use the same increasing bid function. With asymmetric bidders, a bidder with a weaker value distribution bids more aggressively, and the item can go to a bidder whose value is not the highest. The question is how large this loss can be over all value distributions and all equilibria. Syrgkanis and Tardos (2013) showed that every equilibrium keeps at least a fraction $1 - 1/e \approx 0.632$ of the optimal welfare. Jin and Lu (2022) found the exact answer for independent values: $1 - 1/e^2 \approx 0.865$. In the ratio form of the [price of anarchy](/price-of-anarchy/), the optimum is at most $e^2/(e^2 - 1) \approx 1.157$ times the welfare of any equilibrium.

## Statement

**The model.** One item is sold to $n$ bidders by a first-price auction: each bidder submits a bid $b_i \ge 0$, the highest bid wins, ties are broken by any fixed rule, and the winner pays its bid. There is no reserve price. Bidder $i$ has a value $v_i \ge 0$ and [quasilinear utility](/quasilinear-utility/). The value profile $v = (v_1, \ldots, v_n)$ is drawn from a known joint distribution $F$. In the independent case, $F = F_1 \times \cdots \times F_n$ is a product of distributions that can differ, as in the [independent private values](/independent-private-values/) model with asymmetric bidders. A [Bayes-Nash equilibrium](/bayes-nash-equilibrium/) is a profile of strategies, possibly mixed, that map values to bids, such that no bidder of any value gains in expectation by a different bid.

**Welfare.** The welfare of an outcome is the value of the winner. Let $\mathrm{OPT} = \mathbb{E}[\max_i v_i]$, the expected welfare of the efficient allocation, and $W(s) = \mathbb{E}[v_{\text{winner}}]$ the expected welfare at an equilibrium $s$.

**Theorem 1 (Syrgkanis and Tardos 2013).** For every joint distribution $F$, correlated or not, every Bayes-Nash equilibrium $s$ of the first-price auction has $W(s) \ge (1 - 1/e)\, \mathrm{OPT}$.

**Theorem 2 (Jin and Lu 2022).** For every product distribution $F$, every Bayes-Nash equilibrium $s$ of the first-price auction has $W(s) \ge (1 - 1/e^2)\, \mathrm{OPT}$. The constant is tight: for every $\varepsilon > 0$ there are independent distributions and an equilibrium with $W(s) < (1 - 1/e^2 + \varepsilon)\, \mathrm{OPT}$.

In ratio form, the price of anarchy is at most $e/(e - 1) \approx 1.582$ for correlated values and exactly $e^2/(e^2 - 1) \approx 1.1565$ for independent values.

## In plain words

In a first-price auction a bidder shades its bid below its value, and bidders who differ shade by different amounts. So the bidder with the highest value can lose to a rival that shaded less. This can waste welfare, but not much. If the bidder with the highest value is losing too often, it can switch to a random bid with a carefully chosen spread and win often at a fair price. In an equilibrium no such switch helps, so the high-value bidder already wins often, or the others already pay high prices that count toward the welfare. When the values are independent, the worst case keeps about 86.5 percent of the best welfare.

## Proof

This section proves Theorem 1. The proof of the tight bound in Theorem 2 is long and is in Jin and Lu (2022).

**Step 1: a deviation with a guaranteed utility.** Fix a bidder $i$ with value $v_i > 0$, and let $p$ be the highest bid of the other bidders. Consider the random bid $b$ with density $\frac{1}{v_i - b}$ on $[0, (1 - 1/e)\, v_i]$. This is a probability density, since

$$\int_0^{(1 - 1/e) v_i} \frac{db}{v_i - b} = \ln \frac{v_i}{v_i / e} = 1.$$

The bid $b$ has no atom, so it ties with $p$ with probability 0. If $p < (1 - 1/e)\, v_i$, the bidder wins when $b > p$, and its expected utility is

$$\int_p^{(1 - 1/e) v_i} (v_i - b) \cdot \frac{1}{v_i - b}\, db = (1 - 1/e)\, v_i - p.$$

If $p \ge (1 - 1/e)\, v_i$, the utility is at least $0 \ge (1 - 1/e)\, v_i - p$. In both cases the expected utility of the deviation is at least $(1 - 1/e)\, v_i - p$, and it is at least 0.

**Step 2: the equilibrium condition.** Let $P_i$ be the highest bid of the others at the equilibrium $s$. It is a random variable that depends on $v_{-i}$ and on the random choices of the others. The deviation of Step 1 depends only on $v_i$, so it is a valid deviation for bidder $i$ at the interim stage. Let $i^*(v)$ be a bidder with the highest value. By Step 1, for every profile $v$ and every outcome of the others' bids, the deviation gives bidder $i$ an expected utility of at least $\mathbb{1}\{i = i^*(v)\} \bigl((1 - 1/e)\, v_i - P_i\bigr)$, because it is at least 0 for every bidder and at least $(1 - 1/e)\, v_i - P_i$ for the bidder $i^*$. At the equilibrium, each type of bidder $i$ has at least the expected utility of this deviation. Take the expectation over $v_i$ and add over $i$:

$$\sum_i \mathbb{E}[u_i(s)] \;\ge\; (1 - 1/e)\, \mathbb{E}\bigl[v_{i^*}\bigr] - \mathbb{E}\bigl[P_{i^*}\bigr] = (1 - 1/e)\, \mathrm{OPT} - \mathbb{E}\bigl[P_{i^*}\bigr].$$

**Step 3: welfare is utility plus revenue.** In the first-price auction the winner pays the highest bid, so the revenue is $R = \max_j b_j \ge P_{i^*}$. With quasilinear utility, the welfare is the sum of the utilities plus the revenue:

$$W(s) = \sum_i \mathbb{E}[u_i(s)] + \mathbb{E}[R] \;\ge\; (1 - 1/e)\, \mathrm{OPT} - \mathbb{E}[P_{i^*}] + \mathbb{E}[R] \;\ge\; (1 - 1/e)\, \mathrm{OPT}. \qquad \square$$

The proof uses independence nowhere, which is why Theorem 1 holds for correlated values. It has the form of a smoothness argument ([smoothness framework](/smoothness-framework/)): a deviation that depends only on the bidder's own value, a utility bound of the form $\lambda \cdot v_i - \mu \cdot p$ with $\lambda = 1 - 1/e$ and $\mu = 1$, and the fact that the prices are paid to the seller.

## Consequences

- **The ratio is a constant.** No first-price auction loses more than about 13.5 percent of the optimal welfare at any Bayes-Nash equilibrium, for any number of bidders and any independent distributions.
- **The best equilibrium is no better in the worst case.** With independent values, the price of stability is also $1 - 1/e^2$: there are instances where even the best equilibrium has this ratio (Jin and Lu, SODA 2023). See [price of stability](/price-of-stability/).
- **Symmetric bidders.** If all $F_i$ are the same, the symmetric equilibrium is efficient ([first-price auction equilibrium](/first-price-auction-equilibrium/)), so the loss comes from asymmetry.
- **A typical loss is small.** With one bidder uniform on $[0, 1]$ and the other uniform on $[0, 2]$, the equilibrium gives the item to the wrong bidder with probability about $1/12$, but the welfare is about $98.1$ percent of the optimum. This is a numerical computation for one instance.
- **The Vickrey auction is efficient.** The [Vickrey auction](/vickrey-auction/) has a truthful dominant-strategy equilibrium with ratio 1. The bound measures what is lost when a seller uses a first-price auction, for example because bidders find it simpler or because it is used as part of a larger mechanism.
- **Mixed equilibria.** The proof of Theorem 1 compares the equilibrium with one fixed deviation for each bidder, so it covers mixed strategies and every tie-breaking rule without change.

## Tightness

- **Correlated values.** The bound $1 - 1/e$ of Theorem 1 cannot be improved when values may be correlated; Syrgkanis (2014) gave an example with three bidders, and the survey of Roughgarden, Syrgkanis and Tardos (2017) discusses it. A better bound needs independence.
- **Independent values.** Hoy, Taggart and Wang (2018) raised the bound to about $0.743$, while the worst example then known had a ratio of about $0.869$. Jin and Lu (2022) closed the gap with $1 - 1/e^2 \approx 0.8647$, and they gave instances whose ratio tends to this value, so Theorem 2 is tight.
- **An example of an inefficient equilibrium.** Jin and Lu give a small example with two bidders. Alice has value 1. Bob has a value uniform on $[0, 1]$ and bids $\max(1 - \frac{1}{4v}, 0)$, so his bid has the distribution function $\frac{1}{4 - 4b}$ on $[0, 3/4]$. Alice bids at random with distribution function $B(b) = \frac{1}{4b - 2} \exp\bigl(\frac{4b - 3}{2b - 1}\bigr)$ on $[1/2, 3/4]$. Every bid of Alice in $[0, 3/4]$ gives her the utility $(1 - b) \cdot \frac{1}{4 - 4b} = 1/4$, and Bob's bid satisfies his first-order condition $B'(b)/B(b) = 1/(v - b)$, so this is an equilibrium. Alice always has the higher value, so $\mathrm{OPT} = 1$, but Bob wins with probability $1/4$. A numerical integration gives an expected welfare of about $0.9627$, a ratio of about $1.039$. Bob with value $3/4$ bids $2/3$ and wins with probability $B(2/3) = \frac{3}{2e} \approx 0.552$.

## History

Syrgkanis and Tardos (2013) proved the bound $1 - 1/e$ as part of their smoothness framework for composed mechanisms, building on the smoothness method for games of complete information. Syrgkanis (2014) showed that this bound is tight for correlated values. For independent values, Hoy, Taggart and Wang (2018) improved the bound to about $0.743$. Jin and Lu proved the tight value $1 - 1/e^2$ at FOCS 2022, with the journal version in the Journal of the ACM in 2023, and in a second paper at SODA 2023 they showed that the price of stability has the same value.

## References
