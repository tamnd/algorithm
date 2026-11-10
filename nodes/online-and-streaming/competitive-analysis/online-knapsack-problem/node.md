---
tag: 1TC7DE
kind: problem
slug: online-knapsack-problem
name: Online knapsack problem
aliases:
- online unit-density knapsack
- online knapsack
- online simple knapsack
area: online-and-streaming/competitive-analysis
level: advanced
summary: Items arrive one at a time and must be taken or refused for good under a capacity. No online algorithm has a bounded ratio in general; bounded densities with small items give 1 + ln(U/L).
prereqs: [knapsack-problem, online-algorithm, competitive-ratio]
see_also: [online-threshold-knapsack, knapsack-problem, fractional-knapsack, secretary-problem, online-adwords-problem, advice-model, yao-minimax-principle, oblivious-adversary]
sources:
  - paper: "Alberto Marchetti-Spaccamela and Carlo Vercellis, Stochastic on-line knapsack problems, Mathematical Programming 68 (1995), 73-104"
    title: Stochastic on-line knapsack problems
    locator: the introduction (no deterministic online algorithm has a bounded ratio in the worst case) and the analysis under random inputs
  - paper: "Yunhong Zhou, Deeparnab Chakrabarty and Rajan Lukose, Budget constrained bidding in keyword auctions and online knapsack problems, Internet and Network Economics (WINE 2008), LNCS 5385, Springer, 566-576"
    title: Budget constrained bidding in keyword auctions and online knapsack problems
    locator: Section 2 (the ratio ln(U/L) + 1 for small items with densities in [L, U], and the lower bound)
  - paper: doi:10.1016/j.tcs.2014.01.027
    title: "Hans-Joachim Böckenhauer, Dennis Komm, Richard Královič and Peter Rossmanith, The online knapsack problem: advice and randomization, Theoretical Computer Science 527 (2014)"
    locator: the results on the simple (unit density) knapsack, ratio 2 with one random bit and the matching lower bound for randomized algorithms, and the advice bounds
  - paper: "Kazuo Iwama and Shiro Taketomi, Removable online knapsack problems, Automata, Languages and Programming (ICALP 2002), LNCS 2380, Springer, 293-305"
    title: Removable online knapsack problems
    locator: the golden ratio for the unit density case when taken items may be discarded
---

The online knapsack problem is the [knapsack problem](/knapsack-problem/) with the items revealed one at a time. Each item has a weight and a value, and it must be taken or refused when it arrives, for good, so that the taken items fit in a knapsack of fixed capacity. The goal is a large total value compared with the best packing of all the items. In this general form no online algorithm, deterministic or randomized, has a bounded competitive ratio: a deterministic algorithm cannot tell whether to keep room for a much better item, and a randomized one cannot guess when the best item has come. Bounded ratios need assumptions. With value equal to weight (the unit density case), randomization gives exactly 2. With densities in a known range $[L, U]$ and small items, the [threshold algorithm](/online-threshold-knapsack/) gives $1 + \ln(U/L)$, which is optimal.

## In plain words

A truck has a fixed load limit. Parcels are offered one by one, each with a size and a fee. The driver must accept or refuse each parcel on the spot and cannot unload later. The goal is to earn as much as possible.

Without more knowledge the task is hopeless. If the driver takes a parcel that fills the truck, a parcel with a far larger fee may come next. If the driver refuses it, no other parcel may come. Even a coin flip does not help, because the fees can grow so fast that only the last parcel counts. Things change when fees are bounded per unit of size and each parcel is small: then a rule that gets choosier as the truck fills earns a fixed share of the best.

## Definition

**Input.** A capacity, normalized to 1, and a sequence of items $(w_1, v_1), (w_2, v_2), \ldots, (w_n, v_n)$ revealed one at a time, with weight $w_i \in (0, 1]$ and value $v_i > 0$. The number $n$ is unknown to the algorithm. The density of item $i$ is $e_i = v_i / w_i$.

