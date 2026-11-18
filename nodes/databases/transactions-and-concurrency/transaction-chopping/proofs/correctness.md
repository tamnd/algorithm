---
title: The SC-cycle test is sound, and FINEST-CHOPPING returns the finest chopping that passes it
proves: [correctness]
status: full
---

**Model.** The workload is $T_1, \ldots, T_n$. A chopping cuts each $T_i$ into contiguous pieces. An execution $E$ runs every piece as a transaction. Pieces that the system aborts are restarted until they commit, and a rollback statement of $T_i$ aborts $T_i$ in the piece that contains it. Let $CG_P(E)$ be the conflict graph of the committed pieces: an arc $p \to q$ when an access of $p$ comes before a conflicting access of $q$ in $E$. The concurrency control of the pieces makes $CG_P(E)$ acyclic. Let $CG_T(E)$ be the conflict graph of the committed whole transactions: an arc $T_a \to T_b$ ($a \ne b$) when an access of $T_a$ comes before a conflicting access of $T_b$. By the [serializability theorem](/serializability-theorem/), $E$ is conflict equivalent to a serial execution of the whole transactions if and only if $CG_T(E)$ is acyclic. The chopping graph $G$ and SC-cycles are as defined on the page. For a fixed $i$, let $H_i$ be the graph on the transactions $T_j$, $j \ne i$, with an edge when two of them have conflicting accesses; its components are the *components of the others*.

**Lemma 1 (rollback safety).** If the chopping is rollback-safe, then in every execution each transaction either commits all its pieces or commits none.

*Proof.* A rollback statement of $T_i$ lies in its first piece. If $T_i$ rolls back, it does so while the first piece runs, and that piece aborts; the later pieces never start, so no piece of $T_i$ commits. Otherwise each piece is restarted until it commits. $\square$

So the committed pieces form whole transactions, and $CG_T(E)$ is defined on them.

**Theorem 2 (Shasha et al.).** If the chopping is rollback-safe and $G$ has no SC-cycle, then $CG_T(E)$ is acyclic for every execution $E$.

*Proof.* Suppose $CG_T(E)$ has a cycle $T_{a_1} \to T_{a_2} \to \cdots \to T_{a_k} \to T_{a_1}$ with $k \ge 2$ distinct transactions. Indices are taken modulo $k$. The arc $T_{a_j} \to T_{a_{j+1}}$ comes from an access in a piece $p_j$ of $T_{a_j}$ that comes before a conflicting access in a piece $q_{j+1}$ of $T_{a_{j+1}}$. Then $p_j \to q_{j+1}$ is an arc of $CG_P(E)$, and $p_j$ and $q_{j+1}$ are joined by a C edge in $G$. In each transaction $T_{a_j}$ of the cycle, the arc in ends at $q_j$ and the arc out starts at $p_j$.

*Case 1: $q_j = p_j$ for every $j$.* Then $p_1 \to p_2 \to \cdots \to p_k \to p_1$ is a closed walk in $CG_P(E)$ through $k$ pieces of distinct transactions, so it is a cycle, and $CG_P(E)$ is not acyclic. This contradicts the model.

*Case 2: $q_j \ne p_j$ for some $j$.* Consider the closed walk in $G$ that goes $p_1, q_2$ by a C edge, then $q_2, p_2$ by an S edge if $q_2 \ne p_2$, then $p_2, q_3$ by a C edge, and so on, until it returns to $p_1$. The transactions $T_{a_j}$ are distinct, and inside one transaction the walk visits $q_j$ and $p_j$, which are distinct whenever both appear. So no node repeats, and the walk is a simple cycle. It has $k \ge 2$ C edges and at least one S edge, so it has at least three nodes. It is an SC-cycle, a contradiction. $\square$

The proof does not use the order of the pieces inside a transaction; it holds for any order in which the pieces of a transaction run.

**Lemma 3 (components).** $G$ has an SC-cycle if and only if, for some $i$, two different pieces of $T_i$ each contain a statement that conflicts with a transaction of the same component of the others.

*Proof.* ($\Leftarrow$) Let pieces $p \ne p'$ of $T_i$ conflict with $T_j$ and $T_l$ of one component $K$ of $H_i$. Take a shortest path $T_j = U_0, U_1, \ldots, U_s = T_l$ in $H_i$; its transactions are distinct and none is $T_i$. For each $t < s$ choose pieces $x_t$ of $U_t$ and $y_{t+1}$ of $U_{t+1}$ with conflicting accesses, let $y_0$ be a piece of $U_0$ that conflicts with $p$, and let $x_s$ be a piece of $U_s$ that conflicts with $p'$. The walk $p, y_0, x_0, y_1, x_1, \ldots, y_s, x_s, p', p$ uses C edges from $p$ to $y_0$, from each $x_t$ to $y_{t+1}$ and from $x_s$ to $p'$, an S edge from $y_t$ to $x_t$ when they differ (drop the step when $y_t = x_t$), and the S edge from $p'$ to $p$. Its nodes are pieces of distinct transactions, except for the pairs $y_t, x_t$ and $p', p$, which are distinct inside each pair. So it is a simple cycle with at least three nodes, an S edge and a C edge.

