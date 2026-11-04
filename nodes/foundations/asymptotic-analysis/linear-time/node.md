---
tag: RTN7JH
kind: concept
slug: linear-time
name: Linear time
area: foundations/asymptotic-analysis
level: intro
summary: Running time that grows in direct proportion to input size, typical of algorithms that process each input element a constant number of times.
prereqs: [asymptotic-notation, time-complexity, input-size]
see_also: [common-growth-rates, constant-time, linearithmic-time, quadratic-time, sublinear-time, doubling-hypothesis, two-pointers, linear-search]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 2 and Chapter 3
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11.1
---

An algorithm runs in linear time when its running time is $T(n) = \Theta(n)$ for an input of size $n$, or $O(n)$ when only an upper bound is known. The cost is proportional to the size of the input, up to a constant factor. Many basic tasks reach this class, and it is the lowest class for a problem whose answer depends on each item of the input.

## In plain words

Reading a book once from the first page to the last is linear work. A book with twice as many pages takes about twice as long. You touch each page a fixed number of times, and the time follows the number of pages.

Most simple loops over a list are of this kind: add the numbers, find the largest one, count how many are negative. The work for one item does not depend on how many items there are.

A linear algorithm does not need to be a single loop. Two loops one after the other are linear. A loop inside a loop can also be linear, if the inner loop does less work in total than it seems. But a loop inside a loop where both run over the whole input is quadratic, not linear.

## The idea

### Definition

Fix a model and a case, and let $T(n)$ be the cost. The algorithm runs in linear time when $T(n) = O(n)$. The bound is tight when $T(n) = \Theta(n)$, that is, when there are $c_1, c_2 > 0$ and $n_0$ with $c_1 n \le T(n) \le c_2 n$ for all $n \ge n_0$. For a problem with several size parameters, "linear" means linear in their sum, for example $\Theta(n + m)$ for a graph with $n$ vertices and $m$ edges. See [multivariate asymptotic notation](/multivariate-asymptotic-notation/).

### Shapes of linear-time algorithms

**One pass over the input.** [Linear search](/linear-search/) in an unsorted array of $n$ items makes at most $n$ comparisons. Finding the maximum of $n$ items makes exactly $n - 1$ comparisons, and no comparison algorithm does better. Proof of the lower bound: build a graph on the items with an edge for each comparison the algorithm makes. Suppose the algorithm makes fewer than $n - 1$ comparisons on some input, and let $x$ be the item that it reports. The graph is not connected, so some component $C$ does not contain $x$. Raise every item of $C$ by the same amount, large enough that some item of $C$ is now above $x$. Each comparison inside $C$ or outside $C$ gives the same result, and no comparison joins $C$ to the rest. The algorithm sees the same results, so it asks the same questions and reports $x$ again, but $x$ is not the maximum now. So at least $n - 1$ comparisons are needed in the worst case. This shows the time is $\Theta(n)$ in the comparison model.

**Merging.** Merging two sorted lists of $a$ and $b$ items, with $a + b \ge 1$, makes at most $a + b - 1$ comparisons, because each comparison puts one item in its final place, and when one list is empty the rest are copied without comparisons. The merge step of [merge sort](/merge-sort/) is linear in this way.

**Two pointers and windows.** The loops of [two pointers](/two-pointers/) and [sliding window](/sliding-window/) have a nested look, but each pointer only moves forward. If each of two pointers makes at most $n$ moves, and each iteration of the loop moves at least one pointer, then there are at most $2n$ iterations of $O(1)$ work each. The bound is a count of moves, not of the nesting of loops.

**Traversal of a structure.** [Breadth-first search](/breadth-first-search/) on a graph with $n$ vertices and $m$ edges, in adjacency lists, visits each vertex once and looks at each edge a constant number of times, so it runs in $\Theta(n + m)$. A tree traversal visits each node once.

