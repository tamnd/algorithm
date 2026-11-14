---
tag: SBR91R
kind: algorithm
slug: modular-fixture-design
name: Brost-Goldberg modular fixture algorithm
aliases:
- modular fixture synthesis
area: cad/manufacturing-process-planning
level: advanced
summary: Brost and Goldberg's complete algorithm that lists all form closure fixtures of three locators and a clamp on a lattice plate for a polygonal part.
solves: [fixture-planning]
model: real-ram
complexity:
  vars: {n: number of edges of the part, d: diameter of the part in lattice units, K: number of fixtures in the output}
  time: {worst: "O(n^4 d^6)"}
  space: {extra: "O(n + K)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1994
  people: [Randy C. Brost, Kenneth Y. Goldberg]
  note: Brost and Goldberg gave the algorithm at ICRA 1994 and in IEEE Transactions on Robotics and Automation in 1996. Zhuang and Goldberg showed in 1996 that some convex polygons have no fixture of this class.
prereqs: [fixture-planning, kinematic-fixture-analysis]
see_also: [three-two-one-locating-principle, form-closure, wrench, point-in-polygon, simple-polygon, minkowski-sum, exact-geometric-computation, caratheodory-theorem]
sources:
  - paper: doi:10.1109/70.481749
    title: Randy C. Brost and Kenneth Y. Goldberg, A complete algorithm for designing planar fixtures using modular components, IEEE Transactions on Robotics and Automation 12(1), 1996, 31 to 46
    locator: the fixture class of three locators and one clamp on a lattice plate for a polygonal part, the enumeration of locator triples and edge triples, and the claim of completeness
  - paper: doi:10.1177/027836499601500608
    title: Yan Zhuang and Ken Goldberg, On the existence of solutions in modular fixturing, International Journal of Robotics Research 15(6), 1996, 646 to 656
    locator: the formal model of lattice locators and clamps with a reach of one unit along a lattice axis, the O(n^5 d^5) bound that they give for the Brost and Goldberg algorithm, convex polygons of any width with no such fixture, and fixtures with four clamps
  - paper: doi:10.1177/027836499000900102
    title: Xanthippi Markenscoff, Luqun Ni and Christos H. Papadimitriou, The geometry of grasping, International Journal of Robotics Research 9(1), 1990, 61 to 74
    locator: four frictionless point contacts are necessary for form closure of a planar part, and enough for almost all parts
---

The Brost-Goldberg algorithm finds every planar modular fixture of a fixed class for a polygonal part. A modular fixture plate has holes on a square lattice. The class has three locators, which are pins in holes, and one clamp, which is anchored at a hole and pushes along a lattice axis. The algorithm puts the three locators on lattice points, tries each triple of edges, solves for each pose of the part that puts the locators on those edges, and then searches the holes near the part for a clamp that gives [form closure](/form-closure/). It is complete: it returns each fixture of the class, or it reports that there is none. Brost and Goldberg (1996) published it, and it is the standard example of a complete algorithm in [fixture planning](/fixture-planning/). This page gives an exact version for point locators and proves that it is complete.

## In plain words

You have a flat part with straight edges and a steel plate with a grid of holes. You put three pins in three holes and push the part against them. A clamp in a fourth hole presses the part against the pins. The part must not be able to slide or turn at all.

The algorithm tries all the ways to do this. It keeps the first pin in one fixed hole, because a shift of the whole layout by grid steps gives the same fixture. It picks two more holes that are close enough to touch the part at the same time. For each choice of three edges, it finds the ways to place the part so that each pin touches its edge. Then it looks at the holes next to the part for a clamp that pushes the part against the pins and holds it.

## The problem

**Input.** A [simple polygon](/simple-polygon/) $P$ with $n$ edges and rational vertices in counterclockwise order, and a clamp reach $\rho > 0$. The lattice is $\mathbb{Z}^2$ with unit spacing.

**Fixture.** A fixture is a pose $g$ of the part (a rotation $R$ and a translation $t$, so a body point $x$ goes to $Rx + t$), three lattice points $q_1 < q_2 < q_3$ in lexicographic order, three edges $e_1, e_2, e_3$, and a clamp $(v, d)$, so that:

1. each $q_k$ is in the relative interior of the edge $g(e_k)$, not at a vertex;
2. $v \in \mathbb{Z}^2$ is strictly outside $g(P)$, and $d$ is one of $(\pm 1, 0)$ and $(0, \pm 1)$;
3. the first point $u$ of the boundary of $g(P)$ on the ray $v + s d$, $s > 0$, is in the relative interior of an edge $e$, with $\lvert u - v \rvert \le \rho$ and $u \notin \{q_1, q_2, q_3\}$;
4. the four contacts give form closure: their [wrenches](/wrench/) positively span $\mathbb{R}^3$.

All contacts are frictionless points. The wrench of a contact at $p$ with inner normal $\nu$ is $(\nu_x, \nu_y, p_x \nu_y - p_y \nu_x)$. A locator is a point, and the clamp is a point at the end of a plunger. This is the model of Zhuang and Goldberg (1996) for the fixtures of Brost and Goldberg, with point fixture elements and $\rho = 1$.

**Output.** Every fixture with $q_1 = (0, 0)$, each one time. A translation by an integer vector maps fixtures to fixtures, so all other fixtures are these, moved on the plate.

## The algorithm

Write $m_k$ for the outward normal of edge $e_k$ in the part frame and $h_k = m_k \cdot a_k$, where $a_k$ is the start vertex of $e_k$. Then $e_k$ lies on the line $m_k \cdot x = h_k$.

```pseudo id=main
MODULAR-FIXTURES(P, ρ)                      ▷ P: polygon with edges e_1 .. e_n, counterclockwise
L1  D ← the diameter of P
L2  for each pair of lattice points q2 < q3, with q1 = (0,0) < q2 and |q_i − q_j| ≤ D for all i, j
L3      for each triple (e_a, e_b, e_c) of edges of P
L4          for each pose g that puts q1, q2, q3 on the lines of g(e_a), g(e_b), g(e_c)
L5              if some q_k is not strictly inside its edge of g(P) then skip this pose
L6              for each lattice point v outside g(P), near g(P), and each d ∈ {+x, −x, +y, −y}
L7                  u ← the first point of ∂g(P) on the ray v + s·d; skip unless u is inside an edge e, |u − v| ≤ ρ and u ∉ {q1, q2, q3}
L8                  if the wrenches of q1, q2, q3 and u positively span R^3 then output (q, edges, g, (v, d, e, u))
```

**Line L2.** The three locators touch the part at the same time, so each pair of them is at most the diameter $D$ apart. The first locator is at the origin, and the other two come after it in lexicographic order. So $q_2$ and $q_3$ are lattice points in a half disk of radius $D$.

**Line L4.** Rotate by the angle $\theta$, with $c = \cos\theta$ and $s = \sin\theta$. The locator $q_k$ is on the line of $g(e_k)$ when $(R m_k) \cdot t = (R m_k) \cdot q_k - h_k$. These are three linear equations in the two entries of $t$. If the three normals are not all parallel, the equations have a solution if and only if the $3 \times 3$ determinant of the system is zero. Expand it along the right side. The cofactors $C_1 = m_2 \times m_3$, $C_2 = m_3 \times m_1$ and $C_3 = m_1 \times m_2$ do not change under a rotation, and $(R m) \cdot q = c\,(m \cdot q) + s\,(m \times q)$. So the condition is one linear equation in $c$ and $s$:

$$A c + B s + C_0 = 0, \qquad A = \sum_k C_k\,(m_k \cdot q_k), \quad B = \sum_k C_k\,(m_k \times q_k), \quad C_0 = -\sum_k C_k h_k.$$

With $r^2 = A^2 + B^2 > 0$ and $\Delta = r^2 - C_0^2 \ge 0$, the line meets the unit circle at

$$c = \frac{-A C_0 \pm B\sqrt{\Delta}}{r^2}, \qquad s = \frac{-B C_0 \mp A\sqrt{\Delta}}{r^2},$$

so there are at most two poses. Cramer's rule on two equations with independent normals gives $t$. If all three normals are parallel or $r^2 = 0$, the line returns no pose. The proof shows that such a triple never gives form closure.

**Exact arithmetic.** Each coordinate of a pose is in the field $\mathbb{Q}(\sqrt{\Delta})$. The implementation stores a number as $a + b\sqrt{\Delta}$ with rational $a$ and $b$. The sign of such a number is exact: if $a$ and $b$ have opposite signs, compare $a^2$ with $b^2 \Delta$. So every test of lines L5 to L8 is an exact sign test, and a contact at the end of an edge is never accepted by rounding.

**Lines L6 and L7.** A clamp hole is within $\rho$ of the boundary, so it is in the bounding box of $g(P)$ grown by $\rho$. The implementation first drops the pairs $(v, d)$ whose segment of length $\rho$ is far from every edge in floating point, with a margin of $10^{-7}$. Then it tests "$v$ outside $g(P)$" with an exact [point in polygon](/point-in-polygon/) test, and finds the first hit $u$ exactly. A hit at a vertex, or on an edge along the ray, is not a valid contact.

**Line L8.** Let $w_1, \ldots, w_4$ be the four wrenches, each with the inner normal of its edge. Set $\lambda_i = (-1)^i \det(w_j : j \ne i)$. Then $\sum_i \lambda_i w_i = 0$. The four wrenches positively span $\mathbb{R}^3$ if and only if all $\lambda_i$ are nonzero and have the same sign. This is the planar form closure test of [kinematic fixture analysis](/kinematic-fixture-analysis/).

## Example

The part is the triangle with vertices $(0, 0)$, $(2, 0)$ and $(1, \tfrac32)$, with $\rho = 1$. Edge $e_0$ is the base, edge $e_1$ the right side and edge $e_2$ the left side. The diameter is $D = 2$. The counts after each line are:

| line | what is counted | count |
|---|---|---|
| L2 | lattice points $q > (0,0)$ with $\lvert q \rvert \le 2$ | 6 |
| L2 | pairs $q_2 < q_3$ with $\lvert q_3 - q_2 \rvert \le 2$ | 10 |
| L3 | pairs times edge triples ($10 \times 27$) | 270 |
| L4 | poses | 428 |
| L5 | poses with each locator inside its edge | 48 |
| L8 | fixtures | 56 |

The 56 fixtures use 36 different pairs of locator sites and edge triples. One of them has $q = ((0,0), (1,0), (1,1))$ and the edges $(e_0, e_0, e_1)$. In the part frame, $m_0 = (0, -2)$ with $h_0 = 0$, and $m_1 = (\tfrac32, 1)$ with $h_1 = 3$. The cofactors are $(3, -3, 0)$, so $A = 0$, $B = -6$ and $C_0 = 0$. The equation is $-6 s = 0$: two locators on the base make the base horizontal. The poses are $c = 1$ and $c = -1$.

- For $c = -1$, the base goes to the segment from $(\tfrac53, 0)$ to $(\tfrac{11}3, 0)$. It does not contain $(0, 0)$, so line L5 skips the pose.
- For $c = 1$, the first equation gives $t_y = 0$ and the second gives $\tfrac32 t_x + t_y = -\tfrac12$, so $t = (-\tfrac13, 0)$. The placed triangle is $(-\tfrac13, 0)$, $(\tfrac53, 0)$, $(\tfrac23, \tfrac32)$. The points $(0,0)$ and $(1,0)$ are inside the base, and $(1,1)$ is inside the right side.

The inner normals have the length of their edge: $(0, 2)$ on the base, $(-\tfrac32, -1)$ on the right side and $(\tfrac32, -1)$ on the left side. The locator wrenches are $w_1 = (0, 2, 0)$, $w_2 = (0, 2, 2)$ and $w_3 = (-\tfrac32, -1, \tfrac12)$. Six pairs $(v, d)$ reach the inside of an edge within distance 1:

| $v$ | $d$ | $u$ | result |
|---|---|---|---|
| $(0, -1)$ | $+y$ | $(0, 0)$ | skip at L7, $u$ is a locator |
| $(1, -1)$ | $+y$ | $(1, 0)$ | skip at L7, $u$ is a locator |
| $(1, 2)$ | $-y$ | $(1, 1)$ | skip at L7, $u$ is a locator |
| $(2, 1)$ | $-x$ | $(1, 1)$ | skip at L7, $u$ is a locator |
| $(0, 1)$ | $+x$ | $(\tfrac13, 1)$ on $e_2$ | $w_4 = (\tfrac32, -1, -\tfrac{11}6)$, $\lambda = (2, 4, 6, 6)$, a fixture |
| $(0, 1)$ | $-y$ | $(0, \tfrac12)$ on $e_2$ | $w_4 = (\tfrac32, -1, -\tfrac34)$, $\lambda = (\tfrac{21}4, \tfrac34, 6, 6)$, a fixture |

For the first fixture, $2 w_1 + 4 w_2 + 6 w_3 + 6 w_4 = (0, 0, 0)$ with all weights positive, so the four contacts positively span $\mathbb{R}^3$. The clamp on the left side pushes the part to the right and down, against the two pins under the base and the pin on the right side.

## Correctness

**Theorem.** MODULAR-FIXTURES$(P, \rho)$ returns each fixture with $q_1 = (0, 0)$ exactly one time, and nothing else.

Soundness follows from the exact tests: line L4 puts the locators on the edge lines, line L5 checks that they are inside the edges, lines L6 and L7 check the clamp, and line L8 checks form closure. For completeness, take a fixture with $q_1 = 0$. Its locators are points of $g(P)$, so they are at most $D$ apart and line L2 tries them. Line L3 tries its edges. Its pose solves the equation of line L4. That equation has at most two solutions unless the three locator wrenches are linearly dependent. Then the null vector of the four wrenches has $\lambda_4 = 0$, so there is no form closure. The clamp hole is in the box of line L6, and the float filter never drops a real hit. A pose and its locators fix the edges, so no fixture comes out twice. The full proof is below.

## Complexity

Let $n$ be the number of edges and $d = D$ the diameter in lattice units. Count field operations in $\mathbb{Q}(\sqrt{\Delta})$; for a fixed input, the numbers have bounded size.

- **Lines L2 and L3.** There are $O(d^2)$ lattice points in a half disk of radius $d$, so $O(d^4)$ pairs, and $n^3$ edge triples. Line L4 runs $O(n^3 d^4)$ times and costs $O(1)$ each time.
- **Line L5.** At most $2$ poses per triple, and $O(1)$ work for each, after the part is placed in $O(n)$.
- **Lines L6 to L8.** The box has $O(d^2)$ holes. For each, the float filter, the point in polygon test and the first hit cost $O(n)$. So one pose that passes line L5 costs $O(n d^2)$.

The worst case is $O(n^3 d^4 \cdot n d^2) = O(n^4 d^6)$. In practice few poses pass line L5 (48 of 428 in the example), so the time is close to the $O(n^3 d^4)$ of the pose step. Only the holes within $\rho$ of the boundary can hold the clamp. Each edge is at most $d$ long, so there are $O(n d)$ such holes. A scan of only these holes costs $O(n^2 d)$ per pose, and the worst case becomes $O(n^3 d^4 \cdot n^2 d) = O(n^5 d^5)$. This is the bound that Zhuang and Goldberg (1996) state for the algorithm of Brost and Goldberg. It is better than $O(n^4 d^6)$ when $n < d$. The extra space is $O(n + K)$, where $K$ is the number of fixtures in the output.

## Properties

- **Complete for its model.** If the list is empty, no fixture of the class exists. This is the main property of the algorithm. A heuristic can only say that it did not find one.
- **Exact.** All signs are computed in $\mathbb{Q}(\sqrt{\Delta})$, so a fixture is never accepted or lost by rounding. The only floating point step is a filter with a margin.
- **Deterministic.** The order of the output is the order of the loops.
- **Lattice invariant.** The output has $q_1 = (0,0)$. Each fixture stands for all its integer translations.
- **Output size.** The number of fixtures grows fast with the size of the part: 56 for the triangle above, 76 for the right triangle with legs 2 and $\tfrac32$.

## Variants and improvements

- **Round locators.** Real locators are pins of radius $r$, with $r$ less than half the lattice spacing. A pin of radius $r$ touches an edge where a point touches the edge moved out by $r$. So a version for round pins works with the boundary of the [Minkowski sum](/minkowski-sum/) of $P$ and a disk of radius $r$, which has arcs at the vertices. Brost and Goldberg treat pins of a fixed size.
- **Quality ranking.** Brost and Goldberg rank the fixtures by a quality measure, so that a planner can take the best one. The complete list makes such a ranking possible.
- **Other fixture classes.** Zhuang and Goldberg (1996) study fixtures with four clamps and no locators. They show that some convex polygons have no fixture with three locators and a clamp, so the empty answer of this algorithm can be correct for a part of any size. They also list complete algorithms for a vise with four locators on a split lattice (Wallack and Canny) and for fixtures with edge contacts (Overmars and others).
- **Three dimensions.** A part in space needs at least 7 frictionless contacts for form closure (Markenscoff, Ni and Papadimitriou 1990). The same plan, contact sites, then poses, then a closure test, applies, but the poses solve larger systems.

## When to use it

Use it when the part is planar, or a prismatic part with a planar section, and the shop has a lattice plate. Use it when you must know if a fixture exists, because it is complete. Use it when you want all the fixtures, to rank them by quality, by access for the tool or by the clamp position. For a single fixture of a large part, a heuristic search over a few candidate sites is faster. For parts with friction, curved edges or a 3D layout, the model does not apply, and a general [fixture planning](/fixture-planning/) method with a [kinematic analysis](/kinematic-fixture-analysis/) of each candidate is the usual way.

## Pitfalls

- **Rounded poses at line L5.** If line L4 gives a pose in floating point, line L5 can accept a contact at a vertex or reject a contact that is just inside the edge. Use exact arithmetic in $\mathbb{Q}(\sqrt{\Delta})$, and test "strictly inside" as two exact sign tests.
- **One root at line L4.** The line $A c + B s + C_0 = 0$ meets the unit circle in two points when $\Delta > 0$. A version that keeps one root loses half of the poses, and the claim of completeness fails.
- **Mixed normals at line L8.** The closure test needs the inner normal for all four contacts. If the locators use the outward normal and the clamp the inner one, line L8 gives the wrong answer. If all four use the outward normal, all $\lambda_i$ change sign, and the test still works.
- **Vertex hits at line L7.** If the clamp ray first meets a vertex, the contact normal is not defined. Line L7 must skip it, not take the normal of one of the two edges.
- **No normal form at line L2.** Without $q_1 = (0, 0)$, each fixture comes with all its integer translations, and the list is infinite.

## Implementations

## History

Brost and Goldberg gave the algorithm at the IEEE International Conference on Robotics and Automation in 1994, and in its full form in IEEE Transactions on Robotics and Automation in 1996. It was the first complete algorithm for modular fixtures. Zhuang and Goldberg (1996) then asked if each polygon has such a fixture, and gave convex polygons of any width that touch at most two lattice points in any pose, so they have none. The idea of form closure goes back to Reuleaux (1876). Four frictionless contacts are necessary in the plane, and Markenscoff, Ni and Papadimitriou (1990) showed that four are enough for almost all planar parts, so three locators and a clamp is the smallest class that can work.

## References
