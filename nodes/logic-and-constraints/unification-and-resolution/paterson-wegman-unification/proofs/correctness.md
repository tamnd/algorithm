---
title: The Paterson-Wegman algorithm is correct and runs in linear time
proves: [correctness]
status: full
---

We use the notation of the page. $G$ is the term DAG of the two input terms, with each variable stored as one node. For a node $p$, $\mathrm{term}(p)$ is the tree term that $p$ denotes. A function node $p = f(c_1, \ldots, c_k)$ has the children $c_1, \ldots, c_k$, and $p$ is a **parent** of each $c_i$. The input pair is the two roots $u, v$, and a unifier of $u, v$ is a substitution $\theta$ with $\mathrm{term}(u)\theta = \mathrm{term}(v)\theta$.

## Part 1: unification as a closure on the DAG

Let $\equiv$ be the least equivalence relation on the nodes of $G$ that contains $(u, v)$ and is **closed under decomposition**: if $p \equiv q$ are function nodes with the same symbol and arity, then their $i$-th children are equivalent for each $i$. The classes of $\equiv$ are the **unification classes**. The **class graph** has an edge from class $C$ to class $D$ when some function node of $C$ has a child in $D$.

**Lemma 1.** If $\theta$ unifies $u, v$, then $\mathrm{term}(p)\theta = \mathrm{term}(q)\theta$ for all $p \equiv q$.

*Proof.* The relation "$\mathrm{term}(p)\theta = \mathrm{term}(q)\theta$" is an equivalence, it contains $(u, v)$, and it is closed under decomposition, because $f(a_1, \ldots, a_k) = f(b_1, \ldots, b_k)$ implies $a_i = b_i$. So it contains the least such relation $\equiv$. $\square$

**Lemma 2.** $u$ and $v$ are unifiable if and only if

- (C1) no class contains two function nodes with different symbols or arities, and
- (C2) the class graph has no cycle.

If they hold, let $T(C)$ be defined on classes by recursion along the class graph: if $C$ has a function node $f(c_1, \ldots, c_k)$, then $T(C) = f(T([c_1]), \ldots, T([c_k]))$; otherwise $T(C) = x_C$ for a chosen variable $x_C \in C$. Then $\sigma = \{x \mapsto T([x]) : x \text{ a variable of } G,\ T([x]) \ne x\}$ is an idempotent most general unifier of $u$ and $v$.

*Proof.* Suppose $\theta$ unifies $u, v$. Two function nodes in one class have equal $\theta$-images by Lemma 1, so they have the same symbol and arity: (C1) holds. Suppose the class graph has a cycle $C_0 \to C_1 \to \cdots \to C_j = C_0$. Each edge $C_i \to C_{i+1}$ comes from a function node $p_i \in C_i$ with a child $c_i \in C_{i+1}$. All nodes of a class have one $\theta$-image by Lemma 1; call its size $h_i$ for $C_i$. As $\mathrm{term}(c_i)\theta$ is a proper subterm of $\mathrm{term}(p_i)\theta$, $h_{i+1} < h_i$ for each $i$, so $h_0 < h_0$, a contradiction. So (C2) holds.

Now suppose (C1) and (C2). $T$ is well defined: by (C1) and closure under decomposition, any two function nodes of a class have the same symbol and equivalent children, so the choice of the function node does not matter, and by (C2) the recursion ends.

*$\sigma$ unifies.* By induction on the height of $p$ in $G$, $\mathrm{term}(p)\sigma = T([p])$. For a variable $x$, $x\sigma = T([x])$ by definition. For $p = f(c_1, \ldots, c_k)$, $\mathrm{term}(p)\sigma = f(T([c_1]), \ldots, T([c_k])) = T([p])$, because $p$ is a function node of $[p]$. As $u \equiv v$, $\mathrm{term}(u)\sigma = T([u]) = \mathrm{term}(v)\sigma$.

*$\sigma$ is most general.* Let $\theta$ unify $u, v$. By induction along the class graph, $T(C)\theta = \mathrm{term}(q)\theta$ for each $q \in C$. If $C$ has a function node $p = f(c_1, \ldots, c_k)$, then $T(C)\theta = f(T([c_1])\theta, \ldots) = f(\mathrm{term}(c_1)\theta, \ldots) = \mathrm{term}(p)\theta$, and this equals $\mathrm{term}(q)\theta$ by Lemma 1. Otherwise $T(C)\theta = x_C\theta = \mathrm{term}(q)\theta$ by Lemma 1. So for each variable $x$ of $G$, $x\sigma\theta = T([x])\theta = x\theta$, and for every other variable $\sigma$ is the identity. So $\sigma\theta = \theta$ and $\sigma \le \theta$.

*$\sigma$ is idempotent.* The variables of each $T(C)$ are chosen variables $x_D$ of classes without function nodes, and $x_D\sigma = T(D) = x_D$. So $\sigma$ fixes every variable of its range. $\square$

So it is enough to show that the algorithm computes the classes of $\equiv$, fails exactly when (C1) or (C2) fails, and binds each variable $x$ to the root of its class, which represents $T([x])$.

## Part 2: what the algorithm computes

A **finished class** is the set $M$ of members of one call FINISH$(r)$ that reaches line L16; $r$ is its **root**. We say a node is **complete** when it has been marked at L16.

**Fact A (soundness of edges).** Each equality edge $\{a, b\}$ that the algorithm adds has $a \equiv b$, and each set of members is inside one class of $\equiv$.

