---
title: The Holm-de Lichtenberg-Thorup algorithm keeps a spanning forest
proves: [correctness]
status: full
---

We prove that after every operation $F_0$ is a spanning forest of the current graph $G$, so that line L12 answers correctly. We prove it together with the invariants of the page. Write $G_i$ for the graph of edges of level at least $i$, $F$ for the set of tree edges, and $F_i = F \cap G_i$.

- **(I0)** $F$ is a forest, every edge of $F$ is an edge of $G$, and $F_0 = F$.
- **(I1)** For every non-tree edge $f$ of level $j$, the ends of $f$ are connected in $F_j$.
- **(I2)** Every tree of $F_i$ has at most $n / 2^i$ vertices.

We first show that (I0) and (I1) are enough for the claim.

**Lemma 1.** If (I0) and (I1) hold, then for every $i$, $F_i$ is a spanning forest of $G_i$, and in particular $F_0$ is a spanning forest of $G$.

*Proof.* $F_i \subseteq G_i$ and $F_i$ is a forest by (I0). Every edge of $G_i$ is either in $F_i$ or a non-tree edge of level $j \ge i$, whose ends are connected in $F_j \subseteq F_i$ by (I1). So every edge of $G_i$ has its ends in one tree of $F_i$, and $F_i$ has the same components as $G_i$. $\square$

So it suffices to prove that every operation keeps (I0), (I1) and (I2). They hold for the empty graph.

**Lemma 2 (insertion).** INSERT keeps (I0), (I1) and (I2).

*Proof.* If $u$ and $v$ are in different trees of $F_0$, line L2 adds $\{u, v\}$ at level 0. Then $F$ stays a forest, and only $F_0$ changes. Its new tree joins two trees, but (I2) at level 0 only asks for at most $n$ vertices. Non-tree edges keep their levels and their paths in $F_j$ only grow. Otherwise $\{u, v\}$ is a non-tree edge of level 0 whose ends are connected in $F_0$, so (I1) holds for it, and the forests do not change. $\square$

**Lemma 3 (deleting a non-tree edge).** Line L3 keeps the invariants.

*Proof.* The forests do not change, and (I1) is a statement about each remaining non-tree edge separately. $\square$

Now let $e = \{u, v\}$ be a tree edge of level $\ell$ that is deleted. Line L4 removes $e$ from $F$, so $F_j$ loses $e$ for $j \le \ell$ and is unchanged for $j > \ell$. For each $i \le \ell$ let $A_i$ and $B_i$ be the trees of $F_i - e$ that contain $u$ and $v$; they are the two halves of the tree of $F_i$ that contained $e$.

**Lemma 4.** Before the search, (I0) and (I2) hold, and (I1) holds for every non-tree edge except possibly those whose ends lie in different halves $A_j$ and $B_j$ at their level $j \le \ell$.

*Proof.* Removing an edge keeps a forest a forest and makes trees smaller. A non-tree edge $f$ of level $j$ had its ends connected in $F_j$. If $j > \ell$, then $F_j$ did not change. If $j \le \ell$ and the path in $F_j$ between the ends of $f$ did not use $e$, it is still there. If it used $e$, the ends of $f$ lie one in $A_j$ and one in $B_j$. $\square$

Call a non-tree edge **crossing at level $j$** if it has level $j$ and its ends are one in $A_j$ and one in $B_j$. Note that $A_j \subseteq A_{j-1}$ and $B_j \subseteq B_{j-1}$, since $F_j \subseteq F_{j-1}$.

**Lemma 5 (the loop at level $i$).** Suppose the loop of lines L5 to L10 starts level $i$ and, at that moment, (I0) and (I2) hold, (I1) holds for every non-tree edge of level greater than $i$, and there is no crossing edge at any level greater than $i$. Then either the iteration ends at line L9 with all invariants restored, or it ends with no crossing edge at level $i$, (I0) and (I2) hold, and (I1) holds for every non-tree edge of level at least $i$.

*Proof.* Line L6 names $T_u$ and $T_v$, which are $A_i$ and $B_i$ in some order; relabel so that $T_u$ is the smaller. Since $T_u \cup T_v$ is the vertex set of one tree of $F_i$ before the cut, (I2) gives $|T_u| + |T_v| \le n / 2^i$, so $|T_u| \le n / 2^{i+1}$.

