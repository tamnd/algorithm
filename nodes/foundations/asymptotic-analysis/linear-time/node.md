---
tag: RTN7JH
kind: concept
slug: linear-time
name: Linear time
area: foundations/asymptotic-analysis
level: intro
summary: Running time that grows in direct proportion to input size, typical of algorithms that process each input element a constant number of times.
prereqs: [asymptotic-notation, time-complexity, input-size]
see_also: [common-growth-rates, constant-time, linearithmic-time, quadratic-time, sublinear-time, doubling-hypothesis, two-pointers, median-of-medians]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.2 (counting sort), Section 9.1 (minimum and maximum), Section 9.3 (selection in worst-case linear time) and Section 32.4 (the Knuth-Morris-Pratt algorithm)
  - paper: doi:10.1016/S0022-0000(73)80033-9
    title: Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest and Robert E. Tarjan, Time bounds for selection, Journal of Computer and System Sciences 7(4), 448 to 461 (1973)
    locator: the linear-time selection algorithm
  - paper: doi:10.1137/0206024
    title: Donald E. Knuth, James H. Morris and Vaughan R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2), 323 to 350 (1977)
    locator: the linear bound on the number of comparisons
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms (order-of-growth classifications and the doubling ratio)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11.1, The O-notation
---

An algorithm runs in linear time when its cost is $T(n) = \Theta(n)$ for an [input size](/input-size/) $n$, or $O(n)$ when only an upper bound is known. The cost is proportional to the size of the input, up to a constant factor. It is the lowest possible class for a problem whose answer depends on every item of the input, because each item must be read. Scanning, merging, counting, graph traversal, string matching with the [Knuth-Morris-Pratt algorithm](/knuth-morris-pratt/) and selection with [median of medians](/median-of-medians/) all reach it.

## In plain words

Reading a book once from the first page to the last is linear work. A book with twice as many pages takes about twice as long. You touch each page a fixed number of times, and the time follows the number of pages.

Most simple loops over a list are of this kind: add the numbers, find the largest one, count how many are negative. The work for one item does not depend on how many items there are.

A linear algorithm does not need to be a single loop. Two loops one after the other are linear. A loop inside a loop can also be linear, when the inner loop does little work in total. But a loop inside a loop where both run over the whole input is quadratic, not linear. To decide, count the total work, not the number of loops.

## The idea

### Definition

Fix a model and a case, and let $T(n)$ be the cost. The algorithm runs in linear time when $T(n) = O(n)$. The bound is tight when $T(n) = \Theta(n)$, that is, when there are $c_1, c_2 > 0$ and $n_0$ with $c_1 n \le T(n) \le c_2 n$ for all $n \ge n_0$. For a problem with several size parameters, "linear" means linear in the total size of the input, for example $\Theta(V + E)$ for a graph with $V$ vertices and $E$ edges in adjacency lists. See [multivariate asymptotic notation](/multivariate-asymptotic-notation/).

### Why linear is the floor when every item matters

If an algorithm reads fewer than $n$ cells of an input of $n$ cells, there is a cell it never reads, and two inputs that differ only in that cell get the same output. So a function that changes when any single item changes, such as the sum, the maximum or the test "does the array contain a 1", needs $n$ reads and $\Omega(n)$ time. The proof in full, for deterministic and randomized algorithms, is on the page of [sublinear time](/sublinear-time/).

### Shapes of linear-time algorithms

**One pass.** Finding the maximum of $n$ items with a scan makes exactly $n - 1$ comparisons, and no comparison algorithm does better in the worst case. *Proof of the lower bound.* Build a graph on the items with an edge for each comparison that the algorithm makes. Suppose that on some input of distinct items it makes fewer than $n - 1$ comparisons, and reports item $x$. A graph with $n$ vertices and fewer than $n - 1$ edges is not connected, so some component $C$ does not contain $x$. Add the same large amount to each item of $C$, so that the largest item of $C$ exceeds $x$. A comparison inside $C$ or outside $C$ has the same outcome as before, and no comparison joins $C$ to the rest. So the algorithm sees the same outcomes, makes the same comparisons, and reports $x$ again, which is now wrong. $\square$ (CLRS, Section 9.1.)

