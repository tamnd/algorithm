---
title: MCS computes a maximum cardinality search order, and its reverse is a perfect elimination ordering exactly for chordal graphs
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a simple undirected graph with $n$ vertices. Write $x <_\sigma y$ if $x$ is visited before $y$. Before step $i$, the weight of an unvisited $x$ is $w(x) = |N(x) \cap \{v_1, \ldots, v_{i-1}\}|$, and $\ell(x) = N(x) \cap \{v_1, \ldots, v_{i-1}\}$ is the set that it counts.

## Part 1: the algorithm follows the MCS rule

**Invariant.** At the start of step $i$ (before line L3): for each unvisited $x$, $\mathrm{size}[x] = w(x)$ and $x \in B[w(x)]$; the buckets hold no visited vertex; and, if some vertex is unvisited, $j$ is the largest index of a non-empty bucket.

*Initialization.* Before step 1, no vertex is visited, every weight is 0, line L1 puts all of $V$ in $B[0]$ with $\mathrm{size} = 0$, and $j = 0$.

*Maintenance.* Step $i$ takes $v$ from $B[j]$ at line L3 and marks it at line L4, so it leaves the buckets. For an unvisited $x$, the new weight is $w(x) + 1$ if $x \in N(v)$ and $w(x)$ otherwise. Lines L5 and L6 run exactly for the unvisited neighbours of $v$, each one time, because the graph is simple. Each such $x$ moves one bucket up and its size grows by 1, so the first two parts hold after the step. Before the step, every weight was at most $j$. After it, every weight is at most $j + 1$. So after line L7, no bucket above $j$ is non-empty, and line L8 lowers $j$ to the largest non-empty bucket, or to $-1$ if all buckets are empty, which happens only when all vertices are visited.

**Lemma 1.** The order $\sigma$ returned by MCS obeys the MCS rule.

*Proof.* By the invariant, at step $i$ the bucket $B[j]$ holds the unvisited vertices of largest weight, and it is not empty because some vertex is unvisited. Line L3 takes one of them. $\square$

**Termination.** Each step visits one vertex, and line L2 runs $n$ times. Each step scans one finite list. The loop of line L8 lowers $j$ each time and stops at $-1$ at the latest.

## Part 2: the weak four-point property

**Lemma 2.** Let $\sigma$ be any order that obeys the MCS rule. If $a <_\sigma b <_\sigma c$, $ac \in E$ and $ab \notin E$, then there is a vertex $d <_\sigma b$ with $db \in E$ and $dc \notin E$.

*Proof.* Consider the step at which $b$ is chosen. Then $a$ is visited and $c$ is not, and $b$ has the largest weight, so $|\ell(b)| \ge |\ell(c)|$. Now $a \in \ell(c) \setminus \ell(b)$, so $|\ell(c) \setminus \ell(b)| \ge 1$. Because

$$|\ell(b) \setminus \ell(c)| = |\ell(b)| - |\ell(b) \cap \ell(c)| \ge |\ell(c)| - |\ell(b) \cap \ell(c)| = |\ell(c) \setminus \ell(b)| \ge 1,$$

there is a vertex $d \in \ell(b) \setminus \ell(c)$. It is visited before $b$, it is a neighbour of $b$, and it is not a neighbour of $c$. $\square$

## Part 3: chordal graphs

For a vertex $x$, let $E(x)$ be the set of its neighbours $y <_\sigma x$. The reverse of $\sigma$ is a perfect elimination ordering exactly when $E(x)$ is a clique for every $x$, because the neighbours of $x$ that come after $x$ in the reverse order are those that come before $x$ in $\sigma$.

**Lemma 3.** Let $\sigma$ obey the MCS rule on a chordal graph $G$. Then there are no two non-adjacent vertices $u <_\sigma w$ joined by a path whose internal vertices are all visited after $w$.

