---
tag: NSGMT8
kind: definition
slug: transferable-utility-game
name: Transferable utility game
aliases:
- TU game
- characteristic function game
- coalitional game
area: algorithmic-game-theory/cooperative-games
level: intro
summary: A cooperative game given by a set of players and a value v(S) for each coalition S, which the coalition can split freely among its members.
see_also: [core-of-a-cooperative-game, least-core, nucleolus, shapley-value, convex-game, weighted-voting-game, marginal-contribution-nets, bankruptcy-problem]
sources:
  - book: isbn:9780691130613
    title: John von Neumann and Oskar Morgenstern, Theory of Games and Economic Behavior, 60th anniversary edition, Princeton University Press, 2007 (first edition 1944)
    locator: Chapter VI, the characteristic function of an n-person game, and the general theory of n-person games that follows it
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: Chapter 16, Coalitional games with transferable utility (Section 16.1 examples, Section 16.2 strategic equivalence, Section 16.4 special families of games, Section 16.5 solution concepts, Section 16.6 the set of imputations)
  - book: "Georgios Chalkiadakis, Edith Elkind and Michael Wooldridge, Computational Aspects of Cooperative Game Theory, Synthesis Lectures on Artificial Intelligence and Machine Learning, Morgan and Claypool, 2011"
    title: Computational Aspects of Cooperative Game Theory
    locator: Chapter 2, Basic concepts (TU games, imputations and solution concepts), and Chapter 3, Representations and algorithms (compact representations of TU games)
  - paper: doi:10.1287/moor.19.2.257
    title: "Xiaotie Deng and Christos H. Papadimitriou, On the complexity of cooperative solution concepts, Mathematics of Operations Research 19(2) (1994), 257-266"
    locator: graph games, a compact class of TU games given by an edge weighted graph, and the cost of solution concepts on them
---

A transferable utility game, or TU game, describes what each group of players can earn by working together. It gives one number $v(S)$ for every coalition $S$, the total value that the members of $S$ can make without the other players, and it assumes that this value is money-like: the members can split it among themselves in any way they agree on. The game says nothing about how a coalition makes its value; the solution concepts built on it, such as the [core](/core-of-a-cooperative-game/), the [least core](/least-core/), the [nucleolus](/nucleolus/) and the [Shapley value](/shapley-value/), say how the value $v(N)$ of all players should be split. This page fixes the notation that those pages use.

## Definition

A TU game is a pair $(N, v)$ where $N = \{1, \ldots, n\}$ is a finite set of players and $v$ is a function from the subsets of $N$ to the real numbers with $v(\emptyset) = 0$. A subset $S \subseteq N$ is a coalition, $N$ is the grand coalition, and $v$ is the characteristic function. The value $v(S)$ is what the members of $S$ can guarantee for themselves together.

A payoff vector is a vector $x \in \mathbb{R}^n$, where $x_i$ is the payoff of player $i$. For a coalition $S$ write $x(S) = \sum_{i \in S} x_i$, with $x(\emptyset) = 0$. The excess of $S$ at $x$ is $e(S, x) = v(S) - x(S)$, the amount by which $S$ gets less than it can make alone.

- $x$ is efficient, or a preimputation, if $x(N) = v(N)$.
- $x$ is individually rational if $x_i \ge v(\{i\})$ for every $i$.
- $x$ is an imputation if it is efficient and individually rational. The set of imputations is not empty exactly when $v(N) \ge \sum_i v(\{i\})$. When the inequality is strict it is a simplex of dimension $n - 1$.

Some common properties of $v$:

- Superadditive: $v(S \cup T) \ge v(S) + v(T)$ for disjoint $S$ and $T$. Joining forces never hurts, so the grand coalition is the natural coalition to form.
- Monotone: $S \subseteq T$ implies $v(S) \le v(T)$.
- Convex: $v(S \cup T) + v(S \cap T) \ge v(S) + v(T)$ for all $S$ and $T$; see [convex game](/convex-game/).
- Simple: every $v(S)$ is 0 or 1, $v(N) = 1$, and $v$ is monotone. A coalition with value 1 is winning. A [weighted voting game](/weighted-voting-game/) is a simple game.
- Additive: $v(S) = \sum_{i \in S} a_i$ for some vector $a$.

