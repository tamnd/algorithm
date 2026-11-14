---
tag: 6QQEE4
kind: algorithm
slug: lp-density-fill
name: Linear programming fill synthesis
aliases:
- Kahng-Robins-Singh-Zelikovsky fill
- LP-based dummy fill
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Kahng, Robins, Singh and Zelikovsky's fill method that solves a linear program over fixed dissections to minimize the largest window density variation.
model: word-ram
complexity:
  vars: {m: the number of tiles on a side, r: the number of tiles on a side of a window}
  time: {build: "O(m^2 r^2)"}
  space: {extra: "O(m^4)"}
properties: {deterministic: true, exact: true, recursive: false, online: false}
history:
  year: 1999
  people: [Andrew B. Kahng, Gabriel Robins, Anish Singh, Alexander Zelikovsky]
  note: Kahng, Robins, Singh and Zelikovsky gave the first min-variation fill formulation as a linear program over a fixed r-dissection in 1999, after their 1998 analysis of fixed against floating windows with Wang.
prereqs: [dummy-fill-problem, linear-programming-problem, simplex-method]
see_also: [lp-duality, strong-duality, karmarkar-algorithm, interior-point-method, binary-integer-programming, prefix-sums, critical-area]
sources:
  - paper: "Andrew B. Kahng, Gabriel Robins, Anish Singh and Alexander Zelikovsky, Filling algorithms and analyses for layout density control, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 18(4), 445 to 462, April 1999"
    locator: the filling problem for a fixed r-dissection, with a fill variable per tile bounded by the tile slack and the linear program that maximizes the minimum window density under the upper bound U
  - paper: doi:10.1145/274535.274549
    title: Andrew B. Kahng, Gabriel Robins, Anish Singh, Huijuan Wang and Alexander Zelikovsky, Filling and slotting, analysis and algorithms, Proceedings of the International Symposium on Physical Design (ISPD), 95 to 102, 1998
    locator: Theorem 8, the bounds L - 1/r + 1/(4r^2) and U + 1/r - 1/(4r^2) on the density of any window when all windows of the fixed r-dissection satisfy [L, U], and their tightness
  - paper: doi:10.1109/TCAD.2007.907061
    title: Andrew B. Kahng and Kambiz Samadi, CMP fill synthesis, a survey of recent studies, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 27(1), 3 to 19, January 2008
    locator: Section IV-B, part 1 on LP-based and Monte Carlo methods, which restates the min-variation LP, the min-fill LP of Tian et al., and the Monte Carlo and greedy fill of Chen, Kahng, Robins and Zelikovsky
---

Linear programming fill synthesis solves the [dummy fill problem](/dummy-fill-problem/) on a fixed grid of tiles. Kahng, Robins, Singh and Zelikovsky observed that once the layout is cut into tiles and the windows are blocks of tiles, the density of a window is a sum of tile amounts, so the min-variation objective becomes a [linear program](/linear-programming-problem/) with one fill variable per tile. The linear program gives the exact optimum for the tiled problem. A geometric lemma from their 1998 paper bounds how far the true sliding windows can then be from the tiled ones, which this page proves.

## In plain words

The chip is cut into a grid of equal tiles, and a window is a square block of tiles. For each tile we know how much metal it already has and how much free space can take fill.

We choose how much fill to put in each tile. A window's metal is the sum over its tiles, so every rule is a sum: no window may go above the upper limit, and we want the emptiest window as full as possible.

Such a set of sums and limits is a linear program, and a standard solver finds the best amounts exactly. Then fill shapes are drawn in each tile to match its amount.

Windows that slide between grid lines are not checked, but their density can differ only by a known small amount, which shrinks as the tiles get finer.

## The problem

**Input.** An $m \times m$ grid of tiles $T_{ij}$ of side $t$, with the feature area $a_{ij} = \operatorname{area}(F \cap T_{ij})$ and the slack $s_{ij}$, the area in $T_{ij}$ where fill may go. An integer $r \ge 1$; the windows are the $(m - r + 1)^2$ blocks $W$ of $r \times r$ tiles, of side $w = rt$ and area $w^2$. An upper density bound $U$.

**Assumption.** Any amount $p_{ij} \in [0, s_{ij}]$ of fill can be drawn in the slack of $T_{ij}$. This is the continuous model; it holds approximately when fill shapes are small against the tile.

**Output.** Fill amounts $p_{ij}$ that maximize the minimum window density

$$ \min_W \frac{1}{w^2} \sum_{T_{ij} \subseteq W} (a_{ij} + p_{ij}) \quad \text{subject to} \quad 0 \le p_{ij} \le s_{ij}, \qquad \frac{1}{w^2} \sum_{T_{ij} \subseteq W} (a_{ij} + p_{ij}) \le U \text{ for every } W, $$

