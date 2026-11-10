---
tag: WTCD0Y
kind: concept
slug: leader-lease
name: Leader lease
area: distributed/consensus
level: advanced
summary: Time-bounded leadership grant that lets a leader serve reads without a round trip.
prereqs: [quorum, clock-drift, multi-paxos]
see_also: [raft, view-change, split-brain, clock-skew, monotonic-clock, truetime, replicated-state-machine, paxos]
sources:
  - paper: doi:10.1145/74851.74870
    title: Cary G. Gray and David R. Cheriton, Leases, an efficient fault-tolerant mechanism for distributed file cache consistency, 12th ACM Symposium on Operating Systems Principles (SOSP), 1989
    locator: the definition of a lease as a contract for a limited term, and the allowance for message delay and clock drift in the term
  - paper: doi:10.1145/1281100.1281103
    title: Tushar D. Chandra, Robert Griesemer and Joshua Redstone, Paxos made live, an engineering perspective, 26th ACM Symposium on Principles of Distributed Computing (PODC), 2007
    locator: the section on master leases (reads served from the local copy of the master while its lease holds)
  - url: https://web.stanford.edu/~ouster/cgi-bin/papers/OngaroPhD.pdf
    title: Diego Ongaro, Consensus, bridging theory and practice, PhD thesis, Stanford University, 2014
    locator: Chapter 6, Section 6.4 (processing read-only queries more efficiently) and Section 6.4.1 (using clocks to reduce messaging for read-only queries)
  - paper: "Mike Burrows, The Chubby lock service for loosely-coupled distributed systems, 7th USENIX Symposium on Operating Systems Design and Implementation (OSDI), 2006"
    locator: the master lease of the Chubby cell, and the client leases kept alive by KeepAlive calls
---

A leader lease is a promise, for a fixed time, that no other node will become leader. A majority of the nodes of a consensus group give the promise to one node. While the lease holds, that node knows that no other leader can commit a write, so it can answer reads from its own copy of the state, with no messages. The idea comes from the leases of Gray and Cheriton (1989), which give a cache a time-limited right to its data. Because the promise is about time, the lease is safe only if the clocks drift by a bounded amount: with the drift bound $\rho$, a promise of $T$ on each granter's clock allows the leader to use the lease for at most $T(1 - \rho)/(1 + \rho)$ on its own clock, counted from the moment it sent the request.

## In plain words

A shop has one person at the till. Before she starts, she asks most of her coworkers: "Do not let anyone else take the till for ten minutes." Each one agrees and starts a timer.

While her ten minutes run, she can answer any question about today's sales at once, because no one else can have sold anything. She does not need to ask around first.

But the timers are cheap and some run fast. If a coworker's timer says ten minutes when only nine have passed, he may let someone else take the till while she still thinks it is hers. So she stops a little early, by an amount that covers the worst timer, and she starts counting from the moment she asked, not from the moment they agreed.

## The idea

### Why a leader needs a lease to read locally

In [Multi-Paxos](/multi-paxos/) or [Raft](/raft/), a write is committed when a [quorum](/quorum/) of nodes accepts it. A node that thinks it is the leader may be wrong: a network partition may have cut it off, and the other nodes may have elected a new leader that has committed new writes. If the old leader answers a read from its own copy, it returns a stale value, and the system is not linearizable. Without a lease, the leader must first check that it is still leader, for example by a round of heartbeats to a majority, which costs a round trip for each read or batch of reads (Ongaro, Section 6.4).

A lease removes the round trip. Each node that grants a lease to node $L$ promises not to grant a lease to another node, and not to vote for another leader, until a time $T$ has passed on its own clock. If $L$ holds grants from a majority, any other node needs a majority too, and the two majorities share a node that is bound by its promise. So, while the lease holds, no other node can become leader and no other node can commit a write. $L$ can serve reads locally.

### The safe length of a lease

