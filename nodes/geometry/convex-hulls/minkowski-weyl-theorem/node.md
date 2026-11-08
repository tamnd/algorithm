---
tag: TFATJZ
kind: theorem
slug: minkowski-weyl-theorem
name: Minkowski-Weyl theorem
aliases:
- Minkowski-Weyl representation theorem
- main theorem for polytopes
- finite basis theorem for polyhedra
area: geometry/convex-hulls
level: advanced
summary: A polytope is both the convex hull of finitely many points and a bounded intersection of finitely many half-spaces.
prereqs: [convex-polytope, polyhedron, conic-hull, fourier-motzkin-elimination]
see_also: [farkas-lemma, vertex-enumeration, convex-hull-3d, beneath-beyond, facet, caratheodory-theorem, separating-hyperplane-theorem, extreme-point]
sources:
  - book: isbn:9780387943657
    title: Günter M. Ziegler, Lectures on Polytopes, Graduate Texts in Mathematics 152, Springer
    locator: Lecture 1, the main theorem for polytopes and cones and its proof by Fourier-Motzkin elimination; Lecture 8, the upper bound theorem and cyclic polytopes
  - book: isbn:9780471908548
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 7, finitely generated cones, the decomposition of polyhedra, and the Farkas lemma
  - paper: doi:10.1007/BF01292722
    title: Hermann Weyl, Elementare Theorie der konvexen Polyeder, Commentarii Mathematici Helvetici 7, 1935
    locator: the proof that finitely generated cones are intersections of finitely many half-spaces
  - paper: doi:10.1112/S0025579300002850
    title: Peter McMullen, The maximum numbers of faces of a convex polytope, Mathematika 17, 1970
    locator: the proof of the upper bound theorem
---

The Minkowski-Weyl theorem says that a polytope has two equivalent descriptions: as the [convex hull](/convex-hull/) of finitely many points, and as a bounded intersection of finitely many closed half-spaces. The general form says the same for every [polyhedron](/polyhedron/), with a cone of directions added to the convex hull. The theorem is why a hull algorithm can turn a list of points into a list of facets, and why [vertex enumeration](/vertex-enumeration/) can go the other way. It does not say that the two descriptions have similar sizes, and the Upper Bound Theorem shows how far apart they can be.

## Statement

Notation: $d$ is the dimension. For a finite set $W \subseteq \mathbb{R}^d$, $\operatorname{conv}(W)$ is its convex hull and $\operatorname{cone}(W)$ the set of its nonnegative combinations ([conic hull](/conic-hull/)), with $\operatorname{conv}(\emptyset) = \emptyset$ and $\operatorname{cone}(\emptyset) = \{0\}$. A **polyhedron** is a set $\{x \in \mathbb{R}^d : Ax \le b\}$ for a real $m \times d$ matrix $A$ and $b \in \mathbb{R}^m$, so an intersection of $m$ closed half-spaces; it is a **polyhedral cone** when $b = 0$. The sum of sets is $X + Y = \{x + y : x \in X, y \in Y\}$. No general position is needed: points may repeat or lie in a lower-dimensional flat, and inequalities may be redundant.

**Theorem (polytopes).** For $P \subseteq \mathbb{R}^d$ the following are equivalent:

1. $P = \operatorname{conv}(V)$ for a finite set $V \subseteq \mathbb{R}^d$ (a V-polytope);
2. $P = \{x : Ax \le b\}$ for some $A$ and $b$, and $P$ is bounded (an H-polytope).

**Theorem (cones).** A set $C \subseteq \mathbb{R}^d$ is $\operatorname{cone}(W)$ for a finite $W$ if and only if $C = \{x : Ax \le 0\}$ for some matrix $A$.

**Theorem (polyhedra).** A set $P \subseteq \mathbb{R}^d$ is a polyhedron if and only if $P = \operatorname{conv}(V) + \operatorname{cone}(W)$ for finite sets $V, W \subseteq \mathbb{R}^d$.

The direction from inequalities to generators is due to Minkowski and the direction from generators to inequalities to Weyl, which gives the name. The polytope theorem is the case $W = \emptyset$.

## In plain words

A polygon can be given in two ways. You can list its corners, or you can list the straight sides as lines and say which side of each line the polygon is on. The theorem says that this works for every shape of this kind in every dimension, and in both directions. A shape made from finitely many corners can always be cut out by finitely many flat cuts. A bounded shape cut out by finitely many flat cuts always has finitely many corners, and it is the hull of them.

The two lists can have very different lengths. A cube in many dimensions has few sides but very many corners, and some shapes have few corners but very many sides.

## Proof

The proof in [the full proof](proofs/main/) first handles cones and then gets polyhedra from cones by adding one coordinate.

