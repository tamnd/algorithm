---
tag: 5BCFKA
kind: theorem
slug: zermelo-theorem
name: Zermelo's theorem
aliases:
- Zermelo's determinacy theorem
area: games-and-search/game-tree-search
level: intro
summary: In a finite two-player game with perfect information and no chance, either the first player can force a win, or the second can, or both can force at least a draw.
prereqs: [game-tree, perfect-information-game, zero-sum-game]
see_also: [minimax, winning-losing-states, solved-game, strategy-stealing-argument, minimax-theorem, hex-game, retrograde-analysis, expectiminimax]
sources:
  - paper: "\"Über eine Anwendung der Mengenlehre auf die Theorie des Schachspiels\""
    title: Ernst Zermelo, Über eine Anwendung der Mengenlehre auf die Theorie des Schachspiels, Proceedings of the Fifth International Congress of Mathematicians, Cambridge 1912, volume II, Cambridge University Press (1913)
    locator: pp. 501 to 504 (winning positions in chess, and the bound on the number of moves that a player in a winning position needs)
  - paper: doi:10.1006/game.2000.0794
    title: Ulrich Schwalbe and Paul Walker, Zermelo and the early history of game theory, Games and Economic Behavior 34(1) (2001)
    locator: pp. 123 to 137 (an English translation of Zermelo's paper, what it proves and what it does not, and the work of König and Kalmár)
  - paper: doi:10.1515/9781400881970-012
    title: Harold W. Kuhn, Extensive games and the problem of information, in Contributions to the Theory of Games II, Annals of Mathematics Studies 28, Princeton University Press (1953)
    locator: pp. 193 to 216 (a finite game with perfect information has an equilibrium in pure strategies, proved by induction on the game tree)
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press (1994)
    locator: Chapter 6, Proposition 99.2 (Kuhn's theorem, by backward induction)
---

Zermelo's theorem says that a finite game for two players, with perfect information and no chance moves, has a determined outcome: either the first player has a strategy that wins whatever the second player does, or the second player has one, or each player has a strategy that gets at least a draw. The theorem says nothing about which case holds for a given game; finding out is [solving the game](/solved-game/). The usual proof is backward induction on the [game tree](/game-tree/), which is the [minimax](/minimax/) rule written as an induction. The name is from Zermelo's 1913 paper on chess, but that paper argued in a different way and proved a different statement, as the History section explains.

## Statement

**Setting.** A game $G$ for two players, 1 and 2, is given by a finite rooted tree. Each inner node belongs to one player, who chooses one of its children. Each leaf is labeled with one of three outcomes: a win for player 1, a win for player 2, or a draw. The hypotheses are:

1. **Finite.** The tree has finitely many nodes, so every play ends after a bounded number of moves.
2. **Perfect information.** The player to move knows the node: every earlier move is visible ([perfect-information game](/perfect-information-game/)).
3. **No chance.** No node is a move of nature.
4. **Two players with opposed aims.** Player 1 prefers a win to a draw to a loss, and player 2 the reverse ([zero-sum](/zero-sum-game/)).

A *strategy* of a player names a child at each node of that player. Two strategies fix a single play, and so an outcome.

**Theorem.** Exactly one of the following holds.

- (a) Player 1 has a strategy that wins against every strategy of player 2.
- (b) Player 2 has a strategy that wins against every strategy of player 1.
- (c) Each player has a strategy that gets at least a draw against every strategy of the other.

**General form.** If the leaves carry real numbers, the payoffs of player 1, there is a number $v$ and strategies $\sigma^*$ of player 1 and $\tau^*$ of player 2 such that $\sigma^*$ gets at least $v$ against every strategy of player 2, and $\tau^*$ holds player 1 to at most $v$ against every strategy of player 1. The number $v$ is the minimax value of the root. With $+1$, $0$ and $-1$ for win, draw and loss, $v = 1$, $v = -1$ and $v = 0$ are the cases (a), (b) and (c).

## In plain words

Take tic-tac-toe, or chess with a rule that stops every game after some number of moves. Nothing is hidden and no dice are thrown. Then one of three things is true: the first player can always win, the second player can always win, or both can always avoid losing.

Why: look at the positions where the game ends. You know the result there. Now look at a position one move before the end. The player to move picks the best result for them, so you know the result there too. Keep going back, one move at a time, and you reach the start. The result you get there is what both sides can force.

The theorem does not tell you which of the three it is for chess. That would need the whole calculation.

## Proof

Write the outcome as a number for player 1: $+1$ for a win, $0$ for a draw, $-1$ for a loss. Define $v(n)$ for every node $n$ from the leaves up: at a leaf, $v(n)$ is its outcome; at a node of player 1, $v(n) = \max_c v(c)$; at a node of player 2, $v(n) = \min_c v(c)$, over the children $c$. The tree is finite, so this defines $v$ at every node. The proof works for real payoffs without change, which gives the general form.

**Claim.** For every node $n$, player 1 has a strategy in the subtree of $n$ that gets at least $v(n)$ against every strategy of player 2, and player 2 has one that holds player 1 to at most $v(n)$.

The proof is by induction on the height of the subtree of $n$.

*Height 0.* The node is a leaf. There is nothing to choose, and the outcome is $v(n)$.

*Inductive step, a node of player 1.* By hypothesis, each child $c$ has a strategy $\sigma_c$ for player 1 with outcome at least $v(c)$ and a strategy $\tau_c$ for player 2 with outcome at most $v(c)$. Player 1 chooses a child $c^*$ with $v(c^*) = v(n)$ and then plays $\sigma_{c^*}$; whatever player 2 does, the play stays in the subtree of $c^*$, and the outcome is at least $v(c^*) = v(n)$. Player 2 plays $\tau_c$ in the subtree of whichever child $c$ player 1 chooses; the outcome is at most $v(c) \le \max_{c'} v(c') = v(n)$. These choices together are a strategy of each player, because the subtrees of different children have no node in common.

*Inductive step, a node of player 2.* The same, with max and min, and the roles of the players, exchanged.

**The three cases.** Apply the claim to the root. If $v = 1$, player 1's strategy gets at least $+1$, a win, which is (a). If $v = -1$, player 2's strategy holds player 1 to $-1$, which is (b). If $v = 0$, the two strategies get at least a draw for each player, which is (c).

**Exactly one.** Suppose (a) and (b) both hold, and let the two winning strategies play against each other. They fix one play, whose outcome would be a win for both players, which is impossible. If (a) and (c) both hold, the winning strategy of player 1 against the drawing strategy of player 2 fixes a play that is both a win for player 1 and at least a draw for player 2, which is impossible. In the same way (b) and (c) exclude each other. $\blacksquare$

**A second proof, on game graphs.** The same result holds on a finite directed graph of positions with no cycle, where the labels come from a backward pass with a counter per position, as on [winning and losing states](/winning-losing-states/). With cycles, and the rule that an endless play is a draw, the same pass still divides the positions into wins, losses and draws, so the theorem holds for such games too. This form is closer to chess without a move limit, the case that Zermelo had in mind.

## Consequences

- **Every such game has a value.** Chess with a rule that ends every game, checkers, Go with a rule that forbids a repeated position, tic-tac-toe, Connect Four and Hex each have a value in $\{+1, 0, -1\}$. The theorem gives existence only.
- **Values found by computation.** For small games the backward induction can be run. The tests of the [solved game](/solved-game/) page run it on all 5,478 reachable positions of tic-tac-toe and find the value 0: a draw. Larger games were solved by search, as listed there.
- **Values found by argument.** In Hex a draw is not possible, so (c) cannot hold, and the [strategy-stealing argument](/strategy-stealing-argument/) rules out (b). So the first player wins [Hex](/hex-game/), though no winning strategy is known for large boards.
- **Pure strategies are enough.** Unlike games with hidden moves, where the [minimax theorem](/minimax-theorem/) needs mixed strategies, here a player needs no randomness. Kuhn (1953) extended the result to finite games with perfect information and any number of players: they have an equilibrium in pure strategies, found by the same induction.
- **Strategies can be read off the values.** The proof builds the strategies: at each node, move to a child of equal value. This is what [best move selection](/best-move-selection/) does, and why [retrograde analysis](/retrograde-analysis/) produces playing tables and not only values.

## Tightness

Each hypothesis is needed.

- **Chance.** Player 1 tosses a fair coin and wins on heads and loses on tails. Neither player can force a win, and no player can force a draw, so none of (a), (b), (c) holds. Only the expected outcome has a value; see [expectiminimax](/expectiminimax/).
- **Hidden moves.** Matching pennies as a game tree: player 1 chooses heads or tails, player 2 chooses without seeing it, and player 1 wins if the two match. For each strategy of one player, the other has a reply that wins, so none of (a), (b), (c) holds. The game has a value only in mixed strategies, by the minimax theorem.
- **Three players.** Player 1 chooses whether player 2 or player 3 wins. Neither player 2 nor player 3 can force a win, and the statement "exactly one of three cases" has no meaning with three players.
- **Infinite plays.** For games with infinitely long plays, determinacy can fail. Gale and Stewart (1953) showed that games in which a win is decided at a finite stage are determined, and, using the axiom of choice, built games of infinite length with perfect information in which neither player has a winning strategy.
- **Finite but huge.** The theorem holds, but the proof gives an algorithm whose time is the size of the tree. For chess this is far beyond reach, so the value of chess is not known.

## History

Zermelo (1913) asked what it means for a chess player to be in a winning position, and whether such a player can force the win within a bounded number of moves. He showed, with set theory, that if a player can force a win from a position, then the player can do it in fewer moves than the number of positions, because no position needs to repeat. He did not use backward induction, and the three-case statement above is not in his paper. Schwalbe and Walker (2001) give a translation and discuss what he proved. König (1927) used his lemma on infinite trees to carry the bound over to games with infinitely many positions but finitely many moves at each one, and Kalmár (1928/29) gave a general treatment of winning and drawing positions and strategies. The induction on the game tree, as above, became standard after von Neumann and Morgenstern (1944) and Kuhn (1953). The theorem is often called "Zermelo's theorem", which this page follows, with this caution about what Zermelo actually proved.

## References
