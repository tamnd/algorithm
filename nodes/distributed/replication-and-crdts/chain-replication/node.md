---
tag: BZKFM5
kind: algorithm
slug: chain-replication
name: Chain replication
aliases:
- chain replication protocol
area: distributed/replication-and-crdts
level: advanced
summary: Replicas form a chain. Updates enter at the head and pass down the chain; the tail answers queries and replies to updates, which makes the object linearizable with n - 1 crashes.
model: asynchronous-model
complexity:
  vars: {n: the number of servers in the chain}
  messages: {update: 2n, query: "2"}
  time: {update: n + 1, query: "2"}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 2004
  people: [Robbert van Renesse, Fred B. Schneider]
  note: Chain replication was introduced at OSDI 2004 for storage services that need strong consistency with high throughput; CRAQ (2009) added reads at every server.
prereqs: [state-machine-replication, linearizability, crash-failure, failure-detector]
see_also: [primary-backup-replication, quorum-replication, active-replication, replicated-log, viewstamped-replication, paxos, total-order-broadcast, cluster-reconfiguration]
sources:
  - paper: "Robbert van Renesse and Fred B. Schneider, Chain replication for supporting high throughput and availability, Proceedings of the 6th USENIX Symposium on Operating Systems Design and Implementation (OSDI), 91-104, 2004"
    locator: Section 3 (the chain, fail-stop servers, query and update processing), Section 3.1 (the Update Propagation Invariant, the Inprocess Requests Invariant, Sent lists and acks, failure of the head, the tail and other servers, extending a chain, the master replicated with Paxos), Section 4 (comparison with primary/backup) and Section 5 (weak-chain, with queries sent to any server)
  - paper: "Jeff Terrace and Michael J. Freedman, Object storage on CRAQ, high-throughput chain replication for read-mostly workloads, Proceedings of the USENIX Annual Technical Conference, 2009"
    locator: the CRAQ protocol (clean and dirty versions, reads at any server, a version query to the tail for dirty objects)
  - paper: doi:10.1145/78969.78972
    title: Maurice P. Herlihy and Jeannette M. Wing, Linearizability, a correctness condition for concurrent objects, ACM Transactions on Programming Languages and Systems 12(3), 463-492, 1990
    locator: the definition of linearizability and its locality
  - paper: doi:10.1006/jpdc.1993.1015
    title: Jeannette M. Wing and Chun Gong, Testing and verifying concurrent objects, Journal of Parallel and Distributed Computing 17(1-2), 164-182, 1993
    locator: the search for a linearization of a history, used by the tests
  - paper: doi:10.1145/98163.98167
    title: Fred B. Schneider, Implementing fault-tolerant services using the state machine approach, a tutorial, ACM Computing Surveys 22(4), 299-319, 1990
    locator: the state machine approach, of which chain replication and primary/backup are instances
---

Chain replication is a way to replicate an object on $n$ servers so that it behaves like one copy, that is, it is [linearizable](/linearizability/), while up to $n - 1$ servers crash. The servers form a chain. The first server, the **head**, receives every update, applies it, and sends the resulting change to the next server, which applies it and passes it on. The last server, the **tail**, applies it and replies to the client. Queries go to the tail alone. So the tail decides what is visible, and what the tail has applied, every server before it has applied too. A master service watches the servers, and when one crashes it removes it and links its two neighbours. van Renesse and Schneider (2004) introduced the protocol for storage services that need strong consistency and high throughput. It is a form of [primary-backup replication](/primary-backup-replication/) in which the primary's two jobs, ordering updates and answering, are split between the head and the tail.

## In plain words

Picture people standing in a line, each holding a copy of the same notebook. Changes are given to the first person. She writes the change in her notebook and passes it to the next person, who does the same, and so on to the last person. When the last person has written it, he tells the one who asked that the change is done.

Questions are always asked to the last person. Everyone before him has every change he has, and maybe more. So when he says a change is done, every copy has it.

If someone in the line leaves, a supervisor closes the gap. The person before the gap passes on the changes that might not have got through.

## The problem

Implement one object, such as a register or a key-value map, on $n$ servers so that every history of client operations is linearizable, and operations keep completing while at most $n - 1$ servers crash.

The model is the [asynchronous model](/asynchronous-model/) with message passing over reliable FIFO links. Servers are fail-stop: they fail by [crashing](/crash-failure/), and their crashes are detected. A master detects crashes and changes the chain; the paper assumes that the master does not fail, and its prototype replicates the master with [Paxos](/paxos/). Detecting crashes without mistakes needs timing assumptions, which is the role of the [failure detector](/failure-detector/) inside the master.

## The algorithm

Each server keeps the object's state, a history Hist of the updates it has applied with their sequence numbers, the number last of the last update it applied, and a list Sent of updates it has forwarded that the tail may not have applied yet. Each update carries a request id, so that a client can retry it safely.

