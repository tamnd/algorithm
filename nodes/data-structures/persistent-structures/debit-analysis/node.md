---
tag: SYHGAY
kind: technique
slug: debit-analysis
name: Debit analysis
aliases:
- debit method
- Okasaki debits
area: data-structures/persistent-structures
level: research
summary: Amortized analysis for lazy structures that charges shared suspensions as debits, valid under persistent use.
prereqs: [accounting-method, amortized-cost, memoization, banker-queue]
see_also: [lazy-rebuilding, potential-method, real-time-queue, finger-tree, catenable-deque, bootstrapping, purely-functional-data-structure, amortized-vs-worst-case]
sources:
  - url: "https://www.cs.cmu.edu/~rwh/students/okasaki.pdf"
    title: Chris Okasaki, Purely Functional Data Structures, PhD thesis, Carnegie Mellon University, CMU-CS-96-177, 1996
    locator: Chapter 3, Section 3.4, The Banker's Method (Section 3.4.1, the justification with the conditions I to III, and Section 3.4.2, the queue example and Theorem 3.1), and Section 3.5, The Physicist's Method
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 6, Amortization and Persistence via Lazy Evaluation (the banker's method, its justification, and banker's queues)
  - paper: doi:10.1137/0606031
    title: Robert E. Tarjan, Amortized computational complexity, SIAM Journal on Algebraic and Discrete Methods 6(2), 1985
    locator: pages 306 to 318 (the banker's view with credits and the physicist's view with potentials, for ephemeral structures)
---

Debit analysis, or the banker's method with debits, is Okasaki's method for proving amortized bounds for lazy data structures that hold even when old versions are reused. The usual [accounting method](/accounting-method/) saves credits in advance and spends them later, which fails under persistence because two futures of one version can spend the same credit. Debit analysis turns this around. When an operation creates a suspended computation, it records its cost as debits placed on the parts of the structure that the computation will produce, and later operations pay off, or *discharge*, a few debits each. The rule is that a suspension may be forced only after all its debits are discharged. With memoization, each suspension runs at most once, so the debits discharged bound the real cost on every branch of the [version tree](/version-tree/).

## In plain words

When a lazy structure decides to do a big job later, it writes an IOU for the job and pins it to the part of the structure that the job will build. Each later operation pays off a small, fixed amount of the IOUs. The rule is that nobody may look at a part before the IOUs pinned to it are paid.

Why does this survive many futures? The job is shared: if two futures both reach it, the work is done once and the result is saved. Paying an IOU twice, once in each future, only overcounts. So the payments always cover the work that is really done, whatever the program does with old versions.

## When it applies

- **The structure uses lazy evaluation with memoization.** Expensive steps, such as a reverse or an append of streams, are suspensions that run when first forced and save their result.
- **The structure is used persistently.** The method is needed when old versions may be used again, as in any purely functional program. For single-threaded use the ordinary accounting or [potential method](/potential-method/) is enough.
- **Costs split into unshared and shared.** The *unshared cost* of an operation is the work it does at once. The *shared cost* is the work it suspends, which may be forced by later operations, possibly in several futures.

## The template

The method assigns to each operation $v$ a set $s(v)$ of debits it creates and a multiset $a(v)$ of debits it discharges, and keeps a *debit invariant* on the structure.

```pseudo id=main
DEBIT-ANALYSIS(structure, operations)
L1  for each suspension that an operation creates, with shared cost c do
L2      create c debits; put them all on the root of its result if it is monolithic, or spread them over its partial results if it is incremental
L3  state a debit invariant: for each node i, D(i), the number of debits on the path from the root to node i, is at most a bound B(i)
L4  choose B so that a node that an operation forces has B = 0 at that moment
L5  for each operation, show that discharging a constant number k of debits restores the invariant
L6  conclude: the amortized cost of an operation is its unshared cost plus the debits it discharges, so O(1) + k
```

Line L2 depends on the kind of suspension. A *monolithic* computation, such as reverse, runs to completion once it starts, so all its debits go on the first node of its result. An *incremental* computation, such as the append of two streams, produces its result node by node, so its debits can be spread, one on each node it produces. Line L3 bounds cumulative debits along a path because forcing a node forces its ancestors first.

**Why it works.** Okasaki states the method as a labelling of the execution trace, the directed acyclic graph of operations in which an edge leads from an operation to each operation that uses its result. The *logical history* $\hat v$ of an operation $v$ is the set of operations from which $v$ can be reached, including $v$. Let $r(v)$ be the multiset of debits realized by $v$, that is, of the suspensions it forces. The analysis must satisfy:

