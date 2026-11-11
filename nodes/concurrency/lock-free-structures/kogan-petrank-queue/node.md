---
tag: MAZDKN
kind: data-structure
slug: kogan-petrank-queue
name: Kogan-Petrank wait-free queue
aliases:
- Kogan-Petrank queue
- KP queue
area: concurrency/lock-free-structures
level: research
summary: First practical wait-free FIFO queue, built by adding helping and phases to the Michael-Scott queue.
implements: [queue]
complexity:
  vars: {n: the number of processes}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [michael-scott-queue, wait-freedom, linearizability]
see_also: [helping, universal-construction, herlihy-wing-queue, lcrq, linearization-point, hazard-pointers, aba-problem]
sources:
  - paper: doi:10.1145/1941553.1941585
    title: Alex Kogan and Erez Petrank, Wait-free queues with multiple enqueuers and dequeuers, PPoPP 2011
    locator: Section 3 (the algorithm, with Java code for enq, deq, help, help_enq, help_finish_enq, help_deq and help_finish_deq); Section 4 (correctness, linearization points and wait-freedom)
  - paper: doi:10.1145/248052.248106
    title: Maged M. Michael and Michael L. Scott, Simple, fast, and practical non-blocking and blocking concurrent queue algorithms, PODC 1996
    locator: Figure 1, the lock-free queue that the wait-free queue extends
  - paper: doi:10.1145/2145816.2145835
    title: Alex Kogan and Erez Petrank, A methodology for creating fast wait-free data structures, PPoPP 2012
    locator: the fast-path-slow-path method, with the queue as the main example
  - paper: doi:10.1145/2851141.2851168
    title: Chaoran Yang and John Mellor-Crummey, A wait-free queue as fast as fetch-and-add, PPoPP 2016
    locator: the related-work comparison with the Kogan-Petrank queue
---

The Kogan-Petrank queue is a [wait-free](/wait-freedom/) [queue](/queue/) for many enqueuers and many dequeuers. Alex Kogan and Erez Petrank published it at PPoPP 2011. It keeps the linked list, the dummy node and the two CAS steps of the [Michael-Scott queue](/michael-scott-queue/), and it adds a shared array `state` with one entry for each process. A process first writes a description of its operation into its entry, with a *phase* number that is larger than all phases it sees. Then it [helps](/helping/) every pending operation whose phase is not larger than its own, its own operation included. So an old operation is finished by every new operation, and no operation waits for ever. The queue is [linearizable](/linearizability/). Each operation ends within $O(n^2)$ of its own steps for $n$ processes, whatever the other processes do.

## In plain words

At a post office counter, people sometimes push to the front, and an unlucky person can wait all day. Here each person takes a ticket number when they arrive, a bit higher than all the numbers they can see. Before anyone may do their own business, they must look at the board and finish the business of every person with a lower or equal number who is still waiting.

So once your ticket is on the board, every person who arrives later must finish your business before they leave. You do not need to win any race. Even if you fall asleep, the others do your work for you.

## The abstract type

The queue has enq$(x)$, which adds $x$ at the back, and deq(), which removes and returns the front item, or returns EMPTY if the queue has no items. The safety condition is [linearizability](/linearizability/) with respect to a sequential FIFO queue. The progress condition is [wait-freedom](/wait-freedom/): each operation of a process that keeps taking steps completes within a bounded number of its own steps, whatever the other processes do, and even if they crash. This is stronger than the [lock-freedom](/lock-freedom/) of the Michael-Scott queue, where one operation can fail its CAS without end.

## Representation

### Model and notation

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes, fixed and known; ids $0, \ldots, n-1$ |
| $p, q$ | process names |
| $i$ | an index into `state` |
| $ph$ | a phase number |

The processes are asynchronous and may crash between any two steps. They use atomic read, write and [compare-and-swap](/compare-and-swap/) (consensus number $\infty$) on single words. The memory is sequentially consistent, except in the paragraph on weak memory. As in the paper, which is written in Java, nodes and descriptors are never reused while a process holds them (a garbage collector). Safety (linearizability) and progress (wait-freedom) are proved apart.

### Fields

- A node has `value`, `next`, `enqTid` (the id of the process whose enqueue made it) and `deqTid` (the id of the process whose dequeue took the item after it, or $-1$).
- `Head` and `Tail` are as in the Michael-Scott queue: `Head` points to the dummy node, and `Tail` points to the last node or to the one before it.
- `state[i]` points to an immutable *descriptor* (phase, pending, enqueue, node) of the last operation of process $i$. A change to an entry always installs a new descriptor with a CAS on the entry, so a CAS that compares descriptors cannot be fooled by an old one.

