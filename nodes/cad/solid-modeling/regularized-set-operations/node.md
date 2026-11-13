---
tag: DRHW8K
kind: definition
slug: regularized-set-operations
name: Regularized set operations
aliases:
- regularized Boolean operations
- regularized Booleans
area: cad/solid-modeling
level: core
summary: Union, intersection and difference of solids followed by the closure of the interior, so that the result is again a solid and has no dangling faces, edges or points.
prereqs: [r-set]
see_also: [constructive-solid-geometry, solid-boolean-operations, set-membership-classification, boundary-evaluation, manifold-solid, polygon-clipping]
sources:
  - paper: doi:10.1109/TC.1980.1675470
    title: Robert B. Tilove, Set membership classification, a unified approach to geometric intersection problems, IEEE Transactions on Computers C-29(10), 874 to 883, 1980
    locator: the regularized operations and the classification of a candidate set against a CSG tree
  - paper: "Robert B. Tilove and Aristides A. G. Requicha, Closure of Boolean operations on geometric entities, Computer-Aided Design 12(5), 219 to 220, 1980"
    locator: the closure of the r-sets under the regularized operations
  - paper: "Aristides A. G. Requicha and Robert B. Tilove, Mathematical foundations of constructive solid geometry, general topology of closed regular sets, Production Automation Project Technical Memorandum 27, University of Rochester, 1978"
    locator: the closed regular sets and their Boolean algebra
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the regularized set operations in the section on mathematical models of solids
  - book: isbn:9780881751086
    title: Martti Mäntylä, An Introduction to Solid Modeling, Computer Science Press, 1988
    locator: Section 3.4.2, Regularity (p. 33), and Appendix B, Elements of point set topology
---

The regularized set operations are the union, intersection and difference that solid modeling uses. Each one does the ordinary set operation and then takes the closure of the interior of the result. This removes the parts of lower dimension, such as the face that two touching cubes have in common, so the result of an operation on two solids is again a solid. Requicha and Tilove defined them in 1978, and they are the operations of a [CSG tree](/constructive-solid-geometry/).

## Definition

For a set $X \subseteq E^3$, write $\operatorname{int} X$ for its interior and $\operatorname{cl} X$ for its closure, as on the [r-set](/r-set/) page. The *regularization* of $X$ is $r(X) = \operatorname{cl}(\operatorname{int} X)$. For two sets $A$ and $B$, the regularized operations are

$$A \cup^* B = r(A \cup B), \qquad A \cap^* B = r(A \cap B), \qquad A -^* B = r(A \setminus B),$$

and the regularized complement is $c^* A = r(E^3 \setminus A)$. In solid modeling these are the set operations. The ordinary operations are only a step of the definition.

The facts below hold for any closed regular sets $A$ and $B$, and so for any r-sets. Each has a short proof.

