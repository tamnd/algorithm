---
tag: 0NEMPZ
kind: theorem
slug: bulow-klemperer-theorem
name: Bulow-Klemperer theorem
aliases:
- competition beats reserve prices
area: algorithmic-game-theory/auctions
level: core
summary: "For i.i.d. regular values, the Vickrey auction with n + 1 bidders and no reserve earns at least as much as the optimal auction with n bidders."
prereqs: [vickrey-auction, myerson-optimal-auction, regular-distribution]
see_also: [reserve-price, virtual-valuation, myerson-lemma, english-auction, independent-private-values, revenue-equivalence-theorem, sample-complexity-of-revenue-maximization, ironing]
sources:
  - paper: "Jeremy Bulow and Paul Klemperer, Auctions versus negotiations, American Economic Review 86(1) (1996), 180-194"
    locator: Theorem 1 (an English auction with no reserve and one more bidder earns more than any mechanism with the original bidders, for i.i.d. values with increasing marginal revenue)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 6, Simple near-optimal auctions, Section 6.4 (prior-independent mechanisms, with the statement and proof of the Bulow-Klemperer theorem)
  - paper: "Jason D. Hartline, Mechanism Design and Approximation, book draft, version with Chapters 1 to 7 revised in September 2021, https://jasonhartline.com/MDnA/"
    locator: Chapter 5, Prior-independent approximation (the Bulow-Klemperer theorem and its use for prior-independent mechanisms)
  - paper: doi:10.1287/moor.6.1.58
    title: "Roger B. Myerson, Optimal auction design, Mathematics of Operations Research 6(1) (1981), 58-73"
    locator: the expected revenue of an incentive compatible mechanism as the expected virtual surplus, and the optimal auction for regular values
  - paper: doi:10.1086/261643
    title: "Jeremy Bulow and John Roberts, The simple economics of optimal auctions, Journal of Political Economy 97(5) (1989), 1060-1090"
    locator: the interpretation of the virtual valuation as marginal revenue, used in the argument of Bulow and Klemperer
---

