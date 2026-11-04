---
tag: NF6DCE
kind: data-structure
slug: kinetic-heap
name: Kinetic heap
aliases:
- kinetic tournament
- kinetic priority queue
area: data-structures/heaps
level: research
summary: Heap over moving keys that maintains the minimum as keys change continuously over time.
implements: [priority-queue]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [binary-heap, heap-property, priority-queue]
see_also: [tournament-tree, binary-heap, d-ary-heap, event-queue, convex-hull, priority-queue]
sources:
  - paper: "Julien Basch, Leonidas J. Guibas and John Hershberger, Data structures for mobile data, Journal of Algorithms 31(1), 1999, pp. 1 to 28"
    title: "Julien Basch, Leonidas J. Guibas and John Hershberger, Data structures for mobile data, Journal of Algorithms 31(1), 1999, pp. 1 to 28; preliminary version in Proceedings of the 8th ACM-SIAM Symposium on Discrete Algorithms (SODA 1997), pp. 747 to 756"
    locator: the introduction of kinetic data structures, the kinetic heap and the kinetic tournament
  - paper: "Julien Basch, Leonidas J. Guibas and G. D. Ramkumar, Sweeping lines and line segments with a heap, Proceedings of the 13th ACM Symposium on Computational Geometry, 1997, pp. 469 to 471"
    title: "Julien Basch, Leonidas J. Guibas and G. D. Ramkumar, Sweeping lines and line segments with a heap, SoCG 1997, pp. 469 to 471"
    locator: the bounds O(n log² n) and Ω(n log n) on the events, and O(n √(n log n)) with insertions and deletions
  - paper: "Guilherme D. da Fonseca and Celina M. H. de Figueiredo, Kinetic heap-ordered trees: tight analysis and improved algorithms, Information Processing Letters 85(3), 2003, pp. 165 to 169"
    title: "Guilherme D. da Fonseca and Celina M. H. de Figueiredo, Kinetic heap-ordered trees: tight analysis and improved algorithms, Information Processing Letters 85(3), 2003, pp. 165 to 169"
    locator: Section 2 (Lemma 1, Lemma 2, Theorem 3, Corollary 4, Theorem 5) and Section 3 (kinetic log n-heaps)
  - paper: "Haim Kaplan, Robert E. Tarjan and Kostas Tsioutsiouliklis, Faster kinetic heaps and their use in broadcast scheduling, Proceedings of the 12th ACM-SIAM Symposium on Discrete Algorithms (SODA 2001)"
    title: "Haim Kaplan, Robert E. Tarjan and Kostas Tsioutsiouliklis, Faster kinetic heaps and their use in broadcast scheduling, SODA 2001"
    locator: the kinetic heaps on (log n)-ary trees and the application to broadcast scheduling
---

A kinetic heap keeps the item of smallest key in a set of items whose keys change continuously with time. Each key is a function of time, here a linear function $a + b t$. The heap is a [binary heap](/binary-heap/) that is correct at the current time. For each edge from a parent to a child it stores a *certificate*, the claim that the parent key is at most the child key, together with the time when the claim will first fail. The certificates are in an [event queue](/event-queue/). When time moves forward, the heap processes the failures in order: each one is an *event*, and it is repaired by one swap of a parent and a child. Basch, Guibas and Hershberger introduced the kinetic heap in 1997 with the idea of kinetic data structures. Da Fonseca and de Figueiredo proved in 2003 that a kinetic heap with $n$ linear keys processes at most $\Theta(n \log n)$ events.

## In plain words

Think of $n$ cars on a road, each with a fixed speed, and ask at any moment which car is last. You could sort the cars again at every moment, but the answer changes only at a few moments, when two cars meet. A kinetic heap keeps a heap of the cars that is right now, and for each parent and child in the heap it computes when the two cars will meet. It keeps these meeting times in a second priority queue.

Nothing has to be done until the first meeting time. At that moment the two cars swap places in the heap, which fixes the heap, and only a few meeting times change. So the work depends on the number of these events and not on how often you ask for the answer.

## The abstract type

A kinetic heap holds items $e$, each with a key $k_e(t) = a_e + b_e t$, and a current time $now$. The operations are these.
- `advance(t)`: set $now \leftarrow t$ for $t \ge now$.
- `find-min()`: return an item with the smallest key at time $now$.
- `insert(e, a, b)` and `delete(e)`, at time $now$.

A change of the motion of one item is a delete and an insert at the same time. This page uses a min-heap; the papers keep the maximum, which is the same with the signs of the keys changed.

## Representation

The items are in an array $H[0 \ldots n - 1]$ with the usual binary heap shape: the parent of position $i > 0$ is $\lfloor (i - 1)/2 \rfloor$. A map gives the position of each item.

The heap order is the order *just after* $now$: item $e$ is before item $f$ if $k_e(now) < k_f(now)$, or the keys are equal and $b_e < b_f$. If $e$ is before $f$ in this order, then $k_e(t) \le k_f(t)$ for all $t$ in some interval $[now, now + \delta)$.

For each $i > 0$, with $p$ the item at the parent of $i$ and $c$ the item at $i$, the certificate of position $i$ is the claim $k_p(t) \le k_c(t)$. Its failure time is

