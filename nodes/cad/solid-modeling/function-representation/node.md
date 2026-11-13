---
tag: 6SDGKH
kind: model
slug: function-representation
name: Function representation
aliases:
- FRep
- F-rep
area: cad/solid-modeling
level: advanced
summary: Represents a solid as the set where a continuous real function is at least 0. Booleans, blends, offsets and maps are operations that make new functions from old ones.
prereqs: [implicit-surface, constructive-solid-geometry]
see_also: [signed-distance-function, r-set, regularized-set-operations, spatial-occupancy-enumeration, brep-to-csg-conversion, blending-surface, isosurface-extraction, sphere-tracing]
sources:
  - paper: doi:10.1007/BF02464333
    title: Alexander Pasko, Valery Adzhiev, Alexei Sourin and Vladimir Savchenko, Function representation in geometric modeling, concepts, implementation and applications, The Visual Computer 11(8), 429 to 446, 1995
    locator: the definition of an object by f(X) ≥ 0 in n dimensions, and the operations on the defining function, set-theoretic operations by R-functions, blending, offsetting, bijective mapping, projection, Cartesian product and metamorphosis
  - paper: doi:10.1017/S096249290631001X
    title: Vadim Shapiro, Semi-analytic geometry with R-functions, Acta Numerica 16, 239 to 303, 2007
    locator: the definition of R-functions, the systems R_α with min and max as the case α = 1, their smoothness, and their history from Rvachev's work of the 1960s
  - paper: doi:10.1093/comjnl/16.2.157
    title: A. Ricci, A constructive geometry for computer graphics, The Computer Journal 16(2), 157 to 160, 1973
    locator: union and intersection of solids given by functions, and their smooth approximations that blend the joins
  - book: isbn:9783540646631
    title: Jacek Bochnak, Michel Coste and Marie-Françoise Roy, Real Algebraic Geometry, Springer, 1998
    locator: Chapter 2, Section 2.7, Theorem 2.7.2 (the finiteness theorem, every closed semi-algebraic set is a finite union of basic closed semi-algebraic sets)
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the properties of a representation scheme, its domain, validity, unambiguity and uniqueness, used here to place F-rep among the schemes
---

Function representation (F-rep) describes a solid by one real function. A continuous function $f$ on space defines the solid $\{x : f(x) \ge 0\}$: the points with $f > 0$ are inside, the points with $f = 0$ are on the boundary, and the points with $f < 0$ are outside. A union, an intersection, a blend or a twist of solids is then an operation that makes a new function from the old ones, so a model is an expression tree of primitives and operations, like a [CSG tree](/constructive-solid-geometry/) with more kinds of nodes. Pasko, Adzhiev, Sourin and Savchenko proposed this framework in 1995, and its set operations use the R-functions of Rvachev, of which $\min$ and $\max$ are the simplest. The page has the kind "model", but F-rep is a representation scheme, not a model of cost; so the four sections of the model kind give the representation ("the machine"), what it can express ("what it counts"), its relation to other representations, and the known results.

## The machine

The "machine" here is the representation: the data that stores a solid and the one query that it answers directly, the sign of $f$ at a point. An F-rep object in $\mathbb{R}^n$ is given by a continuous function $f : \mathbb{R}^n \to \mathbb{R}$, and the object is

$$
S(f) = \{x \in \mathbb{R}^n : f(x) \ge 0\}.
$$

The sign is the opposite of the [signed distance function](/signed-distance-function/), which is negative inside; if $d$ is the signed distance to a solid, then $f = -d$ represents it here. The function is stored as an expression: a tree whose leaves are primitives and whose inner nodes are operations. To classify a point, evaluate the tree at the point and look at the sign of the value. This takes one pass over the tree.

Some primitives, with $c$ a point and $r > 0$:

| primitive | function $f(x)$ |
|---|---|
| ball of radius $r$ at $c$ | $r^2 - \lVert x - c \rVert^2$ |
| halfspace $a \cdot x \le b$ | $b - a \cdot x$ |
| infinite cylinder of radius $r$ about the $z$ axis | $r^2 - x_1^2 - x_2^2$ |
| a sampled volume, such as a CT scan | the interpolated value minus a threshold |

The set operations come from R-functions. For a parameter $\alpha$ with $-1 < \alpha \le 1$,

$$
f_1 \vee_\alpha f_2 = \frac{f_1 + f_2 + \sqrt{f_1^2 + f_2^2 - 2 \alpha f_1 f_2}}{1 + \alpha}, \qquad f_1 \wedge_\alpha f_2 = \frac{f_1 + f_2 - \sqrt{f_1^2 + f_2^2 - 2 \alpha f_1 f_2}}{1 + \alpha}.
$$

Union is $f_1 \vee_\alpha f_2$, intersection is $f_1 \wedge_\alpha f_2$, complement is $-f$ and difference is $f_1 \wedge_\alpha (-f_2)$. With $\alpha = 1$ the root is $\lvert f_1 - f_2 \rvert$, so $\vee_1 = \max$ and $\wedge_1 = \min$. With $\alpha = 0$ the operations are $f_1 + f_2 \pm \sqrt{f_1^2 + f_2^2}$, which are smooth wherever $f_1$ and $f_2$ are smooth and not both 0.

