---
tag: VVXG5M
kind: data-structure
slug: min-queue
name: Queue with minimum
aliases:
- Queue with minimum (Minimum Queue)
area: data-structures/linear-structures
level: core
summary: A queue that returns its current minimum in constant amortized time, built from two minimum stacks or a monotonic deque.
implements: [queue]
prereqs: [min-stack, queue, amortized-cost]
see_also: [two-stacks-queue, monotonic-deque, sliding-window-maximum, sliding-window-aggregation, deque, accounting-method, potential-method]
sources:
  - url: https://cp-algorithms.com/data_structures/stack_queue_modification.html
    title: cp-algorithms, Minimum stack / Minimum queue
    locator: the sections Queue modification (method 1, the monotonic deque, and method 3, two stacks)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.1 and its exercises, a queue implemented with two stacks; Chapter 16 for the amortized analysis
  - paper: "Hania Gajewska and Robert E. Tarjan, Deques with heap order, Information Processing Letters 22(4) (1986)"
    locator: the deque with find-minimum in constant worst-case time per operation
---

A queue with minimum is a first-in first-out [queue](/queue/) that also answers `min`, the least item it holds. The standard construction uses two [stacks with minimum](/min-stack/): new items go on an *in* stack, and when the *out* stack is empty, all of *in* is moved to *out*, which reverses the order so that the oldest item is on top. Each item moves at most once, so enqueue, dequeue and min each cost $O(1)$ [amortized](/amortized-cost/). It solves the sliding-window minimum, and with any associative operation in place of min, it gives sliding-window aggregation in amortized constant time.

## In plain words

A queue serves people in the order they came. You also want to know, at any time, the smallest number held by anyone in the queue. A stack can already do this, because a stack can store "the smallest so far" with each entry. A queue cannot do it directly, because people leave from the other end.

So you build the queue from two piles. New people join the first pile. When someone must leave and the second pile is empty, you move the whole first pile, one by one, onto the second pile. Now the person who came first is on top of the second pile, and leaves from there. Each pile knows its own smallest number, so the smallest in the queue is the smaller of the two.

## The abstract type

The structure implements the [queue](/queue/) type: `enqueue(Q, x)` at the back, `dequeue(Q)` at the front, `is_empty(Q)` and `size(Q)`. It adds `min(Q)`, which returns the least item of a non-empty queue without changing it. The items come from a set with a total order.

## Representation

Two stacks with minimum, $In$ and $Out$. Each holds pairs $(x, m)$ where $m$ is the least item at or below that entry, as on the [stack with minimum](/min-stack/) page. Write $In = \langle a_1, \ldots, a_p \rangle$ and $Out = \langle b_1, \ldots, b_r \rangle$ from the bottom to the top.

**Invariant.** The queue, from the front to the back, is $\langle b_r, \ldots, b_1, a_1, \ldots, a_p \rangle$: first $Out$ from the top down, then $In$ from the bottom up.

## Operations

```pseudo id=main
ENQUEUE(Q, x)
L1  PUSH(Q.in, x)
DEQUEUE(Q)                                 ▷ Q is not empty
L2  if Q.out is empty then
L3      while Q.in is not empty
L4          PUSH(Q.out, POP(Q.in))
L5  return POP(Q.out)
MIN(Q)                                     ▷ Q is not empty
L6  if Q.in is empty then return MIN(Q.out)
L7  if Q.out is empty then return MIN(Q.in)
L8  return min(MIN(Q.in), MIN(Q.out))
```

ENQUEUE is one push. DEQUEUE pops from $Out$. When $Out$ is empty, lines L3 and L4 first move all of $In$ to $Out$. The pops come from the top of $In$, the newest item, so the oldest item ends on top of $Out$. Each PUSH on $Out$ computes the new running minimum, so the minima of $Out$ are right for the reversed order. MIN reads the two stored minima.

A transfer of $p$ items costs $\Theta(p)$, so one DEQUEUE can cost $\Theta(n)$. But each item is pushed on $In$ once, moved once and popped from $Out$ once. So $m$ operations cost $O(m)$ in total.

**The monotonic deque version.** A second construction keeps a [deque](/deque/) $D$ of the items that can still become the minimum, in increasing order from the front. Items are tagged with their arrival number $t$, and a counter $\ell$ holds the arrival number of the current front of the queue.

```pseudo id=mono
ENQUEUE(Q, x)
M1  while D is not empty and the value at the back of D ≥ x
M2      remove the back of D
M3  add (x, t) at the back of D, t ← t + 1
DEQUEUE(Q)                                 ▷ the front item of the queue leaves
M4  if the front of D has arrival number ℓ then remove the front of D
M5  ℓ ← ℓ + 1
MIN(Q)
M6  return the value at the front of D
```

An item $y$ that arrived before a smaller or equal item $x$ can never be the minimum again: $x$ stays in the queue at least as long as $y$. So line M2 drops it. The values in $D$ then increase strictly from the front, and the front of $D$ is the minimum. Each item is added and removed at most once, so ENQUEUE is $O(1)$ amortized and the other operations are $O(1)$ worst case. This version does not store the full queue; if `dequeue` must return the item, keep a plain queue next to it. This is the [monotonic deque](/monotonic-deque/).

## Example

Enqueue 4, 2, 5, then mix dequeues and one more enqueue. The stacks are written from the bottom to the top as pairs $(x, m)$. The column "moves" counts the executions of line L4.