$$fail(i) = \begin{cases} \dfrac{a_c - a_p}{b_p - b_c} & \text{if } b_p > b_c, \\ \infty & \text{otherwise.} \end{cases}$$

If $b_p \le b_c$, the parent key grows no faster than the child key, so the claim never fails. The event queue holds the pairs $(fail(i), i)$ for the finite failure times. All arithmetic is with exact fractions, so equal times are really equal.

**Invariants.** (1) Each parent is before or equal to each child in the order just after $now$. (2) Each position $i > 0$ has a certificate with the correct failure time, and every finite failure time is larger than $now$.

## Operations

```pseudo id=main
CERT(i)                                 ▷ p at the parent of i, c at i
L1  if b_p > b_c then fail ← (a_c - a_p) / (b_p - b_c) else fail ← ∞
L2  put (fail, i) in the event queue Q, in the place of the old certificate of i

ADVANCE(t)                              ▷ t ≥ now
L3  while the earliest failure time τ in Q is at most t:
L4      remove (τ, i) from Q; now ← τ
L5      swap the items at i and at its parent p
L6      CERT for p, i, the other child of p and the children of i
L7  now ← t

FIND-MIN()
L8  return H[0]

INSERT(e, a, b)
L9  append e at the end of H and move it up in the order just after now
L10 CERT for every position whose item changed, and for their children

DELETE(e)
L11 put the last item in the place of e, and move it up or down in the order just after now
L12 CERT for every position whose item changed, and for their children
```

After an event at position $i$, only the certificates of the edges at $p$ and at $i$ can change, because only these two positions get new items. These are the edge above $p$, the two edges below $p$ (one of them is the edge to $i$) and the two edges below $i$: five certificates in all.

At line L5 the two keys are equal and the child has the smaller slope, so after the swap the edge from $p$ to $i$ has a certificate that never fails. Another certificate that line L6 makes can fail at the same time $\tau$, for example when three lines meet in one point. Then the loop processes it next, with the same $now$.

## Example

Take five items with these keys, and start at time 0.

| item | $a$ | $b$ | key at $t = 0$ |
| --- | --- | --- | --- |
| A | 0 | 3 | 0 |
| B | 1 | 1 | 1 |
| C | 2 | 0 | 2 |
| D | 5 | -1 | 5 |
| E | 4 | -2 | 4 |

Insert them in this order. No item moves, so $H = [A, B, C, D, E]$. Then A is the parent of B and C, and B is the parent of D and E. The certificates are $fail(1) = (1 - 0)/(3 - 1) = 1/2$ for A and B, $fail(2) = 2/3$ for A and C, $fail(3) = (5 - 1)/(1 + 1) = 2$ for B and D, and $fail(4) = (4 - 1)/(1 + 2) = 1$ for B and E.

Now advance to $t = 100$.

| time | event | heap after the event | new failure times |
| --- | --- | --- | --- |
| 1/2 | A and B meet at 1.5; swap | B A C D E | A and D at 5/4, A and E at 4/5, B and C at 1 |
| 4/5 | A and E meet at 2.4; swap | B E C D A | B and E at 1; E and D and E and A never |
| 1 | B, C and E all have the key 2. B and C swap, then C and E swap at the same time | E C B D A | C and D at 3 |
| 3 | C and D meet at 2; swap | E D B C A | none |

After time 3 every parent has a slope at most the slopes of its children, so no certificate can fail, and E stays the minimum for ever. There were 5 events. The sum of the depths of the five positions is $0 + 1 + 1 + 2 + 2 = 6$, and the bound below says that there are at most 6 events. The test file checks this trace.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). These are the main points.
- *Between events, nothing changes.* If no certificate fails in $[now, t]$, then every parent key is at most every child key at every time in the interval, so the heap is valid for the whole interval, and $H[0]$ is a minimum. A certificate with $b_p \le b_c$ never fails, and one with $b_p > b_c$ holds exactly until its failure time.
- *An event repairs the heap.* At the failure time the two keys are equal, and the child has the smaller slope. So after the swap the pair is in the right order just after $\tau$. The other neighbours of the two positions are compared with the new items by line L6. Items further away are not affected, because heap order is a property of each edge.
- *Ties.* Using the order just after $now$ makes every certificate fail strictly after $now$ once all the events at $now$ are processed. If several certificates fail at the same time, they are processed one by one; each event lowers the count below, so this ends.

**The number of events.** Let $\Phi'$ be the number of pairs $(f, g)$ such that $f$ is an ancestor of $g$ in the heap and $b_g < b_f$, that is, $g$ will be smaller than $f$ from some time on. Each event lowers $\Phi'$ by at least 1. At the event, the pair (parent, child) stops counting. The items in the subtree of the other child of $p$ change one ancestor, from the old parent item to the old child item, which has the smaller slope, so they count no more than before. All other ancestor relations stay the same as sets. So if no item is inserted or deleted, the number of events is at most $\Phi'$ at the start, which is at most $\Phi$, the sum of the depths of all positions. For a binary heap of $n$ items, $\Phi \le n \lfloor \lg n \rfloor$.

