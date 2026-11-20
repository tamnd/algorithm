---
tag: 0M1H5N
kind: theorem
slug: brouwer-fixed-point-theorem
name: Brouwer fixed-point theorem
aliases:
- "Brouwer's theorem"
area: algorithmic-game-theory/strategic-games
level: core
summary: Every continuous map from a compact convex set in R^n to itself has a fixed point. Nash's proof of equilibrium existence rests on it.
prereqs: [convex-set]
see_also: [kakutani-fixed-point-theorem, nash-existence-theorem, sperner-lemma, hex-game, ppad, end-of-the-line-problem, scarf-algorithm, arrow-debreu-existence-theorem]
sources:
  - paper: doi:10.1007/BF01456931
    title: "L. E. J. Brouwer, Ueber Abbildung von Mannigfaltigkeiten, Mathematische Annalen 71 (1911-1912), 97-115"
    locator: the fixed point theorem for continuous maps of the n-dimensional ball, proved with the degree of a map
  - paper: "Emanuel Sperner, Neuer Beweis fuer die Invarianz der Dimensionszahl und des Gebietes, Abhandlungen aus dem Mathematischen Seminar der Universitaet Hamburg 6 (1928), 265-272"
    title: Neuer Beweis fuer die Invarianz der Dimensionszahl und des Gebietes
    locator: the combinatorial lemma on labelled triangulations used in the proof here
  - paper: doi:10.2307/1969529
    title: "John Nash, Non-cooperative games, Annals of Mathematics 54(2) (1951), 286-295"
    locator: the existence proof of equilibrium points by the Brouwer theorem applied to an explicit improvement map
  - paper: "David Gale, The game of Hex and the Brouwer fixed-point theorem, American Mathematical Monthly 86(10) (1979), 818-827"
    title: The game of Hex and the Brouwer fixed-point theorem
    locator: the equivalence of the no-draw property of Hex and the two-dimensional Brouwer theorem
  - paper: doi:10.1016/0885-064X(89)90017-4
    title: "Michael D. Hirsch, Christos H. Papadimitriou and Stephen A. Vavasis, Exponential lower bounds for finding Brouwer fixed points, Journal of Complexity 5(4) (1989), 379-416"
    locator: the lower bound on the number of function evaluations needed to find an approximate fixed point
  - paper: doi:10.1145/1379759.1379761
    title: "Xi Chen and Xiaotie Deng, Matching algorithmic bounds for finding a Brouwer fixed point, Journal of the ACM 55(3) (2008)"
    locator: the tight query bound for discrete fixed points on a d-dimensional grid
  - paper: "Christos H. Papadimitriou, On the complexity of the parity argument and other inefficient proofs of existence, Journal of Computer and System Sciences 48(3) (1994), 498-532"
    title: On the complexity of the parity argument and other inefficient proofs of existence
    locator: the class PPAD and the PPAD-completeness of finding an approximate Brouwer fixed point
---

