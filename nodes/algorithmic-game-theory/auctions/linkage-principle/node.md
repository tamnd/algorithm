---
tag: DBCP4R
kind: theorem
slug: linkage-principle
name: Linkage principle
aliases:
- Milgrom-Weber linkage principle
area: algorithmic-game-theory/auctions
level: advanced
summary: "For symmetric bidders with affiliated signals and risk neutrality, auctions whose price is more linked to others' signals earn more expected revenue: English, then second-price, then first-price."
prereqs: [common-value-auction, revenue-equivalence-theorem, first-price-auction-equilibrium, english-auction, conditional-expectation]
see_also: [common-value-auction, english-auction, revenue-equivalence-theorem, first-price-auction, vickrey-auction, cremer-mclean-theorem, independent-private-values, bayes-nash-equilibrium]
sources:
  - paper: doi:10.2307/1911865
    title: "Paul R. Milgrom and Robert J. Weber, A theory of auctions and competitive bidding, Econometrica 50(5) (1982), 1089-1122"
    locator: the properties of affiliated random variables, the revenue ranking of the English, second-price and first-price auctions, and the result that the seller gains by a policy of revealing its information
  - book: isbn:9780123745071
    title: Vijay Krishna, Auction Theory, 2nd edition, Academic Press, 2010
    locator: Chapter 7 (the revenue ranking or linkage principle and public information), Chapter 6 (the equilibria and revenue comparisons with interdependent values) and Chapter 8 (asymmetric bidders)
  - book: isbn:9780521536721
    title: Paul Milgrom, Putting Auction Theory to Work, Cambridge University Press, 2004
    locator: Chapter 5 (interdependence of types and values, affiliation and the revenue comparisons of the Milgrom-Weber model)
  - paper: doi:10.1111/1468-0262.00056
    title: "Motty Perry and Philip J. Reny, On the failure of the linkage principle in multi-unit auctions, Econometrica 67(4) (1999), 895-900"
    locator: an example with two units in which an auction with more linkage earns less, so the principle does not extend to multi-unit auctions
---

The linkage principle explains why, when bidders' information is positively related, the standard auctions are no longer equivalent in revenue. A bidder who wins pays a price, and if that price rises with the bidder's own signal through the information of the others, the bidder's private information is worth less and it bids more boldly. So the more the price is *linked* to the information of the other bidders, the higher the expected revenue. Milgrom and Weber (1982) used it to rank the [English auction](/english-auction/) above the second-price auction and the second-price auction above the [first-price auction](/first-price-auction/), in the [common value](/common-value-auction/) and affiliated values model. With [independent private values](/independent-private-values/) the link is zero and the ranking becomes the equality of the [revenue equivalence theorem](/revenue-equivalence-theorem/).

## Statement

