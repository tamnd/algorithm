---
tag: TCFWMA
kind: technique
slug: indifference-principle
name: Indifference principle
aliases:
- equalizing strategies
area: algorithmic-game-theory/computing-equilibria
level: intro
summary: In a mixed Nash equilibrium each player is indifferent among all actions in their support, which gives linear equations for the opponent's mix.
prereqs: [mixed-strategy, best-response, nash-equilibrium, bimatrix-game]
see_also: [support-enumeration, best-response-polytope, nash-equilibrium-computation, zero-sum-game-linear-programming, minimax-theorem, stackelberg-commitment-algorithm, security-game, correlated-equilibrium-linear-program]
sources:
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 3 (Bernhard von Stengel, Equilibrium computation for two-player games in strategic and extensive form), the best response condition and equilibria by support enumeration
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 3 (computing mixed equilibria of small games by indifference) and Chapter 4 (support enumeration for two-player games)
---

The indifference principle says that in a [Nash equilibrium](/nash-equilibrium/) with [mixed strategies](/mixed-strategy/), every pure strategy that a player uses with positive probability gives that player the same expected payoff, and no unused strategy gives more. If you guess which strategies are used, these equalities become linear equations in the probabilities of the other player, and solving them finds the equilibrium. The method is the basic step of [support enumeration](/support-enumeration/), which tries every guess; [Nash equilibrium computation](/nash-equilibrium-computation/) covers the problem as a whole, and [best response polytopes](/best-response-polytope/) give the same equations a geometric form.

## In plain words

If you mix between two moves and one of them pays you more on average, you should play that move all the time. So when a player mixes in an equilibrium, the moves that player mixes between must pay the same. That is a condition on the other player's mix, not on your own: the other player has to play so that you do not care which of your moves you pick. To find an equilibrium, guess which moves each player uses, then choose each player's mix so that the other player's used moves pay equally. At the end, check that the probabilities are not negative and that no unused move pays more.

## When it applies

The principle holds in every finite game, because of the best response condition: a mixed strategy is a [best response](/best-response/) if and only if every pure strategy in its support is a best response. Its payoff is the average of the payoffs of the pure strategies in the support, and an average equals the maximum only if every term equals the maximum.

As a method for finding equilibria it works best when:

- the game has two players, so that each equation is linear in the other player's probabilities;
- the game is small, or the support is known or easy to guess, for example from symmetry or after removing dominated strategies;
- the game is nondegenerate, so that a support of size $k$ for one player goes with a support of size $k$ for the other, and the equations have a unique solution.

With three or more players the equations are polynomial, because a payoff depends on the product of the other players' probabilities. The principle still holds, but solving the equations is harder, and the solutions can be irrational.

## The template

For an $m \times n$ [bimatrix game](/bimatrix-game/) $(A, B)$, where $m$ and $n$ count the pure strategies of the row and the column player:

1. **Guess the supports.** Choose sets $I \subseteq \{1, \ldots, m\}$ and $J \subseteq \{1, \ldots, n\}$ of used strategies, with $|I| = |J|$ for a nondegenerate game.
2. **Make the row player indifferent.** Find $y$ and a number $u$ with $\sum_{j \in J} A_{ij} y_j = u$ for each $i \in I$, $\sum_{j \in J} y_j = 1$ and $y_j = 0$ for $j \notin J$.
3. **Make the column player indifferent.** Find $x$ and $v$ with $\sum_{i \in I} x_i B_{ij} = v$ for each $j \in J$, $\sum_{i \in I} x_i = 1$ and $x_i = 0$ for $i \notin I$.
4. **Check the signs.** All of $x_I$ and $y_J$ must be positive. A negative value means that the guess is wrong.
5. **Check the unused strategies.** For each $i \notin I$, $\sum_j A_{ij} y_j \le u$, and for each $j \notin J$, $\sum_i x_i B_{ij} \le v$. If one of them pays more, that strategy should be used, and the guess is wrong.

If all checks pass, $(x, y)$ is a Nash equilibrium with payoffs $u$ for the row player and $v$ for the column player. The checks of steps 4 and 5 are necessary: the equations of steps 2 and 3 alone do not make an equilibrium.

## Classic examples

