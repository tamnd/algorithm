---
tag: MCW6TZ
kind: technique
slug: shifting-technique
name: Shifting technique
aliases:
- Hochbaum-Maass shifting
- Baker shifting
- shifting strategy
area: approximation/approximation-schemes
level: advanced
summary: Partition the input into strips or layers and shift the partition, so that some shift loses only a small fraction of the optimum.
prereqs: [approximation-ratio, ptas, set-cover]
see_also: [baker-technique, baker-planar-ptas, portal-based-dissection, guillotine-cut-technique, k-center-problem, hitting-set, eptas, local-search]
sources:
  - paper: "D. S. Hochbaum and W. Maass, Approximation schemes for covering and packing problems in image processing and VLSI, Journal of the ACM 32(1), 1985, pp. 130-136"
    title: Hochbaum and Maass 1985
    locator: the shifting lemma and its use for covering points with squares and disks of fixed size in d dimensions
  - paper: "B. S. Baker, Approximation algorithms for NP-complete problems on planar graphs, Journal of the ACM 41(1), 1994, pp. 153-180"
    title: Baker 1994
    locator: the layering of planar graphs, the graph analogue of shifting strips
  - paper: "H. B. Hunt III, M. V. Marathe, V. Radhakrishnan, S. S. Ravi, D. J. Rosenkrantz and R. E. Stearns, NC-approximation schemes for NP- and PSPACE-hard problems for geometric graphs, Journal of Algorithms 26(2), 1998, pp. 238-274"
    title: Hunt, Marathe, Radhakrishnan, Ravi, Rosenkrantz and Stearns 1998
    locator: shifting for unit disk graphs and the schemes for independent set, vertex cover and related problems
  - paper: "T. Erlebach, K. Jansen and E. Seidel, Polynomial-time approximation schemes for geometric intersection graphs, SIAM Journal on Computing 34(6), 2005, pp. 1302-1323"
    title: Erlebach, Jansen and Seidel 2005
    locator: hierarchical shifting for disks of different sizes
---

The shifting technique of Hochbaum and Maass (1985) turns an exact or approximate algorithm for small regions into an approximation scheme for the whole plane. Cut the plane into strips of width $\ell$, solve each strip on its own, and take the union. An object of the optimum that crosses a strip boundary may be paid for twice. There are $\ell$ ways to place the boundaries (the *shifts*), and each object of size 1 crosses the boundaries of exactly one shift. So on average over the shifts only a $1/\ell$ fraction of the optimum is paid twice, and the best shift costs at most $(1 + 1/\ell)$ times the optimum. Applied in each of $d$ directions, it reduces a problem to cells of side $\ell$ at a factor $(1 + 1/\ell)^d$. Baker's [layering for planar graphs](/baker-technique/) is the same idea with breadth-first levels in place of strips.

## In plain words

Suppose you must cover dots on a big map with as few equal stamps as possible. A big map is hard, but a narrow strip of the map is easier. So you draw parallel lines and cut the map into strips, and you cover each strip on its own.

A stamp of the best answer that lies across a line may be counted twice, once in each strip. That is the only loss. Now move all the lines one step sideways, and again, so that every placement of the lines is tried. Each stamp lies across the lines in only one of these placements. So the loss, summed over all placements, is one copy of the best answer, and at least one placement loses only a small part of it. Wider strips make the loss smaller but each strip harder.

## When it applies

The technique needs four things.

- **Objects of bounded size.** Each object of a solution (a square, a disk, a chosen vertex with its neighbourhood) has diameter at most 1 in the direction of the cuts, so it crosses at most one boundary of a given shift.
- **Separate subproblems.** The points or items of the input belong to strips, and a solution of the whole input restricted to one strip is a solution of that strip. For covering, each strip needs only the objects that meet it.
- **A cost that adds up.** The cost of a union of strip solutions is at most the sum of their costs, and the cost of the optimum is the sum of the costs of its objects.
- **A good algorithm for a strip.** An exact algorithm for a strip, or for a cell of side $\ell$ after shifting in every direction, that runs in polynomial time for fixed $\ell$. In a cell of side $\ell$ the optimum has at most $O(\ell^d)$ objects, so trying all small sets of candidate objects is polynomial.

Covering problems lose by counting crossing objects twice; packing problems lose by dropping them. The proof is the same in both cases.

## The template

The input is a set of points in the plane, with integer lines as the possible boundaries. Shift $s \in \{0, \ldots, \ell - 1\}$ uses the vertical lines $x = c$ with $c \equiv s \pmod \ell$, and a point with $b \le x < b + \ell$ belongs to the strip $[b, b + \ell)$. The algorithm $A$ solves one strip.

