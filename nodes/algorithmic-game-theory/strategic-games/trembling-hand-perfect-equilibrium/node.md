---
tag: 1ESJ7S
kind: definition
slug: trembling-hand-perfect-equilibrium
name: Trembling-hand perfect equilibrium
aliases:
- perfect equilibrium
- Selten perfect equilibrium
area: algorithmic-game-theory/strategic-games
level: advanced
summary: A Nash equilibrium that is the limit of equilibria of perturbed games in which every action is played with a small positive probability.
prereqs: [subgame-perfect-equilibrium, dominant-strategy]
see_also: [nash-equilibrium, subgame-perfect-equilibrium, extensive-form-game, information-set, quantal-response-equilibrium, epsilon-nash-equilibrium, kakutani-fixed-point-theorem, separating-hyperplane-theorem]
sources:
  - paper: doi:10.1007/BF01766400
    title: "Reinhard Selten, Reexamination of the perfectness concept for equilibrium points in extensive games, International Journal of Game Theory 4(1) (1975), 25-55"
    locator: perfect equilibria defined by perturbed games, the agent normal form, existence for every finite extensive game with perfect recall, and the fact that perfect equilibria are subgame perfect
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 12 (sequential equilibrium and trembling hand perfect equilibrium)
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: the chapter on equilibrium refinements (perfect equilibrium in strategic and extensive form)
---

A trembling-hand perfect equilibrium is a [Nash equilibrium](/nash-equilibrium/) that stays a best response when every player makes small mistakes: each strategy in it is a best response to some nearby profile in which every pure strategy of every player has positive probability. Selten (1975) defined it to remove equilibria that rely on weakly dominated strategies or on bad play at [information sets](/information-set/) that the equilibrium never reaches, which [subgame perfection](/subgame-perfect-equilibrium/) cannot always remove. Every finite game has one. In two-player normal-form games, the perfect equilibria are exactly the Nash equilibria in which no player uses a weakly dominated strategy.

## Definition

Let $G$ be a finite normal-form game with players $N$, pure strategies $S_i$ and payoffs $u_i$. A mixed strategy is *completely mixed* if it gives every pure strategy a positive probability.

**Definition (Selten 1975).** A profile $\sigma$ is a *trembling-hand perfect equilibrium* of $G$ if there is a sequence $\sigma^k$ of completely mixed profiles with $\sigma^k \to \sigma$ such that, for every $k$ and every player $i$, $\sigma_i$ is a best response to $\sigma^k_{-i}$.

The profile $\sigma^k$ models the mistakes: each player intends $\sigma_i$, but the hand trembles and every strategy is played with a small probability. Two other forms are equivalent to this one.

- **Perturbed games.** For a vector $\eta$ of small positive numbers $\eta_i(s_i)$ with $\sum_{s_i} \eta_i(s_i) < 1$, the perturbed game $G(\eta)$ allows player $i$ only the mixed strategies with $\sigma_i(s_i) \ge \eta_i(s_i)$ for all $s_i$. Then $\sigma$ is perfect if and only if it is a limit of Nash equilibria $\sigma^\eta$ of $G(\eta)$ as $\eta \to 0$.
- **$\varepsilon$-perfect profiles.** A completely mixed profile is $\varepsilon$-perfect if every pure strategy that is not a best response gets probability at most $\varepsilon$. Then $\sigma$ is perfect if and only if it is a limit of $\varepsilon$-perfect profiles as $\varepsilon \to 0$.

**Extensive games.** For an [extensive-form game](/extensive-form-game/), Selten applied the definition to the *agent normal form*: each information set is played by a separate agent who has the payoff of its player, so the trembles at different information sets of one player are independent. A *perfect equilibrium of the extensive game* is a perfect equilibrium of the agent normal form, read as a behavior profile. It is subgame perfect: under the trembles every subgame is reached with positive probability, so the restriction to each subgame is a limit of best responses there, and so a Nash equilibrium of the subgame.

**Existence (Selten 1975).** Every finite normal-form game has a perfect equilibrium, and so every finite extensive game with perfect recall has a perfect equilibrium in behavior strategies.

