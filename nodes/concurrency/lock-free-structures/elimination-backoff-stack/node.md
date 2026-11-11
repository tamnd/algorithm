---
tag: BE3KEB
kind: data-structure
slug: elimination-backoff-stack
name: Elimination-backoff stack
aliases:
- elimination stack
area: concurrency/lock-free-structures
level: advanced
summary: Treiber stack plus an elimination array. A push and a pop that both fail their CAS meet in the array and cancel, so the stack scales under high contention.
implements: [stack]
complexity:
  vars: {n: the number of processes, k: the number of operations that run at the same time}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [treiber-stack, linearizability, lock-freedom]
see_also: [treiber-stack, exponential-backoff, diffracting-tree, combining-tree, flat-combining, linearization-point, aba-problem, hazard-pointers]
sources:
  - paper: doi:10.1145/1007912.1007944
    title: Danny Hendler, Nir Shavit and Lena Yerushalmi, A scalable lock-free stack algorithm, SPAA 2004
    locator: Section 2 (the algorithm, with the location and collision arrays), Section 3 (correctness) and the adaptive elimination strategy
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, 2020
    locator: Chapter 11 (Concurrent stacks and elimination), the lock-free exchanger, the elimination array and the range policy
  - paper: "Nir Shavit and Dan Touitou, Elimination trees and the construction of pools and stacks, SPAA 1995"
    locator: the idea of elimination (a push and a pop that meet cancel each other)
  - paper: "R. Kent Treiber, Systems programming: coping with parallelism, Research Report RJ 5118, IBM Almaden Research Center, April 1986"
    locator: the central lock-free stack that the elimination layer backs off from
---

The elimination back-off stack is a [lock-free](/lock-freedom/) [stack](/stack/) by Danny Hendler, Nir Shavit and Lena Yerushalmi (SPAA 2004). It is a [Treiber stack](/treiber-stack/) with a second path: when a push or a pop fails its [compare-and-swap](/compare-and-swap/) on `top`, it does not only wait, as [exponential back-off](/exponential-backoff/) does. It goes to a random cell of an *elimination array* and tries to meet an operation of the other kind there. A push and a pop that meet cancel each other: the pop takes the value of the push, and neither one touches `top`. The result is still [linearizable](/linearizability/), and under high load many pairs eliminate in parallel, so the stack scales where the plain Treiber stack does not.

## In plain words

Think of a busy kitchen with one pile of plates. Many cooks reach for the pile at the same time and get in the way of each other. So the kitchen adds a few side tables. A cook who could not reach the pile goes to a random side table and waits there a short time. If a cook who wants to add a plate meets a cook who wants to take one, the first one hands the plate over, and both leave. Nobody else sees it, and the pile does not change. A plate that is added and at once taken away has the same effect as if it went on the pile and came off again. If nobody comes in time, the cook goes back to the pile and tries again.

## The abstract type

The stack has push$(x)$ and pop(), and pop returns EMPTY on an empty stack. The safety condition is [linearizability](/linearizability/) and the progress condition is [lock-freedom](/lock-freedom/), as for the [Treiber stack](/treiber-stack/). The elimination path does not weaken either one. It is the stack, and not the elimination array, that is linearizable; the array on its own is an exchanger, a different object.

## Representation

### Model and notation

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names |
| $i, j$ | indices of cells of the elimination array |
| $k$ | the number of operations in progress at the same time (contention) |
| $c$ | the number of cells of the elimination array |

The processes are asynchronous and may crash between steps. They use atomic read, write and [compare-and-swap](/compare-and-swap/) (consensus number $\infty$) on single words, and the memory is sequentially consistent. A cell of the array holds a pair (item, state) in one word; real code packs the state into a stamp next to a pointer, which needs a double-width CAS or spare pointer bits. Nodes are not reused while a process holds them, as with a garbage collector; see the Treiber page for the [ABA problem](/aba-problem/) when they are.

### Fields

- `top`: the top of a [Treiber stack](/treiber-stack/).
- $E[0 \ldots c-1]$: the elimination array. Each cell holds (item, state), with state FREE, WAITING or BUSY. At the start each cell is (none, FREE).
- For each process, a local *range* $r$ with $1 \le r \le c$: the process picks cells only in $E[0 \ldots r-1]$.

