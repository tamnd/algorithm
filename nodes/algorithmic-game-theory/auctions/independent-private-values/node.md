---
tag: DY117C
kind: model
slug: independent-private-values
name: Independent private values model
aliases:
- IPV model
- independent private values
area: algorithmic-game-theory/auctions
level: core
summary: Each bidder's value for one item is drawn independently from a known distribution and known only to that bidder, and no value depends on the private information of the others.
prereqs: [quasilinear-utility, random-variable, probability-distribution, independent-random-variables]
see_also: [vickrey-auction, first-price-auction, revenue-equivalence-theorem, common-value-auction, bayesian-game, myerson-optimal-auction, single-parameter-environment, cremer-mclean-theorem]
sources:
  - book: isbn:9780123745071
    title: Vijay Krishna, Auction Theory, 2nd edition, Academic Press, 2010
    locator: Chapter 2, Section 2.1 (the symmetric model) and Sections 2.2 to 2.3 (second-price and first-price auctions in it), and Chapter 4 (risk aversion, budgets and asymmetric bidders)
  - paper: doi:10.1111/j.1540-6261.1961.tb02789.x
    title: "William Vickrey, Counterspeculation, auctions, and competitive sealed tenders, Journal of Finance 16(1) (1961), 8-37"
    locator: the first analysis of auctions with private values drawn independently from known distributions
  - paper: doi:10.1287/moor.6.1.58
    title: "Roger B. Myerson, Optimal auction design, Mathematics of Operations Research 6(1) (1981), 58-73"
    locator: the model with independent private values and known distributions, the characterization of incentive compatible mechanisms and the revenue formula
  - paper: doi:10.2307/1911865
    title: "Paul R. Milgrom and Robert J. Weber, A theory of auctions and competitive bidding, Econometrica 50(5) (1982), 1089-1122"
    locator: the general symmetric model with affiliated signals, which contains the independent private values model as a special case
  - book: isbn:9780521536721
    title: Paul Milgrom, Putting Auction Theory to Work, Cambridge University Press, 2004
    locator: Chapter 3 (the envelope theorem and payoff equivalence in the private values model) and Chapter 5 (interdependence of types and values)
---

The independent private values (IPV) model is the standard model of a single-item auction. Each bidder has a value for the item, the value is a random draw from a distribution that everyone knows, the draws are independent, and only the bidder sees its own draw. A bidder's value does not depend on what the others know, so information about the others can change a bidder's bid but never its value. The [Vickrey auction](/vickrey-auction/), the [English auction](/english-auction/), the [first-price auction](/first-price-auction/), the [Dutch auction](/dutch-auction/) and the [all-pay auction](/all-pay-auction/) are all studied first in this model, and the [revenue equivalence theorem](/revenue-equivalence-theorem/) is its central result.

## The machine

A seller has one item and values it at 0. There are $n$ bidders, numbered $1, \ldots, n$.

- **Values.** Bidder $i$ has a value $v_i$, a [random variable](/random-variable/) with a cumulative distribution function $F_i$ on an interval $[0, h_i]$, with a density $f_i$ that is positive on the interval. The values $v_1, \ldots, v_n$ are [independent random variables](/independent-random-variables/). The model is *symmetric* if $F_i = F$ for all $i$.
- **Information.** The distributions $F_1, \ldots, F_n$ are common knowledge. Bidder $i$ knows $v_i$ and nothing more about $v_{-i} = (v_j)_{j \ne i}$.
- **Utility.** Bidders are risk neutral and have [quasilinear utility](/quasilinear-utility/). If bidder $i$ wins with probability $x_i$ and pays $p_i$, its utility is $u_i = v_i x_i - p_i$. The payment $p_i$ goes from bidder $i$ to the seller.
- **Auction.** An auction gives each bidder a set of bids, and maps each profile of bids $b = (b_1, \ldots, b_n)$ to an allocation $x(b)$ with $x_i(b) \ge 0$ and $\sum_i x_i(b) \le 1$, and to payments $p(b)$.
- **Strategies and equilibrium.** A strategy of bidder $i$ is a map $\beta_i$ from values to bids. The profile $(\beta_1, \ldots, \beta_n)$ is a [Bayes-Nash equilibrium](/bayes-nash-equilibrium/) if, for each $i$ and for almost every $v_i$, the bid $\beta_i(v_i)$ maximizes the interim expected utility $\mathbb{E}_{v_{-i}}[v_i x_i(b_i, \beta_{-i}(v_{-i})) - p_i(b_i, \beta_{-i}(v_{-i}))]$ over all bids $b_i$. The model is a [Bayesian game](/bayesian-game/) with a continuum of types.

Independence has a precise role. Because $v_{-i}$ has the same distribution for every $v_i$, the interim functions

$$Q_i(v_i) = \mathbb{E}_{v_{-i}}\bigl[x_i(\beta(v))\bigr], \qquad P_i(v_i) = \mathbb{E}_{v_{-i}}\bigl[p_i(\beta(v))\bigr]$$

