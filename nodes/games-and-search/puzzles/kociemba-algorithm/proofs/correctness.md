---
title: Kociemba's two-phase algorithm returns a solution of at most M moves, run to the end it returns a shortest one, and it terminates
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode of the page. The cube group is $G$, the set of the 18 face turns is $S$, and $A = \{U, U2, U', D, D2, D', R2, L2, F2, B2\}$. The set $G_1$ is the set of cubes with every corner twist 0, every edge flip 0 and the four middle-slice edges FR, FL, BL, BR in the four middle-slice positions. A sequence is *canonical* if no two neighbouring moves turn the same face, and two neighbouring moves of opposite faces come in the fixed order U before D, R before L, F before B. For a cube $c$ and a sequence $s$, $c \cdot s$ is the cube after the moves of $s$; $e$ is the solved cube.

**Lemma 1 ($G_1$ is closed under $A$).** If $x \in G_1$ and $m \in A$, then $x \cdot m \in G_1$ and $x \cdot m^{-1} \in G_1$.

*Proof.* For a move $m$ with corner permutation $\pi$ and corner twists $t_m$, the twist of $x \cdot m$ at position $i$ is the twist of $x$ at position $\pi(i)$ plus $t_m(i)$ modulo 3, and the same holds for edge flips modulo 2. A direct computation from the move definitions shows that every move of $A$ has all twists and all flips 0: U and D change none, and in a half turn such as R2 each moved corner gets the twists of two quarter turns, which add to 0 modulo 3 (for R, the twists 2 and 1 alternate along its 4-cycle), and each edge moved by F2 or B2 is flipped twice. So a cube with all twists and flips 0 keeps them. U and D keep each edge in its layer, and each half turn R2, L2, F2, B2 exchanges the two slice positions of its face, so slice edges stay in slice positions. The set $A$ is closed under inverses. $\square$

**Lemma 2 (the coordinates are well defined).** Each of twist, flip, slice (the set of positions that hold slice edges), and, on $G_1$, the corner permutation, the permutation of the eight U and D layer edges and the permutation of the four slice edges, has the following property: its value on $x \cdot m$ depends only on its value on $x$ and on the move $m$.

*Proof.* For a move $m$ with corner permutation $\pi$ and twists $t$, the twist of $x \cdot m$ at position $i$ is the twist of $x$ at position $\pi(i)$ plus $t(i)$ modulo 3. The twist coordinate holds all eight twists, because the eighth follows from the other seven (their sum is 0 modulo 3 on every cube reachable from $e$). The same holds for flips. The positions of the slice edges after $m$ are the images of their positions before $m$. On $G_1$, the moves of $A$ map U and D layer positions to U and D layer positions and slice positions to slice positions, so each of the three permutations after $m$ is the composition of the permutation before $m$ with a fixed permutation given by $m$. $\square$

By Lemma 2 each move table maps a coordinate value and a move to the next value, and a path of $k$ moves between two cubes gives a path of $k$ steps between their coordinate pairs. The pruning table for a pair of coordinates holds the exact distance, found by [breadth-first search](/breadth-first-search/), from the pair of the target in the graph of pairs.

**Lemma 3 (admissible bounds).** For every cube $x$, every sequence of moves of $S$ that takes $x$ into $G_1$ has at least $h_1(x)$ moves. For every $x \in G_1$, every sequence of moves of $A$ that takes $x$ to $e$ has at least $h_2(x)$ moves.

*Proof.* A cube is in $G_1$ exactly when its twist is 0, its flip is 0 and its slice value is that of $e$. A sequence of $k$ moves that takes $x$ into $G_1$ gives a path of $k$ steps from the (slice, twist) pair of $x$ to that of $e$, so $k$ is at least the table value; the same holds for (slice, flip), so $k \ge h_1(x)$, the larger of the two values. The case of $h_2$ is the same, with the pairs (corner permutation, slice permutation) and (layer edge permutation, slice permutation) and the moves of $A$, which keep a cube of $G_1$ in $G_1$ by Lemma 1. $\square$

**Lemma 4 (phase 1).** For a cube $c$ and $d \ge 0$, L5 lists exactly the canonical sequences $p$ with $|p| = d$, $c \cdot p \in G_1$, and $p$ empty or its last move not in $A$.

*Proof.* The depth-first search visits the canonical sequences of length $d$ as a tree of prefixes and at a leaf tests the three conditions. It cuts the subtree of a prefix $u$ with $\ell$ moves left only when $h_1(c \cdot u) > \ell$; by Lemma 3 no sequence of at most $\ell$ further moves takes $c \cdot u$ into $G_1$, so the cut subtree holds no sequence that passes the test. $\square$

**Lemma 5 (phase 2).** For $x \in G_1$ and $\ell \ge 0$, L8 returns a shortest sequence of moves of $A$ that takes $x$ to $e$ if that length is at most $\ell$, and none otherwise.

*Proof.* L8 is [IDA\*](/iterative-deepening-a-star/) with the bound $h_2$, which is admissible by Lemma 3, over the canonical sequences of moves of $A$. A shortest sequence can be made canonical without changing its length or its result: two neighbouring turns of one face would merge into one turn or none, which would give a shorter sequence, and two neighbouring turns of opposite faces commute. Iteration $b$ runs for $b = h_2(x), h_2(x) + 1, \dots, \ell$ and finds a solution of length at most $b$ if one exists, by the argument of Lemma 4. Since iteration $b - 1$ failed, the solution found in iteration $b$ has length exactly $b$, the shortest. If no iteration up to $\ell$ succeeds, no solution of length at most $\ell$ exists, and L8 returns none. For $\ell < 0$ L8 returns none. $\square$

