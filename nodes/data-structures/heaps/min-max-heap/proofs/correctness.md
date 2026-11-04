---
title: The operations of a min-max heap keep the min-max order
proves: [correctness]
status: full
---

Call a pair $(u, w)$ of nodes, with $u$ a proper ancestor of $w$, *good* if $A[u] \le A[w]$ when $u$ is a min node and $A[u] \ge A[w]$ when $u$ is a max node. The heap is in *min-max order* if every pair is good. For a node $i$, write $T(i)$ for its subtree, and say that $x \preceq_i y$ if $x \le y$ when $i$ is a min node and $x \ge y$ when $i$ is a max node. "Better for the level of $i$" means $\prec_i$, the strict form.

**Lemma 0 (answers).** In min-max order, $A[0]$ is a smallest key; a largest key is $A[0]$ if $n = 1$, $A[1]$ if $n = 2$, and the larger of $A[1]$ and $A[2]$ if $n \ge 3$.

*Proof.* The root is a min node and an ancestor of all other nodes. Nodes 1 and 2 are max nodes, and every node other than the root is in $T(1)$ or $T(2)$. $\square$

**Lemma 1 (best candidate).** Let $i$ have a child, and let every pair inside $T(i)$ whose upper node is not $i$ be good. Let $m$ be a child or grandchild of $i$ with the $\preceq_i$-best key among them. Then $A[m] \preceq_i A[w]$ for every $w$ in $T(i)$ other than $i$.

*Proof.* Say $i$ is a min node; the other case is the same with the order reversed. The children of $i$ are max nodes and its grandchildren are min nodes. A node $w \ne i$ of $T(i)$ is a child or a grandchild of $i$, so $A[m] \le A[w]$ by the choice of $m$, or it is a proper descendant of a grandchild $g$, so $A[w] \ge A[g] \ge A[m]$ because $(g, w)$ is good. $\square$

**Lemma 2 (PUSH-DOWN).** If every pair inside $T(i)$ whose upper node is not $i$ is good, then after $\mathrm{PUSH\text{-}DOWN}(A, i, n)$ every pair inside $T(i)$ is good, and the keys of $T(i)$ are permuted among its nodes.

*Proof.* By induction on the height of $i$. All changes are swaps inside $T(i)$, so the keys are permuted. If $i$ has no child, there is no pair to check. Let $i$ be a min node; the max case is symmetric. Let $x$ be the key at $i$ at the start, and let $m$ be chosen at line L2. By Lemma 1, $A[m]$ is a smallest key of $T(i)$ other than $x$.

*Case 1: $m$ is a child (lines L3 to L5).* If $x \le A[m]$, then $x$ is at most every key of $T(i)$, and every pair $(i, w)$ is good. Otherwise the keys swap. Now $A[i]$ is the old $A[m]$, a smallest key of $T(i)$, so the pairs $(i, w)$ are good. The node $m$ now holds $x > A[m]_{\mathrm{old}}$. Its descendants $w$ are grandchildren of $i$ or below them, so $A[w] \ge A[m]_{\mathrm{old}}$ by Lemma 1, and $A[w] \le A[m]_{\mathrm{old}}$ because $(m, w)$ was good. So all of them equal $A[m]_{\mathrm{old}} < x$, and the pairs $(m, w)$, which need $x \ge A[w]$, are good. No other pair changed.

*Case 2: $m$ is a grandchild and $A[m] \ge x$ (line L6).* Then $x$ is at most every key of $T(i)$, and all pairs are good.

*Case 3: $m$ is a grandchild and $A[m] < x$ (lines L7 to L9).* After line L7, $A[i] = y$, the old $A[m]$, which is a smallest key of $T(i)$, so the pairs $(i, w)$ are good, also after the later steps, since they only permute keys of $T(m) \cup \{p\}$. Let $p$ be the parent of $m$, a max node, and let $z$ be its key. Before line L8, $z \ge$ every old key of $T(p)$, because those pairs were good. If $x > z$, line L8 swaps, so $p$ holds $x$, which is larger than every other key now in $T(p)$: those are $z$ and old keys of $T(p)$. If $x \le z$, $p$ keeps $z$, which is at least $x$ and every old key of $T(p)$. Either way, every pair $(p, w)$ is good now and remains good, since the recursion only permutes the keys in $T(m)$. Pairs whose upper node is in $T(i)$ but not in $T(m) \cup \{i, p\}$ did not change. So the only pairs that may be bad have their upper node at $m$, and the loop continues with $i \leftarrow m$. By induction, it makes all pairs inside $T(m)$ good. $\square$