```pseudo id=main
CLIENT-UPDATE(id, op) at the head
L1  if id is the id of an update in Hist then ignore it      ▷ a retry of an update the chain already has
L2  PROCESS((last + 1, id, op))

FORWARD(e) from the predecessor
L3  if e.seq = last + 1 then PROCESS(e)                     ▷ lower numbers are resends; ignore them

PROCESS(e)
L4  apply e.op to the state; last ← e.seq; append e to Hist
L5  if this server is the tail then reply to the client of e, and send ACK(e.seq) to the predecessor
L6  else append e to Sent, and send FORWARD(e) to the successor

ACK(s) from the successor
L7  remove from Sent every e with e.seq ≤ s; send ACK(s) to the predecessor

QUERY(q) at the tail
L8  reply with the answer of q on the state

MASTER, when it detects that server x has crashed
L9  remove x from the chain, and tell the neighbours of x and the clients the new chain     ▷ a new head needs nothing more
L10 if x was the tail: the new tail T replies to the clients of every e in Sent_T, sends ACK of the last one up, and empties Sent_T
L11 if x was in the middle, between S⁻ and S⁺: S⁻ sends every e in Sent_S⁻, in order, to S⁺, before anything else
```

The head is the only server that chooses an order, at line L2. Every other server applies the updates in that order, because links are FIFO and line L3 accepts only the next number. Because each server sends the change, not the request, only the head computes an update; the others only write it. This also means that an update can be nondeterministic: the head makes the choice once.

Line L10 is a small addition to the paper, in which a client simply sends a request again when no reply comes. The updates in the new tail's Sent are complete once it is the tail, so it can reply at once. Line L1 makes the retries safe: an update that is already in the chain is not applied a second time.

**Recovery cases.** If the head crashes, the updates that it applied but did not forward are lost. No client has a reply for them, so dropping them is allowed, and the clients retry. If the tail crashes, its predecessor becomes the tail. Its history extends the old tail's, so nothing that a client has seen is lost. If a middle server S crashes, the updates that S received but did not pass on are still in the Sent list of S⁻, and line L11 sends them to S⁺. In the paper, S⁺ first tells the master the number of the last update it has, so that S⁻ sends only the missing suffix; line L3 gets the same effect by ignoring the duplicates.

**Extending a chain.** A new server joins at the end: the current tail copies its state to it and keeps forwarding new updates, which it also adds to its Sent list, and when the new server is up to date, it becomes the tail.

## Example

Three servers $S_0$ (head), $S_1$ and $S_2$ (tail) replicate a register with value $\bot$. Every message takes 5 time units, and the master detects a crash after 20.

1. At time 0, $S_2$ crashes.
2. At time 1, a client sends write(x) to $S_0$. At time 6, $S_0$ applies it as update 1, adds it to its Sent list and forwards it. At time 11, $S_1$ applies it, adds it to Sent and forwards it to $S_2$. The message is lost.
3. At time 20, the master removes $S_2$. $S_1$ is now the tail. Its Sent list holds update 1, so it replies to the client (line L10), which gets its reply at time 25, and sends ACK(1) to $S_0$, which empties its Sent list.
4. The client then reads at the new tail $S_1$ and gets x.

**A middle crash.** Four servers $A$, $B$, $C$, $D$ have applied updates 1 to 5, and $D$ has acked up to 5. Updates 6 and 7 are applied at $A$ and $B$, and only 6 at $C$. Now $B$ crashes. The master links $A$ to $C$, and $A$ resends its Sent list, updates 6 and 7. $C$ ignores 6, which it has, applies 7, and passes it on. No update that $A$ received is lost.

**Why queries go to the tail.** Suppose a query could go to any server. A write is applied at the head and not yet at the tail. A client reads at the head and sees the new value; then another client reads at the tail and sees the old value. The second read started after the first one ended, so the history is not linearizable. In random runs of the code with reads at random servers, such histories appear; CRAQ, below, fixes this.

## Correctness

**Invariants.** Let the servers of the current chain be numbered from the head. van Renesse and Schneider state two invariants.

- *Update propagation.* If $i$ is before $j$ in the chain, then $\mathrm{Hist}_j$ is a prefix of $\mathrm{Hist}_i$.
- *Inprocess requests.* If $i$ is before $j$, then $\mathrm{Hist}_i$ is $\mathrm{Hist}_j$ merged with $\mathrm{Sent}_i$. That is, an update that $i$ has and $j$ lacks is in $\mathrm{Sent}_i$.

The first holds in normal operation because each server receives updates only from its predecessor, in order, and applies them only in order. A head crash removes the first server, which keeps the property. A tail crash removes the last one. After a middle crash, $\mathrm{Hist}_{S^+}$ is a prefix of $\mathrm{Hist}_{S^-}$, and by the second invariant the missing part is in $\mathrm{Sent}_{S^-}$, which line L11 sends before anything else. The second invariant holds because a server drops an update from Sent only after the tail has applied it, and the tail applies updates only after every server before it.

**Theorem.** If at most $n - 1$ servers crash, every history is linearizable, and every operation of a client that does not crash completes.

