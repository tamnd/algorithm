---
tag: X0EDJD
kind: algorithm
slug: zielonka-algorithm
name: Zielonka's algorithm
aliases:
- Recursive parity game algorithm
- Zielonka's recursive algorithm
- McNaughton-Zielonka algorithm
area: logic-and-constraints/model-checking
level: research
summary: Solve a parity game by recursion on the top priority, with attractors. It gives the winning regions and positional strategies in O(m (n+1)^d) time.
solves: [parity-game-solving]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, d: the number of distinct priorities}
  time: {worst: O(m (n+1)^d)}
  space: {extra: O(d n + m)}
properties: {deterministic: true, recursive: true}
history:
  year: 1998
  people: [Wiesław Zielonka]
  note: Zielonka published the recursive algorithm and its proof of positional determinacy in Theoretical Computer Science in 1998. It adapts an algorithm of McNaughton (1993) for games with a Muller condition.
prereqs: [parity-game, breadth-first-search]
see_also: [parity-game-solving, mu-calculus-model-checking, modal-mu-calculus, emerson-lei-algorithm, fixed-point, quasi-polynomial-time]
sources:
  - paper: doi:10.1016/S0304-3975(98)00009-7
    title: Wiesław Zielonka, Infinite games on finitely coloured graphs with applications to automata on infinite trees, Theoretical Computer Science 200(1-2), 1998, pages 135 to 183
    locator: the recursive construction of the winning regions and the proof of memoryless determinacy for parity conditions
  - paper: "Robert McNaughton, Infinite games played on finite graphs, Annals of Pure and Applied Logic 65(2), 1993, pages 149 to 184"
    title: Infinite games played on finite graphs
    locator: the recursive algorithm for Muller games that Zielonka's algorithm adapts
  - title: Erich Grädel, Wolfgang Thomas and Thomas Wilke (eds.), Automata, Logics, and Infinite Games, Lecture Notes in Computer Science 2500, Springer, 2002
    locator: Chapter 6 (memoryless determinacy of parity games) and Chapter 7 (algorithms for parity games)
  - paper: "Oliver Friedmann, Recursive algorithm for parity games requires exponential time, RAIRO Theoretical Informatics and Applications 45(4), 2011, pages 449 to 457"
    title: Recursive algorithm for parity games requires exponential time
    locator: a family of games on which Zielonka's algorithm takes exponential time
  - paper: "Paweł Parys, Parity games: Zielonka's algorithm in quasi-polynomial time, MFCS 2019, LIPIcs 138"
    title: "Parity games: Zielonka's algorithm in quasi-polynomial time"
    locator: the modified recursion with two precision parameters
  - paper: "Oliver Friedmann and Martin Lange, Solving parity games in practice, ATVA 2009, Lecture Notes in Computer Science 5799, Springer"
    title: Solving parity games in practice
    locator: the experimental comparison of parity game solvers in PGSolver
---

Zielonka's algorithm solves a [parity game](/parity-game/): it computes the set of vertices from which each player wins, and a positional winning strategy for each player on its set. It takes the top priority, computes the *attractor* of the vertices with that priority, solves the rest of the game recursively, and removes the part that the opponent wins until the opponent wins nothing more. The worst-case time is $O(m (n+1)^d)$ for $n$ vertices, $m$ edges and $d$ distinct priorities, and some games force exponential time. In practice it is one of the fastest [parity game solvers](/parity-game-solving/), and its correctness proof is also the standard proof that parity games are positionally determined.

## In plain words

Two players move a token on a graph forever. Each vertex has a number, and a play is good for the first player when the largest number that comes back again and again is even. Look at the largest number in the game. Say it is even. If the token visits those vertices forever, the first player wins. So find every vertex from which the first player can force a visit to them. Remove these vertices and solve the smaller game that is left. If the second player wins nothing there, the first player wins everywhere: the second player can only stay in the smaller game and lose, or come back to the top vertices again and again and lose. If the second player wins some part, that part, and every vertex from which she can force the token into it, is hers for good. Cut it off and repeat.

## The problem

