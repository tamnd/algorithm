---
tag: 85C150
kind: technique
slug: stack-from-two-queues
name: Stack from two queues
aliases:
- Stack implemented with two queues
area: data-structures/linear-structures
level: intro
summary: Implementing a stack using two queues, where one queue holds the elements and the other helps reorder them.
prereqs: [stack, queue, amortized-cost]
see_also: [min-queue, deque, sliding-window-maximum, accounting-method, steque]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 10.1 (Stacks and queues), Exercise 10.1-6 (a queue from two stacks) and Exercise 10.1-7 (a stack from two queues)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3 (Bags, Queues, and Stacks), the stack and queue APIs that the construction uses
  - url: https://leetcode.com/problems/implement-stack-using-queues/
    title: LeetCode 225, Implement Stack using Queues
    locator: the problem statement, which allows only push to back, peek and pop from front, size and is empty on the queues
---

A stack from two queues is the construction of a [stack](/stack/) whose only storage is two [queues](/queue/), used through their own operations: enqueue at the back, dequeue at the front, size and the empty test. One queue holds the items in stack order, and the other is scratch space for the rotation that turns the queue order around. Either push or pop then costs $\Theta(n)$ queue operations, so the construction is an exercise in reasoning about the two orders, not a practical stack; its mirror image, the queue from two stacks, is practical, with $O(1)$ [amortized cost](/amortized-cost/) per operation.

## In plain words

A queue lets the oldest item out first. A stack must let the newest item out first. Those are opposite orders, so a queue cannot hand back its newest item without first passing all the older items out of the way.

The trick uses a second queue as a waiting room. One way: when a new item arrives, put it alone in the empty queue, then move all the old items behind it, one by one. Now the newest item is at the front, and the next removal takes it. The other way: let items pile up in arrival order, and at removal time move all items but the last one to the other queue, then take the last one. Either way, one of the two actions moves every stored item.

## When it applies

- You must give a stack interface, but the storage you are allowed to use is a FIFO channel, a message queue, or a library queue with no access to its back.
- A puzzle or interview question asks for one container type built from another. The signal is "using only the operations of".
- You are proving that two container types are equivalent in power, up to cost, and need the simulation in one direction.

It does not apply when the queue also allows access at both ends: that is a [deque](/deque/), and a deque is already a stack.

## The template

The template has one hole, the side that pays: push or pop. Both variants keep the invariant that all items are in the queue $Q_1$ and the queue $Q_2$ is empty between operations.

```pseudo id=main
PUSH(S, x)                                 ▷ variant A: push pays
L1  ENQUEUE(Q2, x)
L2  while not IS-EMPTY(Q1) do
L3      ENQUEUE(Q2, DEQUEUE(Q1))
L4  swap the names Q1 and Q2               ▷ Q1 holds the stack, newest at the front
POP(S)                                     ▷ variant A
L5  return DEQUEUE(Q1)

PUSH'(S, x)                                ▷ variant B: pop pays
L6  ENQUEUE(Q1, x)                         ▷ Q1 holds the stack, newest at the back
POP'(S)                                    ▷ variant B, Q1 not empty
L7  while SIZE(Q1) > 1 do
L8      ENQUEUE(Q2, DEQUEUE(Q1))
L9  x ← DEQUEUE(Q1)
L10 swap the names Q1 and Q2
L11 return x
```

**Variant A.** The invariant is: $Q_1$ holds the stack with the top at the front. Line L1 puts the new item into the empty $Q_2$, so it is the front of $Q_2$. Lines L2 and L3 move the old items, which are in stack order with the old top first, behind it. So $Q_2$ now holds the new top, then the old stack in order, and line L4 makes it $Q_1$. Pop is one dequeue. A push on a stack of $k$ items makes $k + 1$ enqueues and $k$ dequeues, so $n$ pushes from the empty stack make $\sum_{k=0}^{n-1} (2k + 1) = n^2$ queue operations.

**Variant B.** The invariant is: $Q_1$ holds the stack with the top at the back. Push is one enqueue. Pop moves the $k - 1$ items in front of the top to $Q_2$, in the same order (lines L7 and L8), takes the top (line L9), and swaps (line L10). So $n$ pushes and then $n$ pops make $n + \sum_{k=1}^{n} (2k - 1) = n^2 + n$ queue operations. A `top` in this variant can cache the last pushed item, or do a pop and push the item back.

