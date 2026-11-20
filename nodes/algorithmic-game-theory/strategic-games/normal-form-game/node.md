---
tag: QWH3X8
kind: definition
slug: normal-form-game
name: Normal-form game
aliases:
- strategic-form game
- game in normal form
area: algorithmic-game-theory/strategic-games
level: intro
summary: A game given by a set of players, a finite set of actions for each player and a payoff for each player on every profile of actions.
see_also: [bimatrix-game, mixed-strategy, best-response, nash-equilibrium, extensive-form-game, bayesian-game, zero-sum-game, graphical-game]
sources:
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 2, Section 2.1 (strategic games)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 3 (games in normal form, with the standard examples) and Chapter 5 (the induced normal form of a game tree)
  - book: "John von Neumann and Oskar Morgenstern, Theory of Games and Economic Behavior, Princeton University Press, 1944"
    title: Theory of Games and Economic Behavior
    locator: Chapter II (the general formal description of a game and its normalized form)
---

A normal-form game is a game in which each player chooses one strategy, all at the same time and without seeing the choices of the others, and a table gives the payoff of every player for every combination of choices. It is the basic object of noncooperative game theory: [Nash equilibrium](/nash-equilibrium/), [best responses](/best-response/), dominance and correlated equilibrium are all defined on it. A two-player normal-form game is a [bimatrix game](/bimatrix-game/), and a game tree turns into a normal-form game when each player picks a complete plan in advance ([extensive-form game](/extensive-form-game/)).

## Definition

A *normal-form game* (or *strategic-form game*) is a triple $G = (N, (S_i)_{i \in N}, (u_i)_{i \in N})$ where

- $N = \{1, \ldots, n\}$ is the finite set of *players*;
- $S_i$ is a nonempty set, the *pure strategies* (or *actions*) of player $i$;
- $u_i : S \to \mathbb{R}$ is the *payoff function* (utility) of player $i$, on the set of *profiles* $S = S_1 \times \cdots \times S_n$.

The game is *finite* if every $S_i$ is finite. Each player $i$ wants a high value of $u_i$, and cares about no other number. On this site the payoffs are utilities, which the players maximize. Some games come with costs $c_i$, which the players minimize; set $u_i = -c_i$ to use the definitions here.

For a profile $s = (s_1, \ldots, s_n)$, write $s_{-i}$ for the strategies of all players except $i$, and $(s_i', s_{-i})$ for the profile in which only player $i$ changes to $s_i'$. A *mixed strategy* $\sigma_i$ is a probability distribution on $S_i$; the game in which the players choose mixed strategies independently and get expected payoffs is the *mixed extension* of $G$ ([mixed strategy](/mixed-strategy/)).

**Size.** A finite game with $n$ players and $k$ strategies each has $k^n$ profiles and $n k^n$ payoff numbers. With $n = 10$ players and $k = 2$ strategies this is already 10240 numbers. So "polynomial time" for an $n$-player game in normal form means polynomial in this table, and games with many players are usually given in a succinct form instead.

**What the payoffs mean.** The definition uses the payoffs only to compare profiles for one player at a time. If $a > 0$ and $b$ are numbers, then $u_i' = a\,u_i + b$ gives the same comparisons, the same best responses and the same equilibria as $u_i$, for pure and for mixed strategies (for mixed strategies, $u_i$ must be a von Neumann-Morgenstern utility, so that expected payoffs mean something). Adding to $u_i$ any function of $s_{-i}$ alone also keeps the best responses and the equilibria, because it does not change the difference $u_i(s_i, s_{-i}) - u_i(s_i', s_{-i})$. Such changes can alter the sum of payoffs and turn a game into a [zero-sum game](/zero-sum-game/) or out of one, so welfare comparisons are not invariant.

## Examples and non-examples

Each table lists the payoff of the row player first.

**Prisoner's dilemma.** Two players, two strategies each: cooperate (C) or defect (D).

| | C | D |
| --- | --- | --- |
| C | 3, 3 | 0, 5 |
| D | 5, 0 | 1, 1 |

