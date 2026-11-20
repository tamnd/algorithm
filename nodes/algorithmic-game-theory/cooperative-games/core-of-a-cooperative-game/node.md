---
tag: NMRGBG
kind: definition
slug: core-of-a-cooperative-game
name: Core of a cooperative game
aliases:
- core allocation
area: algorithmic-game-theory/cooperative-games
level: intro
summary: The set of payoff vectors that distribute v(N) so that every coalition S gets at least v(S). It may be empty.
prereqs: [transferable-utility-game]
see_also: [bondareva-shapley-theorem, least-core, nucleolus, convex-game, shapley-convex-games-theorem, assignment-game, weighted-voting-game, linear-programming-problem]
sources:
  - book: "A. W. Tucker and R. D. Luce (eds.), Contributions to the Theory of Games IV, Annals of Mathematics Studies 40, Princeton University Press, 1959"
    title: "Donald B. Gillies, Solutions to general non-zero-sum games"
    locator: pp. 47-85 (the core as the set of undominated imputations)
  - paper: doi:10.1002/nav.3800140404
    title: "Lloyd S. Shapley, On balanced sets and cores, Naval Research Logistics Quarterly 14(4) (1967), 453-460"
    locator: the condition for a nonempty core by balanced collections
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: Chapter 17, The core (Section 17.1 definition, Section 17.2 balanced collections, Section 17.3 the Bondareva-Shapley theorem, Section 17.7 convex games)
  - book: "Bezalel Peleg and Peter Sudholter, Introduction to the Theory of Cooperative Games, 2nd edition, Theory and Decision Library C 34, Springer, 2007"
    title: Introduction to the Theory of Cooperative Games
    locator: Chapter 3, The core (pp. 27-49), with balanced games, market games and totally balanced games
  - book: "Georgios Chalkiadakis, Edith Elkind and Michael Wooldridge, Computational Aspects of Cooperative Game Theory, Synthesis Lectures on Artificial Intelligence and Machine Learning, Morgan and Claypool, 2011"
    title: Computational Aspects of Cooperative Game Theory
    locator: Chapter 2 (the core and the epsilon-core) and Chapter 3 (the cost of core questions for compact representations)
  - paper: doi:10.1287/moor.19.2.257
    title: "Xiaotie Deng and Christos H. Papadimitriou, On the complexity of cooperative solution concepts, Mathematics of Operations Research 19(2) (1994), 257-266"
    locator: the complexity of the core for graph games
---

The core of a [TU game](/transferable-utility-game/) is the set of ways to split the value of the grand coalition so that no group of players can do better on its own. A split outside the core is unstable: some coalition $S$ gets less than $v(S)$, and its members could leave and share $v(S)$ among themselves. The core can be empty, as in the three-player majority game. The [least core](/least-core/) relaxes every core inequality by the same amount and is never empty, and the [nucleolus](/nucleolus/) is one point of the least core, in the core whenever the core is not empty. The [Bondareva-Shapley theorem](/bondareva-shapley-theorem/) says exactly when the core is not empty.

## Definition

Let $(N, v)$ be a TU game with $N = \{1, \ldots, n\}$ and $v(\emptyset) = 0$, and write $x(S) = \sum_{i \in S} x_i$. The core is

$$\mathrm{Core}(v) = \{x \in \mathbb{R}^n : x(N) = v(N) \text{ and } x(S) \ge v(S) \text{ for every } S \subseteq N\}.$$

In the words of excess, $e(S, x) = v(S) - x(S)$, a core point is an efficient vector with no positive excess. Gillies (1959) defined the core by domination: an imputation $y$ dominates $x$ through $S$ if $y_i > x_i$ for all $i \in S$ and $y(S) \le v(S)$, so that $S$ can make every member better off with what it can earn alone. The core is the set of imputations that no imputation dominates when $v$ is superadditive; with the definition above it is a set of linear constraints, which is the form used for computation.

Basic facts:

- The core is a subset of the imputations, because the constraints for $S = \{i\}$ are $x_i \ge v(\{i\})$.
- It is a convex polytope: an intersection of $2^n - 1$ half spaces and one hyperplane, and bounded because $x_i \ge v(\{i\})$ and $x(N) = v(N)$.
- It is covariant: the core of $\alpha v + a$, with $\alpha > 0$ and $a$ additive, is $\alpha \mathrm{Core}(v) + a$.
- It can be empty. By the Bondareva-Shapley theorem it is not empty exactly when the game is balanced: $\sum_S \lambda_S v(S) \le v(N)$ for every family of weights $\lambda_S \ge 0$ with $\sum_{S \ni i} \lambda_S = 1$ for each player $i$.

