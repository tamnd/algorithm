---
tag: E3Q27Y
kind: technique
slug: flat-combining
name: Flat combining
aliases:
- combining lock
- flat-combining synchronization
area: concurrency/lock-free-structures
level: advanced
summary: One thread executes operations on behalf of others, collected in a publication list under a lock.
prereqs: [spin-lock, linearizability, critical-section]
see_also: [combining-tree, combining-funnel, elimination-backoff-stack, universal-construction, treiber-stack, mcs-lock, amdahls-law, starvation-freedom]
sources:
  - paper: doi:10.1145/1810479.1810540
    title: Danny Hendler, Itai Incze, Nir Shavit and Moran Tzafrir, Flat combining and the synchronization-parallelism tradeoff, SPAA 2010, pages 355 to 364
    locator: the publication list, the combiner that holds the global lock, the aging and cleanup of records, the stack, queue and priority queue built with it, and the measurements that show where it beats fine-grained structures
  - paper: doi:10.1007/978-3-642-15763-9_8
    title: Danny Hendler, Itai Incze, Nir Shavit and Moran Tzafrir, Scalable flat-combining based synchronous queues, DISC 2010, LNCS 6343, pages 79 to 93
    locator: flat combining applied to synchronous queues, and a parallel form of flat combining in which several combiners work at once
  - paper: doi:10.1145/2145816.2145849
    title: Panagiota Fatourou and Nikolaos D. Kallimanis, Revisiting the combining synchronization technique, PPoPP 2012, pages 257 to 266
    locator: CC-Synch, DSM-Synch and H-Synch, combining algorithms that serve requests in order, bound the number of requests one combiner serves, and bound the remote memory references per operation
  - title: Yoshihiro Oyama, Kenjiro Taura and Akinori Yonezawa, Executing parallel programs with synchronization bottlenecks efficiently, PDSIA 1999
    locator: an earlier combining lock, in which the holder of the lock runs the operations that other threads have queued for it
---

Flat combining is a way to make a sequential data structure shared by many threads. One global lock guards the structure. Each thread has a *publication record*, and the records of the threads that were active lately form the *publication list*. A thread writes its request into its record and then tries the lock. The thread that gets it becomes the *combiner*: it walks the list, applies every pending request to the structure, writes each result back into its record, and releases the lock. The other threads wait on their own records and find their results there. Hendler, Incze, Shavit and Tzafrir introduced it in 2010. The result is [linearizable](/linearizability/), but it is *blocking*: it uses a lock, and if the combiner stops while it holds the lock, every other thread waits for ever. It is not [lock-free](/lock-freedom/). Its gain is that a structure with a hot spot, such as the top of a stack, is touched by one thread at a time with a warm cache, and that the combiner can often do $k$ requests for less than $k$ times the cost of one.

## In plain words

Think of a busy office with one shared logbook. Instead of every clerk queuing to write in it, each clerk writes a note on a card at their own desk: "please add this line for me".

Whoever reaches the logbook first does not write only their own line. They walk past all the desks, copy every card into the logbook, and write the answer on each card. Then they put the logbook down.

The other clerks just watch their own card until the answer shows up. If the logbook is free and their card still has no answer, they take the logbook and do the round themselves.

One person writes at a time, so the logbook never gets mixed up. If that person faints while holding the logbook, everybody waits.

## When it applies

Use flat combining when all of these hold.

- The object has a *sequential bottleneck*: every operation touches the same few words, as in a stack, a FIFO queue, a counter or a priority queue. A fine-grained lock-free version, such as the [Treiber stack](/treiber-stack/), then spends most of its time on cache misses and failed CAS steps at that hot spot.
- Each operation is short, so that one thread can do many of them quickly while the data stays in its cache.
- The number of threads is moderate, or the operations can be *combined*: a push and a pop can cancel, several inserts into a heap can be done as a batch, several increments of a counter can be added up.
- A blocking algorithm is acceptable: threads are not killed in the middle of an operation, and a thread that is descheduled while it is the combiner only delays the others.

Do not use it when the object has real parallelism, such as a large hash table whose operations hit different buckets: then a fine-grained or lock-free structure scales and flat combining stays at the speed of one thread.

## The template

### Model and notation

Threads share memory with atomic read, write and CAS on single words, and the model is [sequentially consistent](/sequential-consistency/). Threads may be delayed for any time; for the progress claim below they do not crash. The lock is a [spin lock](/spin-lock/) with test and test-and-set.

