---
tag: 5FH55N
kind: definition
slug: half-perimeter-wirelength
name: Half-perimeter wirelength
aliases:
- HPWL
- bounding box wirelength
area: eda/partitioning-floorplanning-and-placement
level: intro
summary: Half the perimeter of the bounding box of a net's pins, exact for nets of two or three pins and the standard estimate of routed wire length.
prereqs: [hypergraph]
see_also: [placement-problem, rectilinear-steiner-tree-problem, hanan-theorem, clique-net-model, log-sum-exp-wirelength, quadratic-placement, min-cut-placement, flute]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (the wirelength objective and its estimates, including the half-perimeter of the bounding box)
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on placement (estimates of wire length used by placement algorithms)
  - paper: doi:10.1137/0114025
    title: M. Hanan, On Steiner's problem with rectilinear distance, SIAM Journal on Applied Mathematics 14(2), 255 to 265, 1966
    locator: the reduction of the rectilinear Steiner problem to the grid of horizontal and vertical lines through the points
---

The half-perimeter wirelength (HPWL) of a net is the width plus the height of the smallest axis-parallel rectangle that contains all its pins. It is a lower bound on the length of every rectilinear tree that connects the pins, and it is equal to the length of the shortest such tree when the net has two or three pins. For larger nets it can be too small by a factor that grows with the number of pins. It is cheap to compute, separates into an $x$ part and a $y$ part, and is a convex function of the pin positions, so it is the standard objective of [placement](/placement-problem/).

## Definition

Let a net $e$ have pins $1, \ldots, p$ with positions $(x_i, y_i)$ in the plane. Its half-perimeter wirelength is

$$ \mathrm{HPWL}(e) = \Big(\max_i x_i - \min_i x_i\Big) + \Big(\max_i y_i - \min_i y_i\Big). $$

For a netlist with nets $e_1, \ldots, e_m$ and net weights $w_j \ge 0$, the total HPWL is $\sum_j w_j \, \mathrm{HPWL}(e_j)$. It costs $O(P)$ time for $P$ pins in total.

**Pin positions.** A pin sits on a cell. If cell $c$ has its reference point at $(X_c, Y_c)$ and the pin has offset $(\delta_x, \delta_y)$ inside the cell, the pin position is $(X_c + \delta_x, Y_c + \delta_y)$, with the offset turned or mirrored when the cell is turned or mirrored. A model *with pin offsets* uses these positions. A model *without pin offsets* puts every pin at the center of its cell, which is the usual choice in global placement. The two models can give different values and different optimal placements, so a statement about HPWL must say which one it uses. Pads and other fixed pins have fixed positions in both models. On this site the examples put pins at the cell centers unless they say otherwise.

**Equivalent forms.** $\mathrm{HPWL}(e) = \max_{i,j} |x_i - x_j| + \max_{i,j} |y_i - y_j|$. It is also the optimal value of the small [linear program](/linear-programming-problem/) "minimize $(u - l) + (u' - l')$ subject to $l \le x_i \le u$ and $l' \le y_i \le u'$ for all $i$". So the total HPWL is a [convex function](/convex-function/) of the cell positions that is piecewise linear but not differentiable, and placement under HPWL can be written as a linear program once the order constraints that prevent overlap are fixed.

**Two facts with proof.** Let $W$ and $H$ be the width and height of the bounding box, and let $\mathrm{RSMT}(e)$ be the length of a rectilinear Steiner minimum tree on the pins (see the [rectilinear Steiner tree problem](/rectilinear-steiner-tree-problem/)).

1. *Lower bound.* Every connected union of horizontal and vertical segments that contains the pins has length at least $W + H$. The projection of a connected set onto the $x$-axis is an interval that contains all $x_i$, so it has length at least $W$. Only the horizontal segments add to that projection, and each adds at most its length, so the horizontal segments have total length at least $W$. In the same way the vertical segments have total length at least $H$. So $\mathrm{HPWL}(e) \le \mathrm{RSMT}(e)$ for every net.
2. *Exact for $p \le 3$.* For two pins, an L-shaped path has length $|x_1 - x_2| + |y_1 - y_2| = W + H$. For three pins, let $(\bar x, \bar y)$ be the point whose coordinates are the medians of the $x_i$ and of the $y_i$. Connect each pin to it by an L-shaped path. The three horizontal parts have total length $\sum_i |x_i - \bar x| = W$, because the median lies between the other two values, and the vertical parts add $H$. With the lower bound, $\mathrm{RSMT}(e) = \mathrm{HPWL}(e)$.

