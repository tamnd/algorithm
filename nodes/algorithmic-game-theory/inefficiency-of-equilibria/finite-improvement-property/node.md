---
tag: 2TATNG
kind: definition
slug: finite-improvement-property
name: Finite improvement property
aliases:
- FIP
- acyclic improvement graph
area: algorithmic-game-theory/inefficiency-of-equilibria
level: core
summary: A game has the finite improvement property if every sequence of strict unilateral improvements ends; a finite game has it exactly when it has a generalized ordinal potential.
prereqs: [potential-game]
see_also: [potential-game, best-response-dynamics, pure-nash-equilibrium, rosenthal-potential-theorem, atomic-congestion-game, pls-completeness-of-congestion-games, local-search-problem]
sources:
  - paper: doi:10.1006/game.1996.0044
    title: "Dov Monderer and Lloyd S. Shapley, Potential games, Games and Economic Behavior 14(1) (1996), 124-143"
    locator: Section 2 (the finite improvement property, and the equivalence with a generalized ordinal potential for finite games)
  - paper: "Igal Milchtaich, Congestion games with player-specific payoff functions, Games and Economic Behavior 13(1) (1996), 111-124"
    locator: the existence of pure equilibria in singleton congestion games with player-specific costs, a class that need not have the finite improvement property
  - paper: doi:10.1145/1007352.1007445
    title: "Alex Fabrikant, Christos Papadimitriou and Kunal Talwar, The complexity of pure Nash equilibria, Proceedings of the 36th Annual ACM Symposium on Theory of Computing (STOC 2004), 604-612"
    locator: congestion games in which some improvement paths are exponentially long
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 16 (best-response dynamics and its convergence in potential games)
---

A game has the finite improvement property (FIP) if every sequence of strict unilateral improvements is finite: players take turns, each move lowers the cost of the player who moves, and the sequence must stop. It is a property of the dynamics, weaker than having an exact [potential](/potential-game/). The two meet in one theorem: a finite game has the FIP if and only if it has a generalized ordinal potential. Exact potential games, and so all congestion games, have it; many games with pure equilibria do not.

## Definition

