---
tag: A6CJ2B
kind: algorithm
slug: weak-conjunctive-predicate-detection
name: Weak conjunctive predicate detection
aliases:
- Garg-Waldecker algorithm
area: distributed/clocks-and-ordering
level: research
summary: A checker gets the vector clocks of the states where each local predicate holds, one queue per process, and drops a head that happened before another head. The heads left form the first cut.
solves: [distributed-predicate-detection]
model: asynchronous-model
complexity:
  vars: {n: the number of processes, m: the largest number of candidate states of one process}
  time: {worst: O(n^2 m)}
  space: {extra: O(n^2 m)}
  messages: {worst: O(n m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1994
  people: [Vijay K. Garg, Brian Waldecker]
  note: Garg and Waldecker published the checker for weak conjunctive predicates in IEEE Transactions on Parallel and Distributed Systems in 1994.
prereqs: [distributed-predicate-detection, vector-clocks]
see_also: [distributed-predicate-detection, consistent-cut, vector-clocks, vector-clock-characterization, global-snapshot, happened-before]
sources:
  - paper: "Vijay K. Garg and Brian Waldecker, Detection of weak unstable predicates in distributed programs, IEEE Transactions on Parallel and Distributed Systems 5(3), 1994, pages 299 to 307"
    locator: the checker process with one queue of vector clocks per process, its proof and its O(n^2 m) bound (volume and pages from memory, to be checked)
  - book: isbn:9780471036005
    title: Vijay K. Garg, Elements of Distributed Computing, Wiley, 2002
    locator: the chapter on global predicate detection (conjunctive predicates, the centralized checker)
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: the chapter on global predicate detection (conjunctive predicates, possibly and definitely)
---

*Weak conjunctive predicate detection* decides whether a conjunction $l_0 \wedge l_1 \wedge \dots \wedge l_{n-1}$ of local predicates, $l_i$ on the state of process $p_i$ only, was *possibly* true: whether some [consistent cut](/consistent-cut/) has every $l_i$ true at once. Each process sends the [vector clock](/vector-clocks/) of each state in which its predicate holds to a checker. The checker keeps one queue per process and drops a queue head when another head shows that it happened before. Garg and Waldecker (1994) showed that the heads that are left form the first such cut, after $O(n^2 m)$ comparisons. For a general predicate the same question is NP-complete (see [distributed predicate detection](/distributed-predicate-detection/)).

## In plain words

Each process writes down the moments when its own condition was true, with a vector clock for each. You want one moment from each process such that all the moments could have happened together. Two moments cannot be together if one process had already left its moment before the other process reached its own, and the vector clocks show exactly this.

Put the moments of each process in a queue, oldest first. Look at the heads of two queues. If the head of process $j$ already knows that process $i$ moved past its head, then the head of $i$ is useless: it cannot go with this head of $j$, and the later moments of $j$ know even more. So throw it away and look at the next moment of $i$. When no head can be thrown away, the heads fit together, and they are the earliest moments that do.

## The problem

**Model.** $n$ processes in the [asynchronous model](/asynchronous-model/), with [vector clocks](/vector-clocks/). Process $p_i$ passes through the states $s_i^0, s_i^1, \dots$, where $s_i^a$ is its state after its first $a$ events. The vector clock of a state is $V(s_i^a) = VC(e_i^a)$, and the zero vector for $a = 0$, so $V(s_i^a)[i] = a$.

**Goal.** Decide whether there are states $s_0^{a_0}, \dots, s_{n-1}^{a_{n-1}}$ with $l_i(s_i^{a_i})$ true for each $i$ whose cut $(a_0, \dots, a_{n-1})$ is consistent. If so, return the least such cut. By the vector clock test on the page on [consistent cuts](/consistent-cut/), the cut is consistent if and only if
$$V(s_j^{a_j})[i] \le a_i \quad \text{for all } i \ne j.$$
The test is pairwise. We call two states $s_i^{a}$ and $t$ of $p_j$ *compatible* if $V(t)[i] \le a$ and $V(s_i^a)[j] \le V(t)[j]$.

## The algorithm

Each process $p_i$ sends $V(s)$ to the checker for each state $s$ in which $l_i$ holds, in order, over a FIFO channel. The checker keeps the queue $Q_i$ of these vectors and runs:

```pseudo id=main
DETECT(Q_0, …, Q_{n−1})
L1  todo ← {0, …, n − 1}
    while todo is not empty
        take i from todo
        for each j ≠ i
L2          if head(Q_j)[i] > head(Q_i)[i] then           ▷ the head of j knows that p_i left its head
L3              remove head(Q_i); put i in todo
L4              if Q_i is empty then return none
                stop this loop and take the next i
L5          if head(Q_i)[j] > head(Q_j)[j] then           ▷ the same test the other way
                remove head(Q_j); put j in todo; if Q_j is empty then return none
L6  return the cut (head(Q_0)[0], …, head(Q_{n−1})[n−1])
```

A process is put in `todo` only if it is not there already. Online, the checker waits for more vectors when a queue is empty, instead of returning none; the version here runs on a finished trace.

## Example

$p_0$ sends $m_0$ to $p_1$ and then runs an internal event. $p_1$ receives $m_0$ and sends $m_1$ to $p_2$. $p_2$ runs an internal event and then receives $m_1$. The state clocks are:

| state | $s^0$ | $s^1$ | $s^2$ |
|---|---|---|---|
| $p_0$ | $(0,0,0)$, $l_0$ true | $(1,0,0)$ | $(2,0,0)$, $l_0$ true |
| $p_1$ | $(0,0,0)$ | $(1,1,0)$, $l_1$ true | $(1,2,0)$ |
| $p_2$ | $(0,0,0)$, $l_2$ true | $(0,0,1)$ | $(1,2,2)$, $l_2$ true |

So $Q_0 = [(0,0,0), (2,0,0)]$, $Q_1 = [(1,1,0)]$ and $Q_2 = [(0,0,0), (1,2,2)]$.

1. $i = 0$, $j = 1$: $\mathrm{head}(Q_1)[0] = 1 > 0 = \mathrm{head}(Q_0)[0]$, so line L3 drops $(0,0,0)$ from $Q_0$. The state of $p_1$ has seen the send of $m_0$, which ends $s_0^0$.
2. $i = 1$: the heads are $(2,0,0)$, $(1,1,0)$ and $(0,0,0)$. No test of lines L2 and L5 fires.
3. $i = 2$, then $i = 0$ again: no test fires, and `todo` is empty.

Line L6 returns the cut $(2, 1, 0)$: $p_0$ after both its events, $p_1$ after the receive, $p_2$ at the start. It is the only consistent cut with all three predicates true. The checker made 13 comparisons.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). A *solution* is a choice of one queued state per process whose cut is consistent.

- **A dropped head is in no solution.** If $\mathrm{head}(Q_j)[i] > \mathrm{head}(Q_i)[i] = a$, then the head of $j$ and every later state of $p_j$ has seen event $e_i^{a+1}$, since vector clocks never decrease along a process. So no state of $p_j$ that a solution can still use is compatible with $s_i^a$.
- **So every solution is at or after the heads**, on every process, and line L4 is right to answer none.
- **At line L6 the heads are pairwise compatible.** A process leaves `todo` only after its head was tested against every other head, and any change of a head puts that process back in `todo`. So the heads form a solution, and by the point before it is the least one.

The seeded tests compare the checker with an enumeration of all choices on 400 random traces of 2 to 4 processes. They check that it finds a cut exactly when one exists, that its cut is the least one, and the bound on comparisons below.

## Complexity

Let $m$ be the largest number of vectors in one queue. Each time the checker takes $i$ from `todo`, it makes at most $2(n-1)$ comparisons. Process $i$ goes back into `todo` only when its head is dropped, and a drop that empties the queue ends the run, so $i$ is taken at most $m$ times. That gives at most $2n(n-1)m$ comparisons, $O(n^2 m)$ time. The queues hold at most $nm$ vectors of $n$ integers, and each process sends at most $m$ messages to the checker.

## Properties

- **Exact for conjunctions.** It decides possibly for $l_0 \wedge \dots \wedge l_{n-1}$ with no search of the lattice of cuts, which can have exponential size.
- **Finds the first cut.** The cut it returns is the least one, so it reports the earliest consistent moment at which the conjunction held.
- **Online.** The checker can run while the computation runs and stop as soon as it finds a cut.
- **Central.** One checker receives all the vectors and does all the work.

## Variants and improvements

- **Fewer vectors.** Between two communication events of $p_i$, the states of $p_i$ have the same clock except for entry $i$, and another state's entry $i$ always names a send of $p_i$. So these states are compatible with exactly the same states of other processes, and $p_i$ needs to send only the first state in each such interval in which $l_i$ holds.
- **Definitely.** For conjunctive predicates, definitely, also called a strong conjunctive predicate, also has a polynomial checker, which looks for intervals of true states that overlap in every run.
- **General predicates.** Without the conjunctive form, the problem is NP-complete, and only the search of the lattice in [distributed predicate detection](/distributed-predicate-detection/) is exact.

## When to use it

Use it to find violations of a property of the form "all of these hold at once": two processes in a critical section, two nodes that each think they lead, all workers idle while work is queued. Write the bad state as a conjunction of local conditions and run the checker on the vector clocks in a trace or online.

## Pitfalls

- **Missing the zero state.** The state before the first event has the clock $(0, \dots, 0)$. If $l_i$ holds at the start, that state must be sent too.
- **Clocks of events and of states.** The state after event $e$ has the clock of $e$. Using the clock of the next event shifts every comparison by one.
- **Not a test of definitely.** A cut returned by the checker says that the conjunction could have held. It does not say that it held in the order that really happened, nor in every order.
- **Order of the queues.** Each $Q_i$ must be in the order of the states of $p_i$, so the channel to the checker must be FIFO.

## Implementations

## History

Robert Cooper and Keith Marzullo defined possibly and definitely in 1991 and detected them by a search of the lattice of consistent cuts. Vijay K. Garg and Brian Waldecker gave the checker for weak conjunctive predicates, with one queue per process and $O(n^2 m)$ comparisons, in IEEE Transactions on Parallel and Distributed Systems in 1994. Later work, such as that of Chase and Garg (1998), extended the fast cases to larger classes of predicates.

## References
