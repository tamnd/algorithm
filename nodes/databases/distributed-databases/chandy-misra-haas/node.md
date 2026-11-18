---
tag: H4QN6P
kind: algorithm
slug: chandy-misra-haas
name: Chandy-Misra-Haas edge chasing
aliases:
- edge chasing
- probe-based distributed deadlock detection
area: databases/distributed-databases
level: advanced
summary: "Detects a deadlock spread over sites by sending small probes along the wait-for edges between sites. A probe that comes back to its initiator shows a cycle of waiting processes."
solves: [cycle-detection]
model: asynchronous-model
complexity:
  vars: {e: the number of wait-for edges between processes at different sites, n: the number of processes at one site, p: the number of processes in the system}
  messages: {worst: "e(e + 1)"}
  space: {extra: "O(n p)"}
properties: {deterministic: true, recursive: false}
history:
  year: 1983
  people: [K. Mani Chandy, Jayadev Misra, Laura M. Haas]
  note: "Chandy and Misra gave the probe algorithm for resource deadlocks at PODC 1982. The 1983 paper with Haas added the query and reply algorithm for communication deadlocks and proved that both find all true deadlocks and no false ones."
prereqs: [deadlock-detection, wait-for-graph]
see_also: [deadlock, wait-die-and-wound-wait, primary-copy-locking, read-one-write-all, lock-table, dijkstra-scholten, termination-detection, chandy-lamport-snapshot]
sources:
  - paper: doi:10.1145/357360.357365
    title: "K. Mani Chandy, Jayadev Misra and Laura M. Haas, Distributed deadlock detection, ACM Transactions on Computer Systems 1(2), 1983, pages 144 to 156"
    locator: "Section 2.1 (the resource model), Section 2.3 (cycles in the resource model and knots in the communication model), Section 3.1 (the probe algorithm and the outline of its proof), Section 4 (query computations for the communication model) and Section 5 (the bound on probes and the idle time before a computation starts)"
  - paper: doi:10.1145/800220.806693
    title: "K. Mani Chandy and Jayadev Misra, A distributed algorithm for detecting resource deadlocks in distributed systems, Proceedings of the First ACM Symposium on Principles of Distributed Computing, 1982, pages 157 to 164"
    locator: the probe algorithm for the resource model with its detailed proofs
---

The Chandy-Misra-Haas algorithm finds deadlocks in a distributed database without building the global [wait-for graph](/wait-for-graph/) anywhere. Each site knows only its own lock table. When a process has waited for some time, its site starts a *probe computation*: it sends a short fixed-size message, a probe, along each wait-for edge that leaves the site. A site that gets a probe for a process that still waits passes it on along the edges that leave that site. If a probe comes back to the process that started it, the process is on a cycle of waiting processes, and it is deadlocked. The method is also called *edge chasing*, because the probes chase the edges of the graph. The paper proves that, if no transaction aborts while probes are in flight, the algorithm reports every deadlock and no false one.

## In plain words

People wait in queues at several offices, and each person can wait for a person in another office. Nobody can see all the queues. If you have waited for a long time, you write your name on a card and give it to the person you wait for. That person, if still waiting, passes your card to the person they wait for, and so on. A person who is not waiting throws the card away. If your own card comes back to you, there is a ring of people who all wait for each other, and none of them will ever move.

Each card is small and the same size, and each person needs to remember only whose cards they have passed on.

## The problem

The model is the resource model of Chandy, Misra and Haas (1983), Section 2.1. Each site has a controller that manages the resources at the site with exclusive locks. A transaction $t$ has a *home process* $(t, h)$ at its home site and at most one *agent* $(t, m)$ at each other site $m$. For a resource at another site, the home controller sends the request to the agent, which asks its own controller and replies when it has the resource. Channels between sites are first in, first out, and messages are not lost, as in the [asynchronous model](/asynchronous-model/) with [FIFO delivery](/fifo-delivery/).

A process is *idle* while it waits. The wait-for edges are:

- a *local edge* $(u, s) \to (v, s)$ when $(u, s)$ waits at $s$ for a resource that $v$ holds at $s$;
- a *remote edge* $(t, h) \to (t, m)$ when the home process waits for the reply of the agent at $m$;
- a *remote edge* $(t, m) \to (t, h)$ when the agent holds resources at $m$ and waits for its home process to tell it to release them.

The paper defines $P_i$ to be *dependent* on $P_k$ when a chain of idle processes leads from $P_i$ to $P_k$, each waiting for the next, and *locally dependent* when the whole chain is at one controller. A process is deadlocked when it is on a cycle of such waits, or depends on a process that is. The task is to declare a process deadlocked if and only if it is on a cycle, with only local knowledge at each controller. Let $\mathrm{LD}^*(P_k)$ be the set of processes that $P_k$ reaches by local edges, with $P_k$ itself.

The third kind of edge is not spelled out in the paper. The code adds it, because without it a cycle can pass through an agent that holds a resource and seems to be executing, and then the detector misses a real deadlock.

## The algorithm

