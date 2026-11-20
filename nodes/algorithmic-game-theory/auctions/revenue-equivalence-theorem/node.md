---
tag: 7394ND
kind: theorem
slug: revenue-equivalence-theorem
name: Revenue equivalence theorem
aliases:
- revenue equivalence
- revenue equivalence principle
area: algorithmic-game-theory/auctions
level: core
summary: "With independent private values and risk-neutral bidders, two auctions with the same equilibrium allocation and the same payment of the lowest type have the same expected revenue."
prereqs: [independent-private-values, vickrey-auction, first-price-auction, expected-value, nash-equilibrium]
see_also: [myerson-optimal-auction, myerson-lemma, all-pay-auction, first-price-auction-equilibrium, linkage-principle, virtual-valuation, bayesian-incentive-compatibility, cremer-mclean-theorem]
sources:
  - paper: doi:10.1287/moor.6.1.58
    title: "Roger B. Myerson, Optimal auction design, Mathematics of Operations Research 6(1) (1981), 58-73"
    locator: the characterization of the Bayesian incentive compatible mechanisms with independent types (monotone interim allocation and the integral formula for the interim utility) and the resulting formula for expected revenue
  - paper: "John G. Riley and William F. Samuelson, Optimal auctions, American Economic Review 71(3) (1981), 381-392"
    locator: equal expected revenue for a class of symmetric auctions in which the highest bidder wins, with or without a reserve
  - paper: doi:10.1111/j.1540-6261.1961.tb02789.x
    title: "William Vickrey, Counterspeculation, auctions, and competitive sealed tenders, Journal of Finance 16(1) (1961), 8-37"
    locator: the equal expected revenue of the first-price and second-price auctions in his examples with uniform values
  - book: isbn:9780123745071
    title: Vijay Krishna, Auction Theory, 2nd edition, Academic Press, 2010
    locator: Chapter 3, Section 3.1 (the main result) and Section 3.2 (applications to unusual auctions and to an uncertain number of bidders), and Chapter 4 (where the assumptions fail)
  - book: isbn:9780521536721
    title: Paul Milgrom, Putting Auction Theory to Work, Cambridge University Press, 2004
    locator: Chapter 3 (the envelope theorem and payoff equivalence)
  - paper: doi:10.1111/1468-0262.00296
    title: "Paul Milgrom and Ilya Segal, Envelope theorems for arbitrary choice sets, Econometrica 70(2) (2002), 583-601"
    locator: the envelope formula for the value of an optimization problem with a parameter, which gives payoff equivalence with an interval of types
---

