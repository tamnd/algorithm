---
tag: X9W66J
kind: data-structure
slug: real-time-queue
name: Real-time queue
aliases:
- Okasaki real-time queue
- Hood-Melville queue
area: data-structures/persistent-structures
level: advanced
summary: A persistent queue with worst-case O(1) operations obtained by incrementally reversing the front list.
implements: [queue]
model: pointer-machine
complexity:
  vars: {n: the number of items in the version, u: the number of operations done}
  time: {push: Θ(1), pop: Θ(1), front: Θ(1), is_empty: Θ(1), size: Θ(1)}
  space: {total: Θ(u)}
history:
  year: 1995
  people: [Chris Okasaki, Robert Hood, Robert Melville]
  note: Hood and Melville gave a purely functional queue with O(1) worst-case operations in 1981 by global rebuilding; Okasaki gave a simpler form in 1995 using lazy evaluation and a schedule.
prereqs: [queue, banker-queue, persistent-stack, memoization]
see_also: [two-stacks-queue, purely-functional-data-structure, lazy-rebuilding, global-rebuilding, debit-analysis, deque, catenable-deque, skew-binary-random-access-list]
sources:
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Section 7.2, Real-Time Queues (rotate, exec and the schedule), and Section 8.2.1 (the Hood-Melville real-time queue by global rebuilding)
  - paper: Chris Okasaki, Simple and efficient purely functional queues and deques, Journal of Functional Programming 5(4), 1995
    locator: the real-time queue with a schedule of suspensions
  - paper: Robert Hood and Robert Melville, Real-time queue operations in pure LISP, Information Processing Letters 13(2), 1981
    locator: the queue with O(1) worst-case operations by incremental reversal
---

A real-time queue is a persistent first-in first-out [queue](/queue/) in which push, pop and front take $O(1)$ time in the worst case, on every version, including versions that are used many times. It keeps a lazy front stream $f$, a rear list $r$ and a *schedule* $s$, which is the part of $f$ not yet evaluated. When $r$ becomes longer than $f$, it starts the lazy rotation $f \mathbin{+\!\!+} \text{reverse}(r)$, and each later operation forces one more step of it through $s$, so the rotation is done before it is needed and no operation pays for more than one step. The form here is Okasaki's of 1995; Hood and Melville reached the same bounds in 1981 by a more complex [global rebuilding](/global-rebuilding/).

## In plain words

A simple queue uses two stacks: items come in on the back stack and leave from the front stack, and when the front stack runs out, the whole back stack is turned over onto it. Turning over a long stack takes a long time, once in a while. With persistence that is worse: you can keep an old queue that is about to turn over, and use it again and again, and each time it pays the full price.

The real-time queue turns the back stack over a little at a time, in advance. As soon as the back stack is longer than the front, it plans the turn-over, and then every push and every pop does one more step of it. The plan is shared by all later versions, and each step is done once and remembered, so no operation is ever slow.

## The abstract type

The structure implements an immutable [queue](/queue/): `empty`, `is_empty(q)`, `size(q)`, `push(q, x)` (add $x$ at the back), `front(q)` and `pop(q)`, which returns the front item and the rest of the queue. Each update returns a new queue, and every version stays valid, so the structure is fully persistent.

## Representation

A *stream* is a lazy list: a suspension that, when forced, gives either the empty stream or a cell with a head and a tail stream. A forced suspension stores its result ([memoization](/memoization/)), so forcing it again costs $O(1)$ and gives the same cell. A queue is a triple $(f, r, s)$ where $f$ is a stream, $r$ is an ordinary list (a [persistent stack](/persistent-stack/)), and $s$ is a stream. The items of the queue, front to back, are $f \mathbin{+\!\!+} \text{reverse}(r)$.

**Invariant.** (I1) $|s| = |f| - |r|$, so $|r| \le |f|$. (I2) $s$ is a suffix of $f$, and every cell of $f$ before $s$ has been forced. (I3) No cell or forced value changes after it is made; a suspension changes only from unforced to forced, and then holds the value its code defines.

By (I1), when $|s| = 0$, all of $f$ is forced, and $|r| = |f|$; the next push or pop would make $|r| = |f| + 1$, and it starts a rotation.

## Operations

