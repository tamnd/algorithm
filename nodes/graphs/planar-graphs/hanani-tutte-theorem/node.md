---
tag: DXF1G0
kind: theorem
slug: hanani-tutte-theorem
name: Hanani-Tutte theorem
aliases:
- strong Hanani-Tutte theorem
area: graphs/planar-graphs
level: research
summary: A graph is planar if and only if it has a drawing in which every pair of independent edges crosses an even number of times.
prereqs: [kuratowski-theorem, planar-graph, crossing-number, jordan-curve-theorem]
see_also: [crossing-number, crossing-lemma, kuratowski-theorem, planarity-testing, graph-genus, rotation-system, graph-drawing, planar-embedding]
sources:
  - paper: "Chaim Chojnacki (Haim Hanani), Über wesentlich unplättbare Kurven im dreidimensionalen Raume, Fundamenta Mathematicae 23, 135 to 142 (1934)"
    locator: the first proof that K5 and K3,3 have no drawing in which independent edges cross evenly
  - paper: "W. T. Tutte, Toward a theory of crossing numbers, Journal of Combinatorial Theory 8(1), 45 to 53 (1970)"
    locator: the parity invariant of drawings and the strong form of the theorem
  - paper: "Michael J. Pelsmajer, Marcus Schaefer and Daniel Štefankovič, Removing even crossings, Journal of Combinatorial Theory, Series B 97(4), 489 to 500 (2007)"
    locator: a direct proof that even crossings can be removed, and the weak form that keeps the rotation system
  - paper: "Marcus Schaefer, Hanani-Tutte and related results, in Geometry, Intuitive, Discrete, and Convex, Bolyai Society Mathematical Studies 24, Springer, 2013, 259 to 299"
    locator: the survey of the strong and weak forms, the proofs through Kuratowski's theorem, and the extensions to other surfaces
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 4.4, Kuratowski's theorem, used in the proof
---

The Hanani-Tutte theorem says that a graph is planar as soon as it has a drawing in which every two independent edges, edges with no common end, cross an even number of times. Crossings between edges that share an end, and crossings of an edge with itself, are not counted at all. So planarity is a property that can be read off modulo 2, which is the reason why planarity has an algebraic test by linear equations over the field with two elements. The theorem was proved by Haim Hanani (as Chaim Chojnacki) in 1934 and again by W. T. Tutte in 1970. **How the embedding is given:** a drawing is given by coordinates, as curves in the plane in general position; the theorem turns such a drawing, with only even independent crossings, into a crossing-free embedding, which can be given by coordinates or by a [rotation system](/rotation-system/).

## Statement

A **drawing** of a graph $G$ puts each vertex at a distinct point of the plane and each edge $uv$ as a curve from $u$ to $v$, in general position: no curve passes through a vertex other than its ends, two curves meet in finitely many points, each of which is a proper crossing, and no three curves pass through one point. Edges may cross themselves, and edges with a common end may cross. Two edges are **independent** if they have no common end. For edges $e, f$ write $\mathrm{cr}(e, f)$ for the number of crossings between them.

**Theorem (Hanani 1934, Tutte 1970).** A graph $G$ is planar if and only if $G$ has a drawing in which $\mathrm{cr}(e, f)$ is even for every pair of independent edges $e, f$.

**Lemma (the parity of $K_5$ and $K_{3,3}$).** In every drawing of $K_5$, and in every drawing of $K_{3,3}$, the sum of $\mathrm{cr}(e, f)$ over all unordered pairs of independent edges is odd.

