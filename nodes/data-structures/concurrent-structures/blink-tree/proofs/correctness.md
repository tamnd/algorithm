---
title: The B-link tree is a linearizable, deadlock-free map with lock-free searches
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page. A READ or WRITE of a node is one atomic step on its whole page, and so are the reads and writes of the anchor (the root and the height). LOCK and UNLOCK are those of a mutex. Keys come from a totally ordered set, extended by $-\infty$ and $+\infty$.

**Writers.** Every WRITE of an existing node $n$ is done by the holder of $n$'s lock, and the write of a new node $u$ at line L14 happens before any pointer to $u$ is written. So while a thread holds the lock of $n$, the page it read after locking is the current page of $n$, and it stays current until this thread writes it.

**Low bounds.** Give each node a fixed low bound: $-\infty$ for the first leaf and for each new root, and $low(u) = y$ for the node $u$ created by a split at line L14, where $y$ is the new high key of the node that split. A node is *in the chain* of its level once a pointer to it has been written.

**Lemma 1 (the chain invariant).** At every moment, for each level $L$ up to the height:

1. The nodes of level $L$ in the chain, from the leftmost node of the level along the right links, are $n_1, n_2, \ldots, n_r$ with $low(n_1) = -\infty$, $low(n_{j+1}) = high(n_j)$ and $high(n_r) = +\infty$, so their ranges $(low(n_j), high(n_j)]$ partition the keys.
2. Every key of a page lies in the range of its node (for an internal node, every separator except the last lies inside the range, and the last equals the high key).
3. For an internal node with entries $(m_1, c_1), \ldots, (m_s, c_s)$: $low(c_1) = low(n)$, and $low(c_i) = m_{i-1}$ for $i > 1$; each $c_i$ is a node of the level below in the chain.

*Proof.* We prove Lemma 1 and Lemma 2 together, by induction on the steps of the execution: Lemma 2 for walks up to a step uses Lemma 1 for the states before it, and Lemma 1 after a write uses Lemma 2 for the walk of the writer. Initially there is one leaf with range $(-\infty, +\infty]$. We check every write.

A write at line L9, L13 or L20 of a node $n$ changes its keys but not its high key or link. At line L13 the inserted key $y$ is in the range of $n$: the thread reached $n$ with $y > low(n)$ (Lemma 2 below) and moved right until $y \le high(n)$. At an internal node, the entry $(m, c)$ with the smallest $m \ge y$ becomes $(y, c), (m, u)$; part 3 still holds for $c$, and $low(u) = y$ is the new separator before $u$. So 2 and 3 hold. Deletions only remove keys.

The write of $u$ at line L14 changes no node in the chain. The write of $n$ at line L14 replaces the page $A$, with range $(low(n), h]$ and link $\ell$, by $A'$ with high key $y = \max(A')$ and link $u$, while $u$ holds $B$ with high key $h$ and link $\ell$. So in the chain, $n$ is replaced by $n, u$ with ranges $(low(n), y]$ and $(y, h]$, and part 1 holds. The keys of $A$ that are at most $y$ are in $A'$, and the others in $B$, so part 2 holds. If $A$ is internal, $B$ starts with an entry whose child has low bound equal to the separator before it in $A$, which is $y = low(u)$, so part 3 holds for $u$, and it is unchanged for $n$.

A new root with entries $(y, old)$ and $(+\infty, u)$ is made only if $old$ is the root, so $old$ is the leftmost and, before its split, only node of its level: then the level is $old, u$, and the new root satisfies 1 to 3 with range $(-\infty, +\infty]$. The height grows by one at the same step. $\square$

**Lemma 2 (routing).** Suppose a thread at level $L$ reads node $n$ while looking for key $k$ with $k > low(n)$. If $k > high(n)$ in the page read, the link $n'$ satisfies $k > low(n') = high(n)$. If $k \le high(n)$ and $n$ is internal, the chosen child $c_i$ satisfies $k > low(c_i)$. So every node that SEARCH, the descents of lines L7, L16 and L19, and MOVE-RIGHT visit has $k > low$, and the last node read covers $k$ at the moment of its read.

