---
tag: GFWMKW
kind: data-structure
slug: timing-wheel
name: Timing wheel
aliases:
- hashed timing wheel
- hierarchical timing wheel
area: systems/scheduling
level: advanced
summary: A circular array of buckets, one per clock tick, that holds timers. Starting and stopping a timer take O(1) time, against O(log n) for a heap; hashed and hierarchical forms handle long intervals.
model: word-ram
history:
  year: 1987
  people: [George Varghese, Anthony Lauck]
  note: Varghese and Lauck described the simple, hashed and hierarchical timing wheels at SOSP 1987, and published a longer version in IEEE/ACM Transactions on Networking in 1997.
prereqs: [circular-buffer, priority-queue]
see_also: [calendar-queue, bucket-queue, binary-heap, hash-table, event-driven-simulation, earliest-deadline-first, round-robin, cpu-scheduling]
sources:
  - paper: "George Varghese and Anthony Lauck, Hashed and Hierarchical Timing Wheels: Data Structures for the Efficient Implementation of a Timer Facility, Proceedings of the 11th ACM Symposium on Operating Systems Principles (SOSP), 1987"
    title: "Hashed and Hierarchical Timing Wheels: Data Structures for the Efficient Implementation of a Timer Facility"
    locator: pages 25 to 38 (the timer module model, Schemes 1 to 7, the simple wheel, the hashed wheels and the hierarchical wheels)
  - paper: "George Varghese and Anthony Lauck, Hashed and Hierarchical Timing Wheels: Efficient Data Structures for Implementing a Timer Facility, IEEE/ACM Transactions on Networking 5(6), 1997"
    title: "Hashed and Hierarchical Timing Wheels: Efficient Data Structures for Implementing a Timer Facility"
    locator: pages 824 to 834 (the journal version, with the analysis of the hashed and hierarchical schemes)
  - book: isbn:9780120884773
    title: George Varghese, Network Algorithmics, Morgan Kaufmann, 2005
    locator: Chapter 7, Maintaining Timers (timing wheels, hashed and hierarchical wheels, and BSD callouts)
---

A timing wheel is a data structure for the timers of an operating system or a network protocol: each timer must fire a given number of clock ticks after it is started, and most timers are stopped before they fire. Time is cut into ticks, and the wheel is a circular array of $N$ buckets, one per tick, with a cursor that moves one bucket per tick. A timer that expires at tick $e$ goes into bucket $e \bmod N$, and the cursor finds it there. So starting and stopping a timer take $O(1)$ time, while a [binary heap](/binary-heap/) takes $O(\log n)$. Varghese and Lauck (1987) gave three forms. The *simple wheel* has a bucket for every possible interval. The *hashed wheel* uses fewer buckets, and each timer stores how many more turns of the wheel it must wait. The *hierarchical wheel* uses several wheels, like the seconds, minutes and hours of a clock, and moves a timer to a finer wheel as its time comes near.

## In plain words

Think of a clock face with 8 slots and a hand that moves one slot each tick. To set an alarm for 3 ticks from now, put a note in the slot that the hand will reach in 3 ticks. At each tick, the hand looks only at its slot and rings the alarms there. To cancel an alarm, take its note out of its slot.

An alarm for 11 ticks from now goes in the slot 3 ahead too, but with a mark that says "wait one more turn". When the hand passes, it lowers the mark instead of ringing.

A clock with an hour hand and a minute hand does the same with fewer slots. An alarm for next week waits on the day wheel. On its day, it moves to the hour wheel, then to the minute wheel, and then it rings.

## The abstract type

A timer facility has four operations, in the model of Varghese and Lauck:

- START-TIMER$(id, j)$: make timer $id$ expire $j \ge 1$ ticks from now.
- STOP-TIMER$(id)$: cancel timer $id$ before it expires.
- PER-TICK-BOOKKEEPING: advance the clock by one tick, and find the timers that expire at the new time.
- EXPIRY-PROCESSING: run the action of an expired timer, for example resend a packet.

The time is an integer count of ticks. A timer expires exactly at the tick $e = \mathit{now} + j$, never earlier and never later. Timers that expire at the same tick fire in the order in which they were started, in this version. This is a [priority queue](/priority-queue/) with integer keys and a clock that only moves forward, which is why buckets can replace comparisons.

## Representation

The hashed wheel (Scheme 6 of the paper) has these parts:

- an array $B[0 \ldots N - 1]$ of buckets, used as a [circular buffer](/circular-buffer/) of ticks; each bucket is a doubly linked list of entries $(id, \mathit{rounds})$;
- the current time $\mathit{now}$; the cursor is the bucket $\mathit{now} \bmod N$;
- a handle $h[id]$ that points to the entry of each running timer, so that STOP-TIMER can unlink it without a search; the handle is kept by the caller, or in a [hash table](/hash-table/).

The invariant: a timer with expiry $e > \mathit{now}$ is in bucket $e \bmod N$, and its count is $\mathit{rounds} = \lfloor (e - \mathit{now} - 1)/N \rfloor$, the number of times the cursor will visit that bucket before tick $e$.

The **simple wheel** (Scheme 4) is the case in which $N$ is larger than every interval, so every count is 0.

The **hierarchical wheel** (Scheme 7) has $L$ wheels of $N$ buckets each. Write times in base $N$. A timer with expiry $e > \mathit{now}$ is on the highest wheel $k$ at which the digits of $e$ and $\mathit{now}$ differ, in bucket $\mathrm{digit}_k(e)$. Timers that differ from $\mathit{now}$ in a digit at or above $L$ wait in an overflow list.

## Operations

```pseudo id=main
START-TIMER(id, j)                         ▷ j ≥ 1 ticks from now
L1  e ← now + j
L2  b ← e mod N
L3  put (id, rounds = ⌊(j − 1)/N⌋) into B[b]; h[id] ← its entry

STOP-TIMER(id)
L4  unlink h[id] from its bucket; delete h[id]

PER-TICK-BOOKKEEPING()
L5  now ← now + 1; b ← B[now mod N]
L6  for each entry (id, rounds) in b do
L7      if rounds = 0 then unlink it and do EXPIRY-PROCESSING(id)
L8      else rounds ← rounds − 1
```

**Hierarchical wheel.** START-TIMER computes the digits of $e$ and puts the timer on the highest wheel at which they differ from those of $\mathit{now}$, in $O(L)$ time. STOP-TIMER unlinks it in $O(1)$. PER-TICK-BOOKKEEPING first adds 1 to $\mathit{now}$. Then, for $k = L - 1$ down to 1, if $\mathit{now}$ is a multiple of $N^k$, it empties the bucket $\mathrm{digit}_k(\mathit{now})$ of wheel $k$ and starts each of its timers again, at its old expiry, on a lower wheel. This step is the *cascade*. If $\mathit{now}$ is a multiple of $N^L$, it does the same with the overflow list first. Then every timer in bucket $\mathrm{digit}_0(\mathit{now})$ of wheel 0 expires.

## Example

**Hashed wheel.** $N = 8$ and $\mathit{now} = 0$. Start A for 3 ticks, B for 11, C for 8 and D for 5.

| timer | expiry $e$ | bucket $e \bmod 8$ | rounds $\lfloor (j-1)/8 \rfloor$ |
|---|---|---|---|
| A | 3 | 3 | 0 |
| B | 11 | 3 | 1 |
| C | 8 | 0 | 0 |
| D | 5 | 5 | 0 |

- At time 2, STOP-TIMER(D) unlinks D from bucket 5.
- Tick 3 visits bucket 3. A has rounds 0, so it expires. B has rounds 1, so line L8 sets it to 0.
- Tick 5 visits bucket 5, which is now empty.
- Tick 8 visits bucket 0, and C expires.
- Tick 11 visits bucket 3 again, and B expires, 11 ticks after its start.

**Hierarchical wheel.** $N = 4$ and $L = 3$, so the wheels count units of 1, 4 and 16 ticks. At time 0, start X for 21 ticks; $21 = 1 \cdot 16 + 1 \cdot 4 + 1$ has the digits $(1, 1, 1)$, and $0$ has $(0, 0, 0)$. The highest digit that differs is digit 2, so X goes into bucket 1 of wheel 2. At tick 16, with digits $(1, 0, 0)$, the bucket 1 of wheel 2 cascades: now X differs first in digit 1, so it goes into bucket 1 of wheel 1. At tick 20, with digits $(1, 1, 0)$, it cascades again into bucket 1 of wheel 0. At tick 21, X expires. It moved twice. The tests replay both examples.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).

1. **Hashed wheel invariant.** Each running timer with expiry $e$ is in bucket $e \bmod N$ with $\mathit{rounds} = \lfloor (e - \mathit{now} - 1)/N \rfloor$. Line L3 sets this count, and at each tick only the visited bucket has its count change, by exactly the 1 of line L8.
2. **Exact firing.** A timer fires at the tick at which its count is 0 when the cursor reaches it, which is the tick $e$ and no other.
3. **Hierarchical invariant.** A timer with $e > \mathit{now}$ is on the highest wheel at which the digits of $e$ and $\mathit{now}$ differ, in bucket $\mathrm{digit}_k(e)$. When the clock reaches a multiple of $N^k$, only the timers in bucket $\mathrm{digit}_k(\mathit{now})$ of wheel $k$ break this, and the cascade moves exactly those.

