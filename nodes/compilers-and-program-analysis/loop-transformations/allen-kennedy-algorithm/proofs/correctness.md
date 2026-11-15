---
title: Allen-Kennedy codegen keeps every dependence and vectorizes each statement as early as possible
proves: [correctness]
status: full
---

We use the notation of the page. The loops form one chain of depth $n$, so for each $k$ the statements of depth $k$ or more are one contiguous run of the text, inside loop $k$. Statement $S$ is inside the loops $1$ to $d_S$. An instance is $S(\vec{i})$ with $\vec{i} = (i_1, \dots, i_{d_S})$. A dependence pair goes from an instance $S(\vec{i})$ that runs first in the sequential program to an instance $T(\vec{j})$. Its level $l$ is the first common loop where $\vec{i}$ and $\vec{j}$ differ, and then $i_l < j_l$. If they agree on all common loops, the level is $n + 1$ (loop independent). For $1 \le m \le n + 1$, the graph $G_m$ has the statements as nodes and an edge $S \to T$ when some pair from $S$ to $T$ has level $m$ or more.

A generated program is a tree. A *loop node* at level $k$ runs its children in order for each value of $i_k$, in increasing order. A *vector node* $(S, k)$ runs, for the current values of $i_1, \dots, i_{k-1}$, all instances of $S$ with those outer indices as one *step*: it reads all its operands, then writes all its results. Each statement is in exactly one vector node, and the loops above it run all values of $i_1, \dots, i_{k-1}$, so each instance runs in exactly one step.

By the reordering theorem on the legality page, the generated program computes the same memory as the original one if two conditions hold: every dependence pair runs in order (the step of the source strictly before the step of the sink), and no dependence pair has both instances in one step. The second condition makes the read-then-write rule of a step exact: no instance of the step reads or overwrites a cell that another instance of the same step writes.

**Lemma 1 (backward edges and cycles).** (a) A loop-independent pair goes from a statement to a statement strictly later in the text. (b) Every statement on a cycle of $G_k$, with $k \le n$, has depth at least $k$. (c) $G_{n+1}$ has no cycle.

*Proof.* (a) If the instances agree on all common loops, the sequential program runs them in text order, and two different instances of one statement cannot agree on all its loops. (c) follows from (a), because the text positions only grow along a path of $G_{n+1}$. For (b), an edge of $G_k$ that does not go strictly forward in the text comes, by (a), from a pair of level $l$ with $k \le l \le n$, so both of its statements share loop $l$ and have depth at least $l \ge k$. Take a cycle of $G_k$. Let $Y$ be its statement that comes first in the text, and $Z$ the one that comes last. The edge of the cycle into $Y$ and the edge out of $Z$ do not go strictly forward, so $Y$ and $Z$ have depth at least $k$. All statements of the cycle lie between $Y$ and $Z$ in the text, and the statements of depth $k$ or more are contiguous, so all of them have depth at least $k$. $\square$

**Lemma 2 (regions).** For $k \ge 2$, the region $R$ of a call CODEGEN$(R, k)$ is a strongly connected component of $G_{k-1}$ restricted to the region of the parent call, with a cycle, and all its statements have depth at least $k - 1$. The call runs inside sequential loop nodes at the levels $1$ to $k - 1$.

*Proof.* Line L6 makes the call at level $k$ for a component of the edges of level $k - 1$ or more that has two statements or a self edge, so it has a cycle. Lemma 1(b) gives the depths. Line L5 emits the loop node at level $k - 1$ around the call, and by induction the parent call is inside the loops at levels $1$ to $k - 2$. $\square$

**Theorem 1 (every dependence is kept).** For every dependence pair from $S(\vec{i})$ to $T(\vec{j})$, with level $l$, the step of $S(\vec{i})$ comes strictly before the step of $T(\vec{j})$, and the two instances are not in one step.

*Proof.* The root call has both $S$ and $T$ in its region. Let CODEGEN$(R, k)$ be the deepest call whose region contains both. There are two cases.

*Case A: $l < k$.* By Lemma 2, the call runs inside a sequential loop node at level $l$, and both steps are below it. The instances agree on $i_1, \dots, i_{l-1}$, so they are in the same run of that loop node, and $i_l < j_l$, so the step of $S(\vec{i})$ runs in an earlier iteration of it. The pair is in order, and not in one step.

*Case B: $l \ge k$.* Then $S \to T$ is an edge in the set $E$ of line L1. If $S$ and $T$ were in the same component, that component would have a cycle (two statements, or the self edge $S \to S$ when $S = T$), and line L6 would call CODEGEN at level $k + 1$ on a region that holds both, against the choice of $R$. So they are in different components, and the edge goes from the component of $S$ to that of $T$. Line L2 puts the component of $S$ first. The instances agree on $i_1, \dots, i_{k-1}$, so they are in the same run of the code of this call, in which all the code of the component of $S$ runs before all the code of the component of $T$. The pair is in order, and not in one step. $\square$

