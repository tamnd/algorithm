---
tag: TQ9X45
kind: abstract-type
slug: steque
name: Steque
area: data-structures/linear-structures
level: intro
summary: A data type combining stack and queue, supporting push, pop and enqueue, where enqueue adds an item at the end.
prereqs: [stack, queue]
see_also: [deque, singly-linked-list, circular-buffer, randomized-queue, generalized-queue]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3 (Bags, Queues, and Stacks), Exercise 1.3.32 (Steque)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.2.1 (Stacks, queues, and deques), the output-restricted deque and its exercises on the permutations it can make
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.2 (Linked lists), the linked list with a head and the insertion at either end
---

A steque, short for *stack-ended queue*, is an abstract data type that holds a sequence of items and supports three changes: `push` adds an item at the top, `pop` removes the item at the top, and `enqueue` adds an item at the bottom. So it is a [stack](/stack/) that also lets items join at the far end, or a [queue](/queue/) that also lets items cut in at the front. Knuth calls the same type an *output-restricted [deque](/deque/)*: items enter at both ends but leave at one. A [singly linked list](/singly-linked-list/) with head and tail pointers gives each operation in $\Theta(1)$ worst-case time.

## In plain words

Think of a line at a counter where the clerk always serves the person at the head of the line. Normal customers join at the end of the line. A customer with an urgent need may step in at the head of the line, and is then served next. Nobody ever leaves from the end.

A steque in a program works the same way. One action puts an item at the head, another puts an item at the end, and the only way out is at the head. If you only use the head, it behaves like a pile of plates. If you only add at the end, it behaves like a fair waiting line.

## Operations

A steque over a set $T$ of items is a value $S$. Its state is a finite sequence $\langle x_1, \dots, x_k \rangle$ of items of $T$, with $x_1$ at the top and $x_k$ at the bottom, and $k \ge 0$.

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}() \to S$ | the empty steque $\langle \rangle$ |
| `push` | $\text{push}(S, x) \to S$ | $\langle x_1, \dots, x_k \rangle$ becomes $\langle x, x_1, \dots, x_k \rangle$ |
| `enqueue` | $\text{enqueue}(S, x) \to S$ | $\langle x_1, \dots, x_k \rangle$ becomes $\langle x_1, \dots, x_k, x \rangle$ |
| `pop` | $\text{pop}(S) \to (x, S)$ | for $k \ge 1$: returns $x_1$, and the steque becomes $\langle x_2, \dots, x_k \rangle$ |
| `top` | $\text{top}(S) \to x$ | for $k \ge 1$: returns $x_1$ and does not change $S$ |
| `is_empty`, `size` | $S \to \text{bool}$, $S \to \mathbb{N}$ | test $k = 0$; return $k$ |

`pop` and `top` on the empty steque are errors. There is no operation that removes the bottom item: a type with it is a deque.

### Example

Start with the empty steque. The top is on the left.

| step | operation | result | steque after |
|---|---|---|---|
| 1 | push 4 | | $\langle 4 \rangle$ |
| 2 | enqueue 9 | | $\langle 4, 9 \rangle$ |
| 3 | push 1 | | $\langle 1, 4, 9 \rangle$ |
| 4 | enqueue 6 | | $\langle 1, 4, 9, 6 \rangle$ |
| 5 | pop | 1 | $\langle 4, 9, 6 \rangle$ |
| 6 | pop | 4 | $\langle 9, 6 \rangle$ |
| 7 | enqueue 2 | | $\langle 9, 6, 2 \rangle$ |
| 8 | pop | 9 | $\langle 6, 2 \rangle$ |
| 9 | pop | 6 | $\langle 2 \rangle$ |
| 10 | size | 1 | $\langle 2 \rangle$ |

The pushed items 1 and 4 come out in the reverse order of their pushes, as from a stack. The enqueued items 9, 6 and 2 come out in the order of their enqueues, as from a queue. And every pushed item still present leaves before every enqueued item still present.

## Laws

Each implementation meets these equations, for each steque $S$ and items $x, y$:

