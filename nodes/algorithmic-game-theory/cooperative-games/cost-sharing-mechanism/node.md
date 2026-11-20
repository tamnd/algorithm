---
tag: SX4VJH
kind: definition
slug: cost-sharing-mechanism
name: Cost-sharing mechanism
aliases:
- cost-sharing method
area: algorithmic-game-theory/cooperative-games
level: core
summary: A mechanism that picks the set of served agents from their bids and splits the service cost among them as payments.
prereqs: [quasilinear-utility, dominant-strategy-incentive-compatibility, budget-balance]
see_also: [moulin-mechanism, cross-monotonicity, vcg-mechanism, green-laffont-theorem, individual-rationality, shapley-value, minimum-cost-spanning-tree-game, jain-vazirani-steiner-cost-sharing]
sources:
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 15 (Kamal Jain and Mohammad Mahdian, Cost Sharing), Section 15.3 on cost-sharing mechanisms with private values and their properties
  - paper: "Herve Moulin, Incremental cost sharing: characterization by coalition strategy-proofness, Social Choice and Welfare 16(2) (1999), 279-320"
    title: "Incremental cost sharing: characterization by coalition strategy-proofness"
    locator: the model of a cost-sharing mechanism with private values and the conditions of no positive transfers, voluntary participation and consumer sovereignty
  - paper: "Herve Moulin and Scott Shenker, Strategyproof sharing of submodular costs: budget balance versus efficiency, Economic Theory 18(3) (2001), 511-533"
    title: "Strategyproof sharing of submodular costs: budget balance versus efficiency"
    locator: the trade-off between budget balance and efficiency for strategyproof cost-sharing mechanisms
  - paper: "Jerry Green, Elon Kohlberg and Jean-Jacques Laffont, Partial equilibrium approach to the free rider problem, Journal of Public Economics 6(4) (1976), 375-394"
    title: Partial equilibrium approach to the free rider problem
    locator: the incompatibility of strategyproofness, efficiency and budget balance for a public good
  - paper: doi:10.1145/1538902.1538907
    title: Quantifying inefficiency in cost-sharing mechanisms
    locator: Tim Roughgarden and Mukund Sundararajan, Journal of the ACM 56(4), Article 23, 2009, the social cost measure of the efficiency of a cost-sharing mechanism
---

A cost-sharing mechanism decides which players receive a service and how much each pays, when the service has a cost and each player's value for it is private. It is the setting of mechanism design with a cost function in place of a fixed set of outcomes. The usual goals are that the players cannot gain by lying, that the payments cover the cost, and that the served set is close to the best one. These goals conflict, and much of the theory is about which pairs of them can hold together.

## Definition

There is a finite set $A$ of $n$ players and a cost function $C : 2^A \to \mathbb{R}_{\ge 0}$ with $C(\emptyset) = 0$. The cost $C(S)$ is the cost of serving exactly the set $S$. Player $i$ has a private value $v_i \ge 0$ for being served.

A **cost-sharing mechanism** is a function $M$ that maps each vector of bids $b \in \mathbb{R}_{\ge 0}^A$ to a set $S(b) \subseteq A$ of served players and a payment vector $p(b) \in \mathbb{R}^A$. Player $i$ has the [quasilinear](/quasilinear-utility/) utility $u_i = v_i [\, i \in S(b) \,] - p_i(b)$.

The mechanism has the following properties if they hold for all bids $b$, all true values $v$ and all players $i$.