**Linear in the size of the input and of the range.** [Counting sort](/counting-sort/) of $n$ integers in the range $0$ to $k - 1$ runs in $\Theta(n + k)$. This is linear when $k = O(n)$, and it is not a comparison sort, so the lower bound for comparison sorting does not apply. See [linearithmic time](/linearithmic-time/).

**Dividing a linear cost.** A recursion that does linear work and then continues on a constant fraction of the input is linear in total. For example, with $T(n) = T(n/2) + n$ (and $T(1) = 1$ for $n$ a power of two), $T(n) = n + n/2 + \cdots + 1 = 2n - 1$. The sum is a [geometric series](/geometric-series/).

### When the input doubles

If $T(n) \sim a n$ (see [tilde notation](/tilde-notation/)), then $T(2n)/T(n) \to 2$. For $T(n) = \Theta(n)$ alone, the ratio $T(2n)/T(n)$ only stays between two positive constants, and the claim "twice as slow" needs the stronger form. The [doubling hypothesis](/doubling-hypothesis/) uses the ratio in experiments, where a ratio near 2 points to linear growth. A linear algorithm on a machine ten times faster handles an input ten times larger in the same time.

### Pitfalls

- **Linear in what.** The size is the number of bits or symbols of the input, see [input size](/input-size/). Trial division of a number $N$ takes $O(\sqrt{N})$ steps. That is sublinear in the value $N$ but exponential in the number of bits of $N$. A loop "for $i$ from 1 to $N$" is linear in the value and exponential in the input size.
- **Hidden linear operations.** A call that looks like one step can cost $\Theta(n)$: insert at the front of an array, test membership in a list, take the length of a linked list that has no stored length, copy a slice, or append to an immutable string. Such a call inside a loop makes the loop quadratic. Building a string of length $n$ by $n$ appends of one character to a string that is copied each time costs $1 + 2 + \cdots + n = \Theta(n^2)$.
- **Nested loops that are not quadratic, and the converse.** The nesting does not decide the class. Count the total work. The pointer loops above are linear. A loop over the items with an inner loop over a growing prefix is quadratic.
- **Amortized or expected linear.** Building a hash set of $n$ items is linear in expectation, not in the worst case. Appending $n$ items to a [dynamic array](/dynamic-array/) is linear in total, but one append can cost $\Theta(n)$.
- **Linear is not the floor for each problem.** An algorithm can be [sublinear](/sublinear-time/) when a precondition on the input lets one probe rule out many items, or when the answer depends on only part of the input. Binary search on a sorted array is an example of the first kind.
- **Constants.** Two linear algorithms can differ by a large factor. A pass that does a cache miss for each item can be much slower than a pass over contiguous memory.

## Examples

- Sum of an array of $n$ numbers: $n - 1$ additions, so $\Theta(n)$.
- Maximum of an array: exactly $n - 1$ comparisons in each case, so $\Theta(n)$, and this is optimal in the comparison model by the argument above.
- Reverse an array in place: $\lfloor n/2 \rfloor$ swaps.
- Merge two sorted arrays of $5$ and $7$ items: at most $11$ comparisons.
- Longest run of equal items, with one pass and one counter: $n - 1$ comparisons of neighbors.
- Non-example: find the maximum by comparing each pair of items. This makes $n(n-1)/2$ comparisons, so it is [quadratic](/quadratic-time/) although the problem is linear.
- Non-example: [insertion sort](/insertion-sort/) is linear on an already sorted input and quadratic in the worst case. Its best case is $\Theta(n)$ and its worst case is $\Theta(n^2)$, so it is not linear without a case.

## Where it is used

Linear time is the target for scanning, counting, filtering and many parsing tasks, and for the preprocessing step before a faster query structure. A problem is said to be solved in "optimal" time when an upper bound of $O(n)$ meets the lower bound of $\Omega(n)$ that comes from reading the input, see [asymptotic optimality](/asymptotic-optimality/). Sorting by comparisons is the main example of a task that does not reach linear time; it needs [linearithmic time](/linearithmic-time/). See the table of the [common growth rates](/common-growth-rates/).

## References
