---
title: The striped hash table is linearizable and deadlock-free
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page, with REMOVE as GET plus a deletion under the same lock. Write $\sigma(k) = h(k) \bmod L$ for the stripe of key $k$, and $C$ for $|T.buckets|$ at a given moment. The *map* of the table at a moment is the set of pairs stored in the buckets of the current array.

**Lemma 1 (stripe fact).** At each moment $L$ divides $C$. For each key $k$ and each bucket index $b = h(k) \bmod C$, $b \bmod L = \sigma(k)$.

*Proof.* The constructor requires $L \mid C$, and RESIZE replaces $C$ by $2C$, so $L \mid C$ always. If $L \mid C$, then $h(k) = qC + b$ for some integer $q$, and $qC \equiv 0 \pmod L$, so $b \equiv h(k) \pmod L$. $\square$

**Lemma 2 (who changes what).** (a) $T.buckets$ is written only at line L16, by a thread that holds all $L$ locks. (b) Bucket $b$ of the current array is changed only by a thread that holds lock $b \bmod L$ or holds all locks. (c) $T.count[i]$ is written only by a holder of lock $i$.

*Proof.* (a) Line L16 is the only write of the field, and it lies between lines L13 and L17. (b) PUT and REMOVE change bucket $h(k) \bmod C$ of the array they read at line L2 (or its analogue), while they hold lock $\sigma(k)$. They read the array while holding that lock, and by (a) the array cannot be replaced while any lock is held by them, so the bucket they change is in the current array; by Lemma 1 its index $b$ has $b \bmod L = \sigma(k)$. RESIZE fills a new array before line L16 publishes it, while it holds all locks. (c) The counter $\sigma(k)$ is changed at line L5 and in REMOVE under lock $\sigma(k)$. $\square$

**Lemma 3 (invariant).** Whenever no thread holds a lock, invariant (S) holds: each pair $(k, v)$ is in bucket $h(k) \bmod C$, no key is in two pairs, and $T.count[i]$ is the number of pairs with $\sigma(k) = i$. Moreover, at each moment, the pairs with keys of stripe $i$ are changed only by the current holder of lock $i$.

*Proof.* The second claim is Lemma 2 (b) with Lemma 1. For (S), we show that each critical section that starts in a state where (S) holds for its stripe leaves it holding. A PUT holds lock $\sigma(k)$ and looks only at bucket $h(k) \bmod C$. All pairs with key $k$ would be in that bucket by (S), so the search of line L3 finds the pair of $k$ if there is one. Line L4 replaces its value, and line L5 appends a pair with a new key to the right bucket and adds one to the right counter. So (S) holds after it. REMOVE is the same with a deletion. GET changes nothing. RESIZE holds all locks, so by Lemma 2 no other thread changes any bucket or counter while it runs; line L15 moves each pair to bucket $h(k) \bmod 2C$ of the new array, which keeps the keys unique and the counters right, and line L16 makes $2C$ the capacity. The map does not change. $\square$

**Theorem (linearizability).** Every history of the table is linearizable with respect to the sequential dictionary.

*Proof.* Let the linearization point of each PUT, GET and REMOVE be the step at which it completes its acquire of lock $\sigma(k)$ (line L1 or line L10). This step is inside the call. A pending call that has not taken its lock has changed nothing; remove it. A pending call that holds its lock may have changed its bucket; it holds the lock for ever in this history, so no other call on its stripe takes a later point. Keep it if it has made its change (complete it with the result it computed), else remove it. A RESIZE inside a PUT does not change the map (Lemma 3), so it needs no point.

Order the kept calls by their points into the sequential history $S$. If call $a$ returns before call $b$ starts, the point of $a$ comes first, so $S$ keeps real time. It remains to show that each call has in $S$ the result it has in the history.

Take a call $o$ on key $k$, with point $t$. In the sequential dictionary, the result of $o$ depends only on the earlier calls on the same key $k$: a put, get or remove on key $k' \ne k$ never changes the value of $k$. The calls on key $k$ all take the same lock $\sigma(k)$, so their critical sections are disjoint and ordered as their points. So each call on key $k$ with a point before $t$ has finished its critical section before $o$ takes the lock, and each call on $k$ with a later point has not yet started its critical section. By the second claim of Lemma 3, the only changes to the pairs of stripe $\sigma(k)$ while $o$ holds the lock are its own, and RESIZE does not change the map. So $o$ sees, for key $k$, exactly the value that the calls on $k$ before $t$ produce in $S$, and it returns what the sequential dictionary returns at that place of $S$. $\square$

**Theorem (deadlock-freedom).** If each lock is deadlock-free, then whenever calls are pending and the threads keep taking steps, some call returns.

*Proof.* Outside RESIZE a thread holds at most one lock, and it waits for no other lock while it holds it. Inside RESIZE a thread waits for lock $i$ only while it holds locks $0, \ldots, i-1$. So each thread that holds locks and waits waits for a lock with a larger index than each lock it holds. A cycle of waits $t_1 \to t_2 \to \cdots \to t_1$, where $t_j$ waits for a lock held by $t_{j+1}$, would then need an index that increases strictly around the cycle, which is impossible. Each critical section is finite: a PUT, GET or REMOVE scans one finite chain, and a RESIZE moves the finite set of pairs. So a lock holder that takes steps releases its locks, and some waiter then enters by deadlock-freedom of the lock, and finishes. $\blacksquare$

A RESIZE may run twice for one doubling only if line L14 were absent: the second caller passes the capacity $C$ it saw, finds the capacity $2C$, and does nothing. So each doubling happens once per distinct full capacity.
