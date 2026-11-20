---
tag: HZA46J
kind: theorem
slug: pls-completeness-of-congestion-games
name: PLS-completeness of congestion games
aliases:
- Fabrikant-Papadimitriou-Talwar theorem
area: algorithmic-game-theory/inefficiency-of-equilibria
level: advanced
summary: Finding a pure Nash equilibrium of a congestion game is PLS-complete, also for symmetric games and for network games, and improvement paths can be exponentially long.
prereqs: [rosenthal-potential-theorem, pls]
see_also: [atomic-congestion-game, symmetric-network-congestion-min-cost-flow, maximum-cut, local-search-problem, best-response-dynamics, finite-improvement-property, tfnp, ppad]
sources:
  - paper: doi:10.1145/1007352.1007445
    title: "Alex Fabrikant, Christos Papadimitriou and Kunal Talwar, The complexity of pure Nash equilibria, Proceedings of the 36th Annual ACM Symposium on Theory of Computing (STOC 2004), 604-612"
    locator: PLS-completeness for general, symmetric and network congestion games by tight reductions from POS-NAE-3SAT, and the polynomial algorithm for symmetric network games
  - paper: "Alejandro A. Schaffer and Mihalis Yannakakis, Simple local search problems that are hard to solve, SIAM Journal on Computing 20(1) (1991), 56-87"
    locator: PLS-completeness of local Max-Cut and of POS-NAE-3SAT under the flip neighbourhood, and tight reductions
  - paper: "David S. Johnson, Christos H. Papadimitriou and Mihalis Yannakakis, How easy is local search?, Journal of Computer and System Sciences 37(1) (1988), 79-100"
    locator: the class PLS, PLS reductions, and the result that a PLS problem is not NP-hard unless NP = coNP
  - paper: "Heiner Ackermann, Heiko Roglin and Berthold Vocking, On the impact of combinatorial structure on congestion games, Journal of the ACM 55(6) (2008), Article 25; FOCS 2006, 613-622"
    locator: a shorter proof of PLS-completeness for network games, and polynomial convergence of best-response dynamics in matroid games
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 19 (pure Nash equilibria and PLS-completeness)
---

