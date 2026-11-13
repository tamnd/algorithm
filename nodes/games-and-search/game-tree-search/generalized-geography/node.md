---
tag: 261S19
kind: problem
slug: generalized-geography
name: Generalized geography
aliases:
- GEOGRAPHY
- vertex geography
- edge geography
area: games-and-search/game-tree-search
level: advanced
summary: Players move a token along a directed graph and may not reuse a vertex (or edge); the stuck player loses. Both directed versions are PSPACE-complete (Schaefer; Lichtenstein and Sipser).
prereqs: [games-on-graphs, qbf, pspace, polynomial-time-reduction]
see_also: [qsat, alternating-turing-machine, hex-game, nim, combinatorial-game-theory, maximum-matching, edmonds-blossom, planar-graph]
sources:
  - paper: doi:10.1016/0022-0000(78)90045-4
    title: Thomas J. Schaefer, On the complexity of some two-person perfect-information games, Journal of Computer and System Sciences 16(2) (1978)
    locator: pp. 185 to 225 (edge geography on directed graphs, a problem suggested by Karp, is PSPACE-complete; also Node Kayles and other games)
  - paper: doi:10.1145/322186.322201
    title: David Lichtenstein and Michael Sipser, GO is polynomial-space hard, Journal of the ACM 27(2) (1980)
    locator: pp. 393 to 401 (vertex geography is PSPACE-complete, also on planar bipartite graphs with maximum degree 3, and the reduction from planar geography to Go)
  - paper: doi:10.1016/0304-3975(93)90026-P
    title: Aviezri S. Fraenkel, Edward R. Scheinerman and Daniel Ullman, Undirected edge geography, Theoretical Computer Science 112(2) (1993)
    locator: pp. 371 to 381 (undirected vertex geography is solved by maximum matchings; undirected edge geography is PSPACE-complete, also for planar graphs of maximum degree 3, and polynomial on bipartite graphs)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, 3rd edition, Cengage Learning (2013)
    locator: Section 8.3, PSPACE-Completeness (generalized geography and its reduction from TQBF; general locator, the theorem number was not checked)
  - paper: "\"The complexity of Go\""
    title: John M. Robson, The complexity of Go, Information Processing 83, Proceedings of the IFIP 9th World Computer Congress (1983)
    locator: pp. 413 to 417 (Go with the Japanese ko rule is complete for exponential time; general locator)
---

Generalized geography is a game on a directed graph: a token starts on a given vertex, the two players move it in turn along an edge, a vertex (in *vertex geography*) or an edge (in *edge geography*) may be used only once, and the player who cannot move loses. The problem is to decide whether the first player has a winning strategy. Both directed versions are PSPACE-complete: Schaefer proved it for edge geography in 1978, and Lichtenstein and Sipser for vertex geography in 1980, even on planar bipartite graphs of maximum degree 3. The game is the standard starting point for PSPACE-hardness proofs of board games, and it is the clearest example of how forbidding repeated positions turns the linear-time [game on a graph](/games-on-graphs/) into a hard problem.

## In plain words

The name comes from a children's word game. One child says a city, say Paris. The next must say a city whose name starts with the last letter, S, such as Sydney. Then a city starting with Y, and so on. No city may be said twice. The child who cannot answer loses.

Draw each city as a dot and an arrow from one city to every city that may follow it. Now the game is: move a marker along the arrows, never land on a dot that was used before, and lose when you are stuck. Generalized geography is this game on any drawing of dots and arrows.

The rule "never return" makes the game end, so there are no draws. But it also means that each player must remember the whole path so far, and this makes the game very hard to solve in general.

## Definition

**Vertex geography (GG).** The input is a directed graph $G = (V, E)$ and a start vertex $s \in V$. A position is a pair $(v, U)$, where $v$ is the vertex of the token and $U \subseteq V$ is the set of used vertices; the start is $(s, \{s\})$. A move from $(v, U)$ goes to $(w, U \cup \{w\})$ for an edge $(v, w) \in E$ with $w \notin U$. Players I and II alternate, player I first. A player with no move loses. The problem: does player I have a winning strategy?

**Edge geography (EG).** The same, but a position is $(v, F)$ with $F \subseteq E$ the set of used edges, a move uses an unused edge out of $v$, and vertices may be visited again.