The theorem follows from the lemma and [Kuratowski's theorem](/kuratowski-theorem/).

## In plain words

Draw a network on paper, and allow crossings. Look only at pairs of lines that do not meet at a common point. If every such pair crosses an even number of times (zero, two, four and so on), then the theorem says that the network can be redrawn with no crossings at all. Crossings between lines that share an end point do not matter, however many there are.

So you never need a perfect drawing to prove that a network fits on paper: a drawing that is right "up to pairs of crossings" is enough. For the two small networks that do not fit on paper, every drawing has an odd number of such crossings, and that odd count can never be removed.

## Proof

The full proof is in [the proof file](proofs/main.md). It has three steps.

1. **Moves.** Any two drawings of a graph with the same vertex positions can be joined by a continuous deformation of the edges, one at a time. In general position this deformation passes through finitely many events. At a tangency between two edges, their crossing count changes by 2. At a triple point, no count changes. When an edge $e$ passes over a vertex $v$, the count $\mathrm{cr}(e, f)$ changes by 1 for each edge $f$ at $v$, and no other count changes. Moving the vertices first, by a deformation of the whole plane, changes no count.
2. **The parity is an invariant.** Let $\sigma$ be the sum of $\mathrm{cr}(e, f)$ over independent pairs. Tangencies change $\sigma$ by 2, and triple points not at all. When an edge $e = ab$ passes over a vertex $v$, only the pairs $\{e, f\}$ with $f$ at $v$ and $f$ independent of $e$ change. If $v \in \{a, b\}$ there is no such $f$. In $K_5$, for $v \notin \{a, b\}$, these $f$ are the two edges from $v$ to the two other vertices. In $K_{3,3}$, for $v \notin \{a, b\}$, $v$ is on the side of $a$ or of $b$, and the $f$ are the two edges from $v$ to the side of the other end, avoiding $a$ or $b$. Either way $\sigma$ changes by 2. So $\sigma \bmod 2$ is the same for all drawings.
3. **One drawing each.** Draw $K_5$ with straight lines on the corners of a convex pentagon: two edges cross exactly when they are crossing diagonals, which are independent, and every 4 of the 5 corners give one crossing, so $\sigma = 5$. Draw $K_{3,3}$ on the corners $0, \ldots, 5$ of a convex hexagon with the even corners on one side: the 6 sides and the 3 long diagonals are the 9 edges, and moving one vertex a little makes the 3 diagonals cross in 3 points, so $\sigma = 3$. Both are odd.

Now, if $G$ is planar, a crossing-free drawing has all counts 0. If $G$ is not planar, it contains a subdivision of $K_5$ or $K_{3,3}$ by Kuratowski's theorem. Given a drawing of $G$, keep only this subdivision, and read each subdivided path as one curve. Two paths that stand for independent edges of $K_5$ or $K_{3,3}$ have no common vertex, so each pair of their edges is independent in $G$. If all independent pairs of $G$ crossed evenly, these curves would cross evenly, and $\sigma$ would be even, against the lemma. $\blacksquare$

## Consequences

- **An algebraic planarity test.** Fix any drawing of $G$, for example with straight lines. Each move "pass edge $e$ over vertex $v$" adds 1 to the counts of the pairs $\{e, f\}$ with $f$ at $v$. By the theorem, $G$ is planar if and only if the vector of independent crossing counts, taken modulo 2, is a sum of such move vectors. This is a system of linear equations over the field with two elements, solvable in polynomial time. The linear-time [planarity tests](/planarity-testing/) are much faster, but the algebraic form is the one that extends to some other problems, for example drawing with prescribed levels.
- **Lower bounds on crossing numbers.** By the lemma, every drawing of $K_5$ or $K_{3,3}$ has an odd number of crossings between independent edges, so at least one; this gives $\mathrm{cr}(K_5) = \mathrm{cr}(K_{3,3}) = 1$ together with the drawings of step 3 with one crossing. More generally, a graph has [crossing number](/crossing-number/) 0 exactly when its independent odd crossing number is 0, the least number of independent pairs that cross an odd number of times.
- **The weak form.** If in some drawing every pair of edges, adjacent or not, crosses an even number of times, then $G$ has a crossing-free drawing with the same rotation system: the cyclic order of the edges at each vertex is kept (Pelsmajer, Schaefer and Štefankovič, 2007).
- **The meaning of the lemma.** The parity $\sigma \bmod 2$ is the van Kampen obstruction of $K_5$ and $K_{3,3}$ in the plane. The analogous statement one dimension up, about linking cycles in space, leads to the characterization of linklessly embeddable graphs.

## Tightness

| graph | planar | a drawing with even independent pairs | $\sigma \bmod 2$ in every drawing |
|---|---|---|---|
| a single vertex | yes | the point itself; there are no pairs | 0 (no pairs) |
| a tree | yes | any crossing-free drawing | 0 for a star, which has no independent pairs; not invariant for most other trees |
| $K_4$ | yes | a triangle with a vertex inside | not invariant |
| $K_5$ | no | none | 1 |
| $K_{3,3}$ | no | none | 1 |

For $K_4$ the parity is not an invariant: passing the edge $ab$ over $c$ toggles only the pair $\{ab, cd\}$, so a drawing with one crossing, of two opposite edges, also exists. In $K_5$ and $K_{3,3}$ every move toggles an even number of independent pairs, which is what makes them special.

- **Adjacent pairs must be ignored, and independent pairs cannot be.** Ignoring adjacent pairs is what makes the strong form strong. If even one odd independent pair is allowed, the statement fails: $K_5$ and $K_{3,3}$ have drawings with exactly one crossing.
- **Odd crossing number differs from crossing number.** The theorem says that the two agree at 0. Pelsmajer, Schaefer and Štefankovič found graphs whose odd crossing number, the least number of pairs of edges that cross an odd number of times, is smaller than the crossing number, so the agreement does not extend to every value.
- **Other surfaces.** The strong form also holds on the projective plane (Pelsmajer, Schaefer and Stasi). Fulek and Kynčl found a counterexample to the strong form on the orientable surface of genus 4. The weak form holds on every surface.

## History

Haim Hanani proved in 1934, under his birth name Chaim Chojnacki, that $K_5$ and $K_{3,3}$ cannot be drawn so that independent edges cross evenly, in a paper on curves in three-dimensional space. The result was forgotten. W. T. Tutte rediscovered it in 1970 in his paper toward a theory of crossing numbers, gave the parity invariant used here, and stated the strong form. Interest returned in the 2000s, when Michael Pelsmajer, Marcus Schaefer and Daniel Štefankovič gave a direct proof that removes even crossings without Kuratowski's theorem and started the study of extensions to other surfaces and to related drawing problems; Schaefer surveyed this work in 2013.

## References
