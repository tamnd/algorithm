---
title: AA tree insertion and deletion keep the level rules
proves: [correctness]
status: full
---

Write $\ell(x)$ for the level of $x$, with $\ell(\text{nil}) = 0$. A subtree is *valid* when it is a binary search tree and every node $t$ satisfies

- (A2) $\ell(t.left) = \ell(t) - 1$,
- (A3) $\ell(t.right) \in \{\ell(t), \ell(t) - 1\}$,
- (A4) $\ell(t.right.right) < \ell(t)$ when $t.right \ne \text{nil}$.

The rules (A1), a leaf has level 1, and (A5), a node above level 1 has two children, follow: a leaf has $\ell(t.left) = 0$, so $\ell(t) = 1$ by (A2); and if $\ell(t) \ge 2$, both children have level at least 1 by (A2) and (A3), so they are not nil. A link from $t$ to a child of the same level is *horizontal*; (A2) forbids horizontal left links, and (A4) forbids two horizontal right links in a row. Lines L1 to L5 are SKEW and SPLIT; a rotation keeps the in-order sequence, so the search order is never at risk, and the proofs below only check levels. "No-op" means that SKEW or SPLIT finds its test false and returns its argument. On a valid subtree, both are no-ops, since their tests are exactly the negations of (A2) and (A4) at the root.

## Insertion

**Lemma 1.** Let $t$ be valid with $\ell(t) = P$ (with $P = 0$ when $t$ is nil), and let $k$ be absent. INSERT$(t, k)$ returns a valid subtree $t'$ with the keys of $t$ and $k$, and $\ell(t') \in \{P, P + 1\}$. If $\ell(t') = P + 1$, then both children of $t'$ have level $P$, and $t$ is nil or has a right child of level $P$.

*Proof.* By induction on the height. If $t$ is nil, line L6 returns a leaf of level $1 = P + 1$ whose children have level $0 = P$.

Let $t$ be a node, with $a = t.left$ of level $P - 1$ and $b = t.right$.

*Left case* (line L7 goes left), with $a'$ the result. By induction $\ell(a') \in \{P - 1, P\}$. If $\ell(a') = P - 1$, the rules at $t$ are as before, SKEW and SPLIT are no-ops, and $t$ is returned at level $P$. If $\ell(a') = P$, both children of $a'$ have level $P - 1$, and SKEW rotates: $a'$ becomes the top, its right child is $t$, and $t.left$ becomes the old $a'.right$, of level $P - 1$. Now $t$ is valid at level $P$, and $a'$ has a left child of level $P - 1$ and the horizontal right child $t$. If $\ell(b) = P - 1$, (A4) holds at $a'$, SPLIT is a no-op, and the result has level $P$. If $\ell(b) = P$, SPLIT rotates left at $a'$: $t$ becomes the top at level $P + 1$, with left child $a'$ and right child $b$, both of level $P$. The node $a'$ now has two children of level $P - 1$, and (A4) at $t$ holds because $\ell(b.right) < P$ by the old (A4) at $t$. This is the case $\ell(t') = P + 1$, and $t$ had the right child $b$ of level $P$.

*Right case,* with $b'$ the result. If $\ell(b) = P - 1$, then by induction $\ell(b') \in \{P - 1, P\}$, and if $\ell(b') = P$, its right child has level $P - 1$. Either way (A3) and (A4) hold at $t$, SKEW and SPLIT are no-ops, and the result has level $P$. If $\ell(b) = P$, then $b$ is a node whose right child has level less than $P$ by (A4) at $t$, so $b$ has no right child of level $P$, and by induction $\ell(b') = P$. (A3) holds. If $\ell(b'.right) < P$, (A4) holds and $t$ is returned at level $P$. If $\ell(b'.right) = P$, SPLIT rotates left at $t$: $b'$ becomes the top at level $P + 1$, with left child $t$ and right child $b'.right$, both of level $P$. The node $t$ has the children $a$ and the old $b'.left$, both of level $P - 1$, and (A4) holds at $b'$ because $b'.right$ is valid. This is the case $\ell(t') = P + 1$, and $t$ had the right child $b$ of level $P$. SKEW at line L8 is a no-op in the right case, because $t.left$ did not change. $\square$

