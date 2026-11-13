---
tag: C4QMRK
kind: theorem
slug: nash-existence-theorem
name: Nash existence theorem
aliases:
- Nash's theorem
area: games-and-search/game-tree-search
level: advanced
summary: Every finite game in normal form, with any number of players, has at least one Nash equilibrium in mixed strategies.
prereqs: [nash-equilibrium, convex-set]
see_also: [minimax-theorem, nash-equilibrium-computation, ppad, banach-fixed-point-theorem, markov-game, zero-sum-game]
sources:
  - paper: doi:10.1073/pnas.36.1.48
    title: "John F. Nash, Equilibrium points in n-person games, Proceedings of the National Academy of Sciences 36(1) (1950), 48-49"
    locator: the existence proof from Kakutani's fixed point theorem applied to the map of best responses
  - paper: doi:10.2307/1969529
    title: "John Nash, Non-cooperative games, Annals of Mathematics 54(2) (1951), 286-295"
    locator: the existence proof from Brouwer's fixed point theorem with the continuous improvement map, and the symmetric case
  - paper: doi:10.1215/S0012-7094-41-00838-4
    title: "Shizuo Kakutani, A generalization of Brouwer's fixed point theorem, Duke Mathematical Journal 8(3) (1941), 457-459"
    locator: the fixed point theorem for upper semicontinuous maps with nonempty convex values on a simplex
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 2 (existence of a Nash equilibrium from Kakutani's theorem) and Chapter 3 (mixed strategy equilibrium)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 2, Christos H. Papadimitriou, The complexity of finding Nash equilibria (the Brouwer proof and why it does not give an efficient algorithm)
---

Nash's theorem says that every finite game has an equilibrium if the players may randomize. It holds for any number of players and any payoffs, so it extends the existence part of the [minimax theorem](/minimax-theorem/) from two-player [zero-sum games](/zero-sum-game/) to all finite games. Nash gave two proofs, with Kakutani's fixed point theorem in 1950 and with Brouwer's in 1951. Neither proof tells how to find the equilibrium.

## Statement

A finite game has players $1, \ldots, n$, finite sets $S_1, \ldots, S_n$ of pure strategies, and payoffs $u_i : S_1 \times \cdots \times S_n \to \mathbb{R}$. A mixed strategy $\sigma_i$ is a point of the simplex $\Delta(S_i)$, and $u_i(\sigma)$ is the expected payoff when the players draw independently ([Nash equilibrium](/nash-equilibrium/) gives the full definitions).

**Theorem (Nash 1950, 1951).** Every finite game has a Nash equilibrium in mixed strategies: a profile $\sigma^* \in \Delta(S_1) \times \cdots \times \Delta(S_n)$ with $u_i(s_i, \sigma^*_{-i}) \le u_i(\sigma^*)$ for every player $i$ and every $s_i \in S_i$.

**Symmetric form (Nash 1951).** If the game is symmetric (all players have the same strategy set, and permuting the players permutes the payoffs in the same way), it has a symmetric equilibrium, in which all players use the same mixed strategy.

The hypotheses are that there are finitely many players and that each has finitely many pure strategies. The payoffs are arbitrary real numbers, and the game need not be zero sum.

## In plain words

Take any game where each player has a finite list of choices and may pick one by chance. The theorem says that there is always a way for all players to mix their choices so that nobody regrets their own mix once they see the mixes of the others. It may be the only such way or one of many, and it may need chance, as in a game of guessing where any fixed choice can be exploited. The proof shows that such a point must exist, much as a stirred cup of coffee must have one point that ends where it started, but it does not say where the point is.

## Proof

We give Nash's 1951 proof. It uses **Brouwer's fixed point theorem**: every continuous map from a nonempty compact convex subset of $\mathbb{R}^k$ to itself has a fixed point.

**The space.** Let $X = \Delta(S_1) \times \cdots \times \Delta(S_n)$. It is a product of simplices, so it is a nonempty, compact, [convex set](/convex-set/) in $\mathbb{R}^{|S_1| + \cdots + |S_n|}$.

**The gains.** For $\sigma \in X$, a player $i$ and $s \in S_i$, let

$$g_{i,s}(\sigma) = \max\big(0,\ u_i(s, \sigma_{-i}) - u_i(\sigma)\big),$$

the gain of player $i$ from a switch to the pure strategy $s$. The function $u_i(\sigma)$ is a polynomial in the coordinates of $\sigma$, so each $g_{i,s}$ is continuous and nonnegative.

**The map.** Define $T : X \to X$ by

$$T(\sigma)_i(s) = \frac{\sigma_i(s) + g_{i,s}(\sigma)}{1 + \sum_{t \in S_i} g_{i,t}(\sigma)} .$$

Each $T(\sigma)_i$ has nonnegative entries that sum to 1, so $T$ maps $X$ to $X$, and $T$ is continuous because the denominator is at least 1. The map moves weight toward the pure strategies that do better than the current mix. By Brouwer's theorem, $T$ has a fixed point $\sigma^*$.

**A fixed point is an equilibrium.** Fix a player $i$ and write $G = \sum_{t} g_{i,t}(\sigma^*)$. Since $u_i(\sigma^*) = \sum_{s} \sigma^*_i(s)\, u_i(s, \sigma^*_{-i})$ is an average over the support of $\sigma^*_i$, some $s$ with $\sigma^*_i(s) > 0$ has $u_i(s, \sigma^*_{-i}) \le u_i(\sigma^*)$, and so $g_{i,s}(\sigma^*) = 0$. For this $s$ the fixed point equation reads $\sigma^*_i(s) = \sigma^*_i(s) / (1 + G)$, and since $\sigma^*_i(s) > 0$, $G = 0$. So $g_{i,t}(\sigma^*) = 0$ for all $t$: no pure deviation gains for player $i$. This holds for every $i$, so $\sigma^*$ is an equilibrium. (Conversely, at an equilibrium all gains are 0 and $T(\sigma^*) = \sigma^*$.)

**The symmetric form.** If the game is symmetric, $T$ maps the convex compact set of symmetric profiles $\{(\tau, \ldots, \tau)\}$ to itself, since all players then have the same gains. Brouwer's theorem on this set gives a symmetric fixed point. $\blacksquare$

**The 1950 proof.** Let $B(\sigma) \subseteq X$ be the set of profiles $\tau$ in which every $\tau_i$ is a best response to $\sigma_{-i}$. Each $B(\sigma)$ is nonempty and convex, because the best responses of player $i$ are the mixes of a set of pure best responses, and the graph of $B$ is closed, because the payoffs are continuous. **Kakutani's fixed point theorem** (1941) says that such a set-valued map on a compact convex set has a point $\sigma^* \in B(\sigma^*)$, and that point is an equilibrium.

### Example

In matching pennies the row player wins 1 if the coins match and loses 1 otherwise. Start at the profile where both players show heads. The row player gets 1 and gains nothing by a switch. The column player gets $-1$ and gains 2 by switching to tails. So $T$ keeps the row strategy at $(1, 0)$ and maps the column strategy to $((1 + 0)/3, (0 + 2)/3) = (1/3, 2/3)$. The only fixed point is $((1/2, 1/2), (1/2, 1/2))$, the unique equilibrium.

The map is not a contraction, so iterating it need not find the fixed point. From (heads, heads), the iterates of $T$ in floating point do not converge: from step 1,000 to step 100,000 the distance from $(1/2, 1/2)$, in the plane of the two probabilities of heads, stays between 0.25 and 0.30. Compare the [Banach fixed point theorem](/banach-fixed-point-theorem/), whose iteration does converge, but only for contractions.

## Consequences

- **The minimax theorem.** In a two-player zero-sum game, an equilibrium $(x^*, y^*)$ gives $\max_x \min_y x^{\mathsf T} M y \ge \min_y x^{*\mathsf T} M y = x^{*\mathsf T} M y^* = \max_x x^{\mathsf T} M y^* \ge \min_y \max_x x^{\mathsf T} M y$, and the reverse inequality always holds. So Nash's theorem implies the [minimax theorem](/minimax-theorem/).
- **A total search problem.** Since an equilibrium always exists, "find one" is a search problem with a guaranteed answer. Its complexity is not that of a decision problem: it is complete for [PPAD](/ppad/) already in the two-player case. PPAD is defined by the parity argument on a directed graph that also proves Sperner's lemma and so Brouwer's theorem ([Nash equilibrium computation](/nash-equilibrium-computation/)).
- **Rational equilibria for two players.** With two players and rational payoffs, the equilibria form a finite union of polytopes whose vertices are rational, so an exact rational equilibrium exists and support enumeration or the Lemke and Howson method finds one. With three or more players there are games with rational payoffs whose only equilibria are irrational.
- **Extensive games.** By Kuhn's theorem, a finite game tree with perfect recall has an equilibrium in behavior strategies. This is the object that [counterfactual regret minimization](/counterfactual-regret-minimization/) approximates in [imperfect-information games](/imperfect-information-game/).
- **Stochastic games.** Fink (1964) and Takahashi (1964) extended existence to stationary equilibria of discounted [Markov games](/markov-game/) with finitely many states.

## Tightness

- **Mixed strategies are needed.** Matching pennies has no pure equilibrium. Pure equilibria exist in special classes, for example finite games of perfect information (backward induction) and potential games, but not in general.
- **Finitely many strategies are needed.** In the game where each of two players names a positive integer and the larger number wins 1, no profile of mixed strategies is an equilibrium: against any distribution, a large enough number wins with probability close to 1, and so every player can always improve. The strategy sets are not compact.
- **Continuity is needed.** For infinite games the standard generalization (Debreu, Glicksberg and Fan, 1952) needs compact convex strategy sets and payoffs that are continuous, and quasi-concave in the player's own strategy for a pure equilibrium. With a discontinuous payoff an equilibrium can fail to exist even on a compact set: if one player picks $x \in [0, 1]$ and gets $x$ for $x < 1$ but 0 for $x = 1$, there is no best choice, and no mixed strategy is a best response either.
- **The theorem is not constructive.** Brouwer's theorem has no proof that gives a fast method to find the point, and the computational results show that, under standard assumptions, no such method exists for Nash equilibria either.

## History

Nash proved the theorem in his doctoral work at Princeton. The 1950 note in PNAS, about one page long, used Kakutani's 1941 fixed point theorem, which Kakutani had stated to give a short proof of von Neumann's results on the minimax theorem. Nash's 1951 paper in the Annals of Mathematics gave the proof with Brouwer's theorem and the explicit improvement map above, defined symmetric equilibria, and applied the idea to a simple three-person poker game. Von Neumann and Morgenstern (1944) had treated games with more than two players through coalitions, and Nash's noncooperative view, in which each player acts alone, became the basis of most of later game theory. Nash shared the 1994 Nobel Memorial Prize in Economic Sciences with Harsanyi and Selten.

## References
