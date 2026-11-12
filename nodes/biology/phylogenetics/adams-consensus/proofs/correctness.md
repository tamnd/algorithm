---
title: The Adams consensus tree is well defined and keeps every common nesting
proves: [correctness]
status: full
---

**Setting.** $T_1, \ldots, T_k$ are rooted trees on the same leaf set $X$, $|X| = n \ge 1$, and no internal node has exactly one child. $C(v)$ is the set of leaves below a node $v$. For a set $B \subseteq X$ with $|B| \ge 2$, $\mathrm{lca}_i(B)$ is the lowest node of $T_i$ whose cluster contains $B$, and $\pi_i(B)$ is the partition of $B$ into the nonempty sets $B \cap C(c)$, for the children $c$ of $\mathrm{lca}_i(B)$. The common refinement $\pi(B)$ has as blocks the nonempty intersections $P_1 \cap \cdots \cap P_k$ with $P_i \in \pi_i(B)$.

ADAMS-CONSENSUS makes a node for $X$, and for each node with a block $B$ of size at least 2 it makes one child for each block of $\pi(B)$. A block of size 1 is a leaf.

For $A \subsetneq B \subseteq X$ with $A \ne \emptyset$, say that $A$ *nests in* $B$ in a tree $T$, written $A <_T B$, if some cluster of $T$ contains $A$ and does not contain $B$. Equivalently, $\mathrm{lca}_T(A)$ is a proper descendant of $\mathrm{lca}_T(B)$, where the lca of a single leaf is that leaf.

**Fact 1 (laminar clusters).** Two clusters of one tree are disjoint or nested.

*Proof.* If one node is an ancestor of the other, the clusters are nested. Otherwise no leaf is below both. $\square$

**Lemma 1 (each split has two blocks or more).** If $|B| \ge 2$, then $\pi_i(B)$ has at least two blocks for each $i$, so $\pi(B)$ has at least two blocks, and each block is a proper subset of $B$.

*Proof.* Let $v = \mathrm{lca}_i(B)$. If all of $B$ were below one child $c$ of $v$, then $C(c)$ would contain $B$ and $c$ would be lower than $v$, against the choice of $v$. So $B$ meets at least two children of $v$. A refinement of a partition with two or more blocks has two or more blocks. $\square$

**Lemma 2 (the output is a tree).** The procedure stops and returns a rooted tree on $X$ in which each internal node has at least two children and the cluster of the node made for a block $B$ is $B$.

*Proof.* The blocks of $\pi(B)$ partition $B$, so by induction the children of the node of $B$ have as leaf sets a partition of $B$, and the cluster of that node is $B$. By Lemma 1, each block is strictly smaller than its parent block, so every chain of blocks ends at a block of size 1 after fewer than $n$ steps, and each internal node has two or more children. A rooted tree with $n$ leaves in which every internal node has at least two children has at most $n - 1$ internal nodes, so the procedure handles at most $2n - 1$ blocks. $\square$

Write $AD$ for the output tree. Its clusters are the blocks that the procedure makes.

**Lemma 3 (the key step).** Let $D$ be a block of $AD$ with $|D| \ge 2$, and let $A \subseteq D$ be a nonempty set such that, for each $i$, some cluster $K_i$ of $T_i$ contains $A$ and satisfies $K_i \subsetneq C(\mathrm{lca}_i(D))$. Then $A$ lies inside one block of $\pi(D)$.

*Proof.* Fix $i$ and let $v = \mathrm{lca}_i(D)$. The cluster $K_i$ is the cluster of a node $u$ with $C(u) \subsetneq C(v)$. Both clusters contain $A$, so by Fact 1 they are nested, and $u$ is a proper descendant of $v$ because $u \ne v$ and no node has one child. So $u$ is below one child $c$ of $v$, and $A \subseteq K_i \subseteq C(c)$. With $A \subseteq D$, $A$ lies in the block $D \cap C(c)$ of $\pi_i(D)$. As this holds for each $i$, $A$ lies in one block of the common refinement. $\square$

**Theorem 1 (common nestings are kept).** If $A <_{T_i} B$ for every $i$, then $A <_{AD} B$.

*Proof.* The set of blocks of $AD$ that contain $B$ is not empty, because it holds $X$, and by Fact 1 it is a chain. Let $D$ be its smallest member. Then $|D| \ge |B| \ge 2$. For each $i$, let $K_i$ be a cluster of $T_i$ that contains $A$ but not $B$, and let $v = \mathrm{lca}_i(D)$. As $B \subseteq D \subseteq C(v)$, the cluster $K_i$ does not contain $C(v)$, so $K_i \ne C(v)$. Both $K_i$ and $C(v)$ contain $A$, so by Fact 1 $K_i \subsetneq C(v)$. By Lemma 3, $A$ lies in one block $D'$ of $\pi(D)$. If $D'$ contained $B$, it would be a block of $AD$ that contains $B$ and is smaller than $D$, which is impossible. So $D'$ is a cluster of $AD$ that contains $A$ and not $B$, and $A <_{AD} B$. $\square$

**Theorem 2 (clusters of all trees are kept).** If a set $K$ with $|K| \ge 2$ is a cluster of every $T_i$, then $K$ is a cluster of $AD$.

*Proof.* Let $D$ be the smallest block of $AD$ that contains $K$, as in the proof of Theorem 1. Suppose $K \ne D$. For each $i$, $K \subsetneq D \subseteq C(\mathrm{lca}_i(D))$, and $K$ is a cluster of $T_i$. Lemma 3 with $A = K$ and $K_i = K$ shows that $K$ lies in one block of $\pi(D)$, which is a block of $AD$ smaller than $D$ that contains $K$. This contradicts the choice of $D$. So $K = D$. $\square$

In particular, a rooted triplet $ab|c$ is shown by a tree exactly when $\{a, b\}$ nests in $\{a, b, c\}$. By Theorem 1, every rooted triplet shown by all input trees is shown by $AD$.

**Running time.** By Lemma 2 there are at most $n - 1$ blocks of size 2 or more. For one such block $B$ and one tree, one postorder pass that counts the leaves of $B$ below each node finds $\mathrm{lca}_i(B)$ as the first node whose count is $|B|$, and one traversal of the subtrees of its children labels each leaf of $B$ with its child. Both take $O(n)$ time. The common refinement groups the leaves of $B$ by their vectors of $k$ labels, in $O(k |B|)$ expected time with a hash table. So one block takes $O(kn)$ time, and the whole procedure takes $O(kn^2)$ time. The trees take $O(kn)$ space, and the stack of blocks and the label vectors of one block take $O(kn)$ more. $\blacksquare$
