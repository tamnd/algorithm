---
tag: 318FME
kind: problem
slug: complex-event-processing
name: Complex event processing
aliases:
- CEP
- event pattern matching
area: databases/stream-and-incremental-processing
level: advanced
summary: Detect patterns of events, such as sequences with predicates and time limits, over a stream and report each match.
model: word-ram
complexity:
  vars: {n: the number of events in the stream, k: the number of components of the pattern, T: the number of matches reported}
  time: {worst: "Ω(n + T)"}
prereqs: [regular-language, nondeterministic-finite-automaton, continuous-query, time-based-window]
see_also: [sase-event-matching, nfa-simulation, regular-expression, kleene-star, deterministic-finite-automaton, event-time-watermark, sliding-window-join, cql-stream-model]
sources:
  - paper: doi:10.1145/2187671.2187677
    title: "Gianpaolo Cugola and Alessandro Margara, Processing flows of information: from data stream to complex event processing, ACM Computing Surveys 44(3), 2012, article 15, pages 15:1 to 15:62"
    locator: "the information flow processing model, the comparison of data stream and complex event processing systems, the operators of event languages (sequences, negation, iteration, windows, parameters) and the survey of systems with automata, trees and rules (general locator)"
  - paper: doi:10.1145/1142473.1142520
    title: "Eugene Wu, Yanlei Diao and Shariq Rizvi, High-performance complex event processing over streams, Proceedings of ACM SIGMOD 2006, pages 407 to 418"
    locator: "the SASE language with SEQ, negation, equivalence tests and WITHIN, and its evaluation with active instance stacks (general locator)"
  - paper: doi:10.1145/1376616.1376634
    title: "Jagrati Agrawal, Yanlei Diao, Daniel Gyllstrom and Neil Immerman, Efficient pattern matching over event streams, Proceedings of ACM SIGMOD 2008, pages 147 to 160"
    locator: "Kleene closure and the four event selection strategies: strict contiguity, partition contiguity, skip till next match and skip till any match (general locator)"
---

Complex event processing is the problem of finding, in a stream of timestamped events, every occurrence of a pattern made of simpler events: for example an item that is read on a shelf and then at the exit with no checkout in between, within 12 hours. A pattern combines event types with sequence, negation, repetition, conditions on attributes and a time window, and each match must be reported as soon as it is complete. Most engines evaluate patterns with automata that read the stream, which makes the problem a form of matching a [regular language](/regular-language/) against an unbounded sequence, with data in the letters. The page [NFA-based event pattern matching (SASE)](/sase-event-matching/) gives one such algorithm in full.

## In plain words

A stream of small events comes in: badge reads, card payments, price ticks, sensor alarms. One event alone says little, but a certain sequence of them means something, such as a card that pays in two cities within an hour. You write a pattern that describes the sequence, with the order of the events, the conditions on their values, events that must not occur in between, and a time limit. The system watches the stream and calls out each time the pattern happens, at the moment of the event that completes it. The hard parts are that many partial sequences can be open at once, that one event can belong to many matches, and that events can arrive out of order.

## Definition

An *event* has a type, a timestamp and attributes. The input is a stream $x_1, x_2, \dots$ of events, ordered by timestamp, with ties broken by a fixed rule. A *sequence pattern* is

$$P = \mathrm{SEQ}(C_1, \dots, C_k) \ \mathrm{WHERE}\ \theta \ \mathrm{WITHIN}\ W,$$

where each component $C_i$ is an event type $E_i$, a negated type $!E_i$ or, in languages with Kleene closure, a repetition $E_i+$; $\theta$ is a condition on the attributes of the chosen events; and $W$ is a time span. Under the most permissive selection, a *match* is a tuple of events $(e_1, \dots, e_m)$, one for each positive component, at increasing positions in the stream, such that $e_i$ has the type of its component, $\theta$ holds, the span from the first to the last event is at most $W$, and for each negated component, no event of that type that satisfies its part of $\theta$ lies between the events of its neighbours.

The task is online: after each event $x_j$, report every match whose last event is $x_j$, each match once. A match cannot be reported earlier, because it is not complete before $x_j$ arrives. With a negated last component, a match can be reported only when the window has passed without the negated event.

## Variants

- **Event selection strategies.** SASE+ names four rules for which events may form a match. *Strict contiguity*: the events of a match are adjacent in the stream. *Partition contiguity*: they are adjacent within the partition given by an equality condition, such as one stock symbol. *Skip till next match*: events that cannot extend a partial match are skipped, but a partial match takes the next event that fits and does not branch. *Skip till any match*: every combination is a match, so a partial match branches on each event that fits.
- **Consumption.** Some languages consume the events of a match, so that an event takes part in at most one match. Others let an event be reused.
- **Kleene closure and aggregates.** A component $E+$ takes one or more events, with conditions such as "each price is higher than the one before", and the output may aggregate them.
- **Windows.** Time windows, count windows, or a window that starts at a given event.
- **Order and time.** Events may carry event time and arrive out of order, or the system may use arrival time only. See below.
- **Output.** Report every match, the first match only, or a summary such as the number of matches.

