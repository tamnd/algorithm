---
tag: 4ABN0H
kind: model
slug: dataflow-model
name: Dataflow model
aliases:
- Akidau dataflow model
- windowing triggers and accumulation model
area: databases/stream-and-incremental-processing
level: advanced
summary: "A model of stream computation that separates what is computed, where in event time (windows), when in processing time (triggers) and how results refine (accumulation)."
prereqs: [continuous-query, event-time-watermark, tumbling-window, session-window]
see_also: [cql-stream-model, hopping-window, stream-punctuation, panes-window-aggregation, stream-slicing, timely-dataflow, asynchronous-barrier-snapshotting, incremental-view-maintenance]
sources:
  - paper: doi:10.14778/2824032.2824076
    title: Tyler Akidau, Robert Bradshaw, Craig Chambers, Slava Chernyak, Rafael J. Fernandez-Moctezuma, Reuven Lax, Sam McVeety, Daniel Mills, Frances Perry, Eric Schmidt and Sam Whittle, The Dataflow Model, a practical approach to balancing correctness, latency, and cost in massive-scale, unbounded, out-of-order data processing, PVLDB 8(12), 2015, pages 1792 to 1803
    locator: "Section 1 (the four questions what, where, when and how), Section 2.2 (AssignWindows, MergeWindows and GroupByKeyAndWindow), Section 2.3 (triggers and the discarding, accumulating and accumulating and retracting modes) and Section 2.4 (the worked examples)"
  - paper: "Tyler Akidau, Alex Balikov, Kaya Bekiroglu, Slava Chernyak, Josh Haberman, Reuven Lax, Sam McVeety, Daniel Mills, Paul Nordstrom and Sam Whittle, MillWheel, fault-tolerant stream processing at internet scale, PVLDB 6(11), 2013, pages 1033 to 1044"
    title: "MillWheel: fault-tolerant stream processing at internet scale"
    locator: the low watermark that the Dataflow model uses as its completion estimate
  - paper: doi:10.1007/s00778-004-0147-z
    title: Arvind Arasu, Shivnath Babu and Jennifer Widom, The CQL continuous query language, semantic foundations and query execution, The VLDB Journal 15(2), 2006, pages 121 to 142
    locator: the window and relation-to-stream operators that the Dataflow model generalizes
---

The Dataflow model, of Akidau et al. (2015) at Google, describes a [continuous query](/continuous-query/) over unbounded data that arrives out of order as answers to four separate questions: *what* is computed (the transformations), *where* in event time the data is grouped (windows), *when* in processing time the results are emitted (triggers), and *how* later results for a window relate to earlier ones (accumulation modes). A continuous query is the general notion; the [CQL stream model](/cql-stream-model/) is a semantics with one time domain that gives each instant one final answer and assumes complete input up to that instant. The Dataflow model instead accepts that a [watermark](/event-time-watermark/) can be wrong, so one window can produce several results, and it makes the user choose how those results relate.

## The machine

**Two time domains.** Each element has an *event time*, the time at which the event happened at its source, and a *processing time*, the time at which the system observes it. Processing time is never before event time, and the gap between them, the skew, changes all the time. Windows are defined in event time. Triggers fire in processing time.

**Elements.** An element is a 4-tuple (key, value, event time, window). An element enters the system in the default *global window*, which covers all of event time, so a pipeline without windows has the meaning of a batch job.

**Core operations.** A pipeline is a graph of two primitives.

- *ParDo* applies a user function to each element and gives zero or more elements. It acts element by element, so it does not care about windows or completeness.
- *GroupByKey* collects the values of each key. On unbounded data, it is replaced by *GroupByKeyAndWindow*, which groups by key and window.

**Windowing.** Windowing is split into two functions.

