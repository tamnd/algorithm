---
tag: S8NDWC
kind: data-structure
slug: monotonic-deque
name: Monotonic deque
aliases:
- Monotonic queue
- monotone queue
- monotonic deque
- monotonic queue
- sliding window deque
area: data-structures/linear-structures
level: intro
summary: Deque kept in monotone order so the window extremum is read off in O(1) per step.
prereqs: [deque, queue, monotonic-stack, amortized-cost]
see_also: [sliding-window-maximum-deque, sliding-window-maximum, min-queue, two-stacks-queue, sliding-window, monotonic-deque-prefix-sums, min-stack, convex-hull-trick]
sources:
  - url: https://cp-algorithms.com/data_structures/stack_queue_modification.html
    title: cp-algorithms, Minimum stack / Minimum queue
    locator: sections Queue modification (method 1), Queue modification (method 2) and Finding the minimum for all subarrays of fixed length
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 8, Amortized analysis, the section Sliding window minimum
  - url: https://arxiv.org/abs/cs/0610046
    title: Daniel Lemire, Streaming maximum-minimum filter using no more than three comparisons per element, Nordic Journal of Computing 13(4), 2006
    locator: the streaming algorithm with a monotone double-ended queue and its comparison count
---

A monotonic deque is a [deque](/deque/) of (position, item) pairs whose items strictly increase from the front to the back, used to keep the minimum of a [queue](/queue/) whose items arrive at the back and leave from the front. A new item removes from the back every pair that it beats, so the front is always the minimum of the items still in the queue. PUSH costs $O(1)$ amortized time, POP and MIN cost $O(1)$ in the worst case, and the structure gives the minimum of every window of a [sliding window](/sliding-window/) in $\Theta(n)$ total time. It is the queue form of the [monotonic stack](/monotonic-stack/): the stack drops the dominated items from the top, and the deque also drops expired items from the bottom.

## In plain words

Think of a line of people waiting to leave a room by the front door. Each person has a number, and at any time you want to know the smallest number in the line. A new person joins at the back. Every person at the back with a number that is not smaller than the new number can be forgotten: they leave before the new person, and while they are in the room, the new person is there too and is at least as small. So they can never be the smallest.

After the new person joins, the numbers you still remember go up from the front to the back. The smallest one is at the front. When the oldest person leaves the room, you forget them if you still remember them, else nothing changes. Each person is remembered once and forgotten once, so the work stays small.

## The abstract type

The monotonic deque implements a queue with a minimum query, in the form that a sliding window needs. The structure stores a sequence $Q = (x_h, x_{h+1}, \ldots, x_{t-1})$ of the items pushed and not yet popped, where $x_j$ is the $j$-th item pushed, counting from 0. The operations are:

- `push(x)`: append $x$ at the back, so $Q$ becomes $(x_h, \ldots, x_{t-1}, x)$;
- `pop()`: remove the front item $x_h$, for $Q$ not empty;
- `min()`: return $\min Q$, for $Q$ not empty;
- `size()`: return $|Q| = t - h$.

`pop` does not return the removed item, because the structure does not keep every item. In a sliding window the caller has the items in the array. A version whose `pop` returns the item is the [min-queue](/min-queue/); it keeps all items, for example in [two stacks](/two-stacks-queue/). The same structure with the order reversed keeps the maximum.

## Representation

The fields are two counters and a deque:

- $h$, the number of items popped so far, which is also the position of the front item of $Q$;
- $t$, the number of items pushed so far, which is the position the next item gets;
- $D$, a deque of pairs $(j, x_j)$.

**Invariant.** (I1) The positions in $D$, from the front to the back, are exactly the positions $j$ with $h \le j < t$ such that $x_j < x_m$ for every $m$ with $j < m < t$. (I2) The pairs of $D$ are in increasing order of position.

So $D$ holds the strict suffix minima of $Q$: the items that are smaller than everything pushed after them. Two facts follow. The items in $D$ strictly increase from the front to the back, since for two positions $j < j'$ in $D$, (I1) for $j$ gives $x_j < x_{j'}$. And the back of $D$ is always the last item pushed, position $t - 1$, when $Q$ is not empty, since the condition of (I1) is empty for $j = t - 1$.

