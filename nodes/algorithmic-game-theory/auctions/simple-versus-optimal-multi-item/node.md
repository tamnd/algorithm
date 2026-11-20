---
tag: 750GJ2
kind: theorem
slug: simple-versus-optimal-multi-item
name: Selling separately or as a bundle
aliases:
- Babaioff-Immorlica-Lucier-Weinberg theorem
- max of separate and bundle
area: algorithmic-game-theory/auctions
level: research
summary: "For an additive buyer with independent item values, the better of selling the items separately and selling the grand bundle earns at least 1/6 of the optimal revenue."
prereqs: [myerson-optimal-auction, independent-private-values, chebyshev-inequality]
see_also: [sequential-posted-pricing, bulow-klemperer-theorem, combinatorial-auction, vcg-mechanism, quasilinear-utility, individual-rationality, revelation-principle, sample-complexity-of-revenue-maximization]
sources:
  - paper: doi:10.1145/3398745
    title: "Moshe Babaioff, Nicole Immorlica, Brendan Lucier and S. Matthew Weinberg, A simple and approximately optimal mechanism for an additive buyer, Journal of the ACM 67(4) (2020), Article 24"
    locator: Theorem 2 in Section 6.2 (the factor 6), Lemma 6 (the core-tail decomposition), Propositions 3 and 4 (the bounds on the tail and the core), and the examples in the introduction
  - paper: doi:10.1016/j.jet.2017.09.001
    title: "Sergiu Hart and Noam Nisan, Approximate revenue maximization with multiple items, Journal of Economic Theory 172 (2017), 313-347"
    locator: the bounds for selling separately (at least 73% of the optimal revenue for two i.i.d. items, 50% for two independent items, and c/log^2 k for k independent items) and for bundling (c/log k for k i.i.d. items)
---

A seller has $m$ different items and one buyer whose value for a set of items is the sum of its values for the items, with the item values drawn independently. The revenue-optimal mechanism for this buyer can be complex: it can need lotteries even for two items. Two simple mechanisms are to post a separate price for each item, and to post one price for the bundle of all items. Each of the two alone can lose a large factor. Babaioff, Immorlica, Lucier and Weinberg proved that the better of the two always earns at least $1/6$ of the optimal revenue. Their proof splits the values into a *core* of small values, which concentrates and so is sold well as a bundle, and a *tail* of large values, which is rare and so is sold well item by item.

## Statement

There is one buyer with [quasilinear utility](/quasilinear-utility/) and $m$ items. The buyer's value $v_i \ge 0$ for item $i$ is drawn from a distribution $D_i$, the values are independent, and $D = D_1 \times \cdots \times D_m$. The buyer is additive: its value for a set $S$ of items, or for a lottery that gives item $i$ with probability $\pi_i$, is $\sum_i \pi_i v_i$. Define:

- $\mathrm{Rev}(D)$, the supremum of the expected revenue over all mechanisms that are incentive compatible and [individually rational](/individual-rationality/) for this buyer, including mechanisms with lotteries. By the [revelation principle](/revelation-principle/) these are menus of lotteries with prices, from which the buyer picks its best entry.
- $\mathrm{SRev}(D) = \sum_i \mathrm{Rev}(D_i)$, the revenue of selling separately: item $i$ gets the optimal single-item price for $D_i$.
- $\mathrm{BRev}(D)$, the revenue of grand bundling: the best single price for the set of all items, which is $\mathrm{Rev}$ of the distribution of $\sum_i v_i$.

**Theorem (Babaioff, Immorlica, Lucier and Weinberg).** For every $m$ and every product distribution $D$,

$$\mathrm{Rev}(D) \le 6 \max\{\mathrm{SRev}(D), \mathrm{BRev}(D)\}.$$

So the seller who offers the buyer the better of the two simple menus earns at least $1/6$ of the optimal revenue. Since both are mechanisms, $\max\{\mathrm{SRev}, \mathrm{BRev}\} \le \mathrm{Rev}$.

## In plain words

Selling many items to one buyer in the best possible way can require strange menus with lotteries. Yet two plain options are always close to the best. One is a price tag on each item. The other is one price for the whole set. When the buyer's values are mostly small and many, the total is predictable, and one price for the whole set takes most of it. When a few values are rare and large, separate prices catch them. Every distribution is a mix of these two parts, so the better of the two plain options always earns at least one sixth of what the best mechanism earns. This works only when the item values are independent.

## Proof

Write $r_i = \mathrm{Rev}(D_i)$ and $r = \mathrm{SRev}(D) = \sum_i r_i$, and assume $r > 0$ (if $r = 0$ every value is 0 almost surely). For a distribution $X$ on a set of items, $\mathrm{Val}(X) = \mathbb{E}_{x \sim X}[\sum_i x_i]$ is the expected welfare. A fact used twice: for a single item with value distribution $D_i$ and any price $x$, $x \Pr[v_i \ge x] \le r_i$.

