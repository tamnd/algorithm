---
tag: MST56H
kind: model
slug: cql-stream-model
name: CQL stream-relation model
aliases:
- Continuous Query Language
- stream-to-relation operators
area: databases/stream-and-incremental-processing
level: advanced
summary: Define stream queries by window operators that turn streams into relations, relational operators, and operators that turn relations back into streams.
prereqs: [continuous-query, relational-algebra, time-based-window]
see_also: [dataflow-model, sliding-window-model, count-based-window, tumbling-window, materialized-view, incremental-view-maintenance, event-time-watermark, stream-punctuation]
sources:
  - paper: doi:10.1007/s00778-004-0147-z
    title: Arvind Arasu, Shivnath Babu and Jennifer Widom, The CQL continuous query language, semantic foundations and query execution, The VLDB Journal 15(2), 2006, pages 121 to 142
    locator: "Section 4 (streams and relations, Definitions 1 and 2), Section 5 (the abstract semantics, Definition 3), Section 6 (the window operators of 6.1 and Istream, Dstream and Rstream of 6.3), Section 8 (heartbeats), Section 10 (window reduction and filter-window commutativity), Section 11 (comparison with Tapestry, Tribeca, GSQL and chronicles, and the stream-only language of 11.6) and Section 12 (the STREAM implementation)"
  - paper: "Brian Babcock, Shivnath Babu, Mayur Datar, Rajeev Motwani and Jennifer Widom, Models and issues in data stream systems, Proceedings of the 21st ACM Symposium on Principles of Database Systems (PODS), 2002, pages 1 to 16"
    title: Models and issues in data stream systems
    locator: the discussion of windows, blocking operators and the memory needs of continuous queries
  - paper: doi:10.1145/130283.130333
    title: Douglas Terry, David Goldberg, David Nichols and Brian Oki, Continuous queries over append-only databases, Proceedings of ACM SIGMOD 1992, pages 321 to 330
    locator: the Tapestry semantics that CQL generalizes
---

The CQL stream model, of Arasu, Babu and Widom (2006), gives a precise meaning to a [continuous query](/continuous-query/) over streams and relations that change with time: window operators turn a stream into a relation, ordinary relational operators act on the relation at each instant, and the operators Istream, Dstream and Rstream turn a relation back into a stream. A continuous query is the general notion of a query whose answer follows a growing input; CQL is one semantics for it, with snapshot answers at each instant of a single ordered time domain. The [Dataflow model](/dataflow-model/) differs: it separates event time from processing time, lets input arrive out of order, and makes the time and the form of each output a choice of the user. CQL also differs from the [sliding window model](/sliding-window-model/), which is a model of computation for small-memory algorithms over the last $W$ items and not a query language.

## The machine

**Time domain.** Time is a discrete, ordered domain $\mathcal{T} = \{0, 1, 2, \ldots\}$. A time instant is an element $\tau$ of $\mathcal{T}$. The domain models the time of the application, not the wall clock of the system, and the semantics needs only a discrete, ordered domain (Section 4).

**Streams.** A stream $S$ is a possibly infinite bag of elements $\langle s, \tau \rangle$, where $s$ is a tuple of the schema of $S$ and $\tau \in \mathcal{T}$ is its timestamp. For each $\tau$, only finitely many elements have timestamp $\tau$ (Definition 1). A base stream is an input; a derived stream is the output of an operator.

**Relations.** A relation $R$ is a map from $\mathcal{T}$ to finite bags of tuples of its schema. $R(\tau)$ is the *instantaneous relation* of $R$ at $\tau$ (Definition 2). A stored table that is updated now and then is a relation in this sense: its value at $\tau$ is its content after the updates up to $\tau$.

**Operators.** There are three classes, and no direct operator from streams to streams.

1. *Stream-to-relation* operators are windows. Each one maps a stream $S$ to a relation $R$.
   - $S\,[\text{Range } T]$, a [time-based window](/time-based-window/): $R(\tau) = \{ s \mid \langle s, \tau' \rangle \in S,\ \max(\tau - T, 0) \le \tau' \le \tau \}$. The interval is closed at both ends, so it covers $T + 1$ instants.
   - $S\,[\text{Now}]$ is $[\text{Range } 0]$: the elements with timestamp exactly $\tau$. $S\,[\text{Range Unbounded}]$ has $T = \infty$: all elements up to $\tau$.
   - $S\,[\text{Rows } N]$, a [count-based window](/count-based-window/): the $N$ elements with the largest timestamps at most $\tau$, or all of them if there are fewer than $N$. If several elements share the timestamp at the boundary, the choice among them is not fixed, so this window can be nondeterministic.
   - $S\,[\text{Partition By } A_1, \ldots, A_k \text{ Rows } N]$: split $S$ by the values of $A_1, \ldots, A_k$, take $[\text{Rows } N]$ of each part, and take the union.
   - $S\,[\text{Range } T \text{ Slide } L]$: the window of $[\text{Range } T]$ taken at the instant $\lfloor \tau / L \rfloor \cdot L$, so the relation changes only once every $L$ instants. With $L = T$ this is a [tumbling window](/tumbling-window/).
