---
tag: VMDH3M
kind: algorithm
slug: myerson-optimal-auction
name: Myerson's optimal auction
aliases:
- Myerson auction
- revenue-optimal auction
area: algorithmic-game-theory/auctions
level: core
summary: Gives the item to the bidder with the highest nonnegative ironed virtual value and charges threshold prices. It maximizes expected revenue for independent private values.
model: word-ram
complexity:
  vars: {n: the number of bidders, N: the total support size of the value distributions, K: the largest support size of one bidder}
  time: {worst: O(N + n K)}
  space: {extra: O(N)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1981
  people: [Roger B. Myerson]
  note: Myerson characterized the revenue-optimal single-item auction for independent private values, with ironing for irregular distributions. Riley and Samuelson found the optimal reserve for symmetric bidders in the same year, and Bulow and Roberts (1989) read the virtual value as a marginal revenue.
prereqs: [virtual-valuation, myerson-lemma, independent-private-values]
see_also: [ironing, regular-distribution, reserve-price, vickrey-auction, bulow-klemperer-theorem, sequential-posted-pricing, revenue-equivalence-theorem, sample-complexity-of-revenue-maximization]
sources:
  - paper: doi:10.1287/moor.6.1.58
    title: "Roger B. Myerson, Optimal auction design, Mathematics of Operations Research 6(1) (1981), 58-73"
    locator: the revenue of an incentive compatible mechanism as expected virtual surplus, the optimal auction for regular distributions, and the ironing of the virtual valuation in the general case
  - paper: "John G. Riley and William F. Samuelson, Optimal auctions, American Economic Review 71(3) (1981), 381-392"
    locator: the optimal reserve price for symmetric bidders and its independence of the number of bidders
  - paper: doi:10.1086/261643
    title: "Jeremy Bulow and John Roberts, The simple economics of optimal auctions, Journal of Political Economy 97(5) (1989), 1060-1090"
    locator: the virtual value as the marginal revenue of a monopolist, and the optimal auction as the sale to the bidder of highest marginal revenue
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 5, Revenue-maximizing auctions, Section 5.2 (expected revenue equals expected virtual welfare, and the optimal auction for regular distributions)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 13, Jason D. Hartline and Anna R. Karlin, Profit maximization in mechanism design (the Bayesian optimal mechanism and virtual values)
  - paper: "Jason D. Hartline, Mechanism Design and Approximation, book draft, version with Chapters 1 to 7 revised in September 2021, https://jasonhartline.com/MDnA/"
    locator: Chapter 3, Optimal mechanisms (revenue curves in quantile space, virtual values as their slopes, and ironing by the concave hull)
---

Myerson's optimal auction sells one item to bidders whose private values are drawn independently from known distributions, and it earns the largest expected revenue of all mechanisms in which bidders report truthfully and never lose by taking part. It maps each bid $b_i$ to its *ironed* [virtual value](/virtual-valuation/) $\bar\varphi_i(b_i)$, gives the item to the bidder with the largest one if that value is nonnegative, and charges the winner the smallest bid with which it would still win. It is a revenue result built on [Myerson's lemma](/myerson-lemma/). The lemma says which allocation rules can be made truthful in any [single-parameter environment](/single-parameter-environment/) and fixes their payments. This auction uses the lemma and the prior to choose the rule that maximizes expected revenue.

## In plain words

A seller has one item and several bidders. The seller does not know what the bidders will pay, but knows from past sales how likely each amount is for each bidder. Selling to the highest bidder is not always best for the seller. A bidder who is likely to bid low is worth less to the seller, because a higher price for that bidder would lose many sales but gain little. The auction corrects each bid for this effect and gets an adjusted bid. The item goes to the highest adjusted bid, and only if that adjusted bid is not negative, so sometimes the seller keeps the item. The winner pays the lowest bid with which it would still have won. So no bidder gains by lying about its value.

## The problem

There are $n$ bidders and one item. Bidder $i$ has a private value $v_i$ drawn from a distribution $F_i$, and the draws are independent ([independent private values](/independent-private-values/)). Utilities are quasilinear: a bidder who wins with probability $x_i$ and pays $p_i$ gets $v_i x_i - p_i$. The seller knows $F_1, \ldots, F_n$ and wants a mechanism that is [DSIC](/dominant-strategy-incentive-compatibility/), or at least [BIC](/bayesian-incentive-compatibility/), and [individually rational](/individual-rationality/), with the largest expected revenue $\mathbb{E}[\sum_i p_i]$.

For a continuous $F$ with density $f$ the virtual value is $\varphi(v) = v - (1 - F(v))/f(v)$. For a discrete $F$ on $s_1 < \cdots < s_K$ with probabilities $f_k$ and $q_k = \Pr[v \ge s_k]$, it is $\varphi(s_k) = (s_k q_k - s_{k+1} q_{k+1})/f_k$, with $s_{K+1} q_{K+1} = 0$. In both cases it is the slope of the revenue curve $q \mapsto q \cdot F^{-1}(1 - q)$, the revenue of a posted price that sells with probability $q$. The ironed virtual value $\bar\varphi$ is the slope of the concave hull of that curve ([ironing](/ironing/)). For a [regular distribution](/regular-distribution/) the curve is already concave and $\bar\varphi = \varphi$.