*Proof sketch.* Linearize each update at the moment it first enters the history of the current tail, which is at line L4 or at the change of tail of line L9, and each query at the moment the tail answers it at line L8. These points are inside the operations' intervals: the tail applies an update after the client sent it and before the client gets the reply, and the reply of line L10 also follows the change of tail. The tail's history only grows: in normal operation it appends, and when the tail changes, the new tail's history extends the old one by the update propagation invariant. So the sequence of linearization points is one sequential run of the object, and each query returns the state after exactly the updates linearized before it. Completion holds because a chain with at least one server always exists, the master repairs the chain after each crash, and a client retries until it gets an answer, with line L1 preventing a second application. The full proof is in the proof file.

## Complexity

The space is that of $n$ copies of the object, plus the Sent lists, which in steady state hold the updates of about one round trip down the chain and back.

- **Messages.** An update costs one request, $n - 1$ forwards, one reply and $n - 1$ acks, so $2n$ messages. A query costs two.
- **Latency.** An update takes $n + 1$ message delays, as the forwards are sequential; [primary-backup replication](/primary-backup-replication/) sends to all backups in parallel and needs 4. A query takes 2, and never waits for updates in progress elsewhere in the chain.
- **Outages.** After a crash is detected, the paper counts the time until service resumes: 2 message delays for updates after a head crash, 4 delays of possible extra update latency after a middle crash with no outage, and 2 delays for queries and updates after a tail crash. Primary-backup needs 5 delays after a primary crash.

## Properties

- **Linearizable** for every object type, since all queries and all updates are ordered at one server, the tail.
- **Tolerates** $n - 1$ fail-stop crashes, with $n$ servers.
- **Throughput.** Updates and queries load different servers, the head and the tail. Many chains, each for a part of the data, spread the load over all servers.
- **Not partition tolerant by itself.** The protocol needs the master to detect crashes correctly. A server that is removed by mistake and keeps answering, for example an old tail, can return stale data unless clients learn the new chain first.
- **Deterministic replicas.** Only the head runs the update; the others apply its result.

## Variants and improvements

- **CRAQ.** Terrace and Freedman (2009) let every server answer reads. A server keeps a clean version and possibly newer dirty versions of each object. A version becomes clean when the ack from the tail comes back. A read of a clean object is answered locally; for a dirty object the server asks the tail for the number of its last committed version. Reads stay linearizable, and read throughput grows with the chain length. CRAQ is a separate protocol built on chain replication, not another name for it.
- **Weak chain.** The paper also measures a variant that sends queries to any server, which gives up strong consistency for read throughput.
- **Many chains.** A storage service puts each object, or each range of keys, on its own chain, so that each server is head of some chains, middle of others and tail of others.
- **Configuration by consensus.** The master is itself replicated, for example with [Paxos](/paxos/), or the chain configuration is kept in a coordination service. See [cluster reconfiguration](/cluster-reconfiguration/).

## When to use it

Use chain replication when the service must be linearizable, crashes are detected reliably, as in one data center with a replicated master, and throughput matters more than update latency. It suits object stores and key-value stores with many reads. For update latency that does not grow with $n$, use [primary-backup replication](/primary-backup-replication/). For a service that must stay correct when failure detection can be wrong, use a consensus protocol such as [Raft](/raft/) or [Multi-Paxos](/multi-paxos/), or [quorum replication](/quorum-replication/).

## Pitfalls

- **Reading at any server.** Wrong: spread queries over all servers to gain read throughput. Right: a server before the tail can show an update that the tail has not applied, and the history stops being linearizable; use CRAQ's version check.
- **Forgetting the Sent list.** Wrong: when a middle server crashes, link its neighbours and continue. Right: the updates that the crashed server did not pass on are lost unless the predecessor resends its Sent list first.
- **Accepting forwards from an old neighbour.** Wrong: apply any forward with the next number. Right: after a repair, ignore messages from a server that is no longer the predecessor; a late message from a removed head can carry a number that the new head has given to another update.
- **Applying a retry twice.** Wrong: treat each request that reaches the head as new. Right: a client retries when a crash delays its reply; without the check of line L1, the update is applied twice.
- **False suspicion.** Wrong: assume the master is always right. Right: if the master removes a live tail, clients that still use it read stale data. The protocol needs fail-stop servers.

## Implementations

The Python code simulates a chain of servers with FIFO links, random delays, crashes at chosen times and a master that detects them after a delay and repairs the chain. Clients retry after a timeout. The tests record each client operation and check linearizability with a Wing and Gong search, and check both invariants after every event.

## History

The state machine approach and primary-backup replication date from the 1970s and 1980s. van Renesse and Schneider (2004) proposed chain replication for large storage services, compared it with primary-backup in a simulation, and showed that it gives better throughput for queries. Terrace and Freedman (2009) added reads at every server in CRAQ. The idea was used in systems such as the FAWN key-value store (2009) and HyperDex (2012), which orders the chain by attribute values.

## References
