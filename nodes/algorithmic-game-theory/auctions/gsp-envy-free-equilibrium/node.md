---
tag: REN7TP
kind: theorem
slug: gsp-envy-free-equilibrium
name: Locally envy-free equilibrium of GSP
aliases:
- Edelman-Ostrovsky-Schwarz theorem
- Varian symmetric Nash equilibrium
area: algorithmic-game-theory/auctions
level: advanced
summary: "GSP has a locally envy-free equilibrium with the VCG slots and payments. Every envy-free equilibrium is efficient and pays at least VCG, so this bidder-optimal one matches VCG."
prereqs: [generalized-second-price-auction, vcg-mechanism, nash-equilibrium]
see_also: [position-auction, myerson-lemma, english-auction, assignment-game, price-of-anarchy, pacing-equilibrium, vickrey-auction, pareto-optimality]
sources:
  - paper: doi:10.1257/aer.97.1.242
    title: "Benjamin Edelman, Michael Ostrovsky and Michael Schwarz, Internet advertising and the generalized second-price auction: selling billions of dollars worth of keywords, American Economic Review 97(1) (2007), 242-259"
    locator: Section III (Definition 1 of a locally envy-free equilibrium, Lemmas 1 and 2, and Theorem 1 on the bids that give the VCG outcome) and Section IV (Theorem 2 on the generalized English auction)
  - paper: doi:10.1016/j.ijindorg.2006.10.002
    title: "Hal R. Varian, Position auctions, International Journal of Industrial Organization 25(6) (2007), 1163-1178"
    locator: the definition of a symmetric Nash equilibrium, the proof that such equilibria are efficient, and the bounds on their prices and revenue
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lectures 2 and 3 (sponsored search, the VCG payments for slots and the generalized second-price auction)
---

The [generalized second-price auction](/generalized-second-price-auction/) (GSP) is not truthful, but it has an equilibrium that looks exactly like the truthful [VCG mechanism](/vcg-mechanism/). Edelman, Ostrovsky and Schwarz (2007) gave explicit bids under which every bidder gets the efficient slot and pays its VCG payment, and no bidder wants to change its bid or envies the bidder just above it: a *locally envy-free equilibrium*. Varian (2007) studied the same profiles as *symmetric Nash equilibria*, in which no bidder envies any slot at the price that slot pays. Every such envy-free profile is efficient and charges every slot at least its VCG payment, so the VCG outcome is the bidder-optimal envy-free outcome of GSP, and the one with the least revenue.

## Statement

Take the [position auction](/position-auction/) with $k$ slots and click-through rates $\alpha_1 > \alpha_2 > \cdots > \alpha_k > 0$, and put $\alpha_t = 0$ for $t > k$. There are $n$ bidders, numbered so that their values per click are $v_1 \ge v_2 \ge \cdots \ge v_n \ge 0$, and put $v_t = 0$ for $t > n$. GSP has no reserve price, sorts the bids with ties broken by the smaller index, and charges the bidder in position $s$ the price $\pi_s = b_{(s+1)}$ per click, where $b_{(t)}$ is the $t$-th highest bid ($0$ if there is none). Let

$$P_s = \sum_{t = s}^{k} (\alpha_t - \alpha_{t+1})\, v_{t+1} \quad (1 \le s \le k), \qquad P_s = 0 \ (s > k)$$

be the VCG payment of slot $s$ for truthful values, and $p_s = P_s / \alpha_s$ its price per click for $s \le k$.

Call a bid profile **envy-free** if the bidder in each position $s$ weakly prefers its own slot to every other slot $t$ at the price that slot pays: $\alpha_s (w_s - \pi_s) \ge \alpha_t (w_s - \pi_t)$ for all $t$, where $w_s$ is the value of the bidder in position $s$. It is **locally envy-free** if this holds for $t = s - 1$, for every position $s \le \min(k + 1, n)$.

**Theorem** (Edelman, Ostrovsky and Schwarz 2007, Theorem 1; Varian 2007).

