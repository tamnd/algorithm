---
tag: 0B550K
kind: technique
slug: panes-window-aggregation
name: Pane-based window aggregation
aliases:
- pane-based aggregation
area: databases/stream-and-incremental-processing
level: advanced
summary: "Split a sliding window of range R and slide S into panes of length gcd(R, S), aggregate each pane once, and compute each window from its R / gcd(R, S) pane partials."
prereqs: [hopping-window, greatest-common-divisor, group-by-aggregation, monoid]
see_also: [stream-slicing, flatfat, sliding-window-aggregation, two-stacks-queue, daba-queue, tumbling-window, session-window, event-time-watermark]
sources:
  - paper: doi:10.1145/1058150.1058158
    title: Jin Li, David Maier, Kristin Tufte, Vassilis Papadimos and Peter A. Tucker, No pane, no gain, efficient evaluation of sliding-window aggregates over data streams, SIGMOD Record 34(1), 2005, pages 39 to 44
    locator: "Section 3.1 (the pane-level sub-query PLQ and the window-level sub-query WLQ, with pane length gcd(RANGE, SLIDE)), Section 3.2 (distributive, algebraic and holistic aggregates, and differential aggregates) and Section 3.3 (when panes give no gain, and holistic aggregates such as heavy hitters)"
  - paper: "Jin Li, David Maier, Kristin Tufte, Vassilis Papadimos and Peter A. Tucker, Semantics and evaluation techniques for window aggregates in data streams, Proceedings of ACM SIGMOD 2005"
    title: Semantics and evaluation techniques for window aggregates in data streams
    locator: the companion paper with window ids, which assigns tuples to windows without buffering them (general locator)
  - paper: doi:10.1145/1142473.1142543
    title: Sailesh Krishnamurthy, Chung Wu and Michael J. Franklin, On-the-fly sharing for streamed aggregation, Proceedings of ACM SIGMOD 2006, pages 623 to 634
    locator: paired windows, which cut a window into two fragments of lengths S mod R and the rest, and need fewer partials than panes
---

Pane-based aggregation, of Li, Maier, Tufte, Papadimos and Tucker (2005), computes a sliding-window aggregate with range $R$ and slide $S$ by cutting the stream into *panes* of length $g = \gcd(R, S)$: each tuple is added once to the partial aggregate of its pane, and each window is the combination of its $k = R / g$ pane partials. It is a technique for one query with fixed $R$ and $S$. [Stream slicing](/stream-slicing/) generalizes it to slices of unequal length and to many queries and window types at once, and [FlatFAT](/flatfat/) is a data structure that combines the partials of a window in $O(\log n)$ operator calls instead of $k$. The [sliding window aggregation](/sliding-window-aggregation/) page states the general problem, and the [two-stacks queue](/two-stacks-queue/) and the [DABA queue](/daba-queue/) solve it for windows that slide one item at a time.

## In plain words

You must report, every 4 minutes, the total sales of the last 6 minutes. The plain way adds each sale to every report that covers it, and the reports overlap, so many sales are added twice. Panes avoid this. Cut time into blocks of 2 minutes, the largest length that fits both 6 and 4 an exact number of times. Keep one running total per block. Each sale goes into exactly one block. When a report is due, add up the last three block totals. Each sale is touched once, and each report costs three additions, however many sales there were.

## When it applies

- The windows are sliding windows in one time domain with a fixed range $R$ and a fixed slide $S$, both integers in the unit of the timestamps: window $j$ is the interval $[jS, jS + R)$ for $j = 0, 1, 2, \ldots$. These are the [hopping windows](/hopping-window/) of other pages, and with $R = S$ the [tumbling windows](/tumbling-window/).
- The aggregate is *bounded*, which Li et al. define as distributive or algebraic in the sense of Gray et al.: it has a partial state of constant size with a lift, an associative combine and a final step. Sum, count, max, min and average (as a sum and a count) are bounded. Median, quantiles and mode are *holistic* and have no partial of constant size.
- The stream gives each pane many tuples. The gain comes from doing one combine per tuple instead of $R / S$ of them, so it is largest when the windows overlap a lot and the tuples are dense.

## The template

The page uses $R$ for the range and $S$ for the slide, both in time units, $g = \gcd(R, S)$ for the pane length and $k = R / g$ for the number of panes per window. Pane $i$ is $[ig, (i + 1)g)$. The aggregate has a lift, a combine $\oplus$ with an identity, and a final step lower. A watermark $w$ says that no more tuples with a timestamp below $w$ are expected, and a pane closes when $w$ reaches its end.