**Decisions.** When item $i$ arrives, the algorithm takes it or refuses it, for good. The taken set $S$ must satisfy $\sum_{i \in S} w_i \le 1$ at all times.

**Goal.** Maximize $\mathrm{ALG} = \sum_{i \in S} v_i$. $\mathrm{OPT}$ is the largest value of a set of items with total weight at most 1. An algorithm has ratio $\rho \ge 1$ if $\mathrm{OPT} \le \rho \cdot \mathrm{ALG}$ on every input, with no additive term; in the convention $\mathrm{ALG} \ge c \cdot \mathrm{OPT}$ of the other maximization pages, $c = 1/\rho$. For randomized algorithms, $\mathrm{OPT} \le \rho \cdot \mathbb{E}[\mathrm{ALG}]$ against an [oblivious adversary](/oblivious-adversary/).

## Variants

- **Unit density (simple knapsack).** $v_i = w_i$, so the goal is to fill the knapsack as much as possible. It is the online form of subset sum.
- **Bounded densities and small items.** $e_i \in [L, U]$ with $L, U$ known, and $w_i \le \varepsilon$ for a small $\varepsilon$. This is the setting of the [threshold algorithm](/online-threshold-knapsack/), and of budgeted bidding.
- **Removable items.** Taken items may be discarded later, but refused items are lost. For unit density the best deterministic ratio is the golden ratio $(1 + \sqrt{5})/2 \approx 1.618$ (Iwama and Taketomi 2002).
- **Random order.** The adversary chooses the items, but they arrive in a uniformly random order. This is the knapsack secretary problem; Babaioff, Immorlica, Kempe and Kleinberg (2007) gave a constant ratio ($10e$), and later work improved the constant. See the [secretary problem](/secretary-problem/).
- **Advice.** The algorithm may read some bits written by an oracle that knows the input. For unit density, one bit gives ratio 2, and Böckenhauer et al. (2014) gave the trade-off between bits and ratio; see the [advice model](/advice-model/).
- **Stochastic inputs.** Weights and values are drawn from known distributions, and the goal is a good expected value; Marchetti-Spaccamela and Vercellis (1995) studied this case.

## Examples

**The adversary for deterministic algorithms.** The first item is $(1, 1)$. If the algorithm refuses it, the input ends: $\mathrm{ALG} = 0$ and $\mathrm{OPT} = 1$. If it takes it, the next item is $(1, M)$, which does not fit: $\mathrm{ALG} = 1$ and $\mathrm{OPT} = M$. For $M = 1000$ the ratio is at least 1000.

**The one-bit algorithm for unit density.** Items of weight $0.3, 0.4, 0.5, 0.6$ arrive. Greedy, which takes each item that fits, takes $0.3$ and $0.4$ and then refuses $0.5$, so it gets $0.7$. The second rule simulates greedy, waits for the first item that greedy refuses, and is greedy from there on: it takes $0.5$ and refuses $0.6$, so it gets $0.5$. The two together get $1.2 > 1 \ge \mathrm{OPT} = 1.0$ (the items $0.4$ and $0.6$). A random bit chooses one of the rules, so the expected value is $0.6 \ge \mathrm{OPT}/2$.

## Known algorithms

- **[Threshold algorithm](/online-threshold-knapsack/)** (Zhou, Chakrabarty and Lukose 2008). For densities in $[L, U]$ and small items: take an item if its density is at least $\Psi(z)$, where $z$ is the used fraction, $\Psi = L$ up to $z = 1/(1 + \ln(U/L))$ and then rises exponentially to $U$. Ratio $1 + \ln(U/L)$ in the limit of small items, optimal.
- **Greedy.** Take each item that fits. For unit density its ratio is unbounded (Theorem 2), but it is the base of the one-bit algorithm.
- **One random bit for unit density.** Run greedy, or run the rule that starts to be greedy at the first item greedy refuses, each with probability $1/2$. Ratio 2 (Theorem 4).
- **Removable unit density.** A deterministic algorithm that keeps a good subset and discards small items when a large one comes, with ratio $(1 + \sqrt{5})/2$ (Iwama and Taketomi).
- **Offline algorithms as tools.** The [fractional knapsack](/fractional-knapsack/) optimum, found by sorting by density, is the usual upper bound on $\mathrm{OPT}$ in analyses and tests.

