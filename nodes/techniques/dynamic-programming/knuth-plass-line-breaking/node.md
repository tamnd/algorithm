---
tag: RPQTNB
kind: algorithm
slug: knuth-plass-line-breaking
name: Knuth-Plass line breaking algorithm
aliases:
- TeX line breaking
- total-fit line breaking
area: techniques/dynamic-programming
level: advanced
summary: DP line breaking used by TeX that minimises the total badness of a paragraph.
solves: [optimal-text-wrapping]
model: word-ram
complexity:
  vars: {m: the number of items of the paragraph, A: the largest number of active nodes}
  time: {worst: O(m A), average: O(m A), best: Θ(m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1981
  people: [Donald E. Knuth, Michael F. Plass]
  note: Knuth and Plass described the total-fit line breaking method of TeX, with the box, glue and penalty model, in Software, Practice and Experience in 1981.
prereqs: [optimal-text-wrapping, dp-on-dag, prefix-sums]
see_also: [optimal-text-wrapping, printing-neatly, dp-on-dag, shortest-path, monge-property, linked-list]
sources:
  - paper: doi:10.1002/spe.4380111102
    title: Donald E. Knuth and Michael F. Plass, Breaking paragraphs into lines, Software, Practice and Experience 11(11), 1119-1184, 1981
    locator: the box, glue and penalty model, the adjustment ratio, badness, demerits, fitness classes, and the algorithm with active and passive nodes
  - paper: doi:10.1137/0216043
    title: D. S. Hirschberg and L. L. Larmore, The least weight subsequence problem, SIAM Journal on Computing 16(4), 628-638, 1987
    locator: line breaking as a least weight subsequence problem
---

The Knuth-Plass algorithm breaks a paragraph into lines for typesetting, and it is the line breaking method of TeX. The paragraph is a sequence of **boxes** (letters or words, with fixed width), **glue** (spaces, with a natural width that can stretch and shrink) and **penalties** (possible breaks, such as hyphens, with a cost). For each candidate line, the algorithm measures how much its glue must stretch or shrink, turns this into a **badness**, and adds a cost for the break into the **demerits** of the line. It then chooses the breaks that minimize the total demerits of the whole paragraph, so a good line can be given up to avoid a bad line later. This is a shortest path in a DAG over the break points, the "total-fit" method, against the "first-fit" method that fills one line at a time. The algorithm keeps only the **active** break points, the ones that can still start a line, which makes it fast in practice. The underlying optimization problem, with simpler costs, is [optimal text wrapping](/optimal-text-wrapping/); [printing neatly](/printing-neatly/) is the CLRS version for monospaced text.

## In plain words

A printed line must be exactly as wide as the column, so the spaces between words are made a bit wider or narrower. A line whose spaces change a lot looks bad, and a line whose spaces would have to shrink more than they can is not allowed.

Each line gets a score from how much its spaces change, plus a score for where it ends: ending at a hyphen costs more. Then all the line ends of the paragraph are chosen together, so that the sum of the scores is smallest.

Go through the possible line ends from left to right, and for each one keep the best way to reach it from an earlier line end. An earlier line end that is too far back to start a line that fits is never used again, so it is dropped.

## The problem

A paragraph is a sequence of items $x_0, \ldots, x_{m-1}$. Each item is one of:

- a **box** of width $w \ge 0$;
- a **glue** of width $w \ge 0$, stretch $y \ge 0$ (possibly $\infty$) and shrink $z$ with $0 \le z \le w$;
- a **penalty** of width $w \ge 0$, cost $p \in [-\infty, \infty]$ and a flag (set for hyphens). A penalty $p = \infty$ forbids a break; $p = -\infty$ forces one.

The last item is a forced penalty, usually after a glue of infinite stretch that fills the last line.

**Legal breaks.** A break may be at a penalty with $p < \infty$, or at a glue that follows a box. A break at glue removes that glue. After a break, the glue and penalties up to the next box or forced penalty are dropped. A paragraph is a sequence of legal breaks $b_1 < \cdots < b_k = m - 1$ that contains every forced break.

**Measures of a line.** For the line from a break $a$ (or the start, $a = -1$) to a break $b$: its natural width $L_{ab}$ is the sum of the box and glue widths in it, plus the width of $x_b$ if $x_b$ is a penalty (the hyphen); its stretch $Y_{ab}$ and shrink $Z_{ab}$ are the sums over its glue. For the line width $L$, the **adjustment ratio** is

$$r = \frac{L - L_{ab}}{Y_{ab}} \text{ if } L_{ab} < L, \qquad r = \frac{L - L_{ab}}{Z_{ab}} \text{ if } L_{ab} > L, \qquad r = 0 \text{ if } L_{ab} = L,$$

with $r = \infty$ or $r = -\infty$ when the divisor is 0. The **badness** is $\beta = \min(100 |r|^3, 10000)$, the cap that TeX uses. The line is **feasible** if $r \ge -1$ (the glue cannot shrink more than its shrink) and $\beta \le \rho$ for a tolerance $\rho$.

**Fitness class.** Tight if $r < -0.5$, decent if $-0.5 \le r \le 0.5$, loose if $0.5 < r \le 1$, very loose if $r > 1$.

**Demerits of a line.** With a line penalty $\ell$ and the penalty $p$ at the break ($p = 0$ at glue), this page uses the form that TeX uses:

$$\delta = \begin{cases} (\ell + \beta)^2 + p^2 & \text{if } p \ge 0, \\ (\ell + \beta)^2 - p^2 & \text{if } -\infty < p < 0, \\ (\ell + \beta)^2 & \text{if } p = -\infty, \end{cases}$$

plus $\alpha$ if this line and the line before both end at flagged penalties (two hyphens in a row), plus $\gamma$ if the fitness classes of this line and the line before differ by more than 1 (the line before the first line counts as decent).

**Goal.** A paragraph whose lines are all feasible, with the least total demerits.

## The algorithm

Each **node** is a break position $a$ with the fitness class $c$ of the line that ends there, the least total demerits $D$ to reach it, and a link to the node before it. The demerits of the next line depend on the past only through $a$ and $c$, so one node per pair $(a, c)$ is enough. With prefix sums of the widths, stretches and shrinks, each line is measured in $O(1)$ time.

```pseudo id=main
KNUTH-PLASS(x_0 .. x_{m−1}, L, ρ, ℓ, α, γ)
L1  active ← { node(position −1, class decent, D 0, link nil) }
L2  for b ← 0 to m − 1 do
L3      if b is not a legal break then continue
L4      best[c] ← none for each class c
L5      for each node a in active do
L6          r ← adjustment ratio of the line from a to b
L7          if r ≥ −1 and badness(r) ≤ ρ then
L8              d ← D(a) + demerits of the line from a to b
L9              if d < D(best[class(r)]) then best[class(r)] ← (d, a)
L10         keep a only if x_b is not forced and its line to b at full shrink, without x_b, is at most L
L11     active ← the kept nodes
L12     for each class c with best[c] ≠ none do add node(b, c, best[c]) to active
L13 if active has no node at m − 1 then return failure
L14 take the node at m − 1 with least D, and follow the links back to the start
L15 return D and the break positions
```

Lines L5 to L9 are the relaxation step of a shortest path in the DAG of nodes. Line L10 is the pruning: the width of a line at full shrink can only grow when the line is extended, because every box and every glue (width minus shrink) adds a nonnegative amount. So once a line from $a$ is too wide even at full shrink, every longer line from $a$ is too, and $a$ is never needed again. A forced break also ends every line that starts before it, so it clears the list. Knuth and Plass deactivate a node when $r < -1$ at a break; line L10 uses the same test without the width of the break item, which keeps the monotonicity exact when a hyphen has a width.

## Example

Take the words of "Dynamic programming finds the best way to break a paragraph into lines" as boxes of width equal to the number of letters, glue of width 1, stretch 1 and shrink 1 between them, the usual ending (a penalty $\infty$, a glue of infinite stretch, a forced break), $L = 19$, $\rho = \infty$, $\ell = 10$ and $\alpha = \gamma = 3000$. The algorithm returns:

| line | natural width | stretch or shrink | $r$ | badness | demerits |
|---|---|---|---|---|---|
| `Dynamic programming` | 19 | | 0 | 0 | 100 |
| `finds the best way` | 18 | stretch 3 | 1/3 | 3.70 | 187.79 |
| `to break a paragraph` | 20 | shrink 3 | −1/3 | 3.70 | 187.79 |
| `into lines` | 10 | stretch $\infty$ | 0 | 0 | 100 |

All four lines are decent, so no $\gamma$ is added, and the total is about 575.58. The first-fit method, which puts as many words on each line as fit with shrinking, makes `Dynamic programming` / `finds the best way to` ($r = -1/2$) / `break a paragraph into` ($r = -1$) / `lines`, with demerits $100 + 506.25 + 12100 + 100 = 12806.25$: its third line has its spaces shrunk to nothing. A search over all sets of breaks confirms the optimum.

## Correctness

The key claim is that a node for $(b, c)$ is created exactly when some feasible sequence of lines ends at $b$ with a line of class $c$, and that its value $D$ is the least total demerits of such a sequence. The proof is by induction on $b$. The demerits of a line depend only on its two ends, the class of the line before it and whether that line ended at a flagged penalty, so the best prefix can be swapped in (the [cut-and-paste argument](/cut-and-paste-argument/)). Pruning removes only nodes that cannot start a feasible line to $b$ or to any later break. The full proof is in the proof file below.

## Complexity

Each legal break $b$ is compared with each active node in $O(1)$ time, so the time is $O(m A)$, where $A$ is the largest size of the active list, and the extra space is $\Theta(m)$, since at most four nodes are created per break. Since a feasible line has bounded width, $A$ is at most four times the number of legal breaks that fit in a line at full shrink, which is small for real text. In the worst case, with very stretchable glue, every earlier break stays active and the time is $O(m^2)$. When a line holds a bounded number of legal breaks, $A$ is a constant and the time is $\Theta(m)$, which is also a lower bound, since every item is read.

## Properties

- **Exact for its model.** It returns a paragraph of least total demerits among those with feasible lines.
- **Fails on purpose.** If no paragraph has all lines feasible, it reports failure. TeX then runs again with a larger tolerance, or allows an overfull line.
- **Not greedy.** A break that is fine locally can be rejected because of its effect on later lines.
- **Iterative and online in the input.** It reads the items once from left to right.

## Variants and improvements

- **Varying line lengths.** For a paragraph with different line widths (for example around a figure), the width depends on the line number, and a node is then a triple (position, line number, class). Knuth and Plass handle this case.
- **Looseness.** TeX can ask for a paragraph with one line more or fewer than the optimum, which also needs the line number in the node.
- **Faster algorithms.** Without the fitness and hyphen terms and with a cost that is a convex function of the slack, the problem is a concave least weight subsequence problem and can be solved in $O(m)$ time; see [optimal text wrapping](/optimal-text-wrapping/).
- **Simplified versions.** Many text tools use only boxes and glue, with badness and line penalty, and drop the classes and flags.

## When to use it

Use it for justified text where quality matters: typesetting, document formatters, and narrow columns. For plain text in a monospaced font, the simpler dynamic program of [printing neatly](/printing-neatly/) is enough. For interactive editing of long documents, first-fit is faster and does not move earlier lines when the end of a paragraph changes.

## Pitfalls

- **Infinite values.** The final glue has infinite stretch, so its line has $r = 0$; a forced break at the end must not add a penalty term. Code that uses large finite numbers for infinity must keep them out of the sums.
- **Glue at the break.** The glue at a break belongs to no line, and the glue and penalties right after a break are dropped. Counting them makes the widths wrong.
- **Pruning too early.** Removing a node as soon as one line from it is infeasible is wrong: a line that is too loose now can become feasible with more words. Only lines that are too wide, or a forced break, end a node.
- **One node per position is not enough.** The fitness term $\gamma$ depends on the class of the line before, so the best node for a position may lose to a more expensive node of another class later.

## Implementations

## History

Donald Knuth developed the algorithm with Michael Plass for TeX, and they described it in "Breaking paragraphs into lines" in 1981, with the box, glue and penalty model, the comparison with first-fit, and the handling of hyphens, varying line widths and looseness. Hirschberg and Larmore later used line breaking as the main example of the least weight subsequence problem, for which faster algorithms exist under the Monge property.

## References
