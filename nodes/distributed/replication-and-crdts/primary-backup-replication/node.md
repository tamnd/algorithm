---
tag: 04PKB8
kind: algorithm
slug: primary-backup-replication
name: Primary-backup replication
aliases:
- primary-copy replication
- passive replication
- master-slave replication
area: distributed/replication-and-crdts
level: core
summary: One primary executes each request and sends the new state to the backups before it replies; on a crash a backup takes over, which needs an accurate failure detector.
solves: [state-machine-replication]
model: synchronous-model
complexity:
  vars: {n: the number of servers, f: the number of crashes tolerated, r: the number of request ids kept in the reply cache}
  messages: {worst: Θ(n)}
  space: {extra: O(r)}
properties: {deterministic: true, recursive: false}
history:
  year: 1976
  people: [Peter A. Alsberg, John D. Day, Navin Budhiraja, Keith Marzullo, Fred B. Schneider, Sam Toueg]
  note: Alsberg and Day (1976) described a primary host kept in step with backups. Budhiraja, Marzullo, Schneider and Toueg (1992, 1993) defined the approach and proved tight bounds on its cost.
prereqs: [state-machine-replication, crash-failure, failure-detector, synchronous-model]
see_also: [active-replication, chain-replication, viewstamped-replication, raft, view-change, split-brain, leader-lease, replicated-log]
sources:
  - paper: "Peter A. Alsberg and John D. Day, A principle for resilient sharing of distributed resources, Proceedings of the 2nd International Conference on Software Engineering (ICSE), 562-570, 1976"
    locator: the description of the primary host and its backup hosts
  - paper: "Navin Budhiraja, Keith Marzullo, Fred B. Schneider and Sam Toueg, Optimal primary-backup protocols, Proceedings of the 6th International Workshop on Distributed Algorithms (WDAG), LNCS 647, Springer, 1992"
    locator: the properties Pb1 to Pb5, Table 1 (lower bounds on replication, blocking time and failover time for each failure type) and the protocols that meet them
  - paper: "Navin Budhiraja, Keith Marzullo, Fred B. Schneider and Sam Toueg, The primary-backup approach, in Sape Mullender (editor), Distributed Systems, second edition, ACM Press and Addison-Wesley, 199-216, 1993"
    locator: the definition of a primary-backup protocol and the summary of the lower bounds
  - paper: doi:10.1145/78969.78972
    title: Maurice P. Herlihy and Jeannette M. Wing, Linearizability, a correctness condition for concurrent objects, ACM Transactions on Programming Languages and Systems 12(3), 463-492, 1990
    locator: Section 2 (the definition of linearizability used in the correctness theorem)
  - paper: doi:10.1006/jpdc.1993.1015
    title: Jeannette M. Wing and Chun Gong, Testing and verifying concurrent objects, Journal of Parallel and Distributed Computing 17(1-2), 164-182, 1993
    locator: the search for a linearization of a history, used by the checker in the code
---

Primary-backup replication, also called passive replication, keeps one copy of a service on each of $n$ servers but lets only one of them, the **primary**, execute requests. The primary applies a request, sends the new state to the **backups**, waits until every backup has it, and then replies. When the primary crashes, a [failure detector](/failure-detector/) reports it and a [view change](/view-change/) makes a backup the new primary. Unlike [active replication](/active-replication/), where every replica executes every command and a crash is masked at once, primary-backup does the work once and accepts a short outage on failover. The approach is safe only if at most one server acts as primary at any time, so it needs a failure detector that does not make mistakes, or a protocol that gets the same effect from quorums. Budhiraja, Marzullo, Schneider and Toueg gave tight lower bounds on the number of servers and on the blocking and failover times for each type of failure.

## In plain words

A team keeps one main notebook and some copies. Only the leader writes in the main notebook. When a customer asks for a change, the leader makes the change, then tells every helper to copy it, and waits until all helpers say they have it. Only then does the leader tell the customer that the change is done.

If the leader stops, a manager notices and picks a helper as the new leader. The new leader first makes all the other helpers' copies equal to its own. Then it starts to take requests.