**One queue is enough.** In variant A, the rotation can use the same queue: enqueue $x$, then do $k$ times ENQUEUE(Q, DEQUEUE(Q)). This makes $2k + 1$ operations, as before, and needs no second queue.

**Example.** Variant A, push 1, 2, 3, 4 and then pop twice. The front of $Q_1$ is on the left.

| step | operation | $Q_1$ after | queue operations so far |
|---|---|---|---|
| 1 | push 1 | [1] | 1 |
| 2 | push 2 | [2, 1] | 4 |
| 3 | push 3 | [3, 2, 1] | 9 |
| 4 | push 4 | [4, 3, 2, 1] | 16 |
| 5 | pop, returns 4 | [3, 2, 1] | 17 |
| 6 | pop, returns 3 | [2, 1] | 18 |

**Why no variant is cheap.** Variant A costs $2k + 1$ on every push and variant B costs $2k - 1$ on every pop, whatever came before, so neither has an $O(1)$ amortized bound: the sequences above cost $\Theta(n^2)$ for $\Theta(n)$ operations. The reason is that one rotation does not leave a state that helps the next operation. Compare the queue from two stacks, where one transfer reverses the order once and for all.

## Classic examples

- **Queue from two stacks** (the mirror image, on the [queue](/queue/) page). Push on an inbox stack; pop from an outbox stack, and refill the outbox from the inbox only when it is empty. Each item moves once, so each operation costs $O(1)$ amortized by the [accounting method](/accounting-method/), and $\Theta(n)$ in the worst case.
- **Min-queue from two min-stacks.** A [min-queue](/min-queue/) applies the two-stack queue to stacks that each keep the minimum of their items, so the queue minimum is the smaller of the two stack minima, in $O(1)$ amortized time per operation.
- **Sliding window maximum.** The [sliding window maximum](/sliding-window-maximum/) problem can be solved with the two-stack max-queue: push each new item, pop the item that leaves the window, and read the maximum, for $O(n)$ total time.
- **Deque from two stacks.** A [deque](/deque/) can be built from two stacks, one for each end. When one stack is empty and a pop needs it, split the other stack in half and rebuild both. This gives $O(1)$ amortized time per operation.
- **Steque from a stack and a queue.** A [steque](/steque/) can be built from a linked list directly, but also from a stack for the pushed items and a queue for the enqueued ones, since every pushed item still present leaves before every enqueued one.

## Variations

- **Push pays or pop pays** (variants A and B). Choose A when pops are more frequent, B when pushes are.
- **One queue** with rotation, as above.
- **Lazy top.** In variant B, keep the last pushed item in a field, so `top` costs $O(1)$; after a pop, the new top is the last item moved in line L8.

## Pitfalls

- **Forgetting the swap.** Without line L4, the stack is left in $Q_2$, and the next push moves the wrong queue. Without line L10, the moved items stay in $Q_2$ and the next pop finds $Q_1$ empty.
- **Peeking at the back.** Code that reads the back of a queue, or indexes it, is not using a queue. Many library queues allow this, and then the construction is trivial and the exercise is missed.
- **An empty pop in variant B.** The loop of line L7 runs while the size is more than 1. If $Q_1$ is empty, line L9 fails. Test for the empty stack first.
- **Top that destroys order.** Implementing `top` in variant B as POP' without pushing the item back loses the item.
- **Claiming an amortized bound.** The cost per operation is $\Theta(n)$ on the sequences of the template, in both variants, so a claim of $O(1)$ amortized time is false.

## Exercises

1. In variant A, count the enqueues and the dequeues separately for $n$ pushes from the empty stack. (Answer: $n(n+1)/2$ enqueues and $n(n-1)/2$ dequeues.)
2. In variant B, give a sequence of $2n$ operations whose cost is $\Theta(n^2)$ even if pops and pushes alternate. (Hint: push $n$ items first, then alternate pop and push.)
3. Build a queue from two stacks and prove the amortized bound with a potential function equal to twice the number of items in the inbox.

## References
