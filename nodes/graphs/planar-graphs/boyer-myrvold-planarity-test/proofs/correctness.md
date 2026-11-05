---
title: Correctness of the Boyer-Myrvold planarity test
proves: [correctness, termination]
status: sketch
---

Line numbers refer to the pseudocode on the main page. Vertices are their preorder numbers in the search of line L2. Soundness (an output rotation system is planar) and the main invariant are proved in full. Completeness (if line L7 fails, the graph is not planar) is proved for the Minors A, B and C below; for the remaining cases the proof follows the case analysis of Boyer and Myrvold (2004) and only states it, so this file has the status of a sketch.

## Setting

The *embedded graph* $\tilde G$ is the set of tree edges and of back edges embedded so far, with each component stored as a rotation system: a cyclic list of edges at each node, read in one direction for the component. A node is a vertex or a root copy $r_c$. *Step* $v$ means one round of lines L5 to L7. A *component* is a connected part of $\tilde G$ that is joined to the rest only through root copies, so its root copy $r_c$ is the only node of it that stands for a vertex outside the subtree $T(c)$.

**Fact 1.** At the start of step $v$, every back edge $(u, w)$ with $u > v$ is embedded, and none with $u \le v$ is. Every component has the form: a root copy $r_c$, and a set of vertices of $T(c)$ that includes $c$.

