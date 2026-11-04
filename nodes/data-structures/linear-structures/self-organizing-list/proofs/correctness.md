---
title: Each operation of a self-organizing list keeps the invariant and returns the right result
proves: [correctness, termination]
status: full
---

**Statement.** Let $L$ satisfy the invariant (I1), (I2) and, under the rule COUNT, (I3), for a map $M$ from keys to values. Then each of ACCESS, GET, PUT and DELETE stops, the invariant holds after it, and:

- ACCESS$(L, k)$ returns the node of $k$ when $k \in M$ and nil otherwise, and the map is still $M$;
- GET$(L, k)$ returns $M(k)$ when $k \in M$ and nil otherwise, and the map is still $M$;
- after PUT$(L, k, v)$ the map is $M$ with $k$ mapped to $v$;
- after DELETE$(L, k)$ the map is $M$ without $k$.

**Setup.** Let the nodes be $N_1, \ldots, N_n$ in list order, with $n = L.n$, before the operation. By (I1) this order is well defined and $N_n.next = nil$.

**Lemma 1 (the scan of ACCESS).** The loop of lines L2 and L3 stops. At its exit, either $cur = nil$ and no node has key $k$, or $cur = N_i$ is the only node with key $k$, $prev = N_{i-1}$ and $pp = N_{i-2}$, where $N_0$ and $N_{-1}$ mean nil.

*Proof.* Each time line L2 tests its condition, the invariant is: $cur = N_j$ for some $1 \le j \le n + 1$ (with $N_{n+1}$ meaning nil), $prev = N_{j-1}$, $pp = N_{j-2}$, and no node among $N_1, \ldots, N_{j-1}$ has key $k$. Line L1 makes it true with $j = 1$. If the test succeeds, $cur = N_j$ with $j \le n$ and $N_j.key \ne k$, and line L3 moves the three pointers one node forward, so the invariant holds for $j + 1$. The number $n + 1 - j \ge 0$ drops by exactly 1 in each round, so the loop runs at most $n$ rounds. At the exit, either $cur = nil$, so $j = n + 1$ and no node has key $k$, or $cur.key = k$, and by (I2) $N_j$ is the only such node. $\square$

**Lemma 2 (the move).** If ACCESS finds $cur = N_i$, then after line L11 the list holds the same $n$ nodes, each once, and ends in nil. Under COUNT, the counts do not increase along the list, and the count of $N_i$ is 1 more than before.

*Proof.* Line L5 makes the predecessor of $N_i$ (or $L.head$ when $i = 1$) point to $N_{i+1}$, so the list from $L.head$ is $N_1, \ldots, N_{i-1}, N_{i+1}, \ldots, N_n$, a list of $n - 1$ nodes that ends in nil. Lines L6 to L10 do not change any $next$ field. They set $p$ to nil or to a node of this shorter list: under MTF $p = nil$; under TRANSPOSE $p = pp = N_{i-2}$, a node of the shorter list or nil; under COUNT, $p$ is nil or a node reached from $L.head$ by line L10. Line L11 links $N_i$ at the front when $p = nil$, and else between $p$ and the node after $p$. In both cases the list is the shorter list with $N_i$ put in at one place, so it holds each of the $n$ nodes once and ends in nil.

Under COUNT, let $c$ be the old count of $N_i$. By (I3), the counts of $N_1, \ldots, N_{i-1}$ are at least $c$, and those of $N_{i+1}, \ldots, N_n$ are at most $c$. Line L9 sets the count of $N_i$ to $c + 1$. The loop of line L10 walks the shorter list, which has non-increasing counts, and stops at the first node $q$ with $q.count < c + 1$, or at nil; $p$ is the node just before $q$, or nil if $q$ is the first node. This loop also stops: it advances one node per round along a list of $n - 1$ nodes. Every node before the new place of $N_i$ has count at least $c + 1$, and every node after it has count at most $c$, since the counts are non-increasing and $q.count \le c$. So the counts along the new list do not increase. The other counts do not change, so the second part of (I3) holds: the count of $k$ grows by 1 for this successful access. $\square$

**ACCESS.** If $k \notin M$, Lemma 1 gives $cur = nil$, line L4 returns nil, and nothing changes. If $k \in M$, Lemma 2 shows that (I1) and (I3) hold after the move. The pairs stored in the nodes do not change (only $next$ and $count$ fields change), so (I2) holds for the same map $M$. Line L12 returns $N_i$, the node of $k$.

**GET.** By the result of ACCESS, line P2 returns $M(k)$ or nil.

**PUT.** If ACCESS returns a node $x$, it is the node of $k$, and line P4 sets its value to $v$. The keys do not change, so (I1) to (I3) still hold, and the map is $M$ with $k \mapsto v$. Otherwise $k \notin M$, and line P5 makes one new node with key $k$, value $v$ and count 1, and adds 1 to $L.n$. Line P6 or P7 links it at the front or at the end, so the list has $L.n$ nodes and ends in nil (I1). The keys are still distinct, since $k$ was absent, and the pairs are those of $M$ plus $(k, v)$ (I2). Under COUNT the new node is last, and its count 1 is at most every other count, which are all at least 1; its count is 1 plus its 0 accesses (I3).

**DELETE.** The scan of lines D1 and D2 is the scan of Lemma 1 without $pp$, so it stops at the node of $k$ or at nil. If $k \notin M$, line D3 returns with no change. Otherwise line D4 unlinks $N_i$ as line L5 does, and line D5 lowers $L.n$ by 1. The list holds the other $n - 1$ nodes in their old order (I1), the pairs are those of $M$ without $k$ (I2), and a sublist of a non-increasing sequence is non-increasing, with each count unchanged (I3). $\blacksquare$
