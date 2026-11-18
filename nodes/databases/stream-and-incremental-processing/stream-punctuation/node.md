---
tag: JR2PEY
kind: concept
slug: stream-punctuation
name: Punctuation (data streams)
aliases:
- stream punctuation
area: databases/stream-and-incremental-processing
level: advanced
summary: "A marker embedded in a data stream that says no later tuple will match a given predicate, so that blocking operators can emit results and stateful operators can drop state."
prereqs: [continuous-query, event-time-watermark, group-by-aggregation]
see_also: [cql-stream-model, dataflow-model, symmetric-hash-join, sliding-window-join, tumbling-window, incremental-view-maintenance, iterator-model, complex-event-processing]
sources:
  - paper: doi:10.1109/TKDE.2003.1198390
    title: Peter A. Tucker, David Maier, Tim Sheard and Leonidas Fegaras, Exploiting punctuation semantics in continuous data streams, IEEE Transactions on Knowledge and Data Engineering 15(3), 2003, pages 555 to 568
    locator: the definition of punctuations as patterns over the attributes, the match of a tuple and a punctuation, and the pass, keep and propagation behaviors of the query operators (general locator; this page relies on the journal version)
  - paper: "Peter A. Tucker and David Maier, Architectural considerations for punctuated data streams, Proceedings of the 18th International Conference on Data Engineering (ICDE), 2002"
    title: Architectural considerations for punctuated data streams
    locator: the earlier conference version of the punctuation work (general locator)
  - paper: doi:10.1007/s00778-004-0147-z
    title: Arvind Arasu, Shivnath Babu and Jennifer Widom, The CQL continuous query language, semantic foundations and query execution, The VLDB Journal 15(2), 2006, pages 121 to 142
    locator: Section 8 (heartbeats, which are punctuations on the timestamp)
  - paper: doi:10.14778/2824032.2824076
    title: Tyler Akidau et al., The Dataflow Model, a practical approach to balancing correctness, latency, and cost in massive-scale, unbounded, out-of-order data processing, PVLDB 8(12), 2015, pages 1792 to 1803
    locator: Section 2.3 (punctuations and watermarks as global progress metrics, and triggers on data punctuations)
---

A *punctuation* is an item placed inside a data stream, between the tuples, that says "no tuple after this point matches the predicate $p$"; Tucker, Maier, Sheard and Fegaras (2003) use it to let operators that would block on an unbounded stream emit results early and drop state. An [event-time watermark](/event-time-watermark/) is a special case: a punctuation on the event time attribute alone, of the form "no later tuple has an event time below $w$", that only moves forward and is often an estimate made by the system. A general punctuation can name any attributes, for example "no more bids for auction 17", which no single watermark can say.

## In plain words

An auction site sends you every bid as it comes in, and you must report the highest bid of each auction. On its own, the stream never tells you that an auction is over, so you can never be sure of a highest bid, and you must remember every auction forever. A punctuation fixes this: when auction 17 closes, the site puts a note in the stream that says "no more bids for auction 17". When you read that note, you report the highest bid of auction 17 and forget that auction. The note does not have to be about time. It can be about any value that the source knows is finished.

## The idea

**Punctuations as patterns.** Let a stream have a schema with attributes $A_1, \ldots, A_a$. A punctuation is a list of patterns $(q_1, \ldots, q_a)$, one for each attribute. In the paper a pattern is a wildcard $*$ (any value), a constant, a range, a list of constants, or the empty pattern (no value). A tuple $t$ *matches* a punctuation if each value $t.A_i$ matches $q_i$. A *punctuated stream* is a sequence of tuples and punctuations, and it is *well formed* if no tuple matches a punctuation that comes before it in the sequence. So a punctuation is a promise about the rest of the stream: the subset of the domain that it describes is finished.

**Three behaviors of an operator.** For each operator, Tucker et al. define what it may do when punctuations arrive.

- *Pass*: which results the operator can now output. A group-by with an aggregate can output the result for group $g$ once the punctuations seen so far cover all tuples of $g$. Duplicate elimination, sort and set difference are other operators that a punctuation can unblock.
- *Keep*: which state the operator must still keep. A [symmetric hash join](/symmetric-hash-join/) of $R$ and $S$ on $B$ keeps each tuple of $R$ in a table so that later tuples of $S$ can match it. When a punctuation on $S$ says that no more $S$ tuples with $B = b$ will come, the stored $R$ tuples with $B = b$ can never match again, and the join can delete them.
- *Propagation*: which punctuations the operator can send to its output. A selection can pass a punctuation on unchanged. A group-by that has output group $g$ can send "no more results for $g$". A join on $B$ can send the punctuation "no more results with $B = b$" when both inputs have punctuated $b$.

