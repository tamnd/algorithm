---
tag: MFEP4T
kind: theorem
slug: sperner-lemma
name: Sperner's lemma
aliases:
- Sperner lemma
area: algorithmic-game-theory/computing-equilibria
level: core
summary: Every Sperner coloring of a triangulated simplex has an odd number of fully colored cells. Its path-following proof finds one.
prereqs: [triangulation, handshaking-lemma]
see_also: [brouwer-fixed-point-theorem, scarf-algorithm, end-of-the-line-problem, ppad, rental-harmony, su-rental-harmony-algorithm, nash-existence-theorem, ppad-completeness-of-nash]
sources:
  - paper: doi:10.1007/BF02940617
    title: "Emanuel Sperner, Neuer Beweis für die Invarianz der Dimensionszahl und des Gebietes, Abhandlungen aus dem Mathematischen Seminar der Universität Hamburg 6 (1928), 265-272"
    locator: the combinatorial lemma on colored subdivisions of a simplex, used to prove the invariance of dimension and of domain
  - paper: doi:10.1016/S0022-0000(05)80063-7
    title: "Christos H. Papadimitriou, On the complexity of the parity argument and other inefficient proofs of existence, Journal of Computer and System Sciences 48(3) (1994), 498-532"
    locator: the Sperner problem is in PPAD, and its 3-dimensional version is PPAD-complete
  - paper: doi:10.1016/j.tcs.2009.07.052
    title: "Xi Chen and Xiaotie Deng, On the complexity of 2D discrete fixed point problem, Theoretical Computer Science 410(44) (2009), 4448-4456"
    locator: the 2-dimensional Sperner problem is PPAD-complete; conference version in ICALP 2006
  - paper: doi:10.1137/0115116
    title: "Herbert Scarf, The approximation of fixed points of a continuous mapping, SIAM Journal on Applied Mathematics 15(5) (1967), 1328-1343"
    locator: the path-following method that turns the counting proof into an algorithm for approximate fixed points
---

Sperner's lemma is a counting fact about colored triangulations. Divide a simplex into small simplices, and give each vertex of the division a color that names a corner of the face on which the vertex lies. Then the number of small simplices that show all the colors is odd, so there is at least one. Sperner proved it in 1928 to give a short proof of the invariance of dimension. It is the combinatorial core of the [Brouwer fixed-point theorem](/brouwer-fixed-point-theorem/), and its proof by doors is a walk along a path. This walk is the model for [Scarf's algorithm](/scarf-algorithm/), for the [Lemke-Howson algorithm](/lemke-howson-algorithm/) and for the class [PPAD](/ppad/).

## Statement

Let $\Delta$ be a $d$-dimensional simplex with corners $v_0, \dots, v_d$. A point $x$ of $\Delta$ has barycentric coordinates $x_0, \dots, x_d \ge 0$ with sum 1, so $x = \sum_i x_i v_i$. Let $T$ be a triangulation of $\Delta$: a finite set of $d$-dimensional simplices, the **cells**, whose union is $\Delta$, such that any two cells meet in a common face or not at all. A **Sperner coloring** is a map $\lambda$ from the vertices of $T$ to $\{0, \dots, d\}$ such that $x_{\lambda(x)} > 0$ for every vertex $x$. In words, each vertex gets the color of a corner of the smallest face of $\Delta$ that contains it. So corner $v_i$ gets color $i$, and a vertex on the face opposite $v_i$ never gets color $i$. A cell is **fully colored** if its $d + 1$ vertices have all $d + 1$ colors.

**Theorem (Sperner 1928).** For every triangulation $T$ of a $d$-simplex and every Sperner coloring of $T$, the number of fully colored cells is odd. In particular, there is at least one.

For $d = 1$, the simplex is a segment from $v_0$ (color 0) to $v_1$ (color 1), divided into short segments. As we go from $v_0$ to $v_1$, the color changes an odd number of times, so an odd number of short segments have both colors.

## In plain words

Draw a big triangle and cut it into small triangles. Color each corner of the big triangle with its own color: red, green and blue. A point on a side of the big triangle may only take a color of the two ends of that side. A point inside may take any color. Then some small triangle has all three colors, and in fact an odd number of them do. The proof is a walk: enter the big triangle through a side whose ends are red and green, and keep going through red-green sides. You can never get stuck in a loop, and the only way to stop is inside a small triangle with all three colors.

## Proof

We use two facts about a triangulation of a $d$-simplex. Every $(d-1)$-face of a cell lies in exactly two cells if it is not on the boundary of $\Delta$, and in exactly one cell if it is on the boundary. The cells of $T$ that lie on a facet of $\Delta$ form a triangulation of that facet.

The proof is by induction on $d$. For $d = 0$, $\Delta$ is one point with color 0, and there is one cell, which is fully colored.

Let $d \ge 1$. Call a $(d-1)$-face of a cell a **door** if its $d$ vertices have exactly the colors $0, \dots, d - 1$. Count the pairs $(c, D)$ where $c$ is a cell and $D$ is a door of $c$.

*Count by cells.* A fully colored cell has exactly one door, the face without the vertex of color $d$. A cell whose colors are exactly $\{0, \dots, d - 1\}$ has one of these colors twice, and it has exactly two doors: remove either vertex with the repeated color. Any other cell misses one of the colors $0, \dots, d - 1$, so it has no door. So the number of pairs is the number $F$ of fully colored cells plus an even number.

