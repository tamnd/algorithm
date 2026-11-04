---
title: Search, range query, insert and delete keep the B+ tree properties and give the right answers
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page and the order $d \ge 1$. The keys are distinct. An internal node $x$ has separators $x.key[1] < \cdots < x.key[m]$ and children $x.c[0], \ldots, x.c[m]$. We write $x.key[0] = -\infty$ and $x.key[m+1] = +\infty$, and $S(x)$ for the set of keys in the leaves below $x$. A subtree is *valid* if:

> **(P1)** The keys in each node are sorted. Each node has at most $2d$ keys, and an internal node with $m$ keys has $m + 1$ children.
> **(P2)** For an internal node $x$ and $0 \le i \le m$, each key $k \in S(x.c[i])$ has $x.key[i] \le k < x.key[i+1]$.
> **(P3)** All leaves have the same depth.
> **(P4)** Each node other than the root of the subtree has at least $d$ keys, and an internal root has at least 1 key.
> **(P5)** The leaves, from left to right, are linked by their `next` pointers, and the last leaf of the whole tree has `next` = NIL.

The keys of the tree are the keys in its leaves. Separators are only guides: a separator need not be a key of the tree. By (P2), the leaves from left to right hold the keys in increasing order.

**Lemma 1 (the search path).** In a valid tree, the leaf $\lambda(k)$ that lines L1 to L5 return is the only leaf that can hold $k$, and every key $k'$ of a leaf to the left of $\lambda(k)$ has $k' < k$.

*Proof.* At an internal node $x$, line L3 takes $i$ = the number of separators $\le k$, so $x.key[i] \le k < x.key[i+1]$. By (P2), each key of a child $x.c[j]$ with $j < i$ is $< x.key[j+1] \le x.key[i] \le k$, and each key of a child with $j > i$ is $\ge x.key[j] \ge x.key[i+1] > k$. So $k$ can only be in $S(x.c[i])$, and every leaf to the left of $x.c[i]$ below $x$ holds only keys smaller than $k$. By induction down the path, the same holds for the leaf that the loop reaches. The loop stops, because each step goes one level down and the leaves are at a finite depth (P3). $\square$

**Theorem 1 (search and range).** In a valid tree, the search for $k$ is true exactly when $k$ is a key, and RANGE$(T, a, b)$ returns the keys $k$ with $a \le k \le b$ in increasing order.

*Proof.* The first claim follows from Lemma 1. For the range, line L6 starts at $\lambda(a)$. By Lemma 1, all keys in leaves to its left are smaller than $a$, so no answer is missed there. Lines L7 to L10 visit the leaves from $\lambda(a)$ to the right through the `next` links, which by (P5) is the order of the keys. Line L8 skips keys below $a$ and stops at the first key above $b$, and every later key is larger still. So the output is exactly the keys in $[a, b]$, in order. $\square$

**Lemma 2 (insert below a node).** Let the subtree of $x$ be valid, and let $k \notin S(x)$. Then INSERT-REC$(x, k)$ adds $k$ to the keys below $x$, keeps (P1) to (P3) and (P5) and keeps (P4) below $x$, and either

- returns NIL, and $x$ has at most $2d$ keys, or
- returns $(s, z)$, where $z$ is a new node at the depth of $x$, placed right after $x$ in the leaf order, $x$ and $z$ each have at least $d$ keys and at most $2d$, every key below $x$ is $< s$, and every key below $z$ is $\ge s$.

*Proof.* By induction on the height of $x$. If $x$ is a leaf, line L15 adds $k$ in order. If it then has at most $2d$ keys, line L16 returns NIL. Otherwise it has $2d + 1$ keys. Line L17 keeps the $d$ smallest in $x$ and puts the other $d + 1$ in $z$, line L18 links $z$ between $x$ and the old successor of $x$, so (P5) holds, and line L19 returns the smallest key of $z$ as $s$. Every key of $x$ is smaller than $s$.

If $x$ is internal, line L20 picks the child $x.c[i]$ whose range contains $k$, as in Lemma 1, and line L21 applies the hypothesis to it. If it returns NIL, (P2) at $x$ holds because $k$ went into the right range. Otherwise line L23 inserts $s$ after $x.key[i]$ and $z$ after $x.c[i]$. The keys below the old $x.c[i]$ were in $[x.key[i], x.key[i+1])$, they are now split into those below $x.c[i]$, all $< s$, and those below $z$, all $\ge s$. So (P2) holds at $x$ for the two new ranges $[x.key[i], s)$ and $[s, x.key[i+1])$, and the separators stay sorted. If $x$ now has at most $2d$ keys, line L24 returns NIL. Otherwise it has $2d + 1$ keys and $2d + 2$ children. Lines L25 and L26 keep the first $d$ keys and the first $d + 1$ children in $x$, move the last $d$ keys and the last $d + 1$ children to $z'$, and return the middle key $s' = x.key[d+1]$. By (P2) before the split, each key below the first $d + 1$ children is $< s'$ and each key below the others is $\ge s'$. Both halves have $d$ keys, and (P2) holds inside each half because each child keeps its two neighbouring separators, or $-\infty$ and $+\infty$ replaced by the bounds that the parent gives. The depth of each leaf does not change. $\square$

