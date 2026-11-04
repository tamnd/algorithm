---
title: The rank-pairing heap operations keep half order and the type-2 rank rule
proves: [correctness]
status: full
---

We use the definitions of the page. A missing child has rank $-1$. For integers $a$ and $b$, let $f(a, b) = \max(a, b)$ if $|a - b| > 1$ and $f(a, b) = \max(a, b) + 1$ if $|a - b| \le 1$. The invariants are (1) half order: the key of each node is at most every key in its left subtree, and every root has no right child; (2) the type-2 rank rule: every root $x$ has $r(x) = r(x.left) + 1$, and every non-root is a 1,1-, 1,2- or 0,$i$-node with $i > 1$.

**Lemma 1 (the rule fixes the rank).** A non-root $u$ with children of ranks $a$ and $b$ obeys the type-2 rule if and only if $r(u) = f(a, b)$.

*Proof.* Let $a \ge b$. If $r(u) = a + 1$ and $a - b \le 1$, the rank differences are $1$ and $1$ or $1$ and $2$. If $r(u) = a$ and $a - b > 1$, they are $0$ and $a - b > 1$. Conversely, a 1,1- or 1,2-node has $r(u) = a + 1$ with $a - b \in \{0, 1\}$, and a 0,$i$-node with $i > 1$ has $r(u) = a$ with $a - b = i > 1$. In each case $r(u) = f(a, b)$. $\square$

**Lemma 2 (monotone).** $f$ does not decrease when one argument increases by one, and it increases by at most one.

*Proof.* Fix $b$ and compare $f(a, b)$ with $f(a + 1, b)$. If $a + 1 \le b - 2$, both are $b$. If $a + 1 = b - 1$, they are $b$ and $b + 1$. If $a + 1 \in \{b, b + 1\}$, they are $b + 1$ and $b + 1$ when $a + 1 = b$, and $b + 1$ and $b + 2$ when $a + 1 = b + 1$. If $a \ge b + 1$, then $a + 1 \ge b + 2$, so $f(a + 1, b) = a + 1$, and $f(a, b) \in \{a, a + 1\}$. In every case the increase is 0 or 1. The function is symmetric. $\square$

**Lemma 3 (link).** If $x$ and $y$ are roots of half trees of equal rank $k$ that satisfy (1) and (2), LINK$(x, y)$ returns the root of a half tree of rank $k + 1$ that satisfies (1) and (2).

*Proof.* After line L1, $x.key \le y.key$. The new left subtree of $x$ holds $y$, the left subtree of $y$, and the old left subtree of $x$. Every key there is at least $x.key$: the first two because $y.key \ge x.key$ and by half order at $y$, the third by half order at $x$. The left subtree of $y$ did not change. The ranks of the two children of $y$ are $r(y.left) = k - 1$ and $r(\text{old } x.left) = k - 1$, so $y$ is a 1,1-node. The root $x$ now has rank $k + 1 = r(y) + 1$, so it is a 1-node and has no right child. $\square$

**Theorem 1 (insert, meld, delete-min).** These operations keep (1) and (2), and delete-min returns a smallest key.

*Proof.* Insert adds a one-node half tree of rank $0 = -1 + 1$. Meld only joins root lists. In delete-min, each root holds the smallest key of its half tree, because the root has no right child and its left subtree holds all other nodes, so $z = H.min$ holds a smallest key. Line L4 removes $z$ and cuts the right spine $s_1 = z.left, s_2 = s_1.right, \ldots$. Each $s_i$ keeps its left subtree, so half order holds in the new half tree rooted at $s_i$, which has no right child, and $r(s_i) = r(s_i.left) + 1$ makes it a 1-node. Nodes inside the left subtrees do not change. The links of lines L5 and L6 join only half trees of equal rank, so they keep (1) and (2) by Lemma 3. $\square$

**Theorem 2 (decrease-key).** DECREASE-KEY keeps (1) and (2).

*Proof.* If $x$ is a root, its key is at most every key in its left subtree before the change, and so also after it. Otherwise let $u$ be the parent of $x$ and $y$ its right child.

*Half order after line L9.* Let $v$ be any node other than $x$. If $x$ was in the left subtree of $v$, then so were $y$ and its subtree; after line L9 the left subtree of $v$ is the old one without $x$ and the left subtree of $x$. So it lost keys and gained none, and half order at $v$ holds. Otherwise the left subtree of $v$ did not change. At $x$, every key of its left subtree was at least the old key of $x$, which is at least the new key. So half order holds everywhere, and $x$ is a root with no right child.

*The rank rule.* Line L9 sets $r(x) = r(x.left) + 1$, so the new root is a 1-node. The nodes in the subtrees of $x.left$ and $y$ did not change. The only node whose children changed is $u$: its child $x$, of rank $r(x)$, was replaced by $y$, of rank $r(y) \le r(x)$, because rank differences are not negative. We prove by induction over the iterations of lines L10 to L14 this claim: at the start of an iteration with node $u$, every node other than $u$ obeys the rule, and the ranks of the children of $u$ are at most what they were when $u$ last obeyed the rule.

If $u$ is a root, line L11 makes it a 1-node, and the rule holds everywhere. Otherwise let $k = f(r(u.left), r(u.right))$. When $u$ last obeyed the rule, $r(u)$ was $f$ of the old ranks of its children, by Lemma 1. The rank of $u$ has not changed since then, and by Lemma 2 $f$ does not increase when the arguments decrease, so $k \le r(u)$. If $k = r(u)$, line L13 returns, and $u$ obeys the rule by Lemma 1. If $k < r(u)$, line L14 sets $r(u) = k$, so $u$ obeys the rule. Its parent now has a child of smaller rank, and every other node obeys the rule, so the claim holds for the next iteration with the parent of $u$. Each iteration goes one level up, so the loop ends, at a root or at line L13. $\blacksquare$