```pseudo id=template
SHIFT(P, ℓ, A)
L1  for s ← 0 to ℓ − 1
L2      cut the plane by the vertical lines x = c with c ≡ s (mod ℓ)
L3      put each point of P into the strip [b, b + ℓ) with b ≤ x < b + ℓ
L4      C_s ← the union of A(points of the strip) over the non-empty strips
L5  keep the C_s of least cost
L6  return it
```

To get cells, use as $A$ the same procedure in the $y$ direction, with an exact algorithm for each cell of side $\ell$.

**Theorem (shifting lemma).** Consider covering a point set $P$ by closed axis-parallel unit squares, with $\ell \ge 1$ an integer. Suppose that $A$, on the points of any strip, returns a cover with at most $r$ times the least number of squares for those points. Then SHIFT returns a cover of $P$ with at most $r\,(1 + 1/\ell)\,\mathrm{OPT}$ squares.

*Proof.* Each point lies in one strip of each shift and $A$ covers it, so every $C_s$ is a cover. Fix an optimal cover $Q^*$ with $|Q^*| = \mathrm{OPT}$, and take a square $q = [x, x+1] \times [y, y+1]$ of $Q^*$. Say that $q$ is *cut* by shift $s$ if some line $x = c$ of shift $s$ has $x < c \le x + 1$.

*Each square is cut by exactly one shift.* The half-open interval $(x, x+1]$ has length 1, so it contains exactly one integer $c$, and $c$ is a line of exactly one shift, the one with $s \equiv c \pmod \ell$.

*An uncut square meets one strip; a cut square meets at most two.* Let $[b, b + \ell)$ be the strip of shift $s$ with $b \le x < b + \ell$. If $q$ is not cut, then $b + \ell$, the next line of shift $s$ after $x$, is larger than $x + 1$. So every point of $q$ has its $x$ in $[b, b + \ell)$ and lies in this strip. If $q$ is cut by a line $c$, the lines of shift $s$ are $\ell \ge 1$ apart, so $c$ is the only one in $(x, x+1]$. Then the points of $q$ lie in the strip of $x$ or in the strip that starts at $c$.

*The cost of one shift.* Let $k_s$ be the number of squares of $Q^*$ cut by shift $s$. For each strip $T$ of shift $s$, the squares of $Q^*$ that meet $T$ cover the points of $T$, so $\mathrm{OPT}(T)$ is at most their number. Summing over the strips, an uncut square is counted once and a cut square at most twice:
$$\sum_T \mathrm{OPT}(T) \le \mathrm{OPT} + k_s, \qquad |C_s| \le r \sum_T \mathrm{OPT}(T) \le r\,(\mathrm{OPT} + k_s).$$

*Averaging.* Each square of $Q^*$ is cut by exactly one shift, so $\sum_s k_s = \mathrm{OPT}$, and
$$\min_s |C_s| \le \frac{1}{\ell} \sum_{s=0}^{\ell - 1} |C_s| \le \frac{r}{\ell} \bigl(\ell\,\mathrm{OPT} + \mathrm{OPT}\bigr) = r \Bigl(1 + \frac{1}{\ell}\Bigr) \mathrm{OPT}. \qquad \blacksquare$$

**Corollary (cells).** Apply SHIFT in the $x$ direction with $A$ = SHIFT in the $y$ direction with an exact cell solver. The theorem applies to the inner call with $r = 1$, inside one strip, and then to the outer call with $r = 1 + 1/\ell$. The result is at most $(1 + 1/\ell)^2\,\mathrm{OPT}$. In $d$ dimensions the same argument gives $(1 + 1/\ell)^d$.

**The cell solver.** A cell of side $\ell$ is covered by the $\ell^2$ unit squares of the integer grid, so its optimum has at most $\ell^2$ squares. A square that covers a set $U$ of points can be moved so that its left side is at the least $x$ in $U$ and its bottom side at the least $y$ in $U$, and it still covers $U$. So there are at most $n_c^2$ candidate squares for a cell with $n_c$ points, and trying all sets of at most $\ell^2$ of them costs $n_c^{O(\ell^2)}$. With $\ell = \lceil 3/\varepsilon \rceil$ we have $(1 + 1/\ell)^2 \le 1 + 3/\ell \le 1 + \varepsilon$, so this is a [PTAS](/ptas/) with time $n^{O(1/\varepsilon^2)}$.

## Classic examples

**Covering points with unit squares.** Take $\ell = 2$ and the 8 points $(0.5, 0.5)$, $(1.25, 0.75)$, $(1.75, 2.5)$, $(2.25, 2.25)$, $(3.5, 0.25)$, $(3.75, 1)$, $(4.5, 3.5)$, $(5, 3.75)$. The optimum uses 4 squares, with lower left corners $(0.5, 0.5)$, $(1.75, 2.25)$, $(3.5, 0.25)$ and $(4.5, 3.5)$, each covering two points.

