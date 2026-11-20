---
tag: 2BHZY9
kind: theorem
slug: bondareva-shapley-theorem
name: Bondareva-Shapley theorem
aliases:
- balancedness theorem
area: algorithmic-game-theory/cooperative-games
level: core
summary: A TU game has a nonempty core if and only if it is balanced. The proof is LP duality for the problem of the cheapest vector that covers every coalition.
prereqs: [core-of-a-cooperative-game, lp-duality, strong-duality]
see_also: [convex-game, shapley-convex-games-theorem, least-core, assignment-game, farkas-lemma, weak-duality, linear-programming-problem, minimax-theorem]
sources:
  - paper: "Olga N. Bondareva, Some applications of linear programming methods to the theory of cooperative games, Problemy Kibernetiki 10 (1963), 119-139 (in Russian)"
    locator: the condition for a nonempty core, proved by linear programming
  - paper: doi:10.1002/nav.3800140404
    title: "Lloyd S. Shapley, On balanced sets and cores, Naval Research Logistics Quarterly 14(4) (1967), 453-460"
    locator: balanced collections, the theorem, and the reduction to minimal balanced collections
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: Chapter 17, The core (Section 17.2 balanced collections of coalitions, Section 17.3 the Bondareva-Shapley theorem)
  - book: "Bezalel Peleg and Peter Sudholter, Introduction to the Theory of Cooperative Games, 2nd edition, Theory and Decision Library C 34, Springer, 2007"
    title: Introduction to the Theory of Cooperative Games
    locator: Chapter 3, The core (pp. 27-49), balanced games and totally balanced games
---

The Bondareva-Shapley theorem says exactly when the [core](/core-of-a-cooperative-game/) of a [TU game](/transferable-utility-game/) is not empty: when no way of splitting the players' time among coalitions earns more than the grand coalition. Bondareva proved it in 1963 and Shapley in 1967, both with [linear programming duality](/lp-duality/). It is a test for every game; for the special class of [convex games](/convex-game/), [Shapley's theorem](/shapley-convex-games-theorem/) gives more, a nonempty core with known corners.

## Statement

Let $(N, v)$ be a TU game with $N = \{1, \ldots, n\}$. A family of weights $\lambda = (\lambda_S)$, one for each nonempty $S \subseteq N$, is balanced if

$$\lambda_S \ge 0 \text{ for every } S \quad \text{and} \quad \sum_{S \ni i} \lambda_S = 1 \text{ for every player } i.$$

The collection of coalitions with $\lambda_S > 0$ is then a balanced collection. The game is balanced if $\sum_S \lambda_S v(S) \le v(N)$ for every balanced $\lambda$.

**Theorem (Bondareva 1963, Shapley 1967).** The core of $(N, v)$ is not empty if and only if the game is balanced.

It is enough to check the minimal balanced collections, those that contain no smaller balanced collection. Each has exactly one balancing family of weights, and these families are the corners of the polytope of balanced $\lambda$ (Shapley 1967).

### Example

In the three-player majority game, $v(S) = 1$ when $|S| \ge 2$ and $v(S) = 0$ otherwise. The three pairs with weight $1/2$ each are balanced, since each player is in two of them. They give $\tfrac12 (1 + 1 + 1) = 3/2 > 1 = v(N)$, so the game is not balanced and its core is empty.

In the glove game, player 1 holds a left glove, players 2 and 3 hold right gloves, and $v(S) = 1$ exactly when $S$ contains player 1 and another player. The same pairs give $\tfrac12 (1 + 1 + 0) = 1 \le v(N)$, the partitions give at most 1, and the core is the point $(1, 0, 0)$.

## In plain words

Think of each player as having one unit of time. The player can spend it all with one coalition, or split it among several coalitions, as long as the parts add up to one unit. A coalition that gets a fraction of the time of all its members earns the same fraction of its value. The theorem says that a stable split of the grand coalition's value exists exactly when no such schedule earns more than the grand coalition earns. If some schedule earns more, then the players can always find a coalition that is paid too little, whatever split is proposed. If no schedule earns more, then a split exists that pays each coalition at least its value. The two sides of the test are a linear program and its dual.

## Proof

Consider the linear program that finds the cheapest payoff vector that gives every coalition at least its value:

$$\text{(P)} \quad \min\ x(N) \quad \text{subject to} \quad x(S) \ge v(S) \text{ for every nonempty } S \subseteq N.$$

Its dual has one variable $\lambda_S \ge 0$ for each constraint and one equality for each variable $x_i$, which is free:

$$\text{(D)} \quad \max\ \sum_S \lambda_S v(S) \quad \text{subject to} \quad \sum_{S \ni i} \lambda_S = 1 \text{ for every } i, \quad \lambda \ge 0.$$

The feasible points of (D) are exactly the balanced families.