**Invariant.** A cell in state WAITING holds the item of exactly one operation, its *owner*, and only the owner can change the cell from WAITING to FREE or from BUSY to FREE. A cell goes from WAITING to BUSY at most once for each WAITING phase, and the operation that does it is the owner's *partner*. The abstract stack is the list of `top`, as in the Treiber stack; the elimination array holds no part of it.

## Operations

```pseudo id=main
PUSH(v)
L1  n ← new node with n.val = v
L2  loop
L3      if TRYPUSH(n) then return              ▷ one CAS attempt on top
L4      i ← random index in [0, r)
L5      (ok, y) ← EXCHANGE(E[i], v)
L6      if ok and y = POP then r ← min(r + 1, c); return   ▷ eliminated
L7      if not ok then r ← max(r − 1, 1)       ▷ timeout: shrink the range

POP()
L8  loop
L9      x ← TRYPOP()                           ▷ an item, EMPTY or FAIL
L10     if x ≠ FAIL then return x
L11     i ← random index in [0, r)
L12     (ok, y) ← EXCHANGE(E[i], POP)
L13     if ok and y ≠ POP then r ← min(r + 1, c); return y  ▷ eliminated
L14     if not ok then r ← max(r − 1, 1)
```

TRYPUSH and TRYPOP are one pass of the Treiber loops: read `top`, prepare, and try one CAS. TRYPOP returns EMPTY if `top` is NULL and FAIL if its CAS fails. A pop offers the special item POP, so a push knows that it met a pop, and two operations of the same kind that meet just try again.

```pseudo id=exchange
EXCHANGE(cell, mine)          ▷ return (true, partner item) or (false, none)
X1  repeat at most T times
X2      (y, s) ← cell
X3      if s = FREE and CAS(cell, (y, FREE), (mine, WAITING)) then
X4          repeat at most T times
X5              (y, s) ← cell
X6              if s = BUSY then cell ← (none, FREE); return (true, y)
X7          if CAS(cell, (mine, WAITING), (none, FREE)) then return (false, none)
X8          (y, s) ← cell; cell ← (none, FREE); return (true, y)   ▷ late partner
X9      else if s = WAITING and CAS(cell, (y, WAITING), (mine, BUSY)) then
X10         return (true, y)
X11 return (false, none)
```

**The exchanger.** The first operation to reach a FREE cell puts its item there and waits. A second one that sees WAITING swaps in its own item and state BUSY with one CAS (X9), and so takes the item of the first. The first one sees BUSY, takes the item of the second, and frees the cell (X6). If nobody comes within $T$ reads, the first one tries to take its offer back with a CAS (X7). If that CAS fails, a partner came at the last moment, and the exchange succeeded after all (X8).

**Linearization points.** An operation that completes on the central stack takes effect where it would in the Treiber stack. An eliminated pair takes effect at the CAS of X9 that set the cell to BUSY: the push first and the pop right after it. At that step both operations are still in progress, so both points lie inside their intervals, and the stack is the same before and after the pair.

**The range policy.** Each process keeps its own range $r$. An elimination makes $r$ one larger, up to $c$, and a timeout makes it one smaller, down to 1. At low load, operations meet more often in a small range; at high load, a large range spreads them out so they do not collide on the same cell. Hendler, Shavit and Yerushalmi adapt both the part of the array that a thread uses and the time that it waits there. The policy above is the simpler form from the textbook of Herlihy and Shavit.

### Memory reclamation

The central stack is a [Treiber stack](/treiber-stack/), with the same need: a popped node must not be reused or freed while another pop may still read it, or the [ABA problem](/aba-problem/) and a use-after-free follow. Use tags with type-stable memory, [hazard pointers](/hazard-pointers/) or [epoch-based reclamation](/epoch-based-reclamation/). The exchanger cells hold items, not nodes, and an eliminated push never publishes its node, so the node can go back to its owner at once.

## Example

The stack holds 0. Process $p$ pushes 1, $q$ pops, $r$ pushes 2, and the array has one cell ($c = 1$).

| step | process | action | result |
|---|---|---|---|
| 1 | $p$ | TRYPUSH reads `top` (node of 0) and writes its node's `next` | |
| 2 | $q$ | TRYPOP reads `top` (node of 0) and its `next` | |
| 3 | $r$ | push(2) completes on the central stack | stack 0, 2 |
| 4 | $p$ | CAS on `top` | false |
| 5 | $q$ | CAS on `top` | false: TRYPOP returns FAIL |
| 6 | $p$ | X2 reads $E[0]$ = (none, FREE), X3 CAS to (1, WAITING) | true |
| 7 | $q$ | X2 reads (1, WAITING), X9 CAS to (POP, BUSY) | true: $q$ returns 1 |
| 8 | $p$ | X5 reads (POP, BUSY), X6 sets $E[0]$ to (none, FREE) | $p$ returns |