or a report that no fill meets the upper bound.

## The algorithm

Write $a(W) = \sum_{T_{ij} \subseteq W} a_{ij}$ and $p(W) = \sum_{T_{ij} \subseteq W} p_{ij}$. The variable $M$ stands for the area of the emptiest window.

```pseudo id=main
LP-DENSITY-FILL(a, s, r, U, w)
L1  if a(W) > U·w² for some window W then return infeasible
L2  variables: p_ij for every tile, and M
L3  objective: maximize M
L4  for every tile T_ij:  p_ij ≤ s_ij
L5  for every window W:   p(W) ≤ U·w² − a(W)
L6  for every window W:   M − p(W) ≤ a(W)
L7  solve with the simplex method from the origin (all p_ij = 0, M = 0)
L8  return M / w², and the amounts p_ij
```

All variables are nonnegative. Line L1 makes every right-hand side nonnegative, so the origin is a feasible start and the simplex method needs no first phase. Line L6 says $M \le a(W) + p(W)$, so at the optimum $M$ equals the smallest window area. After line L8, fill shapes of total area $p_{ij}$ are drawn in the slack of each tile, for example as a regular array of squares.

The implementation is a dense [simplex method](/simplex-method/) in exact rational arithmetic with Bland's rule, which prevents cycling. It also returns the dual solution, so the tests can check [strong duality](/strong-duality/) as a certificate of optimality without trusting the pivots.

## Example

Take a $3 \times 3$ grid of unit tiles, windows of $2 \times 2$ tiles ($r = 2$, $w = 2$, $w^2 = 4$) and $U = \frac{1}{2}$. Rows are listed from the top:

| | feature area $a_{ij}$ | slack $s_{ij}$ |
|---|---|---|
| row 0 | 0.6, 0.2, 0.1 | 0.1, 0.4, 0.5 |
| row 1 | 0.5, 0.3, 0.0 | 0.2, 0.3, 0.6 |
| row 2 | 0.4, 0.1, 0.0 | 0.3, 0.5, 0.2 |

There are four windows. Name them by their top-left tile: $W_{00}$, $W_{01}$, $W_{10}$ and $W_{11}$. Their feature areas are $1.6$, $0.6$, $1.3$ and $0.4$, densities $0.4$, $0.15$, $0.325$ and $0.1$. The upper bound allows each window an area of $2$.

The solver returns $M / w^2 = \frac{19}{40} = 0.475$. One optimal fill, row by row, is $(0, 0.1, 0.3)$, $(0, 0.3, 0.6)$, $(0, 0.4, 0.2)$, which gives window densities $0.5$, $0.475$, $0.5$ and $0.475$.

Why not $0.5$? Window $W_{11}$ has feature area $0.4$ and needs fill $4M - 0.4$ from tiles $(1,1)$, $(1,2)$, $(2,1)$ and $(2,2)$. Tiles $(1,2)$ and $(2,2)$ give at most $0.6 + 0.2$, so $p_{11} + p_{21} \ge 4M - 1.2$. But tiles $(1,1)$ and $(2,1)$ also lie in $W_{10}$, which has room for only $2 - 1.3 = 0.7$ more, so $p_{11} + p_{21} \le 0.7$. Hence $4M \le 1.9$ and $M / w^2 \le 0.475$. This chain of inequalities is a dual solution of the linear program, and it is what the dual certificate in the tests checks in general.

With $U = 0.3$ line L1 reports infeasible, since $W_{00}$ already has density $0.4$.

## Correctness

The [full proof](proofs/correctness.md) shows the following.

**The linear program is the tiled problem.** Every feasible fill gives a feasible point $(p, M)$ with $M$ the smallest window area, and every feasible point gives a feasible fill whose smallest window area is at least $M$. So the optimum of the linear program, divided by $w^2$, is the best minimum density on the fixed dissection, and the optimal $p$ is an optimal fill. The program is feasible after line L1 and bounded, so the simplex method returns an optimum.

**Fixed windows against floating windows.** If every window of the fixed $r$-dissection has density in $[L, U]$, then every $w \times w$ window, at any position, has density in $[L - \varepsilon_r, U + \varepsilon_r]$ with

$$ \varepsilon_r = \frac{1}{r} - \frac{1}{4r^2}. $$

The proof moves a floating window to the nearest fixed window, which is at most $t/2$ away in each coordinate, and bounds the area they do not share. This is Theorem 8 of Kahng et al. (1998). A square of features placed at offset $(t/2, t/2)$ shows the bound is attained.

