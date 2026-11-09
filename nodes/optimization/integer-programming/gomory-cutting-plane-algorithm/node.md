---
tag: BP9Q4E
kind: algorithm
slug: gomory-cutting-plane-algorithm
name: Gomory's cutting-plane algorithm
aliases:
- Gomory's method
- Gomory's fractional cutting-plane algorithm
- Gomory's all-integer algorithm
area: optimization/integer-programming
level: advanced
summary: Solve a pure integer program by solving its LP relaxation and adding Gomory fractional cuts from the simplex tableau until the optimal vertex is integral.
model: real-ram
properties: {deterministic: true, recursive: false}
history:
  year: 1958
  people: [Ralph E. Gomory]
  note: Gomory announced the method and its finiteness in 1958, and published the full proof in 1963.
prereqs: [simplex-method, lp-relaxation, chvatal-gomory-cut, basic-feasible-solution]
see_also: [cutting-plane-method-integer-programming, gomory-mixed-integer-cut, chvatal-closure, chvatal-gomory-finite-convergence, dual-simplex-method, branch-and-cut, mixed-integer-programming]
sources:
  - paper: doi:10.1090/S0002-9904-1958-10224-4
    title: Ralph E. Gomory, Outline of an algorithm for integer solutions to linear programs, Bulletin of the American Mathematical Society 64(5), 1958
    locator: the whole note (the fractional cut and the finiteness claim)
  - paper: "Ralph E. Gomory, An algorithm for integer solutions to linear programs, in R. L. Graves and P. Wolfe (editors), Recent Advances in Mathematical Programming, McGraw-Hill, 1963, pages 269 to 302"
    locator: the full algorithm with the lexicographic rule and the proof of finiteness
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 23 (cutting planes, with Gomory's cutting plane method and its finiteness)
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 5 (Gomory's fractional cuts and the finite convergence of the lexicographic method)
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 8 (Gomory's fractional cutting plane algorithm)
  - paper: "Egon Balas, Sebastián Ceria, Gérard Cornuéjols and N. Natraj, Gomory cuts revisited, Operations Research Letters 19(1) (1996), 1 to 9"
    locator: the computational study of Gomory cuts inside branch and cut
---

Gomory's cutting-plane algorithm solves a pure [integer program](/mixed-integer-programming/) by repeated linear programming. It solves the [LP relaxation](/lp-relaxation/) with the [simplex method](/simplex-method/). If the optimal vertex is fractional, it reads a row of the final tableau whose value is fractional, derives from it a Gomory fractional cut, a special [Chvátal-Gomory cut](/chvatal-gomory-cut/) that every integer point satisfies and the vertex violates, adds the cut, and solves again. With a lexicographic rule it stops after finitely many rounds, with an optimal integer point or a proof that none exists. It was the first finite algorithm for integer programming (Gomory 1958).

## In plain words

First solve the problem as if fractions were allowed. If the answer happens to be whole numbers, it is also the best whole-number answer, and you are done. If not, look at one equation of the final simplex table that has a fractional value. Throw away the whole-number parts of its coefficients. What is left gives a new rule that every whole-number answer obeys, but the current fractional answer breaks.

Add that rule and solve again. The fractional answer moves. Each new rule cuts a slice off the region, and no whole-number point is ever lost. If you always pick the equation in a fixed careful order, the slices cannot get smaller forever, and the method stops. In the worst case it needs very many rounds.

## The problem

The input is integer data $A \in \mathbb{Z}^{m \times n}$, $b \in \mathbb{Z}^m$ and $c \in \mathbb{Z}^n$, where $n$ is the number of variables and $m$ the number of constraints. The problem is

$$\max \{\, c^T x : Ax \le b,\ x \ge 0,\ x \in \mathbb{Z}^n \,\}.$$

The output is an optimal $x^*$, or the answer "infeasible". The algorithm needs the polytope $P = \{x \ge 0 : Ax \le b\}$ to be bounded; a box $0 \le x \le u$ in the rows of $A$ is enough. The data are integral, so each slack $s_r = b_r - A_r x$ is an integer at each integer point. The [LP pages](/lp-standard-form/) use $\min$ and equality form; the slacks give that form.

## The algorithm

Write the components of a point as $v(x) = (c^T x, x_1, \ldots, x_n)$, numbered $0$ to $n$. At an optimal basis of the LP, each component is an affine function of the nonbasic variables $t_h$ (original variables or slacks): $v_k = \bar v_k - \sum_h d_{kh} t_h$. Here $\bar v_k$ is the value at the vertex, and $d_{0h}$ is the reduced cost of $t_h$. For a rational $q$, $\operatorname{frac}(q) = q - \lfloor q \rfloor \in [0, 1)$.

```pseudo id=main
GOMORY(A, b, c)                  ▷ max cᵀx, Ax ≤ b, x ≥ 0, x integer
L1  loop
L2      solve max cᵀx over P_k = {x ≥ 0 : Ax ≤ b}; take the lexicographically largest optimal vertex of v(x), with its tableau
L3      if P_k = ∅ then return INFEASIBLE
L4      v̄ ← (cᵀx̄, x̄_1, ..., x̄_n) at that vertex x̄
L5      if every v̄_k is an integer then return x̄
L6      j ← the smallest k with v̄_k fractional; read its row v_j = v̄_j − Σ_h d_jh t_h
L7      cut: Σ_h frac(d_jh) t_h ≥ frac(v̄_j)
L8      write the cut as gᵀx ≤ g₀ with g, g₀ integer, append it to A and b
```

Line L2 finds the lexicographic maximum in $n + 1$ stages. Stage 0 maximizes $c^T x$. Stage $k$ maximizes component $k$, but may only enter a nonbasic column whose reduced costs in all earlier stages are zero. A pivot on such a column keeps the earlier components fixed, so each stage is an ordinary simplex run on a face, and [Bland's rule](/bland-rule/) inside each stage prevents cycling. In practice the old basis is reused after each cut and the [dual simplex method](/dual-simplex-method/) restores feasibility, because the old vertex violates only the new row.

Line L7 is the fractional cut. Line L8 subtracts the cut from the row equation, which gives the [Chvátal-Gomory](/chvatal-gomory-cut/) form $v_j + \sum_h \lfloor d_{jh} \rfloor t_h \le \lfloor \bar v_j \rfloor$. Then it replaces each slack $t_h = s_r$ by $b_r - A_r x$. All the numbers stay integers, so the slack of the new row is an integer too, and later cuts may use it.

## Example

Maximize $x_2$ subject to $3x_1 + 2x_2 \le 6$, $-3x_1 + 2x_2 \le 0$, $x \ge 0$, $x \in \mathbb{Z}^2$, with slacks $s_1, s_2$. The integer points are $(0,0)$, $(1,0)$, $(2,0)$ and $(1,1)$, so the answer is $x^* = (1, 1)$ with value 1.

| round | LP vertex $\bar x$ | $\bar v$ | source row | Gomory cut | cut in $x$ |
|---|---|---|---|---|---|
| 1 | $(1, 3/2)$ | $(3/2, 1, 3/2)$ | $v_0 = 3/2 - \frac14 s_1 - \frac14 s_2$ | $\frac14 s_1 + \frac14 s_2 \ge \frac12$ | $x_2 \le 1$, slack $s_3$ |
| 2 | $(4/3, 1)$ | $(1, 4/3, 1)$ | $v_1 = 4/3 - \frac13 s_1 + \frac23 s_3$ | $\frac13 s_1 + \frac13 s_3 \ge \frac13$ | $x_1 + x_2 \le 2$ |
| 3 | $(1, 1)$ | $(1, 1, 1)$ | | | stop |

In round 1 the objective row is the first fractional component. With $s_1 = 6 - 3x_1 - 2x_2$ and $s_2 = 3x_1 - 2x_2$ the cut is $6 - 4x_2 \ge 2$, that is $x_2 \le 1$. In round 2 the objective value 1 is integral, and the optimal face is the segment from $(1, 1)$ to $(4/3, 1)$. The lexicographic rule picks its end with the largest $x_1$. Its row has $\operatorname{frac}(1/3) = 1/3$ and $\operatorname{frac}(-2/3) = 1/3$. With $s_3 = 1 - x_2$ the cut $s_1 + s_3 \ge 1$ becomes $x_1 + x_2 \le 2$, which is a facet of the [integer hull](/integer-hull/). The new lexicographic maximum $(1, 1)$ is integral.

## Correctness

Each cut is valid: at an integer point of $P_k$, the component $v_j$ and all $t_h$ are integers with $t_h \ge 0$, and the row equation gives $\sum_h \operatorname{frac}(d_{jh}) t_h \equiv \operatorname{frac}(\bar v_j) \pmod 1$, so the left side, which is $\ge 0$, is at least $\operatorname{frac}(\bar v_j)$. The cut is violated by $\bar x$, where all $t_h = 0$. So $P_k \cap \mathbb{Z}^n = P \cap \mathbb{Z}^n$ for all $k$, and an integral optimal vertex of $P_k$ is optimal for the integer program.

Termination rests on one fact. Because the vertex is the lexicographic maximum and the cut comes from the first fractional component $j$, each point of $P_{k+1}$ that agrees with $\bar v$ in components $0$ to $j - 1$ has $v_j \le \lfloor \bar v_j \rfloor$. The sequence of vertices decreases lexicographically, each component is bounded below on the bounded set $P$, and each fractional value forces a drop to an integer below it. So each component becomes a constant integer after finitely many rounds. The full proof is below.

## Complexity

Each round costs one LP solve over a system with $m + n + k$ inequalities after $k$ cuts. In exact rational arithmetic, each pivot costs $O((m + k)(n + m + k))$ operations on rationals. The lexicographic solve needs at most $n + 1$ simplex stages, and the number of pivots in a stage has no polynomial bound, as for the [simplex method](/simplex-method/) itself.

The number of rounds has no polynomial bound in the input size $L$. Take $P_t = \operatorname{conv}\{(0, 0), (0, 1), (t, 1/2)\}$, written as $x_1 - 2t x_2 \le 0$, $x_1 + 2t x_2 \le 2t$, and maximize $x_1$. The integer optimum is 0 and the LP optimum is $t$. After $k$ cuts the relaxation still contains the [Chvátal closure](/chvatal-closure/) $P_t^{(k)}$, which contains the point $(t - k/2, 1/2)$, so at least $2t$ rounds are necessary. The data have $O(\log t)$ bits, so the number of rounds is exponential in $L$. On this family the implementation below adds exactly $2t$ cuts for $t = 1$ to $6$.

The sizes of the numbers can also grow, which is why practical codes use floating point and safeguards, and why they add Gomory cuts in rounds inside [branch and cut](/branch-and-cut/) rather than run the pure method.

## Properties

- **Exact and finite.** With integer data, a bounded relaxation and the lexicographic rule, the method stops with a correct answer. Without the lexicographic rule, finiteness can fail.
- **Pure integer only.** The fractional cut needs every variable in the row, including slacks, to be an integer. For continuous variables, use the [Gomory mixed-integer cut](/gomory-mixed-integer-cut/).
- **Dual method.** The LP values $c^T \bar x$ decrease from the LP optimum to the integer optimum. No feasible integer point is known until the very end, so stopping early gives only a bound.
- **Tied to the Chvátal closure.** The cut of round $k$ is a Chvátal-Gomory cut of $P_{k-1}$, so by induction $P_k \supseteq P^{(k)}$, the $k$-th [Chvátal closure](/chvatal-closure/).

## Variants and improvements

- **Gomory mixed-integer cuts (1960).** The same tableau row, with a stronger formula that also handles continuous variables. Modern solvers use this version.
- **All-integer and primal methods.** Gomory's all-integer algorithm (1960) keeps the tableau integral by choosing cuts with pivot element $-1$. Primal methods by Young and by Glover move between integer points instead.
- **Rounds of cuts.** Add the cuts of all fractional rows at once, then solve again. This reduces the number of LP solves but makes the LPs larger.
- **Cut management.** Remove cuts that are no longer tight, and skip cuts that are almost parallel to others or have bad numerical properties.
- **Inside branch and cut.** Balas, Ceria, Cornuéjols and Natraj (1996) showed that Gomory cuts at the root node of [branch and cut](/branch-and-cut/) help much. Since then all major solvers use them.

## When to use it

Use the pure algorithm to teach cutting planes, to compute small examples exactly, and to explore the [Chvátal closure](/chvatal-closure/) of small polytopes. For real instances, use [branch and cut](/branch-and-cut/), which adds Gomory mixed-integer cuts together with problem-specific cuts such as [cover inequalities](/cover-inequality/), and branches when the cuts stall. When the constraint matrix is [totally unimodular](/total-unimodularity/), no cut is needed at all: the first LP vertex is integral.

## Pitfalls

- **Fractional slacks.** If $A$ or $b$ has fractional entries, a slack can be fractional at an integer point, and the cut of line L7 is not valid. Scale each row to integers first.
- **No lexicographic rule.** If line L2 returns any optimal vertex and line L6 picks any fractional row, the method may not stop. Keep both rules, or use a proved finite variant.
- **Floating point.** In floating point, a value such as $0.9999999$ looks fractional and its cut is nearly parallel to the objective, or a rounding error makes the cut invalid. Use exact rationals, as the implementation does, or tolerances and safety margins.
- **Unbounded relaxation.** The finiteness proof needs each component bounded below. Add bounds on the variables when the model has none.

## Implementations

## History

Ralph Gomory described the fractional cut and the finite method in a four-page note in 1958, and published the full proof in 1963. In 1960 he gave the mixed-integer cut and the all-integer algorithm. Chvátal (1973) found the same cuts in a geometric form and defined the closure and the rank. For many years Gomory cuts were seen as too slow in practice. The study of Balas, Ceria, Cornuéjols and Natraj (1996) changed this view, and the cuts became a standard part of [branch and cut](/branch-and-cut/).

## References