The results are: push(1) returns, pop returns 1, push(2) returns, and the stack still holds 0, 2. A linearization is push(2) at step 3, then push(1) and pop at step 7. The pop did not return 2, the top of the central stack, but that is fine: at step 7 the pushed 1 was on top in the linearized order.

## Correctness

Safety holds because the central stack is a Treiber stack and each elimination is an exchange of a push and a pop that are both in progress. Linearize the pair at the CAS of X9, push first and pop right after it. In the sequential stack this pair leaves the state unchanged and the pop returns the pushed value, which is what the pop returns. The other operations are linearized as in the Treiber stack. Only the owner frees its cell, so an item is taken at most once, and an operation that times out at X7 has not met anyone. The full proof is in the proof file below.

Progress: each loop iteration of a process makes one CAS attempt on `top` and spends at most $2T + 3$ steps in the exchanger. If an iteration fails both, some other operation changed `top` (a successful CAS on the central stack). So the argument of the Treiber stack applies: in an infinite run, operations keep completing. The stack is lock-free and not wait-free.

## Complexity

Alone, a push takes 4 steps and a pop 4 steps (1 on an empty stack): the first CAS succeeds and the array is never used. Under contention one operation has no bound on its steps, as in the Treiber stack. The space is one node per item plus $c$ cells and one range per process.

The gain is in throughput, not in a step bound. The paper measures it on a shared memory machine and reports that the stack scales with the number of threads where the Treiber stack with back-off does not; these are measurements, not a proved bound. The idea behind it: at high load, most failed operations meet a partner, and the pairs that meet in different cells do not touch the same cache line.

## Variants

- **The original.** Hendler, Shavit and Yerushalmi use an array `location` with one record per thread (the operation and its item) and an array `collision` of thread ids. A thread publishes its record, swaps its id into a random collision cell, and if it finds another thread there, it tries to CAS that thread's record to finish the pair. The implementation of this page uses the exchanger form of Herlihy and Shavit's textbook, which has the same linearization argument.
- **Elimination trees** (Shavit and Touitou, 1995) used the same idea earlier, in a tree of balancers like a [diffracting tree](/diffracting-tree/), to build pools and stacks.
- **Elimination for queues.** A dequeue cannot cancel any enqueue: the items already in the queue must leave first. Moir, Nussbaum, Shalev and Shavit (2005) eliminate only enqueues that are old enough.
- **[Flat combining](/flat-combining/).** A combiner can also cancel pushes with pops in its batch, but it holds a lock.

## When to use it

Use it in place of a [Treiber stack](/treiber-stack/) when many threads push and pop the same stack at once, and the mix of pushes and pops is balanced, so that pairs can meet. At low load it costs the same as the Treiber stack, because the first CAS succeeds. When almost all operations are pushes (or pops), no pairs meet and the array only adds the timeout delay.

## Pitfalls

- **Linearizing the pair at the wrong step.** The pair must take effect while both operations are in progress, at the CAS that makes the cell BUSY. A partner that returns before the owner reads BUSY is fine, because the CAS has already happened.
- **Taking the offer back with a plain write.** At X7 the owner must use a CAS: a write could erase a partner's BUSY, and then the partner returns a value that the owner never gives away.
- **Two pushes meeting.** An exchange between two pushes (or two pops) is not an elimination. Each must see the other's item and try again.
- **Timeouts that are too long.** At low load nobody comes, and each failed CAS costs $T$ wasted reads. The range and the timeout should adapt to the load.

## Implementations

## History

Shavit and Touitou introduced elimination in 1995, in elimination trees for pools and stacks. Hendler, Shavit and Yerushalmi (2004) put an elimination array in front of the [Treiber stack](/treiber-stack/) and used it as the back-off of the stack, which gave a linearizable lock-free stack that scales. Herlihy and Shavit present it in their textbook with a lock-free exchanger and a simple range policy, and the `Exchanger` class of Java is an exchanger of the same kind.

## References
