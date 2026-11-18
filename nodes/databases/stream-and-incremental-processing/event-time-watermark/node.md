---
tag: FEWQXW
kind: concept
slug: event-time-watermark
name: Watermark (event time)
aliases:
- event-time watermark
- low watermark
area: databases/stream-and-incremental-processing
level: core
summary: "A timestamp that moves forward with the stream and claims that no more elements with an earlier event time will arrive. Elements that arrive behind it are late."
prereqs: [continuous-query]
see_also: [stream-punctuation, dataflow-model, cql-stream-model, tumbling-window, session-window, lamport-clocks, timely-dataflow, asynchronous-barrier-snapshotting]
sources:
  - paper: "Tyler Akidau, Alex Balikov, Kaya Bekiroglu, Slava Chernyak, Josh Haberman, Reuven Lax, Sam McVeety, Daniel Mills, Paul Nordstrom and Sam Whittle, MillWheel, fault-tolerant stream processing at internet scale, PVLDB 6(11), 2013, pages 1033 to 1044"
    title: "MillWheel: fault-tolerant stream processing at internet scale"
    locator: "Section 4.5 on low watermarks: the definition as the minimum of the oldest work of a computation and the low watermarks of its upstream computations, the seeding by injectors, late records and the monotonic guarantee"
  - paper: doi:10.14778/2824032.2824076
    title: Tyler Akidau et al., The Dataflow Model, a practical approach to balancing correctness, latency, and cost in massive-scale, unbounded, out-of-order data processing, PVLDB 8(12), 2015, pages 1792 to 1803
    locator: "Section 2.3 (watermarks that are too fast or too slow, and why triggers are needed) and footnote 6 (most watermarks are heuristic)"
  - paper: doi:10.14778/3476311.3476389
    title: Edmon Begoli, Tyler Akidau, Slava Chernyak, Fabian Hueske, Kathryn Knight, Kenneth Knowles, Daniel Mills and Dan Sotolongo, Watermarks in stream processing systems, semantics and comparative analysis of Apache Flink and Google Cloud Dataflow, PVLDB 14(12), 2021, pages 3135 to 3147
    locator: the definition of watermarks and the comparison of how the two systems compute and propagate them (general locator)
  - paper: doi:10.1007/s00778-004-0147-z
    title: Arvind Arasu, Shivnath Babu and Jennifer Widom, The CQL continuous query language, semantic foundations and query execution, The VLDB Journal 15(2), 2006, pages 121 to 142
    locator: Section 8 (heartbeats from the system clock, from the sources or from a bound on the delay)
---

An *event-time watermark* is a timestamp $w$ that a stream system attaches to a point in the stream, with the claim that every element that comes later has an event time of at least $w$; it lets an operator decide that a window is complete and emit its result. A [punctuation](/stream-punctuation/) is the general form: a predicate on any attributes, embedded in the stream, which says that no later element will match it. A watermark is the special case of a punctuation on the event time alone, which only moves forward and is often computed by the system as an estimate. When the estimate is wrong, elements arrive behind the watermark; they are *late data*, and the system needs a policy for them.

## In plain words

Letters about a day's sales come to an office by post, and some are slow. The clerk wants to report the total for Monday, but cannot know if one more Monday letter is still on the way. So the clerk makes a rule: "when I get a letter dated Thursday, I take it that all Monday letters are in." That rule is a watermark. It lets the clerk send the Monday total, but it is a guess. If a Monday letter comes on Friday, the clerk must throw it away, or send a correction, or keep the report open longer next time. A strict rule gives early reports and more corrections. A loose rule gives late reports and fewer corrections.

## The idea

**Definition.** Each element of a stream has an event time $e$, set at its source, and reaches an operator at a processing time $p$. A *watermark* for the stream is a function $w(p)$ of processing time that does not decrease. It is *correct*, or *perfect*, if every element that reaches the operator after processing time $p$ has $e \ge w(p)$. An element with $e < w(p)$, where $w(p)$ is the watermark when it arrives, is *late*. A watermark that is not guaranteed to be correct is *heuristic*.

**Low watermarks in MillWheel.** MillWheel computes, for each computation $A$, a *low watermark*:

$$\mathrm{lwm}(A) = \min\big(\mathrm{oldest}(A),\ \min\{\mathrm{lwm}(C) : C \text{ sends output to } A\}\big),$$

where $\mathrm{oldest}(A)$ is the smallest timestamp of the work of $A$ that is not finished: records in flight, stored or waiting to be delivered. With no input streams, the low watermark is the oldest work. The values at the sources are set by *injectors*, which bring data in from outside systems. They can only estimate the work still pending outside, so a computation must expect a small rate of late records. MillWheel keeps each low watermark monotone even when late data arrives.

**Why the minimum is correct.** Take an acyclic graph of operators in which each source has a correct watermark, and each operator gives every output a timestamp no smaller than the smallest timestamp of the inputs it used. Then the rule above gives a correct watermark at each operator. *Proof (theorem).* Assume that an element $x$ with timestamp $t$ arrives at $A$ after $A$ has reported $\mathrm{lwm}(A) > t$, and that all values were computed at that same moment. If $x$ already existed then, in flight or waiting for delivery to $A$, it was unfinished work of $A$, so $\mathrm{oldest}(A) \le t$, a contradiction. Otherwise an upstream $C$ produced $x$ later, from inputs of which at least one, $y$, has a timestamp of at most $t$. If $y$ was unfinished work of $C$ at that moment, then $\mathrm{lwm}(C) \le t$ and so $\mathrm{lwm}(A) \le t$, a contradiction. If not, $y$ reached $C$ later, and the same argument applies to $y$ at $C$, where $\mathrm{lwm}(C) \ge \mathrm{lwm}(A) > t$. Each step moves one edge upstream, and the graph has no cycles, so the chain ends at a source, where $y$ is a late element for a source watermark that was assumed correct. $\square$ The proof also shows where the watermark becomes wrong in practice: at the sources, and in user code that moves a timestamp backwards.