| shift | lines | strips and their points | strip optima | cost |
|---|---|---|---|---|
| 0 | $x = 0, 2, 4$ | $[0, 2)$: 3, $[2, 4)$: 3, $[4, 6)$: 2 | $2 + 2 + 1$ | 5 |
| 1 | $x = 1, 3, 5$ | $[-1, 1)$: 1, $[1, 3)$: 3, $[3, 5)$: 3, $[5, 7)$: 1 | $1 + 2 + 2 + 1$ | 6 |

Shift 0 cuts the optimal squares at $x \in [1.75, 2.75]$ and $x \in [3.5, 4.5]$, but only the first one has points on both sides, so it pays one extra square. Shift 1 cuts the squares at $x \in [0.5, 1.5]$ and $x \in [4.5, 5.5]$ and pays two. The sum of the costs is $11 \le (\ell + 1)\,\mathrm{OPT} = 12$, and the best shift gives $5 \le (1 + \frac12) \cdot 4 = 6$.

**Covering points with disks.** For disks of diameter $D$, Hochbaum and Maass use strips of width $\ell D$ and cells of side $\ell D$. A cell needs $O(\ell^2)$ disks, and a disk that covers a set of points can be moved until two of the points lie on its boundary, so there are $O(n_c^2)$ candidate disks. The ratio is again $(1 + 1/\ell)^2$ in the plane. This gives a PTAS for covering points with the fewest disks of a given radius, a problem that is NP-hard.

**Packing.** To pick the most pairwise disjoint unit squares from a given family, drop at each shift the squares cut by a line and solve each strip exactly. Each square of the optimum is dropped by exactly one shift, so the best shift keeps at least $(1 - 1/\ell)\,\mathrm{OPT}$ squares.

**Planar graphs.** Baker (1994) replaces the strips by breadth-first levels of a [planar graph](/planar-graph/). Deleting every $k$-th level leaves $k$-outerplanar pieces of bounded treewidth, which are solved exactly; see [Baker's technique](/baker-technique/) and [the planar PTAS](/baker-planar-ptas/).

**Unit disk graphs.** Hunt and coauthors (1998) use shifting on the disk centres to get schemes for maximum independent set, minimum vertex cover and related problems on unit disk graphs, the intersection graphs of disks of equal size.

## Variations

- **Two directions at once.** Shifting in $x$ and then in $y$ inside each strip gives $\ell^2$ shift pairs and the ratio $(1 + 1/\ell)^2$. The inner shift may differ from strip to strip, because each strip is solved on its own.
- **Random shift.** Picking $s$ uniformly at random gives an expected cost of at most $r(1 + 1/\ell)\,\mathrm{OPT}$ with one run. This is the form used in [portal-based dissection](/portal-based-dissection/), where a random shift of a quadtree bounds the expected number of crossings at each level.
- **Higher dimension.** In $d$ dimensions, shifting in each coordinate gives $(1 + 1/\ell)^d$, and the cells of side $\ell$ hold $O(\ell^d)$ objects of the optimum, for time $n^{O(\ell^d)}$.
- **Objects of different sizes.** If the objects have diameters within a factor $\lambda$, strips of width $\ell \lambda$ still keep the loss at $1/\ell$. For arbitrary sizes, a hierarchy of strips, one per size class, is needed, as in Erlebach, Jansen and Seidel for disk graphs.

## Pitfalls

- **Strips narrower than the objects.** If $\ell$ is less than the diameter of an object, one object can cross several lines of one shift, and the counting fails. The width must be measured in units of the object size.
- **Boundary rules.** Each point must lie in exactly one strip. With closed strips a point on a line belongs to two strips and may be covered twice; with open strips it belongs to none. Half-open strips $[b, b + \ell)$ fix this.
- **Covering the points, not the strip.** A strip solution may use squares that stick out of the strip. This is allowed and needed; forcing the squares inside the strip can raise the strip optimum.
- **The exponent.** The cell solver is exponential in $\ell^2$, and $n$ appears in the base, so the scheme is a PTAS but not an [EPTAS](/eptas/).
- **Every shift.** The lemma bounds the best shift, or the average one. A fixed shift, chosen without looking at the input, can be bad for a particular input.

## Exercises

1. In the example, add the point $(2, 3)$ and recompute the costs of the two shifts. Does the bound $(1 + 1/\ell)\,\mathrm{OPT}$ still hold for the best one?
2. Prove the $d$-dimensional bound $(1 + 1/\ell)^d$ by induction on $d$, using the theorem once per coordinate.
3. Give the packing version in full: show that dropping the squares cut by shift $s$ and solving each strip exactly keeps at least $(1 - 1/\ell)\,\mathrm{OPT}$ squares for the best shift.
4. Find four points on a horizontal line for which, with $\ell = 2$, one shift pays exactly $(1 + \frac12)\,\mathrm{OPT}$ and the other pays $\mathrm{OPT}$.
5. For disks of diameter 1 and strips of width $\ell$, which part of the proof changes, and which constant enters the size of the cell optimum?

## References
