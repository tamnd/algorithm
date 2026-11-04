---
tag: PR4H8X
kind: data-structure
slug: min-stack
name: Stack with minimum
aliases:
- Stack with minimum (Minimum Stack)
area: data-structures/linear-structures
level: intro
summary: A stack that also returns its current minimum element in constant time by storing the running minimum with each entry.
implements: [stack]
prereqs: [stack]
see_also: [min-queue, monotonic-stack, monotonic-deque, two-stacks-queue, sliding-window-maximum, priority-queue, dynamic-array]
sources:
  - url: https://cp-algorithms.com/data_structures/stack_queue_modification.html
    title: cp-algorithms, Minimum stack / Minimum queue
    locator: the section Stack modification
  - paper: "Hania Gajewska and Robert E. Tarjan, Deques with heap order, Information Processing Letters 22(4) (1986)"
    locator: the problem statement, a deque with a find-minimum operation, and the reduction to stacks
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.1, the stack operations that the structure extends
---

A stack with minimum is a [stack](/stack/) that also answers `min`, the least item it holds, in $O(1)$ worst-case time. It stores with each entry the minimum of that entry and all entries below it, so the answer is always in the top entry. Push, pop, top and min each cost $O(1)$, and the space is two cells per item. It is the building block of the [queue with minimum](/min-queue/), and through it of sliding-window minimum and maximum algorithms.

## In plain words

You stack boxes, each with a number written on it, and you want to know the smallest number in the pile at any time. Searching the whole pile is slow. Instead, when you put a box down, you also write on it a second number: the smallest number in the pile so far, including this box. To get that number, you compare the new number with the second number on the box below.

Now the answer is always on the top box. When you take the top box off, the box below shows the smallest number of the rest of the pile, which is exactly right, because the pile below did not change.

## The abstract type

The structure implements the [stack](/stack/) type: `push(S, x)`, `pop(S)`, `top(S)` and `is_empty(S)`. It adds one query, `min(S)`, which returns the least item of a non-empty stack and does not change the stack. The items come from a set with a total order.

It does not support removing the minimum. Only the top item can leave. This is why $O(1)$ time is possible here. A [priority queue](/priority-queue/) can remove the minimum, so it can sort, and in the [comparison model](/comparison-model/) its insert and delete-min together need $\Omega(\log n)$ amortized comparisons.

## Representation

The structure is one stack of pairs $(x, m)$. From the bottom to the top, the pairs are $(x_1, m_1), \ldots, (x_k, m_k)$. The user's stack is $\langle x_1, \ldots, x_k \rangle$.

**Invariant.** $m_j = \min\{x_1, \ldots, x_j\}$ for each $1 \le j \le k$.

The stack of pairs can be a [dynamic array](/dynamic-array/) or a linked list.

## Operations

```pseudo id=main
PUSH(S, x)
L1  if S is empty then m ← x else m ← min(x, the m of the top pair)
L2  push the pair (x, m) on S
POP(S)                                     ▷ S is not empty
L3  (x, m) ← pop the top pair of S
L4  return x
TOP(S)                                     ▷ S is not empty
L5  return the x of the top pair
MIN(S)                                     ▷ S is not empty
L6  return the m of the top pair
```

PUSH computes the running minimum with one comparison and pushes it with the item. POP, TOP and MIN only look at the top pair. Each operation does a constant number of steps on top of one stack operation, so each costs $O(1)$ in the worst case on a linked list or a fixed array, and $O(1)$ amortized on a dynamic array.

**The lean variant.** Many entries repeat the same minimum. A second stack $Q$ can hold only the minima: push $x$ on $Q$ when $Q$ is empty or $x \le \text{top}(Q)$, and pop $Q$ when the item popped from the main stack equals $\text{top}(Q)$. Then MIN returns $\text{top}(Q)$. The worst case is the same, $2n$ cells for a non-increasing input, but on random input $Q$ stays short.

## Example

Push 5, 3, 7, 3, 2, then pop four times. A pair is written $(x, m)$, from the bottom to the top.