**Heuristic watermarks.** At a source the system often cannot know what is still on the way: a phone may be offline for a day and then upload its events. So most source watermarks are heuristics. A common one, which Apache Flink provides in this form up to one time unit, is *bounded out-of-orderness*: $w = (\text{largest event time seen so far}) - D$ for a chosen delay $D$. It is correct if and only if no element is more than $D$ behind the largest event time seen before it. The Dataflow paper (Section 2.3) names the two ways a watermark fails.

- *Too fast*: it passes event times that still have data, so data arrives late and results computed at the watermark are wrong.
- *Too slow*: it waits for a slow element or an idle source, so every result is delayed. Because a downstream watermark is the minimum over its inputs, one idle input holds back the whole graph.

**Late data policies.** A system must choose what to do with a late element.

- *Drop it*, and count what was dropped. MillWheel's Zeitgeist pipeline drops late records and reports their number, about 0.001% of the records (a measurement in that pipeline).
- *Correct the result*: send a new value for the window and, where needed, a retraction of the old one, as with the late triggers and accumulation modes of the [Dataflow model](/dataflow-model/).
- *Keep the window open for a bounded time*, the allowed lateness of Apache Beam and Apache Flink, and drop only elements that come after it. Flink can also send such elements to a side output.

**Heartbeats.** The heartbeats of the [CQL stream model](/cql-stream-model/) (Section 8 of Arasu, Babu and Widom 2006) are watermarks. A heartbeat $\tau$ promises that no later element has a timestamp of $\tau$ or less. It can come from the system clock, when the system sets timestamps on arrival and the stream is in order by construction; from each source, with the minimum over the sources; or from a bound $D$ on the network delay, as $t - D$ at global time $t$. Only the first kind is correct by construction.

## Examples

**Bounded out-of-orderness on one stream.** The elements arrive with these event times, in this order: 1, 3, 2, 6, 4, 5, 9, 3, 10, 8. The watermark after each element is the largest event time so far minus $D$. An element is late if its event time is below the watermark when it arrives. A [tumbling window](/tumbling-window/) [0, 4) can fire when the watermark reaches 4.

| $D$ | watermark after each arrival | late elements (position: event time) | window [0, 4) fires after arrival |
|---|---|---|---|
| 0 | 1, 3, 3, 6, 6, 6, 9, 9, 10, 10 | 3: 2, 5: 4, 6: 5, 8: 3, 10: 8 | 4 |
| 1 | 0, 2, 2, 5, 5, 5, 8, 8, 9, 9 | 5: 4, 8: 3, 10: 8 | 4 |
| 2 | -1, 1, 1, 4, 4, 4, 7, 7, 8, 8 | 8: 3 | 4 |
| 3 | -2, 0, 0, 3, 3, 3, 6, 6, 7, 7 | 8: 3 | 7 |
| 6 | -5, -3, -3, 0, 0, 0, 3, 3, 4, 4 | none | 9 |

The element with event time 3 at position 8 arrives after an element with event time 9, so it is 6 behind. The watermark is correct on this stream only for $D \ge 6$, and then the window [0, 4) waits until the ninth arrival. With $D = 2$ the window fires after the fourth arrival with the elements 1, 3 and 2, and the late 3 needs one of the policies above.

**Two inputs.** An operator joins two streams whose watermarks are 7 and 4. Its own watermark is at most 4. If the second stream stops sending data and its watermark stays at 4, the operator's watermark stays at 4 too, and no window that ends after 4 can fire. Systems handle this with an idle timeout: a source that has been silent for a time is left out of the minimum. That is a heuristic, because the silent source can wake up with old data.

**A perfect watermark.** A system that sets the event time of each element to its arrival time, such as Tapestry with its append timestamps, has a correct watermark at once: the current time. There is never late data, but the event time then does not describe when the event happened.

## Where it is used

- Window aggregation in event time: a [tumbling window](/tumbling-window/), a [hopping window](/hopping-window/) or a [session window](/session-window/) emits its result when the watermark passes its end. [Pane-based aggregation](/panes-window-aggregation/) and [stream slicing](/stream-slicing/) close a pane or a slice in the same way.
- MillWheel, Google Cloud Dataflow and Apache Beam (the low watermark and watermark triggers), Apache Flink (watermarks that flow as special records between operators, with the minimum over the input channels) and Spark Structured Streaming (a watermark used to bound the state of aggregations).
- Joins and pattern matching: a [sliding window join](/sliding-window-join/) can delete the state older than the watermark minus the window size, and [complex event processing](/complex-event-processing/) can sort events by time before it matches them.
- Progress tracking in general: [timely dataflow](/timely-dataflow/) has frontiers, which are exact inside the system. [Asynchronous barrier snapshotting](/asynchronous-barrier-snapshotting/) sends barriers through the graph in the same way that Flink sends watermarks, but for consistent snapshots, not for time.

## References
