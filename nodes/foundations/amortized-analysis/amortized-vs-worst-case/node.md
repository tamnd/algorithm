---
tag: 0WHR9K
kind: concept
slug: amortized-vs-worst-case
name: Amortized versus worst-case cost
aliases:
- amortized vs worst-case bound
area: foundations/amortized-analysis
level: intro
summary: Amortized bounds guarantee total cost over a sequence, while worst-case bounds guarantee each single operation.
prereqs: [amortized-cost, worst-case-analysis]
see_also: [potential-method, array-doubling, global-rebuilding, real-time-queue, amortized-vs-expected-cost, amortized-update-time, worst-case-update-time, union-find-with-rollback]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 16, Amortized Analysis (introduction and Section 16.4)
  - paper: doi:10.1137/0606031
    title: Robert E. Tarjan, Amortized computational complexity, SIAM Journal on Algebraic and Discrete Methods 6(2), 1985
    locator: pp. 306 to 318
  - paper: doi:10.1145/3828.3835
    title: Daniel D. Sleator and Robert E. Tarjan, Self-adjusting binary search trees, Journal of the ACM 32(3), 1985
    locator: pp. 652 to 686
  - book: isbn:9783540123309
    title: Mark H. Overmars, The Design of Dynamic Data Structures, Lecture Notes in Computer Science 156, Springer (1983)
    locator: Chapter "Global rebuilding", pp. 67 to 77
  - paper: doi:10.1137/0215072
    title: Norbert Blum, On the single-operation worst-case time complexity of the disjoint set union problem, SIAM Journal on Computing 15(4), 1986
    locator: pp. 1021 to 1024
  - paper: doi:10.1145/73007.73040
    title: Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, STOC 1989
    locator: pp. 345 to 354
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press (1998)
    locator: Chapter 5 (amortization and its failure under persistence) and Chapter 7 (eliminating amortization)
---

A worst-case bound on an operation limits the cost of each single call. An [amortized](/amortized-cost/) bound limits only the total cost of each sequence of calls from the start state, so one call can be far more expensive than its bound. Each worst-case bound is also an amortized bound, but not the other way round: an append to a [doubling array](/array-doubling/) is $O(1)$ amortized and $\Theta(n)$ in the worst case. The choice between the two matters when single operations have deadlines, when old versions of a structure are reused, and when the structure is shared between threads.

## In plain words

A worst-case promise says: no single call will ever take longer than this. An amortized promise says: add up the time of all calls so far, and the sum will never be more than this much per call. Both are guarantees, with no luck involved. But the amortized one lets a single call be slow, as long as the calls before it were fast enough to pay for it. For a program that only cares about its total running time, this is fine. For a program that must answer each request within a few milliseconds, one slow call is a failure, even if the average is excellent. Some amortized structures can be changed so that each call is fast; this is called de-amortization.

## The idea

Fix a data structure, its start state $D_0$ and a cost model. Let $c_i$ be the actual cost of the $i$-th operation of a legal sequence.

- A **worst-case bound** $W(n)$ for an operation type says: each operation of this type on a structure of size $n$ costs $c_i \le W(n)$.
- An **amortized bound** $A(n)$ says: there is a valid assignment of charges $\hat c_i$ with $\hat c_i \le A(n)$ for each operation of this type, and for each legal sequence and each $m$, $\sum_{i \le m} c_i \le \sum_{i \le m} \hat c_i$.

**Facts.**

1. **Worst case implies amortized.** If each operation has $c_i \le W$, then $\hat c_i = W$ is valid. So a worst-case bound is an amortized bound with the same function.
2. **Amortized does not imply worst case.** The doubling array has $A = 3$, but the append that finds $2^{20}$ items in a full array copies 1,048,576 of them.
3. **What an amortized bound says about one operation.** Only that it costs at most the total of all charges so far: $c_m \le \sum_{i \le m} \hat c_i \le m \max_i \hat c_i$.
4. **A window in the middle is not bounded by its charges.** With a [potential](/potential-function/) $\Phi$, the operations $i$ to $j$ cost $\sum_{t=i}^{j} c_t = \sum_{t=i}^{j} \hat c_t + \Phi(D_{i-1}) - \Phi(D_j)$. The stored potential $\Phi(D_{i-1})$ can be spent in a short window. After $n$ pushes onto a [stack with multipop](/stack-with-multipop/), one MULTIPOP$(n)$ costs $n$, although its charge is 0.
5. **Amortized bounds need the newest version.** The proof of an amortized bound follows one line of states $D_0, D_1, D_2, \ldots$. If a program goes back to an old state, as in a [persistent structure](/persistent-data-structure/) or an undo feature, the same stored potential can be spent many times. Worst-case bounds hold for each state, so they survive persistence.