The Brouwer fixed-point theorem says that every continuous map from a nonempty compact [convex set](/convex-set/) in $\mathbb{R}^n$ into itself leaves some point where it is. It is the basic existence tool of game theory: John Nash proved in 1951 that every finite game has a mixed equilibrium by applying it to an improvement map on the set of mixed profiles ([Nash's theorem](/nash-existence-theorem/)), after a 1950 proof with the [Kakutani fixed-point theorem](/kakutani-fixed-point-theorem/). The theorem says nothing about how to find the point, and finding an approximate one is complete for the class [PPAD](/ppad/).

## Statement

**Theorem (Brouwer 1911).** Let $K \subseteq \mathbb{R}^n$ be nonempty, compact and convex, and let $f: K \to K$ be continuous. Then there is $x \in K$ with $f(x) = x$.

The proof below uses the *standard simplex* $\Delta_n = \{x \in \mathbb{R}^{n+1} : x \ge 0,\ \sum_{j=0}^n x_j = 1\}$, with vertices $e_0, \ldots, e_n$. The *support* of $x \in \Delta_n$ is $\mathrm{supp}(x) = \{j : x_j > 0\}$.

## In plain words

Stir a cup of coffee and let it settle. However you stirred, if no coffee left the cup and no drop jumped, some point of the coffee ends where it began. In the same way, if you crumple a sheet of paper and lay it on top of a second copy of the sheet, without tearing it and without letting it overhang, some point of the crumpled sheet lies exactly above its own copy. The theorem needs three things: the shape has no holes, it has no missing edge points and no infinite extent, and the motion has no jumps. Remove any one and the claim fails. The proof does not show where the fixed point is, and finding one, even roughly, can take very long.

## Proof

**Step 1: Sperner's lemma.** A *triangulation* of $\Delta_n$ divides it into finitely many $n$-simplices, the *cells*, any two of which meet in a common face or not at all. A *Sperner labelling* gives every vertex $v$ of the triangulation a label $\lambda(v) \in \mathrm{supp}(v)$. A cell is *fully labelled* if its $n + 1$ vertices have all the labels $0, \ldots, n$.

*Lemma ([Sperner](/sperner-lemma/)).* Every Sperner labelling of a triangulation of $\Delta_n$ has an odd number of fully labelled cells.

*Proof.* Induction on $n$. For $n = 0$ the simplex is one point with label 0. For $n \ge 1$, call a facet of a cell a *door* if its $n$ vertices have exactly the labels $0, \ldots, n - 1$. Count the pairs (cell, door of that cell). A fully labelled cell has exactly one door. A cell whose labels are exactly $0, \ldots, n - 1$, with one label used twice, has exactly two doors. Every other cell has none. So the count is congruent mod 2 to the number of fully labelled cells. Now count by doors. A door inside $\Delta_n$ is a facet of exactly two cells and adds 2. A door on the boundary lies in a facet $\{x_j = 0\}$ of $\Delta_n$; its vertices have $j \notin$ support, so label $j$ is missing, and since all of $0, \ldots, n - 1$ appear, $j = n$. So the boundary doors are the fully labelled cells of the induced triangulation of the facet $\{x_n = 0\}$, which is a copy of $\Delta_{n-1}$ with a Sperner labelling. By induction there is an odd number of them. So the count is odd, and so is the number of fully labelled cells. $\square$

**Step 2: the theorem for $\Delta_n$.** Let $f: \Delta_n \to \Delta_n$ be continuous. For $x \in \Delta_n$ there is $j \in \mathrm{supp}(x)$ with $f(x)_j \le x_j$: otherwise $\sum_{j \in \mathrm{supp}(x)} f(x)_j > \sum_{j \in \mathrm{supp}(x)} x_j = 1$, which is impossible for a point of $\Delta_n$. Label each vertex $v$ of a triangulation by such a $j$. This is a Sperner labelling.

Take triangulations $T_1, T_2, \ldots$ of $\Delta_n$ whose largest cell diameter tends to 0, for example iterated barycentric subdivisions. By Step 1, $T_k$ has a fully labelled cell with vertices $v^{k,0}, \ldots, v^{k,n}$, where $v^{k,j}$ has label $j$, so $f(v^{k,j})_j \le v^{k,j}_j$. Since $\Delta_n$ is compact, a subsequence of $v^{k,0}$ converges to some $x^*$, and since the cell diameters tend to 0, every $v^{k,j}$ converges to $x^*$ along it. By continuity of $f$, $f(x^*)_j \le x^*_j$ for every $j$. Both sides sum to 1 over $j$, so every inequality is an equality, and $f(x^*) = x^*$.

**Step 3: any compact convex set.** Let $K \subseteq \mathbb{R}^n$ be nonempty, compact and convex. Choose an $n$-simplex $D \supseteq K$; an affine bijection maps $D$ onto $\Delta_n$ (as a subset of its affine hull), so Step 2 holds for $D$. Let $r: D \to K$ send $y$ to the nearest point of $K$. It is well defined because $K$ is closed and convex, and $r(y) = y$ for $y \in K$. It is continuous: the nearest point satisfies $\langle y - r(y), z - r(y)\rangle \le 0$ for every $z \in K$; adding this inequality for $y$ with $z = r(y')$ and for $y'$ with $z = r(y)$ gives $|r(y) - r(y')|^2 \le \langle y - y', r(y) - r(y')\rangle$, so $|r(y) - r(y')| \le |y - y'|$. The map $g = f \circ r: D \to K \subseteq D$ is continuous, so it has a fixed point $x = g(x)$ by Step 2. Then $x \in K$, so $r(x) = x$ and $f(x) = x$. $\square$

## Consequences

- **Nash equilibria exist.** For a finite game with mixed profile $\sigma$, let $g_{i}(a) = \max\big(0,\ u_i(a, \sigma_{-i}) - u_i(\sigma)\big)$ be the gain of player $i$ from the pure strategy $a$, and let $f(\sigma)_i(a) = \big(\sigma_i(a) + g_i(a)\big)/\big(1 + \sum_{b} g_i(b)\big)$. This map is continuous from the product of simplices, a compact convex set, to itself, and its fixed points are exactly the Nash equilibria. Nash (1951) used this map and Brouwer's theorem; his 1950 note used Kakutani's theorem on the best-response correspondence ([Nash's theorem](/nash-existence-theorem/)).
- **Kakutani's theorem.** The set-valued version, proved from Brouwer's theorem ([Kakutani fixed-point theorem](/kakutani-fixed-point-theorem/)), gives Nash's theorem and the existence of [competitive equilibria](/arrow-debreu-existence-theorem/).
- **No retraction.** There is no continuous map from the closed ball onto its boundary sphere that fixes every point of the sphere. If $r$ were one, $x \mapsto -r(x)$ would map the ball into itself with no fixed point. Conversely, the theorem follows from the no-retraction statement, so the two are equivalent.
- **Hex.** Gale (1979) proved that a full board of [Hex](/hex-game/) always has a winner and showed that this statement is equivalent to the two-dimensional Brouwer theorem; the game gives a discrete proof.
- **Computation.** The proof of Step 1 is a parity argument; following doors from the boundary gives an algorithm that finds a fully labelled cell, which is the idea of [Scarf's algorithm](/scarf-algorithm/) and of the [end-of-the-line problem](/end-of-the-line-problem/). Finding an approximate fixed point of a function given by a circuit is PPAD-complete (Papadimitriou 1994). When the function is given only by queries, Hirsch, Papadimitriou and Vavasis (1989) proved a lower bound on the number of queries that is exponential in the dimension, and Chen and Deng (2008) showed that the discrete problem on a $d$-dimensional grid of side $N$, for $d \ge 2$, needs $\Theta(N^{d-1})$ queries.

## Tightness

Each hypothesis is needed.

- *Boundedness.* $f(x) = x + 1$ on $\mathbb{R}$, a closed convex set, has no fixed point.
- *Closedness.* $f(x) = x/2$ maps the open interval $(0, 1)$ into itself and has no fixed point.
- *Convexity, or at least no holes.* A rotation of a circle, or of an annulus, by a third of a turn has no fixed point. Convexity can be weakened to "homeomorphic to a compact convex set", but not dropped.
- *Continuity.* On $[0, 1]$, let $f(x) = 1$ for $x < 1/2$ and $f(x) = 0$ for $x \ge 1/2$. It has no fixed point.
- *Finite dimension.* In the Hilbert space $\ell^2$, the closed unit ball is bounded, closed and convex, but there is a continuous map from it to itself with no fixed point (Kakutani 1943). Schauder's theorem restores the result for compact convex subsets of normed spaces.

The theorem gives no uniqueness: the identity fixes every point. Fixed points can be irrational even for simple maps: $f(x) = 1 - x^2/2$ maps $[0, 1]$ into $[1/2, 1]$, and its only fixed point is $\sqrt{3} - 1$. This is one reason algorithms look for approximate fixed points, with $|f(x) - x| \le \varepsilon$.

## History

Piers Bohl proved a form of the theorem in 1904 and Jacques Hadamard gave a proof for all dimensions in 1910; L. E. J. Brouwer published his proof in Mathematische Annalen in 1911-1912, using the degree of a map, and the theorem bears his name. Emanuel Sperner's lemma of 1928 led to the combinatorial proof above, given by Knaster, Kuratowski and Mazurkiewicz in 1929. Shizuo Kakutani extended the theorem to set-valued maps in 1941, and John Nash applied both versions to games in 1950 and 1951. Herbert Scarf turned the combinatorial proof into an algorithm in 1967, and Christos Papadimitriou defined the class PPAD in 1994 to capture the complexity of such parity arguments.

## References
