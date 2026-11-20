---
tag: V535CJ
kind: algorithm
slug: correlated-equilibrium-linear-program
name: Correlated equilibrium by linear programming
aliases:
- correlated equilibrium LP
area: algorithmic-game-theory/computing-equilibria
level: core
summary: "Computes a correlated equilibrium, or one of maximum welfare, of a normal-form game with a linear program over distributions on profiles."
model: real-ram
complexity:
  vars: {n: the number of players, k: the largest number of pure strategies of a player, L: the bit length of the payoffs}
  time: {worst: "poly(n, k^n, L)"}
  space: {extra: "O(n k^(n+2))"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1974
  people: [Robert J. Aumann, Sergiu Hart, David Schmeidler, Itzhak Gilboa, Eitan Zemel]
  note: "Aumann defined correlated equilibria as a set cut out by linear inequalities. Hart and Schmeidler (1989) proved their existence with linear programming duality, and Gilboa and Zemel (1989) noted that one of maximum welfare is found in polynomial time."
prereqs: [correlated-equilibrium, linear-programming-problem]
see_also: [ellipsoid-against-hope, zero-sum-game-linear-programming, regret-matching, blum-mansour-reduction, coarse-correlated-equilibrium, nash-equilibrium-computation, simplex-method, graphical-game]
sources:
  - paper: "Robert J. Aumann, Subjectivity and correlation in randomized strategies, Journal of Mathematical Economics 1(1) (1974), 67-96"
    title: Subjectivity and correlation in randomized strategies
    locator: the definition of correlated equilibrium and the chicken example with a correlated equilibrium better than every Nash equilibrium
  - paper: "Sergiu Hart and David Schmeidler, Existence of correlated equilibria, Mathematics of Operations Research 14(1) (1989), 18-25"
    title: Existence of correlated equilibria
    locator: the elementary existence proof by linear programming duality
  - paper: "Itzhak Gilboa and Eitan Zemel, Nash and correlated equilibria, some complexity considerations, Games and Economic Behavior 1(1) (1989)"
    title: "Nash and correlated equilibria: some complexity considerations"
    locator: "the polynomial-time computation of correlated equilibria, against the NP-hardness of the same questions for Nash equilibria"
  - paper: doi:10.1145/1379759.1379762
    title: "Christos H. Papadimitriou and Tim Roughgarden, Computing correlated equilibria in multi-player games, Journal of the ACM 55(3) (2008), article 14"
    locator: "the introduction (the LP for games in normal form, and why it is too large for succinct games)"
  - book: isbn:9781316624791
    title: "Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016"
    locator: Lecture 13 (the hierarchy of equilibrium concepts) and Lecture 18 (swap regret and correlated equilibria)
---

This algorithm computes a [correlated equilibrium](/correlated-equilibrium/) of a finite game given in normal form. The incentive constraints of a correlated equilibrium are linear in the probabilities $p(s)$ of the profiles, so the set of correlated equilibria is a polytope, and one [linear program](/linear-programming-problem/) finds a point of it that maximizes any linear objective, such as the total welfare. The LP has one variable per profile, so its size is polynomial in the size of the normal form, and the method runs in polynomial time. This is the main computational difference from Nash equilibria, which are PPAD-complete to find even for two players ([Nash equilibrium computation](/nash-equilibrium-computation/)). The LP needs the whole normal form; for succinct games with many players, where the normal form is exponentially large, the [ellipsoid against hope](/ellipsoid-against-hope/) works with the dual instead. In two-player zero-sum games the LP of [zero-sum games](/zero-sum-game-linear-programming/) is the smaller tool.

## In plain words

A trusted mediator draws a combination of actions at random from a list of chances, and tells each player only its own part. The list is fair if no player, told its part, gains on average by doing something else. For each player, each action it could be told and each other action it could switch to, the fairness test is a sum of chances times gains, and it must not be positive. All these tests are straight-line conditions on the chances. So are the conditions that the chances are not negative and add up to one. Finding chances that pass all tests, and that give the largest total reward, is a linear program, and there are standard methods that solve it fast.

## The problem

The input is a finite game with players $N = \{1, \ldots, n\}$, pure strategy sets $S_i$ with $k_i = |S_i| \le k$, and rational utilities $u_i : S \to \mathbb{Q}$ on $S = S_1 \times \cdots \times S_n$, maximized, given as the full table of $n |S|$ numbers. An objective $w : S \to \mathbb{Q}$ is also given; the default is the welfare $w(s) = \sum_i u_i(s)$, and $w = 0$ asks for any correlated equilibrium.

A distribution $p$ on $S$ is a correlated equilibrium if for every player $i$ and every pair $j \ne l$ of strategies of $i$,

$$\sum_{s \in S : s_i = j} p(s)\,\big[u_i(l, s_{-i}) - u_i(s)\big] \le 0 .$$

This says that a player told to play $j$ does not gain, on average over the profiles that the mediator may have drawn, by playing $l$ instead. The output is a correlated equilibrium $p$ that maximizes $\sum_s w(s) p(s)$. Every mixed Nash equilibrium, viewed as a product distribution, is a correlated equilibrium; for a product distribution the constraints are the Nash conditions, which hold exactly when every strategy in the support of $\sigma_i$ is a pure best response. So the set is not empty.

## The algorithm

```pseudo id=main
CE-LP(G, w)                     ▷ w(s) is the objective weight of profile s
L1  create a variable p(s) ≥ 0 for each profile s in S
L2  for each player i and each pair j ≠ l in S_i
L3      add the constraint Σ_{s : s_i = j} p(s) (u_i(l, s_-i) - u_i(s)) ≤ 0
L4  add the constraint Σ_s p(s) = 1
L5  maximize Σ_s w(s) p(s) subject to these constraints
L6  return p
```

Lines L1 to L4 build the LP. It has $|S|$ variables, $\sum_i k_i(k_i - 1) \le n k^2$ inequalities of line L3 and one equation. The row of line L3 for $(i, j, l)$ has a nonzero entry only for the profiles with $s_i = j$, so the constraint matrix is sparse: each column, for a profile $s$, has at most $\sum_i (k_i - 1)$ nonzero entries in the incentive rows. Line L5 can use the [simplex method](/simplex-method/), the [ellipsoid method](/ellipsoid-method/) or an [interior point method](/interior-point-method/). The feasible set is bounded, because it lies in the simplex of distributions on $S$, and it is not empty, so the LP has an optimal solution, at a vertex of the polytope.

## Example

Take chicken with strategies D (dare) and C (chicken) and payoffs (D, D) = (0, 0), (D, C) = (7, 2), (C, D) = (2, 7) and (C, C) = (6, 6). Write $a, b, c, d$ for $p(\text{D}, \text{D})$, $p(\text{D}, \text{C})$, $p(\text{C}, \text{D})$ and $p(\text{C}, \text{C})$. Line L3 gives four constraints, and the welfare is $9b + 9c + 12d$.

| constraint of line L3 | inequality | at the max-welfare optimum |
|---|---|---|
| row player, told D, plays C | $2a - b \le 0$ | $-1/4$, slack |
| row player, told C, plays D | $-2c + d \le 0$ | $0$, tight |
| column player, told D, plays C | $2a - c \le 0$ | $-1/4$, slack |
| column player, told C, plays D | $-2b + d \le 0$ | $0$, tight |

The optimum is $a = 0$, $b = c = 1/4$, $d = 1/2$, with welfare $21/2$, so each player gets $21/4$. Compare the other equilibria of the same game: the pure Nash equilibria (D, C) and (C, D) give welfare 9; the mixed Nash equilibrium, which plays C with probability $2/3$ and gives the product $a = 1/9$, $b = c = 2/9$, $d = 4/9$, gives $14/3$ each; the uniform distribution on (D, C), (C, D) and (C, C) gives 5 each. With $w = -\sum_i u_i$ the same LP finds the worst correlated equilibrium, $a = 1/5$, $b = c = 2/5$, $d = 0$, with welfare $36/5$, which is below every Nash equilibrium.

## Correctness

The constraints of lines L1 and L4 say that $p$ is a probability distribution on $S$, and the constraints of line L3 are exactly the incentive constraints, one for each player and each ordered pair of strategies. So the feasible set of the LP is exactly the set of correlated equilibria. It is not empty, because a mixed Nash equilibrium exists and is a correlated equilibrium (Hart and Schmeidler give a proof that uses only LP duality), and it is bounded. So line L5 returns a correlated equilibrium of maximum objective value, and the simplex method with [Bland's rule](/bland-rule/) finds it in a finite number of pivots. The full proof is in the proof file.

## Complexity

The LP has $|S| \le k^n$ variables and at most $n k^2 + 1$ constraints, and its coefficients are differences of payoffs, so its bit length is polynomial in $n$, $k^n$ and $L$. The ellipsoid method or an interior point method solves it in time polynomial in these numbers, so a correlated equilibrium of maximum welfare is found in time polynomial in the size of the normal form, which is $n k^n$ numbers. The solution is a vertex, a rational vector with a polynomial number of digits. The dense constraint matrix takes $O(n k^2 \cdot k^n)$ space, or $O(n k \cdot k^n)$ as a sparse matrix.

With the simplex method, the number of pivots can be exponential in the worst case, but it is small in practice. The code on this page uses exact rational arithmetic with Bland's rule.

The input size hides the catch: for $n$ players with 2 strategies each, the LP has $2^n$ variables. For games with a short description, such as [graphical games](/graphical-game/) or congestion games, this is exponential in the input, and the ellipsoid against hope is needed.

## Properties

- **Exact and optimizing.** Any linear objective can be optimized over the set, not only found in it; for Nash equilibria the analogous welfare question is NP-hard (Gilboa and Zemel, 1989).
- **A convex set.** The correlated equilibria form a convex polytope, and so do the coarse correlated equilibria. Mixed Nash equilibria form a finite union of polytopes in two-player games and are not convex in general.
- **Vertices.** The simplex method returns a vertex. A vertex has at most $n k^2 + 1$ nonzero probabilities, the number of constraints, which is small compared with $|S|$.
- **Better than Nash.** The optimal welfare is at least that of every Nash equilibrium, and can be strictly larger, as in chicken.

## Variants and improvements

- **Coarse correlated equilibria.** Replace line L3 by one constraint per player $i$ and strategy $l$: $\sum_s p(s)[u_i(l, s_{-i}) - u_i(s)] \le 0$. This gives the larger set of [coarse correlated equilibria](/coarse-correlated-equilibrium/), with $\sum_i k_i$ constraints.
- **Approximate equilibria.** Replace 0 by $\varepsilon$ on the right of line L3 for correlated $\varepsilon$-equilibria.
- **Succinct games.** The dual LP has one variable per incentive constraint and one constraint per profile. The [ellipsoid against hope](/ellipsoid-against-hope/) runs the ellipsoid method on the dual and returns a mixture of polynomially many product distributions, in time polynomial in the description of games with a polynomial-time expected utility oracle.
- **Learning instead of solving.** [Regret matching](/regret-matching/) and the [Blum-Mansour reduction](/blum-mansour-reduction/) give approximate correlated equilibria by repeated play, with no LP and no knowledge of other players' payoffs, at a cost of $O(1/\varepsilon^2)$ rounds or more.
- **Extensive-form games.** Correlation in game trees leads to the extensive-form correlated equilibrium, whose LP is not the normal-form one; the normal form of a tree is exponentially large.

## When to use it

Use it for a game given as a table, when the table fits in memory and an exact answer or an optimum over the correlated equilibria is needed. For two-player zero-sum games, the zero-sum LP is smaller and gives the same answer (every correlated equilibrium there pays the value). For many players with a succinct description, use the ellipsoid against hope. For a quick approximate answer in a large table, use no-swap-regret learning.

## Pitfalls

- **Swapped sign in line L3.** Writing $u_i(s) - u_i(l, s_{-i}) \le 0$ gives the correlated equilibria of the game with negated payoffs, in which no recommendation is better than a switch. The LP is still feasible, so the error is silent. The gain from deviating, $u_i(l, s_{-i}) - u_i(s)$, must be at most 0.
- **Summing over all profiles in line L3.** The sum runs only over the profiles with $s_i = j$. Summing over all profiles gives the coarse constraint for $l$, and the result is only a coarse correlated equilibrium.
- **Unordered pairs in line L2.** Line L2 needs every ordered pair $j \ne l$. A loop over $j < l$ only checks the players who are told the smaller strategy, and the result can fail for a player told $l$.
- **Floating-point solvers.** A floating-point LP solver returns a point that may violate line L3 by rounding. Check the result with exact arithmetic, or accept a correlated $\varepsilon$-equilibrium.
- **Large games.** With many players, line L1 creates $k^n$ variables. Use a succinct method instead.

## Implementations

The Python code builds the LP of lines L1 to L4 with exact rational coefficients and solves it with the shared exact simplex code (two phases, Bland's rule). The tests check the chicken values above, the unique correlated equilibria of matching pennies, rock-paper-scissors (the uniform product, for random objectives) and the prisoner's dilemma, every incentive inequality of each output exactly, and the optimal value against an independent enumeration of all vertices of the polytope on random 2 by 2, 2 by 3 and 3 by 2 games, and against every pure Nash equilibrium on random games with up to 3 players.

## History

Aumann (1974) defined correlated equilibria and showed with chicken that they can give more welfare than any Nash equilibrium. Because the definition consists of linear inequalities, a linear program finds one; Hart and Schmeidler (1989) proved existence by linear programming duality alone, without a fixed point theorem, and Gilboa and Zemel (1989) contrasted the polynomial time of correlated equilibria with the NP-hardness of related questions about Nash equilibria. Papadimitriou and Roughgarden (2008) extended polynomial-time computation to succinct games.

## References