**What the fill achieves for floating windows.** The fixed problem is a relaxation of the floating one, so its optimum $M^*$ is at least the best floating minimum. With the LP fill, every floating window has density at least $M^*/w^2 - \varepsilon_r$ and at most $U + \varepsilon_r$. So the LP fill is within $\varepsilon_r$ of the floating optimum, and it exceeds the floating upper bound by at most $\varepsilon_r$.

**What is not proved here.** The correctness and termination of the simplex method with Bland's rule are cited from the [simplex method](/simplex-method/) page; the tests confirm each returned optimum with a dual certificate. The claim that the slack can be filled by any amount is a modeling assumption, not a theorem.

## Complexity

The program has $m^2 + 1$ variables and $m^2 + 2(m - r + 1)^2$ constraints. Each window constraint has $r^2 + 1$ nonzero entries, so building it costs $O(m^2 r^2)$. A dense tableau has $O(m^4)$ entries.

The time to solve depends on the solver. The simplex method takes few pivots in practice but an exponential number on some inputs. Interior point methods such as [Karmarkar's algorithm](/karmarkar-algorithm/) solve it in time polynomial in its size and the bit length of the data. On the test instances, with up to $m = 6$, the exact solver takes well under a second.

The size grows with $r^2$ for a fixed window: halving $\varepsilon_r$ needs about twice the $r$ and four times the variables. For large layouts this growth is the reason for the Monte Carlo, greedy and hierarchical methods below, which Kahng and Samadi survey; they note that the Monte Carlo and greedy methods can end with a minimum density well below the optimum.

## Properties

- **Exact for the tiled problem.** With rational data the implementation returns the exact optimum and an optimal dual, so the result is certified.
- **Not unique.** Many fills reach the optimum. In the example, any fill within the slacks that keeps every window area between $1.9$ and $2$ is optimal.
- **Ignores coupling.** The objective sees only density. Where fill goes inside a tile, and how it couples to signal wires, is left to the placement step.
- **Error from the grid.** Densities of floating windows can differ from the fixed ones by up to $\varepsilon_r$, which is $0.75$, $0.4375$, $0.234$ and $0.061$ for $r = 1$, $2$, $4$ and $16$.

## Variants and improvements

- **Min-Fill.** Minimize $\sum p_{ij}$ subject to $L w^2 \le a(W) + p(W) \le U w^2$ for every window. Kahng and Samadi credit this linear program to Tian et al.
- **Variation budget.** Given a target density, minimize a budget $\varepsilon$ such that every window lies within $\varepsilon/2$ of the target, again a linear program (Tian et al., as surveyed by Kahng and Samadi).
- **Integer fill.** When fill comes in fixed squares, the amounts are integers and the problem is an [integer program](/binary-integer-programming/). Rounding the LP amounts down keeps every upper bound and loses less than one square per tile, so less than $r^2$ squares per window.
- **Monte Carlo and greedy.** Chen, Kahng, Robins and Zelikovsky (ASP-DAC 2000) add fill one unit at a time to a tile chosen at random with priority proportional to $U$ minus the smallest density of the windows that contain it, or to the tile of highest priority. These scale far better and give no optimality guarantee.
- **Model-based.** Replace window density by an effective density, a weighted sum over nearby tiles. The constraints stay linear, so the method still applies.

## When to use it

Use it when the grid is small enough for an LP solver, for example inside one block or as the exact core of a hierarchical method, and the density rule is the target. Use Monte Carlo or greedy fill for full chips, and a performance-aware method when the added coupling capacitance on critical nets matters.

## Pitfalls

- **Coarse grid.** With $r = 1$ the fixed windows can all meet the rule while a sliding window has density $\frac{3}{4}$ higher. Choose $r$ so that $\varepsilon_r$ is below the tolerance, or tighten $U$ by $\varepsilon_r$.
- **Slack is not free area.** The slack must exclude the buffer around signal wires and the space lost to fill design rules, or the amounts cannot be drawn.
- **Windows at the edge.** The grid must cover the layout so that every window lies inside; partial windows at the edge need their own rule.
- **Infeasible inputs.** If a window already exceeds $U$, no fill helps; the layout must change or wide wires must be slotted.

## Implementations

## History

Kahng, Robins, Singh, Wang and Zelikovsky stated the Filling and Slotting Problem in 1998 and proved the bound on the error of fixed dissections. In 1999 Kahng, Robins, Singh and Zelikovsky gave the min-variation linear program on a fixed dissection. Chen, Kahng, Robins and Zelikovsky followed with Monte Carlo, iterated and hierarchical methods from 2000 to scale to full chips, and Tian et al. gave min-fill and model-based linear programs.

## References
