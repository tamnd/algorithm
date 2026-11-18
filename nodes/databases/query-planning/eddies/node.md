---
tag: CC4NGE
kind: algorithm
slug: eddies
name: Eddies
aliases:
- eddy operator
- adaptive tuple routing
area: databases/query-planning
level: research
summary: "An eddy sends each tuple through the filters and joins of a query in an order it chooses per tuple, from what it sees at run time. With timestamped SteMs, every order gives the same result."
solves: [relational-join]
model: word-ram
complexity:
  vars: {T: the number of base and intermediate tuples built, m: the number of operators}
  time: {expected: "O(T m^2)"}
  space: {extra: "O(T)"}
properties: {deterministic: false, randomized: true, exact: true, greedy: false, recursive: false}
history:
  year: 2000
  people: [Ron Avnur, Joseph M. Hellerstein]
  note: Given at SIGMOD 2000 for the Telegraph project at Berkeley, as a query operator that reorders a plan for each tuple.
prereqs: [iterator-model, symmetric-hash-join, query-optimization]
see_also: [mid-query-reoptimization, ripple-join, xjoin, lottery-scheduling, multi-armed-bandit, continuous-query, pipelining-and-materialization, join-ordering]
sources:
  - paper: "Ron Avnur and Joseph M. Hellerstein, Eddies: continuously adaptive query processing, Proceedings of ACM SIGMOD 2000, 261 to 272"
    title: "Eddies: continuously adaptive query processing"
    locator: the eddy operator, moments of symmetry, the done and ready bits of a tuple, and routing by lottery scheduling
  - paper: "Vijayshankar Raman, Amol Deshpande and Joseph M. Hellerstein, Using state modules for adaptive query processing, Proceedings of ICDE 2003"
    title: Using state modules for adaptive query processing
    locator: SteMs, which let the eddy choose the join order for each tuple, and the timestamp rule against duplicate results
---

An eddy is a query operator that decides, for each tuple, which operator of the query it visits next. Ron Avnur and Joseph M. Hellerstein gave it in 2000. A classic optimizer fixes one plan before the query starts, from estimates that can be wrong, and the plan stays fixed while data and costs change. An eddy sits between the operators of the query. Each operator returns its output to the eddy, and the eddy routes each tuple to an operator it has not yet visited. The routing policy can learn from what it sees, for example by sending tuples first to the filters that drop the most tuples. With state modules (SteMs) and timestamps, the result is the same for every routing choice and every arrival order, so the policy affects only the cost.

## In plain words

Think of a mail room. Each letter must visit several desks, and the order of the desks does not change the letter at the end. But some desks throw away many letters, and some desks are slow. A clerk in the middle hands each letter to the next desk it still needs.

The clerk watches the desks. A desk that throws away many letters saves work for the desks after it, so the clerk sends letters there first. When a desk changes, the clerk changes the order for the next letters. No plan is fixed in advance.

For joins, each table keeps the rows it has seen in a store. A new row looks for partners in the stores of the other tables, in the order the clerk picks. A simple rule on arrival times makes sure that each answer comes out once.

## The problem

The input is a query with joins of relations $R_1, \ldots, R_n$ and filters on single relations, and the tuples of the relations arrive over time, in any interleaving, at rates the system does not know in advance. The output is the join result, the same bag of rows as any static plan gives. The goal is to keep the work small (the number of operator calls and of intermediate results) when selectivities and costs are not known, or change while the query runs. A static plan can be bad for this input, and [mid-query re-optimization](/mid-query-reoptimization/) can change the plan only at a few points.

## The algorithm

Each base tuple, on arrival, gets a timestamp and is built into the SteM of its relation: a hash table of the tuples of that relation seen so far. Then a tuple in the eddy carries the set $P$ of base tuples joined so far, the set $D$ of filters it has passed, and the timestamp $\tau$ of the arrival that started it. The paper keeps this state as bit vectors in the tuple. An operator is eligible for a tuple if it is a filter on a relation of $P$ that is not in $D$, or the SteM of a relation not in $P$ that shares an attribute with $P$.

