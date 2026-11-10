---
tag: Z1DTDF
kind: technique
slug: guillotine-cut-technique
name: Guillotine cut technique
aliases:
- guillotine subdivision
- guillotine dissection
- m-guillotine subdivision
- Mitchell's guillotine method
area: approximation/approximation-schemes
level: advanced
summary: Restrict a geometric partition to recursive axis-parallel cuts that run across the whole region, enabling dynamic programming over subregions.
prereqs: [ptas, approximation-ratio, planar-subdivision]
see_also: [mitchell-guillotine-ptas, mitchell-euclidean-tsp-ptas, portal-based-dissection, arora-euclidean-tsp-ptas, shifting-technique, euclidean-tsp, rectilinear-steiner-tree-problem, euclidean-steiner-tree-problem]
sources:
  - paper: doi:10.1137/S0097539796309764
    title: J. S. B. Mitchell, Guillotine subdivisions approximate polygonal subdivisions, a simple polynomial-time approximation scheme for geometric TSP, k-MST, and related problems, SIAM Journal on Computing 28(4), 1999, pp. 1298-1309
    locator: the m-span, m-perfect cuts and m-guillotine subdivisions, the charging lemma with dark regions, and the length bound with the factor 1 + √2/m
  - paper: "J. S. B. Mitchell, Guillotine subdivisions approximate polygonal subdivisions, a simple new method for the geometric k-MST problem, Proceedings of the 7th ACM-SIAM Symposium on Discrete Algorithms (SODA), 1996, pp. 402-408"
    title: Mitchell 1996
    locator: the first use of guillotine subdivisions for a constant ratio for the k-MST
  - paper: "A. Lingas, R. Y. Pinter, R. L. Rivest and A. Shamir, Minimum edge length partitioning of rectilinear polygons, Proceedings of the 20th Allerton Conference on Communication, Control and Computing, 1982"
    title: Lingas, Pinter, Rivest and Shamir 1982
    locator: NP-hardness of the minimum length partition of a polygon with holes into rectangles
  - paper: doi:10.1145/290179.290180
    title: S. Arora, Polynomial time approximation schemes for Euclidean traveling salesman and other geometric problems, Journal of the ACM 45(5), 1998, pp. 753-782
    locator: Section 1, the comparison of portals with Mitchell's guillotine method
---

The guillotine cut technique makes a geometric network problem small enough for dynamic programming. A *guillotine* structure is one that can be cut by a horizontal or vertical line that runs across the whole region, then each part can be cut again, and so on. A dynamic program over the rectangles of such a cut tree, the *windows*, finds the best guillotine structure. Mitchell (1996, 1999) relaxed the rule to *m-guillotine*: along each cut, apart from at most $m - 1$ pieces near each end, the cut must lie on the structure. He proved that any network of length $L$ becomes m-guillotine when segments of total length at most $\frac{\sqrt 2}{m} L$ are added on the cuts. So an m-guillotine solution exists within a factor $1 + O(1/m)$ of the optimum. Its boundary on each window side is described by $O(m)$ numbers, and the dynamic program takes $n^{O(m)}$ time. This gives a [PTAS](/ptas/) for the [Euclidean TSP](/euclidean-tsp/), Steiner trees and related problems in the plane; see the [guillotine PTAS](/mitchell-guillotine-ptas/).

## In plain words

Think of a drawing made of straight lines inside a frame. We want to cut the frame in two with one straight cut, across or down, and then cut each part again, until no lines are left inside any part.

Where a cut crosses the drawing, a part on one side must fit a part on the other side. If the cut crosses the drawing in many places, there is too much to remember. So we make a rule: count a few crossings in from each end, and draw a line along the cut between them. Then only the few end crossings and one new line describe the cut.

The new lines cost extra length. The trick is to pick each cut well, so that the extra length is small. Then a table over all parts, from small to large, finds the best drawing that follows the rule.

## When it applies

The technique needs three things.

