---
tag: 0MCR8H
kind: concept
slug: logarithmic-time
name: Logarithmic time
aliases:
- O(log n) time
area: foundations/asymptotic-analysis
level: intro
summary: Running time that grows with the logarithm of input size, as in halving the input at each step.
prereqs: [asymptotic-notation, logarithms, time-complexity]
see_also: [common-growth-rates, constant-time, linear-time, polylogarithmic-time, sublinear-time, binary-search, binary-heap, modular-exponentiation]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 2 (analyzing algorithms) and Chapter 3
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1 (searching an ordered table)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4
---

An algorithm runs in logarithmic time when its running time is $T(n) = \Theta(\log n)$, or $O(\log n)$ when only an upper bound is known, for an input of size $n$. The base of the [logarithm](/logarithms/) does not change the class. The typical cause is a step that cuts the remaining work by a constant factor, such as one half.

## In plain words

Think of looking for a name in a printed phone book. You open the book in the middle, see that the name comes earlier, and throw away the second half. You repeat on what is left. A book of one million pages needs at most 20 looks. A book with twice as many pages needs only one more look.

This is the logarithmic pattern. The work does not shrink by a fixed number of items at each step. It shrinks by a fixed fraction. When the input doubles, the cost grows by a fixed amount, not by a fixed factor.

The pattern has a condition. You must be able to jump to the middle at once. In a phone book you can. In a chain of pages where you must turn each page one at a time, you cannot, and the halving idea does not help.

## The idea

### Definition

Fix a model and a case. Let $T(n)$ be the cost in that model and case. The algorithm runs in logarithmic time when $T(n) = O(\log n)$. For a tight claim, $T(n) = \Theta(\log n)$. Since $\log_a n = \log_b n / \log_b a$, the choice of the base only changes the constant, and $\Theta(\lg n) = \Theta(\ln n)$. The claim also needs $n \ge 2$ so that $\log n > 0$.

### Shapes of logarithmic-time algorithms

**Halving a search range.** [Binary search](/binary-search/) in a sorted array of $n$ items keeps an interval of candidates. Each iteration compares the key with the middle item, which removes at least that item, and keeps one side. An interval of $m$ items leaves $\lfloor (m-1)/2 \rfloor$ items on the left and $\lceil (m-1)/2 \rceil = \lfloor m/2 \rfloor$ on the right, so the new size is at most $\lfloor m/2 \rfloor$. After $k$ iterations the size is at most $\lfloor n / 2^k \rfloor$, because $\lfloor \lfloor x \rfloor / 2 \rfloor = \lfloor x/2 \rfloor$ for each real $x \ge 0$. This is $0$ exactly when $2^k > n$, that is, when $k \ge \lfloor \lg n \rfloor + 1$. So the search stops after at most $\lfloor \lg n \rfloor + 1$ iterations, with one comparison in each, A key larger than every item always keeps the right side, of size $\lfloor m/2 \rfloor$, so it takes exactly $\lfloor \lg n \rfloor + 1$ iterations. The worst case is therefore $\Theta(\log n)$ in the word RAM, if reading `A[i]` costs one step. A [decision tree](/decision-tree-model/) argument shows that each comparison-based search in a sorted array needs $\lceil \lg(n+1) \rceil = \lfloor \lg n \rfloor + 1$ comparisons in the worst case, so binary search is optimal. For $n = 10^3, 10^6, 10^9$ the bound is $10, 20, 30$ iterations.

**Walking one root-to-leaf path in a balanced tree.** A binary tree with $n$ nodes whose height is $h$ has $n \le 2^{h+1} - 1$, so $h \ge \lceil \lg(n+1) \rceil - 1$. A [binary heap](/binary-heap/) is a complete binary tree, and its height is $\lfloor \lg n \rfloor$. Insertion and deletion of the minimum move along one path, so each costs $O(\log n)$ in the worst case. A [balanced binary search tree](/balanced-binary-search-tree/) keeps its height $O(\log n)$ by its rebalancing rules, and then search, insert and delete cost $O(\log n)$ in the worst case. An unbalanced search tree has no such bound: its height can be $n - 1$.

