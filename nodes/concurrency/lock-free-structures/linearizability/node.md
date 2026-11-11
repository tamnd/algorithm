---
tag: 68Z96K
kind: definition
slug: linearizability
name: Linearizability
aliases:
- atomic consistency
- atomicity of concurrent objects
- linearizable
- linearizable correctness condition
area: concurrency/lock-free-structures
level: core
summary: A safety condition for concurrent objects. Each operation seems to take effect at one instant between its call and its return, in an order that a sequential object allows.
prereqs: [race-condition, queue]
see_also: [linearization-point, sequential-consistency, quiescent-consistency, serializability, opacity, non-blocking-algorithm, atomic-snapshot, replicated-state-machine]
sources:
  - paper: doi:10.1145/78969.78972
    title: Maurice P. Herlihy and Jeannette M. Wing, Linearizability, A correctness condition for concurrent objects, ACM Transactions on Programming Languages and Systems 12(3), 1990
    locator: pages 463 to 492; Section 2 (histories, sequential specifications and the definition), Section 3 (locality as Theorem 1, the non-blocking property, and the comparison with sequential consistency and serializability)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 3, Concurrent objects (quiescent consistency, sequential consistency, linearizability, the formal definitions, the proof of locality, and the non-blocking property)
  - paper: doi:10.1109/TC.1979.1675439
    title: Leslie Lamport, How to make a multiprocessor computer that correctly executes multiprocess programs, IEEE Transactions on Computers C-28(9), 1979
    locator: pages 690 to 691 (the definition of sequential consistency)
  - paper: doi:10.1145/322154.322158
    title: Christos H. Papadimitriou, The serializability of concurrent database updates, Journal of the ACM 26(4), 1979
    locator: pages 631 to 653 (serializability of transactions)
  - paper: doi:10.1137/S0097539794279614
    title: Phillip B. Gibbons and Ephraim Korach, Testing shared memories, SIAM Journal on Computing 26(4), 1997
    locator: pages 1208 to 1244 (the problem VL of verifying linearizability of a history of reads and writes is NP-complete; special cases in polynomial time)
  - paper: doi:10.1006/jpdc.1993.1015
    title: Jeannette M. Wing and Chun Gong, Testing and verifying concurrent objects, Journal of Parallel and Distributed Computing 17, 1993
    locator: pages 164 to 182 (the search for a linearization of a recorded history)
  - paper: doi:10.1002/cpe.3928
    title: Gavin Lowe, Testing for linearizability, Concurrency and Computation, Practice and Experience 29(4), 2017
    locator: article e3928 (the Wing and Gong search with a memo of configurations, and the just-in-time algorithm)
---

Linearizability is a safety condition for a concurrent object, such as a shared queue or a shared counter. An object is linearizable if each operation seems to take effect at one instant between its invocation and its response, and the order of these instants is a legal run of the sequential object. Herlihy and Wing defined it in 1990. It is local: a system of objects is linearizable if and only if each object is, so you can build and prove objects one at a time.

## Definition

**Notation and model.** These symbols are the same on all pages of this area.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes (threads) |
| $p, q$ | process names; $i, j$ are indices |
| $k$ | the number of processes that compete at the same time (contention) |
| $m$ | the number of shared objects or memory words |

Processes are asynchronous: each process takes steps at its own speed, and a process can stop forever (crash) between two steps. Linearizability does not depend on the memory primitives that an implementation uses, and it says nothing about progress. It is a property of the histories that an object can produce. It is a safety property: if a history breaks it, some finite prefix already breaks it.

### Histories

A *history* $H$ is a finite sequence of events. An event is an *invocation* $\langle x.\mathit{op}(a), p\rangle$ (process $p$ calls method $\mathit{op}$ of object $x$ with argument $a$) or a *response* $\langle x.\mathit{ok}(r), p\rangle$ (the call returns the result $r$ to $p$). A response *matches* the earlier invocation of the same process on the same object. An *operation* is an invocation together with its matching response. An invocation without a matching response is *pending*.

- $H|p$ is the subsequence of the events of process $p$, and $H|x$ is the subsequence of the events on object $x$.
- $H$ is *sequential* if it starts with an invocation, and each invocation, except maybe the last one, is followed at once by its matching response.
- $H$ is *well formed* if each $H|p$ is sequential: a process waits for a response before its next call. All histories on this page are well formed.
- Two histories $H$ and $H'$ are *equivalent* if $H|p = H'|p$ for each process $p$.
- $\mathit{complete}(H)$ is $H$ without its pending invocations.
- The *sequential specification* of an object $x$ is a set of sequential histories of $x$, the legal ones. For a FIFO queue, a legal history is one in which each dequeue returns the oldest item still in the queue. A sequential history $S$ is *legal* if $S|x$ is legal for each object $x$.
- Operation $e$ *precedes* operation $f$ in $H$, written $e <_H f$, if the response of $e$ comes before the invocation of $f$ in $H$. This is the *real-time order*. It is a partial order. Two operations that $<_H$ does not order are *concurrent*: their intervals overlap.

