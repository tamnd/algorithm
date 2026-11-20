---
tag: QH8SNK
kind: theorem
slug: first-price-auction-equilibrium
name: Equilibrium of the symmetric first-price auction
aliases:
- first-price bid shading formula
- symmetric first-price equilibrium
area: algorithmic-game-theory/auctions
level: core
summary: With n symmetric independent private values, bidding the expected highest rival value given that it is below one's own value is a Bayes-Nash equilibrium of the first-price auction.
prereqs: [independent-private-values, first-price-auction, order-statistic, conditional-expectation, nash-equilibrium]
see_also: [first-price-auction, dutch-auction, revenue-equivalence-theorem, bayes-nash-equilibrium, first-price-auction-price-of-anarchy, all-pay-auction, reserve-price, vickrey-auction]
sources:
  - book: isbn:9780123745071
    title: Vijay Krishna, Auction Theory, 2nd edition, Academic Press, 2010
    locator: Chapter 2, Section 2.3 (the symmetric equilibrium of the first-price auction, its derivation from the first-order condition and the check that it is a best response) and Chapter 4 (risk aversion and asymmetric bidders)
  - paper: doi:10.1111/j.1540-6261.1961.tb02789.x
    title: "William Vickrey, Counterspeculation, auctions, and competitive sealed tenders, Journal of Finance 16(1) (1961), 8-37"
    locator: the equilibrium bid (n - 1)v/n for independent uniform values
  - paper: "John G. Riley and William F. Samuelson, Optimal auctions, American Economic Review 71(3) (1981), 381-392"
    locator: the symmetric equilibrium bids of the first-price and other auctions with a reserve, for a general distribution of independent private values
  - book: isbn:9780521536721
    title: Paul Milgrom, Putting Auction Theory to Work, Cambridge University Press, 2004
    locator: Chapter 4 (bidding equilibrium and revenue differences)
  - paper: "Shuchi Chawla and Jason D. Hartline, Auctions with unique equilibria, Proceedings of the 14th ACM Conference on Electronic Commerce (EC), 2013, 181-196"
    locator: the uniqueness of the Bayes-Nash equilibrium of the first-price auction with independent and identically distributed values, which is then the symmetric one
---

In a first-price auction the winner pays its own bid, so each bidder must decide how far below its value to bid. When the bidders are symmetric, with independent private values from one known distribution, the answer has a closed form: bid the expected value of the highest rival value, given that this rival value is below your own. This page states and proves this result, shows that the equilibrium is efficient and earns the same expected revenue as the [Vickrey auction](/vickrey-auction/), and gives the cases where the formula fails. It applies without change to the [Dutch auction](/dutch-auction/), which is the same game as the [first-price auction](/first-price-auction/).

## Statement

Let $n \ge 2$ bidders have values $v_1, \ldots, v_n$ that are independent with the same cumulative distribution function $F$ on $[0, \omega]$, where $\omega \le \infty$, $F$ is continuous and strictly increasing on $[0, \omega]$ with $F(0) = 0$, and $\mathbb{E}[v_i] < \infty$ ([independent private values](/independent-private-values/)). The bidders are risk neutral. In the first-price auction without reserve, the highest bid wins and pays itself, and ties are broken by any rule.

For a bidder, let $Y_1$ be the highest of the other $n - 1$ values, an [order statistic](/order-statistic/) with the distribution function $G = F^{n-1}$.

**Theorem.** The strategy

$$\beta(v) \;=\; \mathbb{E}[\,Y_1 \mid Y_1 < v\,] \;=\; v - \frac{\int_0^v G(t)\, dt}{G(v)} \qquad (v > 0), \qquad \beta(0) = 0,$$

used by every bidder, is a symmetric Bayes-Nash equilibrium. In it:

1. a bidder of value $v$ has the expected utility $U(v) = \int_0^v G(t)\, dt$;
2. the bidder with the highest value wins;
3. the expected revenue is $\mathbb{E}[Y_{(2)}]$, the mean of the second-highest of the $n$ values, which is the revenue of the Vickrey auction.

Conversely, if every bidder uses the same strictly increasing and differentiable strategy and this is an equilibrium, the strategy is $\beta$.

