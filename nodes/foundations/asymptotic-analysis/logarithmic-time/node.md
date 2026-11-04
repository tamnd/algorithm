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
see_also: [common-growth-rates, constant-time, linear-time, polylogarithmic-time, sublinear-time, binary-search, binary-heap, euclidean-algorithm]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Searching an Ordered Table (binary search, its optimality, interpolation search)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.3, Analysis of Euclid's Algorithm; Section 4.6.3, Evaluation of Powers
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6 (heaps, height of a heap) and Chapter 31 (Euclid's algorithm, modular exponentiation)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.1 (binary search) and Section 1.4, Analysis of Algorithms
---

An algorithm runs in logarithmic time when its cost is $T(n) = \Theta(\log n)$, or $O(\log n)$ when only an upper bound is known, for an [input size](/input-size/) $n$. The base of the [logarithm](/logarithms/) does not change the class. The typical cause is a step that cuts the remaining work by a constant factor, as [binary search](/binary-search/) does, and the bound needs a model in which the algorithm can jump to any position in one step.

## In plain words

Think of looking for a name in a printed phone book. You open the book in the middle, see that the name comes earlier, and throw away the second half. You repeat on what is left. A book of one million pages needs at most 20 looks. A book with twice as many pages needs only one more look.

This is the logarithmic pattern. The work does not shrink by a fixed number of items at each step. It shrinks by a fixed fraction. When the input doubles, the cost grows by a fixed amount, not by a fixed factor.

The pattern has two conditions. The input must be in order, so that you know which part to throw away. And you must be able to jump to the middle at once. If you must turn each page one at a time, halving does not help.

## The idea

### Definition

Fix a model and a case. Let $T(n)$ be the cost in that model and case. The algorithm runs in logarithmic time when $T(n) = O(\log n)$, and the bound is tight when $T(n) = \Theta(\log n)$. Since $\log_a n = \log_b n / \log_b a$ for bases $a, b > 1$, the base only changes the constant, and $\Theta(\lg n) = \Theta(\ln n)$. The bound is stated for $n \ge 2$, so that $\log n > 0$.

### The main example: binary search

```pseudo id=bs
BINARY-SEARCH(A, n, x)                 ▷ A[0 .. n − 1] is sorted
L1  lo ← 0, hi ← n                     ▷ candidates are A[lo .. hi − 1]
L2  while lo < hi do
L3      mid ← lo + ⌊(hi − lo − 1) / 2⌋
L4      if A[mid] = x then return mid
L5      if A[mid] < x then lo ← mid + 1 else hi ← mid
L6  return NOT-FOUND
```

*Claim.* For $n \ge 1$, the loop runs at most $\lfloor \lg n \rfloor + 1$ times, and a key larger than every item makes it run exactly that many times.

*Proof.* Let $m = hi - lo$ be the number of candidates. The left part $A[lo \ldots mid-1]$ has $\lfloor (m-1)/2 \rfloor$ items and the right part has $m - 1 - \lfloor (m-1)/2 \rfloor = \lceil (m-1)/2 \rceil = \lfloor m/2 \rfloor$ items. So after one iteration the new size is at most $\lfloor m/2 \rfloor$. By induction, after $k$ iterations the size is at most $\lfloor n/2^k \rfloor$, because $\lfloor \lfloor y \rfloor / 2 \rfloor = \lfloor y/2 \rfloor$ for each real $y \ge 0$. The loop runs an iteration only when the size is at least 1, and $\lfloor n/2^k \rfloor \ge 1$ exactly when $2^k \le n$, that is, when $k \le \lfloor \lg n \rfloor$. So iteration number $\lfloor \lg n \rfloor + 2$ never starts. A key larger than every item always takes the right part, of size exactly $\lfloor m/2 \rfloor$, so the sizes are exactly $\lfloor n/2^k \rfloor$ and all $\lfloor \lg n \rfloor + 1$ iterations run. $\square$

Each iteration does $O(1)$ work in the word RAM, so the worst-case time is $\Theta(\log n)$. For $n = 10^3$, $10^6$ and $10^9$ the bound is 10, 20 and 30 iterations, and a search for the key $10^6 + 1$ in the array $1, 2, \ldots, 10^6$ makes exactly 20.

The bound is optimal among algorithms that learn about the keys only by three-way comparisons. Such an algorithm is a [decision tree](/decision-tree-model/) in which the outcome "equal" ends the search, so it is in effect binary, and it needs a distinct leaf for each of the $n + 1$ gaps where an absent key can fall. A binary tree with $n + 1$ leaves has height at least $\lceil \lg(n+1) \rceil$, and $\lceil \lg(n+1) \rceil = \lfloor \lg n \rfloor + 1$ for each $n \ge 1$. Knuth (Volume 3, Section 6.2.1) gives this argument.

### Other shapes of logarithmic-time algorithms

**One root-to-leaf path in a balanced tree.** A binary tree of height $h$ has at most $2^{h+1} - 1$ nodes, so a tree with $n$ nodes has height at least $\lceil \lg(n+1) \rceil - 1$. A [binary heap](/binary-heap/) is a complete binary tree of height exactly $\lfloor \lg n \rfloor$. Insertion and deletion of the minimum move along one path, so each costs $O(\log n)$ in the worst case. A [balanced binary search tree](/balanced-binary-search-tree/) keeps its height $O(\log n)$ by its rebalancing rules, and then search, insertion and deletion cost $O(\log n)$ in the worst case. An unbalanced search tree has no such bound: its height can be $n - 1$.

**Shrinking a number by a constant factor.** [Modular exponentiation](/modular-exponentiation/) by repeated squaring reads the bits of the exponent $e$ one at a time. It makes $\lfloor \lg e \rfloor$ squarings and one extra multiplication for each 1-bit of $e$ after the first, so at most $2\lfloor \lg e \rfloor$ multiplications. In the [Euclidean algorithm](/euclidean-algorithm/), two steps at least halve the larger number: if $a \ge b$, then $a \bmod b < a/2$. So $\gcd(a, b)$ takes $O(\log a)$ division steps. Lamé's theorem gives the exact worst case, which consecutive [Fibonacci numbers](/fibonacci-numbers/) reach (Knuth, Volume 2, Section 4.5.3). For $a = F_{31} = 1346269$ and $b = F_{30} = 832040$ the algorithm makes 29 divisions.

**Counting digits.** A positive integer $N$ has $\lfloor \log_\beta N \rfloor + 1$ digits in base $\beta$, so a procedure that handles one digit in each step takes $\Theta(\log N)$ steps.

### When the input doubles

For the exact cost $\lg n$, $\lg(2n) = \lg n + 1$, so each doubling adds one step. For $T(n) = a \lg n + b$ each doubling adds $a$. The ratio $T(2n)/T(n)$ tends to 1. Going from $10^3$ to $10^6$ items multiplies the size by 1000, and $\lfloor \lg n \rfloor + 1$ only goes from 10 to 20.

### Pitfalls

- **Random access is required.** Binary search on a [linked list](/linked-list/) makes $O(\log n)$ comparisons, but it must walk to each middle node. Even when each walk starts at the first node of the current interval, the walks take $n/2 + n/4 + \cdots$ steps, which is $\Theta(n)$. On a Turing machine with one tape the same problem appears: moving the head to the middle takes time proportional to the distance.
- **The input must be sorted or structured.** Binary search on an unsorted array gives wrong answers, not only slow ones. Sorting first costs $\Theta(n \log n)$ comparisons, so a single search on unsorted data is cheaper with [linear search](/linear-search/). The logarithmic bound pays off when the sort is done once and many searches follow.
- **The lower bound belongs to the comparison model.** The $\lceil \lg(n+1) \rceil$ bound counts comparisons. An algorithm that computes with the values of the keys is not bound by it. [Interpolation search](/interpolation-search/) on keys drawn uniformly at random takes $O(\log \log n)$ probes in expectation, and $\Theta(n)$ in the worst case (Knuth, Volume 3, Section 6.2.1).
- **Logarithmic in the value is not logarithmic in the input size.** The input of "compute $b^e \bmod m$" holds $e$ in about $\lg e$ bits. A cost of $O(\log e)$ multiplications is therefore linear in the length of $e$, not logarithmic. The same holds for Euclid's algorithm: $O(\log a)$ divisions is linear in the number of bits of $a$. Each division on numbers of $\beta$ bits costs $O(\beta^2)$ bit operations with the school method, so the bit cost of Euclid's algorithm is $O(\beta^3)$ by this count, which is polynomial in the input size. See [input size](/input-size/).
- **Unit cost needs bounded numbers.** Repeated squaring without the reduction modulo $m$ makes numbers that double in length at each step: 10 squarings of 2 give a number of 1025 bits. Counting each multiplication as one step is then false. With the reduction, the numbers stay below $m$, and each step is $O(1)$ when $m$ fits in a word. See [unit-cost model](/unit-cost-model/).
- **Hidden cost of a comparison.** A comparison is one step only when a key fits in a word. For strings of length $m$, a search in a balanced tree costs $O(m \log n)$ character comparisons in the worst case.
- **Amortized and expected claims.** A bound can be logarithmic only amortized, as for a [splay tree](/splay-tree/), or in expectation, as for a [skip list](/skip-list/). Name the case.

## Examples

- Binary search in a sorted array of $10^6$ items: at most 20 iterations, and exactly 20 for a key above all items.
- Insert into a binary heap that holds $10^6$ items: the height is $\lfloor \lg 10^6 \rfloor = 19$, so the sift-up moves at most 19 levels.
- Compute $3^{1000} \bmod 1009$ by repeated squaring. Since $1000 = 1111101000_2$ has ten bits and six 1-bits, the method makes 9 squarings and 5 extra multiplications. The result is 404.
- $\gcd(1346269, 832040)$ by Euclid's algorithm: 29 divisions, for numbers of 21 and 20 bits.
- Non-example: binary search on a linked list of $n$ items, which takes $\Theta(n)$ pointer steps.
- Non-example: find an item in an unsorted array. Any algorithm must read all $n$ items in the worst case, so the time is [linear](/linear-time/).
- Non-example: an algorithm that halves the input but also scans it at each step. At the stage of size $m$ it reads $m$ items, so the total is $n + n/2 + n/4 + \cdots < 2n$, which is $\Theta(n)$.

## Where it is used

Logarithmic time is the cost of one operation in ordered structures: the [binary heap](/binary-heap/), the [balanced binary search tree](/balanced-binary-search-tree/), and the [Fenwick tree](/fenwick-tree/) and [segment tree](/segment-tree/) for range queries. Repeating such an operation $n$ times gives [linearithmic time](/linearithmic-time/): even when the structure grows from 1 to $n$ items, the sum $\lg 1 + \lg 2 + \cdots + \lg n = \lg(n!)$ is $\Theta(n \log n)$. A cost that is a power of $\log n$ is [polylogarithmic](/polylogarithmic-time/). Number theory uses the same shape for the gcd, for modular powers and for the binary representation of numbers. See the table of the [common growth rates](/common-growth-rates/).

## References
