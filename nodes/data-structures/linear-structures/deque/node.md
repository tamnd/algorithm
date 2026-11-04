---
tag: 49QBMA
kind: abstract-type
slug: deque
name: Deque
aliases:
- double-ended queue
area: data-structures/linear-structures
level: intro
summary: Sequence supporting insertion and removal at both ends.
prereqs: [queue, stack]
see_also: [circular-buffer, doubly-linked-list, steque, catenable-deque, monotonic-deque, real-time-queue, min-queue, list]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.1 (Stacks, queues, and deques), the definition of a deque and of the input-restricted and output-restricted deques, and exercises 2.2.1-6 to 2.2.1-13 on the permutations they produce
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3, exercise 1.3.33 (Deque API with pushLeft, pushRight, popLeft and popRight)
  - paper: "Chris Okasaki, Purely Functional Data Structures, Cambridge University Press (1998)"
    locator: Section 5.2 (deques with amortized bounds) and Section 8.4 (real-time deques)
---

A deque, or double-ended queue, is the abstract type of a sequence that a program changes only at its two ends: it can insert and delete at the front and at the back, and read the item at either end. It contains both the [stack](/stack/) (one end only) and the [queue](/queue/) (insert at one end, delete at the other) as special cases. All of its operations can be done in $O(1)$ worst-case time, with a [doubly linked list](/doubly-linked-list/) or a [circular buffer](/circular-buffer/), and also in purely functional form. Deques are the core of the [monotonic deque](/monotonic-deque/) for sliding-window extremes, of 0-1 breadth-first search, and of work-stealing schedulers.

## In plain words

A deque is a line of items that is open at both ends. You can add an item at the front or at the back, and you can take an item from the front or from the back. You cannot reach into the middle.

If you only ever use one end, it behaves like a pile of plates, where the last plate put down is the first one taken. If you add at the back and take from the front, it behaves like a line at a shop. The deque lets one program do both, for example adding urgent work at the front and normal work at the back.

## Operations

The state of a deque over a set $T$ is a finite sequence $D = \langle x_0, \ldots, x_{n-1} \rangle$, with $x_0$ the front and $x_{n-1}$ the back.

| operation | signature | result |
|---|---|---|
| new | $() \to D$ | $\langle\rangle$ |
| is_empty | $(D) \to \text{bool}$ | $n = 0$ |
| size | $(D) \to \mathbb{N}$ | $n$ |
| push_front | $(D, x) \to D$ | $\langle x, x_0, \ldots, x_{n-1} \rangle$ |
| push_back | $(D, x) \to D$ | $\langle x_0, \ldots, x_{n-1}, x \rangle$ |
| pop_front | $(D) \to (T, D)$ | $x_0$ and $\langle x_1, \ldots, x_{n-1} \rangle$, for $n \ge 1$ |
| pop_back | $(D) \to (T, D)$ | $x_{n-1}$ and $\langle x_0, \ldots, x_{n-2} \rangle$, for $n \ge 1$ |
| front, back | $(D) \to T$ | $x_0$, $x_{n-1}$, for $n \ge 1$ |

Pop and peek on an empty deque are errors. Sedgewick and Wayne name the ends *left* and *right* (pushLeft, popRight and so on). C++ and Python name them `push_front` or `appendleft` and `push_back` or `append`.

## Laws

For each deque $D$ and each item $x$:

