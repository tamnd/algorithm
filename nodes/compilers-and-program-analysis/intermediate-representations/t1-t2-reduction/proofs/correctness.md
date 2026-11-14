---
title: T1 and T2 reduce a flow graph to one vertex exactly when it is reducible, and the worklist finds a maximal sequence
proves: [correctness, termination]
status: full
---

**Setting.** A flow graph is $G = (N, E, r)$, where $E$ is a set of ordered pairs (self-loops are allowed, parallel edges are not) and $r$ reaches every vertex. Line L1 of the algorithm keeps only the vertices that $r$ reaches, and an edge from a vertex that $r$ does not reach lies on no path from $r$, so this changes neither the dominators nor the answer; from here on every vertex is reachable. $x$ *dominates* $y$, written $x \,\mathrm{dom}\, y$, if every path from $r$ to $y$ contains $x$. An edge $(t, h)$ is a *back edge* if $h \,\mathrm{dom}\, t$, $B$ is the set of back edges, and $H = (N, E \setminus B)$. $G$ is *reducible* if $H$ has no cycle; call this condition (C). This is the definition on the page of the reducible flow graph.

**T1** deletes a self-loop $(v, v)$. **T2** applies to a vertex $v \ne r$ whose set of predecessors is $\{u\}$ for one vertex $u$. It deletes $v$ and the edge $(u, v)$ and replaces each edge $(v, w)$ by $(u, w)$; an edge that is already there is not added again. Since $v \ne r$ is reachable and $u$ is its only predecessor, $u \ne v$, so $v$ has no self-loop. An edge $(v, u)$ becomes the self-loop $(u, u)$. Let $\varphi(v) = u$ and $\varphi(x) = x$ for $x \ne v$. Then the new graph is $G' = (N', E', r)$ with $N' = N \setminus \{v\}$ and $E' = \{(\varphi(a), \varphi(b)) : (a, b) \in E,\ (a, b) \ne (u, v)\}$, because the only edge into $v$ is $(u, v)$.

Two facts are used many times. A walk from $r$ to $y$ that avoids a vertex $x$ contains a path from $r$ to $y$ that avoids $x$. Dominance is antisymmetric: if $x \,\mathrm{dom}\, y$ and $y \,\mathrm{dom}\, x$, then $x = y$. Indeed, let $x \ne y$ and take a path $P$ from $r$ to $x$. It contains $y$, and $y$ is not its last vertex, so the part of $P$ up to $y$ is a path from $r$ to $y$ that does not contain $x$, because $x$ appears on $P$ only at the end. So $x$ does not dominate $y$.

**Lemma 1 (T1 keeps everything).** T1 does not change reachability, dominance or $H$.

*Proof.* A self-loop is on no path, since a path does not repeat a vertex. So the paths from $r$ are the same, and reachability and dominance are the same. The self-loop $(v, v)$ is a back edge because $v \,\mathrm{dom}\, v$, so it is not in $H$, and the other back edges stay back edges. $\square$

**Lemma 2 (paths through a T2 step).** Let T2 merge $v$ into $u$.

(a) Every vertex of $G'$ is reachable from $r$.

(b) For $x, y \ne v$: $x \,\mathrm{dom}\, y$ in $G$ if and only if $x \,\mathrm{dom}\, y$ in $G'$.

(c) For $b \ne v$: $b \,\mathrm{dom}\, v$ in $G$ if and only if $b \,\mathrm{dom}\, u$ in $G$.

(d) $(u, v)$ is not a back edge of $G$.

*Proof.* Every occurrence of $v$ on a walk from $r$ comes right after an occurrence of $u$, because $v \ne r$ and $u$ is its only predecessor.

*Down.* Map a walk $P$ of $G$ from $r$ by $\varphi$ and drop each step $u \to v$, which becomes $u \to u$. A step $v \to w$ becomes $u \to w$, which is in $E'$. The result is a walk of $G'$ from $r$ with the vertex set $\varphi(V(P))$. If $v \in V(P)$, then also $u \in V(P)$, so $V(P) \setminus \{v\}$ is that vertex set in all cases.

*Up.* An edge $(a, b) \in E'$ is the image of some edge $(a', b') \in E$ other than $(u, v)$. Then $b' \ne v$, so $b' = b$, and $a' = a$, or $a = u$ and $a' = v$. Replace the step $a \to b$ by $a \to b$ in the first case and by $u \to v \to b$ in the second. A walk of $G'$ from $r$ becomes a walk of $G$ from $r$ whose vertex set is the old vertex set, perhaps with $v$ added.

(a) follows from the down map, applied to a path from $r$ to $y \ne v$.

(b) If a path of $G'$ from $r$ to $y$ avoids $x$, its lift is a walk of $G$ from $r$ to $y$ that avoids $x$, since the only new vertex is $v \ne x$. If a path $P$ of $G$ from $r$ to $y$ avoids $x$, its image has the vertex set $V(P) \setminus \{v\}$, which does not contain $x$. So "some path avoids $x$" is true in $G$ exactly when it is true in $G'$.

