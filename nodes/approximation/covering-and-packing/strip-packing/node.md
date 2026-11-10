---
tag: 3FHTTX
kind: problem
slug: strip-packing
name: Strip packing problem
aliases:
- two-dimensional strip packing
- strip packing
area: approximation/covering-and-packing
level: advanced
summary: Pack rectangles into a strip of fixed width minimizing total height.
prereqs: [bin-packing, approximation-ratio, next-fit-bin-packing, first-fit-decreasing]
see_also: [rectangle-packing, bin-packing, cutting-stock-problem, guillotine-cut-technique, bin-packing-aptas, makespan-minimization, partition-problem]
sources:
  - paper: "E. G. Coffman, M. R. Garey, D. S. Johnson and R. E. Tarjan, Performance bounds for level-oriented two-dimensional packing algorithms, SIAM Journal on Computing 9(4), 1980, pp. 808-826"
    title: Coffman, Garey, Johnson and Tarjan 1980
    locator: the shelf algorithms NFDH and FFDH and their bounds 2 OPT + h_max and 1.7 OPT + h_max
  - paper: "B. S. Baker, E. G. Coffman and R. L. Rivest, Orthogonal packings in two dimensions, SIAM Journal on Computing 9(4), 1980, pp. 846-855"
    title: Baker, Coffman and Rivest 1980
    locator: the bottom-left rule and its ratio 3
  - paper: "A. Steinberg, A strip-packing algorithm with absolute performance bound 2, SIAM Journal on Computing 26(2), 1997, pp. 401-409"
    title: Steinberg 1997
    locator: the main theorem
  - paper: "C. Kenyon and E. Rémila, A near-optimal solution to a two-dimensional cutting stock problem, Mathematics of Operations Research 25(4), 2000, pp. 645-656"
    title: Kenyon and Rémila 2000
    locator: the asymptotic FPTAS
  - paper: "R. Harren, K. Jansen, L. Prädel and R. van Stee, A (5/3 + epsilon)-approximation for strip packing, Computational Geometry 47(2), 2014"
    title: Harren, Jansen, Prädel and van Stee 2014
    locator: the main theorem
---

The strip packing problem asks for a placement of axis-parallel rectangles into a vertical strip of width 1, without overlap and without rotation, so that the height used is as small as possible. It is the two-dimensional version of [bin packing](/bin-packing/): with all heights equal to 1 and a packing in rows, it is exactly bin packing. It is NP-hard, no polynomial-time algorithm has absolute ratio below $\frac32$ unless P = NP, and the best known absolute ratio is $\frac53 + \varepsilon$. In the asymptotic sense the problem is almost solved: Kenyon and Rémila (2000) give height $(1 + \varepsilon)\,\mathrm{OPT} + O(1/\varepsilon^2)\,h_{\max}$ in polynomial time.

## In plain words

You have a long roll of material of a fixed width, and a set of rectangles to cut from it. Each rectangle must keep its direction. You want to place all the rectangles on the roll so that they do not overlap and the used length of the roll is as short as possible.

A simple method sorts the rectangles from the tallest to the shortest and places them in rows from left to right. When the next rectangle does not fit into the current row, a new row starts on top. Each row is as tall as its first rectangle. This uses at most about twice the area of the rectangles plus the height of the tallest rectangle.

## Definition

The input is a list of rectangles $R_1, \ldots, R_n$; rectangle $R_i$ has width $w_i \in (0, 1]$ and height $h_i > 0$. A packing assigns to each $R_i$ a position $(x_i, y_i)$ with $0 \le x_i \le 1 - w_i$ and $y_i \ge 0$, such that the open rectangles $(x_i, x_i + w_i) \times (y_i, y_i + h_i)$ are pairwise disjoint. Its height is $\max_i (y_i + h_i)$, and $\mathrm{OPT}$ is the least height. We write $A = \sum_i w_i h_i$ for the total area and $h_{\max} = \max_i h_i$.

