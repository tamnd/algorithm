---
title: The bucket queue returns an item of smallest key
proves: [correctness, termination]
status: full
---

Let $S$ be the set of items in the queue, and for $x \in S$ let $\mathit{key}[x]$ be its key. The queue is correct if EXTRACT-MIN returns some $x \in S$ with $\mathit{key}[x] = \min_{y \in S} \mathit{key}[y]$, removes it, and the other operations change $S$ and the keys as their names say.

**Invariants.** Between operations:

> **(B)** for each $k$, the bucket $B[k]$ holds exactly the items $x \in S$ with $\mathit{key}[x] = k$, and each item at most once;
>
> **(C)** $0 \le \mathit{cur} \le C + 1$, and $B[k]$ is empty for each $k < \mathit{cur}$.

*Initially* $S$ is empty, every bucket is empty, and $\mathit{cur} = C + 1$, so (B) and (C) hold.

**INSERT$(x, k)$** with $0 \le k \le C$ and $x \notin S$. Line L2 adds $x$ to $S$ with key $k$ and appends it to $B[k]$ only, so (B) holds. If $k \ge \mathit{cur}$, the only bucket that changed has index at least $\mathit{cur}$, so (C) holds. Else line L3 sets $\mathit{cur} = k$; the buckets below $k$ were below the old cursor and are empty, so (C) holds.

**DELETE$(x)$** with $x \in S$. By (B), $x$ is in $B[\mathit{key}[x]]$ and nowhere else. Line L4 removes it from that bucket and from $S$, so (B) holds. A bucket only lost an item, so (C) holds.

**DECREASE-KEY$(x, k)$** with $k \le \mathit{key}[x]$ is a DELETE followed by an INSERT of the same item with key $k$, so both invariants hold, and afterwards $\mathit{key}[x] = k$.

**EXTRACT-MIN.** Let $S$ be non-empty, and let $\mu = \min_{y \in S} \mathit{key}[y]$. By (B), $B[\mu]$ is non-empty, and by (C), $\mu \ge \mathit{cur}$, so $\mathit{cur} \le \mu \le C$.

*The loop of line L8.* Claim: before each test, $\mathit{cur} \le \mu$ and $B[k]$ is empty for each $k < \mathit{cur}$. It holds before the first test, as shown. If the test is true, $B[\mathit{cur}]$ is empty, so $\mathit{cur} \ne \mu$ and $\mathit{cur} < \mu$; after the increment, $\mathit{cur} \le \mu$ and $B[k]$ is empty for each $k$ below the new cursor. Each iteration raises $\mathit{cur}$ by one and $\mathit{cur} \le \mu$ stays true, so the loop stops after at most $\mu - \mathit{cur}$ iterations, and it never reads a bucket beyond $C$.

When it stops, $B[\mathit{cur}]$ is non-empty, so by (B) some item has key $\mathit{cur}$, hence $\mu \le \mathit{cur}$, and with the claim, $\mathit{cur} = \mu$. Line L9 takes an item $x$ of $B[\mu]$, so $\mathit{key}[x] = \mu$, and line L10 deletes it. Line L11 returns $(x, \mu)$. The loop kept (C), and DELETE keeps (B) and (C).

**FIND-MIN** is the same without line L10, and it changes only the cursor, which keeps (C).

**Theorem.** Each sequence of operations on a bucket queue with keys in $0 \ldots C$ stops, and each EXTRACT-MIN or FIND-MIN on a non-empty queue returns an item of smallest key and that key. Items with equal keys come out in the order in which they last entered their bucket.

*Proof.* Each operation other than EXTRACT-MIN and FIND-MIN is straight-line code, and their loop stops, as shown. The first claim is the analysis of EXTRACT-MIN above. For the last, each bucket is a first-in, first-out list, and line L9 takes its first item. $\blacksquare$
