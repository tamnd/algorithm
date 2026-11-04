---
tag: YA1PKH
kind: problem
slug: list-reversal
name: List reversal
aliases:
- reverse a linked list
area: data-structures/linear-structures
level: intro
summary: Reverse the order of the nodes in a linked list.
prereqs: [linked-list]
see_also: [reverse-linked-list, singly-linked-list, doubly-linked-list, stack, floyd-cycle-detection, circular-linked-list, loop-invariant, array]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.3 (Linked allocation), exercise 7, inverting a linked linear list in place
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3, exercise 1.3.30, reversing a linked list iteratively and recursively, without creating new nodes
---

List reversal is the problem of putting the nodes of a [singly linked list](/singly-linked-list/) in the opposite order, so that the last node becomes the first and each `next` pointer points to the node that was before it. The standard solution, [reverse linked list](/reverse-linked-list/), walks the list once with three pointers and turns each `next` pointer around, in $\Theta(n)$ time and $O(1)$ extra space, and no faster solution exists, since every pointer must change. The problem is a classic exercise on pointer manipulation and [loop invariants](/loop-invariant/), and it is a step in many list algorithms: palindrome tests, the addition of numbers stored as lists of digits, and reversal of groups of $k$ nodes.

## In plain words

A chain of paper clips hangs from your hand, and each clip holds the next one. You want the last clip at the top and the first at the bottom. With a chain, you cannot jump to the end; you can only work from the top down.

So take the clips off one at a time from the top, and hang each one on a new chain, at its top. The first clip you take ends at the bottom of the new chain, and the last clip ends at the top. You never need more than your two hands and the two chains: one clip in your hand, the rest of the old chain, and the new chain.

## Definition

**Input.** A pointer $h$ to the first node of a singly linked list with nodes $v_0, v_1, \ldots, v_{n-1}$, where $v_i.next = v_{i+1}$ for $i < n - 1$ and $v_{n-1}.next = $ NIL. The list may be empty ($h = $ NIL).

**Output.** A pointer to $v_{n-1}$, with $v_i.next = v_{i-1}$ for $1 \le i \le n - 1$ and $v_0.next = $ NIL. The same nodes are used: the keys do not move, and no node is created.

**Resources.** The usual requirement is $O(1)$ extra space besides the list. Without it, the problem is easy: push the nodes on a [stack](/stack/) and pop them.

## Variants

- **Array reversal.** For an [array](/array/), swap $A[i]$ and $A[n - 1 - i]$ for $i < n/2$, in place.
- **Doubly linked list.** Swap the `next` and `prev` fields of every node, and swap the head and tail pointers. With a sentinel ring, as on the [doubly linked list](/doubly-linked-list/) page, only the fields need swapping.
- **Sublist reversal.** Reverse the nodes from position $m$ to position $p$ and reconnect the two ends to the rest.
- **Groups of $k$.** Reverse each block of $k$ consecutive nodes, keeping the blocks in order.
- **Recursive reversal.** Reverse the rest of the list, then attach the first node at its end. It uses $\Theta(n)$ stack space.
- **Immutable lists.** When nodes cannot be changed, as in functional languages, build a new list by pushing the items on the front of an empty list, in $\Theta(n)$ time and $n$ new nodes.
- **Circular list.** Reverse the ring and move the pointer to the old successor of the last node.

## Examples

**The iterative method on 1 → 2 → 3 → 4.** The method keeps $prev$, the head of the part already reversed, and $cur$, the head of the part not yet reversed. Each step saves $cur.next$, points $cur.next$ to $prev$, then moves both pointers forward.

| step | reversed part (from $prev$) | rest (from $cur$) |
|---|---|---|
| start | empty | 1 → 2 → 3 → 4 |
| 1 | 1 | 2 → 3 → 4 |
| 2 | 2 → 1 | 3 → 4 |
| 3 | 3 → 2 → 1 | 4 |
| 4 | 4 → 3 → 2 → 1 | empty |

The method returns $prev$, the node with key 4. It made 4 writes of `next`, one per node.

**A sublist.** Reversing positions 2 to 4 of 1 → 2 → 3 → 4 → 5 gives 1 → 4 → 3 → 2 → 5. **Groups of 2.** Reversing 1 → 2 → 3 → 4 → 5 in groups of 2 gives 2 → 1 → 4 → 3 → 5, with the short last group left as it is in the usual convention.

**Palindrome test.** To test whether 1 → 2 → 2 → 1 reads the same both ways in $O(1)$ extra space, find the middle with a slow and a fast pointer, reverse the second half to 1 → 2, compare it with the first half 1 → 2, and reverse it back.

## Known algorithms

- **Iterative reversal with three pointers.** The method of the example: $\Theta(n)$ time, $n$ pointer writes, and three pointer variables. Its loop invariant is that $prev$ heads the reversal of the nodes already visited and $cur$ heads the nodes not yet visited, in their old order. It is the [reverse linked list](/reverse-linked-list/) algorithm, and it is Knuth's answer to exercise 2.2.3-7.
- **Recursive reversal.** For $n \le 1$, return the list. Otherwise reverse the list from $h.next$, set $h.next.next = h$ and $h.next = $ NIL, and return the new head. $\Theta(n)$ time and $\Theta(n)$ recursion depth, which can overflow the call stack for long lists.
- **Stack.** Push every node, then pop them and link them in the order popped. $\Theta(n)$ time and $\Theta(n)$ extra space.
- **Copy to an array.** Copy the node pointers to an array, then relink them in reverse. $\Theta(n)$ time and space; useful when the array is needed anyway.

## Bounds

**Lower bound.** For $n \ge 2$, every node's `next` field must change: $v_0.next$ goes from $v_1$ to NIL, and $v_i.next$ from $v_{i+1}$ (or NIL) to $v_{i-1}$ for $i \ge 1$. So any algorithm writes at least $n$ fields and takes $\Omega(n)$ time. The iterative method writes exactly $n$, so it is optimal in pointer writes as well as in time.

**Space.** $O(1)$ extra words are enough, and the iterative method uses three. The recursive method uses $\Theta(n)$ space on the call stack; a compiler that turns tail calls into jumps does not help, since its recursive call is not in tail position. A tail-recursive form with an accumulator, `reverse(cur, prev)`, is the iterative method written as recursion.

## Reductions

- **Stack.** Reversing a sequence is pushing it on a [stack](/stack/) and popping it. The iterative method uses the reversed part as that stack, built from the nodes themselves.
- **Cycle detection.** If the input has a cycle, the iterative method still stops: it goes around the cycle, then walks back along the reversed tail and ends at the original head. So, for a list of two or more nodes, the result is the original head exactly when there is a cycle, and running the method twice tells in $O(n)$ time and $O(1)$ space whether the list has a cycle, and restores the list, without the two pointers of [Floyd's method](/floyd-cycle-detection/).
- **Order of a walk.** Many list procedures build their output by pushing at the front, which gives the reverse order; one reversal at the end gives the right order in $\Theta(n)$ total time.

## Applications

- **Arithmetic on numbers stored as lists of digits**, where the digits are stored from the most significant one and the addition must start from the least significant one.
- **Palindrome tests and comparisons of the two halves** of a list in constant extra space.
- **List algorithms that build in reverse**, such as `map` with an accumulator in functional languages, followed by one reversal.
- **Undo of a sequence of steps**, which replays them in the reverse order.

## References