*Proof.* Line L3 creates one component per tree edge. A step $u$ embeds only back edges $(u, w)$ (line L17 with $R = r_c$ a copy of $u$), and by line L7 it embeds all of them or the run ends. A merge (line L25) puts a component with root copy $r_{c'}$, where $c'$ is a child of a vertex $w$ of the component, into the component of $w$, and $T(c') \subset T(c)$. $\square$

## Soundness

**Lemma 1.** Every component of $\tilde G$ is a plane embedding at all times, and its external face is the face that lines L12, L15, L19 and L21 walk along.

*Proof.* By induction over the operations. A new component $r_c - c$ is one edge, which is planar, and its external face holds both nodes.

*Embedding an edge (line L17).* When $(R, w)$ is embedded on side $d$, the walk has reached $w$ from $R$ along side $d$ of the external face, through components that were merged into one just before (the stack $S$ is emptied first). So $R$ and $w$ are both on the external face of one component, and the new edge is drawn in the external face, next to the part of the boundary that the walk went along. A curve in the outer face between two points of its boundary crosses nothing, so the result is plane. The new external face is the old one with the walked part between $R$ and $w$ replaced by the new edge.

*Merging (lines L24 and L25).* The root copy $r$ is a copy of $w$, and $w$ is on the external face of its component. Putting the whole component of $r$ into the corner of the external face at $w$, between the edge by which the walk came and the next one, and then identifying $r$ with $w$, glues two plane embeddings at one point of their outer faces; this is plane. Its external face is the old external face with the boundary of the component of $r$ inserted at $w$.

*Flipping (line L24).* Reversing every list of a component gives the mirror image of its embedding, which is plane and has the same faces. The code reverses only the list of $r$ and records $\mathrm{sign}(c) = -1$; the lists of the other vertices of the component are taken as reversed. The walk reads lists from both ends and keeps the side by which it entered each node, so it reads the external face of the true embedding in both cases.

*The final join and orientation (lines L8 and L9).* Line L8 glues the remaining components at their root copies, as in a merge, which is plane. In the end, a vertex $u$ lies in the component that was flipped by every flip on its tree path, and only those: a flip of the component of $r_c$ flips the vertices of $T(c)$ that were in it, and later merges carry them along. So the true list of $u$ is the stored list reversed exactly when the product of signs from the root to $u$ is $-1$, which is what line L9 does. $\square$

**Theorem 1 (soundness).** If BM-PLANAR returns a rotation system, then it is a planar embedding of $G$.

*Proof.* All tree edges are embedded by line L3, and every back edge by line L7 (a back edge $(v, w)$ is checked at step $v$). No other edge is ever added, and each edge is added once. By Lemma 1, the result is a plane embedding with every edge of $G$. $\square$

## The main invariant

Being pertinent or externally active with respect to a step $u$ means that $w$ has a path to a vertex $a \le u$ that is an ancestor of $u$, made of edges that are not embedded yet, apart from tree edges into the subtree of a separate child of $w$.

**Lemma 2 (invariant).** After step $v$, every vertex that is pertinent or externally active with respect to $v - 1$ is on the external face of its component.

*Proof.* Being active with respect to $v - 1$ means having a connection to a vertex $u < v$, so it implies being externally active with respect to $v$. Activity only goes down as the steps go on, because embedded edges are not counted and the threshold $v$ goes down. Before step $n - 1$ every component is a single edge, so the claim holds. Assume it holds before step $v$.

A vertex leaves the external face only when an edge $(R, z)$ is embedded at line L17: the nodes on the walked part of the boundary between the previous point and $z$ go inside. Each of these nodes was passed by the walk of this step. The walk passes a node only in three ways: at line L21, which requires it to be not externally active; through line L20, where every node between $r$ and the choice is inactive by the definition of "first active node"; or after the node has had its pertinent edges handled and is not externally active (lines L17 to L21 in order). In the last case of line L20, the walk goes down into a child component $r$ of $w$; then $w$ stays on the external face, because the merge inserts the boundary of the component of $r$ at $w$, and the walked side ends at $z$ while the other side comes back to $w$. So every node closed in at step $v$ is not externally active with respect to $v$, and so not active with respect to $v - 1$. Nodes in the components that are not touched keep their place. $\square$

Lemma 2 also justifies WALKUP: at step $v$, a pertinent vertex is active with respect to $v$, so by Lemma 2 for step $v + 1$ it is on the external face of its component, and walking along that face from it reaches the root copy.

## Termination

The outer loop has $n$ rounds. WALKUP stops at the first node marked in the same step, and every round of its loop marks a new node. In WALKDOWN, every round of line L16 either embeds an edge, merges components, moves to a new node of the external face, or leaves the loop; the walk never passes the root $R$, and a component can be entered from a root copy only while that root copy is in a list of pertinent roots, from which line L25 removes it. Every list operation is bounded by the number of edges. So the run ends.

## Completeness

Assume line L7 fails at step $v$: a back edge $(v, w_0)$ with $w_0 \in T(c)$ for a child $c$ of $v$ is not embedded after WALKDOWN$(v, r_c)$. For each of the cases below we find a subdivision of $K_{3,3}$ or $K_5$ in $G$, so $G$ is not planar by [Kuratowski's theorem](/kuratowski-theorem/) (only the easy direction is used: such a subgraph cannot be drawn without crossings).

**Connections.** Three kinds of paths outside the current component are used. If $x$ is externally active, there is a path $P_x$ from $x$ to a vertex $a_x < v$ that is a proper ancestor of $v$: a back edge from $x$, or a path into the subtree of a separate child of $x$ and then a back edge. If $w$ is pertinent, there is such a path $P_w$ from $w$ to $v$. These paths leave the component only through the subtree of a separate child, or by a single back edge, so paths from different vertices of a component are disjoint except at their ends in the ancestors of $v$. Let $Z$ be the tree path between the smallest and the largest of the ends $a_x$; all of it is below $v$, and the tree path from $v$ up to the largest end joins $v$ to $Z$. In the subdivisions below, $Z$ is one branch vertex: take the largest end as the vertex and the rest of $Z$ as parts of the paths into it.

**Lemma 3 (end state).** One of the following holds.

1. *(Blocked in a child.)* WALKDOWN returned at line L23. Then there is a component $D$ whose root copy $r$ is a copy of a vertex $u \ne v$, two nodes $x \ne y$ on its external face that are externally active and not pertinent, and a pertinent vertex $w$ on the part of the external face of $D$ from $x$ to $y$ that does not contain $r$.
2. *(Blocked at the root.)* Both walks of line L14 stopped at line L22, at $x$ for side 0 and at $y$ for side 1, with $x \ne y$. The component $B$ of $r_c$ has a pertinent vertex $w$ on the part of its external face from $x$ to $y$ that does not contain $r_c$, and all nodes strictly between $r_c$ and $x$, and strictly between $r_c$ and $y$, are inactive.

*Proof.* In case 1, let $D$ be the component of the last entry pushed on $S$. After that push, the walk went to the choice of line L20 and stopped there with $S$ not empty. If the choice were pertinent, line L17 would embed an edge and empty $S$, or line L18 would push again. So the choice is not pertinent, and by the choice rule neither is the other first active node; both are active, so both are externally active. The root copy $r$ was in a list of pertinent roots, so WALKUP of this step passed through $D$ from a pertinent node on its external face (Lemma 2), and $D$ was not changed since. That node is not inactive, so it is not between $r$ and $x$ or between $r$ and $y$; it is not $x$ or $y$ either. If $x = y$, every other node on the external face is between $r$ and $x$ on one side, which is impossible, so $x \ne y$. The root copy $r$ is a copy of the vertex $w'$ whose entry was pushed; $w'$ is in the subtree of $c$, so $w' \ne v$.

In case 2, the last edge embedded on side 0 closes in everything walked before it, and every node walked after it was passed at line L21, so it is inactive. The walk stopped at $x$, which is externally active and, after its edges were handled, not pertinent; the same holds for side 1. The edge $(v, w_0)$ was recorded by WALKUP through a node on the external face of $B$ that is pertinent and was never reached by either walk, so it lies on the part from $x$ to $y$, and $x \ne y$ as in case 1. $\square$

**Minor A.** In case 1, $G$ contains a subdivision of $K_{3,3}$ with parts $\{u, w, Z\}$ and $\{x, y, v\}$.

*Proof.* $D$ has at least 3 nodes, because its external face has $r$, $x$, $y$ and $w$, so it is biconnected and its external face is a cycle $C$ with the nodes in the order $r, x, w, y$. The nine paths are: $u - x$ and $u - y$ along $C$ through $r$, which stands for $u$; $w - x$ and $w - y$ along $C$; $w - v$ by $P_w$; $u - v$ by the tree path from $u$ up to $v$, which is outside $T(u)$ except at $u$; $Z - x$ by $P_x$ and $Z - y$ by $P_y$; and $Z - v$ by the tree path. The paths in $D$ use disjoint parts of $C$. $P_x$, $P_y$ and $P_w$ leave $D$ through different subtrees or single edges and end below $v$, at $v$, or at ancestors of $v$. The two tree paths use ancestors of $u$ that are at least $v$, and ancestors of $v$ below it, which are not in $T(u)$. So the paths are internally disjoint. $\square$

**Minor B.** In case 2, if $w$ has a pertinent child component that is also externally active, then $G$ contains a subdivision of $K_{3,3}$ with parts $\{v, w, Z\}$ and $\{x, y, W\}$, where $W$ is a vertex in that child's subtree.

*Proof.* Let $s$ be the child of $w$ with the pertinent, externally active component. In $T(s)$ there is a path to $v$ (pertinence) and a path to an ancestor of $v$ below $v$ (external activity, since $\mathrm{low}(s) < v$). Both start in $T(s)$, which is connected, so they have a common first part from $w$ to a vertex $W$ after which they split. The nine paths are: $v - x$ and $v - y$ along $C$, the external face cycle of $B$, through $r_c$; $w - x$ and $w - y$ along $C$; $w - W$ in $T(s)$; $W - v$ and $W - Z$; $Z - x$ by $P_x$; $Z - y$ by $P_y$. They are internally disjoint for the same reasons as in Minor A. $\square$

**The x-y path.** In case 2 without Minor B, Boyer and Myrvold show that $B$ has a path $P$ between a node $p_x$ on the external face between $r_c$ and $x$ (with $p_x = x$ allowed) and a node $p_y$ between $r_c$ and $y$, with its inner nodes inside $B$, that separates $r_c$ from $w$ in $B$. It comes from the boundary of the faces of $B$ at $r_c$, all of whose nodes were walked in step $v$. This is the place where the argument here is a sketch.

**Minor C.** If $p_x \ne x$ (or, the same with $x$ and $y$ swapped, $p_y \ne y$), then $G$ contains a subdivision of $K_{3,3}$ with parts $\{p_x, w, Z\}$ and $\{v, x, y\}$.

*Proof.* On $C$ the order is $r_c, p_x, x, w, y, p_y$, with $p_x$ strictly between $r_c$ and $x$. The paths are: $p_x - v$ along $C$; $p_x - x$ along $C$; $p_x - y$ by $P$ and then along $C$ from $p_y$ to $y$; $w - x$, $w - y$ along $C$; $w - v$ by $P_w$; $Z - x$, $Z - y$ by $P_x$, $P_y$; and $Z - v$ by the tree path. The parts of $C$ used are disjoint, $P$ is inside $B$, and the other paths are outside $B$. $\square$

**Minors D and E.** If $p_x = x$ and $p_y = y$, Boyer and Myrvold consider a vertex $z$ inside $P$. If there is a path inside $B$ from $z$ to the part of $C$ from $x$ to $y$, it gives a $K_{3,3}$ (Minor D). Otherwise they use the external activity of the vertices on the lower part of $C$ and of $w$: if $w$ is also externally active the result is a $K_5$, and in the remaining subcases a $K_{3,3}$ (Minor E and its variants). These cases are not reproduced here.

**Theorem 2.** BM-PLANAR returns a rotation system if and only if $G$ is planar. If $G$ is not planar it returns nil, and every graph rejected at line L1 is non-planar by the [edge bound](/planar-edge-bound/).

*Proof.* If it returns a rotation system, $G$ is planar by Theorem 1. If $G$ is planar, line L1 does not reject it, and line L7 never fails because a failure gives a Kuratowski subgraph by Lemma 3 and the minors. $\blacksquare$