- **Solutions are networks of segments.** The solution is a set of straight segments in the plane, for example a tour, a tree or a partition into rectangles, and its cost is its total length.
- **Added segments do not hurt.** Adding segments on the cuts keeps a solution feasible, or it can be repaired at a small cost. For a tour, the added segments are doubled and an Euler circuit is shortcut.
- **Local checks.** Feasibility can be checked from what happens on the boundary of each window: which segments cross it, where, and how they connect inside. Then the boundary is the state of a dynamic program.

It works best in the plane. Problems on graphs without geometry, or costs that do not grow with length, need other methods.

## The template

The form below is the one the code uses. $G$ is a finite set of horizontal and vertical segments of total length $L$, and a *window* $W$ is a closed axis-parallel rectangle. Only the open inside of $W$ counts. For a vertical line $\ell$ through the inside of $W$, the *parts* of $\ell$ are the connected pieces of $\ell \cap \operatorname{int}(W) \cap G$, in order $\xi_1, \ldots, \xi_k$; a part is a point where a horizontal segment crosses $\ell$, or an interval where vertical segments lie on $\ell$. Horizontal lines are the same with $x$ and $y$ swapped.

- **The m-span** $\sigma_m(\ell)$ is empty if $k \le 2(m - 1)$. Otherwise it is the piece of $\ell$ from the low end of $\xi_m$ to the high end of $\xi_{k - m + 1}$.
- **m-perfect.** The cut $\ell$ is *m-perfect* if $\sigma_m(\ell) \subseteq G$.
- **m-guillotine.** $G$ is *m-guillotine* with respect to $W$ if no segment of $G$ meets $\operatorname{int}(W)$, or some m-perfect cut $\ell$ splits $W$ into $W_1$ and $W_2$ and $G$ is m-guillotine with respect to both.
- **Critical coordinates.** The $x$ values strictly inside $W$ where a segment that meets $\operatorname{int}(W)$ starts, ends or lies. They split the $x$ range of $W$ into *pieces*; an *inner* piece lies between two critical values, and an *end* piece touches a side of $W$.
- **Dark length.** For the vertical line $\ell$ at $x$, $h(\ell)$ is the length of the set of points $(x, y)$ of $W$ whose horizontal line has at least $m$ parts of $G$ in $\operatorname{int}(W)$ strictly to the left of $x$ and at least $m$ strictly to the right.
- **Free and favorable cuts.** A cut through a critical coordinate is *free* if its span already lies on $G$. A cut inside an inner piece is *favorable* if $|\sigma_m(\ell)| \le h(\ell)$.

```pseudo id=template
GUILLOTINE(G, B, m)
L1  take a window W from the stack, which starts as the box B; if no segment of G meets the inside of W, skip it
L2  if a cut of W through a critical coordinate is free, use it
L3  otherwise, for the line ℓ in each inner piece, compute the m-span σ(ℓ) and the dark length h(ℓ)
L4  use a favorable line: one with |σ(ℓ)| ≤ h(ℓ), with the least |σ(ℓ)|
L5  add σ(ℓ) to G
L6  push the two windows into which ℓ cuts W, and repeat from L1 until the stack is empty
L7  return G
```

Let $R_V$ be the set of points $p$ of $\operatorname{int}(W)$ with at least $m$ parts of $G$ strictly below $p$ and $m$ strictly above it on its vertical line, and $R_H$ the same with left and right on the horizontal line. They are the *dark regions*.

**Lemma 1 (two ways to measure).** For a vertical line $\ell_x$ in a piece, $|\sigma_m(\ell_x)| = |\ell_x \cap R_V|$. So $\int |\sigma_m(\ell_x)|\,dx = \operatorname{area}(R_V) = \int h(\ell_y)\,dy$, and likewise $\int |\sigma_m(\ell_y)|\,dy = \operatorname{area}(R_H) = \int h(\ell_x)\,dx$.