**Model.** Real time is $t$. Each node $p$ has a clock $C_p$ whose rate is within the [drift](/clock-drift/) bound: $(1 - \rho)(t_2 - t_1) \le C_p(t_2) - C_p(t_1) \le (1 + \rho)(t_2 - t_1)$ for $t_1 \le t_2$, with $0 \le \rho < 1$. Clocks need not be synchronized; only their rates matter. Message delays are unbounded.

**The protocol.**

1. At real time $s$, node $L$ reads its clock $C_L(s)$ and sends a lease request.
2. A node $g$ that receives the request at real time $r_g \ge s$ grants it if it has no promise in force to another node. It records $C_g(r_g) + T$ and refuses every other node until its clock passes that value.
3. When $L$ has grants from a majority, it holds the lease until its own clock reads $C_L(s) + T'$.

**Claim.** If $T' \le T (1 - \rho)/(1 + \rho)$, then no node $g$ that granted the lease to $L$ grants a lease to another node before the lease of $L$ has ended in real time.

*Proof.* Let $e_L$ be the real time at which the lease of $L$ ends, so $C_L(e_L) = C_L(s) + T'$. The clock of $L$ runs at rate at least $1 - \rho$, so $T' = C_L(e_L) - C_L(s) \ge (1 - \rho)(e_L - s)$, which gives $e_L \le s + T'/(1 - \rho)$. Let $f_g$ be the real time at which the promise of $g$ ends, so $C_g(f_g) = C_g(r_g) + T$. The clock of $g$ runs at rate at most $1 + \rho$, so $T \le (1 + \rho)(f_g - r_g)$, which gives $f_g \ge r_g + T/(1 + \rho) \ge s + T/(1 + \rho)$. With the condition on $T'$, $T'/(1 - \rho) \le T/(1 + \rho)$, so $e_L \le f_g$. $\square$

**Corollary.** If every leader takes its lease from a majority with this rule, then at every real time at most one node holds a lease. Two majorities share a node $g$. If $g$ granted to $L$ first, it grants to $M$ only after $f_g \ge e_L$, and $M$ holds its lease only after it receives that grant. So the lease of $M$ starts after the lease of $L$ ends.

The two choices in the protocol are both needed. The lease is measured from the time $L$ sent the request, which is before every grant, because $L$ does not know how long the grants were in transit. And the factor $(1 - \rho)/(1 + \rho)$ covers the worst case, a slow clock at $L$ and a fast clock at a granter. For small $\rho$ it is about $1 - 2\rho$. If the clocks are synchronized to within a skew $\varepsilon$ and the lease is given as an absolute expiry time, the rule becomes "stop $\varepsilon$ early" instead; Gray and Cheriton describe this form, an allowance $\varepsilon$ for clock skew and message delay.

### What else a leader must do before it reads locally

A lease stops other leaders from committing writes while it holds. It does not by itself give $L$ every write that was committed before it took the lease. A new leader must first learn the committed state from a quorum. In Raft, this is the rule that a new leader commits an entry of its own term, for example a no-op, before it serves reads (Ongaro, Section 6.4). After that, a local read at real time $t$ returns every write committed before $t$, because no write by another leader can commit while the lease holds.

Renewal works the same way: before the lease ends, $L$ sends a new request at time $s'$, and on a majority of grants the lease runs to $C_L(s') + T'$. A leader that keeps its lease never has a gap.

### Pitfalls

- **Counting from the reply.** If $L$ starts its lease when the last grant arrives, a delay $d$ in transit adds up to $d$ to its lease. The simulation below finds stale reads in this case with perfect clocks and delays up to 2 time units.
- **No margin for drift.** Setting $T' = T$ is wrong as soon as $\rho > 0$. With $\rho = 0.1$ and $T = 10$, the lease of a slow leader can last $10/0.9 = 11.1$ real time units after it asks, while a fast granter is free after $10/1.1 = 9.1$.
- **Clocks that jump.** The bound is on the rate of the clock. A wall clock that is stepped by NTP or by an operator does not satisfy it. Use a [monotonic clock](/monotonic-clock/) for lease times.
- **Pauses.** A process can check that its lease holds, then stop for a garbage collection pause or a page fault, and send the reply after the lease ended. The check and the reply must both happen inside the lease, so a leader should use a margin for its own pauses or check the lease again after it builds the reply.
- **Availability.** If the leader crashes, no other node can take over until the promises to it have ended. A long lease makes reads cheap but makes the time without a leader after a crash long.
- **Writes are not faster.** A lease saves messages only for reads. A write still needs a quorum.

