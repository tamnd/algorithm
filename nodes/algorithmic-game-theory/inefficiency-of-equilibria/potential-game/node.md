---
tag: 9E88DE
kind: definition
slug: potential-game
name: Potential game
aliases:
- exact potential game
- Monderer-Shapley potential game
area: algorithmic-game-theory/inefficiency-of-equilibria
level: core
summary: A game with a function on profiles whose change under any unilateral deviation equals the change in the deviator's cost.
prereqs: [pure-nash-equilibrium, normal-form-game]
see_also: [finite-improvement-property, rosenthal-potential-theorem, atomic-congestion-game, best-response-dynamics, price-of-stability, beckmann-potential, pls-completeness-of-congestion-games, smoothness-framework]
sources:
  - paper: doi:10.1006/game.1996.0044
    title: "Dov Monderer and Lloyd S. Shapley, Potential games, Games and Economic Behavior 14(1) (1996), 124-143"
    locator: Section 2 (exact, weighted, ordinal and generalized ordinal potentials, the finite improvement property, the cycle test and the uniqueness of the potential) and the isomorphism between finite potential games and congestion games
  - paper: doi:10.1007/BF01737559
    title: "Robert W. Rosenthal, A class of games possessing pure-strategy Nash equilibria, International Journal of Game Theory 2 (1973), 65-67"
    locator: congestion games and the potential function that proves they have pure equilibria
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 13 (potential games and the existence of pure Nash equilibria) and Lecture 16 (best-response dynamics)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 19 (Eva Tardos and Tom Wexler, Network formation games and the potential function method)
---

A potential game is a game with one function on the strategy profiles that tracks the cost of whichever player moves: when one player changes strategy, the function changes by exactly the change in that player's cost. It is the property, not a result. The [finite improvement property](/finite-improvement-property/) is a weaker property of the dynamics that every finite potential game has. [Rosenthal's theorem](/rosenthal-potential-theorem/) is the result that every [atomic congestion game](/atomic-congestion-game/) is a potential game, and congestion games are the main example: Monderer and Shapley showed that every finite exact potential game is isomorphic to one.

## Definition

A game in normal form has players $1, \ldots, n$, strategy sets $S_1, \ldots, S_n$, and costs $c_i : S \to \mathbb{R}$ on the profiles $S = S_1 \times \cdots \times S_n$. Each player minimizes its own cost. For a profile $s$, a player $i$ and a strategy $s_i' \in S_i$, the profile $(s_i', s_{-i})$ is a unilateral deviation of $i$.

A function $\Phi : S \to \mathbb{R}$ is an **exact potential** of the game if for every profile $s$, every player $i$ and every $s_i' \in S_i$,

$$\Phi(s_i', s_{-i}) - \Phi(s) = c_i(s_i', s_{-i}) - c_i(s).$$

The game is an (exact) **potential game** if it has an exact potential. Monderer and Shapley also defined three weaker forms. In each, the condition is on every unilateral deviation from $s$ to $s' = (s_i', s_{-i})$:

- **Weighted potential**, with weights $w_i > 0$: $c_i(s') - c_i(s) = w_i (\Phi(s') - \Phi(s))$.
- **Ordinal potential**: $c_i(s') < c_i(s)$ if and only if $\Phi(s') < \Phi(s)$.
- **Generalized ordinal potential**: $c_i(s') < c_i(s)$ implies $\Phi(s') < \Phi(s)$.

Each form implies the next. Monderer and Shapley wrote payoffs that players maximize; with costs the signs flip, and players move to lower values of $\Phi$.

The definition has four direct consequences, each with a short proof.

