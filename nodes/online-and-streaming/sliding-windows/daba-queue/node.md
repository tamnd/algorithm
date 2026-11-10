---
tag: JMSPSC
kind: data-structure
slug: daba-queue
name: DABA queue
aliases:
- de-amortized banker's aggregation
- DABA
- De-Amortized Banker's Aggregator
area: online-and-streaming/sliding-windows
level: research
summary: A FIFO window aggregator for any associative operator with at most 1, 4 and 3 operator calls per query, insert and evict in the worst case, made by spreading the two-stacks flip over later steps.
solves: [sliding-window-aggregation]
implements: [queue]
model: word-ram
complexity:
  vars: {n: the number of items in the window}
  time: {worst: O(1), amortized: O(1)}
  space: {extra: Θ(n)}
history:
  year: 2017
  people: [Kanat Tangwongsan, Martin Hirzel, Scott Schneider]
  note: DABA was published at DEBS 2017. The extended journal version (VLDB Journal 2021) adds DABA Lite, which stores n + 2 partial aggregates.
prereqs: [two-stacks-queue, monoid, deque, amortized-vs-worst-case]
see_also: [two-stacks-queue, sliding-window-aggregation, real-time-queue, banker-queue, global-rebuilding, min-queue, circular-buffer, count-based-window]
sources:
  - paper: doi:10.1145/3093742.3093925
    title: Kanat Tangwongsan, Martin Hirzel and Scott Schneider, Low-latency sliding-window aggregation in worst-case constant time, DEBS 2017
    locator: pages 66 to 77, the DABA algorithm and its worst-case bound
  - url: https://arxiv.org/abs/2009.13768
    title: Kanat Tangwongsan, Martin Hirzel and Scott Schneider, In-order sliding-window aggregation in worst-case constant time, extended version (VLDB Journal 2021)
    locator: Section 5, DABA (the invariants, fixup, Lemma 8, Theorem 9, and Theorem 10 with 2n space and at most 1, 4 and 3 calls), Section 6, DABA Lite (Theorem 13), Fig. 5 (an example trace)
  - paper: "Chris Okasaki, Simple and efficient purely functional queues and deques, Journal of Functional Programming 5(4), 1995"
    locator: pages 583 to 592, the real-time queue that inspired the incremental reversal
  - paper: doi:10.14778/2752939.2752940
    title: Kanat Tangwongsan, Martin Hirzel, Scott Schneider and Kun-Lung Wu, General incremental sliding-window aggregation, PVLDB 8(7), 2015
    locator: pages 702 to 713, the Reactive Aggregator and FlatFAT, the O(log n) methods that DABA improves for FIFO windows
---

DABA, the De-Amortized Banker's Aggregator, is a first-in first-out window that answers the aggregate of its items under any associative operator $\otimes$ with an identity, a [monoid](/monoid/), with $O(1)$ calls of $\otimes$ per operation in the worst case. It is the [two-stacks queue](/two-stacks-queue/) with the flip done early and spread out: when the front and back parts reach the same length, the back part is reversed one step at a time during the next operations, in the way that Okasaki's [real-time queue](/real-time-queue/) spreads out its reversal. Tangwongsan, Hirzel and Schneider proved that DABA makes at most 1 call per query, 4 per insert and 3 per evict, and stores $2n$ partial aggregates for $n$ items.

## In plain words

You keep a line of values, add at the back, remove at the front, and want a summary of the whole line, such as the largest value or all values glued together in order. The two-pile method is fast on average but sometimes has to rebuild a whole pile at once, and that one step can be very slow. DABA never has a slow step. It keeps the values in one row with six markers that split the row into five parts. Each part stores running summaries in a fixed direction. When the old part and the new part have the same length, DABA starts to turn the new part around, but it does only a fixed small amount of the work in each later step. By the time the old part runs out, the new part is ready.

## The abstract type

The same type as the two-stacks queue: a [queue](/queue/) of monoid values with `insert(v)` at the back, `evict()` at the front, and `query()`, which returns $v_0 \otimes v_1 \otimes \cdots \otimes v_{n-1}$ for the window $v_0, \ldots, v_{n-1}$ from the oldest to the newest, or $1$ when the window is empty. The operator need not be commutative or invertible. This is the FIFO, or in-order, case of [sliding-window aggregation](/sliding-window-aggregation/), where the oldest item always leaves first.

## Representation

The items are in one [deque](/deque/) that supports push at the back, pop at the front and access by position, in $O(1)$ worst-case time; a [circular buffer](/circular-buffer/) works for a window with a known maximum size. Each slot $i$ holds $\mathit{val}(i) = v_i$ and a partial aggregate $\mathit{agg}(i)$. Six positions split the deque:

$$F \le L \le R \le A \le B \le E,$$

where $F$ is the oldest item and $E$ is one past the newest. Write $\Pi(i..j) = v_i \otimes \cdots \otimes v_{j-1}$, with $\Pi(i..i) = 1$. The positions name five sublists, $l_F = [F, L)$, $l_L = [L, R)$, $l_R = [R, A)$, $l_A = [A, B)$ and $l_B = [B, E)$.