For values uniform on $[0, 1]$, $G(t) = t^{n-1}$ and $\beta(v) = \frac{n-1}{n} v$. For $F(v) = v^a$ on $[0, 1]$, $\beta(v) = \frac{a(n-1)}{a(n-1)+1} v$. For two bidders with exponential values, $F(v) = 1 - e^{-v}$, $\beta(v) = 1 - \frac{v e^{-v}}{1 - e^{-v}}$, so a bidder of value 1 bids $1 - \frac{1}{e - 1} \approx 0.418$.

## In plain words

When you bid in a first-price auction and you win, you know that every rival had a lower value. The bid that balances the gain from a lower price against the risk of losing is your best guess of the highest rival value, in the case that you win. If everyone bids this way, a higher value always gives a higher bid, so the right person wins. And the price is, on average, the second-highest value, which is exactly what the winner would pay in an auction where the winner pays the second price.

## Proof

Write $g$ for the density of $G$ where it exists, and use $\int_0^v t\, dG(t)$ for the Stieltjes integral, which is defined because $G$ is nondecreasing and continuous. Integration by parts gives

$$\int_0^v t\, dG(t) = v G(v) - \int_0^v G(t)\, dt, \tag{1}$$

so the two forms of $\beta$ in the statement are the same, as $\mathbb{E}[Y_1 \mid Y_1 < v] = \int_0^v t\, dG(t) / G(v)$, and $G(v) > 0$ for $v > 0$ because $F$ is strictly increasing.

**$\beta$ is continuous and strictly increasing, and $0 < \beta(v) < v$ for $v > 0$.** By (1), $G(v)\beta(v) = \int_0^v t\, dG(t)$. So $\beta(v)$ is an average of $t$ over $[0, v)$ with the weights $dG$, which gives $0 < \beta(v) < v$, and $\beta(v) \to 0$ as $v \to 0$. It is continuous as a ratio of continuous functions with $G > 0$. For $v < w$, $\beta(w)$ is the average over $[0, w)$, which adds to the average over $[0, v)$ the points of $[v, w)$. These points are all at least $v > \beta(v)$ and have positive weight $G(w) - G(v) > 0$, so $\beta(w) > \beta(v)$. Hence the bids of the other bidders have no atoms, and ties have probability 0.

**Best response.** Fix bidder $i$ with value $v$, and let every other bidder use $\beta$. Consider first a bid $\beta(z)$ with $z \in [0, \omega)$. It wins when $Y_1 < z$, up to an event of probability 0, so its expected utility is

$$\Pi(v, z) = G(z)\,(v - \beta(z)) = G(z) v - \int_0^z t\, dG(t) = G(z)(v - z) + \int_0^z G(t)\, dt,$$

by (1). Then

$$\Pi(v, v) - \Pi(v, z) = \int_z^v G(t)\, dt - G(z)(v - z) = \int_z^v \bigl(G(t) - G(z)\bigr)\, dt.$$

If $z < v$, the integrand is at least 0 because $G$ is nondecreasing. If $z > v$, the integral equals $\int_v^z (G(z) - G(t))\, dt$, which is at least 0 for the same reason. So no bid $\beta(z)$ is better than $\beta(v)$. Because $\beta$ is continuous and strictly increasing from 0, every bid in $[0, \sup \beta)$ is of this form. A bid $b \ge \sup \beta$ wins with probability 1 and gives $v - b \le v - \sup \beta = \lim_{z \to \omega} \Pi(v, z) \le \Pi(v, v)$. Negative bids are not allowed. So $\beta(v)$ is a best response for every $v$, and $\beta$ is a symmetric Bayes-Nash equilibrium.

**Part 1.** $U(v) = \Pi(v, v) = \int_0^v G(t)\, dt$, by the formula for $\Pi$ with $z = v$.

**Part 2.** $\beta$ is strictly increasing, so the highest bid comes from the highest value, except on the event of a tie in values, which has probability 0.

**Part 3.** The winner is the bidder with the highest value $Y_{(1)}$, and it pays $\beta(Y_{(1)}) = \mathbb{E}[Y_1 \mid Y_1 < v]$ at $v = Y_{(1)}$. Given that the highest of the $n$ values is $v$, the highest of the others is the second-highest value $Y_{(2)}$, and by independence its conditional distribution is that of $Y_1$ given $Y_1 < v$. So $\beta(Y_{(1)}) = \mathbb{E}[Y_{(2)} \mid Y_{(1)}]$, and by the tower rule of [conditional expectation](/conditional-expectation/), the expected revenue is $\mathbb{E}[Y_{(2)}]$.