## Examples

**Practical numbers.** A crystal oscillator with a drift bound of $\rho = 10^{-4}$ (100 parts per million) and a promise of $T = 10$ seconds gives $T' = 10 \cdot 0.9999/1.0001 \approx 9.998$ seconds. The margin is about 2 milliseconds. The margin is small, so the real cost of the rule is not the lost time but the need for a true bound on the drift.

**A partition, with numbers.** The simulation in `impl/python/leader_lease.py` has three nodes with $T = 10$ and the assumed bound $\rho = 0.1$, so $T' = 10 \cdot 0.9/1.1 \approx 8.18$. Each message takes up to 0.2 time units. Node 0 has the slowest allowed clock, rate 0.9, and nodes 1 and 2 have the fastest, rate 1.1. All clocks start at 0. Node 0 asks for the lease at real time 0.1 (its clock reads 0.09) and gets it. At real time 1 the network cuts it off, but it keeps serving reads from its own copy.

| case | lease of node 0 ends (real time) | promises to node 0 end (real time) | node 1 holds a lease from | stale reads | steps with two leaders |
|---|---|---|---|---|---|
| $T' = 8.18$, rates 0.9 and 1.1 | 9.19 | 9.25 and 9.29 | 9.4 | 0 | 0 |
| $T' = 10$ (no margin), rates 0.9 and 1.1 | 11.21 | 9.25 and 9.29 | 9.5 | 1 | 18 |
| $T' = 8.18$, rates 0.7 and 1.3 (drift beyond the bound) | 11.79 | 7.85 and 7.89 | 8.6 | 8 | 32 |

In the first row the lease of node 0 ends at real time $8.27/0.9 = 9.19$. Node 1 received the request at real time $r$ and promised until its clock reads $1.1 r + 10$, which is real time $r + 10/1.1 \ge 0.1 + 9.09$. So the bound is tight, and still safe. In the second row node 1 commits its first write at real time 9.7, and node 0, whose clock says its lease runs to 10.09, that is real time 11.21, serves a stale read at real time 10.2. In the third row the clocks break the assumed bound, and node 0 serves 8 stale reads.

**Random runs.** The tests also run the protocol with random clock rates in $[1 - \rho, 1 + \rho]$, random partitions, renewals, random message delays and 3 or 5 nodes. With the safe rule, 60 runs of 200 time units each give no stale read and never two lease holders. With $T' = T$, or with true drift $0.3$ against an assumed $0.1$, some runs give two lease holders and stale reads, and with perfect clocks but the lease counted from the last grant, some runs fail when the delays are long.

## Where it is used

- Chubby elects a master with Paxos and gives it a master lease. The master serves reads from its local state, and clients hold their own leases on sessions, kept alive by KeepAlive calls (Burrows, 2006).
- Paxos Made Live describes master leases in the Paxos library under Chubby: while the lease holds, the master serves reads from its local data, and replicas refuse to accept a new master (Chandra, Griesemer and Redstone, 2007).
- The Raft thesis gives the lease form of read-only queries, with a bound on clock drift, as an option next to the safer ReadIndex form that needs a heartbeat round (Ongaro, Section 6.4.1). Implementations such as etcd offer both.
- Spanner gives each Paxos leader a timed lease and uses [TrueTime](/truetime/) to keep the leases of a group from overlapping.
- The first use was for caches: in the V file system a client holds a lease on a file and may use its cached copy until the lease ends, and the server waits for all leases on a file to end, or be given up, before a write (Gray and Cheriton, 1989).
- A lease is also a defence against [split brain](/split-brain/) in [primary-backup replication](/primary-backup-replication/): an old primary stops serving when its lease ends, even if it cannot tell that it was replaced.

## References
