---
title: The adaptive radix tree operations keep the invariant and implement the symbol table
proves: [correctness]
status: full
---

We use the representation, the invariant (A1) to (A3) and the pseudocode of the page. All keys, stored or queried, end with the terminator byte 0 and contain no other 0, so no key is a proper prefix of another. For a node $x$, $path(x)$ is the string of $x$: the concatenation, from the root down to the parent of $x$, of each inner node's prefix and the byte of the edge taken. Write $depth(x) = \lvert path(x) \rvert$. By (A1), every leaf below $x$ has a key that starts with $path(x)$, and if $x$ is inner, with $path(x) \cdot x.prefix$.

**Lemma 1 (layouts).** FIND-CHILD($x$, $b$) returns the child of $x$ with byte $b$ or NIL; ADD-CHILD, REMOVE and the change of layout keep the set of (byte, child) pairs, except for the one pair added or removed.

*Proof.* In Node4 and Node16, the bytes and the children are parallel arrays, so the child of $b$ is at the index of $b$. In Node48, the index array maps $b$ to the slot of its child or to $-1$. In Node256, the slot at $b$ holds the child or NIL. A change of layout reads all pairs of the old node and adds them to the new one. $\square$

**Lemma 2 (search).** Under (A1) to (A3), the walk of lines L1 to L4 on a key $k$ ends at the unique leaf whose key is $k$ if $k$ is stored, and otherwise at NIL or at some leaf.

*Proof.* Suppose $k$ is stored, at leaf $\lambda$. We show that the walk keeps the claim "$x$ is an ancestor of $\lambda$ (or $\lambda$ itself) and $d = depth(x)$". This holds at the root with $d = 0$. At an inner ancestor $x$ of $\lambda$, (A1) gives that $k$ starts with $path(x) \cdot x.prefix$, so line L2 passes and line L3 sets $d = depth(x) + \lvert x.prefix \rvert$. The child of $x$ on the way to $\lambda$ has byte $k[d]$, because $k$ starts with the path of that child, and by Lemma 1 and the distinct bytes of (A2), FIND-CHILD returns it. Line L4 then sets $d$ to the depth of the child. The walk ends at a leaf, which must be $\lambda$. Uniqueness follows from (A3) and the fact that a map stores each key once (as shown for PUT below). If $k$ is not stored, any leaf reached has a different key. $\square$

**GET.** By Lemma 2, line L5 returns the value of $k$ exactly when $k$ is stored, because it compares the full key at the leaf.

**PUT.** If $k$ is stored, the walk reaches its leaf exactly as in Lemma 2, line L8 finds it and replaces the value, and the tree does not change otherwise. Assume now that $k$ is not stored. The walk of lines L8 to L17 keeps the claim of Lemma 2 for the prefix of $k$ it has matched so far: $d = depth(x)$, and $k$ starts with $path(x)$. It ends in one of three ways.

- *Lines L9 and L10, at a leaf $x$.* Its key $x.key$ starts with $path(x)$, as does $k$, and $x.key \ne k$. Neither is a prefix of the other, by the terminator, so they first differ at some position $d + p$ with $p \ge 0$, and the bytes $x.key[d + p]$ and $k[d + p]$ exist and differ. The new Node4 sits where $x$ was, so its path is $path(x)$; its prefix $k[d .. d+p-1]$ is shared by both keys; its two children have distinct bytes. So (A1) holds for both leaves, and the new node has 2 children, so (A2) holds.
- *Line L12, inside the prefix of an inner node $x$.* The keys below $x$ start with $path(x) \cdot x.prefix$, and $k$ agrees with $x.prefix$ on its first $m$ bytes and then differs. The new Node4 takes the place of $x$ with prefix $x.prefix[0 .. m-1]$; $x$ hangs below it at the byte $x.prefix[m]$ with prefix $x.prefix[m+1 ..]$, so the path string of every node below $x$, through the new node, the byte and the shortened prefix, is unchanged; and the new leaf hangs at the byte $k[d + m] \ne x.prefix[m]$. So (A1) and (A2) hold.
- *Lines L14 to L16, at an inner node with no child for $k[d]$.* If $x$ is full, its pairs are copied into the next larger layout (Lemma 1), which has room. The new leaf gets the byte $k[d]$, which no other child has, and its path is $path(x) \cdot x.prefix \cdot k[d]$, a prefix of $k$. So (A1) holds, and the count grows by one, staying in the range of the layout.

In each case one leaf is added, so (A3) holds with the new key counted. Line L17 moves to a child whose path is a prefix of $k$, so the claim holds there. The walk ends because $d$ grows and $k$ is finite.

**DELETE.** If $k$ is not stored, line L19 returns without change, by Lemma 2. Otherwise the walk ends at the leaf of $k$, and line L20 removes it from its parent $q$, which removes exactly one key, so (A3) holds, and (A1) is unaffected for the other leaves. Now $q$ may break (A2).

- If $q$ has one child $c$ left (line L21), $q$ is replaced by $c$. If $c$ is a leaf, its path becomes $path(q)$, which is a prefix of its old path, so (A1) still holds. If $c$ is inner, its new prefix is $q.prefix \cdot b \cdot c.prefix$, where $b$ is its byte in $q$, so $path(c) \cdot c.prefix$ is unchanged, and so are the paths of all nodes below $c$. The parent of $q$ keeps the same number of children.
- If $q$ reaches its shrink threshold (line L22), its pairs move to the smaller layout, which has room for them, and by the choice of thresholds the count is in the range of the new layout.
- Otherwise $q$ keeps at least the lower end of its range, by the choice of thresholds, since its count fell by one from within its range and did not reach the threshold.

So (A1) to (A3) hold after the deletion.

**Order.** The walk over all leaves visits the children of each inner node in increasing byte order, by Lemma 1. Two keys in different subtrees of a node $x$ agree on $path(x) \cdot x.prefix$ and differ at the next byte, which is the byte of their edges, so the leaves come out in increasing byte order of their keys. Removing the terminator does not change the order, because it is the smallest byte and is the last byte of each key. $\blacksquare$
