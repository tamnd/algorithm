---
tag: ZPAWWC
kind: technique
slug: stream-slicing
name: Stream slicing
aliases:
- window slicing
- Cutty slicing
area: databases/stream-and-incremental-processing
level: research
summary: "Cut a stream into non-overlapping slices at the window boundaries of all queries, keep one partial aggregate per slice, and combine slices to answer each window, so that windows share work."
prereqs: [panes-window-aggregation, hopping-window, session-window, monoid]
see_also: [flatfat, sliding-window-aggregation, two-stacks-queue, daba-queue, tumbling-window, event-time-watermark, dataflow-model, segment-tree]
sources:
  - paper: doi:10.1145/1142473.1142543
    title: Sailesh Krishnamurthy, Chung Wu and Michael J. Franklin, On-the-fly sharing for streamed aggregation, Proceedings of ACM SIGMOD 2006, pages 623 to 634
    locator: paired windows and the sharing of slices among queries with different ranges and slides (general locator)
  - paper: doi:10.1145/2983323.2983807
    title: Paris Carbone, Jonas Traub, Asterios Katsifodimos, Seif Haridi and Volker Markl, Cutty, aggregate sharing for user-defined windows, Proceedings of the 25th ACM International Conference on Information and Knowledge Management (CIKM), 2016, pages 1201 to 1210
    locator: slicing at window starts only, for windows defined by user functions (general locator)
  - paper: doi:10.1145/3433675
    title: Jonas Traub, Philipp M. Grulich, Alejandro Rodriguez Cuellar, Sebastian Bress, Asterios Katsifodimos, Tilmann Rabl and Volker Markl, Scotty, general and efficient open-source window aggregation for stream processing systems, ACM Transactions on Database Systems 46(1), 2021, article 1
    locator: general stream slicing for in-order and out-of-order streams, for context-free and context-aware windows, and the split, merge and update of slices (general locator)
  - paper: doi:10.1145/1058150.1058158
    title: Jin Li, David Maier, Kristin Tufte, Vassilis Papadimos and Peter A. Tucker, No pane, no gain, efficient evaluation of sliding-window aggregates over data streams, SIGMOD Record 34(1), 2005, pages 39 to 44
    locator: Section 3.1 (panes of length gcd(RANGE, SLIDE), the special case of slicing for one query)
---

Stream slicing cuts a stream into non-overlapping *slices* at the boundaries of the windows of all queries, keeps one partial aggregate per slice, and computes each window by combining the slices that it covers, so that one tuple is aggregated once even when many windows of many queries contain it. [Pane-based aggregation](/panes-window-aggregation/) is the special case of one query with equal slices of length $\gcd(R, S)$; slicing allows slices of unequal length, cuts only where some window starts or ends, and also handles session windows and out-of-order data. Slicing decides *which partials* exist; a structure such as [FlatFAT](/flatfat/), a [two-stacks queue](/two-stacks-queue/) or a [DABA queue](/daba-queue/) decides *how fast* the partials of one window are combined, and the [sliding window aggregation](/sliding-window-aggregation/) page states that problem.

## In plain words

Two reports read the same sales: one sums the last 6 minutes every 4 minutes, the other the last 5 minutes every 3 minutes. Mark on a time line every moment at which some report's window starts or ends. Between two marks, every sale belongs to exactly the same reports, so you can keep one running total for that stretch. Each report then adds up the totals of the stretches inside its window. A sale is added once, to its stretch, and the stretches are shared by both reports. If the input comes in time order, you need marks only where windows start: when a window ends in the middle of a stretch, the running total of that stretch so far is exactly the part you need.

## When it applies

- Several window aggregates read the same stream with the same aggregate (or aggregates that can share a partial, such as sum and average), but with different windows: [tumbling](/tumbling-window/), [hopping](/hopping-window/) or [session](/session-window/) windows, in time or in tuple counts.
- The aggregate has an associative combine with an identity. If tuples come out of order, it should also be commutative, or the slices must keep their tuples.
- The number of slices that one window covers is small compared with the number of tuples in it. Slicing gains when tuples are dense and windows overlap.

## The template

A query $q$ has range $R_q$ and slide $S_q$, and its windows are $[jS_q, jS_q + R_q)$ for $j = 0, 1, 2, \ldots$. A *cut* is a time at which a slice ends and the next begins. There are two cutting rules.

- *Edges*: cut at every window start $jS_q$ and every window end $jS_q + R_q$ of every query. Each window is then a union of whole slices.
- *Starts*: cut only at window starts. A window end then falls inside a slice. For input in timestamp order this is enough: when the stream reaches the end $e$ of a window, the open slice holds exactly the tuples from its start up to $e$. This is the rule of Cutty (Carbone et al. 2016), which this page calls *Cutty slicing*.

For in-order input, with $\oplus$ the combine and lift the map from a value to a partial:

