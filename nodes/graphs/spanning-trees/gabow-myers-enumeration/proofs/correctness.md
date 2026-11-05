---
title: The Gabow-Myers backtracking lists every spanning tree exactly once
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a finite undirected graph with $V = \{0, \dots, n - 1\}$, $n \ge 1$. Parallel edges are distinct edges, and self-loops are allowed. During the run, some edges are *deleted*. The *current graph* $G'$ is $G$ without the deleted edges. For an edge set $T$, let $V(T)$ be the set $\{0\}$ together with the ends of the edges of $T$. An edge *leaves* $V(T)$ if it has exactly one end in $V(T)$.

## Facts

**Fact 1.** Let $H$ be a connected graph, and let $T$ be a set of edges of $H$ that forms a tree on $V(T)$. Then some spanning tree of $H$ contains $T$.

*Proof.* Start from $T$. While the edge set does not span $V$, some edge of $H$ leaves the set of reached vertices, because $H$ is connected. Adding it keeps the set a tree. After $n - 1 - |T|$ steps, the set is a spanning tree that contains $T$. $\square$

**Fact 2.** If $T$ is a tree on $V(T) \ne V$, then every spanning tree $S \supseteq T$ of a graph $H$ contains an edge of $H$ that leaves $V(T)$.

*Proof.* $S$ connects a vertex of $V(T)$ to a vertex outside it, and the path between them in $S$ has an edge that leaves $V(T)$. $\square$

## The invariant

Call a state of a call GROW$(T, F)$ *good* if the following hold:

- (a) $T$ is a tree on $V(T)$, and $T \subseteq G'$.
- (b) $G'$ is connected.
- (c) $F$ holds exactly the edges of $G'$ that leave $V(T)$, each once.

**Lemma.** If GROW$(T, F)$ is called in a good state, then it terminates. It outputs each spanning tree of $G'$ that contains $T$ exactly once, and nothing else. On return, $G'$ and $F$ are as they were at the call.

*Proof.* By induction on $k = n - 1 - |T|$.

*Base, $k = 0$.* By (a), $T$ is a tree with $n - 1$ edges, so it is a spanning tree. It is the only spanning tree that contains $T$. Line L1 outputs it and returns without changing anything.

*Step, $k > 0$.* Then $|V(T)| = |T| + 1 < n$. Let $G'_1 = G'$ be the current graph at the call. Let $e_1, e_2, \dots$ be the edges popped at line L4 in the successive iterations, and let $G'_j$ be the current graph at the start of iteration $j$. Line L8 gives $G'_{j+1} = G'_j - e_j$, and line L7 together with the induction hypothesis gives that the recursive call changes nothing. We show by induction on $j$ that iteration $j$ starts with $G'_j$ connected and with $F$ equal to the set of edges of $G'_j$ that leave $V(T)$.

For $j = 1$, this is (b) and (c). Suppose it holds for $j$. The graph $G'_j$ is connected and $V(T) \ne V$, so some edge of $G'_j$ leaves $V(T)$, and $F$ is not empty. So line L4 pops an edge $e_j = (v, w)$ with $v \in V(T)$ and $w \notin V(T)$. Line L5 removes the edges of $F$ that join $V(T)$ to $w$ and adds the edges of $G'_j$ from $w$ to $V \setminus (V(T) \cup \{w\})$. Afterwards $F$ holds exactly the edges of $G'_j$ that leave $V(T) \cup \{w\} = V(T \cup \{e_j\})$. The set $T \cup \{e_j\}$ is a tree on that vertex set, because $e_j$ adds the new vertex $w$. So the call at line L6 is made in a good state, with $k - 1$, and the induction hypothesis applies. Line L7 restores $F$ to the edges of $G'_j$ that leave $V(T)$, minus $e_j$. Line L8 deletes $e_j$. So $F$ is now the set of edges of $G'_{j+1}$ that leave $V(T)$. If the loop continues, then $G'_{j+1}$ is connected, by the test at lines L9 and L10. This completes the induction on $j$.

*Termination.* Each iteration deletes an edge of the finite graph $G$, and each recursive call terminates by the induction hypothesis. So the loop runs at most $|E|$ times. Let $q$ be the number of iterations. Then $G'_{q+1} = G' - \{e_1, \dots, e_q\}$ is disconnected.

*What is output.* By the induction hypothesis, iteration $j$ outputs exactly the spanning trees of $G'_j$ that contain $T \cup \{e_j\}$, each once. These are the spanning trees $S$ of $G'$ with $S \supseteq T$, $e_j \in S$ and $e_1, \dots, e_{j-1} \notin S$. Call this set $\mathcal{S}_j$.

- *Disjoint.* If $i < j$, every tree in $\mathcal{S}_i$ contains $e_i$ and every tree in $\mathcal{S}_j$ avoids it. So no tree is output twice.
- *Complete.* Let $S$ be a spanning tree of $G'$ with $S \supseteq T$. If $S$ contains none of $e_1, \dots, e_q$, then $S$ is a spanning tree of the disconnected graph $G'_{q+1}$, which is impossible. So $S$ contains some $e_j$. Taking the least such $j$ gives $S \in \mathcal{S}_j$.
- *Only trees that contain $T$.* Every output tree lies in some $\mathcal{S}_j$.

*Restoration.* Line L11 undeletes $e_1, \dots, e_q$, so the current graph is $G'$ again. It pushes $e_q, \dots, e_1$ back onto $F$, with $e_1$ on top, which reverses the pops of line L4. Lines L7 and L8 left the rest of $F$ as it was. So $F$ is as it was at the call. $\square$

## The theorem

**Theorem.** If $G$ is connected, the top-level call outputs each spanning tree of $G$ exactly once and terminates. If $G$ is disconnected, it outputs nothing.

*Proof.* If $G$ is disconnected, it has no spanning tree, and the top level returns before calling GROW. Otherwise, the call GROW$(\emptyset, F)$, with $F$ the non-loop edges at vertex 0, is made in a good state. $T = \emptyset$ is a tree on $V(\emptyset) = \{0\}$, $G' = G$ is connected, and the edges that leave $\{0\}$ are exactly the non-loop edges at 0. Every spanning tree contains $\emptyset$. The lemma then gives the claim. $\blacksquare$

**Corollary (no dead ends).** Every call of GROW outputs at least one tree.

*Proof.* Every call is made in a good state. By Fact 1, the connected graph $G'$ has a spanning tree that contains $T$, and the lemma says the call outputs it. $\square$

So the recursion tree has $N$ leaves, its depth is at most $n - 1$, and it has at most $(n - 1)N + 1$ nodes. This is the count used in the complexity analysis. Fact 2 is the reason the loop can stop at a bridge: once $G'_{j+1}$ is disconnected, no remaining tree avoids $e_1, \dots, e_j$.
