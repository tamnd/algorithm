---
tag: 4YSQ42
kind: definition
slug: sequential-consistency
name: Sequential consistency
aliases:
- sequential consistency model
area: data-structures/concurrent-structures
level: advanced
summary: 'Weaker correctness condition: operations appear in some single sequential order that respects each thread''s program order.'
prereqs: [race-condition, queue]
see_also: [linearizability, quiescent-consistency, consistency-models, causal-consistency, serializability, concurrent-queue]
sources:
  - paper: doi:10.1109/TC.1979.1675439
    title: Leslie Lamport, How to make a multiprocessor computer that correctly executes multiprocess programs, IEEE Transactions on Computers C-28(9), 1979
    locator: pages 690 to 691, the definition of sequential consistency
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 3, Section 3.4 (Sequential Consistency) and Section 3.6 (Formal Definitions)
  - paper: doi:10.1109/2.546611
    title: Sarita V. Adve and Kourosh Gharachorloo, Shared memory consistency models, a tutorial, IEEE Computer 29(12), 1996
    locator: the sections on sequential consistency and on relaxed memory models
  - paper: doi:10.1137/S0097539794279614
    title: Phillip B. Gibbons and Ephraim Korach, Testing shared memories, SIAM Journal on Computing 26(4), 1997
    locator: the NP-completeness of testing sequential consistency
---

Sequential consistency is a correctness condition for shared objects and shared memory: an execution is sequentially consistent if its operations give the same results as some single sequential order of all of them, in which the operations of each thread keep the order of that thread's program. Lamport defined it in 1979 for multiprocessor memory. It is weaker than [linearizability](/linearizability/), because the single order need not respect real time between threads, and unlike linearizability it is not compositional: two sequentially consistent objects used together can give an execution that is not sequentially consistent.

## Definition

We use the model of histories of Herlihy and Wing. A *history* $H$ is a finite sequence of *invocation* events $\langle t: o.m(a) \rangle$ and *response* events $\langle t: o.r \rangle$, where $t$ is a thread, $o$ an object, $m$ a method with argument $a$, and $r$ a result. A response *matches* the last earlier invocation of the same thread. Write $H|t$ for the subsequence of the events of thread $t$, and $H|o$ for the events on object $o$.

- $H$ is *well formed* if each $H|t$ alternates invocation, matching response, invocation, and so on, starting with an invocation. So each thread has at most one pending call.
- $H$ is *sequential* if it starts with an invocation, and each invocation, except possibly the last, is immediately followed by its matching response.
- A sequential history is *legal* if, for each object $o$, $H|o$ is in the sequential specification of $o$.
- Two histories $H$ and $H'$ are *equivalent* if $H|t = H'|t$ for each thread $t$.
- A *completion* of $H$ is a history obtained by appending responses for some pending invocations and then removing the remaining pending invocations; complete$(H)$ denotes the set of these.

**Definition.** A well-formed history $H$ is *sequentially consistent* if there is a completion $H'$ of $H$ and a legal sequential history $S$ such that $S$ is equivalent to $H'$.

An object is sequentially consistent if each of its histories is. For shared memory, the objects are read/write registers: a read returns the value of the last write to the same address before it in $S$, or the initial value.

Compare with linearizability. Write $a \to_H b$ if the response of call $a$ comes before the invocation of call $b$ in $H$. Then $H$ is *linearizable* if, in addition, $S$ can be chosen so that $a \to_H b$ implies that $a$ comes before $b$ in $S$. Sequential consistency keeps only the order inside each thread, which is the part of $\to_H$ between calls of the same thread. So

$$\text{linearizable} \Rightarrow \text{sequentially consistent},$$

and the converse is false, as the first example shows.

## Examples and non-examples

**Sequentially consistent but not linearizable.** One FIFO queue $q$, initially empty. Thread $A$ calls $q$.enq$(x)$, which returns. Then thread $B$ calls $q$.enq$(y)$, which returns. Then $A$ calls $q$.deq() and gets $y$. In real time, enq$(x)$ ends before enq$(y)$ starts, so a linearization must put $x$ first, and then deq must return $x$: the history is not linearizable. But the sequential history $B$.enq$(y)$, $A$.enq$(x)$, $A$.deq() → $y$ is legal and keeps the order of each thread ($A$ enqueues before it dequeues). So the history is sequentially consistent. A search over all six orders of the three calls finds exactly this one as legal and equivalent.