The danger is a manager that is wrong. If the manager thinks the leader has stopped, but the leader is only slow, two leaders can take requests at once. Then customers can see two different notebooks.

## The problem

The problem is [state machine replication](/state-machine-replication/) for a service such as a key-value store: answer client requests as one correct server would, and stay available while up to $f$ of the $n$ servers fail. The correctness condition is [linearizability](/linearizability/).

The model on this page is the [synchronous model](/synchronous-model/) with [crash failures](/crash-failure/) of servers: messages between correct processes arrive within a known bound $\delta$, and a server that crashes stops for good. A view service detects a crash within a known time and never reports a server that has not crashed, so it acts as a perfect failure detector. Clients may retry; each request has a unique id.

Budhiraja et al. state the goal as five properties. Pb1: at any time there is at most one primary. Pb2: each client sends its requests to a server named by the protocol. Pb3: a request that reaches a server that is not the primary is not queued. Pb4: the service has bounded outages that happen only a finite number of times (they call such a service a $(k, \Delta)$-bofo server). Pb5: a correct primary stays the primary until some failure occurs.

## The algorithm

The current view is a triple (number $v$, primary $p$, backups $B$). Each server keeps the state $s$ and a reply cache that maps request ids to outputs. The primary handles one write at a time.

```pseudo id=main
PRIMARY(r)                                 ▷ at the primary p of view v; r has client, id, op
L1  append r to the queue, and serve the queue one request at a time
L2  if r.id is in cache then reply cache[r.id] to r.client, and go to the next request
L3  if r.op is a read then reply ω(s, r) to r.client, and go to the next request
L4  s ← δ(s, r); cache[r.id] ← ω(s, r)
L5  send UPDATE(v, s, r.id) to each backup b in B; waiting ← B
L6  on ACK(v) from backup b: waiting ← waiting \ {b}
L7  when waiting is empty:
L8      reply cache[r.id] to r.client

NEW-VIEW(v', p', B')                       ▷ installed by the view service after a crash
L9  if p' = me then send STATE(v', s, cache) to each b in B', and serve only when all have sent ACK(v')

BACKUP(UPDATE(v, s', id) from p)           ▷ ignored if v is not the current view
L10 s ← s'; cache[id] ← the output
L11 send ACK(v) to p
```

Line L4 is the only place where a request is executed. Lines L5 to L8 make the primary wait until every backup of the view holds the new state, so a reply is sent only for a state that survives the crash of the primary. Line L9 is the state transfer of a new primary: its state overwrites the state of every backup, which removes any update that the old primary sent to some backups but not to the new primary. Line L2 makes a retried request take effect once, even when it reaches a new primary that already holds its result. Reads in line L3 are answered by the primary alone, which is correct only because there is one primary.

A backup is passive: it does not execute requests, it only stores the state (line L10). This is why the service does not need to be deterministic. Only the primary runs $\delta$, and the backups copy the result.

## Example

Three servers $S_0, S_1, S_2$ hold one register with the initial value none. View 1 has primary $S_0$ and backups $S_1, S_2$. One client runs write(1), write(2) and read().

1. The client sends write(1) to $S_0$. $S_0$ sets $s = 1$ (L4), sends UPDATE to $S_1$ and $S_2$ (L5), gets both acks (L6), and replies ok (L8).
2. The client sends write(2). $S_0$ sets $s = 2$ and sends UPDATE to $S_1$. Then $S_0$ crashes, before it sends UPDATE to $S_2$. Now $S_1$ holds 2, $S_2$ holds 1, and the client has no reply.
3. The view service detects the crash and installs view 2 with primary $S_1$ and backup $S_2$. $S_1$ sends STATE(2, 2, cache) to $S_2$ (L9). $S_2$ now holds 2 and the id of write(2) in its cache, and acks.
4. The client times out and sends write(2) again, with the same id, to $S_1$. The id is in the cache, so $S_1$ replies ok without running the write again (L2).
5. The client sends read() to $S_1$ and gets 2.