## Bounds

**Theorem 1 (deterministic, general values: unbounded).** For each deterministic online algorithm and each $M > 1$ there is an input of two items on which $\mathrm{OPT} \ge M \cdot \mathrm{ALG}$ or $\mathrm{ALG} = 0 < \mathrm{OPT}$.

*Proof.* The adversary of the examples. The algorithm is deterministic, so the adversary knows whether it takes $(1, 1)$. If not, the input ends with $\mathrm{ALG} = 0$ and $\mathrm{OPT} = 1$. If so, the item $(1, M)$ follows, the knapsack is full, and $\mathrm{ALG} = 1$ while $\mathrm{OPT} = M$. $\square$

**Theorem 2 (deterministic, unit density: unbounded).** For each deterministic online algorithm for unit density and each $\varepsilon \in (0, 1)$ there is an input with $\mathrm{OPT} \ge \mathrm{ALG} / \varepsilon$, or with $\mathrm{ALG} = 0 < \mathrm{OPT}$.

*Proof.* The first item is $(\varepsilon, \varepsilon)$. If the algorithm refuses it, the input ends with $\mathrm{ALG} = 0$. If it takes it, the item $(1, 1)$ follows; it does not fit, because $\varepsilon + 1 > 1$, so $\mathrm{ALG} = \varepsilon$ and $\mathrm{OPT} = 1$. $\square$

**Theorem 3 (randomized, general values: unbounded).** For each randomized online algorithm and each integer $k \ge 2$ there is an input with $\mathbb{E}[\mathrm{ALG}] \le (2/k) \cdot \mathrm{OPT}$. So no randomized algorithm has a bounded ratio, even against an oblivious adversary.

*Proof.* Let $M = k + 1$. Item $i$, for $i = 1, \ldots, k$, is $(1, M^i)$. The knapsack holds one item. The input $\sigma_j$ is the first $j$ items, so $\mathrm{OPT}(\sigma_j) = M^j$. All inputs $\sigma_j$ share their prefixes, so the probability $p_i$ that the algorithm takes item $i$ is the same in each $\sigma_j$ with $j \ge i$. The algorithm takes at most one item, so $\sum_{i=1}^k p_i \le 1$, and some $j$ has $p_j \le 1/k$. On $\sigma_j$,

$$\mathbb{E}[\mathrm{ALG}] = \sum_{i \le j} p_i M^i \le M^j \Bigl(\sum_{i < j} M^{i - j} + p_j\Bigr) \le M^j \Bigl(\frac{1}{M - 1} + \frac{1}{k}\Bigr) = \frac{2}{k}\, \mathrm{OPT}(\sigma_j). \qquad \square$$

The input $\sigma_j$ is fixed in advance, so the adversary is oblivious. Small items alone do not help either: the lower bound of Theorem 5 holds for items of any small size and grows like $\ln(U/L)$, so it is unbounded when the densities are not bounded.

**Theorem 4 (randomized, unit density: exactly 2).** For unit density, the one-bit algorithm has $\mathbb{E}[\mathrm{ALG}] \ge \mathrm{OPT}/2$, and no randomized online algorithm has ratio below 2. Böckenhauer, Komm, Královič and Rossmanith (2014) proved both statements.

*Proof of the upper bound.* If greedy takes every item, it gets the total weight of all items, which is at least $\mathrm{OPT}$. Otherwise let item $j$ be the first item that greedy refuses, and let $W$ be the weight greedy holds at that time, so $W + w_j > 1$. The second rule starts with an empty knapsack at item $j$ and takes it, so it gets at least $w_j$. Greedy keeps at least $W$. Together they get more than $W + w_j > 1 \ge \mathrm{OPT}$, so the average of the two is above $\mathrm{OPT}/2$. $\square$