(c) Each path from $r$ to $v$ ends with the step $u \to v$, so its part up to $u$ is a path from $r$ to $u$. If every path to $u$ contains $b$, so does every path to $v$. If a path to $u$ avoids $b$, then adding the step $u \to v$ gives a path to $v$ that avoids $b$, because $b \ne v$ and the path to $u$ does not contain $v$ (it would contain $u$ before it).

(d) $u \,\mathrm{dom}\, v$, since every path to $v$ passes through $u$. If also $v \,\mathrm{dom}\, u$, then $u = v$ by antisymmetry, which is false. So $v$ does not dominate $u$, and $(u, v)$ is not a back edge. $\square$

**Lemma 3 (T2 keeps (C)).** If T2 turns $G$ into $G'$, then $G$ satisfies (C) if and only if $G'$ does.

*Proof.* First, an edge $(a, b) \ne (u, v)$ of $G$ is a back edge of $G$ exactly when its image $(\varphi(a), \varphi(b))$ is a back edge of $G'$. If $a, b \ne v$ this is Lemma 2(b). The case $b = v$ does not occur. If $a = v$ and $b \ne v$, then $(v, b)$ is a back edge iff $b \,\mathrm{dom}\, v$ in $G$, iff $b \,\mathrm{dom}\, u$ in $G$ by Lemma 2(c), iff $b \,\mathrm{dom}\, u$ in $G'$ by Lemma 2(b), iff $(u, b)$ is a back edge of $G'$. Two edges with the same image, $(u, w)$ and $(v, w)$, are therefore both back edges or both not.

So the edges of $H'$ are the images of the edges of $H$ other than $(u, v)$, and $(u, v)$ is an edge of $H$ by Lemma 2(d). In other words, $H'$ is $H$ with the edge $(u, v)$ contracted, where $(u, v)$ is the only edge of $H$ into $v$.

A graph has a cycle exactly when it has a closed walk with at least one edge. Let $C$ be a cycle of $H$. If $C$ avoids $v$, it is a cycle of $H'$. Otherwise $C$ contains the steps $u \to v \to w$, and replacing them by $u \to w$ gives a closed walk of $H'$ with at least one edge; if $C$ is $u \to v \to u$, the result is the self-loop $(u, u)$. Conversely, a closed walk of $H'$ with at least one edge lifts as in the proof of Lemma 2, by putting $u \to v$ before every step that comes from an edge $(v, w)$, to a closed walk of $H$ with at least one edge. $\square$

**Lemma 4 (progress).** If $G$ satisfies (C), has at least 2 vertices and has no self-loop, then some vertex $w \ne r$ has exactly one predecessor.

*Proof.* By strong induction on $|N|$. Every edge $(a, r)$ is a back edge, because $r$ dominates every vertex. The edges of a depth-first search tree from $r$ are not back edges: for a tree edge $(x, y)$, the tree path from $r$ to $x$ does not contain $y$, so $y$ does not dominate $x$. So $H$ contains a spanning tree from $r$, every vertex $x \ne r$ has a predecessor in $H$, and $r$ has none. $H$ is acyclic by (C), so it has a topological order, and $r$ comes first because it is the only vertex without a predecessor in $H$ and all others are reachable from it in $H$. Let $v$ be the second vertex in this order. Its predecessors in $H$ come before it, so they are $\{r\}$. Every other predecessor $p$ of $v$ in $G$ is the tail of a back edge $(p, v)$, so $v \,\mathrm{dom}\, p$, and $p \ne v$ because there is no self-loop. The edge $(r, v)$ is not a back edge, since $v$ does not dominate $r$.

*Case 1.* $v$ has no predecessor other than $r$. Then $w = v$ works.

*Case 2.* Some predecessor $p \ne r$ has $v \,\mathrm{dom}\, p$. Let $D = \{x : v \,\mathrm{dom}\, x\}$. Then $v, p \in D$, $r \notin D$, so $2 \le |D| < |N|$.

(i) *Every edge into $D \setminus \{v\}$ starts in $D$.* Let $(a, x) \in E$ with $x \in D$, $x \ne v$. If $a \notin D$, a path from $r$ to $a$ that avoids $v$, followed by the step to $x$, is a path to $x$ that avoids $v$; this contradicts $x \in D$.

(ii) *$v$ reaches every vertex of $D$ inside $D$.* Take a path from $r$ to $x \in D$ and its part $S$ after the last $v$. A vertex $y$ of $S$ is in $D$: if a path $Q$ from $r$ to $y$ avoided $v$, then $Q$ followed by the rest of $S$ would be a walk to $x$ that avoids $v$.

So $G_D = (D, E \cap (D \times D), v)$ is a flow graph with root $v$, fewer vertices than $G$, at least 2 vertices and no self-loop.

