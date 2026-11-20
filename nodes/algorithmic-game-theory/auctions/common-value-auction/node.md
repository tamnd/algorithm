---
tag: C3737X
kind: model
slug: common-value-auction
name: Common value auction
aliases:
- mineral rights model
- pure common value auction
area: algorithmic-game-theory/auctions
level: core
summary: The item has one value that is the same for all bidders but unknown, and each bidder sees a private noisy signal of it. The winner tends to hold the most optimistic signal, the winner's curse.
prereqs: [independent-private-values, conditional-expectation, order-statistic, vickrey-auction, first-price-auction]
see_also: [linkage-principle, english-auction, independent-private-values, cremer-mclean-theorem, bayesian-game, bayes-nash-equilibrium, revenue-equivalence-theorem, first-price-auction]
sources:
  - paper: "Robert B. Wilson, Competitive bidding with disparate information, Management Science 15(7) (1969), 446-448"
    locator: the first model of bidding for an item of common but unknown value with private signals
  - paper: doi:10.2307/2296904
    title: "Robert Wilson, A bidding model of perfect competition, Review of Economic Studies 44(3) (1977), 511-518"
    locator: the symmetric equilibrium of the first-price common value auction and the result that, with many bidders, the winning bid tends to the true value
  - paper: doi:10.2118/2993-PA
    title: "E. C. Capen, R. V. Clapp and W. M. Campbell, Competitive bidding in high-risk situations, Journal of Petroleum Technology 23(6) (1971), 641-653"
    locator: the winner's curse in sales of offshore oil and gas leases, where the winning bidder tends to be the one who overestimated the value most
  - paper: doi:10.2307/1911865
    title: "Paul R. Milgrom and Robert J. Weber, A theory of auctions and competitive bidding, Econometrica 50(5) (1982), 1089-1122"
    locator: the general symmetric model with affiliated signals and interdependent values, the equilibria of the English, second-price and first-price auctions, and their revenue ranking
  - book: isbn:9780123745071
    title: Vijay Krishna, Auction Theory, 2nd edition, Academic Press, 2010
    locator: Chapter 6 (auctions with interdependent values, the second-price, English and first-price equilibria and their revenue comparison) and Chapter 7 (the linkage principle)
  - book: isbn:9780521536721
    title: Paul Milgrom, Putting Auction Theory to Work, Cambridge University Press, 2004
    locator: Chapter 5 (interdependence of types and values, affiliation and the Milgrom-Weber models)
  - paper: "John H. Kagel and Dan Levin, The winner's curse and public information in common value auctions, American Economic Review 76(5) (1986), 894-920"
    locator: laboratory common value auctions in which bidders fall prey to the winner's curse, more so with more bidders
---

In a common value auction the item is worth the same to every bidder, but nobody knows how much. Each bidder sees a private signal, a noisy estimate of the value, and bids on it. The bidder with the highest estimate tends to win, and the highest of several noisy estimates is too high on average, so a bidder who bids its estimate loses money when it wins. This is the *winner's curse*. A rational bidder corrects for it by asking what the value is worth given that it won. The model is the opposite extreme of the [independent private values](/independent-private-values/) model, and the [linkage principle](/linkage-principle/) ranks the standard auctions by revenue in it.

## The machine

There are $n$ bidders and one item. The model has these parts.

- **The value.** A random variable $V$ with a known prior distribution. Every bidder who wins gets $V$, so the values are $v_1 = \cdots = v_n = V$. This is the *pure common value* case. The general case of Milgrom and Weber (1982) has $v_i = u(X_i, X_{-i}, S)$, a function of all signals and of a hidden state $S$, and contains both this model and private values.
- **The signals.** Bidder $i$ sees a signal $X_i$. In the standard form the signals are independent given $V$, with the same distribution, such as $X_i = V + \varepsilon_i$ with independent noise $\varepsilon_i$. Then the signals are not independent: a high $X_j$ makes a high $V$ and so a high $X_i$ more likely. They are *affiliated*, a strong form of positive dependence (Milgrom and Weber 1982).
- **Utility.** Bidders are risk neutral with [quasilinear utility](/quasilinear-utility/): $V - p$ if the bidder wins and pays $p$, and 0 if it loses.
- **Strategies and equilibrium.** A strategy maps signals to bids, and the bidders play a symmetric [Bayes-Nash equilibrium](/bayes-nash-equilibrium/) of the resulting [Bayesian game](/bayesian-game/).

Two conditional expectations organize the analysis. Let $Y_1$ be the highest signal among the other $n - 1$ bidders. Then

$$v(x, y) = \mathbb{E}[V \mid X_1 = x,\; Y_1 = y]$$

is the value to bidder 1 when its signal is $x$ and the best rival signal is $y$, and $v(x, x)$ is the value when it ties with the best rival. The naive estimate is $\mathbb{E}[V \mid X_1 = x]$, and the estimate given a win at a symmetric increasing equilibrium is $\mathbb{E}[V \mid X_1 = x, Y_1 < x]$, which is lower. The gap between the two is the size of the winner's curse.

## What it counts