1. (I) $s(v) \cap s(v') = \emptyset$ for $v \ne v'$: each debit is created once.
2. (II) $a(v) \subseteq \bigcup_{w \in \hat v} s(w)$: a debit is discharged only after it is created, in the logical history.
3. (III) $r(v) \subseteq \bigcup_{w \in \hat v} a(w)$: a debit is realized only after it is discharged, in the logical history.

The total actual cost is the total unshared cost plus the cost of the suspensions that run. By memoization each suspension runs at most once, so the realized shared cost is $\left|\bigcup_v r(v)\right|$, without duplicates. By (III), $\bigcup_v r(v) \subseteq \bigcup_v a(v)$, so
$$\Bigl|\bigcup_{v} r(v)\Bigr| \le \Bigl|\bigcup_{v} a(v)\Bigr| \le \sum_{v} |a(v)|.$$
So the total actual cost is at most the total unshared cost plus the total number of debits discharged, which is the total amortized cost. The debits created are not part of the amortized cost, and debits that are never discharged belong to suspensions that are never forced. The argument needs memoization: with recomputation, the realized cost would be $\sum_v |r(v)|$, which has no such bound.

## Classic examples

### The banker's queue

The [banker's queue](/banker-queue/) of Okasaki's thesis keeps a front stream $F$ and a rear stream $R$ with $|F| \ge |R|$, and rotates to $F \mathbin{+\!\!+} \text{reverse}(R)$ when $|R| = |F| + 1$. Let $d(i)$ be the number of debits on node $i$ of the front stream, counting from 0, and $D(i) = \sum_{j \le i} d(j)$. The invariant is
$$D(i) \le \min(2i, |F| - |R|).$$
The term $2i$ makes $D(0) = 0$, so the head can be forced at any time. The term $|F| - |R|$ makes all debits zero just before a rotation, when $|F| = |R|$. Theorem 3.1 of the thesis shows that snoc discharges one debit and tail two.

Take a rotation with $|F| = 3$ and $|R| = 4$. The append costs 3 debits, one on each of nodes 0 to 2, since it is incremental. The reverse costs 4 debits, all on node 3, the first node of the reversed part, since it is monolithic. After the rotation, $|F| = 7$ and $|R| = 0$.

| node $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $d(i)$ | 1 | 1 | 1 | 4 | 0 | 0 | 0 |
| $D(i)$ | 1 | 2 | 3 | 7 | 7 | 7 | 7 |
| bound $\min(2i, 7)$ | 0 | 2 | 4 | 6 | 7 | 7 | 7 |
| $D(i)$ after one discharge | 0 | 1 | 2 | 6 | 6 | 6 | 6 |

The invariant fails at nodes 0 and 3, and discharging the one debit on node 0 lowers every $D(i)$ by one and restores it. In general, a rotation with $|F| = m$ gives $D(i) = i + 1$ for $i < m$ and $D(i) = 2m + 1$ for $i \ge m$, and one discharge is enough.

### Why reuse does not break it

Let $q_0$ have $|F| = |R| = m$, and let $q_i$ be the tail of $q_{i-1}$. The first tail rotates, and the $m + 1$-th forces the reverse. If a program runs the tail of $q_m$ many times, every run forces the same memoized suspension, so the reverse is done once. If it branches at $q_0$ instead, each branch creates its own rotation, but then each branch also has its own $m + 1$ operations to pay for it. This is the informal argument of Section 3.4.2 of the thesis, and conditions (I) to (III) make it precise.

### Other examples

- **Lazy rebuilding.** The banker's deque and other structures of [lazy rebuilding](/lazy-rebuilding/) are analysed with debits placed on the rebuilt lists.
- **Finger trees.** Hinze and Paterson prove the $O(1)$ amortized bounds of [finger trees](/finger-tree/) under persistence by placing debits on the lazy middle trees.
- **Catenable and bootstrapped structures.** Okasaki's [catenable deques](/catenable-deque/) and the structures built by [bootstrapping](/bootstrapping/) use debits on the suspended inner structures.
- **From amortized to worst case.** If each operation forces the suspensions whose debits it discharges, one step each, the amortized bound becomes a worst-case bound. This is how the [real-time queue](/real-time-queue/) arises from the banker's queue.

## Variations

- **The physicist's method with debts.** Instead of placing debits on nodes, define a potential that bounds the unpaid shared cost of the whole structure. An operation's amortized cost is its unshared cost plus its shared cost minus the change in potential. It needs fewer choices than placing debits, but its single bound for the whole structure is weaker when parts of the structure are forced at different times. Okasaki presents both methods side by side in Chapter 3 of his thesis.
- **Credits in ephemeral analysis.** The classic banker's view of Tarjan stores credits on the structure and spends them later. It is correct only when each version is used at most once, since a credit can be spent twice in two futures, while a debit paid twice only overcounts.
- **Scheduling.** Debit arguments tell which suspension is paid for when, which is the information needed to build a schedule and eliminate the amortization.

## Pitfalls

- **No memoization.** Without memoization, condition (III) bounds the wrong quantity, and the persistent bound fails. In a strict language every suspension must cache its result.
- **Charging the creation instead of the discharge.** The debits created by an operation are not part of its amortized cost. An analysis that charges them is valid but usually gives a worse bound.
- **Monolithic debits spread out.** Putting the debits of a reverse on several nodes is wrong: the first node of the result cannot be produced before the whole reverse runs, so all its debits must be paid before that node is forced.
- **Forcing too early.** If an operation forces a node whose cumulative debit is not yet zero, the analysis is broken. The invariant must make $B = 0$ for every node that the operations force, as the term $2i$ does for the head of the queue.
- **Ignoring nested suspensions.** The nodes of an incremental computation are suspensions that do not exist yet. Their debits are counted on the positions where they will appear, as in the append above.

## Exercises

1. Redo the table for a rotation with $|F| = 5$ and $|R| = 6$, and show that one discharge restores the invariant.
2. Show that a tail that does not rotate lowers $2i$ by 2 for every remaining node, and that discharging the first two debits restores the invariant.
3. Explain why the invariant $D(i) \le |F| - |R|$ alone does not suffice for the queue.
4. Give an execution trace in which the same debit is discharged twice, by catenating a list with itself, and check that conditions (I) to (III) still give a valid bound.

## References