(iii) *$G_D$ satisfies (C).* Let $x, y \in D$ with $y \,\mathrm{dom}\, x$ in $G$. We show $y \,\mathrm{dom}\, x$ in $G_D$. If $y = v$ this holds, because $v$ is the root of $G_D$. Let $y \ne v$. Take a path from $r$ to $v$ and cut it at its first $v$; call this part $Q$. $Q$ does not contain $y$: otherwise its part up to $y$ would avoid $v$, and $v \,\mathrm{dom}\, y$ would fail. So if a path of $G_D$ from $v$ to $x$ avoided $y$, then $Q$ followed by it would be a walk of $G$ from $r$ to $x$ that avoids $y$, which is false. Hence every back edge of $G$ inside $D$ is a back edge of $G_D$, and the graph $H_D$ of $G_D$ is a subgraph of $H$. A subgraph of an acyclic graph is acyclic.

By induction, some $w \in D$, $w \ne v$, has exactly one predecessor in $G_D$. By (i), all predecessors of $w$ in $G$ lie in $D$, so $w$ has exactly one predecessor in $G$, and $w \ne r$ because $r \notin D$. $\square$

**Theorem 1 (the T1-T2 characterization).** A sequence of T1 and T2 steps is *maximal* if neither applies to its last graph. Every sequence is finite, because each step removes an edge or a vertex. For a flow graph $G$, these are equivalent:

1. $G$ is reducible.
2. Every maximal sequence of T1 and T2 steps ends in a graph with one vertex.
3. Some maximal sequence ends in a graph with one vertex.

*Proof.* (1) ⇒ (2): by Lemmas 1 and 3, every graph of the sequence satisfies (C) and is a flow graph. The last graph has no self-loop, since T1 does not apply, and no vertex $w \ne r$ with exactly one predecessor, since T2 does not apply. By Lemma 4 it has one vertex. (2) ⇒ (3): a maximal sequence exists, since any sequence can be extended until it stops. (3) ⇒ (1): the last graph has one vertex and no self-loop, so it has no edge and satisfies (C). Lemmas 1 and 3 hold in both directions, so going back along the sequence, every graph satisfies (C), and so does $G$. $\square$

So the verdict does not depend on the order of the steps. Hecht and Ullman (1972) proved more: the last graph of a maximal sequence is the same, up to the names of the vertices, for every order. This file does not prove that stronger claim, and the algorithm does not need it.

**Lemma 5 (the worklist finds a maximal sequence).** Each T1 in line L6 and each T2 in lines L8 to L11 is a step on the current graph, and when line L3 finds $W$ empty, neither T1 nor T2 applies to any vertex.

*Proof.* Lines L5 and L7 test exactly the conditions of T1 and T2 on the current sets, and lines L8 to L11 update $succ$ and $pred$ as T2 says, with sets, so a repeated edge is stored once. Whether T1 or T2 applies to a vertex $x$ depends only on $succ[x]$, $pred[x]$ and whether $x = r$. Invariant: each vertex to which T1 or T2 applies is in $W$ when line L3 tests it. At the start every vertex is in $W$. When $v$ is popped, line L6 removes a self-loop if there is one, and then line L7 tests T2 on the new sets of $v$. If T2 is not done, then neither step applies to $v$ any more, and no other set has changed. If T2 is done, $v$ is gone. The sets that change are $succ[u]$, the sets $pred[w]$ for $w \in succ[v]$, and $pred[u]$ when $u \in succ[v]$; line L11 pushes $u$ and every such $w$. A T1 changes only the sets of $v$. So the invariant holds after each iteration, and when $W$ is empty no step applies. $\square$

**Termination and cost.** Let $n$ and $m$ be the numbers of vertices and edges. There are at most $n - 1$ T2 steps, because each removes a vertex and the root is never removed, and at most $m + n - 1$ T1 steps, because a self-loop is either an edge of the input or made by a T2 step from an edge $(v, u)$, at most one per T2. Line L2 pushes $n$ vertices and each T2 pushes $1 + |succ[v]| \le n$ vertices, so there are at most $n + (n - 1) n$ pushes, and the loop runs $O(n^2)$ times. Line L1 takes $O(n + m)$ steps. Each T2 step does $O(1 + |succ[v]|) = O(n)$ set operations. With a hash table per set, each set operation takes expected constant time, and the total is $O(n^2 + m)$ expected; with an $n \times n$ bit table for edge membership and lists for iteration the same bound holds in the worst case. The space is $O(n + m)$ for the sets.

**What is proved and what is measured.** Theorem 1, Lemma 5 and the bound $O(n^2 + m)$ are proved here. The uniqueness of the limit graph is cited from Hecht and Ullman. The tests check, on seeded random graphs, that the result agrees with the definition of reducibility computed by brute force, and that a naive applier that picks T1 and T2 steps in random orders always reaches the same verdict; these are measurements and do not replace the proof.
