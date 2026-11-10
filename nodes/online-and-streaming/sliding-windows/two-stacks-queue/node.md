---
tag: 69X9SB
kind: data-structure
slug: two-stacks-queue
name: Two-stacks queue
aliases:
- banker's queue with aggregation
- two-stack aggregation
- Two-Stacks
- two-stack queue
area: online-and-streaming/sliding-windows
level: advanced
summary: A FIFO window built from two stacks that answers the aggregate of an associative operator with one operator call per insert and per query, and O(1) amortized operator calls per evict.
solves: [sliding-window-aggregation]
implements: [queue]
model: word-ram
complexity:
  vars: {n: the number of items in the window}
  time: {worst: O(n), amortized: O(1)}
  space: {extra: Θ(n)}
history:
  year: 2011
  note: The two-stack queue is folklore. Its use for a window aggregate appears in a 2011 Stack Overflow answer by the user adamax, which Tangwongsan, Hirzel and Schneider cite as the source of the Two-Stacks algorithm.
prereqs: [monoid, stack, queue, amortized-cost, potential-method]
see_also: [min-queue, daba-queue, sliding-window-aggregation, banker-queue, real-time-queue, monotonic-deque, sliding-window-maximum, count-based-window]
sources:
  - paper: doi:10.1145/3093742.3093925
    title: Kanat Tangwongsan, Martin Hirzel and Scott Schneider, Low-latency sliding-window aggregation in worst-case constant time, DEBS 2017
    locator: pages 66 to 77, the Two-Stacks algorithm and its comparison with DABA
  - url: https://arxiv.org/abs/2009.13768
    title: Kanat Tangwongsan, Martin Hirzel and Scott Schneider, In-order sliding-window aggregation in worst-case constant time, extended version (VLDB Journal 2021)
    locator: Section 3, Two-Stacks (Lemma 1 and Theorem 2 for the invariants and the query, Theorem 3 for 2n space and the operator counts), Section 4, Two-Stacks Lite (Theorem 7, n + 1 space)
  - url: https://stackoverflow.com/questions/4802038/
    title: Implement a queue in which push_rear(), pop_front() and get_min() are all constant time operations, Stack Overflow, 2011
    locator: the answer by adamax, two stacks that each keep the running minimum
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.1, exercises on a queue built from two stacks, and Chapter 16, the potential method
---

The two-stacks queue is a first-in first-out window that answers the aggregate $v_1 \otimes v_2 \otimes \cdots \otimes v_n$ of its items under an associative operator $\otimes$ with an identity, that is, a [monoid](/monoid/). It keeps the older items on a front [stack](/stack/) that stores suffix aggregates, and the newer items on a back stack with one running aggregate. Insert and query each make exactly one call of $\otimes$, and evict makes no call except when the front stack is empty, when it moves the whole back stack in $n$ calls. With the [potential method](/potential-method/) the cost of every operation is $O(1)$ [amortized](/amortized-cost/), and the worst case for one evict is $\Theta(n)$.

## In plain words

You keep a line of numbers, add at the back, remove at the front, and want a summary of the whole line, such as its total, its largest value, or all its strings glued together in order. You keep two piles. New items go on the back pile, and you keep one running summary for that pile. The front pile holds older items, and each item there carries the summary of itself and of every item between it and the bottom of that pile. When you must remove an item and the front pile is empty, you move the back pile over, one item at a time, and you rebuild the summaries during the move. The answer is then the stored summary on top of the front pile, glued to the running summary of the back pile. Most removals are cheap, and each item is moved only once.

## The abstract type

The structure implements a [queue](/queue/) of values from a monoid $(M, \otimes, 1)$, with three operations. `insert(v)` adds $v$ as the newest item. `evict()` removes the oldest item and returns it. `query()` returns $v_1 \otimes \cdots \otimes v_n$ when the window holds $v_1, \ldots, v_n$ from the oldest to the newest, and $1$ when it is empty. The operator must be associative. It need not be commutative and need not have an inverse, so max, string concatenation and matrix products all work. This is the FIFO case of [sliding-window aggregation](/sliding-window-aggregation/); in a [count-based window](/count-based-window/) of size $W$, each new item is an insert followed by an evict once $n > W$.

