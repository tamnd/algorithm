---
tag: VEN1KY
kind: algorithm
slug: first-price-auction
name: First-price sealed-bid auction
aliases:
- first-price auction
- pay-your-bid auction
area: algorithmic-game-theory/auctions
level: intro
summary: Each bidder submits one sealed bid, and the highest bidder wins and pays its own bid. Bidders shade their bids below their values, and the equilibrium depends on the prior.
model: word-ram
complexity:
  vars: {n: the number of bidders}
  time: {worst: O(n)}
  space: {extra: O(1)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1961
  people: [William Vickrey]
  note: Sealed tenders that pay the bid are old. Vickrey in 1961 found the equilibrium bids for independent uniform values and showed that the expected revenue equals that of the second-price auction.
prereqs: [quasilinear-utility, independent-private-values, vickrey-auction]
see_also: [first-price-auction-equilibrium, dutch-auction, vickrey-auction, revenue-equivalence-theorem, first-price-auction-price-of-anarchy, all-pay-auction, bayes-nash-equilibrium, reserve-price]
sources:
  - paper: doi:10.1111/j.1540-6261.1961.tb02789.x
    title: "William Vickrey, Counterspeculation, auctions, and competitive sealed tenders, Journal of Finance 16(1) (1961), 8-37"
    locator: the equilibrium of the first-price auction with independent uniform values, and the equal expected revenue of the first-price and second-price auctions
  - book: isbn:9780123745071
    title: Vijay Krishna, Auction Theory, 2nd edition, Academic Press, 2010
    locator: Chapter 2, Section 2.3 (first-price auctions, the symmetric equilibrium and the revenue comparison) and Chapter 4 (risk-averse bidders and asymmetric bidders)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 2, Section 2.3 (first-price auctions, why the bids are hard to reason about)
  - paper: doi:10.1111/1467-937X.00137
    title: "Eric Maskin and John Riley, Asymmetric auctions, Review of Economic Studies 67(3) (2000), 413-438"
    locator: first-price auctions with asymmetric bidders, in which the weak bidder bids more aggressively than the strong one and the outcome need not be efficient
  - paper: doi:10.3982/ECTA15925
    title: "Mohammad Akbarpour and Shengwu Li, Credible auctions, a trilemma, Econometrica 88(2) (2020), 425-467"
    locator: the first-price auction with a reserve is credible, so the auctioneer cannot gain by a hidden deviation, while the second-price auction is not
  - paper: doi:10.1145/3617902
    title: "Yaonan Jin and Pinyan Lu, First price auction is 1 - 1/e^2 efficient, Journal of the ACM 70(5) (2023), article 36"
    locator: the tight bound on the welfare of Bayes-Nash equilibria of first-price auctions with independent values
---

The first-price sealed-bid auction sells one item. Each bidder submits one sealed bid, the highest bid wins, and the winner pays its own bid. A bidder who bids its value gains nothing when it wins, so bidders bid less than their values; this is called *bid shading*. How much to shade depends on the number of bidders and on what each bidder believes about the others, so the auction is studied at a Bayes-Nash equilibrium in the [independent private values](/independent-private-values/) model. It is strategically the same game as the [Dutch auction](/dutch-auction/), and its symmetric equilibrium is derived on the page [equilibrium of the symmetric first-price auction](/first-price-auction-equilibrium/).

## In plain words

Everyone writes a price in an envelope. The highest price wins, and the winner pays what it wrote. If you write what the item is worth to you, you win nothing even when you win, because you pay all of it. So you write less. Writing less gives a better deal when you win but makes you win less often. The best amount depends on how much the others will write, which you do not know. With many rivals you shade only a little, and with few rivals you shade a lot. When everyone thinks this way and the bidders are alike, the item still goes to the one who values it most, and the seller earns on average the same as in the auction where the winner pays the second price.

## The problem

One item is for sale to $n$ bidders with private values $v_i$ and [quasilinear utility](/quasilinear-utility/). The seller sets a reserve $r \ge 0$. The auction receives bids $b_1, \ldots, b_n$ and must choose a winner and a price, with the rule that the winner pays its own bid and losers pay nothing. The algorithmic task is only to run this rule. The strategic question is how the bidders bid: in the model with independent values drawn from known distributions $F_1, \ldots, F_n$, a strategy $\beta_i$ maps values to bids, and the bidders play a [Bayes-Nash equilibrium](/bayes-nash-equilibrium/).

## The algorithm

```pseudo id=main
FIRST-PRICE(b_1, ..., b_n, r)
L1  w ← NIL
L2  for i ← 1 to n:
L3      if b_i ≥ r and (w = NIL or b_i > b_w): w ← i
L4  if w = NIL: return NIL, 0                         ▷ no bid reaches the reserve
L5  return w, b_w                                     ▷ w wins and pays its own bid
```

Ties go to the smallest index, because line L3 needs a strictly larger bid to change the leader. With values drawn from distributions without atoms, the equilibrium bids tie with probability 0, so the tie rule does not change the equilibrium.

The implementation also gives the symmetric equilibrium bid for values with CDF $F(v) = v^a$ on $[0, 1]$, which is $\beta(v) = \frac{a(n-1)}{a(n-1)+1} v$, and the exact expected utility of a bidder who bids as another type. The tests use them to check the equilibrium by best response.

## Example

Three bidders bid $(10, 7, 3)$. Bidder 1 wins and pays 10. If its value is 10, its utility is 0. With the bid 8 it still wins and its utility is 2. So truthful bidding is not a dominant strategy here, unlike in the [Vickrey auction](/vickrey-auction/).

Now let the values be independent and uniform on $[0, 1]$. In the symmetric equilibrium each bidder bids $\beta(v) = \frac{n-1}{n} v$.

| bidders $n$ | bid at value $v$ | bid at $v = 0.8$ | expected revenue |
|---|---|---|---|
| 2 | $v/2$ | 0.4 | $1/3$ |
| 3 | $2v/3$ | 0.533 | $1/2$ |
| 5 | $4v/5$ | 0.64 | $2/3$ |

With $n = 2$ and value $0.8$, a bid $b \le 1/2$ wins when the other value $w$ has $w/2 < b$, with probability $2b$. The expected utility is $(0.8 - b) \cdot 2b$. It is $0.32$ at the equilibrium bid $0.4$, and $0.30$ at the bids $0.3$ and $0.5$. The expected revenue $(n-1)/(n+1)$ is the mean of the second-highest value, the same as in the Vickrey auction.

With asymmetric bidders the first-price auction can give the item to the wrong bidder. Let bidder 1 have a value uniform on $[0, 1]$ and bidder 2 a value uniform on $[0, 2]$. The equilibrium has the inverse bid functions $v_1(b) = 8b/(4 + 3b^2)$ and $v_2(b) = 8b/(4 - 3b^2)$ on $[0, 2/3]$. At the value 1, the weak bidder 1 bids $2/3$ and the strong bidder 2 bids about $0.43$. The weak bidder bids more aggressively, and it wins in some cases where bidder 2 has the higher value. By numerical integration, this happens with probability about $0.083$, and the expected welfare is about $1.0628$ against the optimum $13/12 \approx 1.0833$.

## Correctness

The proof is in `proofs/correctness.md`. It shows three facts.

- **The outcome.** The loop keeps the first highest eligible bid, and line L5 charges it its own bid.
- **The equilibrium for values $v^a$.** If the others bid $\beta(t) = \frac{k}{k+1} t$ with $k = a(n-1)$, a bidder of value $v$ who bids $\beta(t)$ gets $u(v, t) = (v - \beta(t)) t^k$. Its derivative in $t$ is $k t^{k-1}(v - t)$, so the best $t$ is $v$. Bids above $\beta(1)$ are worse than $\beta(1)$. So $\beta$ is a symmetric Bayes-Nash equilibrium.
- **Revenue.** With uniform values the price is $\frac{n-1}{n}$ times the highest value, whose mean is $\frac{n}{n+1}$, so the expected revenue is $\frac{n-1}{n+1}$.

The general symmetric equilibrium is $\beta(v) = \mathbb{E}[Y_1 \mid Y_1 < v]$, with $Y_1$ the highest of the other $n - 1$ values ([equilibrium of the symmetric first-price auction](/first-price-auction-equilibrium/)).

## Complexity

One pass over the bids with at most two comparisons per bid: $\Theta(n)$ time and $O(1)$ extra space. The rule is as cheap as the Vickrey auction. The cost of the first-price auction is on the side of the bidders: to bid well, a bidder must know or estimate the distribution of the others' bids. For symmetric bidders the equilibrium has the closed form above. For asymmetric bidders it solves a system of differential equations with a free end point, which has a closed form only in special cases, such as the uniform example.

## Properties

- **Not DSIC.** The best bid depends on the others' bids. A bid at or above the value never gives a positive utility.
- **Efficient with symmetric bidders.** The symmetric equilibrium bid is strictly increasing, so the highest value wins.
- **Inefficient with asymmetric bidders.** The example above has a welfare loss of about $1.9\%$. In every Bayes-Nash equilibrium with independent values, the expected welfare is at least $1 - 1/e^2 \approx 0.865$ of the optimum, and this bound is tight ([price of anarchy of first-price auctions](/first-price-auction-price-of-anarchy/)).
- **Revenue.** With symmetric, independent, risk-neutral bidders, the expected revenue equals that of the Vickrey auction ([revenue equivalence theorem](/revenue-equivalence-theorem/)). With risk-averse bidders the first-price auction earns more, because a risk-averse bidder shades less to win more surely (Krishna, Chapter 4).
- **Credible.** The winner pays its own bid, so the seller cannot raise the price by a fake bid. The second-price auction does not have this property (Akbarpour and Li 2020).
- **Equivalent to the Dutch auction.** A bidder in a [Dutch auction](/dutch-auction/) chooses the price at which to stop the falling clock, learns nothing useful before that, and pays that price. So a Dutch strategy is a first-price bid.

## Variants and improvements

- **Reserve price.** With a reserve $r$, a bidder with value below $r$ does not bid, and a bidder with value $v \ge r$ bids $\mathbb{E}[\max(Y_1, r) \mid Y_1 < v]$ in the symmetric equilibrium. With uniform values and the reserve $1/2$, the first-price auction earns the same as the Vickrey auction with the same reserve, which is optimal ([reserve price](/reserve-price/)).
- **Procurement.** In a reverse auction, the lowest bid wins and is paid its bid. This is the sealed tender of public procurement.
- **Many identical units.** The *discriminatory* or pay-as-bid auction gives units to the highest bids, and each winner pays its bids. Treasury bills are sold this way in some countries.
- **Advertising.** Display advertising exchanges moved from second-price to first-price auctions around 2019. Then each buyer must shade its bids, and bid-shading programs learn the distribution of the highest other bid.
- **All-pay.** In the [all-pay auction](/all-pay-auction/) every bidder pays its bid, and the highest still wins.

## When to use it

Use the first-price auction when the seller must be trusted by the bidders (the price is the winner's own bid), when the bidders are risk averse, or when a sealed one-shot sale is needed. It is the standard form for public tenders. It is a poor choice when the bidders are very unequal, because then it can give the item to the wrong bidder, and when simple bidding matters more than revenue, because bidders must guess the others' behaviour.

## Pitfalls

- **Bidding the value.** It gives utility 0 in every case. A bidder must shade.
- **The equilibrium depends on $n$ and on the prior.** The bid $\frac{n-1}{n}v$ is right only for $n$ symmetric uniform bidders. With $F(v) = v^2$ and two bidders the bid is $\frac{2}{3}v$, not $\frac{1}{2}v$.
- **Discrete values have no pure equilibrium.** With two bidders whose values are 0 or 1 with probability $1/2$ each, no pure strategy profile is an equilibrium: a bidder of value 1 who bids $b$ wants to bid just above $b$. The equilibrium is mixed, with bids on $[0, 1/2]$ (see [the equilibrium page](/first-price-auction-equilibrium/)).
- **Asymmetry.** The symmetric formula is wrong for asymmetric bidders. Each bidder's bid depends on all the distributions.
- **Ties in tests.** A test that runs the auction on equilibrium bids must use distributions without atoms or handle ties by the rule of line L3.

## Implementations

## History

Sealed tenders in which the lowest bid wins and is paid its price are old, and governments use them for contracts and for the sale of bonds. Vickrey (1961) found the equilibrium of the first-price auction for independent uniform values and showed that its expected revenue equals that of the second-price auction. Riley and Samuelson (1981) and Myerson (1981) proved the general revenue equivalence. Maskin and Riley (2000) studied the asymmetric case and showed that the weak bidder bids more aggressively. Syrgkanis and Tardos (2013) proved that every equilibrium keeps at least $1 - 1/e$ of the optimal welfare, and Jin and Lu (2022) found the tight bound $1 - 1/e^2$.

## References
