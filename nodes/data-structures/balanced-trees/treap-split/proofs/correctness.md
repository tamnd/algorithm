---
title: Treap split returns two treaps that partition the keys
proves: [correctness]
status: full
---

A *treap* is a binary tree with (P1) the search order on keys and (P2) the max-heap order on priorities. Write $K(t)$ for the set of keys of the subtree $t$, and $N(t)$ for its set of nodes.

**Theorem.** Let $t$ be a treap or nil and $k$ a key. Then SPLIT$(t, k)$ returns $(L, R)$, where $L$ and $R$ are treaps, $K(L) = \{x \in K(t) : x < k\}$, $K(R) = \{x \in K(t) : x \ge k\}$, and $N(L) \cup N(R) = N(t)$. Each node keeps its key and priority.

*Proof.* By induction on the number of nodes of $t$. If $t$ is nil, line L1 returns two empty trees, which is right.

*Case $t.key < k$ (lines L2 to L5).* Let $l = t.left$ and $r = t.right$. Since $t.right$ is a treap with fewer nodes, the induction hypothesis gives, at line L3, treaps $A$ and $B$ with $N(A) \cup N(B) = N(r)$, $K(A) = \{x \in K(r) : x < k\}$ and $K(B) = \{x \in K(r) : x \ge k\}$.

After line L4, $t$ has the left subtree $l$ and the right subtree $A$. We check that this tree, $L$, is a treap.

- (P1) at $t$: each key of $l$ is less than $t.key$, since $l$ is unchanged. Each key of $A$ is a key of $r$, so it is greater than $t.key$. Inside $l$ and $A$, (P1) holds since they are treaps.
- (P2) at $t$: the root of $A$, if any, is a node of $r$, and every node of $r$ has priority at most $t.pri$, by (P2) in the old $t$. The left child is unchanged. Inside $l$ and $A$, (P2) holds.

Its keys are $K(l) \cup \{t.key\} \cup K(A)$. Every key of $l$ and $t.key$ itself is less than $k$, and $K(A)$ is the set of keys of $r$ less than $k$. Since $K(t) = K(l) \cup \{t.key\} \cup K(r)$, the keys of $L$ are exactly the keys of $t$ less than $k$. The tree $R = B$ is a treap whose keys are those of $r$ that are at least $k$; the keys of $l$ and $t.key$ are less than $k$, so these are all the keys of $t$ at least $k$. The nodes of $L$ and $R$ are $N(l) \cup \{t\} \cup N(A) \cup N(B) = N(t)$.

*Case $t.key \ge k$ (lines L6 to L9).* This is the mirror image: every key of $t.right$ is greater than $t.key \ge k$, so $t$ and its right subtree belong in $R$. By induction, line L7 splits $l$ into $A$ (keys less than $k$) and $B$ (keys at least $k$). After line L8, $t$ has the left subtree $B$ and the right subtree $r$. The keys of $B$ come from $l$, so they are less than $t.key$, and their priorities are at most $t.pri$; so $R$ is a treap with the keys of $t$ at least $k$, and $L = A$ is a treap with the keys of $t$ less than $k$.

**Termination and cost.** Each call recurses on one child of $t$, so the calls follow one path from the root down, and there are at most $h + 1$ of them, where $h$ is the height of $t$. Each does $O(1)$ work. The visited nodes are the nodes on the search path of $k$: at each node, the call goes right when the key is less than $k$ and left otherwise, as a search for $k$ would (with a key equal to $k$ treated as greater). $\blacksquare$