1. The bids $b^*_1 = v_1$, $b^*_s = p_{s-1}$ for $2 \le s \le \min(k + 1, n)$, and $b^*_s = v_s$ for $s > k + 1$ form a pure [Nash equilibrium](/nash-equilibrium/) of GSP that is envy-free, so also locally envy-free. In it bidder $s$ gets slot $s$ and pays exactly $P_s$, the VCG outcome.
2. In every envy-free profile, the slots go to the bidders in the order of their values, so the welfare is optimal, and the bidder in slot $s$ pays at least $P_s$.

So among envy-free profiles, the profile $b^*$ gives every bidder its largest utility at the same time, and gives the seller its least revenue, the VCG revenue.

## In plain words

In the ad auction that ranks bids and charges the next bid, honest bids are not always best. Still, there is a natural set of bids that every bidder is content with. In it the ads appear in the order of their real values, as they should, and each advertiser pays exactly what the truthful VCG auction would charge. No advertiser gains by changing its bid, and none would rather have another slot at that slot's price. Among all bid lists with this property, this one is the cheapest for every advertiser at once.

## Proof

Write $u_i(t) = \alpha_t (v_i - p_t)$ for the utility of bidder $i$ in slot $t \le k$ at the VCG price per click, and $u_i(t) = 0$ for $t > k$. In both cases $u_i(t) = \alpha_t v_i - P_t$.

**The VCG prices per click decrease.** From the definition, $P_k = \alpha_k v_{k+1}$ and $P_s = (\alpha_s - \alpha_{s+1}) v_{s+1} + P_{s+1}$ for $s < k$. So $p_k = v_{k+1}$, and for $s < k$, $p_s$ is a weighted average of $v_{s+1}$ and $p_{s+1}$ with weights $(\alpha_s - \alpha_{s+1})/\alpha_s$ and $\alpha_{s+1}/\alpha_s$. By induction from $s = k$ down, $p_s \le v_{s+1}$, and then $p_s \ge p_{s+1}$ because $v_{s+1} \ge v_{s+2} \ge p_{s+1}$.

**Part 1, the outcome.** The bids satisfy $b^*_1 = v_1 \ge v_2 \ge p_1 = b^*_2 \ge p_2 = b^*_3 \ge \cdots \ge p_k = v_{k+1} \ge v_{k+2} = b^*_{k+2} \ge \cdots$. With ties broken by index, bidder $s$ is in position $s$, and for $s \le k$ it pays $\alpha_s b^*_{s+1} = \alpha_s p_s = P_s$.

**Part 1, no envy.** For every $t$, $P_t - P_{t+1} = (\alpha_t - \alpha_{t+1}) v_{t+1}$; this also holds for $t \ge k$, where both sides are $0$ or $\alpha_k v_{k+1}$. So

$$u_i(t) - u_i(t + 1) = (\alpha_t - \alpha_{t+1})(v_i - v_{t+1}).$$

For $t \ge i$ the right side is at least 0, so summing over $t = i, \ldots, j - 1$ gives $u_i(i) \ge u_i(j)$ for $j > i$. For $t < i$ the right side is at most 0, so summing over $t = j, \ldots, i - 1$ gives $u_i(i) \ge u_i(j)$ for $j < i$. So no bidder envies any slot, which includes the slot just above.

**Part 1, Nash equilibrium.** Fix bidder $i$ and any other bid. The others keep their order, and $i$ lands in some position $j$. If $j = i$, nothing changes. If $j < i$, the bidder right below $i$ is the old holder of slot $j$, so $i$ pays $b^*_j$ per click; this is $v_1 \ge v_i$ if $j = 1$, giving utility at most 0, and $p_{j-1} \ge p_j$ if $j \ge 2$, giving utility at most $\alpha_j (v_i - p_j) = u_i(j)$. If $j > i$, the bidder right below $i$ is the old holder of position $j + 1$, so $i$ pays $b^*_{j+1} = p_j$ per click if $j \le k$, giving utility $u_i(j)$, and gets nothing if $j > k$. In every case the utility is at most $\max(0, u_i(j)) \le u_i(i)$, because $u_i(i) \ge u_i(t) = 0$ for a position $t > k$.

**Part 2, efficiency.** Take an envy-free profile, and positions $s < t$ with bidders of values $x$ and $y$. The bidder at $s$ does not envy $t$, and the bidder at $t$ does not envy $s$:

$$\alpha_s (x - \pi_s) \ge \alpha_t (x - \pi_t), \qquad \alpha_t (y - \pi_t) \ge \alpha_s (y - \pi_s).$$

