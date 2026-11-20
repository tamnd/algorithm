---
tag: E96CN1
kind: definition
slug: subgame-perfect-equilibrium
name: Subgame perfect equilibrium
aliases:
- SPE
- subgame perfect Nash equilibrium
area: algorithmic-game-theory/strategic-games
level: core
summary: A strategy profile that is a Nash equilibrium of every subgame. In finite perfect-information games backward induction finds one.
prereqs: [extensive-form-game, nash-equilibrium, perfect-information-game]
see_also: [trembling-hand-perfect-equilibrium, zermelo-theorem, retrograde-analysis, minimax, stackelberg-equilibrium, rubinstein-bargaining-model, kuhn-theorem-behavioral-strategies, information-set]
sources:
  - paper: "Reinhard Selten, Spieltheoretische Behandlung eines Oligopolmodells mit Nachfrageträgheit, Zeitschrift für die gesamte Staatswissenschaft 121 (1965), 301-324 and 667-689"
    title: Selten 1965
    locator: the definition of a subgame perfect equilibrium point, for an oligopoly model with demand inertia
  - book: "H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games, Volume II, Annals of Mathematics Studies 28, Princeton University Press, 1953"
    title: "Harold W. Kuhn, Extensive games and the problem of information"
    locator: pp. 193 to 216 (every finite game of perfect information has an equilibrium in pure strategies, by induction on the tree)
  - paper: doi:10.1007/BF01766400
    title: "Reinhard Selten, Reexamination of the perfectness concept for equilibrium points in extensive games, International Journal of Game Theory 4(1) (1975), 25-55"
    locator: subgame perfectness recalled, its limits in games without proper subgames, and existence through perfect equilibria
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 6 (extensive games with perfect information, subgame perfect equilibrium, the one deviation property and Kuhn's theorem)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 5 (subgame perfect equilibrium and backward induction)
---

A subgame perfect equilibrium is a strategy profile of an [extensive-form game](/extensive-form-game/) that is a [Nash equilibrium](/nash-equilibrium/) not only of the whole game but also of every subgame, the game that starts at any node where all earlier moves are known. It removes equilibria that rest on threats a player would not carry out if the moment came. Selten (1965) defined it. In a finite game of [perfect information](/perfect-information-game/), backward induction from the leaves finds one in pure strategies, in time linear in the size of the tree. Backward induction for two-player win or lose games is also on [Zermelo's theorem](/zermelo-theorem/) and [retrograde analysis](/retrograde-analysis/); this page treats the general case with any number of players and any payoffs.

## Definition

Let $\Gamma$ be a finite extensive-form game. A node $h$ starts a **subgame** if

- $h$ is alone in its [information set](/information-set/), and
- every information set that contains a node below $h$ contains only nodes below $h$.

The subgame $\Gamma_h$ is the part of the tree below $h$, with the same players, actions, chance probabilities, information sets and payoffs. The whole game is a subgame of itself. A strategy of $\Gamma$ (pure, mixed through its behavior form, or behavior) restricts to a strategy of $\Gamma_h$ by keeping only its choices at the information sets below $h$.

**Definition.** A profile $b$ of behavior strategies is a *subgame perfect equilibrium* if, for every subgame $\Gamma_h$, the restriction of $b$ to $\Gamma_h$ is a Nash equilibrium of $\Gamma_h$.

In a game of perfect information, every inner node starts a subgame, so the profile must be an equilibrium below every node, also below nodes that the equilibrium play never reaches. That is where the definition differs from Nash equilibrium: a Nash equilibrium can prescribe any action at an unreached node, because a change there does not change any payoff.

**Backward induction.** In a finite game of perfect information, solve the tree from the leaves up. At a leaf, the value is its payoff vector. At a chance node, the value is the expected value of the children. At a node of player $i$, pick an action whose child has the largest value for player $i$, and take that child's value.

```pseudo id=main
BACKWARD-INDUCTION(h)                 ▷ returns the payoff vector of the subgame at h
L1  if h is a leaf then return u(h)
L2  if h is a chance node then return Σ_a p_c(a | h) · BACKWARD-INDUCTION(h a)
L3  i ← P(h); best ← none
L4  for each action a in A(h), in order
L5      v ← BACKWARD-INDUCTION(h a)
L6      if best is none or v_i > best_i then best ← v; s(h) ← a
L7  return best
```

The profile $s$ that this builds is a pure subgame perfect equilibrium. It visits each node once, so it takes time $O(|T|)$ for a tree with $|T|$ nodes, with one comparison per edge. Ties go to the first action. The implementation has this procedure for trees with chance nodes in exact fractions, and its tests compare it with a brute force check that tries every change of every player below every node: on random trees with distinct payoffs the brute force finds exactly one subgame perfect profile, the output of backward induction, and on random trees with ties the subgame perfect profiles are exactly the outputs of backward induction under all rules for ties.

*Proof that $s$ is subgame perfect.* By induction on the height of $h$, $s$ is a Nash equilibrium of $\Gamma_h$. For a leaf there is nothing to prove. At a chance node, a deviation of player $j$ in $\Gamma_h$ is a deviation in each child subgame, and by induction it gains in none of them, so it gains nothing on average. At a node of player $i$, a deviation of a player $j \ne i$ changes only the play inside the child that $s$ chooses, where by induction it gains nothing. A deviation of player $i$ may change the action at $h$ to some $a'$ and also the play inside the children. The play then goes into $\Gamma_{h a'}$, where $s$ is a Nash equilibrium by induction, so player $i$ gets at most $v(h a')_i$, and $v(h a')_i \le v(h)_i$ by the choice at L6. $\square$

**The one-shot deviation property.** In a finite game of perfect information, a pure profile is subgame perfect if and only if no player gains by changing the action at a single node, with the rest of the profile fixed and the payoff measured in the subgame at that node. So a profile is subgame perfect exactly when backward induction with some rule for ties produces it.

**Existence in general.** In a finite game with [perfect recall](/perfect-recall/), a subgame perfect equilibrium in behavior strategies exists. Take a subgame with no smaller proper subgame, pick a Nash equilibrium of it in behavior strategies (by [Nash's theorem](/nash-existence-theorem/) and [Kuhn's theorem](/kuhn-theorem-behavioral-strategies/)), replace the subgame by a leaf with its equilibrium payoffs, and repeat. Selten (1975) also showed it as a consequence of the existence of [trembling-hand perfect equilibria](/trembling-hand-perfect-equilibrium/), which are subgame perfect.

## Examples and non-examples

**The entry game.** Player 1 chooses Out, which ends the game with payoffs $(0, 2)$, or In; after In, player 2 chooses Fight, with payoffs $(-1, -1)$, or Accommodate, with payoffs $(1, 1)$. The pure Nash equilibria are (Out, Fight) and (In, Accommodate). In (Out, Fight), player 2 never moves, so the threat to fight costs nothing. In the subgame after In, Fight gives player 2 $-1$ and Accommodate gives 1, so (Out, Fight) is not a Nash equilibrium of that subgame. Backward induction gives (In, Accommodate) only, with payoffs $(1, 1)$, as on [normal-form game](/normal-form-game/).

**The centipede game.** Two players take turns, 6 stages in all, and player 1 moves at the even stages. At stage $k = 0, \ldots, 5$ the mover can take, which ends the game with $k + 2$ for the mover and $k$ for the other, or pass. If both pass at every stage, both get 6. At the last stage, taking gives the mover 7 against 6 for passing, so the mover takes. At each earlier stage, taking gives $k + 2$, while passing leads to the other player taking at once, which gives the mover $k + 1$. So the only subgame perfect equilibrium takes at every stage, and the play ends at once with payoffs $(2, 0)$, although both players could get 6. In experiments people usually pass for several stages.

**An ultimatum game with ties.** Player 1 offers $x \in \{0, 1, 2\}$ of 2 units to player 2, who accepts, with payoffs $(2 - x, x)$, or rejects, with $(0, 0)$. After $x = 1$ or $x = 2$, accepting is strictly better. After $x = 0$, player 2 is indifferent. So there are two pure subgame perfect equilibria: player 2 accepts every offer and player 1 offers 0, with payoffs $(2, 0)$; or player 2 rejects 0 and accepts the rest and player 1 offers 1, with payoffs $(1, 1)$. Nash equilibria are many more: for each $x$, "accept only offers of at least $x$" against the offer $x$ is one. With payoffs that are all different for each player, backward induction never meets a tie, and the subgame perfect equilibrium is unique.

**Non-example: a game without proper subgames.** Player 1 chooses Out, with payoffs $(2, 2)$, or L or R. Player 2 then chooses $\ell$ or $r$ without seeing whether L or R was played. The payoffs are $(3, 1)$ after (L, $\ell$), $(0, 0)$ after (L, $r$) and (R, $\ell$), and $(1, 3)$ after (R, $r$). The two nodes of player 2 form one information set, so the only subgame is the whole game, and every Nash equilibrium is subgame perfect. One of them is (Out, $r$): it asks player 2 to answer as if player 1 had played R, which is worse for player 1 than Out whatever player 2 does. Subgame perfection does not rule this out. Refinements that put beliefs on information sets, such as sequential equilibrium (Kreps and Wilson 1982), or that use [trembles](/trembling-hand-perfect-equilibrium/), are needed for such games.

## Related definitions

- **Zero-sum games.** In a two-player zero-sum game of perfect information, backward induction is the [minimax](/minimax/) rule, and [alpha-beta pruning](/alpha-beta-pruning/) finds the same value with fewer node visits. Games given as graphs with cycles, such as chess endgames, are solved by [retrograde analysis](/retrograde-analysis/).
- **Commitment.** A [Stackelberg equilibrium](/stackelberg-equilibrium/) is the subgame perfect equilibrium of the game in which the leader first commits to a strategy and the follower then responds.
- **Infinite horizon.** In games with infinitely long plays, backward induction has no last node to start from, but the definition still applies. In the [Rubinstein bargaining model](/rubinstein-bargaining-model/), the subgame perfect equilibrium is unique, and in infinitely repeated games the folk theorems describe a large set of them.
- **Trembling-hand perfection.** A [trembling-hand perfect equilibrium](/trembling-hand-perfect-equilibrium/) is subgame perfect, and in addition it handles unreached information sets that do not start a subgame.
- **Computation.** For perfect information, the algorithm above is linear in the tree, which can itself be exponential in the description of the game, as for chess. With imperfect information, the bottom-up method needs a Nash equilibrium of each minimal subgame, which is [PPAD](/ppad/)-hard in general ([computation](/nash-equilibrium-computation/)).

## References
