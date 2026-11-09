---
tag: VWN457
kind: theorem
slug: picks-theorem
name: Pick's theorem
aliases:
- Pick's formula
- Pick theorem
area: geometry/polygons
level: intro
summary: For a lattice polygon, area equals I + B/2 - 1, with I interior and B boundary lattice points.
prereqs: [simple-polygon, polygon-triangulation, shoelace-formula, gcd-of-two-integers]
see_also: [lattice-points-in-non-lattice-polygon, lattice-point-counting, polygon-area, polygon-with-holes, oriented-triangle-area, unimodular-matrix, lattice, euler-formula]
sources:
  - paper: "Georg Pick, Geometrisches zur Zahlenlehre, Sitzungsberichte des deutschen naturwissenschaftlich-medicinischen Vereines fuer Boehmen Lotos in Prag 19, 1899, 311 to 319"
    locator: the original statement and proof
  - paper: "Branko Gruenbaum and G. C. Shephard, Pick's theorem, American Mathematical Monthly 100(2), 1993, 150 to 161"
    locator: the whole paper (proofs, the version for polygons with holes, and the history)
  - book: "Martin Aigner and Guenter M. Ziegler, Proofs from THE BOOK, Springer"
    locator: the chapter Three applications of Euler's formula (Pick's theorem from Euler's formula, and the area of an elementary triangle)
  - book: "Matthias Beck and Sinai Robins, Computing the Continuous Discretely, Springer"
    locator: Chapter 2, A Gallery of Discrete Volumes (Pick's theorem, and Reeve's tetrahedra for the failure in dimension 3)
  - paper: "J. E. Reeve, On the volume of lattice polyhedra, Proceedings of the London Mathematical Society (3) 7, 1957, 378 to 395"
    locator: the empty lattice tetrahedra of unbounded volume
---

Pick's theorem gives the area of a simple polygon whose vertices have integer coordinates by counting lattice points: $A = I + B/2 - 1$, where $I$ is the number of lattice points strictly inside and $B$ the number on the boundary. Georg Pick proved it in 1899. It turns a question about area into a question about counting, and back: with the [shoelace formula](/shoelace-formula/) for $A$ and a [gcd](/gcd-of-two-integers/) per edge for $B$, it counts the interior lattice points of a polygon in $O(n \log C)$ time, with no enumeration.

## Statement

**Notation.** A polygon is a cyclic list of vertices $v_0, \ldots, v_{n-1}$ with edges $v_i v_{i+1}$, indices modulo $n$, and a point is $p = (x, y)$. A *lattice point* is a point of $\mathbb{Z}^2$, and a *lattice polygon* is a polygon whose vertices are all lattice points. For a [simple polygon](/simple-polygon/) $P$, $R$ is its closed region, $A$ the area of $R$, $I$ the number of lattice points in the interior of $R$, and $B$ the number of lattice points on the boundary.

**Theorem (Pick, 1899).** For every simple lattice polygon,

$$A = I + \frac{B}{2} - 1.$$

**Computing $B$.** The edge from $a$ to $b$ contains exactly $\gcd(|b_x - a_x|, |b_y - a_y|) + 1$ lattice points, so $B = \sum_i \gcd(|v_{i+1,x} - v_{i,x}|, |v_{i+1,y} - v_{i,y}|)$, each vertex being counted once.

## In plain words

Draw a shape with straight sides on squared paper, with every corner on a crossing of the grid lines. Count the crossings strictly inside the shape, and the crossings on its outline. The area, in squares, is the inside count, plus half the outline count, minus one.

So the area of such a shape can be read off by counting dots, and the number of dots inside can be found from the area and the outline without looking inside at all.

## Proof

The proof gives each lattice point a weight equal to the fraction of the space around it that the region covers, shows that the total weight is $I + B/2 - 1$ and that it adds up like area, and then checks it on the smallest lattice triangles.

**Step 1 (the weight).** For a closed polygonal region $X$ and a point $p$, let $w_X(p) = \lim_{r \to 0} \operatorname{area}(X \cap D(p, r)) / (\pi r^2)$, where $D(p, r)$ is the disk of radius $r$ around $p$. For a simple polygon with region $R$ and $r$ small, $R \cap D(p, r)$ is a circular sector whose angle is the angle of $R$ at $p$. So $w_R(p) = 1$ for an interior point, $0$ for an exterior point, $1/2$ for a boundary point that is not a corner, and $\theta / (2\pi)$ at a corner with interior angle $\theta$. Let $W(X) = \sum_{p \in \mathbb{Z}^2} w_X(p)$, a finite sum.

