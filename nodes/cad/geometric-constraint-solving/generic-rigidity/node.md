---
tag: 3R139P
kind: definition
slug: generic-rigidity
name: Generic rigidity
aliases:
- combinatorial rigidity
area: cad/geometric-constraint-solving
level: core
summary: A graph is generically rigid in d dimensions when its frameworks at almost all positions are rigid, a property of the graph alone.
prereqs: [bar-and-joint-framework, infinitesimal-rigidity]
see_also: [laman-theorem, pebble-game-rigidity, maxwell-counting-rule, tay-theorem, global-rigidity, schwartz-zippel-lemma, distance-based-formation-control, degrees-of-freedom-analysis]
sources:
  - paper: doi:10.1090/S0002-9947-1978-0511410-9
    title: L. Asimow and B. Roth, The rigidity of graphs, Transactions of the American Mathematical Society 245, 279 to 289, 1978
    locator: the regular points of the edge function and the theorem that rigidity and infinitesimal rigidity agree at them
  - book: isbn:9780821838013
    title: Jack Graver, Brigitte Servatius and Herman Servatius, Combinatorial Rigidity, Graduate Studies in Mathematics 2, American Mathematical Society, 1993
    locator: Chapter 2, Infinitesimal Rigidity (generic frameworks), Chapter 4, Linear and Planar Rigidity, and Chapter 5, Rigidity in Higher Dimensions
  - paper: doi:10.1137/0603009
    title: L. Lovász and Y. Yemini, On generic rigidity in the plane, SIAM Journal on Algebraic and Discrete Methods 3(1), 91 to 98, 1982
    locator: the rank formula of the generic planar rigidity matroid, and the theorem that 6-connected graphs are generically rigid in the plane
  - paper: doi:10.1109/MCS.2008.929280
    title: B. D. O. Anderson, C. Yu, B. Fidan and J. M. Hendrickx, Rigid graph control architectures for autonomous formations, IEEE Control Systems Magazine 28(6), 48 to 63, 2008
    locator: the use of rigid graphs for formation shape control and the Laman test for formations in the plane
  - paper: doi:10.1109/TMC.2006.174
    title: J. Aspnes, T. Eren, D. K. Goldenberg, A. S. Morse, W. Whiteley, Y. R. Yang, B. D. O. Anderson and P. N. Belhumeur, A theory of network localization, IEEE Transactions on Mobile Computing 5(12), 1663 to 1678, 2006
    locator: the conditions of rigidity and global rigidity for sensor network localization
---

A graph is generically rigid in $\mathbb{R}^d$ when its [frameworks](/bar-and-joint-framework/) are rigid at almost every placement of the vertices. Rigidity of one framework depends on the exact coordinates, but at a *generic* placement it depends only on the graph, because there rigidity and [infinitesimal rigidity](/infinitesimal-rigidity/) agree and the rank of the rigidity matrix takes its largest value. In the plane [Laman's theorem](/laman-theorem/) turns generic rigidity into a count of edges on subsets, which the [pebble game](/pebble-game-rigidity/) tests in $O(n^2)$ time. In three and more dimensions no such count is known.

## Definition

Let $G = (V, E)$ be a graph with $n$ vertices and $m$ edges, $d \ge 1$, and $D = d(d + 1)/2$. Let $R(G, p)$ be the rigidity matrix of the framework $(G, p)$, with one row per edge.

**Generic rank.** The *generic rank* of $G$ in $\mathbb{R}^d$ is
$$ r_d(G) = \max_{p \in \mathbb{R}^{dn}} \operatorname{rank} R(G, p). $$

**Generic placement.** A placement $p$ is *generic* if its $dn$ coordinates are algebraically independent over $\mathbb{Q}$: no nonzero polynomial with integer coefficients vanishes at them. Almost every placement is generic, in the sense of measure, since there are countably many such polynomials and each has a zero set of measure zero.

**Lemma 1.** At every generic $p$, $\operatorname{rank} R(G, p) = r_d(G)$. *Proof.* Each $r \times r$ minor of $R(G, q)$ is a polynomial in the coordinates of $q$ with integer coefficients. Take $r = r_d(G)$ and a minor that is nonzero at some $q$. As a polynomial it is not zero, so it does not vanish at the algebraically independent coordinates of $p$. So the rank at $p$ is at least $r_d(G)$, and it is at most $r_d(G)$ by definition.

**Definition.** $G$ is *generically rigid* in $\mathbb{R}^d$ if $(G, p)$ is rigid for a generic $p$. By the theorem below, this holds for one generic $p$ if and only if it holds for all of them, and for $n \ge d$ it is equivalent to
$$ r_d(G) = dn - D. $$
For $n < d$ it means that $G$ is complete. $G$ is *generically minimally rigid* (also called isostatic) if it is generically rigid and $G - e$ is not, for every edge $e$; equivalently $m = r_d(G) = dn - D$ (for $n \ge d$).

**Theorem (Asimow and Roth 1978).** At a generic placement $p$, the framework $(G, p)$ is rigid if and only if it is infinitesimally rigid.

*Proof.* Infinitesimal rigidity implies rigidity for every placement (see [infinitesimal rigidity](/infinitesimal-rigidity/)). For the converse, let $n \ge d$ (for $n < d$, let $ij$ be a missing bar of a generic framework that is not complete; turn $p_i$ about the affine span of the other $n - 2$ points, which has dimension at most $d - 4$, so the distances from $p_i$ to those points stay and the distance from $p_i$ to $p_j$ changes) and suppose $(G, p)$ is not infinitesimally rigid. A generic $p$ spans $\mathbb{R}^d$, so the rank form gives $r := r_d(G) < dn - D$. The set of placements with rank $r$ is open, so the rank is constant near $p$, and by the constant rank theorem the fiber $f_G^{-1}(f_G(p))$ is, near $p$, a connected manifold $M$ of dimension $dn - r > D$. The placements congruent to $p$ form a manifold of dimension $D$, so they do not fill $M$: there is a point $q \in M$ that is not congruent to $p$. A path in $M$ from $p$ to $q$ keeps all bar lengths and ends at a non-congruent placement, so it is a non-trivial motion and $(G, p)$ is flexible.

**Random placements.** The proof of Lemma 1 also gives a test. Choose the $dn$ coordinates independently and uniformly from $\{1, \ldots, N\}$. A nonzero minor of size $r$ has degree $r$, so by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) it vanishes with probability at most $r / N \le dn / N$. Computing the rank at such a point, exactly or modulo a large prime, gives $r_d(G)$ with probability at least $1 - dn/N$, and it never gives more. This is a randomized test for generic rigidity in every dimension, an instance of [polynomial identity testing](/polynomial-identity-testing/).

