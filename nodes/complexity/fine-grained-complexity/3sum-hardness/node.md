---
tag: HMPCF4
kind: concept
slug: 3sum-hardness
name: 3SUM-hardness
aliases:
- 3SUM-hard
area: complexity/fine-grained-complexity
level: advanced
summary: "A problem is 3SUM-hard if 3SUM reduces to it in subquadratic time. Many geometric problems are. Since the 2026 3SUM algorithms, this no longer gives a lower bound."
prereqs: [3sum, 3sum-conjecture, fine-grained-reduction]
see_also: [3sum, 3sum-conjecture, collinear-points, conditional-lower-bound, quadratic-time-hardness, dynamic-lower-bounds, convolution-3sum, fine-grained-equivalence-class]
sources:
  - paper: doi:10.1016/0925-7721(95)00022-2
    title: "Anka Gajentaan and Mark H. Overmars, On a class of O(n^2) problems in computational geometry, Computational Geometry: Theory and Applications 5(3), 1995, 165-185"
    locator: the definition of the relation PR1 << PR2 and of 3SUM-hard problems, the problem GeomBase, and the list of 3SUM-hard problems
  - paper: "Virginia Vassilevska Williams, On some fine-grained questions in algorithms and complexity, Proceedings of the International Congress of Mathematicians (ICM 2018), Vol. 3, 3447-3487"
    locator: the definition of fine-grained reductions and the section on problems that are hard under the 3SUM hypothesis
  - paper: doi:10.1145/1806689.1806772
    title: "Mihai Pătraşcu, Towards polynomial lower bounds for dynamic problems, STOC 2010, 603-610"
    locator: the reduction from 3SUM to Convolution 3SUM, the triangle listing bound and the multiphase problem
  - paper: doi:10.1109/FOCS.2014.53
    title: "Amir Abboud and Virginia Vassilevska Williams, Popular conjectures imply strong lower bounds for dynamic problems, FOCS 2014, 434-443"
    locator: the dynamic lower bounds from the 3SUM conjecture
  - paper: doi:10.1137/1.9781611974331.ch89
    title: "Tsvi Kopelowitz, Seth Pettie and Ely Porat, Higher lower bounds from the 3SUM conjecture, SODA 2016, 1272-1287"
    locator: the reductions from 3SUM to set disjointness and set intersection, and the lower bounds for triangle listing and dynamic problems
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the abstract and the introduction (truly subquadratic 3SUM, Convolution 3SUM and GeomBase, and the remark that collinear points is now open); not yet refereed
---

A problem is 3SUM-hard if [3SUM](/3sum/) reduces to it so that a subquadratic algorithm for the problem gives a subquadratic algorithm for 3SUM. Gajentaan and Overmars defined the class in 1995 and showed that many problems of computational geometry belong to it, among them deciding whether $n$ points in the plane contain three on a line. Later work added problems on graphs, strings and dynamic data structures.

For thirty years, "3SUM-hard" was read as "probably needs quadratic time", because of the [3SUM conjecture](/3sum-conjecture/). In October 2026, preprints by Alman and Vassilevska Williams and by Chan, Itakura, Ma and Yu gave truly subquadratic algorithms for 3SUM. If they are correct, 3SUM-hardness no longer gives any lower bound. The reductions are still theorems, and they still show that each 3SUM-hard problem is at least as hard as 3SUM, but 3SUM is no longer believed to need quadratic time.

The problem is on [3SUM](/3sum/), and the hypothesis is on [3SUM conjecture](/3sum-conjecture/). This page is about the class of problems that 3SUM reduces to.

## In plain words

Some problems hide a copy of another problem inside them. If you can turn every question about adding three numbers into a question about your problem, then your problem is at least as hard as the number question.

For a long time, people believed that the number question needed a slow method. So they used this trick to show that many other problems, mostly about points and lines in the plane, also needed a slow method, unless the belief was wrong.