```pseudo id=main
PANES(R, S)                          ▷ windows [jS, jS + R) for j = 0, 1, 2, ...
L1  g ← gcd(R, S);  k ← R / g;  next ← 0          ▷ next is the first pane that is not closed
L2  open ← an empty map from pane id to partial;  last ← an empty queue of partials

INSERT(t, v)                         ▷ the pane-level query
L3  i ← ⌊t / g⌋
L4  if i < next then count the tuple as late, drop it and return
L5  open[i] ← open[i] ⊕ lift(v)                    ▷ a missing entry is the identity

ADVANCE(w)                           ▷ the watermark: no more tuples with a timestamp below w
L6  while (next + 1) · g ≤ w do
L7      append open[next] (the identity if missing) to last; remove it from open; if last holds k + 1 partials, drop the oldest
L8      e ← (next + 1) · g;  next ← next + 1
L9      if e ≥ R and (e - R) mod S = 0 then        ▷ a window ends at e
L10         emit the window [e - R, e) with lower(⊕ of the k partials in last)    ▷ the window-level query
```

Li et al. state the technique as a rewrite of the query: the *pane-level sub-query* (PLQ) is a [tumbling window](/tumbling-window/) aggregate with range and slide $g$, and the *window-level sub-query* (WLQ) is an aggregate over the stream of pane results with range $k$ panes and slide $S / g$ panes. For count, the PLQ is count and the WLQ is sum; for max, both are max. Lines L3 to L5 are the PLQ and lines L9 and L10 are the WLQ.

**Why it works.** Three facts, each a theorem.

1. *Each window is exactly $k$ consecutive panes.* Both ends $jS$ and $jS + R$ are multiples of $g$, because $g$ divides $S$ and $R$. So the window is the union of the panes from $jS / g$ to $jS / g + k - 1$.
2. *No longer pane works for all windows.* A pane length $h$ that puts every window boundary on a pane boundary must divide $jS$ and $jS + R$ for every $j$, so it divides $S$ (take $j = 1$ and $j = 0$ for the starts) and $R$ (take the two ends of window 0), and so it divides $g$.
3. *The output is the window aggregate.* By fact 1 and line L7, when a window ends at $e$ the queue holds the partials of panes $e / g - k$ to $e / g - 1$, which are its panes. Each partial is the $\oplus$ of the lifted values of its tuples, so by associativity the $\oplus$ of the $k$ partials is the $\oplus$ over all tuples of the window. Tuples can arrive in any order inside a pane, so $\oplus$ must also be commutative unless the input is in timestamp order.

**Cost.** Let $n$ be the number of tuples and $m$ the number of windows emitted.

- *Per tuple*: one $\oplus$ and one map lookup, $O(1)$ worst case. A plain method that adds each tuple to every open window costs $R / S$ combines per tuple when $S$ divides $R$, and $\lceil R / S \rceil$ or $\lfloor R / S \rfloor$ otherwise.
- *Per window*: $k$ combines, worst case. In total, exactly $n + mk$ calls of $\oplus$ when each combine starts from the identity; the tests check this count.
- *Per pane*: $O(1)$ to close it, even if it is empty.
- *Memory*: the last $k$ closed partials plus the open panes, independent of the number of tuples in a window. With in-order input there is one open pane, so at most $k + 1$ partials. With a watermark that lags the largest timestamp by $D$, about $D / g + 1$ panes are open.

**Late data.** The technique needs to know when a pane is complete. The original paper assumes input in timestamp order, so a pane closes when the first tuple of a later pane arrives. With out-of-order input, a pane closes when the watermark passes its end, as above. A tuple that arrives after its pane has closed is late. The template drops it and counts it. The other choice is to reopen the pane, update its partial and emit a corrected result for each of the windows that contain it, which are at most $\lceil R / S \rceil$; this needs the pane partials of those windows to be kept until the corrections are no longer wanted. If the disorder is at most $D$ (each tuple arrives after only tuples whose timestamps are at most $D$ above its own) and the watermark is the largest timestamp seen minus $D$, no tuple is late. *Proof.* The watermark before a tuple $x$ is at most $t_x + D - D = t_x$, and the pane of $x$ ends after $t_x$, so it is still open. $\square$

## Classic examples

**The example from the plain words.** $R = 6$, $S = 4$, so $g = 2$ and $k = 3$. The tuples (time, value) are (0, 3), (1, 5), (3, 2), (4, 7), (5, 1), (7, 4), (8, 6), (9, 2), (11, 8), (12, 3) and (13, 5).

| pane | interval | tuples | sum | max |
|---|---|---|---|---|
| 0 | [0, 2) | 3, 5 | 8 | 5 |
| 1 | [2, 4) | 2 | 2 | 2 |
| 2 | [4, 6) | 7, 1 | 8 | 7 |
| 3 | [6, 8) | 4 | 4 | 4 |
| 4 | [8, 10) | 6, 2 | 8 | 6 |
| 5 | [10, 12) | 8 | 8 | 8 |
| 6 | [12, 14) | 3, 5 | 8 | 5 |