```pseudo id=main
ROTATE(f, r, a)                              ▷ lazy f ++ reverse(r) ++ a; needs |r| = |f| + 1
L1  return a suspension of: if FORCE(f) is empty then CONS(r.head, a) else CONS(head of f, ROTATE(tail of f, r.next, CONS(r.head, a)))

EXEC(f, r, s)                                ▷ do one step of the schedule
L2  if FORCE(s) is a cell then return (f, r, tail of s)
L3  f′ ← ROTATE(f, r, empty); return (f′, nil, f′)

PUSH(q, x)
L4  return EXEC(q.f, CONS(x, q.r), q.s)

FRONT(q)
L5  if FORCE(q.f) is empty then error "empty"; return head of q.f

POP(q)
L6  if FORCE(q.f) is empty then error "empty"
L7  return (head of q.f, EXEC(tail of q.f, q.r, q.s))
```

ROTATE does no work when it is called: it only makes a suspension. When the suspension is forced, it forces the first cell of $f$, which by (I2) is already forced and costs $O(1)$, and makes one cell whose tail is a new suspension for the next step. So each forced step of a rotation costs $O(1)$. The accumulator $a$ collects $r$ in reverse, one item per step.

**Why the rotation is always ready.** A rotation starts when $|r| = |f| + 1$, with $|f| = m$, and makes a stream of $2m + 1$ items with $s = f'$. Each following push or pop forces one cell of $s$, and each such cell is the next step of the rotation. The front of $f'$ is consumed by pops at most one cell per operation, and the schedule is forced at the same rate, so the cell that a pop needs is always forced. The rotation is complete after $2m + 1$ operations, while the rear can grow by at most one per operation, and the next rotation starts only when $|r| = |f| + 1$ again. By then $s$ is empty, so all of $f$ is forced, as ROTATE needs.

**Size.** Store $|f|$ and $|r|$ as integers with the triple; then `size` and `is_empty` take $O(1)$ without forcing anything.

## Example

Start from the empty queue $q_0 = (\langle\rangle, \text{nil}, \langle\rangle)$ and write the state as $(|f|, |r|, |s|)$.

| step | operation | what happens | state |
|---|---|---|---|
| 1 | $q_1 = \text{push}(q_0, 1)$ | $s$ is empty, so rotate $f = \langle\rangle$, $r = [1]$ | $(1, 0, 1)$ |
| 2 | $q_2 = \text{push}(q_1, 2)$ | force one cell of $s$; it gives 1 | $(1, 1, 0)$ |
| 3 | $q_3 = \text{push}(q_2, 3)$ | $s$ is empty, so rotate $f = \langle 1 \rangle$, $r = [3, 2]$ | $(3, 0, 3)$ |
| 4 | $q_4 = \text{push}(q_3, 4)$ | force one step of the rotation: cell 1 | $(3, 1, 2)$ |
| 5 | $q_5 = \text{push}(q_4, 5)$ | force the next step: cell 2 | $(3, 2, 1)$ |
| 6 | $(1, q_6) = \text{pop}(q_5)$ | return 1; force the last step: cell 3 | $(2, 2, 0)$ |
| 7 | $q_7 = \text{push}(q_6, 6)$ | $s$ is empty, so rotate $f = \langle 2, 3 \rangle$, $r = [6, 5, 4]$ | $(5, 0, 5)$ |

$q_7$ holds $2, 3, 4, 5, 6$, while $q_5$ still holds $1, 2, 3, 4, 5$ and $q_2$ still holds $1, 2$. If a program now pops $q_5$ a thousand times, each pop finds the cells of the shared front already forced, and does one step of work, not a reversal of the rear.

## Correctness

The items of a queue are $\text{items}(q) = f \mathbin{+\!\!+} \text{reverse}(r)$, and laziness does not change values: a stream denotes the same sequence whether it is forced or not. PUSH keeps $f$ and puts $x$ at the head of $r$, so $x$ is the last item. POP removes the head of $f$, which by (I1) is non-empty when the queue is not empty, because $|f| \ge |r|$ and $|f| + |r| > 0$. EXEC either drops one cell of $s$, which keeps the items, or replaces $(f, r)$ by $(f \mathbin{+\!\!+} \text{reverse}(r), \text{nil})$, which keeps them too; ROTATE$(f, r, a)$ denotes $f \mathbin{+\!\!+} \text{reverse}(r) \mathbin{+\!\!+} a$ by induction on $|f|$. Counting shows that (I1) holds after each operation, and (I2) holds because EXEC forces the head of $s$ before dropping it. By (I3) old versions keep their items. The full proof is in the proofs folder.