In 2026, new papers claim a faster method for the number question. The trick still works, and it still shows that each of those problems is at least as hard as the number question. But since the number question is now easier than people thought, the trick no longer shows that the other problems are slow.

## The idea

### The definition of Gajentaan and Overmars

Gajentaan and Overmars write $PR_1 \ll_{f(n)} PR_2$ when every instance of $PR_1$ of size $n$ can be solved with a constant number of instances of $PR_2$ of total size $O(n)$, plus $O(f(n))$ extra time. A problem $PR$ is 3SUM-hard if $3SUM \ll_{f(n)} PR$ for some $f(n) = o(n^2)$.

This definition is strict about size: the instances of $PR$ must have linear total size. So if $PR$ has an $o(n^2)$ algorithm, then 3SUM has an $o(n^2)$ algorithm too. Most of their reductions take $O(n)$ or $O(n \log n)$ time.

### The fine-grained definition

The modern definition uses [fine-grained reductions](/fine-grained-reduction/). A problem $B$ is 3SUM-hard for a time bound $b(n)$ if 3SUM with $a(n) = n^2$ is $(a, b)$-reducible to $B$. Then for every $\varepsilon > 0$ there is a $\delta > 0$ such that an $O(b(n)^{1-\varepsilon})$ algorithm for $B$ gives an $O(n^{2-\delta})$ algorithm for 3SUM.

- The reduction may make many calls on small instances, not only a constant number of calls on linear instances.
- The time bound $b(n)$ need not be $n^2$. For example, Pătraşcu showed that listing $m$ triangles in a graph with $m$ edges is 3SUM-hard for $b(m) = m^{4/3}$.
- The reduction may be randomized. Pătraşcu's reduction from 3SUM to [Convolution 3SUM](/convolution-3sum/) uses hashing, and many later reductions go through it. Chan and He (SOSA 2020) made that step deterministic.

### Hypothesis (used by every bound on this page)

For every $\varepsilon > 0$, 3SUM on $n$ integers in $\{-n^{c}, \ldots, n^{c}\}$ has no $O(n^{2-\varepsilon})$ algorithm on the [word RAM](/word-ram/), with randomized algorithms excluded. For the geometric problems, the same statement for real numbers on the [real RAM](/real-ram/) was used. Both forms are refuted in the 2026 preprints; see [3SUM conjecture](/3sum-conjecture/).

### What a member of the class tells you

Every statement below is conditional, and each has two readings.

- **Before 2026.** If $B$ is 3SUM-hard for $b(n)$, then $B$ has no $O(b(n)^{1-\varepsilon})$ algorithm, conditional on the 3SUM conjecture.
- **After 2026.** The reduction still gives: an $O(b(n)^{1-\varepsilon})$ algorithm for $B$ gives an $O(n^{2-\delta})$ algorithm for 3SUM. Since 3SUM now has an $O(n^{1.9992})$ algorithm (Alman and Vassilevska Williams, arXiv:2610.06783, not yet refereed), this is no longer a contradiction. The lower bound for $B$ is gone, and no upper bound for $B$ follows.

### Hard is not the same as equivalent

3SUM-hardness asks for a reduction in one direction only, from 3SUM to $B$. A problem is subquadratically equivalent to 3SUM only if there is also a reduction from $B$ back to 3SUM; see [fine-grained equivalence class](/fine-grained-equivalence-class/).

- **Equivalent.** Convolution 3SUM, the three-set form of 3SUM, and GeomBase. For these, a fast 3SUM algorithm gives a fast algorithm, and the 2026 algorithms make them truly subquadratic.
- **Hard but not known to be equivalent.** Three [collinear points](/collinear-points/), most other geometric members, and the dynamic and graph members. For these, the 2026 algorithms say nothing. Alman and Vassilevska Williams write that it is now open whether three collinear points can be found in truly subquadratic time.

### Pitfalls

