---
title: Under the granular lock protocol, implicit locks on the leaves never conflict, so strict 2PL with intention locks is serializable
proves: [correctness]
status: full
---

**Setting.** The items form a rooted tree. Reads and writes act on the leaves. Each transaction holds at most one mode on each node, from $M = \{IS, IX, S, SIX, X\}$, with the compatibility matrix of the page. The order on $M$ is IS < IX < SIX < X and IS < S < SIX, and $m \ge n$ means that $m$ is $n$ or above it in this order. For a mode $m$, let $\mathrm{need}(m) = IS$ if $m \in \{IS, S\}$ and $\mathrm{need}(m) = IX$ if $m \in \{IX, SIX, X\}$.

The matrix has two facts that the proof uses. Both can be read off the table:

- **(F1)** X is compatible with no mode.
- **(F2)** Each mode $m \ge IX$, that is IX, SIX or X, is compatible with none of S, SIX and X.

The tests also check that the matrix is symmetric, that it follows from the meanings of the modes, and that the supremum $\sup(a, b)$ is the least mode above $a$ and $b$, with $\mathrm{compat}(\sup(a, b), m)$ exactly when $\mathrm{compat}(a, m)$ and $\mathrm{compat}(b, m)$.

**Definitions.** $T$ *implicitly holds X* on a leaf $\ell$ if $T$ holds X on some node on the path from the root to $\ell$ (the leaf included). $T$ *implicitly holds S* on $\ell$ if it holds S, SIX or X on some node of that path. A read of $\ell$ by $T$ needs an implicit S lock, and a write needs an implicit X lock; the driver checks this before each action.

**Lemma 1 (safety of the table).** At every moment, if two different transactions hold modes $m_1$ and $m_2$ on the same node, then $m_1$ and $m_2$ are compatible.

*Proof.* Line L5 grants $m'$ to $T$ on $v$ only when $m'$ is compatible with the mode of each other holder of $v$. Release steps only remove locks. So the claim holds after each step, by induction. A conversion replaces the mode of $T$ by $m' = \sup(\text{old}, m)$, and the test is made with $m'$. $\square$

**Lemma 2 (parent rule).** At every moment, if $T$ holds mode $m$ on a node $v$ that is not the root, then $T$ holds a mode $\ge \mathrm{need}(m)$ on the parent of $v$. Hence, by induction up the path, $T$ holds a mode $\ge \mathrm{need}(m)$ on every proper ancestor of $v$.

*Proof.* Look at the steps that could break the claim.

- A grant of $m'$ on $v$ (line L5). Line L1 checked that the mode of $T$ on the parent is at least $\mathrm{need}(m)$, where $m$ is the mode that $T$ asked for. If the grant is a conversion, $m' = \sup(m_{old}, m)$, and $\mathrm{need}(m')$ is the larger of $\mathrm{need}(m_{old})$ and $\mathrm{need}(m)$, since $\mathrm{need}$ is monotone and $\{IS, IX\}$ is a chain. The parent mode was at least $\mathrm{need}(m_{old})$ by the claim before the step, and at least $\mathrm{need}(m)$ by line L1, so it is at least $\mathrm{need}(m')$.
- A grant on the parent $p$ of $v$. This replaces the mode of $T$ on $p$ by a supremum, which is at least the old mode, so the claim for $v$ still holds.
- A release of the lock of $T$ on the parent $p$. Line L8 refuses it while $T$ holds a lock on a child of $p$, and release at the end goes deepest first, so by the time $p$ is released, $T$ holds nothing on its children. $\square$

For the second sentence: $\mathrm{need}(m') = \mathrm{need}(m)$ or IS when $m' \ge \mathrm{need}(m)$, because $\mathrm{need}(m') = IX$ exactly when $m' \ge IX$. Applying the first sentence to the parent, then to its parent, and so on, gives a mode $\ge \mathrm{need}(m)$ on each ancestor.

**Theorem 1 (implicit locks never conflict).** At every moment, if $T$ implicitly holds X on a leaf $\ell$, then no other transaction $U$ implicitly holds S or X on $\ell$.

*Proof.* Let $T$ hold X on the node $a$ and $U$ hold $m_U \in \{S, SIX, X\}$ on the node $b$, where $a$ and $b$ are on the path from the root to $\ell$. The nodes of one root path are ordered by depth, so there are three cases.

- $a = b$. Then $T$ holds X and $U$ holds $m_U$ on the same node, which contradicts Lemma 1 by (F1).
- $a$ is a proper ancestor of $b$. By Lemma 2, $U$ holds a mode $\ge \mathrm{need}(m_U) \ge IS$ on $a$, so it holds some mode on $a$, while $T$ holds X on $a$. This contradicts Lemma 1 by (F1).
- $b$ is a proper ancestor of $a$. By Lemma 2, $T$ holds a mode $\ge \mathrm{need}(X) = IX$ on $b$, while $U$ holds S, SIX or X on $b$. This contradicts Lemma 1 by (F2). $\square$

**Theorem 2 (serializability and strictness).** Let each transaction follow the protocol (lines L1 to L8) and release all its locks only at its commit or abort (line L9). Then every output schedule is strict, and its committed projection is conflict serializable, in commit order.

*Proof.* Let $p_i(\ell)$ come before $q_j(\ell)$, $i \ne j$, on the same leaf, with at least one write. When $p_i(\ell)$ runs, $T_i$ implicitly holds S or X on $\ell$, through a lock on some node of the root path; it holds this lock to its end, since locks are released only at line L9, and conversions only make modes stronger, so the implicit lock stays. In the same way, when $q_j(\ell)$ runs, $T_j$ implicitly holds S or X on $\ell$. One of the two is an implicit X, because one action is a write. By Theorem 1, the two implicit locks are not held at the same time. $T_i$ holds its lock from before $p_i(\ell)$ to its end, and $T_j$ holds its lock at the moment of $q_j(\ell)$, which is after $p_i(\ell)$. So $T_i$ ended before $q_j(\ell)$.

Every action that follows a write of another transaction on the same leaf therefore follows the end of that transaction, so the schedule is strict. Also every pair of conflicting actions of committed transactions $T_i$ and $T_j$, with the action of $T_i$ first, has $c_i$ before the action of $T_j$, and so before $c_j$. So all conflicting pairs are in commit order, and the committed projection is conflict equivalent to the serial schedule in commit order. $\square$

The argument does not need the lock point of the [two-phase locking theorem](/two-phase-locking-theorem/), because locks are held to the end; with locks released earlier (but still two-phase and from the leaves up) the same lemmas give the general case through that theorem, applied to the implicit locks on the leaves.

**Deadlock.** The protocol does not prevent deadlocks. A waiting transaction has a request $(v, m')$ that is not compatible with the lock of some other holder of $v$, and the wait-for graph has an edge to each such holder. If every unfinished transaction waits, every node of the graph has an edge out of it, and every edge goes to an unfinished transaction, so the graph has a cycle. The driver of the tests then aborts the largest transaction id on the cycle and releases its locks.

The tests check Lemma 2 and Theorem 1 after every step of the driver, on all interleavings of four pairs of programs (a scan and a row write, a table update and a row read, two table rewrites in opposite orders, a read then write against a read) and on 250 random interleavings of three or six transactions on a database with three tables. On each output they check Theorem 2 with the helper `dbsched`: strictness, and conflict equivalence with the serial schedule in commit order, and for up to three transactions also against every serial order by brute force.
