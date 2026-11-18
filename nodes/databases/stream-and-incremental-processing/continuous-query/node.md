---
tag: 56TPJP
kind: definition
slug: continuous-query
name: Continuous query
aliases:
- standing query
area: databases/stream-and-incremental-processing
level: core
summary: A query that is registered once and runs over unbounded input streams, producing new results as data arrives.
prereqs: [relational-algebra, materialized-view]
see_also: [cql-stream-model, dataflow-model, sliding-window-model, incremental-view-maintenance, time-based-window, event-time-watermark, complex-event-processing, streaming-model]
sources:
  - paper: doi:10.1145/130283.130333
    title: Douglas Terry, David Goldberg, David Nichols and Brian Oki, Continuous queries over append-only databases, Proceedings of ACM SIGMOD 1992, pages 321 to 330
    locator: the definition of continuous semantics over an append-only database, the restriction to monotone queries and their incremental evaluation in the Tapestry system
  - paper: "Brian Babcock, Shivnath Babu, Mayur Datar, Rajeev Motwani and Jennifer Widom, Models and issues in data stream systems, Proceedings of the 21st ACM Symposium on Principles of Database Systems (PODS), 2002, pages 1 to 16"
    title: Models and issues in data stream systems
    locator: the section on queries (one-time against continuous queries, predefined against ad hoc queries) and the discussion of unbounded memory, blocking operators and windows
  - paper: doi:10.1007/s00778-004-0147-z
    title: Arvind Arasu, Shivnath Babu and Jennifer Widom, The CQL continuous query language, semantic foundations and query execution, The VLDB Journal 15(2), 2006, pages 121 to 142
    locator: Section 2 (the Tapestry semantics as the union of one-time queries over snapshots) and Section 11.2 (Tapestry queries expressed in CQL)
---

A *continuous query* is a query that a user registers once and that the system then evaluates again and again, or incrementally, while its input keeps growing; its answer at time $t$ depends only on the input that has arrived by time $t$. The page gives the definition and its two common output semantics. The [CQL stream model](/cql-stream-model/) is one precise semantics for continuous queries over streams and relations, built from windows and relation-to-stream operators, and the [Dataflow model](/dataflow-model/) is a programming model for continuous computations over out-of-order data with event time, triggers and accumulation modes. The [sliding window model](/sliding-window-model/) is different again: it is a model of computation for algorithms that summarize the last $W$ items in small memory, and it does not define a query language.

## Definition

**Input.** Fix a discrete, ordered time domain $\mathcal{T} = \{0, 1, 2, \ldots\}$. The input of a continuous query is a set of relations whose contents change only by appends, or, equivalently, a set of unbounded streams of timestamped tuples. Write $I(t)$ for the finite instance that has arrived by time $t$: for each input, the bag of tuples with a timestamp of at most $t$. The input is *append-only*: if $s \le t$, then $I(s) \subseteq I(t)$.

**Query.** A continuous query is a query $Q$ over finite instances, for example a query of the [relational algebra](/relational-algebra/) or of SQL, together with a time $t_0$ at which it is registered. It is not evaluated once. Instead, it defines an answer $A(t)$ for each $t \ge t_0$, and the system must deliver that answer, or the changes to it, as time advances. Babcock et al. (2002) contrast it with a *one-time query*, which is evaluated once on a snapshot and then forgotten, and they separate *predefined* continuous queries, registered before the data arrives, from *ad hoc* ones, registered later.

**Output semantics.** Two semantics are in common use.

- *Snapshot semantics.* $A(t) = Q(I(t))$. The answer at time $t$ is what the query would return if it were run as a one-time query on the input so far. A [materialized view](/materialized-view/) that the system keeps up to date has this semantics, and the [CQL stream model](/cql-stream-model/) uses it at each instant.
- *Cumulative semantics* (Terry et al. 1992). $A_M(t) = \bigcup_{s \le t} Q(I(s))$. The query is run, in concept, at every instant, and the answers of all runs are merged with set union. A tuple that was in the answer once stays in it.

**Monotone queries.** A query $Q$ is *monotone* if $I \subseteq J$ implies $Q(I) \subseteq Q(J)$. Queries of selection, projection, join and union are monotone; queries with set difference, negation or aggregation are in general not.

**Proposition (theorem).** If the input is append-only and $Q$ is monotone, then $A_M(t) = Q(I(t))$ for each $t$, and $A_M(s) \subseteq A_M(t)$ for $s \le t$.

