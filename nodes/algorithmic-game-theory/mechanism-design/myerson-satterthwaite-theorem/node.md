---
tag: DGX7N8
kind: theorem
slug: myerson-satterthwaite-theorem
name: Myerson-Satterthwaite theorem
aliases:
- impossibility of efficient bilateral trade
area: algorithmic-game-theory/mechanism-design
level: core
summary: "With independent private values on overlapping intervals with positive densities, no BIC, interim IR and weakly budget balanced mechanism trades efficiently between a buyer and a seller."
prereqs: [bayesian-incentive-compatibility, individual-rationality, budget-balance, independent-private-values]
see_also: [agv-mechanism, vcg-mechanism, double-auction, mcafee-trade-reduction, green-laffont-theorem, revenue-equivalence-theorem, cremer-mclean-theorem, automated-mechanism-design]
sources:
  - paper: doi:10.1016/0022-0531(83)90048-0
    title: "Roger B. Myerson and Mark A. Satterthwaite, Efficient mechanisms for bilateral trading, Journal of Economic Theory 29(2) (1983), 265-281"
    locator: Theorem 1 (p. 269, the formula for the gains of the worst types), Corollary 1 (p. 273, the impossibility), the discrete counterexample (p. 273), Theorem 2 and the uniform example (pp. 274-277)
  - paper: doi:10.1287/opre.31.5.835
    title: "Kalyan Chatterjee and William Samuelson, Bargaining under incomplete information, Operations Research 31(5) (1983), 835-851"
    locator: the sealed-bid double auction in which the price is the average of the two bids, and its linear equilibrium for uniform values
  - book: isbn:9780195073409
    title: Andreu Mas-Colell, Michael D. Whinston and Jerry R. Green, Microeconomic Theory, Oxford University Press, 1995
    locator: Chapter 23, Section 23.E (participation constraints and the Myerson-Satterthwaite theorem)
  - book: isbn:9780123745071
    title: Vijay Krishna, Auction Theory, 2nd edition, Academic Press, 2010
    locator: Chapter 5 (mechanism design, efficiency and budget balance in bilateral trade)
  - paper: doi:10.2307/1913602
    title: "Peter Cramton, Robert Gibbons and Paul Klemperer, Dissolving a partnership efficiently, Econometrica 55(3) (1987)"
    locator: efficient dissolution is possible when the ownership shares are close enough to equal, in contrast with bilateral trade
---

The Myerson-Satterthwaite theorem says that a buyer and a seller who each know only their own value cannot be brought to trade exactly when trade is worth it, by any mechanism that is incentive compatible, that each side is willing to join, and that needs no money from outside. It holds under independent private values with overlapping ranges and positive densities, and it uses only Bayesian incentive compatibility and interim individual rationality, so it rules out dominant-strategy mechanisms too. The result is the reason why double auctions and bargaining lose some gains from trade. The [AGV mechanism](/agv-mechanism/) and the [VCG mechanism](/vcg-mechanism/) each give up one of the three conditions; this page proves that one must always be given up.

## Statement

A seller owns one indivisible good and has cost (value for the good) $c$. A buyer has value $v$ for it. The cost $c$ is drawn from a distribution $F_s$ on $[a_s, b_s]$ and the value $v$ from $F_b$ on $[a_b, b_b]$. The two are independent, each side knows only its own number, and both distributions have densities that are positive on their intervals. The intervals overlap: $a_b < b_s$ and $a_s < b_b$. These are [independent private values](/independent-private-values/).

A direct mechanism takes reports and gives a trade probability $x(v, c) \in [0, 1]$, a payment $p_b(v, c)$ by the buyer and a receipt $r_s(v, c)$ for the seller. Utilities are quasilinear: the buyer gets $v\, x - p_b$ and the seller $r_s - c\, x$, with no trade and no money worth 0 to both. For the interim versions, write $X_b(v) = \mathbb{E}_c[x(v, c)]$, $U_b(v) = \mathbb{E}_c[v\, x(v, c) - p_b(v, c)]$, $X_s(c) = \mathbb{E}_v[x(v, c)]$ and $U_s(c) = \mathbb{E}_v[r_s(v, c) - c\, x(v, c)]$, all under truthful reports.