$$\begin{aligned}
&(\text{T1})\quad \text{is\_empty}(\text{new}()) = \text{true}, \qquad \text{is\_empty}(\text{push}(S, x)) = \text{is\_empty}(\text{enqueue}(S, x)) = \text{false},\\
&(\text{T2})\quad \text{pop}(\text{push}(S, x)) = (x, S), \qquad \text{top}(\text{push}(S, x)) = x,\\
&(\text{T3})\quad \text{pop}(\text{enqueue}(S, x)) = \begin{cases} (x, \text{new}()) & \text{if } \text{is\_empty}(S),\\ (y, \text{enqueue}(S', x)) & \text{else, where } (y, S') = \text{pop}(S), \end{cases}\\
&(\text{T4})\quad \text{push}(\text{enqueue}(S, x), y) = \text{enqueue}(\text{push}(S, y), x), \qquad \text{push}(\text{new}(), x) = \text{enqueue}(\text{new}(), x),\\
&(\text{T5})\quad \text{size}(\text{new}()) = 0, \qquad \text{size}(\text{push}(S, x)) = \text{size}(\text{enqueue}(S, x)) = \text{size}(S) + 1.
\end{aligned}$$

For each nonempty $S$, $\text{top}(S)$ is the first part of $\text{pop}(S)$, so the laws of pop also fix top. Law (T2) is the law of a stack and law (T3) is the law of a queue, with pop in the role of dequeue. Law (T4) says that the two ends do not interact: an item added at the bottom and an item added at the top can be added in either order, and in an empty steque the two ends are the same place. Each law holds in the sequence model of the table: for (T4), both sides are $\langle y, x_1, \dots, x_k, x \rangle$; for (T3), if $k \ge 1$ both sides remove $x_1$ and leave $\langle x_2, \dots, x_k, x \rangle$.

**Two restrictions.** A program that calls only new, push and pop sees a [stack](/stack/), because (T1), (T2) and (T5) are the stack laws. A program that calls only new, enqueue and pop sees a [queue](/queue/), because (T1), (T3) and (T5) are the queue laws with dequeue renamed to pop. So a steque implementation gives both types at once.

**Canonical form.** Each steque built from $\text{new}()$ by valid calls equals $\text{enqueue}(\cdots\text{enqueue}(\text{new}(), y_1)\cdots, y_k)$ for exactly one sequence $\langle y_1, \dots, y_k \rangle$, which is its state. For existence, the first equation of (T4) moves a push inside each enqueue, and the second turns $\text{push}(\text{new}(), y)$ into $\text{enqueue}(\text{new}(), y)$; by induction on $k$ this gives $\text{push}(E(y_1, \dots, y_k), y) = E(y, y_1, \dots, y_k)$, where $E$ is the nested enqueue term. A pop of a term is handled by (T3) as on the [queue](/queue/) page. Uniqueness follows from (T5) and (T3) by the same induction on $k$ as for the queue: equal terms have the same size, the same popped item and equal rests.

**Permutations.** Feed the items $1, 2, \dots, n$ in order, each by a push or by an enqueue, mixed with pops, and write down the popped items. A stack can make $\frac{1}{n+1}\binom{2n}{n}$ outputs and a queue only one. A steque can make more than a stack: for $n = 1$ to $7$ the counts are 1, 2, 6, 22, 90, 394 and 1806, the large Schröder numbers. For $n = 4$ the two outputs it cannot make are $4\,1\,3\,2$ and $4\,2\,3\,1$. Knuth studies these permutations of output-restricted deques in the exercises of Section 2.2.1.

## Implementations

| implementation | push | enqueue | pop and top | space for $n$ items |
|---|---|---|---|---|
| [singly linked list](/singly-linked-list/) with head and tail, top at the head | $\Theta(1)$ worst case | $\Theta(1)$ worst case | $\Theta(1)$ worst case | $n$ nodes |
| [circular buffer](/circular-buffer/) with a fixed capacity $N$ | $\Theta(1)$ worst case | $\Theta(1)$ worst case | $\Theta(1)$ worst case | $N$ cells, so $n \le N$ |
| circular buffer in a [dynamic array](/dynamic-array/) | $\Theta(1)$ amortized | $\Theta(1)$ amortized | $\Theta(1)$ amortized | $\Theta(n)$ |
| any [deque](/deque/) | as its push front | as its push back | as its pop front | as the deque |

The linked list is the natural fit: push is PUSH-FRONT, enqueue is PUSH-BACK, and pop is POP-FRONT, the three operations that a singly linked list does in $O(1)$ time. The one operation that a singly linked list cannot do fast, the removal at the tail, is exactly the one that a steque leaves out. In the circular buffer, the top index $h$ moves back by one, modulo the capacity, on a push.

## References