| Symbol | Meaning |
|---|---|
| $r.\mathit{slot}$ | the record's request (req, name, args) or response (resp, value) |
| $r.\mathit{active}$ | true while record $r$ is in the publication list |
| $r.\mathit{age}$ | the number of the last combining pass that served $r$ |
| $\mathit{head}$ | the first record of the publication list |
| $\mathit{data}$ | the sequential object, touched only by the lock holder |
| $p$ | the number of threads |
| $R$ | the number of records in the list |
| $s$ | the time to apply one operation to warm data |
| $m$ | the time of one cache miss on a shared line |

```pseudo id=main
OP(name, args)                                ▷ run by thread t; r is t's record
L1  r.slot ← (req, name, args)
    loop
L2      if not r.active then
L3          r.active ← true
L4          repeat h ← head; r.next ← h
L5          until CAS(head, h, r)
L6      s ← r.slot
L7      if s = (resp, v) then return v
L8      if lock = 0 and CAS(lock, 0, 1) then
L9          COMBINE()
L10         lock ← 0

COMBINE()                                     ▷ only the lock holder runs this
L11 count ← count + 1; c ← count
L12 d ← data
L13 pred ← null; x ← head
L14 while x ≠ null do
L15     s ← x.slot; nxt ← x.next
        if s = (req, name', args') then
L16         (d, v) ← apply name'(args') to d
L17         x.slot ← (resp, v); x.age ← c
L18     else if c mod CLEANUP = 0 and pred ≠ null and c − x.age > MAXAGE then
L19         pred.next ← nxt; x.active ← false; x ← nxt; continue
        pred ← x; x ← nxt
L20 data ← d
```

New records go in at the head with a CAS (L4, L5), so a thread can join the list without the lock. Only the combiner removes records, and it never removes the first one, so its writes never race with an insert at the head. It also never removes a record with a pending request. A thread whose record was removed sees `active = false` at L2 and adds the record again.

The implementation on this page follows this template with a stack as the sequential object. The cleanup rule that skips records with pending requests is our choice; the paper removes records by age.

### Why it is correct (sketch)

*Safety.* Only the lock holder runs COMBINE, so the passes are run one after another, and within a pass the requests are applied one after another to the same copy $d$ of the object. Take as the linearization point of an operation the write of its response at L17. That write comes after the request was written at L1, and before the owner reads it at L6, so it lies inside the operation. The responses are written in the order in which the requests are applied, so the order of the points is a sequential history of the object with the same results. Each request is applied once: the combiner applies only slots that hold a request, and it replaces the request by the response in the same write.

*Progress.* Flat combining is blocking. If the lock holder stops, no thread can apply a request, and every thread that has published one waits for ever; the test `test_it_blocks_when_the_combiner_stops` shows it. If no thread stops and the lock is [deadlock-free](/deadlock-freedom/), every operation completes: once a request is published and its record is in the list, the record stays there until it is served, and the next pass that starts serves it. Some pass starts, because the owner itself takes the lock when it sees the lock free. So, with no crashes, flat combining is [starvation-free](/starvation-freedom/) even over an unfair test-and-set lock, because a thread that keeps losing the lock is served by the winners.

### A bug: the combiner that runs its own operation from memory

A tempting shortcut is for the combiner to apply its own operation from its local variables before it walks the list, without looking at its own record. But a thread can read its record at L6, see a request, and lose the processor; another combiner then serves the request; then the first thread takes the lock at L8. With the shortcut it applies its operation a second time. The test `test_the_combiner_must_read_its_own_record` replays this run, in which push(1) puts 1 on the stack twice, and the explorer finds it by itself.

### Cost model

This model is ours; it is a rough guide and not a result of the paper. Count only cache misses ($m$ each) and sequential work ($s$ per request).

- With one global lock and no combining, each operation moves the lock line and the $D$ lines of data it touches to its own core: about $(1 + D)m + s$ per operation, all in sequence, so the throughput is at most $1 / ((1 + D)m + s)$.
- With flat combining, a pass that serves $k$ requests among $R$ records costs about $m$ for the lock, $Rm$ to read the records (each was written by its owner), $Dm$ to bring the data over once, and $ks$ of work. With $k \approx R \approx p$ under full load, that is about $m + s + (1 + D)m/p$ per request. The throughput tends to $1 / (m + s)$, independent of $D$.
- A waiting thread spins on its own record, which is in its own cache until the combiner writes it, so waiting adds no traffic on shared lines except one miss per answer.
- The latency of one operation is up to two passes: the one in progress and the one that serves it. That is $O(p(m + s))$ under full load.
- With combining of requests, for example a pass that matches pushes with pops and applies only the rest, the work per pass drops below $ks$.