The input is a parity game $G = (V, V_0, V_1, E, \Omega)$ with a finite set of vertices $V = V_0 \sqcup V_1$, edges $E \subseteq V \times V$ such that each vertex has at least one successor, and priorities $\Omega : V \to \mathbb{N}$. Player $j$ moves from the vertices of $V_j$. Player 0 wins a play $v_0 v_1 v_2 \ldots$ when $\max \{ q : q = \Omega(v_k) \text{ for infinitely many } k \}$ is even. The output is the pair of winning regions $(W_0, W_1)$ and positional strategies $\sigma_0 : W_0 \cap V_0 \to V$ and $\sigma_1 : W_1 \cap V_1 \to V$ that win from every vertex of the region. This is the [parity game solving](/parity-game-solving/) problem. We write $n = |V|$, $m = |E|$ and $d$ for the number of distinct priorities.

For a set $X \subseteq V$ such that each vertex of $V \setminus X$ has a successor in $V \setminus X$, the subgame $G \setminus X$ has the vertices $V \setminus X$, the same owners and priorities, and the edges of $E$ inside $V \setminus X$.

## The algorithm

The *attractor* $\mathrm{Attr}_j(G, U)$ is the set of vertices from which player $j$ can force the token into $U$ in a finite number of moves. It is the least set $A \supseteq U$ such that a vertex of $V_j$ with a successor in $A$ is in $A$, and a vertex of $V_{1-j}$ with all its successors in $A$ is in $A$. The procedure ATTR computes it backwards from $U$, like a [breadth-first search](/breadth-first-search/) on the reversed graph. A vertex of the opponent keeps a counter of its successors that are not yet in $A$, and it joins $A$ when the counter reaches zero.

```pseudo id=attractor
ATTR_j(G, U)                               ▷ the vertices from which player j forces a visit to U
L13 A ← U, Q ← a queue that holds the vertices of U
L14 for each v ∈ V(G) do c[v] ← the number of successors of v in G
L15 while Q ≠ ∅ do
L16     w ← DEQUEUE(Q)
L17     for each predecessor v of w in G with v ∉ A do
L18         if v ∈ V_j then A ← A ∪ {v}, σ[v] ← w, ENQUEUE(Q, v)
L19         else c[v] ← c[v] − 1
L20             if c[v] = 0 then A ← A ∪ {v}, ENQUEUE(Q, v)
L21 return A
```

The main procedure is the recursion of Zielonka, with the second recursive call written as a loop. The sets $X_0$ and $X_1$ collect the vertices that are already decided.

```pseudo id=main
ZIELONKA(G)                                ▷ returns the winning regions (W_0, W_1) of G
L1  X_0 ← ∅, X_1 ← ∅
L2  while V(G) ≠ ∅ do
L3      p ← max{Ω(v) : v ∈ V(G)}, i ← p mod 2
L4      U ← {v ∈ V(G) : Ω(v) = p}
L5      A ← ATTR_i(G, U)
L6      (W'_0, W'_1) ← ZIELONKA(G \ A)
L7      if W'_{1−i} = ∅ then
L8          X_i ← X_i ∪ V(G), return (X_0, X_1)
L9      B ← ATTR_{1−i}(G, W'_{1−i})
L10     X_{1−i} ← X_{1−i} ∪ B
L11     G ← G \ B
L12 return (X_0, X_1)
```

Line L3 picks the top priority $p$; player $i$ is the player who likes it. Lines L4 and L5 compute the attractor $A$ of player $i$ to the top vertices. The set $V \setminus A$ is a trap for player $i$: she cannot leave it, and the opponent can stay in it, so $G \setminus A$ is a game and line L6 solves it. If the opponent wins nothing in $G \setminus A$ (line L7), player $i$ wins from every vertex of $G$. Else the opponent's region $W'_{1-i}$ is also hers in $G$, and so is her attractor $B$ to it (line L9). Lines L10 and L11 record $B$ and cut it off, and the loop starts again on the smaller game, which can have a new top priority.

The strategies come out of the same steps. In the case of line L8, player $i$ plays the strategy of the subgame on $W'_i = V(G) \setminus A$, the attractor strategy $\sigma$ of line L18 on $A \setminus U$, and any successor in $G$ on $U$. In the case of line L9, player $1-i$ plays the strategy of the subgame on $W'_{1-i}$ and the attractor strategy on $B \setminus W'_{1-i}$.

## Example

The game has six vertices. Player 0 owns $a$, $c$ and $e$, and player 1 owns $b$, $d$ and $f$.

| vertex | owner | priority | successors |
|---|---|---|---|
| a | 0 | 3 | b |
| b | 1 | 2 | a, c |
| c | 0 | 1 | c, d |
| d | 1 | 4 | e |
| e | 0 | 0 | d, f |
| f | 1 | 5 | b, f |

