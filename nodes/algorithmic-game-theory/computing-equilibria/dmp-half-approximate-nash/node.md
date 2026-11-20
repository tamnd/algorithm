---
tag: F0ZSX8
kind: algorithm
slug: dmp-half-approximate-nash
name: Daskalakis-Mehta-Papadimitriou algorithm
aliases:
- DMP algorithm
- 1/2-approximate Nash algorithm
area: algorithmic-game-theory/computing-equilibria
level: advanced
summary: Finds a 1/2-approximate Nash equilibrium of a bimatrix game in linear time from one action, its best response and the best response to that.
solves: [nash-equilibrium-computation]
model: real-ram
complexity:
  vars: {m: the number of pure strategies of the row player, n: the number of pure strategies of the column player}
  time: {worst: O(m + n)}
  space: {extra: O(m + n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2006
  people: [Constantinos Daskalakis, Aranyak Mehta, Christos H. Papadimitriou]
  note: Presented at WINE 2006 and published in Theoretical Computer Science in 2009 as the first of a series of polynomial-time bounds for additive approximate equilibria in two-player games.
prereqs: [bimatrix-game, best-response, epsilon-nash-equilibrium, mixed-strategy]
see_also: [lipton-markakis-mehta-algorithm, rubinstein-approximate-nash-lower-bound, ppad-completeness-of-nash, nash-equilibrium-computation, support-enumeration, lemke-howson-algorithm, approximation-ratio]
sources:
  - paper: doi:10.1016/j.tcs.2008.12.031
    title: "Constantinos Daskalakis, Aranyak Mehta and Christos H. Papadimitriou, A note on approximate Nash equilibria, Theoretical Computer Science 410(17) (2009), 1581-1588"
    locator: the linear-time algorithm that examines two strategies of one player and one of the other and reaches a 1/2-approximate equilibrium; conference version in WINE 2006
  - paper: doi:10.1145/1250910.1250962
    title: "Constantinos Daskalakis, Aranyak Mehta and Christos H. Papadimitriou, Progress in approximate Nash equilibria, Proceedings of the 8th ACM Conference on Electronic Commerce (EC 2007), 355-358"
    locator: the improvement to about 0.38 with a linear program and larger supports
  - paper: doi:10.1080/15427951.2008.10129172
    title: "Haralampos Tsaknakis and Paul G. Spirakis, An optimization approach for approximate Nash equilibria, Internet Mathematics 5(4) (2008), 365-382"
    locator: the descent method that reaches a 0.3393-approximation
  - paper: doi:10.1145/3606697
    title: "Argyrios Deligkas, Michail Fasoulakis and Evangelos Markakis, A polynomial-time algorithm for 1/3-approximate Nash equilibria in bimatrix games, ACM Transactions on Algorithms 19(4) (2023), 31:1-31:17"
    locator: the (1/3 + delta)-approximation in polynomial time; conference version in ESA 2022
---

The Daskalakis-Mehta-Papadimitriou (DMP) algorithm finds an approximate [Nash equilibrium](/nash-equilibrium/) of a two-player game in strategic form (a [bimatrix game](/bimatrix-game/)) with payoffs in $[0, 1]$. It takes any row, a best column against that row, and a best row against that column. The row player mixes the two rows with equal weight and the column player plays the column. No player can then gain more than $1/2$ by a change of strategy, so the pair is a $1/2$-Nash equilibrium in the additive sense of the [epsilon-Nash equilibrium](/epsilon-nash-equilibrium/) page. The method reads only one row and one column of the input. It is the simplest member of a line of polynomial-time approximations, and the bound $1/2$ is the best possible for every method whose strategies have small supports.

## In plain words

Two players each pick a move, and every outcome pays each of them between 0 and 1. We want a pair of plans where nobody can win much by switching. Start with any move of the first player. Let the second player pick a best answer to it. Let the first player pick a best answer to that answer. Now the first player flips a fair coin between the start move and its best answer, and the second player keeps its answer. Half of the time the first player already plays its best move, so it loses at most half a point. Half of the time the second player meets the move it answered best, so it also loses at most half a point.

## The problem

The input is two $m \times n$ matrices $A$ and $B$ with entries in $[0, 1]$. On this page $m$ and $n$ are the numbers of pure strategies of the row player and of the column player, not numbers of players. If the row player plays row $r$ and the column player plays column $c$, they get $A_{rc}$ and $B_{rc}$, and both maximize. A pair of [mixed strategies](/mixed-strategy/) $x \in \Delta_m$, $y \in \Delta_n$ is an $\varepsilon$-Nash equilibrium if

$$\max_r (Ay)_r - x^{\mathsf T} A y \le \varepsilon \quad\text{and}\quad \max_c (x^{\mathsf T} B)_c - x^{\mathsf T} B y \le \varepsilon.$$

The maxima are over pure strategies, and this is enough: a mixed strategy is a [best response](/best-response/) if and only if its support is inside the set of pure best responses, and any mixed deviation earns an average of pure deviation payoffs. The output is a pair $(x, y)$ with $\varepsilon = 1/2$. The scale $[0, 1]$ matters, because the additive $\varepsilon$ has a meaning only relative to the range of the payoffs.

## The algorithm

```pseudo id=main
DMP(A, B, i)                       ▷ A, B are m by n with entries in [0, 1]; i is any row
L1  j ← a column that maximizes B[i][c]        ▷ a best response to row i
L2  k ← a row that maximizes A[r][j]           ▷ a best response to column j
L3  x ← (1/2) e_i + (1/2) e_k                  ▷ x = e_i if k = i
L4  y ← e_j
L5  return (x, y)
```

Line L1 reads one row of $B$, and line L2 reads one column of $A$. The code breaks ties to the smallest index, but any tie rule gives the same guarantee.

## Example

Take $A = \begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix}$, $B = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$ and the start row $i = 0$. Row 0 of $B$ is $(1, 1)$, so line L1 picks $j = 0$. Column 0 of $A$ is $(0, 1)$, so line L2 picks $k = 1$. The output is $x = (1/2, 1/2)$ and $y = (1, 0)$.

| player | payoff of $(x, y)$ | best pure deviation | gain |
|---|---|---|---|
| row | $\tfrac12 \cdot 0 + \tfrac12 \cdot 1 = 1/2$ | row 1, payoff 1 | $1/2$ |
| column | $\tfrac12 \cdot 1 + \tfrac12 \cdot 0 = 1/2$ | column 1, payoff $\tfrac12 \cdot 1 + \tfrac12 \cdot 1 = 1$ | $1/2$ |

Both gains are exactly $1/2$, so the bound of the analysis is reached. The game also has the pure equilibrium (row 1, column 1), and the algorithm finds it from the start row $i = 1$: then $j = 1$ and $k = 1$, and the output is pure.

In matching pennies scaled to $[0, 1]$, with $A = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$ and $B = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$, the start row 0 gives $j = 1$, $k = 1$, $x = (1/2, 1/2)$ and $y = (0, 1)$. The column player has gain 0, and the row player has gain $1/2$, while the only equilibrium is the uniform pair.

## Correctness

Let $y = e_j$. The row player gets $\tfrac12 A_{ij} + \tfrac12 A_{kj}$, and its best pure payoff is $A_{kj}$ by line L2. So the row gain is $\tfrac12(A_{kj} - A_{ij}) \le \tfrac12$, because both entries are in $[0, 1]$.

The column player gets $\tfrac12 B_{ij} + \tfrac12 B_{kj}$. A deviation to column $c$ gives $\tfrac12 B_{ic} + \tfrac12 B_{kc}$, and $B_{ic} \le B_{ij}$ by line L1. So the gain from column $c$ is at most $\tfrac12 (B_{kc} - B_{kj}) \le \tfrac12$. In words, on the half of the time when the row player plays $i$, the column player already plays a best response, and on the other half it loses at most 1.

By the best-response fact, pure deviations give the largest gains, so $(x, y)$ is a $1/2$-Nash equilibrium. If $k = i$, both gains are 0 and the output is a pure Nash equilibrium. If the payoffs are in $[a, b]$ instead of $[0, 1]$, the same argument gives a $(b - a)/2$-Nash equilibrium. The [proof file](proofs/correctness.md) has the details and the tight example.

## Complexity

Line L1 reads $n$ entries and line L2 reads $m$ entries, and the output has $m + n$ numbers. So the time is $O(m + n)$ and the extra space is $O(m + n)$, in the real-RAM model with one step for each comparison. This is sublinear in the input size $2mn$ if the input can be read at any position. Trying all $m$ start rows and keeping the best pair costs $O(m(m + n))$ and still guarantees only $1/2$.

## Properties

- **Small supports.** The row player uses at most 2 strategies and the column player uses 1.
- **Deterministic and exact.** With rational payoffs the output and its gains are exact rationals.
- **Tight analysis.** The example above reaches the bound $1/2$ for both players at the same time.
- **Not an equilibrium in general.** The output is an exact equilibrium only when $k = i$, that is, when the start row is a best response to its own best response.
- **Additive only.** The guarantee needs payoffs on a common scale. It says nothing about relative approximation.

## Variants and improvements

- **Smaller $\varepsilon$ in polynomial time.** Larger supports and linear programs give better bounds: about $0.38$ (Daskalakis, Mehta and Papadimitriou, EC 2007), $0.36$ (Bosse, Byrka and Markakis), $0.3393$ (Tsaknakis and Spirakis 2008, by a descent method) and $1/3 + \delta$ for every constant $\delta > 0$ (Deligkas, Fasoulakis and Markakis, ESA 2022 and ACM Transactions on Algorithms 2023). A 2026 preprint of Li and Li claims about $0.3095 + \delta$, and it is not yet peer reviewed as of November 2026.
- **Quasi-polynomial time for any $\varepsilon$.** The [Lipton-Markakis-Mehta algorithm](/lipton-markakis-mehta-algorithm/) searches over supports of size $O(\log n / \varepsilon^2)$. Under an exponential-time hypothesis for [PPAD](/ppad/), constant $\varepsilon$ cannot be done much faster ([Rubinstein's theorem](/rubinstein-approximate-nash-lower-bound/)).
- **Well-supported equilibria.** In an $\varepsilon$-well-supported equilibrium every strategy in the support must be within $\varepsilon$ of a best response. The same note of DMP gives a reduction of this notion to win-lose games and a $5/6$ bound that depends on a graph conjecture. The best known polynomial bound is $1/2 + \delta$ (Deligkas, Fasoulakis and Markakis).
- **Exact equilibria.** [Lemke-Howson](/lemke-howson-algorithm/) or [support enumeration](/support-enumeration/) give exact answers in exponential time in the worst case. The exact problem is PPAD-complete ([PPAD-completeness of Nash](/ppad-completeness-of-nash/)).

## When to use it

Use it as a fast baseline, as a warm start for a local search, or when the game is too large to read in full and only $m + n$ queries are allowed. Use it in tests and in teaching, because the analysis fits in a few lines. When $1/2$ is too coarse, use the LP-based methods with a bound near $1/3$, or an exact method on small games.

## Pitfalls

- **Payoffs outside $[0, 1]$.** The bound $1/2$ is in units of the payoff range. Scale the payoffs first, or read the result as $(b - a)/2$.
- **Wrong matrix in a step.** Line L1 uses the column player's payoffs $B$ and line L2 uses the row player's payoffs $A$. Swapping them breaks the proof.
- **Two entries for one row when $k = i$.** If the code stores $x$ as a list of (row, weight) pairs, row $i$ appears twice with weight $1/2$. Merge the pairs, so that row $i$ has weight 1.
- **Expecting better on easy games.** A good start row helps, but no choice of start row improves the worst-case bound, and the example above has gain $1/2$ from row 0.
- **Small supports cannot do better.** Feder, Nazerzadeh and Saberi (EC 2007) showed games in which every $\varepsilon$-Nash equilibrium with $\varepsilon < 1/2$ needs supports of logarithmic size. So no method of this kind, with supports of constant size, can beat $1/2$.

## Implementations

The Python code follows lines L1 to L5 in exact rational arithmetic and returns the two gains. The tests check the tight example for several values of the free entries, a pure equilibrium found when $k = i$, battle of the sexes, matching pennies and chicken scaled to $[0, 1]$, and 300 random games with every start row, each checked against the shared exact checker. They also scale random integer payoffs to test the bound $(b - a)/2$, and count the entries that are read, which must be exactly $m + n$.

## History

Althöfer (1994) had shown that some games need supports of logarithmic size for a $1/4$-approximation, and Lipton, Markakis and Mehta (2003) had given a quasi-polynomial algorithm. Daskalakis, Mehta and Papadimitriou presented the simple $1/2$ method at WINE 2006, with the journal version in Theoretical Computer Science in 2009. The following year they gave the $0.38$ bound at EC 2007, where Feder, Nazerzadeh and Saberi also showed that small supports cannot go below $1/2$. The bound then went down to $0.3393$ in 2007 and 2008, and to $1/3 + \delta$ in 2022.

## References