*Count by doors.* A door inside $\Delta$ lies in two cells, and a door on the boundary lies in one. A door on the boundary lies in a facet of $\Delta$, and in the facet opposite $v_i$ no vertex has color $i$. A door has the colors $0, \dots, d - 1$, so it can lie only on the facet opposite $v_d$. That facet is a $(d-1)$-simplex with corners $v_0, \dots, v_{d-1}$, the cells of $T$ on it triangulate it, and the coloring restricted to it is a Sperner coloring with colors $0, \dots, d - 1$. The boundary doors are exactly its fully colored cells. By induction their number $B$ is odd. So the number of pairs is $B$ plus an even number.

The two counts are equal, so $F \equiv B \equiv 1 \pmod 2$. $\square$

**The path version.** The same doors give a walk. Make a graph whose nodes are the cells and one extra node, *outside*, which is joined to the cell of each boundary door. Join two cells if they share a door. Each cell has degree equal to its number of doors, so degree 0, 1 or 2, and degree 1 means fully colored. The outside node has odd degree $B$. Every graph has an even number of nodes of odd degree (the [handshaking lemma](/handshaking-lemma/)), which gives the parity again. To find one fully colored cell, start at a boundary door and walk through doors. The walk cannot return to a cell it left, because every cell has at most two doors. So it ends in a fully colored cell or leaves through another boundary door. In dimension $d$ the starting door is itself found by a walk in dimension $d - 1$, or the walk is arranged so that it starts at the corner, as in [Scarf's algorithm](/scarf-algorithm/). Papadimitriou (1994) used this walk to put the problem in PPAD.

## Consequences

- **Brouwer's fixed-point theorem.** Let $f$ be a continuous map of $\Delta$ to itself. Color a vertex $x$ by an $i$ with $x_i > 0$ and $f_i(x) \le x_i$; such an $i$ exists because $f(x)$ and $x$ both have coordinates with sum 1. This is a Sperner coloring, so each triangulation has a fully colored cell. As the cells get finer, these cells have a limit point $x^*$ with $f_i(x^*) \le x^*_i$ for all $i$, so $f(x^*) = x^*$. This gives the [Brouwer fixed-point theorem](/brouwer-fixed-point-theorem/), and through it [Nash's theorem](/nash-existence-theorem/).
- **Approximate fixed points.** On a fixed triangulation with cells of diameter $\delta$, a fully colored cell gives a point that $f$ moves by an amount bounded by $\delta$ and the modulus of continuity of $f$. [Scarf's algorithm](/scarf-algorithm/) computes such a cell.
- **Complexity.** The problem "given a Sperner coloring by a circuit, find a fully colored cell" is in PPAD by the path version. It is PPAD-complete in dimension 3 (Papadimitriou 1994) and already in dimension 2 (Chen and Deng 2006, 2009). In dimension 1 it is easy: binary search finds a segment with both colors in $O(\log N)$ queries for $N$ segments. The reductions of the [END OF THE LINE](/end-of-the-line-problem/) problem to Nash equilibria go through discrete fixed-point problems of this kind ([PPAD-completeness of Nash](/ppad-completeness-of-nash/)).
- **Fair division.** Su (1999) used the lemma for [rental harmony](/rental-harmony/): for $n$ housemates and $n$ rooms, there is a division of the rent in which every person prefers a different room, under mild conditions on the preferences ([Su's algorithm](/su-rental-harmony-algorithm/)).
- **KKM and Hex.** The lemma implies the KKM lemma on closed covers of a simplex. A path argument of the same kind shows that the game of Hex cannot end in a draw.

## Tightness

The boundary condition is needed. If every vertex gets color 0, no cell is fully colored. It is also not enough that the corners keep their colors. Divide a triangle in four by the midpoints of its sides, give the corners $v_0, v_1, v_2$ the colors 0, 1, 2, and give all three midpoints color 0. The midpoint of the side $v_1 v_2$ breaks the condition, and no cell has all three colors.

The bound "at least one" is tight: the triangulation with one cell, the simplex itself, has exactly one fully colored cell. The parity cannot be improved to an exact count, because any odd number can occur. A finer statement holds with orientation: if each fully colored cell is counted as $+1$ or $-1$ by the orientation of its colors, the sum is exactly 1.

The lemma does not say how fast one can find a fully colored cell. If the coloring is given only by queries, any algorithm needs a number of queries that grows like a power of the number of grid points per edge in each fixed dimension, and exponentially in the dimension (Hirsch, Papadimitriou and Vavasis 1989; Chen and Deng 2008).

## History

Sperner proved the lemma in his 1928 doctoral thesis at Hamburg and used it to give elementary proofs of the invariance of dimension and of domain. Knaster, Kuratowski and Mazurkiewicz (1929) derived the KKM lemma and from it the Brouwer theorem. Scarf (1967) and Kuhn (1968) turned the door argument into algorithms for fixed points, and Papadimitriou (1994) used it to define PPAD. Chen and Deng proved PPAD-completeness in dimension 2 in 2006. Su (1999) brought the lemma to fair division.

## References
