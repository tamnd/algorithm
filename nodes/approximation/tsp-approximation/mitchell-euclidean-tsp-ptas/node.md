---
tag: D2DB1X
kind: algorithm
slug: mitchell-euclidean-tsp-ptas
name: Mitchell's guillotine PTAS for Euclidean TSP
aliases:
- Mitchell's guillotine subdivision algorithm
area: approximation/tsp-approximation
level: research
summary: A deterministic PTAS for the Euclidean TSP in the plane; any tour becomes an m-guillotine graph at a cost of a 1 + O(1/m) factor, and a dynamic program over windows finds the best such graph.
solves: [euclidean-tsp]
model: real-ram
complexity:
  vars: {n: the number of points, m: "the guillotine parameter (the ratio is 1 + O(1/m))"}
  time: {worst: n^O(m)}
  space: {extra: n^O(m)}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 1996
  people: [Joseph S. B. Mitchell]
  note: Mitchell found guillotine subdivisions for geometric approximation in 1996 and the m-guillotine PTAS for the TSP independently of Arora; the journal paper appeared in 1999.
prereqs: [euclidean-tsp, guillotine-cut-technique, ptas, eulerian-circuit]
see_also: [mitchell-guillotine-ptas, guillotine-cut-technique, arora-euclidean-tsp-ptas, portal-based-dissection, euclidean-tsp, ptas, christofides-algorithm, lin-kernighan]
sources:
  - paper: doi:10.1137/S0097539796309764
    title: Joseph S. B. Mitchell, Guillotine subdivisions approximate polygonal subdivisions, a simple polynomial-time approximation scheme for geometric TSP, k-MST, and related problems, SIAM Journal on Computing 28(4), 1999
    locator: pages 1298 to 1309 (m-spans, m-guillotine subdivisions, the length theorem with the factor 1 + √2/m, and the dynamic program)
  - paper: doi:10.1145/290179.290180
    title: Sanjeev Arora, Polynomial time approximation schemes for Euclidean traveling salesman and other geometric problems, Journal of the ACM 45(5), 1998
    locator: Section 1 (the comparison with Mitchell's method)
---

Mitchell's scheme is a deterministic [PTAS](/ptas/) for the [Euclidean TSP](/euclidean-tsp/) in the plane. Its key idea is the *m-guillotine* graph: a set of edges whose bounding box can be cut again and again by horizontal and vertical lines, such that along each cut, between the $m$-th edge crossing from one end and the $m$-th from the other, the line is covered by edges. Mitchell proved that any graph becomes m-guillotine by adding *bridges* on the cuts of total length at most $\frac{\sqrt{2}}{m}$ times its length. So some m-guillotine graph that gives a tour costs at most $1 + O(1/m)$ times OPT, and a dynamic program over rectangles, with a boundary state of $O(m)$ edges per side, finds the best one in $n^{O(m)}$ time. The method is the [guillotine cut technique](/guillotine-cut-technique/); the [guillotine PTAS](/mitchell-guillotine-ptas/) page describes it in general.

## In plain words

Draw a box around the tour. Cut the box with a straight line, across or down, and cut each part again, until no city is inside a part.

Each cut line meets the tour at some points. Count $m$ points in from each end. Between those two points, lay a straight road on the cut line, the bridge, if there is not one already.

Now each cut is simple to describe: a few roads near each end and one bridge. So a table can hold the best way to fill each box for each such description, built from small boxes to big ones.

Mitchell showed that the bridges are short when the cuts are chosen well, so the best tour that the table finds is close to the best tour.

## The problem

The input is a set $P$ of $n$ points in the plane with the Euclidean distance and an integer $m \ge 1$. The output is a tour of $P$. OPT is the length of a shortest tour and ALG is the length of the returned tour. The convention is ALG $\le \rho \cdot$ OPT for a minimization problem, and here $\rho = 1 + O(1/m)$, so $m = O(1/\varepsilon)$ gives the ratio $1 + \varepsilon$.

For a window $W$ and a cut line $\ell$, let $\xi_1, \ldots, \xi_k$ be the parts of $\ell \cap W$ that lie on edges, in order. The *m-span* is empty if $k \le 2(m - 1)$, and otherwise it runs from the low end of $\xi_m$ to the high end of $\xi_{k-m+1}$. A cut is *m-perfect* if its m-span lies on edges.

## The algorithm

```pseudo id=main
MITCHELL-TSP(P, m)
L1  the windows are the rectangles whose sides lie on the lines x = x_i and y = y_i through the points
L2  for each window W, from small to large, and each boundary state of W do
L3      value(W, state) = the least cost over cuts of W with an m-span bridge and over states of the two halves that agree on the cut
L4  take the least value at the bounding box over the states that give a connected graph with even degrees
L5  shortcut an Euler circuit of that graph to a tour, and return it
```

A boundary state lists, for each side of the window, the bridge on it, at most $2m$ edges that cross the side outside the bridge, and a pattern that says which of these pieces are joined inside. There are $n^{O(m)}$ states per window.

**What the code covers.** The code implements the m-span, an exhaustive checker of the m-guillotine property with cuts at vertex coordinates, and the conversion that adds bridges window by window, at each step on the cut with the shortest uncovered span. It does not implement the dynamic program. In its place it takes, by brute force over all orders, the order with the least length plus bridge length; the theorem bounds this sum for an optimal order. This takes exponential time. The bound on the bridges is Mitchell's theorem, which the code measures but does not prove.

## Example

Take the seven cities of the [3-opt](/three-opt/) page, $A(1,2)$, $B(0,5)$, $C(3,3)$, $D(1,0)$, $E(0,0)$, $F(3,4)$ and $G(2,6)$, and the optimal tour $A\,E\,D\,C\,F\,G\,B$ of length 15.476. The bounding box is $[0, 3] \times [0, 6]$, and only $A$ lies strictly inside it.

| cut | parts on edges | 1-span | uncovered |
|---|---|---|---|
| $x = 1$ | $D$ at $y = 0$, $A$ at $y = 2$, edge $GB$ at $y = 5.5$ | $y$ from 0 to 5.5 | 5.5 |
| $y = 2$ | $A$ at $x = 1$, edge $DC$ at $x = 2.333$ | $x$ from 1 to 2.333 | 1.333 |

1. **$m = 1$.** No cut is 1-perfect, so the tour is not 1-guillotine. The conversion takes the cut $y = 2$ and adds a bridge of length 1.333 from $A$ to the edge $DC$. Then the two halves have no city inside, and the graph is 1-guillotine. The bridge is far below the bound $\sqrt{2} \cdot 15.476 = 21.886$.
2. **$m = 2$.** The cut $y = 2$ has only 2 parts, so its 2-span is empty and the cut is 2-perfect. The tour is 2-guillotine with no bridge.
3. **The code.** For $m = 1$ the brute force returns $A\,C\,F\,G\,B\,D\,E$, of length 16.043 with bridges of 0.4, since $16.443 < 15.476 + 1.333$. This is 1.037 times OPT. For $m = 2$ it returns OPT.

**A graph that is not 1-guillotine.** Five rectangles in a pinwheel, $[0,2] \times [0,1]$, $[2,3] \times [0,2]$, $[1,3] \times [2,3]$, $[0,1] \times [1,3]$ and the middle square $[1,2] \times [1,2]$, have no cut that runs along edges across the box. One bridge of length 3 on $x = 1$ makes them 1-guillotine. They are 2-guillotine as they are.

**Measured behavior.** On 300 seeded random tours of 4 to 8 random points, in random order, so with many crossings, the bridges of the conversion were at most 0.42 times the bound $\frac{\sqrt{2}}{m} L$ for $m = 1$, at most 0.10 times it for $m = 2$, and 0 for $m = 3$. Like Arora's scheme, the method is too slow for real instances, where [Lin-Kernighan](/lin-kernighan/) gives better tours. These are measured values, not bounds.

## Correctness

**Theorem.** For each $m \ge 1$, the scheme returns a tour of length at most $(1 + O(1/m)) \cdot$ OPT, in time $n^{O(m)}$. Mitchell's length theorem gives the bridge factor $1 + \frac{\sqrt{2}}{m}$.

The proof has three steps.

1. **Bridges make cuts m-perfect.** Adding the m-span of a cut merges the middle parts into one, so the new span lies on edges. The ends of a bridge are old points of the graph, so later bridges do not spoil earlier cuts, and the conversion gives an m-guillotine graph.
2. **The bridges are short.** In each window some cut has a span no longer than the part of the window that is dark for the other direction, by Fubini's theorem. Charging $1/m$ of the span to the $m$ nearest edges on one side bounds the total by $\frac{1}{m}$ times the $x$ and $y$ extents of the edges, which is at most $\frac{\sqrt{2}}{m}$ times their length.
3. **The dynamic program.** The m-guillotine graph from an optimal tour, with doubled bridges, is connected with even degrees, so it is one of the graphs that the table considers. The best such graph gives a tour by shortcutting an Euler circuit.

The full proof is in the proof file. Step 1 is proved in full and is checked by the tests. Step 2 is a sketch of Mitchell's argument, except for the averaging step, and step 3 is a sketch.

**Lower bounds.** The Euclidean TSP has no FPTAS unless P = NP, by the reduction from Hamiltonian cycles in grid graphs on the [Euclidean TSP](/euclidean-tsp/) page. So the time must grow faster than any polynomial in $m$ and $n$ together, unless P = NP.

**Hardness.** For general metric costs no polynomial algorithm has a ratio below $123/122$ unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality no constant ratio is possible unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **Windows.** $O(n^4)$ rectangles with sides on the lines through the points.
- **States.** Each side carries a bridge and at most $2m$ crossing edges, each fixed by $O(n^2)$ choices, and a joining pattern on $O(m)$ pieces, so $n^{O(m)}$ states per window.
- **Transitions.** $O(n)$ cuts per window and $n^{O(m)}$ pairs of agreeing states, so $n^{O(m)}$ time in total.
- **The code.** $O(n!)$ orders, each converted in polynomial time, for checking only.

## Properties

- **Deterministic.** No random shift is needed, unlike [Arora's scheme](/arora-euclidean-tsp-ptas/).
- **Exponent.** The time $n^{O(m)}$ grows in the exponent of $n$, while Arora's scheme puts the dependence on $c$ in a power of $\log n$.
- **General.** The same length theorem gives schemes for the $k$-MST, the Steiner tree and other problems whose solutions are networks of segments.
- **Stated in the plane.** The length theorem uses the plane; Arora's portals extend more directly to fixed dimension $d$.

## Variants and improvements

- **Earlier guillotine results.** Mitchell first used guillotine subdivisions for constant ratios for the $k$-MST, and then the m-guillotine form for the PTAS.
- **Faster versions.** Later work by Mitchell gave faster schemes based on the same idea.
- **Arora's portals.** [Arora's scheme](/arora-euclidean-tsp-ptas/) reaches $n (\log n)^{O(c)}$ by portals and patching. The two papers shared the Gödel Prize in 2010.
- **Other problems.** The general method is on the [guillotine PTAS](/mitchell-guillotine-ptas/) page.

## When to use it

Use the scheme to prove that a geometric network problem has a PTAS, or as a deterministic counterpart of [Arora's scheme](/arora-euclidean-tsp-ptas/). For real tours use [Lin-Kernighan](/lin-kernighan/) or [LKH](/lin-kernighan-helsgaun/), or [Christofides](/christofides-algorithm/) for a guarantee of 1.5.

## Pitfalls

- **Spans of components, not of edges.** An edge on the cut line is one component, not many crossings. Code that counts each edge on the line separately gets the span wrong.
- **Bridges that add crossings.** The ends of a bridge must be old points of the graph; otherwise later bridges can spoil the earlier cuts.
- **Even degrees.** A bridge adds odd degree at its ends. Doubling it, or counting it in the states, keeps the degrees even.
- **The constant.** The factor is $1 + \frac{\sqrt{2}}{m}$ for the bridges. The ratio for the tour depends on how the bridges are paid for, so check the constant in the source before you use it.

## Implementations

## History

Mitchell introduced guillotine subdivisions for approximation in 1996, first for constant ratios for the $k$-MST and then for the m-guillotine PTAS for the TSP. He found it independently of Arora's PTAS of the same year. The journal version appeared in SIAM Journal on Computing in 1999. Arora and Mitchell received the Gödel Prize in 2010 for these schemes.

## References