**Split into core and tail.** Use the threshold $r$ for every item. Item $i$ is in the *tail* if $v_i > r$ and in the *core* otherwise. Let $p_i = \Pr[v_i > r]$. The price $r$ on item $i$ earns $r p_i \le r_i$, so $p_i \le r_i / r$ and $\sum_i p_i \le 1$. For a set $A$ of items, let $p_A$ be the probability that the tail is exactly $A$. Let $D_A^T$ be the distribution of the values of the items in $A$, each conditioned on being above $r$, and $D_{\bar A}^C$ that of the other items, each conditioned on being at most $r$. By independence, the distribution $D$ conditioned on the tail being $A$ is the product $D_{\bar A}^C \times D_A^T$.

**Lemma 1 (marginal mechanism).** For independent $X$ and $Y$ on disjoint sets of items, $\mathrm{Rev}(X \times Y) \le \mathrm{Val}(X) + \mathrm{Rev}(Y)$.

*Proof.* Take a mechanism $M$ for $X \times Y$ with allocation $(q_X, q_Y)$ and payment $p$. Build $M'$ for $Y$ alone: the seller draws $x \sim X$ itself, the buyer reports $y$, and $M'$ gives the lottery $q_Y(x, y)$ for the items of $Y$ and charges $p(x, y) - x \cdot q_X(x, y)$. The utility of type $y$ in $M'$ for each report equals the utility of type $(x, y)$ in $M$ for the same report of $y$, so $M'$ is incentive compatible and individually rational. Its revenue is $\mathbb{E}[p] - \mathbb{E}[x \cdot q_X] \ge \mathrm{Rev}(M) - \mathrm{Val}(X)$. $\square$

**Lemma 2 (core-tail decomposition).** With $V = \sum_i v_i \mathbf{1}[v_i \le r]$, the value of the core,

$$\mathrm{Rev}(D) \le \mathbb{E}[V] + \sum_A p_A\, \mathrm{Rev}(D_A^T).$$

*Proof.* An optimal mechanism for $D$ earns $\sum_A p_A$ times its revenue on $D$ conditioned on the tail being $A$, and each of these is at most $\mathrm{Rev}(D_{\bar A}^C \times D_A^T)$. By Lemma 1 this is at most $\mathrm{Val}(D_{\bar A}^C) + \mathrm{Rev}(D_A^T)$. Finally $\sum_A p_A \mathrm{Val}(D_{\bar A}^C) = \sum_i \Pr[v_i \le r]\, \mathbb{E}[v_i \mid v_i \le r] = \mathbb{E}[V]$. $\square$

**The tail earns at most $2\,\mathrm{SRev}$.** Two bounds are needed. First, for any product distribution $E$ on $k$ items, $\mathrm{Rev}(E) \le k \cdot \mathrm{SRev}(E)$ (Lemma 2 of Babaioff et al., in its form for one buyer). Second, for an item $i$ with $p_i > 0$, a price $x$ for $D_i^T$ earns $x \Pr[v_i \ge x \mid v_i > r] \le x \Pr[v_i \ge x]/p_i \le r_i / p_i$, so $\mathrm{Rev}(D_i^T) \le r_i / p_i$. Hence

$$\sum_A p_A \mathrm{Rev}(D_A^T) \le \sum_A p_A |A| \sum_{i \in A} \frac{r_i}{p_i} = \sum_i \frac{r_i}{p_i}\, \mathbb{E}\big[|A|\, \mathbf{1}[i \in A]\big] = \sum_i r_i \Big(1 + \sum_{j \ne i} p_j\Big) \le 2r,$$

where the middle step uses that the events $j \in A$ are independent, and the last step uses $\sum_j p_j \le 1$.

**The core earns at most $4 \max\{\mathrm{SRev}, \mathrm{BRev}\}$.** Let $C = \mathbb{E}[V]$. If $C \le 4r$, then $C \le 4\,\mathrm{SRev}$. Otherwise $C > 4r$, and the bundle price $\frac{2}{5} C$ does well. The terms $w_i = v_i \mathbf{1}[v_i \le r]$ are independent and lie in $[0, r]$, and $\Pr[w_i \ge x] \le \Pr[v_i \ge x] \le r_i / x$ for $x > 0$. So

$$\mathrm{Var}(w_i) \le \mathbb{E}[w_i^2] = \int_0^r 2x \Pr[w_i \ge x]\, dx \le \int_0^r 2x \min\Big(1, \frac{r_i}{x}\Big) dx \le 2 r r_i,$$

