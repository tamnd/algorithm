---
tag: D00TZM
kind: technique
slug: failover
name: Failover
aliases:
- automatic failover
- active-passive failover
area: systems/load-balancing-and-hashing
level: intro
summary: "When a server fails, move its work to a standby or to the other servers. The time is detection plus promotion; a lease and a fencing token keep an old primary from writing."
prereqs: [health-checking, split-brain]
see_also: [leader-lease, primary-backup-replication, raft, quorum, dns-load-balancing, chain-replication, hinted-handoff, connection-draining]
sources:
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: "Chapter 5, the section on handling node outages (leader failure: failover), and Chapter 8, the section on the leader and the lock (fencing tokens)"
  - url: https://www.rfc-editor.org/rfc/rfc5798
    title: "S. Nadas (editor), RFC 5798, Virtual Router Redundancy Protocol (VRRP) Version 3 for IPv4 and IPv6, 2010"
    locator: "Section 6.1 (Skew_Time and Master_Down_Interval), Section 6.4.2 (the backup becomes master and sends gratuitous ARP), Section 7.3 (the virtual MAC address)"
  - paper: doi:10.1145/74850.74870
    title: Cary G. Gray and David R. Cheriton, Leases, an efficient fault-tolerant mechanism for distributed file cache consistency, Proceedings of the 12th ACM Symposium on Operating Systems Principles (SOSP), 1989
    locator: the definition of a lease, and why a lease lets the server act after a holder fails without hearing from it
  - url: https://raft.github.io/raft.pdf
    title: Diego Ongaro and John Ousterhout, In search of an understandable consensus algorithm (extended version), 2014
    locator: Section 5.2 (leader election with randomized timeouts) and Section 5.4.1 (the election restriction, so that a new leader holds all committed entries)
---

Failover is the technique of moving the work of a failed server to another server without a person in the loop. In *active-passive* failover a standby waits and takes over the role of the primary; in *active-active* failover all servers carry traffic and the survivors absorb the share of the failed one. The time to fail over is the time to detect the failure plus the time to promote the new server, and the main danger is [split brain](/split-brain/): the old primary is not dead, only slow or cut off, and keeps acting. A lease bounds when the standby may take over, and a fencing token makes the shared resource refuse the old primary even after a long process pause.

## In plain words

A shop has one cashier and one helper who waits in the back. The cashier holds a badge that is good for ten minutes, and gets a fresh badge from the office every few minutes. If the office gives no fresh badge for ten minutes, the old badge is no good, and the office gives a new badge to the helper, who then opens the till.

Each badge has a number, and each new badge has a bigger number. The till remembers the biggest badge number it has seen. If the old cashier was only asleep and comes back with the old badge, the till sees a smaller number and stays shut.

So customers wait for at most the life of a badge plus the time the helper needs to get ready, and two people never use the till at the same time.

## When it applies

- A role can have only one holder at a time: the primary of a database, the owner of a virtual IP address, the leader of a job queue. Two holders would corrupt data or answer clients in two different ways.
- For stateless servers behind a [load balancer](/load-balancer/), failover is just [health checking](/health-checking/): remove the failed server, and the others take its share. This is active-active failover, and it has no split brain problem, because no role is unique.
- The model of this page: an integer clock that every party reads, with no drift (drift is a pitfall below); a lease service that is itself fault tolerant, for example a lock service built on [Raft](/raft/) or ZooKeeper; a lease length $L$; the primary renews every $R < L$ ticks; the standby polls every $P$ ticks and needs $S \ge 1$ ticks to promote itself; a node can crash, or pause and then resume the step it was in.

## The template

```pseudo id=main
ACQUIRE(n, now)                              ▷ on the replicated lease service
L1  if holder ≠ n and now < expiry then return NONE
L2  if holder = n and now < expiry then expiry ← now + L; return (token, expiry)    ▷ renew
L3  token ← token + 1; holder ← n; expiry ← now + L; return (token, expiry)        ▷ new grant

STANDBY(n)                                   ▷ every P ticks, while it is not primary
L4  g ← ACQUIRE(n, now); if g = NONE then return
L5  (t, e) ← g; promote: catch up the replica, take the address, open for writes   ▷ S ticks
L6  while it holds the lease: call ACQUIRE every R ticks to renew
L7      send each write to the storage as WRITE(t, v)

WRITE(t, v)                                  ▷ on the storage, as one atomic step
L8  if t < maxToken then reject
L9  maxToken ← max(maxToken, t); apply v
```

