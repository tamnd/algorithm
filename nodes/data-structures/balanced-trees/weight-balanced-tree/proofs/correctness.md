---
title: Weight-balanced tree operations keep the weight rule
proves: [correctness]
status: full
---

The *weight* of a tree is its number of keys plus one, so $w(\text{nil}) = 1$ and $w(t) = w(t.left) + w(t.right)$ for a node $t$. A tree is *balanced* when each node $t$ satisfies

$$w(t.left) \le 3\, w(t.right) \quad\text{and}\quad w(t.right) \le 3\, w(t.left). \tag{B}$$

This is the rule with $\Delta = 3$; the rotation test uses $\Gamma = 2$. A pair of trees $(l, r)$ is *nearly balanced* when

$$w(l) \le 3\, w(r) + 3 \quad\text{and}\quad w(r) \le 3\, w(l) + 3. \tag{P}$$

If $(l, r)$ satisfies (B) and then one key is added to or removed from one of them, the new pair satisfies (P): adding a key to $r$ gives $w(r) \le 3w(l) + 1$, removing one from $l$ gives $w(r) \le 3(w(l) + 1)$, and the other side is only easier. NODE$(l, k, r)$ makes a node with the right size, so the stored sizes are always correct, and we do not mention them again.

**Lemma 1 (BALANCE).** Let $l$ and $r$ be balanced search trees with every key of $l$ less than $k$ and every key of $r$ greater, and let $(l, r)$ satisfy (P). Then BALANCE$(l, k, r)$ returns a balanced search tree with the keys of $l$, then $k$, then the keys of $r$, in order.

*Proof.* Rotations keep the in-order sequence of the keys, so only (B) needs a proof, and only at the nodes that BALANCE builds; all other nodes are nodes of $l$ and $r$. If lines L1 and L2 both fail, (B) holds at the new root, and line L3 is right.

Let line L1 succeed, so $3a < w(r)$ with $a = w(l) \ge 1$. Then $w(r) > 3$, so $r$ is a node; let $b = w(r.left)$ and $c = w(r.right)$, so $3a < b + c \le 3a + 3$ by (P), and $b \le 3c$, $c \le 3b$ by (B) at $r$. Line L2 cannot also succeed.

*Single rotation, $b < 2c$ (line L4).* The new nodes are $x = (l, k, r.left)$, with weights $a$ and $b$, and the root $(x, r.key, r.right)$, with weights $a + b$ and $c$.

- $b \le 3a$: from $b \le 2c - 1$ we get $c \ge (b + 1)/2$, and $b + c \le 3a + 3$ gives $3b + 1 \le 6a + 6$, so $b \le 2a + 1 \le 3a$.
- $a \le 3b$: $3a < b + c \le 4b$, so $a < 4b/3 \le 3b$.
- $a + b \le 3c$: $3a \le b + c - 1$, so $3(a + b) \le 4b + c - 1 \le 4(2c - 1) + c - 1 < 9c$.
- $c \le 3(a + b)$: $c \le 3b$.

*Double rotation, $b \ge 2c$ (line L5).* Then $b \ge 2$, so $r.left$ is a node; let $d$ and $e$ be the weights of its subtrees, so $d + e = b$, and by (B) at $r.left$, $d \le 3e$ and $e \le 3d$, hence $b/4 \le d, e \le 3b/4$. The new nodes are $x = (l, k, d\text{-subtree})$ with weights $a$ and $d$, $y = (e\text{-subtree}, r.key, r.right)$ with weights $e$ and $c$, and the root $(x, r.left.key, y)$ with weights $a + d$ and $e + c$. From $b \ge 2c$ and $b \le 3c$ we have $b/3 \le c \le b/2$. Also $3a < b + c \le 3b/2$, so $a < b/2$.

