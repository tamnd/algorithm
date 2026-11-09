---
tag: BE2X79
kind: definition
slug: parity-game
name: Parity game
aliases:
- Parity games
- Two-player parity game
area: logic-and-constraints/model-checking
level: research
summary: A two-player game of infinite duration on a finite graph. Player 0 wins a play when the largest priority seen infinitely often is even. Both players have positional winning strategies.
prereqs: [strongly-connected-components, buchi-automaton]
see_also: [parity-game-solving, zielonka-algorithm, modal-mu-calculus, mu-calculus-model-checking, unambiguous-polynomial-time, quasi-polynomial-time, stochastic-game]
sources:
  - paper: "E. Allen Emerson and Charanjit S. Jutla, Tree automata, mu-calculus and determinacy, 32nd IEEE Symposium on Foundations of Computer Science (FOCS 1991), pages 368 to 377"
    title: Tree automata, mu-calculus and determinacy
    locator: the memoryless determinacy of parity games (called rank or Rabin chain games there) and the link to the mu-calculus
  - paper: "Andrzej W. Mostowski, Games with forbidden positions, Technical Report 78, University of Gdańsk, 1991"
    title: Games with forbidden positions
    locator: the independent proof of positional determinacy
  - paper: doi:10.1016/S0304-3975(98)00009-7
    title: Wiesław Zielonka, Infinite games on finitely coloured graphs with applications to automata on infinite trees, Theoretical Computer Science 200(1-2), 1998, pages 135 to 183
    locator: the inductive proof of positional determinacy by attractors
  - paper: "E. Allen Emerson, Charanjit S. Jutla and A. Prasad Sistla, On model-checking for fragments of mu-calculus, CAV 1993, Lecture Notes in Computer Science 697, Springer"
    title: On model-checking for fragments of mu-calculus
    locator: the NP ∩ co-NP bound for mu-calculus model checking through parity games
  - paper: "Marcin Jurdziński, Deciding the winner in parity games is in UP ∩ co-UP, Information Processing Letters 68(3), 1998, pages 119 to 124"
    title: Deciding the winner in parity games is in UP ∩ co-UP
    locator: the reduction to discounted payoff games and the unique certificates
  - paper: "Cristian S. Calude, Sanjay Jain, Bakhadyr Khoussainov, Wei Li and Frank Stephan, Deciding parity games in quasipolynomial time, 49th ACM Symposium on Theory of Computing (STOC 2017), pages 252 to 263"
    title: Deciding parity games in quasipolynomial time
    locator: the main theorem, a quasi-polynomial time bound and a polynomial bound when the number of priorities is at most the logarithm of the number of vertices
  - title: Erich Grädel, Wolfgang Thomas and Thomas Wilke (eds.), Automata, Logics, and Infinite Games, Lecture Notes in Computer Science 2500, Springer, 2002
    locator: Chapter 2 (infinite games) and Chapter 6 (memoryless determinacy of parity games)
---

A *parity game* is a two-player game of infinite duration on a finite directed graph whose vertices carry natural numbers called priorities. The two players move a token along the edges forever, and player 0 wins the resulting play when the largest priority that occurs infinitely often is even. Parity games are the game form of [mu-calculus model checking](/mu-calculus-model-checking/) and of the emptiness problem for automata on infinite trees. They are positionally determined: from each vertex one of the players has a winning strategy that looks only at the current vertex. Deciding the winner is in [NP](/np/) ∩ [co-NP](/co-np/), in [UP](/unambiguous-polynomial-time/) ∩ co-UP and in [quasi-polynomial time](/quasi-polynomial-time/), and no polynomial algorithm is known.

## Definition

### The arena and the winning condition

A *parity game* is a tuple $G = (V, V_0, V_1, E, \Omega)$ where

- $V$ is a finite set of vertices, and $V = V_0 \sqcup V_1$ is a partition: player $j \in \{0, 1\}$ *owns* the vertices of $V_j$;
- $E \subseteq V \times V$ is a set of edges, and each vertex $v$ has at least one successor $w$ with $(v, w) \in E$;
- $\Omega : V \to \{0, 1, \ldots, d\}$ assigns a *priority* to each vertex.

We write $n = |V|$ and $m = |E|$. Player 0 is also called Even, and player 1 is called Odd. A *play* from $v_0$ is an infinite sequence $\pi = v_0 v_1 v_2 \ldots$ with $(v_k, v_{k+1}) \in E$ for all $k \ge 0$: at each step, the owner of the current vertex picks a successor. Let $\mathrm{Inf}(\pi) = \{ q : \Omega(v_k) = q \text{ for infinitely many } k \}$. This set is not empty because $\Omega$ has finitely many values. Player 0 wins $\pi$ when $\max \mathrm{Inf}(\pi)$ is even, and player 1 wins $\pi$ when it is odd.