- The direction matters. "3SUM reduces to $B$" makes $B$ 3SUM-hard. "$B$ reduces to 3SUM" makes $B$ easy whenever 3SUM is.
- 3SUM-hard does not mean NP-hard. All the members have polynomial algorithms, most of them quadratic.
- Linear decision tree lower bounds do not transfer through these reductions, because the reductions may use operations that a decision tree of that kind cannot do, such as $a \mapsto a^3$.

## Examples

**From 3SUM to GeomBase.** GeomBase asks: given $n$ points with integer coordinates on the three horizontal lines $y = 0$, $y = 1$ and $y = 2$, is there a non-horizontal line through three of them? Gajentaan and Overmars reduce the three-set form of 3SUM (find $a \in A$, $b \in B$, $c \in C$ with $a + b = c$) to it. Map $a$ to $(2a, 0)$, $c$ to $(c, 1)$ and $b$ to $(2b, 2)$. Three points, one on each line, are on a line exactly when the middle $x$-coordinate is the mean of the other two, that is, when $c = a + b$.

Take $A = \{1, 4, 7\}$, $B = \{2, 5, -3\}$ and $C = \{3, 10, 6\}$. The 9 points are

$$(2,0), (8,0), (14,0), \quad (3,1), (10,1), (6,1), \quad (4,2), (10,2), (-6,2).$$

The solutions of $a + b = c$ are $(1, 2, 3)$, $(1, 5, 6)$ and $(4, 2, 6)$. The non-horizontal lines through three points are exactly the three lines through $(2,0), (3,1), (4,2)$, through $(2,0), (6,1), (10,2)$ and through $(8,0), (6,1), (4,2)$, one for each solution. A non-horizontal line meets each horizontal line at most once, so it cannot hold two points of the same set. The reduction is deterministic, takes $O(n)$ time and makes one call of size $3n$, with $a(n) = b(n) = n^2$.

**From GeomBase to three collinear points.** GeomBase is a special case of the general question "do $n$ points in the plane contain three on a line?", once you remove the horizontal lines, which hold all of a row. So three collinear points is 3SUM-hard, with the identity map. Gajentaan and Overmars also give the direct map $a \mapsto (a, a^3)$ from one-set 3SUM: three distinct points of the cubic $y = x^3$ are on a line exactly when their $x$-coordinates sum to zero.

**From 3SUM to triangle listing.** Pătraşcu (STOC 2010) reduced 3SUM through Convolution 3SUM to listing triangles. The result: listing $m$ triangles in a graph with $m$ edges has no $O(m^{4/3 - \varepsilon})$ algorithm, conditional on the 3SUM conjecture. The reduction is randomized in its first step. Kopelowitz, Pettie and Porat (SODA 2016) proved more bounds of this kind, for set intersection, set disjointness and triangle listing. All these bounds are conditional, and they no longer have a hypothesis that is believed.

## Where it is used

- **Computational geometry.** Gajentaan and Overmars listed many 3SUM-hard problems, for example: GeomBase, three collinear points, separating a set of line segments by a line, deciding whether a set of strips covers a rectangle, deciding whether a set of triangles covers a triangle, visibility between two segments among triangles, and planar motion planning of a segment among obstacles. For most of them, quadratic algorithms are known and the exponent is now open.
- **Dynamic problems.** Pătraşcu, Abboud and Vassilevska Williams, and Kopelowitz, Pettie and Porat used 3SUM-hardness for polynomial bounds on update and query times; see [dynamic lower bounds](/dynamic-lower-bounds/). The bounds that also follow from the [OMv conjecture](/omv-conjecture/) or from [SETH](/strong-exponential-time-hypothesis/) stand. The others lose their base.
- **Graphs and sets.** Triangle listing, set disjointness and set intersection queries, through the reductions of Pătraşcu and of Kopelowitz, Pettie and Porat; see [triangle listing by degree](/triangle-listing-by-degree/) for a simple $O(m^{3/2})$ upper bound.
- **Teaching.** The reduction to GeomBase is a short first example of a [conditional lower bound](/conditional-lower-bound/) for a [quadratic-time](/quadratic-time-hardness/) problem.

## References