## Examples

Take $\mathrm{SEQ}(a, b)$ WITHIN 10 on the stream $a@1, a@2, b@3, c@4, b@5$.

| strategy | matches |
|---|---|
| strict contiguity | (a@2, b@3) |
| skip till next match | (a@1, b@3), (a@2, b@3) |
| skip till any match | (a@1, b@3), (a@1, b@5), (a@2, b@3), (a@2, b@5) |

Under strict contiguity, a@1 is followed by a@2, which is not a $b$, so only a@2 and b@3 are adjacent. Under skip till next match, a partial match starts at each $a$ and takes the next $b$, which is b@3 for both. Under skip till any match, every $a$ pairs with every later $b$ in the window.

With a negation, $\mathrm{SEQ}(a, !c, b)$ WITHIN 10 under skip till any match gives (a@1, b@3) and (a@2, b@3), because c@4 lies between each $a$ and b@5.

With an equality condition, a card fraud rule is $\mathrm{SEQ}(\mathrm{Pay}\ p, \mathrm{Pay}\ q)$ WHERE $p.\mathrm{card} = q.\mathrm{card}$ and $p.\mathrm{city} \ne q.\mathrm{city}$ WITHIN 1 hour. The equality on the card splits the stream into one sub-stream per card.

## Known algorithms

- **Automata with shared stacks or buffers.** SASE (Wu, Diao and Rizvi, 2006) runs a nondeterministic automaton over the stream and keeps the partial matches in stacks with pointers to their predecessors; it builds each match when its last event arrives and pushes the window and the equality tests into the stacks. SASE+ (2008) extends this to Kleene closure with an NFA and a shared match buffer. The SASE page proves that the stack scheme reports each match once, with a search cost of $O(k^2)$ per match.
- **Other automaton models.** Cugola and Margara (2012) survey engines that compile patterns into automata, such as Cayuga, and the CEP libraries of stream processors such as Apache Flink also use automata.
- **Trees of operators.** Some engines evaluate a sequence as a tree of join-like operators over buffers of events, which allows a cost-based choice of the order in which the components are joined; ZStream (Mei and Madden, 2009) is an example.
- **Relational evaluation.** A sequence pattern with a window is a self-join of the stream with conditions on the order of the timestamps, so a [continuous query](/continuous-query/) engine can evaluate it with window joins. This is general but usually slower than a dedicated matcher.
- **Plain automata for strict contiguity.** With strict contiguity and conditions on single events only, the pattern is a regular expression over the event types, and a [deterministic automaton](/deterministic-finite-automaton/) or an [NFA simulation](/nfa-simulation/) finds the matches in time proportional to the stream.

## Bounds

- **Theorem (output size).** Any algorithm must read every event and report every match, so it needs $\Omega(n + T)$ time. Under skip till any match, $T$ can be very large: if a window holds $n/k$ events of each of the types $E_1, \dots, E_k$, in this order, then every choice of one event per type is a match, so $T \ge (n/k)^k$.
- **Theorem (strict contiguity).** For a fixed pattern of types under strict contiguity, without conditions across events, the set of streams that end with a match is a regular language, so a deterministic automaton reports matches in $O(1)$ time per event, with a number of states that depends only on the pattern. A time window adds a test on the timestamps of the open match, which the automaton cannot do with its states alone; for a pattern of $k$ single events, keeping the last $k$ timestamps is enough.
- **Skip till next match.** Each partial match takes one path, so it gives at most one match per start event. The work per event is proportional to the number of open partial matches, which the window bounds.
- **Measurements.** The papers on SASE, SASE+ and their successors measure throughput on synthetic and real streams. These are measurements on their systems, and this page does not repeat them.

## Reductions

- **Regular expression matching.** Strict contiguity on event types is the same as regular expression search in a string whose letters are the event types, so CEP under strict contiguity is at least as hard as this classic problem and, without data conditions, no harder.
- **Window joins.** A sequence of $k$ components under skip till any match is a $k$-way self-join of the stream with the conditions $e_1.ts \le \cdots \le e_k.ts$, $e_k.ts - e_1.ts \le W$ and $\theta$. A negation becomes an anti-join. So every sequence pattern can be written as a continuous query over windows, as in the [CQL stream model](/cql-stream-model/).
- **From matches to streams.** The output of a pattern is a stream of complex events, which can be the input of other patterns. This is how hierarchies of events are built.

## Applications

The SASE papers motivate the problem with RFID tracking in retail and supply chains, such as the shoplifting pattern. Other common uses are financial trading, where a pattern detects a price movement across stocks; fraud detection on payments; intrusion detection on network logs; and the monitoring of sensors and business processes.

**Late data.** Most matchers need the events in timestamp order. A stream with bounded disorder can be reordered with a buffer that holds each event for a fixed delay, as on the [event-time watermark](/event-time-watermark/) page, at the cost of that delay in every report. A late event that falls outside the delay can complete a match that was already missed, or, under negation, show that a reported match was false. A system must then drop the event, report the missed match late, or retract the earlier report. The choice is part of the semantics of the query, not of the algorithm.

## References
