---
title: The tree locking protocol gives conflict serializable schedules and has no deadlocks
proves: [correctness]
status: full
---

**Setting.** The items are the nodes of a finite rooted tree. A *history* $H$ is a finite sequence of events $\mathrm{lock}(T, x)$ and $\mathrm{unlock}(T, x)$ on the nodes, and $T$ *holds* $x$ from its lock of $x$ to its unlock of $x$, or to the end of $H$. The history is *legal* if:

- **(A1)** each transaction locks each node at most once (line L1);
- **(A2)** each lock by $T$, other than the first lock of $T$, is of a node whose parent $T$ holds at that moment (line L2);
- **(A3)** no two transactions hold the same node at the same moment (lines L3 and L4), and a transaction unlocks only a node that it holds (line L5).

Let $N_T$ be the set of nodes that $T$ locks in $H$, and $F(T)$ the node of its first lock. Define the relation $\rho_H$ by $T \mathrel{\rho_H} U$ when $T \ne U$, both lock some node $x$, and $T$ locks $x$ before $U$ does.

**Lemma 1 (the locked nodes form a subtree).** In a legal history, every node of $N_T$ other than $F(T)$ has its parent in $N_T$, locked earlier. So every node of $N_T$ is a descendant of $F(T)$ (or $F(T)$ itself), and the path from $F(T)$ to it lies in $N_T$, locked from the top down.

*Proof.* By (A2), when $T$ locks $x \ne F(T)$ it holds the parent of $x$, which it locked earlier. Follow parents from $x$: the lock times go down strictly, so the walk stops, and it can stop only at $F(T)$. $\square$

**Theorem 1 (the lock order has no cycle).** For every legal history $H$, the relation $\rho_H$ has no cycle.

*Proof.* By induction on the number of nodes of the tree.

*Base.* If the tree is one node $r$, then each transaction locks only $r$, at most once, and $T \mathrel{\rho_H} U$ means that the lock of $r$ by $T$ comes first. This is a strict total order on the transactions that lock $r$, so it has no cycle.

*Step.* Let $r$ be the root, $c_1, \dots, c_k$ its children and $S_1, \dots, S_k$ their subtrees, each with fewer nodes than the tree. Let $R$ be the set of transactions that lock $r$. The root has no parent, so by (A2) a lock of $r$ is the first lock of its transaction, and $F(T) = r$ for each $T \in R$. Number $R$ as $R_1, \dots, R_m$ in the order of their locks of $r$. By (A1) and (A3), the times in which they hold $r$ are disjoint intervals, in the same order.

Let $H_i$ be $H$ restricted to the events on the nodes of $S_i$. It is a legal history on the tree $S_i$. (A1) and (A3) carry over. For (A2), let $T$ lock $x$ in $H_i$, not as its first lock in $H_i$. If $x \ne c_i$, the lock is not the first lock of $T$ in $H$ either, so $T$ holds the parent of $x$, which is in $S_i$. The case $x = c_i$ does not happen: by Lemma 1 the earlier node $y \in S_i$ that $T$ locked has the path from $F(T)$ to $y$ in $N_T$, locked from the top down. If $F(T) = r$, the path goes through $c_i$, so $c_i$ was locked before $y$. If $F(T) \ne r$, then $F(T)$ is in $S_i$ and $c_i$ is a descendant of $F(T)$, so $F(T) = c_i$, which is the first lock of $T$. Both contradict the choice of $y$. The relation $\rho_{H_i}$ is $\rho_H$ restricted to pairs that both lock a node of $S_i$, with the order on that node. So $\rho_H$ is the union of the pairs $R_a \mathrel{\rho_H} R_b$ for $a < b$, which come from $r$, and of the relations $\rho_{H_1}, \dots, \rho_{H_k}$. By induction, no $\rho_{H_i}$ has a cycle.

*Claim A.* If $R_a$ and $R_b$ both lock $c_i$, then $R_a$ locks $c_i$ first exactly when $a < b$. Indeed, $R_a$ locks $c_i$ while it holds $r$ (A2), so inside its interval on $r$, and the same holds for $R_b$. The intervals are disjoint and in the order of the indices.

*Claim B.* If $R_a \ne R_b$ are joined by a path $R_a = U_0 \mathrel{\rho_{H_i}} U_1 \mathrel{\rho_{H_i}} \cdots \mathrel{\rho_{H_i}} U_j = R_b$ with $j \ge 1$, all of its edges in the same $\rho_{H_i}$, then $a < b$. Indeed, $R_a$ and $R_b$ lock nodes of $S_i$, so by Lemma 1, with $F = r$, both lock $c_i$. If $b < a$, then $R_b$ locks $c_i$ first by Claim A, so $R_b \mathrel{\rho_{H_i}} R_a$, and with the path this is a cycle of $\rho_{H_i}$, which cannot be.

Now let $C$ be a cycle of $\rho_H$. A transaction $T \notin R$ does not lock $r$, so by Lemma 1 all of $N_T$ lies in the subtree of $F(T)$, inside one $S_i$. An edge between two transactions outside $R$ comes from a common node, which is not $r$, so the two lie in the same $S_i$, and the edge is in $\rho_{H_i}$.

