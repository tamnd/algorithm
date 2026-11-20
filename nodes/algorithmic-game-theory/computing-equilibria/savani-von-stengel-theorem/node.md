---
tag: TRMMHR
kind: theorem
slug: savani-von-stengel-theorem
name: Exponential paths of the Lemke-Howson algorithm
aliases:
- Savani-von Stengel theorem
area: algorithmic-game-theory/computing-equilibria
level: research
summary: There are bimatrix games on which every Lemke-Howson path, from every starting label, has length exponential in the number of actions.
prereqs: [lemke-howson-algorithm, best-response-polytope, bimatrix-game]
see_also: [support-enumeration, ppad-completeness-of-nash, end-of-the-line-problem, lemke-algorithm, linear-complementarity-problem, simplex-method, smoothed-analysis, nash-equilibrium-computation]
sources:
  - paper: doi:10.1111/j.1468-0262.2006.00667.x
    title: "Rahul Savani and Bernhard von Stengel, Hard-to-solve bimatrix games, Econometrica 74(2) (2006), 397-429"
    locator: "Section 3, Lemke-Howson on labeled dual cyclic polytopes: the square games with exponentially long paths for every missing label, and the extension to nonsquare games that are also hard for support enumeration; conference version in FOCS 2004"
  - paper: doi:10.1137/0112033
    title: "C. E. Lemke and J. T. Howson, Jr., Equilibrium points of bimatrix games, Journal of the Society for Industrial and Applied Mathematics 12(2) (1964), 413-423"
    locator: the path-following algorithm whose running time the theorem bounds
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 3 (Bernhard von Stengel), the best-response polytopes, the Lemke-Howson algorithm and its exponential running time
---

The [Lemke-Howson algorithm](/lemke-howson-algorithm/) finds a Nash equilibrium of a two-player game by following a path of pivots, much as the simplex method follows edges of a polytope. The path starts with a choice of one label, a pure strategy of either player, and different labels can give paths of very different lengths. Savani and von Stengel (2004, 2006) built square games in which every one of these paths is exponentially long in the number of strategies. So even the best choice of the starting label does not make the algorithm polynomial. The games come from pairs of dual cyclic polytopes, the same polytopes that give the upper bound theorem for the number of vertices. The result is a statement about one algorithm, and it is not a proof that Nash equilibria are hard to find. That evidence comes from [PPAD-completeness](/ppad-completeness-of-nash/).

## Statement

Let $(A, B)$ be a nondegenerate $d \times d$ [bimatrix game](/bimatrix-game/), with $d$ strategies for each player, and let $P$ and $Q$ be its [best-response polytopes](/best-response-polytope/). Each of the $2d$ pure strategies is a label. The Lemke-Howson path for a missing label $k$ starts at the artificial equilibrium $(0, 0)$, drops label $k$, and pivots alternately in $P$ and $Q$ until it reaches a Nash equilibrium. Its length is the number of pivots.

**Theorem (Savani and von Stengel 2006).** For infinitely many dimensions $d$ there is a nondegenerate $d \times d$ bimatrix game $\Gamma(d, d)$, built from two labeled dual cyclic polytopes in dimension $d$ with $2d$ facets, such that for every missing label $k \in \{1, \dots, 2d\}$ the Lemke-Howson path from the artificial equilibrium has length exponential in $d$. The shortest of these paths grows like $\varphi^{3d/4}$ and the longest like $\varphi^{3d/2}$, where $\varphi = (1 + \sqrt 5)/2$ is the golden ratio; the longest path lengths are given by every third Fibonacci number. The game has a single completely mixed equilibrium.

**Extension.** The construction extends to nonsquare games, of size $d \times 2d$, on which the Lemke-Howson paths are still exponentially long, and on which [support enumeration](/support-enumeration/) also takes exponential time on average over the order in which it tries the supports.

## In plain words

One classical method for two-player games starts from a fake solution and walks step by step to a real one. The walk can start in several ways, one for each move of either player. One might hope that at least one of these starts gives a short walk. This theorem builds games where every start gives a walk with a number of steps that doubles again and again as the game grows. The games are made from special shapes with many corners, where the walk has to visit corners in an order much like counting in a strange number system. So the method can be very slow, whichever way you start it.

## Proof