Two games $v$ and $w$ on $N$ are strategically equivalent if $w = \alpha v + a$ for some $\alpha > 0$ and some additive game $a$, that is, $w(S) = \alpha v(S) + a(S)$. Most solution concepts are covariant under this map: the solution of $w$ is $\alpha$ times the solution of $v$ plus $a$. Every game with $v(N) > \sum_i v(\{i\})$ is strategically equivalent to exactly one game with $v(\{i\}) = 0$ for all $i$ and $v(N) = 1$.

A cost game gives a cost $c(S)$ to each coalition, the cost of serving its members together. Its savings game $v(S) = \sum_{i \in S} c(\{i\}) - c(S)$ is a TU game in the sense above, and the solution concepts carry over.

As an input to an algorithm, a general TU game is a table of $2^n$ numbers, often given by an oracle that returns $v(S)$ for a given $S$. Many classes have a short description: weighted voting games (a weight for each player and a quota), graph games (Deng and Papadimitriou 1994, where $v(S)$ is the total weight of the edges inside $S$), [marginal contribution nets](/marginal-contribution-nets/), and games defined by a combinatorial optimization problem, such as the [assignment game](/assignment-game/) and the [minimum cost spanning tree game](/minimum-cost-spanning-tree-game/). The cost of a solution concept depends very much on this choice.

## Examples and non-examples

- **The glove game.** Player 1 has a left glove, players 2 and 3 each have a right glove, and a pair of gloves sells for 1. So $v(S) = \min(\text{left gloves in } S, \text{right gloves in } S)$: $v(\{1, 2\}) = v(\{1, 3\}) = v(N) = 1$, and every other coalition has value 0. The game is superadditive and simple. It is the weighted voting game with quota 51 and weights $(50, 49, 1)$: the winning coalitions are exactly those with player 1 and at least one other player. Its core is the single point $(1, 0, 0)$, and its Shapley value is $(2/3, 1/6, 1/6)$.
- **The three-player majority game.** $v(S) = 1$ if $|S| \ge 2$ and $v(S) = 0$ otherwise. It is simple and superadditive, but its core is empty: the three pairs would need $x_1 + x_2$, $x_1 + x_3$ and $x_2 + x_3$ all at least 1, which sum to $2(x_1 + x_2 + x_3) \ge 3 > 2 v(N)$. Its nucleolus and Shapley value are both $(1/3, 1/3, 1/3)$.
- **The bankruptcy game.** For claims $c_1, \ldots, c_n$ and an estate $E$, $v(S) = \max(0, E - c(N \setminus S))$; see the [bankruptcy problem](/bankruptcy-problem/). It is convex.
- **A cost game.** The [airport game](/airport-game/) gives each coalition the cost of the longest runway that one of its planes needs. Its savings game is convex.
- **Not a TU game: a strategic game.** A [normal form game](/normal-form-game/) gives payoffs to strategy profiles, not values to coalitions. Von Neumann and Morgenstern turned it into a TU game by letting $v(S)$ be the max-min value of the two-player zero-sum game between $S$ and $N \setminus S$, but the two objects are different.
- **Not a TU game: matching without money.** In the [stable matching](/stable-matching/) problem the players have preferences over partners and cannot pay each other. A coalition can reach a set of outcomes, not a sum of money, so the model is a game without transferable utility (an NTU game). With money, the same market becomes the assignment game, which is a TU game.
- **Not a TU game in this sense: externalities.** If the value of $S$ depends on how the players outside $S$ group themselves, one number per coalition is not enough. Such games need a partition function.

## Related definitions

- The [core](/core-of-a-cooperative-game/) is the set of efficient $x$ with $e(S, x) \le 0$ for every coalition $S$.
- The [least core](/least-core/) relaxes every core inequality by the same amount $\varepsilon$ and takes the smallest $\varepsilon$ for which the set is not empty.
- The [nucleolus](/nucleolus/) is the imputation whose vector of excesses, sorted from the largest, is lexicographically smallest.
- The [Shapley value](/shapley-value/) gives each player its average marginal contribution $v(S \cup \{i\}) - v(S)$ over all orders in which the players can join.
- [Convex games](/convex-game/) are the TU games with increasing marginal contributions; their core contains the Shapley value.

## References
