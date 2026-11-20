---
tag: F0ETC8
kind: theorem
slug: rosenthal-potential-theorem
name: "Rosenthal's theorem"
aliases:
- Rosenthal potential function
area: algorithmic-game-theory/inefficiency-of-equilibria
level: core
summary: Every atomic congestion game is an exact potential game with Rosenthal's potential, so it has a pure Nash equilibrium and every improvement path ends.
prereqs: [atomic-congestion-game, potential-game]
see_also: [beckmann-potential, finite-improvement-property, best-response-dynamics, pls-completeness-of-congestion-games, symmetric-network-congestion-min-cost-flow, harmonic-price-of-stability, price-of-stability, pure-nash-equilibrium]
sources:
  - paper: doi:10.1007/BF01737559
    title: "Robert W. Rosenthal, A class of games possessing pure-strategy Nash equilibria, International Journal of Game Theory 2 (1973), 65-67"
    locator: the class of congestion games and the proof by a potential that each game in it has a pure equilibrium
  - paper: doi:10.1006/game.1996.0044
    title: "Dov Monderer and Lloyd S. Shapley, Potential games, Games and Economic Behavior 14(1) (1996), 124-143"
    locator: the term potential, the finite improvement property, and the converse that every finite exact potential game is isomorphic to a congestion game
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 13 (potential games, Rosenthal's potential and the existence of pure equilibria)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 19 (Eva Tardos and Tom Wexler, Network formation games and the potential function method)
---

Rosenthal's theorem says that an atomic congestion game always has a pure Nash equilibrium, and it proves this with one function, Rosenthal's potential, that changes by exactly the cost change of any player who moves alone. It is the theorem behind the [potential game](/potential-game/) definition, and it is the atomic counterpart of the [Beckmann potential](/beckmann-potential/): Beckmann's potential is an integral over a continuum of tiny users and its minimizers are Wardrop flows, while Rosenthal's is a sum over whole players and its minimizers are pure equilibria of a finite game.

## Statement

Let a [congestion game](/atomic-congestion-game/) have players $1, \ldots, n$, a finite set $E$ of resources, and for each player $i$ a finite set $S_i$ of subsets of $E$. Each resource has a cost function $c_e : \{1, \ldots, n\} \to \mathbb{R}$, with no assumption of sign or monotonicity. For a profile $s = (s_1, \ldots, s_n) \in S = S_1 \times \cdots \times S_n$, the load of $e$ is $x_e(s) = |\{i : e \in s_i\}|$ and player $i$ pays $c_i(s) = \sum_{e \in s_i} c_e(x_e(s))$. Define

$$\Phi(s) = \sum_{e \in E} \sum_{j=1}^{x_e(s)} c_e(j).$$

**Theorem (Rosenthal 1973).** For every profile $s$, every player $i$ and every $s_i' \in S_i$,

$$\Phi(s_i', s_{-i}) - \Phi(s) = c_i(s_i', s_{-i}) - c_i(s).$$

So $\Phi$ is an exact potential, and:

1. every profile that minimizes $\Phi$ is a pure Nash equilibrium, so a pure equilibrium exists;
2. a profile is a pure Nash equilibrium if and only if no unilateral deviation lowers $\Phi$;
3. every path of strict unilateral improvements is finite, and it ends at a pure equilibrium.

The game is finite and the equilibrium notion is pure Nash equilibrium. The theorem needs no mixed strategies, and each resource must charge all its users the same amount, which depends only on their number.

## In plain words

Players share resources, and a resource gets more or less costly with the number of its users. Think of the users of each resource as arriving one after another, the first paying the price for one user, the second the price for two, and so on, and add up all these prices over all resources. When one player changes its choice, this total changes by exactly the amount that player saves or loses. So a player who moves to save money always lowers the total. The total cannot fall forever, because there are only finitely many choices, so the moves stop, and where they stop nobody wants to move.

## Proof

Fix $s$, a player $i$ and $s_i' \in S_i$, and let $t = (s_i', s_{-i})$. The loads under $s$ and $t$ differ only on the resources in exactly one of $s_i$ and $s_i'$, so split $E$ into four parts.

- $e \in s_i' \setminus s_i$: the load rises from $x_e(s)$ to $x_e(s) + 1 = x_e(t)$. The inner sum of $\Phi$ gains the term $c_e(x_e(t))$, which is what player $i$ pays for $e$ under $t$; it paid nothing for $e$ under $s$.
- $e \in s_i \setminus s_i'$: the load falls from $x_e(s)$ to $x_e(s) - 1$. The inner sum loses the term $c_e(x_e(s))$, which is what player $i$ paid for $e$ under $s$; it pays nothing for $e$ under $t$.
- $e \in s_i \cap s_i'$: the load is the same, and player $i$ pays $c_e(x_e(s))$ for $e$ in both profiles.
- $e \notin s_i \cup s_i'$: the load is the same, and player $i$ does not use $e$.

Adding the four parts,

$$\Phi(t) - \Phi(s) = \sum_{e \in s_i' \setminus s_i} c_e(x_e(t)) - \sum_{e \in s_i \setminus s_i'} c_e(x_e(s)) = c_i(t) - c_i(s),$$

because the terms of $c_i(t)$ and $c_i(s)$ over $s_i \cap s_i'$ cancel. This is the identity.

