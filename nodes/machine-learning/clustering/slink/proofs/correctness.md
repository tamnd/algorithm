---
title: SLINK keeps the pointer representation of single linkage after each new point
proves: [correctness]
status: full
---

**Setup.** For points $1, \ldots, N$ with dissimilarity $d$, let $u_N$ be the single linkage cophenetic distance, which is the minimax path distance: $u_N(i, j)$ is the least, over the paths from $i$ to $j$ through the points $1, \ldots, N$, of the largest $d$ on the path (see [single-linkage clustering](/single-linkage-clustering/)). It is an [ultrametric](/ultrametric/). For a height $h$, write $K(i, h) = \{k : u_N(i, k) \le h\}$, the cluster of $i$ at height $h$. The pointer representation is $\lambda(i) = \min_{k > i} u_N(i, k)$ and $\pi(i) = \max K(i, \lambda(i))$ for $i < N$, with $\pi(N) = N$ and $\lambda(N) = \infty$. Since $\pi(i) > i$, the pointers form a tree with root $N$. We use two facts of an ultrametric: $u(x, z) \le \max(u(x, y), u(y, z))$, and if $u(x, y) < u(y, z)$ then $u(x, z) = u(y, z)$.

**Lemma 1 (chain).** For $i < N$ and $p = \pi(i)$: $u_N(i, p) = \lambda(i)$ and $\lambda(p) > \lambda(i)$.

*Proof.* $p \in K(i, \lambda(i))$ gives $u_N(i, p) \le \lambda(i)$, and $p > i$ gives $u_N(i, p) \ge \lambda(i)$. If some $k > p$ had $u_N(p, k) \le \lambda(i)$, then $u_N(i, k) \le \lambda(i)$, so $k \in K(i, \lambda(i))$ with $k > p$, against the choice of $p$. So $\lambda(p) > \lambda(i)$. $\square$

**Lemma 2 (descendants).** Let $\text{Desc}(j)$ be the set of points whose pointer path reaches $j$, with $j$ itself. Then $\text{Desc}(j) = \{j\} \cup \{j' : u_N(j', j) < \lambda(j)\}$.

