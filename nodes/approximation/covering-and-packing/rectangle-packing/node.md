---
tag: RNFZP6
kind: problem
slug: rectangle-packing
name: Rectangle packing problem
aliases:
- two-dimensional bin packing
- 2D bin packing
- two-dimensional geometric bin packing
area: approximation/covering-and-packing
level: advanced
summary: Pack axis-parallel rectangles into the fewest fixed-size containers.
prereqs: [bin-packing, strip-packing, approximation-ratio, asymptotic-ptas]
see_also: [strip-packing, bin-packing, cutting-stock-problem, guillotine-cut-technique, bin-packing-aptas, configuration-lp, bin-packing-lower-bound, apx]
sources:
  - paper: "F. R. K. Chung, M. R. Garey and D. S. Johnson, On packing two-dimensional bins, SIAM Journal on Algebraic and Discrete Methods 3(1), 1982, pp. 66-76"
    title: Chung, Garey and Johnson 1982
    locator: the hybrid first fit algorithm and its asymptotic ratio 2.125
  - paper: "N. Bansal, J. R. Correa, C. Kenyon and M. Sviridenko, Bin packing in multiple dimensions: inapproximability results and approximation schemes, Mathematics of Operations Research 31(1), 2006, pp. 31-49"
    title: Bansal, Correa, Kenyon and Sviridenko 2006
    locator: the theorem that two-dimensional bin packing has no asymptotic PTAS unless P = NP
  - paper: "N. Bansal, A. Caprara and M. Sviridenko, A new approximation method for set covering problems, with applications to multidimensional bin packing, SIAM Journal on Computing 39(4), 2009, pp. 1256-1278"
    title: Bansal, Caprara and Sviridenko 2009
    locator: the round and approx framework and the asymptotic ratio 1 + ln 1.691
  - paper: "N. Bansal and A. Khan, Improved approximation algorithm for two-dimensional bin packing, SODA 2014, pp. 13-25"
    title: Bansal and Khan 2014
    locator: the asymptotic ratio 1.405
  - paper: "J. Y.-T. Leung, T. W. Tam, C. S. Wong, G. H. Young and F. Y. L. Chin, Packing squares into a square, Journal of Parallel and Distributed Computing 10(3), 1990, pp. 271-275"
    title: Leung, Tam, Wong, Young and Chin 1990
    locator: the NP-completeness of deciding whether a set of squares fits into one square
---

The rectangle packing problem, also called two-dimensional bin packing, asks for a placement of axis-parallel rectangles into the fewest unit squares, without overlap and without rotation. With all heights equal to 1 it is exactly [bin packing](/bin-packing/), so it is strongly NP-hard. Unlike one-dimensional bin packing, it has no asymptotic polynomial-time approximation scheme unless P = NP (Bansal, Correa, Kenyon and Sviridenko 2006). The best known asymptotic ratio is 1.405 (Bansal and Khan 2014), and the best possible absolute ratio is 2.

## In plain words

You have many rectangular pieces and a supply of equal square boards. Each piece must lie flat on a board, keep its direction, and not overlap other pieces. You want to use as few boards as possible.

A common method first puts the pieces in rows, from the tallest to the shortest, as if the boards were joined into one long strip. Then it puts whole rows onto boards, so that the rows on one board are not taller than the board. Two pieces that are each more than half as wide and more than half as tall as a board can never share a board. This simple fact already shows that the area of the pieces can be much less than the number of boards needed.

## Definition

The input is a list of rectangles $R_1, \ldots, R_n$; rectangle $R_i$ has width $w_i \in (0, 1]$ and height $h_i \in (0, 1]$. A packing into $m$ bins assigns to each $R_i$ a bin $b_i \in \{1, \ldots, m\}$ and a position $(x_i, y_i)$ with $0 \le x_i \le 1 - w_i$ and $0 \le y_i \le 1 - h_i$, such that for two rectangles in the same bin the open rectangles $(x_i, x_i + w_i) \times (y_i, y_i + h_i)$ are disjoint. $\mathrm{OPT}$ is the least $m$. We write $A = \sum_i w_i h_i$ for the total area.

*Ratio convention.* This is a minimization problem. An algorithm has asymptotic ratio $\rho$ if $\mathrm{ALG} \le \rho\,\mathrm{OPT} + c$ for a constant $c$ on every input, and absolute ratio $\rho$ if $\mathrm{ALG} \le \rho\,\mathrm{OPT}$ on every input. The analyses compare with two lower bounds on $\mathrm{OPT}$:

$$\mathrm{OPT} \ge \lceil A \rceil \qquad \text{and} \qquad \mathrm{OPT} \ge \bigl|\{ i : w_i > \tfrac12,\ h_i > \tfrac12 \}\bigr|.$$

The first holds because each bin has area 1. For the second, take two rectangles with width and height more than $\frac12$ in the same bin. Their $x$-intervals have length more than $\frac12$ inside $[0, 1]$, so they overlap; for the same reason their $y$-intervals overlap; so the rectangles overlap. Thus each bin holds at most one such rectangle.

## Variants

- **Rotations allowed.** Each rectangle may be turned by 90 degrees. Most algorithms and ratios have versions for this case.
- **Guillotine packings.** Each bin must be cut into its pieces by a sequence of edge-to-edge cuts; in $k$-stage packings the cuts alternate between horizontal and vertical at most $k$ times. See the [guillotine cut technique](/guillotine-cut-technique/).
- **Squares.** All rectangles are squares. This case has an asymptotic PTAS (Bansal, Correa, Kenyon and Sviridenko 2006).
- **Higher dimensions.** Boxes in unit cubes of dimension $d$.
- **Strip instead of bins.** One container of width 1 and unbounded height, with the height to minimize, is [strip packing](/strip-packing/).
- **High multiplicity.** Few rectangle types with large demands, as in two-dimensional [cutting stock](/cutting-stock-problem/).