Lines L1 to L3 grant at most one unexpired lease at a time: a new grant happens only when no other node holds a lease that has not expired (line L1), and each new grant gets a larger token (line L3). A renewal keeps the token. Lines L8 and L9 are the fencing check: the storage refuses any write whose token is smaller than one it has already accepted. The primary stops writing when its own view of the lease runs out, but that check alone is not safe: a process can decide to write, pause for a long time, and send the write after its lease has gone to someone else. The token check at the storage catches this case.

**Claim (safety).** In this model, (a) at each time at most one node holds an unexpired lease, by the clock of the service, and (b) the tokens of the accepted writes never decrease, in the order the storage applies them. So once the new primary has written with token $t$, no write of an older primary is accepted, whatever its pauses.

*Proof.* (a) A new grant to node $n$ at time $now$ passes line L1, so the lease before it had expiry at most $now$, and renewals only move the expiry of the current holder. (b) Let $M$ be maxToken. Line L9 never lowers $M$ and makes $M \ge t$ for each accepted $t$. A write passes line L8 only if $t \ge M$, so its token is at least the token of every write accepted before it. The full argument, with its history, is on the [split brain](/split-brain/) page. $\square$

**Claim (timing).** Let the primary crash at time $c \ge 1$, after it renewed at the multiples of $R$ before $c$. Its last renewal is at $\rho = \lfloor (c-1)/R \rfloor R$, so its lease expires at $\rho + L$. The standby gets the lease at the first poll at or after the expiry, $a = \lceil (\rho + L)/P \rceil P$, and writes from $a + S$. Hence the gap from the crash to the first write of the new primary satisfies

$$L - R + S \;\le\; a + S - c \;\le\; L + P - 2 + S.$$

*Proof.* $\rho$ is the largest multiple of $R$ below $c$, so $c - R \le \rho \le c - 1$. Then $\rho + L \le a \le \rho + L + P - 1$, since $a$ is the first multiple of $P$ at or after $\rho + L$. Add $S$ and subtract $c$. $\square$

The detection part, $a - c$, is at least $L - R$: a lease cannot detect a failure faster than its length minus the renewal period. A shorter lease detects faster but costs more renewals and makes a short pause or a slow network look like a failure. On a continuous clock the bounds are $L - R + S$ and $L + P + S$.

**Example.** Take $L = 10$, $R = 3$, $P = 2$, $S = 2$, and a crash at $c = 7$.

| time | event | token at the storage |
|---|---|---|
| 0 | the primary gets token 1, lease to 10 | |
| 3, 6 | the primary renews: lease to 13, then to 16 | 1 |
| 6 | last write of the primary | 1 |
| 7 | the primary crashes | 1 |
| 8 to 14 | the standby polls at 8, 10, 12, 14: refused by line L1 | 1 |
| 16 | the standby polls, gets token 2, lease to 26 | 1 |
| 18 | promotion done, first write of the new primary | 2 |

Writes stop for 11 ticks, from 7 to 17; the bounds give 9 to 12. Now replace the crash by a pause: at time 7 the primary decides to write with token 1, then stops for 20 ticks. The standby still takes over at 16 and writes from 18. At 27 the old primary wakes and sends its write with token 1. The storage holds maxToken 2, so line L8 rejects it. Without line L8 the write is accepted after the writes of the new primary, which is a lost update. In 300 seeded runs of three nodes with random pauses and crashes, the run without fencing accepts a write with a smaller token after a larger one in 267 runs; with fencing, no run does, and no two leases overlap.

**Cost.** Each renewal is one round trip to the lease service, which commits it through its own consensus, so the service handles $1/R$ renewals per tick per role. The storage check is one comparison and one stored integer per resource.

## Classic examples

