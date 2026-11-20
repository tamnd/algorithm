---
tag: YNBXA4
kind: model
slug: arrow-debreu-market
name: Arrow-Debreu market
aliases:
- exchange market
- exchange economy
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: A market in which each agent owns an endowment of goods and sells it at equilibrium prices to buy its optimal bundle.
prereqs: [competitive-equilibrium]
see_also: [fisher-market, arrow-debreu-existence-theorem, ppad-hardness-of-arrow-debreu, first-welfare-theorem, tatonnement, gross-substitutes, shapley-scarf-housing-market, ppad]
sources:
  - paper: doi:10.2307/1907353
    title: "Kenneth J. Arrow and Gerard Debreu, Existence of an equilibrium for a competitive economy, Econometrica 22(3), 265-290 (1954)"
    locator: the whole paper (the model with consumers, producers, endowments and profit shares, and the existence theorem)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 5, Vijay V. Vazirani, Combinatorial algorithms for market equilibria (the exchange model and its reduction from Fisher's model), and Chapter 6, Bruno Codenotti and Kasturi Varadarajan, Computation of market equilibria by convex programming
  - paper: doi:10.1137/S0097539705447384
    title: "Kamal Jain, A polynomial time algorithm for computing an Arrow-Debreu market equilibrium for linear utilities, SIAM Journal on Computing 37(1), 303-318 (2007)"
    locator: the whole paper (a convex feasibility program for linear exchange markets, solved by the ellipsoid method)
  - paper: doi:10.1007/s10107-006-0065-5
    title: "Yinyu Ye, A path to the Arrow-Debreu competitive market equilibrium, Mathematical Programming 111(1), 315-348 (2008)"
    locator: the whole paper (interior point algorithms for linear Fisher and exchange markets)
  - paper: doi:10.1016/j.ic.2014.12.009
    title: "Ran Duan and Kurt Mehlhorn, A combinatorial polynomial algorithm for the linear Arrow-Debreu market, Information and Computation 243, 112-132 (2015)"
    locator: the whole paper (the first combinatorial polynomial algorithm for linear exchange markets)
  - paper: doi:10.1145/3313276.3316340
    title: "Jugal Garg and Laszlo A. Vegh, A strongly polynomial algorithm for linear exchange markets, Proceedings of the 51st ACM Symposium on Theory of Computing (STOC 2019), 54-65"
    locator: the whole paper (a strongly polynomial algorithm, built on a variant of the Duan-Mehlhorn algorithm)
  - paper: "Bruno Codenotti, Sriram Pemmaraju and Kasturi Varadarajan, On the polynomial time computation of equilibria for certain exchange economies, Proceedings of the 16th ACM-SIAM Symposium on Discrete Algorithms (SODA 2005), 72-81"
    locator: the whole paper (polynomial algorithms for exchange markets with weak gross substitutes)
---

An Arrow-Debreu market, or exchange market, is a market in which every agent is both a seller and a buyer. Each agent owns some goods, her endowment. At given prices she sells her endowment, and with the money she buys the bundle she likes best. Prices are in equilibrium when the agents together buy exactly what they together own, good by good. The model was set out by Arrow and Debreu (1954), who also allowed firms that turn goods into other goods, and it is the standard model of general equilibrium in economics. The [Fisher market](/fisher-market/) is the special case in which buyers own only money. The exchange model is harder than the Fisher model because each budget, the value of an endowment, moves with the prices.

## The machine

**Agents and goods.** There are $n$ agents and $m$ divisible goods. Agent $i$ owns an endowment $w_i \in \mathbb{R}^m_{\ge 0}$ and has a utility function $u_i : \mathbb{R}^m_{\ge 0} \to \mathbb{R}$, which she maximizes. There is no money apart from the prices that are used to value goods.

**Budgets and demand.** A price vector is $p \in \mathbb{R}^m_{\ge 0}$, $p \ne 0$. At $p$ agent $i$ earns $p \cdot w_i$ from her endowment, and her demand set $D_i(p)$ is the set of bundles $x_i \ge 0$ that maximize $u_i$ subject to $p \cdot x_i \le p \cdot w_i$. Demand does not change when $p$ is multiplied by a positive number, so prices are normalized, for example to $\sum_j p_j = 1$.

**Equilibrium.** $(p, x)$ is an equilibrium, a [competitive equilibrium](/competitive-equilibrium/), when $x_i \in D_i(p)$ for every agent and $\sum_i x_{ij} \le \sum_i w_{ij}$ for every good, with equality when $p_j > 0$.

**Linear utilities.** In the linear exchange model, $u_i(x_i) = \sum_j u_{ij} x_{ij}$ with $u_{ij} \ge 0$. As in the Fisher market, agent $i$ spends her income $p \cdot w_i$ only on goods of maximum bang per buck $u_{ij} / p_j$. Other classes studied in the literature are CES, Cobb-Douglas, Leontief and additively separable piecewise-linear concave (SPLC) utilities.

**Production.** In the full model of Arrow and Debreu there are also firms. Firm $f$ chooses a production plan $y_f$ in a production set $Y_f \subseteq \mathbb{R}^m$ (inputs negative, outputs positive) to maximize profit $p \cdot y_f$, and agent $i$ owns the share $\theta_{if}$ of each firm, so her income is $p \cdot w_i + \sum_f \theta_{if} \, p \cdot y_f$. The pages of this area use the exchange model, without firms.

**Assumptions.** Results in the model assume some of the following, and each statement on this site says which: utilities are continuous, quasi-concave (convex preferences) and locally nonsatiated; endowments are positive in every good, or a weaker irreducibility condition holds that makes every agent's income positive at every candidate equilibrium; and for linear utilities, every good is liked by some agent.

## What it counts

The input is the list of endowments and utility parameters, as rational numbers of total bit length $L$. Algorithms are measured in $n$, $m$ and $L$, and the pages say whether they are exact, strongly polynomial or approximate. An $\varepsilon$-approximate equilibrium relaxes optimality and clearing by a factor $1 \pm \varepsilon$; definitions differ between papers, so the pages state the one they use. For hardness results, the input is the market and the output is one equilibrium (any one, when there are several), so the problem is a total search problem in [TFNP](/tfnp/) once existence is guaranteed, and the natural class for it is [PPAD](/ppad/).

The linear exchange model has rational equilibria whose bit length is polynomial in $L$, so exact algorithms make sense. Eaves (1976) found one by Lemke's method for linear complementarity, a finite algorithm that is not polynomial.

## Relation to other models

- **Fisher market.** A Fisher market with budgets $e_i$ is an exchange market with one extra good, money: buyer $i$ owns $e_i$ units of money and likes only the goods, and one more agent owns all the goods and likes only money. Conversely, an exchange market behaves at prices $p$ like a Fisher market with budgets $e_i = p \cdot w_i$, which is the starting point of many algorithms for the exchange model.
- **Housing markets.** The [Shapley-Scarf housing market](/shapley-scarf-housing-market/) is an exchange market with indivisible goods: each agent owns one house and wants one house. A competitive equilibrium exists there, and with strict preferences its allocation is the top trading cycles allocation.
- **Markets with money.** In the [assignment game](/assignment-game/) and in auctions, agents have [quasilinear utilities](/quasilinear-utility/), with money valued one for one. That model is not an exchange model of this kind, since money is not a good whose price is set by the market.
- **Games.** An exchange market is not a game, because agents take prices as given. Arrow and Debreu proved existence by turning the market into an abstract economy with a price player who maximizes the value of the excess demand, and then using a fixed point theorem for games.

## Known results in the model

- **Existence.** An equilibrium exists when utilities are continuous, quasi-concave and locally nonsatiated, and endowments are positive (Arrow and Debreu 1954); see the [Arrow-Debreu existence theorem](/arrow-debreu-existence-theorem/). For linear utilities an equilibrium can fail to exist when some agent can have zero income; the existence page gives an example.
- **Efficiency.** Every equilibrium allocation is Pareto optimal when utilities are locally nonsatiated, by the [first welfare theorem](/first-welfare-theorem/).
- **Linear utilities, polynomial time.** Jain (2007) wrote the equilibria of linear exchange markets as the solutions of a convex feasibility program and found one with the ellipsoid method. Ye (2008) gave interior point algorithms. Duan and Mehlhorn (2015) gave the first combinatorial polynomial algorithm, and Garg and Vegh (2019) the first strongly polynomial one.
- **Gross substitutes.** For markets whose demand satisfies weak gross substitutes, equilibria can be computed in polynomial time by convex programming and related methods (Codenotti, Pemmaraju and Varadarajan 2005), and continuous [tatonnement](/tatonnement/) converges to them (Arrow, Block and Hurwicz 1959).
- **Hardness.** For SPLC utilities, finding an equilibrium is PPAD-complete (Chen, Dai, Du and Teng 2009; Vazirani and Yannakakis 2011); see [PPAD-hardness of market equilibria](/ppad-hardness-of-arrow-debreu/). For CES utilities with strong complements, and for Leontief utilities, the problem is PPAD-hard as well.

**Example.** Agent 1 owns one unit of good 1 and has $u_1 = (1, 2)$; agent 2 owns one unit of good 2 and has $u_2 = (1, 1)$. Fix $p_1 = 1$. If $p_2 < 1$, agent 1 has bang per buck $2/p_2 > 1$ on good 2, so she spends her income $1$ on it and asks for $1/p_2 > 1$ units, more than exists. If $p_2 > 1$, agent 2 has bang per buck $1$ on good 1 and $1/p_2 < 1$ on good 2, so she spends her income $p_2$ on good 1 and asks for $p_2 > 1$ units. So $p = (1, 1)$ is the only equilibrium price vector up to scale. At these prices agent 1 spends $1$ on good 2 (bang per buck $2$), and agent 2, who is indifferent, spends $1$ on good 1: the agents swap their goods.

## References