## The algorithm

The implementation takes discrete distributions, so every value and payment is an exact fraction, and bids must lie in the bidder's support.

```pseudo id=main
MYERSON(F_1, ..., F_n, b_1, ..., b_n)
L1  for each bidder i: φ̄_i ← slopes of the concave hull of the revenue curve of F_i
L2  for each bidder i: c_i ← φ̄_i(b_i)
L3  if c_i < 0 for every i: return no sale, all payments 0
L4  w ← the smallest index i with c_i maximal
L5  p_w ← the smallest s in the support of F_w with which w would still win; p_i ← 0 for i ≠ w
L6  return w, p
```

Line L1 depends only on the distributions and can be done once for many auctions. Line L4 breaks ties by index, a fixed rule, which keeps the allocation monotone in each bid. In line L5, "would still win" means that $\bar\varphi_w(s) \ge 0$, that $\bar\varphi_w(s) > c_j$ for each $j < w$ and that $\bar\varphi_w(s) \ge c_j$ for each $j > w$, with the other bids fixed. For continuous regular distributions with strictly increasing $\varphi_i$, line L5 is $p_w = \varphi_w^{-1}(\max(0, \max_{j \ne w} c_j))$.

## Example

**Uniform values.** For $v_i$ drawn from $U[0, 1]$, $\varphi(v) = 2v - 1$, so the auction is the [Vickrey auction](/vickrey-auction/) with [reserve price](/reserve-price/) $1/2$. One bidder faces the posted price $1/2$ and the revenue is $1/4$. With two bidders the revenue is $\mathbb{E}[\max(0, 2\max(v_1, v_2) - 1)] = 5/12$, more than the $1/3$ of the Vickrey auction without reserve. With bids $(0.8, 0.6)$ bidder 1 wins and pays $0.6$, with bids $(0.8, 0.3)$ it pays the reserve $0.5$, and with bids $(0.4, 0.3)$ the item is not sold.

**An irregular distribution.** Two bidders have values in $\{2, 3, 5\}$ with probabilities $1/2, 1/6, 1/3$. Then $q = (1, 1/2, 1/3)$ and the revenue curve has the points $(0, 0)$, $(1/3, 5/3)$, $(1/2, 3/2)$ and $(1, 2)$. The virtual values are $\varphi = (1, -1, 5)$, which is not monotone, so the distribution is not regular. The point $(1/2, 3/2)$ lies below the chord from $(1/3, 5/3)$ to $(1, 2)$, whose slope is $1/2$. So the ironed virtual values are $\bar\varphi = (1/2, 1/2, 5)$: the values 2 and 3 are treated as equal.

| bids $(b_1, b_2)$ | $(c_1, c_2)$ | winner | payment |
|---|---|---|---|
| $(2, 2)$, $(2, 3)$, $(3, 2)$, $(3, 3)$ | $(1/2, 1/2)$ | 1 (tie) | 2 |
| $(5, 2)$ or $(5, 3)$ | $(5, 1/2)$ | 1 | 2 |
| $(2, 5)$ or $(3, 5)$ | $(1/2, 5)$ | 2 | 5 |
| $(5, 5)$ | $(5, 5)$ | 1 (tie) | 5 |

With bids $(2, 3)$ the bidder with the lower bid wins, because both bids have the same ironed virtual value and the tie goes to bidder 1. With bids $(5, 3)$ bidder 1 pays only 2, since it would win the tie with the bid 2. Bidder 2 needs $\bar\varphi > 1/2$ to beat bidder 1, so it pays 5. The expected revenue is $3$, which equals $\mathbb{E}[\max(0, \bar\varphi_1(v_1), \bar\varphi_2(v_2))]$. The Vickrey auction earns $89/36 \approx 2.47$ here, and with reserve 5 it earns $25/9 \approx 2.78$.

## Correctness

The proof is in `proofs/correctness.md`. It has three parts.