Claim 2 follows: a deviation lowers the deviator's cost if and only if it lowers $\Phi$ by the same amount, so $s$ is an equilibrium exactly when no deviation lowers $\Phi$. Claim 1 follows from claim 2, because a global minimizer of $\Phi$ exists in the finite set $S$ and no deviation lowers $\Phi$ there. For claim 3, $\Phi$ strictly falls along an improvement path, so no profile repeats, and a path in the finite set $S$ has fewer than $|S|$ steps. Its last profile has no improving deviation, so it is an equilibrium. $\blacksquare$

### Example

Take resources $e$, $f$, $g$ with $c_e(1) = 1$, $c_e(2) = 4$, $c_f(1) = 2$, $c_f(2) = 3$ and $c_g = 3$ for any load. Player 1 picks $\{e, f\}$ or $\{g\}$; player 2 picks $\{e\}$ or $\{f, g\}$.

| player 1 | player 2 | loads $x_e, x_f, x_g$ | costs $c_1, c_2$ | $\Phi$ |
|---|---|---|---|---|
| $\{e, f\}$ | $\{e\}$ | 2, 1, 0 | 6, 4 | $1 + 4 + 2 = 7$ |
| $\{e, f\}$ | $\{f, g\}$ | 1, 2, 1 | 4, 6 | $1 + 2 + 3 + 3 = 9$ |
| $\{g\}$ | $\{e\}$ | 1, 0, 1 | 3, 1 | $1 + 3 = 4$ |
| $\{g\}$ | $\{f, g\}$ | 0, 1, 2 | 3, 5 | $2 + 3 + 3 = 8$ |

Every deviation obeys the identity. From the last row, player 1 moves to $\{e, f\}$: it now shares $f$ with player 2, the load of $f$ goes from 1 to 2 and adds $c_f(2) = 3$ to $\Phi$, $e$ adds $c_e(1) = 1$, and $g$ loses $c_g(2) = 3$; the net change $+1$ is the change of player 1's cost, from 3 to 4. The minimizer of $\Phi$, ($\{g\}$, $\{e\}$), is the only pure equilibrium.

## Consequences

- **Best-response dynamics ends.** Every congestion game has the [finite improvement property](/finite-improvement-property/), so [best-response dynamics](/best-response-dynamics/) and any other improvement dynamics stop at an equilibrium. With integer costs, the number of steps is at most $\Phi(s^0) - \min \Phi$.
- **Computing an equilibrium is a local search.** A pure equilibrium is a local minimum of $\Phi$ for the neighbourhood of unilateral deviations, so the search problem is in [PLS](/pls/). It is PLS-complete ([PLS-completeness of congestion games](/pls-completeness-of-congestion-games/)). For symmetric network games a global minimizer of $\Phi$ is a [min-cost flow](/symmetric-network-congestion-min-cost-flow/).
- **The potential function method.** If $\Phi(s) \le C(s) \le A\, \Phi(s)$ for the social cost $C$ and every $s$, a minimizer of $\Phi$ costs at most $A$ times the optimum, so the [price of stability](/price-of-stability/) is at most $A$. For affine costs $c_e(x) = a_e x + b_e \ge 0$ this gives $A = 2$. For the Shapley cost sharing $c_e(x) = c_e / x$ it gives the [harmonic bound](/harmonic-price-of-stability/) $H(n)$.
- **The converse.** Monderer and Shapley proved that every finite exact potential game is isomorphic to a congestion game. So Rosenthal's class is, up to renaming, the class of all finite exact potential games.

## Tightness

- **Weights break it.** If player $i$ has a weight $w_i$ and a resource cost depends on the total weight of its users, the identity fails, and some such games have no pure equilibrium (Libman and Orda 2001; Goemans, Mirrokni and Vetta 2005). With affine costs a weighted potential still exists (Fotakis, Kontogiannis and Spirakis 2005). Harks and Klimm (Mathematics of Operations Research, 2012) characterized the classes of continuous cost functions that guarantee a pure equilibrium in every weighted congestion game: in essence affine costs and certain exponential costs.
- **Player-specific costs break it.** If $c_e$ depends on the player, the potential is gone. Milchtaich (1996) showed that pure equilibria still exist when every strategy is a single resource, but improvement paths can cycle.
- **The minimizer need not be good.** $\Phi$ is not the social cost. With two players, link 1 of cost 2 and link 2 of cost $c(x) = x$, both "one player on each link" (cost 3) and "both on link 2" (cost 4) minimize $\Phi = 3$; the potential cannot tell them apart.
- **Finiteness matters.** The existence part needs finitely many profiles, or compactness and continuity. The identity itself holds for any strategy sets.
- **No bound on time.** The proof gives no polynomial bound on the number of improvement steps, and none exists in general: some congestion games have exponentially long improvement paths from some starting profiles.

## History

Robert Rosenthal introduced congestion games and the potential in a three-page paper in 1973. The name "potential game" and the general theory came from Monderer and Shapley in 1996, who also proved the converse. Fabrikant, Papadimitriou and Talwar turned the proof into a question about computation in 2004, showing that the local search on $\Phi$ is PLS-complete. Anshelevich and coauthors used the potential to bound the price of stability of network design in 2004, and the potential function method is now a standard tool for bounding the price of stability.

## References