$$\begin{aligned}
&(\text{D1})\quad \text{pop\_front}(\text{push\_front}(D, x)) = (x, D), \qquad \text{pop\_back}(\text{push\_back}(D, x)) = (x, D),\\
&(\text{D2})\quad \text{push\_front}(\text{push\_back}(D, y), x) = \text{push\_back}(\text{push\_front}(D, x), y),\\
&(\text{D3})\quad \text{pop\_back}(\text{push\_front}(\text{new}(), x)) = (x, \text{new}()), \qquad \text{pop\_front}(\text{push\_back}(\text{new}(), x)) = (x, \text{new}()),\\
&(\text{D4})\quad \text{if } D \ne \text{new}() \text{ and } \text{pop\_back}(D) = (y, D'), \text{ then } \text{pop\_back}(\text{push\_front}(D, x)) = (y, \text{push\_front}(D', x)),\\
&(\text{D5})\quad \text{if } D \ne \text{new}() \text{ and } \text{pop\_front}(D) = (y, D'), \text{ then } \text{pop\_front}(\text{push\_back}(D, x)) = (y, \text{push\_back}(D', x)),\\
&(\text{D6})\quad \text{size}(\text{new}()) = 0, \qquad \text{size}(\text{push\_front}(D, x)) = \text{size}(\text{push\_back}(D, x)) = \text{size}(D) + 1.
\end{aligned}$$

Law (D1) gives the stack behaviour at each end. Laws (D3) to (D5) say that an item pushed at one end comes out at the other end only after every older item on that side, which is the queue behaviour. Law (D2) says that the two ends do not interfere.

**The laws fix every pop.** Let $D$ be any term built from new by pushes. Then the laws compute $\text{pop\_front}(D)$ and $\text{pop\_back}(D)$ whenever $D$ is not new.

*Proof.* By induction on the number of pushes in $D$. Take pop_front; pop_back is the mirror case. If the last push is $\text{push\_front}(D_0, x)$, law (D1) gives $(x, D_0)$. If it is $\text{push\_back}(D_0, x)$ with $D_0 = \text{new}()$, law (D3) gives $(x, \text{new}())$. Otherwise $D_0$ is not new and has fewer pushes, so by the induction hypothesis the laws give $\text{pop\_front}(D_0) = (y, D')$, and law (D5) gives $(y, \text{push\_back}(D', x))$. $\square$

**Restricted deques.** Knuth defines two restricted forms. An *input-restricted* deque allows push at one end only, and an *output-restricted* deque allows pop at one end only. A [steque](/steque/), with push at both ends and pop at one, is the output-restricted form. Knuth (Section 2.2.1, exercises) studies which permutations of $1, \ldots, n$ each form can produce when the items pass through it, and shows that some permutations that a deque produces cannot be produced by either restricted form.

## Implementations

| implementation | push and pop at each end | front, back | get at $i$ | space |
|---|---|---|---|---|
| [doubly linked list](/doubly-linked-list/) | $O(1)$ worst case | $O(1)$ | $\Theta(\min(i, n - i) + 1)$ | $n + 1$ nodes of 3 fields |
| [circular buffer](/circular-buffer/), fixed capacity $N$ | $O(1)$ worst case, fails when full | $O(1)$ | $O(1)$ | $N$ cells |
| [circular buffer](/circular-buffer/), growable | $O(1)$ amortized | $O(1)$ | $O(1)$ | $\Theta(n)$ |
| array of fixed blocks with a map (C++ `std::deque`) | $O(1)$ amortized | $O(1)$ | $O(1)$ | $\Theta(n)$ |
| doubly linked list of blocks (CPython `collections.deque`) | $O(1)$ worst case | $O(1)$ | $\Theta(\min(i, n - i)/B + 1)$ | $\Theta(n)$ |
| two stacks, split in half when one runs out | $O(1)$ amortized | $O(1)$ amortized | | $\Theta(n)$ |
| [real-time](/real-time-queue/) functional deque | $O(1)$ worst case, persistent | $O(1)$ | | $\Theta(n)$ |
| [catenable deque](/catenable-deque/) | $O(1)$, and concatenation in $O(1)$ | $O(1)$ | | $\Theta(n)$ |

The two-stack form extends the [two-stack queue](/two-stacks-queue/): when the stack for one end is empty, move half of the other stack across, which gives $O(1)$ amortized time per operation. Okasaki's book gives this form in a purely functional setting and a real-time form with worst-case bounds.

A singly linked list with a tail pointer is not enough: it gives push at both ends and pop at the front, the steque, but pop at the back costs $\Theta(n)$ because the node before the tail must be found.

## References