and $\mathrm{Var}(V) \le 2r \sum_i r_i = 2r^2$. This variance bound is a form of a lemma of Li and Yao. By [Chebyshev's inequality](/chebyshev-inequality/),

$$\Pr\Big[V < \tfrac{2}{5} C\Big] \le \frac{\mathrm{Var}(V)}{(3C/5)^2} \le \frac{50 r^2}{9 C^2} < \frac{50}{9 \cdot 16} = \frac{25}{72}.$$

Since $\sum_i v_i \ge V$, the bundle at price $\frac{2}{5} C$ sells with probability more than $47/72$, so $\mathrm{BRev} \ge \frac{2}{5} \cdot \frac{47}{72} C = \frac{47}{180} C > \frac{C}{4}$.

**Conclusion.** By Lemma 2 and the two bounds, $\mathrm{Rev}(D) \le C + 2r \le 4 \max\{\mathrm{SRev}, \mathrm{BRev}\} + 2\,\mathrm{SRev} \le 6 \max\{\mathrm{SRev}, \mathrm{BRev}\}$. $\blacksquare$

## Consequences

- **Two simple menus suffice up to a constant.** The seller does not need to compute the optimal mechanism, which can need lotteries. It can compute two quantities, each from one-dimensional distributions, and offer the better menu.
- **The examples that motivate the theorem.** Two i.i.d. items with values uniform on $\{1, 2\}$: each item earns 1 alone, so $\mathrm{SRev} = 2$, while the bundle at price 3 sells with probability $3/4$ and earns $9/4$. Two items with $v_1$ uniform on $\{1, 2\}$ and $v_2$ uniform on $\{1, 3\}$: $\mathrm{SRev} = 1 + 3/2 = 5/2$ and $\mathrm{BRev} = 9/4$, but the menu "both items for 4, or item 1 together with item 2 with probability $1/2$ for $5/2$" earns $21/8$, with ties broken in favor of the seller. Daskalakis, Deckelbaum and Tzamos showed that this lottery menu is optimal.
- **Selling separately alone is not enough.** Let the $m$ values be i.i.d. from the equal-revenue distribution $\Pr[v_i \ge x] = 1/x$ for $x \ge 1$. Every price earns at most 1 per item, so $\mathrm{SRev} = m$. The truncated values $\min(v_i, m)$ have mean $1 + \ln m$ and second moment $2m - 1$, so by Chebyshev's inequality the sum is at least $\frac{1}{2} m \ln m$ with probability at least $1 - 8/\ln^2 m$. So $\mathrm{BRev} \ge \frac{1}{2} m \ln m \,(1 - 8/\ln^2 m)$, larger than $\mathrm{SRev}$ by a factor that grows with $m$.
- **Bundling alone is not enough.** Let $v_i = 2^i$ with probability $2^{-i}$ and $v_i = 0$ otherwise, for $i = 1, \ldots, m$. Each item earns 1 alone, so $\mathrm{SRev} = m$. If the largest nonzero value is $2^j$, the sum is less than $2^{j+1}$, so the sum is at least $x$ with probability at most $\sum_{2^i > x/2} 2^{-i} \le 4/x$, and $\mathrm{BRev} \le 4$.
- **Many buyers.** For several additive buyers with independent values, selling separately with the optimal single-item auction per item is an $O(\log m)$ approximation (Theorem 3 of Babaioff et al.), but the better of separate sales and grand bundling is not a constant approximation. Yao (2015) found a constant factor with a VCG mechanism plus an entry fee, Rubinstein and Weinberg (2015) extended the single-buyer result to subadditive buyers, and Cai, Devanur and Weinberg (2016) gave a unified proof by duality.

## Tightness

- **The constant.** The first versions of the paper proved the factor 7.5, and an observation of Rubinstein improved it to 6, the factor above. The journal version reports a later analysis with the factor 5.2. In the other direction, Rubinstein built an instance in which $\max\{\mathrm{SRev}, \mathrm{BRev}\} = (1/2 + o(1))\, \mathrm{Rev}$, so no constant below 2 is possible. The exact constant is open.
- **Neither menu alone.** The two examples in the section above show that the maximum cannot be replaced by $\mathrm{SRev}$ alone or by $\mathrm{BRev}$ alone: each of them loses a factor that grows with $m$.
- **Assumptions.** The proof uses the independence of the item values in Lemma 1, in the tail bound and in the variance bound, and it uses additivity in Lemma 1 and in the bound $\sum_i v_i \ge V$.

## History

Hart and Nisan (EC 2012, Journal of Economic Theory 2017) started the study of simple mechanisms for one additive buyer. They showed that selling separately earns at least a $c/\log^2 m$ fraction of the optimal revenue for independent items, and that bundling earns a $c/\log m$ fraction for i.i.d. items. Li and Yao (2013) improved the bound for separate sales to $O(\log m)$, which is tight, and showed that bundling is a constant approximation for i.i.d. items. Their proof introduced the core-tail decomposition. Babaioff, Immorlica, Lucier and Weinberg (FOCS 2014, Journal of the ACM 2020) combined the two menus and proved the constant factor for independent, not necessarily identical, items. A warm-up result in their paper gives $\mathrm{Rev} \le (\ln m + 3)\, \mathrm{SRev}$.

## References