## Representation

A front stack $F$ of pairs $(v, a)$, a back stack $B$ of values, and one value $a_B$. Let the window be $v_1, \ldots, v_n$, with $F$ holding $v_1, \ldots, v_f$ with $v_1$ on top and $B$ holding $v_{f+1}, \ldots, v_n$ with $v_n$ on top.

**Invariant.** The entry of $v_i$ in $F$ has $a_i = v_i \otimes v_{i+1} \otimes \cdots \otimes v_f$, and $a_B = v_{f+1} \otimes \cdots \otimes v_n$, which is $1$ when $B$ is empty.

So the top of $F$ holds the aggregate of the whole front part, and $a_B$ holds the aggregate of the whole back part. The structure stores $2f + (n - f) + 1 \le 2n + 1$ values. The Two-Stacks of Tangwongsan, Hirzel and Schneider stores a pair in both stacks, for $2n$ values; their Two-Stacks Lite keeps the items in one array, overwrites each front value with its aggregate, and stores $n + 1$ values.

## Operations

```pseudo id=main
INSERT(v)
L1  PUSH(B, v)
L2  a_B ← a_B ⊗ v
EVICT()                                    ▷ the window is not empty
L3  if F is empty then                     ▷ flip
L4      a ← 1
L5      while B is not empty do
L6          v ← POP(B)
L7          a ← v ⊗ a
L8          PUSH(F, (v, a))
L9      a_B ← 1
L10 return the value of POP(F)
QUERY()
L11 a_F ← the a of TOP(F), or 1 if F is empty
L12 return a_F ⊗ a_B
```

INSERT extends the running aggregate of $B$ on the right. EVICT pops the top of $F$, which is the oldest item. When $F$ is empty, lines L5 to L8 pop $B$ from the newest item down and push each item on $F$ with $v \otimes a$, so the aggregates are built from the right end of the front part to the left. The order of the two arguments in lines L2, L7 and L12 matters when $\otimes$ is not commutative: older items always stand on the left.

## Example

Take string concatenation, with the empty string as the identity. Stacks are written from the bottom to the top. The last column counts the calls of $\otimes$ by the operation, not counting the query.

| operation | $F$ | $B$ | $a_B$ | returns | query | calls |
|---|---|---|---|---|---|---|
| insert(a) | | a | a | | a | 1 |
| insert(b) | | a b | ab | | ab | 1 |
| insert(c) | | a b c | abc | | abc | 1 |
| evict | (c, c) (b, bc) | | | a | bc | 3 |
| insert(d) | (c, c) (b, bc) | d | d | | bcd | 1 |
| evict | (c, c) | d | d | b | cd | 0 |
| evict | | d | d | c | d | 0 |
| evict | | | | d | | 1 |

The first evict flips: it pushes $(c, c)$, then $(b, bc)$, then $(a, abc)$, and pops the last one. The query after the insert of d is $bc \otimes d = bcd$, in the window order. Over the 8 operations, the 4 inserts made 4 calls, and the 2 flips made 4 calls: one call for each item at each of its two stages.

## Correctness

Each operation keeps the invariant. INSERT puts $v_{n+1}$ on top of $B$, and line L2 makes $a_B = v_{f+1} \otimes \cdots \otimes v_{n+1}$. An evict without a flip removes $v_1$ and leaves the aggregates of $v_2, \ldots, v_f$ unchanged, and they are still right because each $a_i$ covers only items from $v_i$ to $v_f$. A flip with $F$ empty moves $v_n, v_{n-1}, \ldots, v_1$ in that order, and after it pushes $v_i$, the value $a$ is $v_i \otimes \cdots \otimes v_n$, so the new front part is the whole window and $B$ is empty with $a_B = 1$. Under the invariant, line L12 returns $(v_1 \otimes \cdots \otimes v_f) \otimes (v_{f+1} \otimes \cdots \otimes v_n)$, which by associativity is the aggregate of the window. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The cost model counts calls of $\otimes$, which is the expensive step when the operator is a sketch merge or a matrix product. Stack pushes and pops follow the same pattern.