($\Rightarrow$) Let $Z$ be a simple SC-cycle. Let $u, v$ be the ends of an S edge of $Z$; they are pieces of one transaction $T_i$. Remove that edge from $Z$ to get a simple path from $v$ to $u$. Two pieces of $T_i$ are joined only by S edges, and $Z$ has a C edge, whose ends lie in different transactions, so the path visits a piece of another transaction. Let $w$ be the last piece of $T_i$ before the first such visit, and $w'$ the first piece of $T_i$ after it. They are different nodes of a simple path. Every node strictly between them is a piece of a transaction other than $T_i$, and consecutive nodes there are pieces of one transaction (S edge) or of two conflicting transactions (C edge). So all their transactions lie in one component $K$ of $H_i$. The node after $w$ conflicts with $w$, and the node before $w'$ conflicts with $w'$, so $w$ and $w'$ are different pieces of $T_i$ that conflict with $K$. $\square$

The condition of Lemma 3 for a given $i$ depends on the chopping of $T_i$ only, since $H_i$ is built from whole transactions. If the other transactions are not chopped, they have one piece each, and the condition for them is empty. So:

**Corollary 4.** A chopping has no SC-cycle if and only if, for each $i$, the chopping of $T_i$ with all other transactions whole has no SC-cycle. In particular the union of SC-free private choppings is SC-free.

**Lemma 5 (the classes).** After line L7 for transaction $T_i$, two statements of $T_i$ are in the same class of $P$ if and only if a chain of statements of $T_i$ joins them, in which each consecutive pair conflicts with a common component of the others. All statements that conflict with one component $K$ are in one class.

*Proof.* Lines L2 and L3 finish before line L5 starts, so $FIND(U, j)$ in line L7 returns the final representative of the component of $T_j$. Line L7 unites each statement that conflicts with $K$ with $owner[K]$, the first statement that did. So all such statements share a class, and every UNION joins two statements that conflict with a common component. $\square$

**Theorem 6 (finest chopping).** Let $F_i$ be the chopping of $T_i$ made by lines L8 to L10. A contiguous chopping $c_i$ of $T_i$ is rollback-safe and satisfies the condition of Lemma 3 for $i$ if and only if every cut of $c_i$ is a cut of $F_i$.

*Proof.* For a position $p$, let $last(p)$ be the last position in the class of $p$, and let $e_0$ be the last rollback position of $T_i$, or 1. After line L9 at position $p$, $end = \max(e_0, \max_{q \le p} last(q))$, and line L10 cuts after $p$ exactly when this value is $p$.

(Only if.) Let $c_i$ pass the test. By Lemma 5, each UNION joins two statements that conflict with a common component, which by Lemma 3 lie in the same piece of $c_i$; so each class lies inside one piece of $c_i$. Suppose $c_i$ cuts after a position $p$ where $F_i$ does not, so $end > p$ there. If $e_0 > p$, then positions 1 and $e_0$ are on different sides of the cut, and the rollback statement at $e_0$ is not in the first piece of $c_i$, a contradiction. Otherwise $last(q) > p$ for some $q \le p$, and $q$ and $last(q)$ are in one class but on different sides of the cut, a contradiction.

(If.) Every piece of $c_i$ is a union of pieces of $F_i$. The first piece of $F_i$ ends at or after $e_0$, because $end \ge e_0$ throughout; so the first piece of $c_i$ contains every rollback statement. If two pieces of $c_i$ had statements $s, s'$ that conflict with one component $K$, then by Lemma 5 $s$ and $s'$ are in one class. For every position $p$ with $first \le p < last$ of that class, $end \ge last > p$, so $F_i$ has no cut inside the span of the class; $s$ and $s'$ are in one piece of $F_i$, hence in one piece of $c_i$, a contradiction. $\square$

**Conclusion.** Taking $c_i = F_i$ in Theorem 6 shows that each $F_i$ passes the test, and Corollary 4 shows that the union $F$ has no SC-cycle; it is rollback-safe by construction. By Theorem 2, $F$ is correct. By Theorem 6 and Corollary 4, the choppings that pass the test are exactly those whose cuts are cuts of $F$, so $F$ is the unique finest one. The function HAS-SC-CYCLE of the implementation checks the condition of Lemma 3 directly, so it agrees with the definition of an SC-cycle; the tests also compare it with a search over all simple cycles on small workloads.
