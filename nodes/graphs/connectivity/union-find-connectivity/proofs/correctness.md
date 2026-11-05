---
title: Connectivity by union-find stops and labels the connected components
proves: [correctness, termination]
status: full
---

Let $V = \{0, \ldots, n-1\}$ and let $e_1, \ldots, e_m$ be the edges in the order line L2 reads them. Self-loops and repeated edges are allowed. Let $G_i = (V, \{e_1, \ldots, e_i\})$, and write $x \equiv_i y$ when $G_i$ has a path from $x$ to $y$. This is an equivalence relation, and its classes are the components of $G_i$.

For a vertex $x$, the *chain* of $x$ is $x, parent[x], parent[parent[x]], \ldots$. A vertex $r$ with $parent[r] = r$ is a *root*.

**Lemma 1 (ranks).** At every moment, each vertex $x$ that is not a root has $rank[x] < rank[parent[x]]$. So the chain of each vertex reaches a root after at most $n - 1$ steps, and the loops of lines L7 and L8 stop.

*Proof.* After line L1 every vertex is a root, so the claim holds. Only lines L8, L11 and L12 change $parent$ or $rank$.

- Line L11 sets $parent[b] \leftarrow a$, where $a$ and $b$ are distinct roots and, after line L10, $rank[a] \ge rank[b]$. If $rank[a] > rank[b]$ the claim holds for $b$. If they are equal, line L12 raises $rank[a]$ by 1, and then $rank[b] < rank[a]$.
- Line L12 raises only the rank of the root $a$. For a child $c$ of $a$, $rank[c] < rank[a]$ stays true. The ranks of non-roots never change, because lines L11 and L12 change only the ranks of roots and $b$ stops being a root after its rank is fixed.
- Line L8 sets $parent[x] \leftarrow r$, where $r$ is the root that line L7 found at the end of the chain of $x$. Along the chain the ranks strictly increase, by the claim before the step, so $rank[x] < rank[r]$.

So the claim holds at every moment. Along a chain the ranks strictly increase. A rank is at most $n - 1$, because it grows only in line L12, which runs at most once for each LINK, and there are at most $n - 1$ LINK calls (each one makes a root into a non-root, and a non-root never becomes a root again). So a chain has at most $n$ vertices, and line L7 stops. Each step of line L8 moves $x$ one place forward on its own chain toward $r$, so line L8 stops after at most $n - 1$ steps. $\square$

Write $\rho(x)$ for the root at the end of the chain of $x$. Then $\mathrm{FIND}(x)$ returns $\rho(x)$, by line L7.

**Lemma 2 (FIND keeps the roots).** A call of FIND does not change $\rho(y)$ for any vertex $y$.

*Proof.* Line L8 changes $parent[x]$ only for vertices $x$ on the chain of the argument, all of which have $\rho(x) = r$, and it sets $parent[x] = r$. Take any $y$. If its chain does not meet a changed vertex, it is the same as before. Else let $x$ be the first changed vertex on it. Before the change, the chain of $y$ continued from $x$ to $r$, and after it, it goes from $x$ to $r$ in one step. In both cases it ends at $r$. $\square$

**Lemma 3 (LINK merges two classes).** Let $a \ne b$ be roots. After LINK$(a, b)$, $\rho(y)$ is the new parent root for each $y$ that had $\rho(y) \in \{a, b\}$ before, and $\rho(y)$ is unchanged for every other $y$.

*Proof.* After line L10 let the roots be named so that line L11 sets $parent[b] \leftarrow a$. This is the only change of a parent. A chain that ended at $b$ now continues to $a$, which is still a root. A chain that ended at $a$ or at another root does not pass through $b$, because $b$ was a root and a chain stops at its root, so it is unchanged. $\square$

**Theorem.** UF-COMPONENTS stops, and it returns $comp$ with $comp[x] = comp[y]$ if and only if $x$ and $y$ are joined by a path in $G = G_m$.

*Proof.* Every loop stops by Lemma 1, and the loops of lines L2 and L5 have $m$ and $n$ steps. We show by induction on $i$ the invariant

> **(I)** After the first $i$ steps of the loop of line L2, $\rho(x) = \rho(y)$ if and only if $x \equiv_i y$.

*Base.* For $i = 0$, every vertex is its own root, and $G_0$ has no edges, so $x \equiv_0 y$ exactly when $x = y$.

*Step.* Let $e_i = \{u, v\}$, and assume (I) for $i - 1$. Line L3 computes $a = \rho(u)$ and $b = \rho(v)$, and by Lemma 2 it does not change any $\rho$.

First, we compare $\equiv_i$ with $\equiv_{i-1}$. Each path of $G_{i-1}$ is a path of $G_i$. A walk of $G_i$ that uses $e_i$ goes from one end of $e_i$ to the other at that place. So $x \equiv_i y$ if and only if $x \equiv_{i-1} y$, or $x \equiv_{i-1} u$ and $v \equiv_{i-1} y$, or $x \equiv_{i-1} v$ and $u \equiv_{i-1} y$. In words: the classes of $u$ and $v$ in $G_{i-1}$ merge, and every other class stays as it is.

If $a = b$, then $u \equiv_{i-1} v$ by (I), the two classes are one, and $\equiv_i$ equals $\equiv_{i-1}$. Line L4 does nothing, so (I) holds for $i$. This case covers self-loops and repeated edges. If $a \ne b$, the classes of $u$ and $v$ in $G_{i-1}$ are the sets $\{y : \rho(y) = a\}$ and $\{y : \rho(y) = b\}$, by (I). Line L4 calls LINK$(a, b)$, and by Lemma 3 exactly these two sets get one common root, while every other vertex keeps its root. This is the same merge as the one of $\equiv_i$, so (I) holds for $i$.

*End.* After the loop, (I) holds with $i = m$. Line L5 sets $comp[x] = \mathrm{FIND}(x) = \rho(x)$, and by Lemma 2 the calls of line L5 do not change any $\rho$, so all labels are taken from the same root function. So $comp[x] = comp[y]$ if and only if $x \equiv_m y$. $\blacksquare$

**Spanning forest.** Let $T$ be the set of edges that caused a LINK. Each such edge joins two different classes of $\equiv_{i-1}$, so it closes no cycle with the earlier edges of $T$, and $T$ is a forest. The same induction shows that $T$ and $G_i$ have the same classes after each step, so $T$ is a spanning forest of $G$ with $n - c$ edges, where $c$ is the number of components.