- **Battle of the sexes.** $A = \begin{pmatrix} 2 & 0 \\ 0 & 1 \end{pmatrix}$, $B = \begin{pmatrix} 1 & 0 \\ 0 & 2 \end{pmatrix}$, both supports full. Row indifference: $2 y_1 = y_2$, so $y = (1/3, 2/3)$ and $u = 2/3$. Column indifference: $x_1 = 2 x_2$, so $x = (2/3, 1/3)$ and $v = 2/3$. The row player mixes with weights that depend only on $B$. The other two equilibria are pure, with supports of size 1, where the equations are empty and only step 5 matters.
- **Matching pennies and rock-paper-scissors.** In matching pennies, row indifference $y_1 - y_2 = -y_1 + y_2$ gives $y = (1/2, 1/2)$. In rock-paper-scissors, row indifference over the full support gives three equations whose solution is $(1/3, 1/3, 1/3)$, and the same holds for the row player's mix by symmetry.
- **$2 \times 2$ zero-sum games without a saddle point.** For $A = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$ with no pure saddle point, both players mix, and indifference gives $x_1 = (d - c)/D$, $y_1 = (d - b)/D$ and the value $(a d - b c)/D$, with $D = a - b - c + d$. For $A = \begin{pmatrix} 3 & -1 \\ -2 & 1 \end{pmatrix}$: $D = 7$, $x = (3/7, 4/7)$, $y = (2/7, 5/7)$ and the value is $1/7$. Here the row player's mix is the equalizing strategy, which makes both columns pay $1/7$, and in a [zero-sum game](/zero-sum-game/) it is also an optimal strategy by the [minimax theorem](/minimax-theorem/).
- **A $3 \times 2$ game with a wrong guess.** $A = \begin{pmatrix} 3 & 3 \\ 2 & 5 \\ 0 & 6 \end{pmatrix}$, $B = \begin{pmatrix} 3 & 2 \\ 2 & 6 \\ 3 & 1 \end{pmatrix}$. With $I = \{1, 2\}$, $J = \{1, 2\}$: column indifference $3 x_1 + 2 x_2 = 2 x_1 + 6 x_2$ gives $x = (4/5, 1/5, 0)$, and row indifference $3 y_1 + 3 y_2 = 2 y_1 + 5 y_2$ gives $y = (2/3, 1/3)$ with $u = 3$. Row 3 pays $2 \le 3$, so this is an equilibrium. With $I = \{1, 3\}$, column indifference $3 x_1 + 3 x_3 = 2 x_1 + x_3$ gives $x_1 = -2 x_3$, which is negative, so no equilibrium has this support.
- **Prisoner's dilemma.** $A = \begin{pmatrix} 3 & 0 \\ 5 & 1 \end{pmatrix}$ (cooperate, defect). Row indifference $3 y_1 = 5 y_1 + y_2$ has no solution with $y \ge 0$, $y \ne 0$, because defect is strictly better against every mix. The only equilibrium is pure.
- **All-pay auction.** Two bidders both value a prize at 1, both pay their bids, and the higher bid wins. If one bidder bids uniformly on $[0, 1]$, a bid $b$ of the other wins with probability $b$ and pays $b$, so every bid in $[0, 1]$ gives payoff $b - b = 0$. Each bidder is indifferent over the whole interval, and both bidding uniformly is an equilibrium. The principle works the same way with a continuum of strategies.

## Variations

- **Square nonsingular games with full support.** If both players use all strategies of an $n \times n$ zero-sum game with a nonsingular matrix $A$, indifference gives $x^{\mathsf T} A = u \mathbf 1^{\mathsf T}$, so $x^{\mathsf T} = \mathbf 1^{\mathsf T} A^{-1} / (\mathbf 1^{\mathsf T} A^{-1} \mathbf 1)$ and the value is $1 / (\mathbf 1^{\mathsf T} A^{-1} \mathbf 1)$, whenever $\mathbf 1^{\mathsf T} A^{-1} \mathbf 1 \ne 0$.
- **Support enumeration.** Run the template for every pair of supports of equal size. In a nondegenerate game this lists all equilibria; see [support enumeration](/support-enumeration/). Ordering the guesses by size and balance finds one equilibrium fast on many games.
- **Linear programs for zero-sum games.** The [linear program for zero-sum games](/zero-sum-game-linear-programming/) does not need a guess. Its constraints are inequalities "every column pays at least $v$", and the columns in the support of the opponent's optimal strategy are the ones that hold with equality, by complementary slackness.
- **Commitment and security games.** A leader who commits to a mixed strategy often makes the follower indifferent between several responses and lets the follower break the tie in the leader's favor. The [Stackelberg commitment algorithm](/stackelberg-commitment-algorithm/) and [security games](/security-game/) use this.
- **Correlated equilibrium.** The incentive constraints of a [correlated equilibrium](/correlated-equilibrium-linear-program/) are inequalities on a joint distribution, one for each recommended and each deviating action, and are linear for any number of players.
- **Many players.** For three or more players the indifference equations are multilinear in the probabilities of the others.

## Pitfalls

- **Whose mix is it?** Player 1's indifference fixes player 2's probabilities. A common error is to solve "player 1 is indifferent" for player 1's own probabilities.
- **Indifference is not enough.** The equations say only that the used strategies pay the same. An unused strategy can pay more, as the next exercise shows, so step 5 is needed.
- **Negative probabilities.** A solution with a negative entry means that the guessed support is wrong. It is not an equilibrium with a sign changed.
- **Degenerate games.** If a mixed strategy with $k$ strategies in its support has more than $k$ best responses, the supports can have different sizes and the equations can have a whole segment of solutions. The template with $|I| = |J|$ then misses some equilibria.
- **Pure equilibria.** For supports of size 1 the equations are empty and the method is only the best response check of step 5.
- **Why mix exactly so?** At a mixed equilibrium a player has no strict reason to keep the equilibrium probabilities, because all used strategies pay the same. The mix is pinned down only by the need to keep the other player indifferent.

## Exercises

1. In the game $A = \begin{pmatrix} 4 & 0 \\ 0 & 4 \\ 3 & 3 \end{pmatrix}$, $B = \begin{pmatrix} 0 & 1 \\ 1 & 0 \\ 0 & 0 \end{pmatrix}$, apply the template with $I = \{1, 2\}$ and $J = \{1, 2\}$. Show that $x = (1/2, 1/2, 0)$ and $y = (1/2, 1/2)$ make both players indifferent, and that row 3 pays $3 > 2$, so this is not an equilibrium. Find the equilibria of the game.
2. Find all equilibria of the game of chicken with $A = \begin{pmatrix} 0 & -1 \\ 1 & -10 \end{pmatrix}$ and $B = A^{\mathsf T}$. Show that in the mixed one each player swerves with probability $9/10$.
3. Derive the $2 \times 2$ zero-sum formula of the examples from the template, and show that the condition "no saddle point" is what makes $x_1$ and $y_1$ lie strictly between 0 and 1.
4. Show that in a nondegenerate game a solution of the template with $|I| \ne |J|$ cannot exist, by counting the labels of the [best response polytopes](/best-response-polytope/).
5. In the all-pay auction, show that no pure strategy profile is an equilibrium.

## References