1. **$r(X)$ is regular.** Let $Y = \operatorname{cl}(\operatorname{int} X)$. Then $\operatorname{int} X \subseteq \operatorname{int} Y$, since $\operatorname{int} X$ is open and lies in $Y$, so $Y = \operatorname{cl}(\operatorname{int} X) \subseteq \operatorname{cl}(\operatorname{int} Y)$. And $\operatorname{cl}(\operatorname{int} Y) \subseteq \operatorname{cl} Y = Y$. So $Y = r(Y)$, and every regularized result is a closed regular set.
2. **Union needs no regularization.** $\operatorname{int}(A \cup B) \supseteq \operatorname{int} A \cup \operatorname{int} B$, so $r(A \cup B) \supseteq \operatorname{cl}(\operatorname{int} A) \cup \operatorname{cl}(\operatorname{int} B) = A \cup B$. The other inclusion holds because $A \cup B$ is closed. So $A \cup^* B = A \cup B$.
3. **Intersection keeps only shared volume.** An open set lies in $A \cap B$ only if it lies in both, so $\operatorname{int}(A \cap B) = \operatorname{int} A \cap \operatorname{int} B$, and $A \cap^* B = \operatorname{cl}(\operatorname{int} A \cap \operatorname{int} B)$. A point of $A \cap B$ survives only if it is a limit of points inside both solids.
4. **Difference.** $A \setminus B = A \cap (E^3 \setminus B)$, and $\operatorname{int}(E^3 \setminus B) = E^3 \setminus \operatorname{cl} B = E^3 \setminus B$ because $B$ is closed. So $A -^* B = \operatorname{cl}(\operatorname{int} A \setminus B)$. The same steps give $c^* A = \operatorname{cl}(E^3 \setminus A)$ and $A -^* B = A \cap^* c^* B$.
5. **Boolean algebra.** The closed regular subsets of $E^3$, with $\cup^*$, $\cap^*$ and $c^*$, the empty set and $E^3$, form a Boolean algebra (Requicha and Tilove 1978). So the regularized operations are associative, commutative and distributive over each other, and a CSG tree can be rearranged by the usual laws of Boolean algebra.
6. **Closure on r-sets.** If $A$ and $B$ are r-sets, then $A \cup^* B$, $A \cap^* B$ and $A -^* B$ are r-sets (Tilove and Requicha 1980). Fact 1 gives regularity, and the results are bounded because they lie in $A \cup B$. The part that needs a theorem is that the interior and the closure of a semianalytic set are semianalytic. The complement $c^* A$ is not bounded, so it is not an r-set, and a modeler gives the user only the difference.
7. **One regularization at the end is enough.** Let $\Phi(A_1, \ldots, A_k)$ be an expression of unions, intersections and differences, let $\Phi^*$ be the same expression with the regularized operations, and let the $A_i$ be closed regular sets. Then $r(\Phi) = \Phi^*$. *Proof.* Let $N = \partial A_1 \cup \cdots \cup \partial A_k$. The boundary of a closed regular set has no interior point (an open set in $\partial A$ lies in $\operatorname{cl}(\operatorname{int} A)$, so it meets $\operatorname{int} A$, which is disjoint from $\partial A$), so $N$ is a closed set with empty interior. A point $p \notin N$ has a ball $U$ that lies inside or outside each $A_i$. On $U$ the set $\Phi$ is all of $U$ or empty, and, by induction on the expression, so is $\Phi^*$, with the same answer, because $r(X) \cap U = \operatorname{cl}(\operatorname{int} X \cap U) \cap U$ depends only on $X \cap U$. So $\Phi$ and $\Phi^*$ agree outside $N$. For any set $X$, $\operatorname{int} X \setminus N$ is dense in $\operatorname{int} X$ and equals $\operatorname{int}(X \setminus N)$, so $r(X) = \operatorname{cl}(\operatorname{int}(X \setminus N))$ depends only on $X \setminus N$. So $r(\Phi) = r(\Phi^*) = \Phi^*$, the last step by fact 1. $\square$ So regularization changes nothing at points off the boundaries of the inputs. It decides only which boundary points stay. A point-membership test can evaluate the ordinary expression at points near $p$ in general position (see the [CSG](/constructive-solid-geometry/) page), but a boundary algorithm, which computes exactly these boundary points, must regularize.

## Examples and non-examples

All examples use axis-aligned boxes, so each result can be checked by hand.

| $A$ | $B$ | ordinary result | regularized result |
|---|---|---|---|
| $[0, 1]$ | $[1, 2]$ | $A \cap B = \{1\}$ | $A \cap^* B = \emptyset$ |
| $[0, 1]$ | $[1, 2]$ | $A \setminus B = [0, 1)$ | $A -^* B = [0, 1]$ |
| $[0, 1]^3$ | $[1, 2] \times [0, 1]^2$ | $A \cap B = \{1\} \times [0, 1]^2$, a face | $A \cap^* B = \emptyset$ |
| $[0, 1]^3$ | $[1, 2] \times [0, 1]^2$ | $A \cup B = [0, 2] \times [0, 1]^2$ | the same set |
| $[0, 2]^3$ | $[1, 3] \times [0, 2]^2$ | $A \setminus B = [0, 1) \times [0, 2]^2$, not closed | $A -^* B = [0, 1] \times [0, 2]^2$ |

