---
tag: F1V2JQ
kind: algorithm
slug: nucleolus-sequential-lp
name: Nucleolus by sequential linear programming
aliases:
- Kopelowitz algorithm
- Maschler-Peleg-Shapley procedure
area: algorithmic-game-theory/cooperative-games
level: advanced
summary: Computes the nucleolus of a TU game with a sequence of linear programs; each round minimizes the largest free excess and fixes the coalitions that stay tight on the whole optimal face.
model: real-ram
complexity:
  vars: {n: the number of players, L: the bit length of the coalition values}
  time: {worst: "poly(2^n, L)"}
  space: {extra: O(4^n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1967
  people: [A. Kopelowitz, Michael Maschler, Bezalel Peleg, Lloyd S. Shapley]
  note: Kopelowitz described the sequence of linear programs in a 1967 research memorandum of the Hebrew University; Maschler, Peleg and Shapley gave the geometry of the sequence of least cores in 1979.
prereqs: [nucleolus, least-core, lp-duality, complementary-slackness]
see_also: [core-of-a-cooperative-game, talmud-rule, bankruptcy-problem, assignment-game, simplex-method, ellipsoid-method, linear-programming-problem, lexicographic-order]
sources:
  - paper: "A. Kopelowitz, Computation of the kernels of simple games and the nucleolus of n-person games, Research Memorandum 31, Department of Mathematics, The Hebrew University of Jerusalem, 1967"
    locator: the computation of the nucleolus by a sequence of linear programs (an unpublished memorandum)
  - paper: doi:10.1137/0117107
    title: "David Schmeidler, The nucleolus of a characteristic function game, SIAM Journal on Applied Mathematics 17(6) (1969), 1163-1170"
    locator: the definition of the nucleolus and the proof that it exists and is unique
  - paper: doi:10.1287/moor.4.4.303
    title: "Michael Maschler, Bezalel Peleg and Lloyd S. Shapley, Geometric properties of the kernel, nucleolus, and related solution concepts, Mathematics of Operations Research 4(4) (1979), 303-338"
    locator: the least core and the nested sequence of least cores that ends in the nucleolus
  - paper: doi:10.1137/0120009
    title: "Elon Kohlberg, On the nucleolus of a characteristic function game, SIAM Journal on Applied Mathematics 20(1) (1971), 62-66"
    locator: the characterization of the nucleolus by balanced collections of coalitions
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: Chapter 20, The nucleolus (Section 20.2 on nonemptiness and uniqueness, Section 20.4 on computing the nucleolus, Section 20.5 on the characterization of the prenucleolus)
  - book: "Bezalel Peleg and Peter Sudholter, Introduction to the Theory of Cooperative Games, 2nd edition, Theory and Decision Library C 34, Springer, 2007"
    title: Introduction to the Theory of Cooperative Games
    locator: Chapter 5 (the prekernel, kernel and nucleolus) and Chapter 6 (the prenucleolus, with Kohlberg's criterion)
  - paper: doi:10.1007/BF01240179
    title: "Tamas Solymosi and T. E. S. Raghavan, An algorithm for finding the nucleolus of assignment games, International Journal of Game Theory 23 (1994), 119-143"
    locator: a polynomial algorithm for the nucleolus of the assignment game
  - paper: "Ulrich Faigle, Walter Kern and Jeroen Kuipers, On the computation of the nucleolus of a cooperative game, International Journal of Game Theory 30 (2001), 79-98"
    locator: the nucleolus in polynomial time from a separation oracle for the least core, by the ellipsoid method; the case of convex games
  - paper: "Ulrich Faigle, Walter Kern and Jeroen Kuipers, Computing the nucleolus of min-cost spanning tree games is NP-hard, International Journal of Game Theory 27(3) (1998), 443-450"
    locator: the NP-hardness of the nucleolus of minimum cost spanning tree games
---

The nucleolus of a [TU game](/transferable-utility-game/) is the imputation whose worst excess is as small as possible, then whose second worst excess is as small as possible, and so on. This page is the algorithm that computes it. The definition and its properties are on the [nucleolus](/nucleolus/) page. The first round of the algorithm is the linear program of the [least core](/least-core/); each later round solves a least core problem again, inside the set that the earlier rounds left. Kopelowitz described the method in 1967. With exact arithmetic it returns the exact nucleolus after at most $n - 1$ rounds.

## In plain words

Some players must share a sum of money, and every group of players can say how much it could earn alone. The complaint of a group is what it could earn alone minus what it gets in the shared plan. First find the plans that make the largest complaint as small as possible. This is one linear program. Some groups have this largest complaint in every one of those plans: nothing can make them happier without making a group at least as unhappy. Freeze their complaints at that level. Then, among the plans left, make the largest complaint of the other groups as small as possible, and freeze again. Each freeze fixes at least one more direction in which the plan can move. After at most one round fewer than the number of players, only one plan is left, and that plan is the nucleolus.

## The problem

The input is a TU game $(N, v)$: players $N = \{1, \ldots, n\}$ and a value $v(S)$ for each coalition $S \subseteq N$, with $v(\emptyset) = 0$. For a payoff vector $x$ let $x(S) = \sum_{i \in S} x_i$, and let the excess of $S$ at $x$ be $e(S, x) = v(S) - x(S)$, the amount by which $S$ is short of what it can earn alone. The imputations are the vectors with $x(N) = v(N)$ and $x_i \ge v(\{i\})$ for every $i$. They exist exactly when $v(N) \ge \sum_i v(\{i\})$. For an imputation $x$ let $\theta(x)$ be the vector of the $2^n - 2$ excesses of the coalitions $S$ with $\emptyset \ne S \ne N$, sorted from the largest to the smallest. The output is the nucleolus, the imputation with the lexicographically smallest $\theta(x)$. Schmeidler proved that it exists and is unique. If the bounds $x_i \ge v(\{i\})$ are dropped, the same minimum over all $x$ with $x(N) = v(N)$ is the prenucleolus, and the algorithm computes it with the same steps.

The excesses of $\emptyset$ and $N$ are 0 at every imputation, so it makes no difference whether $\theta$ lists them. The input has $2^n$ numbers, so the algorithm is meant for games given as a full table. For games with a short description, see "Variants and improvements".

## The algorithm

```pseudo id=main
NUCLEOLUS(N, v)
L1  if v(N) < v({1}) + ... + v({n}): stop, the game has no imputation
L2  F ← all coalitions S with ∅ ≠ S ≠ N; E ← ∅
L3  while the indicator vectors of N and of the coalitions in E have rank < n:
L4      t* ← min t over the imputations x with v(S) - x(S) = t_S for (S, t_S) in E and v(S) - x(S) ≤ t for S in F
L5      for each S in F:
L6          if the row of S has a nonzero dual value at L4, or max{x(S) : x optimal at L4} = v(S) - t*:
L7              remove S from F and add (S, t*) to E
L8      for each S in F:
L9          if the indicator vector of S is in the span of those of N and E: remove S from F
L10 return the unique x with x(N) = v(N) and x(S) = v(S) - t_S for every (S, t_S) in E
```

The set $F$ holds the free coalitions, whose excess the algorithm still tries to lower. The set $E$ holds the fixed coalitions, each with the level $t_S$ at which its excess is frozen. Line L4 is a linear program with the $n$ numbers $x_i$ and the level $t$ as variables. It finds the smallest possible largest free excess, $t^*$, inside the set that the earlier rounds left. Its optimal points form a face of a polyhedron, and lines L5 to L7 freeze the free coalitions whose excess is $t^*$ on the whole face. Line L6 has two tests. A constraint with a nonzero dual value is tight at every optimal point, by [complementary slackness](/complementary-slackness/), so it needs no more work. For the other coalitions, one more LP checks whether $x(S)$ can be raised above $v(S) - t^*$, which would lower the excess of $S$ below $t^*$ somewhere on the face. Lines L8 and L9 drop the free coalitions whose excess is already a fixed number, because their indicator vector is a linear combination of fixed ones. Line L10 solves the final linear system.

The proof shows that at least one coalition is frozen in each round, and that its indicator vector is new. So the rank in line L3 grows by at least 1 per round, from 1 to $n$.

## Example

Take the [bankruptcy problem](/bankruptcy-problem/) with claims $c = (100, 200, 300)$ and an estate of $E = 200$. Its game gives a coalition what is left after it pays the claims of the others in full: $v(S) = \max(0, E - c(N \setminus S))$. Here $v(\{2, 3\}) = 100$, $v(N) = 200$, and every other coalition has value 0. Since every $v(\{i\})$ is 0, the imputations are the vectors $x \ge 0$ with $x_1 + x_2 + x_3 = 200$.

Round 1. The free excesses are $-x_1$, $-x_2$, $-x_3$, $-(x_1 + x_2)$, $-(x_1 + x_3)$ and $100 - x_2 - x_3 = x_1 - 100$. A pair of players never has the largest excess, because its excess is below that of each of its members. The largest of $-x_1$ and $x_1 - 100$ is smallest at $x_1 = 50$, where both are $-50$. Then $x_2 + x_3 = 150$, and $-x_2, -x_3 \le -50$ holds whenever both are at least 50. So $t^* = -50$, and the optimal face is $\{x_1 = 50,\ 50 \le x_2 \le 100,\ x_3 = 150 - x_2\}$. On the whole face, $\{1\}$ and $\{2, 3\}$ have excess $-50$; the others do not. Line L7 fixes both. Their indicators are $(1, 0, 0)$ and $(0, 1, 1)$, and the span of these and $(1, 1, 1)$ has rank 2. No free coalition is in this span, so line L9 drops nothing.

Round 2. Now $x_1 = 50$ and $x_2 + x_3 = 150$. The free excesses are $-x_2$, $-x_3$, $-50 - x_2$ and $-50 - x_3$. The largest is smallest at $x_2 = x_3 = 75$, so $t^* = -75$, and the face is that single point. Line L7 fixes $\{2\}$ and $\{3\}$, the rank becomes 3, and line L9 drops $\{1, 2\}$ and $\{1, 3\}$.

| round | $t^*$ | fixed in this round | dropped | rank after the round |
|---|---|---|---|---|
| 1 | $-50$ | $\{1\}$, $\{2, 3\}$ | none | 2 |
| 2 | $-75$ | $\{2\}$, $\{3\}$ | $\{1, 2\}$, $\{1, 3\}$ | 3 |

Line L10 returns $(50, 75, 75)$, the award of the [Talmud rule](/talmud-rule/) for this estate. The excess vector is $\theta = (-50, -50, -75, -75, -125, -125)$. The estates 100 and 300 give $(100/3, 100/3, 100/3)$ and $(50, 100, 150)$, which are also Talmud awards.

A game with a one-round run is the glove game: player 1 owns a left glove, players 2 and 3 own right gloves, and a pair is worth 1. So $v(S) = 1$ when $S$ contains player 1 and at least one other player, and $v(S) = 0$ otherwise. Round 1 gives $t^* = 0$ and fixes all five coalitions except $\{1\}$, whose indicator is then in the span. Line L10 returns $(1, 0, 0)$, the only point of the core. The three-player majority game, where every pair is worth 1, also takes one round: $t^* = 1/3$, the three pairs are fixed, and the result is $(1/3, 1/3, 1/3)$.

## Correctness

The file proofs/correctness.md has the full proof. It keeps the set $X$ of imputations that satisfy the fixed equations, and an invariant with three parts: the nucleolus $\nu$ is in $X$; the dropped coalitions have indicators in the fixed span and the free ones do not; and $\nu$ minimizes the sorted vector of free excesses over $X$. The last part needs a small lemma. Adding the same numbers to two vectors does not change which of the two sorted vectors is lexicographically smaller. Then, in each round:

- the first entry of the sorted free excesses is the largest free excess, so $\nu$ is optimal at line L4;
- lines L5 to L7 fix exactly the free coalitions that are tight on the whole optimal face, and there is at least one, because the average of points that each loosen one coalition would loosen all of them and beat $t^*$;
- a fixed coalition was free, so its indicator was not in the span, and the rank grows.

When the rank reaches $n$, the fixed equations have exactly one solution. Every point of $X$ solves them, and $\nu$ is in $X$, so line L10 returns $\nu$. The same lemma also gives the uniqueness of the nucleolus (Schmeidler's midpoint argument), which the proof includes.

## Complexity

The loop runs at most $n - 1$ times. Each round solves one LP at line L4 and at most $|F| \le 2^n - 2$ LPs at line L6, so there are at most $(n - 1)(2^n - 1)$ LPs in total. Each has $n + 1$ variables and at most $2^n + n$ constraints. With a polynomial LP method, such as the [ellipsoid method](/ellipsoid-method/) or an interior point method, each LP takes time polynomial in $2^n$ and the bit length $L$ of the values, so the whole run is polynomial in the size of the table, which already has $2^n$ entries. The span tests of lines L8 and L9 are Gaussian elimination on vectors of length $n$, $O(n^2)$ operations per coalition with the reduced rows kept up to date.

The code uses the shared exact [simplex method](/simplex-method/) with Bland's rule and fractions, so it is exact but not polynomial in the worst case; on the small tables of the tests it is fast. Its tableau is dense, with one slack column per constraint, which takes $O(4^n)$ numbers; this is the space bound in the front matter. A sparse LP solver needs only $O(n 2^n)$. Most of the LPs of line L6 are not needed in practice: a basic optimal dual solution gives many tight coalitions at once, and a coalition whose excess is below $t^*$ at the optimal point of line L4 is clearly not tight on the whole face.

## Properties

- **Exact.** All numbers are fractions, so the tests "dual is nonzero" and "the maximum equals $v(S) - t^*$" have no tolerance. With floating point, a coalition that is tight only up to rounding can be fixed by mistake, and the final system can become inconsistent.
- **Levels do not increase.** The values $t^*$ of the rounds form a nonincreasing sequence, and they are entries of $\theta(\nu)$: the largest is $\theta_1(\nu)$, the least core value.
- **Covariant.** If $w = a v + b$ for $a > 0$ and an additive game $b$, the run on $w$ makes the same choices and returns $a \nu + b$. The tests check this.
- **Symmetric.** Renaming the players renames the result; equal players get equal payoffs.
- **In the core when the core is not empty.** Then $t^* \le 0$ in round 1, so every excess at the result is at most 0, and the result is in the [core](/core-of-a-cooperative-game/).

## Variants and improvements

- **Prenucleolus.** Drop the bounds $x_i \ge v(\{i\})$ from line L4 and the check of line L1. The proof is the same. For games where the core is not empty, the nucleolus and the prenucleolus are equal, because both are in the core.
- **Fewer LPs.** In a strictly complementary pair of optimal primal and dual solutions, the coalitions with a nonzero dual value are exactly the coalitions that are tight on the whole optimal face. So a solver that returns such a pair, as interior point methods do, makes the extra LPs of line L6 unnecessary.
- **One balancedness check.** Kohlberg's criterion characterizes the prenucleolus: $x$ is the prenucleolus exactly when, for every level $\alpha$, the coalitions with excess at least $\alpha$ form a balanced collection. It does not give a fast algorithm, but it is a good certificate; the tests use it to check the prenucleolus mode.
- **Compact games.** When the game has a short description, the exponential number of constraints can be handled by a separation oracle and the ellipsoid method. Faigle, Kern and Kuipers (2001) show that the nucleolus can then be computed in polynomial time when the separation problem of the least core can be solved in polynomial time, and they apply this to convex games. For [assignment games](/assignment-game/), Solymosi and Raghavan give a direct polynomial algorithm. For [minimum cost spanning tree games](/minimum-cost-spanning-tree-game/) the nucleolus is NP-hard to compute (Faigle, Kern and Kuipers 1998).
- **Bankruptcy games.** The nucleolus of a bankruptcy game is the Talmud rule, which runs in $O(n \log n)$ time; there is no need for LPs.

## When to use it

Use the sequential LP when the game is given as a full table of $2^n$ values, $n$ is small, and you need the exact nucleolus or prenucleolus. It is the reference method to test special algorithms against, as the tests of the Talmud rule do. For larger games use a structure of the game: a polynomial special algorithm, or constraint generation when the largest excess can be found by a combinatorial search.

## Pitfalls

- **Fixing every coalition that is tight at one optimal point.** A coalition can have excess $t^*$ at the point that the solver returns but less elsewhere on the face. Fixing it at $t^*$ cuts the face and can exclude the nucleolus. Only fix a coalition that is tight on the whole face (line L6).
- **Forgetting the dependent coalitions.** If a free coalition with a fixed excess stays in $F$, a later round can return $t^*$ equal to its constant excess and fix only that coalition. The round then does not raise the rank, and the bound of $n - 1$ rounds is lost. Line L9 prevents this.
- **Nucleolus and prenucleolus mixed up.** They can differ when the core is empty. In the game with $v(\{1, 2\}) = 2$, $v(\{1, 3\}) = 3$, $v(\{2, 3\}) = 4$, $v(N) = 2$ and $v(\{i\}) = 0$, the prenucleolus is $(-1/3, 2/3, 5/3)$, which gives player 1 less than it can get alone, while the nucleolus is $(0, 1/2, 3/2)$.
- **No imputation.** If $v(N) < \sum_i v(\{i\})$, the nucleolus does not exist, but the prenucleolus does. The code raises an error in the first case and computes the prenucleolus on request.
- **Floating point tolerances.** With a floating point solver, compare with a tolerance that scales with the values, and check the result at the end by Kohlberg's criterion.

## Implementations

## History

Schmeidler defined the nucleolus and proved its existence and uniqueness in a paper published in 1969. Kopelowitz, at the Hebrew University of Jerusalem, wrote the sequence of linear programs in a research memorandum of 1967, which was never published as a paper but is the usual source for the method. Kohlberg characterized the nucleolus by balanced collections in 1971. Maschler, Peleg and Shapley described in 1979 the nested sequence of least cores whose last element is the nucleolus, which is the geometric picture behind the rounds. Later work replaced the exponential LPs by polynomial algorithms for structured classes: assignment games (Solymosi and Raghavan 1994) and, with the ellipsoid method, convex games and other classes (Faigle, Kern and Kuipers 2001).

## References
