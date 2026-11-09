---
title: Graph-based backjumping never skips a solution
proves: [correctness]
status: full
---

We use the pseudocode of the page with the fixed order $x_1, \ldots, x_n$, and the notation of the proof for [conflict-directed backjumping](/conflict-directed-backjumping/). For $S \subseteq \{1, \ldots, n\}$, a solution $\tau$ *agrees with* $\sigma$ on $S$ if $\tau(x_k) = \sigma(x_k)$ for all $k \in S$. A value $v$ of $x_k$ is *refuted* if line L9 took it out of $CD[k]$ since $CD[k]$ was last reset.

**Lemma 1 (shape of the state).** With $i$ the current level: (1) $J[k] \subseteq \{1, \ldots, k - 1\}$ for each $k \le i$; (2) for each $k < i$, the value $\sigma(x_k)$ is refuted and consistent with $\sigma(x_1), \ldots, \sigma(x_{k-1})$; (3) a jump to level $h$ changes no value at a level at most $h$.

*Proof.* (1) $P(k)$ holds only earlier variables, and line L6 adds the indices of $J[i] \setminus \{h\}$, which are smaller than $h = \max J[i]$. (2) The search goes from level $k$ to $k + 1$ only at line L12, after line L10 found $\sigma(x_k)$ consistent. (3) Line L7 only changes $i$. $\square$

**Lemma 2 (invariant).** At the start of each iteration, with $i$ the current level: for every $k \le i$ and every refuted value $v$ of $x_k$, except the current value $\sigma(x_k)$ when $k < i$, no solution agrees with $\sigma$ on $J[k]$ and gives $v$ to $x_k$. Also $P(k) \subseteq J[k]$ for each $k \le i$.

*Proof.* By induction on the iterations. At the start, nothing is refuted and $J[1] = \emptyset = P(1)$.

*Lines L9, L10 and L12.* The new level $i + 1$ has $J[i+1] = P(i+1)$ and no refuted values. The value of $x_i$ is now the current value of a level below the current one, so nothing is claimed for it.

*Lines L9 and L10, the check fails.* The value $a$ violates some constraint with an earlier $x_j$. A constraint between $x_j$ and $x_i$ is an edge of the constraint graph, so $j \in P(i) \subseteq J[i]$. A solution that agrees with $\sigma$ on $J[i]$ gives $\sigma(x_j)$ to $x_j$, so it does not give $a$ to $x_i$. The other refuted values of $x_i$ keep the property, since $J[i]$ did not change.

*In the all-solutions mode, line L11 records $\sigma$.* Read "no solution" as "no solution that is not yet recorded". The value $a$ of $x_n$ is refuted, and the only solution that agrees with $\sigma$ on $\{1, \ldots, n - 1\}$ and gives $a$ to $x_n$ is $\sigma$, which is now recorded. So setting $J[n] = \{1, \ldots, n - 1\}$ keeps the invariant, and it contains $P(n)$.

*A dead end, lines L3 to L7.* All values of $D(x_i)$ are refuted. By the invariant, for each $v \in D(x_i)$ no solution agrees with $\sigma$ on $J[i]$ and gives $v$ to $x_i$. So no solution agrees with $\sigma$ on $J[i]$. Let $h = \max J[i]$ and $S = J[i] \setminus \{h\}$. No solution agrees with $\sigma$ on $S$ and gives $\sigma(x_h)$ to $x_h$. After line L6, $S \subseteq J[h]$, so the statement holds for the value $\sigma(x_h)$, which is refuted by Lemma 1 and is now the value at the current level $h$. For the other refuted values of $x_h$ it held before, and $J[h]$ only grew. $P(h) \subseteq J[h]$ still holds. Levels below $h$ do not change. $\square$

**Theorem 1 (soundness).** Each assignment returned or recorded at line L11 is a solution.

*Proof.* The value of $x_n$ passed line L10, and by Lemma 1 every earlier value is consistent with the values before it. $\square$

**Theorem 2 (completeness).** GBJ returns failure only if no solution exists (in the all-solutions mode: only after every solution is recorded), and the loop ends.

*Proof.* Line L4 returns failure at a dead end with $J[i] = \emptyset$. By the dead-end case of Lemma 2, no solution (no unrecorded solution) agrees with $\sigma$ on the empty set, so none exists.

Each iteration takes a value at line L9 or jumps at line L7. Each value taken makes a node $\sigma(x_1), \ldots, \sigma(x_i)$. A level is reset only right after a new consistent node at the level above it, and at a level a value is taken at most once between resets, so by induction on $i$ no node is made twice, and there are at most $d + d^2 + \cdots + d^n$ nodes. Each jump lowers the level, and the level rises only at line L12, once per node, so there are at most as many jumps as nodes. $\square$

**Theorem 3 (comparison with backtracking).** With the same order, every node of GBJ is a node of chronological backtracking, GBJ meets them in the same depth-first order, and the solutions come in the same order.

*Proof.* Each node of GBJ extends a consistent assignment, by Lemma 1, so backtracking makes it too. A jump to $x_h$ is followed by the next value of $x_h$, which in depth-first order comes after every node below the current value of $x_h$. So GBJ only moves forward in the order of backtracking. The nodes it skips are below the current value of $x_h$ and keep the values of $J[i]$, so by Lemma 2 they hold no solution (no unrecorded solution). Hence both methods meet the same solutions in the same order. $\blacksquare$
