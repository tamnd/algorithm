---
title: Splay tree operations keep the binary search tree and return the right answers
proves: [correctness, termination]
status: full
---

We use the result of [splaying](/splaying/): SPLAY$(T, x)$ ends, keeps the strict BST property, the in-order sequence and the parent links, and makes $x$ the root. Write $D$ for the set of keys of $T$.

**Lemma 1 (access).** After ACCESS$(T, k)$ with $D \ne \emptyset$, the root is the node of $k$ if $k \in D$; otherwise the root key is $\mathrm{floor}(k) = \max\{d \in D : d < k\}$ or $\mathrm{ceiling}(k) = \min\{d \in D : d > k\}$. ACCESS returns the node of $k$ or NIL, correctly.

*Proof.* The loop of line L2 is the BST search; if $k \in D$ it stops at the node of $k$ and line L4 splays it. If $k \notin D$, the search ends at NIL below the last node $\ell$ of the path. If the search left $\ell$ to the left, then $k < \ell.key$ and the left subtree of $\ell$ is empty. Suppose some key $d \in D$ lies strictly between $k$ and $\ell.key$. For each node $v \ne \ell$ on the path, $k$ and $\ell.key$ are on the same side of $v.key$, because $\ell$ is in the subtree that the search for $k$ entered at $v$. So $v.key$ is not in the closed range from $k$ to $\ell.key$, and $d$ is on the same side of $v.key$ as $k$. Hence $d$ is in the subtree that the search entered at each $v$, so it is in the subtree of $\ell$, and as $d < \ell.key$ it is in the empty left subtree of $\ell$, a contradiction. So $\ell.key = \mathrm{ceiling}(k)$. The case to the right gives the floor. Splaying $\ell$ makes it the root. Line L5 tests the root key against $k$. $\square$

**Insert.** If $k \in D$, line L7 returns and the set does not change. Otherwise, by Lemma 1, the root $r$ is the floor or the ceiling of $k$. If $k < r.key$, then $r$ is the ceiling, so every key in the left subtree of $r$ is less than $r.key$ and not in $(k, r.key)$, hence less than $k$; the keys of $r$ and its right subtree are greater than $k$. So the tree with root $z$, left subtree the old left subtree of $r$, and right subtree $r$ (without its left subtree) has the BST property at $z$, and at $r$ (which lost only a subtree). The case $k > r.key$ is the mirror image. Line L11 sets the parent links. The new key set is $D \cup \{k\}$.

**Join.** Let all keys of $L$ be less than all keys of $R$. If $L = $ NIL the answer is $R$. Otherwise the maximum $m$ of $L$, after the splay, is the root of $L$; it has no right child, since a right child would have a larger key. Hanging $R$ as its right subtree keeps the BST property at $m$, as all keys of $R$ exceed $m.key$, and at every other node the subtrees are unchanged.

**Delete.** If ACCESS returns NIL, $k \notin D$ and nothing changes in the set. Otherwise the root holds $k$, its left subtree $L$ holds exactly the keys less than $k$ and its right subtree $R$ the keys greater than $k$. So JOIN$(L, R)$ is legal and gives a BST on $D \setminus \{k\}$.

**Split.** After ACCESS, the root $r$ is the node of $k$, or its floor or ceiling, by Lemma 1. If $r.key \le k$, then $r$ is $k$ or its floor, so each key of the right subtree of $r$ is greater than $k$ (a key in $(r.key, k]$ would contradict the choice of $r$), and each key of $r$ and its left subtree is at most $r.key \le k$. So line L19 splits $D$ into the keys $\le k$ and $> k$. If $r.key > k$, then $r$ is the ceiling, so every key in the left subtree of $r$ is less than $k$, and line L20 splits correctly.

**Termination.** Each search walks down a finite tree, each splay ends, and the walk to the maximum in line L16 walks down a finite tree. $\blacksquare$