```pseudo id=main
INITIATE(i)                                    ▷ at the controller of an idle process P_i
L1  if P_i is on a cycle of local edges then declare P_i deadlocked and stop
L2  m_i ← m_i + 1                              ▷ the number of this computation
L3  for each P_a in LD*(P_i) and each P_b at another site such that P_a waits for P_b do
L4      send probe(i, m_i, a, b) to the controller of P_b
RECEIVE-PROBE(i, m, j, k)                      ▷ at the controller of P_k
L5  if P_k is idle and P_k has not answered P_j and dependent_k(i) < m then
L6      dependent_k(i) ← m
L7      if P_i is in LD*(P_k) then declare P_i deadlocked
L8      else for each P_a in LD*(P_k) and each P_b at another site such that P_a waits for P_b do
L9          send probe(i, m, a, b) to the controller of P_b
WHEN P_k STOPS BEING IDLE
L10 clear dependent_k
```

A probe $(i, m, j, k)$ belongs to computation number $m$ of the initiator $P_i$, and goes from $P_j$ at one site to $P_k$ at another. The flag dependent$_k(i)$ means that the controller of $P_k$ knows that $P_i$ depends on $P_k$. A probe that fails the test of line L5 is dropped. The test "has not answered $P_j$" is condition (iii) of the paper: if $P_k$ is an agent, the request of its home is still waiting; if $P_k$ is a home process, it has not sent a new request to the agent $P_j$, which would answer the wait of the agent.

The code differs from Section 3.1 of the paper in two places, and the page shows why:

- **The declaration test.** The paper declares $P_i$ when $k = i$. Line L7 also declares when $P_i$ is in $\mathrm{LD}^*(P_k)$, that is, when the probe comes back to the site of $P_i$ through a remote edge that ends at another process. The option literal=True of the code uses the test of the paper.
- **Numbered computations.** The paper keeps a Boolean flag. The code keeps the number of the last computation, as the query computations of Section 4 of the paper do.

The paper does not say when to start a computation. Section 5 suggests starting one only for a process that has been idle for some time $T$. The code starts one when a process becomes idle, at a random later step, and again for every idle process when no message is in transit.

## Example

**Two sites, and the test $k = i$.** Transaction 1 has its home at $S_1$ and holds $a$ there. Transaction 2 has its home at $S_2$ and holds $b$ there. Then 1 asks for $b$ and 2 asks for $a$. The cycle is

$$(1, S_1) \to (1, S_2) \to (2, S_2) \to (2, S_1) \to (1, S_1),$$

with remote edges from each home process to its agent and local edges from each agent to the home process of the other transaction. $S_1$ starts a computation for $(1, S_1)$. It sends probe$(1, 1, (1,S_1), (1,S_2))$ to $S_2$. There the agent $(1, S_2)$ waits for $b$, held by $(2, S_2)$, which waits for its agent at $S_1$, so $S_2$ sends probe$(\dots, (2,S_2), (2,S_1))$ back to $S_1$. The probe arrives at $(2, S_1)$, not at $(1, S_1)$. With line L7, $S_1$ sees that $(1, S_1)$ is in $\mathrm{LD}^*((2, S_1))$ and declares it deadlocked after 2 probes. With the test $k = i$, $S_1$ passes the probe on along the edge from $(1, S_1)$ to $(1, S_2)$ again, and $S_2$ drops it because the flag is set: 3 probes and no declaration. A computation for $(2, S_1)$, the end of a remote edge, finds the cycle with either test.

**Three sites, and the numbers.** Transaction $t$ has its home at $S_t$ and holds a resource there. Transaction 1 asks for the resource of 2, and 2 asks for the resource of 3, while 3 is still running. A computation for $(1, S_1)$ sets flags at $(1, S_2)$ and $(2, S_3)$, and stops, because $(3, S_3)$ is not idle. Then 3 asks for the resource of 1, and the cycle closes. A second computation for $(1, S_1)$ with Boolean flags is dropped at $(1, S_2)$, and the deadlock is never reported for $(1, S_1)$. With numbers, the second computation passes and declares $(1, S_1)$.

## Correctness

The proofs are on [the proof page](proofs/correctness.md). They assume, as the paper does in Section 3, that no transaction aborts while a computation runs.

- **No false deadlocks (theorem).** When a process is declared, it is on a cycle of the true wait-for graph. The key facts are that the target of a wait edge must stop being idle before the edge can go away, so chains of waits ending at an idle process are stable, and that first in, first out channels keep a probe behind the request or the reply that it follows.
- **Every cycle is found (theorem).** If a computation for $P_i$ starts while $P_i$ is on a cycle, $P_i$ is declared by it or by a later computation. With the test $k = i$, this holds only when the edge of the cycle that enters $P_i$ is a remote edge.
- **Measurements.** The tests compare every declaration with a global wait-for graph built from all controllers at once. In 150 random runs on 3 sites with 3 to 5 transactions, while other transactions still move and change the graph, all 652 declarations were of processes on a cycle, and each of the 95 runs that ended in a deadlock had a declared process on each cycle. In 739 single computations on frozen graphs, a process was declared exactly when it was on a cycle (405 times).

