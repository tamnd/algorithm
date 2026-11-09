---
tag: SGDVTP
kind: problem
slug: competitive-facility-location
name: Competitive facility location problem
aliases:
- Competitive Facility Location Problem
- competitive facility location game
area: optimization/combinatorial-optimization
level: advanced
summary: A two-player game where players alternately claim sites with values and proximity limits, asking whether the second player can guarantee a given total; it is PSPACE-complete.
prereqs: [pspace, game-tree, minimax, 3-sat]
see_also: [facility-location-problem, pspace, generalized-geography, hex-game, game-tree, minimax, independent-set, sat]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Chapter 9, PSPACE, A Class of Problems beyond NP (Section 9.2 states the problem and Competitive 3-SAT; Section 9.5 proves Competitive Facility Location PSPACE-complete)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Chapter 19, Polynomial space (QSAT and games)
  - paper: doi:10.1016/0022-0000(78)90045-4
    title: Thomas J. Schaefer, On the complexity of some two-person perfect-information games, Journal of Computer and System Sciences 16(2), 185 to 225, 1978
    locator: the games on formulas and graphs, including Node Kayles, shown PSPACE-complete
  - paper: doi:10.2307/2224214
    title: Harold Hotelling, Stability in competition, The Economic Journal 39(153), 41 to 57, 1929
    locator: the model of two sellers choosing locations on a line
---

Competitive facility location is a two-player game on a graph whose nodes are sites with values. The players take turns to claim a site, and no site may be claimed if a neighbor of it is already claimed. The question is whether the second player can make sure that the total value of its sites is at least a bound $B$, whatever the first player does. Kleinberg and Tardos use it as a natural example of a [PSPACE](/pspace/)-complete problem: it is in PSPACE because the game lasts at most $n$ moves, and it is PSPACE-hard by a reduction from Competitive 3-SAT, the game form of [SAT](/sat/). So it is not expected to be in NP, and no polynomial-length certificate of a winning strategy is expected to exist.

## In plain words

Two coffee chains open shops in a town, one at a time, in turns. Each possible site has a value, such as the number of customers near it. A town rule says that no two shops may be on neighboring sites. So a shop takes its own site and also blocks the sites next to it for everybody. The question is: can the chain that moves second be sure to collect at least a given total value, however the first chain plays?

To answer it you must think about moves and answers to moves, many turns ahead, like in chess. The best known exact methods try the whole tree of moves. This problem is believed to be harder than the problems where a single good answer can be checked quickly.

## Definition

**Input.** An undirected graph $G = (V, E)$, a value $b_v \ge 0$ for each node, and a bound $B$.

**Game.** Player 1 and Player 2 take turns, Player 1 first. A move selects one node that is not yet selected and has no selected neighbor, so the selected nodes always form an [independent set](/independent-set/). The game ends when no node can be selected. A player's total is the sum of $b_v$ over the nodes it selected.

**Question.** Does Player 2 have a strategy that guarantees a total of at least $B$ against every strategy of Player 1?

The game always ends after at most $|V|$ moves, because each move selects a new node. The question is about a strategy, not a single play: it has the form "for every first move there is an answer such that for every next move there is an answer such that ... Player 2 reaches $B$".

## Variants

- **Maximize the own total.** Each player wants the largest own total. The decision question above fixes the view of Player 2 and lets Player 1 act against it.
- **Unit values.** With $b_v = 1$ the game counts moves. It is close to Node Kayles, where the player who makes the last move wins, which Schaefer (1978) proved PSPACE-complete.
- **No edges.** With $E = \emptyset$ there is no blocking, and taking the largest remaining value is optimal for both players. Player 2 then gets the values at positions 2, 4, 6, ... of the sorted list.
- **Location in the plane.** Hotelling (1929) studied two sellers who choose positions on a line to capture customers. Voronoi games and leader-follower (Stackelberg) location problems, such as the centroid problem, are later forms of competitive location with distances instead of a graph.
- **The non-competitive problem.** With a single decision maker who opens sites to serve clients at least cost, the problem is the [facility location problem](/facility-location-problem/).

## Examples

Take a path $a - b - c - d - e$ with values $1, 10, 1, 10, 1$.

- If Player 1 selects $b$ (value 10), then $a$ and $c$ are blocked, and Player 2 answers with $d$ (value 10).
- If Player 1 selects $c$ (value 1), then $b$ and $d$ are both blocked. Only $a$ and $e$ are left, Player 2 takes one, and Player 1 takes the other. Player 2 gets 1.