| operation | $In$ | $Out$ | result | min | moves |
|---|---|---|---|---|---|
| enqueue(4) | (4,4) | | | 4 | 0 |
| enqueue(2) | (4,4) (2,2) | | | 2 | 0 |
| enqueue(5) | (4,4) (2,2) (5,2) | | | 2 | 0 |
| dequeue | | (5,5) (2,2) | 4 | 2 | 3 |
| enqueue(1) | (1,1) | (5,5) (2,2) | | 1 | 3 |
| dequeue | (1,1) | (5,5) | 2 | 1 | 3 |
| dequeue | (1,1) | | 5 | 1 | 3 |
| dequeue | | | 1 | | 4 |

In the first dequeue, the transfer pops 5, 2 and 4 from $In$ and pushes them on $Out$ as $(5,5)$, $(2,2)$ and $(4,2)$. Line L5 then pops $(4,2)$ and returns 4, the oldest item. After it the queue is $\langle 2, 5 \rangle$, and $Out$ holds its minimum 2 in the top pair. After the third dequeue, $Out$ is empty, so line L7 answers from $In$. Seven operations made 4 moves, one for each enqueued item.

## Correctness

The invariant says how the two stacks spell the queue. ENQUEUE adds at the back, which is the top of $In$. A DEQUEUE with $Out$ not empty removes the top of $Out$, which is the front. A transfer moves $a_p, \ldots, a_1$ to $Out$ so that $a_1$ is on top, and the queue spelled by the invariant does not change. MIN returns the least of the minima of the two stacks, which is the least item of the queue because the two stacks together hold exactly its items. The full proof, with the amortized bound, is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | worst case | amortized |
|---|---|---|
| enqueue | $O(1)$ | $O(1)$, 3 stack operations |
| dequeue | $\Theta(n)$ | $O(1)$, 1 stack operation |
| min | $O(1)$ | $O(1)$ |
| space | $2n$ cells | |

**Amortized bound.** Let $\Phi = 2p$, twice the size of $In$. ENQUEUE does one push and raises $\Phi$ by 2, so its amortized cost is 3. A DEQUEUE that moves $p$ items does $2p + 1$ stack operations and drops $\Phi$ by $2p$, so its amortized cost is 1. A DEQUEUE without a transfer costs 1. Since $\Phi \ge 0$ and starts at 0, any $m$ operations cost at most $3m$ stack operations. The bound is in the [potential method](/potential-method/); the same count by credits is the [accounting method](/accounting-method/).

The monotonic deque version has the same amortized bounds and uses at most $n$ cells for $D$.

## Variants

- **Any associative operation.** Store $x_1 \oplus \cdots \oplus x_j$ in each stack entry and combine the two stack values with $\oplus$ in line L8, in the order $Out$ then $In$. This gives [sliding-window aggregation](/sliding-window-aggregation/) for sums, products of matrices, gcd or max. The operation does not have to be commutative, but it must be associative.
- **Monotonic deque.** The second construction above. It needs only comparisons and does not need associativity, but it works only for min and max.
- **Worst-case constant time.** Gajewska and Tarjan (1986) gave a deque with heap order, with $O(1)$ worst-case time for each operation, including find-minimum. Real-time queues of the kind in [real-time queue](/real-time-queue/) remove the long transfers by moving a few items in each operation.
- **Two-stack queue without minimum.** Dropping the min fields gives the [two-stack queue](/two-stacks-queue/).

## When to use it

Use a queue with minimum for a sliding window whose size changes, for example the minimum price in the last $T$ seconds of a stream. For a window of a fixed width over an array, the [monotonic deque](/monotonic-deque/) is shorter to write and keeps fewer items. Use the two-stack version when the operation is a general associative operation, such as a sum modulo a prime or a matrix product, since the deque method works only for min and max. If the program must remove the minimum itself, not only the oldest item, use a [priority queue](/priority-queue/).

## Pitfalls

- **Transfer when $Out$ is not empty.** Moving items from $In$ to $Out$ while $Out$ still holds items puts newer items above older ones, and DEQUEUE returns the wrong item. Line L2 must test that $Out$ is empty.
- **Reading a stored minimum from an empty stack.** Line L8 reads both minima. With one stack empty, use line L6 or L7, or give each stack a bottom sentinel of $+\infty$.
- **Combining in the wrong order.** For a non-commutative operation, $Out$ holds the older items, so the result is $\text{agg}(Out) \oplus \text{agg}(In)$, not the other order. Also, the running value in $Out$ must be built so that it covers the items from the top down, which is the queue order.
- **Value test in the deque version.** A common short form of DEQUEUE pops the front of $D$ when its value equals the leaving item, with no arrival numbers. That form is correct only if line M1 keeps equal items, with $>$ in place of $\ge$. With $\ge$, after enqueue 2, enqueue 2 and one dequeue, $D$ is empty while the queue still holds a 2. Use arrival numbers as in line M4, or pair the value test with $>$.
- **A worst-case bound claimed.** One dequeue can move all $n$ items. In a latency-bound loop, use the deque version or a real-time queue.

## Implementations

## History

A queue built from two stacks is folklore, and it is a standard exercise of CLRS Section 10.1. The extension to a minimum query follows from the stack with minimum. Gajewska and Tarjan (1986) studied the general problem of a deque with heap order and gave a structure with constant worst-case time per operation.

## References