**Reducing a number by a constant factor.** [Modular exponentiation](/modular-exponentiation/) by repeated squaring computes $b^e$ with at most $\lfloor \lg e \rfloor$ squarings and at most $\lfloor \lg e \rfloor$ extra multiplications, because the bits of $e$ are processed one at a time. The same shape holds for the Euclidean algorithm, where two steps at least halve the larger number. These costs are logarithmic in the value $e$, which is linear in the number of bits of $e$. See the pitfalls.

**Counting the digits.** The number of digits of $n$ in base $b$ is $\lfloor \log_b n \rfloor + 1$, so any procedure that handles one digit per step is logarithmic in the value of $n$.

### When the input doubles

For exact cost $\lg n$, we have $\lg(2n) = \lg n + 1$, so the cost grows by a fixed amount, here one step for each doubling. For $T(n) = a \lg n + b$ the added cost is $a$. The ratio $T(2n)/T(n)$ tends to 1 from above as $n$ grows. Going from $10^3$ to $10^6$ items is a factor 1000 in size and a factor of only about 2 in $\lg n$ (10 to 20).

### Pitfalls

- **Random access is required.** Binary search on a [linked list](/linked-list/) makes $O(\log n)$ comparisons, but each time it needs the middle node it walks the list. Even when each walk starts at the first node of the current interval, the walks cost $n/2 + n/4 + \cdots$ steps, which is $\Theta(n)$ in total. So the time is not logarithmic. The model must let the algorithm reach the middle item in $O(1)$ time.
- **The input must be sorted or structured.** Binary search on an unsorted array is wrong, not only slow. A tree gives a logarithmic bound only when it is balanced.
- **Logarithmic in the value is not logarithmic in the input size.** The input of "compute $b^e \bmod m$" includes $e$, which takes $\Theta(\log e)$ bits, see [input size](/input-size/). A cost of $O(\log e)$ multiplications is then linear in the input size. Also, the multiplications act on numbers that grow, so the unit-cost assumption can fail. In modular exponentiation the numbers stay below the modulus $m$, so each multiplication has a fixed cost that depends on the size of $m$, and it is $O(1)$ when $m$ fits in a word.
- **Hidden extra cost.** A comparison between keys is one step only when a key fits in a word. For strings of length $m$, a search in a balanced tree costs $O(m \log n)$ character comparisons in the worst case.
- **Amortized and expected claims.** A bound can be logarithmic only amortized, as for a [splay tree](/splay-tree/), or in expectation, as for a [skip list](/skip-list/). Name the case.
- **Sublinear, but not free.** A logarithmic algorithm reads only $O(\log n)$ items of the input, so it can be correct only when the structure of the input (sorted order, a heap order) tells where the answer is. See [sublinear time](/sublinear-time/).

## Examples

- Binary search in a sorted array of $10^6$ items: at most 20 iterations in the worst case.
- Insert into a binary heap that holds $10^6$ items: the height is $\lfloor \lg 10^6 \rfloor = 19$, so the sift-up moves at most 19 levels.
- Compute $3^{1000} \bmod 1009$ by repeated squaring: $\lfloor \lg 1000 \rfloor = 9$ squarings and 5 extra multiplications, because $1000 = 1111101000_2$ has six 1-bits.
- Non-example: binary search on a linked list of $n$ items, which takes $\Theta(n)$ pointer steps.
- Non-example: finding an item in an unsorted array. Any algorithm must read $\Omega(n)$ items in the worst case, so the time is [linear](/linear-time/).
- Non-example: the number of steps of an algorithm that halves the input but also scans it at each step. If it scans $m$ items at the stage of size $m$, the total is $n + n/2 + n/4 + \cdots < 2n$, which is $\Theta(n)$.

## Where it is used

Logarithmic time is the cost of one operation in ordered structures: the [binary heap](/binary-heap/), the [balanced binary search tree](/balanced-binary-search-tree/) and the [Fenwick tree](/fenwick-tree/) and [segment tree](/segment-tree/) for range queries. Repeating such an operation $n$ times gives [linearithmic time](/linearithmic-time/). A cost that is a power of $\log n$ is [polylogarithmic](/polylogarithmic-time/). The sum $\lg 1 + \lg 2 + \cdots + \lg n = \lg(n!) = \Theta(n \log n)$, so $n$ logarithmic steps on a structure that grows still cost linearithmic time. See the table of the [common growth rates](/common-growth-rates/).

## References
