---
tag: 9S85XA
kind: problem
slug: games-on-graphs
name: Games on arbitrary graphs
aliases:
- token game on a directed graph
- graph game
area: games-and-search/game-tree-search
level: core
summary: "Two players push a token along the edges of a directed graph, and a player with no move loses. The problem: label each vertex a win, loss or draw, where cycles allow infinite play."
prereqs: [winning-losing-states, game-tree, depth-first-search]
see_also: [generalized-geography, nim, grundy-number, retrograde-analysis, parity-game, parity-game-solving, reachability-problem, alternating-turing-machine]
sources:
  - book: isbn:9780821851906
    title: Aaron N. Siegel, Combinatorial Game Theory, Graduate Studies in Mathematics 146, American Mathematical Society (2013)
    locator: Chapter VI, Loopy Games, from p. 279 (games whose positions can repeat, infinite play as a draw, and the outcomes of loopy impartial games)
  - book: isbn:9783540003885
    title: Erich Grädel, Wolfgang Thomas and Thomas Wilke (editors), Automata, Logics, and Infinite Games, Lecture Notes in Computer Science 2500, Springer (2002)
    locator: Chapter 2, Infinite Games (arenas, reachability and safety games, attractors, Büchi and parity conditions; general locator)
  - paper: "\"Provably difficult combinatorial games\""
    title: Larry J. Stockmeyer and Ashok K. Chandra, Provably difficult combinatorial games, SIAM Journal on Computing 8(2) (1979)
    locator: pp. 151 to 174 (games on graphs given by a succinct rule are complete for exponential time)
  - book: isbn:9780195085914
    title: Raymond Greenlaw, H. James Hoover and Walter L. Ruzzo, Limits to Parallel Computation, P-Completeness Theory, Oxford University Press (1995)
    locator: Appendix A, the list of P-complete problems (alternating graph accessibility, the reachability game; general locator)
---

A game on a graph is played by two players who take turns moving a token along the edges of a finite directed graph; under normal play a player whose vertex has no outgoing edge loses, and a play that goes on forever is a draw. The problem is to decide, for each vertex, whether the player to move there wins, loses or draws with best play. Every finite game of [perfect information](/perfect-information-game/) without chance is a game of this kind once its positions are the vertices, and Nim, chess endgames and tic-tac-toe all fit. When the graph is written out, the problem takes linear time by the backward labeling of [winning and losing states](/winning-losing-states/); the hard cases come from graphs that are described by a rule and are far too large to write out.

## In plain words

Draw some dots and arrows between them. Put a coin on one dot. Two players take turns, and a turn means sliding the coin along one arrow. If the coin is on a dot with no arrow out, the player to move is stuck and loses. If the coin can go around a loop, the game may never end, and then nobody wins.

The question is, for every dot: if the coin starts here, does the player to move win, lose, or only draw, when both sides play as well as possible?

A game tree is the special case with no loops, where every game ends. Loops are what make draws possible, and they are why you cannot just look a fixed number of moves ahead. Many real games, such as chess, have positions that can repeat, so they are games on graphs with loops.

## Definition

**The token game.** The input is a finite directed graph $G = (V, E)$, given by adjacency lists, so its size is $|V| + |E|$. A *play* from $v_0 \in V$ is a sequence $v_0, v_1, v_2, \dots$ with $(v_i, v_{i+1}) \in E$; the player to move at $v_0$ chooses $v_1$, the other player chooses $v_2$, and so on. A finite play that stops at a vertex with no out-edge (a *dead end*) is lost by the player to move there. An infinite play is a draw. A *strategy* of a player maps each finite play that ends at a vertex where this player is to move, and that is not a dead end, to an out-edge of that vertex.

**Outcome.** The outcome $o(v) \in \{W, L, D\}$ of a vertex is

- $W$ if the player to move at $v$ has a strategy that wins against every strategy of the opponent,
- $L$ if the opponent has such a strategy,
- $D$ otherwise.

The sets of $W$ and $L$ vertices are the smallest sets closed under two rules: a vertex with a successor in $L$ is in $W$, and a vertex whose successors are all in $W$ is in $L$ (a dead end has no successors, so it is in $L$). The $D$ vertices are the rest. The labeling page proves this, and proves that in case $D$ each player has a strategy that never loses. The strategies read off the labels look only at the current vertex, so memoryless strategies suffice.

