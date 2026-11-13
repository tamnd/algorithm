---
tag: YFAZJ2
kind: definition
slug: imperfect-information-game
name: Imperfect-information game
aliases:
- hidden-information game
area: games-and-search/game-tree-search
level: advanced
summary: Game in which players have private or hidden information, such as cards held in hand.
prereqs: [game-tree, stochastic-game, nash-equilibrium]
see_also: [counterfactual-regret-minimization, nash-equilibrium-computation, minimax-theorem, expectiminimax, pomdp, belief-space, perfect-information-game, linear-programming-problem]
sources:
  - book: "H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games, Volume II, Annals of Mathematics Studies 28, Princeton University Press, 1953"
    title: "Harold W. Kuhn, Extensive games and the problem of information"
    locator: pp. 193 to 216 (extensive games with information sets, perfect recall, and the theorem that behavior strategies suffice under perfect recall)
  - book: "H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games, Volume I, Annals of Mathematics Studies 24, Princeton University Press, 1950"
    title: "Harold W. Kuhn, A simplified two-person poker"
    locator: pp. 97 to 103 (the three-card poker game and its equilibria)
  - paper: doi:10.1016/0899-8256(92)90035-Q
    title: "Daphne Koller and Nimrod Megiddo, The complexity of two-person zero-sum games in extensive form, Games and Economic Behavior 4(4) (1992), 528-552"
    locator: NP-hardness without perfect recall, and a polynomial algorithm with perfect recall
  - paper: doi:10.1006/game.1996.0051
    title: "Daphne Koller, Nimrod Megiddo and Bernhard von Stengel, Efficient computation of equilibria for extensive two-person games, Games and Economic Behavior 14(2) (1996), 247-259"
    locator: the sequence form, a strategy representation of size linear in the game tree
  - paper: doi:10.1016/S0004-3702(97)00082-9
    title: "Ian Frank and David Basin, Search in games with incomplete information: a case study using Bridge card play, Artificial Intelligence 100(1-2) (1998), 87-123"
    locator: strategy fusion and non-locality, the two errors of searching each possible world as a game of perfect information
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 5 (extensive-form games with imperfect information, perfect recall and the sequence form)
---

An imperfect-information game is a game in which a player who must move may not know everything that has happened so far. Some earlier moves of chance or of other players are hidden: the cards in the other hands, the tiles on another rack, or a move made at the same time. The player knows only which group of possible positions the game is in, called an information set. Poker, bridge, Scrabble and simultaneous-move games are examples. Optimal play then often needs randomness, and the search methods for games of [perfect information](/perfect-information-game/) do not apply directly.

## Definition

A finite **extensive game with imperfect information** consists of:

- a finite rooted game tree; its nodes are **histories** $h$ (the sequences of actions from the root), and its leaves are the terminal histories $z$;
- a set of players $N$ and a **player function** $P$ that maps each non-terminal history to a player in $N$ or to **chance** $c$;
- for each history $h$ with $P(h) = c$, a probability distribution on the actions at $h$;
- for each player $i$, a partition $\mathcal I_i$ of the histories where $i$ moves into **information sets**, such that all histories in one set $I$ have the same set of actions $A(I)$;
- a payoff $u_i(z)$ for each player $i$ at each leaf $z$.

At a history $h \in I$, player $i$ knows that the game is at some history of $I$ but not at which one. The game has **perfect information** when every information set is a single history; chance moves are then allowed, as in a [stochastic game](/stochastic-game/).

A **pure strategy** of player $i$ picks one action in $A(I)$ for each $I \in \mathcal I_i$. It must pick the same action at all histories of $I$, since the player cannot tell them apart. A **mixed strategy** is a probability distribution on pure strategies. A **behavior strategy** $\sigma_i$ picks, at each information set $I$ separately, a distribution $\sigma_i(I, \cdot)$ on $A(I)$.

The game has **perfect recall** if no player ever forgets what they knew or did: for any two histories in the same information set of player $i$, the sequences of information sets of $i$ visited on the way, and the actions $i$ took there, are the same. Under perfect recall, **Kuhn's theorem** (1953) says that every mixed strategy has a behavior strategy that gives the same probability to every leaf against every strategy of the others. So behavior strategies, with one distribution per information set, are enough.