- If $C$ has no member of $R$, all its members lie in one $S_i$, and $C$ is a cycle of $\rho_{H_i}$. This cannot be.
- Otherwise cut $C$ at its members of $R$ into segments from $R_a$ to $R_b$ whose inner members are not in $R$. A segment of one edge comes from a node that is $r$, so $a < b$, or that is in some $S_i$, so $a < b$ by Claim B. A segment with inner members has all of them in one $S_i$, and its first and last edges come from nodes in that $S_i$ too, so it is a path in $\rho_{H_i}$. If $a = b$ (the only member of $R$ on $C$), this path is a cycle of $\rho_{H_i}$, which cannot be; else $a < b$ by Claim B. So the index goes up strictly along every segment, and it cannot come back to its start. $\square$

**Corollary 1 (serializability).** Under the protocol, every schedule, and every prefix of one, is conflict serializable, and every topological order of $\rho_H$ is an equivalent serial order.

*Proof.* A transaction reads or writes a node only while it holds the lock on it. If $p_i(x)$ comes before a conflicting $q_j(x)$, then $T_i$ holds $x$ at $p_i(x)$ and $T_j$ at $q_j(x)$. By (A3) the two intervals are disjoint, so the one of $T_i$ comes first, and $T_i \mathrel{\rho_H} T_j$. So every edge of the conflict graph is in $\rho_H$, the conflict graph has no cycle by Theorem 1, and the [serializability theorem](/serializability-theorem/) gives the claim. The committed projection has a subgraph of this conflict graph. $\square$

**Theorem 2 (no deadlock).** In every state that the protocol reaches, the wait-for graph has no cycle.

*Proof.* Let $T_1, \dots, T_k$, $k \ge 2$, be a cycle: each $T_i$ waits for the node $x_i$, which $T_{i+1}$ holds (indices mod $k$). Each $T_i$ holds a lock, since $T_{i-1}$ waits for it, so its request is not its first lock. The request passed lines L1 and L2, so $T_i$ never locked $x_i$, and it holds $p_i$, the parent of $x_i$. A waiting transaction takes no step, so it still holds $p_i$. Let $H$ be the history so far. Extend it as follows.

1. Each $T_i$ unlocks every node that it holds except $p_i$. Now $x_i$ is held only if $x_i = p_{i+1}$, by $T_{i+1}$.
2. It is not true that $x_i = p_{i+1}$ for all $i$, since then $\mathrm{depth}(x_{i+1}) = \mathrm{depth}(x_i) + 1$ for all $i$, and the sum around the cycle gives $k = 0$. Choose $j$ with $x_j \ne p_{j+1}$, so $x_j$ is free.
3. For $i = j, j-1, \dots, j+1$ (going back around the cycle, $k$ turns): $T_i$ locks $x_i$, then unlocks $x_i$ and $p_i$. At the turn of $T_i$ with $i \ne j$, the node $x_i$ is free, because $T_{i+1}$, the only possible holder, had its turn before and unlocked $p_{i+1}$.

Every lock of the extension is legal: $T_i$ holds $p_i$, has never locked $x_i$, and $x_i$ is free. So the extended history $H'$ is legal. In $H'$, $T_{i+1}$ locked $x_i$ in $H$, before $T_i$ locks it in the extension, so $T_{i+1} \mathrel{\rho_{H'}} T_i$ for every $i$. This is a cycle of $\rho_{H'}$, which contradicts Theorem 1. $\square$

A transaction that waits for its first lock holds nothing, so nobody waits for it, and it is on no cycle. So with no deadlock, the driver of the tests never has to abort a transaction.

**Lemma 2 (the planner follows the protocol).** The steps that `plan` builds satisfy (A1) and (A2), every access happens while the transaction holds its node, and no lock is left at the commit.

*Proof.* Let $U$ be the union of the paths from the top node $t$ (line L6, the lowest common ancestor of the accessed nodes) to each accessed node. The planner locks only nodes of $U$, each at most once, and always the whole path from $t$ to the next accessed node, from the top down (line L7). So the locked nodes are closed under parents inside $U$, and on a path the nodes that are still to be locked come after the ones that are locked. When it locks $u \ne t$, the parent of $u$ is in $U$ and was locked. It was not unlocked, because line L8 unlocks a node only when every child of it in $U$ is locked, and $u$ was not. The first lock is $t$. A node that is accessed now or later is not unlocked, because line L8 checks the accesses from the current one on. After the last access, each held node has no later access and all its children in $U$ are locked, since every node of $U$ lies on the path to an accessed node and all of them were locked. So line L8 unlocks all of them. $\square$

**What the protocol does not give.** A transaction can unlock a node that it wrote before it commits, so another transaction can read the value and commit first. The example of the page gives $w_1(d)\, r_2(b)\, r_2(d)\, c_2\, w_1(e)\, c_1$, which is conflict serializable but not [recoverable](/recoverable-schedule/). The protocol is also not two-phase: in the same example $T_1$ unlocks $d$ before it locks $e$.

The tests check Lemma 2 on fixed plans; the state checks (the locked nodes of each transaction form a subtree with one top, and a waiter holds the parent of the node it waits for) after every step; Theorem 1 on the lock log; the inclusion of the conflict graph in $\rho_H$; and Corollary 1 with the helper `dbsched`, against the serial schedule in a topological order of $\rho_H$, and by brute force for up to three transactions. They run all interleavings of two pairs of programs, 3000 random interleavings of two programs that write $d$ and $e$ in opposite orders, and 700 random interleavings of three or six transactions on a tree of 15 nodes. No run ever has a deadlock.
