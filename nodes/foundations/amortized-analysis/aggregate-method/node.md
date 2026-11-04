---
tag: XAF6YT
kind: technique
slug: aggregate-method
name: Aggregate method
aliases:
- aggregate analysis
area: foundations/amortized-analysis
level: intro
summary: Bounds the total cost of a sequence of n operations and divides by n to get the amortized cost.
prereqs: [amortized-cost, asymptotic-notation, geometric-series]
see_also: [accounting-method, potential-method, stack-with-multipop, binary-counter-increment, array-doubling, monotonic-stack, graham-scan, knuth-morris-pratt]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 16.1, Aggregate analysis (stack operations and incrementing a binary counter)
  - paper: doi:10.1137/0606031
    title: Robert E. Tarjan, Amortized computational complexity, SIAM Journal on Algebraic and Discrete Methods 6(2), 1985
    locator: pp. 306 to 318
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms (amortized analysis of the resizing array)
---

The aggregate method is the simplest way to prove an [amortized cost](/amortized-cost/): you bound the total actual cost $T(n)$ of each legal sequence of $n$ operations, and then charge $T(n)/n$ to each operation. The bound on the total comes from a global count, such as "each item is pushed at most once and popped at most once", and not from a bound on each single operation. It gives the same charge to all operation types. It is the first of the three methods in CLRS, before the [accounting method](/accounting-method/) and the [potential method](/potential-method/).

## In plain words

Some operations of a data structure are cheap most of the time and expensive now and then. If you add the worst case of each operation, the sum is too large, because the expensive cases cannot all happen. The aggregate method does not look at the operations one at a time. It looks at the whole run and asks a different question: how many times, in total, can each piece of work happen? An item that enters a stack one time can leave it at most one time. A bit of a counter that flips at each second step flips about half as often as the step before it. When you count the work in this way, the total is often a small multiple of the number of operations. Then the average cost of an operation in the run is a small constant, even if one operation is slow.

## When it applies

- The expensive work of one operation consumes something that cheaper operations made: items that were pushed, ones that were set, slots that were filled. Then each unit of work can be charged to the event that created it.
- Each item or each position takes part in the expensive work a bounded number of times, or a number of times that drops geometrically.
- You need one bound for the whole sequence, and all operation types can share the same charge. If you need different charges for different types (push 2, pop 0), the [accounting method](/accounting-method/) or the [potential method](/potential-method/) is a better fit.
- The sequence starts from a fixed state, usually empty. The bound is for sequences from that state.

## The template

```pseudo id=main
AGGREGATE-BOUND(structure, operation types)
L1  fix the cost model: the unit that each operation pays for (a step, a bit flip, a copied item)
L2  take an arbitrary legal sequence o_1, ..., o_n from the start state D_0
L3  split the actual cost into kinds of work W_1, ..., W_r          ▷ hole: the split
L4  for each kind W_j, find a global count: W_j ≤ g_j(n)            ▷ hole: the counting argument
L5  T(n) ← g_1(n) + ... + g_r(n)                                   ▷ total, valid for every sequence
L6  report the amortized cost T(n) / n for each operation
```

The two holes are the split of line L3 and the counts of line L4. The count must hold for every legal sequence of length $n$, not for a typical one. Because each prefix of a legal sequence is a legal sequence of shorter length, the bound $T(k) \le g(k)$ for all $k$ also covers each prefix, which is what the definition of amortized cost asks for. If $g$ is not linear, report $T(n)/n$ as a function of $n$; it is then an upper bound on the average cost in a sequence of length $n$, not a charge that each operation can use in a shorter sequence.

Three ways to do the count of line L4 come up again and again.

1. **One event per creation.** Each unit of expensive work destroys an object that one earlier operation created. Then the expensive work is at most the number of creations.
2. **Per position.** Count, for each position $i$, how often it takes part in the work, and add over $i$. If the counts fall geometrically in $i$, the sum is a constant times the largest count.
3. **Per expensive event.** List the expensive events and their sizes, and add them as a [geometric series](/geometric-series/).

## Classic examples

