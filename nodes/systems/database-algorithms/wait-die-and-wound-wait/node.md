---
tag: 8VMTDE
kind: algorithm
slug: wait-die-and-wound-wait
name: Wait-die and wound-wait
aliases:
- deadlock prevention by timestamps
- wait-die
- wound-wait
area: systems/database-algorithms
level: core
summary: "Two rules that prevent deadlock in a locking scheduler by age: in wait-die only older transactions wait, in wound-wait only younger ones do. A restart keeps its timestamp."
solves: [concurrency-control]
model: word-ram
complexity:
  vars: {k: the number of active transactions, h: the number of holders of the requested lock}
  time: {per-conflict: "O(h)", deadlock-search: "O(1)"}
  space: {extra: "O(k)"}
properties: {deterministic: true, online: true}
prereqs: [two-phase-locking, deadlock-prevention, wait-for-graph]
see_also: [two-phase-locking, strict-two-phase-locking, deadlock-prevention, deadlock-detection, wait-for-graph, starvation, timestamp-ordering, contention-management]
sources:
  - paper: doi:10.1145/320251.320260
    title: Daniel J. Rosenkrantz, Richard E. Stearns and Philip M. Lewis II, System level concurrency control for distributed database systems, ACM Transactions on Database Systems 3(2), 1978, pages 178 to 198
    locator: the wait-die and wound-wait systems, the proof that they cannot deadlock, and the argument that a transaction which keeps its timestamp is not restarted forever
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 3 (deadlock prevention with timestamps, wait-die and wound-wait)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Chapter 17 (deadlock prevention by priorities, wait-die and wound-wait)
---

Wait-die and wound-wait are two rules that keep a [two-phase locking](/two-phase-locking/) scheduler free of deadlocks without ever looking for a cycle. Each transaction gets a timestamp when it starts, and a smaller timestamp means older. When a transaction asks for a lock that another transaction holds, the rule compares their ages. In *wait-die*, an older requester waits and a younger requester dies (aborts). In *wound-wait*, an older requester wounds (aborts) the younger holder, and a younger requester waits. In both, waits go in one direction of age only, so the [wait-for graph](/wait-for-graph/) cannot have a cycle. Rosenkrantz, Stearns and Lewis introduced them in 1978 for distributed databases. An aborted transaction restarts with its old timestamp, so it gets older over time and is not starved.

## In plain words

Two people each hold a key that the other one needs, and both wait forever. That is a deadlock. Instead of waiting and then looking for such a circle, we can stop it from forming by using age.

In wait-die, an older person who meets a younger key holder waits patiently. A younger person who meets an older key holder gives up, puts back every key, and starts again later. In wound-wait it is the other way around. An older person who meets a younger key holder forces that younger person to give up. A younger person who meets an older key holder waits.

In both rules, everyone who waits is waiting for someone of the same "direction" of age, so nobody can end up waiting for themselves. A person who starts again keeps their original age, so sooner or later they are the oldest and always win.

## The problem

The scheduler runs [two-phase locking](/two-phase-locking/), normally in its [strict](/strict-two-phase-locking/) form. Locks are S (shared) or X (exclusive), and a request waits when another transaction holds a conflicting lock. Such waits can form a [deadlock](/deadlock/), a cycle in the wait-for graph. The task is a rule for each conflicting request (wait, or abort someone) such that no cycle can ever form, the [Coffman condition](/coffman-conditions/) of circular wait is denied, and no transaction is aborted forever. The rule may use only local data: the timestamps of the requester and of the holders. This matters in a distributed database, where the wait-for graph is spread over many sites and hard to search.

## The algorithm

Each transaction $T$ has a timestamp $\mathrm{ts}(T)$, for example a counter or a clock value with the site number to break ties. It is given when $T$ first starts and is kept on every restart. Let $H$ be the set of other transactions that hold a lock on $x$ that conflicts with the requested mode.

```pseudo id=main
REQUEST(T_i, x, m)                 ▷ H = holders of locks on x that conflict with m
L1  if H is empty then go to L6
    if the policy is wait-die then
L2      if ts(T_i) < ts(T_j) for every T_j ∈ H then T_i waits, and asks again later
L3      else abort T_i (it dies); restart it later with the same timestamp
    else                                                   ▷ wound-wait
L4      for each T_j ∈ H with ts(T_i) < ts(T_j) do abort T_j (T_i wounds it); T_j restarts with its timestamp
L5      if a holder is left then T_i waits for it, and asks again later
L6  grant the lock (x, m) to T_i and run the action
L7  on commit of T_i: release all its locks
L8  on abort of T_i: restore its before images in reverse order, then release all its locks
```

Lines L2 and L3 are wait-die; lines L4 and L5 are wound-wait. With several holders, wait-die waits only if the requester is older than all of them, and wound-wait wounds every younger holder and waits for the older ones. When the set of holders changes while a transaction waits, the rule is applied again.

## Example

Let $T_1$ be older than $T_2$, with $T_1 = w_1(x)\, w_1(y)$ and $T_2 = w_2(y)\, w_2(x)$. The requests arrive as $w_1(x)$, $w_2(y)$, $w_1(y)$, $w_2(x)$. Plain 2PL deadlocks here.

| step | event | wait-die | wound-wait |
|---|---|---|---|
| 1 | $T_1$ asks X on $x$ | granted | granted |
| 2 | $T_2$ asks X on $y$ | granted | granted |
| 3 | $T_1$ asks X on $y$, held by the younger $T_2$ | $T_1$ waits for $T_2$ | $T_1$ wounds $T_2$; $T_2$ aborts and releases $y$; $T_1$ gets $y$ |
| 4 | $T_2$ asks X on $x$, held by the older $T_1$ | $T_2$ dies, releases $y$; $T_1$ gets $y$ | (in its new attempt, $T_2$ waits for $T_1$) |
| 5 | $T_1$ commits | $T_2$ restarts with timestamp 2 | $T_2$ continues |