```pseudo id=main
INSERT(t, v)                          ▷ timestamps do not decrease
L1  EMIT-UNTIL(t)                     ▷ finish every window that ends at or before t
L2  CLOSE-UNTIL(t)
L3  cur ← cur ⊕ lift(v)               ▷ the partial of the open slice

EMIT-UNTIL(t)
L4  for each window end e ≤ t, in time order, of a query with range R do
L5      CLOSE-UNTIL(e)
L6      acc ← the ⊕ of the closed slices that start at or after e - R, in time order; then acc ← acc ⊕ cur if the open slice starts before e
L7      emit the window [e - R, e) with acc; drop the closed slices that no open window can use

CLOSE-UNTIL(t)
L8  while the next cut after the start of the open slice is at most t do
L9      move the open slice to the list of closed slices; open an empty slice at that cut
```

With the edges rule, line L5 always closes the slice that ends at $e$, so the second part of line L6 never applies. With the starts rule, it applies whenever $e$ is not also a window start.

**Why it works (theorem).** Every window start is a cut under both rules, so each window $[e - R, e)$ begins at a slice boundary. Under the edges rule it also ends at one, and it is the union of the closed slices that start in $[e - R, e)$. Under the starts rule, the slices that start in $[e - R, e)$ cover $[e - R, e)$ exactly when the open slice is cut off at $e$. Line L1 runs before any tuple with timestamp $t \ge e$ is added, so the open slice holds only tuples with timestamps below $e$. In both cases line L6 combines, in time order, the partials of disjoint consecutive pieces whose union is the window, and associativity gives the aggregate of the window. Because the pieces are combined in time order, commutativity is not needed for in-order input. The tests check this with string concatenation, which is not commutative.

**Cost.** Let $n$ be the number of tuples, $c$ the number of slices that one window covers, and $m$ the number of windows emitted over all queries.

- *Per tuple*: one $\oplus$, $O(1)$ worst case. A plain method costs one $\oplus$ for each window that contains the tuple, about $\sum_q R_q / S_q$.
- *Per window*: $c$ calls of $\oplus$ with a linear fold, as in the template. With the slice partials kept in [FlatFAT](/flatfat/), a window costs $O(\log s)$ calls, where $s$ is the number of slices kept; with a [two-stacks queue](/two-stacks-queue/) per query, $O(1)$ amortized.
- *Total*: exactly $n + \sum_{\text{windows}} c$ calls of $\oplus$ for the template; the tests check this count.
- *Memory*: the slices from the earliest open window start to now. For hopping windows this is the slices of the longest range, about $\max_q R_q$ divided by the mean slice length.
- *Number of slices*: in a period of the least common multiple of the slides, the edges rule makes one slice per distinct start or end, the starts rule one per distinct start. A single query with $S$ dividing $R$ gets $R / S$ slices per window under both rules; panes would make $R / \gcd(R, S) = R / S$ too, but for $S$ not dividing $R$ the starts rule needs $\lceil R / S \rceil$ slices per window and panes need $R / \gcd(R, S)$.

**Late data.** The template needs input in timestamp order. With out-of-order input and a watermark, Scotty (Traub et al. 2021) keeps the slices of the windows that are still open, adds a tuple that arrives behind the newest slice to the slice of its timestamp, and changes the slices when the tuple changes the windows: a late tuple can join two session windows, which merges their slices, or start a new session in a gap, which splits a slice. If the aggregate is commutative, the slice partial is updated in place; if not, or if a split falls inside a slice, the slice must keep its tuples, and Scotty keeps them only when the workload needs it. A tuple that arrives after the watermark has passed the end of all its windows is late and is dropped, or is used to send corrected results, by the same policies as in the [Dataflow model](/dataflow-model/). The starts rule does not work for such input: a window end inside a slice needs the partial up to that end, and a late tuple before the end can arrive after the partial has moved on.

## Classic examples

**Two queries on one stream.** $Q_1$ has $R = 6$, $S = 4$, and $Q_2$ has $R = 5$, $S = 3$. The tuples (time, value) are (0, 3), (1, 5), (3, 2), (4, 7), (5, 1), (7, 4), (8, 6), (9, 2), (11, 8), (12, 3) and (13, 5). In $[0, 24)$, the window starts are 0, 3, 4, 6, 8, 9, 12, 15, 16, 18, 20 and 21, and the window ends are 5, 6, 8, 10, 11, 14, 17, 18, 20, 22 and 23.

| rule | cuts in $[0, 24)$ | slices |
|---|---|---|
| edges | the 19 distinct starts and ends | 19 |
| starts (Cutty) | the 12 starts | 12 |
| shared panes, $\gcd(2, 1) = 1$ | every time unit | 24 |