- **[Stack with multipop](/stack-with-multipop/)** (way 1). Each item is popped at most once after it is pushed, so the pops of all POP and MULTIPOP calls cost at most the number of pushes. With $n$ operations, $T(n) \le 2n$, so each operation costs at most 2 amortized.
- **[Binary counter increment](/binary-counter-increment/)** (way 2). In $n$ increments from 0, bit $i$ flips exactly $\lfloor n / 2^i \rfloor$ times, because it flips each time the value of the counter passes a multiple of $2^i$. So $T(n) = \sum_{i \ge 0} \lfloor n / 2^i \rfloor < n \sum_{i \ge 0} 2^{-i} = 2n$. The exact total is $2n - s_2(n)$, where $s_2(n)$ is the number of 1 bits of $n$. For $n = 1000$ it is 1994.
- **[Array doubling](/array-doubling/)** (way 3). An append into a full array of capacity $c$ copies $c$ items, and the capacities that fill up are $1, 2, 4, \ldots$. For $n \ge 1$ appends from an empty array, the copies are $1 + 2 + \cdots + 2^{\lceil \lg n \rceil - 1} = 2^{\lceil \lg n \rceil} - 1 < 2n$, so $T(n) < 3n$. For $n = 1000$ the copies are 1023 and the total is 2023.
- **[Depth-first search](/depth-first-search/)** (way 2). The loop over the neighbours of a vertex runs once for each vertex, so the scans of all adjacency lists cost $\sum_v \deg(v) = 2|E|$ in an undirected graph, although one vertex can have $|V| - 1$ neighbours.
- **[Monotonic stack](/monotonic-stack/) and [Graham scan](/graham-scan/)** (way 1). Each item is pushed once, so the while loops that pop cost $O(n)$ in total over the whole scan, although one step can pop many items.
- **The [prefix function](/prefix-function/) of [Knuth, Morris and Pratt](/knuth-morris-pratt/)** (way 1). The current border length $k$ grows by at most 1 in each step and each fallback lowers it by at least 1, so all fallbacks together cost at most $n - 1$.
- **[Linked-list disjoint sets](/linked-list-disjoint-sets/) with union by size** (way 2). An element changes its representative pointer only when its list is the smaller one, so the size of its list at least doubles each time. Each element is moved at most $\lfloor \lg n \rfloor$ times, and $m$ operations on $n$ elements cost $O(m + n \log n)$.

## Variations

- **Count with an inequality, not an identity.** Most proofs only need $T(n) \le g(n)$. When an exact identity is easy, as for the counter, it also shows that the bound is tight.
- **Several parameters.** In union-find and in graph algorithms, the total depends on two sizes, as in $O(m + n \log n)$. Report the bound in both parameters and do not divide by one of them.
- **Start state other than empty.** If the structure starts in a state $D_0$ that already holds work to do (a counter with ones, a stack with items), add that stored work to $T(n)$. For a stack that starts with $s_0$ items, $T(n) \le 2n + s_0$.
- **Lower bounds by the same count.** A sequence that makes each count of line L4 tight shows that the amortized bound is tight. Pushes followed by one MULTIPOP reach $2k$ for $k + 1$ operations.

## Pitfalls

- **Adding worst cases.** "Each MULTIPOP costs up to $n$, so $n$ operations cost $O(n^2)$" is a correct upper bound, but it is not tight. The aggregate method replaces this sum by a global count.
- **A count for one good sequence.** The total must be bounded for each legal sequence. A sequence of only increments gives $2n$, but a mix of increments and decrements of a $k$-bit counter can cost $kn$. If the set of operations changes, redo the count.
- **Forgetting a prefix.** The amortized charge must cover each prefix of a sequence. A bound that is true only at the end of a full cycle, for example "after each rebuild the total is $3n$", does not cover a sequence that stops in the middle of the cycle, unless the work done so far is also bounded.
- **Dividing a nonlinear total.** If $T(n) = \Theta(n \log n)$, then $T(n)/n = \Theta(\log n)$ is an average, and each operation is charged $O(\log n)$ only if the same $n$ bounds the length of the sequence. State which $n$ you use.
- **One charge for all types.** The aggregate method gives the same charge to a cheap operation and an expensive one. If you need the cost of one type alone, for example a bound on the number of pops in terms of pushes, use the [accounting method](/accounting-method/).

## Exercises

1. A stack supports PUSH, POP and MULTIPUSH$(k)$, which pushes $k$ items. Show that the aggregate method does not give an $O(1)$ amortized cost for MULTIPUSH, and give a valid amortized cost in terms of $k$.
2. A counter in base 3 counts from 0 to $n$. Show that the total number of digit changes is less than $\tfrac{3}{2} n$.
3. An array grows by a factor of 3 when it is full. Bound the total number of copies for $n$ appends from an empty array of capacity 1.
4. Show that $\sum_{i \ge 0} \lfloor n / 2^i \rfloor = 2n - s_2(n)$ by writing $n$ in binary.

## References
