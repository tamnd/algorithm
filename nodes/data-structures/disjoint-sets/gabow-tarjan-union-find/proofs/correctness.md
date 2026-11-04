---
title: The Gabow-Tarjan structure returns the nearest unlinked ancestor
proves: [correctness, termination]
status: full
---

Write $\mathrm{ans}(v)$ for the nearest ancestor of $v$ in $T$, $v$ included, that is not linked. The root of $T$ is never linked, so $\mathrm{ans}(v)$ exists. Links are never undone, so the set of linked nodes only grows.

**Lemma 1 (cutting).** After INIT: (a) each node is in exactly one microset; (b) each microset $S$ has at most $b$ nodes; (c) for each $x \in S$, $x.p \in S$ or $x.p = r(S)$, and if $r(S) = \mathrm{NONE}$ then $S$ contains the root of $T$; (d) if $x.p \in S$ then $x.p$ has a smaller number than $x$; (e) the number of microsets is at most $2n/b + 1$.

*Proof.* Call the list held by a node $v$ after its step its *open list*. By induction from the leaves up: the open list of $v$ starts with $v$, is a connected set of nodes whose top is $v$, lists each node after its parent, and has fewer than $h + 1$ nodes, where $h = \lceil b/2 \rceil$. Indeed, $v$ concatenates the open lists of some of its children into $G$, each of size at most $h$, closing $G$ when $|G| \ge h$, so the part left has fewer than $h$ nodes, and $v$ is put in front. Each closed group is a concatenation of open lists of children of $v$, each a connected set with top a child of $v$ and in parent-first order, which gives (c) with $r(S) = v$ and (d). Its size is at least $h$, and at most $(h - 1) + h \le b$, because $G$ had fewer than $h$ nodes before the last list was added; this gives (b). The root closes its own open list with root NONE, a connected set with top the root of $T$, of size at most $h \le b$. Each node is put in exactly one open list, and moves with it until that list is closed, which gives (a). All closed groups but the last have at least $h \ge b/2$ nodes, which gives (e). $\square$

A *piece* of $S$ is a maximal part of $S$ connected by parent edges inside $S$. By (c), the top $t$ of a piece has $t.p = r(S)$, or $t$ is the root of $T$. INIT computes $\mathrm{anc}(x)$ in the order of the numbers, so by (d) the value for $x.p$ is ready, and $\mathrm{anc}(x)$ is the set of nodes on the path from $x$ up to the top of its piece.

**Lemma 2 (micro find).** $M(S)$ is always the set of linked nodes of $S$, by line L5. MICRO-FIND$(x)$ returns the deepest unlinked node on the path from $x$ to the top of its piece, or NONE if all of them are linked. If it returns a node, that node is $\mathrm{ans}(x)$.

*Proof.* $u = \mathrm{anc}(x) \setminus M(S)$ is the set of unlinked nodes on that path. The nodes of the path have numbers that grow with depth, by (d), so the largest number in $u$ is the deepest of them, the first one met when walking up from $x$. All nodes below it on the path are linked, so it is $\mathrm{ans}(x)$. $\square$

Call $x$ *exhausted* when MICRO-FIND$(x)$ is NONE. This is permanent, since marks only grow.

**Lemma 3 (leaving a microset).** If $x$ is exhausted, then $r(S(x)) \ne \mathrm{NONE}$ and $\mathrm{ans}(x) = \mathrm{ans}(r(S(x)))$.

*Proof.* All nodes from $x$ to the top $t$ of its piece are linked. The root of $T$ is never linked, so $t$ is not the root, and $t.p = r(S(x))$ by (c). The walk from $x$ to $\mathrm{ans}(x)$ passes through $t$ and continues at $t.p$, so $\mathrm{ans}(x) = \mathrm{ans}(t.p)$. $\square$

**Invariant (N) of the macro forest.** For each macro set $X$ with name $z$: $z \in X$, and every $y \in X$ with $y \ne z$ is exhausted and has $r(S(y)) \in X$.

*Consequence.* Let $y \in X$. Follow $y, r(S(y)), r(S(r(S(y)))), \ldots$ while the current node is not $z$. By (N) each step stays in $X$, and each step goes to a proper ancestor, so the walk is finite and must stop, which happens only at $z$. By Lemma 3, which holds at every moment, each step keeps the answer. So, at every moment, $z$ is an ancestor of every member of $X$ (or equal to it), and $\mathrm{ans}(y) = \mathrm{ans}(z)$ for every $y \in X$.

At INIT every set is $\{y\}$ with name $y$, so (N) holds. A link changes no macro set, and exhaustion is permanent, so (N) stays true. Path compression and union by size change neither the sets nor the names.

*Line L12.* Here $z$ is the name of its set $X$, and $z$ is exhausted. Let $y = r(S(z))$, which is not NONE by Lemma 3, so $y \in R$; it is a proper ancestor of $z$. Let $Y$ be its set, with name $z'$, which is an ancestor of $y$ by the consequence. If $Y = X$, then $z$ would be an ancestor of $y$, a proper ancestor of $z$, which is impossible. So $X \ne Y$ and the union merges two sets, with the name $z'$. For the merged set: the members of $Y$ other than $z'$ satisfy (N) as before; the members of $X$ other than $z$ are exhausted and have their $r(S(\cdot))$ in $X$, which is in the merged set; and $z$ is exhausted with $r(S(z)) = y$ in the merged set. So (N) holds.

**FIND is correct.** If line L9 returns, the answer is right by Lemma 2. Otherwise $v$ is exhausted and $\mathrm{ans}(v) = \mathrm{ans}(r(S(v)))$ by Lemma 3. Line L10 sets $z$ to the name of the set of $r(S(v))$, so $\mathrm{ans}(z) = \mathrm{ans}(v)$ by the consequence of (N). The loop keeps $\mathrm{ans}(z) = \mathrm{ans}(v)$, because line L12 keeps (N) and line L13 takes the new name. When the loop stops, $w = $ MICRO-FIND$(z) \ne \mathrm{NONE}$, and $w = \mathrm{ans}(z) = \mathrm{ans}(v)$ by Lemma 2.

**Termination.** Each pass through lines L12 and L13 merges two different macro sets, so the loop runs at most $|R| - 1$ times over the whole run. MICRO-FIND and LINK take $O(1)$ steps, and the macro finds terminate because the macro forest is a forest. INIT walks each node a constant number of times. $\blacksquare$