| window | panes | sum | max |
|---|---|---|---|
| [0, 6) | 0, 1, 2 | 8 + 2 + 8 = 18 | 7 |
| [4, 10) | 2, 3, 4 | 8 + 4 + 8 = 20 | 7 |
| [8, 14) | 4, 5, 6 | 8 + 8 + 8 = 24 | 8 |
| [12, 18) | 6, 7, 8 | 8 | 5 |

Pane 2 is in two windows, and its partial is computed once. The three full windows hold 15 tuple occurrences, so the plain method adds 15 values; panes add the 11 tuples once and then combine 3 partials per window. Recomputed from scratch, the sums of the windows are 18, 20, 24 and 8, the same.

**Count and average.** For count, the PLQ counts the tuples of each pane and the WLQ adds the counts. For average, the partial is the pair (sum, count), the WLQ adds the pairs, and the final step divides. The implementation returns the pair, so that the tests compare exact integers.

**A query that is not helped.** With $R = 7$ and $S = 3$, $g = 1$ and $k = 7$: every time unit is a pane, and each window combines 7 partials. If a time unit holds about one tuple, this is no better than the plain method. Li et al. name this case, with very many groups and with slow streams, as the cases with no gain.

## Variations

- **Differential aggregates.** If $\oplus$ has an inverse (sum, count, average), keep a running window value: at each window, add the new panes and subtract the panes that left. This costs $S / g$ additions and $S / g$ subtractions per window instead of $k$ combines. Li et al. call such aggregates differential. Max has no inverse.
- **A tree or a queue over the panes.** For an aggregate that is associative but not invertible, such as max, keep the pane partials in a [two-stacks queue](/two-stacks-queue/), a [DABA queue](/daba-queue/) or a [FlatFAT](/flatfat/) instead of combining $k$ partials each time. Each window then costs $O(1)$ amortized, $O(1)$ worst case, or $O(\log k)$ operator calls.
- **Group-by.** With a Group By clause, each group has its own panes. The memory is $k + 1$ partials per group, and a pane must be closed for every group, which costs time in proportion to the number of groups even when a group has no tuples.
- **Holistic aggregates.** For a holistic aggregate, the pane partial must be a summary that can be merged, for example the counts of each value for a heavy-hitter query, as in Section 3.3 of the paper. The partial then has no constant bound.
- **Paired windows and slicing.** Krishnamurthy, Wu and Franklin (2006) cut each window of range $R$ and slide $S$ into two fragments of alternating lengths $R \bmod S$ and $S - (R \bmod S)$, so each slide has at most two partials instead of $S / g$. With several queries, the fragments of all queries are cut at the union of their boundaries. This is the start of [stream slicing](/stream-slicing/).
- **Count-based windows.** With $[\text{Rows } N \text{ Slide } L]$ the same scheme works on tuple positions, with panes of $\gcd(N, L)$ tuples, as long as the tuples arrive in order.

## Pitfalls

- **Coprime range and slide.** If $\gcd(R, S) = 1$, panes have the length of one time unit and each window combines $R$ partials. Choose the time unit with care, or use paired windows or slicing.
- **Empty panes.** The loop at line L6 closes every pane, also empty ones. On a sparse stream with a fine time unit this costs more than the tuples do. An implementation can jump over empty panes, but it must still emit the windows that end in the gap.
- **Late data.** A heuristic watermark can be too fast. Then a tuple arrives after its pane has closed, and the results of the windows that contain it are wrong unless the system corrects them. State the policy: drop and count, or update and re-emit.
- **Holistic aggregates.** Median and quantiles cannot be split into constant-size partials. A pane of sorted values or a mergeable summary works, but the cost bounds above no longer hold.
- **Windows that are not aligned.** The template assumes that window $j$ starts at $jS$. If the windows start at an offset $o$, cut the panes from $o$ as well. [Session windows](/session-window/) have no fixed boundaries, so panes do not apply to them; stream slicing handles them.
- **Commutativity.** With out-of-order input, tuples enter a pane in arrival order. A combine that is associative but not commutative, such as the concatenation of strings, gives a wrong partial. Sort each pane by timestamp first, or use a commutative aggregate.

## Exercises

1. For $R = 10$ and $S = 4$, give $g$, $k$ and the panes of the windows $[0, 10)$, $[4, 14)$ and $[8, 18)$. How many partials does each window combine, and how many would paired windows need?
2. Show that with a differential aggregate the cost per window is $S / g$ updates in each direction. Write the update of the running sum and say which pane leaves the window when the window that ends at $e$ is emitted.
3. A stream has 3 tuples per time unit, $R = 60$ and $S = 1$. Compare the number of combines per window of the plain method, of panes, and of panes in a [two-stacks queue](/two-stacks-queue/).
4. Prove that if the disorder of the stream is at most $D$, a watermark of the largest timestamp seen minus $D$ makes no tuple late, and give a stream with disorder $D + 1$ on which a tuple is late.

## References
