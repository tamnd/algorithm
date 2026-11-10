---
tag: D4HW7M
kind: problem
slug: bahncard-problem
name: Bahncard problem
aliases:
- discount card problem
area: online-and-streaming/competitive-analysis
level: core
summary: Ski rental generalised to buying a discount card that lowers the price of later trips.
prereqs: [ski-rental-problem, break-even-strategy]
see_also: [competitive-ratio, randomized-online-algorithm, oblivious-adversary, tcp-acknowledgment-problem, offline-optimum, yao-minimax-principle, learning-augmented-algorithms]
sources:
  - paper: doi:10.1016/S0304-3975(00)00266-8
    title: "Rudolf Fleischer, On the Bahncard problem, Theoretical Computer Science 268(1) (2001), 161-174"
    locator: the problem BP(C, beta, T), the algorithm SUM and the deterministic bound 2 - beta, the randomized lower bound e/(e - 1 + beta), and the algorithm RAND for T infinite
  - paper: doi:10.1007/s00453-003-1013-x
    title: "Anna R. Karlin, Claire Kenyon and Dana Randall, Dynamic TCP acknowledgment and other stories about e/(e - 1), Algorithmica 36 (2003), 209-224"
    locator: the randomized e/(e - 1 + beta)-competitive algorithm for the Bahncard problem with finite validity T
  - paper: doi:10.1145/380752.380845
    title: "Anna R. Karlin, Claire Kenyon and Dana Randall, Dynamic TCP acknowledgment and other stories about e/(e - 1), Proceedings of the 33rd ACM Symposium on Theory of Computing (2001), 502-509"
    locator: the conference version of the same results
---

In the Bahncard problem, a traveller buys train tickets online and may at any time buy a discount card. The card costs $C$, stays valid for a time $T$, and lowers the price of each ticket from $p$ to $\beta p$, with $0 \le \beta < 1$. Rudolf Fleischer (2001) named it after the German railway's BahnCard, showed that the best deterministic ratio is $2 - \beta$, and showed that no randomized algorithm beats $e/(e - 1 + \beta)$. For $\beta = 0$ and $T = \infty$ it is the [ski rental problem](/ski-rental-problem/).

## In plain words

A railway sells a card that gives a discount on every ticket for one year. The card is not free. If you travel a lot this year, the card pays for itself. If you travel little, it is wasted money. You do not know your future trips, and you must decide before each trip whether to buy the card now.

This is like renting or buying skis, with two changes. The card does not make trips free, only cheaper. And the card runs out, so the decision comes back again and again. A good rule is: look at what you paid at full price in the last year. When that amount reaches the point where a card would have paid for itself, buy a card.

## Definition

**Notation.** $\sigma$ is the request sequence, $\mathrm{ALG}(\sigma)$ and $\mathrm{OPT}(\sigma)$ are the costs of the online algorithm and of the optimal offline solution on $\sigma$, $c$ is the competitive ratio, and $\beta$ is the discount factor.

**The problem $\mathrm{BP}(C, \beta, T)$ (Fleischer 2001).** The parameters are the card price $C > 0$, the discount factor $\beta \in [0, 1)$ and the validity $T \in (0, \infty]$. The input is a sequence of travel requests $\sigma = (t_1, p_1), (t_2, p_2), \ldots, (t_n, p_n)$ with times $t_1 \le t_2 \le \cdots \le t_n$ and regular prices $p_i \ge 0$. When request $i$ arrives, the algorithm may first buy a card, for cost $C$. A card bought at time $t$ is valid in $[t, t + T)$. Then it pays the ticket: $\beta p_i$ if a valid card exists at time $t_i$, and $p_i$ otherwise. An online algorithm decides at request $i$ knowing only the requests $1, \ldots, i$.

**The break-even point.** A card pays for itself on a set of trips with total regular price $P$ when $C + \beta P \le P$, that is when

$$P \ge \gamma = \frac{C}{1 - \beta}.$$

The number $\gamma$ is the break-even point. For $\beta = 0$ it is the card price, as in ski rental.

**The offline optimum.** $\mathrm{OPT}(\sigma)$ chooses the buy times with knowledge of all of $\sigma$. For $T = \infty$, one card bought at the first request covers everything, so $\mathrm{OPT}(\sigma) = \min(P, C + \beta P)$ with $P = \sum_i p_i$. For finite $T$, an optimal solution may buy a card at a request time only, and a dynamic program over the requests computes it.

## Variants