*Proof of the lower bound.* Fix $\varepsilon \in (0, 1)$ and let $p$ be the probability that the algorithm takes a first item $(\varepsilon, \varepsilon)$. On the input of this item alone, $\mathbb{E}[\mathrm{ALG}] = p \varepsilon$ and $\mathrm{OPT} = \varepsilon$, so the ratio is $1/p$. On the input $(\varepsilon, \varepsilon), (1, 1)$, the second item fits only if the first was refused, so $\mathbb{E}[\mathrm{ALG}] \le p \varepsilon + (1 - p)$ while $\mathrm{OPT} = 1$. The better of the two is at best $\min(p, 1 - p + p\varepsilon)$, which is largest at $p = 1/(2 - \varepsilon)$. So the ratio is at least $2 - \varepsilon$ for each $\varepsilon > 0$. $\square$

**Theorem 5 (bounded densities and small items: $1 + \ln(U/L)$).** If every density is in $[L, U]$ and every weight is at most $\varepsilon$, the [threshold algorithm](/online-threshold-knapsack/) has $\mathrm{OPT} \le (1 + \ln(U/L)) (Ue/L)^{2\varepsilon}\, \mathrm{ALG}$ for $\varepsilon \le 1 - 1/(1 + \ln(U/L))$. Each online algorithm, also randomized, has ratio at least $1 + N(1 - (L/U)^{1/N})$ for each $N$, which tends to $1 + \ln(U/L)$. Both proofs are on the [algorithm page](/online-threshold-knapsack/); the lower bound uses batches of tiny items with densities that rise geometrically from $L$ to $U$.

| setting | best ratio $\rho$ |
|---|---|
| general, deterministic | unbounded (Theorem 1) |
| general, randomized | unbounded (Theorem 3) |
| unit density, deterministic | unbounded (Theorem 2) |
| unit density, randomized | 2 (Theorem 4) |
| unit density, removable, deterministic | $(1 + \sqrt{5})/2$ (Iwama and Taketomi) |
| densities in $[L, U]$, small items | $1 + \ln(U/L)$ (Theorem 5) |
| random order | a constant (knapsack secretary) |

For $U/L = 2$, $10$ and $100$ the ratio of Theorem 5 is $1.6931$, $3.3026$ and $5.6052$.

## Reductions

- **From offline knapsack.** An offline instance is an online one in any order, so a polynomial-time online algorithm would be an offline one with the same ratio. Here this gives nothing new, because offline knapsack has an [FPTAS](/knapsack-fptas/); the online hardness is all about information.
- **To fractional knapsack with small items.** When all items are small, the integral and the [fractional](/fractional-knapsack/) optimum differ by a factor at most $1/(1 - \varepsilon)$, because the items of highest density that fit whole already fill at least $1 - \varepsilon$ of the capacity. So the small items setting is the online fractional knapsack in disguise.
- **To adwords.** One budget with small bids that pay their value is one knapsack with small items. The [adwords problem](/online-adwords-problem/) has many budgets and lets each query go to one of them, and its trade-off function plays the role of the knapsack threshold.
- **To one-way trading.** Spending a budget at prices that arrive online and lie in a known range is the small items knapsack with densities in $[L, U]$, and its optimal ratio is logarithmic in the range in the same way.

## Applications

- **Budgeted bidding.** An advertiser with a daily budget sees keyword auctions one at a time, each costing a small part of the budget and giving a value per cost in a known range. This was the motivation of Zhou, Chakrabarty and Lukose.
- **Admission control.** Requests for bandwidth, compute or memory arrive with a size and a payment, and must be admitted or turned away at once under a fixed capacity.
- **Revenue management.** Selling a fixed stock of seats or rooms to customers who arrive with offers, without knowing future demand.

## References