**Undirected versions.** The graph is undirected, and a move goes along any unused (edge version) or to any unused neighbor (vertex version).

**Size and finiteness.** The input size is $|V| + |E|$. Every play of vertex geography has at most $|V| - 1$ moves, and every play of edge geography at most $|E|$, so the game is finite, has no draws, and by [Zermelo's theorem](/zermelo-theorem/) one player has a winning strategy. The number of positions, though, is exponential: up to $|V| \cdot 2^{|V|}$ in vertex geography.

## Variants

The complexity depends on the version and on the graph class.

| version | directed graphs | undirected graphs |
|---|---|---|
| vertex geography | PSPACE-complete (Lichtenstein and Sipser 1980), also planar bipartite with maximum degree 3 | polynomial: player I wins exactly when every [maximum matching](/maximum-matching/) covers $s$ (Fraenkel, Scheinerman and Ullman 1993) |
| edge geography | PSPACE-complete (Schaefer 1978) | PSPACE-complete, also planar with maximum degree 3; polynomial on bipartite graphs (Fraenkel, Scheinerman and Ullman 1993) |

- **Acyclic graphs.** On a DAG the token can never return, so the used set never matters, and the game is the token game of [games on graphs](/games-on-graphs/), solved in linear time.
- **Partisan geography.** Each player has their own edge set. Hardness carries over, because the impartial game is the special case where both sets are equal.
- **Sums of geography games.** Several tokens on separate graphs, one moved per turn. The [Sprague-Grundy theorem](/sprague-grundy-theorem/) applies, but computing the Grundy value of one component is already as hard as deciding it.

## Examples

**A small graph.** Take vertices $a, b, c, d, e$ and edges $a \to b$, $a \to c$, $b \to d$, $c \to d$, $d \to e$, $e \to b$. The graph has no dead end, so in the token game where vertices may repeat every vertex is a draw: play can circle $b, d, e$ forever. Geography forbids that, and each start has a winner:

| start | winner | reason |
|---|---|---|
| $a$ | player I | $a \to b$; then $b \to d$, $d \to e$ are forced, and at $e$ player II cannot return to the used $b$ |
| $b$ | player II | $b \to d$, $d \to e$ are forced, and player I is stuck at $e$ |
| $c$ | player I | $c \to d$, $d \to e$, $e \to b$ are forced, and player II is stuck at $b$ |
| $d$ | player II | $d \to e$, $e \to b$ are forced, and player I is stuck at $b$ |
| $e$ | player II | $e \to b$, $b \to d$ are forced, and player I is stuck at $d$ |

From $a$, the move $a \to c$ loses: after it, $c \to d$, $d \to e$, $e \to b$ are forced and player I is stuck at $b$, since $d$ is used.

**Cycles.** On a directed cycle with $n$ vertices, every play visits all vertices and has $n - 1$ moves, so player I wins exactly when $n$ is even.

**Edge geography.** On the graph with edges $0 \to 1$, $1 \to 0$, $0 \to 2$, $2 \to 0$ from $0$, edge geography lasts four moves and player II wins, while vertex geography lasts one move and player I wins: the two versions can disagree on the same graph.

**The reduction on a formula.** The formula $\exists x_1 \forall x_2 \exists x_3 : (x_1 \lor x_2) \land (\lnot x_2 \lor x_3) \land (\lnot x_1 \lor \lnot x_3)$ is false: if $x_1$ is false, player $\forall$ sets $x_2$ false and the first clause fails; if $x_1$ is true, the third clause forces $x_3$ false, and then $x_2$ true breaks the second clause. The construction in Reductions gives a graph with 16 vertices and 24 edges, on which player I loses vertex geography, as the reduction requires.

## Known algorithms

- **Exhaustive search with a memo** over the positions $(v, U)$: $O(|V| \cdot 2^{|V|})$ positions, each examined in $O(\deg v)$ time, so $O(2^{|V|} (|V| + |E|))$ time and as much space. This is the backward labeling of [winning and losing states](/winning-losing-states/) on the exponential graph of positions.
- **Depth-first [minimax](/minimax/)** without a memo: the stack holds one path of at most $|V|$ vertices, so the space is polynomial, $O(|V| \log |V|)$ bits besides the input, and the time is exponential. This places vertex and edge geography in PSPACE.
- **Undirected vertex geography** in polynomial time: compute the matching number $\nu(G)$ and $\nu(G - s)$ with [Edmonds' blossom algorithm](/edmonds-blossom/); every maximum matching covers $s$ exactly when $\nu(G - s) < \nu(G)$.
- **Game-tree search** with pruning ([alpha-beta pruning](/alpha-beta-pruning/), [proof-number search](/proof-number-search/)) helps in practice, but the transposition key must include the used set, because the same vertex with different used sets is a different position.

## Bounds

- **Upper bound.** Vertex and edge geography are in PSPACE, by the depth-first search above, and in time $2^{O(|V|)}$ (vertex version) by the memo.
- **Lower bound.** Both directed versions are PSPACE-hard under polynomial-time reductions, so they have no polynomial-time algorithm unless P = PSPACE. Hardness holds for vertex geography even on planar bipartite graphs where every vertex has total degree at most 3 and in-degree and out-degree at most 2 (Lichtenstein and Sipser).
- **The undirected vertex case is easy.** The matching criterion gives a polynomial algorithm, which shows that the hardness comes from the direction of the edges.

## Reductions

**From TQBF to vertex geography.** Let $\Phi = \exists x_1 \forall x_2 \exists x_3 \cdots Q x_n\, \varphi$, where $\varphi$ is in conjunctive normal form and the quantifiers alternate ([QBF](/qbf/), [QSAT](/qsat/)). Add a dummy variable if needed so that $n$ is odd and the last quantifier is $\exists$. Build:

1. For each variable $x_k$ a *diamond*: a top $t_k$ with edges to two vertices $P_k$ and $N_k$, both with an edge to a bottom $b_k$. Add $b_k \to t_{k+1}$ for $k < n$, and $b_n \to c$.
2. For each clause $C_j$ a vertex $C_j$, with an edge $c \to C_j$.
3. For each literal of $C_j$, an edge from $C_j$ to $P_k$ if the literal is $x_k$, and to $N_k$ if it is $\lnot x_k$.

The start is $t_1$. The graph has $4n + 1 + m$ vertices for $m$ clauses, and is built in polynomial time.

*Why it works.* At $t_k$ the player to move picks $P_k$ or $N_k$; the opponent must move to $b_k$, and the first player moves on to $t_{k+1}$. So player I chooses in the diamonds of odd $k$ and player II in those of even $k$, which matches the quantifiers. Read "the path went through $N_k$" as $x_k$ true, which leaves $P_k$ unused, and "through $P_k$" as $x_k$ false, which leaves $N_k$ unused. After $b_n$, player I moves to $c$ (as $n$ is odd), player II picks a clause vertex $C_j$, and player I must move to a literal vertex of $C_j$. That vertex is unused exactly when its literal is true. If player I reaches an unused $P_k$ or $N_k$, player II must move to $b_k$, which is used, so player II is stuck and loses. If every literal of $C_j$ is false, player I is stuck and loses. So player I wins exactly when player $\exists$ can choose values so that every clause that player $\forall$ points to has a true literal, that is, when $\Phi$ is true.

**Further reductions.** Lichtenstein and Sipser reduce to planar geography by crossover gadgets and then to Go on an $n \times n$ board, which shows that Go is PSPACE-hard. Schaefer's paper reduces from formula games to edge geography and to Node Kayles. Generalized Hex is also PSPACE-complete, by a different reduction ([Hex](/hex-game/)).

## Applications

- **Hardness of board games.** Geography gadgets are the usual first step in proofs that a game is PSPACE-hard: Go (Lichtenstein and Sipser), and many puzzles and games collected by Hearn and Demaine. With the ko rule, where a position may not repeat in a set way, Robson showed Go to be complete for exponential time; geography's "no repeats" rule is what keeps it inside PSPACE.
- **Teaching PSPACE.** Generalized geography is the textbook example of a PSPACE-complete game, next to TQBF, because the alternation of the quantifiers matches the alternation of the players. The link to [alternating Turing machines](/alternating-turing-machine/) is the same idea in machine form.
- **Testing game solvers.** Random geography instances have no draws and a known answer by exhaustive search, so they are used to test solvers that must handle path-dependent positions.

## References