This is the *max-parity* convention. Many papers use the *min-parity* convention, where the least priority seen infinitely often decides. The two are equivalent: replace each priority $q$ by $d' - q$ for an even $d' \ge d$.

### Strategies and winning regions

A *strategy* of player $j$ maps each finite play prefix $v_0 \ldots v_k$ with $v_k \in V_j$ to a successor of $v_k$. A strategy is *positional* (or memoryless) when it depends only on the last vertex, so that it is a map $\sigma : V_j \to V$ with $(v, \sigma(v)) \in E$. A play *follows* $\sigma$ when each move of player $j$ is the one that $\sigma$ gives. Player $j$ *wins from* $v$ when she has a strategy $\sigma$ such that each play from $v$ that follows $\sigma$ is won by player $j$, whatever the opponent does. The *winning region* $W_j$ is the set of vertices from which player $j$ wins.

The *attractor* $\mathrm{Attr}_j(U)$ of a set $U$ is the least set $A \supseteq U$ that contains each vertex of $V_j$ with a successor in $A$ and each vertex of $V_{1-j}$ with all successors in $A$. From $A$, player $j$ can force the token into $U$. A *trap* for player $j$ is a set $T$ such that each vertex of $T \cap V_j$ has all its successors in $T$, and each vertex of $T \cap V_{1-j}$ has a successor in $T$. The complement of $\mathrm{Attr}_j(U)$ is a trap for player $j$, and $\mathrm{Attr}_j(U)$ is computed in $O(n + m)$ time, as shown on the [Zielonka's algorithm](/zielonka-algorithm/) page.

### Positional determinacy

**Theorem (Emerson and Jutla 1991, Mostowski 1991).** Let $G$ be a parity game with a finite set of vertices in which each vertex has a successor. Then $V = W_0 \sqcup W_1$, and for each $j$ there is one positional strategy $\sigma_j$ of player $j$ that wins from every vertex of $W_j$, against all strategies of the opponent.

*Proof (Zielonka's argument).* We prove a stronger claim by strong induction on $n$: $V$ is the union of two disjoint sets $W_0$, $W_1$, and for each $j$ there is a positional $\sigma_j$ such that each play that starts in $W_j$ and follows $\sigma_j$ stays in $W_j$ and is won by player $j$. Then $W_j$ is the winning region, since one vertex cannot be won by both players: the unique play that follows a winning strategy of each would be won by both.

For $n = 0$ there is nothing to prove. Let $n \ge 1$, let $p$ be the largest priority, $i = p \bmod 2$, $U = \Omega^{-1}(p)$ and $A = \mathrm{Attr}_i(U)$. The set $V \setminus A$ is a trap for player $i$, so it holds a subgame $G'$ with fewer vertices, and the claim holds for $G'$ with regions $W'_0$, $W'_1$ and strategies $\sigma'_0$, $\sigma'_1$. Two facts are used below. (a) Whether a play is won does not change when a finite prefix changes. (b) A play that follows the attractor strategy from $A$ reaches $U$ in at most $|A|$ moves.

If $W'_{1-i} = \emptyset$, player $i$ plays $\sigma'_i$ on $V \setminus A$, the attractor strategy on $A \setminus U$, and any move on $U$. A play that visits $A$ infinitely often visits $U$ infinitely often by (b), so $\max \mathrm{Inf} = p$, which has the parity $i$. A play that visits $A$ finitely often stays in $V \setminus A$ from some point, where it follows $\sigma'_i$ and is won by player $i$, so by (a) player $i$ wins it. So $W_i = V$ and $W_{1-i} = \emptyset$.

If $W'_{1-i} \neq \emptyset$, the opponent $1-i$ wins from $W'_{1-i}$ in $G$ with $\sigma'_{1-i}$, because player $i$ cannot leave the trap $V \setminus A$, and player $i$ cannot leave $W'_{1-i}$ inside $G'$. Let $B = \mathrm{Attr}_{1-i}(W'_{1-i}) \neq \emptyset$. Player $1-i$ wins from $B$ by the attractor strategy, then $\sigma'_{1-i}$, and (a). The set $V \setminus B$ is a trap for player $1-i$ and holds a smaller subgame $G''$, with regions $W''_0$, $W''_1$ by the induction hypothesis. Player $i$ wins from $W''_i$ in $G$ with $\sigma''_i$, because player $1-i$ cannot leave $V \setminus B$. Player $1-i$ wins from $W''_{1-i} \cup B$: she plays $\sigma''_{1-i}$ until player $i$ moves into $B$, if ever, and then the strategy of $B$. So $W_i = W''_i$ and $W_{1-i} = W''_{1-i} \cup B$. $\blacksquare$

The full proof, with each trap and strategy step written out, is the correctness proof of [Zielonka's algorithm](/zielonka-algorithm/), which turns this induction into an algorithm. Positional determinacy also holds for parity games on infinite graphs with finitely many priorities; Zielonka's paper proves that case by transfinite induction.

### The complexity of deciding the winner

The decision problem asks: given $G$ and a vertex $v$, is $v \in W_0$?

- **In NP ∩ co-NP.** A certificate for $v \in W_0$ is a positional strategy $\sigma_0$, which has polynomial size by the theorem. To check it, keep only the edges of $\sigma_0$ at the vertices of player 0. Player 0 wins from $v$ with $\sigma_0$ if and only if no cycle reachable from $v$ in this graph has an odd largest priority. For each odd $q$, compute the [strongly connected components](/strongly-connected-components/) of the subgraph of vertices with priority at most $q$; a reachable component with a cycle and a vertex of priority $q$ is a bad cycle. This takes $O(d (n + m))$ time. By symmetry, $v \in W_1$ has a certificate too, and $W_1 = V \setminus W_0$ by the theorem. Emerson, Jutla and Sistla gave this bound for the mu-calculus in 1993.
- **In UP ∩ co-UP.** Jurdziński (1998) showed that the problem has certificates that are unique, by a reduction to discounted payoff games.
- **In quasi-polynomial time.** Calude, Jain, Khoussainov, Li and Stephan (2017) solved parity games in time $n^{O(\log d)}$, and in polynomial time when $d \le \log n$. The [parity game solving](/parity-game-solving/) page lists this and the other algorithms.
- **Open.** It is not known whether parity games can be solved in polynomial time.

## Examples and non-examples

**A small game.** Player 0 owns $u$; player 1 owns $v$, $w$ and $x$.

| vertex | owner | priority | successors |
|---|---|---|---|
| u | 0 | 2 | v, w |
| v | 1 | 1 | u, x |
| w | 1 | 0 | u |
| x | 1 | 3 | x, w |

From $x$, player 1 takes the self-loop forever, so the play has $\mathrm{Inf} = \{3\}$ and player 1 wins. From $v$, player 1 moves to $x$ and wins. From $u$, player 0 moves to $w$, which must go back to $u$, so the play is $(u w)^\omega$ with $\mathrm{Inf} = \{0, 2\}$, and player 0 wins. So $W_0 = \{u, w\}$ and $W_1 = \{v, x\}$, with the positional strategies $\sigma_0(u) = w$ and $\sigma_1(v) = \sigma_1(x) = x$. If player 0 moved from $u$ to $v$, she would lose: the move matters, not only the priorities.

**A Büchi game.** A game with priorities in $\{1, 2\}$ only is a Büchi game: player 0 wins when she visits the vertices of priority 2 infinitely often. A game with priorities in $\{0, 1\}$ is a co-Büchi game. These are the special cases with $d = 2$, and both are solved in $O(n m)$ time by a loop of attractors.

**A larger example.** The six-vertex game on the [Zielonka's algorithm](/zielonka-algorithm/) page needs two levels of recursion and both cases of the proof above.

**Non-example: a vertex without successors.** If $v$ has no successor, a play from $v$ cannot be infinite, and the definition does not apply. A common fix makes $v$ a loss for its owner by a self-loop with a priority of the other parity.

**Non-example: a Muller condition needs memory.** Let player 0 own a vertex $c$ with edges to $a$ and $b$, and let $a$ and $b$ each have the one edge back to $c$. Say player 0 wins when both $a$ and $b$ occur infinitely often. This is a Muller condition, not a parity condition. Each positional strategy of player 0 fixes the same move at $c$, so it visits only one of $a$ and $b$ after the first move, and loses. The strategy that alternates wins. So the positional determinacy theorem does not extend to all conditions on $\mathrm{Inf}$. Muller games are determined with finite memory instead.

**Non-example: one play does not decide the region.** The play $u v u v \ldots$ in the small game has $\mathrm{Inf} = \{1, 2\}$ and is won by player 0. This does not make $v$ a vertex of $W_0$, because player 1 has another move at $v$.

## Related definitions

- [Parity game solving](/parity-game-solving/) is the computational problem on parity games, and lists the algorithms: [Zielonka's algorithm](/zielonka-algorithm/), small progress measures, strategy improvement and the quasi-polynomial algorithms.
- The [modal mu-calculus](/modal-mu-calculus/) model checking problem reduces to parity game solving in polynomial time, and back. The priority of a vertex comes from the alternation depth of the fixed point that it unfolds; see [mu-calculus model checking](/mu-calculus-model-checking/) and [fixed point](/fixed-point/).
- A [Büchi automaton](/buchi-automaton/) accepts with a condition that is the parity condition with two priorities. Parity automata are the standard target of determinization of Büchi automata.
- [Stochastic games](/stochastic-game/) add random vertices. Mean payoff games and discounted payoff games, the targets of Jurdziński's reduction, put weights on edges instead of priorities on vertices.
- [Linear temporal logic](/linear-temporal-logic/) synthesis builds a parity game from a deterministic parity automaton for the specification.

## References