## Deletion

**Lemma 2.** Let $t$ be valid with $\ell(t) = P \ge 1$, and let $k$ be a key of $t$. DELETE$(t, k)$ returns a valid subtree $t'$ with the keys of $t$ without $k$, and

1. (a) $\ell(t') \in \{P - 1, P\}$;
2. (b) if $t$ has no right child of level $P$ and $\ell(t') = P$, then $t'$ has no right child of level $P$;
3. (c) if $t$ has a right child of level $P$, then $\ell(t') = P$.

*Proof.* By induction on the height. If $t$ is a leaf holding $k$, line L10 returns nil, of level $0 = P - 1$; (b) and (c) hold since $t$ has no right child. Otherwise lines L9, L11 or L12 replace one child of $t$ by the result of a recursive call on it, and maybe replace $t.key$ by the least key $s$ of $t.right$ or the largest key $p$ of $t.left$, which is then deleted from that child. In each case the keys are those of $t$ without $k$, and the search order holds: $s$ is less than all other keys of $t.right$ and greater than the keys of $t.left$, and symmetrically for $p$. At line L11, $t.left$ is nil, so $P = 1$, and $t.right$ is a node of level 1. Let $a = t.left$, of level $P - 1$, and $b = t.right$, of level $P - 1$ or $P$.

*Case L1: the left child, $\ell(a') = P - 1$.* DECREASE-LEVEL computes $\min(P - 1, \ell(b)) + 1 = P$ and changes nothing. All rules at $t$ hold as before, and lines L14 and L15 are no-ops: SKEW at $t$ because $\ell(a') \ne P$, and SKEW and SPLIT at the right side because those subtrees are unchanged and valid, and SPLIT at $t$ because (A4) holds at $t$. The result is $t$ at level $P$ with the same right child, so (b) and (c) hold.

*Case L2: the left child, $\ell(a') = P - 2$.* Lines L16 and L17 set $\ell(t) = P - 1$, and lower $b$ to $P - 1$ if it was at $P$.

*L2a: $\ell(b) = P - 1$ before.* The children of $b$ have levels $P - 2$ and $P - 2$ or $P - 1$. The three SKEWs are no-ops: $a'$ and $b.left$ are one level below their parents, and $b.right$ is valid. If $\ell(b.right) = P - 2$, SPLIT is a no-op and $t$ is returned at level $P - 1$: its children have levels $P - 2$ and $P - 1$, and (A4) holds. If $\ell(b.right) = P - 1$, SPLIT rotates left at $t$: $b$ becomes the top at level $P$ with left child $t$ and right child $b.right$ of level $P - 1$. The node $t$, at level $P - 1$, has children $a'$ and the old $b.left$, both of level $P - 2$. (A4) at $b$ holds since $\ell(b.right.right) \le P - 1$. The second SPLIT, at $b.right$, is a no-op. The result has level $P$ and no right child of level $P$, as (b) needs.

*L2b: $\ell(b) = P$ before.* By (A4) at $t$ and (A3) at $b$, both children of $b$ had level $P - 1$; call them $x = b.left$ and $y = b.right$. After line L17, $t$, $b$, $x$ and $y$ all have level $P - 1$. The node $x$ has a left child of level $P - 2$ and a right child $z$ of level $P - 2$ or $P - 1$; if $\ell(z) = P - 1$, then by (A4) at $x$ the children of $z$ have level $P - 2$. The first SKEW, at $t$, is a no-op. The second, at $b$, rotates right: $x$ takes the place of $b$, and $b$ becomes the right child of $x$ with left child $z$. The third, at $b$ again: if $\ell(z) = P - 1$, it rotates right, so $z$ is the right child of $x$, and $b$ the right child of $z$ with a left child of level $P - 2$. Now the right spine from $t$ is $t, x, (z,)\ b, y$, all at level $P - 1$, and each of them has a left child of level $P - 2$; after $y$ comes $y.right$, of level $P - 2$ or $P - 1$.

The SPLIT at $t$ rotates left, because $t.right.right$ (the node $z$ or $b$) has level $P - 1$: $x$ becomes the top at level $P$, with left child $t$, which now has two children of level $P - 2$. The SPLIT at $x.right$ then acts on the node $w$ after $x$.

- If $w = z$: $z.right = b$ and $b.right = y$ have level $P - 1$, so it rotates left and $b$ rises to level $P$, with children $z$ and $y$ of level $P - 1$. The node $z$ has two children of level $P - 2$. (A4) at $x$ holds since $\ell(y) = P - 1$, and (A4) at $b$ holds since $\ell(y.right) \le P - 1$.
- If $w = b$ and $\ell(y.right) = P - 1$: it rotates left, and $y$ rises to level $P$, with children $b$ (whose children have level $P - 2$) and $y.right$ of level $P - 1$. (A4) holds at $x$, since $\ell(y.right) < P$, and at $y$, since $y.right$ is valid.
- If $w = b$ and $\ell(y.right) = P - 2$: it is a no-op. The node $b$ has children of levels $P - 2$ and $P - 1$, and (A4) at $b$ holds; (A4) at $x$ holds since $\ell(y) = P - 1$.

In all three cases the result is valid at level $P$, as (c) needs.

*Case R1: the right child, $\ell(b) = P$ before.* By (A4) at $t$, $b$ has no right child of level $P$. By induction $\ell(b') \in \{P - 1, P\}$, and if $\ell(b') = P$, by (b) $b'$ has no right child of level $P$. DECREASE-LEVEL computes $\min(P - 1, \ell(b')) + 1 = P$ and changes nothing. (A3) and (A4) hold at $t$, all SKEWs and SPLITs are no-ops, and $t$ is returned at level $P$, as (c) needs.

*Case R2: the right child, $\ell(b) = P - 1$ before, $\ell(b') = P - 1$.* As in case L1, nothing changes at $t$, (A4) holds because $\ell(b'.right) \le P - 1$, and $t$ is returned at level $P$ with a right child of level $P - 1$, as (b) needs.

*Case R3: the right child, $\ell(b) = P - 1$ before, $\ell(b') = P - 2$.* DECREASE-LEVEL sets $\ell(t) = P - 1$; $b'$ is lower and does not change. Now $a$, of level $P - 1$, is a horizontal left child. Its children have level $P - 2$ and, for $u = a.right$, $P - 2$ or $P - 1$; if $\ell(u) = P - 1$, the children of $u$ have level $P - 2$ by (A4) at $a$. The first SKEW rotates right at $t$: $a$ is the top, with right child $t$, and $t.left = u$.

- If $\ell(u) = P - 2$: the second and third SKEWs are no-ops ($u$ is one below $t$, and $b'$ is valid), and SPLIT at $a$ is a no-op since $\ell(b') = P - 2$. The result is $a$ at level $P - 1$, with children of levels $P - 2$ and $P - 1$; $t$ has two children of level $P - 2$.
- If $\ell(u) = P - 1$: the second SKEW rotates right at $t$, so the right spine is $a, u, t$ at level $P - 1$, and $t$ has children of level $P - 2$. The third SKEW, at $t$, is a no-op. SPLIT at $a$ rotates left: $u$ rises to level $P$, with left child $a$ (children of level $P - 2$) and right child $t$ of level $P - 1$. (A4) at $u$ holds since $\ell(b') = P - 2$, and SPLIT at $t$ is a no-op. The result has level $P$ and no right child of level $P$, as (b) needs.

These are all cases. $\square$

## Conclusion

**Theorem.** Starting from the empty tree, after any sequence of insertions and deletions the tree is a valid AA tree with exactly the keys inserted and not deleted since, and its height is at most $2 \lg(n + 1)$.

*Proof.* The class methods search first, so INSERT gets an absent key and DELETE a present one; Lemmas 1 and 2 at the root give a valid tree with the right keys. For the height: a node of level $\ell$ has at least $2^\ell - 1$ nodes in its subtree, by induction, because its two children have level at least $\ell - 1$ by (A2) and (A3). On a downward path, a left step lowers the level by one, and of two right steps in a row at least one lowers it, by (A4). So a path from the root, of level $L$, has at most $2L$ nodes, and $n \ge 2^L - 1$ gives $h \le 2L \le 2 \lg(n + 1)$. $\blacksquare$
