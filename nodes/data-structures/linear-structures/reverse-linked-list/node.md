---
tag: X89XHB
kind: algorithm
slug: reverse-linked-list
name: In-place linked list reversal
aliases:
- iterative list reversal
area: data-structures/linear-structures
level: intro
summary: Reverse a singly linked list in O(n) time and O(1) extra space by re-pointing each node.
solves: [list-reversal]
model: word-ram
complexity:
  vars: {n: the number of nodes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {in_place: true, deterministic: true, recursive: false}
prereqs: [singly-linked-list, pointer, loop-invariant]
see_also: [list-reversal, doubly-linked-list, linked-list, xor-linked-list, floyd-cycle-detection]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 10.2, Exercise 10.2-7 (a Θ(n) nonrecursive reversal of a singly linked list with constant extra storage)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3, Exercise 1.3.30 (destructive reversal of a linked list, given its first node)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.3 (Linked allocation)
---

In-place list reversal turns a [singly linked list](/singly-linked-list/) $x_1 \to x_2 \to \dots \to x_n$ into $x_n \to \dots \to x_1$ by changing the next [pointer](/pointer/) of each node, without allocating any node. It solves the [list reversal](/list-reversal/) problem in $\Theta(n)$ time with $\Theta(1)$ extra space: one pass over the list, three pointer variables and one pointer write per node. It is a basic step in many list algorithms, for example the check that a list is a palindrome and the reversal of a list in groups of $k$ nodes.

## In plain words

Think of a line of people where each person points at the person behind them. You want the line to point the other way. Walk along the line from the front. At each person, first remember who is behind them, because you are about to lose that link. Then turn the person around so that they point at the person you visited just before. Step to the person you remembered and do the same again.

At each moment the line has two parts: the people you have turned, who now form a reversed line, and the people you have not reached yet, who are still in their old order. When no one is left, the last person you turned is the new front of the line.

## The problem

The input is the first node $head$ of a singly linked list with nodes $x_1, \dots, x_n$, where $x_i.next = x_{i+1}$ for $i < n$ and $x_n.next = \text{nil}$. The list has no cycle. For $n = 0$, $head = \text{nil}$. The output is the first node of a list with the same nodes in the order $x_n, x_{n-1}, \dots, x_1$: after the call, $x_{i+1}.next = x_i$ for $1 \le i < n$ and $x_1.next = \text{nil}$. The keys stay in their nodes, and no node is created or freed.

## The algorithm

```pseudo id=main
REVERSE(head)                       ▷ head is the first node, or nil
L1  prev ← nil
L2  curr ← head
L3  while curr ≠ nil do
L4      next ← curr.next            ▷ save the rest before the link is lost
L5      curr.next ← prev            ▷ turn the link of curr
L6      prev ← curr
L7      curr ← next
L8  return prev
```

The variable $prev$ is the first node of the part that is already reversed, and $curr$ is the first node of the part that is not yet visited. Line L4 saves the pointer to the rest of the list, because line L5 overwrites $curr.next$. Line L5 makes $curr$ the new first node of the reversed part. Lines L6 and L7 move both pointers one node to the right. When $curr$ is nil, all nodes are in the reversed part, and $prev$ is its first node, the old last node $x_n$. For an empty list the loop does not run and line L8 returns nil.

## Example

Reverse the list $1 \to 2 \to 3 \to 4 \to 5$. The table shows the state at each test of line L3, after $k$ iterations of the loop.

| $k$ | $prev$ | $curr$ | reversed part (from $prev$) | rest (from $curr$) |
|---|---|---|---|---|
| 0 | nil | 1 | (empty) | 1 → 2 → 3 → 4 → 5 |
| 1 | 1 | 2 | 1 | 2 → 3 → 4 → 5 |
| 2 | 2 | 3 | 2 → 1 | 3 → 4 → 5 |
| 3 | 3 | 4 | 3 → 2 → 1 | 4 → 5 |
| 4 | 4 | 5 | 4 → 3 → 2 → 1 | 5 |
| 5 | 5 | nil | 5 → 4 → 3 → 2 → 1 | (empty) |

In the third iteration, line L4 saves $next = 4$, line L5 sets the next pointer of node 3 from 4 to 2, and lines L6 and L7 set $prev = 3$ and $curr = 4$. The loop runs 5 times, makes 5 pointer writes, and line L8 returns node 5.

## Correctness

The proof uses this [loop invariant](/loop-invariant/) of line L3. After $k$ iterations, $prev$ is the first node of the list $x_k \to x_{k-1} \to \dots \to x_1 \to \text{nil}$ (nil when $k = 0$), $curr = x_{k+1}$ (nil when $k = n$), and the links $x_{k+1} \to \dots \to x_n \to \text{nil}$ are not changed. One iteration moves $x_{k+1}$ from the front of the rest to the front of the reversed part. The quantity $n - k$ drops by exactly 1 in each iteration, so the loop stops after $n$ iterations, and then the invariant with $k = n$ says that $prev$ is the first node of $x_n \to \dots \to x_1$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The loop of lines L3 to L7 runs exactly $n$ times, once for each node, and each iteration does a constant number of reads and writes of pointers. Lines L1, L2 and L8 run once. So the time is $\Theta(n)$ in the best, the average and the worst case on the [word RAM](/word-ram/), and the algorithm makes exactly $n$ writes to next fields. The extra space is the three pointers $prev$, $curr$ and $next$, so it is $\Theta(1)$.

No algorithm can do better than $\Omega(n)$ time: each of the $n$ nodes must get a new next pointer when $n \ge 2$ (each $x_i$ with $i < n$ changes from $x_{i+1}$ to $x_{i-1}$ or nil, and $x_n$ changes from nil to $x_{n-1}$), and one step writes one field.

## Properties

- **In place.** The algorithm reuses the $n$ nodes and needs only three pointer variables.
- **One pass.** Each node is read and written once, in list order, so the access pattern is sequential.
- **Not recursive.** A recursive version is shorter to write, but it uses $\Theta(n)$ stack space (see Variants).
- **Destructive.** The input list does not exist after the call. A caller that keeps a pointer to the old $head$ now holds the last node of the result.

## Variants and improvements

- **Recursive reversal.** Reverse the rest $x_2 \to \dots \to x_n$, then set $x_2.next \leftarrow x_1$ and $x_1.next \leftarrow \text{nil}$. It takes $\Theta(n)$ time but $\Theta(n)$ stack space, and a long list overflows the call stack in most languages.
- **Persistent reversal.** In a functional language, build a new list by pushing each item of the old list on the front of an accumulator. It takes $\Theta(n)$ time and $\Theta(n)$ new nodes, and the old list stays valid.
- **Doubly linked lists.** For a [doubly linked list](/doubly-linked-list/), swap the $next$ and $prev$ fields of each node and swap the head and the tail. An [XOR linked list](/xor-linked-list/) needs no change at all: swapping its head and its tail reverses it in $O(1)$ time.
- **Reverse a part.** To reverse the nodes at positions $m$ to $r$, walk to the node before position $m$, run the loop for $r - m + 1$ iterations, and then link the two ends of the reversed part to the rest. The same step, repeated, reverses a list in groups of $k$ nodes.
- **Palindrome test.** Find the middle with a slow and a fast pointer, reverse the second half, compare the two halves, and reverse the second half again to restore the list. This uses $O(1)$ extra space.

## When to use it

Use the iterative loop whenever a singly linked list must be reversed and the old order is no longer needed: it is the fastest method and uses constant memory. Use the persistent version when other parts of the program still hold the old list. If the program reverses often, use a doubly linked list or a [deque](/deque/), which can be read in both directions without any reversal.

## Pitfalls

- **Losing the rest of the list.** Writing line L5 before line L4 sets $curr.next$ to $prev$ and then reads that new value as $next$. In the first iteration $prev$ is nil, so the loop stops at once and returns only the first node, and the other nodes are lost. Save $next \leftarrow curr.next$ first. The test with a list of 2 or more nodes catches this.
- **Returning the wrong node.** Returning $head$ instead of $prev$ in line L8 returns the old first node, which is now the last node, so the caller sees a list of one item. Return $prev$.
- **Not clearing the old head.** A version that starts with $prev \leftarrow head$, $curr \leftarrow head.next$ must also set $head.next \leftarrow \text{nil}$; else the old first and second nodes form a cycle. Starting with $prev \leftarrow \text{nil}$, as in line L1, handles this and the empty list without a special case.
- **Cycles.** On a list with a cycle the loop never stops. If the input may have a cycle, test it first with [Floyd's cycle detection](/floyd-cycle-detection/).
- **Recursion depth.** The recursive variant fails on long lists in Python, Java and C. Use the loop.

## Implementations

## History

The in-place reversal of a linked list is a standard exercise of the first textbooks on list processing. Knuth's Section 2.2.3 treats linked allocation, and the reversal appears as an exercise in CLRS (Exercise 10.2-7 of the third edition, which asks for a nonrecursive $\Theta(n)$ procedure with constant extra storage) and in Sedgewick and Wayne (Exercise 1.3.30).

## References