The history write(1), write(2), read() = 2 is linearizable. During step 3 no server was primary, which is the failover time.

**A run with split brain.** Two servers, with timeouts in place of a perfect detector. A client writes 1, and both servers hold 1. Then the link between $S_0$ and $S_1$ fails. $S_1$ hears nothing from $S_0$, decides that $S_0$ has crashed, and makes itself primary. A second client writes 2 at $S_1$ and gets ok. Then the first client reads at $S_0$, which still believes it is the primary, and gets 1. The write of 2 completed before the read began, so the history is not linearizable. This is [split brain](/split-brain/).

## Correctness

**Theorem.** In the synchronous model with crash failures, a perfect failure detector, and at most $n - 1$ crashes among $n$ servers, the protocol is linearizable, and every request of a correct client completes.

The proof rests on three facts.

1. **One primary at a time (Pb1).** The view service installs view $v + 1$ only after the primary of view $v$ has crashed or been removed as crashed, and a perfect detector reports only real crashes. So two servers never serve in the same period.
2. **Backup invariant.** When the primary of view $v$ is serving and has no write in flight, every backup of $v$ has the same state and the same cache as the primary. State transfer (L9) makes this true at the start of a view. A write keeps it true, because the primary serves the next request only after all backups have acked (L5 to L7), and messages of older views are ignored.
3. **No lost or doubled write.** A write that got a reply is at every backup (fact 2), so it is in the state of the next primary. A write that the old primary executed but did not reply to is either in the new primary's state, or in no state at all after L9. In both cases no read has seen it except through the new primary, since the old primary does not serve reads while a write is in flight. The cache (L2) makes a retried write take effect at most once.

The linearization point of a write is the run of L4 whose result survives into the final view chain; for a retried write that the new primary already holds, it is the original run of L4, which lies inside the interval of the call because the client had no reply yet. The point of a read is its run of L3. By facts 1 and 2 these points are in real-time order and each read returns the value of the last write before its point. Liveness follows because each crash is detected within a known time, the new primary needs one round trip for state transfer, and a correct client retries until it gets a reply. The full proof is in the proof file.

## Complexity

- **Messages.** A write costs $2(n - 1)$ messages between servers (UPDATE and ACK) plus the request and the reply, so $\Theta(n)$. A read costs 2 messages. A view change costs $2(n - 2)$ messages for state transfer, plus the work of the view service.
- **Time.** Without failures, a write takes 4 message delays: client to primary, UPDATE, ACK, reply. The extra time at the primary, here $2\delta$, is what Budhiraja et al. call the blocking time. After a crash of the primary there is no primary for the detection time plus one round trip for state transfer.
- **Space.** Each server holds the state and a reply cache of $r$ entries, one per recent request id; the cache can be cut to the last request of each client.
- **Servers.** With crash failures, $n = f + 1$ servers tolerate $f$ crashes.

**Lower bounds.** Budhiraja et al. prove the following bounds in a synchronous model with a known delay bound $\delta$ and a FIFO point-to-point network. Blocking time is the extra time a request can wait at the primary before the reply, in runs without failures; failover time is the longest period with no primary.

| failure type | servers | blocking time | failover time |
|---|---|---|---|
| crash | $n > f$ | 0 | $f\delta$ |
| crash and link | $n > f + 1$ | 0 | $2f\delta$ |
| send omission | $n > f$ | $\delta$ if $f = 1$, $2\delta$ if $f > 1$ | $2f\delta$ |
| receive omission | $n > \lfloor 3f/2 \rfloor$ | $\delta$ if $n \le 2f$ and $f = 1$; $2\delta$ if $n \le 2f$ and $f > 1$; 0 if $n > 2f$ | $2f\delta$ |
| general omission | $n > 2f$ | $\delta$ if $f = 1$, $2\delta$ if $f > 1$ | $2f\delta$ |

