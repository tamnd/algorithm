---
title: Correctness of TGDH
proves: [correctness]
status: full
---

We prove that after any sequence of joins and leaves, all members compute the same root key, and that with joins only the height stays $\lceil \log_2 n \rceil$. Notation is that of the page: $G$ has prime order $q$ and generator $g$, exponents are taken modulo $q$, and $f(x) = x \bmod q$, or 1 if that is 0. A tree is consistent if every inner node $v$ other than the root with children $l$ and $r$ has $BK_v = g^{k_v}$ with $k_v = f(g^{k_l k_r})$, and every leaf has $BK = g^{k}$ for the member's current leaf key $k$.

**Lemma 1 (node keys are symmetric).** For any $a, b \in [1, q)$, $f\bigl((g^b)^a\bigr) = f\bigl((g^a)^b\bigr)$.

*Proof.* Both are $f(g^{ab})$. $\square$

**Lemma 2 (walks agree in a consistent tree).** In a consistent tree, for every node $v$ and every member $M$ below $v$, the value that $M$'s walk of line L1 holds at $v$ equals $k_v$, the key defined from the leaf keys by $k_v = f(g^{k_l k_r})$.

*Proof.* By induction on the height of $v$. If $v$ is a leaf, the walk starts with the member's leaf key. If $v$ has children $l$ and $r$ and $M$ is below $l$, then by induction $M$ holds $k_l$ at $l$, reads $BK_r = g^{k_r}$ (consistency), and computes $f(g^{k_r k_l}) = k_v$. If $M$ is below $r$, it computes $f(g^{k_l k_r})$, the same value by Lemma 1. $\square$

**Lemma 3 (the changed nodes lie on the sponsor's path).** In a join, the nodes whose keys change are the new inner node and its ancestors, and in a leave they are the ancestors of the promoted subtree; in both cases they all lie on the sponsor's path.

*Proof.* The key of a node depends only on the leaf keys and the shape of its subtree. In a join (line L4), only the subtrees that contain the replaced leaf $s$ change, that is, the new inner node and its ancestors; the sponsor is the member at $s$, a child of the new inner node, so its path contains all of them. The sponsor's new leaf key in line L5 changes exactly the nodes on its own path. In a leave (line L7), only the subtrees that contained the removed parent change, which are the ancestors of the promoted subtree; the sponsor of line L8 is a leaf of that subtree, so its path passes through the root of the subtree and all these ancestors. Again line L5 changes only nodes on that path. $\square$

**Lemma 4 (operations keep the tree consistent).** If the tree is consistent before a join or a leave, it is consistent after the sponsor runs lines L5 and L6.

*Proof.* Nodes off the sponsor's path keep their keys and blinded keys by Lemma 3, so their consistency is unchanged. The sponsor publishes $BK_s = g^{k_s}$ for its fresh leaf key in line L5. Walking up, at each node $v$ on its path, the sponsor holds the new key of the child on its path (by induction along the path) and reads the blinded key of the sibling, which is correct: either the sibling is off the path and unchanged, or (only at the new inner node of a join) it is the new member's leaf with $BK = g^{k}$ from line L3. So the sponsor computes the new $k_v$ and, for $v$ not the root, publishes $BK_v = g^{k_v}$ (line L2). $\square$

**Lemma 5 (height under joins).** If the tree is built only by joins at a shallowest leaf, then all leaf depths lie in $\{d, d + 1\}$ for some $d$, and the height is $\lceil \log_2 n \rceil$ for $n$ members.

*Proof.* A single leaf has depth 0. Assume all leaf depths lie in $\{d, d + 1\}$ with $d$ the least depth. A join replaces a leaf of depth $d$ by two leaves of depth $d + 1$, so depths stay in $\{d, d + 1\}$ (with $d$ increased by one when no leaf of depth $d$ remains). Let $h$ be the height. If all leaves have depth $h$, then $n = 2^h$. Otherwise there are leaves at depths $h - 1$ and $h$; a binary tree whose leaves all have depth at least $h - 1$ has all levels up to $h - 1$ full, so $n > 2^{h-1}$, and $n \le 2^h$ always. In both cases $2^{h-1} < n \le 2^h$ (for $n \ge 2$), so $h = \lceil \log_2 n \rceil$. $\square$

**Theorem.** Starting from one member, after any sequence of joins and leaves, every member's walk of line L9 outputs the same root key.

*Proof.* A tree with one leaf whose blinded key is $g^k$ is consistent. By Lemma 4, every join and every leave keeps the tree consistent. By Lemma 2 applied to the root, every member's walk outputs $k_{\mathrm{root}}$. $\blacksquare$