**Theorem 2 (the vector level).** Statement $S$ becomes a vector node $(S, m)$ where $m$ is the least integer $m \ge 1$ such that $S$ is on no cycle of $G_m$. Also $m \le d_S + 1$.

*Proof.* The graphs shrink as $m$ grows: $G_1 \supseteq G_2 \supseteq \dots \supseteq G_{n+1}$. By Lemma 1(b), $S$ is on no cycle of $G_{d_S + 1}$ when $d_S < n$, and by Lemma 1(c) when $d_S = n$. So the least $m$ is at most $d_S + 1$.

Let $C_k(S)$ be the set of statements that are on a common cycle with $S$ in $G_k$, together with $S$; this is the strongly connected component of $S$ in $G_k$. We show by induction on $k$: if the call at level $k$ whose region contains $S$ exists, its region contains $C_k(S)$, and the component of $S$ that its line L2 finds is exactly $C_k(S)$. For $k = 1$ the region is all statements and $E$ is all edges of $G_1$. For the step, the call at level $k + 1$ exists only if line L4 found $C_k(S)$ cyclic, and its region is $C_k(S)$. A cycle of $G_{k+1}$ through $S$ is a cycle of $G_k$, so $C_{k+1}(S) \subseteq C_k(S)$, and line L1 at level $k + 1$ keeps every edge of $G_{k+1}$ inside $C_k(S)$. So the component of $S$ there is $C_{k+1}(S)$.

Line L4 at level $k$ finds the component of $S$ cyclic exactly when $S$ is on a cycle of $G_k$. So the calls go down while $S$ is on a cycle, and $S$ becomes a vector node at the first level $m$ where it is not. $\square$

**Theorem 3 (maximality in the distribution model).** Take any program built from the original loops, in their original nesting and direction, by loop distribution and by reordering the pieces at each level, in which each statement $S$ is in one vector node $(S, k)$ that replaces its loops $k$ to $d_S$. If the program keeps every dependence pair in order and has no pair inside one step, then $k \ge m_S$ for each statement, where $m_S$ is the level of Theorem 2.

*Proof.* Assume that the program runs $S$ as $(S, k)$ with $k < m_S$. Then $S$ is on a cycle $S = S_0 \to S_1 \to \dots \to S_p = S$ of $G_k$, which we take simple. If $p = 1$, a pair of instances of $S$ has level $k$ or more, so it shares $i_1, \dots, i_{k-1}$ and lies in one step, which is not allowed. So $p \ge 2$, and $S$ appears only at the two ends of the cycle.

By Lemma 1(b), every statement of the cycle has depth at least $k$, so it is inside the loops $1$ to $k - 1$ of the original program. In the new program these loops were distributed, and the pieces were ordered. At the level of the vector node $(S, k)$, inside the loops $1$ to $k - 1$ that hold it, consider the sequence of pieces that holds $(S, k)$. Each statement of the cycle with the same $i_1, \dots, i_{k-1}$ as $S$ either runs in a piece of this sequence or runs entirely before or after the whole sequence; we give it the position $-\infty$ or $+\infty$ in those two cases and the index of its piece otherwise. The order of the pieces does not depend on $i_1, \dots, i_{k-1}$. Write $P(X)$ for the position of statement $X$.

Each edge $S_a \to S_{a+1}$ comes from a pair of level $k$ or more, so its two instances share $i_1, \dots, i_{k-1}$. The program keeps the pair in order, so $P(S_a) \le P(S_{a+1})$, because a later position runs later for the same outer indices. When one of $S_a$ and $S_{a+1}$ is $S$, the inequality is strict: the piece of $S$ is the single step $(S, k)$, and the other statement is not $S$, so it is in another piece or outside the sequence. Around the cycle this gives $P(S) < P(S)$, which is impossible. $\square$

Theorem 3 is limited to programs of this kind. Darte and Vivien (1997) proved a stronger result: if the only information about the dependences is their level, no transformation finds more parallel loops than Allen and Kennedy's algorithm.

**Termination and cost.** Each call at level $k$ calls itself only at level $k + 1$, and by Lemma 1(c) no call at level $n + 2$ is made, so the depth of the recursion is at most $n + 1$. The regions of the calls at one level are disjoint. If each call passes the edges inside each child region down to that child, the work at one level is $O(r + e)$ for line L1, Tarjan's algorithm and the topological sort. The total is $O(n(r + e))$ time.