| operation | pairs after it | result | min after it |
|---|---|---|---|
| push(5) | (5,5) | | 5 |
| push(3) | (5,5) (3,3) | | 3 |
| push(7) | (5,5) (3,3) (7,3) | | 3 |
| push(3) | (5,5) (3,3) (7,3) (3,3) | | 3 |
| push(2) | (5,5) (3,3) (7,3) (3,3) (2,2) | | 2 |
| pop | (5,5) (3,3) (7,3) (3,3) | 2 | 3 |
| pop | (5,5) (3,3) (7,3) | 3 | 3 |
| pop | (5,5) (3,3) | 7 | 3 |
| pop | (5,5) | 3 | 5 |

After the second pop, the minimum is still 3, because the first 3 is still in the stack. The lean variant pushes 5, 3, 3 and 2 on $Q$, since the second 3 satisfies $3 \le 3$. It pops $Q$ on the pops of 2, of the second 3 and of the first 3, and leaves $Q = \langle 5 \rangle$ at the end.

## Correctness

The invariant holds for the empty stack. PUSH sets $m_{k+1} = \min(x, m_k) = \min\{x_1, \ldots, x_{k+1}\}$ by the invariant for $k$, and leaves the lower pairs unchanged. POP removes the top pair and changes no other pair, so the invariant still holds for the rest. MIN returns $m_k$, which is the least item by the invariant. The full proof, with the proof of the lean variant, is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | comparisons |
|---|---|---|
| push | $O(1)$ worst case | 1 (0 on an empty stack) |
| pop, top | $O(1)$ worst case | 0 |
| min | $O(1)$ worst case | 0 |
| space | $2n$ cells | |

The times are worst case on a linked list or a fixed array, and amortized on a dynamic array. The lean variant uses $n + q$ cells, where $q$ is the number of prefix minima with repeats; $q$ is $n$ for a non-increasing input and 1 for an increasing input.

## Variants

- **Maximum or any associative operation.** Replace min by max, gcd, sum or any associative operation $\oplus$. Each entry stores $x_1 \oplus \cdots \oplus x_j$. This is the base of [sliding-window aggregation](/sliding-window-aggregation/).
- **Lean variant.** The second stack of minima above saves space when the minimum changes rarely.
- **Difference encoding.** For integers, store $x - m$ instead of the pair, and keep the current minimum in one variable. A negative stored value marks a new minimum. This uses one cell per item, but $x - m$ can overflow a fixed-width integer.
- **Queue with minimum.** Two stacks with minimum make a [queue with minimum](/min-queue/), with $O(1)$ amortized per operation.
- **Deque with minimum.** Gajewska and Tarjan (1986) gave a deque with a find-minimum operation in $O(1)$ worst-case time per operation.

## When to use it

Use a stack with minimum when a stack-shaped process must also know its smallest or largest element: the undo history of a value, the open intervals of a scan, or as one half of a queue with minimum. If the program must also remove the minimum, use a [priority queue](/priority-queue/) instead. If it needs the minimum of every window of a fixed width, a [monotonic deque](/monotonic-deque/) does it with one structure.

## Pitfalls

- **Strict test in the lean variant.** If the push test is $x < \text{top}(Q)$ instead of $x \le \text{top}(Q)$, then after push 2, push 1, push 1 and one pop, $Q$ is $\langle 2 \rangle$ and MIN returns 2 while the stack still holds 1. Repeated minima must be pushed.
- **Empty stack in line L1.** On an empty stack there is no top pair to read. The test of line L1 is necessary; a sentinel of $+\infty$ at the bottom also works.
- **Equality test on floating-point values.** The lean variant compares the popped item with $\text{top}(Q)$ for equality. With NaN values, equality fails and $Q$ goes out of step. The pair form has no equality test.
- **Overflow in the difference encoding.** With 64-bit integers, $x - m$ overflows when $x$ and $m$ are far apart. Use the pair form, or a wider type.

## Implementations

## History

The method of storing the running minimum with each entry is folklore, and we do not know its first publication. Gajewska and Tarjan (1986) solved the harder problem of a deque with heap order, where items enter and leave at both ends and the minimum must still be found in constant time.

## References