*Proof.* For $s \le t$, append-only input gives $I(s) \subseteq I(t)$, and monotonicity gives $Q(I(s)) \subseteq Q(I(t))$. So each term of the union is a subset of the term for $s = t$, and the union equals that term. The second claim follows because $Q(I(s)) \subseteq Q(I(t))$. $\square$

So for a monotone query the two semantics agree, the answer only grows, and the system can deliver it as a stream of new tuples: at each time, it sends $A(t) \setminus A(t - 1)$. This is why Terry et al. restrict the queries of the Tapestry system to monotone ones and evaluate each query in an incremental form that finds only the new answers since the previous run. For a query that is not monotone, an answer that was delivered can become wrong later, and the output must be able to say so: by sending the full new answer, as an *Rstream* in CQL, or by sending deletions, as a *Dstream* in CQL or a retraction in the [Dataflow model](/dataflow-model/).

**Late data.** The definition assumes that a tuple with timestamp $t$ is known to the system at time $t$. In Tapestry this holds by construction, because the database gives each tuple its timestamp when the tuple is appended. When timestamps come from the source (event time), a tuple can arrive after the system has already given an answer for its time. Such a tuple is *late*. The definition alone says nothing about late data. A system must either wait, with a [watermark](/event-time-watermark/) or [punctuation](/stream-punctuation/) that says when the input up to $t$ is complete, or correct an answer that it delivered. The [Dataflow model](/dataflow-model/) makes this choice explicit.

## Examples and non-examples

**A monotone continuous query.** Sensors send readings (time, sensor, temperature): (1, s1, 28), (2, s2, 31), (3, s1, 33), (4, s3, 29), (5, s2, 35). The query $Q$ selects the readings with a temperature above 30.

| $t$ | $Q(I(t))$ | new tuples sent at $t$ |
|---|---|---|
| 1 | empty | none |
| 2 | (2, s2, 31) | (2, s2, 31) |
| 3 | (2, s2, 31), (3, s1, 33) | (3, s1, 33) |
| 4 | (2, s2, 31), (3, s1, 33) | none |
| 5 | (2, s2, 31), (3, s1, 33), (5, s2, 35) | (5, s2, 35) |

At each time, the cumulative answer $A_M(t)$ equals $Q(I(t))$, as the proposition says, and the output is an append-only stream.

**A query that is not monotone.** On the same input, $Q'$ returns the sensor with the highest reading so far. The snapshot answers are s1, s2, s1, s1 and s2 at times 1 to 5. The cumulative answer is {s1} at time 1 and {s1, s2} from time 2 on, so under the cumulative semantics the query returns every sensor that was ever the maximum. Under the snapshot semantics the answer at time 3 replaces s2 with s1, and an output stream must retract s2. The two semantics give different results.

**An aggregate.** $Q''$ counts the readings. The snapshot answers are 1, 2, 3, 4 and 5. The count of 1 is wrong from time 2 on, so the output cannot be a stream of appends of final results. This is the reason that stream systems put aggregates over [time-based windows](/time-based-window/) or [count-based windows](/count-based-window/): an aggregate over a window that has closed can be delivered once and then never changes.

**Non-examples.**

- A one-time SQL query on a snapshot of the database. It runs once, and later appends do not change its delivered answer.
- A query rerun by hand each night on a full copy of the data, if the user takes only the last result. Each run is a one-time query; nothing defines a relation between the runs.
- A [sliding window](/sliding-window-model/) algorithm that keeps an estimate of a count over the last $W$ items. It answers a fixed function of the last $W$ items with bounded memory, which is a computational model, not a query language. A continuous query with a window can use such an algorithm as an operator.

## Related definitions

- [CQL stream model](/cql-stream-model/): streams and time-varying relations, with window operators from streams to relations and the operators Istream, Dstream and Rstream from relations to streams. It gives snapshot semantics at each instant and can express the Tapestry semantics (Arasu, Babu and Widom 2006, Section 11.2).
- [Dataflow model](/dataflow-model/): windows in event time, triggers in processing time, and the accumulation modes that relate the successive answers for one window.
- [Materialized view](/materialized-view/) and [incremental view maintenance](/incremental-view-maintenance/): a view kept up to date under inserts and deletes, which is a continuous query with snapshot semantics over a database that can also delete.
- [Event-time watermark](/event-time-watermark/) and [stream punctuation](/stream-punctuation/): the signals that tell a continuous query that its input up to a time is complete.
- [Complex event processing](/complex-event-processing/): continuous queries whose answers are patterns of events in order, not relations.
- [Streaming model](/streaming-model/) and [sliding window model](/sliding-window-model/): the models of computation for one pass over a stream with small memory.

## References
