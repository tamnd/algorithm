---
title: The virtual tree build returns the vertices and the parents of the virtual tree
proves: [correctness, termination]
status: full
---

Let $T$ be a tree rooted at $r$, with the preorder positions $\mathrm{tin}$, and let $K$ be a non-empty set of vertices. Write $u \preceq v$ when $u$ is an ancestor of $v$ (each vertex is its own ancestor), and $\overline{K} = \{\mathrm{lca}(x, y) : x, y \in K\}$, which contains $K$ since $\mathrm{lca}(x, x) = x$. The build is BUILD-VIRTUAL-TREE with the lines L1 to L8.

**Termination.** Every line is a sort, a loop with a fixed bound, or a single step, so the build stops.

**Fact 1 (intervals).** The subtree of $u$ is the set of vertices whose preorder positions form the interval $I(u) = [\mathrm{tin}(u), \mathrm{tin}(u) + s(u) - 1]$. So (a) $u \preceq v$ implies $\mathrm{tin}(u) \le \mathrm{tin}(v)$, with equality only for $u = v$; and (b) if $u \preceq w$ and $\mathrm{tin}(u) \le \mathrm{tin}(v) \le \mathrm{tin}(w)$, then $u \preceq v$, because $I(u)$ contains $\mathrm{tin}(u)$ and $\mathrm{tin}(w)$, and so every position between them.

**Lemma 1 (adjacent LCAs).** Let $x_1, \ldots, x_b$ be distinct vertices sorted by $\mathrm{tin}$, and $1 \le i < j \le b$. Let $\ell_t = \mathrm{lca}(x_t, x_{t+1})$. Then $\mathrm{lca}(x_i, x_j)$ is the shallowest of $\ell_i, \ldots, \ell_{j-1}$, and it equals $\mathrm{lca}(x_i, x_{i+1}, \ldots, x_j)$.

*Proof.* Let $c = \mathrm{lca}(x_i, x_j)$. By Fact 1(b) with $u = c$ and $w = x_j$, $c \preceq x_t$ for every $i \le t \le j$. So $c \preceq \ell_t$ for every $t$, and $c = \mathrm{lca}(x_i, \ldots, x_j)$, since a common ancestor of all of them is one of $x_i$ and $x_j$. Each $\ell_t$ is at least as deep as $c$. Now suppose every $\ell_t$ is strictly deeper than $c$. Then each $\ell_t$ lies in the subtree of one child of $c$, and $\ell_t$ is an ancestor of both $x_t$ and $x_{t+1}$, so $x_t$ and $x_{t+1}$ lie below the same child of $c$. By induction on $t$, all of $x_i, \ldots, x_j$ lie below the same child of $c$, which is then a common ancestor of $x_i$ and $x_j$ deeper than $c$, a contradiction. So some $\ell_t$ has the depth of $c$, and being a descendant of $c$, it equals $c$. $\square$

**Lemma 2 (closure).** The set $A$ after line L4 is $\overline{K}$, and $\overline{K}$ is closed under LCA: $\mathrm{lca}(a, a') \in \overline{K}$ for all $a, a' \in \overline{K}$.

*Proof.* Line L1 lists the distinct keys $x_1, \ldots, x_b$ in preorder, and line L3 adds $\ell_1, \ldots, \ell_{b-1}$. Each $\ell_t$ is in $\overline{K}$. Conversely, each $\mathrm{lca}(x_i, x_j)$ with $i < j$ is some $\ell_t$ by Lemma 1, and $\mathrm{lca}(x_i, x_i) = x_i$ is a key. So the set of line L4 is $\overline{K}$.

For closure, let $a = \mathrm{lca}(x_i, x_j)$ and $a' = \mathrm{lca}(x_{i'}, x_{j'})$. Then $\mathrm{lca}(a, a')$ is the LCA of the set $X = \{x_i, x_j, x_{i'}, x_{j'}\}$. The LCA of a set of keys is a common ancestor of all of them, and by the argument of Lemma 1 it equals the LCA of the first and the last of them in preorder, which is in $\overline{K}$. $\square$

**Lemma 3 (parents).** Let $A[0], \ldots, A[m-1]$ be $\overline{K}$ sorted by $\mathrm{tin}$. Then $A[0] = \mathrm{lca}(K)$, and for $i \ge 1$ the nearest proper ancestor of $A[i]$ in $\overline{K}$ is $c = \mathrm{lca}(A[i-1], A[i])$.

*Proof.* $\mathrm{lca}(K)$ is in $\overline{K}$ by Lemma 1 (with $i = 1$, $j = b$) and is an ancestor of every vertex of $\overline{K}$, so by Fact 1(a) its position is the smallest, and it is $A[0]$.

Let $i \ge 1$, $a = A[i]$, $a^- = A[i-1]$. By Lemma 2, $c \in \overline{K}$, and $c \preceq a$. If $c = a$, then $a \preceq a^-$, and Fact 1(a) gives $\mathrm{tin}(a) < \mathrm{tin}(a^-)$, against the order. So $c$ is a proper ancestor of $a$ in $\overline{K}$. Suppose $x \in \overline{K}$ is a proper ancestor of $a$ and strictly deeper than $c$. Then $\mathrm{tin}(x) < \mathrm{tin}(a)$ by Fact 1(a), and since $a^-$ is the element of $\overline{K}$ just before $a$, $\mathrm{tin}(x) \le \mathrm{tin}(a^-) < \mathrm{tin}(a)$. By Fact 1(b) with $u = x$, $w = a$, $x \preceq a^-$. So $x$ is a common ancestor of $a^-$ and $a$ deeper than their LCA $c$, a contradiction. So $c$ is the nearest proper ancestor of $a$ in $\overline{K}$. $\square$

**Theorem.** BUILD-VIRTUAL-TREE$(K)$ returns the vertex set $\overline{K}$ of the virtual tree $V(K)$ in preorder, sets $\mathrm{par}[0] = \mathrm{NIL}$ for its root $\mathrm{lca}(K)$, and gives each other vertex its parent in $V(K)$. The virtual tree has at most $2k - 1$ vertices.

*Proof.* By Lemma 2 the list of line L4 is $\overline{K}$ in preorder. Line L5 marks $A[0]$, which is $\mathrm{lca}(K)$ by Lemma 3, as the root. Line L7 sets the parent of $A[i]$ to $\mathrm{lca}(A[i-1], A[i])$, which by Lemma 3 is the nearest proper ancestor of $A[i]$ in $\overline{K}$, the parent in the definition of $V(K)$. Line L2 starts with $b \le k$ vertices and line L3 adds $b - 1$, so $m \le 2b - 1 \le 2k - 1$. $\blacksquare$