## Operations

```pseudo id=main
NEW()
L1  D ← an empty deque; h ← 0; t ← 0

PUSH(x)
L2  while D is not empty and BACK(D).item ≥ x do
L3      POP-BACK(D)                            ▷ dominated: x is newer and at most as large
L4  PUSH-BACK(D, (t, x))
L5  t ← t + 1

POP()                                          ▷ requires h < t
L6  if FRONT(D).pos = h then POP-FRONT(D)      ▷ the oldest item leaves
L7  h ← h + 1

MIN()                                          ▷ requires h < t
L8  return FRONT(D).item
```

PUSH removes from the back the pairs whose items are at least $x$. They form a suffix of $D$, because the items of $D$ increase towards the back. Then it appends $(t, x)$. One call can remove all of $D$, so the worst case of one PUSH is $\Theta(|D|)$, but each pair is removed at most once after it is added, so PUSH costs $O(1)$ amortized.

POP removes the front pair only when it belongs to the oldest item $x_h$. If $x_h$ is not in $D$, a later item that was at most as large removed it, and POP only moves $h$. The front of $D$ never has a position less than $h$, so one test is enough. POP costs $O(1)$ in the worst case.

MIN reads the front pair in $O(1)$ time. The front is the minimum of $Q$, and it is the last occurrence of the minimum when items repeat.

The windows of a [sliding window](/sliding-window/) of length $k$ over an array are one PUSH per item and one POP for each item that leaves:

```pseudo id=window
SLIDING-MIN(A, k)                              ▷ A[0 .. n − 1], 1 ≤ k ≤ n
W1  NEW()
W2  for r ← 0 to n − 1 do
W3      PUSH(A[r])
W4      if t − h > k then POP()
W5      if r ≥ k − 1 then output MIN()         ▷ min of A[r − k + 1 .. r]
```

## Example

Run SLIDING-MIN on $A = [4, 2, 12, 3, 8, 5, 1, 7]$ with $k = 3$. Each pair is written as position:item.

| $r$ | $A[r]$ | PUSH removes from the back | POP | $D$ after the round | output |
|---|---|---|---|---|---|
| 0 | 4 | none | | 0:4 | |
| 1 | 2 | 0:4 | | 1:2 | |
| 2 | 12 | none | | 1:2, 2:12 | 2 |
| 3 | 3 | 2:12 | position 0 is not in $D$; only $h$ moves | 1:2, 3:3 | 2 |
| 4 | 8 | none | removes 1:2 | 3:3, 4:8 | 3 |
| 5 | 5 | 4:8 | position 2 is not in $D$ | 3:3, 5:5 | 3 |
| 6 | 1 | 5:5, then 3:3 | position 3 was removed by PUSH | 6:1 | 1 |
| 7 | 7 | none | position 4 is not in $D$ | 6:1, 7:7 | 1 |

The outputs $[2, 2, 3, 3, 1, 1]$ are the minimums of the six windows. In round 6, one PUSH removes two pairs, and in round 4 the POP removes the front. Over the 8 rounds, PUSH removes 5 pairs in total, fewer than the 8 pairs added.

## Correctness

Each operation keeps (I1) and (I2), and then MIN returns $\min Q$. NEW makes $Q$ and $D$ empty. PUSH of $x$ at position $t$ keeps exactly the pairs with $x_j < x$, which by (I1) and the increasing order are a prefix of $D$, and adds $(t, x)$: these are the strict suffix minima of the longer sequence. POP removes position $h$, which is the front pair if it is in $D$ at all, by (I2). For MIN, the last position $j^\ast$ of the minimum of $Q$ satisfies (I1), and no position of $D$ has a smaller item, so the front of $D$, which has the least item of $D$, is $\min Q$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $n$ be the number of operations in a sequence that starts from NEW. Each PUSH adds one pair, and each pair is removed at most once, by line L3 or by line L6. So the loop of lines L2 and L3 runs at most $n$ times over the whole sequence, and the total time is $O(n)$. With the potential $\Phi = |D|$, a PUSH that removes $p$ pairs costs $p + 1$ units and changes $\Phi$ by $1 - p$, so its amortized cost is 2.

