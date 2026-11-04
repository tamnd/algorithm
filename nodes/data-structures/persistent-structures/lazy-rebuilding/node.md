---
tag: FBFR1K
kind: technique
slug: lazy-rebuilding
name: Lazy rebuilding
aliases:
- Okasaki lazy rebuilding
- incremental rebuilding
area: data-structures/persistent-structures
level: advanced
summary: Spread the cost of a global rebuild over many later operations using lazy evaluation to keep persistent bounds.
prereqs: [global-rebuilding, banker-queue, memoization]
see_also: [debit-analysis, real-time-queue, bootstrapping, purely-functional-data-structure, catenable-deque, deque, amortized-vs-worst-case, persistent-data-structure]
sources:
  - url: "https://www.cs.cmu.edu/~rwh/students/okasaki.pdf"
    title: Chris Okasaki, Purely Functional Data Structures, PhD thesis, Carnegie Mellon University, 1996
    locator: Chapter 5, Lazy Rebuilding (Section 5.1, batched rebuilding, Section 5.2, global rebuilding, Section 5.3, lazy rebuilding, and Section 5.4, double-ended queues)
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 8, Lazy Rebuilding (batched rebuilding, global rebuilding, lazy rebuilding, and the banker's and real-time deques)
  - paper: doi:10.1016/0020-0190(81)90030-2
    title: Robert Hood and Robert Melville, Real-time queue operations in pure LISP, Information Processing Letters 13(2), 1981
    locator: pages 50 to 54 (a queue by global rebuilding, with the rebuild done in small steps)
---

Lazy rebuilding is Okasaki's way of keeping a purely functional data structure balanced with amortized bounds that stay valid under [persistence](/persistent-data-structure/). The structure is allowed to drift out of perfect balance, within a constant factor. When an operation would break this weaker invariant, the structure is rebuilt, but the rebuild is not done at once: it is set up as a lazy, memoized computation whose cost is paid by the operations that follow, before its result is needed. It sits between batched rebuilding, which rebuilds at once and loses its amortized bounds when an old version is reused, and [global rebuilding](/global-rebuilding/), which keeps a second copy and gets worst-case bounds at the cost of much more code. The [banker's queue](/banker-queue/) and the banker's [deque](/deque/) are its standard examples.

## In plain words

A structure works best when it is in good shape, for instance with its two halves of about equal size. Keeping it perfect after every change costs too much, so we let it get a little out of shape. When it gets too far out, we must fix it, and the fix is a big job.

We do not do the big job at once. We write down the job as a promise to be done later, and we make the promise early, while the structure is still usable. The next operations pay for the job a little at a time. The result is saved once it is done, so even if many old copies of the structure ask for it, the job is done only once.

## When it applies

- **A purely functional structure with a balance invariant.** A queue or deque made of two lists, a tree that must not get too deep, or any structure that is fast when a rebuild has restored its shape.
- **The rebuild can be suspended.** The language, or the implementation, provides lazy evaluation with [memoization](/memoization/): a suspended computation runs at most once, and later requests get the saved result.
- **Amortized bounds are enough, but persistence is required.** Lazy rebuilding gives amortized bounds that hold for every sequence of operations on any versions. For worst-case bounds, add a schedule that forces the suspension in small steps, which turns it into a form of global rebuilding.

## The template

The structure $s$ has a cheap part, where most operations work, and lazy parts. BALANCED tests the weak invariant, and REBUILD returns a balanced structure with the same contents whose expensive parts are suspensions.

```pseudo id=main
CHECK(s)
L1  if BALANCED(s) then return s
L2  return REBUILD(s)                ▷ builds suspensions; the real work happens when they are forced

OPERATION(s, x)
L3  s′ ← the change applied to the cheap part of s, forcing at most O(1) suspended steps
L4  return CHECK(s′)
```

The rebuild must leave enough slack: after REBUILD, a constant fraction of the size $n$ of the structure must be added or removed before BALANCED fails again. Then the $\Theta(n)$ cost of the rebuild can be charged to the $\Theta(n)$ operations that come before the next rebuild, and, with the [debit method](/debit-analysis/), to the operations that come before the result is forced.

**Why it survives persistence.** In batched rebuilding, the rebuild runs inside one operation. A program can keep the version just before the rebuild and apply that operation to it again and again, paying the full cost each time. In lazy rebuilding, the rebuild is a suspension stored in the version. Every use of that version shares the same suspension, so it runs at most once, and a debit argument shows that each suspension is paid for before it is forced, on every path through the [version tree](/version-tree/).

## Classic examples

### A trace of the banker's deque