*Proof.* The first case is part 1 of Lemma 1. In the second, $m_{i-1} < k \le m_i$, and $low(c_i) = m_{i-1}$ by part 3, or $c_1$ has $low(c_1) = low(n) < k$. Every walk starts at the root, of low bound $-\infty$. A walk stops at level $L$ only when $k \le high(n)$ in the page just read, and with $k > low(n)$ the node covers $k$ at that read. Since low bounds never change, $k > low(n)$ stays true after the read. For the move right at the parent with key $y$ in line L17: the popped node $p$ was visited at the level above on the way to the leaf, so $k > low(p)$; the leaf $n$ that split had $low(n) \ge$ the low bound of the node reached from $p$, which is at least $low(p)$, and $y = \max(A')$ with $A'$ nonempty and inside $(low(n), \ldots]$, so $y > low(p)$. The same holds by induction at each higher level. $\square$

**The abstract map.** At each moment, the map $M$ is the set of pairs in the pages of the leaves in the chain. By part 1 and 2 of Lemma 1, each key is in at most one leaf, the one whose range holds it.

**Theorem (linearizability).** Each history of the B-link tree is linearizable with respect to the sequential ordered map.

*Proof.* Choose the points:

- a search: its last READ, at line L2 or L5;
- an insert that finds $k$ present: its WRITE at line L9; an insert of a new key: its WRITE of the leaf, at line L13 or at the second WRITE of line L14;
- a delete that finds $k$: its WRITE at line L20; a delete that does not: the READ of the locked leaf after MOVE-RIGHT.

Each point is inside its call, so the order of the points respects real time; pending calls past their point are completed, the others removed.

Search: by Lemma 2 its last page read is of the leaf that covers $k$ at that moment, so the value it returns is $M(k)$ then, or NIL.

Updates: by Lemma 2 the leaf $n$ locked after MOVE-RIGHT covers $k$, and since the thread holds the lock, its page is the current page and $n$ keeps covering $k$ until the thread writes it (only a split of $n$, by a lock holder, could shrink its range). An insert that finds $k$ changes only the value of $k$ in $M$ and returns the old value. An insert of a new key at line L13 adds $(k, v)$ to the leaf that covers $k$. At line L14, the first WRITE, of $u$, changes no leaf in the chain, so it does not change $M$; the second puts $A'$ and $B$ in the chain, whose pairs are the old pairs of $n$ plus $(k, v)$. So $M$ gains exactly $(k, v)$, and the insert returns NIL as it should. All later steps of the insert act on internal nodes or the anchor and do not change $M$. A delete removes $k$ from the leaf that covers it and returns its value; a delete that does not find $k$ in the current page of the covering leaf returns NIL with $M(k)$ undefined at that moment. Every write of a leaf page is one of these points, so $M$ changes only at linearization points, each by the change of the sequential map. $\square$

**Theorem (progress).** Searches take no locks and never wait. Updates are deadlock-free: if threads keep taking steps, some update that has started finishes, and with finitely many updates every operation finishes.

*Proof.* Order the nodes by (level, low bound). This order is fixed, since neither changes, and it is total among nodes of the chain, since low bounds on a level are distinct by part 1 of Lemma 1. An update that holds locks only waits for a lock that is higher in the order: at line L18 it holds $n$ and waits for the link, of a larger low bound on the same level; at line L17 it holds $old$ and waits for a node one level up. So a cycle of threads waiting for locks is impossible. The anchor is held only inside one atomic step, so nobody waits for it. The only other wait is the loop of line L16 when the top level has a node $old$ that is not the root: then the root $r$ has split, its new right part is in the chain, and the thread that split $r$ holds the lock of $r$ until it makes the new root, which it does at its next step with the anchor without waiting for anything. So every waiting thread waits for a thread that is not waiting, or for one that waits for a higher lock, and the highest one in a chain of waits makes progress.

Each update does at most one split per level, and the number of levels grows only by root splits, so an update that keeps getting locks finishes after a bounded number of its own steps plus the moves right. A walk at level $L$ moves right only past nodes that exist in the chain between its node and the one that covers $k$; each move right passes a node created by a split, and with finitely many updates there are finitely many splits, so every walk ends. $\blacksquare$