## Complexity

- **Messages.** If the graph does not change during a computation, each process accepts the computation at most once, so at most $e$ processes and the initiator forward probes, each at most one per remote edge: at most $e(e + 1)$ probes. The paper, Section 5, states a bound of $e$ probes, where $e$ is the number of pairs of processes that communicate. In the code, two processes at one site can forward the same probe, and on frozen graphs a computation sent at most 7 probes and at most 1.5 times the number of remote edges.
- **Message size.** A probe has four fields, the initiator, the number, the sender and the receiver, whatever the size of the graph.
- **Space.** A controller keeps, for each of its $n$ processes, a number per initiator: $O(n p)$. It also keeps the number of the last computation of each of its own processes.
- **Time.** A probe moves one remote edge per message delay, so a computation that finds a cycle with $r$ remote edges takes $r$ delays.

## Properties

- **No central site.** No controller builds the global graph. Each one answers a probe from its own lock table.
- **Work only when processes wait.** Probes are sent only for idle processes, and a running process drops them. Section 5 of the paper points out that the cost of detection falls on idle processes.
- **Many initiators per cycle.** Every process on a cycle can start a computation, and each can declare itself. If each declaration aborts a victim, one cycle can lose several transactions.
- **Phantom deadlocks with aborts.** The proofs assume no aborts during a computation. With victims, a probe that is in flight when a victim aborts can still close a cycle that no longer exists. In 150 random runs with victims, 58 of 232 declarations were of a process that was no longer on a cycle. Every such case came after an earlier declaration in the same run, no transaction stayed waiting, and 387 transactions committed.

## Variants and improvements

- **The communication model.** Section 4 of the paper handles processes that wait for a message from any one process of a set, as in CSP. Deadlock is then a knot, not a cycle, and the algorithm uses query and reply messages, in the style of the [Dijkstra-Scholten](/dijkstra-scholten/) algorithm for [termination detection](/termination-detection/).
- **Probes sent once.** A controller that remembers which probes of a computation it has already sent can skip duplicates, and then a computation on a frozen graph sends at most one probe per remote edge.
- **One initiator per cycle.** If the transactions have priorities and a site passes on only the probes of initiators with a higher priority than the process that the probe reaches, only the process with the highest priority on a cycle can complete a computation. Then each cycle gives one declaration. This idea is a heuristic: with aborts during a computation, phantoms can still occur.
- **Path pushing.** Obermarck (1982), cited by the paper, sends whole paths of the wait-for graph between sites instead of fixed-size probes. The messages are larger, and the sites can see which transactions form the cycle.
- **Avoiding detection.** Timestamp rules such as [wait-die and wound-wait](/wait-die-and-wound-wait/) prevent cycles, at the cost of some aborts that are not needed. Many systems also use timeouts.

## When to use it

Use edge chasing when locks are kept by many sites, as in [primary copy locking](/primary-copy-locking/) or [read-one write-all](/read-one-write-all/), deadlocks are rare, and you do not want a central detector that collects the lock tables. Start computations only for processes that have waited for some time, so that short waits cost nothing. If deadlocks are frequent, or if a wrong abort is expensive, a central detector or a prevention rule can be simpler.

## Pitfalls

- **The declaration test.** With the test $k = i$ alone, a computation for a process whose cycle comes back through a local edge never reports it. Either check $\mathrm{LD}^*(P_k)$ as in line L7, or start computations for every waiting process.
- **Stale flags.** Boolean flags that stay set at a process that stays idle can stop a later computation for the same initiator. Number the computations.
- **Hidden waits.** An agent that holds a resource for its transaction looks busy at its own site, but it cannot release the resource until its home tells it to. Leaving out this wait hides real deadlocks.
- **Channels that reorder.** Lemma 2 of the proof needs a probe to stay behind the request or the reply that it follows on the same channel. On a network that reorders messages, a probe can arrive before the request it is about and be dropped, or arrive after a reply and close a cycle that is gone.
- **Aborts during a computation.** Probes in flight can name a cycle that an abort has broken. Treat a declaration as a reason to abort only if the transaction is still waiting, and expect some victims that were not needed.

## Implementations

## History

By the early 1980s many distributed deadlock detection protocols had been published, and Chandy, Misra and Haas (1983) quote Gligor and Shattuck (1980): "renewed interest in distributed systems has resulted in the publication of at least ten protocols for deadlock detection. However, few of these protocols are correct and fewer appear to be practical." Chandy and Misra (1982) gave the probe algorithm for the resource model at the first PODC, with detailed proofs. The 1983 paper in ACM Transactions on Computer Systems, with Haas, took the resource model from Menasce and Muntz (1979), restated the probe algorithm, and added the query algorithm for the communication model, which builds on the termination detection of Dijkstra and Scholten (1980). Obermarck (1982), whom the paper cites, had given a path-pushing algorithm in ACM Transactions on Database Systems in the same period.

## References