The banker's deque is a front list $f$ and a rear list $r$, both lazy streams, with the sequence $f$ followed by the reverse of $r$. The weak invariant, for a constant $c$, is $|f| \le c|r| + 1$ and $|r| \le c|f| + 1$. When $|r| > c|f| + 1$, with $n = |f| + |r|$, the rebuild sets $j = \lfloor n/2 \rfloor$ and $i = n - j$, then $r' = \text{take}(j, r)$ and $f' = f \mathbin{+\!\!+} \text{reverse}(\text{drop}(j, r))$. The case $|f| > c|r| + 1$ is symmetric. Take $c = 2$ and snoc the numbers 1 to 5 onto the empty deque.

| step | $f$ | $r$ (newest first) | check |
|---|---|---|---|
| snoc 1 | $[\,]$ | $[1]$ | $1 \le 2 \cdot 0 + 1$ |
| snoc 2 | $[1]$ | $[2]$ | $2 > 1$: rebuild with $n = 2$, $j = 1$ |
| snoc 3 | $[1]$ | $[3, 2]$ | $2 \le 3$ |
| snoc 4 | $[1]$ | $[4, 3, 2]$ | $3 \le 3$ |
| snoc 5 | $[1, 2, 3]$ | $[5, 4]$ | $4 > 3$: rebuild with $n = 5$, $j = 2$ |

The contents are always $1, 2, \ldots$ in order: after snoc 5, $f = [1, 2, 3]$ and the reverse of $r$ is $[4, 5]$. The second rebuild only creates suspensions for $f \mathbin{+\!\!+} \text{reverse}([3, 2])$ and for $\text{take}(2, r)$. Their work is done when later operations walk into them. After a rebuild the two lists differ in length by at most one, so a constant fraction of $n$ operations must happen before the next rebuild.

### Other examples

- **The banker's queue.** The rotation $f \mathbin{+\!\!+} \text{reverse}(r)$ is done when $|r| = |f| + 1$, long before the front is empty, and as a lazy stream. It gives $O(1)$ amortized time per operation under persistence; see [banker's queue](/banker-queue/).
- **Real-time queues and deques.** If each operation also forces one step of the pending rotation, the suspension is fully evaluated by the time it is needed, and the bounds become worst case. See [real-time queue](/real-time-queue/).
- **Bootstrapped and catenable structures.** Okasaki's [catenable deques](/catenable-deque/) and the structures built by [bootstrapping](/bootstrapping/) use lazy rebuilding of their inner parts to keep amortized $O(1)$ bounds.

## Variations

- **Batched rebuilding.** Rebuild at once when the invariant fails, for example by reversing the rear list when the front becomes empty. This is simpler and has the same amortized bounds when each version is used once, but not under persistence.
- **Global rebuilding.** Build a new copy of the structure in the background, a few steps per operation, while the old copy answers queries, and switch when the copy is ready. Hood and Melville's real-time queue works this way. It gives worst-case bounds without lazy evaluation, but it must keep track of the updates that happen during the rebuild.
- **Scheduling.** Lazy rebuilding together with a schedule of suspensions to force gives worst-case bounds with simpler code than global rebuilding. This is how Okasaki derives real-time deques from banker's deques.

## Pitfalls

- **Laziness without memoization.** If a suspension is recomputed on each use, two uses of one version pay the rebuild twice, and the persistent bounds fail. Suspensions must be memoized.
- **Rebuilding too late.** If the rebuild is set up only when its result is needed at once, as when the front list is empty, the suspension is forced right away and the method becomes batched rebuilding.
- **A monolithic step that is forced too soon.** A reverse cannot produce its first element before it has seen the whole list. The rebuild must place it where it is reached only after enough operations, such as after the old front in $f \mathbin{+\!\!+} \text{reverse}(r)$.
- **Too little slack.** If the rebuilt structure is close to the edge of the invariant, the next rebuild comes after $o(n)$ operations, and the cost per operation is no longer constant.
- **Strict languages.** In a strict language the laziness must be explicit, with suspension objects that cache their result. An ordinary function closure without a cache is not enough.

## Exercises

1. Continue the trace with snoc 6, 7, 8 and 9, and give $f$, $r$ and each check.
2. In the banker's deque with $c = 2$, show that between two rebuilds caused by snoc alone, at least about $n/2$ elements are added, where $n$ is the size after the first of the two rebuilds.
3. Give a sequence of operations on persistent versions of a batched queue that takes $\Theta(n)$ time per operation, and explain why the banker's queue avoids it.
4. What changes in the rebuild if the deque must also support a size query in $O(1)$ time?

## References