```pseudo id=main
EDDY(arriving base tuples, filters, one SteM per relation, routing policy π)
L1  while base tuples arrive or tuples wait in the eddy do
L2      on the arrival of base tuple b of R_j: ts(b) ← the next timestamp; build b into SteM_j
L3          put (P = {b}, D = ∅, τ = ts(b)) into the eddy
L4      otherwise take a waiting tuple t = (P, D, τ)
L5          E ← the operators that are eligible for t
L6          if E is empty then output P (it joins every relation and passed every filter)
L7          else o ← π(E)
L8              if o is a filter: if t passes, put (P, D ∪ {o}, τ) back; else drop t
L9              if o is SteM_k: for each s in SteM_k with ts(s) < τ that joins with P, put (P ∪ {s}, D, τ) back
```

The lottery policy of the paper is in line L7. Each operator has tickets. An operator gets a ticket when the eddy gives it a tuple and loses a ticket for each tuple it returns, and the eddy picks among the eligible operators with probability proportional to their tickets. A filter that drops most of its input keeps most of its tickets, so it is picked more often. The paper adds a window to the ticket counts so that the policy forgets old behavior.

## Example

Take $R(a, b)$ with $r_1 = (1, 7)$ and $r_2 = (2, 8)$, and $S(b, c)$ with $s_1 = (7, 3)$ and $s_2 = (7, 4)$. They arrive in the order $r_1, s_1, r_2, s_2$, with timestamps 0 to 3, and each tuple is routed before the next one arrives.

| step | event | result |
|---|---|---|
| 1 | $r_1$ arrives, is built into SteM(R), and probes SteM(S) | SteM(S) is empty, nothing |
| 2 | $s_1$ arrives and probes SteM(R) for $b = 7$ | finds $r_1$ (timestamp 0 < 1), outputs $(r_1, s_1)$ |
| 3 | $r_2$ arrives and probes SteM(S) for $b = 8$ | no match |
| 4 | $s_2$ arrives and probes SteM(R) for $b = 7$ | finds $r_1$, outputs $(r_1, s_2)$ |

Now let all four tuples arrive before any of them is routed, which can happen in a pipelined system. When the tuple of $r_1$ probes SteM(S), it sees $s_1$ and $s_2$, but both have later timestamps, so the probe returns nothing. The two results come from the probes of $s_1$ and $s_2$ as before. Without the timestamp test, $r_1$ would also find both and every result would come out twice. The code tests both cases.

For filters, take one relation with two filters: one passes 90 percent of the tuples, the other 10 percent, and both cost the same. The order "10 percent first" makes about $1 + 0.1 = 1.1$ filter calls per tuple, and the other order about $1.9$. On 3000 tuples, the lottery policy in the code makes 3318 calls, close to the 3288 of the better fixed order and far from the 5710 of the worse one. This is a measurement on one input, not a bound.

## Correctness

The proof file proves that for every arrival order, every interleaving of arrivals with routing, and every routing policy, the eddy outputs each row of the filtered join exactly once. The invariant is that a tuple in the eddy is a consistent partial join row that passed the filters in $D$, and that all its base tuples except the one that started it have smaller timestamps. If no operator is eligible, the tuple covers every relation (the join graph is connected) and passed every filter, so it is a result. A result $\gamma$ is built from the routing of its base tuple with the largest timestamp, because every other tuple of $\gamma$ is in its SteM by then, and each probe returns it. It is built only there, because a routing started by an earlier tuple of $\gamma$ cannot see the later one. The routing choices form a tree, so $\gamma$ is built once in that routing.

## Complexity