The revenue equivalence theorem says that, in the [independent private values](/independent-private-values/) model with risk-neutral bidders, the expected payment of each bidder type in a Bayes-Nash equilibrium depends only on who wins and on what the lowest type pays. So the [Vickrey auction](/vickrey-auction/), the [first-price auction](/first-price-auction/), the [English](/english-auction/) and [Dutch](/dutch-auction/) auctions and the [all-pay auction](/all-pay-auction/) all earn the same expected revenue with symmetric bidders, because in each the highest value wins and a bidder of the lowest value pays nothing. The result is due to Myerson (1981) and Riley and Samuelson (1981), with the first case found by Vickrey (1961), and it is the base of [Myerson's optimal auction](/myerson-optimal-auction/).

## Statement

There are $n$ risk-neutral bidders with [quasilinear utility](/quasilinear-utility/). The value $v_i$ of bidder $i$ is drawn from a distribution $F_i$ on an interval $[a_i, b_i]$, with $a_i < b_i$, and the values are independent. Consider an auction, that is, any rules that map bids to an allocation and payments, and a Bayes-Nash equilibrium $\beta = (\beta_1, \ldots, \beta_n)$ in which every type of every bidder plays a best response. For bidder $i$ and a type $v \in [a_i, b_i]$, define the interim functions, where the expectation is over the other values $v_{-i}$:

- $Q_i(v)$, the probability that bidder $i$ wins when it plays $\beta_i(v)$ and the others play $\beta_{-i}(v_{-i})$;
- $P_i(v)$, the expected payment of bidder $i$ in the same situation;
- $U_i(v) = v Q_i(v) - P_i(v)$, its expected utility.

**Theorem.** For each bidder $i$:

1. $Q_i$ is nondecreasing on $[a_i, b_i]$;
2. $U_i(v) = U_i(a_i) + \int_{a_i}^{v} Q_i(t)\, dt$ for every $v \in [a_i, b_i]$;
3. $P_i(v) = P_i(a_i) + v Q_i(v) - a_i Q_i(a_i) - \int_{a_i}^{v} Q_i(t)\, dt$.

**Corollary (revenue equivalence).** Take two auctions and an equilibrium of each, in the same setting. If for every bidder $i$ the two equilibria have the same $Q_i$ and the same $P_i(a_i)$, then they have the same $P_i(v)$ for every type $v$, and so the same expected revenue $\sum_i \mathbb{E}[P_i(v_i)]$ and the same expected utility of each type.

The same holds with "almost every type" in place of "every type", as long as $Q_i$ agrees for almost every type. The statement covers any rules, also the direct revelation mechanisms that are [Bayesian incentive compatible](/bayesian-incentive-compatibility/), where it says that $P_i$ is fixed by $Q_i$ and $P_i(a_i)$.

## In plain words

Think of a bidder who can pretend to be any other type, by bidding as that type would. Because the others' values do not depend on its own, pretending gives it exactly the chance of winning and the expected payment of the other type. In equilibrium no pretence pays. That condition is so strong that it fixes how fast a bidder's expected gain grows with its value: the growth rate is its chance of winning. So once you know who wins in each case, and what the weakest type pays, the expected payment of every type is fixed. Any two auctions that agree on these two things earn the same on average, whatever their rules on paper.

## Proof

Fix bidder $i$ and drop the index $i$: write $Q, P, U$ and $[a, b]$.

**The mimic inequality.** A type $v$ can bid $\beta_i(z)$, the bid of type $z$. The values $v_{-i}$ are independent of $v_i$, so their distribution, and the distribution of the others' bids $\beta_{-i}(v_{-i})$, is the same for every own type. So the bid $\beta_i(z)$ wins with probability $Q(z)$ and costs $P(z)$ in expectation for type $v$ as well, and gives type $v$ the expected utility $v Q(z) - P(z) = U(z) + (v - z) Q(z)$. Because $\beta_i(v)$ is a best response for type $v$,

$$U(v) \ge U(z) + (v - z)\, Q(z) \qquad \text{for all } v, z \in [a, b]. \tag{1}$$

**Part 1.** Apply (1) twice, with the roles of $v$ and $z$ swapped:

$$(v - z)\, Q(z) \;\le\; U(v) - U(z) \;\le\; (v - z)\, Q(v). \tag{2}$$

For $v > z$, dividing by $v - z > 0$ gives $Q(z) \le Q(v)$.

**Part 2.** Fix $v \in (a, b]$ and a partition $a = t_0 < t_1 < \cdots < t_m = v$. Apply (2) to each piece $[t_{k-1}, t_k]$ and add:

$$\sum_{k=1}^m (t_k - t_{k-1})\, Q(t_{k-1}) \;\le\; U(v) - U(a) \;\le\; \sum_{k=1}^m (t_k - t_{k-1})\, Q(t_k).$$

Since $Q$ is nondecreasing, the left side is a lower Riemann sum of $Q$ on $[a, v]$ and the right side an upper Riemann sum. A monotone bounded function is Riemann integrable, so both sums tend to $\int_a^v Q(t)\, dt$ as the mesh goes to 0. Hence $U(v) - U(a) = \int_a^v Q(t)\, dt$.

**Part 3.** Substitute $U(v) = v Q(v) - P(v)$ and $U(a) = a Q(a) - P(a)$ into Part 2 and solve for $P(v)$.

**Corollary.** Part 3 writes $P_i(v)$ through $Q_i$ and $P_i(a_i)$ alone. If two equilibria agree on these, they agree on $P_i(v)$ for every $v$, hence on $\mathbb{E}[P_i(v_i)]$ and on the sum over $i$. If $Q_i$ agrees only for almost every type, the integral in Part 3 is the same, and $P_i(v)$ differs only where $Q_i(v)$ differs, on a set of probability 0, so the expectations agree.

For the version with "almost every type": the inequalities (1) hold for $v$ in a set of full measure and all $z$, and the same argument applies to the restriction of $U$ to that set, whose closure is $[a, b]$. $\square$

## Consequences

- **The standard auctions.** With symmetric bidders whose $F$ is continuous, the Vickrey, English, first-price, Dutch and all-pay auctions all have an equilibrium in which the highest value wins, so $Q(v) = F(v)^{n-1}$, and the type $a = 0$ pays 0. So all earn $\mathbb{E}[Y_{(2)}]$, the mean of the second-highest value. For values uniform on $[0, 1]$ this is $(n-1)/(n+1)$: $1/3$ with two bidders and $1/2$ with three.
- **Bids from revenue.** The theorem gives equilibrium bids without solving a differential equation. In the Vickrey auction a type $v$ pays $m(v) = \mathbb{E}[Y_1 \mathbb{1}\{Y_1 < v\}]$, with $Y_1$ the highest other value. In the all-pay auction a type pays its bid for sure, so the bid is $m(v)$, which is $\frac{n-1}{n} v^n$ for uniform values. In the first-price auction a type pays its bid when it wins, with probability $F(v)^{n-1}$, so the bid is $m(v)/F(v)^{n-1} = \mathbb{E}[Y_1 \mid Y_1 < v]$ ([equilibrium of the symmetric first-price auction](/first-price-auction-equilibrium/)).
- **Unusual auctions.** In the third-price auction with $n \ge 3$ uniform bidders, the highest bid wins and pays the third-highest bid. The equilibrium bid is $\frac{n-1}{n-2} v$, above the value, and the revenue is again $\frac{n-1}{n-2} \cdot \frac{n-2}{n+1} = \frac{n-1}{n+1}$.
- **The revenue formula.** If $F_i$ has a density $f_i$, then by Part 3 and a change of the order of integration, $\mathbb{E}[P_i(v_i)] = \mathbb{E}[\phi_i(v_i)\, Q_i(v_i)] - U_i(a_i)$ with the [virtual valuation](/virtual-valuation/) $\phi_i(v) = v - \frac{1 - F_i(v)}{f_i(v)}$. So expected revenue is expected virtual welfare minus the utilities of the lowest types. Myerson's optimal auction maximizes the virtual welfare point by point ([Myerson's optimal auction](/myerson-optimal-auction/), [Myerson's lemma](/myerson-lemma/)).
- **Reserve prices.** With the same reserve $r$ in the first-price and Vickrey auctions, types below $r$ never win and the others win when they have the highest value, so both auctions earn the same. For uniform values and two bidders, the reserve $1/2$ raises the revenue of both from $1/3$ to $5/12$.

## Tightness

Each assumption is needed.

- **Types in an interval.** With a gap in the type space, the payments are not fixed. Let one bidder have the value 1 or 2, and let $Q(1) = 1/2$, $Q(2) = 1$, $P(1) = 0$. Incentive compatibility for type 2 asks $2 - P(2) \ge 2 \cdot \frac{1}{2} - 0$, so $P(2) \le 1$, and for type 1 it asks $\frac{1}{2} \ge 1 - P(2)$, so $P(2) \ge 1/2$. Every $P(2)$ in $[1/2, 1]$ works, and the revenue is not unique.
- **Independence.** With correlated values, mimicking another type changes the distribution of the others' bids, and (1) fails. Cremer and McLean showed that with correlated finite types a seller can extract the whole surplus ([Cremer-McLean theorem](/cremer-mclean-theorem/)). With affiliated values, the English, second-price and first-price auctions earn different amounts ([linkage principle](/linkage-principle/)).
- **Risk neutrality.** With risk-averse bidders, utility is not linear in the payment. In the first-price auction they bid more to win more surely, and it earns more than the Vickrey auction, where the dominant bid does not change (Krishna, Chapter 4).
- **The same allocation.** With asymmetric bidders the first-price auction does not always give the item to the highest value, so its $Q_i$ differs from that of the Vickrey auction. With bidder 1 uniform on $[0, 1]$ and bidder 2 uniform on $[0, 2]$, the Vickrey auction earns $\mathbb{E}[\min(v_1, v_2)] = 5/12 \approx 0.417$, while the first-price auction earns about $0.459$ by numerical integration.
- **The same payment of the lowest type.** An entry fee or a payment to the lowest type changes $P_i(a_i)$, and with it the revenue, by the same amount for every type.
- **No budgets.** A bidder who cannot pay more than a budget has no quasilinear utility on all bids, and the auctions differ (Krishna, Chapter 4).

## History

Vickrey (1961) computed, for uniform values, that the first-price and second-price auctions earn the same expected revenue, and saw that this was not an accident of the example. Myerson (1981) and Riley and Samuelson (1981) proved the general result in the same year, by different routes. Myerson characterized all Bayesian incentive compatible mechanisms with independent types by the monotonicity of $Q_i$ and the integral formula for $U_i$, and used it to find the optimal auction. Riley and Samuelson showed equal revenue for a broad class of symmetric auctions in which the highest bidder wins. The modern form, with the envelope theorem, is in Milgrom and Segal (2002) and in Milgrom (2004).

## References