*Line L7.* The tree edges of level $i$ in $T_u$ rise to level $i + 1$ and are linked in $F_{i+1}$. All edges of $T_u$ now have level at least $i + 1$, so $T_u$ is a single tree of $F_{i+1}$, made of the trees of $F_{i+1}$ inside $T_u$ joined by the raised edges. It has at most $n / 2^{i+1}$ vertices, so (I2) holds at level $i + 1$. Other trees of $F_{i+1}$ are unchanged. $F$ itself does not change, so (I0) holds. Raising tree edges only adds edges to $F_{i+1}$, so (I1) still holds for every edge for which it held.

*Lines L8 to L10.* Take a non-tree edge $f$ of level $i$ with an end $x$ in $T_u$ and let $y$ be the other end. If $f$ is not crossing at level $i$, then by Lemma 4 its ends are connected in $F_i - e$, so $y \in T_u$. If $f$ is crossing, then $y \in T_v$. So the test of line L9 is true exactly for crossing edges.

If $y \in T_u$, line L10 raises $f$ to level $i + 1$. Its ends are in $T_u$, which is a tree of $F_{i+1}$, so (I1) holds for $f$. Nothing else changes.

If $y \in T_v$, line L9 makes $f$ a tree edge of level $i$ and links it in $F_0, \ldots, F_i$. Then $F$ stays a forest, because $f$ joins $A_0 \supseteq T_u$ and $B_0 \supseteq T_v$ (in some order), which are different trees of $F_0 - e$. So (I0) holds. For (I2), $F_j$ changes only for $j \le i$, where its tree $A_j \cup B_j$ is joined again by $f$; this tree has vertex set equal to that of the tree of $F_j$ that held $e$, which had at most $n / 2^j$ vertices. For (I1), take any non-tree edge $g$ of level $j$. If $j > i$, (I1) held by assumption or by the steps above. If $j \le i$, then in $F_j$ the halves $A_j$ and $B_j$ are joined again by $f$, and every other tree of $F_j$ is unchanged, so the ends of $g$, which were in one tree of $F_j$ before $e$ was cut, are in one tree again. So all invariants hold, and the deletion ends.

If the scan ends without line L9, every non-tree edge of level $i$ with an end in $T_u$ has been raised, so no crossing edge of level $i$ is left; one crossing at level $i$ would have an end in $T_u$ and would have been found. Every remaining non-tree edge of level $i$ is not crossing, so (I1) holds for it by Lemma 4, and the raised edges satisfy (I1) as shown. $\square$

**Lemma 6.** A non-tree edge of level $j > \ell$ is never crossing.

*Proof.* Its level is greater than the level of $e$, so $F_j$ did not contain $e$, and by (I1) before the deletion its ends are connected in $F_j \subseteq F_i - e$ for every $i \le \ell$, so they lie in one tree of $F_i - e$. Raising edges during the search moves edges to level at most $\ell + 1$ with both ends in one tree of $F_{\ell+1}$, so this stays true. $\square$

**Theorem.** After every operation, (I0), (I1) and (I2) hold, so $F_0$ is a spanning forest of $G$ and CONNECTED is correct.

*Proof.* By induction on the operations. Insertions and deletions of non-tree edges are Lemmas 2 and 3. For the deletion of a tree edge $e$ of level $\ell$, Lemmas 4 and 6 give the assumption of Lemma 5 at $i = \ell$, and each iteration of Lemma 5 that does not return gives the assumption for $i - 1$. If some iteration returns at line L9, the invariants hold. Otherwise, after level 0, there is no crossing edge at any level, (I0) and (I2) hold, and (I1) holds for every non-tree edge. In that case no edge of $G$ joins $A_0$ and $B_0$: tree edges do not, since $A_0$ and $B_0$ are different trees of $F$, and a non-tree edge of level $j$ has its ends connected in $F_j \subseteq F_0$ by (I1), so both ends lie in one tree of $F_0$. So the component of $e$ is split in $G$ as in $F_0$ (line L11). By Lemma 1, $F_0$ is a spanning forest of $G$, and $u$ and $v$ are connected in $G$ exactly when they are in one tree of $F_0$. $\blacksquare$
