---
tag: JVH3TC
kind: model
slug: fisher-market
name: Fisher market
aliases:
- Fisher market model
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: A market of buyers with budgets and sellers with fixed supplies of goods. Prices clear the market when all budgets are spent and goods sold.
prereqs: [competitive-equilibrium]
see_also: [arrow-debreu-market, eisenberg-gale-program, dpsv-algorithm, orlin-fisher-market-algorithm, proportional-response-dynamics, tatonnement, competitive-equilibrium-from-equal-incomes, maximum-nash-welfare]
sources:
  - paper: doi:10.1111/j.1536-7150.2005.00349.x
    title: "William C. Brainard and Herbert E. Scarf, How to compute equilibrium prices in 1891, American Journal of Economics and Sociology 64(1), 57-83 (2005)"
    locator: the whole paper (the market model of Fisher's 1891 thesis and the hydraulic machine that computed its prices)
  - paper: doi:10.1214/aoms/1177706369
    title: "Edmund Eisenberg and David Gale, Consensus of subjective probabilities, the pari-mutuel method, Annals of Mathematical Statistics 30(1), 165-168 (1959)"
    locator: the whole paper (existence and uniqueness of equilibrium prices for linear utilities, by a convex program)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 5, Vijay V. Vazirani, Combinatorial algorithms for market equilibria (Fisher's model, the linear case and the Eisenberg-Gale program), and Chapter 6, Bruno Codenotti and Kasturi Varadarajan, Computation of market equilibria by convex programming
  - paper: doi:10.1145/1411509.1411512
    title: "Nikhil R. Devanur, Christos H. Papadimitriou, Amin Saberi and Vijay V. Vazirani, Market equilibrium via a primal-dual algorithm for a convex program, Journal of the ACM 55(5), Article 22 (2008)"
    locator: Section 2 (Fisher's linear case, the existence and uniqueness of prices, and the reduction to unit supplies and integer data)
  - paper: doi:10.1145/1970392.1970394
    title: "Vijay V. Vazirani and Mihalis Yannakakis, Market equilibrium under separable, piecewise-linear, concave utilities, Journal of the ACM 58(3), Article 10 (2011)"
    locator: the whole paper (rational equilibria, membership in PPAD and hardness for Fisher markets with these utilities)
---

A Fisher market has buyers who come with money and sellers who come with goods. Each buyer has a budget and a utility function over the goods, and wants to spend the budget on the bundle she likes best. The money has no other use for her. A price vector is an equilibrium when every buyer can get a best bundle at these prices and, all together, the buyers take exactly the supply of every good with a positive price. The model is due to Irving Fisher, who in his 1891 thesis built a hydraulic machine that found the equilibrium prices of such a market. It is the special case of the [Arrow-Debreu market](/arrow-debreu-market/) in which buyers own only money, and it is the market on which most of the algorithms for market equilibrium were first found: the [Eisenberg-Gale program](/eisenberg-gale-program/), the [DPSV algorithm](/dpsv-algorithm/), [Orlin's algorithm](/orlin-fisher-market-algorithm/) and [proportional response dynamics](/proportional-response-dynamics/).

## The machine

**Agents and goods.** There are $n$ buyers $1, \dots, n$ and $m$ divisible goods $1, \dots, m$. The sellers bring a fixed supply of each good, and by a change of units each supply is one unit. Buyer $i$ has a budget $e_i > 0$ of money. The sellers want only money and are not modeled further.

**Utilities.** Buyer $i$ has a utility function $u_i : \mathbb{R}^m_{\ge 0} \to \mathbb{R}_{\ge 0}$ over bundles $x_i = (x_{i1}, \dots, x_{im})$. The main case is *linear* utilities, $u_i(x_i) = \sum_j u_{ij} x_{ij}$ with $u_{ij} \ge 0$: the goods are perfect substitutes for the buyer, at fixed rates. Other classes in the literature are Cobb-Douglas ($\prod_j x_{ij}^{a_{ij}}$ with $\sum_j a_{ij} = 1$), CES ($(\sum_j a_{ij} x_{ij}^\rho)^{1/\rho}$ with $\rho < 1$, $\rho \ne 0$), Leontief ($\min_j x_{ij} / a_{ij}$), and additively separable piecewise-linear concave utilities (SPLC), where each good has its own concave piecewise-linear utility.

**Demand.** At prices $p \in \mathbb{R}^m_{> 0}$, the demand set of buyer $i$ is the set of bundles that maximize $u_i(x_i)$ subject to $\sum_j p_j x_{ij} \le e_i$ and $x_i \ge 0$. Money left over is worth nothing to her, so with monotone utilities she spends all of it.

**Equilibrium.** Prices $p \ge 0$ and bundles $x_1, \dots, x_n$ form a (market) equilibrium, or [competitive equilibrium](/competitive-equilibrium/), when

1. every $x_i$ is in the demand set of buyer $i$ at $p$, and
2. $\sum_i x_{ij} \le 1$ for every good, with equality when $p_j > 0$.

**The linear case in money.** With linear utilities, a buyer gets the most utility per unit of money from the goods with the largest *bang per buck* $u_{ij} / p_j$. Write $\alpha_i = \max_j u_{ij} / p_j$ and let $b_{ij} = p_j x_{ij}$ be the money that buyer $i$ spends on good $j$. Then $(p, b)$ is an equilibrium if and only if

- $\sum_j b_{ij} = e_i$ for every buyer (budgets are spent),
- $\sum_i b_{ij} = p_j$ for every good (goods are sold),
- $b_{ij} > 0$ only if $u_{ij} / p_j = \alpha_i$ (money goes only to goods of maximum bang per buck).

The edges $(i, j)$ with $u_{ij} / p_j = \alpha_i$ form the *equality graph* at $p$. The conditions above say that a flow of money from the buyers to the goods, along equality edges, uses every budget and pays every price. This is the max-flow test that the DPSV algorithm uses.

**Standing assumption.** Every good has a buyer with $u_{ij} > 0$ and every buyer has a good with $u_{ij} > 0$. In the linear case this is the condition under which equilibrium prices exist, and then they are positive (Eisenberg and Gale 1959; see the remark in Section 2 of Devanur, Papadimitriou, Saberi and Vazirani 2008).

## What it counts

The input is the list of budgets and utility parameters, as rational numbers with total bit length $L$. Algorithms are measured in $n$, $m$ and $L$, and the pages of this area say for each one whether it is exact, strongly polynomial (the number of arithmetic operations depends on $n$ and $m$ only) or approximate.

- **Exact algorithms** output rational prices and a rational allocation that satisfy the conditions above exactly. This is possible for linear utilities because the equilibrium is the optimum of a convex program whose optimal face is fixed by linear equations on a forest of equality edges, so the prices are rational with polynomial bit length.
- **Approximate equilibria** relax the conditions by a factor $1 \pm \varepsilon$: for example, each buyer spends at least $(1 - \varepsilon) e_i$, only on goods with bang per buck at least $\alpha_i / (1 + \varepsilon)$, and the demand of each good is within $1 \pm \varepsilon$ of its supply. Papers differ in the exact form, so each page says which one it uses.
- **Combinatorial algorithms** such as DPSV are often counted in max-flow computations, and each max flow is then charged at the cost of the flow algorithm used.
- **Dynamics** such as [tatonnement](/tatonnement/) and proportional response are counted in rounds $T$, with the cost of one round given apart. A round costs $O(nm)$ arithmetic operations for linear utilities.

## Relation to other models

- **Arrow-Debreu market.** In an exchange market every agent owns goods and buys with the money from selling them. A Fisher market is the case where the buyers own only money and the owners of the goods want only money. An exchange market can also be read as a Fisher market whose budgets $e_i = p \cdot w_i$ depend on the prices, which is why the Arrow-Debreu market is harder: the budgets move with the prices.
- **Quasilinear markets.** In the [assignment game](/assignment-game/) and in auctions, a buyer keeps the money she does not spend and values it, so her utility is $v_i(S) - p(S)$, a [quasilinear utility](/quasilinear-utility/). In a Fisher market unspent money is worth nothing. The two models have different equilibria and different algorithms; the [Demange-Gale-Sotomayor auction](/demange-gale-sotomayor-auction/) and the [Kelso-Crawford process](/kelso-crawford-process/) are for the quasilinear case.
- **Equal budgets.** A Fisher market with $e_i = 1$ for all buyers is a [competitive equilibrium from equal incomes](/competitive-equilibrium-from-equal-incomes/). For linear utilities its allocation maximizes the product of the utilities, which is the [maximum Nash welfare](/maximum-nash-welfare/) allocation of divisible goods. With unequal budgets the equilibrium maximizes the budget-weighted product $\prod_i u_i^{e_i}$.
- **Trading post game.** If each buyer submits bids $b_{ij}$ (money on each good) and each good is split in proportion to the bids, the market becomes the trading post game of Shapley and Shubik. Proportional response dynamics is a simple update rule for these bids.

## Known results in the model

All results below are for one unit of each good and the standing assumption.

- **Existence and uniqueness (linear).** Equilibrium prices exist and are unique, and the equilibrium allocations form a convex set (Eisenberg and Gale 1959). The allocations are the optimal solutions of the Eisenberg-Gale program, and the prices are its dual variables. Eisenberg (1961) extended the program to concave utilities that are homogeneous of degree one, which include CES, Cobb-Douglas and Leontief.
- **Rational solutions (linear).** Prices and allocations are rational with bit length polynomial in $L$, so exact algorithms make sense (Lemma 7.1 of Devanur, Papadimitriou, Saberi and Vazirani 2008).
- **Polynomial algorithms (linear).** The Eisenberg-Gale program can be solved by the [ellipsoid method](/ellipsoid-method/) or an [interior point method](/interior-point-method/) to any accuracy. Devanur, Papadimitriou, Saberi and Vazirani (2002, 2008) gave the first combinatorial polynomial algorithm, with $O(m^4 (\log m + m \log U + \log M))$ max-flow computations, where $U$ is the largest integer utility and $M$ is the total integer money. Orlin (2010) gave the first strongly polynomial algorithm, with $O(n^4 \log n)$ operations when $n$ counts buyers and goods together.
- **Dynamics.** Proportional response dynamics converges to the equilibrium for linear utilities, and the gap of its potential falls like $O(1/T)$ (Birnbaum, Devanur and Xiao 2011). Discrete [tatonnement](/tatonnement/) with a suitable step size converges to an approximate equilibrium, with explicit bounds on the number of rounds, for Fisher markets with weak gross substitutes and bounded elasticity (Cole and Fleischer 2008), and for markets with some complementary goods, where it is a form of gradient descent (Cheung, Cole and Devanur 2020).
- **Hardness (SPLC).** With additively separable piecewise-linear concave utilities, rational equilibria exist under mild conditions and computing one is PPAD-complete (Chen and Teng 2009; Vazirani and Yannakakis 2011); the same holds in the Arrow-Debreu model (see [PPAD-hardness of market equilibria](/ppad-hardness-of-arrow-debreu/)).

**Check value.** Two buyers with budgets $1$ and $1$, utilities $u_1 = (2, 1)$ and $u_2 = (1, 2)$. The equilibrium prices are $(1, 1)$, and buyer $i$ buys all of good $i$: her bang per buck is $2$ on good $i$ and $1$ on the other good, and she spends her budget of $1$ on one unit at price $1$.

**A larger example.** Three buyers with budgets $(1, 1, 3)$ and utilities $u_1 = (1, 4, 3)$, $u_2 = (4, 2, 1)$, $u_3 = (1, 1, 2)$. The equilibrium prices are $(5/4, 5/4, 5/2)$. Buyer 1 has bang per buck $(4/5, 16/5, 6/5)$ and spends $1$ on good 2. Buyer 2 has $(16/5, 8/5, 2/5)$ and spends $1$ on good 1. Buyer 3 has $4/5$ on every good, so all goods are best for her, and she spends $1/4$, $1/4$ and $5/2$ on goods 1, 2 and 3. Each good then receives exactly its price: $1 + 1/4$, $1 + 1/4$ and $5/2$. The page [DPSV algorithm](/dpsv-algorithm/) traces how the algorithm finds these prices.

**Non-unique allocations.** Two buyers with the same utilities $(1, 1)$ and budgets $1$ and $3$ face prices $(2, 2)$. Any split in which buyer 1 spends $1$, buyer 2 spends $3$ and each good receives $2$ is an equilibrium, for example $b_1 = (1, 0)$, $b_2 = (1, 2)$ or $b_1 = (1/2, 1/2)$, $b_2 = (3/2, 3/2)$. The prices are unique; the allocations form a segment.

## References
