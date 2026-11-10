---
tag: GQ5H12
kind: data-structure
slug: vector-clocks
name: Vector clocks
aliases:
- vector timestamps
area: distributed/clocks-and-ordering
level: core
summary: A vector of n counters per process, merged by entrywise maximum on each receive, so that event a happened before event b if and only if V(a) < V(b).
model: asynchronous-model
complexity:
  vars: {n: the number of processes}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1988
  people: [Colin Fidge, Friedemann Mattern]
  note: Fidge in 1988 and Mattern in 1989 published vector timestamps that capture happened-before exactly.
prereqs: [happened-before, lamport-clocks, asynchronous-model]
see_also: [vector-clock-characterization, lamport-clock-condition, concurrent-events, matrix-clocks, version-vectors, plausible-clocks, interval-tree-clocks, causal-broadcast]
sources:
  - paper: "Colin J. Fidge, Timestamps in message-passing systems that preserve the partial ordering, Proceedings of the 11th Australian Computer Science Conference, 1988"
    title: Colin J. Fidge, Timestamps in message-passing systems that preserve the partial ordering
    locator: pages 56 to 66
  - paper: "Friedemann Mattern, Virtual time and global states of distributed systems, in Parallel and Distributed Algorithms, Cosnard et al. (eds.), North-Holland, 1989"
    title: Friedemann Mattern, Virtual time and global states of distributed systems
    locator: pages 215 to 226
  - paper: doi:10.1007/BF02277859
    title: Reinhard Schwarz and Friedemann Mattern, Detecting causal relationships in distributed computations, in search of the holy grail, Distributed Computing 7(3), 1994
    locator: pages 149 to 174
  - paper: doi:10.1016/0020-0190(91)90055-M
    title: Bernadette Charron-Bost, Concerning the size of logical clocks in distributed systems, Information Processing Letters 39(1), 1991
    locator: pages 11 to 16 (n entries are necessary)
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 3, Section 3.4 (vector time)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 6, Section 6.1 (vector clocks)
  - paper: doi:10.1109/TSE.1983.236733
    title: D. Stott Parker Jr. et al., Detection of mutual inconsistency in distributed systems, IEEE Transactions on Software Engineering SE-9(3), 1983
    locator: pages 240 to 247 (version vectors)
---

A vector clock is an array of $n$ counters that each of $n$ processes keeps, one counter for each process. A process adds 1 to its own entry at each event, sends a copy of the array with each message, and on a receive takes the entrywise maximum with the copy in the message. Entry $k$ of the timestamp $V(e)$ is then the number of events of process $k$ that [happened before](/happened-before/) $e$, with $e$ itself counted. So $e \to f$ if and only if $V(e) < V(f)$, and [concurrent events](/concurrent-events/) have incomparable vectors. [Lamport clocks](/lamport-clocks/) give only one direction of this test.

## In plain words

Each computer keeps a row of counters, one counter for each computer in the group. When something happens on a computer, it adds one to its own counter. When it sends a message, it sends a copy of the whole row. When it gets a message, it keeps the larger value of each pair of counters. Then it adds one to its own counter.

The row of an event says, for each computer, how many of its events could have had an effect on this event. To compare two events, compare their rows counter by counter. If no counter of the first row is larger, and the rows differ, the first event came first. If each row has a counter that is larger than in the other row, neither event could have affected the other.

## The abstract type

The type is a logical clock for the [asynchronous model](/asynchronous-model/) with $n$ processes $p_1, \ldots, p_n$, known in advance, with reliable point-to-point channels that need not be FIFO. No failure assumption is needed: crashes, lost messages and duplicates do not break the properties below, because each property is about the events that happen. Each process has one instance. The operations are TICK for a local event, SEND, which returns the timestamp to put on a message, and RECEIVE, which takes the timestamp of a message. A query compares two timestamps. The specification is the characterization