*Ratio convention.* An algorithm has absolute ratio $\rho$ if its height is at most $\rho\,\mathrm{OPT}$ on every input. Bounds of the form $\rho\,\mathrm{OPT} + c\,h_{\max}$ are asymptotic: the term $h_{\max}$ is small compared with $\mathrm{OPT}$ when there are many rectangles. The basic lower bounds are

$$\mathrm{OPT} \ge A \qquad \text{and} \qquad \mathrm{OPT} \ge h_{\max}.$$

## Variants

- **Rotations allowed.** Each rectangle may be turned by 90 degrees.
- **Shelf (level) packings.** The rectangles are placed in horizontal shelves, and each rectangle stands on the floor of its shelf. Many algorithms build such packings.
- **Guillotine packings.** The packing must be cut out by a sequence of edge-to-edge cuts; see the [guillotine cut technique](/guillotine-cut-technique/).
- **Online strip packing.** The rectangles arrive one by one.
- **Fixed number of bins or machines.** With heights read as processing times and widths as numbers of machines, strip packing is scheduling of parallel jobs that need contiguous machines; with all widths equal to $1/m$, it is [makespan minimization](/makespan-minimization/) on $m$ machines.
- **Bins instead of a strip.** Packing rectangles into the fewest unit squares is [rectangle packing](/rectangle-packing/).

## Examples

Take a strip of width 1 and five rectangles (width, height): $R_1 = (0.6, 3)$, $R_2 = (0.5, 2)$, $R_3 = (0.4, 2)$, $R_4 = (0.3, 1)$, $R_5 = (0.7, 1)$. The area is $A = 4.6$ and $h_{\max} = 3$.

| shelf | height | rectangles | used width |
|---|---|---|---|
| 1 | 3 | $R_1$ | 0.6 |
| 2 | 2 | $R_2, R_3$ | 0.9 |
| 3 | 1 | $R_4, R_5$ | 1.0 |

This is the packing of next fit decreasing height (NFDH), with height 6. It is optimal, although $A = 4.6$: the widths of $R_1$, $R_2$, $R_5$ add up to more than 1 in each pair, so no two of them can stand side by side, and their $x$-intervals pairwise overlap. Intervals on a line that pairwise overlap have a common point, so one vertical line meets all three rectangles, and the height is at least $3 + 2 + 1 = 6$.

## Known algorithms

- **Next fit decreasing height (NFDH).** Sort by decreasing height. Put each rectangle to the right of the previous one on the current shelf if it fits; otherwise open a new shelf on top, as tall as this rectangle. Time $O(n \log n)$.
  *Theorem.* NFDH has height at most $2A + h_{\max} \le 3\,\mathrm{OPT}$. *Proof.* Let the shelves have heights $H_1 \ge H_2 \ge \cdots \ge H_t$, where $H_j$ is the height of the first rectangle of shelf $j$. For $j < t$, the first rectangle $F_{j+1}$ of shelf $j+1$ did not fit on shelf $j$, so the used width $U_j$ of shelf $j$ plus $w(F_{j+1})$ is more than 1. Each rectangle on shelf $j$ has height at least $H_{j+1}$, and $F_{j+1}$ has height $H_{j+1}$, so the area of shelf $j$ plus the area of $F_{j+1}$ is at least $H_{j+1}(U_j + w(F_{j+1})) > H_{j+1}$. Summing over $j < t$ counts each rectangle at most twice, so $2A > H_2 + \cdots + H_t$. The height is $H_1 + \cdots + H_t < h_{\max} + 2A$. $\square$