## Examples and non-examples

- **Kuhn poker.** Each of two players gets one card from J < Q < K, and the third card is not seen. The deal is a chance node with 6 outcomes, and each player sees only their own card. Player 1 has 6 information sets: the card (3 choices) together with either the start or the history "check, bet". Player 2 has 6: the card together with "check" or "bet". Each player has $2^6 = 64$ pure strategies. Kuhn (1950) showed that in every equilibrium player 1 sometimes bets J, a bluff, and that the value to player 1 is $-1/18$. No pure strategy is optimal, so randomness is needed although no moves are simultaneous. [Counterfactual regret minimization](/counterfactual-regret-minimization/) solves it with these 12 information sets.
- **A matrix game as a tree.** In rock, paper, scissors, player 1 moves and then player 2 moves without seeing it: the three nodes of player 2 form one information set. Every simultaneous-move game is an imperfect-information game of this form, and the [minimax theorem](/minimax-theorem/) gives the value of the zero-sum ones.
- **Bridge, Scrabble, Stratego and Kriegspiel chess.** Bridge hides the other hands, Scrabble the other rack and the bag, Stratego the identity of the pieces, and Kriegspiel the moves of the opponent.
- **Non-example: backgammon.** Dice add chance, but each roll is seen by both players, so every information set is a single history. This is a game of perfect information with chance, solved by [expectiminimax](/expectiminimax/).
- **Non-example of perfect recall.** A player moves twice and forgets the first move before the second. The mixed strategy "left both times with probability 1/2, right both times with probability 1/2" makes the two moves agree. No behavior strategy can do that while it plays left with probability 1/2 at each move, so Kuhn's theorem fails without perfect recall. Bridge, played as a two-player game of two teams, also lacks perfect recall: each team is one player, but the two partners do not see each other's cards.

### Why tree search breaks

A natural method samples the hidden information, solves each sample as a game of perfect information, and picks the move that is best on average. This is called determinization, or perfect-information Monte Carlo. Frank and Basin (1998) named its two errors.

- **Strategy fusion.** The method assumes that the player can choose differently in each sample, although the samples lie in the same information sets. Example: chance picks world 1 or world 2 with probability 1/2 each, hidden from MAX. MAX may take a sure payoff of $3/4$, or go on to a second move, left or right, still without knowing the world. Left pays 1 in world 1 and 0 in world 2, and right pays the opposite. Going on is really worth $1/2$, whichever second move MAX picks. But each sample, solved alone, picks the right second move and values going on at 1, so the method goes on and loses $1/4$ on average.
- **Non-locality.** In a game of perfect information, the value of a node depends only on its subtree. Here the value of a history depends on how likely the other histories of its information set are, and so on the strategy in other parts of the tree. In Kuhn poker, whether player 2 should call a bet with Q depends on how often player 1 bets with J and with K.

## Related definitions

- **Sequence form.** Koller, Megiddo and von Stengel (1996) describe a behavior strategy under perfect recall by its realization weights, the probabilities of the player's own action sequences. These weights satisfy linear constraints, the number of sequences is at most the number of histories, and the expected payoff is bilinear in them. So a two-player zero-sum game with perfect recall is solved by a linear program of size linear in the tree, while the normal form can have exponentially many pure strategies. In Kuhn poker each player has 13 sequences, against 64 pure strategies. See [equilibrium computation](/nash-equilibrium-computation/).
- **Complexity.** Koller and Megiddo (1992) showed that computing the value of a two-player zero-sum game in extensive form is NP-hard without perfect recall, and polynomial with perfect recall.
- **Incomplete information.** A game in which the payoffs or the types of the players are not common knowledge (a Bayesian game). Harsanyi's transformation adds a chance move that picks the types, which turns it into a game of imperfect information.
- **Partially observable Markov decision process.** One player who does not see the state, with no opponent: a [POMDP](/pomdp/). The player can track a belief, a distribution on the states ([belief space](/belief-space/)). With an opponent the belief depends on the opponent's strategy, which is the non-locality above.
- **Public information.** Actions and chance outcomes that all players see, such as the bets in poker. Many algorithms split the tree into public states and solve subgames of them.

## References