$$e \to f \iff V(e) < V(f) \qquad \text{for all events } e, f,$$

where $V \le W$ means $V[k] \le W[k]$ for each $k$, and $V < W$ means $V \le W$ and $V \ne W$. The [vector clock characterization](/vector-clock-characterization/) page states this theorem with its hypotheses and proves it.

## Representation

Process $p_i$ stores an array $V_i[1 \ldots n]$ of non-negative integers. Entry $V_i[i]$ is the number of events of $p_i$ so far. For $k \ne i$, entry $V_i[k]$ is the number of events of $p_k$ that are in the causal past of the present state of $p_i$. A timestamp is a copy of $V_i$, taken at an event.

## Operations

```pseudo id=main
VECTOR-CLOCK at process p_i
L1  V_i ← (0, 0, …, 0)                     ▷ n entries

TICK()                                     ▷ a local event
L2  V_i[i] ← V_i[i] + 1
L3  return a copy of V_i

SEND(m)
L4  attach t ← TICK() to m, and send m

RECEIVE(m)                                 ▷ m carries W
L5  for k ← 1 to n do
L6      V_i[k] ← max(V_i[k], W[k])
L7  return TICK()

LEQ(V, W)
L8  return V[k] ≤ W[k] for each k

LESS(V, W)                                 ▷ for event stamps: happened-before
L9  return LEQ(V, W) and V ≠ W

CONCURRENT(V, W)
L10 return not LEQ(V, W) and not LEQ(W, V)
```

A message that $p_i$ receives never has $W[i] > V_i[i]$, because the sender knows at most the events of $p_i$ that $p_i$ has done. So it does not matter whether RECEIVE takes the maximum before or after the tick of line L2. Fidge and Mattern state the two rules in different orders.

If the process $p_i$ of an event $e$ is known, a cheaper test exists: for $f \ne e$, $e \to f$ if and only if $V(e)[i] \le V(f)[i]$. It reads one entry of each vector.

## Example

Three processes run seven events. $P_1$ sends a message to $P_2$ (event $a$) and then does a local event $b$. $P_2$ does a local event $c$, receives the message of $a$ (event $d$) and sends a message to $P_3$ (event $e$). $P_3$ does a local event $f$ and receives the message of $e$ (event $g$).

| event | process | kind | $V$ |
|---|---|---|---|
| $a$ | $P_1$ | send | $(1, 0, 0)$ |
| $b$ | $P_1$ | local | $(2, 0, 0)$ |
| $c$ | $P_2$ | local | $(0, 1, 0)$ |
| $d$ | $P_2$ | receive from $a$ | $\max((0,1,0), (1,0,0))$, then tick: $(1, 2, 0)$ |
| $e$ | $P_2$ | send | $(1, 3, 0)$ |
| $f$ | $P_3$ | local | $(0, 0, 1)$ |
| $g$ | $P_3$ | receive from $e$ | $\max((0,0,1), (1,3,0))$, then tick: $(1, 3, 2)$ |

- $a \to g$: $(1, 0, 0) < (1, 3, 2)$. The cheap test reads entry 1: $1 \le 1$.
- $b \parallel e$: $(2, 0, 0)$ and $(1, 3, 0)$ are incomparable, since $2 > 1$ in entry 1 and $0 < 3$ in entry 2. The [Lamport clock](/lamport-clocks/) values of the same events are 2 and 3, which look ordered.
- $b \parallel g$: entry 1 of $V(b)$ is 2, and entry 1 of $V(g)$ is 1. So the event $b$ is not in the past of $g$, although $g$ has heard from $P_1$.

## Correctness

The key invariant is a count: $V(e)[k]$ equals the number of events of $p_k$ in the causal past of $e$, with $e$ included. The causal past restricted to one process is always a prefix of that process's events. A receive takes the union of two causal pasts, and the union of two prefixes of one sequence is the longer one, so its length is the maximum of the two lengths. This is why line L6 takes the maximum. The tick of line L2 then counts $e$. The characterization follows: $e \to f$ makes the past of $e$ a subset of the past of $f$ that misses $f$, and $V(e)[i] \le V(f)[i]$ puts $e$ inside the prefix of $p_i$ that $f$ knows. The full proof is below.

