---
title: Search, insert and delete keep the B-tree properties and give the right answers
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page and the minimum degree $t \ge 2$. The keys are distinct. For a node $x$, $S(x)$ is the set of keys in the subtree of $x$, and $\mathrm{ht}(x)$ is the number of edges from $x$ down to a leaf of its subtree. A subtree is *valid* if it satisfies these properties at each of its nodes $y$:

> **(B1)** $y.key[1] < \cdots < y.key[y.n]$ and $y.n \le 2t - 1$. If $y$ is internal, it has $y.n + 1$ children.
> **(B2)** If $y$ is internal, each key of $S(y.c[i])$ is larger than $y.key[i-1]$ (when $i \ge 2$) and smaller than $y.key[i]$ (when $i \le y.n$).
> **(B3)** All leaves of the subtree of $y$ have the same depth.
> **(B4)** $y.n \ge t - 1$, except at the root of the subtree, where $y.n \ge 1$ if $y$ is internal.

A tree is a B-tree when the subtree of its root is valid. By (B2), an in-order walk lists $S(y)$ in increasing order, and $\mathrm{ht}(y.c[i]) = \mathrm{ht}(y) - 1$ for each child, by (B3).

**Lemma 1 (search).** If the subtree of $x$ is valid, B-TREE-SEARCH$(x, k)$ returns $(x', i)$ with $x'.key[i] = k$ when $k \in S(x)$, and NIL otherwise. It makes at most $\mathrm{ht}(x)$ disk reads.

*Proof.* By induction on $\mathrm{ht}(x)$. Lines L1 and L2 stop at the least $i$ with $i > x.n$ or $k \le x.key[i]$. So $x.key[i-1] < k$ when $i \ge 2$, and $k \le x.key[i]$ when $i \le x.n$. If line L3 finds $k = x.key[i]$, the answer is right. Otherwise $k$ is not a key of $x$, because the keys of $x$ before position $i$ are smaller than $k$ and those from position $i$ on are larger. If $x$ is a leaf, $S(x)$ is the keys of $x$, and line L4 returns NIL correctly. If $x$ is internal, by (B2) every key of $S(x)$ that lies strictly between $x.key[i-1]$ and $x.key[i]$ is in $S(x.c[i])$, and $k$ lies there, so $k \in S(x)$ if and only if $k \in S(x.c[i])$. The child has height $\mathrm{ht}(x) - 1$, and its subtree is valid (with the weaker root rule of (B4), which the search does not use). The induction hypothesis gives the answer, with at most $\mathrm{ht}(x) - 1$ reads, plus the one read of line L5. In the base case $\mathrm{ht}(x) = 0$, $x$ is a leaf and no read happens. $\square$

**Lemma 2 (split).** Let $x$ be an internal node that is not full, and let $y = x.c[i]$ be full, with $2t - 1$ keys. After SPLIT-CHILD$(x, i)$, the subtree of $x$ has the same key set and the same leaf depths, $y$ and the new node $z$ have $t - 1$ keys each, $x$ has one key more, and (B1) to (B3) still hold at each node.

*Proof.* Write $a_1 < \cdots < a_{2t-1}$ for the keys of $y$ and $T_1, \ldots, T_{2t}$ for its child subtrees, if any. Lines L14 to L17 leave $a_1, \ldots, a_{t-1}$ and $T_1, \ldots, T_t$ in $y$, and put $a_{t+1}, \ldots, a_{2t-1}$ and $T_{t+1}, \ldots, T_{2t}$ in $z$. Lines L18 and L19 put $a_t$ into $x$ at position $i$, with $y$ to its left and $z$ to its right. No key is lost: $a_t$ moved up, and the others stay below. (B1) holds at $y$ and $z$, which have $t - 1$ keys and $t$ children each if internal. At $x$, $x.n$ grows by one, to at most $2t - 1$ because $x$ was not full, and the keys stay sorted: by (B2) at $x$ before the split, $a_t$ lies between $x.key[i-1]$ and the old $x.key[i]$. (B2) holds at $y$ and $z$ because their children kept their old neighbouring keys, and at $x$ because the keys of $y$ are below $a_t$ and those of $z$ are above it. The subtrees $T_j$ keep their depth below $x$, so (B3) holds. $\square$

**Lemma 3 (insert into a node that is not full).** Let the subtree of $x$ be valid, let $x$ be not full, and let $k \notin S(x)$. Then INSERT-NONFULL$(x, k)$ makes the subtree of $x$ hold $S(x) \cup \{k\}$, keeps it valid, keeps the depth of its leaves, and does not touch a node outside it.

*Proof.* By induction on $\mathrm{ht}(x)$. If $x$ is a leaf, lines L23 and L24 shift the keys larger than $k$ one place right and put $k$ in the gap. The keys stay sorted, and $x.n \le 2t - 1$ because $x$ was not full. If $x$ is internal, line L25 finds the child $x.c[i]$ whose key range, by (B2), contains $k$. If that child is full, line L28 splits it, which is allowed because $x$ is not full, and Lemma 2 keeps the subtree valid. After the split, $k$ is in the range of $x.c[i]$ or of $x.c[i+1]$, and line L29 picks the right one by comparing $k$ with the new key $x.key[i]$, which is not $k$ because $k \notin S(x)$. In both cases the chosen child is not full: it was not full, or it is one of the two halves with $t - 1 < 2t - 1$ keys. Its subtree is valid and has height $\mathrm{ht}(x) - 1$, so the induction hypothesis applies to line L30. The child keeps at least $t - 1$ keys and gains at most one, so (B4) holds there, and (B2) holds at $x$ because $k$ went into the right range. $\square$

**Theorem 1 (insert).** If $T$ is a B-tree and $k$ is not in $T$, then after B-TREE-INSERT$(T, k)$ the tree $T$ is a B-tree with the keys of $T$ and $k$.

*Proof.* If the root $r$ is not full, line L13 applies Lemma 3 to $r$. If $r$ is full, lines L9 and L10 make a new root $s$ with no key and the single child $r$, and line L11 splits $r$. Lemma 2 applies to $s$, which is not full, and leaves $s$ with one key and two children with $t - 1$ keys each, so (B4) holds. All leaves are now one level deeper, all by the same amount, so (B3) holds. Then line L13 applies Lemma 3 to $s$. $\square$

**Lemma 4 (delete).** Let the subtree of $x$ be valid, and let $x$ be the root of the tree or have at least $t$ keys. Then B-TREE-DELETE$(x, k)$ makes the subtree of $x$ hold $S(x) \setminus \{k\}$, keeps (B1) to (B3) at each of its nodes and (B4) at each of its nodes other than $x$, removes at most one key from $x$, keeps the depth of its leaves, and does not touch a node outside it.

*Proof.* By induction on $\mathrm{ht}(x)$. Line L31 finds the least $i$ with $k \le x.key[i]$, or $i = x.n + 1$.

*Case 1, line L33.* $k$ is a key of the leaf $x$. Removing it keeps the keys sorted and removes one key.

*Case 2a, line L35.* $k = x.key[i]$, $x$ is internal and $y = x.c[i]$ has at least $t$ keys. Let $k'$ be the largest key of $S(y)$. By (B2), $k'$ is the largest key of $S(x)$ below $k$. The deletion of $k'$ from $y$ touches only the subtree of $y$, so it gives the same tree whether $x.key[i] \leftarrow k'$ is done before it or after it. Do it before it in the analysis order "delete, then replace". The node $y$ has at least $t$ keys, so the induction hypothesis applies: the subtree of $y$ becomes valid on $S(y) \setminus \{k'\}$, with at least $t - 1$ keys at $y$. All these keys are below $k'$, and $k' < k$ is above every key of $x.c[i-1]$. So writing $k'$ in place of $k$ keeps (B1) and (B2) at $x$. The number of keys of $x$ does not change.

*Case 2b, line L36.* The same with the smallest key of $S(z)$, $z = x.c[i+1]$, which has at least $t$ keys.

*Case 2c, line L37.* Both $y$ and $z$ have $t - 1$ keys. The new $y$ is $y$, then $k$, then $z$, with $2t - 1$ keys and, if internal, $2t$ children. Its keys are sorted by (B2) at $x$, so (B1) holds. $x$ loses the key $k$ and the child $z$. The children of $y$ and $z$ have the same depth by (B3), so (B3) holds. Now $y$ has $2t - 1 \ge t$ keys and $k \in S(y)$, and the induction hypothesis deletes $k$ from the subtree of $y$, leaving at least $2t - 2 \ge t - 1$ keys at $y$.

*Line L38.* $k$ is not a key of $x$ and $x$ is a leaf, so $k \notin S(x)$, and nothing changes.

*Case 3, lines L39 to L41.* $k$ is not a key of $x$, $x$ is internal, and by (B2) $k \in S(x)$ only if $k \in S(x.c[i])$. If $c = x.c[i]$ has at least $t$ keys, the induction hypothesis applies to it directly. Else $c$ has $t - 1$ keys. In case 3a a sibling, say the left one $\ell = x.c[i-1]$, has at least $t$ keys. The key $x.key[i-1]$ moves down to the front of $c$, the last key of $\ell$ moves up in its place, and the last child of $\ell$ becomes the first child of $c$. The in-order sequence of the subtree of $x$ is the same as before, so (B1) and (B2) hold, no depth changes, $\ell$ keeps at least $t - 1$ keys, and $c$ now has $t$. The right sibling is the mirror image. In case 3b both siblings that exist have $t - 1$ keys, and $c$ is merged with one of them and the key of $x$ between them, as in case 2c. The merged node has $2t - 1$ keys, $x$ loses one key, and (B1) to (B3) hold as in case 2c. In both cases, line L42 continues at a child with at least $t$ keys, whose key range contains $k$, and the induction hypothesis applies.

In each case $x$ loses at most one key, so it keeps at least $t - 1$ keys if it had at least $t$. Each child that the procedure leaves behind kept or gained keys, or is the node of the recursive call, which keeps (B4) by the hypothesis. A node outside the subtree of $x$ is never touched, because each step changes only $x$ and its children. In the base case $\mathrm{ht}(x) = 0$, $x$ is a leaf and only case 1 or line L38 applies. $\square$

**Theorem 2 (delete).** If $T$ is a B-tree, then after B-TREE-DELETE$(T.root, k)$ and the final check, $T$ is a B-tree on its old keys without $k$.

*Proof.* Lemma 4 applies to the root, whatever its number of keys. Afterwards (B1) to (B4) hold at each node except that the root may have 0 keys. If the root is a leaf with 0 keys, the tree is empty. If it is internal with 0 keys, it has exactly one child by (B1), and the final check makes that child the new root. All leaves become one level less deep, all by the same amount, so (B3) holds, and the new root has at least $t - 1 \ge 1$ keys. $\square$

**Termination.** Each recursive call, or each round of the loop in the code, moves from a node $x$ to one of its children, or to a node in the subtree of a child, so $\mathrm{ht}$ of the current node drops by at least 1. The search for the largest key of $y$ in case 2a also moves down one level at each step. So each operation stops after at most $h + 1$ rounds of each kind, where $h$ is the height of the tree. $\blacksquare$