This theorem is about the time to find the pure equilibrium that [Rosenthal's theorem](/rosenthal-potential-theorem/) promises. Rosenthal's proof is a local search: move players until the potential stops falling. Fabrikant, Papadimitriou and Talwar showed in 2004 that, in the worst case, no shortcut is likely. Finding a pure Nash equilibrium of a congestion game is complete for [PLS](/pls/), the class of local search problems, even when all players have the same strategies and even when the strategies are paths in a network. The exception is the symmetric network case, which is a [min-cost flow](/symmetric-network-congestion-min-cost-flow/).

## Statement

The problem CONGESTION-PNE takes a [congestion game](/atomic-congestion-game/) with $n$ players, a finite set $E$ of resources, nonnegative integer costs $c_e(1), \ldots, c_e(n)$ written in binary, and strategy sets $S_i \subseteq 2^E$, and asks for a pure Nash equilibrium. The strategy sets are given either as explicit lists of resource sets, or, in network games, as the sets of directed $s_i$-$t_i$ paths of a graph with edge set $E$. A pure equilibrium always exists, so this is a total search problem in [TFNP](/tfnp/).

**Theorem (Fabrikant, Papadimitriou and Talwar 2004).** CONGESTION-PNE is PLS-complete. It stays PLS-complete for symmetric congestion games, where all $S_i$ are the same list, and for network congestion games with directed graphs and player-specific sources and sinks. The reductions are tight, so for each of these classes there are games and starting profiles from which every path of strict unilateral improvements to an equilibrium has exponential length.

**Theorem (same paper).** For symmetric network congestion games with nondecreasing costs, a pure Nash equilibrium can be computed in polynomial time.

PLS-complete does not mean NP-hard. If a problem in PLS were NP-hard, then NP would equal coNP (Johnson, Papadimitriou and Yannakakis 1988). The theorem says that computing a pure equilibrium is as hard as finding any local optimum that a polynomial local search defines, such as a local optimum of Max-Cut under single flips.

## In plain words

Every congestion game has a stable state, and the obvious way to find one is to let players improve one at a time. This theorem says that the obvious way can take an astronomically long time, and that no clever method is known that always does better. The problem is as hard as every other problem of the type "keep improving until stuck", such as dividing a weighted graph into two halves so that no single node wants to switch sides. Only when all players travel between the same two points of a network does a fast method exist.

## Proof

**Membership in PLS.** A solution is a profile $s$, and its value is Rosenthal's potential $\Phi(s) = \sum_e \sum_{j \le x_e(s)} c_e(j)$, computed in polynomial time. The neighbours of $s$ are its unilateral deviations. For explicit lists there are polynomially many. For network games there can be exponentially many, but a best response of player $i$ is a shortest $s_i$-$t_i$ path with edge lengths $c_e(x_e + 1)$ on the edges that $i$ does not use and $c_e(x_e)$ on the edges it uses, so an improving neighbour, if one exists, is found in polynomial time. By Rosenthal's identity a deviation lowers the deviator's cost if and only if it lowers $\Phi$, so the local minima of $\Phi$ are exactly the pure equilibria.

**Hardness for general games.** We reduce from local Max-Cut with the flip neighbourhood, which Schaffer and Yannakakis proved PLS-complete under tight reductions. An instance is a graph $(V, F)$ with edge weights $w_f \ge 0$, a solution is a partition of $V$ into sides 0 and 1, and a neighbour moves one vertex to the other side. Build a congestion game with one player per vertex and two resources $r_f^0$, $r_f^1$ per edge $f$. Player $v$ has two strategies: side $b$ means the resource set $\{r_f^b : f \ni v\}$. Each resource of edge $f$ costs $c(1) = 0$ and $c(2) = w_f$; only the two endpoints of $f$ can use it. Player $v$ on side $b$ pays $w_f$ for each edge $f = vu$ with $u$ also on side $b$, that is, for each uncut edge at $v$. Rosenthal's potential is $\Phi = \sum_f w_f [f \text{ is uncut}] = W - \mathrm{cut}$, where $W$ is the total weight. A player gains by switching sides exactly when the flip raises the cut, by the same amount. So the solutions, the neighbourhoods and the improvement graphs of the two problems are the same, the pure equilibria are the local max cuts, and the reduction is tight. Fabrikant, Papadimitriou and Talwar reduced from POS-NAE-3SAT, the same idea with clauses of up to three variables: a clause resource costs its weight when all its variables pick its side.

**Hardness for symmetric games.** Take any congestion game with players $1, \ldots, n$ and strategy lists $S_1, \ldots, S_n$. Add new resources $z_1, \ldots, z_n$ with $c_{z_i}(1) = 0$ and $c_{z_i}(j) = M$ for $j \ge 2$, where $M$ is larger than the sum of all costs of the old game. Let every player of the new symmetric game choose from the one list $\{s \cup \{z_i\} : i \le n, s \in S_i\}$. In a pure equilibrium, if two players used the same $z_i$, some $z_j$ would be unused, and one of them, who pays at least $M$, could switch to a strategy with $z_j$ and pay less than $M$. So each $z_i$ is used by exactly one player. Renaming players by their $z_i$ gives a profile of the old game in which each deviation available in the old game is available in the new one at the same cost change, so it is an equilibrium of the old game. The map is computed in polynomial time, which completes a PLS reduction.

**Network games** need gadgets that force paths to behave like the strategies above. Fabrikant, Papadimitriou and Talwar gave such a reduction, and Ackermann, Roglin and Vocking gave a shorter proof.

**Exponential improvement paths.** Schaffer and Yannakakis showed that for problems that are PLS-complete under tight reductions there are instances and starting solutions from which every improving path to a local optimum is exponentially long. Tight reductions keep this property, and the Max-Cut reduction above even keeps the improvement graph, so the same holds for congestion games and their improvement dynamics. $\blacksquare$

### Example

Take a triangle with vertices $a$, $b$, $c$ and weights $w_{ab} = 1$, $w_{bc} = 2$, $w_{ca} = 3$. With all three players on side 0, every edge is uncut, $\Phi = 6$, and player $a$ pays $w_{ab} + w_{ca} = 4$. If $a$ moves to side 1, it pays 0 and $\Phi$ falls by 4 to 2, the weight of the uncut edge $bc$. Then $b$ pays 2 and would pay 1 on side 1, so it moves, and $\Phi = 1$ with only $ab$ uncut. Now $a$ pays 1 against 3, $b$ pays 1 against 2, and $c$ pays 0, so the profile with $a, b$ on one side and $c$ on the other is an equilibrium and a local max cut. Up to swapping the sides it is the only one: the partition with $b$ alone leaves $ca$ uncut and $a$ pays 3 against 1, and the partition with $a$ alone leaves $bc$ uncut and $b$ pays 2 against 1.

## Consequences

- **Best-response dynamics is slow in the worst case.** No rule for choosing the next mover makes improvement dynamics polynomial on all congestion games, because some starting profiles have only exponentially long improving paths.
- **Where the line is.** Symmetric network games are polynomial by min-cost flow. Matroid congestion games, including singleton games, converge after polynomially many best responses, and Ackermann, Roglin and Vocking showed that the matroid property is the most general property of the strategy sets alone that guarantees this.
- **Approximate and mixed equilibria.** The theorem is about exact pure equilibria. Computing a mixed Nash equilibrium of a congestion game is CLS-complete (Babichenko and Rubinstein, STOC 2021), and [no-regret dynamics](/no-regret-dynamics/) reach coarse correlated equilibria quickly.
- **Price of anarchy bounds still apply.** The worst-case equilibria of the [price of anarchy](/price-of-anarchy/) are hard to find, but the bounds hold for whatever equilibrium the players reach.

## Tightness

- **Costs written in binary.** With unary costs, or costs bounded by a polynomial, $\Phi$ takes polynomially many values and improvement dynamics ends in polynomial time. Hardness needs large weights, as in weighted Max-Cut.
- **Symmetry plus networks.** Each of the two restrictions alone keeps the problem PLS-complete; together they make it polynomial. The symmetric network algorithm needs nondecreasing costs, which keep the potential a convex flow cost.
- **Explicit strategies.** In the general and symmetric cases the strategies are listed, so the hardness does not come from a succinct description; it comes from the interaction of the players.

## History

Johnson, Papadimitriou and Yannakakis defined PLS in 1988. Schaffer and Yannakakis proved local Max-Cut and POS-NAE-3SAT PLS-complete in 1991, with tight reductions. Fabrikant, Papadimitriou and Talwar placed congestion games in this picture in 2004, which made the question of how hard it is to find a pure equilibrium a standard part of algorithmic game theory. Ackermann, Roglin and Vocking found the matroid boundary in 2006.

## References
