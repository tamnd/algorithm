---
tag: CZJZK8
kind: data-structure
slug: calendar-queue
name: Calendar queue
aliases:
- calendar queues
area: data-structures/heaps
level: advanced
summary: Bucket-based queue for discrete-event simulation that expects near-uniform event times.
implements: [priority-queue]
model: real-ram
prereqs: [bucket-queue, priority-queue]
see_also: [bucket-queue, event-driven-simulation, timing-wheel, radix-heap, binary-heap, priority-queue, bucket-sort, skip-list]
sources:
  - paper: "Randy Brown, Calendar queues: a fast O(1) priority queue implementation for the simulation event set problem, Communications of the ACM 31(10), 1988"
    locator: pages 1220 to 1227, the structure, the dequeue scan, and the resize rule with the width estimate
  - paper: "Wee Tiong Tang, Rick Siow Mong Goh and Ian Li-Jin Thng, Ladder queue: an O(1) priority queue structure for large-scale discrete event simulation, ACM Transactions on Modeling and Computer Simulation 15(3), 2005"
    locator: the description of the cases where the calendar queue degrades and the multi-level fix
---

A calendar queue is a [priority queue](/priority-queue/) for events with real-valued times, made for the event set of a [discrete-event simulation](/event-driven-simulation/). It is a [bucket queue](/bucket-queue/) that wraps around, like a desk calendar of one year: there are $N$ buckets, each one "day" of width $w$, and an event at time $t$ goes into the bucket $\lfloor t/w \rfloor \bmod N$, kept in sorted order. To find the next event, the queue looks at the current day, and if that bucket holds no event of this year, it moves on to the next day. Brown (1988) chose $N$ and $w$ so that each bucket holds about one event of the current year, and resized the array as the queue grows and shrinks; then insert and extract-min take $O(1)$ expected time when event times are spread evenly. Unlike a heap, it has no $O(\log n)$ guarantee: skewed times can make it scan or sort large buckets.

## In plain words

Think of a desk calendar with one page per day for a year. To note an event, write it on the page of its day, in time order; events of next year go on the same page, below. To find the next event, look at today's page. If it has an event for this year, that is the next one. Else turn the page and look at the next day.

If the pages are the right size, each page has about one event, so writing and finding take a few steps no matter how many events there are. If there are many more events than pages, the pages get crowded; if far fewer, you turn many empty pages. So the calendar is rebuilt with more or fewer pages, and a new page size, when the number of events doubles or halves.

## The abstract type

A calendar queue implements the min-[priority queue](/priority-queue/) for events with real keys, the times: INSERT$(e, t)$ and EXTRACT-MIN, which removes and returns an event of smallest time. Simulations call them as a *hold*: extract the next event, then insert one or more new events a little later. Events with equal times leave in the order of arrival in this version.

## Representation

- An array $B[0 \ldots N - 1]$ of buckets. Each bucket is a list of events sorted by time, then by arrival.
- The width $w > 0$ of a bucket. The *virtual bucket* of a time is $\mathrm{vb}(t) = \lfloor t/w \rfloor$, and the event lives in $B[\mathrm{vb}(t) \bmod N]$. A *year* is $N$ consecutive virtual buckets, of total length $Nw$.
- A current virtual bucket $V$, with the invariant that $\mathrm{vb}(t) \ge V$ for each event in the queue. The current bucket is $B[V \bmod N]$.

Brown keeps the time of the last event and the top of the current bucket instead of $V$; the integer $V$ is the same thing and avoids rounding errors when the top is updated by repeated additions of $w$.

## Operations

```pseudo id=main
INSERT(e, t)
L1  i ← vb(t) mod N
L2  insert (t, e) into the sorted list B[i]
L3  if the queue was empty or vb(t) < V then V ← vb(t)
L4  n ← n + 1; if n > 2N then RESIZE(2N)

EXTRACT-MIN()
L5  if n = 0 then error "underflow"
L6  repeat N times                         ▷ at most one year
L7      if B[V mod N] is not empty and vb(its first time) = V then
L8          remove the first (t, e) of B[V mod N]; n ← n − 1; if n < N/2 then RESIZE(N/2)
L9          return (e, t)
L10     V ← V + 1
L11 (t, e) ← the smallest first element over all buckets      ▷ direct search
L12 V ← vb(t); remove it, as in line L8, and return (e, t)

RESIZE(N′)
L13 take all events out; N ← N′
L14 sample the first 25 events, and their gaps g, with mean ḡ
L15 w ← 3 × the mean of the gaps g ≤ 2ḡ; put the events back; V ← the least vb(t)
```

**Extract-min.** The first event of the current bucket is the minimum if it belongs to the current year, which is the test $\mathrm{vb}(t) = V$ of line L7. Else no event has the virtual bucket $V$, and line L10 moves to the next day. If a whole year passes with no event, the queue is sparse compared with the calendar; line L11 then finds the minimum by looking at the first event of each bucket, and jumps $V$ to it.

**Resize.** Brown doubles $N$ when the queue has more than $2N$ events and halves it when it has fewer than $N/2$. The new width is three times the average gap between the first events of the queue, where gaps more than twice the average are left out as outliers. The aim is a few events per day near the front of the queue, where the scan happens. A resize costs $O(n)$, and it happens only after $\Theta(N)$ inserts or extracts since the last one, so its amortized cost is $O(1)$.

## Example

Take $N = 4$, $w = 1$, and no resize. Insert $a$ at 0.3, $b$ at 2.6, $c$ at 1.2, $d$ at 5.1, $e$ at 3.9 and $f$ at 2.2. The event $d$ has $\mathrm{vb} = 5$, so it lives in $B[1]$, one year after $c$.