**The problem.** Given $G$, compute $o(v)$ for every $v \in V$, or given $G$ and one vertex $v_0$, compute $o(v_0)$. A winning strategy is part of a full answer: for each $W$ vertex, a successor that is $L$.

**Two-player arenas.** In the form used in verification and in [parity games](/parity-game/), the vertices are split as $V = V_0 \sqcup V_1$, and the owner of a vertex moves from it, whoever moved last. A *winning condition* is a set of infinite (or maximal finite) plays that player 0 wants. The token game above is the arena on $V \times \{0, 1\}$, where $(v, p)$ means "token on $v$, player $p$ to move", with edges $(v, p) \to (w, 1 - p)$ for $(v, w) \in E$, and with player 0 aiming to reach a dead end where player 1 is to move.

## Variants

- **Reachability and safety games.** Player 0 wins when the token reaches a target set $T$, and player 1 wins otherwise; a safety game swaps the roles. The winning region of player 0 is the *attractor* of $T$: add a vertex of player 0 when one successor is already in the set, and a vertex of player 1 when all its successors are. One pass with a counter per vertex computes it in $O(|V| + |E|)$; the [parity game](/parity-game/) page defines attractors and traps in full. The token game is a reachability game on the doubled arena above.
- **Büchi, parity and Muller games.** The winner of an infinite play depends on which vertices it visits infinitely often. Büchi games are solved by repeated attractors in $O(|V| \cdot |E|)$ time. Parity games are in NP $\cap$ co-NP and have quasi-polynomial algorithms ([parity game solving](/parity-game-solving/), [Zielonka's algorithm](/zielonka-algorithm/)); no polynomial algorithm is known. These games are the core of controller synthesis and of model checking for the modal mu-calculus, whose formulas are nested [fixed points](/fixed-point/).
- **Misère play.** A player with no move wins. This is the token game on the graph with one new dead end $z$ and an edge from every old dead end to $z$, so it costs the same.
- **Acyclic graphs.** If $G$ is a DAG, every play ends, no vertex is $D$, and the labeling is a pass in reverse [topological order](/topological-sort/). This is the setting of finite impartial games and of [Grundy numbers](/grundy-number/).
- **Several tokens.** With several tokens, where a move pushes one token of the mover's choice, the game is a sum of token games. On a DAG the [Sprague-Grundy theorem](/sprague-grundy-theorem/) solves it with the XOR of the Grundy numbers of the tokens' vertices. On a graph with cycles, a generalized Grundy function with an extra value for loopy positions plays the same role.
- **Deleting visited vertices or edges.** If a vertex (or edge) may not be used twice, the game is [generalized geography](/generalized-geography/). The state now includes the set of used vertices, and the problem becomes PSPACE-complete on directed graphs.

## Examples

**A graph with a draw.** Take six vertices $a, \dots, f$ with edges $a \to b$, $a \to e$, $b \to c$, $c \to d$, $e \to a$, $e \to f$ and $f \to e$. The vertex $d$ is the only dead end. Looking ahead $k$ moves settles the vertices whose result is forced within $k$ moves:

| moves looked ahead | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ |
|---|---|---|---|---|---|---|
| 1 | ? | ? | ? | L | ? | ? |
| 2 | ? | ? | W | L | ? | ? |
| 3 | ? | L | W | L | ? | ? |
| 4 | W | L | W | L | ? | ? |
| any larger number | W | L | W | L | D | D |

From $a$ the winning move is $a \to b$. At $e$ the player to move has no move to an $L$ vertex: $a$ is $W$, and $f$ only leads back to $e$. So both players can keep the token on the cycle $e, f$, and $e$ and $f$ are draws. No depth of lookahead decides them, which is why a depth-limited search, such as [minimax](/minimax/) with a cutoff, cannot certify a draw.

**One edge changes several labels.** Add the edge $f \to d$. Now $f$ is $W$ (move to $d$), and $e$ becomes $L$: its moves go to $a$ and $f$, both $W$. The draws are gone.

**An arena.** Give the original six vertices owners: player 0 moves at $a$, $c$, $e$ and player 1 at $b$, $d$, $f$, and let player 0 aim for $T = \{d\}$. The attractor is all six vertices: from $f$ player 1 must go to $e$, then player 0 goes $e \to a \to b$, player 1 must go $b \to c$, and player 0 plays $c \to d$. If player 1 gets one more edge, $b \to e$, the attractor shrinks to $\{c, d\}$: player 1 answers $a \to b$ with $b \to e$, and the token can circle $a, b, e$ forever.

**Nim as a graph.** The [Nim](/nim/) position $(3, 4, 5)$ is a vertex of a DAG whose vertices are all $4 \cdot 5 \cdot 6 = 120$ tuples $(b_1, b_2, b_3)$ with $b_i$ at most the heap size. The graph is exponential in the input size, the number of bits of the heap sizes, while the XOR rule answers in linear time.

## Known algorithms

- **Backward labeling with counters**, $O(|V| + |E|)$ time and space, on [winning and losing states](/winning-losing-states/). It labels dead ends $L$, then repeatedly marks a vertex $W$ when a successor is $L$ and $L$ when its count of unlabeled successors reaches zero; whatever stays unlabeled is $D$. In game programs the same method over all positions with few pieces is [retrograde analysis](/retrograde-analysis/), which builds [endgame tablebases](/endgame-tablebase/).
- **Attractor computation**, $O(|V| + |E|)$, for reachability and safety games on arenas; see [parity game](/parity-game/).
- **Iterated attractors and progress measures** for Büchi and parity conditions; see [parity game solving](/parity-game-solving/).
- **Forward search** from one vertex, when the graph is given implicitly: [minimax](/minimax/) or [alpha-beta pruning](/alpha-beta-pruning/) with a [transposition table](/transposition-table/), or [proof-number search](/proof-number-search/) and [df-pn](/df-pn/). On graphs with cycles these need care with repeated positions, because a result found along one path may depend on the path.

## Bounds

- **Explicit graphs.** $\Theta(|V| + |E|)$ time on a RAM. The upper bound is the backward labeling. For the lower bound, take a vertex whose read out-edges all lead to $W$ vertices: as long as one of its out-edges is unread, that edge may lead to a dead end, which would turn the vertex from $L$ into $W$. So every edge must be read on some inputs.
- **Parallel complexity.** The reachability game on arenas (alternating graph accessibility) is P-complete under logspace reductions, so it has no fast parallel algorithm unless every polynomial-time problem has one.
- **Succinct graphs.** When positions are bit strings of length $n$ and the moves are given by a rule, such as a Boolean formula over the old and new position, the graph has up to $2^n$ vertices. The labeling then takes time exponential in $n$, and Stockmeyer and Chandra showed that some such games are complete for exponential time, so no algorithm is much faster in the worst case.
- **Polynomial-length plays.** If every play from a position of size $n$ ends after a number of moves polynomial in $n$, a depth-first [minimax](/minimax/) search keeps one path of polynomial length and decides the game in polynomial space. Generalized geography meets this condition and is PSPACE-complete, so the polynomial-space bound cannot be replaced by a polynomial-time bound unless P = PSPACE.

## Reductions

- **Token game to reachability game**, linear: the doubled arena $V \times \{0, 1\}$ of the Definition, with the targets "dead end, player 1 to move". The $W$ vertices of $G$ are the vertices $(v, 0)$ won by player 0, the $L$ vertices are those won by player 1 with the symmetric targets, and the $D$ vertices are won by neither.
- **Misère to normal play**, linear: add a fresh dead end below every dead end.
- **Finite games of perfect information to games on graphs**: positions become vertices and moves become edges. A [game tree](/game-tree/) is the unfolding of this graph from the start; merging equal positions turns the tree back into a graph, which is what a transposition table does.
- **Alternating machines.** Deciding a game on the configuration graph of an [alternating Turing machine](/alternating-turing-machine/) is the same as deciding acceptance. This is the link between games and the classes P, PSPACE and EXPTIME.

## Applications

- **Endgame databases.** Retrograde analysis over all positions of a chess or checkers endgame is backward labeling on an explicit graph with cycles; the draws are the positions where neither side can force progress.
- **Verification and synthesis.** A controller that must keep a system safe against an adversarial environment is a winning strategy of a safety game; richer specifications give Büchi and parity games, and [contingent planning](/contingent-planning/) with adversarial outcomes is a reachability game.
- **Loopy combinatorial games.** Board games where positions can repeat are analyzed as games on graphs with draws; Siegel's chapter on loopy games develops their values.
- **Testing solvers.** Random graphs with cycles are standard test inputs for search algorithms that must handle repeated positions, because the backward labeling gives the exact answer.

## References