**Theorem (Myerson and Satterthwaite 1983).** No mechanism has all four properties:

1. [BIC](/bayesian-incentive-compatibility/): truth telling is a Bayes-Nash equilibrium.
2. Interim [individual rationality](/individual-rationality/): $U_b(v) \ge 0$ for every $v$ and $U_s(c) \ge 0$ for every $c$.
3. Weak [budget balance](/budget-balance/): $p_b(v, c) \ge r_s(v, c)$ at every profile. In fact the proof needs it only in expectation.
4. Ex post efficiency: $x(v, c) = 1$ when $v > c$ and $x(v, c) = 0$ when $v < c$.

More precisely, every mechanism with properties 1, 2 and 4 has expected budget surplus

$$\mathbb{E}[p_b - r_s] \ \le\ -\int_{L}^{H} F_s(t)\,\big(1 - F_b(t)\big)\, dt \ <\ 0, \qquad L = \max(a_s, a_b),\ H = \min(b_s, b_b),$$

and the bound is attained by a shifted VCG mechanism. The paper labels the seller as trader 1 and the buyer as trader 2, and its mechanisms have a single payment from buyer to seller, which is strong budget balance. Its Theorem 1 and equation (7) give the same integral, with $a_2$ and $b_1$ for the limits when $a_s \le a_b$ and $b_s \le b_b$. The form here allows a broker who keeps money and so covers weak budget balance.

### Example

Let $v$ and $c$ be uniform on $[0, 1]$. Then $F_s(t) = t$, $1 - F_b(t) = 1 - t$, and the bound is $-\int_0^1 t(1 - t)\, dt = -1/6$. The expected gains from efficient trade are $\mathbb{E}[(v - c)^+] = 1/6$ as well. So an efficient mechanism that both sides join must be subsidized with $1/6$ in expectation, which is all the gains from trade.

Myerson and Satterthwaite also find the mechanism with the largest expected gains among those with properties 1 to 3. For uniform values it trades exactly when $v \ge c + 1/4$. Its expected gains are

$$\int_0^{3/4} \int_{c + 1/4}^{1} (v - c)\, dv\, dc = \frac{9}{64},$$

which is $27/32$ of the first-best $1/6 = 32/192$; the lost $5/192$ comes from pairs with $0 < v - c < 1/4$. The same trades happen in the linear equilibrium of the Chatterjee-Samuelson double auction, where the seller asks $\frac{2}{3}c + \frac{1}{4}$, the buyer bids $\frac{2}{3}v + \frac{1}{12}$, and trade takes place at the average of the two when the bid is at least the ask.

## In plain words

A buyer and a seller each know what the good is worth to them, and nobody else does. If they report honestly, a referee could make them trade exactly when the buyer values the good more. But each side can shade its report: the seller can claim a higher cost and the buyer a lower value, to get a better price. To stop this, the referee must reward honest reports, and those rewards cost money. If both sides must be willing to take part, and nobody outside pays the rewards, the money runs out. So some good trades must be missed, or someone must pay in, or someone must be allowed to lose.

## Proof

The proof computes how much utility the incentive constraints force the mechanism to leave with the two traders, and compares it with the gains from trade.