Against the second opening Player 2 cannot get more than 1, so Player 2 can guarantee a total of 1 and no more. For $B = 1$ the answer is yes, and for $B = 2$ the answer is no. The example shows the main feature of the game: a move of low value can be strong because it blocks valuable sites.

## Known algorithms

- **[Minimax](/minimax/) search.** Search the [game tree](/game-tree/) depth first. The depth is at most $|V|$, so the search uses polynomial space, but the time can be exponential.
- **Memoized search over positions.** A position is the set of nodes that can still be selected, plus whose turn it is. Storing the value of each position gives $O(2^{|V|} \cdot |V|)$ time and exponential space. Alpha-beta pruning and symmetry reduce the work in practice.
- **Special cases.** With no edges, the greedy rule above is optimal. No polynomial-time algorithm for general graphs is known, and none exists unless P = PSPACE.

## Bounds

- **Membership in PSPACE.** The depth-first minimax search keeps one path of at most $|V|$ positions, each of polynomial size, so it decides the question in polynomial space.
- **PSPACE-hardness.** Kleinberg and Tardos (Section 9.5) reduce Competitive 3-SAT to it. So the problem is PSPACE-complete.
- **Consequences.** A polynomial-time algorithm would give P = PSPACE, and membership in NP would give NP = PSPACE.

## Reductions

- **From Competitive 3-SAT.** In Competitive 3-SAT, a formula $\Phi$ in conjunctive normal form has variables $x_1, \ldots, x_n$. Player 1 sets $x_1$, Player 2 sets $x_2$, and so on in order, and Player 1 wins if $\Phi$ is true at the end. This is the quantified formula $\exists x_1 \forall x_2 \exists x_3 \cdots \Phi$, so deciding the winner is PSPACE-complete. Take $n$ odd (add an unused variable if needed) and let $m$ be the number of clauses. The reduction below follows the plan of Kleinberg and Tardos.
  - **Variable gadget.** For each $i$, two nodes $t_i$ ("$x_i$ true") and $f_i$ ("$x_i$ false") joined by an edge, both of value $V_i = (m + 1) \cdot 4^{n - i}$. The values drop so fast that $V_i$ exceeds the sum of all later values plus $m$.
  - **Clause gadget.** For each clause $C_j$, a node $c_j$ of value 1 joined to the node of each literal of $C_j$: to $t_i$ if $x_i \in C_j$, and to $f_i$ if $\bar x_i \in C_j$.
  - **Bound.** $B = \sum_{i \text{ even}} V_i + 1$.
  - **Why it works.** A player who does not take a node of the lowest free variable pair lets the other player take it, and the value of that pair outweighs everything that follows. So both players set $x_1, x_2, \ldots, x_n$ in order. Since $n$ is odd, Player 2 then moves first among the clause nodes. The node $c_j$ is still free exactly when no selected literal node satisfies $C_j$, so Player 2 gets one more point exactly when some clause is false. So Player 2 reaches $B$ if and only if Player 2 wins Competitive 3-SAT, that is, if and only if Player 1 does not. PSPACE is closed under complement, so the problem is PSPACE-hard.
  - **Check.** We compared the winner of the formula game with the minimax value of the constructed game, by exhaustive search, on 2000 random formulas with up to 5 variables and up to 4 clauses of 1 to 3 literals (Python `random.Random(7)`). The two answers agreed on every formula. With all values equal to 1, the same construction fails on the one-clause formula $(x_2)$, which shows that the drop in values is needed.
- **Relation to Node Kayles and Geography.** [Generalized geography](/generalized-geography/), Node Kayles and [Hex](/hex-game/) are other PSPACE-complete games on graphs, proved by reductions from quantified formulas of the same shape.

## Applications

- **Teaching.** The problem is the standard natural example of a PSPACE-complete problem in Kleinberg and Tardos. It shows that planning against an opponent can be harder than search for one solution.
- **Competitive location.** Retail chains, franchise placement and zoning rules that forbid neighboring shops. The PSPACE-completeness means that exact optimal play is out of reach on large maps, so practice uses heuristics, depth-limited search or simpler leader-follower models.
- **Game analysis.** The game is an example of a two-player selection game on graphs, a family that also contains Node Kayles and many puzzles.

## References
