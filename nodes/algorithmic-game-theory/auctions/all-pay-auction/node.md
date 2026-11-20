---
tag: HC5JY0
kind: algorithm
slug: all-pay-auction
name: All-pay auction
aliases:
- all-pay contest
area: algorithmic-game-theory/auctions
level: core
summary: Each bidder submits one sealed bid, the highest bid wins, and every bidder pays its bid, win or lose. It models contests, lobbying and races in which effort is spent before the winner is known.
model: word-ram
complexity:
  vars: {n: the number of bidders}
  time: {worst: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1989
  people: [Arye L. Hillman, John G. Riley, Michael R. Baye, Dan Kovenock, Casper G. de Vries]
  note: Hillman and Riley used the all-pay auction in 1989 as a model of political rent seeking, and Baye, Kovenock and de Vries characterized all its equilibria with complete information in 1996.
prereqs: [quasilinear-utility, nash-equilibrium, independent-private-values, first-price-auction, revenue-equivalence-theorem]
see_also: [revenue-equivalence-theorem, first-price-auction, vickrey-auction, first-price-auction-equilibrium, mixed-strategy, bayes-nash-equilibrium, indifference-principle, independent-private-values]
sources:
  - paper: doi:10.1111/j.1468-0343.1989.tb00003.x
    title: "Arye L. Hillman and John G. Riley, Politically contestable rents and transfers, Economics and Politics 1(1) (1989), 17-39"
    locator: the all-pay auction as a model of rent seeking, its mixed equilibrium with known values and the dissipation of the rent
  - paper: doi:10.1007/BF01211819
    title: "Michael R. Baye, Dan Kovenock and Casper G. de Vries, The all-pay auction with complete information, Economic Theory 8(2) (1996), 291-305"
    locator: the full set of Nash equilibria of the all-pay auction with known values, unique when the second-highest value is strictly larger than the third
  - book: isbn:9780123745071
    title: Vijay Krishna, Auction Theory, 2nd edition, Academic Press, 2010
    locator: Chapter 3, Section 3.2 (applications of revenue equivalence to unusual auctions, among them the all-pay auction and the war of attrition)
  - paper: doi:10.3982/ECTA7537
    title: "Ron Siegel, All-pay contests, Econometrica 77(1) (2009), 71-92"
    locator: the equilibrium payoffs of a general class of all-pay contests with complete information
  - paper: doi:10.1007/s10683-014-9421-0
    title: "Emmanuel Dechenaux, Dan Kovenock and Roman M. Sheremeta, A survey of experimental research on contests, all-pay auctions and tournaments, Experimental Economics 18(4) (2015), 609-669"
    locator: laboratory evidence that subjects in all-pay auctions bid more in total than the equilibrium predicts
---

In an all-pay auction every bidder submits one sealed bid, the highest bid wins the item, and every bidder pays its own bid, also the losers. It models situations in which effort or money is spent before the winner is known: lobbying for a license, a race for a patent, a sports tournament or a crowdsourcing contest. With [independent private values](/independent-private-values/) the [revenue equivalence theorem](/revenue-equivalence-theorem/) applies, so the all-pay auction earns the same expected revenue as the [first-price auction](/first-price-auction/) and the [Vickrey auction](/vickrey-auction/), and its equilibrium bid can be read off from the Vickrey payments. With known values it has no pure equilibrium, and the bidders mix.

## In plain words

Everyone writes a price in an envelope. The highest price wins the item, but everyone pays what they wrote, also those who lose. So a bid is a cost you pay for sure, in return for a chance to win. A bidder with a low value bids very little, because it will almost always lose and pay for nothing. A bidder with a high value bids more, because it will often win. When the values are private and the bidders are alike, the seller gets on average the same amount as in the usual auctions. When everyone knows the values, there is no safe bid: any fixed bid invites a rival to bid just above it, so the bidders choose their bids at random.

## The problem

One prize is given to one of $n$ bidders. Bidder $i$ has a value $v_i$ for the prize and [quasilinear utility](/quasilinear-utility/): $v_i - b_i$ if it wins and $-b_i$ if it loses, where $b_i \ge 0$ is its bid. The auction receives the bids and must name the winner and the payments, with the rule that the highest bid wins and all bids are paid. The strategic question is how to bid: at a [Bayes-Nash equilibrium](/bayes-nash-equilibrium/) when the values are private, and at a [Nash equilibrium](/nash-equilibrium/) in [mixed strategies](/mixed-strategy/) when the values are known.

## The algorithm

```pseudo id=main
ALL-PAY(b_1, ..., b_n)
L1  w ← 1
L2  for i ← 2 to n:
L3      if b_i > b_w: w ← i                  ▷ ties go to the smallest index
L4  for i ← 1 to n: p_i ← b_i                ▷ every bidder pays its bid
L5  return w, (p_1, ..., p_n)
```

The rule is the first-price rule with one change in line L4: the losers pay too. The implementation also gives the symmetric equilibrium bid $\beta(v) = \frac{n-1}{n} v^n$ for values uniform on $[0, 1]$, and the exact expected utility of a bidder who bids as another type, which the tests use to check the equilibrium.

## Example

**Private uniform values.** With $n = 2$ the equilibrium bid is $\beta(v) = v^2/2$.

| value $v$ | 0.2 | 0.5 | 0.8 | 1 |
|---|---|---|---|---|
| all-pay bid $v^2/2$ | 0.02 | 0.125 | 0.32 | 0.5 |
| first-price bid $v/2$ | 0.1 | 0.25 | 0.4 | 0.5 |

A bidder of value $0.8$ who bids $0.32$ wins with probability $0.8$ and has expected utility $0.8 \cdot 0.8 - 0.32 = 0.32$. In the first-price auction the same bidder bids $0.4$, wins with probability $0.8$ and has expected utility $0.4 \cdot 0.8 = 0.32$: the same, as revenue equivalence says. A low type bids much less in the all-pay auction, because it pays for sure. The expected revenue is $2 \cdot \mathbb{E}[v^2/2] = 1/3$, and with $n$ bidders it is $(n-1)/(n+1)$, as in the first-price and Vickrey auctions.

**Known values.** Two bidders have values $v_1 = 10$ and $v_2 = 6$, and both know them. In the unique equilibrium, bidder 1 bids uniformly on $[0, 6]$. Bidder 2 bids 0 with probability $0.4$ and otherwise uniformly on $[0, 6]$. Bidder 1 gets $10 - 6 = 4$ for every bid in $[0, 6]$, and bidder 2 gets 0. The expected payments are 3 for bidder 1 and $0.6 \cdot 3 = 1.8$ for bidder 2, so the seller gets $4.8$. Bidder 1 wins with probability $0.4 + 0.6 \cdot 0.5 = 0.7$, so the expected welfare is $0.7 \cdot 10 + 0.3 \cdot 6 = 8.8$, which is the payoffs $4 + 0$ plus the revenue $4.8$. If both values are 10, both bid uniformly on $[0, 10]$, both get 0 and the seller gets 10: the whole value of the prize is spent on bids.

## Correctness

The proof is in `proofs/correctness.md`. It shows three facts.

- **The outcome.** The loop keeps the first highest bid, and line L4 charges every bid.
- **The equilibrium with uniform private values.** If the others bid $\beta(t) = \frac{n-1}{n} t^n$, a bidder of value $v$ who bids $\beta(t)$ gets $u(v, t) = v t^{n-1} - \beta(t)$. Its derivative in $t$ is $(n-1) t^{n-2} (v - t)$, so $t = v$ is best. The expected revenue is $n \cdot \frac{n-1}{n} \mathbb{E}[v^n] = \frac{n-1}{n+1}$.
- **The equilibrium with known values.** Each bidder makes the other indifferent over the support $[0, v_2]$, and bids above $v_2$ are worse ([indifference principle](/indifference-principle/)).

The formula for $\beta$ comes from revenue equivalence. In equilibrium the highest value wins, as in the Vickrey auction, and the lowest type pays 0. So a type $v$ must pay in expectation what it pays in the Vickrey auction, $\mathbb{E}[Y_1 \mathbb{1}\{Y_1 < v\}] = \frac{n-1}{n} v^n$, where $Y_1$ is the highest of the other values. In the all-pay auction this payment is the bid itself.

## Complexity

One pass over the bids and one copy of them: $\Theta(n)$ time and $O(n)$ extra space for the list of payments. The general symmetric equilibrium is $\beta(v) = \int_0^v t \, dG(t)$ with $G = F^{n-1}$, which needs one integral per value. For asymmetric private values and for many prizes the equilibrium has no closed form in general.

## Properties

- **Revenue equivalence.** With symmetric, independent, risk-neutral bidders, the all-pay auction earns the same expected revenue as the first-price, Dutch, English and Vickrey auctions, and each type has the same expected utility.
- **Efficient with symmetric private values.** The equilibrium bid is strictly increasing, so the highest value wins.
- **Not efficient with known, unequal values.** In the example above, the weaker bidder wins with probability $0.3$.
- **Rent dissipation.** With known values, the expected total payment is $\frac{v_2}{2}(1 + \frac{v_2}{v_1})$, which equals the whole prize $v_1$ when $v_1 = v_2$. With $n \ge 2$ bidders of equal known value, the rent is fully dissipated (Hillman and Riley 1989).
- **Losers pay.** The auction is not ex post individually rational: a loser has a negative utility. It is interim individually rational in the private values equilibrium, since $u(v, v) = v^n/n \ge 0$.

## Variants and improvements

- **War of attrition.** The highest bid wins, the winner pays the second-highest bid, and the losers pay their own bids, as in a contest of endurance. With two bidders and uniform values the symmetric equilibrium is $\beta(v) = -v - \ln(1 - v)$, and the expected revenue is again $1/3$ (Krishna, Section 3.2).
- **Many prizes.** Contests with several prizes of decreasing size, such as tournaments with a first and a second prize. The designer's choice of prizes changes the total effort (Moldovanu and Sela 2001 study this question).
- **Lottery contests.** In a Tullock contest a bidder wins with probability proportional to its bid, so a higher bid only raises the chance of winning. It has a pure equilibrium with known values.
- **General contests.** Siegel (2009) found the equilibrium payoffs of a wide class of all-pay contests with complete information, with different costs of effort and head starts.

## When to use it

Use the all-pay auction as a model, not as a sale: it describes lobbying, research races, sports, election campaigns and crowdsourcing contests, where the effort is sunk before the winner is chosen. As a selling method it is rare, because losers are unhappy to pay. It is the right model when the main question is how much total effort a prize attracts.

## Pitfalls

- **No pure equilibrium with known values.** With known values $v_1 \ge v_2 > 0$, any pure profile has a profitable deviation: the loser can bid 0, or the winner can lower its bid. Search for mixed strategies instead.
- **Bids are not the first-price bids.** The all-pay bid $\frac{n-1}{n} v^n$ is much lower than the first-price bid $\frac{n-1}{n} v$ for low values. Using the first-price formula makes low types lose money.
- **Overbidding in experiments.** In the laboratory, the total bids often exceed the equilibrium prediction and sometimes the value of the prize (Dechenaux, Kovenock and Sheremeta 2015).
- **Ties at zero.** With known values, bidder 2 bids 0 with positive probability. The tie rule matters only if bidder 1 also bids 0, which has probability 0 in equilibrium, but a discrete test must handle the tie.
- **Budgets and risk aversion.** Revenue equivalence needs risk-neutral bidders without budgets. A bidder who cannot pay a high bid, or who fears a sure loss, bids differently.

## Implementations

## History

Tullock (1980) started the study of rent seeking, in which firms spend resources to win a monopoly from the state. Hillman and Riley (1989) modelled it as an all-pay auction with known values, found the mixed equilibrium and showed how much of the rent is dissipated. Baye, Kovenock and de Vries (1996) characterized all Nash equilibria with complete information: the equilibrium is unique with two bidders, and with three or more bidders it is unique when the second-highest value is strictly larger than the third, while ties among the lower values give a continuum of equilibria. The private values case follows from revenue equivalence (Myerson 1981; Riley and Samuelson 1981). Siegel (2009) extended the analysis to general contests.

## References