They also give protocols that meet these bounds. All bounds for crash and for crash and link failures are tight. For general omission all bounds are tight except the blocking time for $f = 1$. For receive omission, the blocking time bound for $n > 2f$ and the failover bound are tight, but their protocol needs $n > 2f$; with $\lfloor 3f/2 \rfloor < n \le 2f$ a correct primary may have to give up control to a faulty backup. The protocol on this page waits for acks, so its blocking time is $2\delta$, not the optimal 0 for crashes; a protocol with blocking time 0 sends the update and the reply at the same time, and relies on synchronous links to deliver the update even if the primary then crashes.

## Properties

- **Only the primary computes.** The backups store state, so the service may use clocks, random numbers or threads. This is the main advantage over [active replication](/active-replication/).
- **Outage on failover.** A crash of the primary stops the service for the detection time plus state transfer. A crash of a backup only shrinks the view.
- **Safety depends on the detector.** If the detector can be wrong, Pb1 can fail, and the service can return stale data (split brain).
- **Reads are local.** The primary answers reads from its own state, without messages to the backups, as long as it is the only primary.

## Variants and improvements

- **Majority-based primary-backup.** [Viewstamped Replication](/viewstamped-replication/), [Raft](/raft/) and [Zab](/zab/) keep a primary and backups, but a write is complete when a majority acks, and a view change needs a majority. With $n = 2f + 1$ they stay safe under [partial synchrony](/partial-synchrony/), where a detector can be wrong; the price is $2f + 1$ servers in place of $f + 1$.
- **Leases.** A primary holds a time-bounded [leader lease](/leader-lease/), and a new primary waits until the old lease has run out. This keeps Pb1 with loosely synchronized clocks in place of a perfect detector.
- **Log shipping.** The primary sends its [write-ahead log](/write-ahead-logging/) records in place of the full state; the backups replay them. This is how many databases build replicas; see [replicated log](/replicated-log/).
- **Asynchronous backups.** The primary replies before the backups ack. This lowers latency, but a crash of the primary can lose writes that clients saw as done.
- **Chain replication.** [Chain replication](/chain-replication/) orders the servers in a chain, sends updates down it, and lets the tail answer queries, which spreads the load of the primary.

## When to use it

Use primary-backup when requests are expensive or not deterministic, so that running them on every server is wasteful or impossible, and when a short outage on failover is acceptable. Use it with a perfect detector only where the environment gives one, for example a single switch, a shared disk with fencing, or a separate service that is itself replicated with consensus. Where the network can partition, use a majority-based variant or leases. Use [active replication](/active-replication/) when failures must not cause any pause, or when servers can be Byzantine.

## Pitfalls

- **Timeouts as a perfect detector.** Wrong: let a backup become primary when it stops hearing the old primary. Right: make the takeover depend on a view service or a majority vote, and fence the old primary, for example with a lease. The split brain run above shows the failure.
- **Replying before the backups have the update.** Wrong: reply at L4. Right: reply after all acks (L7), or accept that a crash can lose acknowledged writes.
- **No state transfer.** Wrong: a new primary starts serving at once. Right: first make all backups equal to its state (L9). Otherwise a backup that got an UPDATE the new primary missed keeps a value that no client can explain.
- **No reply cache.** Wrong: run a retried write again. Right: keep the output by request id (L2). Otherwise a write such as "add 1" takes effect twice.
- **Old messages.** Wrong: apply any UPDATE. Right: tag each message with the view number and drop messages of older views.

## Implementations

The Python code runs servers, a view service and clients in a discrete event simulator with seeded delays and crash times. The view service detects a crash after a fixed delay. The module also has a small Wing and Gong style search that decides whether a short register history is linearizable.

## History

Alsberg and Day (1976) described a resilient service built from a primary host and backup hosts that the primary keeps up to date. Many later systems used the same scheme under the names primary copy, passive replication and master-slave replication. Oki and Liskov's Viewstamped Replication (1988) combined a primary with view changes decided by a majority. Budhiraja, Marzullo, Schneider and Toueg (1992, with the chapter of 1993) gave a precise definition of a primary-backup protocol by the properties Pb1 to Pb5, proved lower bounds on the number of servers, the blocking time and the failover time for crash, link and omission failures, and gave protocols that meet most of them.

## References
