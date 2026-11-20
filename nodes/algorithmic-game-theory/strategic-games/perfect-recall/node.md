---
tag: RBDEM7
kind: definition
slug: perfect-recall
name: Perfect recall
aliases:
- game with perfect recall
area: algorithmic-game-theory/strategic-games
level: core
summary: The property that no player forgets their own past actions or what they knew earlier in an extensive-form game.
prereqs: [information-set]
see_also: [kuhn-theorem-behavioral-strategies, extensive-form-game, imperfect-information-game, sequence-form, sequence-form-linear-program, counterfactual-regret-minimization, mixed-strategy, np-hard]
sources:
  - book: "H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games, Volume II, Annals of Mathematics Studies 28, Princeton University Press, 1953"
    title: "Harold W. Kuhn, Extensive games and the problem of information"
    locator: pp. 193 to 216 (the definition of perfect recall and the theorem that behavior strategies suffice under it)
  - paper: doi:10.1006/game.1997.0536
    title: "Michele Piccione and Ariel Rubinstein, On the interpretation of decision problems with imperfect recall, Games and Economic Behavior 20(1) (1997), 3-24"
    locator: the absent-minded driver, where the best behavior strategy beats every pure and mixed strategy
  - paper: doi:10.1016/0899-8256(92)90035-Q
    title: "Daphne Koller and Nimrod Megiddo, The complexity of two-person zero-sum games in extensive form, Games and Economic Behavior 4(4) (1992), 528-552"
    locator: NP-hardness of two-person zero-sum games without perfect recall, and a polynomial algorithm with perfect recall
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 11 (perfect recall, and the equivalence of mixed and behavioral strategies)
---

Perfect recall is the property of an [extensive-form game](/extensive-form-game/) that no player ever forgets their own earlier moves or anything they knew before. Formally, two nodes in one [information set](/information-set/) of a player must have the same history of that player's own information sets and actions. Kuhn (1953) defined it and proved that, with perfect recall, a player loses nothing by randomizing separately at each information set ([Kuhn's theorem](/kuhn-theorem-behavioral-strategies/)). Poker and most card games have perfect recall; the [sequence form](/sequence-form/) and [counterfactual regret minimization](/counterfactual-regret-minimization/) both need it.

## Definition

Fix a finite extensive-form game and a player $i$. For a node $h$, let the *experience* $X_i(h)$ be the sequence of pairs $(I, a)$ in which $I$ is an information set of $i$ that the path from the root to $h$ passes through, before $h$, and $a$ is the action taken there, in the order of the path. Chance moves and moves of the other players are not in $X_i(h)$.

**Definition.** Player $i$ has *perfect recall* if for every information set $I$ of $i$ and every two nodes $h, h' \in I$,

$$X_i(h) = X_i(h').$$

The game has perfect recall if every player has it.

The condition says two things. The player remembers every action they took, since the actions are in $X_i$. The player also remembers everything they knew, since the earlier information sets are in $X_i$, and two paths that the player could tell apart earlier lead to different earlier sets. With perfect recall, no path meets an information set twice: if $h \in I$ came before $h' \in I$ on one path, then $X_i(h')$ would contain a pair at $I$ and $X_i(h)$ would not, and the two sequences would differ in length.

**The sequence of an information set.** With perfect recall, the common value $X_i(I) = X_i(h)$ for $h \in I$ is well defined. The last action in it is the action of player $i$ that leads toward $I$, and the sequence of actions in it is the *sequence* $\mathrm{seq}_i(I)$ used by the [sequence form](/sequence-form/).

**A linear-time test.** It is enough to check, for each information set $I$, that all its nodes have the same *last* pair of $X_i$ (or that none of them has one). By induction on the length of the experience: if all nodes of $I$ have the last pair $(I', a')$, the nodes of $I'$ that come before them have equal experiences by the induction hypothesis, and adding $(I', a')$ gives equal experiences at $I$. A depth-first walk that carries the last own pair of each player checks the game in time linear in the size of the tree.

## Examples and non-examples

**Poker.** In Kuhn poker (see [imperfect-information games](/imperfect-information-game/)), each player sees their own card and all bets. At every information set, the player's own card and their own earlier bets are the same at all nodes, so the game has perfect recall. The same holds for Texas hold'em and most card games with one human per player.

**A simultaneous game.** Every finite normal-form game, written as a tree with one information set per player, has perfect recall: each player moves once, so every experience is empty.

**Non-example: the forgetful player.** Player 1 chooses L or R, and later chooses l or r at one information set that contains both nodes, after L and after R. Player 1 gets 1 after (L, l) or (R, r) and 0 otherwise. The two nodes have the experiences $((I_0, L))$ and $((I_0, R))$, which differ, so recall is not perfect. The mixed strategy that plays (L, l) or (R, r) with probability $1/2$ each reaches the leaves Ll and Rr with probability $1/2$ each and gets 1. A behavior strategy plays L with probability $\alpha$ and l with probability $\gamma$, independently. Probability 0 on Lr and Rl needs $\alpha(1 - \gamma) = 0$ and $(1 - \alpha)\gamma = 0$, so $\alpha = \gamma \in \{0, 1\}$, and then one of Ll and Rr has probability 0. No behavior strategy gives the distribution of the mixed strategy.

**Non-example: the absent-minded driver (Piccione and Rubinstein 1997).** A driver on a highway at night must take the second exit. Exiting at the first exit X pays 0, exiting at the second exit Y pays 4, and going past both pays 1. The driver cannot tell the two exits apart and does not remember passing one, so the nodes X and Y form one information set, and the path through Y meets this set twice. The pure strategies are Exit, which pays 0, and Continue, which pays 1, so no mixed strategy pays more than 1. The behavior strategy that continues with probability $p$ at each exit pays

$$0 \cdot (1 - p) + 4\, p (1 - p) + 1 \cdot p^2 = 4p - 3p^2,$$

with the maximum $4/3$ at $p = 2/3$. It reaches X, Y and the end with the probabilities $(1/3, 2/9, 4/9)$, which no mixed strategy gives. In the other direction, the mixed strategy that exits for sure or continues for sure, with probability $1/2$ each, gives $(1/2, 0, 1/2)$, which no behavior strategy gives. So without perfect recall, neither kind of strategy covers the other.

**Non-example: bridge as a two-player game.** If each team of two partners in bridge is one player, the player forgets: when one partner plays, the player does not know the cards of the other partner, which the same player knew when the partner moved. Team games are a standard source of imperfect recall.

## Related definitions

- **Kuhn's theorem.** With perfect recall, every mixed strategy has a behavior strategy with the same distribution on outcomes against every profile of the others, and conversely ([Kuhn's theorem](/kuhn-theorem-behavioral-strategies/)). The two examples above show that both directions can fail without it.
- **Computation.** Koller and Megiddo (1992) showed that finding the value of a two-player zero-sum extensive game without perfect recall is [NP-hard](/np-hard/), and that with perfect recall it is solvable in polynomial time. The polynomial method is the [sequence form](/sequence-form/) LP ([sequence-form linear program](/sequence-form-linear-program/)).
- **Absent-mindedness.** A path meets one information set twice. Perfect recall excludes it. Piccione and Rubinstein use the absent-minded driver to show that, in such a game, the best plan made before the trip and the best choice at an exit can differ.

## References