### The definition

A history $H$ is **linearizable** if you can append zero or more responses to pending invocations of $H$, to get a history $H'$, so that:

- (L1) $\mathit{complete}(H')$ is equivalent to a legal sequential history $S$, and
- (L2) $e <_H f$ implies $e <_S f$ for all operations $e$ and $f$ of $\mathit{complete}(H')$.

$S$ is a *linearization* of $H$. An object is linearizable if each history that it can produce is linearizable. Rule (L2) is the one that matters: if one operation finished before another started, the linearization must keep that order. Concurrent operations can go in either order.

A pending operation may or may not have taken effect. The extension $H'$ lets a pending operation take effect, with some response, if another process already saw its effect. Otherwise $\mathit{complete}$ drops it.

The *instant* in the informal statement is the *linearization point* of the operation. Rule (L2) holds exactly when you can choose one instant in each operation interval so that the order of the instants is $S$. The [linearization point](/linearization-point/) page uses this view as a proof method.

### Locality

A property $P$ of histories is *local* if a history $H$ has $P$ if and only if $H|x$ has $P$ for each object $x$.

**Theorem 1 (Herlihy and Wing 1990).** $H$ is linearizable if and only if $H|x$ is linearizable for each object $x$.

*Proof.* Only if: let $S$ be a linearization of $H$, with extension $H'$. Then $S|x$ is legal because $S$ is legal, $\mathit{complete}(H'|x)$ is equivalent to $S|x$, and each real-time pair of $H|x$ is a pair of $H$, so $S|x$ keeps it. So $S|x$ is a linearization of $H|x$.

If: for each object $x$, let $S_x$ be a linearization of $H|x$, with the responses $R_x$ that it appends to pending invocations of $x$. Let $H'$ be $H$ followed by all the responses in all the $R_x$. Each operation of $\mathit{complete}(H')$ is on exactly one object. Let $\to$ be the union of the real-time order $<_H$ and of the orders $<_{S_x}$ for all $x$. We show that $\to$ has no cycle. Then any total order $S$ of the operations that extends $\to$ is a sequential history. It has $S|x = S_x$, which is legal, so $S$ is legal. It is equivalent to $\mathit{complete}(H')$ because it keeps the order of each process (that order is part of $<_H$). It keeps $<_H$. So $S$ is a linearization of $H$.

Suppose $\to$ has a cycle, and take one with the fewest edges. Call an edge a *time edge* if it is in $<_H$ and an *object edge* if it is in some $<_{S_x}$.

1. Two time edges in a row, $a <_H b <_H c$, give $a <_H c$, because $<_H$ is transitive. That makes a shorter cycle (or, if $a = c$, a contradiction, since $<_H$ has no cycle).
2. Two object edges in a row, $a <_{S_x} b <_{S_y} c$, have $x = y$, because $b$ is an operation of one object only. Then $a <_{S_x} c$, and the cycle is shorter again.
3. So the edges of the cycle alternate between time edges and object edges, and the cycle has an even length. A length of 2 means $a <_{S_x} b$ and $b <_H a$. That is impossible, because $S_x$ keeps the real-time order of $H|x$.
4. A length of 4 or more contains three edges $b <_H c$, $c <_{S_y} d$, $d <_H e$. Since $S_y$ keeps the real-time order of $H|y$, $d <_H c$ is false, so $c$ is invoked before $d$ responds. With times, $\mathit{res}(b) < \mathit{inv}(c) < \mathit{res}(d) < \mathit{inv}(e)$. So $b <_H e$, and this one time edge replaces three edges. The cycle is shorter, which is a contradiction.

So $\to$ has no cycle. $\square$

Locality is why you can prove a queue linearizable on its own and then use it next to a linearizable stack, with no new proof.

### The non-blocking property

Linearizability never forces a process to wait. If $H$ is linearizable and $p$ has a pending invocation of a *total* operation (one that has a legal result in every state), then there is a response $r$ such that $H$ followed by $r$ is linearizable.

*Proof.* Let $S$ be a linearization of $H$ with extension $H'$. If $H'$ already gives the pending invocation a response $r$, the same $S$ works. If not, the operation is not in $S$. Because it is total, some response $r$ makes $S$ followed by the operation with result $r$ legal. In $H$ followed by $r$, the response of this operation is the last event, so no operation must come after it in real time. So $S$ with the operation at the end is a linearization. $\square$

This *non-blocking property* of the condition is not the progress condition of a [non-blocking algorithm](/non-blocking-algorithm/). It says only that the condition itself never makes a total operation wait for a pending one. Whether an implementation lets the operation finish is a separate question: a lock-based queue is linearizable and blocking.

### Checking a history

To check one recorded history, search for $S$: pick an operation whose predecessors in $<_H$ are all placed, apply it to the sequential object, and keep it if the result matches. This is the search of Wing and Gong (1993). It can take exponential time. Gibbons and Korach (1997) showed that it is NP-complete in general to decide whether a history of reads and writes on shared registers is linearizable, and they found special cases that are polynomial. The checker of this page (lincheck.py in the implementation folder) is this search with a memo of (set of placed operations, object state) pairs, as in Lowe (2017). The other pages of this area copy it to check their objects.

## Examples and non-examples

The histories below are in the tests of this page. The checker finds each answer. Process $p_0$ and $p_1$ use one FIFO queue unless the example says otherwise. Time goes from left to right in the pictures.

**Linearizable, two orders allowed.** $p_0$ calls enq(x), $p_1$ calls enq(y), $p_1$ returns, $p_0$ returns. Then $p_0$ calls deq and gets y.

```text
p0:  |--- enq(x) ---|   |-- deq() -> y --|
p1:     |- enq(y) -|
```

The two enqueues overlap, so either order is allowed. The checker returns enq(y), enq(x), deq() returns y, and this sequence is legal.

**Not linearizable, but sequentially consistent.** enq(x) by $p_0$ returns before enq(y) by $p_1$ starts. Then deq by $p_0$ returns y.

```text
p0:  |- enq(x) -|                  |- deq() -> y -|
p1:                |- enq(y) -|
```

Real time forces enq(x) before enq(y), so a legal dequeue must return x. The history is not linearizable. It is sequentially consistent: the order enq(y), enq(x), deq() returns y keeps the order of each process, and only real time between different processes is lost.

**A stale read.** On a register with initial value 0, $p_0$ calls write(1), which returns. Then $p_1$ calls read and gets 0. This is not linearizable (the write finished before the read started) but it is sequentially consistent. A cache that is not yet up to date produces exactly this history.

**Pending operations.** $p_0$ calls enq(x) and never returns (it crashed or is slow). $p_1$ calls deq and gets x. This is linearizable: the extension gives enq(x) a response, and the order is enq(x), deq. If $p_1$ gets "empty" instead, it is also linearizable: complete() drops enq(x). If $p_1$ gets z, which nobody enqueued, it is not.

**Sequential consistency is not local.** Two queues $P$ and $Q$, and this sequential history:

```text
p0: P.enq(x)                 Q.enq(x)                 P.deq() -> y
p1:            Q.enq(y)                 P.enq(y)                       Q.deq() -> x
```

On $P$ alone, the order P.enq(y), P.enq(x), P.deq() returns y keeps each process order and is legal, so $H|P$ is sequentially consistent. On $Q$ alone, Q.enq(x), Q.enq(y), Q.deq() returns x works. But the whole history is not sequentially consistent: $P$ needs P.enq(y) before P.enq(x), the order of $p_0$ puts P.enq(x) before Q.enq(x), $Q$ needs Q.enq(x) before Q.enq(y), and the order of $p_1$ puts Q.enq(y) before P.enq(y). These four constraints form a cycle. Linearizability does not have this problem, by Theorem 1. Here $H|P$ is not linearizable either, because the history is sequential and P.deq() returns the second item.

**Locality on random histories.** The tests make 400 random histories of 5 operations by 3 processes on two queues, with random results (seed 7). The checker finds 88 linearizable and 312 not. For each of the 400, the answer for the whole history equals the answer for the two projections together, as Theorem 1 says. This is a check of the checker, not a proof.

**Linearizable implies sequentially consistent.** A linearization keeps $<_H$, and $<_H$ contains the order of each process, so each linearization is also a sequential order that keeps each process order. The tests check this on 300 more random histories.

## Related definitions

- [Sequential consistency](/sequential-consistency/) (Lamport 1979) asks for a legal sequential order that keeps the order of each process, but not the real-time order between processes. It is weaker, and it is not local, as the example above shows. It is the usual target for a memory model, not for an object.
- [Quiescent consistency](/quiescent-consistency/) keeps real-time order only across a quiescent moment, when no operation is pending. It is incomparable with sequential consistency. Counting networks give it.
- [Serializability](/serializability/) (Papadimitriou 1979) is about transactions, each of which is a group of operations on many objects: the result must equal some serial order of the transactions, with no real-time rule. Strict serializability adds the real-time rule. Linearizability is strict serializability where each transaction is one operation on one object. Serializability is not local and it can block.
- [Opacity](/opacity/) is the condition for transactional memory. It also constrains transactions that abort.
- [Linearization point](/linearization-point/) is the proof method: pick one step inside each operation where it takes effect.
- Progress conditions such as [lock-freedom](/lock-freedom/) and [wait-freedom](/wait-freedom/) are separate. Linearizability is about what results are allowed; progress is about whether operations finish. A page should state both.
- In distributed storage, "strong consistency" often means linearizability of a replicated register or of a [replicated state machine](/replicated-state-machine/). The definition is the same; there the processes are clients and the object is the service.

## References