*Proof.* Inside a piece, $\ell_x$ contains no vertical segment, so its parts are crossing points $y_1 < \cdots < y_k$. A point $y$ has $m$ parts below it if and only if $y > y_m$, and $m$ above it if and only if $y < y_{k-m+1}$. So $|\ell_x \cap R_V| = y_{k-m+1} - y_m$ if $k \ge 2m$ and 0 otherwise. This is the span length: for $k = 2m - 1$ the span is the single point $y_m$, and for $k \le 2m - 2$ it is empty. Integrating over $x$ gives the area of $R_V$. The same area, integrated along horizontal lines, is $\int |\ell_y \cap R_V|\,dy$, and $|\ell_y \cap R_V|$ is the dark length of the horizontal line $\ell_y$. $\square$

**Lemma 2 (a cut exists).** If a segment of $G$ meets $\operatorname{int}(W)$, then $W$ has a free cut or a favorable line in an inner piece.

*Proof.* Both $|\sigma|$ and $h$ are constant on each piece, since nothing changes between two critical values. By Lemma 1, $\int (h - |\sigma|)\,dx = \operatorname{area}(R_H) - \operatorname{area}(R_V)$ and $\int (h - |\sigma|)\,dy$ is its negative, so one direction $D$ has $\int_D (h - |\sigma|) \ge 0$. On an end piece $h = 0$: for $x$ beyond the last critical value, no vertical segment inside $W$ lies to the right of $x$, since its $x$ would be critical. So the end pieces add at most 0, and if $D$ has an inner piece, some inner piece has $h \ge |\sigma|$.

Suppose $D$, say the $x$ direction, has at most one critical value. A point of $R_H$ needs vertical segments at two different $x$ values, both critical, so $\operatorname{area}(R_H) = 0$. Then $\int_D (h - |\sigma|) = -\operatorname{area}(R_V) \ge 0$ gives $\operatorname{area}(R_V) = 0$, so in the $y$ direction $\int (h - |\sigma|) = 0$, and if that direction has an inner piece, the argument above gives a favorable line in it. The case left is at most one critical value $e$ in $x$ and at most one $e'$ in $y$. Every segment inside $W$ lies on $x = e$ or $y = e'$ and ends at $e$, at $e'$ or outside $\operatorname{int}(W)$. The line $x = e$ then meets $G$ in one connected part, the vertical pieces through or up to $(e, e')$ together with that point, so it has $k = 1$ and is free. If there is no critical $x$, the line $y = e'$ is free in the same way. $\square$

**Lemma 3 (the procedure stops and is correct).** The two windows of a cut have critical sets inside that of $W$, and each loses at least one value. So the procedure stops, and the result is m-guillotine with respect to $B$.

*Proof.* A segment that meets the inside of a part meets $\operatorname{int}(W)$, so the critical values of a part are critical for $W$. A free cut at $e$ puts $e$ on the boundary of both parts. A favorable line in the inner piece $(a, b)$ leaves $b$ out of the left part and $a$ out of the right part. The span lies on the cut, which is on the boundary of both parts, so it adds no critical value. A window with no critical value has no segment inside, since a segment inside $W$ has its own coordinate critical. Later spans lie strictly inside smaller windows on one side of the cut, so they never touch an earlier cut line, and its parts and span do not change. Every cut is m-perfect after line L5, so by induction from the last windows back to $B$, the result is m-guillotine. $\square$

**Theorem (length).** GUILLOTINE returns an m-guillotine set of segments that contains $G$, of length at most $(1 + 1/m)\,L$.

*Proof.* Free cuts add nothing. Before $W$ is cut, every span added earlier lies outside $\operatorname{int}(W)$, so the parts inside $W$ belong to the original $G$. Take a favorable vertical cut $\ell_x$ of $W$; it adds $|\sigma| \le h(\ell_x)$. Each point $p = (x, y)$ of $\ell_x \cap R_H$, with $y$ not critical, has at least $m$ parts on each side on its horizontal line, and these are crossing points with vertical segments of $G$. Give a charge of $\frac{1}{2m}$ per unit of $y$ to each of the $m$ nearest parts on each side. The total charge is $h(\ell_x) \ge |\sigma|$.

