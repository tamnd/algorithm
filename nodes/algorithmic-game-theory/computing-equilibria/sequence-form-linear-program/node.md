---
tag: 7V6BC9
kind: algorithm
slug: sequence-form-linear-program
name: Sequence-form linear program
aliases:
- sequence-form LP for zero-sum games
area: algorithmic-game-theory/computing-equilibria
level: advanced
summary: Solves a two-player zero-sum extensive-form game with perfect recall by a linear program of size linear in the game tree.
solves: [nash-equilibrium-computation]
model: real-ram
complexity:
  vars: {N: the number of nodes of the game tree, L: the bit length of the payoffs and chance probabilities}
  time: {worst: "poly(N, L)"}
  space: {extra: O(N^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1996
  people: [Daphne Koller, Nimrod Megiddo, Bernhard von Stengel]
  note: Koller, Megiddo and von Stengel, and von Stengel in a companion paper, gave the sequence form and its LP in 1996; Romanovskii had a related reduction for zero-sum games with perfect recall in 1962.
prereqs: [sequence-form, zero-sum-game-linear-programming, lp-duality]
see_also: [sequence-form, zero-sum-game-linear-programming, counterfactual-regret-minimization, extensive-form-game, perfect-recall, kuhn-theorem-behavioral-strategies, imperfect-information-game, lemke-algorithm]
sources:
  - paper: doi:10.1006/game.1996.0051
    title: "Daphne Koller, Nimrod Megiddo and Bernhard von Stengel, Efficient computation of equilibria for extensive two-person games, Games and Economic Behavior 14(2) (1996), 247-259"
    locator: the LP for zero-sum games in sequence form and the LCP for general two-person games
  - paper: "Bernhard von Stengel, Efficient computation of behavior strategies, Games and Economic Behavior 14(2) (1996), 220-246"
    title: Efficient computation of behavior strategies
    locator: the sequence form, the LP of a zero-sum game with perfect recall, and the behavior strategies read from its solution
  - paper: "I. V. Romanovskii, Reduction of a game with complete memory to a matrix game, Soviet Mathematics 3 (1962), 678-681"
    title: Reduction of a game with complete memory to a matrix game
    locator: an earlier reduction of zero-sum games with perfect recall to a linear program of small size
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Section 5.2.3 (Computing equilibria, the sequence form)
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 3 (Bernhard von Stengel, Equilibrium computation for two-player games in strategic and extensive form), the sections on the sequence form
---

The sequence-form linear program finds the value and optimal strategies of a two-player zero-sum game in extensive form with imperfect information and [perfect recall](/perfect-recall/), such as a small poker game. It writes the strategies of both players in the [sequence form](/sequence-form/), where a strategy is a vector with one entry per sequence of own moves and a few linear equations, and then solves one linear program whose size is linear in the game tree. The sequence form itself is a representation and has its own page; this page is the algorithm. It replaces the [LP for matrix games](/zero-sum-game-linear-programming/), which on the normal form of a game tree can be exponentially large, and it differs from [counterfactual regret minimization](/counterfactual-regret-minimization/), which approximates the same equilibrium by repeated play.

## In plain words

A strategy in a card game says what to do in every situation you can tell apart. Listing whole strategies gives far too many. Instead, keep for each line of your own moves the chance that you play all of it. These numbers must add up the right way: the chance of a line equals the sum of the chances of its continuations. The expected payoff is then a simple sum over the leaves of the tree. For a fixed plan of the first player, the best reply of the second player is a small linear program, and its dual can be merged into the first player's problem. The result is one linear program. Its solution gives the first player's plan, and its dual prices give the second player's plan.

## The problem

Input: a finite game tree with two players and chance moves, information sets with perfect recall, and payoffs $u(\ell)$ to player 1 at the leaves; player 2 gets $-u(\ell)$. Output: the value $v$ of the game and realization plans $x$ and $y$, so that $x$ guarantees player 1 at least $v$ against every strategy of player 2 and $y$ holds player 1 to at most $v$ against every strategy of player 1.

In the sequence form, player 1's plans are $X = \{x : E x = e,\ x \ge 0\}$ and player 2's are $Y = \{y : F y = f,\ y \ge 0\}$, where $e = (1, 0, \ldots, 0)$ and $f = (1, 0, \ldots, 0)$; the expected payoff is $x^{\mathsf T} A y$ with the sequence payoff matrix $A$. The problem is

$$v = \max_{x \in X} \min_{y \in Y} x^{\mathsf T} A y = \min_{y \in Y} \max_{x \in X} x^{\mathsf T} A y .$$

For a fixed $x$, the inner problem $\min \{(A^{\mathsf T} x)^{\mathsf T} y : F y = f,\ y \ge 0\}$ is a linear program, and by [LP duality](/lp-duality/) its value is $\max \{f^{\mathsf T} q : F^{\mathsf T} q \le A^{\mathsf T} x\}$ with $q$ free. Putting the two maximizations together gives one LP.

## The algorithm

```pseudo id=main
SEQUENCE-FORM-LP(T)                  ▷ T: a two-player zero-sum game tree with perfect recall
L1  walk T; list the sequences S1, S2 and the parent sequence σ_h of each information set h
                                     ▷ reject T if two nodes of one h have different sequences
L2  at each leaf ℓ: A[σ1(ℓ)][σ2(ℓ)] ← A[σ1(ℓ)][σ2(ℓ)] + c(ℓ) · u(ℓ)   ▷ c(ℓ): chance probability
L3  build E, e for player 1 and F, f for player 2  ▷ one row for ∅ and one per information set
L4  constraints: F^T q - A^T x ≤ 0 (one row per sequence of player 2), E x = e, x ≥ 0, q free
L5  maximize q_∅ subject to L4               ▷ q_∅: the entry of q for the row of ∅ in F
L6  x ← the optimal x; y ← the dual prices of the rows of L4
    return (q_∅, x, y)
```

Line L4 has one inequality for each sequence $\tau$ of player 2. On its left, $\tau = \emptyset$ gives $q_\emptyset + \sum q_{h'}$, and a sequence that ends at an information set $h$ gives $-q_h + \sum q_{h'}$, where the sums run over the information sets $h'$ of player 2 whose parent sequence is $\tau$. On its right is $(A^{\mathsf T} x)_\tau$, the payoff that player 1 gets, weighted by chance and by $x$, from the leaves that player 2 reaches with $\tau$ and no further own move. So $-q_h$ is a lower bound on what player 1 gets below $h$, whatever player 2 does there, and the LP pushes these bounds up from the leaves to the root.

The dual of the LP of line L4 is player 2's LP: minimize $p_\emptyset$ subject to $E^{\mathsf T} p - A y \ge 0$, $F y = f$, $y \ge 0$, $p$ free. So the dual prices of the inequality rows, which are $y$, form an optimal realization plan of player 2. A behavior strategy is read from $x$ by $\beta(h, a) = x(\sigma_h a) / x(\sigma_h)$ where $x(\sigma_h) > 0$.

## Example

Player 1 plays $L$, which ends the game with payoff 1, or $R$. After $R$, player 2 picks $a$ or $b$, and then player 1 picks $c$ or $d$ without seeing that choice. The payoffs to player 1 are 3 after $R a c$, 0 after $R a d$ and $R b c$, and 2 after $R b d$. The sequences are $S_1 = (\emptyset, L, R, Rc, Rd)$ and $S_2 = (\emptyset, a, b)$, and the nonzero entries of $A$ are $A(L, \emptyset) = 1$, $A(Rc, a) = 3$ and $A(Rd, b) = 2$.

Player 2 has one information set, $p_2$, so $q = (q_\emptyset, q_{p_2})$, and the three rows of line L4 are

| sequence of player 2 | row of L4 |
|---|---|
| $\emptyset$ | $q_\emptyset + q_{p_2} \le x(L)$ |
| $a$ | $-q_{p_2} \le 3\, x(Rc)$ |
| $b$ | $-q_{p_2} \le 2\, x(Rd)$ |

with $x(\emptyset) = 1$, $x(L) + x(R) = 1$ and $x(Rc) + x(Rd) = x(R)$. The best choice of $q$ gives $q_\emptyset = x(L) + \min(3 x(Rc), 2 x(Rd))$: player 2 picks the better of $a$ and $b$ against player 1's plan. The maximum is at $x(L) = 0$ and $3 x(Rc) = 2 x(Rd)$, so

$$x = (1, 0, 1, 2/5, 3/5), \qquad v = q_\emptyset = 6/5 .$$

The dual prices of the three rows are $y = (1, 2/5, 3/5)$: player 2 plays $a$ with probability $2/5$. Against it, $R$ then $c$ gives $3 \cdot 2/5 = 6/5$, $R$ then $d$ gives $2 \cdot 3/5 = 6/5$, and $L$ gives $1 < 6/5$, so player 1 cannot get more than $6/5$. The game has 4 pure strategies for player 1, while the LP has 5 variables for player 1.

On Kuhn poker (three cards, one bet), each player has 6 information sets and 13 sequences, and the LP gives the value $-1/18$ for the first player.

## Correctness

By LP duality, for each fixed $x \in X$ the maximum of $q_\emptyset$ over the $q$ with $F^{\mathsf T} q \le A^{\mathsf T} x$ is $\min_{y \in Y} x^{\mathsf T} A y$, because $Y$ is a nonempty polytope and the inner LP has an optimum. So the LP of lines L4 and L5 computes $\max_{x \in X} \min_{y \in Y} x^{\mathsf T} A y$, and its optimal $x$ is a maximin realization plan. Its dual is the same construction for player 2, and strong duality makes the two values equal. Under perfect recall every point of $X$ and of $Y$ is the realization plan of a behavior strategy, and the payoff of a pair of strategies depends only on their realization plans, so the LP optimum is the value of the game and $x$ and $y$ give optimal strategies. The proof file has the details.

## Complexity

The LP has $|S_1| + 2 (|H_2| + 1)$ variables, counting $q$ split into two nonnegative parts, and $|S_2| + |H_1| + 1$ constraints, where $|S_i| \le N$ and $|H_i| \le N$ for a tree with $N$ nodes. The matrix $A$ has at most one nonzero entry per leaf. Building it takes $O(N)$ time plus the dense storage, $O(N^2)$ in the code. With a polynomial-time LP method ([ellipsoid](/ellipsoid-method/) or [interior point](/interior-point-method/)), the total time is polynomial in $N$ and the bit length $L$ of the numbers. The code uses the [simplex method](/simplex-method/) with exact rational arithmetic, which is fast on small games but has no polynomial bound.

The normal form of the same tree can have a number of pure strategies exponential in $N$, so the LP for matrix games on it can be exponentially larger.

## Properties

- **Exact.** With rational payoffs and chance probabilities, the value and the plans are rational, and the code computes them exactly.
- **Both players at once.** The primal gives player 1's plan and the dual gives player 2's.
- **Linear size.** The LP has size linear in the tree, and the payoff matrix is sparse.
- **Needs perfect recall.** Without it, sequences do not identify information sets, and finding optimal strategies of zero-sum games with imperfect recall is NP-hard in general (Koller and Megiddo).

## Variants and improvements

- **General-sum games.** For two-player games that are not zero-sum, the equilibrium conditions in sequence form are a [linear complementarity problem](/linear-complementarity-problem/) of linear size, solved by a variant of [Lemke's algorithm](/lemke-algorithm/) (Koller, Megiddo and von Stengel).
- **Large games.** Games with millions of information sets are beyond exact LP. [Counterfactual regret minimization](/counterfactual-regret-minimization/) and first-order methods on the polytopes of realization plans approximate the equilibrium of the same min-max problem.
- **Refinements.** An optimal plan can be arbitrary at information sets that it reaches with probability 0. Refined solutions that also play well there need perturbed versions of the LP.
## When to use it

Use it to solve a two-player zero-sum game tree with imperfect information exactly, when the tree fits in memory and an LP solver can handle a few times its size: small poker variants, endgames of bigger games, and search games. Use the LP for matrix games when the game is given in normal form. For trees too large for an LP, use an iterative method and accept an approximate equilibrium.

## Pitfalls

- **Perfect recall.** The code checks that all nodes of an information set have the same own sequence and rejects the tree otherwise. Without this check the LP is wrong without warning.
- **Unreached information sets.** Where $x(\sigma_h) = 0$, the behavior strategy is not determined by $x$; any choice there keeps the plan optimal, but it can be a poor move if the opponent errs.
- **Dual signs.** Player 2's plan is the vector of dual prices of the inequality rows, which must be nonnegative and satisfy $F y = f$; a solver with a different sign convention returns $-y$.
- **Free variables.** The vector $q$ has no sign condition, and its entries for player 2's information sets are usually negative when player 1 wins. Forcing $q \ge 0$ gives a wrong value.
- **Floating point.** With a floating-point LP solver, check $x$ and $y$ by best responses in the tree and allow a tolerance.

## Implementations

The Python code walks the tree once to build the sequences, the constraint matrices and the sequence payoff matrix (lines L1 to L3), then calls the shared exact simplex code on the LP of lines L4 and L5 and reads $y$ from its duals. It also converts realization plans to behavior strategies. The tests check the example above, Kuhn poker with value $-1/18$, and 40 random game trees with chance moves and hidden moves. For each one, $x$ must guarantee the value against every pure strategy of player 2, and $y$ must hold player 1 to it against every pure strategy of player 1, both computed in the tree. The value must also equal that of the normal-form game, solved by a separate LP over all pure strategies. Trees without perfect recall and inconsistent information sets must be rejected.

## History

Romanovskii (1962) reduced zero-sum games with perfect recall to linear programs of small size. Koller, Megiddo and von Stengel (1996), and von Stengel (1996) in a companion paper, introduced the sequence form under that name, gave the LP for zero-sum games and the LCP for general two-player games, and showed that the size is linear in the game tree.

## References