Let $T$ be the number of tuples the eddy builds (base tuples, tuples after each filter, and partial join results) and $m$ the number of operators. Each built tuple is routed once, and finding the eligible operators costs $O(m)$ attribute checks, so the routing costs $O(T m^2)$ in the worst case of this simple code; a real eddy keeps bit vectors and makes this $O(m)$ word operations per routing. A probe of a SteM is a hash lookup, $O(1)$ expected plus the matches. The SteMs keep every base tuple, and the eddy keeps the waiting tuples, so the space is $O(T)$. $T$ depends on the routing: a good policy keeps the number of intermediate results small, as a good static plan does. The routing decision for each tuple is the overhead of an eddy against a fixed plan, and the paper measures it as small in its prototype.

## Properties

- **Correct for every policy, proved.** The output bag does not depend on the routing policy or on the arrival order.
- **Adaptive per tuple.** Two tuples of the same relation can take different orders. The order can change at any time, not only at points fixed in advance.
- **Heuristic routing.** The lottery policy has no proved bound on its work. Its benefit is measured.
- **Pipelined.** Results come out while the input arrives, as with a [symmetric hash join](/symmetric-hash-join/), which suits streams and remote sources.
- **Memory heavy.** SteMs keep every base tuple, so the memory is that of a symmetric hash join on every relation.

## Variants and improvements

- **Binary join operators.** The original eddy routed tuples among fixed pipelined join operators, such as ripple joins and index joins, and could reorder only at moments of symmetry, when a join can take input from either side. SteMs (Raman, Deshpande and Hellerstein, 2003) split each join into its two hash tables, so the eddy also chooses the join order and the access method for each tuple.
- **Back-pressure.** The paper first routes by the queue lengths of the operators, so that fast operators get more tuples, and then adds lottery tickets to learn selectivity.
- **Continuous queries.** Eddies were used in the Telegraph project for [continuous queries](/continuous-query/) over streams, where many queries share one eddy and one set of SteMs.
- **Routing as learning.** Choosing the next operator for many tuples is close to a [multi-armed bandit](/multi-armed-bandit/) problem, and later work used ideas from learning for the routing policy.
- **Plan switching.** [Mid-query re-optimization](/mid-query-reoptimization/) changes the plan a few times at checkpoints; eddies go to the other end and decide for every tuple.

## When to use it

Use an eddy when the inputs are streams or remote sources with unknown and changing rates and selectivities, when statistics are missing, or when a query runs long enough for the data to change. For short queries over local tables with good statistics, a static plan from a cost-based optimizer is usually cheaper, because it pays no routing cost per tuple and it can use blocking operators such as sort and hash join builds.

## Pitfalls

- **Duplicate results.** If tuples of earlier arrivals can still probe after later tuples are built, some results are found twice. The timestamp test of line L9, or an equivalent rule, is required.
- **Forgetting filters of joined tuples.** A tuple from a SteM joins a partial result before its own filters have run. The eddy must route the new tuple through those filters too, or it outputs rows that fail them.
- **Cross products.** If the policy probes a SteM that shares no attribute with the tuple, it builds a cross product. Allow only connected probes when the join graph is connected.
- **Slow adaptation.** Ticket counts that are never aged keep a policy on an old order after the data changes.
- **Routing overhead.** A routing decision per tuple costs more than a fixed pipeline, so for cheap filters the overhead can be larger than the saving.

## Implementations

## History

Adaptive query processing grew from the observation that static plans fail when estimates are wrong or when data comes from slow or changing sources. Query scrambling and mid-query re-optimization changed plans at a few points. Ron Avnur and Joseph M. Hellerstein proposed the eddy in 2000 in the Telegraph project at Berkeley, which went to the other end and made the order a decision for each tuple, with a lottery policy borrowed from operating system scheduling. Raman, Deshpande and Hellerstein added SteMs in 2003, which let the eddy also choose join orders and access methods, and later Telegraph work used eddies for shared continuous queries over streams.

## References