So flat combining is never faster than one thread working on warm data, plus one miss per request. It wins when the alternative is slower than that, which is the case for a hot spot under contention. It loses when the alternative scales with $p$; this is the "synchronization-parallelism tradeoff" of the paper's title.

The implementation's solo cost is exact: $15 + 2R$ steps for an operation whose record is in the list, and 4 more when it must add its record; `test_solo_cost` checks it.

### Weak memory and memory reclamation

The write at L1 must be a release and the combiner's read at L15 an acquire, so that the combiner sees the arguments; the response write at L17 must be a release and the owner's read at L6 an acquire. The lock gives the order between passes. Records live as long as their threads and are reused for every operation, so there is no reclamation problem during normal use. A thread that exits must not free its record while the record is in the list, because a combiner can still read it; it can leave it for the cleanup and free it once it sees `active = false` and the lock has been released after that.

## Classic examples

- **Stack.** The combiner first matches pushes with pops within the pass, so that they cancel without touching the stack, and applies the rest. This is the same idea as the [elimination backoff stack](/elimination-backoff-stack/), done by one thread.
- **FIFO queue.** The paper's queue lets the combiner add a batch of enqueued items at once, and serve dequeues from the front.
- **Priority queue.** A sequential heap or skip list under the combiner; inserts in one pass can be done as a batch.
- **Synchronous queues.** Hendler et al. matched producers with consumers in the combiner, and also gave a parallel form with several combiners.
- **Counters.** A pass adds the increments of all its requests and gives each thread its own value; [combining trees](/combining-tree/) do the same with a tree of threads.

## Variations

- **CC-Synch and DSM-Synch.** Fatourou and Kallimanis put the requests in a queue like that of the [MCS lock](/mcs-lock/) and let the combiner hand the role to the next waiting thread. Requests are served in order, a combiner serves at most a fixed number of them, and the number of remote memory references per operation is bounded. H-Synch adds one combiner per cluster of cores, as a [cohort lock](/cohort-lock/) does.
- **Combining without a lock.** A [universal construction](/universal-construction/) can use the same idea in a wait-free way: every thread tries to apply all announced requests to a copy of the state and installs it with a CAS. This is not blocking, but each try copies the state.
- **Combining trees and funnels.** Older forms in which requests meet in a tree ([combining tree](/combining-tree/)) or in layers of random meeting places ([combining funnel](/combining-funnel/)) and are merged on the way to the object. Flat combining differs from them in that it has no tree: one thread scans a flat list.
- **Delegation.** A dedicated server thread that owns the object and serves requests from the others. It is flat combining with a fixed combiner, at the cost of one core.

## Pitfalls

- **Assuming it is lock-free.** It is not; a combiner that is preempted or crashes stops everybody. Use it where threads are not killed and preemption is rare.
- **Running the combiner's own operation from local variables.** See the bug above.
- **Removing the first record of the list.** Inserts change the head with a CAS. A removal that writes the head without the CAS can lose a new record; the template never removes the first record.
- **Removing a record with a pending request, without a retry.** The owner must check its active flag while it waits and add the record again, or its request is never served.
- **Long operations.** One long operation delays every waiting thread, because they are all served in one pass.
- **Unbounded passes.** If new requests keep arriving, a combiner that scans until there is nothing left can serve for ever while its own caller waits. Bound the number of scans per pass.

## Exercises

1. Show the linearization point of an operation of the template, and check that it lies in the interval of the operation even when the request is served by a pass that started before the request was published.
2. Give a run of three threads in which a thread is served by a combiner, then becomes the combiner itself and serves nobody. Why is that pass still needed?
3. Change the template so that a stack combiner matches pushes with pops in a pass. Which order must the matched pairs take in the linearization?
4. In the cost model, find the number of threads at which a [Treiber stack](/treiber-stack/) whose successful operation costs about $3m$ and flat combining with $s = m/4$ have the same throughput, if the Treiber stack's failed CAS steps are ignored. What happens to the comparison when they are counted?
5. Prove that, with no crashes and a deadlock-free lock, every operation of the template completes, even when the cleanup removes records.

## References