| operation | worst case | amortized |
|---|---|---|
| NEW | $O(1)$ | $O(1)$ |
| PUSH | $\Theta(\lvert D \rvert)$ | $O(1)$ |
| POP | $O(1)$ | $O(1)$ |
| MIN | $O(1)$ | $O(1)$ |
| SLIDING-MIN on $n$ items | $\Theta(n)$ | |
| space | $O(\lvert Q \rvert)$ pairs, at most $k$ in a window of length $k$ | |

The space reaches $|Q|$ when the items of $Q$ strictly increase, and drops to one pair after a push of a new minimum. Each PUSH makes at most one failing comparison, so SLIDING-MIN makes at most $2n$ item comparisons. Lemire gives a refinement for the minimum and the maximum at once with at most three comparisons per item.

## Variants

- **Maximum.** Replace $\ge$ by $\le$ in line L2. The items then strictly decrease from the front, and the front is the maximum. The [sliding window maximum](/sliding-window-maximum-deque/) algorithm is this version.
- **Without positions.** Store only the items, keep equal items (remove only items strictly greater than $x$ in line L2), and give POP the item that leaves: POP$(y)$ removes the front if it equals $y$. This is method 1 of cp-algorithms. It needs the caller to know the leaving item.
- **Windows of varying length.** Nothing in the operations needs a fixed $k$. Two-pointer methods that move each end forward only use the same PUSH and POP, for example the [monotonic deque on prefix sums](/monotonic-deque-prefix-sums/) for the shortest subarray with a sum of at least a bound.
- **Dynamic programming.** A recurrence $f(i) = \min_{i - k \le j < i} f(j) + c(i)$ is computed in $\Theta(n)$ time by a monotonic deque over the values $f(j)$, instead of $\Theta(nk)$. This is the usual speed-up of the bounded knapsack and of many window recurrences.
- **Two stacks.** A [queue from two stacks](/two-stacks-queue/), each stack with its running minimum, gives the same operations with $O(1)$ amortized cost, keeps all items, and works for any associative operation, not only the minimum.

## When to use it

Use a monotonic deque when items enter at one end and leave at the other in the same order, and you need the minimum or the maximum after each step. It is the simplest $\Theta(n)$ solution of the sliding window minimum, faster than a heap with lazy deletion ($O(n \log n)$) and than a [sparse table](/sparse-table/) built in advance ($O(n \log n)$ space). Use the two-stack queue when the aggregate is not a minimum or a maximum (a sum modulo $m$, a gcd, a matrix product), because the deque relies on domination, and dominated items exist only for an order. Use a balanced search tree or a heap when items leave in an order other than the order they came.

## Pitfalls

- **Mixing the two tie rules.** With positions, line L2 removes items $\ge x$ and line L6 tests the position. With values only, line L2 must remove only items $> x$ and POP tests the value. A mix fails: with removal of items $\ge x$ and a value test, PUSH(2), PUSH(2) leaves only the second 2 in the deque, and a POP of the first 2 then removes it, although a 2 is still in the queue. The test case is $A = [2, 2, 5]$ with $k = 2$, whose window minimums are $[2, 2]$.
- **An off-by-one in the window test.** Line W4 pops when the queue holds $k + 1$ items, after the push. With the test $t - h \ge k$, each window is one item short. For $A = [1, 3]$ and $k = 2$, the program then outputs 3 instead of 1.
- **Storing only positions and reading the array.** This works for a sliding window over a fixed array, but not for a stream, where the item at a position is gone. Store the item with the position.
- **A per-operation bound.** PUSH is $O(1)$ only amortized. For a hard real-time bound on each operation, use another structure.

## Implementations

## History

The deque method for the sliding window minimum is a standard tool of programming contests, and it has no clear first source. Lemire published an analysis of the streaming version in 2006 with at most three comparisons per item for the minimum and the maximum together. Laaksonen's handbook presents it in the chapter on amortized analysis, next to the nearest smaller elements of the [monotonic stack](/monotonic-stack/).

## References