**Aggregate invariant.** For each slot $i$:

| sublist | $\mathit{agg}(i)$ | direction |
|---|---|---|
| $l_F = [F, L)$ | $\Pi(i..B)$ | to the end of the front part |
| $l_L = [L, R)$ | $\Pi(i..R)$ | to the end of $l_L$ |
| $l_R = [R, A)$ | $\Pi(R..i+1)$ | from the start of $l_R$ |
| $l_A = [A, B)$ | $\Pi(i..B)$ | to the end of the front part |
| $l_B = [B, E)$ | $\Pi(B..i+1)$ | from the start of the back part |

**Size invariant.** Either the window is empty ($F = B = E$), or

$$L - F = (E - B) + 1 \quad\text{and}\quad R - L = A - R.$$

The front part $[F, B)$ plays the role of the front stack of Two-Stacks, and $l_B$ the role of the back stack. The front part is longer than the back part by $|l_L| + |l_R| + |l_A| + 1$, which is the number of steps left in the current reversal plus one. $l_L$ and $l_R$ are the old front and the old back during a reversal, and $l_A$ is the accumulator: the part of the old back whose aggregates already point to the right. Write $\Pi_F, \Pi_L, \Pi_R, \Pi_A, \Pi_B$ for the aggregate of each sublist, read from one slot, or $1$ when it is empty: $\Pi_F = \mathit{agg}(F)$, $\Pi_L = \mathit{agg}(L)$, $\Pi_R = \mathit{agg}(A-1)$, $\Pi_A = \mathit{agg}(A)$ and $\Pi_B = \mathit{agg}(E-1)$.

## Operations

```pseudo id=main
QUERY()
L1  return Π_F ⊗ Π_B
INSERT(v)
L2  push (v, Π_B ⊗ v) at the back, E ← E + 1
L3  FIXUP()
EVICT()                                    ▷ the window is not empty
L4  pop the front, F ← F + 1
L5  FIXUP()
FIXUP()
L6  if F = B then                          ▷ singleton: 0 or 1 item
L7      B ← E, A ← E, R ← E, L ← E
    else
L8      if L = B then                      ▷ flip: front and back have the same length
L9          L ← F, A ← E, B ← E
L10     if L = R then                      ▷ shift: no reversal in progress
L11         A ← A + 1, R ← R + 1, L ← L + 1
        else                               ▷ shrink: one step of the reversal
L12         agg(L) ← Π_L ⊗ Π_R ⊗ Π_A
L13         L ← L + 1
L14         agg(A − 1) ← val(A − 1) ⊗ Π_A
L15         A ← A − 1
```

INSERT and EVICT each break the size invariant by one, and FIXUP repairs it. A **flip** turns the old front into $l_L$ and the old back into $l_R$ without touching any aggregate, because both already point the right way for their new roles. A **shrink** finishes one slot of each: the slot at $L$ gets the aggregate to the end of the front part and joins $l_F$, and the slot at $A - 1$ joins the accumulator $l_A$. A **shift** moves the boundary past one accumulator slot whose aggregate is already final. A flip is always followed by a shrink, and from one flip to the next there are as many shrinks as shifts.

## Example

String concatenation, with the empty string as the identity. The positions are given relative to $F$. The last column counts the calls of $\otimes$ by the operation, without the query.

| operation | $F, L, R, A, B, E$ | $\mathit{agg}$ from $F$ to $E - 1$ | cases | calls | query |
|---|---|---|---|---|---|
| insert(a) | 0, 1, 1, 1, 1, 1 | a | singleton | 1 | a |
| insert(b) | 0, 1, 1, 1, 2, 2 | ab, b | flip, shrink | 4 | ab |
| insert(c) | 0, 2, 2, 2, 2, 3 | ab, b, c | shift | 1 | abc |
| insert(d) | 0, 1, 2, 3, 4, 4 | abcd, b, c, d | flip, shrink | 4 | abcd |
| insert(e) | 0, 2, 2, 2, 4, 5 | abcd, bcd, cd, d, e | shrink | 4 | abcde |
| evict | 0, 2, 2, 2, 3, 4 | bcd, cd, d, e | shift | 0 | bcde |
| evict | 0, 2, 2, 2, 2, 3 | cd, d, e | shift | 0 | cde |
| insert(f) | 0, 1, 2, 3, 4, 4 | cdef, d, e, f | flip, shrink | 4 | cdef |

Take insert(d). Before it, the front part is a, b with aggregates ab, b, and the back part is c with aggregate c. Line L2 appends d with $\Pi_B \otimes d = cd$. Now $L = B$, so line L9 flips: $l_L$ holds a, b and $l_R$ holds c, d, with aggregates ab, b and c, cd. The shrink sets $\mathit{agg}(0) = ab \otimes cd \otimes 1 = abcd$ and $\mathit{agg}(3) = d \otimes 1 = d$. The insert of e then does the second and last shrink: $\mathit{agg}(1) = b \otimes c \otimes d = bcd$ and $\mathit{agg}(2) = c \otimes d = cd$. Two-Stacks would have done this reversal later, all at once, in the first evict after the window had become all back part.