**The graph view.** Generic rigidity is a property of the graph, and the sets of edges whose rows are independent at a generic $p$ form a matroid on $E$, the generic rigidity matroid in dimension $d$. In dimension 1 it is the [graphic matroid](/graphic-matroid/): a graph is generically rigid on the line if and only if it is connected. In dimension 2 its independent sets are the edge sets with at most $2k - 3$ edges on every $k \ge 2$ vertices ([Laman's theorem](/laman-theorem/)). In dimension 3 and more no combinatorial description is known: the count $3k - 6$ is necessary but not sufficient, as the double banana below shows. For the related body-and-bar model, [Tay's theorem](/tay-theorem/) gives a count in every dimension.

**For robotics.** Let $n \ge 2$ robots in the plane hold the distances on the pairs $E$, by sensing or by control. For almost every shape of the formation, the distances fix the shape locally, up to a translation and a rotation, exactly when the graph is generically rigid in the plane, and Laman's count decides it. The formation is generically minimally rigid when it has $2n - 3$ links and no $k \ge 2$ robots carry more than $2k - 3$ of them, so the loss of any single link makes it flexible. The same test applies to the network of measured distances in sensor localization: generic rigidity is necessary for the positions to be locally unique, and unique positions need the stronger [global rigidity](/global-rigidity/). A formation that is rigid as a graph can still be flexible at a special shape, for example with three robots on a line, so controllers keep the formation away from such shapes. See [distance-based formation control](/distance-based-formation-control/) and [formation control](/formation-control/).

## Examples and non-examples

The ranks below are exact ranks at random integer placements. The planar ones agree with the pebble game.

- **4-cycle.** $C_4$ in the plane has generic rank 4 $< 5$, so it is not generically rigid. With one diagonal the rank is 5 $= 2 \cdot 4 - 3$, and the graph is generically minimally rigid.
- **Triangular prism.** Two triangles $012$ and $345$ joined by the edges $03$, $14$, $25$ have $9 = 2 \cdot 6 - 3$ edges and generic rank 9, so the prism is generically minimally rigid in the plane.
- **$K_{3,3}$.** It has generic rank $9 = 2 \cdot 6 - 3$ and is generically minimally rigid in the plane. On six points of a conic its rank drops to 8. So a generically rigid graph can have infinitesimally flexible frameworks at special placements.
- **Enough edges, still flexible.** $K_4$ plus a vertex joined to one vertex of the $K_4$ has $n = 5$ and $7 = 2n - 3$ edges, but generic rank 6. The $K_4$ carries 6 edges on 4 vertices, one more than the 5 that 4 vertices can use, and the pendant vertex can turn. So the total count alone does not decide generic rigidity.
- **Bowtie.** Two triangles that share one vertex have $n = 5$, $6$ edges and generic rank 6 $< 7$. They turn about the shared vertex.
- **Double banana in space.** Take two copies of $K_5$ minus one edge, and glue them at the two ends of the missing edge. The result has $n = 8$ and $m = 18 = 3n - 6$ edges, and every set $X$ of at least 3 vertices spans at most $3|X| - 6$ edges (each banana spans exactly $9 = 3 \cdot 5 - 6$). But its generic rank in $\mathbb{R}^3$ is 17, so it is not generically rigid in space: each banana can turn about the line through the two shared vertices. This is why the counts of [Maxwell's rule](/maxwell-counting-rule/) do not characterize generic rigidity in three dimensions.
- **Dimension 1.** A path is generically rigid on the line, and a graph with two components is not.

## Related definitions

- **[Infinitesimal rigidity](/infinitesimal-rigidity/).** The linear test used at each placement. At generic placements it agrees with rigidity.
- **[Laman's theorem](/laman-theorem/).** The combinatorial description of generic rigidity in the plane. Lovász and Yemini (1982) gave the rank of the planar rigidity matroid by a covering formula and proved that every 6-connected graph is generically rigid in the plane.
- **[Pebble game](/pebble-game-rigidity/).** A fast exact test of the planar count, which also finds the rigid components and the redundant edges.
- **[Henneberg construction](/henneberg-construction/).** Builds every generically minimally rigid graph in the plane from one edge.
- **[Global rigidity](/global-rigidity/).** The generic version asks for a unique realization, not only a locally unique one. It needs redundant rigidity and 3-connectivity in the plane ([Jackson-Jordán theorem](/jackson-jordan-theorem/)).
- **[Degrees of freedom analysis](/degrees-of-freedom-analysis/).** CAD solvers count degrees of freedom in the same way to find well-constrained parts of a constraint system. A generic count can pass while the actual geometry is degenerate, see [well-constrained system](/well-constrained-system/).

## References