**Invariant.** (Q1) to (Q3) of the [Michael-Scott queue](/michael-scott-queue/) hold for `Head`, `Tail` and the list. In addition:

- **(K1)** A node is linked into the list at most once, and only while the descriptor that holds it is pending.
- **(K2)** If `Tail.next` is a node $x$, then the descriptor of process $x.enqTid$ either has node $x$ and is pending, or is no longer pending.
- **(K3)** If `Head.deqTid` is a process $p$, then the descriptor of $p$ points to `Head` (or is no longer pending), and `Head.next` is not NULL.

## Operations

```pseudo id=main
ENQ(v)                                         ▷ process tid
L1  ph ← MAXPHASE() + 1; x ← new node(v, next = NULL, enqTid = tid, deqTid = −1)
L2  state[tid] ← (ph, pending = true, enqueue = true, x)   ▷ publish
L3  HELP(ph)
L4  HELPFINISHENQ()

DEQ()                                          ▷ process tid
L5  ph ← MAXPHASE() + 1
L6  state[tid] ← (ph, pending = true, enqueue = false, NULL)
L7  HELP(ph)
L8  HELPFINISHDEQ()
L9  d ← state[tid]
L10 if d.node = NULL then return EMPTY
L11 return d.node.next.value

HELP(ph)
L12 for i ← 0 to n − 1 do
L13     d ← state[i]
L14     if d.pending and d.phase ≤ ph then
L15         if d.enqueue then HELPENQ(i, ph)
L16         else HELPDEQ(i, ph)

HELPENQ(i, ph)
L17 while ISSTILLPENDING(i, ph) do
L18     last ← Tail
L19     nx ← last.next
L20     if last = Tail then
L21         if nx = NULL then
L22             if ISSTILLPENDING(i, ph) then
L23                 if CAS(last.next, NULL, state[i].node) then   ▷ enqueue takes effect
L24                     HELPFINISHENQ(); return
L25         else HELPFINISHENQ()               ▷ Tail lags: finish that enqueue first

HELPFINISHENQ()
L26 last ← Tail
L27 nx ← last.next
L28 if nx ≠ NULL then
L29     j ← nx.enqTid
L30     cur ← state[j]
L31     if last = Tail and cur.node = nx then
L32         CAS(state[j], cur, (cur.phase, false, true, nx))    ▷ mark the enqueue done
L33     CAS(Tail, last, nx)
```

`MAXPHASE()` reads all $n$ entries and returns the largest phase. `ISSTILLPENDING(i, ph)` reads `state[i]` and returns whether it is pending with phase at most $ph$. The dequeue side has two more procedures.

```pseudo id=helpdeq
HELPDEQ(i, ph)
D1  while ISSTILLPENDING(i, ph) do
D2      first ← Head; last ← Tail; nx ← first.next
D3      if first ≠ Head then continue
D4      if first = last then
D5          if nx = NULL then                  ▷ the queue looks empty
D6              cur ← state[i]
D7              if last = Tail and cur is pending with phase ≤ ph then
D8                  CAS(state[i], cur, (cur.phase, false, false, NULL))   ▷ deq returns EMPTY
D9          else HELPFINISHENQ()
D10     else
D11         cur ← state[i]; x ← cur.node
D12         if not (cur.pending and cur.phase ≤ ph) then break
D13         if first = Head and x ≠ first then
D14             if not CAS(state[i], cur, (cur.phase, true, false, first)) then continue
D15         CAS(first.deqTid, −1, i)           ▷ dequeue takes effect
D16         HELPFINISHDEQ()

HELPFINISHDEQ()
D17 first ← Head; nx ← first.next; j ← first.deqTid
D18 if j ≠ −1 then
D19     cur ← state[j]
D20     if first = Head and nx ≠ NULL then
D21         CAS(state[j], cur, (cur.phase, false, false, cur.node))   ▷ mark the dequeue done
D22         CAS(Head, first, nx)
```