- **Infinite validity, $T = \infty$.** The card never expires. This is a rent-or-buy problem where buying gives a discount, not a free use.
- **Finite validity.** The card expires after $T$, so the decision repeats. The bounds below are the same, but the randomized upper bound needed a new algorithm (Karlin, Kenyon and Randall).
- **Several card types.** Cards with different prices and discounts, or different validities. With several validities and full discount, it is close to the parking permit problem, where permits of several lengths are on sale.
- **With predictions.** The algorithm gets a prediction of the future trips and should do well when it is right and stay bounded when it is wrong. See [learning-augmented algorithms](/learning-augmented-algorithms/).

## Examples

**Infinite validity.** Let $C = 1$, $\beta = 1/2$ and $T = \infty$, so $\gamma = 2$. Each request has price $1/2$. The rule SUM (below) pays the first three tickets at full price, $3/2$ in total. At the fourth request the full-price cost, with the current ticket, reaches $2 = \gamma$, so SUM buys a card and pays $1 + 1/4$.

| requests | SUM | $\mathrm{OPT} = \min(P, 1 + P/2)$ | ratio |
|---|---|---|---|
| 4 | $3/2 + 5/4 = 11/4$ | $2$ | $11/8$ |
| 10 | $11/4 + 6 \cdot 1/4 = 17/4$ | $7/2$ | $17/14$ |

Both ratios are below $2 - \beta = 3/2$.

**Finite validity.** Let $C = 1$, $\beta = 1/2$, $T = 3$, and one request of price 1 at each time $0, 1, 2, 3, 4, 5$. SUM pays 1 at time 0. At time 1 the full-price cost in $(-2, 1]$ with the current ticket is $2 = \gamma$, so it buys a card, valid in $[1, 4)$, and pays $1 + 1/2$. It pays $1/2$ at times 2 and 3. At time 4 the card has expired and the full-price cost in $(1, 4]$ is only the current ticket, so it pays 1. At time 5 the full-price cost in $(2, 5]$ is 2, so it buys again and pays $1 + 1/2$. In total SUM pays 6. The optimum buys cards at times 0 and 3 and pays $2 \cdot (1 + 3/2) = 5$. The ratio is $6/5$.

## Known algorithms

- **SUM (Fleischer 2001).** At a request $(t, p)$ with no valid card, add up the regular prices of the requests in $(t - T, t]$ that were paid at full price, including the current one. If the sum is at least $\gamma$, buy a card and pay $\beta p$; otherwise pay $p$. SUM is the [break-even strategy](/break-even-strategy/) applied to a sliding window of length $T$. It is $(2 - \beta)$-competitive, and Fleischer also gives a variant OSUM. The current request must be in the sum: a rule that adds up only the earlier requests pays $p$ for a single request of large price $p$, against $\mathrm{OPT} = C + \beta p$, and its ratio tends to $1/\beta$.
- **RAND (Fleischer 2001).** A randomized rule for $T = \infty$ that is $e/(e - 1 + \beta)$-competitive against an [oblivious adversary](/oblivious-adversary/).
- **Karlin, Kenyon and Randall (2001).** A randomized rule that is $e/(e - 1 + \beta)$-competitive for every finite $T$, which proves a conjecture of Fleischer.

## Bounds

| algorithm class | lower bound | upper bound |
|---|---|---|
| deterministic, any $T$ | $2 - \beta$ (Fleischer) | $2 - \beta$, SUM (Fleischer) |
| randomized, oblivious adversary, $T = \infty$ | $e/(e - 1 + \beta)$ (Fleischer) | $e/(e - 1 + \beta)$, RAND (Fleischer) |
| randomized, oblivious adversary, finite $T$ | $e/(e - 1 + \beta)$ (Fleischer) | $e/(e - 1 + \beta)$ (Karlin, Kenyon and Randall) |

The bounds depend only on $\beta$, not on $C$ or $T$. For $\beta = 0$ they are 2 and $e/(e-1)$, the ratios of continuous ski rental. For $\beta = 1/2$ they are $3/2$ and $e/(e - 1/2) \approx 1.2254$.

**Upper bound for SUM, $T = \infty$.** For every $\sigma$, $\mathrm{SUM}(\sigma) < (2 - \beta) \cdot \mathrm{OPT}(\sigma)$ when $\mathrm{OPT}(\sigma) > 0$.

*Proof.* Let $P$ be the total regular price. If SUM never buys, the full-price sum stays below $\gamma$ up to the last request, so $P < \gamma$, and SUM pays $P = \mathrm{OPT}(\sigma)$. Otherwise SUM buys at some request $k$. Let $R < \gamma$ be the regular cost of the requests before $k$. SUM pays $R + C + \beta(P - R) = (1 - \beta) R + C + \beta P$. Since $P \ge \gamma$, $\mathrm{OPT} = C + \beta P$. Then

$$(2 - \beta)\,\mathrm{OPT} - \mathrm{SUM} = (1 - \beta)(C + \beta P) - (1 - \beta) R = (1 - \beta)(C + \beta P - R) > 0,$$