*Proof.* The edge of L1 is $\{u, v\}$. The members of a call are connected to its root by equality edges (L12), so by induction they are equivalent. At L15, $r$ and $s$ are function nodes of one set of members, so $r \equiv s$, and L9 has checked that they have the same symbol and arity. So their $i$-th children are equivalent, by closure under decomposition. $\square$

**Fact T (timing).** As long as the run has not failed: (i) when an equality edge is added, both of its ends are incomplete; (ii) no edge is added to a node $t$ after the pass of L11 over $t$.

*Proof.* (i) At L1 nothing is complete. At L15 the edge joins children of $r$ and of $s$. A node completes only at L16 of its call, after it was popped, and when it was popped L10 made all its parents complete. As $r$ and $s$ are not complete, their children are not complete. (ii) Edges to $t$ are added only at L15, while an active call holds a parent of $t$. When $t$ was popped, L10 made every parent of $t$ complete before L11 (a parent in an active call would have made L5 fail), and a complete class adds no more edges. $\square$

**Fact B (failure is correct).**

- *L9.* Two function nodes $r \equiv s$ with different symbols or arities violate (C1).
- *L5 and L13.* At any time, the active calls form a chain FINISH$(r_0)$, ..., FINISH$(r_j)$, where each $r_{i+1}$ is a parent of a member of the call of $r_i$ (L10). So the class of $r_{i+1}$ has an edge to the class of $r_i$ in the class graph. At L5, FINISH$(p)$ is called for a parent $p$ of a member of the current call, and $p$ already has a pointer but is not complete. So $p$ is a member of an active call $i \le j$. The class of $p$ then has an edge to the class of the current call $j$, and the chain gives edges from the class of call $j$ down to the class of call $i$. This is a closed walk, so the class graph has a cycle and (C2) fails. At L13, a neighbor $t$ of $s$ has a pointer $r' \ne r$. By Fact T, the edge $\{s, t\}$ existed before the pass of L11 over $t$, if that pass has happened. If it had happened, it would have read the edge and given $s$ the pointer $r'$, or failed; but $s$ has the pointer $r$. So $t$ has not been popped yet. Then $t$ is a waiting member of an active call $i < j$, not complete. By Fact A, $t \equiv s$, so the members of calls $i$ and $j$ lie in one class of $\equiv$, and the chain from call $j$ down to call $i$ is a closed walk in the class graph. So (C2) fails.

**Fact C (completeness of a finished class).** In a run that does not fail, each equality edge joins two members of the same finished class.

*Proof.* Consider an edge $\{a, b\}$. By Fact T, both ends are incomplete when it is added, and it is added before the passes of L11 over $a$ and over $b$. Let $a$ be the end of the edge that first gets a pointer, in the call with root $r$. When $a$ is popped, L11 reads the edge to $b$. If $b$ has no pointer, it joins the members of $r$ (L12). If it has a pointer, it is $r$, since otherwise L13 fails. So $a$ and $b$ end in the same finished class. $\square$

**The classes are exact.** In a run that does not fail, let $p \sim q$ mean that $p$ and $q$ are in the same finished class. Every node is complete at the end, because of the loops of L2 and L3. By Fact A, $\sim$ is contained in $\equiv$. For the converse, $\sim$ contains $(u, v)$ by Fact C, and it is closed under decomposition: the root of a class that has a function node is a function node, because FINISH is called on variables only at L3, after every function node is complete, and by Fact C a complete function node has its whole class complete. So for function nodes $p \sim q$ with root $r$, L15 added the edges $\{\text{child}_i(r), \text{child}_i(p)\}$ and $\{\text{child}_i(r), \text{child}_i(q)\}$ (or $p = r$, or $q = r$), and Fact C puts all three children in one finished class. So $\equiv$ is contained in $\sim$, and the finished classes are exactly the classes of $\equiv$.

**No failure means (C1) and (C2).** L9 checks every function member against the root, so (C1) holds. A class completes only after the classes of all parents of its members (L10). For an edge $C \to D$ of the class graph, a function node of $C$ is a parent of a node of $D$, so $C$ completes before $D$. The completion order is a topological order, so the class graph has no cycle, and (C2) holds.

**The output.** L14 binds each variable member $s \ne r$ to the root $r$. If $r$ is a function node, expanding the bindings below $r$ gives $T([s])$, because each child of $r$ is expanded in the same way. If $r$ is a variable, its class has no function node, $r$ stays unbound, and it plays the role of $x_C$. So the bindings represent the $\sigma$ of Lemma 2, an idempotent mgu, and the algorithm fails exactly when no unifier exists.

## Part 3: linear time

Let $N$ be the number of nodes plus the number of DAG edges of $G$.

- Each node gets a pointer at most once (L6, L12), so it is pushed and popped at most once.
- When a node $s$ is popped, L10 reads its parent list once. The parent lists hold one entry per DAG edge, so L10 costs $O(N)$ in total.
- FINISH sets the pointer of its argument at L6 or stops the run at L5, so there are at most (number of nodes) $+ 1$ calls.
- L1 adds one equality edge, and L15 adds $k$ edges for each function member $s \ne r$ of arity $k$, at most once per node. So there are at most $1 + (\text{number of DAG edges})$ equality edges, and L11 reads each of them twice.
- L16 marks each node once.

So the algorithm runs in $O(N)$ time and space. Building $G$ from two trees with a hash table of nodes takes time linear in their size, in expectation. $\blacksquare$