The edges slices up to time 14 are [0, 3) with sum 8, [3, 4) with 2, [4, 5) with 7, [5, 6) with 1, [6, 8) with 4, [8, 9) with 6, [9, 10) with 2, [10, 11) with 0, [11, 12) with 8 and [12, 14) with 8. The window $[4, 10)$ of $Q_1$ is the slices from 4 to 10: $7 + 1 + 4 + 6 + 2 = 20$. The window $[3, 8)$ of $Q_2$ is $2 + 7 + 1 + 4 = 14$. Under the starts rule the slices are [0, 3), [3, 4), [4, 6), [6, 8), [8, 9), [9, 12) and [12, 15) up to 15, and the window $[0, 5)$ of $Q_2$ is $8 + 2$ plus the open slice [4, 6) at the moment the stream reaches 5, which holds only the 7, so $17$.

The nine windows that start before time 14 have the sums 18, 20, 24 and 8 for $Q_1$ and 17, 14, 12, 18 and 8 for $Q_2$, the same as a recomputation of each window from scratch. Their windows hold 34 tuple occurrences in all. The template makes 49 calls of $\oplus$ with the edges rule and 38 with the starts rule: 11 for the tuples, and 38 or 27 for the slices of the windows. On this sparse example a plain method, with 34 additions, is cheaper, because each slice holds about one tuple. With 100 tuples per time unit, the plain method needs about 100 times as many additions, and the slice counts stay the same.

**Panes as slices.** For one query, the edges rule cuts at the multiples of $S$ and at the multiples of $S$ plus $R$. All of these are multiples of $\gcd(R, S)$, so slicing never makes more slices than panes, and it makes fewer when not every multiple of the gcd is a boundary: for $R = 10$ and $S = 4$, the cuts in a period of 4 are at 0 and 2, so slicing gives slices of length 2, the same as panes, but for $R = 10$ and $S = 6$ the cuts in a period of 6 are at 0 and 4, which gives slices of lengths 4 and 2 where panes use three slices of length 2.

**Session windows.** A session window of gap $g$ ends when no tuple arrives for $g$ time units. A slicer cuts a new slice when a gap of $g$ is seen, and the slice is the session. With in-order input this is one partial per session. With out-of-order input, a late tuple that falls in a gap between two sessions and is closer than $g$ to both merges them, and Scotty merges their slices.

## Variations

- **Paired windows** (Krishnamurthy, Wu and Franklin 2006). For one query, cut each slide into two fragments, of lengths $R \bmod S$ and $S - (R \bmod S)$, so that each slide has at most two slices. For many queries, take the union of their cuts. These are the edges cuts of the query.
- **Cutty** (Carbone et al. 2016). Windows are given by user functions that say when a window begins and ends, as long as the start of a window is known when its first tuple arrives. Slices begin only at window starts.
- **General stream slicing** (Scotty, Traub et al. 2021). One slicer for all the windows of a stream: context-free windows (tumbling, hopping) and context-aware windows (sessions, and windows that end on a punctuation), measures in time and in tuple counts, in-order and out-of-order input. It chooses, from the aggregates and windows, whether slices must keep their tuples and whether they must support split and merge.
- **Combining slices fast.** Keep the slice partials in [FlatFAT](/flatfat/), a [two-stacks queue](/two-stacks-queue/) or a [DABA queue](/daba-queue/), so that the cost per window does not grow with $c$.
- **Shared selections.** Krishnamurthy et al. also share work between queries whose filters differ, by cutting the data into fragments by the filters that each tuple passes. This is outside the time slicing of this page.

## Pitfalls

- **Few tuples per slice.** As the example shows, many queries with different slides can give slices that hold one tuple or none. The work per window then grows with the number of slices, and the plain method can be cheaper. Use a tree over the slices.
- **The starts rule needs order.** Cutting only at starts uses the running partial of the open slice at the moment of a window end. Out-of-order input breaks this; use the edges rule, or keep the tuples of the open slice.
- **Late data.** A heuristic watermark can be too fast, and a late tuple can change a window that has already been emitted. State the policy for each query. Session windows make this worse, because a late tuple can merge two sessions that were both emitted.
- **Count-based windows out of order.** A window of the last $N$ tuples in timestamp order changes its contents when a late tuple arrives, because every later window moves by one tuple. The slice boundaries in counts shift, so slices must keep tuples to be split.
- **Holistic aggregates.** Median and quantiles have no constant-size partial, so a slice holds a sorted run or a summary, and combining $c$ slices is not $O(c)$.
- **Different aggregates.** Queries can share slices only if their partials can be derived from one stored partial, for example a (sum, count) pair for sum, count and average. Max and sum need two partials per slice.

## Exercises

1. For the queries $(R, S) = (10, 4)$ and $(9, 6)$, list the cuts of the edges rule and of the starts rule in $[0, 24)$. How many slices does each window cover under each rule?
2. Prove that for one query with $S$ dividing $R$, the edges rule and the starts rule give the same cuts. Then give a query for which the starts rule makes fewer slices.
3. Give an out-of-order stream, a watermark and a window for which the starts rule gives a wrong result while the edges rule gives the right one.
4. A query has session windows with gap 3. The tuples arrive with timestamps 1, 2, 9, 10 and then, late, 5. Show the sessions and slices before and after the late tuple, and say which emitted results change.

## References
