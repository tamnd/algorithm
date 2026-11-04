---
title: Correctness of the pairing heap
proves: [correctness]
status: full
---

We prove that each operation of the pairing heap keeps the invariant (P1) to (P3) of the page and changes the multiset of keys as the priority queue requires. Write $K(T)$ for the multiset of keys of a tree $T$. A tree is *heap-ordered* if each node has a key at least the key of its parent.

**Lemma 1 (link).** Let $A$ and $B$ be heap-ordered trees with roots $a$ and $b$, or let one of them be empty. Then $\mathrm{LINK}(a, b)$ returns the root of a heap-ordered tree $T$ with $K(T) = K(A) \uplus K(B)$, and the root of $T$ holds $\min K(T)$.

*Proof.* If one tree is empty, LINK returns the other, and the claim holds. Otherwise, after line L2 we have $a.key \le b.key$. Line L3 adds one edge, from $a$ to $b$, and puts $b$ at the front of the child list of $a$. The new edge is in heap order because $b.key \ge a.key$. All other parent and child pairs are as before, so they are in heap order. No node is added or removed, so $K(T) = K(A) \uplus K(B)$. In a heap-ordered tree, each key is at least the key of the root, by induction on the depth, so the root $a$ holds $\min K(T)$. $\square$

**Lemma 2 (pairing).** Let $T_1, \dots, T_k$ be heap-ordered trees, $k \ge 0$. Then $\mathrm{MERGE\text{-}PAIRS}(T_1, \dots, T_k)$ returns one heap-ordered tree $T$ with $K(T) = \biguplus_i K(T_i)$, or NIL if $k = 0$.

*Proof.* The first pass (lines L8 and L9) replaces each pair $T_i, T_{i+1}$ by their link and keeps a last tree alone if $k$ is odd. By Lemma 1, the list $Y$ holds heap-ordered trees whose multisets of keys add up to $\biguplus_i K(T_i)$. In the second pass (lines L10 and L11) we use this loop invariant: $r$ is NIL or the root of a heap-ordered tree whose keys are the union of the keys of the trees of $Y$ already processed. It holds at the start with $r = $ NIL. Each step links the next tree of $Y$ with $r$, and by Lemma 1 the invariant holds again. At the end, all trees of $Y$ are processed, and line L12 returns the claimed tree. $\square$

**Theorem.** Each operation keeps (P1) to (P3) and is correct.

*Proof.* Assume the invariant holds before the operation.

*Find-min.* By (P2) and the remark in Lemma 1, the root holds a smallest key.

*Insert and meld.* A new node is a heap-ordered tree with one node. By Lemma 1, line L5 or line L1 gives one heap-ordered tree whose keys are the old keys plus the new key, or the keys of both heaps. The count grows by one, or becomes the sum of the counts.

*Delete-min.* The root $r$ holds a smallest key, so line L7 returns a correct answer. The children of $r$ are the roots of heap-ordered trees, and these trees hold all keys except one copy of $r.key$. By Lemma 2, line L6 makes them one heap-ordered tree, so (P1) and (P2) hold, and the count goes down by one.

*Decrease-key.* Let the new key be $k \le x.key$. If $x$ is the root, only its key goes down, and its children still have keys at least $k$, so heap order holds. Otherwise, line L14 cuts the subtree $S$ of $x$ out. The rest of the tree is still heap-ordered, because removing a subtree removes edges and adds none. In $S$, the children of $x$ had keys at least the old key of $x$, which is at least $k$, so $S$ is heap-ordered. By Lemma 1, the link of the root with $x$ gives one heap-ordered tree with the old keys, except that the key of $x$ is now $k$.

*Delete.* If $x$ is the root, this is a delete-min. Otherwise, line L16 cuts the subtree of $x$; as before, the rest is heap-ordered. The children of $x$ are roots of heap-ordered trees, so by Lemma 2 MERGE-PAIRS gives one heap-ordered tree with the keys of the subtree of $x$ without $x$. By Lemma 1, the final link gives one heap-ordered tree with all keys except one copy of $x.key$.

*Pointers.* LINK puts $b$ at the front of the child list of $a$: $b.sibling$ becomes the old first child, the $prev$ of that old first child becomes $b$, $b.prev$ becomes $a$, and $a.child$ becomes $b$. A cut of $x$ sets the pointer that pointed to $x$ (the $child$ of the parent if $x$ is a first child, else the $sibling$ of the left sibling) to $x.sibling$, and sets the $prev$ of $x.sibling$ to $x.prev$. These are the updates of a doubly linked list, so (P3) holds after each operation.

Every operation keeps (P1) to (P3), and each answer is a smallest key of the current multiset. So the pairing heap implements the meldable priority queue. $\blacksquare$
