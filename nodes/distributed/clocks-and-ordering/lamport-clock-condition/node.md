---
tag: JFSZ4G
kind: definition
slug: lamport-clock-condition
name: Lamport's clock condition
aliases:
- clock condition
area: distributed/clocks-and-ordering
level: core
summary: A logical clock C satisfies the clock condition if a happened before b implies C(a) < C(b). The converse needs vectors of n entries, by a result of Charron-Bost.
prereqs: [happened-before]
see_also: [lamport-clocks, happened-before, vector-clock-characterization, vector-clocks, total-order, event-ordering, hybrid-logical-clocks, plausible-clocks]
sources:
  - paper: doi:10.1145/359545.359563
    title: Leslie Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7), 1978
    locator: pages 558 to 565, section Logical Clocks (the Clock Condition, conditions C1 and C2) and section Physical Clocks (the Strong Clock Condition)
  - paper: doi:10.1016/0020-0190(91)90055-M
    title: Bernadette Charron-Bost, Concerning the size of logical clocks in distributed systems, Information Processing Letters 39(1), 1991
    locator: the main theorem, that a vector clock that characterizes causality needs n entries
  - paper: doi:10.1109/2.485846
    title: Michel Raynal and Mukesh Singhal, Logical time, capturing causality in distributed systems, IEEE Computer 29(2), 1996
    locator: the consistency and strong consistency properties of logical clocks
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 3 (consistency and strong consistency of logical clocks, Sections 3.2 to 3.4)
---

Lamport's clock condition is the minimum that a logical clock must satisfy: if event $a$ [happened before](/happened-before/) event $b$, then the clock value of $a$ is smaller than that of $b$. Lamport stated it in 1978 and showed that two local rules give it. The condition goes one way only. A clock that also satisfies the converse captures causality exactly, and Charron-Bost proved in 1991 that such a clock, if it is a vector with the componentwise order, needs one entry per process. This page proves that bound.

## Definition

**Clocks.** Fix a run with $n$ processes and its happened-before relation $\to$. A *logical clock* assigns to each event $e$ a value $C(e)$ in a set with a strict partial order $<$, usually the integers or vectors of integers.

**Clock Condition (Lamport 1978).** For all events $a$ and $b$: if $a \to b$, then $C(a) < C(b)$.

Lamport split it into two local conditions:

- **C1.** If $a$ and $b$ are events of the same process and $a$ comes before $b$, then $C(a) < C(b)$.
- **C2.** If $a$ is the send of a message and $b$ is its receipt, then $C(a) < C(b)$.

**Proposition 1.** A clock satisfies the Clock Condition if and only if it satisfies C1 and C2.

*Proof.* The pairs of C1 and C2 are in $\to$, so the Clock Condition implies them. Conversely, $\to$ is the transitive closure of these pairs, and $<$ is transitive, so C1 and C2 give $C(a) < C(b)$ along every chain. $\square$

**Names for the two directions.** Raynal and Singhal call a clock *consistent* if it meets the Clock Condition, and *strongly consistent* if also $C(a) < C(b)$ implies $a \to b$. This differs from Lamport's own *Strong Clock Condition*, which appears in the section on physical clocks of his paper. There the relation is extended by causality outside the system, such as a telephone call, and the condition is still one-way: if $a$ precedes $b$ in the extended relation, then $C(a) < C(b)$.

**Proposition 2.** Suppose a run has events $a \to c$ and an event $b$ that is [concurrent](/concurrent-events/) with both. Then no clock with values in a total order is strongly consistent.

*Proof.* A strongly consistent clock cannot have $C(b) < C(a)$ or $C(a) < C(b)$, since either would claim an order between concurrent events. In a total order this leaves $C(a) = C(b)$, and in the same way $C(b) = C(c)$. Then $C(a) = C(c)$, but the Clock Condition requires $C(a) < C(c)$. $\square$

The running example has such a triple: $a \to b$ on $P_1$, and $f$ is concurrent with both.

**Theorem (Charron-Bost 1991).** Let $n \ge 2$. There is a run of $n$ processes such that every map $V$ from its events to $\mathbb{R}^k$ with
$$a \to b \iff V(a) < V(b)$$
(componentwise $\le$, and not equal) has $k \ge n$.

*Proof.* Number the processes $p_0, \ldots, p_{n-1}$ and read indices modulo $n$. Each process $p_j$ does, in this order:

