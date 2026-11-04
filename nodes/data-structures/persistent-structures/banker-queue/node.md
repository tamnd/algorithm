---
tag: WBJ0ZE
kind: data-structure
slug: banker-queue
name: Banker's queue
aliases:
- Okasaki banker's queue
- batched queue
- two-list queue
area: data-structures/persistent-structures
level: core
summary: A persistent queue of a lazy front stream and a rear list, rebuilt lazily when the rear outgrows the front, with O(1) amortized operations that stay valid under persistent reuse.
implements: [queue]
model: pointer-machine
complexity:
  vars: {n: the number of items in the queue}
  time: {worst: Θ(n), amortized: O(1)}
  space: {extra: Θ(n)}
history:
  year: 1996
  people: [Chris Okasaki]
  note: The banker's queue and the banker's method of analysis are in Okasaki's 1996 thesis (Section 3.4) and his 1998 book. The two-list queue it improves is older, from Hood and Melville (1981) and from Burton (1982).
prereqs: [queue, persistent-stack, amortized-cost]
see_also: [real-time-queue, two-stacks-queue, debit-analysis, lazy-rebuilding, purely-functional-data-structure, potential-method, deque, persistent-data-structure]
sources:
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Section 5.2, Queues (the batched queue), Section 5.6, The Bad News (its failure under persistence), Section 6.3, The Banker's Method, with 6.3.2, Example, Queues (the banker's queue and its debit invariant)
  - url: https://www.cs.cmu.edu/~rwh/students/okasaki.pdf
    title: Chris Okasaki, Purely Functional Data Structures, PhD thesis, Carnegie Mellon University, CMU-CS-96-177, 1996
    locator: Chapter 3, Amortization and Persistence via Lazy Evaluation, Section 3.4, The Banker's Method, with 3.4.1 (its justification) and 3.4.2, Example, Queues (Theorem 3.1, the debit invariant)
  - paper: doi:10.1016/0020-0190(81)90030-2
    title: Robert Hood and Robert Melville, Real-time queue operations in pure LISP, Information Processing Letters 13(2), 1981
    locator: pages 50 to 54 (the two-list queue and its real-time version)
  - paper: doi:10.1016/0020-0190(82)90015-1
    title: F. Warren Burton, An efficient functional implementation of FIFO queues, Information Processing Letters 14(5), 1982
    locator: pages 205 to 206
---

The banker's queue is a [persistent](/persistent-data-structure/) [queue](/queue/) that keeps a lazy front stream $F$ and a rear list $R$, with the invariant $|R| \le |F|$. An insertion conses onto $R$, and a removal takes the first cell of $F$. When $R$ would become longer than $F$, the queue is rebuilt as $F$ followed by the reverse of $R$, but the rebuild is a suspension that runs only when its cells are needed. Each operation takes $O(1)$ amortized time, and because suspensions are memoized, this bound holds even when old versions are used again. Chris Okasaki gave it as the first example of his [debit analysis](/debit-analysis/).

## In plain words

A queue made of two piles is an old trick. New items go on top of a back pile. Items leave from the top of a front pile. When the front pile is empty, you turn the back pile over and it becomes the new front. Each item is turned over once, so the work is small on average.

The trick fails if you keep old states. Take a state where the front is empty and the back is large, and remove an item from it again and again: each time you pay for the large turn-over.

The banker's queue starts the turn-over earlier, as soon as the back pile gets longer than the front. It also delays the work: it writes a plan and does the work only when someone reaches those items. The plan is shared by all copies, so the work is done at most once.

## The abstract type

The queue holds a sequence $\langle x_1, \ldots, x_n \rangle$, with $x_1$ at the front. The operations are those of the [queue](/queue/) type, in persistent form: each update returns a new queue and leaves its argument unchanged.

- `empty()` returns $\langle \rangle$.
- `snoc(Q, x)` returns $\langle x_1, \ldots, x_n, x \rangle$.
- `head(Q)` returns $x_1$, and `tail(Q)` returns $\langle x_2, \ldots, x_n \rangle$. Both are errors on the empty queue.

## Representation

A queue is a tuple $(\ell_f, F, \ell_r, R)$:

- $F$ is a *stream*: a lazy list whose cells are suspensions. A suspension is a delayed computation that runs at its first force and stores its result, so a second force costs $O(1)$. $F$ holds the front part of the queue in queue order.
- $\ell_f$ is the length of $F$.
- $R$ is an ordinary immutable list, a [persistent stack](/persistent-stack/), that holds the rear part of the queue, newest item first.
- $\ell_r$ is the length of $R$.

The queue represented is $F$ followed by the reverse of $R$. The **invariant** is

$$ \ell_r \le \ell_f. $$

So $F$ is empty only when the whole queue is empty, and `head` never has to look at $R$.

## Operations

All operations are in one block. ++ is lazy concatenation of streams: it produces each cell of its result only when that cell is forced. REVERSE is a monolithic suspension: at its first force it reverses the whole list.