**Lemma 6 (canonical split).** Let $s$ be a sequence of moves of $S$ with $c \cdot s = e$ and with no shorter such sequence. Then $s$ can be rewritten as a canonical sequence $s'$ of the same length with $c \cdot s' = e$. Let $p$ be the shortest prefix of $s'$ such that all later moves are in $A$, and let $q$ be the rest. Then $c \cdot p \in G_1$, $p$ is canonical, and $p$ is empty or its last move is not in $A$.

*Proof.* Neighbouring turns of one face cannot occur in $s$, because they merge into one turn or none. Sort each maximal block of neighbouring turns on one axis into the fixed order; such turns commute, so the result is unchanged, and the block cannot hold two turns of one face for the same reason. This gives $s'$. The cube $c \cdot p$ equals $q^{-1}$ applied to $e$, and $q^{-1}$ is a sequence of moves of $A$, so $c \cdot p \in G_1$ by Lemma 1. If $p$ were nonempty with its last move in $A$, a shorter prefix would have all later moves in $A$, which contradicts the choice of $p$. A prefix of a canonical sequence is canonical. $\square$

**Theorem 1 (validity).** If the call returns a sequence, the sequence takes $c$ to $e$ and has at most $M$ moves.

*Proof.* The value of best changes only at L9, to $p\,q$ with $c \cdot p = c'$ and $c' \cdot q = e$ by Lemma 5. Its length is $d + |q| \le d + \ell \le M$ by L7. $\square$

**Theorem 2 (first solution).** If $M \ge 30$, the call with first set returns a solution.

*Proof.* Every cube is at most 12 moves from $G_1$ and every cube of $G_1$ is at most 18 moves of $A$ from $e$; Reid proved both bounds, and Rokicki lists the distance counts of $G_1$ (see the page). Let $d_1$ be the length of a shortest sequence of moves of $S$ from $c$ into $G_1$, so $d_1 \le 12$. A shortest such sequence ends with a move not in $A$, unless it is empty: by Lemma 1 the last move could be dropped. Making it canonical as in Lemma 6 keeps its length and its end, and in the last block of moves on one axis no move is in $A$ (it would commute to the end and could be dropped), so the last move after sorting is not in $A$. By Lemma 4, L5 lists it when $d = d_1$, and no earlier value of $d$ lists any sequence. At that point best is none, so $\ell = M - d_1 \ge 18$ and L8 returns a sequence by Lemma 5. $\square$

**Theorem 3 (optimality).** Let $L$ be the length of a shortest solution of $c$, and $L \le M$. The call with first not set returns a solution of length $L$.

*Proof.* By Theorem 1 every value of best is a solution, so it has length at least $L$. Take $s'$, $p$ and $q$ as in Lemma 6, with $|s'| = L$. We show that the loop at $d = |p|$ ends with $|\text{best}| \le L$. The loop reaches $d = |p|$: L4 returns earlier only when $d \ge |\text{best}| \ge L \ge |p|$, which cannot happen for $d < |p|$. If at that point best already has length $L$, the claim holds. Otherwise L4 does not return, and by Lemma 4 the loop at L5 lists $p$. When it does, $\ell = (|\text{best}| - 1) - |p| \ge L - |p| = |q|$ if best is set, since then $|\text{best}| > L$, and $\ell = M - |p| \ge |q|$ if not. The sequence $q$ uses moves of $A$ and takes $c \cdot p$ to $e$, so by Lemma 5 L8 returns a sequence of length at most $|q|$, and best gets length at most $|p| + |q| = L$. Lengths of best only go down, so the returned value has length exactly $L$. $\square$

With $M = 30$ and the fact that every cube has a solution of at most 20 moves (God's number), Theorem 3 holds for every cube.

**Theorem 4 (termination).** Every call returns.

*Proof.* The loop of L3 runs at most $M + 1$ times. For each $d$, L5 visits at most $18^d$ sequences, a finite number, and L8 runs at most $\ell + 1 \le M + 1$ iterations, each over at most $10^{\ell}$ sequences. The table construction is a breadth-first search over finite sets. $\square$

**Theorem 5 (complexity).** Let $t$ be the total number of entries of the move and pruning tables, $a$ the number of moves of phase 1 and $b$ the bound reached in phase 2. Building the tables takes $O(t)$ time, with 18 moves per entry. The search for the first solution takes $O(18^a + 10^b)$ table lookups, and the extra memory is $O(t + a + b)$.

*Proof.* Each move table entry is computed once from a representative cube, in $O(1)$ time for a fixed cube size, and each breadth-first search for a pruning table looks at each pair once with at most 18 moves. In the search for the first solution, the iterations of phase 1 for $d = 0, \dots, a$ visit at most $\sum_{d \le a} 18^d = O(18^a)$ prefixes. By the proof of Theorem 2, the first sequence listed at $d = a$ gives a phase-2 call that succeeds, and its iterations visit at most $\sum_{k \le b} 10^k = O(10^b)$ prefixes. Each prefix costs $O(1)$ lookups. The recursion stacks hold at most $a$ and $b$ moves. With $a \le 12$ and $b \le 18$ these are constants for the 3 by 3 by 3 cube; the tables make the real counts far smaller. $\square$