- AssignWindows(element) gives the set of windows of the element, zero or more. *Fixed* windows of size $W$ give one window $[kW, (k + 1)W)$. *Sliding* windows of size $W$ and period $L$ give the $W / L$ windows that contain the event time when $L$ divides $W$; these are the [hopping windows](/hopping-window/) of other pages. *Sessions* with gap $g$ give the one window $[e, e + g)$ for an element with event time $e$.
- MergeWindows(set of windows) merges windows at grouping time. For sessions it merges overlapping windows into one, so a session grows as data arrives.

GroupByKeyAndWindow is a composite of five steps: drop the event times and keep (key, (value, window)) pairs; group by key; merge the windows of each key; group the values of each key by window; and expand each (key, window, values) result into elements with a new event time for the window. The paper uses the end of the window; any time at or after the earliest event of the window keeps the watermark correct.

**Watermark.** The completion estimate is a watermark in the sense of MillWheel: a lower bound on the event times that may still arrive. For most real sources the system cannot know this bound, so the watermark is a heuristic (Section 2.3, footnote 6). The paper names its two failures. A watermark that is *too fast* passes event times for which data still exists; that data is *late*. A watermark that is *too slow* waits on one slow element and delays every result.

**Triggers.** A trigger says when, in processing time, a window emits a result. Each result is called a *pane*. This is not the pane of [pane-based window aggregation](/panes-window-aggregation/); in this model a pane is one firing of one window. The paper gives triggers on the watermark (and on percentile watermarks), on points in processing time and on data arrival (counts, bytes, punctuations, patterns), and triggers can be combined with and, or, sequences and repetition. A common trigger fires early panes in processing time, one on-time pane when the watermark passes the end of the window, and one late pane for each late element.

**Accumulation modes.** When a window fires again, the mode says how the new pane relates to the earlier ones.

- *Discarding*: the window state is cleared after each pane, so each pane covers only the elements since the previous pane.
- *Accumulating*: the state is kept, so each pane covers all elements of the window so far and replaces the previous pane.
- *Accumulating and retracting*: as accumulating, and the system also stores the last emitted value; at the next firing it first emits a retraction of that value and then the new value. Retractions are needed when a later grouping step regroups the results by another key, because the earlier value may have gone to a different group.

**Late data.** Late data is a normal input in this model. A late element joins the windows that AssignWindows gives for its event time, and a late trigger then emits a new pane for each of them, in the mode of the pipeline. The paper does not fix a time after which the state of a window is deleted. Systems that implement the model, such as Apache Beam and Apache Flink, add an allowed lateness: after the watermark passes the end of a window plus this bound, the state is deleted and later elements for the window are dropped.

## What it counts

The model assigns to each key and window a sequence of panes in processing time, and to each pane a value that depends on the accumulation mode. With $W$ the window size, $L$ the period of sliding windows and $p$ the number of panes of one window:

- *Per element.* AssignWindows gives one window for fixed windows and sessions and $W / L$ windows for sliding windows. Without sharing, an element is added to the state of each of its windows, so the work is $\Theta(W / L)$ combiner calls per element, worst case. [Pane-based aggregation](/panes-window-aggregation/) and [stream slicing](/stream-slicing/) cut this to one call per element.
- *Memory.* Per key, the state is one combiner value for each open window when the aggregate is associative and commutative, and the list of values otherwise. A window stays open until its last trigger, so late data and a long allowed lateness increase the number of open windows. Accumulating and retracting also keeps the last emitted value of each window.
- *Output.* Discarding emits $p$ partial values whose combination is the final value. Accumulating emits $p$ values of which the last one is the final value. Accumulating and retracting emits $p$ values and $p - 1$ retractions.

## Relation to other models