**Enqueue.** L1 to L2 choose a phase and publish a pending descriptor that holds the new node. From then on, any process may link this node. HELPENQ is the enqueue loop of the Michael-Scott queue, run on behalf of process $i$: it links `state[i].node` after the last node with a CAS at L23. Before it links, it checks again that the operation is still pending (L22), so a node is never linked twice. HELPFINISHENQ finishes the enqueue whose node is after `Tail`: it marks that descriptor not pending (L32), and only then moves `Tail` (L33). The order matters: while `Tail` lags, no other node can be linked, so nobody can link the same node again.

**Dequeue.** A dequeue descriptor first gets the dummy node that it will remove (D14), and then claims the node by writing its id into `deqTid` with a CAS (D15). Only one process can claim a dummy, so only one dequeue gets each item. HELPFINISHDEQ marks the owner of the claim done (D21) and then moves `Head` (D22). A dequeue that finds the list empty with `Tail` not lagging finishes with node NULL (D8) and returns EMPTY. The owner reads its result from its own descriptor (L9 to L11): the value is in the node after the old dummy.

**Linearization points.** An enqueue takes effect at the successful CAS at L23, by whatever process does it. A dequeue that returns an item takes effect at the successful CAS at D15 that writes its id. A dequeue that returns EMPTY takes effect at the read of `first.next` in D2 of the iteration whose CAS at D8 succeeds: at that moment `Head` is `first` and its `next` is NULL. All these steps lie between the publication of the operation and its return, since helpers act only on a pending descriptor, and the owner returns only after the descriptor is no longer pending.

**Why it is wait-free.** An operation $O$ with phase $ph$ that is published is helped by every operation that starts later, because a later operation reads the phase of $O$ during MAXPHASE, so its own phase is larger. A later operation cannot return while $O$ is pending. So each other process can have at most two operations that take effect while $O$ is pending, and each loop iteration that does not end the loop needs one of a few kinds of change (a node linked, `Tail` or `Head` moved, or the descriptor changed). This gives the bound in the section on complexity.

**Phases by a counter.** MAXPHASE costs $n$ reads. A shared counter with [fetch-and-add](/fetch-and-add/) gives phases with the same property in one step.

### Memory reclamation

The paper relies on the Java garbage collector, and the code needs it in two places. First, a node that leaves the list as the old dummy can still be read by a helper that read it as `Head` or `Tail`, as in the Michael-Scott queue. Second, `state[i]` is changed by CAS on descriptor pointers: if an old descriptor were freed and its address reused for a new one, a stale CAS at L32, D8, D14 or D21 could succeed on the wrong descriptor and, for example, mark a new enqueue done before its node is linked (the [ABA problem](/aba-problem/)). The implementation here gives each descriptor a unique id, which plays the part of a fresh object. In C or C++, protect nodes and descriptors with [hazard pointers](/hazard-pointers/) or [epoch-based reclamation](/epoch-based-reclamation/); then a helper that is stalled still keeps only $O(1)$ objects alive.

### Weak memory

The wait-freedom argument uses the fact that an operation that starts after $O$ is published sees $O$ in MAXPHASE: a write to `state[p]` followed by reads of other entries, in other processes. This is a store-then-load pattern, which needs sequential consistency for these accesses. Java `AtomicReference` gives it. In C++, use `memory_order_seq_cst` for the accesses to `state`, `Head`, `Tail` and the node links, or prove a weaker choice again.

## Example

**A crashed enqueue is finished by another process.** The queue is empty, and $n = 2$. Process 1 calls enq(7). It reads both phases ($-1$), takes phase 0, makes node $x$, and publishes (phase 0, pending, enq, $x$) at L2. Then it crashes. Process 0 calls deq() twice.

| step | process | lines | action | state after it |
|---|---|---|---|---|
| 1 | 1 | L1, L2 | publish enq(7) with phase 0 | `state[1]` pending, list $D$ |
| 2 | 0 | L5, L6 | read phases $-1$ and 0, publish deq with phase 1 | `state[0]` pending |
| 3 | 0 | L13, D1 to D8 | entry 0 has phase $1 \le 1$; the list is empty, so finish it with node NULL | `state[0]` done, EMPTY |
| 4 | 0 | L13, L17 to L23 | entry 1 has phase $0 \le 1$; link $x$ after $D$ | list $D \to x$ |
| 5 | 0 | L26 to L33 | mark `state[1]` done, move `Tail` to $x$ | `state[1]` done |
| 6 | 0 | L9, L10 | the first deq returns EMPTY | |
| 7 | 0 | L5 to D22 | the second deq: claim $D$, mark done, move `Head` | returns 7 |