Here $N = \{1, 2\}$, $S_1 = S_2 = \{C, D\}$, and $u_1(D, C) = 5$, $u_2(D, C) = 0$. The table has $2 \cdot 2^2 = 8$ numbers. The [prisoner's dilemma](/prisoners-dilemma/) page studies this game.

**A three-player game.** Each of three players chooses 0 or 1, and a player gets 1 if their choice agrees with the majority and 0 otherwise. The game has $2^3 = 8$ profiles and $3 \cdot 2^3 = 24$ payoff numbers. A table for three players is drawn as two $2 \times 2$ tables, one for each choice of player 3. The profiles $(0, 0, 0)$ and $(1, 1, 1)$ are the only [pure Nash equilibria](/pure-nash-equilibrium/): at a profile with a 2 to 1 split, the player in the minority gains 1 by a switch.

**The normal form of a game tree.** In an entry game, player 1 chooses Out, which ends the game with payoffs $(0, 2)$, or In; after In, player 2 chooses Fight, with payoffs $(-1, -1)$, or Accommodate, with $(1, 1)$. A pure strategy of a player is a plan that names a move at each point where the player may have to move. Here each player has one such point and two moves, and the normal form is

| | Fight | Accommodate |
| --- | --- | --- |
| Out | 0, 2 | 0, 2 |
| In | -1, -1 | 1, 1 |

Its pure equilibria are (In, Accommodate) and (Out, Fight). The second one rests on a threat to fight that player 2 would not carry out once In has happened; the normal form forgets the order of the moves, and the [subgame perfect equilibrium](/subgame-perfect-equilibrium/) of the tree is (In, Accommodate) only. In general, a player with decision points $h_1, \ldots, h_r$ in a tree, with $a_1, \ldots, a_r$ moves at them, has $a_1 a_2 \cdots a_r$ pure strategies, so the normal form can be exponentially larger than the tree.

**Non-example: a game with timing that matters.** Chess is not given in normal form: its rules describe a [game tree](/game-tree/). It has a normal form in principle, with one strategy for each complete plan, but the table is far too large to write down, and the analysis of such games works on the tree.

**Non-example: a game with hidden types.** In a [Bayesian game](/bayesian-game/) the payoffs depend on private types drawn by chance. It is not a normal-form game as given. It becomes one when a strategy is a map from types to actions and the payoffs are expectations over the prior.

**Infinite strategy sets.** In a Cournot duopoly each firm chooses a quantity $q_i \ge 0$, and $u_i(q_1, q_2) = q_i\,(a - q_1 - q_2) - c\,q_i$. This is a normal-form game, but not a finite one, and [Nash's theorem](/nash-existence-theorem/) does not apply to it as stated: infinite games need compactness and continuity conditions.

## Related definitions

- **Bimatrix game.** The case $n = 2$ with finite sets, given by two $m \times n$ matrices $A$ and $B$ ([bimatrix game](/bimatrix-game/)).
- **Zero-sum and constant-sum games.** Two-player games with $u_1 + u_2 = 0$ (or constant), the setting of the [minimax theorem](/minimax-theorem/).
- **Symmetric games.** All players have the same strategy set, and permuting the players permutes the payoffs in the same way. Nash proved that a finite symmetric game has a symmetric equilibrium.
- **Succinct games.** Classes whose payoffs are given by a short formula instead of a table: [graphical games](/graphical-game/), [atomic congestion games](/atomic-congestion-game/) and other [potential games](/potential-game/).
- **Extensive-form and Bayesian games.** Games with moves in sequence ([extensive-form game](/extensive-form-game/)) or with private information ([Bayesian game](/bayesian-game/)); each has an induced normal form.
- **Solution concepts.** [Dominant strategies](/dominant-strategy/), [iterated dominance](/iterated-elimination-of-dominated-strategies/), [Nash equilibrium](/nash-equilibrium/), [correlated equilibrium](/correlated-equilibrium/) and [coarse correlated equilibrium](/coarse-correlated-equilibrium/) are all defined on a normal-form game.

## References