The other operations of the F-rep framework act on the function in the same way. The blend below is the bounded blending used in F-rep: a displacement added to an R-function.

| operation | new function | what it does |
|---|---|---|
| blended union | $f_1 \vee_\alpha f_2 + \dfrac{a_0}{1 + (f_1 / a_1)^2 + (f_2 / a_2)^2}$ | adds material near the meeting of the two boundaries, so the join is rounded; $a_0 < 0$ removes material instead |
| offset | $f - t$ or $f + t$ | shrinks or grows the solid; it is the true offset by $t$ only when $f$ is a distance |
| bijective map $T$ | $f(T^{-1}(x))$ | moves, scales, twists or bends the solid |
| metamorphosis | $(1 - \tau) f_1 + \tau f_2$ for $0 \le \tau \le 1$ | turns one solid into the other as $\tau$ goes from 0 to 1 |
| Cartesian product | $f_1(x) \wedge_\alpha f_2(y)$ on the pairs $(x, y)$ | the product of an $n$-dimensional and an $m$-dimensional object |
| projection | $\max_y f(x, y)$ | the shadow of an object of dimension $n + 1$ in dimension $n$ |

## What it counts

F-rep counts no cost; this section says which solids it can express. In the terms of Requicha's theory of [representation schemes](/r-set/), F-rep has these properties.

- **Domain.** Every closed set is $S(f)$ for some continuous $f$, for example $f(x) = -\operatorname{dist}(x, S)$. So the domain is limited only by the primitives and operations that a system offers. With polynomial primitives and $\min$ and $\max$, the domain is exactly the closed semialgebraic sets (see the known results).
- **Validity.** Every continuous $f$ gives a closed set, but the set can be empty, unbounded, or not regular. For $f(x) = -x_1^2$ the set is the plane $x_1 = 0$, which has no interior. So a valid solid needs a check that the tree alone does not give.
- **Unambiguity.** The function decides each point, so the set is fixed by the function.
- **Uniqueness.** It fails. The functions $f$, $2f$ and $f^3$, and the R-function operations for every $\alpha$, give the same set with different functions.

The model is not limited to three dimensions. A function of $(x, \tau)$ is an object that changes with the time $\tau$, a function of more coordinates can carry material or colour, and the product and the projection move between dimensions.

## Relation to other models

The other models here are the other representation schemes of solids and surfaces.

- **[Constructive solid geometry](/constructive-solid-geometry/).** A CSG tree whose primitives have defining functions becomes an F-rep tree when each $\cup^*$, $\cap^*$ and $-^*$ is replaced by $\max$, $\min$ and $\min(f_1, -f_2)$. The known results below give the condition under which this is exact for the regularized operations. Blends, metamorphosis and general maps have no CSG node, so F-rep is the larger scheme.
- **[Implicit surfaces](/implicit-surface/).** The boundary $f = 0$ is an implicit surface, and it is a smooth surface where the gradient of $f$ is not 0. F-rep is about the solid, not about the surface: the sign gives the inside.
- **Distance functions.** A signed distance is one choice of $f$, with the opposite sign. F-rep does not need it: most F-rep functions, among them every $\vee_0$ and $\wedge_0$ result, are not distances.
- **[Spatial occupancy enumeration](/spatial-occupancy-enumeration/).** Sampling the sign of $f$ at the centres of grid cells gives a voxel set, and a voxel grid of values with interpolation gives an F-rep primitive.
- **[Boundary representation](/boundary-representation/).** F-rep stores no faces or edges. A B-rep or a mesh must be computed, usually by [isosurface extraction](/isosurface-extraction/) such as [marching cubes](/marching-cubes/), and it is an approximation. In the other direction, [B-rep to CSG conversion](/brep-to-csg-conversion/) in the work of Shapiro and Vossler finds a Boolean expression of halfspaces, and R-functions can turn such an expression into one function.
## Known results in the model

**The sign sets of min and max.** For continuous $f$ and $g$, $S(\max(f, g)) = S(f) \cup S(g)$, $S(\min(f, g)) = S(f) \cap S(g)$ and $S(\min(f, -g)) = S(f) \cap \{g \le 0\}$, since $\max(a, b) \ge 0$ exactly when $a \ge 0$ or $b \ge 0$, and $\min(a, b) \ge 0$ exactly when both are. These are the ordinary set operations, not the [regularized](/regularized-set-operations/) ones. For the halfspaces $f = x_1$ and $g = -x_1$, $S(\min(f, g))$ is the plane $x_1 = 0$: a dangling face.

**The regularized reading.** Read the solid of $f$ as $[f] = \operatorname{cl}\{f > 0\}$, which is always closed and regular. Suppose the zero sets $\{f = 0\}$ and $\{g = 0\}$ have no interior. Then $[\max(f, g)] = [f] \cup^* [g]$, $[\min(f, g)] = [f] \cap^* [g]$ and $[\min(f, -g)] = [f] -^* [g]$, and the three new functions again have zero sets with no interior, so the rule holds for whole trees. In the example above, $[\min(f, g)] = \emptyset$, the regularized answer.