A point $q = (x_q, y)$ of a vertical segment is charged *from the right* at most once. When $\ell_x$ charges it, at most $m - 1$ parts lie strictly between $q$ and $(x, y)$. Every later window $W'$ with $q$ inside lies in the left part, so $x'_1 \le x$ for its right side. A later charge from the right by a cut at $x' > x_q$ needs $m$ parts strictly between $x'$ and $x'_1$ on the same horizontal line, and these lie strictly between $q$ and $(x, y)$. There are at most $m - 1$, a contradiction. The same holds from the left, and for horizontal segments with horizontal cuts. So a segment $s$ receives at most $2 \cdot \frac{1}{2m} |s| = \frac{|s|}{m}$, and the total added length is at most $\frac{L}{m}$. $\blacksquare$

**General segments (proof sketch).** For segments in any direction, Mitchell's argument is the same: on a line in general position each part is a crossing point, Lemma 1 holds, and the charges from vertical cuts are at most $\frac{1}{m}$ times the $y$ extent of each edge, and from horizontal cuts at most $\frac{1}{m}$ times its $x$ extent. Since $|\Delta x| + |\Delta y| \le \sqrt 2$ times the length of an edge, the added length is at most $\frac{\sqrt 2}{m} L$. Choosing the cuts at a finite set of coordinates, so that the recursion stops, needs more care than in the axis-parallel case; the details are in Mitchell (1999).

**The dynamic program.** Restrict the windows to rectangles with sides on $O(n)$ candidate lines, for example the lines through the input points, so there are $O(n^4)$ windows. In an m-guillotine solution, a window side is described by its span, two endpoints, and at most $2(m - 1)$ parts outside the span, each at one of $O(n)$ positions, plus whatever the problem needs, such as which parts are joined inside. That is $n^{O(m)}$ states per window. A state of $W$ is solved by trying the $O(n)$ cuts and the spans on them, and pairs of states of the two parts that agree on the cut. The total time is $n^{O(m)}$, and with $m = \lceil c/\varepsilon \rceil$ the ratio is $1 + \varepsilon$.

## Classic examples

**A set that needs one span.** Take the box $[0, 8]^2$ and the lines $y = 2, 4, 6$ and $x = 2, 4, 6$, each with one gap of length 1: on $y = 2$ the gap is $(4, 5)$, on $y = 4$ it is $(5, 6)$, on $y = 6$ it is $(2, 3)$, on $x = 2$ it is $(1, 2)$, on $x = 4$ it is $(5, 6)$, and on $x = 6$ it is $(2, 3)$. The length is $L = 42$. For $m = 1$ no cut of the box is 1-perfect: every line meets the set in at least two parts with a gap between them. The vertical lines give:

| $x$ | parts | 1-span | dark length $h$ |
|---|---|---|---|
| in $(0, 2)$ | crossings at $y = 2, 4, 6$ | 4 | 0 |
| 2 | $[0, 1]$ and $[2, 8]$ | 8, of which 1 is not on $G$ | 0 |
| in $(2, 3)$ | crossings at $y = 2, 4$ | 2 | 7 |
| in $(3, 4)$ | crossings at $y = 2, 4, 6$ | 4 | 7 |
| in $(4, 5)$ | crossings at $y = 4, 6$ | 2 | 7 |
| in $(5, 6)$ | crossings at $y = 2, 4, 6$ | 4 | 7 |
| in $(6, 8)$ | crossings at $y = 2, 4, 6$ | 4 | 0 |

The dark length of $(2, 3)$ is 7: a horizontal line has a vertical segment on its left, at $x = 2$, except for $y \in (1, 2)$, and always one on its right. Both integrals of Lemma 1 are 28. GUILLOTINE finds no free cut and takes the favorable line $x = 5/2$, adding the span from $(5/2, 2)$ to $(5/2, 4)$ of length $2 \le 7$. After that, all 20 later cuts are free, and the result has length $44 \le 2L$. For $m = 2$ the set is already 2-guillotine.