because $C + \beta P \ge C + \beta \gamma = \gamma > R$. $\square$

**Deterministic lower bound, $T = \infty$.** Let all requests have a small price $\varepsilon$, and let the adversary stop right after the request where the algorithm buys. Let $x$ be the regular cost the algorithm paid before it buys. As $\varepsilon \to 0$, the algorithm pays $x + C$ and $\mathrm{OPT} = \min(x, C + \beta x)$.

- If $x \le \gamma$, the ratio is $(x + C)/x = 1 + C/x \ge 1 + C/\gamma = 2 - \beta$.
- If $x \ge \gamma$, the ratio is $(x + C)/(C + \beta x)$. Its derivative in $x$ has the sign of $(C + \beta x) - \beta(x + C) = (1 - \beta) C > 0$, so it is at least its value at $x = \gamma$, which is $(\gamma + C)/\gamma = 2 - \beta$.
- If the algorithm never buys, the ratio $P/(C + \beta P)$ tends to $1/\beta$ (or to $\infty$ if $\beta = 0$), and $1/\beta \ge 2 - \beta$ because $(1 - \beta)^2 \ge 0$.

For example, with $C = 1$ and $\beta = 1/2$, SUM on this input has ratio $59/40 = 1.475$ for $\varepsilon = 1/10$ and $1.49975$ for $\varepsilon = 1/1000$. Scaling $C$ and all prices up makes $\mathrm{OPT}$ large, so the bound also holds with an additive constant.

**Randomized bound, continuous version with $T = \infty$.** Take $\gamma = 1$, so $C = 1 - \beta$, and let the prices be infinitesimal, so that the input is the total regular price $P$. A randomized rule buys when its full-price spending reaches a random threshold $x \in [0, 1]$, or never. With density $p(x)$ on $[0, 1]$ and probability $q$ of never buying, it pays $(1 - \beta) x + C + \beta P$ if $P \ge x$, and $P$ otherwise. Requiring $\mathbb{E}[\mathrm{ALG}(P)] = c \cdot P$ for $P \in [0, 1]$ and differentiating twice gives $p(x) = a e^x$ and $(1 - \beta) a + 1 = c$. Requiring $\mathbb{E}[\mathrm{ALG}(P)] = c (C + \beta P)$ for $P \ge 1$ gives $a + a(e - 1) = c$, so $c = a e$. Together,

$$a = \frac{1}{e - 1 + \beta}, \qquad c = \frac{e}{e - 1 + \beta}, \qquad q = \frac{\beta}{e - 1 + \beta}.$$

So the rule never buys with probability $\beta/(e - 1 + \beta)$, and otherwise buys at a threshold with density $e^x/(e - 1 + \beta)$ on $[0, 1]$. Its expected cost is exactly $\tfrac{e}{e - 1 + \beta} \mathrm{OPT}(P)$ for every $P$. The atom at "never" matters: a rule that always buys by $x = 1$ and equalizes only on $[0, 1]$ reaches only $(e - \beta)/(e - 1)$, which is worse for $\beta > 0$. This derivation shows where the constant comes from; Fleischer's RAND and its analysis for general prices are in his paper.

## Reductions

- **Ski rental is a special case.** Set $\beta = 0$, $T = \infty$, $C = B$, and one request of price 1 per day. A card makes all later days free, so it is a pair of skis, and $\mathrm{OPT} = \min(n, B)$. SUM buys when the full-price sum with the current day reaches $B$, which is on day $B$: the [break-even strategy](/break-even-strategy/).
- **Lower bounds from ski rental.** Since ski rental is the case $\beta = 0$, a lower bound for continuous ski rental is a lower bound for $\mathrm{BP}(C, 0, \infty)$. At $\beta = 0$ the Bahncard bounds $2 - \beta$ and $e/(e - 1 + \beta)$ are the ski rental bounds 2 and $e/(e-1)$.
- **TCP acknowledgment.** Karlin, Kenyon and Randall solve the Bahncard problem and the [TCP acknowledgment problem](/tcp-acknowledgment-problem/) with the same method, and get the optimal randomized ratio $e/(e-1)$ for TCP acknowledgment.

## Applications

- **Railway and transit cards.** Discount cards with a yearly price, such as the BahnCard of Deutsche Bahn, are the original motivation.
- **Cloud computing.** Reserved instances or savings plans cost a fixed fee for a period and lower the hourly price; on-demand use is the full price.
- **Subscriptions and memberships.** Any membership that costs a fee and gives a discount for a limited time, for example in shops or for software licences.
- **Teaching.** The problem shows how a ski-rental argument extends to a partial discount and to a sliding time window.

## References