## Complexity

| operation | time, worst case | new cells |
|---|---|---|
| push | $O(1)$ | $O(1)$ |
| pop | $O(1)$ | $O(1)$ |
| front, is_empty, size | $O(1)$ | none |

**Time.** Each operation forces at most two suspensions: the head of $f$ (already forced by (I2), so $O(1)$) and the head of $s$, which is one step of a rotation. One step of ROTATE forces the head of its own $f$, which is forced by (I2) for the rotation's input, and makes $O(1)$ cells. So no operation does more than a constant amount of work, in the worst case, on any version. This holds under persistence because a suspension shared by many versions is forced once: the second and later forces return the stored cell.

**Space.** Each operation makes $O(1)$ new cells and suspensions, so after $u$ operations the total is $O(u)$. The live space of a version of $n$ items is $O(n)$, because $|f| + |r| = n$ and $s$ is part of $f$.

**Model.** The bounds are on a [pointer machine](/pointer-machine/) with memoized suspensions: forcing writes the result into the suspension once. This is the only write to an existing cell, and it does not change the value that the suspension denotes.

## Variants

- **Banker's queue.** The [banker's queue](/banker-queue/) uses the same lazy rotation without a schedule, and has $O(1)$ amortized bounds that hold under persistence, by the [debit method](/debit-analysis/). The real-time queue adds the schedule to make them worst case.
- **Hood-Melville queue.** Hood and Melville do the reversal of $r$ and the reversal back onto $f$ step by step, as an explicit state machine with a fixed number of steps per operation, without lazy evaluation. This is [global rebuilding](/global-rebuilding/); it works in strict languages but has more cases.
- **Deques.** The same technique with two streams and a schedule for each gives real-time double-ended queues ([deque](/deque/)), with rotations started when one side is more than $c$ times longer than the other for a constant $c \ge 2$.
- **Catenable queues.** [Catenable deques](/catenable-deque/) add concatenation in $O(1)$; Kaplan and Tarjan gave real-time catenable deques, and Okasaki gave simpler amortized ones.
- **Strict two-stacks queue.** The [two-stacks queue](/two-stacks-queue/) is simpler and has $O(1)$ amortized bounds, but only when each version is used at most once.

## When to use it

Use a real-time queue when a purely functional program needs a queue with a hard bound on each operation, for example in interactive or real-time code, or when old versions of a queue are reused, as in backtracking search over queue states. If old versions are never reused and only total time matters, the two-stacks queue or the banker's queue is simpler and faster in practice. In a strict language without memoized laziness, use the Hood-Melville form or a mutable ring buffer.

## Pitfalls

- **No memoization.** If a suspension is evaluated each time it is forced, a shared rotation step is paid by every version that forces it, and the bounds fail under persistence. The suspension must store its result.
- **Forcing the schedule wrong.** EXEC must force the head of $s$ before it drops it (L2). Dropping $s$ without forcing leaves cells of $f$ unevaluated, and a later step of a rotation then forces a long chain at once.
- **Building the rotation strictly.** A strict ROTATE does the whole reversal in one call, which is the slow step the structure is designed to avoid.
- **Deep chains of thunks in a strict host.** In a language like Python, a stream built by nested closures is fine if the schedule forces it one cell at a time, as here. Forcing a long unforced stream at once can overflow the call stack.
- **The invariant needs exact counts.** The rotation must start exactly when $|r| = |f| + 1$; then $|s| = 0$ and $f$ is fully forced. Starting it later breaks the $O(1)$ bound.

## Implementations

## History

Robert Hood and Robert Melville gave a queue for pure Lisp with $O(1)$ worst-case operations in 1981, by doing the two reversals incrementally. Chris Okasaki showed in 1995 that lazy evaluation with memoization and an explicit schedule gives the same bound with much simpler code, and his book of 1998 presents the real-time queue together with the banker's and physicist's methods and the general technique of scheduling. Kaplan and Tarjan extended worst-case purely functional sequences to catenable deques in 1999.

## References