**Partitions into rectangles.** Given a rectangle and $n$ points inside it, find a partition of the rectangle into smaller rectangles, of least total cut length, such that every point lies on a cut. The problem is NP-hard for polygons with holes (Lingas, Pinter, Rivest and Shamir 1982). The best *guillotine* partition, where every cut runs across its window, has a dynamic program over the $O(n^4)$ windows on the lines through the points, with $O(n)$ cuts each, in $O(n^5)$ time. For the box $[0, 5]^2$ and the points $(1, 2)$, $(2, 4)$, $(3, 1)$, $(4, 3)$, the best partition is a pinwheel of length 12, with no cut across the box, and the best guillotine partition has length 13. The pinwheel is 1-guillotine as it is. With $m = 1$, the theorem says that the best 1-guillotine partition has length at most $2 \cdot \mathrm{OPT}$, since the spans of a rectangular partition end on its segments and keep all faces rectangles.

**The TSP and other networks.** For the [Euclidean TSP](/euclidean-tsp/), the boundary state also records how the parts are joined inside the window, and the spans are doubled so that all degrees stay even. The same idea gives schemes for the $k$-MST, the [Euclidean Steiner tree](/euclidean-steiner-tree-problem/) and the [rectilinear Steiner tree](/rectilinear-steiner-tree-problem/). See the [guillotine PTAS](/mitchell-guillotine-ptas/) and [Mitchell's TSP scheme](/mitchell-euclidean-tsp-ptas/).

## Variations

- **Guillotine and m-guillotine.** A guillotine cut lies entirely on $G$ inside the window. The m-guillotine rule asks this only for the m-span, which is what makes the length bound possible. The pinwheel above is not guillotine, but it is 1-guillotine.
- **Portals in place of spans.** [Portal-based dissection](/portal-based-dissection/), used by [Arora's scheme](/arora-euclidean-tsp-ptas/), bounds the crossings of each square by moving them to fixed points. It uses a random shift, while the guillotine method is deterministic.
- **Integer coordinates.** Snapping the input to a grid of polynomial size, as in other schemes, keeps the candidate lines at $O(n)$ per direction after scaling.
- **Higher dimension.** The charging argument uses the plane. In fixed dimension $d$, portals are the more common tool.

## Pitfalls

- **Parts, not segments.** Two segments that touch on the cut line form one part, and a vertical segment on a vertical cut is one part, not many crossings. Counting segments in place of parts gives wrong spans.
- **The window boundary.** This page counts only parts inside the open window, so a span on an earlier cut does not count again. Sources differ on this convention. Fix one, and use it in both the definition and the proof.
- **End pieces.** A cut in an end piece leaves a window equal to the old one, so a procedure that allows it can repeat forever. The free cuts through critical coordinates are what make the recursion stop.
- **The span must end on parts.** A span that ends between parts creates new crossings and can spoil earlier cuts.
- **The exponent.** The time is $n^{O(m)}$ with $m = \Theta(1/\varepsilon)$, so the scheme is a PTAS but not an [EPTAS](/eptas/).
- **Feasibility after adding spans.** For a tour, an added span creates odd degrees at its ends. Doubling it costs a factor 2 on the added length.

## Exercises

1. In the example with gaps, check by hand that no cut of the box is 1-perfect, and that the line $x = 5/2$ is favorable while $x = 1$ is not.
2. Show that for $m \ge 2$ a set of segments in which every line meets at most $2m - 2$ parts is m-guillotine with no added span.
3. Show that the set with gaps is 2-guillotine, and find the cut tree.
4. Prove that the guillotine dynamic program for partitions into rectangles needs only cuts through the coordinates of the points.
5. For segments in general directions, show that the charges to an edge from vertical cuts are at most $\frac{1}{m}$ times its $y$ extent, and conclude the bound $\frac{\sqrt 2}{m} L$.

## References