- $a \le 3d$: $3d \ge 3b/4 > b/2 > a$.
- $d \le 3a$: from $b + b/3 \le b + c \le 3a + 3$, $b \le 9(a + 1)/4$, so $d \le 3b/4 \le 27(a + 1)/16$, which is at most $3a$ when $a \ge 2$. When $a = 1$, $b \le 4$, so $d \le 3 = 3a$.
- $e \le 3c$: $e \le 3b/4 \le 9c/4$.
- $c \le 3e$: $c \le b/2 < 3b/4 \le 3e$.
- $a + d \le 3(e + c)$: $3(e + c) \ge 3e + b = d + 4e$, and $a + d < (d + e)/2 + d = (3d + e)/2$, which is at most $d + 4e$ because $d \le 7e$.
- $e + c \le 3(a + d)$: $3a \ge b + c - 3 = d + e + c - 3$, so $3(a + d) \ge 4d + e + c - 3 \ge e + c + 1$, because $d \ge 1$.

So (B) holds at the three new nodes. The case where line L2 succeeds is the mirror image. $\square$

**Lemma 2 (INSERT).** If $t$ is a balanced search tree, INSERT$(t, k)$ returns a balanced search tree with the keys of $t$ and $k$, of size $|t|$ or $|t| + 1$.

*Proof.* By induction on the size of $t$. Line L6 returns one node. If $k < t.key$, the induction hypothesis makes the new left subtree balanced, with the keys of $t.left$ and $k$, all less than $t.key$, and with at most one more key. So the pair of subtrees satisfies (P), and Lemma 1 applies to line L7. Line L8 is the mirror image, and if $k = t.key$ the tree is returned unchanged. $\square$

**Lemma 3 (DELETE-MIN, DELETE-MAX).** For a balanced nonempty $t$, DELETE-MIN$(t)$ returns the least key $m$ of $t$ and a balanced search tree with the other keys. The same holds for DELETE-MAX with the largest key.

*Proof.* By induction. If $t.left$ is nil, $t.key$ is the least key, and $t.right$ is balanced. Otherwise the induction hypothesis gives the least key of $t.left$, which is the least of $t$, and a balanced left subtree with one key fewer, so Lemma 1 applies. $\square$

**Lemma 4 (GLUE).** Let $l$ and $r$ be the subtrees of a balanced node, without its key. GLUE$(l, r)$ (lines L11 and L12) returns a balanced search tree with the keys of $l$ and $r$.

*Proof.* If one side is nil, the other is returned. Let $a = w(l)$ and $c = w(r)$, both at least 2, with $a \le 3c$ and $c \le 3a$. If $|l| > |r|$, then DELETE-MAX takes the largest key $m$ of $l$, which is greater than the rest of $l$ and less than all of $r$, and leaves a tree of weight $a - 1 \ge c$. Then $a - 1 \le 3c$ and $c \le a - 1 \le 3(a - 1)$, so the pair satisfies (B), and by Lemma 1 the result is right. If $|l| \le |r|$, DELETE-MIN on $r$ leaves weight $c - 1 \ge a$, and the same argument applies. $\square$

**Lemma 5 (DELETE).** If $t$ is a balanced search tree, DELETE$(t, k)$ returns a balanced search tree with the keys of $t$ other than $k$, of size $|t|$ or $|t| - 1$.

*Proof.* By induction. If $k < t.key$, the induction hypothesis gives a balanced left subtree with at most one key fewer, so (P) holds and Lemma 1 applies to line L9; the case $k > t.key$ is the mirror image. If $k = t.key$, line L10 returns GLUE of the two subtrees, which is right by Lemma 4. $\square$

**Height.** At a node $t$ of a balanced tree, $w(t.left) \le 3\,w(t.right) = 3(w(t) - w(t.left))$, so $w(t.left) \le \frac34 w(t)$, and the same holds on the right. A node at depth $h$ has weight at least 2, so $2 \le (3/4)^h (n + 1)$ and $h \le \log_{4/3} \frac{n + 1}{2}$.

**Theorem.** Starting from the empty tree, after any sequence of insertions and deletions the tree is balanced, holds exactly the keys inserted and not deleted, and has height at most $\log_{4/3}\frac{n+1}{2} < 2.41 \lg (n + 1)$. Search, rank and select are correct.

*Proof.* The empty tree is balanced. Lemmas 2 and 5 keep it balanced with the stated keys. The height bound is the paragraph above. Search is the search of a binary search tree. Select and rank are correct because each stored size is the number of keys in its subtree, as for an [order-statistic tree](/order-statistic-tree/). $\blacksquare$
