---
tag: QAKMJW
kind: concept
slug: constant-time
name: Constant time
aliases:
- O(1) time
area: foundations/asymptotic-analysis
level: intro
summary: Running time that does not grow with input size.
prereqs: [asymptotic-notation, time-complexity]
see_also: [common-growth-rates, logarithmic-time, linear-time, sublinear-time, word-ram, amortized-vs-worst-case, amortized-vs-expected-cost, hash-table]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2 (the RAM model), Chapter 11 (hash tables) and Section 16.4 (dynamic tables)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11.1
  - paper: "Michael L. Fredman, János Komlós and Endre Szemerédi, Storing a sparse table with O(1) worst case access time, Journal of the ACM 31 (1984)"
    locator: the two-level perfect hashing scheme
  - paper: "Rasmus Pagh and Flemming Friche Rodler, Cuckoo hashing, Journal of Algorithms 51 (2004)"
    locator: worst-case constant lookup time
---

An algorithm runs in constant time when its running time $T(n)$ is bounded by a constant that does not depend on the input size $n$. In the notation of [asymptotic notation](/asymptotic-notation/), this is $T(n) = O(1)$. It is the lowest class in the [common growth rates](/common-growth-rates/).

## In plain words

A constant-time operation takes about the same time on a small input and on a huge one. Reading the first item of a list is an example. The list can have ten items or ten billion, and the work is the same: go to the first place and read it.

This does not mean the operation is fast. It means that the cost does not grow with the size of the input. A step that takes one hour is a constant-time step, if it takes one hour for each input.

An algorithm that runs in constant time cannot look at every item of a large input, because looking at each item takes more time when there are more items. So it must use a structure that tells it where to look, such as an array index or a hash value.

## The idea

### Definition

Fix a cost model, for example the [word RAM](/word-ram/) with unit cost for each basic operation on a word, and fix a case: worst, average, expected or amortized. Let $T(n)$ be the cost of the algorithm in that model and case on inputs of size $n$ (see [input size](/input-size/)). The algorithm runs in constant time when

$$\exists c > 0 \ \exists n_0 \ \forall n \ge n_0 : \ T(n) \le c.$$

This is $T(n) = O(1)$. When $T(n) \ge c' > 0$ also holds for all large $n$, then $T(n) = \Theta(1)$. A running time is at least one step on each input, so for a real algorithm $O(1)$ and $\Theta(1)$ say the same thing. A bound $O(1)$ always needs its case. "Worst-case $O(1)$" is a statement about each input. "Amortized $O(1)$" is a statement about a sequence of operations.

### Shapes of constant-time operations

- **Direct access.** Reading or writing `A[i]` in an [array](/array/) costs one address computation and one memory access in the word RAM, so it is worst-case $\Theta(1)$.
- **Arithmetic on words.** Addition, comparison and bit operations on integers of $w$ bits take one step when the word size is $w$. See the pitfalls below for the limit of this rule.
- **Fixed-size pieces of a structure.** [Push and pop](/stack/) on a stack in an array with free space, enqueue and dequeue on a [queue](/queue/) in a circular buffer, and insertion after a known node of a [linked list](/linked-list/) each change a fixed number of fields.
- **Amortized constant time.** Appending to a [dynamic array](/dynamic-array/) that doubles its capacity when it is full costs $O(1)$ amortized. Start with capacity 1 and append $n$ items. For $n \ge 2$, a copy happens when the array is full, at sizes $1, 2, 4, \dots, 2^k$, where $k$ is the largest integer with $2^k \le n - 1$. For $n = 1$ there is no copy. These copies move $1 + 2 + \cdots + 2^k = 2^{k+1} - 1 < 2n$ items. Together with the $n$ writes of the new items, the total is less than $3n$, so the amortized cost of one append is less than 3 writes. A single append that triggers a copy still costs $\Theta(n)$. See [array doubling](/array-doubling/) and [amortized vs worst case](/amortized-vs-worst-case/).
- **Expected constant time.** A lookup in a [hash table](/hash-table/) with a good hash function and a bounded load factor costs $O(1)$ in expectation. See the pitfalls below.

### When the input doubles