*Proof.* Call such a pair $(u, w)$ *bad*. Assume bad pairs exist, and choose one in which the later vertex $w$ is as early in $\sigma$ as possible. Among the paths for this pair, choose a shortest one, $P = u, z, \ldots, w$. It has at least one internal vertex, since $uw \notin E$, so $z$ is internal and $w <_\sigma z$. The path is chordless: a chord would give a shorter path between $u$ and $w$ whose internal vertices are a subset of those of $P$.

Apply Lemma 2 to $u <_\sigma w <_\sigma z$, with $uz \in E$ and $uw \notin E$. It gives $d <_\sigma w$ with $dw \in E$ and $dz \notin E$. Then $d \ne u$, because $uz \in E$. Also $d$ is not on $P$: every vertex of $P$ other than $u$ is $w$ or after $w$.

The walk $d, w, \ldots, z, u$, which is $d$ followed by $P$ backwards, is a path from $d$ to $u$. Its internal vertices are $w$ and the internal vertices of $P$, and they are all visited after $w$, so after both $d$ and $u$. If $du \notin E$, then the pair of $d$ and $u$, in the order of $\sigma$, is bad, and its later vertex is before $w$. This contradicts the choice of $w$. So $du \in E$.

Now $d$ is adjacent to $u$ and to $w$, but not to $z$. Walk along $P$ from $u$, and let $y$ be the first vertex after $u$ that is adjacent to $d$. It exists, because $w$ is adjacent to $d$, and $y \ne z$. The cycle $d, u, z, \ldots, y, d$ has at least 4 vertices, because the part of $P$ from $u$ to $y$ has at least 3. It has no chord: the part of $P$ is chordless, $u$ and $y$ are not adjacent because $P$ is chordless and $y$ is not the next vertex $z$ after $u$, and $d$ is adjacent to no vertex strictly between $u$ and $y$ by the choice of $y$. A chordless cycle of length at least 4 contradicts that $G$ is chordal. $\square$

**Theorem 1 (Tarjan and Yannakakis).** Let $\sigma$ be an order that obeys the MCS rule, in particular the output of MCS. Then $G$ is chordal if and only if the reverse of $\sigma$ is a perfect elimination ordering.

*Proof.* Let $G$ be chordal, and assume that some $E(c)$ contains two non-adjacent vertices $a <_\sigma b$. Then $a, c, b$ is a path between the non-adjacent vertices $a <_\sigma b$ whose only internal vertex $c$ is visited after $b$. Lemma 3 forbids this. So every $E(x)$ is a clique.

Conversely, let every $E(x)$ be a clique, and let $C$ be a cycle of length at least 4. Let $x$ be the vertex of $C$ visited last. Its two neighbours on $C$ are in $E(x)$, so they are adjacent. They are not consecutive on $C$, because $C$ has length at least 4, so this edge is a chord. So $G$ is chordal. $\blacksquare$

**Lemma 4 (the linear-time test).** For each $x$ with $E(x) \ne \emptyset$, let $p(x)$ be the vertex of $E(x)$ visited last. Then every $E(x)$ is a clique if and only if, for every $x$, each vertex of $E(x) \setminus \{p(x)\}$ is adjacent to $p(x)$.

*Proof.* If every $E(x)$ is a clique, the test holds. Conversely, assume the test holds, and show that $E(x)$ is a clique by induction on the position of $x$ in $\sigma$. Take $y \ne z$ in $E(x)$. If one of them is $p(x)$, they are adjacent by the test. If not, both are adjacent to $p(x)$ by the test and are visited before $p(x)$, so both are in $E(p(x))$, which is a clique by the induction hypothesis, since $p(x) <_\sigma x$. $\square$

**Corollary.** MCS followed by the test of Lemma 4 decides in $O(n + m)$ time whether $G$ is chordal, and if it is, the reverse of $\sigma$ is a perfect elimination ordering. This follows from Lemma 1, Theorem 1 and Lemma 4. $\blacksquare$
