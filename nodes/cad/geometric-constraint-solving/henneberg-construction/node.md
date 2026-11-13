---
tag: KWQN1F
kind: technique
slug: henneberg-construction
name: Henneberg construction
aliases:
- Henneberg moves
area: cad/geometric-constraint-solving
level: advanced
summary: Builds every minimally rigid planar graph from one edge by adding a vertex of degree two, or a vertex of degree three that replaces an edge.
prereqs: [laman-theorem, generic-rigidity, induction]
see_also: [laman-theorem, pebble-game-rigidity, jackson-jordan-theorem, constructive-constraint-solving, ruler-and-compass-constructibility, distance-based-formation-control, global-rigidity, tay-theorem]
sources:
  - book: "L. Henneberg, Die graphische Statik der starren Systeme, B. G. Teubner, Leipzig, 1911"
    locator: the construction of plane trusses by joints of degree two and by the replacement of a bar with a joint of degree three
  - paper: doi:10.1007/BF01534980
    title: G. Laman, On graphs and rigidity of plane skeletal structures, Journal of Engineering Mathematics 4(4), 331 to 340, 1970
    locator: the proof that the two moves generate exactly the graphs with the Laman counts
  - book: isbn:9780821838013
    title: Jack Graver, Brigitte Servatius and Herman Servatius, Combinatorial Rigidity, Graduate Studies in Mathematics 2, American Mathematical Society, 1993
    locator: Chapter 4, Linear and Planar Rigidity (the Henneberg sequences), and Chapter 5, Rigidity in Higher Dimensions (the moves in space)
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, Chapman and Hall/CRC, 2018
    locator: the chapter Inductive constructions for combinatorial local and global rigidity (general locator)
  - paper: doi:10.1016/j.jctb.2004.11.002
    title: Bill Jackson and Tibor Jordán, Connected rigidity matroids and unique realizations of graphs, Journal of Combinatorial Theory, Series B 94(1), 1 to 29, 2005
    locator: the construction of all 3-connected redundantly rigid graphs from K4 by edge additions and 1-extensions
---

