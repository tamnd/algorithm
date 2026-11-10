---
tag: 6PTRCW
kind: problem
slug: event-ordering
name: Event ordering
aliases:
- ordering of events
- logical ordering of events
area: distributed/clocks-and-ordering
level: intro
summary: Give each event of a distributed run a timestamp, computed from local knowledge and message tags only, so that timestamps respect happened-before, or capture it exactly.
prereqs: [happened-before, asynchronous-model]
see_also: [lamport-clocks, vector-clocks, lamport-clock-condition, vector-clock-characterization, total-order, hybrid-logical-clocks, plausible-clocks, matrix-clocks]
sources:
  - paper: doi:10.1145/359545.359563
    title: Leslie Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7), 1978
    locator: pages 558 to 565, sections Logical Clocks and Ordering the Events Totally
  - paper: doi:10.1109/2.485846
    title: Michel Raynal and Mukesh Singhal, Logical time, capturing causality in distributed systems, IEEE Computer 29(2), 1996
    locator: the whole paper (scalar, vector and matrix time, and their properties)
  - paper: doi:10.1016/0020-0190(91)90055-M
    title: Bernadette Charron-Bost, Concerning the size of logical clocks in distributed systems, Information Processing Letters 39(1), 1991
    locator: the lower bound of n entries for vector clocks that characterize causality
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 3 (logical time, Sections 3.3 to 3.7)
---

The event ordering problem asks for timestamps on the events of a distributed run that agree with causality. There is no shared clock, and physical clocks disagree, so the timestamps must be computed from what each process knows: its own events and the tags carried by the messages it receives. The weak form asks that an event that [happened before](/happened-before/) another get a smaller timestamp. The strong form asks that the timestamps capture happened-before exactly, so that concurrency can be read off them.

## In plain words

Several computers work together and send each other messages. Later, someone wants to sort what happened. Their wall clocks are not reliable, so the computers need another way to stamp their events.

The minimum we ask for: if one event could have caused another, its stamp must be smaller. A simple counter that each computer keeps, and that jumps ahead when it sees a bigger number on a message, already does this.

Sometimes we want more. We may want to look at two stamps and know whether the events are related at all, or were independent. Then each stamp needs to say what the event knew about every computer, which costs one number per computer. We may also want stamps close to the wall clock, or one fixed order that all computers agree on.

## Definition

**Model.** A system of $n$ processes runs in the [asynchronous model](/asynchronous-model/). Each process sees only its own events. It may attach a tag to each message it sends and read the tags of messages it receives.

**Task.** At each event $e$, the process of $e$ must compute a timestamp $T(e)$ from a set $\mathcal{T}$ with a strict partial order $<$. The computation may use only the local state and the tags of received messages. The timestamps must satisfy one of:

- **Weak clock condition.** $a \to b$ implies $T(a) < T(b)$. This is [Lamport's clock condition](/lamport-clock-condition/).
- **Strong clock condition.** $a \to b$ if and only if $T(a) < T(b)$. This is the property of the [vector clock characterization](/vector-clock-characterization/).

The cost measures are the size of a timestamp, the size of a message tag, and the local work per event.

## Variants

- **Total ordering.** Produce a [total order](/total-order/) of all events that extends $\to$, and that every process can compute alike. Lamport clocks with process ids as tie-breakers give one.
- **Concurrency detection.** Decide, from the timestamps of two events, whether they are [concurrent](/concurrent-events/). This needs the strong condition.
- **Bounded size with few errors.** Use timestamps of fixed size, keep the weak condition, and report as few concurrent pairs as ordered as possible. These are [plausible clocks](/plausible-clocks/).
- **Closeness to real time.** Keep the weak condition and also stay within the [clock skew](/clock-skew/) of physical time, as [hybrid logical clocks](/hybrid-logical-clocks/) do.
- **Knowledge of others.** Let each process know a lower bound on what every other process knows, for example to discard old data. [Matrix clocks](/matrix-clocks/) give this.
- **Versions of replicas.** Order the states of replicas, not single events, and detect conflicting updates: [version vectors](/version-vectors/), [dotted version vectors](/dotted-version-vectors/) and, with changing sets of replicas, [interval tree clocks](/interval-tree-clocks/).

## Examples

In the running example, $P_1$ sends from $a$ to $d$ on $P_2$, and $P_2$ sends from $e$ to $g$ on $P_3$. The events $b$, $c$ and $f$ are local.

| event | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ | $g$ |
|---|---|---|---|---|---|---|---|
| Lamport clock | 1 | 2 | 1 | 2 | 3 | 1 | 4 |
| vector clock | $(1,0,0)$ | $(2,0,0)$ | $(0,1,0)$ | $(1,2,0)$ | $(1,3,0)$ | $(0,0,1)$ | $(1,3,2)$ |

Both rows meet the weak condition on all 11 ordered pairs. The Lamport row fails the strong condition: $2 < 3$ for $b$ and $e$, although $b \parallel e$. The vector row meets the strong condition: $(2,0,0)$ and $(1,3,0)$ are incomparable. Sorting by the pair (Lamport value, process number) gives the total order $a, c, f, b, d, e, g$, which is one of the 52 orders of these events that extend $\to$.

## Known algorithms

| algorithm | condition | timestamp size | what it adds |
|---|---|---|---|
| [Lamport clocks](/lamport-clocks/) | weak | 1 integer | a total order with tie-breakers |
| [Vector clocks](/vector-clocks/) | strong | $n$ integers | concurrency detection |
| [Matrix clocks](/matrix-clocks/) | strong | $n^2$ integers | what every process knows about every process |
| [Plausible clocks](/plausible-clocks/) | weak | a fixed number of integers, chosen in advance | fewer false orders than a scalar in practice; exact with $n$ entries |
| [Hybrid logical clocks](/hybrid-logical-clocks/) | weak | 2 integers | closeness to physical time |

Lamport clocks and vector clocks are proved correct on their pages, and the strong condition for vector clocks is the [vector clock characterization](/vector-clock-characterization/).

## Bounds

- **Weak condition.** One integer per event suffices, and the Lamport value of an event is the length of the longest causal chain that ends at it. So a timestamp needs only about $\log_2$ of the number of events bits.
- **Strong condition.** Charron-Bost proved in 1991 that a vector clock with values in $\mathbb{N}^k$ and the componentwise order needs $k \ge n$ to capture $\to$ in all runs of $n$ processes. The proof builds a run whose order has dimension $n$. It is given on the page of the [clock condition](/lamport-clock-condition/), and cited on the [vector clock characterization](/vector-clock-characterization/).
- **Any scalar is weak only.** A total order on timestamps cannot capture a partial order with concurrent pairs, so no scalar clock meets the strong condition.

## Reductions

- **Total order from the weak condition.** Any timestamps that meet the weak condition, sorted with process ids as tie-breakers, give a total order that extends $\to$. See [total order](/total-order/).
- **Concurrency from the strong condition.** If $T$ meets the strong condition, $a \parallel b$ exactly when $T(a)$ and $T(b)$ are incomparable.
- **Causal delivery from vector timestamps.** [Causal broadcast](/causal-broadcast/) uses vector timestamps on messages to hold back messages whose causes have not been delivered.

## Applications

- **Mutual exclusion.** Lamport's 1978 paper used the total order to grant requests in timestamp order, see [mutual exclusion](/mutual-exclusion-problem/).
- **Conflict resolution.** [Last-writer-wins](/last-writer-wins/) registers order writes by timestamp, and version vectors detect concurrent writes.
- **Snapshots and debugging.** Consistent cuts, [global snapshots](/global-snapshot/) and predicate detection reason about runs through timestamps.
- **Databases.** Multi-version stores read at a timestamp, often a hybrid logical clock.

## References