**The model.** There are $n$ symmetric, risk-neutral bidders. Bidder $i$ sees a signal $X_i \in [0, \omega]$, and its value is $v_i = u(X_i, X_{-i})$, where $u$ is the same for all bidders, symmetric in the others' signals, nondecreasing in every signal and strictly increasing in its own. The signals have a joint density that is symmetric and *affiliated*: for all signal vectors $x, x'$, $f(x \vee x') f(x \wedge x') \ge f(x) f(x')$, with the componentwise maximum $\vee$ and minimum $\wedge$. For bidder 1, let $Y_1 = \max_{j \ne 1} X_j$, let $G(\cdot \mid x)$ with density $g(\cdot \mid x)$ be the distribution of $Y_1$ given $X_1 = x$, and let $v(x, y) = \mathbb{E}[v_1 \mid X_1 = x, Y_1 = y]$, with $v(0, 0) = 0$.

**The link.** Consider an auction format A and a symmetric equilibrium with an increasing strategy, in which the highest signal wins. Let $W^A(z, x)$ be the expected payment of bidder 1 *given that it wins*, when its signal is $x$ and it bids as a type $z$ would, while the others follow the equilibrium. The derivative $W^A_2(z, x) = \partial W^A / \partial x$ measures how much the price, given a win, depends on the bidder's own signal through the information of the others. Assume that $W^A$ and the functions $v$, $G$ and $g$ are differentiable, and $G(x \mid x) > 0$ for $x > 0$.

**Theorem (linkage principle).** Let A and B be two such auction formats with equilibria as above. If

1. $W^A_2(x, x) \ge W^B_2(x, x)$ for all $x$, and
2. $W^A(0, 0) = W^B(0, 0) = 0$,

then the expected revenue of A is at least that of B.

**Corollary (Milgrom and Weber 1982).** In this model, the expected revenue of the second-price sealed-bid auction is at least that of the first-price sealed-bid auction. The English auction earns at least as much as the second-price auction.

## In plain words

When signals are related, the winner's price can depend on the other bidders' information. In a second-price auction, the price is set by the second-best rival, and the rival's signal tends to be high when the winner's own signal is high. So the price "follows" the winner's signal. In a first-price auction the price is only the winner's own bid, which follows nothing. A bidder whose price follows the truth worries less about the winner's curse, because a mistake in its own estimate is partly corrected by the price. So it bids more aggressively, and the seller gains. The English auction links the price to even more information, since every exit reveals a signal.

## Proof

**Step 1: the first-order condition.** A bidder with signal $x$ who bids as $z$ wins when $Y_1 < z$. Its expected profit is

$$\Pi^A(z, x) = \int_0^z v(x, y)\, g(y \mid x)\, dy \;-\; G(z \mid x)\, W^A(z, x).$$

In equilibrium the best $z$ is $x$, so $\partial \Pi^A / \partial z = 0$ at $z = x$:

$$v(x, x)\, g(x \mid x) - g(x \mid x)\, W^A(x, x) - G(x \mid x)\, W^A_1(x, x) = 0,$$

so

$$W^A_1(x, x) = \frac{g(x \mid x)}{G(x \mid x)} \bigl(v(x, x) - W^A(x, x)\bigr),$$

and the same holds for B.

**Step 2: comparing the two formats.** Let $\Delta(x) = W^A(x, x) - W^B(x, x)$. By the chain rule, $\frac{d}{dx} W^A(x, x) = W^A_1(x, x) + W^A_2(x, x)$, and so by Step 1

$$\Delta'(x) = -\frac{g(x \mid x)}{G(x \mid x)}\, \Delta(x) + \bigl(W^A_2(x, x) - W^B_2(x, x)\bigr).$$

By condition 2, $\Delta(0) = 0$, and by condition 1 the bracket is at least 0. Suppose $\Delta(x_1) < 0$ for some $x_1 > 0$. Let $x_0 = \sup\{x \le x_1 : \Delta(x) \ge 0\}$, which exists because $\Delta(0) = 0$. By continuity $\Delta(x_0) = 0$ and $\Delta < 0$ on $(x_0, x_1]$. On this interval $\Delta'(x) \ge -\frac{g}{G} \Delta(x) \ge 0$, so $\Delta$ is nondecreasing there and $\Delta(x_1) \ge \Delta(x_0) = 0$, a contradiction. So $\Delta(x) \ge 0$ for all $x$.

**Step 3: revenue.** The expected payment of a bidder with signal $x$ in equilibrium is $G(x \mid x)\, W^A(x, x)$ in A and $G(x \mid x)\, W^B(x, x)$ in B, because it wins with the same probability $G(x \mid x)$ in both. By Step 2 the first is at least the second for every $x$, and so the expected revenue of A is at least that of B. $\square$

**Proof of the corollary for the sealed-bid auctions.** We use one property of affiliated variables (Milgrom and Weber 1982): if $h$ is nondecreasing, then $\mathbb{E}[h(Y_1) \mid X_1 = x, Y_1 < z]$ is nondecreasing in $x$. Both auctions have a symmetric increasing equilibrium, in which the highest signal wins (Krishna, Chapter 6).

- In the first-price auction with equilibrium bid $\beta^I$, the price given a win is the bidder's own bid: $W^I(z, x) = \beta^I(z)$. It does not depend on $x$, so $W^I_2 = 0$, and $\beta^I(0) = 0$.
- In the second-price auction with equilibrium bid $\beta^{II}(y) = v(y, y)$, the price given a win is the bid of the best rival: $W^{II}(z, x) = \mathbb{E}[v(Y_1, Y_1) \mid X_1 = x, Y_1 < z]$. The function $y \mapsto v(y, y)$ is nondecreasing, so by the property above $W^{II}_2 \ge 0$. With the normalization $v(0, 0) = 0$, a type 0 pays 0, so $W^{II}(0, 0) = 0$.

The theorem with A the second-price and B the first-price auction gives the ranking. The comparison of the English and second-price auctions uses the same argument with the exit prices of the $n - 2$ lowest bidders as extra information that enters the English price (Milgrom and Weber 1982; Krishna, Chapter 6). $\square$

## Consequences

- **Independent private values give equality.** If $v_i = X_i$ and the signals are independent, $W^{II}(z, x) = \mathbb{E}[Y_1 \mid Y_1 < z]$ does not depend on $x$, so $W^{II}_2 = 0 = W^I_2$ and the theorem applies in both directions. This is revenue equivalence for the two sealed-bid auctions.
- **A numerical example with affiliated private values.** Let two bidders have private values $v_i = X_i$ with the joint density $f(x, y) = (1 + 4xy)/2$ on $[0, 1]^2$, which is affiliated because $\partial^2 \ln f / \partial x \partial y = 4/(1 + 4xy)^2 > 0$. The second-price auction earns $\mathbb{E}[\min(X_1, X_2)] = 13/30 \approx 0.4333$. The first-price equilibrium is $\beta(x) = x - \frac{(1 + 2x^2)^{3/2} - 1}{6 x \sqrt{1 + 2x^2}}$, with $\beta(1/2) \approx 0.272$ and $\beta(1) \approx 0.596$, and by numerical integration it earns about $0.4230$. With independent uniform values both would earn $1/3$. With two bidders the English auction gives the same outcome as the second-price auction, because no exit is seen before the end.
- **Public information.** If the seller has a signal $S$ affiliated with the bidders' information and commits to reveal it, the price is linked to $S$, and the expected revenue of the first-price, second-price and English auctions does not fall (Milgrom and Weber 1982; Krishna, Chapter 7). This is the "honesty is the best policy" result: expert appraisals of art and published geological surveys raise the expected price.
- **Bidders prefer the first-price auction.** In this model every bidder type has at least as much expected profit in the first-price auction as in the second-price auction, because the same allocation and lower expected payments mean higher utility.

## Tightness

- **Asymmetric bidders.** With bidders who differ, the ranking can fail: the second-price or the English auction can earn less than the first-price auction (Krishna, Chapter 8).
- **Many units.** Perry and Reny (1999) gave an example with two units and bidders who want both, in which an auction with more linkage earns less. The principle does not extend to multi-unit auctions in general.
- **Risk aversion.** Risk-averse bidders bid more in the first-price auction. With independent private values this gives the first-price auction a strict advantage, and with affiliated values the two effects go in opposite directions, so the ranking of the sealed-bid auctions can go either way.
- **The conditions of the theorem.** The proof uses a symmetric increasing equilibrium in each format, differentiability, and a type 0 that pays 0. A format whose price given a win is not linked to the signals at all, such as the first-price auction, is the minimum in the ranking.
- **Correlation that is not affiliation.** Positive correlation alone does not give the monotone conditional expectations that the corollary needs.

## History

Milgrom and Weber (1982) built the model with affiliated signals, which contains private values and common values as special cases, and derived the symmetric equilibria of the English, second-price and first-price auctions. They showed that the revenue ranking is English, then second-price, then first-price, and that a seller gains by a policy of revealing its own information. The name "linkage principle" and the general form with the function $W$ come from the later presentations of their argument; Krishna (Chapter 7) gives the form used on this page. Perry and Reny (1999) showed that the principle fails with many units, and examples with asymmetric bidders show it fails there as well.

## References
