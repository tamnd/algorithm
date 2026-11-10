---
tag: 5MWFYB
kind: definition
slug: consistent-cut
name: Consistent cut
aliases:
- consistent global state
- consistent global checkpoint
area: distributed/clocks-and-ordering
level: core
summary: A cut takes a prefix of the events of each process. It is consistent if it is closed under happened-before, that is, it holds no receive without its send. Consistent cuts form a lattice.
prereqs: [happened-before, vector-clocks]
see_also: [global-snapshot, chandy-lamport-snapshot, happened-before, vector-clocks, vector-clock-characterization, space-time-diagram, distributed-predicate-detection, checkpointing]
sources:
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 2 (cuts of a distributed computation, consistent global states) and Chapter 3 (vector time)
  - book: isbn:9780471036005
    title: Vijay K. Garg, Elements of Distributed Computing, Wiley, 2002
    locator: the chapters on global state, consistent cuts and their lattice
  - paper: doi:10.1145/214451.214456
    title: K. Mani Chandy and Leslie Lamport, Distributed snapshots, determining global states of distributed systems, ACM Transactions on Computer Systems 3(1), 1985
    locator: pages 63 to 75 (global states and the states reachable from them; DOI from memory, to be checked)
  - paper: doi:10.1006/jpdc.1993.1075
    title: Friedemann Mattern, Efficient algorithms for distributed snapshots and global virtual time approximation, Journal of Parallel and Distributed Computing 18(4), 1993
    locator: pages 423 to 434 (cuts, consistent cuts and their vector time)
---

A *cut* of a distributed computation takes, for each process, the events up to some point. It is *consistent* if it is closed under [happened-before](/happened-before/): when it holds an event, it holds every event that happened before it. In practice this means that the cut holds no receive event without the matching send. The states of the processes at a consistent cut, with the messages in transit, form a global state that could have existed, and the consistent cuts of a computation form a distributive lattice.

## Definition

**Computation.** There are $n$ processes $p_0, \dots, p_{n-1}$. Process $p_i$ runs the events $e_i^1, e_i^2, \dots$ in order. Events are internal events, sends and receives, and $\to$ is the [happened-before](/happened-before/) relation: the smallest transitive relation that holds when two events are on one process in that order, or when one is the send and the other the receive of the same message.

**Cut.** A cut is a vector $k = (k_0, \dots, k_{n-1})$ of natural numbers, and it stands for the set $C_k = \{ e_i^j : j \le k_i \}$ of the first $k_i$ events of each process. Its *frontier* is the set of last events $e_i^{k_i}$, for each $i$ with $k_i \ge 1$. Cuts are drawn as a line across the [space-time diagram](/space-time-diagram/).

**Consistent cut.** $C$ is consistent if, for all events $e$ and $f$,
$$e \in C \text{ and } f \to e \implies f \in C.$$

**Global state.** The global state of a cut is the local state of each $p_i$ after $e_i^{k_i}$, together with the state of each channel: the messages sent in $C$ and not received in $C$. For a consistent cut no message is received in $C$ and sent outside it, so every received message has a sender, and the state is one that the system could have passed through.

**Lemma 1 (messages are enough).** $C$ is consistent if and only if every receive event in $C$ has its send event in $C$.

*Proof.* If $C$ is consistent, a send happened before its receive, so it is in $C$. For the converse, let $f \to e$ with $e \in C$. There is a chain $f = g_0, g_1, \dots, g_r = e$ in which each step is either the next event on the same process or a send followed by its receive. Go back along the chain from $e$. A step on one process keeps the event in $C$, since $C$ holds a prefix of each process. A step from a receive to its send keeps it in $C$ by the assumption. So $f \in C$. $\square$

**Lemma 2 (exact vector clock test).** Let $VC$ be the [vector clocks](/vector-clocks/) of the computation, so that $VC(e)[i]$ is the number of events of $p_i$ that happened before or are equal to $e$. Then the cut $k$ is consistent if and only if
$$VC(e_j^{k_j})[i] \le k_i \quad \text{for all } i, j \text{ with } k_j \ge 1.$$
Since $VC(e_i^{k_i})[i] = k_i$, the condition says that the componentwise maximum of the frontier clocks is exactly $k$.

*Proof.* By the [vector clock characterization](/vector-clock-characterization/), $e_i^r \to e$ or $e_i^r = e$ holds if and only if $r \le VC(e)[i]$. If $C$ is consistent, the events $e_i^1, \dots, e_i^{VC(e_j^{k_j})[i]}$ happened before or equal the frontier event $e_j^{k_j}$, so they are in $C$, and $VC(e_j^{k_j})[i] \le k_i$. Conversely, let $f = e_i^r \to e$ with $e = e_j^m \in C$, so $m \le k_j$. Then $f \to e_j^{k_j}$ too, since $e_j^m$ is equal to or before $e_j^{k_j}$. So $r \le VC(e_j^{k_j})[i] \le k_i$, and $f \in C$. $\square$

