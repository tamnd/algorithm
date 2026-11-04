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
    locator: Section 1.4, Analysis of Algorithms (order-of-growth classifications); Section 1.3 (resizing arrays)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11.1, The O-notation
  - paper: doi:10.1145/828.1884
    title: Michael L. Fredman, János Komlós and Endre Szemerédi, Storing a sparse table with O(1) worst case access time, Journal of the ACM 31(3), 538 to 544 (1984)
    locator: the two-level perfect hashing scheme
  - paper: doi:10.1016/j.jalgor.2003.12.002
    title: Rasmus Pagh and Flemming Friche Rodler, Cuckoo hashing, Journal of Algorithms 51(2), 122 to 144 (2004)
    locator: lookup with at most two probes
---

An algorithm or an operation runs in constant time when its cost $T(n)$ is bounded by a constant that does not depend on the [input size](/input-size/) $n$. In [asymptotic notation](/asymptotic-notation/) this is $T(n) = O(1)$. It is the lowest class of the [common growth rates](/common-growth-rates/). A claim of constant time is only meaningful with a stated model of computation, such as the [word RAM](/word-ram/), and a stated case: worst, expected or amortized.

## In plain words

A constant-time operation takes about the same time on a small input and on a huge one. Reading the first item of a list is an example. The list can have ten items or ten billion, and the work is the same: go to the first place and read it.

This does not mean the operation is fast. A step that takes one hour on each input is a constant-time step.

An algorithm that runs in constant time cannot look at every item of a large input, because looking at each item takes more time when there are more items. So it must use a structure that tells it where to look, such as an array index or a hash value. It also depends on the machine: one step on a number is only one step when the number fits in a machine word.

## The idea

### Definition

Fix a cost model, for example the [word RAM](/word-ram/) with unit cost for each basic operation on a word of $w$ bits, and fix a case: worst, expected or amortized. Let $T(n)$ be the cost of the algorithm in that model and case on inputs of size $n$. The algorithm runs in constant time when

$$\exists c > 0 \ \exists n_0 \ \forall n \ge n_0 : \ T(n) \le c.$$

This is $T(n) = O(1)$. A real algorithm takes at least one step on each input, so $T(n) \ge 1$, and then $O(1)$ and $\Theta(1)$ say the same thing. For an operation on a data structure, $n$ is the number of items in the structure, and the bound must hold for each $n$.

The word RAM assumes $w \ge \lg n$, so that one word holds an index into the input. Without this assumption, reading `A[i]` for an index $i$ of $\lceil \lg n \rceil$ bits cannot be one step for every $n$. See [transdichotomous model](/transdichotomous-model/).

### Shapes of constant-time operations

- **Direct access.** Reading or writing `A[i]` in an [array](/array/) costs one address computation and one memory access in the word RAM, so it is worst-case $\Theta(1)$.
- **Arithmetic and bit operations on words.** Addition, comparison, shifts and bit operations on integers of $w$ bits each take one step. For example, $x$ is a power of 2 exactly when $x > 0$ and $x \mathbin{\&} (x - 1) = 0$, because subtracting 1 clears the lowest 1-bit and sets the bits below it. For $x = 40 = 101000_2$ the test gives $32$, so 40 is not a power of 2. For $x = 64$ it gives 0.
- **Fixed-size pieces of a structure.** [Push and pop](/stack/) on a stack in an array with free space, enqueue and dequeue on a [queue](/queue/) in a circular buffer, and insertion after a known node of a [linked list](/linked-list/) each change a fixed number of fields.
- **Queries after preprocessing.** After $O(n)$ preprocessing, [prefix sums](/prefix-sums/) answer the sum of any range $A[i \ldots j]$ as $P[j+1] - P[i]$ in worst-case $O(1)$ time. A [sparse table](/sparse-table/) answers a [range minimum query](/range-minimum-query/) in worst-case $O(1)$ time after $O(n \log n)$ preprocessing.

### Amortized constant time: the doubling array

Appending to a [dynamic array](/dynamic-array/) that doubles its capacity when it is full costs $O(1)$ amortized. Start with capacity 1 and append $n \ge 2$ items. Item number $s + 1$ causes a copy of $s$ items exactly when the array is full with $s$ items, and the capacity is always a power of 2. So the copies happen at sizes $1, 2, 4, \ldots, 2^k$, where $k$ is the largest integer with $2^k \le n - 1$. These copies move

$$1 + 2 + \cdots + 2^k = 2^{k+1} - 1 \le 2(n-1) - 1 < 2n$$

items. Together with the $n$ writes of the new items, the total is less than $3n$ writes, so the amortized cost of one append is less than 3 writes. For $n = 10^6$, $k = 19$, the copies move $2^{20} - 1 = 1048575$ items, and the total is $2048575$ writes, about $2.05$ for each append.

The growth factor is essential. If the capacity grows by a fixed amount instead, say by 1000 slots from a start of 1000, then $10^6$ appends copy $1000 + 2000 + \cdots + 999000 = 499500000$ items, about 500 for each append. In general $n$ appends then copy $\Theta(n^2)$ items, so one append costs $\Theta(n)$ amortized. See [array doubling](/array-doubling/).

### Expected and worst-case constant time for dictionaries