The calls run as follows. Each row is one pass of the loop, and the indent of the game shows the depth of the recursion.

| call on | p, i | U | A | result of the subgame | B, or the end |
|---|---|---|---|---|---|
| {a, b, c, d, e, f} | 5, 1 | {f} | {f} | $W'_0$ = {c, d, e} | B = Attr_0({c, d, e}) = {c, d, e}, so $X_0$ = {c, d, e} |
| . {a, b, c, d, e} | 4, 0 | {d} | {c, d, e} | $W'_1$ = {a, b} | B = Attr_1({a, b}) = {a, b}, so $X_1$ = {a, b} |
| . . {a, b} | 3, 1 | {a} | {a, b} | empty game | $W'_0 = \emptyset$, return ({}, {a, b}) |
| . {c, d, e} | 4, 0 | {d} | {c, d, e} | empty game | return ({c, d, e}, {a, b}) |
| {a, b, f} | 5, 1 | {f} | {f} | $W'_0 = \emptyset$ on {a, b} | return ({c, d, e}, {a, b, f}) |

So $W_0 = \{c, d, e\}$ and $W_1 = \{a, b, f\}$. Player 0 wins with $\sigma_0(c) = \sigma_0(e) = d$: the play then cycles through $d$ and $e$, with top priority 4. Player 1 wins with $\sigma_1(b) = a$ and $\sigma_1(f) = b$: the play reaches the cycle $a b$, with top priority 3. In the first row, $e$ is not in $A$ because player 0 owns $e$ and can go to $d$. In the second row, $b$ is not in the 0-attractor of $\{d\}$ because player 1 can go to $a$.

## Correctness

**Theorem.** For every finite parity game $G$ in which each vertex has a successor, ZIELONKA$(G)$ terminates and returns a partition $(W_0, W_1)$ of $V$, and the strategies built with it are positional and winning: every play that starts in $W_j$ and follows $\sigma_j$ stays in $W_j$ and is won by player $j$, whatever the opponent does. So $W_0$ and $W_1$ are the winning regions.

The proof is by strong induction on the number of vertices, and it rests on two facts about attractors. First, from $\mathrm{Attr}_j(G, U)$ the attractor strategy reaches $U$ in at most $|A|$ moves, because each move goes to a vertex that ATTR added earlier. Second, the complement of an attractor is a trap for player $j$, so it is a subgame, and a strategy that wins in the subgame for the opponent still wins in $G$. In the case of line L8, a play that follows the strategy of player $i$ either visits $U$ infinitely often, and then the top priority seen infinitely often is $p$, or it stays in $W'_i$ from some point on and is won there. The full proof, with the loop written as the recursion it replaces, is in [the correctness proof](proofs/correctness.md). The theorem gives the [positional determinacy](/parity-game/) of finite parity games as a corollary.

## Complexity

**Attractor.** Line L14 takes $O(n + m)$ time. Each vertex enters $Q$ at most once, because it enters $Q$ when it joins $A$, and it never leaves $A$. When $w$ leaves $Q$, line L17 scans its predecessors, so the scans take $\sum_w |\mathrm{pred}(w)| = m$ steps in total. So ATTR runs in $O(n + m)$ time, which is linear in the size of the game.