1. a local event $x_j$;
2. a send to every $p_k$ with $k \notin \{j, j+1\}$;
3. the receipt of every message sent to it;
4. a local event $y_{j-1}$.

All sends happen before all receipts, so a message carries only the knowledge of $x_j$. The process $p_j$ receives from every $p_k$ with $j \notin \{k, k+1\}$, that is, with $k \notin \{j, j-1\}$. So the causal past of $y_{j-1}$ contains $x_j$ and the $x_k$ with $k \ne j-1$, and nothing else among the $x$ events. Renaming $m = j - 1$:
$$x_i \to y_m \iff i \ne m.$$
The events $x_0, \ldots, x_{n-1}$ are pairwise [concurrent](/concurrent-events/), because each is the first event of its process.

Suppose $V$ captures $\to$ as stated. Fix $i$. Since $x_i \not\to y_i$, we have $V(x_i) \not< V(y_i)$. If $V(x_i) \le V(y_i)$ componentwise, then $V(x_i) = V(y_i)$. Take $j \ne i$, which exists since $n \ge 2$. Then $x_j \to y_i$ gives $V(x_j) < V(y_i) = V(x_i)$, so $x_j \to x_i$, which is false. Hence there is a coordinate $c(i)$ with
$$V(x_i)[c(i)] > V(y_i)[c(i)].$$
If $k < n$, two indices $i \ne j$ have the same coordinate $c = c(i) = c(j)$. Using $x_j \to y_i$ and $x_i \to y_j$:
$$V(x_i)[c] > V(y_i)[c] \ge V(x_j)[c] > V(y_j)[c] \ge V(x_i)[c],$$
a contradiction. So $k \ge n$. $\blacksquare$

A script that builds this run and computes vector clocks confirms $x_i \to y_m \iff i \ne m$ for $n = 2$ to $7$. The events $x_i$ and $y_i$ form what order theory calls the standard example of dimension $n$. [Vector clocks](/vector-clocks/) have exactly $n$ entries and are strongly consistent, so the bound is tight. The [vector clock characterization](/vector-clock-characterization/) proves the matching upper bound.

## Examples and non-examples

The running example: $P_1$ has $a$ (send to $P_2$) and $b$; $P_2$ has $c$, $d$ (receive from $a$) and $e$ (send to $P_3$); $P_3$ has $f$ and $g$ (receive from $e$).

**Examples.**

- [Lamport clocks](/lamport-clocks/) give $a = 1$, $b = 2$, $c = 1$, $d = 2$, $e = 3$, $f = 1$, $g = 4$. All 11 ordered pairs get increasing values, so the clock is consistent. It is not strongly consistent: $2 < 3$ for $b$ and $e$, but $b \parallel e$.
- Vector clocks give $b = (2,0,0)$ and $e = (1,3,0)$, which are incomparable, and they are strongly consistent on all 21 pairs.
- [Hybrid logical clocks](/hybrid-logical-clocks/) meet the Clock Condition with the lexicographic order on pairs $(l, c)$.

**Non-examples.**

- **Counting only local events.** If each process counts its own events and ignores messages, then $a = 1$, $b = 2$, $c = 1$, $d = 2$, $e = 3$, $f = 1$, $g = 2$. C1 holds, but C2 fails for the message from $e$ to $g$: $3 > 2$.
- **Physical timestamps.** If the clock of $P_3$ runs 5 time units behind that of $P_2$, a message sent when $P_2$ reads $10$ and received one time unit later gets the receive stamp $6$ at $P_3$. C2 fails, since $10 > 6$.
- **Equal values.** A clock with $C(a) = C(b)$ for $a \to b$ fails the condition, which is strict. The tie-break by process id in a [total order](/total-order/) applies only to events with no order between them.

## Related definitions

- **[Happened-before](/happened-before/).** The relation that the condition refers to.
- **[Vector clock characterization](/vector-clock-characterization/).** The theorem that vector clocks are strongly consistent, with $a \to b$ if and only if $V(a) < V(b)$.
- **[Total order](/total-order/).** A consistent clock plus a tie-break gives a total order that extends $\to$.
- **[Plausible clocks](/plausible-clocks/).** Clocks of fixed size that keep the Clock Condition and give up some of the converse.
- **[Event ordering](/event-ordering/).** The problem of computing clocks with these conditions online.

## References