To test whether $x$ is in the core given a table of $v$, check the $2^n - 1$ inequalities, in $O(n 2^n)$ time, or $O(2^n)$ if the sums $x(S)$ are updated along a Gray code. To test whether the core is empty, solve one linear program: minimize $x(N)$ subject to $x(S) \ge v(S)$ for all $S \ne \emptyset$; the core is not empty exactly when the minimum is at most $v(N)$. For games with a short description the same questions can be hard. For graph games, where $v(S)$ is the total weight of the edges inside $S$ and the weights may be negative, Deng and Papadimitriou (1994) show that testing whether a vector is in the core is coNP-complete.

## Examples and non-examples

- **The glove game.** Player 1 owns a left glove and players 2 and 3 each own a right glove; a pair is worth 1. The core constraints are $x_1 + x_2 \ge 1$, $x_1 + x_3 \ge 1$, $x_i \ge 0$ and $x_1 + x_2 + x_3 = 1$. The first gives $x_3 \le 0$ and the second $x_2 \le 0$, so the core is the single point $(1, 0, 0)$: the scarce left glove takes all the value. The Shapley value $(2/3, 1/6, 1/6)$ is not in the core.
- **The majority game.** With $v(S) = 1$ when $|S| \ge 2$, the pair constraints sum to $2 x(N) \ge 3$, but $x(N) = 1$. The core is empty.
- **A game with a large core.** Let $v(\{i\}) = 0$, $v(S) = 1/2$ for each pair and $v(N) = 1$. A pair constraint $x_i + x_j \ge 1/2$ says that the third player gets at most $1/2$. So the core is the triangle of vectors with $0 \le x_k \le 1/2$ and $x_1 + x_2 + x_3 = 1$, with corners $(1/2, 1/2, 0)$, $(1/2, 0, 1/2)$ and $(0, 1/2, 1/2)$.
- **Three-player superadditive games.** For such a game the core is not empty exactly when $v(\{1, 2\}) + v(\{1, 3\}) + v(\{2, 3\}) \le 2 v(N)$. The minimal balanced families on three players are the partitions and the three pairs with weight $1/2$ each, and superadditivity already gives the condition for every partition.
- **Simple games.** A simple game has a nonempty core exactly when it has a veto player, one that belongs to every winning coalition; the core is then the set of ways to split 1 among the veto players. If there is no veto player, each $i$ is outside some winning $S_i$, and $x(S_i) \ge 1 = x(N)$ with $x \ge 0$ forces $x_i = 0$ for every $i$, which is impossible. In the glove game player 1 is the only veto player.
- **Convex games.** The core is never empty; it contains the Shapley value, and its corners are the marginal vectors ([Shapley's theorem](/shapley-convex-games-theorem/)). [Bankruptcy games](/bankruptcy-problem/) are convex, and their core is exactly the set of award vectors.
- **Assignment games.** The core of the [assignment game](/assignment-game/) is the set of optimal solutions of the dual of the assignment LP, so it is never empty.
- **Not the core: the imputations.** In the majority game, $(1/3, 1/3, 1/3)$ is an imputation, but every pair gets $2/3 < 1$. Individual rationality alone does not make a split stable.

## Related definitions

- **Imputation set.** The efficient and individually rational vectors. The core is the part of it that also satisfies the constraints of coalitions with two or more players.
- **Epsilon-core and least core.** The epsilon-core asks $x(S) \ge v(S) - \varepsilon$ for every $S$ with $\emptyset \ne S \ne N$. The [least core](/least-core/) is the epsilon-core for the smallest $\varepsilon$ that makes it nonempty.
- **Nucleolus.** The [nucleolus](/nucleolus/) refines the least core to one point; it lies in the core when the core is not empty.
- **Balanced and totally balanced games.** A game is balanced when its core is not empty, and totally balanced when every subgame has a nonempty core. Market games are exactly the totally balanced games (Peleg and Sudholter, Chapter 3).
- **Weber set.** The convex hull of the marginal vectors. It always contains the core, and equals it exactly for convex games.
- **Core of a cost game.** For a cost game $c$, the core is the set of cost shares with $x(N) = c(N)$ and $x(S) \le c(S)$: no group pays more than it would pay alone.

## References