| step | $B[0]$ | $B[1]$ | $B[2]$ | $B[3]$ | $V$ | result |
|---|---|---|---|---|---|---|
| after the inserts | 0.3 | 1.2, 5.1 | 2.2, 2.6 | 3.9 | 0 | |
| EXTRACT-MIN | | 1.2, 5.1 | 2.2, 2.6 | 3.9 | 0 | $a$ at 0.3 |
| EXTRACT-MIN | | 5.1 | 2.2, 2.6 | 3.9 | 1 | $c$ at 1.2, after one empty day |
| EXTRACT-MIN | | 5.1 | 2.6 | 3.9 | 2 | $f$ at 2.2; 5.1 in $B[1]$ is next year, so the scan moves on |
| EXTRACT-MIN | | 5.1 | | 3.9 | 2 | $b$ at 2.6 |
| EXTRACT-MIN | | 5.1 | | | 3 | $e$ at 3.9 |
| INSERT($g$, 40.0) | 40.0 | 5.1 | | | 3 | $\mathrm{vb}(40.0) = 40$, so $B[0]$ |
| EXTRACT-MIN | 40.0 | | | | 5 | $d$ at 5.1, at $V = 5$ after the days 3 and 4 |
| EXTRACT-MIN | | | | | 40 | $g$ at 40.0: the days 5 to 8 find nothing, so the direct search of line L11 jumps to $V = 40$ |

## Correctness

The structure keeps (B) each event at time $t$ is in the bucket $B[\mathrm{vb}(t) \bmod N]$, which is sorted, and (V) $\mathrm{vb}(t) \ge V$ for each event. Since $\mathrm{vb}$ is non-decreasing in $t$, all events with $\mathrm{vb}(t) = V$ are in $B[V \bmod N]$, before the events of later years, and they are earlier than all other events. So when line L7 succeeds, its event is a minimum; when it fails, no event has the virtual bucket $V$, and $V + 1$ keeps (V). The direct search returns a minimum by (B). The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| INSERT | $O(1 + \ell)$ for a bucket of length $\ell$, plus amortized $O(1)$ for resizes |
| EXTRACT-MIN | $O(1 + s)$ for $s$ days scanned, at most $N$, or $O(N)$ with the direct search; plus amortized $O(1)$ for resizes |
| space | $\Theta(N + n)$; the resize rule keeps $N$ within a factor of about 2 of $n$ |

**Expected $O(1)$.** In the hold model with event gaps drawn from a fixed, smooth distribution, the width rule keeps about three events per day near the front, so a scan visits $O(1)$ days and a sorted insert passes $O(1)$ events on average. Brown's measurements showed nearly constant hold times over a wide range of queue sizes for several such distributions. This is an empirical and average-case claim, not a worst-case bound.

**Bad cases.** If most events cluster in a short interval and a few lie far ahead, the width is set by the cluster or by the outliers. A small width makes a sparse year, so the scan often falls back to the $O(N)$ direct search; a large width puts the cluster into one bucket, and the sorted insert costs $\Theta(n)$. Both can give $\Theta(n)$ per operation.

## Variants

- **Dynamic width.** Later versions recompute the width more often, or from more events, to follow changes in the distribution.
- **Ladder queue.** Tang, Goh and Thng (2005) split crowded buckets into a finer calendar of their own, in a ladder of levels, and keep far-future events in an unsorted list. They report $O(1)$ amortized behaviour for skewed distributions where the calendar queue degrades.
- **Unsorted buckets.** Keeping each bucket unsorted makes insert $O(1)$ and moves the work to the scan of the current bucket.
- **Timing wheel.** A [timing wheel](/timing-wheel/) is the integer, fixed-width form used for timers in operating systems and networks.

## When to use it

Use a calendar queue as the event set of a large discrete-event simulation where the event times spread out evenly and the operations come as holds, which is the setting it was made for. For skewed or unknown distributions, or when a worst-case bound matters, use a [binary heap](/binary-heap/), whose $O(\log n)$ is predictable, or a ladder queue.

## Pitfalls

- **Rounding in the bucket top.** Updating the top of the current bucket by adding $w$ many times drifts; an event can then fail the test of its own day, or pass the test of the wrong day. Compare virtual bucket numbers computed with the same floor function, as here.
- **Events in the past.** Brown's queue assumes that no event is inserted before the last extracted time, which holds in a simulation. If the program can insert earlier events, line L3 must move $V$ back, else such an event is found only one year later.
- **No direct search.** Without lines L11 and L12, a queue whose events all lie more than a year ahead loops over empty years.
- **The width from a few events.** A sample of 25 events near the front can be unrepresentative, for example right after many events with equal times, which give gaps of 0. Then guard against a width of 0.

## Implementations

The Python class `CalendarQueue(nbuckets, width, resize)` keeps the buckets as sorted lists of (time, arrival, event) triples and the integer `v` for $V$. `insert` and `extract_min` follow the pseudocode, `_resize` and `_new_width` follow lines L13 to L15, and `check_invariant` checks (B) and (V). The `resize` flag turns resizing off, which the example uses.

## History

Brown published the calendar queue in the Communications of the ACM in 1988, as an $O(1)$ average-time structure for the simulation event set, and compared it with the heaps and trees that simulation packages used at the time. Its weakness on skewed distributions led to many variants, among them the dynamic calendar queue, the SNOOPy calendar queue and the ladder queue of Tang, Goh and Thng (2005).

## References