*Proof.* Let $a_0 = j', a_1 = \pi(a_0), \ldots$ be a pointer path. By Lemma 1 and induction, $u_N(a_0, a_t) \le \lambda(a_{t-1}) < \lambda(a_t)$ for $t \ge 1$, so a proper descendant $j' = a_0$ of $j = a_t$ has $u_N(j', j) < \lambda(j)$. Conversely, let $j' \ne j$ with $h = u_N(j', j) < \lambda(j)$, and let $K = K(j, h)$. Each $k > j$ has $u_N(j, k) \ge \lambda(j) > h$, so $\max K = j$. Let $s$ be the least index with $\lambda(a_s) \ge h$; it exists because the path ends at $N$. By the bound above, $a_s \in K(a_0, \lambda(a_{s-1})) \subseteq K$ when $s \ge 1$, and $a_0 \in K$ when $s = 0$. So $a_s \le j$. If $a_s < j$, then $\lambda(a_s) \le u_N(a_s, j) \le h$, so $\lambda(a_s) = h$, and $\pi(a_s) = \max K(a_s, h) = \max K = j$. In both cases $j$ is on the path. $\square$

**Lemma 3 (adding a point).** Let $u = u_{m-1}$, $u' = u_m$, and $\mu(i) = \min_{j < m} \max(u(i, j), d(j, m))$ for $i < m$. Then $u'(i, m) = \mu(i)$, $u'(i, k) = \min(u(i, k), \max(\mu(i), \mu(k)))$ for $i, k < m$, and the new representation is

$$\lambda'(i) = \min(\lambda(i), \mu(i)), \qquad \pi'(i) = m \text{ if } \mu(i) \le \lambda(i), \quad \pi'(i) = \pi(i) \text{ if } \mu(i) > \lambda(i).$$

*Proof.* A path from $i$ to $m$ runs inside the old points until it first meets $m$, from some $j$, so $u'(i, m) = \mu(i)$. A path between old points either avoids $m$, with best value $u(i, k)$, or passes through $m$, with best value $\max(\mu(i), \mu(k))$. Now $u'(i, k) \le u(i, k)$ for $k < m$ and $u'(i, m) = \mu(i)$, so $\lambda'(i) \le \min(\lambda(i), \mu(i))$. Each $k < m$ has $u'(i, k) \ge \min(u(i, k), \mu(i)) \ge \min(\lambda(i), \mu(i))$ when $k > i$, so equality holds. If $\mu(i) \le \lambda(i)$, then $m$ is in the cluster of $i$ at height $\lambda'(i)$ and has the largest index, so $\pi'(i) = m$. If $\mu(i) > \lambda(i)$, then $\lambda'(i) = \lambda(i) < \mu(i)$. A point $k < m$ with $u'(i, k) \le \lambda(i)$ has $\max(\mu(i), \mu(k)) > \lambda(i)$, so $u(i, k) \le \lambda(i)$. So the cluster of $i$ at height $\lambda(i)$ does not change, and neither does its largest index. $\square$

**Lemma 4 (the first loop).** In step $m$, when the loop of line L4 reaches $j$,

$$M(j) = \nu(j) := \min_{j' \in \text{Desc}(j)} \max\bigl(d(j', m), u(j', j)\bigr),$$

with $\text{Desc}$ and $\lambda$, $\pi$ taken before step $m$.

*Proof.* Each point $c$ changes only $M(\pi(c))$, with the old pointer: line L6 reads $\pi(c)$ before line L7 changes it. The value sent is $\lambda(c)$ at line L6, where $\lambda(c) \ge M(c)$, and $M(c)$ at line L8, where $M(c) > \lambda(c)$. So $c$ sends $\max(\lambda(c), M(c))$ with its old $\lambda(c)$. The children $c$ of $j$ have $c < j$, so they are done when the loop reaches $j$, and

$$M(j) = \min\Bigl(d(j, m),\ \min_{c : \pi(c) = j} \max(\lambda(c), M(c))\Bigr).$$

By induction on the index, $M(c) = \nu(c)$. For $j' \in \text{Desc}(c)$, Lemma 2 gives $u(j', c) < \lambda(c)$ or $j' = c$, and Lemma 1 gives $u(c, j) = \lambda(c)$, so $u(j', j) = \lambda(c)$. Hence $\max(\lambda(c), \nu(c)) = \min_{j' \in \text{Desc}(c)} \max(d(j', m), u(j', j))$. The set $\text{Desc}(j)$ is $\{j\}$ with the disjoint sets $\text{Desc}(c)$ of the children, so $M(j) = \nu(j)$. $\square$

**Lemma 5.** $\nu(j) \ge \mu(j)$. If $\mu(j) < \lambda(j)$, then $\nu(j) = \mu(j)$. If $\mu(j) \ge \lambda(j)$, then $\nu(j) \ge \lambda(j)$.

*Proof.* $\nu(j)$ is the minimum of the terms of $\mu(j)$ over a subset. By Lemma 2, each point $j'$ outside $\text{Desc}(j)$ has $u(j, j') \ge \lambda(j)$, so its term is at least $\lambda(j)$. If $\mu(j) < \lambda(j)$, the least term comes from a point of $\text{Desc}(j)$. If $\mu(j) \ge \lambda(j)$, each term is at least $\lambda(j)$. $\square$

**Lemma 6 (after the first loop).** After the loop of line L4, $\lambda(j) = \lambda'(j)$ for each $j < m$. Also $\pi(j) = \pi'(j)$, except when $\mu(j) = \lambda(j) < \nu(j)$, where $\pi(j)$ is the old pointer and $\pi'(j) = m$.

*Proof.* Line L5 compares the old $\lambda(j)$ with $M(j) = \nu(j)$. If $\mu(j) < \lambda(j)$, then $\nu(j) = \mu(j) < \lambda(j)$, and line L7 sets $\lambda(j) = \mu(j) = \lambda'(j)$ and $\pi(j) = m = \pi'(j)$. If $\mu(j) > \lambda(j)$, then $\nu(j) > \lambda(j)$, and nothing changes, which is right by Lemma 3. If $\mu(j) = \lambda(j) = \nu(j)$, line L7 sets $\lambda'(j)$ and $\pi'(j) = m$. If $\mu(j) = \lambda(j) < \nu(j)$, then $\lambda(j)$ is right but $\pi(j)$ keeps the old value. $\square$

**Lemma 7 (the second loop).** After the loop of line L9, $\pi = \pi'$.

*Proof.* The loop reads $\lambda$, which it does not change, and changes only $\pi(j)$ at the turn of $j$. So the order does not matter. If $\pi(j) = m$ already, the test of line L10 is $\lambda'(j) \ge \lambda(m) = \infty$, which fails since $\lambda'(j) \le \mu(j) < \infty$. Otherwise $p = \pi(j)$ is the old pointer, $\lambda'(j) = \lambda(j) \le \mu(j)$, and we must show that the test holds exactly when $\mu(j) = \lambda(j)$. By Lemma 1, $u(j, p) = \lambda(j)$ and $\lambda(p) > \lambda(j)$, and $u'(j, p) \le \lambda(j)$.

- If $\mu(j) = \lambda(j)$, then $\mu(p) = u'(p, m) \le \max(u'(p, j), u'(j, m)) \le \lambda(j)$. So $\lambda'(p) \le \lambda'(j)$, the test holds, and $\pi(j) = m = \pi'(j)$.
- If $\mu(j) > \lambda(j)$, then $\mu(j) \le \max(u'(j, p), \mu(p)) \le \max(\lambda(j), \mu(p))$ forces $\mu(p) \ge \mu(j) > \lambda(j)$. With $\lambda(p) > \lambda(j)$, this gives $\lambda'(p) > \lambda'(j)$. The test fails, and $\pi(j) = \pi'(j)$. $\square$

**Theorem.** After step $m$ of line L1, $(\pi, \lambda)$ on $1, \ldots, m$ is the pointer representation of single linkage on the first $m$ points. So SLINK$(n, d)$ returns the representation for all $n$ points.

*Proof.* Induction on $m$. For $m = 1$, line L2 sets $\pi(1) = 1$ and $\lambda(1) = \infty$. For $m > 1$, line L2 sets the right values for $m$, and Lemmas 6 and 7 give the right values for $j < m$. $\square$

**From pointers to merges.** For each $h$, the clusters of $u_n$ at height $h$ are the components of the graph with the edges $\{j, \pi(j)\}$ for $\lambda(j) \le h$. Each such edge has $u_n(j, \pi(j)) = \lambda(j) \le h$, so its ends are in one cluster. Conversely, in a cluster $K$ at height $h$, each point $j \ne \max K$ has $\lambda(j) \le h$, and $\pi(j) \in K(j, \lambda(j)) \subseteq K$, with $\pi(j) > j$. So the pointer path from each point of $K$ stays in $K$ and ends at $\max K$. The $n - 1$ edges form a tree, so a union of $j$ and $\pi(j)$ for the points $j < n$ in increasing order of $\lambda(j)$ joins two different clusters each time, at height $\lambda(j)$, and gives the merges of the dendrogram.

**Running time.** Step $m$ calls $d$ for $m - 1$ pairs at line L3 and does $O(1)$ work for each $j < m$ in each of the two loops. The total is $\sum_m O(m) = \Theta(n^2)$, with $n(n - 1)/2$ calls of $d$. The memory is the three arrays $\pi$, $\lambda$ and $M$, which is $\Theta(n)$.
