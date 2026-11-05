---
title: Tarjan's offline LCA algorithm answers every query correctly
proves: [correctness, termination]
status: full
---

Let $T$ be a tree with the vertices $0, \ldots, n-1$, rooted at $r$, and let $p(v)$ be the parent of $v \ne r$. Write $T_v$ for the subtree of $v$, and $u \preceq v$ when $u$ is an ancestor of $v$ (each vertex is an ancestor of itself). The algorithm is TARJAN-OFFLINE-LCA with the lines L1 to L11.

**Lemma 1 (the search).** The stack $S$ always holds the path from $r$ to its top vertex, with the parent of each entry below it. Each vertex is pushed exactly once and popped exactly once, and a vertex $v$ is popped at line L8 only after every vertex of $T_v \setminus \{v\}$ has been popped.

*Proof.* Line L6 pushes a child $c$ of the top $v$, so the path property holds after a push, and a pop removes the last vertex of the path. A vertex $c \ne r$ is pushed only from its parent, at most once per edge $\{p(c), c\}$, because each neighbour of $v$ is taken once. The vertex $v$ is popped only when it has no neighbour left to take, that is, after each child $c$ was pushed and, since $c$ lies above $v$ on the stack, popped again. By induction on the height of $v$, every vertex of $T_c$ was popped before $c$. Each vertex is pushed: by induction on the depth, a child $c$ of $v$ is taken before $v$ is popped. $\square$

**Termination.** Each iteration of line L4 either pushes a vertex or pops one. By Lemma 1 there are $n$ pushes and $n$ pops, so the loop stops after $2n$ iterations.

Call a vertex *open* when it is on $S$, and *done* when it has been popped. For a done vertex $w$, let $a(w)$ be the lowest open ancestor of $w$, if one exists.

**Lemma 2 (the invariant).** At the start of each iteration of line L4, and also during line L9 for a vertex $v$, the following hold.

(a) For each open vertex $x$, the set of $x$ is $\{x\}$ together with the subtrees $T_c$ of the children $c$ of $x$ that are done.

(b) For each done vertex $w$ with an open ancestor, the set of $w$ is the set of $a(w)$, and its label is $a(w)$.

During line L9 for $v$, the vertex $v$ is done but not yet merged, and (a) holds for $v$ as if it were open: the set of $v$ is $T_v$, with the label $v$.

*Proof.* At the start every set is a single vertex with its own label, and no vertex is done, so (a) and (b) hold. A push of $c$ changes no set, and $c$ has no done child yet, so its set $\{c\}$ fits (a).

Consider the pop of $v$ with parent $p$. Just before it, by Lemma 1 all children of $v$ are done, so by (a) the set of $v$ is $T_v$, and its label is $v$: by (b) for a done $w \in T_v$, $a(w) = v$ because $v$ is open and every vertex between $w$ and $v$ is done. This is the claim during line L9.

At line L10, UNION$(p, v)$ joins the set of $p$, which by (a) is $\{p\}$ and the subtrees of the done children of $p$, with $T_v$. The child $v$ is now done, so the new set is what (a) asks for $p$. The label of the new set becomes $p$. For each $w \in T_v$, now done, the lowest open ancestor is $p$, since $v$ is no longer open and $p$ is. For each done $w$ in an older subtree of a child of $p$, $a(w) = p$ is unchanged. All other sets are unchanged, and the open status of no other vertex changes. So (a) and (b) hold after the pop. If $v = r$, line L10 does nothing and no open vertex is left. $\square$

**Lemma 3 (the answer).** Let line L9 run for $v$, and let $w$ be done. Then $\mathit{anc}[\mathrm{FIND}(w)] = \mathrm{lca}(v, w)$.

*Proof.* At this moment the open vertices are the proper ancestors of $v$, and $v$ itself counts as open for its set, as Lemma 2 says. If $w \in T_v$, then $\mathrm{lca}(v, w) = v$, and the set of $w$ is $T_v$ with the label $v$.

Otherwise $w \notin T_v$. The root is an ancestor of $w$ and is open, so $a(w)$ exists, and by Lemma 2(b) the label of the set of $w$ is $a(w)$, the lowest vertex of the path from $r$ to $p(v)$ that is an ancestor of $w$. Every vertex of this path is an ancestor of $v$. So $a(w)$ is a common ancestor of $v$ and $w$. Every common ancestor of $v$ and $w$ that is not $v$ lies on the path from $r$ to $p(v)$, and $v$ is not a common ancestor because $w \notin T_v$. So $a(w)$ is the lowest common ancestor. $\square$

**Theorem.** TARJAN-OFFLINE-LCA stops, and for each query $i = (u, v)$ it returns $\mathrm{lca}(u, v)$ in $\mathit{ans}[i]$.

*Proof.* It stops by the termination argument. By line L2, the query $i$ is stored at $u$ and at $v$. Each vertex is popped once (Lemma 1). If $u = v$, then when $v$ is popped, line L8 marks $v$ done before line L9, and Lemma 3 with $w = v$ gives $\mathit{anc}[\mathrm{FIND}(v)] = v = \mathrm{lca}(v, v)$. If $u \ne v$, let $v$ be the one popped second. At the pop of $u$, $v$ is not done, so line L9 writes nothing for $i$ there; at the pop of $v$, $u$ is done, and Lemma 3 gives $\mathit{ans}[i] = \mathrm{lca}(v, u)$. No later step writes $\mathit{ans}[i]$, since both entries of the query are read only at these two pops. $\blacksquare$