For $p \ge 4$ a horizontal trunk at the median $\bar y$ from $\min x$ to $\max x$, with a vertical branch from each pin, has length $W + \sum_i |y_i - \bar y| \le W + \lfloor p/2 \rfloor H$. Pair the sorted $y$ values from the outside in: each pair adds at most $H$, and the middle value of an odd count adds 0. So

$$ \mathrm{HPWL}(e) \le \mathrm{RSMT}(e) \le W + \lfloor p/2 \rfloor H \le \lfloor p/2 \rfloor \, \mathrm{HPWL}(e) \quad (p \ge 2). $$

## Examples and non-examples

- **Two pins.** Pins at $(1, 4)$ and $(5, 1)$: $\mathrm{HPWL} = 4 + 3 = 7$, the length of any monotone staircase between them.
- **Three pins.** Pins at $(0, 0)$, $(4, 1)$ and $(2, 3)$. The box is $4 \times 3$, so $\mathrm{HPWL} = 7$. The median point is $(2, 1)$, and the three L-shaped paths have lengths $2 + 1$, $2 + 0$ and $0 + 2$, which sum to 7. No tree is shorter.
- **Four corners, a non-example.** Pins at the corners of a $2 \times 2$ square: $\mathrm{HPWL} = 4$, but every rectilinear tree on them has length at least 6 (an H shape with three segments of length 2 reaches 6). Here HPWL is too small by a factor $3/2$.
- **A grid of pins.** Take the $k \times k$ unit grid of pins $\{0, \ldots, k-1\}^2$. Then $\mathrm{HPWL} = 2(k - 1)$. Every point of the Hanan grid (the grid of horizontal and vertical lines through the pins, see the [Hanan theorem](/hanan-theorem/)) is a pin, so a Steiner minimum tree is a spanning tree of the grid graph and has length $k^2 - 1$. For $k = 3$ this is 8 against an HPWL of 4. The ratio $(k + 1)/2$ grows like $\sqrt{p}/2$ in the number $p = k^2$ of pins, so no constant factor links HPWL and Steiner length for large nets.
- **Pin offsets change the answer.** Two cells of width 4 sit side by side with centers at $x = 0$ and $x = 4$. A net joins a pin at offset $+2$ (the right edge) of the first cell with a pin at offset $-2$ (the left edge) of the second. Without offsets the net has HPWL 4. With offsets both pins are at $x = 2$ and the HPWL is 0. Mirroring both cells moves the pins to $x = -2$ and $x = 6$, and the HPWL becomes 8.
- **Not a routed length.** HPWL ignores blockages, congestion, layers and vias. A net that the router must detour around a macro has a routed length larger than its RSMT, and so larger than its HPWL.

## Related definitions

- **Rectilinear Steiner minimum tree.** The exact length of the shortest connection. Computing it is NP-hard (see [rectilinear Steiner tree problem](/rectilinear-steiner-tree-problem/)). [FLUTE](/flute/) gives it exactly for small nets by lookup tables. HPWL is the cheap lower bound that is tight for $p \le 3$.
- **Rectilinear minimum spanning tree.** Another estimate, at most $3/2$ times the Steiner length (Hwang 1976, see [rectilinear minimum spanning tree](/rectilinear-minimum-spanning-tree/)). It costs more than HPWL.
- **Clique and star models.** Quadratic placers replace HPWL by a sum of squared distances on the edges of a clique or a star (see [clique net model](/clique-net-model/)). These are smooth, but they are not equal to HPWL for $p \ge 3$.
- **Smooth approximations.** Analytical placers replace the max and the min by a soft maximum, as in the [log-sum-exp wirelength](/log-sum-exp-wirelength/), so that gradients exist.
- **Cut-line form.** On a grid with integer pin coordinates, the HPWL of a net equals the number of the lines $x = j + \frac12$ and $y = j + \frac12$ that separate its pins. Summed over nets, the total HPWL equals the sum over these lines of the number of nets that cross them. [Min-cut placement](/min-cut-placement/) is built on this form.

## References
