---
title: Conflict-directed backjumping never skips a solution
proves: [correctness]
status: full
---

We use the pseudocode of the page with the fixed order $x_1, \ldots, x_n$. For a set $S \subseteq \{1, \ldots, n\}$, write $\sigma|_S$ for the current assignment restricted to the variables $x_k$ with $k \in S$. A solution $\tau$ *agrees with* $\sigma$ on $S$ if $\tau(x_k) = \sigma(x_k)$ for every $k \in S$. A value $v$ of $x_k$ is *refuted* if line L9 took it out of $CD[k]$ since the last time line L13 (or line L1 for $k = 1$) reset $CD[k]$.

We first treat the mode that stops at the first solution. In it, "solution" in the invariant means any solution.

**Lemma 1 (shape of the state).** At every time, with $i$ the current level:

1. $CS[k] \subseteq \{1, \ldots, k - 1\}$ for each $k \le i$;
2. for each $k < i$, the current value $\sigma(x_k)$ has been refuted (taken out of $CD[k]$) and it is consistent with $\sigma(x_1), \ldots, \sigma(x_{k-1})$;
3. the levels $k \le i$ have not changed their $\sigma(x_k)$ since level $i$ was last entered from above or jumped to.

*Proof.* Part 1: line L14 adds $h < i$, and line L6 adds the indices of $CS[i] \setminus \{h\}$, which are smaller than $h = \max CS[i]$. Part 2: the search moves from level $k$ to $k + 1$ only at line L13, after the value of $x_k$ passed line L10, so it is consistent with the earlier values. Part 3: line L9 changes only $\sigma(x_i)$, and a jump goes to a level $h < i$ and does not change any value at levels at most $h$. $\square$

**Lemma 2 (invariant).** Let $i$ be the current level at the start of an iteration of line L2. For every level $k \le i$ and every refuted value $v$ of $x_k$, except the current value $\sigma(x_k)$ when $k < i$: no solution agrees with $\sigma$ on $CS[k]$ and gives $v$ to $x_k$.

By part 1 of Lemma 1, the condition only involves the values of variables before $x_k$, and by part 3 those values do not change while level $k$ stays active. At the current level the statement covers every refuted value, including the current one.

*Proof.* By induction on the iterations. At the start no value is refuted.

*Line L9 followed by L13.* The new level $i + 1$ has no refuted values. The value $a$ of $x_i$ is now the current value of a level below the current one, so the statement does not claim anything for it. Nothing else changes.

*Line L9 followed by L14.* The value $a$ violates $C_{hi}$ with $\sigma(x_h)$, so no solution gives $\sigma(x_h)$ to $x_h$ and $a$ to $x_i$. After $h$ is added to $CS[i]$, a solution that agrees with $\sigma$ on $CS[i]$ gives $\sigma(x_h)$ to $x_h$, so it does not give $a$ to $x_i$. For the other refuted values of $x_i$, the set $CS[i]$ grew, and agreeing on a larger set is a stronger condition, so the statement stays true. Levels $k < i$ do not change.

*A dead end, lines L3 to L7.* Every value of $D(x_i)$ is refuted, since $CD[i]$ is empty. By the invariant at level $i$, for each $v \in D(x_i)$ no solution agrees with $\sigma$ on $CS[i]$ and gives $v$ to $x_i$. Every solution gives some value of $D(x_i)$ to $x_i$, so no solution agrees with $\sigma$ on $CS[i]$. Let $h = \max CS[i]$ and $S = CS[i] \setminus \{h\}$. Then no solution agrees with $\sigma$ on $S$ and gives $\sigma(x_h)$ to $x_h$. After line L6, $S \subseteq CS[h]$, so no solution agrees with $\sigma$ on $CS[h]$ and gives $\sigma(x_h)$ to $x_h$. This is the statement for the value $\sigma(x_h)$, which is refuted by part 2 of Lemma 1 and which is now the value at the current level $h$. For the other refuted values of $x_h$ the statement held before (they are not current) and $CS[h]$ only grew. Levels $k < h$ do not change, and the levels above $h$ are no longer active. $\square$

**Theorem 1 (soundness).** An assignment returned at line L12 is a solution.

*Proof.* At line L12 the value $a$ of $x_n$ passed line L10, so it is consistent with the earlier values, and by part 2 of Lemma 1 each earlier value is consistent with the values before it. So every constraint holds. $\square$

**Theorem 2 (completeness, no solution is skipped).** If a solution exists, CBJ returns one. It returns failure only if there is no solution.

*Proof.* Line L4 returns failure at a dead end with $CS[i] = \emptyset$. By the dead-end case of Lemma 2, no solution agrees with $\sigma$ on the empty set, so there is no solution at all.

It remains to show that the loop ends. Each iteration either takes a value at line L9 or jumps at line L7. Each value taken creates a node: a partial assignment $\sigma(x_1), \ldots, \sigma(x_i)$. No node is created twice: at a level, a value is taken at most once between two resets, and a reset of level $i$ happens only right after a new node at level $i - 1$ is created and passes line L10. By induction on $i$, each assignment to $x_1, \ldots, x_i$ occurs at most once. So there are at most $d + d^2 + \cdots + d^n$ nodes. Each jump goes to a smaller level, and the level grows only at line L13, once per node. So the number of jumps is at most the number of nodes. The loop ends after a finite number of iterations, at line L4 or line L12. $\square$

**Theorem 3 (comparison with backtracking).** With the same order, every node of CBJ is a node of chronological backtracking, CBJ meets the nodes in the same depth-first order, and it returns the same first solution.

*Proof.* A node of CBJ at level $i$ extends an assignment $\sigma(x_1), \ldots, \sigma(x_{i-1})$ that is consistent by part 2 of Lemma 1, and chronological backtracking tries every value of $x_i$ below every consistent assignment to $x_1, \ldots, x_{i-1}$ that it reaches, and it reaches all of them. So every node of CBJ is a node of backtracking.

Order: line L9 takes the values of each level in the domain order, and a jump to $x_h$ is followed by the next value of $x_h$ in that order. In the depth-first order of the tree of all partial assignments, the next value of $x_h$ comes after every node below the current value of $x_h$. So each move of CBJ goes forward in this order, and CBJ meets its nodes in the order of backtracking. The jump skips only nodes below the current value of $x_h$ in which the variables of $CS[i]$ keep their values. By the dead-end case of Lemma 2, no solution lies there. So every solution that backtracking meets before the first one that CBJ returns would be in a skipped part, which is not possible, and the first solutions are the same. $\square$

**All solutions.** In the all-solutions mode, line L12 records $\sigma$ and sets $CS[n] = \{1, \ldots, n - 1\}$, and the search goes on. Replace "no solution" in Lemma 2 by "no solution that is not yet recorded". The case of line L12 is new: the recorded value $a$ of $x_n$ is refuted, and every solution that agrees with $\sigma$ on $\{1, \ldots, n - 1\}$ and gives $a$ to $x_n$ is $\sigma$ itself, which is now recorded. The other cases are proved in the same way. At the end, line L4 finds that every solution is recorded. No solution is recorded twice, because no node is created twice. $\blacksquare$