- **Touching cubes.** The two unit cubes $[0, 1]^3$ and $[1, 2] \times [0, 1]^2$ share the face $x = 1$. The ordinary intersection is that square: it has no volume, but it is not empty, so a program that tests "do the solids intersect?" with the ordinary operation says yes. The interior of the square in $E^3$ is empty, so the regularized intersection is empty. This is the case that the definition was made for.
- **Difference.** For $A = [0, 2]^3$ and $B = [1, 3] \times [0, 2]^2$, the ordinary difference is $[0, 1) \times [0, 2]^2$. It is not closed: the face $x = 1$ is missing, so it has no boundary there. By fact 4, $A -^* B = \operatorname{cl}((0, 2)^3 \setminus B) = \operatorname{cl}((0, 1) \times (0, 2)^2) = [0, 1] \times [0, 2]^2$, which is a closed box with the face $x = 1$ back in place.
- **Part solid, part dangling.** In the plane, take the rectangle $A = [0, 2] \times [0, 1]$ and the set $B = [1, 3] \times [0, 1] \cup [0, 1] \times [1, 2]$, which is a rectangle to the right of $x = 1$ and a square that sits on top of $A$. Then $A \cap B = [1, 2] \times [0, 1] \cup [0, 1] \times \{1\}$: a square with a segment that hangs from its corner $(1, 1)$. The regularized intersection is the square $[1, 2] \times [0, 1]$ alone. So regularization does not only turn empty-looking results into the empty set; it also cuts the lower-dimensional parts off a result that has volume.
- **The result can be a non-manifold r-set.** $[0, 1]^3 \cup^* [1, 2] \times [1, 2] \times [0, 1]$ is the two cubes that share one edge. It is regular, so regularization does not change it, but its boundary is not a 2-manifold at the shared edge. The [manifold solids](/manifold-solid/) are not closed under the regularized operations, even though the r-sets are.
- **Regularizing once at the end.** Take $A = [0, 1]$, $B = [1, 2]$ and $D = [1, 3]$ in $E^1$, and the expression $(D \setminus A) \cup (A \cap B)$. The ordinary steps give $(1, 3] \cup \{1\} = [1, 3]$, and $r([1, 3]) = [1, 3]$. The regularized steps give $(D -^* A) \cup^* (A \cap^* B) = [1, 3] \cup^* \emptyset = [1, 3]$. The intermediate sets differ, a half-open interval against a closed one and a point against the empty set, but only at the point $1$, which is on the boundary of the inputs, so fact 7 makes the final results equal.
- **Non-example: the ordinary result is not a solid even when it has volume.** In the third row of the table the ordinary intersection is a face, and in the "part solid, part dangling" case it is a square with a segment. A B-rep algorithm that computes the ordinary intersection of two boundaries keeps that face or that segment, and it then stores a set that is not an r-set. Fact 7 does not help here, because the boundary is the output.

## Related definitions

- An [r-set](/r-set/) is a bounded, closed, regular, semianalytic set. Fact 6 says that the r-sets are closed under the regularized operations.
- [Constructive solid geometry](/constructive-solid-geometry/) describes a solid as a tree of primitives and regularized operations.
- [Set membership classification](/set-membership-classification/) (Tilove 1980) computes the part of a point, a segment or a face that is in, on or out of a regularized result. The "on" part needs neighborhood information, which [vertex neighborhood classification](/vertex-neighborhood-classification/) gives.
- [Solid Boolean operations](/solid-boolean-operations/) is the problem of computing a regularized operation on two [boundary representations](/boundary-representation/), and [boundary evaluation](/boundary-evaluation/) computes the boundary of a whole CSG tree.
- On [spatial occupancy enumeration](/spatial-occupancy-enumeration/), the set operations on cells are the regularized operations, with no extra step.
- In the plane, [polygon clipping](/polygon-clipping/) computes the 2D form of the same operations, and clippers must decide the same question about shared edges.

## References
