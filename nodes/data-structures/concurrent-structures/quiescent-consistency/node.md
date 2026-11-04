---
tag: JA50FD
kind: definition
slug: quiescent-consistency
name: Quiescent consistency
area: data-structures/concurrent-structures
level: advanced
summary: Correctness condition that requires operations to be ordered only between quiescent periods with no pending operations, used by counting networks.
prereqs: [race-condition, fetch-and-add]
see_also: [linearizability, sequential-consistency, counting-network, diffracting-tree, combining-tree, consistency-models]
sources:
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 3, Section 3.3 (Quiescent Consistency) and Section 3.6 (Formal Definitions); Chapter 12, Section 12.4 (Quiescently Consistent Pools and Counters)
  - paper: doi:10.1145/185675.185815
    title: James Aspnes, Maurice Herlihy and Nir Shavit, Counting networks, Journal of the ACM 41(5), 1994
    locator: the step property and the definition of a counter in a quiescent state
  - paper: doi:10.1145/235543.235546
    title: Nir Shavit and Asaph Zemach, Diffracting trees, ACM Transactions on Computer Systems 14(4), 1996
    locator: the correctness section, which proves the step property in quiescent states
---

Quiescent consistency is a correctness condition for concurrent objects: the calls must appear to take effect one at a time in some legal sequential order, and two calls must keep their real-time order only when a moment of quiescence, with no pending call at all, lies between them. It is weaker than [linearizability](/linearizability/), which keeps the real-time order of any two calls that do not overlap. Herlihy and Shavit introduced the name for the counters built from [counting networks](/counting-network/) and [diffracting trees](/diffracting-tree/), which give each value exactly once but may give a later caller a smaller value while other calls are still in progress.

## Definition

Use the history model of [sequential consistency](/sequential-consistency/): a history $H$ is a sequence of invocation and response events of threads on objects, $H|t$ is the subhistory of thread $t$, and a sequential history is *legal* if it is in the sequential specification of each object.

- A *quiescent point* of $H$ is a position in $H$ at which each invocation before it already has its matching response before it. So no call is pending there.
- For two complete calls $a$ and $b$, write $a \Rightarrow_H b$ if some quiescent point of $H$ lies after the response of $a$ and before the invocation of $b$.

**Definition.** A well-formed history $H$ is *quiescently consistent* if there is a completion $H'$ of $H$ and a legal sequential history $S$ with the same calls and the same results as $H'$, such that $a \Rightarrow_{H'} b$ implies that $a$ precedes $b$ in $S$.

An object is quiescently consistent if each of its histories is. In the words of Herlihy and Shavit, the condition is two principles: calls appear to happen in a one-at-a-time sequential order, and calls separated by a period of quiescence appear to take effect in their real-time order.

The definition keeps no program order. Two calls of the same thread can be reordered in $S$ if a call of another thread is pending across the time between them. Compare with the other conditions, where $a \to_H b$ means that $a$ responds before $b$ is invoked:

| condition | the order $S$ must keep |
|---|---|
| sequential consistency | $a \to_H b$ when $a$ and $b$ are calls of the same thread |
| quiescent consistency | $a \to_H b$ when a quiescent point lies between them |
| linearizability | each $a \to_H b$ |

Each $a \Rightarrow_H b$ and each pair of the same thread is a case of $a \to_H b$, so a linearizable history is both quiescently consistent and sequentially consistent. Neither of quiescent and sequential consistency implies the other, as the examples show.

Two more properties hold. Quiescent consistency is *compositional*: a history is quiescently consistent if and only if its subhistory on each object is. And it is *nonblocking*: a pending call of a total method never has to wait for another call for a quiescently consistent response to exist.

## Examples and non-examples

**A counting-network counter.** A shared counter gives each caller of getAndIncrement() a distinct value. A counter built from a counting network of width 2 gives value $2k + j$ to the $k$-th token that leaves on output wire $j$. Thread $B$ enters, passes the balancer to wire 0 and stalls before it reads the counter of wire 0. Thread $A$ then calls twice: its first token goes to wire 1 and gets value 1, its second goes to wire 0, finds the counter of wire 0 still at 0, and gets value 0. Then $B$ resumes and gets value 2. In real time $A$ got 1 before 0, so the history is not linearizable, and not sequentially consistent either, because both calls of $A$ are in program order. But $B$ was pending during the whole time, so no quiescent point lies between the two calls of $A$. The sequential order $S$: the second call of $A$ → 0, the first call of $A$ → 1, $B$ → 2 is legal for a counter, and the only quiescent points are before all calls and after all calls. So the history is quiescently consistent.

**Quiescently consistent but not sequentially consistent.** One FIFO queue, empty. Thread $B$ invokes deq() and stays pending. During that time thread $A$ calls enq$(x)$ and then enq$(y)$, both complete. Then $B$'s deq returns $y$. The order enq$(y)$, deq() → $y$, enq$(x)$ is legal and no quiescent point lies inside the history, so the history is quiescently consistent. It is not sequentially consistent, since program order puts enq$(x)$ before enq$(y)$, and then the first dequeue must return $x$.

**Sequentially consistent but not quiescently consistent.** One FIFO queue, empty. $A$ calls enq$(x)$ and it returns. Then, with no call pending, $B$ calls enq$(y)$ and it returns. Then $A$ calls deq() and gets $y$. The quiescent point between the two enqueues forces enq$(x)$ before enq$(y)$, so deq must return $x$: not quiescently consistent. The order enq$(y)$, enq$(x)$, deq() → $y$ keeps each thread's order, so the history is sequentially consistent.

**Not quiescently consistent.** A counter at 0. $A$ calls getAndIncrement() and gets 0. With nothing pending, $B$ calls and gets 0 too. No legal sequential counter gives the same value twice, whatever the order.

**The step property.** For counting networks the condition takes this concrete form: in each quiescent state, if $n$ calls have completed, they returned exactly the values $0, 1, \ldots, n - 1$. Aspnes, Herlihy and Shavit proved this from the step property of the output wires: in a quiescent state the numbers of tokens $y_0, \ldots, y_{w-1}$ that left the $w$ output wires satisfy $0 \le y_i - y_j \le 1$ for $i < j$.

## Related definitions

- [Linearizability](/linearizability/): keeps every real-time order, and implies quiescent consistency.
- [Sequential consistency](/sequential-consistency/): keeps program order but no real-time order between threads. It is not compositional, while quiescent consistency is.
- [Counting network](/counting-network/), [diffracting tree](/diffracting-tree/) and [combining tree](/combining-tree/): counters and pools whose natural guarantee is quiescent consistency; a combining tree is in fact linearizable.
- Quasi-linearizability and other relaxations of the sequential specification, used for [relaxed priority queues](/relaxed-priority-queue/), relax the legal sequential order instead of the real-time order.
- [Consistency models](/consistency-models/): the wider map of conditions for memory and for replicated data.

## References