**Theorem 2 (insert).** If $T$ is a valid B+ tree and $k$ is not a key, then after BPT-INSERT$(T, k)$ the tree is a valid B+ tree whose keys are the old keys and $k$.

*Proof.* Lemma 2 applies to the root. If it returns NIL, nothing more is needed. If it returns $(s, z)$, line L13 makes a new root with the one separator $s$ and the children old root and $z$. (P2) holds at the new root by Lemma 2, the new root has one key, so (P4) holds, and all leaves are now one level deeper, so (P3) holds. $\square$

**Lemma 3 (fix a child).** Let $x$ be internal, let the subtrees of its children be valid, let (P2) hold at $x$, and let $c = x.c[i]$ have exactly $d - 1$ keys while each other child has at least $d$. Then FIX-CHILD$(x, i)$ keeps the keys below $x$, keeps (P2), (P3) and (P5), leaves each child of $x$ with $d$ to $2d$ keys, and removes at most one separator from $x$.

*Proof.* A sibling $y$ next to $c$ exists, because $x$ has at least 2 children ($x$ has at least 1 key by (P1) and (P4) or by the root rule).

*Borrow from a leaf (line L36, $y$ has more than $d$ keys).* Say $y = x.c[i-1]$ is the left sibling. Its largest key moves to the front of $c$, and the separator $x.key[i]$ becomes the new smallest key of $c$. The keys left in $y$ are below the moved key, and those in $c$ are at least it, so (P2) holds. The moved key was $\ge x.key[i-1]$, so the range of $y$ stays correct. Now $c$ has $d$ keys and $y$ at least $d$. The right sibling is the mirror image, with the new separator equal to the new smallest key of $y$.

*Borrow from an internal node.* With the left sibling $y$: the separator $x.key[i]$ moves down to the front of $c$, the last child of $y$ becomes the first child of $c$, and the last key of $y$ moves up to become $x.key[i]$. This is a rotation. The keys below the moved child lie between the last key of $y$ and the old $x.key[i]$, which are the new bounds of that child inside $c$. So (P2) holds at $x$, at $y$ and at $c$, and no leaf changes depth. The right sibling is the mirror image.

*Merge (line L37, $y$ has exactly $d$ keys).* Let $a$ be the left one of $c$ and $y$, and $b$ the right one, with separator $s$ between them in $x$. If they are leaves, $a$ takes all keys of $b$ and the link $b.next$. Together they have $2d - 1 \le 2d$ keys, in order, because the keys of $a$ are $< s \le$ the keys of $b$. If they are internal, $a$ takes $s$, then the keys and children of $b$, for $(d - 1) + 1 + d = 2d$ keys. The children of $b$ had bounds from $b$'s separators and from $s$ and the next separator of $x$, and these are now the separators around them in $a$. Then $x$ loses $s$ and the child $b$, and the range of $a$ in $x$ is the union of the two old ranges. Leaves of $a$ and $b$ had the same depth by (P3). $\square$

**Lemma 4 (delete below a node).** Let the subtree of $x$ be valid. Then DELETE-REC$(x, k)$ removes $k$ from the keys below $x$ if it is there, keeps (P1) to (P3), (P5), and (P4) at each node below $x$ other than $x$, removes at most one key from $x$, and returns true exactly when $x$ ends with fewer than $d$ keys.

*Proof.* By induction on the height. A leaf removes $k$ if it holds it (line L30). An internal node goes to the only child whose range can hold $k$ (line L31), by Lemma 1. By the hypothesis that child keeps all properties below it and loses at most one key, so it has at least $d - 1$ keys. If it has fewer than $d$, line L33 applies Lemma 3, which removes at most one separator from $x$. Line L34 reports whether $x$ dropped below $d$. $\square$

**Theorem 3 (delete).** If $T$ is a valid B+ tree, after BPT-DELETE$(T, k)$ it is a valid B+ tree on its old keys without $k$.

*Proof.* Lemma 4 applies to the root, and the root may have any number of keys, so (P4) holds except that an internal root may have no key. Then it has exactly one child, and line L29 makes that child the root. All leaves move up one level, so (P3) holds. $\square$

**Termination.** Each recursive call of INSERT-REC and DELETE-REC goes one level down, and the search loop of lines L2 to L4 does too, so there are at most $h + 1$ calls, where $h$ is the height. The range loop visits each leaf at most once, because the `next` links go strictly to the right. $\blacksquare$