| operation | worst case | amortized |
|---|---|---|
| insert | 1 call | 2 calls |
| evict | $n$ calls | 0 calls |
| query | 1 call | 1 call |
| space | $2n + 1$ values | |

**Amortized bound.** Let $\Phi = |B|$, the number of items on the back stack. INSERT makes one call and raises $\Phi$ by 1, so its amortized cost is 2. An evict with a flip of $k$ items makes $k$ calls and drops $\Phi$ by $k$, so its amortized cost is 0. Since $\Phi \ge 0$ and starts at 0, any sequence of $I$ inserts, any evicts and $Q$ queries makes at most $2I + Q$ calls. With pushes and pops counted too, $\Phi = 3|B|$ gives amortized cost 5 for INSERT and 1 for EVICT. The proof is in [the complexity proof](proofs/complexity.md).

**Worst case.** After $n$ inserts into an empty window, the first evict flips all $n$ items and makes $n$ calls. A real-time stream that must answer within a fixed time after each tuple sees this spike once every $n$ evicts.

## Variants

- **Two-Stacks Lite.** One array, with the front aggregates written over the front values, so the space is $n + 1$ values with the same operator counts (Tangwongsan, Hirzel and Schneider, Theorem 7).
- **Queue with minimum.** With $\otimes = \min$ this is the [queue with minimum](/min-queue/), whose page gives the stack-level details and the two-stack layout for a total order.
- **De-amortized.** [DABA](/daba-queue/) runs the flip a few steps at a time, as Okasaki's real-time queues do, and reaches $O(1)$ worst case per operation: at most 1 call per query, 4 per insert and 3 per evict.
- **Persistent queues.** The purely functional [banker's queue](/banker-queue/) and [real-time queue](/real-time-queue/) use the same front and rear lists for a queue without aggregates.
- **Max and min only.** For an idempotent selection such as max, the [monotonic deque](/monotonic-deque/) needs only comparisons and keeps fewer items; see [sliding-window maximum](/sliding-window-maximum/).

## When to use it

Use the two-stacks queue for a count-based or time-based window over any associative operator, when the throughput matters more than the latency of single operations. It has the smallest code of the $O(1)$ amortized methods and only one call of $\otimes$ per insert. If the operator has an inverse, the subtract-on-evict running total is cheaper still. If each operation must finish in bounded time, use DABA. If items can arrive out of order, neither works, since both assume FIFO order.

## Pitfalls

- **Wrong argument order.** For a non-commutative operator, line L7 must be $v \otimes a$ and line L12 must be $a_F \otimes a_B$. Code tested only with sum or max can hide this bug; test with string concatenation.
- **Flip with $F$ not empty.** Moving $B$ onto a non-empty $F$ puts newer items above older ones.
- **Stale back aggregate.** After a flip, $a_B$ must be reset to the identity in line L9, or the query counts the moved items twice.
- **No identity.** Some operators, such as max over an unbounded type, have no natural identity. Add a formal identity element, or test for empty stacks in lines L11 and L12 instead.
- **Latency.** The amortized bound says nothing about a single evict. A flip of a window of a million sketches is a million merges in one step.

## Implementations

## History

The queue built from two stacks is folklore and a standard exercise. Its use with a running minimum in each stack was posted by the user adamax on Stack Overflow in 2011. Tangwongsan, Hirzel and Schneider named the general monoid version Two-Stacks in their DEBS 2017 paper, analysed its operator counts, and used it as the starting point for DABA.

## References
