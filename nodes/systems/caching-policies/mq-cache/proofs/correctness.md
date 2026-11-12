---
title: MQ keeps each resident block in exactly one queue, always has a victim, keeps Qout apart from the cache, and is LRU when m is 1
proves: [correctness]
status: full
---

We use the pseudocode of the page, a cache of capacity $k \ge 1$, $m \ge 1$ queues, $lifeTime \ge 0$, $h \ge 0$, all queues and $Q_{out}$ empty at the start, and a request sequence $\sigma_1 \ldots \sigma_n$. Let $R$ be the set of resident blocks.

**Invariant.** After each request:

1. each block of $R$ is in exactly one of $Q_0, \ldots, Q_{m-1}$, and no other block is in a queue;
2. $|R| \le k$;
3. $|Q_{out}| \le h$, and no identifier in $Q_{out}$ is in $R$;
4. each block of $R$ has $f \ge 1$;
5. the requested block is in $R$.

*Proof.* By induction on the requests. At the start all sets are empty.

*A hit, lines L1 and L2.* The block $x$ is in exactly one queue by part 1. Line L2 removes it, and line L9 adds it to one queue, so part 1 holds again. $R$ and $Q_{out}$ do not change, and $f[x]$ grows, so parts 2 to 4 hold.

*A miss, lines L3 to L7.* The block $x$ is not in $R$. Line L4 removes $x$ from $Q_{out}$ if it is there, and sets $f[x] \ge 2$; otherwise line L5 sets $f[x] = 1$. If $|R| = k \ge 1$, then by part 1 the queues hold $k$ blocks, so some queue is not empty, and line L11 removes the head $v$ of the first non-empty queue. Then $v$ is in no queue and not in $R$, and $|R| = k - 1$. The block $v$ is not $x$, because $x$ was not resident. Lines L12 and L13 add $v$ to $Q_{out}$, after they remove the oldest entry if $Q_{out}$ is full, so $|Q_{out}| \le h$; with $h = 0$ nothing is added. Now $x \notin Q_{out}$, and line L9 adds $x$ to one queue. So $|R| \le k$, part 1 holds, and no identifier in $Q_{out}$ is resident.

*Line L9.* Since $f[x] \ge 1$, $\lfloor \log_2 f[x] \rfloor \ge 0$, and the index $\min(m - 1, \lfloor \log_2 f[x] \rfloor)$ is in $0, \ldots, m - 1$.

*ADJUST, lines L14 to L17.* Each move takes a block from the head of $Q_j$, $j \ge 1$, to the tail of $Q_{j-1}$. The block stays in exactly one queue, and $R$ and $Q_{out}$ do not change. So parts 1 to 5 hold. $\square$

The tests check these parts after each request, and compare the code with a direct version on Python lists, for random traces and random $k$, $m$, $lifeTime$ and $h$.

**Claim (EVICT takes the least recently used block of the lowest non-empty queue).** Inside each queue, blocks are in the order of their last move into it. A request adds its block at the tail, and ADJUST adds a moved block at the tail. So the head is the block that entered the queue first among those still there. Line L11 takes it from the queue with the smallest index that is not empty. This is the rule of the paper. $\square$

**Claim (LRU as a special case).** If $m = 1$, MQ has the same hits, misses and victims as LRU with $k$ blocks, for any $lifeTime$ and $h$.

*Proof.* With $m = 1$, the index at line L9 is always 0, and the loop of ADJUST is empty. So all blocks are in $Q_0$, and $Q_0$ changes only at lines L2, L9 and L11. A hit moves $x$ from its place to the tail, a miss in a full cache removes the head, and a miss adds $x$ at the tail. With the head as the least recently used end, these are the rules of LRU. The counts and $Q_{out}$ change the counts, but with one queue they do not change the queue, so they do not change any decision. $\square$

**Claim (an idle block moves down at most one queue per lifeTime requests).** When a block enters a queue at time $t$, at line L9 or at line L17, its expiry is $t + lifeTime$. Line L16 moves it only at a time $t' > t + lifeTime$. So between two moves of the same block, with no request to it, more than $lifeTime$ requests pass. A block of $Q_j$ that is not requested again stays resident at least while a queue $Q_i$, $i < j$, is not empty, and leaves $Q_j$ only after more than $lifeTime$ requests. $\square$

**Claim (not competitive with $h = 0$ and a long lifeTime).** Let $k = 2$, $m = 2$, $h = 0$ and $lifeTime \ge 2r + 2$. On $a, a, (x, y)^r$, MQ has $1 + 2r$ misses, and an optimal offline algorithm has 3.

*Proof.* The first $a$ misses, and the second $a$ hits and gives $f[a] = 2$, so $a$ enters $Q_1$ at time 2, with expiry $2 + lifeTime > 2r + 2$, the last time. So ADJUST never moves $a$. With $h = 0$, $Q_{out}$ stays empty, so each of $x$ and $y$ comes back with $f = 1$ and enters $Q_0$. When $x$ is requested, $y$ is the only block of $Q_0$, so EVICT removes $y$, and the other way round. So all $2r$ requests to $x$ and $y$ miss. An offline algorithm misses on $a$, on the first $x$ and on the first $y$, evicting $a$, and hits on all other requests. $\square$

With $h \ge 1$ on the same sequence, $x$ comes back from $Q_{out}$ with count 2, enters $Q_1$, and $Q_0$ becomes empty, so $a$ is evicted. MQ then has 5 misses. The tests check both cases for $r = 10, 40, 160$.

**Cost.** With a hash map and a doubly linked list per queue and for $Q_{out}$, lines L1 to L10 take $O(1)$ expected time, plus $O(m)$ for line L11 and $O(m)$ for ADJUST. So $n$ requests take $O(n m)$ expected time. The space is $\Theta(k + h + m)$.