```pseudo id=main
EMPTY()
L1  return (0, ⟨⟩, 0, ⟨⟩)

SNOC(Q, x)
L2  (ℓf, F, ℓr, R) ← Q
L3  return CHECK(ℓf, F, ℓr + 1, cons(x, R))

HEAD(Q)
L4  if ℓf = 0 then error "empty queue"
L5  return the item of the first cell of F                     ▷ forces that cell

TAIL(Q)
L6  if ℓf = 0 then error "empty queue"
L7  return CHECK(ℓf − 1, the rest of F after its first cell, ℓr, R)

CHECK(ℓf, F, ℓr, R)
L8  if ℓr ≤ ℓf then return (ℓf, F, ℓr, R)
L9  return (ℓf + ℓr, F ++ $REVERSE(R), 0, ⟨⟩)                  ▷ a rotation; nothing is evaluated yet
```

**Snoc.** Line L3 conses the new item onto $R$ in $O(1)$ time and calls CHECK.

**Head and tail.** Line L5 forces the first cell of $F$. Line L7 forces the same cell to get the rest of the stream, then calls CHECK. By the invariant, $\ell_f = 0$ means that the queue is empty.

**Check and rotation.** CHECK returns the tuple as it is when the invariant holds. Otherwise $\ell_r = \ell_f + 1$, since each update changes $\ell_r - \ell_f$ by exactly 1, and line L9 makes a *rotation*: the new front is the suspension $F$ ++ REVERSE$(R)$, of length $2\ell_f + 1$, and the new rear is empty. Line L9 builds two suspensions and does no other work. The first $\ell_f$ cells of the new stream cost $O(1)$ each when they are forced. The cell at index $\ell_f$ forces REVERSE$(R)$, which costs $\Theta(\ell_r)$, and the cells after it are already built by that reversal.

**Why the rotation comes early.** In the [two-stack queue](/two-stacks-queue/) the reversal happens when $F$ is empty and is paid at once. Here the reversal is created when $|F| = m$ and $|R| = m + 1$, and it is forced only after the $m$ cells of the old front have been removed. Those $m$ removals pay for it in advance. Every version that reaches the forced cell has made those $m$ removals in its own history, and the memoized result is shared by all of them.

## Example

Start with the empty queue and do snoc 1, 2, 3, 4, 5, then tail twice. The table shows $\ell_f$, $\ell_r$, the front in queue order and the rear newest first. "rot" marks a rotation, and a front written with ++ is not evaluated yet.

| step | operation | $\ell_f$ | $\ell_r$ | $F$ | $R$ |
|---|---|---|---|---|---|
| 0 | empty | 0 | 0 | ⟨⟩ | ⟨⟩ |
| 1 | snoc 1, rot | 1 | 0 | ⟨⟩ ++ rev⟨1⟩ | ⟨⟩ |
| 2 | snoc 2 | 1 | 1 | as step 1 | ⟨2⟩ |
| 3 | snoc 3, rot | 3 | 0 | (⟨⟩ ++ rev⟨1⟩) ++ rev⟨3, 2⟩ | ⟨⟩ |
| 4 | snoc 4 | 3 | 1 | as step 3 | ⟨4⟩ |
| 5 | snoc 5 | 3 | 2 | as step 3 | ⟨5, 4⟩ |
| 6 | tail (removes 1) | 2 | 2 | the stream after 1, that is ⟨2, 3⟩ | ⟨5, 4⟩ |
| 7 | tail (removes 2), rot | 3 | 0 | ⟨3⟩ ++ rev⟨5, 4⟩ | ⟨⟩ |

At step 6, the tail forces the first cell of the front of step 3. That forces the first cell of the inner stream, which forces rev⟨1⟩, one step of work, and yields 1. At step 7 the queue is $\langle 3, 4, 5 \rangle$. The version of step 5 is still $\langle 1, 2, 3, 4, 5 \rangle$, and a second tail of it reuses the cell that step 6 already forced, at a cost of $O(1)$.

## Correctness

Let $\text{seq}(Q) = F \cdot \text{reverse}(R)$ be the sequence that $Q$ represents. Each operation keeps $\ell_r \le \ell_f$ and the lengths exact, and acts on $\text{seq}$ as the queue type says: SNOC appends $x$ at the end, because $\text{reverse}(\text{cons}(x, R)) = \text{reverse}(R) \cdot \langle x \rangle$; TAIL drops the first item of $F$, which is the first item of $\text{seq}$ because $F$ is non-empty when the queue is; and a rotation does not change $\text{seq}$, because $F$ ++ REVERSE$(R)$ denotes $F \cdot \text{reverse}(R)$. No operation writes into an existing cell, list or tuple, so every old version keeps its sequence: the structure is fully persistent. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | worst case | amortized, also under persistent reuse |
|---|---|---|
| empty, snoc | $O(1)$ | $O(1)$ |
| head, tail | $\Theta(n)$ | $O(1)$ |
| space | $\Theta(n)$ for one version | $O(1)$ new cells for each operation |