The bound is exact. Take the lines $k_s(t) = -2 s t + s^2$ for $s = 0, \ldots, n - 1$, tangent to the parabola $-t^2$. At time $t$ the smallest key belongs to the line whose $s$ is nearest to $t$, so every item is the minimum at some time and must reach the root. Each event moves one item up one level, so the item at depth $d$ needs at least $d$ events, and there are at least $\Phi$ events. The test file checks that there are exactly $\Phi$ events for several $n$.

## Complexity

| quantity | bound | source |
| --- | --- | --- |
| events with $n$ linear keys and no inserts or deletes | $\Theta(n \log n)$ | da Fonseca and de Figueiredo, Theorem 3 and Corollary 4; proved on this page |
| earlier bound on the events | $O(n \log^2 n)$ and $\Omega(n \log n)$ | Basch, Guibas and Ramkumar (1997) |
| events with $n$ inserts and $n$ deletes, from an empty heap | $O(n \sqrt{n \log n})$ | Basch, Guibas and Ramkumar, as cited by da Fonseca and de Figueiredo |
| time per event | $O(\log n)$ | five certificates, each a queue operation |
| find-min | $O(1)$ | the root |
| insert, delete | $O(\log^2 n)$ in this implementation | $O(\log n)$ swaps and certificates, each a queue operation |

The event queue holds at most $n - 1$ certificates. The implementation on this page uses a binary heap with lazy deletion for it, so old certificates stay in it until they come to the top; this costs at most a constant factor in time. Space is $\Theta(n)$ apart from these stale entries.

## Variants

- *Kinetic tournament.* A [tournament tree](/tournament-tree/) over the moving items: each internal node holds the winner of its two children. Basch, Guibas and Hershberger proved that it processes $O(n \log n)$ events for linear keys, before the same bound was known for the kinetic heap.
- *Kinetic $k$-heaps.* A heap-ordered $k$-ary tree. By the same count, a kinetic $f(n)$-heap processes $\Theta(n \log n / \log f(n))$ events. For $f(n) = \log n$ this is $O(n \log n / \log \log n)$ events, and in that version each parent keeps a certificate only for the child that will first become smaller than it (da Fonseca and de Figueiredo, Section 3; Kaplan, Tarjan and Tsioutsiouliklis).
- *Pseudo-lines.* The count of events holds for any keys such that every two meet at most once, not only for lines.

## When to use it

Use a kinetic heap when the keys move in a known way and you need the minimum at many times, or need to know when it changes: the closest of moving objects, scheduling where priorities grow with time, or a sweep over lines. With $n$ lines $y = a + b t$, a kinetic heap that is run from $t = -\infty$ to $+\infty$ reports the lower envelope of the lines, which is dual to the [convex hull](/convex-hull/) of points; but an ordinary $O(n \log n)$ hull algorithm is better for that one task. If the keys change in steps and not continuously, use an ordinary [priority queue](/priority-queue/) with decrease-key.

## Pitfalls

- **Floating-point times.** Two failure times that should be equal can come out in the wrong order, and then the heap swaps the wrong pair or computes a failure time in the past. Use exact arithmetic, or a careful order on times.
- **Ties in the heap order.** If two keys are equal now, the one with the larger slope must be the child. If the order uses the current key alone, a certificate can fail at once, at time $now$, and the event loop can see it as a failure in the past.
- **Forgetting the sibling.** After a swap at positions $p$ and $i$, the edge from $p$ to the other child of $p$ has a new parent item, and its certificate must be computed again.
- **Stale events.** A certificate that was replaced is still in a lazy event queue. Mark certificates with a version number and skip the old ones.
- **Expecting the same bound with updates.** The bound of $\Theta(n \log n)$ events holds for a fixed set of items. With inserts and deletes the known upper bound is weaker.

## Implementations

The Python implementation in `impl/python/kinetic_heap.py` follows the pseudocode. It uses `fractions.Fraction` for all keys and times, a dictionary for the positions, and `heapq` with version numbers as the event queue. It counts the events. `check_invariant` checks the positions, heap order just after $now$, and that each edge has a certificate with the right failure time, later than $now$. The tests check the example trace, the tangent lines that meet the bound $\Phi$ exactly, parallel and equal lines, and 600 random sequences of inserts, deletes and advances against a brute-force minimum; in each advance, the number of events must be at most $\Phi'$ at its start.

## History

Basch, Guibas and Hershberger defined kinetic data structures at SODA 1997, with the kinetic heap and the kinetic tournament as the first examples for a moving minimum or maximum. They noted that the number of events of the kinetic heap was hard to count. Basch, Guibas and Ramkumar proved the bounds $O(n \log^2 n)$ and $\Omega(n \log n)$ in 1997, and asked if $O(n \log n)$ holds. Da Fonseca and de Figueiredo proved in 2003 that the number of events of any kinetic heap-ordered tree is exactly the number of ancestor and descendant pairs in the worst case, which answered the question. Kaplan, Tarjan and Tsioutsiouliklis (2001) gave faster kinetic heaps for broadcast scheduling.

## References
