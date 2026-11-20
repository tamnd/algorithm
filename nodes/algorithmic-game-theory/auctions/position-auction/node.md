---
tag: ZAC1D5
kind: model
slug: position-auction
name: Position auction
aliases:
- sponsored search auction
area: algorithmic-game-theory/auctions
level: core
summary: "A model of ad auctions: k ranked slots with click-through rates that fall from the top, the same for every ad, and bidders with a private value per click."
prereqs: [quasilinear-utility, vickrey-auction, single-parameter-environment]
see_also: [generalized-second-price-auction, gsp-envy-free-equilibrium, vcg-mechanism, myerson-lemma, assignment-game, pacing-equilibrium, online-adwords-problem, combinatorial-auction]
sources:
  - paper: doi:10.1016/j.ijindorg.2006.10.002
    title: "Hal R. Varian, Position auctions, International Journal of Industrial Organization 25(6) (2007), 1163-1178"
    locator: the model of position auctions with separable click-through rates, and its symmetric Nash equilibria
  - paper: doi:10.1257/aer.97.1.242
    title: "Benjamin Edelman, Michael Ostrovsky and Michael Schwarz, Internet advertising and the generalized second-price auction: selling billions of dollars worth of keywords, American Economic Review 97(1) (2007), 242-259"
    locator: the model of sponsored search slots, the generalized second-price auction and the VCG mechanism in it
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lectures 2 and 3 (sponsored search, Myerson's lemma and the payment formula for slots)
---

A position auction is the model of selling ad slots on a page of search results. There are $k$ slots ranked from the top, and slot $s$ gets $\alpha_s$ clicks, with $\alpha_1 \ge \alpha_2 \ge \cdots \ge \alpha_k$. The same numbers hold for every ad. Each bidder has a private value per click and wants to be as high as possible at a low price. Because a bidder's value for slot $s$ is its value per click times $\alpha_s$, the model is a [single-parameter environment](/single-parameter-environment/), and [Myerson's lemma](/myerson-lemma/) gives the truthful mechanisms. Varian (2007) and Edelman, Ostrovsky and Schwarz (2007) introduced it to study the [generalized second-price auction](/generalized-second-price-auction/), the format that search engines used.

## The machine

- **Slots.** There are $k$ slots with click-through rates $\alpha_1 \ge \alpha_2 \ge \cdots \ge \alpha_k \ge 0$. The rates are known to everyone and do not depend on the ad in the slot. Put $\alpha_s = 0$ for $s > k$.
- **Bidders.** There are $n$ bidders. Bidder $i$ has a private value $v_i \ge 0$ per click.
- **Outcomes.** A mechanism gives each slot to at most one bidder and each bidder at most one slot, and sets a payment $P_i$. A bidder in slot $s$ gets $\alpha_s$ clicks.
- **Utility.** [Quasilinear](/quasilinear-utility/): bidder $i$ in slot $s$ gets $\alpha_s v_i - P_i$, and a bidder with no slot gets $-P_i$, usually 0.
- **Bids.** Mechanisms usually ask for one bid per click, and charge a price per click $\pi_i$, so that $P_i = \alpha_s \pi_i$.

## What it counts

- **Welfare** $\sum_i \alpha_{s(i)} v_i$. It is largest when slots go to bidders in the order of their values: the highest value gets slot 1, and so on.
- **Revenue** $\sum_i P_i$.
- **Incentives.** Whether truthful bidding is dominant, and if not, which equilibria the bidders reach. For the generalized second-price auction the usual solution concept is the [locally envy-free equilibrium](/gsp-envy-free-equilibrium/).
- **Computation** is easy: sorting the bids gives the efficient allocation in $O(n \log n)$ time.

## Relation to other models

- With one slot it is the single-item auction, and the [Vickrey auction](/vickrey-auction/) is the truthful efficient mechanism.
- It is a special case of the [assignment game](/assignment-game/), in which bidder $i$ values slot $s$ at $\alpha_s v_i$. The product form makes the efficient assignment a sort, and it makes the envy-free prices form a lattice with a simple bottom element.
- It is a special case of a [combinatorial auction](/combinatorial-auction/) with unit-demand bidders.
- Models with budgets add a spending limit per bidder; see [pacing equilibrium](/pacing-equilibrium/) and the [online AdWords problem](/online-adwords-problem/).
- Extensions let the click-through rate depend on the ad, as $\alpha_s \beta_i$ for an ad quality $\beta_i$; ranking by $\beta_i b_i$ then reduces to the basic model.

## Known results in the model

- **VCG.** The [VCG mechanism](/vcg-mechanism/) sorts by bid and charges the bidder in slot $s$ the externality $\sum_{t = s}^{k} (\alpha_t - \alpha_{t+1})\, b_{(t+1)}$, where $b_{(t)}$ is the $t$-th highest bid. It is truthful and efficient. This formula is also the payment of [Myerson's lemma](/myerson-lemma/) for the monotone rule that sorts by bid.
- **GSP is not truthful.** The [generalized second-price auction](/generalized-second-price-auction/) charges $\alpha_s b_{(s+1)}$. With $k \ge 2$ truthful bidding is not dominant, as the example with values $10, 4, 2$ and rates $200, 199$ shows (Edelman, Ostrovsky and Schwarz 2007).
- **GSP equilibria.** GSP has a locally envy-free equilibrium with the same allocation and payments as VCG, and every envy-free equilibrium is efficient and pays at least the VCG payments (Edelman, Ostrovsky and Schwarz 2007; Varian 2007); see the [theorem page](/gsp-envy-free-equilibrium/).
- **Optimal revenue.** With values drawn independently from a [regular distribution](/regular-distribution/), the revenue-optimal mechanism sorts by [virtual value](/virtual-valuation/), drops bidders with negative virtual values, and charges threshold payments. With identical regular distributions, this is VCG or GSP with a [reserve price](/reserve-price/) that solves $\varphi(r) = 0$.
- **Price of anarchy.** Pure Nash equilibria of GSP can have welfare below the optimum, but by a bounded factor, and smoothness arguments extend the bounds to Bayes-Nash equilibria; see [price of anarchy](/price-of-anarchy/).

## References