**Step 1: the buyer's utility.** Let the mechanism be BIC. A buyer of value $v$ can report $v'$, which gives the trade probability $X_b(v')$ and the expected payment of type $v'$. So

$$U_b(v) \ \ge\ v\, X_b(v') - \mathbb{E}_c[p_b(v', c)] \ =\ U_b(v') + (v - v')\, X_b(v').$$

Take $v > a_b$ and points $a_b = w_0 < w_1 < \cdots < w_K = v$. Apply the inequality with $v = w_{k+1}$ and $v' = w_k$, and add over $k$:

$$U_b(v) - U_b(a_b) \ \ge\ \sum_{k=0}^{K-1} (w_{k+1} - w_k)\, X_b(w_k).$$

Under ex post efficiency, $X_b(w) = \Pr[c < w] = F_s(w)$, which is continuous because $F_s$ has a density. As the points get finer, the sum tends to the integral, so $U_b(v) \ge U_b(a_b) + \int_{a_b}^{v} F_s(t)\, dt$.

**Step 2: the seller's utility.** In the same way, a seller of cost $c$ who reports $c'$ gets $U_s(c) \ge U_s(c') - (c - c')\, X_s(c')$. With points $c = w_0 < \cdots < w_K = b_s$, apply it with $c = w_k$ and $c' = w_{k+1}$ and add:

$$U_s(c) - U_s(b_s) \ \ge\ \sum_{k=0}^{K-1} (w_{k+1} - w_k)\, X_s(w_{k+1}) \ \to\ \int_c^{b_s} \big(1 - F_b(t)\big)\, dt,$$

because efficiency gives $X_s(t) = \Pr[v > t] = 1 - F_b(t)$.

**Step 3: interim IR.** Property 2 at the worst types gives $U_b(a_b) \ge 0$ and $U_s(b_s) \ge 0$. Only these two constraints are used. Write $g(t) = F_s(t)(1 - F_b(t))$. Taking expectations of the bounds in Steps 1 and 2 and exchanging the order of integration,

$$\mathbb{E}[U_b(v)] \ \ge\ \int_{a_b}^{b_b} F_s(t) \Pr[v > t]\, dt = \int_{a_b}^{b_b} g(t)\, dt, \qquad \mathbb{E}[U_s(c)] \ \ge\ \int_{a_s}^{b_s} \big(1 - F_b(t)\big) \Pr[c < t]\, dt = \int_{a_s}^{b_s} g(t)\, dt.$$

**Step 4: the gains from trade.** Since $(v - c)^+ = \int 1[c < t < v]\, dt$ and $v$ and $c$ are independent, $\mathbb{E}[(v - c)^+] = \int g(t)\, dt$. The function $g$ is zero below $a_s$ (where $F_s = 0$) and above $b_b$ (where $F_b = 1$), so this is $\int_{a_s}^{b_b} g$.

**Step 5: the budget.** By the definitions of $U_b$ and $U_s$,

$$\mathbb{E}[p_b - r_s] = \mathbb{E}[(v - c)\, x(v, c)] - \mathbb{E}[U_b] - \mathbb{E}[U_s] = \mathbb{E}[(v - c)^+] - \mathbb{E}[U_b] - \mathbb{E}[U_s],$$

where the second equality uses efficiency. The two bounds of Step 3 cover $[\max(a_b, a_s), b_b]$ and $[a_s, \min(b_s, b_b)]$ after dropping the parts where $g = 0$. Their union is $[a_s, b_b]$ and their overlap is $[L, H]$, which is a proper interval by the overlap hypothesis. So

$$\mathbb{E}[p_b - r_s] \ \le\ \int_{a_s}^{b_b} g - \int_{a_s}^{b_b} g - \int_L^H g = -\int_L^H g(t)\, dt.$$

On the open interval $(L, H)$, $t > a_s$ gives $F_s(t) > 0$ and $t < b_b$ gives $F_b(t) < 1$, since both densities are positive. So the integral is positive and the expected budget surplus is negative. Weak budget balance at every profile would make it nonnegative, so properties 1 to 4 cannot hold together. $\blacksquare$

**The bound is tight.** Take the VCG mechanism for this setting: trade when $v > c$, the buyer pays $c$ and the seller receives $v$. Each side then gets the whole gain $(v - c)^+$, truth is dominant, and the deficit is $\mathbb{E}[(v - c)^+]$. Charge the buyer an entry fee $K_b = \mathbb{E}_c[(a_b - c)^+]$, the utility of the lowest buyer, and the seller $K_s = \mathbb{E}_v[(v - b_s)^+]$, the utility of the highest seller. This keeps DSIC and interim IR and makes the inequalities of Steps 1 to 3 hold with equality, so the deficit equals $\int_L^H g$. With uniform values, $K_b = K_s = 0$ and the deficit is $1/6$.

## Consequences

- **Bilateral trade loses gains.** Every BIC, interim IR and budget balanced mechanism misses some efficient trades. With uniform values the best one keeps $27/32$ of the gains, as in the example, and the Chatterjee-Samuelson [double auction](/double-auction/) reaches this bound in one of its equilibria.
- **Dominant strategies do not help.** DSIC implies BIC and ex post IR implies interim IR, so no DSIC, ex post IR and budget balanced mechanism is efficient either. This is a two-sided cousin of the [Green-Laffont theorem](/green-laffont-theorem/), which forbids efficiency with exact budget balance in dominant strategies.
- **Each property can be kept by dropping another.** VCG with entry fees keeps efficiency, DSIC and IR, and runs the deficit above. [AGV](/agv-mechanism/) keeps efficiency, BIC and exact budget balance, and fails interim IR. A posted price keeps DSIC, ex post IR and budget balance, and misses trades.
- **Large markets.** With many buyers and sellers, mechanisms such as [McAfee's trade reduction](/mcafee-trade-reduction/) lose at most one efficient trade, so the share of lost gains goes to zero as the market grows. The impossibility is sharpest with one buyer and one seller.
- **VCG is the best efficient mechanism for the budget.** Steps 1 to 3 hold with equality for VCG with entry fees, so among all efficient, BIC and interim IR mechanisms it has the largest expected budget surplus. To decide whether some efficient mechanism can balance the budget, it is enough to compute the expected surplus of this one VCG mechanism.

## Tightness

Each hypothesis is needed.

- **Overlap.** If $b_s \le a_b$, a posted price $q$ with $b_s \le q \le a_b$ always trades, which is efficient, and both sides gain. If $b_b \le a_s$, never trading is efficient. In both cases the integral in the bound is over an empty interval.
- **Densities.** With discrete values the conclusion can fail. Myerson and Satterthwaite give this example: the seller's cost is 1 or 4 and the buyer's value is 0 or 3, each with probability 1/2. Trade is efficient only when the cost is 1 and the value is 3, and "trade at price 2 when both agree" is DSIC, ex post IR, budget balanced and efficient, although the ranges $[1, 4]$ and $[0, 3]$ overlap.
- **Independence.** With correlated values, mechanisms can bet on one trader's report against the other's beliefs, as in the [Cremer-McLean theorem](/cremer-mclean-theorem/), and efficient trade can become possible.
- **Ownership.** The seller owns the whole good. Cramton, Gibbons and Klemperer show that when two or more partners own shares that are close enough to equal, efficient dissolution of the partnership is possible with BIC, IR and budget balance. The hard case is the extreme ownership of bilateral trade.
- **Interim IR at the worst types.** Without IR, AGV is efficient, BIC and balanced. Only the two constraints $U_b(a_b) \ge 0$ and $U_s(b_s) \ge 0$ are used, so asking for IR at all types costs nothing more.

## History

Chatterjee and Samuelson (1983) studied the sealed-bid double auction with the average price and found its linear equilibrium. In the same year Myerson and Satterthwaite proved, by a characterization of all BIC and IR mechanisms, that no mechanism trades efficiently without a subsidy, and they found the mechanism with the largest expected gains. Their method, the payment identity of Steps 1 and 2 combined with the worst-type IR constraints, became the standard tool of Bayesian mechanism design. Cramton, Gibbons and Klemperer (1987) then showed how much the conclusion depends on who owns the good.

## References