Two simple facts explain why this works. If all tuples of group $g$ are in, the aggregate of $g$ is final, so output on a punctuation is correct. And a stored tuple that no future input can match does not change any future output, so deleting it is safe. Both depend on the stream being well formed.

**Relation to watermarks and heartbeats.** A watermark $w$ on the event time $E$ is the punctuation with the pattern $(-\infty, w)$ on $E$ and wildcards elsewhere. A sequence of watermarks is a sequence of such punctuations whose ranges grow. A heartbeat of the [CQL stream model](/cql-stream-model/) is the same with a closed range up to $\tau$. Watermarks are the common case in practice because one number covers every window, and the system can compute it with a minimum over the inputs. Punctuations are more general: they can be on keys with no order, and they can close a key while older keys stay open.

**Late data.** The theory assumes that punctuations are correct, which holds when the source knows the fact, for example when the auction system itself closes an auction. A tuple that matches an earlier punctuation makes the stream ill formed. The operator has already output a result and deleted state that the tuple needs, so it can only drop the tuple, report an error, or send a correction downstream. If punctuations are generated from an estimate, such as a bound on the network delay, they are heuristics with the same risk as a heuristic watermark.

**Cost.** A punctuation does not reduce the work per tuple. It bounds the state: a group-by keeps one row for each group that is not yet closed, and a join keeps only the tuples of keys that are still open on the other input. Without punctuations or windows, both keep state for every key that has ever appeared. Each punctuation costs a match against the state; with constant patterns on the key, a hash lookup does this in $O(1)$ expected time per closed key.

## Examples

**Group-by with punctuation.** The stream holds bids (auction, amount) and punctuations "auction $a$ is closed", written $\langle a, * \rangle$. The query outputs, for each auction, the number of bids and the highest bid.

| item | state after the item (open auctions) | output |
|---|---|---|
| bid (1, 10) | 1 | none |
| bid (2, 5) | 1, 2 | none |
| bid (1, 12) | 1, 2 | none |
| punctuation $\langle 1, * \rangle$ | 2 | (1, 2 bids, 12) |
| bid (2, 7) | 2 | none |
| bid (3, 4) | 2, 3 | none |
| punctuation $\langle 2, * \rangle$ | 3 | (2, 2 bids, 7) |
| bid (3, 6) | 3 | none |
| punctuation $\langle 3, * \rangle$ | none | (3, 2 bids, 6) |

The operator never holds more than two open auctions. Without the punctuations it could output nothing until the end of the stream, which never comes, and its state would grow with the number of auctions. A bid (1, 15) after the first punctuation would make the stream ill formed: the result (1, 2 bids, 12) is already out.

**A join that deletes state.** Join the stream of bids with a stream of item descriptions on the auction number. A punctuation $\langle 1, * \rangle$ on the bid stream says that no more bids for auction 1 will come, so the join can delete the description of auction 1. It must still keep the bids for auction 1 if a description of auction 1 could arrive later, unless the description stream also has a punctuation for auction 1.

**A punctuation that is not a watermark.** In a stream of sensor readings, the pattern $(*, \text{sensor 7}, *)$ says that sensor 7 has been switched off. A per-sensor aggregate can then close sensor 7 at once, while all other sensors stay open. No event-time watermark can express this, because the readings of the other sensors with the same times are still coming.

## Where it is used

- The Niagara stream engine, in which both the punctuation work and [pane-based aggregation](/panes-window-aggregation/) were built.
- Window aggregation: a punctuation on the window id or the timestamp closes a [tumbling window](/tumbling-window/) or a pane.
- Watermarks and heartbeats in later systems, which are punctuations on time: MillWheel and the [Dataflow model](/dataflow-model/), whose triggers can also fire on data punctuations; the heartbeats of STREAM; and punctuated watermark generators in Apache Flink, which emit a watermark when a special record arrives.
- Joins over streams, such as the [symmetric hash join](/symmetric-hash-join/) and the [sliding window join](/sliding-window-join/), where punctuations or windows bound the state.

## References