The Bulow-Klemperer theorem compares two ways to raise the revenue of an auction. One is to know the value distribution and set the optimal [reserve price](/reserve-price/). The other is to find one more bidder and run the [Vickrey auction](/vickrey-auction/) with no reserve. For bidders with i.i.d. [regular](/regular-distribution/) values, the second way always wins: the Vickrey auction with $n + 1$ bidders earns at least as much as [Myerson's optimal auction](/myerson-optimal-auction/) with $n$ bidders. Bulow and Klemperer proved it in 1996 to compare auctions with negotiations. In algorithmic game theory it is the first example of a prior-independent guarantee, since the Vickrey auction does not use the distribution at all.

## Statement

Let $n \ge 1$. The values of the bidders are i.i.d. draws from a distribution $F$ on an interval $[a, b]$ with $0 \le a < b \le \infty$, a positive density $f$ and a finite mean. Assume $F$ is regular, that is, its [virtual valuation](/virtual-valuation/) $\varphi(v) = v - (1 - F(v))/f(v)$ is nondecreasing. Then

$$\mathbb{E}\big[\text{revenue of the Vickrey auction with } n + 1 \text{ bidders}\big] \;\ge\; \mathbb{E}\big[\text{revenue of the optimal auction with } n \text{ bidders}\big].$$

Here the Vickrey auction has no reserve, and the optimal auction is the revenue-maximizing mechanism among all dominant-strategy incentive compatible and individually rational mechanisms, deterministic or randomized. By Myerson's theorem this optimum is the Vickrey auction with the reserve $\varphi^{-1}(0)$, and no Bayesian incentive compatible mechanism earns more. In the [independent private values](/independent-private-values/) model the [English auction](/english-auction/) earns the same as the Vickrey auction, which is the form in which Bulow and Klemperer state the result.

## In plain words

A seller who knows the bidders' value distribution can compute the best reserve price and earn the most possible from the bidders who came. A seller who knows nothing can run a plain second-price auction. The theorem says the seller who knows nothing but brings in one more bidder of the same kind earns at least as much. So more competition is worth more than perfect knowledge of the market, when the values are drawn independently from one regular distribution. The reason is that a plain auction with one more bidder can copy the optimal auction on the old bidders and still has one bidder left to sell to.

## Proof

The proof uses two facts about a mechanism with allocation rule $x_i(v) \in [0, 1]$ and payment rule $p_i(v)$ for a value profile $v$.

**Revenue is virtual surplus.** By [Myerson's lemma](/myerson-lemma/), for every dominant-strategy incentive compatible and individually rational mechanism,

$$\mathbb{E}\Big[\sum_i p_i(v)\Big] = \mathbb{E}\Big[\sum_i \varphi(v_i)\, x_i(v)\Big] - \sum_i \mathbb{E}_{v_{-i}}\big[u_i(a, v_{-i})\big] \le \mathbb{E}\Big[\sum_i \varphi(v_i)\, x_i(v)\Big],$$

where $u_i(a, v_{-i}) \ge 0$ is the utility of bidder $i$ when its value is the lowest value $a$. This is the identity on the [virtual valuation](/virtual-valuation/) page, with the utility of the lowest type kept.

**Step 1: the Vickrey auction is optimal among auctions that always sell.** Fix $n + 1$ bidders, and let $M$ be a dominant-strategy incentive compatible and individually rational mechanism that always sells the item, so $\sum_i x_i(v) = 1$ for every $v$. Then $\sum_i \varphi(v_i)\, x_i(v)$ is an average of the numbers $\varphi(v_i)$, so it is at most $\max_i \varphi(v_i)$, and the revenue of $M$ is at most $\mathbb{E}[\max_i \varphi(v_i)]$. The Vickrey auction gives the item to the bidder with the highest value. Since $\varphi$ is nondecreasing, this bidder also has the highest virtual value, so the Vickrey auction attains $\max_i \varphi(v_i)$ for every $v$. A bidder with value $a$ wins only on a tie, which has probability 0, so its utility is 0 and the inequality above is an equality. Hence the Vickrey auction earns exactly $\mathbb{E}[\max_i \varphi(v_i)]$, which is at least the revenue of $M$.

**Step 2: an auction with $n + 1$ bidders that always sells and earns the optimal revenue for $n$ bidders.** Let $\mathrm{OPT}_n$ be the optimal auction for bidders $1, \ldots, n$. Define the mechanism $M$ for $n + 1$ bidders as follows. Run $\mathrm{OPT}_n$ on the bids of bidders $1, \ldots, n$. If it sells the item, stop. If not, give the item to bidder $n + 1$ at the price $a$. For bidders $1, \ldots, n$ the mechanism is $\mathrm{OPT}_n$, so truthful bidding is a dominant strategy for them and they get nonnegative utility. The outcome of bidder $n + 1$ does not depend on its bid, and it pays $a$, which is at most its value. So $M$ is dominant-strategy incentive compatible and individually rational, and it always sells. Its expected revenue is the revenue of $\mathrm{OPT}_n$ plus $a$ times the probability that $\mathrm{OPT}_n$ does not sell, so it is at least the revenue of $\mathrm{OPT}_n$.

By Step 1 applied to $M$, the Vickrey auction with $n + 1$ bidders earns at least the revenue of $M$, which is at least the optimal revenue with $n$ bidders. $\blacksquare$

**Check.** For $F = U[0, 1]$ and $n = 2$, the Vickrey auction with three bidders earns the expected second-highest of three values, $1/2$. The optimal auction with two bidders is the Vickrey auction with reserve $1/2$, which earns $5/12$. For $n = 1$, the Vickrey auction with two bidders earns $1/3$ and the best posted price earns $1/4$. For the exponential distribution with mean 1, the best posted price to one bidder is 1 and earns $1/e \approx 0.368$, and the Vickrey auction with two bidders earns the expected minimum of two values, $1/2$.

## Consequences

- **Competition is worth more than knowledge.** A seller who can recruit one more bidder does not need to learn the distribution. This is the base of prior-independent mechanism design, where one auction must do well for every distribution in a class. The single-sample result of Dhangwatnotai, Roughgarden and Yan, in which a price equal to one sample from the distribution earns half of the optimal revenue from a regular buyer, follows the same idea (see [sample complexity of revenue maximization](/sample-complexity-of-revenue-maximization/)).
- **The Vickrey auction with the same bidders is near optimal.** For $n \ge 2$ i.i.d. regular bidders, the Vickrey auction with no reserve earns at least $(n - 1)/n$ of the optimal revenue. The optimal revenue with $n$ bidders is $\mathbb{E}[\max(0, \max_i \varphi(v_i))]$. If one bidder chosen uniformly at random is removed, the bidder with the largest term stays with probability $(n - 1)/n$, so the optimal revenue with $n - 1$ bidders is at least $(n - 1)/n$ of it. The theorem gives that the Vickrey auction with $n$ bidders earns at least the optimal revenue with $n - 1$ bidders.
- **Many identical items.** With $k$ identical items and unit-demand bidders, the same two steps show that the Vickrey auction with $n + k$ bidders, which charges the $(k+1)$st highest bid, earns at least the optimal revenue with $n$ bidders. In Step 2, the items that the optimal auction does not sell go to the $k$ extra bidders.
- **Auctions against negotiations.** The original form of the result: an auction with no reserve and one more bidder is better for the seller than any negotiation or mechanism with the original bidders, so the seller should spend effort on attracting bidders, not on bargaining.

## Tightness

- **Regularity is needed.** Let $F$ be the mixture that draws from $U[0, 1]$ with probability $1 - p$ and from $U[h, h + 1]$ with probability $p$, with $h = 1/p^2$. This $F$ is not regular. (It also has a gap in its support. A small density spread over the gap removes the gap and changes the numbers below only a little.) One bidder facing the price $h$ buys with probability $p$, so the optimal revenue with one bidder is at least $hp = 1/p$. The Vickrey auction with two bidders earns at most $h + 1$ when both values are high, which has probability $p^2$, and at most 1 otherwise, so it earns at most $2 + p^2$. For small $p$ one extra bidder is far from enough. The proof breaks at Step 1, where the bidder with the highest value need not have the highest virtual value.
- **Identical distributions are needed.** If the bidders have different regular distributions, the highest bidder need not have the highest virtual value, and Step 1 fails again. The extra bidder must also be drawn from $F$: an extra bidder with value 0 adds nothing.
- **The extra bidder is needed.** With $n = 1$ and no extra bidder, the Vickrey auction with no reserve has no competing bid and earns nothing for $U[0, 1]$, while the optimal revenue is $1/4$.

## History

Myerson (1981) and Riley and Samuelson (1981) found the optimal auction for i.i.d. values, a second-price or English auction with a reserve price that does not depend on the number of bidders. Bulow and Roberts (1989) explained this result with the language of marginal revenue. Bulow and Klemperer (1996), in "Auctions versus negotiations", asked how much the optimal reserve is worth and showed that one more bidder is always worth more. Their proof uses the marginal revenue view. Kirkegaard (2006) gave a short proof. The argument above, which shows that the Vickrey auction is the optimal auction that always sells, is the one given in the texts of Roughgarden and Hartline, where the theorem opens the study of prior-independent mechanisms.

## References