*Proof.* Write $A = [f]$, $B = [g]$, $P = \{f > 0\}$ and $Q = \{g > 0\}$; these sets are open, and $P$ is dense in $A$. Union: $\{\max(f, g) > 0\} = P \cup Q$, whose closure is $A \cup B$, and a union of two regular closed sets is regular, so it is $A \cup^* B$. Intersection: let $U = \operatorname{int} A \cap \operatorname{int} B = \operatorname{int}(A \cap B)$. The open set $P$ is dense in $\operatorname{int} A$, so $P \cap U$ is dense and open in $U$, and in the same way $Q \cap U$ is dense and open in $U$. Two dense open subsets of $U$ meet in a dense subset, so $\operatorname{cl}(P \cap Q) = \operatorname{cl} U = A \cap^* B$. Difference: $A -^* B = \operatorname{cl}(\operatorname{int} A \cap (\mathbb{R}^n \setminus B))$, because $B$ is closed. The set $N = \{g < 0\}$ is open and misses $B$. Each nonempty open $W$ outside $B$ has $g \le 0$ on it, and $W$ is not inside the zero set of $g$, so $W$ meets $N$: $N$ is dense in $\mathbb{R}^n \setminus B$. As for the intersection, $\operatorname{cl}(P \cap N) = A -^* B$. The zero sets of $\max(f, g)$ and $\min(f, \pm g)$ lie in the union of the zero sets of $f$ and $g$, a finite union of closed sets with no interior, which has no interior. $\square$

**R-functions keep the sign of min and max.** For $-1 < \alpha \le 1$, $f_1 \vee_\alpha f_2$ has the sign of $\max(f_1, f_2)$ and $f_1 \wedge_\alpha f_2$ has the sign of $\min(f_1, f_2)$, so every result above holds for them too. *Proof.* Write $x = f_1$, $y = f_2$ and $D = x^2 + y^2 - 2 \alpha x y$, so $D - (x + y)^2 = -2(1 + \alpha) x y$. If $x, y < 0$, then $D < (x + y)^2$ and $x + y + \sqrt D < 0$. If one of them is 0 and the other is at most 0, the sum is 0. If $x y < 0$, then $\sqrt D > \lvert x + y \rvert$ and the sum is positive; if $x, y \ge 0$ and not both 0, the sum is positive. Divide by $1 + \alpha > 0$. For $\wedge_\alpha$, note $f_1 \wedge_\alpha f_2 = -((-f_1) \vee_\alpha (-f_2))$. $\square$ This is the defining property of an R-function: its sign depends only on the signs of its arguments, through a Boolean function. It also means that an exact sign test of an R-function tree needs no square roots: compute the signs of the leaves and combine them by the Boolean rules, as in [exact geometric computation](/exact-geometric-computation/).

**The functions are not the same as the sets.** The operations $\vee_\alpha$ and $\wedge_\alpha$ for $\alpha < 1$ are not idempotent on functions: $f \vee_0 f = (2 + \sqrt 2) f$ for $f \ge 0$. So the function of a tree depends on its shape, a distance function does not stay a distance after an R-function, and an offset $f - t$ of such a result is not the true offset by $t$ (see [solid offsetting](/solid-offsetting/)).

**The domain with polynomials.** If the primitives are polynomials and the operations are $\min$, $\max$ and $-f$, then $S(f)$ is a closed semialgebraic set, by induction on the tree. Conversely, by the finiteness theorem of real algebraic geometry, every closed [semialgebraic set](/semialgebraic-set/) is a finite union of sets $\{p_{i1} \ge 0, \ldots, p_{ik} \ge 0\}$, so it is $S(\max_i \min_j p_{ij})$.

**Point membership and rendering.** One point test costs one evaluation of the tree, $O(N)$ operations for a tree of $N$ nodes. With [interval arithmetic](/interval-arithmetic/), the same tree evaluated on a box gives an interval that contains every value of $f$ on the box. If the interval is positive, the whole box is inside; if it is negative, the whole box is outside. This gives guaranteed in and out boxes for meshing and for octrees, and only the unknown boxes need more work. Ray casting needs the first root of $f$ along a ray; when $f$ has a known Lipschitz constant ([Lipschitz condition](/lipschitz-condition/)), [sphere tracing](/sphere-tracing/) finds it without missing a thin part. Without such a bound, sampling of $f$ at grid points or along a ray can miss features smaller than the step. These guarantees are proved; the speed of the methods depends on the model and is only measured.

**History.** Ricci in 1973 defined union and intersection of solids given by functions, with $\max$ and $\min$, and smooth approximations of them that blend the joins. Rvachev developed the theory of R-functions from the 1960s, as Shapiro's survey of 2007 describes. Pasko, Adzhiev, Sourin and Savchenko gave the F-rep framework in 1995, with R-functions for the set operations and a list of other operations on the defining function, in any number of dimensions.

## References
