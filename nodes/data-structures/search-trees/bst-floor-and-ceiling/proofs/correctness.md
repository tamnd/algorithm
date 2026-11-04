---
title: BST floor and ceiling return the largest key at most k and the smallest key at least k
proves: [correctness, termination]
status: full
---

Let $T$ be a binary search tree with root $r$ and distinct keys, with the strict [binary search tree property](/binary-search-tree-property/), and let $k$ be a key. For a node $x$ (or NIL) write $D(x)$ for the set of keys in the subtree rooted at $x$, with $D(\mathrm{NIL}) = \emptyset$. For a finite set $A$ of keys, write $f(A) = \max\{a \in A : a \le k\}$, with $f(A) = $ NIL when no element of $A$ is at most $k$. Treat NIL as smaller than each key, so that $\max(\mathrm{NIL}, a) = a$. Then $f(A \cup B) = \max(f(A), f(B))$ for all finite $A, B$.

We prove that FLOOR$(r, k)$ returns $f(D(r))$. The proof for CEILING is the same with the order reversed.

**Invariant.** Before each test of line L2:

$$\text{(I)} \qquad f(D(r)) = \max(\mathrm{key}(best), f(D(x))),$$

where $\mathrm{key}(\mathrm{NIL}) = $ NIL.

*Initialization.* Before the first test, $best = $ NIL and $x = r$, so the right side is $f(D(r))$.

*Maintenance.* Suppose (I) holds, $x \ne $ NIL, and line L3 does not return, so $k \ne x.key$. Write $L = D(x.left)$ and $R = D(x.right)$, so $D(x) = L \cup \{x.key\} \cup R$, and by the BST property each key of $L$ is less than $x.key$ and each key of $R$ is greater.

- Case $k < x.key$ (line L4). Each key in $\{x.key\} \cup R$ is at least $x.key > k$, so $f(\{x.key\} \cup R) = $ NIL, and $f(D(x)) = f(L)$. Line L4 sets $x$ to $x.left$ and leaves $best$ alone, so (I) holds after the step.
- Case $x.key < k$ (line L5). Then $f(\{x.key\}) = x.key$, and each key of $L$ is less than $x.key$, so $f(L) \le x.key$ and $f(L \cup \{x.key\}) = x.key$. Hence $f(D(x)) = \max(x.key, f(R))$. Also $\mathrm{key}(best) \le x.key$ if $best \ne $ NIL: by Lemma A below, $best$ is a proper ancestor of $x$ at which the path went right, so $x$ is in its right subtree and $x.key > best.key$. So
$$\max(\mathrm{key}(best), f(D(x))) = \max(\mathrm{key}(best), x.key, f(R)) = \max(x.key, f(R)),$$
and after line L5 sets $best \leftarrow x$ and $x \leftarrow x.right$, the right side of (I) is $\max(x.key_{\text{old}}, f(R))$, the same value. So (I) holds.

**Lemma A.** At each test of line L2 with $best \ne $ NIL, $best$ is a proper ancestor of $x$ (or $x$ is NIL below it), and $x$ lies in the right subtree of $best$.

*Proof.* $best$ changes only in line L5, where it becomes the current node and $x$ becomes its right child. Each later step moves $x$ to a child of $x$, so $x$ stays in the subtree of that right child. $\square$

**Termination.** Each step moves $x$ from a node of depth $j$ to a child of depth $j + 1$ or to NIL. The depth of a node is at most $h$, so after at most $h + 1$ steps $x$ is NIL or line L3 has returned.

**The answer.** If line L3 returns $k$, then $k = x.key \in D(r)$, and no key at most $k$ is larger than $k$, so $f(D(r)) = k$. If the loop ends, then $x = $ NIL and $f(D(x)) = $ NIL, so by (I) $f(D(r)) = \mathrm{key}(best)$, which line L6 returns. The algorithm writes only the local variables $x$ and $best$, so $T$ does not change. $\blacksquare$
