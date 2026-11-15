---
title: The best-first trie search returns the top k completions in the tie order
proves: [correctness]
status: full
---

The log is a finite map from non-empty strings (queries) to positive integers (counts). The trie has one node for each prefix of a logged query, and the node of a string $u$ is written $v(u)$. For a node $x$, $\mathrm{best}(x)$ is the largest count of a query in the subtree of $x$, and $\mathrm{pre}(x)$ is the preorder number of $x$ in a traversal that visits the children in character order. The tie order on answers is count descending, then query ascending. The answer $(q, c)$ has the key $\kappa(q) = (-c, \mathrm{pre}(v(q)), 0)$, and a node $x$ has the key $\kappa(x) = (-\mathrm{best}(x), \mathrm{pre}(x), 1)$. Keys are compared as tuples, and all keys are distinct.

**Lemma 1 (preorder is string order).** $\mathrm{pre}(v(u)) < \mathrm{pre}(v(w))$ if and only if $u < w$ in string order, where a proper prefix is smaller than its extensions.

*Proof.* Let $u \ne w$. If $u$ is a proper prefix of $w$, the traversal visits $v(u)$ before every node of its subtree, so $\mathrm{pre}(v(u)) < \mathrm{pre}(v(w))$, and $u < w$. Else let $z$ be the longest common prefix, with next characters $a$ in $u$ and $b$ in $w$, $a \ne b$. The traversal finishes the subtree of $v(za)$ before it starts the subtree of $v(zb)$ exactly when $a < b$, which holds exactly when $u < w$. $\square$

So the order of the answer keys is the tie order of the page.

**Lemma 2 (search tree).** In the search, the successors of a popped node $x$ are its first child in the order $(-\mathrm{best}, \mathrm{pre})$, its next sibling in that order (not followed for the start node $s = v(p)$), and the answer that ends at $x$. Every node and every answer of the subtree of $s$ is pushed exactly once, and a node successor has a larger key than $x$.

*Proof.* The first-child and next-sibling links are the left-child, right-sibling form of the subtree of $s$, so each node of the subtree is pushed exactly once, by its parent or by its previous sibling, and each answer once, by its node. For a child $y$ of $x$, $\mathrm{best}(y) \le \mathrm{best}(x)$ and $\mathrm{pre}(y) > \mathrm{pre}(x)$, so $\kappa(y) > \kappa(x)$. A next sibling comes later in the sorted order of the siblings, so its key is larger. $\square$

The answer at $x$ can have a smaller key than $x$, when its count is $\mathrm{best}(x)$. Along a path of the search tree from $s$ to a node $v(b)$, the keys increase, so every node $z$ on it has $\kappa(z) \le \kappa(v(b))$. $(\ast)$

**Theorem 1 (output).** For every prefix $p$ and every $k \ge 0$, the search returns the first $\min(k, n_p)$ answers that start with $p$ in the tie order, where $n_p$ is the number of logged queries that start with $p$.

*Proof.* If $v(p)$ does not exist, no query starts with $p$ and the search returns the empty list. Else, by Lemma 2, the answers that can appear are exactly the queries in the subtree of $s$, which are the queries that start with $p$. We show that they leave the heap in increasing key order. Suppose an answer $a$ is popped while an answer $b$ with $\kappa(b) < \kappa(a)$ has not been popped. On the search path from $s$ to $v(b)$ and then to $b$, the first element is pushed, so some element $z$ of the path is in the heap at that moment. If $z = b$, then $\kappa(z) < \kappa(a)$. If $z$ is a node, then $\kappa(z) \le \kappa(v(b))$ by $(\ast)$. With $c_b$ the count of $b$, $\mathrm{best}(v(b)) \ge c_b$. If the inequality is strict, $\kappa(v(b)) < \kappa(b) < \kappa(a)$. If it is an equality, $\kappa(v(b)) = (-c_b, \mathrm{pre}(v(b)), 1)$, and $\kappa(a) > \kappa(b) = (-c_b, \mathrm{pre}(v(b)), 0)$ with third entry $0$ forces $\kappa(a) > \kappa(v(b))$. In every case the heap holds a smaller key than $\kappa(a)$ when $a$ is popped, which is impossible. So the answers come out in increasing key order, which is the tie order by Lemma 1, and the loop stops after $k$ answers or when the heap is empty. $\square$

**Theorem 2 (work).** Let $L$ be the length of the longest query. The search pops at most $\min(k, n_p) \cdot (L - |p| + 1)$ nodes.

*Proof.* If the search returns all $n_p$ answers, it pops at most every node of the subtree of $s$. Each such node lies on the path from $s$ to the end of some query, because the trie has no node without a query below it, so there are at most $n_p (L - |p| + 1)$ of them. Else the search stops at its $k$-th answer $t$, with count $c_t$. Let $x$ be a popped node, $m = \mathrm{best}(x)$ and $u$ its string. When $x$ is popped, $t$ is not, so as in Theorem 1 some element $z$ of the path to $t$ is in the heap and $\kappa(x) \le \kappa(z)$. By $(\ast)$ and $\mathrm{best}(v(t)) \ge c_t$, this gives $(-m, \mathrm{pre}(x)) \le (-c_t, \mathrm{pre}(v(t)))$ as pairs. Let $b$ be the answer of the subtree of $x$ with the smallest key; its count is $m$. If $m > c_t$, then $\kappa(b) < \kappa(t)$, so $b$ is returned, and $x$ is on the path from $s$ to $v(b)$. If $m = c_t$, then $u \le t$ by Lemma 1. When $u$ is a prefix of $t$, $x$ is on the path to $v(t)$. Otherwise every extension of $u$ is smaller than $t$, so $\kappa(b) < \kappa(t)$ and $b$ is returned. So every popped node lies on the path from $s$ to the node of a returned answer. There are at most $\min(k, n_p)$ answers and each path has at most $L - |p| + 1$ nodes. $\square$

Each node pop pushes at most three entries, so the heap never holds more than $3 \min(k, n_p)(L - |p| + 1) + 1$ entries. The search costs $O(|p|)$ expected time to walk down the prefix with hash table lookups, then $O(kL \log(kL))$ time for the heap. The test file checks Theorem 1 against a sort of the whole log for every prefix and every $k$ on random logs, and checks the bound of Theorem 2.