2. *Relation-to-relation* operators are the operators of SQL or the [relational algebra](/relational-algebra/), applied at each instant: $O(R_1, \ldots, R_n)(\tau) = O(R_1(\tau), \ldots, R_n(\tau))$.
3. *Relation-to-stream* operators. With bag union, bag difference and $R(-1) = \emptyset$:
   - $\text{Istream}(R) = \bigcup_{\tau \ge 0} \big( (R(\tau) - R(\tau - 1)) \times \{\tau\} \big)$: the tuples inserted at $\tau$.
   - $\text{Dstream}(R) = \bigcup_{\tau > 0} \big( (R(\tau - 1) - R(\tau)) \times \{\tau\} \big)$: the tuples deleted at $\tau$.
   - $\text{Rstream}(R) = \bigcup_{\tau \ge 0} \big( R(\tau) \times \{\tau\} \big)$: the whole relation at every instant.

**Queries and their semantics.** A CQL query is a composition of these operators, written in SQL with window clauses after each stream in the From clause and an Istream, Dstream or Rstream in the Select clause. When the query result is a relation and no relation-to-stream operator is given, but the relation can only grow, CQL adds Istream by default (Section 6.4). The *continuous semantics* (Definition 3) is that the result at $\tau$, a relation $R(\tau)$ or the stream elements with timestamp $\tau$, depends only on the input elements with timestamp at most $\tau$ and on the relations up to $\tau$.

**When time advances.** Time advances from $\tau - 1$ to $\tau$ when all inputs with timestamps up to $\tau - 1$ have been processed. The semantics thus assumes that the system knows when the input of an instant is complete. Section 8 of the paper meets this with *heartbeats*: a heartbeat with timestamp $\tau$ promises that no later stream element has a timestamp of $\tau$ or less. A heartbeat can come from the system clock (the system stamps elements on arrival, so they are in order by construction), from each source (the query-level heartbeat is the minimum of the source heartbeats), or from a known bound $D$ on the delay, as $t - D$ at global time $t$.

**Late data.** An element that arrives after a heartbeat that covers its timestamp breaks the promise. The model does not give it a meaning: the answers for the instants up to the heartbeat are already final. A heartbeat of the third kind is a heuristic if the bound $D$ is only an estimate, and then the system must drop such elements or treat them by a policy outside the model. This is the main difference from the [Dataflow model](/dataflow-model/), where late data is a normal case and earlier answers can be refined. Heartbeats are the same idea as an [event-time watermark](/event-time-watermark/) and as a [punctuation](/stream-punctuation/) on the timestamp attribute.

## What it counts

The model assigns to each query and each instant $\tau$ one result: the instantaneous relation $R(\tau)$ if the query returns a relation, or the bag of elements with timestamp $\tau$ if it returns a stream. Equality of two queries means equality of these results at every instant, for every input. The model is about meaning, not cost, but the paper and the STREAM system give the memory that each operator needs, its *synopsis*. With the cost conventions of this area, where $n$ is the number of elements in the window:

- $[\text{Rows } N]$ keeps the last $N$ elements in a [queue](/queue/). Each arrival does one insert and at most one expiry, so the work is $O(1)$ worst case per element and the memory is $N$ elements.
- $[\text{Range } T]$ keeps the elements of the last $T + 1$ instants. Each element is inserted once and expired once, so the work is $O(1)$ amortized per element. The memory $n$ has no bound in terms of $T$ alone, because the model allows any finite number of elements per instant.
- $\text{Istream}$ and $\text{Dstream}$ must compare $R(\tau)$ with $R(\tau - 1)$, so they keep the previous instantaneous relation or receive their input as a stream of inserts and deletes. The STREAM system does the second: every operator exchanges a stream of insertions and deletions, which it calls a plus-minus stream (Section 12).
- An aggregate over a window, such as $\text{Count}(*)$ over $[\text{Range } T]$, is maintained in $O(1)$ per insert and delete when the aggregate has an inverse. Without an inverse, it needs the methods of [sliding window aggregation](/sliding-window-aggregation/).

## Relation to other models

