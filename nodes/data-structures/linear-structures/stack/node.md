---
tag: AEN74Z
kind: abstract-type
slug: stack
name: Stack
aliases:
- LIFO
area: data-structures/linear-structures
level: intro
summary: Collection with push and pop in last-in first-out order.
prereqs: [asymptotic-notation]
see_also: [queue, deque, steque, min-stack, singly-linked-list, dynamic-array, monotonic-stack, postfix-evaluation]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.1 (Simple array-based data structures), the part on stacks and queues
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.2.1 (Stacks, queues, and deques), with its exercises on the permutations that a stack can make
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3 (Bags, Queues, and Stacks), the pushdown stack API, the array and linked-list implementations
  - url: https://opendatastructures.org/
    title: Pat Morin, Open Data Structures
    locator: Section 2.1 (ArrayStack) and Section 3.1 (SLList)
  - paper: John V. Guttag, Abstract data types and the development of data structures, Communications of the ACM 20(6) (1977)
    locator: the algebraic axioms of the type Stack
---

A stack is an abstract data type that holds a finite sequence of items and changes it only at one end, the *top*: `push` adds an item at the top, and `pop` removes the item at the top and returns it. So the item that comes out is always the one that went in last, which is the *last in, first out* (LIFO) rule. A [dynamic array](/dynamic-array/) or a [singly linked list](/singly-linked-list/) gives each operation in $O(1)$ time. Stacks hold the return addresses of procedure calls, the pending vertices of [depth-first search](/depth-first-search/), and the operands of [postfix evaluation](/postfix-evaluation/).

## In plain words

Think of a pile of plates. You put a clean plate on top of the pile. When you need a plate, you take the one on top. You never pull a plate out of the middle. So the plate you take is always the one that was put down most recently.

A stack in a program works the same way. It has two main actions: put an item on top, and take the top item off. You can also look at the top item without taking it, and ask if the pile is empty. Because only the top is used, the computer does not search for anything, and each action takes the same short time, however many items the stack holds.

## Operations

A stack over a set $T$ of items is a value $S$. Its state is a finite sequence $\langle x_1, x_2, \dots, x_k \rangle$ of items of $T$, with $x_k$ at the top and $k \ge 0$.

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}() \to S$ | the empty stack $\langle \rangle$ |
| `push` | $\text{push}(S, x) \to S$ | $\langle x_1, \dots, x_k \rangle$ becomes $\langle x_1, \dots, x_k, x \rangle$ |
| `pop` | $\text{pop}(S) \to (x, S)$ | for $k \ge 1$: returns $x_k$, and the stack becomes $\langle x_1, \dots, x_{k-1} \rangle$ |
| `top` | $\text{top}(S) \to x$ | for $k \ge 1$: returns $x_k$ and does not change $S$ (also called `peek`) |
| `is_empty` | $\text{is\_empty}(S) \to \text{bool}$ | true when $k = 0$ |
| `size` | $\text{size}(S) \to \mathbb{N}$ | returns $k$ |

`pop` and `top` on the empty stack are errors, called *underflow*. An implementation with a fixed capacity $N$ also has *overflow*: a `push` when $k = N$. Some libraries let `pop` return only the item and change the stack in place; the pair in the table makes the change explicit.

### Example

Start with the empty stack. The top is on the right.

| step | operation | result | stack after |
|---|---|---|---|
| 1 | push 5 | | $\langle 5 \rangle$ |
| 2 | push 2 | | $\langle 5, 2 \rangle$ |
| 3 | push 8 | | $\langle 5, 2, 8 \rangle$ |
| 4 | pop | 8 | $\langle 5, 2 \rangle$ |
| 5 | top | 2 | $\langle 5, 2 \rangle$ |
| 6 | push 7 | | $\langle 5, 2, 7 \rangle$ |
| 7 | size | 3 | $\langle 5, 2, 7 \rangle$ |
| 8 | pop | 7 | $\langle 5, 2 \rangle$ |
| 9 | pop | 2 | $\langle 5 \rangle$ |
| 10 | pop | 5 | $\langle \rangle$ |
| 11 | is_empty | true | $\langle \rangle$ |

The items 5, 2, 7 were pushed in this order and still in the stack at step 8. Steps 8 to 10 pop them in the reverse order 7, 2, 5.

## Laws

Each implementation meets these equations, for each stack $S$ and each item $x$:

$$\begin{aligned}
&(\text{S1})\quad \text{is\_empty}(\text{new}()) = \text{true}, \qquad (\text{S2})\quad \text{is\_empty}(\text{push}(S, x)) = \text{false},\\
&(\text{S3})\quad \text{top}(\text{push}(S, x)) = x, \qquad (\text{S4})\quad \text{pop}(\text{push}(S, x)) = (x, S),\\
&(\text{S5})\quad \text{size}(\text{new}()) = 0, \qquad \text{size}(\text{push}(S, x)) = \text{size}(S) + 1.
\end{aligned}$$

The terms $\text{pop}(\text{new}())$ and $\text{top}(\text{new}())$ are not defined. These five laws are the algebraic specification of the type, in the style of Guttag (1977). Law (S4) is the LIFO rule in one line: a pop right after a push undoes the push.

**Canonical form.** Each stack that a program can build from $\text{new}()$ by valid calls of push and pop is equal to exactly one term $\text{push}(\cdots\text{push}(\text{push}(\text{new}(), y_1), y_2)\cdots, y_k)$ with $k \ge 0$.

*Proof.* Existence, by induction on the number of calls. The value $\text{new}()$ is the term with $k = 0$. If $S$ is the term for $\langle y_1, \dots, y_k \rangle$, then $\text{push}(S, x)$ is the term for $\langle y_1, \dots, y_k, x \rangle$. A valid pop needs $k \ge 1$ by (S1) and (S2), and then (S4) gives the stack part $\langle y_1, \dots, y_{k-1} \rangle$, which is a term of the same form. Uniqueness, by induction on $k$. If two such terms are equal, then (S5) gives them the same $k$. For $k = 0$ both are $\text{new}()$. For $k \ge 1$, law (S3) gives them the same last item, and (S4) gives equal inner terms, which have the same items by the induction hypothesis. $\square$

So the state of a stack is exactly the sequence $\langle y_1, \dots, y_k \rangle$, as the table of operations says, and two implementations that meet (S1) to (S5) give the same result for each sequence of operations.

**Order of removal.** If $x$ is pushed after $y$, and neither is popped in between, then $x$ is popped before $y$. This follows from the canonical form: $y$ is at a lower position than $x$, and pop removes only the last position.

**Stack permutations.** Push the items $1, 2, \dots, n$ in this order, with pops mixed in, and write down each popped item. The outputs that this can make are exactly the permutations $p_1 p_2 \dots p_n$ with no indices $i < j < k$ such that $p_j < p_k < p_i$, and there are $C_n = \frac{1}{n+1}\binom{2n}{n}$ of them, the Catalan numbers (Knuth, Section 2.2.1, exercises). For $n = 3$ the five outputs are all permutations except $3\,1\,2$; for $n = 4, 5, 6$ there are 14, 42 and 132.

## Implementations

| implementation | push | pop and top | space for $n$ items |
|---|---|---|---|
| [array](/array/) with a fixed capacity $N$ | $\Theta(1)$ worst case | $\Theta(1)$ worst case | $N$ cells, so $n \le N$ |
| [dynamic array](/dynamic-array/), doubled when full | $\Theta(1)$ amortized, $\Theta(n)$ worst case | $\Theta(1)$ amortized with shrinking at one quarter full | $\Theta(n)$ |
| [singly linked list](/singly-linked-list/), top at the head | $\Theta(1)$ worst case | $\Theta(1)$ worst case | $n$ nodes, one item and one [pointer](/pointer/) each |
| [stack from two queues](/stack-from-two-queues/) | $\Theta(1)$ or $\Theta(n)$, by the variant | $\Theta(n)$ or $\Theta(1)$ | $\Theta(n)$ |

The array form keeps the top index $t$: push writes $A[t] \leftarrow x$ and sets $t \leftarrow t + 1$, pop sets $t \leftarrow t - 1$ and returns $A[t]$. The linked form makes the new node the head. A [deque](/deque/) or a [steque](/steque/) also gives a stack, by use of one end only. A [min-stack](/min-stack/) adds a `min` operation in $O(1)$ time.

The amortized bound of the dynamic array needs a careful rule for shrinking: halve the array when it is one quarter full, not when it is half full. With halving at one half, a push and a pop that alternate at the boundary cost $\Theta(n)$ each (Sedgewick and Wayne, Section 1.3). See [dynamic array resizing](/dynamic-array-resizing/) for the analysis.

## References