**Step 2 ($W(R) = I + B/2 - 1$).** Let $P$ be a simple lattice polygon, and let its corners (the vertices with interior angle other than $\pi$) be $m \ge 3$ in number. The corners are vertices, so they are lattice points. The interior angles of a simple polygon with $m$ corners sum to $(m - 2)\pi$, by a [triangulation](/polygon-triangulation/) into $m - 2$ triangles. By Step 1,

$$W(R) = I + \frac{B - m}{2} + \sum_{\text{corners}} \frac{\theta}{2\pi} = I + \frac{B - m}{2} + \frac{m - 2}{2} = I + \frac{B}{2} - 1.$$

**Step 3 ($W$ is additive).** Let $X = X_1 \cup \cdots \cup X_k$, where the $X_j$ are polygonal regions with pairwise disjoint interiors. Two of them meet only in boundary points, a set of area zero, so $\operatorname{area}(X \cap D) = \sum_j \operatorname{area}(X_j \cap D)$ for every disk $D$. Hence $w_X(p) = \sum_j w_{X_j}(p)$ for every $p$, and $W(X) = \sum_j W(X_j)$. Area is additive in the same way.

**Step 4 (a primitive triangle has area $1/2$).** Call a lattice triangle *primitive* if its only lattice points are its three vertices. Let $T$ be primitive. Translating by a lattice vector maps $\mathbb{Z}^2$ to itself, so we may take the vertices to be $0$, $u$ and $v$, with $u$ and $v$ linearly independent. The point reflection $p \mapsto u + v - p$ maps $\mathbb{Z}^2$ to itself and $T$ onto the triangle $u + v, v, u$, so the parallelogram $\{s u + t v : 0 \le s, t \le 1\}$ contains no lattice points except $0, u, v, u + v$. Hence the half-open parallelogram $F = \{s u + t v : 0 \le s, t < 1\}$ contains only the lattice point $0$. Let $z \in \mathbb{Z}^2$. Write $z = \alpha u + \beta v$ with real $\alpha, \beta$, and let $\lambda = \lfloor \alpha \rfloor u + \lfloor \beta \rfloor v$, a lattice point. Then $z - \lambda$ is a lattice point in $F$, so $z = \lambda$. This shows that every lattice point, in particular $(1, 0)$ and $(0, 1)$, is an integer combination of $u$ and $v$. So the integer matrix $M$ with columns $u, v$ has an integer matrix $N$ with $M N = \mathrm{Id}$, and $\det M \cdot \det N = 1$ with both factors integers, so $|\det M| = 1$. The area of $T$ is $|\det M| / 2 = 1/2$. Also $W(T) = 0 + 3/2 - 1 = 1/2$ by Step 2.

**Step 5 (every lattice triangle).** Let $T$ be a lattice triangle. We show $W(T) = \operatorname{area}(T)$ by induction on the number of lattice points in $T$. If $T$ is primitive, this is Step 4. Otherwise let $p$ be a lattice point of $T$ other than a vertex. If $p$ is interior, the segments from $p$ to the three vertices split $T$ into three triangles; if $p$ is inside an edge, the segment from $p$ to the opposite vertex splits $T$ into two. The pieces are lattice triangles of positive area with disjoint interiors, each has lattice points only among those of $T$, and each misses a vertex of $T$. So each piece has fewer lattice points, and by induction $W$ equals the area on each piece. By Step 3 the same holds for $T$.

**Step 6 (every simple lattice polygon).** A simple polygon has a [triangulation](/polygon-triangulation/) by diagonals between its vertices, so its region $R$ is a union of lattice triangles with disjoint interiors. By Steps 3 and 5, $W(R) = \operatorname{area}(R) = A$, and by Step 2, $W(R) = I + B/2 - 1$. $\blacksquare$