- **First fit decreasing height (FFDH).** As NFDH, but put each rectangle on the lowest shelf where it fits. Height at most $1.7\,\mathrm{OPT} + h_{\max}$ (Coffman, Garey, Johnson and Tarjan 1980), with a proof based on the 1.7 analysis of [first fit](/first-fit-bin-packing/).
- **Bottom-left.** Place each rectangle as low as possible, then as far left as possible. With the rectangles sorted by decreasing width, the height is at most $3\,\mathrm{OPT}$ (Baker, Coffman and Rivest 1980).
- **Absolute ratios.** Sleator (1980) reached 2.5, Steinberg (1997) and Schiermeyer (1994) reached 2, and Harren, Jansen, Prädel and van Stee (2014) reached $\frac53 + \varepsilon$.
- **Asymptotic schemes.** Kenyon and Rémila (2000) round the widths by grouping, solve a [configuration LP](/configuration-lp/) for the wide rectangles, and add the narrow ones by a shelf rule, for height $(1 + \varepsilon)\,\mathrm{OPT} + O(1/\varepsilon^2)\,h_{\max}$ in time polynomial in $n$ and $1/\varepsilon$.
- **Pseudo-polynomial time.** If the running time may be polynomial in the numbers, ratios below $\frac32$ are possible; Nadiradze and Wiese (2016) gave $\frac75 + \varepsilon$.

## Bounds

| claim | statement | source |
|---|---|---|
| NFDH | $\le 2A + h_{\max} \le 2\,\mathrm{OPT} + h_{\max}$; asymptotic ratio 2 | proved above; Coffman et al. 1980 |
| FFDH | $\le 1.7\,\mathrm{OPT} + h_{\max}$ | Coffman et al. 1980 |
| best absolute | $\frac53 + \varepsilon$ | Harren et al. 2014 |
| hardness, absolute | no ratio below $\frac32$ unless P = NP | from partition, below |
| asymptotic | $(1 + \varepsilon)\,\mathrm{OPT} + O(1/\varepsilon^2)\,h_{\max}$ | Kenyon and Rémila 2000 |

*NFDH can reach ratio near 2.* Take $2N$ rectangles with heights decreasing slowly from 1, and widths alternating $\frac12$ and a tiny $\eta$, starting with $\frac12$. Each shelf of NFDH takes one rectangle of width $\frac12$ and one of width $\eta$, because the next rectangle of width $\frac12$ does not fit, so NFDH has height about $N$. Putting the wide rectangles two per row and the narrow ones side by side in one row gives height about $\frac N2 + 1$.

## Reductions

- **From bin packing.** Give each item of a bin packing list a rectangle of width $s_i$ and height 1. *Claim:* a packing of height $H$ gives a bin packing with $\lfloor H \rfloor$ bins. *Proof.* Take the rectangles in the order of increasing $y_i$, and move each one straight down until it touches the floor or the top of a rectangle below it whose $x$-interval overlaps its own. The rectangles that it can touch were moved before it, so by induction their $y$ values are integers, and so its new $y$ value is an integer too. No overlap appears and the height does not grow. Now each rectangle lies in a row $[y, y+1]$ with integer $y < H$, and the rectangles in one row have disjoint $x$-intervals, so each row is a bin. $\square$ So strip packing contains bin packing and is strongly NP-hard.
- **The $\frac32$ bound from partition.** Take a [partition](/partition-problem/) instance with total $2B$ and use the bin packing list $a_i / B$ as above. If a partition exists, $\mathrm{OPT} = 2$. If not, a packing of height less than 3 would give 2 bins by the claim, so $\mathrm{OPT} \ge 3$. So an algorithm with absolute ratio below $\frac32$ would decide partition.
- **To scheduling.** Strip packing with the extra rule that each rectangle uses a set of machines, not necessarily contiguous, is scheduling of parallel tasks; the shelf algorithms apply there as well.

## Applications

- **Cutting from rolls.** Cutting rectangular pieces of cloth, paper, glass or steel from a roll of fixed width, to use the least length.
- **Scheduling with contiguous resources.** Jobs that need a block of adjacent processors or memory cells for some time, with time as the height.
- **Layout.** Placing modules on a chip of fixed width, or pictures on a web page of fixed width.

## References