**De-amortization.** Many amortized structures have a version with the same bounds in the worst case. The usual tool is to do the expensive work in small steps in advance, before it is needed: [global rebuilding](/global-rebuilding/) in the sense of Overmars (1983), incremental copying for [array doubling](/array-doubling/), the [real-time queue](/real-time-queue/) of Hood and Melville, and the scheduling of lazy computations in Okasaki's book. The price is more complex code, a larger constant factor and often more memory. Not every amortized bound can be de-amortized; union-find below is an example.

## Examples

| structure | operation | amortized | worst case of one operation |
|---|---|---|---|
| [dynamic array](/dynamic-array/) with doubling | append | $O(1)$ | $\Theta(n)$; $O(1)$ with incremental copying |
| [queue from two stacks](/two-stacks-queue/) | dequeue | $O(1)$ | $\Theta(n)$; $O(1)$ for the [real-time queue](/real-time-queue/) |
| [binary counter](/binary-counter-increment/) | increment | 2 bit flips | $k$ bit flips |
| [splay tree](/splay-tree/) | access | $O(\log n)$ | $\Theta(n)$ |
| [Fibonacci heap](/fibonacci-heap/) | extract-min | $O(\log n)$ | $\Theta(n)$: after $n$ inserts the first extract-min consolidates $n - 1$ roots; the [Brodal queue](/brodal-queue/) and the [strict Fibonacci heap](/strict-fibonacci-heap/) reach the heap bounds in the worst case |
| [union-find](/union-find-amortized-bound/) with rank and path compression | find | $O(\alpha(m, n))$ | $\Theta(\log n)$ |

**Splay tree.** Insert the keys $1, 2, \ldots, n$ in increasing order into an empty splay tree. Each insertion puts the new key at the root with the old tree as its left subtree, so each insert is cheap and the tree becomes a path. Then an access to key 1 makes $n - 1$ rotations. The amortized bound $3 \lg n + 1$ per access is still true, because the cheap inserts raised the potential that this access spends.

**Union-find.** With union by rank and path compression, $m$ operations on $n$ elements take $O(m\,\alpha(m, n))$ time (see [union-find amortized bound](/union-find-amortized-bound/)), but one find can take $\Theta(\log n)$ time. Blum (1986) gave a structure with $O(\log n / \log \log n)$ worst-case time for each operation, and showed this is optimal for a class of pointer algorithms; Fredman and Saks (1989) proved a lower bound of the same order for each operation in the [cell probe model](/cell-probe-model/). So for union-find the best worst-case bound per operation is much larger than the best amortized bound, and no de-amortization can close the gap. See [Blum's structure](/blum-union-find/).

**Union-find with undo.** The [union-find with rollback](/union-find-with-rollback/) used in offline dynamic connectivity undoes unions. Undo returns to old states, which breaks the amortized argument of path compression. The usual version drops path compression and keeps union by rank, which gives $O(\log n)$ worst-case finds.

## Where it is used

- **Algorithms that only need the total.** In [Dijkstra's algorithm](/dijkstra/) with a [Fibonacci heap](/fibonacci-heap/), or in Kruskal's algorithm with union-find, only the total running time matters, so amortized bounds are the right tool and give the best known totals.
- **Real-time and interactive systems.** Audio processing, games, control loops and network switches have a deadline for each step. They use worst-case structures, or de-amortized ones. [Baker's real-time collector](/baker-real-time-collector/) and [incremental garbage collection](/incremental-garbage-collection/) do the work of a collection in small steps for this reason.
- **Services with latency targets.** A server that must answer 99.9 percent of requests within a time limit sees a resize of a large table as a spike in tail latency. Incremental resizing of hash tables is common for this reason.
- **Persistent and functional data structures.** Okasaki shows that amortized bounds proved by credits or potential fail when old versions are reused, and gives two answers: lazy evaluation with debits, which restores amortized bounds, and scheduling, which gives worst-case bounds.
- **Concurrency.** If one operation holds a lock for $\Theta(n)$ time, all other threads wait. Concurrent hash tables resize in steps, or let several threads share the work of a resize.
- **Dynamic graph algorithms.** The literature states [amortized update time](/amortized-update-time/) and [worst-case update time](/worst-case-update-time/) as separate results, and the worst-case version of a bound is often a separate, harder paper.

## References