## Complexity

| operation | time | message overhead |
|---|---|---|
| TICK | $\Theta(1)$, plus $\Theta(n)$ for the copy | none |
| SEND | $\Theta(n)$ | $n$ integers |
| RECEIVE | $\Theta(n)$ | none |
| LEQ, LESS, CONCURRENT | $\Theta(n)$ | none |
| the cheap test with a known process | $\Theta(1)$ | none |

Each process stores $n$ integers. Each entry is at most the number of events of one process, so with $k$ events in the run a timestamp has $O(n \log k)$ bits.

The size $n$ is necessary. Charron-Bost proved in 1991 that for each $n$ there is a run of $n$ processes in which no map of events into $\mathbb{R}^d$ with $d < n$, ordered entrywise, captures happened-before in both directions. The [clock condition](/lamport-clock-condition/) page gives this proof. So vector clocks are optimal in the number of entries among clocks of this form, and a smaller clock must give up exactness, as [plausible clocks](/plausible-clocks/) do.

## Variants

- **Differential sends.** Singhal and Kshemkalyani send only the entries that changed since the last message to the same process. This needs FIFO channels and two more vectors per process. Kshemkalyani and Singhal describe it in Chapter 3 of their book.
- **[Version vectors](/version-vectors/).** The same array, used for the state of a replica instead of an event: one entry per replica, increased on an update, merged on a sync. They detect conflicting updates.
- **[Matrix clocks](/matrix-clocks/).** Each process also keeps its best knowledge of the vector of each other process. This tells it which events every process knows about.
- **[Interval tree clocks](/interval-tree-clocks/).** A tree in place of an array, for a set of processes that grows and shrinks.
- **[Dotted version vectors](/dotted-version-vectors/).** A version vector plus one isolated event, for key-value stores with many clients.

## When to use it

Use vector clocks when you must decide, after the fact, whether two events are causally ordered or concurrent, and the set of processes is fixed and small. Typical uses are [causal broadcast](/causal-broadcast/), the detection of concurrent writes, debuggers and race detectors for message-passing programs, [consistent cuts](/consistent-cut/) and [predicate detection](/distributed-predicate-detection/). If you only need a total order that respects causality, one Lamport integer is enough. If processes join and leave often, an interval tree clock avoids a global array of identifiers.

## Pitfalls

- **Comparing with the wrong order.** $V \le W$ must hold in every entry. A comparison by sum, by the largest entry or in lexicographic order gives a total order and loses the concurrency information.
- **Vector clocks against version vectors.** A vector clock timestamps every event, including each send and receive. A version vector changes only on an update of the data, and a sync merges without a tick. Using one rule where the other belongs gives either false conflicts or lost ones.
- **Unbounded growth of the set of processes.** If a key-value store gives one entry to each client that ever wrote, the vectors grow with the number of clients. Pruning entries to save space can make old updates look concurrent, or make a new update look old.
- **Equal vectors.** For two different events the vectors are never equal. Equal vectors in a real system usually mean that a process restarted and reused old counters.
- **Copy, do not share.** The timestamp of an event must be a copy. If a message keeps a reference to the live array, later events change the timestamp in the message.

## Implementations

## History

Colin Fidge published vector timestamps at the Australian Computer Science Conference in 1988, and Friedemann Mattern published them in 1989 as part of a theory of virtual time and global states. Both proved that the vectors characterize happened-before. Charron-Bost proved in 1991 that $n$ entries are necessary. Schwarz and Mattern surveyed the theory in 1994. Vectors of this kind appeared earlier in work on replicated data, such as the version vectors of Parker et al. in 1983.

## References