describe everything that bidder $i$ cares about: a bidder of value $v$ who bids as type $z$ gets $v Q_i(z) - P_i(z)$. This one-dimensional form is what the [revenue equivalence theorem](/revenue-equivalence-theorem/) and [Myerson's optimal auction](/myerson-optimal-auction/) use. Each bidder has one number of private information and one kind of outcome, so the model is a [single-parameter environment](/single-parameter-environment/) with a prior.

## What it counts

The model measures auctions in expectation over the values, at a Bayes-Nash equilibrium.

- **Expected revenue** $\mathbb{E}[\sum_i p_i]$, the measure of the seller.
- **Expected welfare** $\mathbb{E}[\sum_i v_i x_i]$, the measure of efficiency. Welfare is revenue plus the sum of bidder utilities. The largest possible value is $\mathbb{E}[\max_i v_i]$, reached when the item always goes to a bidder of the highest value.
- **Interim utility** $U_i(v_i) = v_i Q_i(v_i) - P_i(v_i)$ of each type. An auction is interim individually rational if $U_i(v_i) \ge 0$ for each type ([individual rationality](/individual-rationality/)).

In the symmetric model the [order statistics](/order-statistic/) of the values give most of the numbers. Let $Y_1 \ge Y_2 \ge \cdots$ be the order statistics of $n$ values drawn from $F$. With $F$ uniform on $[0, 1]$, $\mathbb{E}[Y_k] = (n + 1 - k)/(n + 1)$, so the optimal welfare is $n/(n+1)$ and the second-highest value has mean $(n-1)/(n+1)$.

## Relation to other models

- **Interdependent and common values.** In the [common value auction](/common-value-auction/), the value of the item is the same for all bidders but unknown, and each bidder sees a private signal of it. Then the signals of the others change a bidder's estimate of its value, and the winner's curse appears. The general model of Milgrom and Weber (1982) has values $v_i = u(X_i, X_{-i}, S)$ that depend on all signals, with affiliated signals. IPV is the case $v_i = X_i$ with independent $X_i$. In the general model the [linkage principle](/linkage-principle/) ranks the auctions by revenue, and revenue equivalence fails.
- **Correlated private values.** If the values are private but correlated, a seller can learn about $v_i$ from $v_{-i}$. Cremer and McLean showed that then, for a generic finite prior, the seller can extract the full surplus in Bayes-Nash equilibrium ([Cremer-McLean theorem](/cremer-mclean-theorem/)). Independence is what leaves the bidders an information rent.
- **Prior-free mechanism design.** The [Vickrey auction](/vickrey-auction/) is [DSIC](/dominant-strategy-incentive-compatibility/) and needs no prior. The IPV model adds the prior, which is needed to speak of first-price bidding, of expected revenue and of the optimal auction.
- **Asymmetric bidders.** If the $F_i$ differ, the model is still IPV, but the first-price auction has no closed form in general and need not give the item to the highest value. The [price of anarchy of first-price auctions](/first-price-auction-price-of-anarchy/) bounds the welfare loss.
- **Other generalizations.** Risk-averse bidders, bidders with budgets and multi-unit or [combinatorial auctions](/combinatorial-auction/) all leave the model, and each breaks some of the results below (Krishna, Chapter 4).

## Known results in the model

Each item is a theorem in the model as stated above, unless it says otherwise.

- **Truthful bidding in second-price and English auctions.** In the Vickrey auction a bid equal to the value is a weakly dominant strategy. In the English auction with private values, staying in until the price reaches the value is also weakly dominant. Both results need no prior and no independence.
- **Symmetric first-price equilibrium.** With $n$ symmetric bidders, the first-price auction has the equilibrium $\beta(v) = \mathbb{E}[Y_1 \mid Y_1 < v]$, where $Y_1$ is the highest of the other $n - 1$ values. With $F$ uniform on $[0, 1]$, $\beta(v) = (n-1)v/n$ ([first-price auction equilibrium](/first-price-auction-equilibrium/)).
- **Revenue equivalence.** Two auctions with the same interim allocation rule in equilibrium and the same utility of the lowest type give the same expected revenue. For $n$ uniform bidders on $[0, 1]$, the second-price, first-price and all-pay auctions all earn $(n-1)/(n+1)$, that is $1/3$ for $n = 2$ and $1/2$ for $n = 3$.
- **Optimal auctions.** With regular distributions, the auction that maximizes expected revenue gives the item to the bidder with the largest [virtual valuation](/virtual-valuation/) $\phi_i(v_i) = v_i - (1 - F_i(v_i))/f_i(v_i)$ if it is positive. In the symmetric regular case this is the Vickrey auction with the [reserve price](/reserve-price/) $\phi^{-1}(0)$. For the uniform distribution on $[0, 1]$, $\phi(v) = 2v - 1$ and the reserve is $1/2$. One bidder then pays $1/2$ with probability $1/2$, which earns $1/4$. Two bidders earn $5/12$, more than the $1/3$ of the Vickrey auction without a reserve ([Myerson's optimal auction](/myerson-optimal-auction/)).
- **Competition against a reserve.** In the symmetric regular case, the Vickrey auction with $n + 1$ bidders earns at least as much as the optimal auction with $n$ bidders ([Bulow-Klemperer theorem](/bulow-klemperer-theorem/)). For uniform values on $[0, 1]$, three bidders in a Vickrey auction earn $1/2$, more than $5/12$.
- **Efficiency of first-price auctions.** In the symmetric model the first-price equilibrium is efficient. With asymmetric independent values, every Bayes-Nash equilibrium of the first-price auction has expected welfare at least $1 - 1/e^2 \approx 0.865$ of the optimum, and this bound is tight (Jin and Lu 2022).