The full proof is in Section 3 of the paper. Here is the structure.

**Labeled polytopes.** A Lemke-Howson path is a path in the product $P \times Q$ of the two best-response polytopes, along vertex pairs that have all labels except $k$. Each pivot leaves a facet of one polytope and enters a new facet, and the label of the new facet decides which polytope pivots next. So the path is fixed by the combinatorial structure of $P$ and $Q$ and by their facet labels. The paper shows that the labeled polytopes below can be realized as the best-response polytopes of a game, with a vertex where $d$ facets with the labels of one player meet as the artificial equilibrium. So it is enough to give two labeled polytopes and to count pivots on them.

**Dual cyclic polytopes.** The dual cyclic polytope with $2d$ facets in dimension $d$ has a simple combinatorial description: its vertices are the bitstrings of length $2d$ with exactly $d$ ones that satisfy Gale's evenness condition, that is, every maximal run of ones that does not touch either end of the string has even length. A bit 1 in position $j$ means that the vertex lies on facet $j$. A pivot drops one bit 1 and adds a new bit 1, in the only place that keeps the evenness condition. So a Lemke-Howson path is a sequence of bitstring operations on two strings at the same time.

**The labels and the path length.** Savani and von Stengel label the facets of the two polytopes with two different orders of the labels, chosen with care, because a careless labeling can create short paths or extra equilibria. For their labeling the path for each missing label decomposes into paths of the same kind in smaller dimensions, as in a recursive construction. The lengths then satisfy linear recurrences whose solutions are Fibonacci numbers. Solving the recurrences gives the bounds of the theorem for the shortest and the longest path.

**A shorter route.** McLennan and Tourky (2010) gave a simpler proof of the exponential bound with *imitation games*, in which one player has the identity matrix as payoff matrix. The Lemke-Howson paths of an imitation game correspond to Lemke paths on a single polytope, and Morris (1994) had already shown that Lemke paths on labeled dual cyclic polytopes are exponentially long. On those polytopes, the length $a_m$ of the longest path in dimension $m$ satisfies $a_m = 2 a_{m-2} + a_{m-4}$, so it grows by a factor of about $1 + \sqrt 2$ when $m$ grows by 2.

## Consequences

- **No good starting label.** Running Lemke-Howson from all $2d$ labels at the same time, and stopping when the first path ends, still takes exponential time on these games.
- **Exponential worst case for related methods.** The paths are also paths of [Lemke's algorithm](/lemke-algorithm/) for the [linear complementarity problem](/linear-complementarity-problem/) of the game, so the result gives hard instances for complementary pivoting.
- **Support enumeration.** The nonsquare games are hard for both standard simple methods at the same time.
- **Easy for other methods.** The square games have one completely mixed equilibrium, which one finds by solving the linear equations that make all pure strategies of each player equally good. So the games are hard for Lemke-Howson, not hard in general. The general hardness of the problem is the subject of [PPAD-completeness of Nash](/ppad-completeness-of-nash/).

## Tightness

The theorem shows exponential paths for a specific family of games, and it says nothing about typical games. Lemke-Howson is fast on many games in practice, and it is not known whether small random perturbations of the payoffs remove the long paths. Chen, Deng and Teng showed that no algorithm has polynomial [smoothed complexity](/smoothed-analysis/) for bimatrix games unless PPAD is contained in RP. Each path is longer than polynomial, but its length is at most the number of vertex pairs, which is at most exponential in $d$, so the order of growth is right up to the base of the exponent. Goldberg, Papadimitriou and Savani (2013) showed a stronger kind of hardness: computing the specific equilibrium that Lemke-Howson finds from a given label is PSPACE-complete.

## History

Lemke and Howson published the algorithm in 1964. Murty (1978) gave linear complementarity problems with exponentially long paths for Lemke's algorithm, and Morris (1994) used dual cyclic polytopes to show exponentially long Lemke paths for symmetric games. These did not settle the question for Lemke-Howson in bimatrix games, because the hard symmetric games can have easy nonsymmetric equilibria. Savani and von Stengel presented the bimatrix construction at FOCS 2004, and the journal version appeared in Econometrica in 2006. McLennan and Tourky (2010) gave the shorter proof with imitation games, and Savani and von Stengel later extended it to unit vector games.

## References