**Converse.** Let every bidder use a strictly increasing and differentiable strategy $s$, with inverse $s^{-1}$, in equilibrium. A bidder of value $v$ who bids $s(z)$ gets $G(z)(v - s(z))$, and since $s(v)$ is optimal, the derivative in $z$ is 0 at $z = v$ when $F$ has a density:

$$g(v)\,(v - s(v)) - G(v)\, s'(v) = 0, \quad\text{that is,}\quad \frac{d}{dv}\bigl(G(v) s(v)\bigr) = v\, g(v).$$

A type 0 never gains by a positive bid, and $s$ is increasing, so $G(v)s(v) \to 0$ as $v \to 0$. Integrating gives $G(v) s(v) = \int_0^v t\, g(t)\, dt$, so $s = \beta$. $\square$

## Consequences

- **The revenue of first-price and second-price auctions is the same.** Part 3 is a direct case of the [revenue equivalence theorem](/revenue-equivalence-theorem/). For uniform values the revenue is $(n-1)/(n+1)$ in both.
- **Shading falls with competition.** For uniform values the shading is $v/n$. For any $F$ and fixed $v < \omega$, $\beta(v) \to v$ as $n \to \infty$, because $G = F^{n-1}$ puts its mass near $v$ on $[0, v)$.
- **Interim utility.** A bidder of value $v$ gets $\int_0^v F(t)^{n-1} dt$, the same as in the Vickrey auction, where it gets $\mathbb{E}[(v - Y_1)^+] = \int_0^v G(t)\, dt$.
- **The Dutch auction has the same equilibrium.** A bidder in a [Dutch auction](/dutch-auction/) chooses a stop price, which is a first-price bid.
- **With a reserve $r$.** Types below $r$ do not bid, and a type $v \ge r$ bids $\mathbb{E}[\max(Y_1, r) \mid Y_1 < v]$. With uniform values the revenue is then that of the Vickrey auction with the same reserve, which is optimal for $r = 1/2$ ([reserve price](/reserve-price/)).

## Tightness

Each assumption of the theorem is needed.

- **Asymmetric bidders.** With different distributions, the bids differ by bidder and the formula is wrong. With bidder 1 uniform on $[0, 1]$ and bidder 2 uniform on $[0, 2]$, the equilibrium has the inverse bids $8b/(4 + 3b^2)$ and $8b/(4 - 3b^2)$ on $[0, 2/3]$. The weaker bidder bids more aggressively, the item goes to the lower value with probability about $0.083$, and the welfare is about $98.1\%$ of the optimum. The worst case over all independent distributions is $1 - 1/e^2$ ([price of anarchy of first-price auctions](/first-price-auction-price-of-anarchy/)).
- **Atoms in the distribution.** Let two bidders have values 0 or 1, each with probability $1/2$. No pure symmetric equilibrium exists: if a type 1 bids $b$, a deviation to just above $b$ wins every tie with the other type 1. In the equilibrium, type 0 bids 0 and type 1 mixes with the CDF $H(b) = b/(1-b)$ on $[0, 1/2]$. A type 1 who bids $b$ gets $(1 - b)\bigl(\frac{1}{2} + \frac{1}{2}H(b)\bigr) = \frac{1}{2}$ for every $b$ in this interval, and less above it. The expected revenue is $1/4$, which is again the mean of the second-highest value.
- **Risk aversion.** Risk-averse bidders bid more than $\beta$, to raise the chance of winning, and the first-price auction then earns more than the Vickrey auction, in which risk does not change the dominant bid (Krishna, Chapter 4).
- **Differentiability in the converse.** The converse assumes a differentiable increasing strategy. Chawla and Hartline (2013) showed that, with independent and identically distributed values, the first-price auction has no other Bayes-Nash equilibrium at all, symmetric or not, so the restriction does not hide other equilibria in this setting.
- **Correlated or common values.** With affiliated values, the first-price equilibrium has a different form, and the first-price auction earns at most as much as the second-price auction ([linkage principle](/linkage-principle/)).

## History

Vickrey (1961) found the equilibrium bid $(n-1)v/n$ for uniform values and noted that the expected revenue equals that of the second-price auction. The general formula for any distribution, with a reserve, appears in Riley and Samuelson (1981), in the same paper that proved revenue equivalence for a wide class of auctions. Textbooks derive it as on this page, by the first-order condition and a check by integration by parts (Krishna, Section 2.3). Chawla and Hartline (2013) proved that the symmetric equilibrium is the only one with identically distributed values.

## References