- **Projection.** [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) removes one variable from a system of linear inequalities: every lower bound on the variable must be at most every upper bound. So the projection of a polyhedron is a polyhedron, and of a polyhedral cone a polyhedral cone.
- **Generators to inequalities (Weyl).** $\operatorname{cone}(w_1, \ldots, w_m)$ is the projection onto $x$ of the cone $\{(x, \lambda) : x = \sum_j \lambda_j w_j,\ \lambda \ge 0\}$, so it is a polyhedral cone.
- **Inequalities to generators (Minkowski).** For $C = \{x : Ax \le 0\}$, apply Weyl's direction to the cone generated by the rows $a_i$ of $A$. This writes it as $\{y : By \le 0\}$, and the rows $w_k$ of $B$ generate $C$. Each $w_k$ is in $C$ because $a_i \cdot w_k \le 0$. If some $x \in C$ were outside $\operatorname{cone}(w_k)$, a defining inequality $g \cdot y \le 0$ of that cone, again from Weyl's direction, would have $g \cdot x > 0$. But $g$ lies in the cone of the $a_i$, and then $g \cdot x \le 0$.
- **Homogenization.** $x \in \{x : Ax \le b\}$ exactly when $(x, 1)$ lies in the cone $\{(x, t) : Ax - bt \le 0, t \ge 0\}$. Its generators $(y, 1)$ give $V$ and its generators $(y, 0)$ give $W$. The same trick with the generators $(v, 1)$ and $(w, 0)$ gives the other direction.
- **Bounded case.** A nonzero $w \in W$ gives the unbounded ray $v + \lambda w$ in $P$, so a bounded nonempty $P$ has $\operatorname{cone}(W) = \{0\}$ and is $\operatorname{conv}(V)$.

## Consequences

- **Two descriptions of a polytope.** Every [convex polytope](/convex-polytope/) has a V-description and an H-description. Computing the facets from the points is the convex hull problem, solved in 3D by the [3D convex hull](/convex-hull-3d/) algorithms and in any dimension by [beneath-beyond](/beneath-beyond/). Computing the points from the inequalities is [vertex enumeration](/vertex-enumeration/). For a polytope with the origin in its interior, polarity turns one task into the other.
- **The smallest V is the vertex set.** If $v \in V$ lies in $\operatorname{conv}(V \setminus \{v\})$, dropping it does not change the hull. When no point can be dropped, every point of $V$ is an [extreme point](/extreme-point/) of $P$, and every extreme point of $P$ must be in $V$, as it is not a convex combination of other points of $P$. So $P$ is the hull of its finitely many vertices.
- **Operations on polytopes.** Intersections of polytopes are polytopes, which is clear from the H-description. Linear images and Minkowski sums of polytopes are polytopes, which is clear from the V-description. The theorem lets each operation use the description that makes it easy.
- **Linear programming.** A linear function on $\operatorname{conv}(V)$ reaches its maximum at a point of $V$, since $c \cdot \sum_j \lambda_j v_j \le \max_j c \cdot v_j$. So a linear program over a bounded feasible region has an optimal vertex, which is the base of the simplex method. Over a polyhedron $\operatorname{conv}(V) + \operatorname{cone}(W)$ the objective $\max c \cdot x$ is unbounded exactly when $c \cdot w > 0$ for some $w \in W$.
- **Farkas lemma.** By Weyl's direction, $\operatorname{cone}(a_1, \ldots, a_m) = \{y : Gy \le 0\}$. So if $b$ is not in this cone, some row $g$ of $G$ has $g \cdot b > 0$ and $g \cdot a_i \le 0$ for all $i$. This is the [Farkas lemma](/farkas-lemma/).

## Tightness

- **Boundedness is needed in the polytope theorem.** The half-plane $\{x : x_1 \ge 0\}$ in $\mathbb{R}^2$ is a polyhedron, but it is not the hull of finitely many points. The polyhedron theorem covers it with $V = \{0\}$ and $W = \{(1,0), (0,1), (0,-1)\}$.
- **Finiteness is needed.** A closed disc is the hull of infinitely many points and the intersection of infinitely many half-planes, but it is neither the hull of finitely many points nor an intersection of finitely many half-planes. Each direction of the theorem uses finiteness of the given description.
- **The sizes can be far apart.** The $d$-cube $[0,1]^d$ has $2d$ facets and $2^d$ vertices. Its dual, the cross-polytope $\operatorname{conv}\{\pm e_1, \ldots, \pm e_d\}$, has $2d$ vertices and $2^d$ facets. So neither description is polynomial in the other in general.
- **The Upper Bound Theorem.** A $d$-polytope with $n$ vertices has at most as many faces of each dimension as the cyclic polytope with $n$ vertices in $\mathbb{R}^d$, the hull of $n$ points on the moment curve $t \mapsto (t, t^2, \ldots, t^d)$. For facets the maximum is $\frac{n}{n - m}\binom{n - m}{m}$ for $d = 2m$ and $2\binom{n - m - 1}{m}$ for $d = 2m + 1$, which is $\Theta(n^{\lfloor d/2 \rfloor})$ for fixed $d$. For $d = 2$ this is $n$, and for $d = 3$ it is $2n - 4$. McMullen proved the theorem in 1970. By duality, $m$ half-spaces in $\mathbb{R}^d$ bound a polytope with $O(m^{\lfloor d/2 \rfloor})$ vertices. So converting one description into the other can take output of size $\Theta(n^{\lfloor d/2 \rfloor})$, and this is a lower bound on the time of every hull algorithm that lists facets.
- **Fourier-Motzkin is not efficient.** One elimination step can turn $m$ inequalities into $m^2/4$, so the proof is constructive but the construction can be very slow. Practical conversions use the double description method, beneath-beyond or reverse search.

## History

Hermann Minkowski showed in his work on the geometry of numbers in the 1890s that a bounded intersection of finitely many half-spaces is the hull of finitely many points. Gyula Farkas proved his lemma on linear inequalities in 1902. Hermann Weyl published the converse direction for cones in 1935, in "Elementare Theorie der konvexen Polyeder", and Theodore Motzkin's 1936 thesis gave the decomposition of a general polyhedron into a polytope and a cone. The Upper Bound Theorem was stated by Theodore Motzkin in 1957 and proved by Peter McMullen in 1970. In computational geometry the theorem is the starting point for convex hull and vertex enumeration algorithms.

## References
