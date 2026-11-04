---
title: Merge keeps a leftist heap, and the right spine is short
proves: [correctness]
status: full
---

A *leftist heap* is a binary tree with the invariant (L1) heap order, (L2) $s(x.left) \ge s(x.right)$ at each node, and (L3) $x.s = s(x.right) + 1$ at each node, with $s(\mathrm{NIL}) = 0$. Write $K(T)$ for the multiset of keys of a tree $T$.

**Lemma 1.** A leftist tree whose root has rank $r$ has at least $2^r - 1$ nodes, so $r \le \lg(n + 1)$.

*Proof.* We show first that every path from the root down to an empty subtree has at least $r$ nodes, by induction on the number of nodes. An empty tree has $r = 0$. For a node $x$ of rank $r$, a path goes to the left or to the right subtree. The right subtree has rank $r - 1$ by (L3), and the left subtree has rank at least $r - 1$ by (L2). By induction, the path has at least $r - 1$ nodes below $x$, so at least $r$ with $x$. So all nodes at depths $0$ to $r - 1$ exist, which gives at least $1 + 2 + \dots + 2^{r-1} = 2^r - 1$ nodes. Then $n \ge 2^r - 1$, so $r \le \lg(n + 1)$. $\square$

**Lemma 2.** If $a$ and $b$ are the roots of leftist heaps $A$ and $B$, possibly empty, then $\mathrm{MERGE}(a, b)$ returns the root of a leftist heap $T$ with $K(T) = K(A) \uplus K(B)$, and it makes at most $s(a) + s(b) + 1$ calls.

*Proof.* By induction on $s(a) + s(b)$. If $a$ or $b$ is NIL, line L1 returns the other heap with one call, and the claim holds. Otherwise, after line L2, $a.key \le b.key$. The call at line L3 has the arguments $a.right$ and $b$, and $s(a.right) + s(b) = s(a) - 1 + s(b)$ by (L3). By induction, it returns a leftist heap $R$ with the keys of the right subtree of $a$ and of $B$, after at most $s(a) - 1 + s(b) + 1$ calls. So the total number of calls is at most $s(a) + s(b) + 1$.

Now check the invariant at the node $a$ after lines L3 to L5. All other nodes are in the left subtree of $a$, which did not change, or in $R$, which is a leftist heap.

- (L1) Every key of $R$ is a key of the old right subtree of $a$, which is at least $a.key$ by heap order of $A$, or a key of $B$, which is at least $b.key \ge a.key$ by heap order of $B$. The left subtree of $a$ did not change. So heap order holds at $a$, and a swap of the children does not change this.
- (L2) After line L4, the child of the larger rank is on the left.
- (L3) Line L5 sets $a.s$ from the final right child.

The keys of $T$ are the keys of $a$, its left subtree and $R$, which is $K(A) \uplus K(B)$. $\square$

**Theorem.** INSERT, DELETE-MIN and MELD keep the invariant, and DELETE-MIN returns a smallest key. Each of them takes $O(\log n)$ time.

*Proof.* A new node with rank 1 and no children is a leftist heap. By Lemma 2, line L7 returns a leftist heap with the old keys and $k$. In DELETE-MIN, the root holds a smallest key, because by heap order every key is at least the key of its parent, and so, by induction on the depth, at least the key of the root. The two subtrees of the root are leftist heaps, because the invariant is local to each node. By Lemma 2, line L8 returns a leftist heap with all keys except the key of the root. Meld is a single MERGE.

By Lemma 2 and Lemma 1, MERGE makes at most $\lg(n_a + 1) + \lg(n_b + 1) + 1 \le 2\lg(n + 1) + 1$ calls, each with $O(1)$ work outside the recursion. So each operation takes $O(\log n)$ time. $\blacksquare$
