---
title: The Fischer-Heun query formula returns the leftmost minimum
proves: [correctness, complexity]
status: full
---

Let $A[1 \ldots n]$ with $n \ge 1$ and a virtual $A[0] = -\infty$. The 2d-Min-heap has the nodes $0, \ldots, n$, and $\mathrm{parent}(u)$ for $u \ge 1$ is the largest $p < u$ with $A[p] \le A[u]$. The children of a node are ordered by position. The DFUDS sequence is $E = \texttt{(} \, \mathrm{desc}(0) \, \mathrm{desc}(1) \cdots \mathrm{desc}(n)$ with $\mathrm{desc}(v) = \texttt{(}^{\deg(v)} \texttt{)}$. Positions in $E$ start at 1, $D[p]$ is the number of "(" minus the number of ")" in $E[1 \ldots p]$, with $D[0] = 0$, and $\mathrm{end}(v)$ is the position of the last symbol of $\mathrm{desc}(v)$.

**Lemma 1 (stack build).** Line L1 computes the parents in $O(n)$ time.

*Proof.* Keep a stack of positions, with 0 at the bottom. Before position $u$ is pushed, pop every top $t \ge 1$ with $A[t] > A[u]$; the top that remains is the parent. By induction the stack holds, from the bottom, the positions $t < u$ with $A[t] < A[s]$ for no $s \in (t, u)$, that is, the positions with $A[t] \le A[s]$ for all $s \in (t, u)$, in increasing order of position and non-decreasing order of value. The largest $p < u$ with $A[p] \le A[u]$ has $A[s] > A[u] \ge A[p]$ for all $s \in (p, u)$, so it is on the stack, and every stack entry above it has a value greater than $A[u]$, else it would be a larger candidate. So the pops stop exactly at $p$. The popped entries $t$ have a later $u$ with $A[u] < A[t]$, so they leave the stack for good. Each position is pushed and popped at most once. $\square$

**Lemma 2 (preorder).** For $u > v$, the node $u$ is in the subtree of $v$ exactly when $A[s] \ge A[v]$ for all $s \in (v, u]$. So each subtree is a range $[v, v + s_v)$ of positions, and the preorder of the 2d-Min-heap is $0, 1, \ldots, n$.

*Proof.* By induction on $u$. If $A[s] \ge A[v]$ for all $s \in (v, u]$, then $v$ is a candidate for the parent of $u$, so $p' = \mathrm{parent}(u) \in [v, u)$, and $p'$ is $v$ or, by induction, in the subtree of $v$; so is $u$. Conversely, if $u$ is in the subtree of $v$, then $p' = \mathrm{parent}(u)$ is $v$ or in the subtree of $v$, so $A[s] \ge A[v]$ for $s \in (v, p']$ by induction, and $A[p'] \ge A[v]$. The items in $(p', u)$ are greater than $A[u]$, by the choice of the parent, and $A[u] \ge A[p'] \ge A[v]$, so the condition holds up to $u$. The condition is closed under smaller $u$, so the subtree of $v$ is a range starting at $v$. It is $\{v\}$ together with the subtrees of the children of $v$, which are disjoint ranges ordered by position, so by induction on the size the preorder that visits $v$ and then its children in order lists the range in increasing order. $\square$

**Lemma 3 (excess at the ends).** $D[\mathrm{end}(v)] = P(v)$, where $P(v) = \#\{u > v : \mathrm{parent}(u) \le v\}$. Also, $u > v$ has $\mathrm{parent}(u) \le v$ exactly when $A[u] < A[s]$ for all $s \in (v, u)$, that is, when $u$ is a strict prefix minimum of $A[v + 1 \ldots n]$.

*Proof.* $E[1 \ldots \mathrm{end}(v)]$ has $1 + \sum_{t \le v} \deg(t)$ symbols "(" and $v + 1$ symbols ")". Every node $u \ge 1$ has its parent below $u$, so $\sum_{t \le v} \deg(t) = \#\{u \ge 1 : \mathrm{parent}(u) \le v\} = v + P(v)$. So $D[\mathrm{end}(v)] = 1 + v + P(v) - (v + 1) = P(v)$. The second part is the definition of the parent: the largest $p < u$ with $A[p] \le A[u]$ is at most $v$ exactly when no $s \in (v, u)$ has $A[s] \le A[u]$. $\square$

**Lemma 4 (inside a description).** For $v \ge 1$, every position $p$ of $\mathrm{desc}(v)$ other than $\mathrm{end}(v)$ has $D[p] > D[\mathrm{end}(v - 1)]$.

*Proof.* The symbols before $\mathrm{end}(v)$ in $\mathrm{desc}(v)$ are all "(", so $D[p] = D[\mathrm{end}(v - 1)] + k$ for some $k \ge 1$. $\square$

**Lemma 5 (matching).** For $u \ge 1$, the ")" at $\mathrm{end}(u - 1)$ matches a "(" inside $\mathrm{desc}(\mathrm{parent}(u))$.

*Proof.* The ")" that matches a "(" at $q$ is at the first position $q' > q$ with $D[q'] = D[q] - 1$. Let $p = \mathrm{parent}(u)$ with $d = \deg(p)$, let $u$ be the $k$-th child of $p$, and let $q$ be the position of the $(d - k + 1)$-st "(" of $\mathrm{desc}(p)$. Set $\mathrm{end}(-1) = 1$, so $D[\mathrm{end}(-1)] = 1$. Let $Q = \#\{t > p : \mathrm{parent}(t) < p\}$; by Lemma 2 these $t$ lie outside the subtree of $p$, so $t > u - 1$ for all of them. By Lemma 3, $D[\mathrm{end}(p - 1)] = P(p - 1) = Q + 1$, counting $p$ itself, so $D[q] = Q + d - k + 2$.