- **Tapestry.** A Tapestry query returns at $\tau$ the union of the answers of a one-time query at all instants up to $\tau$ (see [continuous query](/continuous-query/)). Section 11.2 shows that this is the CQL query Select Istream(Distinct \*) From (Istream($Q$)) [Range Unbounded]. Tapestry has no sliding windows and no relation-to-stream operators.
- **Materialized views and chronicles.** A view defined by a SQL query $Q$ over relations is the same $Q$ in CQL. The chronicle data model of Jagadish et al. has streams (chronicles), relations and persistent views, and both of its operator classes are expressible in CQL (Section 11.1).
- **Stream-only languages.** For each relational operator $O$, define a stream operator $O_s(S_1, \ldots, S_n) = \text{Rstream}(O(S_1[\text{Now}], \ldots, S_n[\text{Now}]))$, and for each window $W$, define $S[W_s] = \text{Rstream}(S[W])$. Section 11.6 shows that the stream-only language $L_s$ obtained this way has essentially the same power as CQL, and that it is close to the language of TelegraphCQ. The authors keep both types because SQL then applies unchanged.
- **The Dataflow model.** CQL has one time domain and assumes complete input up to each instant. The [Dataflow model](/dataflow-model/) has event time and processing time, uses a watermark that may be wrong, lets a window emit early, on-time and late results, and defines how later results relate to earlier ones. A CQL window at instant $\tau$ is close to a Dataflow window that fires once when the watermark passes its end, in discarding mode.
- **Windows of other pages.** $[\text{Range } T \text{ Slide } L]$ with $L < T$ is a [hopping window](/hopping-window/), and with $L = T$ a [tumbling window](/tumbling-window/). CQL has no [session window](/session-window/); a session window is defined by gaps in the data and not by a fixed interval.

## Known results in the model

All results here are theorems in the model, from Sections 6, 10 and 11 of Arasu, Babu and Widom (2006).

**Rstream is enough.** Istream and Dstream can be written with Rstream, windows and relational operators (Section 6.3). So every query has an equivalent form whose only relation-to-stream operator is Rstream.

**Window reduction (Section 10.1).** For any list $L$ of attributes and any condition $C$,
Select Istream($L$) From $S$ [Range Unbounded] Where $C$ is equivalent to Select Rstream($L$) From $S$ [Now] Where $C$. Both return each element of $S$ that satisfies $C$, at its own timestamp. More generally, Istream and Rstream give the same stream on any relation $R$ with $R(\tau) \cap R(\tau - 1) = \emptyset$ for all $\tau$. The second form needs no state, so a system should use it.

**Filter-window commutativity (Section 10.2).** A filter on a stream commutes with a time-based window: $\sigma_C(S\,[\text{Range } T]) = (\sigma_C S)\,[\text{Range } T]$. The same does not hold for a tuple-based window in general. For example, with $[\text{Rows } 1]$, the filter applied after the window can return nothing when the last element fails $C$, while the window over the filtered stream returns the last element that passes $C$.

**Expressiveness (Section 11).** Basic CQL, without user-defined functions, aggregates or windows beyond those above, is strictly more expressive than Tapestry, Tribeca, GSQL and materialized views over relations with or without chronicles.

**A worked example.** The stream $S$ has the elements $\langle a, 1 \rangle$, $\langle b, 1 \rangle$, $\langle c, 2 \rangle$, $\langle d, 4 \rangle$ and $\langle e, 5 \rangle$. The window is $S\,[\text{Range } 2]$, so at $\tau$ it holds the elements with timestamps from $\max(\tau - 2, 0)$ to $\tau$.

| $\tau$ | $S\,[\text{Range } 2](\tau)$ | Istream at $\tau$ | Dstream at $\tau$ | $S\,[\text{Now}](\tau)$ |
|---|---|---|---|---|
| 0 | empty | none | none | empty |
| 1 | a, b | a, b | none | a, b |
| 2 | a, b, c | c | none | c |
| 3 | a, b, c | none | none | empty |
| 4 | c, d | d | a, b | d |
| 5 | d, e | e | c | e |
| 6 | d, e | none | none | empty |
| 7 | e | none | d | empty |

The Rstream of the window repeats the whole relation at each instant, for example $\langle c, 4 \rangle$ and $\langle d, 4 \rangle$ at $\tau = 4$. Select Rstream(Count(\*)) From $S$ [Range 2] gives the counts 2, 3, 3, 2, 2, 2 and 1 at $\tau = 1$ to 7. For $S\,[\text{Rows } 2]$ at $\tau = 2$, the window holds $c$ and one of $a$ and $b$, because both have timestamp 1; CQL leaves this choice open. The Istream of $S\,[\text{Range Unbounded}]$ and the Rstream of $S\,[\text{Now}]$ both give $a$ and $b$ at 1, $c$ at 2, $d$ at 4 and $e$ at 5, as window reduction says.

## References