## Examples

*The area bound can be far from the truth.* Four squares of side $0.6$ have $A = 1.44$, so $\lceil A \rceil = 2$, but each has width and height more than $\frac12$, so $\mathrm{OPT} = 4$. With $n$ such squares, $\mathrm{OPT} = n$ while $A = 0.36\,n$.

*A tight instance for the area bound.* Take two copies each of $P = (0.6, 0.6)$, $Q = (0.4, 0.6)$, $T = (0.6, 0.4)$ and $U = (0.4, 0.4)$, as (width, height). The area is $A = 2$, and one copy of each tiles a unit square: $P$ at $(0, 0)$, $Q$ at $(0.6, 0)$, $T$ at $(0, 0.6)$, $U$ at $(0.6, 0.6)$. So $\mathrm{OPT} = 2$. Hybrid first fit, below, also finds 2 bins:

| step | result |
|---|---|
| sort by height | $P, P, Q, Q$ (height 0.6), then $T, T, U, U$ (height 0.4) |
| first fit decreasing height into a strip | shelves $\{P, Q\}$, $\{P, Q\}$ of height 0.6 and $\{T, U\}$, $\{T, U\}$ of height 0.4 |
| first fit decreasing on shelf heights | bin 1 gets shelves of heights 0.6 and 0.4, bin 2 the same |

## Known algorithms

- **Hybrid first fit (HFF).** Pack the rectangles into shelves of width 1 by first fit decreasing height, as in [strip packing](/strip-packing/). Each shelf has a height at most 1. Then pack the shelves into bins as a one-dimensional bin packing of the shelf heights, by [first fit decreasing](/first-fit-decreasing/). Chung, Garey and Johnson (1982) proved asymptotic ratio at most 2.125. Time $O(n \log n)$.
- **Finite first fit and finite best strip.** Variants that pack shelves into bins directly, or that pack shelves by best fit. They are simple and fast in practice.
- **Caprara (2002 and 2008).** Asymptotic ratio $T_\infty \approx 1.691$, the harmonic constant of bin packing, with 2-stage guillotine packings.
- **Round and approx.** Bansal, Caprara and Sviridenko (2009) solve a [configuration LP](/configuration-lp/) over the patterns of a bin, round the solution randomly, and finish the rest with an algorithm that has a subset oblivious property. This gives asymptotic ratio $1 + \ln 1.691 \approx 1.525$.
- **Bansal and Khan (2014).** Asymptotic ratio $1 + \ln 1.5 \approx 1.405$, by a structural result that packings where each bin has a few compartments are almost optimal.
- **Absolute ratio 2.** Harren and van Stee, and Jansen, Prädel and Schwarz (both 2009), give algorithms with $\mathrm{ALG} \le 2\,\mathrm{OPT}$ on every input.

## Bounds

| claim | statement | source |
|---|---|---|
| lower bounds | $\mathrm{OPT} \ge \lceil A \rceil$ and $\mathrm{OPT} \ge$ the number of rectangles with both sides above $\frac12$ | proved above |
| HFF | asymptotic ratio at most 2.125 | Chung, Garey and Johnson 1982 |
| best asymptotic | $1 + \ln 1.5 \approx 1.405$ | Bansal and Khan 2014 |
| no asymptotic PTAS | there is $\rho > 1$ such that no polynomial-time algorithm has asymptotic ratio below $\rho$, unless P = NP | Bansal, Correa, Kenyon and Sviridenko 2006 |
| best absolute | ratio 2 in polynomial time | Harren and van Stee 2009; Jansen, Prädel and Schwarz 2009 |
| absolute hardness | no polynomial-time algorithm has absolute ratio below 2, unless P = NP | from squares into one square, below |

*The absolute bound 2 is best possible.* Deciding whether a given set of squares fits into one unit square is NP-complete (Leung, Tam, Wong, Young and Chin 1990). Suppose an algorithm has $\mathrm{ALG} < 2\,\mathrm{OPT}$ on every input. If the squares fit into one bin, then $\mathrm{OPT} = 1$ and $\mathrm{ALG} < 2$, so $\mathrm{ALG} = 1$. If not, $\mathrm{ALG} \ge \mathrm{OPT} \ge 2$. So the algorithm decides the NP-complete question, and P = NP. In one dimension the same argument gives only $\frac32$, because there the question "do the items fit into 2 bins" is the hard one.

## Reductions

- **From bin packing.** Give each item of size $s_i$ the rectangle $(s_i, 1)$. Each such rectangle spans the full height of a bin, so the rectangles in one bin have disjoint $x$-intervals and widths of total at most 1. So the two problems have the same optimum, and rectangle packing is strongly NP-hard.
- **Through strip packing.** A shelf packing in a strip of width 1 becomes a bin packing of the shelves, with the shelf heights as item sizes. This is the scheme behind HFF and many later algorithms.
- **Large rectangles.** For a list of squares with side more than $\frac12$, the answer is the number of squares; the hardness in the asymptotic case comes from rectangles with one long side, where Bansal, Correa, Kenyon and Sviridenko reduce from a bounded version of [3-dimensional matching](/three-dimensional-matching/).

## Applications

- **Cutting sheets.** Cutting rectangular parts from standard sheets of wood, glass, metal or paper, to use the fewest sheets; in practice guillotine cuts are often required.
- **Pallet and container loading.** Placing boxes of equal height on standard pallets, seen from above.
- **Page layout.** Placing advertisements or pictures on pages of fixed size, to use the fewest pages.
- **Resource allocation over time.** Jobs that need a block of contiguous memory for some time, with a fixed number of machines, each with a fixed time horizon.

## References