**Merging.** Merging two sorted lists of $a$ and $b$ items, with $a + b \ge 1$, makes at most $a + b - 1$ comparisons, because each comparison moves one item to its final place, and when one list is empty the rest is copied with no comparison. The merge step of [merge sort](/merge-sort/) is linear in this way.

**Pointers that only move forward.** The loops of [two pointers](/two-pointers/) and [sliding window](/sliding-window/) look nested, but each pointer only moves forward. If each of two pointers makes at most $n$ moves, and each iteration moves at least one pointer, there are at most $2n$ iterations. The [Knuth-Morris-Pratt algorithm](/knuth-morris-pratt/) uses the same count. After it has built the failure function of a pattern of length $m$ in $O(m)$ time, it scans a text of length $n$. Each comparison either moves the text pointer forward (on a match, or on a mismatch with an empty current match) or shortens the current match (on a mismatch). The text pointer moves $n$ times, and the current match grows by one at most $n$ times, so it shrinks at most $n$ times. So the scan makes at most $2n$ comparisons (Knuth, Morris and Pratt, 1977).

**Traversal.** [Breadth-first search](/breadth-first-search/) on a graph in adjacency lists puts each vertex in the queue at most once and reads each adjacency list at most once, so it runs in $O(V + E)$ time.

**Linear in the size and in the range.** [Counting sort](/counting-sort/) of $n$ integers in the range $0$ to $k - 1$ runs in $\Theta(n + k)$ time. This is linear when $k = O(n)$. It is not a comparison sort, so the $\Omega(n \log n)$ bound for comparison sorting does not apply.

**A shrinking recursion.** A recursion that does linear work and then continues on a constant fraction of the input is linear in total. With $T(n) = T(n/2) + n$ and $T(1) = 1$, for $n$ a power of 2, $T(n) = n + n/2 + \cdots + 1 = 2n - 1$, a [geometric series](/geometric-series/).

### Worked example: selection in worst-case linear time

The [median of medians](/median-of-medians/) algorithm of Blum, Floyd, Pratt, Rivest and Tarjan (1973) finds the $i$-th smallest of $n$ items. It splits the items into groups of 5, takes the median of each group, finds the median $p$ of these medians by a recursive call, partitions around $p$, and recurses on the one side that holds the answer. At least half of the $\lceil n/5 \rceil$ groups have a median $\ge p$, and each such group, except possibly the group of $p$ and a last short group, gives three items $\ge p$. So about $3n/10$ items are $\ge p$, and the same number are $\le p$, and the recursive call on one side has at most about $7n/10$ items. The exact form, with the rounding, is $T(n) \le T(\lceil n/5 \rceil) + T(7n/10 + 6) + O(n)$ (CLRS, Section 9.3).

*Lemma.* Let $a, b > 0$ with $a + b < 1$, $d > 0$, and let $T(n) \le T(\lfloor an \rfloor) + T(\lfloor bn \rfloor) + dn$ for $n \ge 1$, with $T(0) = 0$. Then $T(n) \le dn/(1 - a - b)$ for each $n \ge 0$.

*Proof.* By strong induction on $n$. For $n = 0$ both sides are 0. For $n \ge 1$, $\lfloor an \rfloor < n$ and $\lfloor bn \rfloor < n$ because $a, b < 1$, so the hypothesis gives $T(n) \le \frac{d}{1-a-b}(an + bn) + dn = \frac{d\,n\,(a + b + 1 - a - b)}{1-a-b} = \frac{dn}{1-a-b}$. $\square$

With $a = 1/5$ and $b = 7/10$, $a + b = 9/10$ and the bound is $10\,dn$. The rounding terms of the exact recurrence change only the constant, as CLRS shows. The key fact is that the two parts together hold a fraction $9/10 < 1$ of the input. With groups of 3 in place of 5, the fractions are $1/3$ and $2/3$, which sum to 1, and the argument gives only $O(n \log n)$.