1. **Uniqueness.** Any two exact potentials differ by a constant. Two profiles are joined by a chain of unilateral deviations, one coordinate at a time, and along the chain the change of $\Phi$ is fixed by the costs.
2. **Equilibria are local minima.** Call $s$ a local minimum of $\Phi$ if no unilateral deviation lowers $\Phi$. With an ordinal potential, $s$ is a [pure Nash equilibrium](/pure-nash-equilibrium/) if and only if it is a local minimum, because a deviation lowers the deviator's cost exactly when it lowers $\Phi$. With a generalized ordinal potential every local minimum is an equilibrium. So a finite game with a generalized ordinal potential has a pure equilibrium: a global minimum of $\Phi$.
3. **Coordination plus dummy.** A game has an exact potential $\Phi$ if and only if $c_i = \Phi + d_i$ for functions $d_i$ that do not depend on $s_i$. If $\Phi$ is an exact potential, set $d_i = c_i - \Phi$; a deviation of $i$ changes $c_i$ and $\Phi$ by the same amount, so it does not change $d_i$. The converse is immediate. So every potential game is a game of identical costs $\Phi$ plus, for each player, a cost that the player cannot influence.
4. **The cycle test.** In a finite game, an exact potential exists if and only if, for every two players $i \ne j$, every profile $s$ and every $a \ne s_i$, $b \ne s_j$, the four deviations $s \to (a, s_{-i}) \to (a, b, s_{-ij}) \to (b, s_{-j}) \to s$, made by $i$, $j$, $i$, $j$ in turn, have deviators' cost changes that sum to zero.

Proof of the cycle test. If $\Phi$ exists, the four changes are the four changes of $\Phi$ around a closed path, which sum to zero. For the converse, number the strategies of each player from 0, let $s^0 = (0, \ldots, 0)$, and define $\Phi(s)$ as the sum of the deviators' cost changes along the canonical path from $s^0$ to $s$ that sets coordinate 1 to $s_1$, then coordinate 2 to $s_2$, and so on, skipping steps that change nothing. Two observations hold for any path of unilateral deviations. Swapping two adjacent steps of different players, both of which change something, does not change the sum, by the 4-cycle condition. Merging two adjacent steps of the same player, $a \to b \to c$, into one step $a \to c$ does not change the sum, because both give $c_i(\ldots c \ldots) - c_i(\ldots a \ldots)$, and a merged step $a \to a$ contributes 0 and can be dropped. Now let $t = (t_i, s_{-i})$ with $t_i \ne s_i$. The canonical path to $s$ followed by the step $s \to t$ goes from $s^0$ to $t$. Swap the last step back past the steps of players $n, n - 1, \ldots, i + 1$, then merge it with the step of player $i$. The result is the canonical path to $t$, with the same sum. So $\Phi(t) = \Phi(s) + c_i(t) - c_i(s)$, and $\Phi$ is an exact potential. $\square$

### Testing a finite game

The proof of uniqueness gives a direct test: fix the value at one profile, spread values along unilateral deviations, and check every deviation.

```pseudo id=main
EXACT-POTENTIAL(S_1, ..., S_n, c)
L1  Φ(s0) ← 0 for the profile s0 = (0, ..., 0); Q ← [s0]
L2  while Q is not empty: take a profile s from Q
L3      for each player i and each s_i' ≠ s_i, with t = (s_i', s_-i):
L4          if Φ(t) is not set: Φ(t) ← Φ(s) + c_i(t) - c_i(s); put t in Q
L5          else if Φ(t) ≠ Φ(s) + c_i(t) - c_i(s): return "no exact potential"
L6  return Φ
```

The search takes $O(|S| \sum_i |S_i|)$ steps, which is linear in the size of the cost table times $\sum_i |S_i|$. The file proofs/correctness.md proves that it returns a potential exactly when one exists. With exact rational costs no tolerance is needed.

## Examples and non-examples