Take a game in normal form with players $1, \ldots, n$, strategy sets $S_1, \ldots, S_n$ and costs $c_i : S \to \mathbb{R}$ on $S = S_1 \times \cdots \times S_n$, which each player minimizes. An **improvement step** goes from a profile $s$ to $s' = (s_i', s_{-i})$ with $c_i(s') < c_i(s)$: one player changes strategy and pays strictly less. An **improvement path** is a sequence $s^0, s^1, s^2, \ldots$, finite or infinite, in which each pair $s^k, s^{k+1}$ is an improvement step. The **improvement graph** has the profiles as vertices and the improvement steps as arcs.

The game has the **finite improvement property** if every improvement path is finite. For a finite game this is the same as an acyclic improvement graph, which is the reason for the alias: a cycle gives an infinite path by going around it, and in a finite acyclic graph every path has at most $|S| - 1$ arcs.

Two weaker properties are in common use. A **best-response step** is an improvement step in which $s_i'$ minimizes $c_i(\cdot, s_{-i})$; the game has the **finite best-response property** if every path of best-response steps is finite. The game is **weakly acyclic** if from every profile some finite improvement path leads to a pure Nash equilibrium. FIP implies both, and each of the two implications is strict, as the examples show.

**Theorem (Monderer and Shapley 1996).** A finite game has the FIP if and only if it has a generalized ordinal potential, that is, a function $\Phi : S \to \mathbb{R}$ with $\Phi(s') < \Phi(s)$ for every improvement step from $s$ to $s'$.

Proof. If $\Phi$ exists, $\Phi$ strictly falls along every improvement path. A finite game has finitely many values of $\Phi$, so no path visits a profile twice, and every path has at most $|S| - 1$ steps. Conversely, suppose the game is finite and has the FIP. Then its improvement graph is finite and acyclic. Let $\Phi(s)$ be the number of arcs of a longest path in the improvement graph that starts at $s$; it is at most $|S| - 1$. If $s \to s'$ is an improvement step, a longest path from $s'$ with the arc $s \to s'$ in front is a path from $s$, so $\Phi(s) \ge \Phi(s') + 1 > \Phi(s')$. $\square$

**Corollary.** In a finite game with the FIP, every maximal improvement path ends, and it ends at a pure Nash equilibrium, because a profile with no improvement step is an equilibrium. So any order of moves, and any rule for picking an improving strategy, reaches an equilibrium.

The FIP says nothing about the number of steps. The bound $|S| - 1$ is exponential in the number of players. With integer costs and an exact potential, the number of steps is at most $\Phi(s^0) - \min \Phi$, which is pseudo-polynomial. In congestion games some improvement paths are exponentially long, and finding a pure equilibrium is [PLS-complete](/pls-completeness-of-congestion-games/).

## Examples and non-examples

**Potential games.** Every finite game with an exact, weighted or ordinal [potential](/potential-game/) has the FIP, since each of these is a generalized ordinal potential. By [Rosenthal's theorem](/rosenthal-potential-theorem/) this includes every [atomic congestion game](/atomic-congestion-game/). In the prisoner's dilemma with costs $(1, 1)$ at (C, C), $(3, 0)$ at (C, D), $(0, 3)$ at (D, C) and $(2, 2)$ at (D, D), the longest improvement path is (C, C), (D, C), (D, D), and the longest-path function of the proof is 2 at (C, C), 1 at (C, D) and (D, C), and 0 at (D, D).

**Matching pennies.** Player 1 pays 0 when the coins match and 1 otherwise; player 2 pays the opposite. The path (H, H), (H, T), (T, T), (T, H), (H, H) is an improvement cycle: player 2, player 1, player 2 and player 1 move in turn, and each lowers its cost from 1 to 0. The game has no pure equilibrium at all.

**Best responses stop, but other improvements cycle.** Two players have the strategies H, T and X. In the table, each entry is (cost of player 1, cost of player 2), with player 1 choosing the row.

| | H | T | X |
|---|---|---|---|
| H | (2, 4) | (4, 2) | (10, 10) |
| T | (4, 2) | (2, 4) | (10, 10) |
| X | (1, 2) | (1, 2) | (0, 0) |

Restricted to H and T this is matching pennies, so (H, H), (H, T), (T, T), (T, H), (H, H) is an improvement cycle, and the game does not have the FIP. But in that cycle player 1 moves from a cost of 4 to 2, and its best response is X at cost 1. On a best-response path, player 2 can move at most once inside the H, T block before it pays 2 and has no better strategy; then player 1 moves to X, player 2 moves to X, and the path stops at (X, X), the only pure equilibrium. So the game has the finite best-response property.

**Weakly acyclic, but best responses cycle.** Change the row X to $(3, 2)$, $(3, 2)$, $(0, 0)$. Now player 1's best response inside the block is the other block strategy, at cost 2, so the cycle above is a cycle of best responses. But from any profile in the block, player 1 can move from cost 4 to X at cost 3, then player 2 moves to X, and the path ends at (X, X). From (H, X) or (T, X), player 1 moves to X. So the game is weakly acyclic.

**Player-specific costs.** If each player has its own cost function on each resource and picks one resource, the game is not a congestion game in Rosenthal's sense. Milchtaich proved that these games always have a pure equilibrium, but they need not have the FIP, so they have no generalized ordinal potential.

**An infinite game.** One player picks $s \in (0, 1]$ and pays $s$. The path $1, 1/2, 1/4, \ldots$ is an infinite improvement path, although $\Phi(s) = s$ is an exact potential. The theorem above needs a finite game. Infinite games use an approximate version: if the potential is bounded below and each step must gain at least $\epsilon > 0$, every path is finite.

## Related definitions

- [Potential game](/potential-game/): exact, weighted, ordinal and generalized ordinal potentials. The last is the same as FIP for finite games.
- [Pure Nash equilibrium](/pure-nash-equilibrium/): the sinks of the improvement graph. A game with the FIP has one; a game with a pure equilibrium need not have the FIP, as the tables above show.
- [Best-response dynamics](/best-response-dynamics/): the dynamics whose termination is the finite best-response property.
- [Local search](/local-search-problem/): an improvement path is a local search for a local minimum of a potential, which is why the complexity of finding the end of a path is a question about the class [PLS](/pls/).

## References