### When the input doubles

If $T(n) \sim a n$ (see [tilde notation](/tilde-notation/)), then $T(2n)/T(n) \to 2$. For $T(n) = \Theta(n)$ alone, the ratio only stays between two positive constants, so the claim "twice as slow" needs the stronger form. The [doubling hypothesis](/doubling-hypothesis/) uses the measured ratio, and a ratio near 2 points to linear growth.

### Pitfalls

- **Linear in what.** The size is the length of the input, in bits or in words, see [input size](/input-size/). A loop "for $i$ from 1 to $N$" on an input integer $N$ is linear in the value $N$ and exponential in the length $\lg N$. This is [pseudo-polynomial](/pseudo-polynomial-time/) time, not linear time. In the same way counting sort is $\Theta(n + k)$, and with $k$ up to $2^{w}$ the term $k$ dominates.
- **Words or bits.** Adding $n$ numbers of $\beta$ bits each makes $n - 1$ additions, which is linear in the word RAM when each number fits in a word. With $\beta$ larger than the word, each addition costs $\Theta(\beta / w)$ word operations, and the total $\Theta(n \beta / w)$ is still linear in the input length of $n\beta$ bits. A linear count of operations becomes a nonlinear time when the operands grow during the run, as in repeated multiplication.
- **Hidden linear operations.** A call that looks like one step can cost $\Theta(n)$: inserting at the front of an array, testing membership in a list, taking the length of a linked list without a stored length, copying a slice, or appending to an immutable string. Inside a loop of $n$ rounds, such a call makes the loop quadratic. Building a string of length $n$ by $n$ appends that each copy the string costs $1 + 2 + \cdots + n = n(n+1)/2$ character copies.
- **The nesting does not decide the class.** The pointer loops above are linear, although they are nested. A single loop whose body calls a linear search is quadratic.
- **Amortized or expected linear.** Building a hash set of $n$ items is linear in expectation, not in the worst case. Appending $n$ items to a [dynamic array](/dynamic-array/) is linear in total, but one append can cost $\Theta(n)$.
- **Constants.** Two linear algorithms can differ by a large factor. Median of medians has a much larger constant than [quickselect](/quickselect/), which is linear only in expectation. A pass that misses the cache on each item can be many times slower than a pass over contiguous memory.

## Examples

- Sum of an array of $n$ numbers: $n - 1$ additions.
- Maximum of an array: exactly $n - 1$ comparisons on each input, which is optimal in the comparison model.
- Reverse an array in place: $\lfloor n/2 \rfloor$ swaps.
- Merge two sorted arrays of 5 and 7 items: at most 11 comparisons.
- Knuth-Morris-Pratt search for the pattern `aab` in the text of 999 letters `a` followed by one `b`: 1997 comparisons in the scan, below the bound $2n = 2000$, and one match, at position 997.
- Universal-sink test in a $1000 \times 1000$ adjacency matrix: at most 2997 queries. This is linear in the number of vertices and sublinear in the input size of $10^6$ entries, see [sublinear time](/sublinear-time/).
- Non-example: find the maximum by comparing each pair of items. This makes $n(n-1)/2$ comparisons, so it is [quadratic](/quadratic-time/) although the problem is linear.
- Non-example: [insertion sort](/insertion-sort/) is $\Theta(n)$ in the best case, on a sorted input, and $\Theta(n^2)$ in the worst case. It is not a linear-time algorithm without a named case.

## Where it is used

Linear time is the target for scanning, counting, filtering, parsing and string matching, and for the preprocessing step before a faster query structure. An algorithm with an $O(n)$ upper bound for a problem whose every item matters is optimal up to a constant factor, see [asymptotic optimality](/asymptotic-optimality/). Sorting by comparisons is the main example of a task that does not reach linear time: it needs $\Omega(n \log n)$ comparisons, see [linearithmic time](/linearithmic-time/). See the table of the [common growth rates](/common-growth-rates/).

## References
