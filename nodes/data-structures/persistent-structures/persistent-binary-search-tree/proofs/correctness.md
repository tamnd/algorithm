---
title: Path-copying insertion and deletion keep the search order and every old version
proves: [correctness]
status: full
---

Write $K(t)$ for the set of keys in the subtree of $t$, with $K(\text{nil}) = \emptyset$. A tree $t$ is a *search tree* if (B1) holds at each node of it. For an interval $I = (a, b)$ with $a < b$ in the order extended by $-\infty$ and $+\infty$, say that $t$ *fits* $I$ if $t$ is a search tree and $K(t) \subseteq I$.

**Lemma 0 (old versions do not change).** Let $v$ be a root that exists at some moment. Then the tree reachable from $v$ is the same at each later moment.

*Proof.* The procedures write fields only in NEW-NODE, which sets the fields of a node that it has just made. So no field of an existing node changes (B2). The tree reachable from $v$ is determined by the fields of the nodes reachable from $v$, which all exist at that moment. $\square$

So we can reason about each call as if it ran on a fixed tree, and its result does not affect any other version.

**Lemma 1 (DESCEND).** Let $t$ be a search tree and $k$ a key. DESCEND$(t, k)$ returns $(path, x)$ where $path = [y_1, \ldots, y_d]$, $y_1 = t$ (if $d \ge 1$), each $y_{i+1}$ is the child of $y_i$ on the side of $k$ (left if $k < y_i.key$, else right), $k \ne y_i.key$ for each $i$, and $x$ is the child of $y_d$ on the side of $k$ (or $x = t$ when $d = 0$). Moreover $x \ne \text{nil}$ exactly when $k \in K(t)$, and then $x.key = k$.

*Proof.* The loop of lines L16 to L18 keeps the statement for the nodes appended so far, with the current $t$ in the role of $x$. It stops when $t = \text{nil}$ or $t.key = k$, and it stops after at most $h$ steps, because each step goes one level down. If it stops at a node of key $k$, then $k \in K(t)$. If it stops at nil, then $k \notin K(t)$: by (B1), at each $y_i$ the key $k$ can only be in the subtree on the side of $k$, so if $k$ were in $K(t)$, it would be in the subtree of the final position, which is empty. $\square$

For the path of Lemma 1, define the interval $I_0 = (-\infty, +\infty)$, and $I_i = (a_i, b_i)$ where $b_i = y_i.key$ and $a_i = a_{i-1}$ if $k < y_i.key$, and $a_i = y_i.key$ and $b_i = b_{i-1}$ otherwise. By (B1), the subtree of the child of $y_i$ on the side of $k$ fits $I_i$, and $k \in I_i$ for each $i$ by induction.

**Lemma 2 (REBUILD).** Let $t$ be a search tree, let $(path, x) = $ DESCEND$(t, k)$ with $d = |path|$, and let $c$ fit $I_d$. Then $r = $ REBUILD$(path, k, c)$ is a search tree with $K(r) = (K(t) \setminus K(x)) \cup K(c)$, where for $d = 0$ we read $r = c$ and $K(t) = K(x)$.

*Proof.* By induction on the iterations of line L20, from $i = d$ down to $i = 1$. Let $c_d = c$, and let $c_{i-1}$ be the copy of $y_i$ that the iteration for $y_i$ makes. We show that $c_{i-1}$ fits $I_{i-1}$ and has the keys $(K(y_i) \setminus K(x)) \cup K(c)$.

Take the case $k < y_i.key$ (line L21); the other case (line L22) is the mirror image. The copy has key $y_i.key$, left child $c_i$ and right child $y_i.right$. The left child fits $I_i = (a_{i-1}, y_i.key)$ by the hypothesis (or by the assumption for $i = d$), so all its keys are below $y_i.key$ and above $a_{i-1}$. The right child is the old right subtree of $y_i$, which is a search tree whose keys are above $y_i.key$ and, since $y_i$ lies in a subtree that fits $I_{i-1}$, below $b_{i-1}$. And $y_i.key \in I_{i-1}$ for the same reason. So the copy is a search tree and fits $I_{i-1}$. Its keys are $\{y_i.key\} \cup K(y_i.right) \cup K(c_i)$. The old subtree had $\{y_i.key\} \cup K(y_i.right) \cup K(y_{i+1})$ (with $x$ in place of $y_{i+1}$ for $i = d$), and by the hypothesis $K(c_i) = (K(y_{i+1}) \setminus K(x)) \cup K(c)$, which gives the claim, because $K(x) \subseteq K(y_{i+1})$ is disjoint from $\{y_i.key\} \cup K(y_i.right)$.

At $i = 1$ we get $r = c_0$, which fits $I_0$ and has the keys $(K(t) \setminus K(x)) \cup K(c)$. $\square$

**Theorem 1 (INSERT).** If $t$ is a search tree, INSERT$(t, k)$ returns a search tree with keys $K(t) \cup \{k\}$, and $t$ is unchanged.

*Proof.* If $k \in K(t)$, Lemma 1 gives $x \ne \text{nil}$, and line L5 returns $t$. Else $x = \text{nil}$, so $K(x) = \emptyset$, and the leaf with key $k$ fits $I_d$ because $k \in I_d$. Lemma 2 gives a search tree with keys $K(t) \cup \{k\}$. Lemma 0 gives that $t$ is unchanged. $\square$

**Theorem 2 (DELETE).** If $t$ is a search tree, DELETE$(t, k)$ returns a search tree with keys $K(t) \setminus \{k\}$, and $t$ is unchanged.

*Proof.* If $k \notin K(t)$, line L8 returns $t$. Else $x$ is the node of key $k$, and the subtree of $x$ fits $I_d$. We build $c$ that fits $I_d$ with $K(c) = K(x) \setminus \{k\}$. Then Lemma 2 gives the result.

If $x.left = \text{nil}$ (line L9), $c = x.right$ is a subtree of $x$, so it fits $I_d$, and $K(c) = K(x) \setminus \{k\}$. Line L10 is the mirror image.

If $x$ has two children (lines L11 to L13), let $y$ be the last node of the left steps from $x.right$, so $y.left = \text{nil}$ and $y.key$ is the least key of $K(x.right)$. Let $q$ be the nodes before $y$ on these steps. This is the path that DESCEND$(x.right, y.key)$ returns, with $y$ as its node: at each node of $q$, $y.key$ is smaller, so the search goes left. By Lemma 2 applied to the search tree $x.right$ with $c = y.right$ (which fits the interval of $y$ on that path, being a subtree of $y$), the tree $r' = $ REBUILD$(q, y.key, y.right)$ is a search tree with keys $K(x.right) \setminus \{y.key\}$. The new node of line L13 has key $y.key$, left child $x.left$, whose keys are below $k < y.key$, and right child $r'$, whose keys are in $K(x.right)$ and greater than the least one, $y.key$. So it is a search tree, with keys $K(x.left) \cup K(x.right) = K(x) \setminus \{k\}$, all in $I_d$. $\square$

**Corollary (full persistence).** For each sequence of operations in which each update takes any earlier version, every version $v$ is at the end a search tree whose key set is the result of applying, in order, the updates on the chain from the empty tree to $v$, and SEARCH$(v, k)$ returns true exactly when $k$ is in this set.

*Proof.* By induction on the number of updates, with Theorems 1 and 2 for the step and Lemma 0 for the fact that later updates change no earlier version. SEARCH returns $x \ne \text{nil}$ at line L3 with the same loop as DESCEND, so by Lemma 1 it is right. $\blacksquare$