If $T(n) = \Theta(1)$, then $T(2n) = \Theta(1)$: the cost stays within the same constant bounds. The ratio $T(2n)/T(n)$ stays between two positive constants, and in experiments it is usually close to 1. On a real machine the measured ratio can be well above 1 when doubling $n$ pushes the data out of a cache level (L1, L2, L3 or the TLB). This happens at large $n$, for example at millions of items, and the word RAM does not model it.

### Pitfalls

- **Amortized is not worst case.** A dynamic array append has amortized cost $O(1)$ but worst-case cost $\Theta(n)$. A real-time system that needs a hard bound for each operation cannot use the amortized claim. Incremental resizing, which moves a few old items on each append, gives worst-case $O(1)$ appends, if allocating an uninitialized block takes $O(1)$ time. See [amortized vs worst case](/amortized-vs-worst-case/).
- **Expected is not worst case.** A hash table lookup is $O(1)$ in expectation over the random choice of the hash function (or over a random input), under the assumption that the load factor is bounded. If all keys fall in one bucket and the bucket is a list, one lookup takes $\Theta(n)$. [Perfect hashing](/perfect-hashing/) (Fredman, Komlós and Szemerédi, 1984) for a static set, and [cuckoo hashing](/cuckoo-hashing/), look up a key in worst-case $O(1)$. See [amortized vs expected cost](/amortized-vs-expected-cost/).
- **The word size is part of the model.** Adding two integers is one step only when each fits in one word. Adding two numbers of $n$ bits takes $\Theta(\lceil n/w \rceil)$ word operations. A big-integer library, a string comparison or copying a slice is not $O(1)$ in general. The same is true for a hash table lookup with a key of $m$ words: hashing the key and comparing it with a stored key each cost $\Theta(m)$.
- **A large constant is still constant.** A step that costs $10^9$ operations on every input is $\Theta(1)$. The notation does not say which of two constant-time operations is faster. Memory access costs differ by a large factor between cache and main memory, and the word RAM does not model this.
- **The word in cryptography.** In cryptography, "constant-time code" means code whose running time does not depend on secret values, as a defense against a [timing attack](/timing-attack/). A constant-time comparison of two strings of $n$ bytes still takes $\Theta(n)$ time.
- **Fixed-size inputs.** Every algorithm is $O(1)$ on a set of inputs with bounded size. The class is only meaningful when $n$ can grow.
- **No time for the whole input.** An algorithm that runs in $O(1)$ time reads only $O(1)$ items of the input. It cannot compute a function that depends on all $n$ items, such as the sum of an array. This is the extreme case of [sublinear time](/sublinear-time/).

## Examples

- Read `A[i]` for a given index $i$ in an array: worst-case $\Theta(1)$.
- Test whether an integer in a machine word is even, by testing its lowest bit: worst-case $\Theta(1)$.
- Push onto a stack held in an array that has free space: worst-case $\Theta(1)$. When the array is full and must grow, that one push costs $\Theta(n)$. If the capacity grows by a constant factor, for example by doubling, the push is amortized $O(1)$. If it grows by a fixed amount, $n$ pushes cost $\Theta(n^2)$ in total, so one push is amortized $\Theta(n)$.
- Look up a key in a hash table: expected $O(1)$, worst case $\Theta(n)$ for a table with chaining, worst case $O(1)$ with static perfect hashing or cuckoo hashing.
- Non-example: find the maximum of an unsorted array. The answer depends on each item, so the time is $\Omega(n)$. See [linear time](/linear-time/).
- Non-example: look up a key in a sorted array by [binary search](/binary-search/). The cost grows by one comparison each time the size doubles, so it is [logarithmic](/logarithmic-time/), not constant.

## Where it is used

Constant-time operations are the unit of cost in the [word RAM](/word-ram/) and in the [random access machine](/random-access-machine/), and the analysis of each algorithm counts them. A data structure page gives the cost of each operation, and the best result is worst-case $O(1)$ for each operation. When that is not possible, the page gives an amortized or an expected bound and says so. Typical constant-time queries after preprocessing are a range sum from [prefix sums](/prefix-sums/) after $O(n)$ preprocessing, and a [range minimum query](/range-minimum-query/) with a [sparse table](/sparse-table/) after $O(n \log n)$ preprocessing. Graph algorithms number the vertices 0 to $n - 1$ and test membership in a boolean array in worst-case $O(1)$ time. They use a hash set, with expected $O(1)$ time, only when the vertex labels are not small integers.

## References
