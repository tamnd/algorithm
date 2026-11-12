---
tag: VFWZYA
kind: algorithm
slug: mq-cache
name: Multi-queue (MQ) caching
aliases:
- MQ replacement
area: systems/caching-policies
level: advanced
summary: m LRU queues by the log of the reference count, an expiry time that moves idle blocks down one queue, and a history Qout of evicted counts. Built for second-level caches.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size in blocks, m: the number of queues, h: the size of Qout}
  time: {expected: O(n m)}
  space: {extra: Θ(k + h + m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2001
  people: [Yuanyuan Zhou, James F. Philbin, Kai Li]
  note: Zhou, Philbin and Li presented MQ at the USENIX Annual Technical Conference in 2001 for buffer caches below a client cache, such as storage servers.
prereqs: [lru, lfu]
see_also: [two-q, slru, lfu, lru-k, arc, lirs, ghost-lists, cache-replacement-policy]
sources:
  - paper: "Yuanyuan Zhou, James F. Philbin and Kai Li, The multi-queue replacement algorithm for second level buffer caches, Proceedings of the USENIX Annual Technical Conference, 2001, 91-104"
    title: The multi-queue replacement algorithm for second level buffer caches
    locator: the three properties of a good second level policy, the MQ pseudocode with lifeTime, QueueNum and Qout, and the comparison with LRU, LFU, 2Q, LRU-2 and FBR on server traces
  - paper: "Yuanyuan Zhou, Zhifeng Chen and Kai Li, Second-level buffer cache management, IEEE Transactions on Parallel and Distributed Systems 15(6), 2004, 505-519"
    title: Second-level buffer cache management
    locator: the journal version of MQ, with more traces and the setting of lifeTime from the temporal distance
---

Multi-queue (MQ) is a [cache replacement policy](/cache-replacement-policy/) by Zhou, Philbin and Li (2001) for **second-level** buffer caches, such as the cache of a storage server below the caches of its clients. The clients' caches absorb the requests with short reuse, so the requests that reach the server are spread out in time, and [LRU](/lru/) does poorly on them. MQ keeps $m$ LRU queues $Q_0, \ldots, Q_{m-1}$. A block with reference count $f$ lives in queue $\min(m - 1, \lfloor \log_2 f \rfloor)$, so a block needs about twice as many references to climb one more queue. Each block has an expiry time. When the head of a queue has not been requested for $lifeTime$ requests, it moves down one queue. The victim is the least recently used block of the lowest non-empty queue. A history buffer $Q_{out}$ remembers the counts of recently evicted blocks, so a block that comes back soon keeps its rank.

## In plain words

Picture a building with several floors. A new item goes to the ground floor. Each time someone asks for an item again, its count goes up, and when the count doubles, the item moves up one floor. When space runs out, the item that has waited longest on the lowest floor that has items has to leave.

High floors are safe, but not for ever. If the item at the front of a floor is not asked for during a set time, it moves down one floor. So an item that was popular long ago slowly comes down and can leave.

When an item leaves, its count goes on a short list at the door. If it comes back while still on the list, it gets its old count back and goes straight to its old floor.

## The problem

The model is the [paging problem](/paging-problem/): a cache of $k$ blocks of equal size, a request sequence $\sigma$ of length $n$, an empty cache at the start, and the number of misses as the cost. MQ is online and deterministic. Zhou, Philbin and Li studied the requests that reach a second-level cache. They found that few of them come back within a short distance, and that the blocks with many references matter most. They asked for three properties: a block must stay long enough to see its next reference (**minimal lifetime**), blocks with more references must have a higher rank (**frequency-based priority**), and blocks that were used often long ago must lose their rank (**temporal frequency**).

## The algorithm

MQ has three parameters: the number of queues $m$, the time $lifeTime$, measured in requests, and the size $h$ of $Q_{out}$. Each queue is an LRU list with its least recently used block at the **head**. For each resident block $x$, MQ keeps a count $f[x]$ and an expiry time $expire[x]$. $Q_{out}$ is a FIFO list of identifiers with their counts, and it holds no data.

```pseudo id=main
MQ-ACCESS(x)                   ▷ Q0..Qm−1 LRU, head = LRU end; Qout FIFO
L1  now ← now + 1; if x is resident then
L2      remove x from its queue; f[x] ← f[x] + 1; result ← hit
L3  else
L4      if x ∈ Qout then f[x] ← Qout[x] + 1; remove x from Qout
L5      else f[x] ← 1
L6      if k blocks are resident then EVICT()
L7      result ← miss
L8  expire[x] ← now + lifeTime
L9  add x to the tail of Q[min(m − 1, ⌊log2 f[x]⌋)]
L10 ADJUST(); return result

EVICT()
L11 v ← the head of the first non-empty queue; remove v
L12 if h > 0 and |Qout| = h then remove the head of Qout
L13 if h > 0 then add v with f[v] to the tail of Qout

ADJUST()
L14 for j ← 1 to m − 1 do
L15     if Qj is not empty then c ← the head of Qj
L16         if expire[c] < now then
L17             move c to the tail of Qj−1; expire[c] ← now + lifeTime
```

ADJUST looks only at the head of each queue, so it costs $O(m)$ per request, and an idle block moves down at most one queue per request. A block that moves down keeps its count. Its next request puts it back in the queue that its count gives. The paper suggests $m = 8$ and $h$ equal to four times the number of blocks of the cache, and it sets $lifeTime$ from the **temporal distance**, the number of requests between two references to the same block, at the peak of its distribution on the workload.

## Example

Run MQ with $k = 3$, $m = 2$, $lifeTime = 6$ and $h = 2$ on $a, a, b, c, d, b, e, f, g, a, b$. A count of 1 gives $Q_0$, and a count of 2 or more gives $Q_1$. Each block is written as $x^{f}_{e}$, with its count $f$ and its expiry time $e$, and each queue from its head to its tail.

| $t$ | request | result | evicted | $Q_0$ | $Q_1$ | $Q_{out}$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | a | miss | | $a^1_7$ | | |
| 2 | a | hit | | | $a^2_8$ | |
| 3 | b | miss | | $b^1_9$ | $a^2_8$ | |
| 4 | c | miss | | $b^1_9\ c^1_{10}$ | $a^2_8$ | |
| 5 | d | miss | b | $c^1_{10}\ d^1_{11}$ | $a^2_8$ | b:1 |
| 6 | b | miss | c | $d^1_{11}$ | $a^2_8\ b^2_{12}$ | c:1 |
| 7 | e | miss | d | $e^1_{13}$ | $a^2_8\ b^2_{12}$ | c:1 d:1 |
| 8 | f | miss | e | $f^1_{14}$ | $a^2_8\ b^2_{12}$ | d:1 e:1 |
| 9 | g | miss | f | $g^1_{15}\ a^2_{15}$ | $b^2_{12}$ | e:1 f:1 |
| 10 | a | hit | | $g^1_{15}$ | $b^2_{12}\ a^3_{16}$ | e:1 f:1 |
| 11 | b | hit | | $g^1_{15}$ | $a^3_{16}\ b^3_{17}$ | e:1 f:1 |

At $t = 6$, $b$ misses, but $Q_{out}$ still has its count 1, so $b$ comes back with count 2 and goes to $Q_1$. From $t = 5$ to $t = 9$ the new blocks evict only from $Q_0$. At $t = 9$, the head $a$ of $Q_1$ has $expire = 8 < 9$, so ADJUST moves it to the tail of $Q_0$. It is behind $g$ there, so $g$ would go first, and $a$ is hit at $t = 10$. MQ has 8 misses. LRU with 3 blocks evicts $a$ at $t = 5$ and $b$ at $t = 9$, and has 9 misses.

## Correctness

After each request the $m$ queues are disjoint, they hold exactly the resident blocks, at most $k$ blocks are resident, $Q_{out}$ holds at most $h$ identifiers, none of them resident, and the requested block is resident. When the cache is full at line L6, some queue is not empty, so EVICT has a victim. With $m = 1$ there is only $Q_0$, ADJUST does nothing, and MQ is LRU. The proofs are below.

## Complexity

- **Time.** Each queue is a hash map from block identifiers to the nodes of a [doubly linked list](/doubly-linked-list/), and $Q_{out}$ is one more. Lines L1 to L9 take $O(1)$ expected time, and lines L11 and L14 to L17 take $O(m)$. So $n$ requests take $O(n m)$ expected time. With $m = 8$, as in the paper, this is a small constant per request, as for LRU.
- **Space.** $\Theta(k + h + m)$: the resident blocks with their counts and expiry times, $h$ entries of $Q_{out}$ and $m$ list heads.
- **Hit ratio.** On the server traces of the paper, MQ had higher hit ratios than LRU, [LFU](/lfu/), [2Q](/two-q/), [LRU-2](/lru-k/) and FBR at the second level.
- **Worst case.** With $h = 0$ and $lifeTime$ longer than the sequence, the requests $a, a, (x, y)^r$ with $k = 2$ and $m = 2$ cost MQ $1 + 2r$ misses, because $a$ holds $Q_1$ while $x$ and $y$ evict each other from the only other slot. An optimal policy has 3 misses. So MQ has no competitive bound that does not depend on its parameters.

## Properties

- **Logarithmic ranks.** A block climbs one queue each time its count doubles. A few references are enough to leave $Q_0$, and many more are needed for the top queues.
- **Aging by expiry.** ADJUST is what gives the temporal frequency property. Without it, MQ would keep blocks that were popular long ago, like LFU.
- **Ghost counts.** $Q_{out}$ is a [ghost list](/ghost-lists/) with counts. It lets a block that was evicted too early come back with its old rank.
- **Minimal lifetime.** A block of $Q_j$, $j \ge 1$, cannot be evicted while a lower queue has blocks, and it moves down at most one queue per $lifeTime$ requests while it is idle.

## Variants and improvements

- **$m = 1$.** One queue gives LRU.
- **No expiry.** With an infinite $lifeTime$, the queues never age, and MQ behaves like LFU on the classes $\lfloor \log_2 f \rfloor$, with LRU order inside each class.
- **Adaptive lifeTime.** The paper and its journal version set $lifeTime$ from the measured temporal distance, and change it as the workload changes.
- **SLRU with more segments.** [SLRU](/slru/) with several segments also moves blocks up on a hit and down on overflow, but it uses the overflow of a segment, not an expiry time, to move blocks down.
- **Other policies for the lower level.** [ARC](/arc/) and [LIRS](/lirs/) were later tested on second-level traces as well. They need no $lifeTime$ parameter.

## When to use it

Use MQ for a cache that sees requests filtered by a cache above it: a storage server under database or file system clients, a disk array controller, or a proxy below browser caches. Its parameters must fit the workload: a good $lifeTime$ is near the typical temporal distance, and the paper suggests $m = 8$. For a first-level cache with strong recency, LRU, [SLRU](/slru/) or [ARC](/arc/) are simpler and do as well.

## Pitfalls

- **Forgetting ADJUST.** Without the expiry step, blocks that were hot once stay in the top queues for ever, and MQ fails the temporal frequency property.
- **Resetting the count on expiry.** A block that moves down keeps its count $f$. Only its queue changes.
- **Ignoring $Q_{out}$ on a miss.** A block found in $Q_{out}$ must take its old count plus one, and its identifier must leave $Q_{out}$. Otherwise it starts again in $Q_0$, and a block can be both resident and in $Q_{out}$.
- **Checking all blocks for expiry.** Only the head of each queue needs a check. The head is the least recently used block of the queue, so it is the first to expire.
- **$lifeTime$ too short.** Blocks then fall to $Q_0$ before their next reference, and MQ is close to LRU.

## Implementations

## History

Zhou, Philbin and Li presented MQ at the USENIX Annual Technical Conference in 2001. They studied the buffer caches of storage servers, below the caches of database and file system clients, and found that the access patterns there differ from those at the first level. Their analysis of these patterns led to the three properties of minimal lifetime, frequency-based priority and temporal frequency, and to the design of MQ. Zhou, Chen and Li published a longer version in IEEE Transactions on Parallel and Distributed Systems in 2004.

## References