A Henneberg construction builds a graph from a single edge by two moves that add one vertex each: a *vertex addition* (or 0-extension) joins a new vertex to two old ones, and an *edge split* (or 1-extension) removes an edge $ab$ and joins a new vertex to $a$, $b$ and a third vertex. Both moves keep generic rigidity in the plane, and by [Laman's theorem](/laman-theorem/) every generically minimally rigid graph in the plane has such a construction. As a technique, it is the standard way to prove that a property holds for a whole class of rigid graphs: show it for the base graph, show that each move keeps it, and show that every graph of the class can be reduced by an inverse move. In CAD, robotics and structural design it also gives a way to build or realize a rigid structure one vertex at a time.

## In plain words

Start with one rod between two points. To grow the structure, either add a new point and tie it to two old points with two rods, or take out one rod and add a new point tied to the two ends of that rod and to one more point. Each step adds one point and two rods, so the count of rods stays twice the points minus three. If the points are in general position, each step keeps the structure stiff.

The useful part is the reverse. Every stiff structure in the plane with no spare rod can be taken apart again by these steps. So to prove a fact about all such structures, you only prove it for one rod and check that the two steps keep it true.

## When it applies

- **A class closed under inverse moves.** The method needs a class of graphs in which every graph with more than a base number of vertices has a vertex whose removal, by an inverse move, gives a smaller graph of the same class. For Laman graphs a vertex of degree 2 or 3 always exists, because the average degree is $(4n - 6)/n < 4$, and the proof of Laman's theorem shows that a degree 3 vertex always has a good inverse split.
- **A property that each move keeps.** The property must survive both moves: generic rigidity, independence of the rows of the rigidity matrix, an orientation with bounded out-degree, a drawing with some extra property, a stress with a given sign pattern.
- **Generic geometry.** The moves keep rigidity only when the new point is placed well: off the line through its two neighbors for a vertex addition, and away from a set of measure zero for an edge split. For a construction that must be exact at special positions, the moves are not enough.
- **Not for the counts in space.** In $\mathbb{R}^3$ the analogous moves keep generic rigidity but do not reach every generically minimally rigid graph by known inverse moves, so the method does not prove a characterization there.

## The template

The reduction below finds a Henneberg sequence of a graph, or reports that the graph is not a Laman graph. The forward part, lines L11 and L12, uses the sequence to place the points.

```pseudo id=main
HENNEBERG-SEQUENCE(G)
L1  if |E| ≠ 2|V| - 3 then return NOT-LAMAN
L2  S ← empty stack
L3  while |V| > 2 do
L4      v ← a vertex of least degree;  if deg v ∉ {2, 3} then return NOT-LAMAN
L5      if deg v = 2 with neighbors a, b then push (ADD, v; a, b) on S;  G ← G - v
L6      else let a, b, c be the neighbors of v
L7          find a pair xy among ab, bc, ca that is not an edge and with G - v + xy a Laman graph;  z ← the third neighbor
L8          if there is no such pair then return NOT-LAMAN
L9          push (SPLIT, v; x, y; z) on S;  G ← G - v + xy
L10 return the last edge and the moves of S, popped in order
REALIZE(sequence)
L11 place the two ends of the first edge at random points
L12 for each move, in order, place the new vertex v at a random point (ADD keeps v off the line of a and b; SPLIT removes the edge xy and adds vx, vy, vz)
```

**Why the reduction is right.** If $G$ is a Laman graph, the proof of [Laman's theorem](/laman-theorem/) shows that line L4 finds a vertex of degree 2 or 3, that $G - v$ is a Laman graph in line L5, and that line L7 finds a pair in the degree 3 case, by the union argument on tight sets. Each step keeps the Laman property, so the loop ends at a single edge. Conversely, if the loop ends, then $G$ is built from an edge by the moves, so $G$ is a Laman graph. So the procedure answers correctly in both cases. Line L4 also rejects graphs with a vertex of degree at most 1, which a Laman graph with $n \ge 3$ never has.

**Why the realization is rigid.** A vertex addition at a point off the line of its two neighbors adds two independent rows to the rigidity matrix. For an edge split, the proof of Laman's theorem puts $v$ on the line of $x$ and $y$ and shows that the rows stay independent there. That placement is special, but the generic rank is at least the rank at any placement, so a random placement also gives independent rows with high probability, by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/). The final framework is infinitesimally rigid with probability at least $1 - 2n/N$ when coordinates are drawn from $\{1, \ldots, N\}$.

**Cost.** Each Laman test in line L7 takes $O(n^2)$ time with the [pebble game](/pebble-game-rigidity/), at most three tests per step and $n - 2$ steps, so the reduction takes $O(n^3)$ time with this direct method.

**Example.** Take the triangular prism: triangles $012$ and $345$ and the edges $03$, $14$, $25$. All degrees are 3.

| step | graph before | $v$ | neighbors | move found | graph after |
| --- | --- | --- | --- | --- | --- |
| 1 | prism, 9 edges | 5 | 2, 3, 4 | $34$ is an edge; $23$ works: (SPLIT, 5; 2, 3; 4) | $01, 02, 12, 03, 14, 34, 23$ |
| 2 | 7 edges on $0..4$ | 4 | 1, 3 | (ADD, 4; 1, 3) | $01, 02, 12, 03, 23$ |
| 3 | 5 edges on $0..3$ | 3 | 0, 2 | (ADD, 3; 0, 2) | triangle $012$ |
| 4 | triangle | 2 | 0, 1 | (ADD, 2; 0, 1) | edge $01$ |

Read upward, the sequence is: edge $01$, add 2 to $0, 1$, add 3 to $0, 2$, add 4 to $1, 3$, split $23$ with vertex 5 and third neighbor 4. At random integer points the final rigidity matrix has rank $9 = 2 \cdot 6 - 3$.

## Classic examples

- **[Laman's theorem](/laman-theorem/).** The original use. Henneberg moves keep independence of the rows of the rigidity matrix, and every Laman graph reduces by an inverse move, so Laman graphs are exactly the generically minimally rigid graphs in the plane.
- **[Jackson-Jordán theorem](/jackson-jordan-theorem/).** Every 3-connected, redundantly rigid graph in the plane is built from $K_4$ by edge additions and edge splits, and Connelly showed that an edge split keeps generic global rigidity. Together this proves that these graphs are generically globally rigid.
- **[Constructive constraint solving](/constructive-constraint-solving/).** A sketch whose constraint graph has a sequence of vertex additions only can be solved one point at a time, each point as an intersection of two circles, which is a [ruler and compass](/ruler-and-compass-constructibility/) construction. An edge split has no such local solution: removing the edge $xy$ leaves the new point and the old graph coupled, so the solver must solve a larger system. This is why $K_{3,3}$ and the prism are hard cases for triangle-decomposition solvers.
- **[Formation control](/distance-based-formation-control/).** A rigid formation of robots can be grown by letting each new robot keep the distance to two robots already in place (a vertex addition), which gives a leader-follower structure that stays rigid. Edge splits let a new robot take over one link.
- **Body-and-bar frameworks.** The graphs of [Tay's theorem](/tay-theorem/), unions of $D$ edge-disjoint spanning trees, have inductive constructions of the same kind: a new body comes with $D$ new bars, or it pinches some old bars (each bar $xy$ becomes two bars $vx$ and $vy$) and gets new bars for the rest of its count.

## Variations

- **Moves in space.** In $\mathbb{R}^3$ the 0-extension adds a vertex of degree 3 and the 1-extension removes an edge and adds a vertex of degree 4. Both keep generic rigidity in $\mathbb{R}^3$. But they do not generate all generically minimally rigid graphs in space with the known inverse steps, and the extra X-replacement move is only conjectured to keep rigidity. This is one reason why no Laman theorem for space is known.
- **Vertex-to-$K_4$ and vertex splitting.** Other moves keep generic rigidity in the plane, for example replacing a vertex by a copy of $K_4$, or splitting a vertex into two joined by an edge. They give shorter constructions for special classes.
- **Count matroids.** For $(k, \ell)$-sparse graphs, where every $j$ vertices span at most $kj - \ell$ edges, there are similar moves that generate the tight graphs, and the [pebble game](/pebble-game-rigidity/) handles the same counts.
- **Global rigidity.** Edge additions and 1-extensions, starting from $K_4$, generate all 3-connected redundantly rigid graphs in the plane (Jackson and Jordán 2005). The 1-extension keeps generic global rigidity in every dimension (Connelly 2005).

## Pitfalls

- **Taking the wrong pair.** In the inverse edge split, not every non-edge among the three neighbors works. For a vertex $v$ with neighbors $a$, $b$, $c$, the graph $G - v + ab$ can break the count when $a$ and $b$ already lie in a tight set. Line L7 must test each pair, and the proof guarantees that one of them works.
- **Degenerate placement.** A vertex addition that puts the new point on the line through its two neighbors gives an infinitesimally flexible framework. In exact CAD geometry, such a position can come from the design intent, for example a midpoint, and then the generic argument does not apply.
- **Henneberg sequences of only vertex additions.** Graphs built by vertex additions alone are a proper subclass. A graph whose every vertex has degree 3, such as $K_{3,3}$ or the prism, needs at least one edge split, because the last vertex of a vertex addition has degree 2.
- **Counting in space.** In $\mathbb{R}^3$, a graph built by 0-extensions and 1-extensions is generically rigid, but a graph that meets the counts $3n - 6$ and $3k - 6$ need not have such a construction or be rigid at all, as the double banana shows.
- **Reduction cost.** A direct reduction with a Laman test for each candidate pair takes $O(n^3)$ time. For long sequences, reuse the pebble game state between steps.

## Exercises

1. Show that $K_{3,3}$ has a Henneberg sequence, and that every sequence of it uses at least one edge split.
2. Show that a vertex addition in $\mathbb{R}^3$, a new vertex of degree 3 whose point is not on the plane through its three neighbors, keeps the rows of the rigidity matrix independent.
3. Find a graph with $2n - 3$ edges and minimum degree 2 for which line L4 picks a vertex of degree 2 and the reduction still ends with NOT-LAMAN.

## References
