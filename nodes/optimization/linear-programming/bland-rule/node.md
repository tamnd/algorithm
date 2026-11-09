---
tag: H8SV7C
kind: concept
slug: bland-rule
name: Bland's rule
aliases:
- smallest index rule
- anti-cycling rule
- least index rule
area: optimization/linear-programming
level: core
summary: Choose the lowest-index eligible variable, which guarantees termination on degenerate LPs.
prereqs: [simplex-method, pivot-operation, ratio-test]
see_also: [simplex-termination, lp-degeneracy, dantzig-pivot-rule, steepest-edge-pivot-rule, klee-minty-cube, ratio-test, fundamental-theorem-of-lp, strong-duality]
sources:
  - paper: doi:10.1287/moor.2.2.103
    title: Robert G. Bland, New finite pivoting rules for the simplex method, Mathematics of Operations Research 2(2), 1977
    locator: pages 103 to 107, the least-index rule and the proof that it does not cycle
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 3, Pitfalls and how to avoid them (cycling, the smallest subscript rule and its proof)
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 3.4, Anticycling, lexicography and Bland's rule
  - paper: doi:10.1007/BFb0121192
    title: David Avis and Vašek Chvátal, Notes on Bland's pivoting rule, Mathematical Programming Study 8, 1978
    locator: pages 24 to 34, exponential examples for the rule and its behavior on random programs
  - paper: doi:10.1002/nav.3800020406
    title: E. M. L. Beale, Cycling in the dual simplex algorithm, Naval Research Logistics Quarterly 2(4), 1955
    locator: pages 269 to 275, the cycling example
---

Bland's rule is a pivot rule for the [simplex method](/simplex-method/) that picks both the entering and the leaving variable by the smallest index: the entering variable is the first one with a negative [reduced cost](/reduced-cost/), and among the rows tied in the [ratio test](/ratio-test/), the leaving variable is the one with the smallest index. Bland proved in 1977 that with this rule the simplex method never cycles, so it always stops after finitely many pivots, even on [degenerate](/lp-degeneracy/) programs. The rule is simple to state and to prove, but in practice it is slow, and it can take exponentially many pivots.

## In plain words

Number all the variables once, at the start. Whenever the simplex method has a choice, it takes the candidate with the smallest number: the first variable that can improve the objective enters, and if several variables are tied to leave, the one with the smallest number leaves.

This dull rule has one strong property. On a degenerate corner, other rules can swap variables in and out without moving and come back to a set they had before, so they loop for ever. With the smallest-number rule, such a loop is impossible, so the method always ends. The price is speed: the rule ignores how good each choice is, so it often makes many small steps.

## The idea

**The rule.** For minimize $c^\top x$ subject to $Ax = b$, $x \ge 0$, with variables $x_1, \ldots, x_n$ and a feasible basis $B$:

1. *Entering.* $q = \min\{ j : r_j < 0 \}$. If there is none, the basis is optimal.
2. *Leaving.* With $d = B^{-1}A_q$, let $\theta^* = \min\{ x_{B(i)}/d_i : d_i > 0 \}$. Among the rows $i$ with $d_i > 0$ and $x_{B(i)}/d_i = \theta^*$, leave the variable $x_{B(i)}$ with the smallest index $B(i)$.

**Why it cannot cycle.** In a cycle every pivot has step $0$, so the point does not move, and every variable that enters or leaves during the cycle is $0$ throughout. Let $x_t$ be the one with the largest index. Compare a basis where $x_t$ leaves (and some $x_s$ with $s < t$ enters) with a later basis where $x_t$ enters. At the second basis the rule chose $t$, so all variables with smaller index have nonnegative reduced cost. Testing the edge direction of $x_s$ at the first basis against these reduced costs gives a variable $x_j$ with $j < t$ that was tied with $x_t$ in the ratio test, and the rule would have chosen $x_j$ to leave instead. The full proof is on the page [simplex termination](/simplex-termination/).

**Consequences.** Since the method stops, and there are finitely many bases, every feasible program in standard form either has an optimal basic feasible solution or is unbounded. This gives a constructive proof of the [fundamental theorem of linear programming](/fundamental-theorem-of-lp/), and with the final reduced costs, of [strong duality](/strong-duality/).

**Order matters.** The rule depends on the numbering of the variables. A different numbering of the same program gives a different path, and possibly a very different number of pivots.

## Examples

**Beale's example.** Minimize $-\frac34 x_4 + 20x_5 - \frac12 x_6 + 6x_7$ subject to $x_1 + \frac14 x_4 - 8x_5 - x_6 + 9x_7 = 0$, $x_2 + \frac12 x_4 - 12x_5 - \frac12 x_6 + 3x_7 = 0$, $x_3 + x_6 = 1$, $x \ge 0$, from the basis $\{x_1, x_2, x_3\}$. [Dantzig's rule](/dantzig-pivot-rule/) cycles here with period 6. Bland's rule makes these pivots:

| pivot | enters | leaves | step | value |
|---|---|---|---|---|
| 1 | $x_4$ | $x_1$ | 0 | 0 |
| 2 | $x_5$ | $x_2$ | 0 | 0 |
| 3 | $x_6$ | $x_4$ | 0 | 0 |
| 4 | $x_1$ | $x_5$ | 0 | 0 |
| 5 | $x_2$ | $x_3$ | 1/2 | $-1/2$ |
| 6 | $x_4$ | $x_2$ | 1 | $-5/4$ |

The first three pivots are the same as Dantzig's. At the fourth basis, $x_1$ and $x_7$ both have negative reduced costs. Dantzig's rule takes $x_7$, the more negative one, and goes on round the cycle; Bland's rule takes $x_1$, the smaller index, and leaves the degenerate vertex two pivots later. The optimum is $-5/4$ at $x = (\frac34, 0, 0, 1, 0, 1, 0)$.

**The Klee-Minty cube.** On the program minimize $-\sum_j 10^{n-j} x_j$ subject to $2\sum_{j<i} 10^{i-j}x_j + x_i \le 100^{i-1}$, $x \ge 0$, with the structural variables numbered before the slacks, Bland's rule needs these numbers of pivots:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Bland's rule | 1 | 3 | 5 | 9 | 15 | 25 | 41 | 67 | 109 | 177 |
| Dantzig's rule | 1 | 3 | 7 | 15 | 31 | 63 | 127 | 255 | 511 | 1023 |

For $n \ge 3$ in this table, each entry of Bland's row is the sum of the two before it plus one, which is $2F_{n+1} - 1$ with the Fibonacci numbers $F_k$; if the pattern goes on, the count grows like $1.618^n$. Avis and Chvátal (1978) gave programs on which Bland's rule takes exponentially many pivots.

## Where it is used

- **Proofs.** It is the shortest way to prove that the simplex method can always stop, and so to prove the [fundamental theorem of LP](/fundamental-theorem-of-lp/) and [strong duality](/strong-duality/) by the simplex method, as Chvátal and Bertsimas and Tsitsiklis do.
- **Exact solvers and teaching codes.** Codes in exact rational arithmetic, where cycling is real, use it, or switch to it after a number of degenerate pivots in a row and switch back after the next nondegenerate pivot.
- **Other pivoting methods.** The least-index idea also makes the dual simplex method and the criss-cross method finite, and Bland stated it for oriented matroids, where only the signs of the tableau entries are known.

## References