## Correctness

INSERT and EVICT start FIXUP in a state where the order and aggregate invariants hold and either the window has at most one item and $F = B$, or $L - F = E - B$ and $R - L = A - R$. Each case of FIXUP turns that state into one where all invariants hold: the singleton case makes the one item a front item with $\mathit{agg} = v$, the flip relabels the old front and back as $l_L$ and $l_R$ with $R - L = A - R \ge 1$, the shift moves one final accumulator slot into $l_F$, and the shrink computes $\Pi_L \otimes \Pi_R \otimes \Pi_A = \Pi(L..B)$ for the slot at $L$ and $v_{A-1} \otimes \Pi_A = \Pi(A-1..B)$ for the slot at $A - 1$. Under the invariants $\Pi_F = \Pi(F..B)$ and $\Pi_B = \Pi(B..E)$, so QUERY returns $\Pi(F..E)$ by associativity alone. The full proof, case by case, is in [the correctness proof](proofs/correctness.md).

## Complexity

The cost is the number of calls of $\otimes$. FIXUP has no loop, so each count is read off the code.

| operation | worst case | amortized |
|---|---|---|
| query | 1 call | 1 call |
| insert | 4 calls | 2.5 calls on average |
| evict | 3 calls | 1.5 calls on average |
| space | $2n$ values | |

INSERT makes 1 call in line L2, and FIXUP makes at most 3, in a shrink: 2 in line L12 and 1 in line L14. EVICT makes no call before FIXUP, so at most 3. The singleton, flip and shift cases make no call. The averages are the paper's: between two flips the shrinks and shifts are equal in number, so FIXUP makes 1.5 calls on average (Theorem 10). The proof of the worst-case counts is in [the complexity proof](proofs/complexity.md). Pointer moves and deque steps are $O(1)$ per operation as well, provided the deque has worst-case $O(1)$ push, pop and access.

Compared with Two-Stacks, DABA never makes $n$ calls in one evict, but it makes more calls on average: Two-Stacks makes 2 calls per item over its life, against 4 for DABA. **DABA Lite** stores $n + 2$ values and makes at most 1, 3 and 2 calls per query, insert and evict (Theorem 13 of the extended paper).

## Variants

- **DABA Lite.** It stores only the aggregates of the front part, with the back part kept as plain values plus one running aggregate, and a separate aggregate of $l_R$ and $l_A$. This saves $n - 2$ values and one call per operation.
- **Two-Stacks.** The [two-stacks queue](/two-stacks-queue/) is the amortized parent: simpler and with fewer calls in total, but with an $O(n)$ evict.
- **Out-of-order streams.** DABA needs FIFO order. For streams where items can arrive late, the same authors later gave the finger B-tree aggregator (FiBA, PVLDB 2019), a tree-based method outside the scope of this page.
- **Fixed windows and batches.** In a [count-based window](/count-based-window/) of size $W$, each new item is one insert and, once the window is full, one evict, so at most 7 calls per item plus 1 per query.

## When to use it

Use DABA when the window aggregate feeds a latency-bound path, such as a trading or alerting rule that must answer within a fixed time after each tuple, and the operator has no inverse. If only the throughput matters, Two-Stacks or Two-Stacks Lite is faster on average. If the operator has an inverse, a running total with subtract on evict makes one or two calls per item. For max or min alone, the [monotonic deque](/monotonic-deque/) is simpler.

## Pitfalls

- **Reading the wrong end of a sublist.** $\Pi_R$ reads slot $A - 1$, the right end of $l_R$, while $\Pi_L$ and $\Pi_A$ read the left end of their sublists. Reading $\mathit{agg}(R)$ for $\Pi_R$ gives only $v_R$.
- **Order of the arguments.** Lines L2, L12 and L14 keep the older items on the left. Sum and max hide a swap; a test with string concatenation finds it.
- **Reading $\Pi_A$ after line L14.** Line L14 writes slot $A - 1$, not slot $A$, so $\Pi_A$ is the same in lines L12 and L14, but an implementation that moves $A$ before line L14 reads the wrong slot.
- **A deque without worst-case bounds.** A growable array that copies itself on resize makes some operations $\Theta(n)$ and loses the point of DABA. Use a circular buffer of fixed size or a deque of fixed-size chunks.
- **Counting the identity.** The counts include calls with the identity as an argument, such as $1 \otimes v$ in line L2 on an empty back part. An implementation that skips them makes fewer calls, never more.

## Implementations

## History

Tangwongsan, Hirzel and Schneider first described DABA in a 2015 IBM research report, Constant-time sliding window aggregation (RC25574), and published it at DEBS 2017, after their Reactive Aggregator of 2015 had reached $O(\log n)$ amortized time for general windows. They describe it as a de-amortized version of the Two-Stacks method, and they credit Okasaki's purely functional real-time queues as the model for the incremental reversal. The extended paper of 2021 adds DABA Lite.

## References