- **Truthful.** The ironed virtual value is nondecreasing in the bid, so the allocation is monotone, and the payment is the threshold bid. By [Myerson's lemma](/myerson-lemma/) this is DSIC, and a truthful bidder never pays more than its value, so it is ex post IR.
- **Revenue identity.** For any monotone rule with threshold payments, an exchange of sums (or an integration by parts) gives $\mathbb{E}[p_i] = \mathbb{E}[x_i(v) \varphi_i(v_i)]$. Since the auction decides only through $\bar\varphi$, its allocation is constant where the revenue curve lies strictly below its hull, and then $\varphi$ can be replaced by $\bar\varphi$. So the revenue is $\mathbb{E}[\max(0, \max_i \bar\varphi_i(v_i))]$.
- **Optimal.** Any BIC and interim IR mechanism, randomized or not, has a nondecreasing interim allocation and payments at most the threshold sum. Its revenue is at most $\mathbb{E}[\sum_i x_i \bar\varphi_i] \le \mathbb{E}[\max(0, \max_i \bar\varphi_i)]$, because $\bar R \ge R$ and at most one bidder gets the item.

## Complexity

Line L1 builds one hull per bidder by the monotone chain method in time linear in its support size, so $O(N)$ in total for supports given in sorted order, and stores $O(N)$ slopes. One auction then takes $O(n)$ for lines L2 to L4 and at most $K$ checks in line L5. With an $O(n)$ check this is $O(nK)$. With the largest $c_j$ of the bidders before $w$ and after $w$ computed once, each check is $O(1)$ and the run takes $O(n + K)$. For continuous regular distributions given by $\varphi_i$ and its inverse, one run takes $O(n)$ evaluations.

## Properties

- **Optimal among BIC mechanisms, with a DSIC implementation.** No mechanism with truthful Bayes-Nash equilibrium and interim IR earns more, and this one is DSIC and ex post IR.
- **Deterministic.** The optimum needs no randomization in this single-item setting, unlike the multi-item case ([selling separately or as a bundle](/simple-versus-optimal-multi-item/)).
- **Symmetric case.** If all bidders have the same regular distribution, the auction is the Vickrey auction with the reserve $\varphi^{-1}(0)$, which does not depend on $n$.
- **Asymmetric case.** With different distributions the winner need not have the highest bid. For example, with $v_1$ from $U[0, 1]$ and $v_2$ from $U[0, 2]$, $\varphi_1(v) = 2v - 1$ and $\varphi_2(v) = 2v - 2$, so bids $(0.9, 1.3)$ give the item to bidder 1.
- **Not efficient.** It keeps the item, or sells to a lower bidder, even when that loses welfare.

## Variants and improvements

- **Single-parameter environments.** The same proof applies whenever the feasible sets of winners are known: maximize the ironed virtual surplus $\sum_i x_i \bar\varphi_i(v_i)$ over feasible $x$ at each profile. For $k$ identical items this sells to the up to $k$ highest nonnegative ironed virtual values.
- **Simple approximations.** The [Vickrey auction](/vickrey-auction/) with one more bidder beats the optimal auction for i.i.d. regular values ([Bulow-Klemperer theorem](/bulow-klemperer-theorem/)). [Sequential posted pricing](/sequential-posted-pricing/) earns at least a $1 - 1/e$ fraction of the optimum for any independent values.
- **Unknown distributions.** When $F_i$ is known only through samples, one runs the auction on an empirical estimate ([sample complexity of revenue maximization](/sample-complexity-of-revenue-maximization/)).
- **Multiple items.** For one buyer with additive values for two or more items, no comparably simple optimal mechanism is known, and the optimum may need randomization.

## When to use it

Use it when one item, or a single-parameter allocation, must be sold for revenue, the values are independent, and the seller trusts its prior. It is the benchmark against which simpler auctions are measured. When the prior is unknown or doubtful, or when the bidders are asymmetric and an auction that sells to a lower bid would be unacceptable, a Vickrey auction with reserves or a posted price scheme is often preferred at a small loss.

## Pitfalls

- **No ironing.** Using the raw $\varphi$ for an irregular distribution gives a rule that is not monotone. In the example above, a bidder with value 3 would have $\varphi = -1$ and lose, but with the bid 2 it would have $\varphi = 1$ and win. It would gain by bidding lower.
- **The reserve for asymmetric bidders.** Each bidder has its own reserve $\bar\varphi_i^{-1}(0)$, and a single reserve for all is in general not optimal.
- **Correlated values.** With correlated values the optimal revenue can be much higher, up to the full welfare in the setting of the [Crémer-McLean theorem](/cremer-mclean-theorem/), and this auction is no longer optimal.
- **The tie rule must be fixed.** A tie rule that depends on the winner's own bid in other ways can break monotonicity. A random tie rule that does not depend on the bids gives the same expected revenue.
- **Exact arithmetic.** The hull test and the comparisons with $0$ decide the outcome, so they should be done in exact arithmetic for discrete distributions.

## Implementations

## History

Myerson (1981) wrote the revenue of any incentive compatible mechanism as the expected virtual surplus and so turned revenue maximization into a pointwise maximization. For distributions where $\varphi$ is not monotone he introduced the ironing procedure. In the same year Riley and Samuelson showed that, for symmetric bidders, the standard auctions with the right reserve are optimal and that this reserve does not depend on the number of bidders. Bulow and Roberts (1989) explained the result through the revenue curve of a monopolist: the virtual value is a marginal revenue, and the auction sells to the bidder of highest marginal revenue. Myerson shared the 2007 Nobel Memorial Prize in Economic Sciences for the foundations of mechanism design.

## References