- **CQL.** A CQL time-based window at instant $\tau$ is like a fixed or sliding Dataflow window that fires once, when the watermark passes its end, in discarding mode, with a watermark that is never wrong. CQL has no session windows and no form of refinement; its heartbeats play the part of a perfect watermark.
- **Batch, micro-batch and Lambda.** The paper shows by examples in Section 2.4 that a batch job is the global window with one trigger at the end of the input, that micro-batch execution is a repeated processing-time trigger, and that a Lambda Architecture (a fast streaming job and a later batch job that corrects it) is a pipeline with early panes and a final accumulating pane. These are design claims shown by examples, not theorems.
- **MillWheel and FlumeJava.** The model is implemented on MillWheel for streaming and FlumeJava for batch, and in Google Cloud Dataflow; Apache Beam is the open-source form of its SDK. [Asynchronous barrier snapshotting](/asynchronous-barrier-snapshotting/) is a way to make such a pipeline tolerate faults, and is outside the model.
- **Timely dataflow.** [Timely dataflow](/timely-dataflow/) tracks progress with timestamps from a partial order and frontiers, which are exact by construction inside the system. The Dataflow watermark plays the role of the frontier, but at the sources it is an estimate.

## Known results in the model

**Proposition 1 (theorem).** Let the aggregate be a combiner $\oplus$ that is associative and commutative, let one window receive the elements $x_1, \ldots, x_m$ in some order, and let the window fire $p$ times, the last time after its last element. Then:

1. in discarding mode, the $\oplus$ of the values of the $p$ panes is $x_1 \oplus \cdots \oplus x_m$;
2. in accumulating mode, the last pane is $x_1 \oplus \cdots \oplus x_m$;
3. in accumulating and retracting mode with an aggregate that has an inverse (a sum), a consumer that adds each value and subtracts each retraction holds $x_1 \oplus \cdots \oplus x_m$ after the last pane.

*Proof.* In discarding mode the panes cover disjoint consecutive blocks of the elements, and together the blocks are all $m$ elements; associativity and commutativity give the claim. In accumulating mode the last pane covers all elements received, which are all $m$. In the third mode, the consumer receives $v_1$, then $-v_1$ and $v_2$, and so on; the sum telescopes to $v_p$, which is the accumulating value of the last pane. $\square$

**Proposition 2 (theorem).** If AssignWindows depends only on the event time and the key, and no element is dropped, then the final value of each window does not depend on the arrival order, on the watermark, or on the triggers. It equals the result of the same pipeline run as a batch job on all the data. *Proof.* The set of elements of each window is fixed by their event times, and Proposition 1 gives the same final value for any order and any firing times. $\square$ Late data does change *when* the final value is known, and it changes the values of all panes but the last. If a system drops late data, Proposition 2 fails for each window that loses an element.

**A worked example.** Fixed windows of 2 minutes, a sum, and a heuristic watermark that is the largest event time seen so far minus 1. Each element is (event time, processing time, value): (0, 1, 5), (1, 3, 7), (3, 4, 3), (2, 5, 4), (5, 6, 8) and (1, 8, 9). The trigger fires one on-time pane when the watermark reaches the end of a window, and one late pane for each late element.

| processing time | watermark after the element | pane | discarding | accumulating | accumulating and retracting |
|---|---|---|---|---|---|
| 4 | 2 | [0, 2) on time | 12 | 12 | 12 |
| 6 | 4 | [2, 4) on time | 7 | 7 | 7 |
| 8 | 4 | [0, 2) late | 9 | 21 | retract 12, then 21 |
| end of input | infinity | [4, 6) on time | 8 | 8 | 8 |

The element (2, 5, 4) arrives after (3, 4, 3) but it is not late, because the watermark is only 2 and the window [2, 4) has not fired. The element (1, 8, 9) is late: the watermark reached 2 at processing time 4 on the evidence of the event time 3, and window [0, 2) had already fired with 12. In discarding mode the two panes of [0, 2) add up to 21; in accumulating mode the last pane is 21; with retractions a downstream sum goes from 12 to 21. This is Proposition 1 on the example. The same pipeline as a batch job gives 21, 7 and 8, as Proposition 2 says.

## References
