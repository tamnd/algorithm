---
title: Skew merge keeps heap order and the keys
proves: [correctness]
status: full
---

A tree is in heap order if the key of each node is at least the key of its parent. Write $K(T)$ for the multiset of keys of $T$.

**Lemma.** If $A$ and $B$ are heap-ordered trees with roots $a$ and $b$, possibly empty, then $\mathrm{MERGE}(a, b)$ returns the root of a heap-ordered tree $T$ with $K(T) = K(A) \uplus K(B)$.

*Proof.* By induction on the total number of nodes $|A| + |B|$. If $a$ or $b$ is NIL, line L1 returns the other tree, and the claim holds. Otherwise, after line L2, $a.key \le b.key$, and $a.key$ is at most every key of $A$, by heap order and induction on depth. So $a.key$ is a smallest key of $A \cup B$.

Let $R$ be the old right subtree of $a$ and $L$ the old left subtree. Line L4 makes $L$ the right subtree of $a$. The call at line L5 has fewer nodes in total, because $a$ is not in $R$ or $B$, so by induction it returns a heap-ordered tree $M$ with $K(M) = K(R) \uplus K(B)$, which becomes the left subtree of $a$.

The tree $T$ with root $a$, left subtree $M$ and right subtree $L$ is in heap order: $L$ and $M$ are heap-ordered, every key of $L$ and of $R$ is at least $a.key$ by heap order of $A$, and every key of $B$ is at least $b.key \ge a.key$. Its keys are $\{a.key\} \uplus K(L) \uplus K(R) \uplus K(B) = K(A) \uplus K(B)$. $\square$

**Theorem.** INSERT, DELETE-MIN and MELD keep heap order and the correct multiset, and DELETE-MIN returns a smallest key.

*Proof.* A one-node tree is heap-ordered, so line L7 is correct by the lemma. In DELETE-MIN, the root holds a smallest key by heap order. Its two subtrees are heap-ordered and hold all other keys, so line L8 gives a heap-ordered tree of those keys by the lemma. Meld is one MERGE. The loop form in the implementation performs the same steps as the recursion: at each node of the merge path it moves the old left subtree to the right and continues the merge in the left field, and when the old right subtree is empty, MERGE(NIL, $b$) returns $b$ unchanged. $\blacksquare$