**Number of calls.** Let $C(n, d)$ be the largest number of passes of the loop, over all recursive calls, on a game with at most $n$ vertices and at most $d$ distinct priorities. The pass of the loop on $G$ makes one call on $G \setminus A$, which has fewer vertices ($A \supseteq U \neq \emptyset$) and fewer distinct priorities (it has no vertex of priority $p$). If it does not stop, it continues on $G \setminus B$, which has fewer vertices ($B \supseteq W'_{1-i} \neq \emptyset$). So $C(0, d) = 0$ and, for $n \ge 1$,

$$C(n, d) \le 1 + C(n-1, d-1) + C(n-1, d).$$

By induction on $n$, $C(n, d) + 1 \le 2 \binom{n+d}{d}$: the base is $C(0, d) + 1 = 1$, and the step uses $\binom{n+d-2}{d-1} + \binom{n+d-1}{d} \le \binom{n+d-1}{d-1} + \binom{n+d-1}{d} = \binom{n+d}{d}$. Since $\binom{n+d}{d} = \prod_{k=1}^{d} \frac{n+k}{k} \le (n+1)^d$, there are at most $2(n+1)^d$ passes.

**Time.** One pass, without its recursive call, costs $O(n + m)$: two attractors, a maximum, and set differences. Each vertex has a successor, so $n \le m$, and the total time is $O(m (n+1)^d)$ in the worst case.

**Lower bound.** The bound is not only an artefact of the analysis. Friedmann (2011) built a family of games on which the algorithm takes time exponential in the number of vertices. So Zielonka's algorithm is not polynomial, and it is not quasi-polynomial without changes.

**Space.** The recursion has depth at most $d + 1$, because each nested call has fewer distinct priorities, and each level keeps $O(n)$ sets of vertices. With the $O(n + m)$ working space of ATTR, the extra space is $O(d n + m)$.

## Properties

- **Exact and deterministic.** It returns the true winning regions and no estimate.
- **Gives strategies.** Positional winning strategies for both players come out of the same recursion, at no extra cost in the $O$ bound.
- **Symbolic.** It uses only set operations, predecessors and attractors, so it also runs on sets that are stored as [BDDs](/symbolic-model-checking/).
- **Global.** It solves all vertices at once. It cannot stop early when only one start vertex matters.

## Variants and improvements

- **McNaughton's algorithm.** The same recursion for Muller games, where the winner depends on the set of vertices seen infinitely often (McNaughton 1993). Zielonka's version is the special case of parity conditions, and parity conditions make the strategies positional.
- **Quasi-polynomial Zielonka.** Parys (2019) adds two precision parameters that limit the depth at which the opponent's regions are searched, and gets a quasi-polynomial time bound.
- **Priority compression and decomposition.** Before the run, renumber the priorities so that two priorities next to each other in the order have different parities; this keeps the winner of each play and can make $d$ smaller. Solve the [strongly connected components](/strongly-connected-components/) of the game graph one at a time, from the bottom. PGSolver uses both steps (Friedmann and Lange 2009).
- **Small progress measures and strategy improvement.** Other solvers of the same problem. They are compared on the [parity game solving](/parity-game-solving/) page.

## When to use it

Use Zielonka's algorithm as the default solver for parity games that come from [mu-calculus model checking](/mu-calculus-model-checking/), from LTL synthesis or from automata on infinite trees. In the measurements of Friedmann and Lange (2009) on the benchmark games of PGSolver, it was in most cases faster than small progress measures and strategy improvement. If you need a guaranteed bound below $n^d$, use a quasi-polynomial algorithm. If the game has only a few priorities, any of the algorithms is polynomial, and the attractor-based recursion is the simplest to write.

## Pitfalls

- **Attractor of the wrong player.** Line L5 uses the attractor of player $i = p \bmod 2$, the player who likes priority $p$. Line L9 uses the attractor of the opponent $1 - i$. On the example, the 0-attractor of $\{d\}$ is $\{c, d, e\}$, but the 1-attractor of $\{d\}$ is only $\{d\}$, because player 0 owns $c$ and $e$ and can move away from $d$.
- **Stopping after one removal.** After line L11, the top priority of $G \setminus B$ can be different, and the opponent can win more of the smaller game. The loop must run again; a single pass returns $W_i = V \setminus B$, which is wrong when the second pass finds a new region of the opponent.
- **Vertices without successors.** The theory needs a successor at each vertex. A dead end must be removed first (its owner loses), or given a self-loop with a priority of the opponent's parity.
- **The min-parity convention.** Some papers let player 0 win when the least priority seen infinitely often is even. The algorithm is the same with the least priority in line L3. Mixing the two conventions in one tool gives the wrong winner.
- **Recursion depth.** The plain recursion has depth up to $n + d$. Writing the second call as the loop of line L2 keeps the depth at $d + 1$.

## Implementations

## History

Robert McNaughton gave a recursive algorithm for games with Muller conditions in 1993. Wiesław Zielonka adapted it in 1998 to parity conditions and gave with it a constructive proof that parity games are determined with positional strategies, a result that Emerson and Jutla and, independently, Mostowski had proved in 1991. Friedmann showed in 2011 that the algorithm needs exponential time on some games. After the quasi-polynomial algorithm of Calude, Jain, Khoussainov, Li and Stephan in 2017, Parys showed in 2019 that a modified Zielonka recursion is also quasi-polynomial.

## References