- **Expected revenue** $\mathbb{E}[p]$. In the pure common value model, expected welfare is $\mathbb{E}[V]$ whenever the item is sold, so efficiency is not an issue, and revenue is the main measure.
- **Bidder profit** $\mathbb{E}[V - p]$ of the winner, the information rent. It comes from the private part of the signals: a bidder who knows what the others know earns no rent.
- **The winner's curse.** The expected loss of a bidder who bids its naive estimate, or the gap $\mathbb{E}[V \mid X_1 = x] - \mathbb{E}[V \mid X_1 = x, Y_1 < x]$.
- **Information aggregation.** Whether the price tends to $V$ as $n$ grows.

**Example.** Let $V$ be uniform on $[0, 100]$, $X_i = V + \varepsilon_i$ with $\varepsilon_i$ uniform on $[-10, 10]$, and $n = 5$. For a signal $x \in [10, 90]$, the naive estimate is $\mathbb{E}[V \mid X_1 = x] = x$. Given that $x$ is the highest of the 5 signals, $V$ has the posterior density proportional to $\bigl((x - V + 10)/20\bigr)^4$ on $[x - 10, x + 10]$, and $\mathbb{E}[V \mid X_1 = x, Y_1 < x] = x - 10 \cdot \frac{n-1}{n+1} = x - 20/3 \approx x - 6.67$.

- If all five bidders bid their signals in a [Vickrey auction](/vickrey-auction/), the winner pays the second-highest signal. All signals are $V$ plus noise, so the price minus $V$ is the second-highest of 5 noise terms, whose mean is $-10 + 20 \cdot \frac{4}{6} = 10/3$. The winner loses $10/3 \approx 3.33$ on average, for every prior.
- In the symmetric equilibrium of the Vickrey auction, a bidder bids $v(x, x)$, the value when it ties with the best rival. Given $X_1 = Y_1 = x$, the other three signals are below $x$, which gives the posterior density proportional to $\bigl((x - V + 10)/20\bigr)^3$, and $v(x, x) = x - 10 \cdot \frac{n-2}{n} = x - 6$ for signals in the interior. With $n = 2$, $v(x, y) = (x + y)/2$ and the bid is $x$ itself.

The more bidders there are, the larger the correction: the winning signal is the maximum of more noisy draws.

## Relation to other models

- **Private values.** In the [independent private values](/independent-private-values/) model, $v_i = X_i$ and the signals are independent. Learning the others' signals changes nothing, there is no winner's curse, and the [revenue equivalence theorem](/revenue-equivalence-theorem/) holds. In the common value model the signals are affiliated and the value depends on all of them, so revenue equivalence fails.
- **Interdependent values.** The general Milgrom-Weber model has $v_i = u(X_i, X_{-i})$ with $u$ symmetric in the others' signals and affiliated signals. Pure common values and private values are its two extremes. The "wallet game", where the value is the sum of the bidders' signals, is a common value case with independent signals.
- **The English auction.** With interdependent values, the [English auction](/english-auction/) is no longer equivalent to the Vickrey auction. Each exit price reveals a signal, so the remaining bidders bid on more information.
- **Correlated private values.** If values are private but correlated, the seller can use the correlation against the bidders and, with finite types and a generic prior, extract the full surplus ([Cremer-McLean theorem](/cremer-mclean-theorem/)). With common values the same idea applies to the signals.

## Known results in the model

Each item is a theorem for the model with affiliated signals and symmetric bidders, unless stated otherwise.

- **Second-price equilibrium.** The bid $b(x) = v(x, x)$ is a symmetric equilibrium of the second-price auction (Milgrom and Weber 1982; Krishna, Chapter 6). It is not dominant: the best bid depends on the others' strategies.
- **English equilibrium.** In the clock form with visible exits, a bidder stays in until the price reaches the expected value given that all remaining bidders have its signal and given the signals revealed by the exits so far (Krishna, Chapter 6).
- **First-price equilibrium.** A bidder bids $b(x) = \int_0^x v(y, y)\, dL(y \mid x)$ with $L(y \mid x) = \exp\bigl(-\int_y^x \frac{g(t \mid t)}{G(t \mid t)} dt\bigr)$, where $G(\cdot \mid x)$ is the distribution of $Y_1$ given $X_1 = x$ (Milgrom and Weber 1982; Krishna, Chapter 6). For independent private values this is the formula $\mathbb{E}[Y_1 \mid Y_1 < x]$.
- **Revenue ranking.** The English auction earns at least as much as the second-price auction, which earns at least as much as the first-price auction ([linkage principle](/linkage-principle/)).
- **Public information.** If the seller commits to reveal a signal that is affiliated with the values, the expected revenue of the standard auctions does not fall. So "honesty is the best policy" for the seller (Milgrom and Weber 1982).
- **Information aggregation.** In the first-price auction with signals independent given $V$ and conditions on their distribution, the winning bid tends to $V$ in probability as $n \to \infty$ (Wilson 1977).
- **The winner's curse in practice.** In auctions of oil leases, the winners often earned low returns, which Capen, Clapp and Campbell (1971) explained by the winner's curse. In laboratory common value auctions, inexperienced bidders often bid above $\mathbb{E}[V \mid X_1 = x, Y_1 < x]$ and lose money, more so with more bidders (Kagel and Levin 1986). These are measurements, not theorems.

## References