**The edge count.** For the edge from $a$ to $b$ with $g = \gcd(|b_x - a_x|, |b_y - a_y|)$, the points $a + (k/g)(b - a)$ for $k = 0, \ldots, g$ are lattice points. A lattice point $a + t(b - a)$ with $0 \le t \le 1$ needs $t(b_x - a_x)$ and $t(b_y - a_y)$ to be integers, which forces $t$ to be a multiple of $1/g$. So the edge has $g + 1$ lattice points, and summing $g$ over the edges counts every boundary lattice point once.

## Consequences

- **Interior points from area.** $I = A - B/2 + 1$. With the [shoelace formula](/shoelace-formula/) for $2A$ and a gcd per edge for $B$, this counts the interior lattice points in $O(n \log C)$ time for coordinates of size $C$, which is the standard method for [lattice point counting](/lattice-point-counting/) in lattice polygons. For polygons with non-lattice vertices, see [lattice points in a non-lattice polygon](/lattice-points-in-non-lattice-polygon/).
- **Half-integer areas.** The area of a lattice polygon is a multiple of $1/2$. This also follows from the shoelace formula.
- **No equilateral lattice triangle.** An equilateral triangle with side $s$ has area $(\sqrt{3}/4) s^2$. For a lattice triangle, $s^2$ is an integer, so this area is irrational, but Pick's theorem makes it rational.
- **Unimodular bases.** Step 4 shows that two lattice vectors $u, v$ span a primitive triangle if and only if $|u \times v| = 1$, that is, if and only if they form a basis of $\mathbb{Z}^2$; see [unimodular matrix](/unimodular-matrix/). Consecutive fractions $a/b < c/d$ of a [Farey sequence](/farey-sequence/) satisfy $bc - ad = 1$, which is this fact for the vectors $(b, a)$ and $(d, c)$.
- **Polygons with holes.** For a lattice [polygon with holes](/polygon-with-holes/) with $h$ holes, $A = I + B/2 - 1 + h$, where $B$ counts the lattice points on all boundary rings. The proof is the same, with the interior angle sum $(N - 2 + 2h)\pi$ for $N$ corners in all, which comes from the [Euler formula](/euler-formula/) or from a triangulation into $N - 2 + 2h$ triangles.

## Tightness

**Examples where it holds.** The triangle $(0,0), (5,1), (2,4)$ has $2A = 18$, edges with gcds $1, 3, 2$, so $B = 6$, and $I = 9 - 3 + 1 = 7$ interior points. The nonconvex polygon $(0,0), (6,0), (6,2), (3,1), (2,4), (0,3)$ has $2A = 28$, $B = 6 + 2 + 1 + 1 + 1 + 3 = 14$ and $I = 8$; and $14 = 8 + 7 - 1$.

**The vertices must be lattice points.** The square $[0, 1/2]^2$ has area $1/4$, but its only lattice point is the corner $(0,0)$, so $I + B/2 - 1 = -1/2$.

**The polygon must be simple.** The bowtie $(0,0), (2,2), (2,0), (0,2)$ crosses itself at $(1,1)$. Its two triangles have total area $2$, while $I = 0$ and $B = 7$, so $I + B/2 - 1 = 5/2$. Each triangle alone satisfies the formula with $I = 0$, $B = 4$; the shared point $(1,1)$ is counted once instead of twice.

**Holes change the constant.** The square $[0,3]^2$ with the hole $[1,2]^2$ has area $8$, $I = 0$ and $B = 12 + 4 = 16$, so $I + B/2 - 1 = 7$. The corrected formula with $h = 1$ gives $8$.

**No such formula in dimension 3.** Reeve's tetrahedra with vertices $(0,0,0), (1,0,0), (0,1,0), (1,1,r)$ contain no lattice points except their four vertices for every positive integer $r$, but have volume $r/6$. So no formula in the numbers of interior and boundary lattice points gives the volume. The right generalization is the Ehrhart polynomial, which counts the lattice points of all dilates $tP$.

## History

Georg Pick published the theorem in 1899 in Prague, in a paper on geometry in number theory. It became widely known after Hugo Steinhaus included it in his book Mathematical Snapshots. Reeve showed in 1957 that it has no direct analogue in three dimensions, and gave a version with the dilate $2P$. Ehrhart's theory of lattice point counting polynomials (1962) puts it in a general setting: for a lattice polygon, the number of lattice points in $tP$ is $A t^2 + (B/2) t + 1$. Grünbaum and Shephard (1993) surveyed the many proofs and generalizations.

## References
