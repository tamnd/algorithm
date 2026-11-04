---
title: Correctness of navigation on the BP representation
proves: [correctness]
status: full
---

Let $P$ be written by a preorder traversal, `(` on entering a node and `)` on leaving it, let $o(v)$ and $c(v)$ be the positions of the two parentheses of $v$, and let $E(i)$ be the excess of $P[0..i]$, with $E(-1) = 0$.

**Lemma 1 (nesting).** $P[o(v)..c(v)]$ consists of the parentheses of the descendants of $v$, and of nothing else. The traversal enters $v$, then visits the subtrees of its children one after another, then leaves $v$. By induction on the height of $v$, each child's subtree writes exactly its own pairs, and nothing else is written between $o(v)$ and $c(v)$.

**Lemma 2 (excess).** $E(o(v)) = \text{depth}(v) + 1$ and $E(c(v)) = \text{depth}(v)$, with the root at depth 0. The nodes entered and not yet left right after $o(v)$ are $v$ and its ancestors, each with one unmatched `(` and no other open pair; after $c(v)$, $v$ is closed too. Lemma 1 also shows that $E(i) > E(c(v))$ for $o(v) \le i < c(v)$: inside the subtree, $v$ itself stays open. So $c(v) = \text{findclose}(o(v))$, the first position after $o(v)$ with excess $E(o(v)) - 1$.

**FIRST-CHILD.** If $v$ has children, its first child is entered right after $v$, so $P[o(v) + 1] = ($ is its opening. If not, $v$ is left right away and $P[o(v)+1] = )$.

**NEXT-SIBLING.** After leaving $v$ at $c(v) = \text{findclose}(o(v))$, the traversal enters the next child of the parent if one exists, writing `(` at $c(v) + 1$; otherwise it leaves the parent, writing `)`. The root has no next position.

**PARENT.** By Lemma 2 only the root has $E(o(v)) = 1$. Otherwise let $p$ be the parent. By Lemma 1, the pair of $p$ contains the pair of $v$, and so do the pairs of all ancestors of $v$, and no other pair does. The tightest of them is the deepest ancestor, $p$, which is $\text{enclose}(o(v))$.

**SUBTREE-SIZE.** By Lemma 1 the range $[o(v), c(v)]$ holds two parentheses for each node of the subtree, so its length $c(v) - o(v) + 1$ is twice the size.

**DEPTH.** Lemma 2.

**IS-ANCESTOR.** $u$ is an ancestor of $v$ or $u = v$ exactly when the pair of $v$ lies in the pair of $u$, by Lemma 1, that is, when $o(u) \le o(v) \le c(u)$; the pair of a non-descendant either ends before $o(u)$ or starts after $c(u)$.

**LCA.** Let $o(u) < o(v)$, with $u$ not an ancestor of $v$, and let $a$ be their lowest common ancestor. Then $u$ lies in the subtree of a child $a_1$ of $a$ and $v$ in the subtree of a later child $a_k$, $k \ge 2$, since $a$ is the lowest common ancestor and $u$ is not an ancestor of $v$. Let $d = \text{depth}(a)$. On $[o(u), o(v)]$:

- every position inside the pair of a child of $a$ has excess at least $d + 1$, by Lemma 2 applied to that child, since its own `(` is still open;
- the positions $c(a_1), \ldots, c(a_{k-1})$ lie in the range, because $c(a_1) > o(u)$ (Lemma 1) and $c(a_{k-1}) < o(a_k) \le o(v)$, and each has excess exactly $d$;
- the range lies inside the pair of $a$ and after $o(a_1)$, and $c(a_j)$ is followed directly by $o(a_{j+1})$, so every position of the range is either inside the pair of some child $a_j$ or is one of the closings $c(a_j)$.

So the minimum of $E$ on $[o(u), o(v)]$ is $d$, reached first at $m = c(a_1)$, or at another $c(a_j)$ with $j < k$. In every case $P[m + 1] = ($ is the opening of $a_{j+1}$, a child of $a$, and $\text{enclose}(m + 1) = a$ by the PARENT case. If $u$ is an ancestor of $v$, the answer is $u$, which line L12 returns. $\blacksquare$