Process 1 never runs again, yet its item is in the queue, and the history (enq(7) pending, deq() = EMPTY, deq() = 7) is linearizable: enq(7) takes effect at step 4. The order of the help scan is by index, not by phase, which is why the first deq of process 0 is finished first.

## Correctness

Safety follows the Michael-Scott queue: the list, `Head` and `Tail` change only as in that queue, so (Q1) to (Q3) hold. The new parts are the descriptor rules (K1) to (K3). A node is linked only after a check that its descriptor is pending, and its descriptor is marked done before `Tail` moves past it, so no node is linked twice. A dummy is claimed by one CAS on `deqTid`, its claimer is marked done before `Head` moves, so each item goes to exactly one dequeue. The proof file gives the linearizability argument in outline and the step bound with its derivation. The paper gives the full proof (Section 4).

## Complexity

| operation | alone (this implementation) | worst case, any schedule |
|---|---|---|
| enq | $2n + 18$ steps | $O(n^2)$ steps |
| deq of an item | $2n + 24$ steps | $O(n^2)$ steps |
| deq on an empty queue | $2n + 14$ steps | $O(n^2)$ steps |

The space is one node per item plus the dummy, plus $n$ descriptors. The solo counts are measured on the implementation; they grow with $n$ because MAXPHASE and HELP read all $n$ entries even when no other process runs, which is the main cost of this queue at low contention.

The worst case is derived on this page, as an outline in the proof file: at most $2n + 12 + 20n(6n + 2)$ steps for each operation. The paper proves that the queue is wait-free; we did not find this explicit constant there. The tests check every operation against this bound in all schedules with at most three preemptions for two processes, and in seeded random runs with up to four processes. In that search with two processes, the largest count is 48 steps, against a bound of 576.

## Variants

- **Help fewer entries.** A process can help its own entry and only one other entry per operation, picked in turn, in place of all $n$ entries. Each operation then does less helping. An old operation gets help later than in the basic scheme, so its bound is larger; this page does not derive that bound.
- **Fast path, slow path.** Kogan and Petrank (2012) run the lock-free Michael-Scott code first and switch to the wait-free code only after a number of failed attempts. This keeps the speed of the lock-free queue in the common case and the bound of the wait-free one.
- **Queues based on fetch-and-add.** Yang and Mellor-Crummey (2016) built a wait-free queue on [fetch-and-add](/fetch-and-add/) over a long array, with a similar fast-path-slow-path scheme; [LCRQ](/lcrq/) is a fast lock-free queue on the same idea.
- **Universal construction.** A [universal construction](/universal-construction/) makes any object wait-free with the same kind of helping, but it copies or replays whole states, so it is much slower than this queue.

## When to use it

Use it when every operation must end in bounded time, for example in real-time or interactive code where one thread must not starve behind the others. It is slower than the [Michael-Scott queue](/michael-scott-queue/) when nobody needs help, because each operation scans the $n$ entries twice. In most other code the lock-free queue, or the fast-path-slow-path version of this one, is the better choice. The number of processes must be known, and each process needs a fixed id.

## Pitfalls

- **Linking without the second pending check.** Without L22, a slow helper can link the node of an enqueue that another helper already finished, and the item enters the queue twice.
- **Moving `Tail` before marking the descriptor.** If L33 came before L32, a new node could be linked after $x$ while the descriptor of $x$ still looks pending, and a helper could link $x$ again.
- **Comparing descriptors by value.** A CAS on `state[i]` must compare a descriptor that cannot come back. Two descriptors with the same fields are different objects; with reuse of memory, use a unique id or a reclamation scheme.
- **A strict test at L14.** Two operations can get the same phase, and an operation is done only by HELP, its own included. With $<$ in place of $\le$, an operation never helps itself, and it can wait for ever.

## Implementations

## History

Herlihy (1991) showed that every object has a wait-free implementation from consensus objects, with a [universal construction](/universal-construction/), but it is far too slow for a queue. Earlier practical wait-free queues allowed only one enqueuer or one dequeuer, or used a [Herlihy-Wing](/herlihy-wing-queue/) style array that is wait-free only for enqueue. Kogan and Petrank (2011) gave the first practical wait-free queue for many enqueuers and many dequeuers, with helping by phases on the list of the Michael-Scott queue, and in 2012 a method to make it nearly as fast as the lock-free queue. Later queues based on fetch-and-add are faster still.

## References