For $v = u - 1$, the nodes $t > u - 1$ with $\mathrm{parent}(t) \le u - 1$ are the $Q$ nodes above and the children $u, \ldots$ of $p$ from the $k$-th on; no node after $u - 1$ has its parent in $(p, u - 1]$, because those parents are in the subtrees of the first $k - 1$ children, which end at $u - 1$ by Lemma 2. So $D[\mathrm{end}(u - 1)] = Q + d - k + 1 = D[q] - 1$.

It remains to show that the excess stays at least $D[q]$ on $(q, \mathrm{end}(u - 1))$. The positions after $q$ inside $\mathrm{desc}(p)$, other than its end, are "(" and so above $D[q]$. For $p \le v \le u - 2$, the count $P(v)$ includes the $Q$ nodes, the $d - k + 1$ children of $p$ from $u$ on, and the node $v + 1 \le u - 1$, whose parent is at most $v$; so $D[\mathrm{end}(v)] = P(v) \ge D[q]$. By Lemma 4, the positions inside $\mathrm{desc}(v)$ for $p < v \le u - 1$ are above $D[\mathrm{end}(v - 1)] \ge D[q]$. So $\mathrm{end}(u - 1)$ is the first position after $q$ at the excess $D[q] - 1$. $\square$

**Theorem (Eq. (2) of the papers).** For $1 \le i < j \le n$, let $x = \mathrm{select}_0(i + 1) = \mathrm{end}(i)$, $y = \mathrm{select}_0(j) = \mathrm{end}(j - 1)$, and $w$ the leftmost minimum of $D[x \ldots y]$. If $\mathrm{rank}_0(\mathrm{open}(w)) = i$, then $i$ is the leftmost minimum of $A[i \ldots j]$; otherwise $\mathrm{rank}_0(w)$ is. For $i = j$ the answer is $i$.

*Proof.* The range $E[x \ldots y]$ is $\mathrm{end}(i)$ followed by $\mathrm{desc}(i + 1), \ldots, \mathrm{desc}(j - 1)$. By Lemma 4 no position inside a description is a leftmost minimum, because the end of the previous description, which is in the range and earlier, is lower. So $w = \mathrm{end}(v)$ for the least $v \in [i, j - 1]$ that minimises $P(v)$.

Let $c'$ be the leftmost minimum of $A[i + 1 \ldots j]$, and $R$ the set of strict prefix minima of $A[c' \ldots n]$ that lie after $j$. Since $A[c'] \le A[s]$ for all $s \in [c', j]$, the prefix minima of $A[c' \ldots n]$ are $c'$ and $R$, so $P(c' - 1) = 1 + |R|$ by Lemma 3.

- For $i \le v \le c' - 2$: $A[v + 1]$ is a prefix minimum of $A[v + 1 \ldots n]$, and $c'$ is one too, since $A[c'] < A[s]$ for $s \in [i + 1, c')$. Each $u \in R$ is one too, since $A[u]$ is below every item of $A[c' \ldots u - 1]$ and so below $A[c']$, which is below every item of $A[v + 1 \ldots c' - 1]$. These are $|R| + 2$ distinct nodes, so $P(v) \ge P(c' - 1) + 1$.
- For $c' \le v \le j - 1$: $A[v + 1]$ with $v + 1 \le j$ is a prefix minimum of $A[v + 1 \ldots n]$, and each $u \in R$ is one too, as $A[u] < A[c'] \le A[s]$ for $s \in [v + 1, j]$ and $A[u]$ is below the items between $j$ and $u$. So $P(v) \ge 1 + |R| = P(c' - 1)$.

So $w = \mathrm{end}(c' - 1)$ and $\mathrm{rank}_0(w) = c'$. The items $A[i + 1 \ldots c' - 1]$ are greater than $A[c']$, so $\mathrm{parent}(c') \le i$. By Lemma 5, $\mathrm{open}(w)$ lies in $\mathrm{desc}(\mathrm{parent}(c'))$, and $\mathrm{rank}_0$ of a position inside $\mathrm{desc}(t)$, before its end, is $t$. So the test of line L7 holds exactly when $\mathrm{parent}(c') = i$, that is, when $A[i] \le A[c']$, and then $i$ is the leftmost minimum of $A[i \ldots j]$. Otherwise $\mathrm{parent}(c') < i$, so $A[i] > A[c']$, and $c'$ is the leftmost minimum of $A[i \ldots j]$. $\square$

**Complexity.** The build is $O(n)$: Lemma 1, one pass to write $E$, and directories built in one pass each. $E$ has $2n + 2$ bits. With the $o(n)$-bit directories for rank, select, the leftmost ±1 range minimum on $D$ and parenthesis matching described by Fischer and Heun, each of the $O(1)$ steps of a query is $O(1)$ on the word RAM, so a query is $O(1)$ and the structure has $2n + o(n)$ bits. $\square$