*Proof.* Take $\eta^k \to 0$ with all entries positive. Each $G(\eta^k)$ has compact convex strategy sets and multilinear payoffs, so it has a Nash equilibrium $\sigma^k$ by the argument of [Kakutani's fixed point theorem](/kakutani-fixed-point-theorem/). In $\sigma^k$, a pure strategy of player $i$ that is not a best response to $\sigma^k_{-i}$ gets exactly its minimum probability $\eta^k_i(s_i)$, since any extra weight on it could be moved to a best response. The profiles lie in a compact set, so a subsequence converges to some $\sigma$. If $\sigma_i(s_i) > 0$, then $\sigma^k_i(s_i) > \eta^k_i(s_i)$ for large $k$, so $s_i$ is a best response to $\sigma^k_{-i}$. Every pure strategy in the support of $\sigma_i$ is then a best response to $\sigma^k_{-i}$, and so is $\sigma_i$. The $\sigma^k$ are completely mixed, so $\sigma$ is perfect. $\square$

**Basic properties.**

- *Perfect implies Nash.* Let $k \to \infty$ in $u_i(\sigma_i, \sigma^k_{-i}) \ge u_i(s_i, \sigma^k_{-i})$; the payoffs are continuous.
- *Perfect implies undominated.* A strategy $s_i$ is *weakly dominated* if some mixed strategy $\tau_i$ does at least as well against every profile of the others and strictly better against one ([dominant strategy](/dominant-strategy/)). Against a completely mixed $\sigma^k_{-i}$, $\tau_i$ does strictly better than $s_i$, so a best response to $\sigma^k_{-i}$ gives $s_i$ probability 0. So no strategy in the support of a perfect equilibrium is weakly dominated.
- *For two players, undominated Nash implies perfect.* Let $(\sigma_1, \sigma_2)$ be a Nash equilibrium in which neither $\sigma_i$ is weakly dominated. By the [separating hyperplane theorem](/separating-hyperplane-theorem/), applied to the payoff vectors against the pure strategies of the opponent, a mixed strategy that is not weakly dominated is a best response to some completely mixed strategy $\tau_{-i}$ of the opponent. Put $\sigma^k_{-i} = (1 - 1/k)\sigma_{-i} + (1/k)\tau_{-i}$. It is completely mixed, and $\sigma_i$ is a best response to both parts of the mix, so to $\sigma^k_{-i}$. So the equilibrium is perfect.

For three or more players, the last statement fails in general. The hyperplane argument gives a full-support belief about the others that may be correlated, while the trembles of different players must be independent.

## Examples and non-examples

**A weakly dominated equilibrium.** In the 2 by 2 game with payoffs $(1, 1)$ at (U, L) and $(0, 0)$ in the other three cells, the Nash equilibria are (U, L) and (D, R). Against a completely mixed strategy of the column player with $q > 0$ on L, U gives $q$ and D gives 0, so D is never a best response, and (D, R) is not perfect. The profile (U, L) is perfect, with any trembles. Here D is weakly dominated by U, and R by L.

**The entry game.** In the entry game, player 1 chooses Out, with payoffs $(0, 2)$, or In, and then player 2 chooses Fight, $(-1, -1)$, or Accommodate, $(1, 1)$. In the normal form, Fight is weakly dominated by Accommodate: they tie when player 1 plays Out and Accommodate is better after In. So the equilibrium (Out, Fight) is not perfect, and the only perfect equilibrium is (In, Accommodate), the [subgame perfect](/subgame-perfect-equilibrium/) one.

**Normal-form perfection is not enough in a tree.** Player 1 chooses L, which ends the game with payoffs $(2, 0)$, or R. After R, player 2 chooses $\ell$, with payoffs $(1, 1)$, or $r$. After $r$, player 1 chooses $a$, with $(3, 3)$, or $b$, with $(0, 0)$. Backward induction gives $a$, then $r$, then R, with payoffs $(3, 3)$. In the normal form, player 1 has the four strategies La, Lb, Ra and Rb. The profile (Lb, $\ell$) is a perfect equilibrium of the normal form: with the trembles $\varepsilon$ on La, $\varepsilon$ on Ra, $4\varepsilon$ on Rb and $\varepsilon$ on $r$, player 2 gets $5\varepsilon$ from $\ell$ and $3\varepsilon$ from $r$, and player 1 gets 2 from La and Lb, $1 + 2\varepsilon$ from Ra and $1 - \varepsilon$ from Rb. Yet (Lb, $\ell$) is not subgame perfect, because $b$ is a bad move at player 1's second node. The trembles make the mistake $b$ more likely than $a$ after a mistake R, which a single hand that trembles at each move independently would not do. In the agent normal form, the agent at the last node trembles alone, plays $a$, and the only perfect equilibrium is the backward induction one.

**Non-example: a strict equilibrium is never removed.** If every deviation from $\sigma$ loses strictly, $\sigma$ is pure and stays a strict best response to all nearby profiles, so it is perfect. Refinement matters only when some player is indifferent.

## Related definitions

- **Proper equilibrium.** Myerson (1978) asked in addition that a costlier mistake be much less likely than a cheaper one. Proper equilibria exist and are perfect.
- **Sequential equilibrium.** Kreps and Wilson (1982) attach beliefs to information sets and ask that the strategies be best responses to the beliefs, and that the beliefs come from Bayes' rule along completely mixed profiles. Every perfect equilibrium of the agent normal form is sequential.
- **Quantal response.** In a [quantal response equilibrium](/quantal-response-equilibrium/), every strategy also gets positive probability, but the probability depends on the payoff in a fixed way, so worse mistakes are less likely. Its limits, as the noise goes to 0, are Nash equilibria.
- **Approximate equilibrium.** An [$\varepsilon$-Nash equilibrium](/epsilon-nash-equilibrium/) bounds the gain of a deviation. An $\varepsilon$-perfect profile instead bounds the probability of the strategies that are not best responses, which is a different condition.

## References