- **Virtual IP takeover with VRRP.** Routers or balancers share a virtual IP address and a virtual MAC address 00-00-5E-00-01-{VRID}. The master sends an advertisement every Advertisement_Interval, by default 100 centiseconds. A backup declares the master down after Master_Down_Interval $= 3 \cdot$ Master_Adver_Interval $+$ Skew_Time, with Skew_Time $= ((256 - \text{priority}) \cdot \text{Master\_Adver\_Interval}) / 256$. With the default interval and priority 100 this is $360.9375$ centiseconds, about 3.61 s; with priority 254 it is $300.78125$ centiseconds, so the backup with the higher priority speaks first. The new master then sends a gratuitous ARP for the address, so that the switches and hosts on the link learn where the address now lives. VRRP has no fencing: a partition of the link gives two masters.
- **Database primaries.** In [primary-backup replication](/primary-backup-replication/), a failure detector or an operator picks a backup, the backup replays the log it has, and clients are pointed to it. With asynchronous replication the new primary can lack writes that the old one acknowledged, and those writes are lost or must be reconciled.
- **Consensus groups.** In [Raft](/raft/), a follower that hears no heartbeat within its election timeout starts an election; the term number acts as the fencing token, and the election restriction makes sure the new leader has all committed entries. [Leader leases](/leader-lease/) let the leader serve reads without a round of messages, at the price of a bound on clock drift.
- **DNS failover.** A health checker changes the DNS answer to point to a standby site. The switch takes at least the TTL of the record, and longer for resolvers that ignore it; see [DNS load balancing](/dns-load-balancing/).
- **Shared disks and STONITH.** In a cluster with a shared disk, the survivor cuts the old node off from the disk, or turns its power off ("shoot the other node in the head"), before it mounts the disk. This is fencing done by the resource, without tokens.

## Variations

- **Active-active.** Every server carries traffic; on a failure the [load balancer](/load-balancer/) or the client spreads the share of the failed server over the others. The survivors need spare capacity: with $n$ equal servers, each must stay below a load of $(n-1)/n$ of its capacity to absorb one failure. With [consistent hashing](/consistent-hashing/) only the keys of the failed server move.
- **Chains and quorums.** [Chain replication](/chain-replication/) removes a failed node from the chain under the control of a master service. [Dynamo-style replication](/dynamo-style-replication/) needs no failover for writes: a sloppy quorum writes to another node, and [hinted handoff](/hinted-handoff/) returns the data later.
- **Manual failover.** An operator confirms the failure and starts the promotion. It is slower, and it avoids the case where a false detection moves the role during a short network fault and causes two outages instead of none.
- **Failback.** When the old primary returns, it joins as a standby with a new identity and catches up. Moving the role back at once doubles the number of switches and the risk.
- **Graceful switchover.** For a planned change, the primary first stops taking writes and [drains](/connection-draining/) its clients, the standby catches up fully, and then the role moves with no lost writes.

## Pitfalls

- **Failover without fencing.** A lease alone does not stop a paused process: it checks its lease, pauses, and writes with a stale view. Every resource the primary writes to must check the token, or the old primary must be cut off by force.
- **Clock drift.** A holder that measures its lease on a slow clock thinks it still holds the lease after the service has given it away. The holder must stop early by a margin larger than the drift over $L$. Fencing tokens do not depend on clocks, which is why they are the stronger guard.
- **Losing acknowledged writes.** A backup that is behind the primary, promoted after an asynchronous replication gap, lacks the last writes. Systems that cannot lose writes promote only a replica that has them all, as Raft does.
- **A lease service that is not itself replicated.** If the lease service is one machine, it is the new single point of failure. If it is replicated without consensus, it can grant two leases.
- **Timeouts that are too short.** A garbage collection pause or a burst of load that exceeds $L - R$ starts a failover that was not needed, and the promotion load can then fail the standby too. Detection time and false failovers trade against each other, as for any [failure detector](/failure-detector/).
- **Flapping between sites.** Failover, failback and failover again within minutes cost more than the original fault. Add a hold-down time before a node can take the role again.

## Exercises

1. With $L = 15$ s, $R = 5$ s, $P = 1$ s and $S = 4$ s, give the smallest and the largest time from a crash to the first write of the new primary.
2. Show that the storage check $t < $ maxToken in line L8 is still safe if the storage receives the writes of each holder out of order. Is it safe if two writes with the same token come from two different nodes?
3. A primary measures its lease on a clock that runs at rate $1 - \delta$ of the service clock. How early must it stop writing so that, without fencing, it never writes after the service has granted the lease to another node?
4. Compute the VRRP Master_Down_Interval for an advertisement interval of 50 centiseconds and priorities 100, 150 and 254, and explain why the priorities make the backups start at different times.

## References