**Worst case.** A head or a tail that forces the cell where a rotation reaches its REVERSE pays for the whole reversal, $\Theta(n)$ time. In step 7 of the example, a later tail of the queue $\langle 3, 4, 5 \rangle$ forces rev⟨5, 4⟩. The [real-time queue](/real-time-queue/) removes this worst case by forcing one cell of the stream at each operation.

**Amortized cost.** The [debit analysis](/debit-analysis/) gives each suspension debits equal to its own cost, and allows a suspension to be forced only after all its debits are paid. Let $D(i)$ be the total of the debits on the first $i + 1$ cells of $F$. The proof keeps the debit invariant

$$ D(i) \le \min(2i,\ \ell_f - \ell_r) \quad \text{for } 0 \le i < \ell_f. $$

So $D(0) = 0$, and the first cell, the only cell that head and tail force, is always paid for. A snoc without a rotation lowers $\ell_f - \ell_r$ by 1 and pays 1 debit. A tail without a rotation shifts the cells down by one place and pays 2 debits. A rotation happens when $\ell_f - \ell_r$ was 0 before the operation, so the old front has no debits left. The new stream gets 1 debit on each of its first $m$ cells and $m + 2$ debits on cell $m$, and paying 2 debits restores the invariant. So each operation does $O(1)$ work of its own and pays at most 2 debits, and the total cost of any sequence of $k$ operations, on any versions, is $O(k)$. Okasaki proves the same bound with a slightly different count of debits. The full argument, with the reason that it holds under persistence, is in [the complexity proof](proofs/complexity.md).

**Space.** A version has $\ell_f + \ell_r = n$ items, so $\Theta(n)$ cells once its front is fully forced. Each operation makes $O(1)$ new cells and suspensions; the cells of a rotation are made later, one at each force.

## Variants

- **The batched queue.** Okasaki's Section 5.2 queue has two plain lists and the invariant "$F$ is empty only if $R$ is empty". When a tail empties $F$, it reverses $R$ at once. Its operations are $O(1)$ amortized in single-threaded use, but not under persistence: repeat the tail of a version with $|F| = 1$ and $|R| = n - 1$, and each tail costs $\Theta(n)$. This is the queue that the aliases "batched queue" and "two-list queue" name; the banker's queue is its repair. The same structure with two mutable stacks is the [two-stack queue](/two-stacks-queue/).
- **The physicist's queue.** Okasaki's Section 6.4.2 keeps a prefix of $F$ as an ordinary list and analyzes the queue with a potential function instead of debits. It also has $O(1)$ amortized bounds under persistence.
- **The real-time queue.** The [real-time queue](/real-time-queue/) of Okasaki's Section 7.2 forces one cell of the rotation at each operation, so that each operation takes $O(1)$ time in the worst case. Hood and Melville (1981) had earlier given a real-time queue in pure Lisp with a more complex incremental reversal.
- **Banker's deque.** The same idea with two streams and the invariant $|F| \le c|R| + 1$ and $|R| \le c|F| + 1$ for a constant $c > 1$ gives a deque with $O(1)$ amortized operations at both ends (Okasaki, Section 8.4.2). See [lazy rebuilding](/lazy-rebuilding/).

## When to use it

Use the banker's queue in a functional language with lazy evaluation, when a queue may be shared and old versions may be used again, as in a search that branches. If the queue is used in single-threaded style, the batched queue is simpler and faster. If each operation must be fast, for example in an interactive or real-time program, use the [real-time queue](/real-time-queue/). In an imperative program without persistence, a circular buffer or a [two-stack queue](/two-stacks-queue/) is faster than any of these.

## Pitfalls

- **A strict rotation.** If line L9 evaluates $F$ ++ REVERSE$(R)$ at once, the queue is the batched queue with a different trigger, and the persistent bound fails: snoc on a version with $\ell_r = \ell_f$ costs $\Theta(n)$ each time it is repeated.
- **A suspension without memoization.** If a forced suspension does not store its result, each version that reaches the reversal pays for it again. Lazy evaluation is call by need, not call by name.
- **An incremental reverse.** Reverse cannot produce its first cell before it has seen the whole list, so it is monolithic. The analysis charges its full cost to one cell; a version of REVERSE that pretends to be incremental hides that cost.
- **Testing the invariant before the update.** Line L8 must test the lengths after the snoc or the tail. Testing before lets $\ell_r$ reach $\ell_f + 1$ and leaves the queue with an empty $F$ and a non-empty $R$, so that HEAD fails on a queue that is not empty.
- **Counting length by walking the stream.** Computing $\ell_f$ by traversal forces every cell. Keep the lengths as fields.

## Implementations

The Python version has a class `Susp` for memoized suspensions, the lazy `append` and the monolithic `reverse`, and a class `BankerQueue` whose methods return new queues. The tests check the trace of the example and run long random sequences of operations on random old versions against Python lists.

## History

The two-list representation of a functional queue appears in Hood and Melville (1981), who also made it real-time, and in Burton (1982). Okasaki observed that its amortized bound fails under persistence and repaired it with lazy evaluation and memoization; the banker's queue and the banker's method of analysis appear in Section 3.4 of his 1996 thesis and in Section 6.3 of his 1998 book.

## References