A lookup in a [hash table](/hash-table/) with chaining, a hash function drawn from a universal family, and a load factor bounded by a constant, costs $O(1)$ in expectation over the choice of the hash function, for each fixed set of keys. The worst case over the choice is $\Theta(n)$: all keys can fall in one bucket. Two schemes give worst-case $O(1)$ lookups. The static [perfect hashing](/perfect-hashing/) of Fredman, Komlós and Szemerédi (1984) stores a fixed set of $n$ keys in $O(n)$ space with two levels of hash tables. [Cuckoo hashing](/cuckoo-hashing/) (Pagh and Rodler, 2004) keeps each key in one of two cells, so a lookup reads at most two cells. Its insertions are expected amortized $O(1)$, not worst case.

### When the input doubles

If $T(n) = \Theta(1)$, then $T(2n)/T(n)$ stays between two positive constants, and for an operation with a fixed instruction count it is 1. On a real machine the measured ratio can be well above 1 when doubling $n$ pushes the data out of a cache level or out of the TLB. The word RAM does not model this. See [cache-oblivious model](/cache-oblivious-model/) and [external-memory model](/external-memory-model/) for models that do.

### Pitfalls

- **Amortized is not worst case.** A doubling array append has amortized cost $O(1)$ but worst-case cost $\Theta(n)$. A real-time system that needs a hard bound for each operation cannot use the amortized claim. Incremental resizing, which moves a few old items on each append, gives worst-case $O(1)$ appends, if the allocation of an uninitialized block takes $O(1)$ time. See [amortized vs worst case](/amortized-vs-worst-case/).
- **Expected is not worst case.** The $O(1)$ bound for hashing with chaining is an expectation over the random hash function, under a bounded load factor. A fixed hash function and an adversary who picks the keys give $\Theta(n)$ for each lookup. See [amortized vs expected cost](/amortized-vs-expected-cost/).
- **The word size is part of the model.** Adding two integers is one step only when each fits in one word. Adding two numbers of $b$ bits takes $\Theta(\lceil b/w \rceil)$ word operations. A big-integer operation, a string comparison or the copy of a slice is not $O(1)$ in general. A hash table lookup with a key of $m$ words costs $\Theta(m)$ to hash the key and to compare it.
- **Unit cost for unbounded numbers is not a fair model.** A RAM that multiplies integers of any size in one step can compute $2^{2^k}$ with $k$ squarings, a number with $2^k + 1$ bits. After 10 squarings of 2 the result has 1025 bits. A constant number of such steps can do the work of very long computations, so a claim of constant time in that model says little. See [unit-cost model](/unit-cost-model/) and [logarithmic-cost model](/logarithmic-cost-model/).
- **Allocation and initialization.** Allocating an array of $n$ cells is often counted as one step, but filling it with zeros takes $\Theta(n)$ writes. An algorithm that allocates a fresh zeroed table in each call is not constant time.
- **The measure of input size.** "Test whether $N$ is even" is $O(1)$: read the lowest bit. "Test whether $N$ is prime" is not, although the input is one number: its size is the number of bits of $N$. A claim of $O(1)$ for an operation on a number holds only while the number fits in one word. See [input size](/input-size/).
- **A large constant is still constant.** A step that costs $10^9$ operations on every input is $\Theta(1)$. The notation does not say which of two constant-time operations is faster.
- **The word in cryptography.** In cryptography, "constant-time code" means code whose running time does not depend on secret values, as a defense against a [timing attack](/timing-attack/). A constant-time comparison of two strings of $n$ bytes in this sense takes $\Theta(n)$ time.
- **Fixed-size inputs.** Every algorithm is $O(1)$ on a set of inputs with bounded size, such as a chess position on a board of fixed size. The class is only meaningful when $n$ can grow.
- **No time for the whole input.** An algorithm that runs in $O(1)$ time reads only $O(1)$ cells of the input. It cannot compute a function that depends on all $n$ items, such as the sum of an array. This is the extreme case of [sublinear time](/sublinear-time/).

## Examples

- Read `A[i]` for a given index $i$ in an array: worst-case $\Theta(1)$ in the word RAM.
- Test whether a word $x$ is a power of 2 with $x \mathbin{\&} (x-1)$: worst-case $\Theta(1)$. For $x = 40$ the result is 32, and for $x = 64$ it is 0.
- Push onto a stack held in a doubling array: amortized $O(1)$, with fewer than $3n$ writes for $n$ pushes, and worst-case $\Theta(n)$ for the one push that resizes.
- The sum of $A[i \ldots j]$ from a prefix-sum array: two reads and one subtraction, worst case, after $\Theta(n)$ preprocessing.
- Look up a key in a hash table: expected $O(1)$ with chaining and a universal hash family, worst-case $\Theta(n)$ for chaining, worst-case $O(1)$ with static perfect hashing or with cuckoo hashing.
- Non-example: find the maximum of an unsorted array. The answer depends on each item, so the time is $\Omega(n)$. See [linear time](/linear-time/).
- Non-example: look up a key in a sorted array by [binary search](/binary-search/). The cost grows by one comparison each time the size doubles, so it is [logarithmic](/logarithmic-time/), not constant.
- Non-example: add two integers of $n$ bits stored as arrays of bits. The time is $\Theta(n)$ bit operations, or $\Theta(\lceil n/w \rceil)$ word operations.

## Where it is used

Constant-time operations are the unit of cost in the [word RAM](/word-ram/) and in the [random-access machine](/random-access-machine/), and the analysis of each algorithm counts them. A data structure page gives the cost of each operation, and the best result is worst-case $O(1)$ for each operation. When that is not possible, the page gives an amortized or an expected bound and says so. Graph algorithms number the vertices 0 to $n - 1$ and keep a boolean array to test membership in worst-case $O(1)$ time. They use a hash set, with expected $O(1)$ time, only when the vertex labels are not small integers.

## References