Both programs are feasible. For (P), let $M = \max_S |v(S)|$ and $x_i = M$ for all $i$; then $x(S) = |S| M \ge M \ge v(S)$. For (D), put $\lambda_{\{i\}} = 1$ for each $i$ and $\lambda_S = 0$ otherwise. By [strong duality](/strong-duality/), both programs have optimal solutions, with the same value $z^*$.

The constraint of (P) for $S = N$ gives $x(N) \ge v(N)$ at every feasible point, so $z^* \ge v(N)$.

- If the core is not empty, a core point $x$ is feasible for (P) with $x(N) = v(N)$, so $z^* \le v(N)$ and $z^* = v(N)$. Every balanced $\lambda$ is feasible for (D), so $\sum_S \lambda_S v(S) \le z^* = v(N)$. The game is balanced.
- If the game is balanced, every feasible point of (D) has value at most $v(N)$, so $z^* \le v(N)$, and $z^* = v(N)$. An optimal solution $x$ of (P) has $x(N) = v(N)$ and $x(S) \ge v(S)$ for all $S$, so it is in the core.

This proves the theorem. The first direction needs only [weak duality](/weak-duality/), and it has a one-line form: if $x$ is in the core and $\lambda$ is balanced, then

$$\sum_S \lambda_S v(S) \le \sum_S \lambda_S x(S) = \sum_i x_i \sum_{S \ni i} \lambda_S = x(N) = v(N).$$

For the reduction to minimal collections: the feasible set of (D) is a polytope, bounded because $\lambda_S \le \sum_{T \ni i} \lambda_T = 1$ for any $i \in S$. A linear function on a polytope reaches its maximum at a corner, so it is enough to check the corners. At a corner the indicator vectors of the coalitions with $\lambda_S > 0$ are linearly independent, so the weights are the only solution of the equalities on that support, and Shapley (1967) shows that these supports are exactly the minimal balanced collections. $\square$

For the majority game, (P) has the optimum $x = (1/2, 1/2, 1/2)$ with value $3/2$, and (D) has the optimum with weight $1/2$ on each pair, also with value $3/2$. The gap $3/2 - 1$ is what the grand coalition is short of.

## Consequences

- **An algorithm.** The core is not empty exactly when the optimum of (P) is $v(N)$. Given a table of $v$, this is one LP with $n$ variables and $2^n - 1$ constraints, so the test runs in time polynomial in $2^n$ and the bit length of the values. An optimal $x$ of (P) is then a core point, and an optimal $\lambda$ of (D) is a certificate that the core is empty when the value is above $v(N)$.
- **Three players.** The minimal balanced collections on three players are the partitions and the three pairs with weight $1/2$ each. So a three-player game has a nonempty core exactly when the partition conditions hold (for example, when it is superadditive) and $v(\{1, 2\}) + v(\{1, 3\}) + v(\{2, 3\}) \le 2 v(N)$.
- **Simple games.** A simple game has a nonempty core exactly when it has a veto player, a player in every winning coalition.
- **Cost games.** For a cost game $c$, apply the theorem to $-c$: the core $\{x : x(N) = c(N),\ x(S) \le c(S)\}$ is not empty exactly when $\sum_S \lambda_S c(S) \ge c(N)$ for every balanced $\lambda$.
- **Totally balanced games.** A game whose every subgame is balanced is totally balanced. The [assignment game](/assignment-game/) and the [minimum cost spanning tree game](/minimum-cost-spanning-tree-game/) are examples; for both, a duality argument for the underlying optimization problem gives a core point directly.
- **Convex games.** Every [convex game](/convex-game/) is balanced, because a marginal vector is a core point. This gives a direct proof that needs no LP.
- **The least core.** The [least core](/least-core/) relaxes every constraint of (P) except $S = N$ by the same $\varepsilon$, and the smallest such $\varepsilon$ is again the value of an LP. The core is not empty exactly when this value is at most 0.

## Tightness

- **Partitions are not enough.** The majority game satisfies $\sum_{S \in P} v(S) \le v(N)$ for every partition $P$ of $N$; it is superadditive. Its core is still empty. Balanced families with fractional weights are needed.
- **The equalities matter.** If the condition allowed $\sum_{S \ni i} \lambda_S \le 1$, the theorem would fail. Take two players with $v(\{1\}) = v(\{2\}) = v(\{1, 2\}) = -1$. The core is the segment of vectors with $x_1 + x_2 = -1$ and $x_1, x_2 \ge -1$, which is not empty. But $\lambda = 0$ satisfies the weak form and gives $0 > -1 = v(N)$.
- **Transferable utility matters.** For games without transferable utility, Scarf (1967) showed that balancedness is enough for a nonempty core, but it is not necessary.

## History

Olga Bondareva proved the theorem in 1963, in Russian, by linear programming. Lloyd Shapley proved it on his own in 1967, introduced the language of balanced collections, and reduced the test to the minimal balanced collections. Herbert Scarf extended the sufficient direction to games without transferable utility in the same year. The theorem became the standard tool to show that the core of a class of games is not empty, through a duality argument for the underlying optimization problem.

## References