The tests run random starts and stops on both wheels and on the simple wheel, and check after every tick that the expired timers are the same, in the same order, as for a reference built on a [binary heap](/binary-heap/).

## Complexity

Let $n$ be the number of running timers.

| operation | hashed wheel | hierarchical wheel | binary heap |
|---|---|---|---|
| START-TIMER | $O(1)$ | $O(L)$ | $O(\log n)$ |
| STOP-TIMER | $O(1)$ | $O(1)$ | $O(\log n)$ |
| PER-TICK-BOOKKEEPING | $O(1 + $ the size of the bucket$)$ | $O(1 + $ expired $+$ moved timers$)$ | $O(1 + k \log n)$ for $k$ expired timers |
| space | $O(N + n)$ | $O(LN + n)$ | $O(n)$ |

For the hashed wheel, the work per tick is the length of one bucket. If the expiry times are spread evenly over the buckets, the mean length is $n/N$, so $N$ near $n$ gives $O(1)$ time per tick on average. For the simple wheel every entry in the visited bucket expires, so a tick costs $O(1)$ plus the number of expired timers. For the hierarchical wheel, a timer with an interval below $N^L$ moves at most $L$ times (once from the overflow list and once from each wheel above 0), so the moves cost $O(L)$ per timer in total. The tests check this bound.

## Variants

- **Sorted lists per bucket.** Scheme 5 of the paper keeps each bucket sorted by expiry, so a tick stops at the first entry that is not due, but START-TIMER then costs the length of the bucket.
- **Absolute expiry instead of rounds.** Store $e$ and fire when $e = \mathit{now}$; the scan of a bucket is the same, and no count needs to change.
- **Lazy cascading.** The Linux timer wheel since version 4.8 does not cascade: a timer stays on its coarse wheel and fires late, by up to the width of a bucket on that wheel. This trades exact firing for fewer moves, and it suits time-outs that are almost always stopped.
- **Calendar queue.** A [calendar queue](/calendar-queue/) is a wheel for real-valued event times, with a bucket width that adapts to the events.
- **Tickless operation.** A system that sleeps between timers asks the wheel for the next non-empty bucket and programs the hardware for it, instead of taking every tick.

## When to use it

Use a timing wheel when there are many timers, most of them are stopped before they expire, and a resolution of one tick is enough: retransmission and keep-alive timers of TCP, time-outs in network servers, and time slices in a scheduler. Netty, Kafka and the Linux kernel use wheels for this. Use a [binary heap](/binary-heap/) or a balanced tree when timers have arbitrary real times, when they are few, or when the clock jumps far ahead, because a wheel must step through every tick between.

## Pitfalls

- **Off by one in the rounds.** A timer for exactly $N$ ticks lands in the current bucket of the cursor, and it must wait one full turn, not fire at once. The count $\lfloor (j - 1)/N \rfloor$ handles this, and the count $\lfloor j/N \rfloor$ fires $N$ ticks late.
- **A start inside the expiry processing.** An action that starts a timer for one tick adds an entry to the next bucket, not to the bucket being scanned. Starting a timer for 0 ticks must be refused or run at once.
- **Stopping without a handle.** If STOP-TIMER must search the bucket for the timer, it costs the length of the bucket, not $O(1)$.
- **Cascading in the wrong order.** In the hierarchical wheel, cascade the higher wheels first. A timer that moves down from wheel 2 can land in the very bucket of wheel 1 that must cascade at the same tick.
- **Large clock jumps.** After a long sleep, the wheel must replay every missed tick, or jump straight to the next non-empty bucket.

## Implementations

## History

Varghese and Lauck, at Digital Equipment Corporation, studied the timer modules of operating systems and network protocols, where most timers are stopped before they fire. At SOSP 1987 they described seven schemes, from an unordered list to the hierarchical wheels, and showed that the hashed and hierarchical wheels give $O(1)$ start and stop. They noted that the hierarchical scheme works like a digital clock, and that the hashed scheme is a hash table on the expiry time. A longer version appeared in IEEE/ACM Transactions on Networking in 1997. Timing wheels then spread into the BSD and Linux kernels and into network libraries.

## References