**Lemma 3 (PUSH-UP).** If every pair not involving the leaf $i$ is good, then after $\mathrm{PUSH\text{-}UP}(A, i)$ every pair is good.

*Proof.* Let $x$ be the key at $i$. If $i = 0$ there is nothing to prove. Let $p$ be the parent of $i$. Say $i$ is a min node and $p$ a max node; the other case is symmetric. Note that the ancestors of $i$ alternate between max nodes ($p$, its grandparent, and so on) and min nodes.

*If $x > A[p]$ (line L12 true).* Line L13 swaps. The leaf $i$ now holds $z = A[p]_{\mathrm{old}}$. All pairs $(u, i)$ are good: $u = p$ now holds $x > z$; the other ancestors $u$ of $i$ are ancestors of $p$, and $(u, p)$ was good for $z$. Now $x$ is at $p$. The pairs $(p, w)$ are good, because every key of $T(p)$ other than $x$ was at most $z < x$. A min ancestor $u$ of $p$ satisfies $A[u] \le z < x$. Only the pairs $(u, p)$ with $u$ a max ancestor of $p$ may be bad, and these $u$ are the grandparent chain of $p$. Lines L14 and L15 move $x$ up this chain while it is larger than the next grandparent $g$. Each swap puts the key $A[g]$, which was at least every key below $g$, at the position of $x$ below it; so the pairs below the new place of $A[g]$ stay good, and the min node between them holds a key at most $A[g]$, since it was below $g$. When the loop stops, $x$ is at most its next max ancestor and so at most all of them, and it is larger than all keys below it and than its min ancestors, by the same argument as for $p$. All pairs are good.

*If $x \le A[p]$ (line L12 false).* Every max ancestor $u$ of $i$ is $p$ or an ancestor of $p$, so $A[u] \ge A[p] \ge x$, and these pairs are good. Only the pairs $(u, i)$ with $u$ a min ancestor may be bad, and these $u$ are the grandparent chain of $i$. Lines L14 and L15 move $x$ up this chain while it is smaller than the next grandparent, with the same argument as above, and the order reversed. $\square$

**Theorem.** INSERT, DELETE-MIN, DELETE-MAX and the build keep min-max order, and find-min, find-max, DELETE-MIN and DELETE-MAX return correct keys.

*Proof.* *Insert.* Before line L20, all pairs are good; the new leaf adds only pairs that involve it, so Lemma 3 applies.

*Delete-min.* By Lemma 0, $A[0]$ is a smallest key. After the last key moves to the root, every pair whose upper node is not the root is a pair of the old heap, so it is good. Lemma 2 at $i = 0$ makes all pairs good.

*Delete-max.* By Lemma 0, line L18 finds a largest key. If $m$ is the last cell, removing it removes only pairs. Otherwise the last key $y$ moves to $m \in \{0, 1, 2\}$. If $m = 0$, then $n = 1$ before the delete and nothing remains. If $m \in \{1, 2\}$, the only pair with upper node outside $T(m)$ that involves $m$ is $(0, m)$, and $A[0] \le y$ because the root was a smallest key. Inside $T(m)$, all pairs with upper node other than $m$ are old pairs. Lemma 2 at $m$ makes all pairs inside $T(m)$ good, and pairs $(0, w)$ stay good since $T(m)$ only permutes its keys.

*Build.* By induction on the steps: when PUSH-DOWN runs at $i$, the nodes with a larger index have already been processed, or are leaves, so the subtrees of the children of $i$ are in order, and every pair inside $T(i)$ whose upper node is not $i$ is good. Lemma 2 makes $T(i)$ in order. After $i = 0$, the whole heap is in order.

Find-min and find-max are correct by Lemma 0. $\blacksquare$