**The prisoner's dilemma.** In cost form, with C to cooperate and D to defect, the costs (player 1, player 2) are $(1, 1)$ at (C, C), $(3, 0)$ at (C, D), $(0, 3)$ at (D, C) and $(2, 2)$ at (D, D). The function $\Phi(\text{C}, \text{C}) = 2$, $\Phi(\text{C}, \text{D}) = \Phi(\text{D}, \text{C}) = 1$, $\Phi(\text{D}, \text{D}) = 0$ is an exact potential: each change from C to D lowers the deviator's cost by 1 and lowers $\Phi$ by 1. Its minimum (D, D) is the only pure equilibrium, although (C, C) has a lower total cost, so the potential is not the social cost.

**Congestion games.** In an [atomic congestion game](/atomic-congestion-game/), $\Phi(s) = \sum_e \sum_{j=1}^{x_e(s)} c_e(j)$, where $x_e(s)$ is the number of players on resource $e$, is an exact potential. This is [Rosenthal's theorem](/rosenthal-potential-theorem/). The routing games of [selfish routing](/selfish-routing-model/) with finitely many players and the [Shapley network design game](/shapley-network-design-game/) are special cases.

**Identical costs.** If all players have the same cost function $c_i = F$, then $F$ is an exact potential. Coordination games are of this type.

**An ordinal potential that is not exact.** Two players choose A or B. Player 1 pays 0 at (A, A), 1 at (B, A), 0 at (A, B) and 2 at (B, B). Player 2 pays 0 at (A, A), 1 at (A, B), 0 at (B, A) and 1 at (B, B). Around the cycle (A, A), (B, A), (B, B), (A, B), (A, A), the deviators' cost changes are $1$, $1$, $-2$ and $-1$, which sum to $-1$, so by the cycle test there is no exact potential. But each player pays more when it plays B, so the number of players who play B is an ordinal potential, and (A, A) is the unique pure equilibrium.

**Matching pennies.** Player 1 pays 0 when the two coins match and 1 otherwise, and player 2 pays the opposite. From every profile one player gains by switching, so the four profiles form a cycle of strict improvements, and there is no pure equilibrium. By consequence 2, the game has no generalized ordinal potential.

**An infinite non-example.** One player picks $s \in (0, 1]$ and pays $s$. Then $\Phi(s) = s$ is an exact potential, but no strategy is best and there is no equilibrium. The existence of a pure equilibrium needs a finite game, or a compact strategy space with a continuous potential.

**Weighted congestion games.** If players have weights and the cost of a resource depends on the total weight on it, the game can have no pure equilibrium and then has no potential (Libman and Orda 2001; Goemans, Mirrokni and Vetta 2005). With affine costs it has a weighted potential (Fotakis, Kontogiannis and Spirakis 2005).

## Related definitions

- [Finite improvement property](/finite-improvement-property/): every path of strict unilateral improvements is finite. A finite game has it if and only if it has a generalized ordinal potential (Monderer and Shapley 1996).
- [Pure Nash equilibrium](/pure-nash-equilibrium/): in a potential game, the local minima of the potential, as shown above.
- [Best-response dynamics](/best-response-dynamics/): in a finite potential game it stops at an equilibrium, because $\Phi$ falls at each step. The number of steps can be exponential: computing a pure equilibrium of a congestion game is [PLS-complete](/pls-completeness-of-congestion-games/).
- [Beckmann potential](/beckmann-potential/): the potential of nonatomic selfish routing, an integral in place of a sum; its minimizers are the Wardrop equilibria.
- [Price of stability](/price-of-stability/): the potential function method bounds it. If $\Phi(s) \le C(s) \le A\, \Phi(s)$ for the social cost $C$ and every profile $s$, then a global minimizer $s^*$ of $\Phi$ has $C(s^*) \le A\, \Phi(s^*) \le A\, \Phi(o) \le A\, C(o)$ for an optimum $o$, so the price of stability is at most $A$. The [harmonic bound](/harmonic-price-of-stability/) for network design comes from this argument.
- Fictitious play: Monderer and Shapley also showed that fictitious play converges in beliefs in games with identical interests (Journal of Economic Theory 68 (1996), 258-265), and so in weighted potential games, which have the same best responses.

## References