In both cases $T_1$ commits first and $T_2$ commits after it, and in both cases $T_2$ is aborted once. Now take $T_1 = w_1(x)$ and $T_2 = w_2(x)\, w_2(y)$, where the younger $T_2$ locks $x$ first. Under wait-die, $T_1$ simply waits for $T_2$, and nobody aborts. Under wound-wait, $T_1$ wounds $T_2$, although no deadlock was possible. If instead the younger transaction asks second, wound-wait lets it wait and wait-die makes it die. Each rule makes some aborts that a cycle search would not make.

## Correctness

The proof file has the details.

- **No deadlock.** Under wait-die every wait-for edge goes from an older to a younger transaction; under wound-wait every edge goes from a younger to an older one. Along a path the timestamps move in one direction, so no path returns to its start.
- **The oldest is safe.** The oldest unfinished transaction is never aborted: under wait-die nobody is older than it, so it never dies; under wound-wait only an older transaction can wound it. Under wound-wait it also never waits.
- **No starvation.** A restarted transaction keeps its timestamp. New transactions are younger. So after the finitely many older transactions finish, it is the oldest and is never aborted again. This needs a lock manager that does not let younger transactions take a released lock ahead of the oldest waiter again and again.
- **Serializability.** The rules choose only who waits and who aborts; the locking is still 2PL, so every committed projection is conflict serializable. With strict 2PL the schedules are strict and an abort is undone by before images.

## Complexity

- **Per conflict.** Comparing the requester with $h$ holders costs $O(h)$. No graph search is needed, so the deadlock work per request is $O(1)$ beyond the comparison.
- **Space.** One timestamp per transaction.
- **Aborts.** Both rules abort transactions that are not in a deadlock, so they waste more work than detection when conflicts are frequent but cycles are rare. In wait-die a young transaction can die and restart many times while it waits for one old holder, but each attempt is short: it dies at the first conflict with an older holder, often before it has done much. In wound-wait an old transaction can kill a young one that has done much work, but a wounded transaction that restarts and meets the older one again waits instead of being wounded again.

## Properties

- **Prevention, not detection.** No cycle can form, so no global wait-for graph is needed. This was the point in the distributed setting of Rosenkrantz, Stearns and Lewis: each site decides with the two timestamps it sees.
- **Wait-die is non-preemptive.** A transaction aborts only itself. Wound-wait is preemptive: it aborts a transaction that holds a lock, so it denies the no-preemption [Coffman condition](/coffman-conditions/) in a controlled way.
- **Fair by age.** Both rules favour old transactions, and keeping the timestamp on restart makes every transaction old in the end.
- **Same output class as 2PL.** The schedules are those of (strict) two-phase locking with some extra aborts.

## Variants and improvements

- **Wound in commit.** In practice a wound is ignored if the wounded transaction is already committing (for example, it has voted yes in [two-phase commit](/two-phase-commit/)). It will release its locks soon anyway.
- **No-waiting and cautious waiting.** The no-waiting rule aborts any requester that meets a conflict. Cautious waiting lets a requester wait only if the holder is not itself waiting. Both avoid deadlocks without timestamps: under no-waiting nobody waits, and under cautious waiting a transaction only starts to wait for a holder that is not waiting at that moment, so along each path of the wait-for graph the holder started to wait later than the waiter, and no cycle can form.
- **Detection instead.** Most centralized databases use [deadlock detection](/deadlock-detection/) on the wait-for graph, often with timeouts, because it aborts only on real cycles.
- **Timestamps as priorities in transactional memory.** [Contention management](/contention-management/) in software transactional memory solves a similar conflict question between transactions. Some contention managers also give priority by start time, so that the older transaction wins, which is the idea of wound-wait in a setting without locks held for long.

## When to use it

Use wait-die or wound-wait when a global search for deadlock cycles is expensive or impossible, as in a distributed database, or when a simple local rule is wanted. Prefer wound-wait when old transactions are long and should not wait behind young ones; prefer wait-die when killing a holder in the middle of its work is costly. Use detection when conflicts are frequent and real deadlocks are rare, so that the extra aborts would cost more than the search.

## Pitfalls

- **A new timestamp on restart.** If an aborted transaction gets a fresh timestamp, it is again the youngest and can be aborted forever. This is [starvation](/starvation/), and keeping the first timestamp prevents it.
- **Using the timestamps for ordering.** These timestamps are only priorities for deadlock prevention. They are not a serialization order; the order is still given by the locks. Do not confuse the rules with [timestamp ordering](/timestamp-ordering/), which uses timestamps as the serial order and takes no locks.
- **Mixing up the names.** The first word says what an *older* requester does to a younger holder: in wait-die it waits, in wound-wait it wounds. The second word says what a younger requester does: it dies or waits.
- **Restart too soon.** A transaction that died in wait-die and restarts at once will usually meet the same older holder and die again. Delay the restart until that holder is gone.
- **Equal timestamps.** Ties must be broken by a fixed rule, such as the site number, or two transactions could both wait or both die.

## Implementations

## History

Rosenkrantz, Stearns and Lewis proposed the two rules in 1978, in a paper on concurrency control for distributed database systems. They used the transaction's timestamp as a priority and proved that the systems are free of deadlock and that a transaction which keeps its timestamp is restarted only finitely often. The rules became standard textbook material through Bernstein, Hadzilacos and Goodman (1987) and later database textbooks, as the classic examples of deadlock prevention in contrast to detection.

## References