So the test needs only the $n$ frontier clocks: $O(n^2)$ time, with no search over the events.

**Lemma 3 (successor form).** The cut $k$ is consistent if and only if no successor event $e_i^{k_i + 1}$ happened before a frontier event $e_j^{k_j}$.

*Proof.* If some successor $e_i^{k_i+1} \to e_j^{k_j}$, the cut holds $e_j^{k_j}$ but not $e_i^{k_i+1}$, so it is not consistent. Conversely, if the cut is not consistent, some $e_i^r \to e \in C$ with $r > k_i$. Then $e_i^{k_i+1}$ is equal to or before $e_i^r$, and $e$ is equal to or before the frontier event of its process, so $e_i^{k_i+1} \to e_j^{k_j}$. $\square$

**Theorem (lattice).** The consistent cuts of a computation, ordered by inclusion, form a distributive lattice. The join of $C_a$ and $C_b$ is $C_a \cup C_b$, the cut $\max(a, b)$ taken componentwise, and the meet is $C_a \cap C_b$, the cut $\min(a, b)$. The least element is the empty cut and the greatest is the whole computation.

*Proof.* The union of two cuts is the cut of the componentwise maximum, and the intersection is the cut of the componentwise minimum, since each cut is a prefix on each process. Let $e \in C_a \cup C_b$ and $f \to e$; then $e$ is in one of them, which is consistent, so $f$ is in it, and $f \in C_a \cup C_b$. Let $e \in C_a \cap C_b$ and $f \to e$; then $f$ is in both, so in the intersection. So both sets are consistent cuts, and they are the least upper bound and the greatest lower bound under inclusion. Union and intersection of sets distribute over each other, so the lattice is distributive. The empty cut and the full cut are consistent by definition. $\square$

The lattice is the lattice of down-sets of the event order, so by Birkhoff's theorem every finite distributive lattice arises this way. [Predicate detection](/distributed-predicate-detection/) searches this lattice level by level.

## Examples and non-examples

Take three processes. $p_0$ runs an internal event, then sends $m_0$ to $p_1$. $p_1$ receives $m_0$, then sends $m_1$ to $p_2$. $p_2$ runs an internal event, then receives $m_1$. The vector clocks are:

| event | $e^1$ | $e^2$ |
|---|---|---|
| $p_0$ | $(1,0,0)$ | $(2,0,0)$, send $m_0$ |
| $p_1$ | $(2,1,0)$, receive $m_0$ | $(2,2,0)$, send $m_1$ |
| $p_2$ | $(0,0,1)$ | $(2,2,2)$, receive $m_1$ |

- **The cut $(2,1,1)$ is consistent.** The frontier clocks are $(2,0,0)$, $(2,1,0)$ and $(0,0,1)$, and their maximum is $(2,1,1)$, the cut itself. Its global state has empty channels.
- **The cut $(2,0,1)$ is consistent** and has $m_0$ in transit: it is sent in the cut and received outside it.
- **The cut $(1,1,1)$ is not consistent.** It holds the receive of $m_0$ but not its send. The test shows it: $VC(e_1^1)[0] = 2 > 1$.
- **The cut $(2,1,2)$ is not consistent.** It holds the receive of $m_1$ but not its send: $VC(e_2^2)[1] = 2 > 1$.
- **Counting.** Of the $3 \cdot 3 \cdot 3 = 27$ cuts, 11 are consistent. If $k_1 \ge 1$ then $k_0 = 2$, and if $k_2 = 2$ then $k_1 = 2$. So $k_1 = 0$ gives $3 \cdot 2 = 6$ cuts, $k_1 = 1$ gives 2, and $k_1 = 2$ gives 3.
- **Pairwise concurrent frontiers are not needed.** In a computation where $p_0$ sends one message and $p_1$ receives it, the full cut $(1,1)$ is consistent, but its two frontier events are not concurrent: the send happened before the receive. So "the frontier events are pairwise concurrent" is a sufficient test, not a necessary one.

## Related definitions

- **Global snapshot.** A [global snapshot](/global-snapshot/) is the problem of recording the global state of some consistent cut while the computation runs. This page defines what a correct answer is; the snapshot page asks how to get one.
- **Cut versus global state.** A consistent cut fixes a global state, local states plus channel states. The alias *consistent global state* names that state rather than the set of events.
- **Consistent checkpoint.** In [checkpointing](/checkpointing/), a set of local checkpoints, one per process, is consistent if the cut that they define is consistent. Recovery rolls back to such a set.
- **Linear extension.** A run of the system that respects $\to$ passes through a chain of consistent cuts, one event at a time. Every path from the empty cut to the full cut in the lattice is such a run.
- **Happened-before.** A cut is consistent exactly when it is a down-set of the order $\to$ (see [happened-before](/happened-before/)).

## References
