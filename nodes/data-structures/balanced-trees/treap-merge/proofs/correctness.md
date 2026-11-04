---
title: Treap merge returns a treap of the union
proves: [correctness]
status: full
---

A *treap* is a binary tree with (P1) the search order on keys and (P2) the max-heap order on priorities. Write $K(t)$ for the set of keys of the subtree $t$, and $N(t)$ for its set of nodes. In a treap, the root has the highest priority of all its nodes, since every node is reached from the root by edges that do not increase the priority.

**Theorem.** Let $A$ and $B$ be treaps or nil, with $x < y$ for every $x \in K(A)$ and $y \in K(B)$. Then MERGE$(A, B)$ returns a treap $T$ with $K(T) = K(A) \cup K(B)$ and $N(T) = N(A) \cup N(B)$, and its root is the root of $A$ or of $B$. Each node keeps its key and priority.

*Proof.* By induction on $|N(A)| + |N(B)|$. If $A$ is nil, line L1 returns $B$, which is right; if $B$ is nil, line L2 returns $A$.

*Case $A.pri > B.pri$ (lines L3 to L5).* The pair $A.right$ and $B$ meets the precondition: the keys of $A.right$ are keys of $A$, so they are less than the keys of $B$. It has one node fewer, so by induction line L4 makes $A.right$ a treap $T'$ with keys $K(A.right) \cup K(B)$, whose root is the old root of $A.right$ or the root of $B$. We check that $A$ with left subtree $A.left$ and right subtree $T'$ is a treap.

- (P1) at the root: the keys of $A.left$ are less than $A.key$, as before. The keys of $T'$ are keys of $A.right$, which are greater than $A.key$, or keys of $B$, which are greater than every key of $A$. Inside $A.left$ and $T'$, (P1) holds.
- (P2) at the root: the left child is unchanged. The root of $T'$ is the root of $A.right$, whose priority is at most $A.pri$ by (P2) in $A$, or the root of $B$, whose priority $B.pri$ is less than $A.pri$. Inside $A.left$ and $T'$, (P2) holds.

The keys are $K(A.left) \cup \{A.key\} \cup K(A.right) \cup K(B) = K(A) \cup K(B)$, the nodes likewise, and the root is the root of $A$.

*Case $A.pri \le B.pri$ (lines L6 and L7).* This is the mirror image. The pair $A$ and $B.left$ meets the precondition, so by induction line L6 makes $B.left$ a treap $T'$ with keys $K(A) \cup K(B.left)$ whose root is the root of $A$ or of $B.left$. Its keys are keys of $A$, less than every key of $B$ and so less than $B.key$, or keys of $B.left$, less than $B.key$. Its root has priority $A.pri \le B.pri$ or at most $B.pri$ by (P2) in $B$. So $B$ with the left subtree $T'$ and its old right subtree is a treap with the keys $K(A) \cup K(B)$, and its root is the root of $B$.

**Termination and cost.** Each call either stops or recurses with one node fewer in total, and the node that is set aside is the root of $A$ or of $B$. In the first case the next call works on $A.right$, a step down the right spine of $A$; in the second case on $B.left$, a step down the left spine of $B$. So the number of calls is at most the length of the right spine of $A$ plus the length of the left spine of $B$, plus one, and each call does $O(1)$ work. $\blacksquare$