- **No positive transfers (NPT):** $p_i(b) \ge 0$.
- **Voluntary participation (VP):** a player who bids its value has $u_i \ge 0$. Equivalently, an unserved player pays 0 and a served player pays at most its bid.
- **Consumer sovereignty (CS):** for each $i$ there is a bid that makes $i$ served, whatever the other bids are.
- **$\beta$-budget balance:** $C(S(b)) \le \sum_{i \in A} p_i(b) \le \beta\, C(S(b))$, for some $\beta \ge 1$. With $\beta = 1$ the mechanism is budget balanced. Some authors write the condition as $\frac{1}{\beta} C(S) \le \sum_i p_i \le C(S)$, with the shares divided by $\beta$.
- **Strategyproofness:** bidding $b_i = v_i$ is a dominant strategy for every player, as in [dominant-strategy incentive compatibility](/dominant-strategy-incentive-compatibility/).
- **Group strategyproofness (GSP):** for every coalition $K \subseteq A$ and every change of the bids of $K$, if no member of $K$ is worse off than under truthful bidding, then no member is better off.
- **Efficiency:** $S(v)$ maximizes the social welfare $\sum_{i \in S} v_i - C(S)$ over all $S \subseteq A$. A weaker goal is $\alpha$-approximate social cost: $C(S) + \sum_{i \notin S} v_i$ is at most $\alpha$ times its minimum over all $S$ (Roughgarden and Sundararajan 2009).

A **cost-sharing method** is a function $\xi$ that gives a share $\xi(i, S) \ge 0$ to each player $i$ of each nonempty set $S \subseteq A$. It describes only how a given set splits its cost, not who is served. It is $\beta$-budget balanced if $C(S) \le \sum_{i \in S} \xi(i, S) \le \beta\, C(S)$ for every $S$. A method is the input of the [Moulin mechanism](/moulin-mechanism/), which turns it into a mechanism. The two terms are often used loosely for each other, but the method is the share function and the mechanism is the full rule from bids to outcomes.

## Examples and non-examples

- **Moulin mechanism with equal split.** A public good costs 1 to provide to any nonempty set, so $C(S) = 1$ for $S \neq \emptyset$. The method $\xi(i, S) = 1/|S|$ is cross-monotonic. The Moulin mechanism removes players who bid less than the current share until all remaining can pay. It satisfies NPT, VP and CS, is budget balanced and is group strategyproof. With bids $(0.6, 0.5, 0.3)$ it serves players 1 and 2 at price $1/2$ each.
- **Marginal cost mechanism.** The [VCG mechanism](/vcg-mechanism/) with the [Clarke pivot rule](/clarke-pivot-rule/) serves a set that maximizes welfare and is strategyproof, but it is not budget balanced. With the same public good and two players with values $0.6$ and $0.6$, it serves both. Each pays $0.4$: without player 1 the best welfare of the others is 0, and with player 1 the welfare of the others is $0.6 - 1 = -0.4$. The payments sum to $0.8 < 1$, a deficit.
- **Shares of the full set without a loop.** The rule that serves player $i$ if $b_i \ge \xi(i, A)$ and charges $\xi(i, A)$ is not budget balanced. If some players drop out, the shares of the others no longer cover the cost of the smaller set.
- **Pay your bid.** A mechanism that serves the players when their bids cover the cost and charges each served player its bid is not strategyproof. A player gains by lowering its bid to the smallest amount that still keeps it served.
- **The impossibility.** No mechanism is strategyproof, efficient and budget balanced for all cost functions. This is a result of Green, Kohlberg and Laffont (1976) and of the [Green-Laffont theorem](/green-laffont-theorem/). Every mechanism on this page gives up one of the three.

## Related definitions

- **[Cross-monotonicity](/cross-monotonicity/).** A method is cross-monotonic if no share rises when the set grows. This is the condition under which the Moulin mechanism is group strategyproof.
- **[Budget balance](/budget-balance/).** The general mechanism design notion, in which the payments sum to zero or to the cost.
- **[Individual rationality](/individual-rationality/).** The general form of voluntary participation.
- **Core of the cost game.** A budget balanced method gives, for each $S$, a vector that splits $C(S)$. If it is cross-monotonic, each such vector is in the [core](/core-of-a-cooperative-game/) of the game restricted to $S$.
- **Social cost.** The cost of the served set plus the values of the players not served, the quantity that an approximately efficient mechanism keeps small.

## References