Adding them gives $(\alpha_s - \alpha_t)(x - y) \ge 0$. If $s \le k$, then $\alpha_s > \alpha_t$, so $x \ge y$. So the bidders in slots $1, \ldots, k$ have the $k$ largest values in decreasing order, which maximizes $\sum_s \alpha_s w_s$. As numbers, $w_s = v_s$ for $s \le k$, and the largest value of a bidder with no slot is $v_{k+1}$.

**Part 2, payments.** A bidder with no slot does not envy slot $k$: $0 \ge \alpha_k (y - \pi_k)$, so $\pi_k \ge y$ for every such $y$, hence $\pi_k \ge v_{k+1}$ and $\alpha_k \pi_k \ge P_k$. For $s < k$, the bidder in position $s + 1$ does not envy slot $s$:

$$\alpha_{s+1} v_{s+1} - \alpha_{s+1}\pi_{s+1} \ge \alpha_s v_{s+1} - \alpha_s \pi_s, \quad\text{so}\quad \alpha_s \pi_s \ge (\alpha_s - \alpha_{s+1}) v_{s+1} + \alpha_{s+1}\pi_{s+1}.$$

The VCG payments satisfy the same relation with equality, so by induction from $s = k$ down, $\alpha_s \pi_s \ge P_s$ for every slot.

**Bidder-optimality.** In an envy-free profile, bidder $s$ gets $\alpha_s v_s - \alpha_s \pi_s \le \alpha_s v_s - P_s$, its utility under $b^*$, and the revenue $\sum_s \alpha_s \pi_s$ is at least $\sum_s P_s$. $\square$

## Consequences

- **GSP and VCG agree in a natural equilibrium.** Under the envy-free refinement, GSP gives the efficient allocation and at least the VCG revenue, even though its bids are not truthful. In this equilibrium, a platform that moves from GSP to VCG keeps the same allocation and the same revenue.
- **The generalized English auction.** In an ascending version of GSP in which the price per click rises and bidders drop out, there is a unique perfect Bayesian equilibrium with continuous strategies, and its outcome is the VCG outcome, whatever the distribution of values (Edelman, Ostrovsky and Schwarz 2007, Theorem 2).
- **Equilibrium bids are below values.** In $b^*$ every bidder except the top one bids $p_{s-1} \le v_s$, so it shades its bid, but it never bids above its value.
- **A computable equilibrium.** The bids $b^*$ take $O(n \log n + k)$ time to compute from the sorted values, by the recursion for $P_s$.

## Tightness

- **The local condition alone is not enough for Part 2.** Take one slot ($k = 1$, $\alpha_1 = 1$), values $5, 1, 8$, and bids $10, 2, 0$. The bidder with value 5 wins and pays 2. The bidder with value 1 is in position 2 and does not envy slot 1 at the price 2, so the profile is locally envy-free in the sense above. It is also a Nash equilibrium: to win, the bidder with value 8 must bid above 10 and would pay 10. But the welfare is 5 instead of 8, and the revenue 2 is below the VCG revenue 5. Here the bidder with value 8, in position 3, envies slot 1 at its price. So the payment bound needs the no-envy condition for every bidder, including those with no slot, as in Varian's definition.
- **Revenue can be higher.** Other envy-free profiles pay more than VCG. With one slot and values 5 and 3, the bids $5$ and $4$ are envy-free and pay 4, above the VCG payment 3. So the bound of Part 2 is attained only at the VCG outcome.
- **Nash equilibria that are not envy-free** can be inefficient, as the example above shows, so the refinement is needed for efficiency.
- **Strictly decreasing rates.** If two slots have the same click-through rate, the bidders in them can appear in either order, and the statement holds for the welfare but the order of values in those slots is not fixed.

## History

Google adopted the generalized second-price rule in 2002, and in the following years it became the standard format for search ads. Edelman, Ostrovsky and Schwarz (2007) showed that the auction is not truthful, defined locally envy-free equilibria, showed that the bids $b^*$ form one with the VCG outcome, and analyzed the generalized English auction. Varian (2007) independently defined symmetric Nash equilibria of position auctions, proved their efficiency and revenue bounds, and fitted them to data from search ads.

## References