**Not compositional.** Two queues $p$ and $q$, both empty. All calls of the same step overlap in time.

| | thread $A$ | thread $B$ |
|---|---|---|
| first | $p$.enq$(x)$ | $q$.enq$(y)$ |
| second | $q$.enq$(x)$ | $p$.enq$(y)$ |
| third | $p$.deq() → $y$ | $q$.deq() → $x$ |

On $p$ alone the order $B$: $p$.enq$(y)$, $A$: $p$.enq$(x)$, $A$: $p$.deq() → $y$ is legal and keeps the order of each thread, so $H|p$ is sequentially consistent. In the same way $H|q$ is. But $H$ is not. Suppose $S$ were a legal equivalent order. On $p$, $A$ gets $y$, so $p$.enq$(y)$ precedes $p$.enq$(x)$ in $S$. Program order puts $q$.enq$(y)$ before $p$.enq$(y)$ in $B$, and $p$.enq$(x)$ before $q$.enq$(x)$ in $A$. So $q$.enq$(y)$ precedes $q$.enq$(x)$, and $B$'s dequeue on $q$ must return $y$, not $x$. A contradiction. This is why Herlihy and Wing call linearizability *local* and sequential consistency not: for linearizability, $H$ is linearizable if and only if each $H|o$ is.

**Store buffering.** Two registers $x = y = 0$. Thread 1 runs $x \leftarrow 1$; $r_1 \leftarrow y$. Thread 2 runs $y \leftarrow 1$; $r_2 \leftarrow x$. Under sequential consistency the outcome $r_1 = r_2 = 0$ is impossible. In a single order $S$ that keeps program order, let the last of the four operations be, say, $r_1 \leftarrow y$ (the other cases are the same up to names). Then $y \leftarrow 1$ is before it, so $r_1 = 1$. In general the last operation is a read, and the write of the other thread comes before it. The outcomes $(r_1, r_2) = (0, 1), (1, 0), (1, 1)$ are all sequentially consistent. Processors with store buffers, such as x86 under its total store order model, allow $r_1 = r_2 = 0$, so they are not sequentially consistent without fence instructions. Programs such as [Peterson's algorithm](/peterson-algorithm/) and [Dekker's algorithm](/dekker-algorithm/) rely on sequential consistency and fail on such hardware without fences.

**Not sequentially consistent.** One register $x = 0$. Thread $A$ writes 1 and then reads 0. In any equivalent order the write of $A$ comes before its read, and no other write exists, so the read must return 1.

**A sequentially consistent object that is not linearizable.** A register implemented by a write that returns at once and is applied later, while each thread reads its own pending writes first, gives histories like the first example: each thread sees its own operations in order, but a read in another thread may miss a write that has already returned.

**Checking.** Gibbons and Korach proved that deciding whether a given history of reads and writes is sequentially consistent is NP-complete. Small histories can be checked by searching all orders that keep program order, as for the examples above.

## Related definitions

- [Linearizability](/linearizability/): sequential consistency plus the real-time order between threads. It is local (compositional) and is the usual condition for concurrent data structures.
- [Quiescent consistency](/quiescent-consistency/): respects real time only across periods of quiescence, and does not keep program order. Neither of quiescent and sequential consistency implies the other.
- [Serializability](/serializability/): the analogue for transactions, groups of operations, in databases. Strict serializability adds real time and is the analogue of linearizability.
- [Causal consistency](/causal-consistency/) and [eventual consistency](/eventual-consistency/): weaker conditions for replicated data. See [consistency models](/consistency-models/).
- [Linearization point](/linearization-point/): the usual tool to prove linearizability, and so also sequential consistency.
- Memory models: total store order and the models of C++ and Java are weaker than sequential consistency. The C++ and Java models guarantee sequential consistency to programs without data races.

## References
