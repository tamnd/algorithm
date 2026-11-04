---
tag: 5TGWDS
kind: concept
slug: best-case-analysis
name: Best-case analysis
aliases:
- best-case running time
area: foundations/asymptotic-analysis
level: intro
summary: Gives the minimum running time over all inputs of a given size.
prereqs: [time-complexity, input-size]
see_also: [worst-case-analysis, average-case-analysis, adaptive-sorting, insertion-sort, asymptotic-notation]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2, Analyzing algorithms (best case and worst case of insertion sort) and Section 3.1 (O, Omega and Theta for the best case)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.10, Analysis of an Algorithm (the minimum, maximum and average of a step count)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4 (Analysis of Algorithms) and Section 2.1 (insertion sort)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.1 (sorting by insertion) and Section 6.2.1 (binary search, Algorithm B and the comparison tree)
---

Best-case analysis measures the running time of an algorithm as the smallest time over all inputs of the same size. The result is a function $T_{\min}(n)$. It is a lower bound on the cost of the algorithm on every input, and it is not a promise of speed.

## In plain words

An algorithm can be fast on one input and slow on another input of the same size. The best case asks for the fastest case. If you look for a name in a list and the name is first, you stop at once. That is the best case for the list, and it says little about the lists that you will meet.

The best case is rarely the number that you want. It gives no forecast and no promise of speed. It is also easy to fake. Take any slow method and add a quick test for one special input. The new method has a fast best case, and it is not better in any other way.

The best case still has some uses. It shows which inputs make a method fast. It also shows that no input can be faster than a given amount.

## The idea

For an algorithm $A$ (see [time complexity](/time-complexity/)) on a set $I_n$ of inputs of [size](/input-size/) $n$, with $t_A(x)$ the number of steps on input $x$ in a stated model:
$$T_{\min}(n) = \min_{x \in I_n} t_A(x).$$
The minimum exists when $t_A$ takes values in the natural numbers and $I_n$ is not empty. For every distribution on $I_n$, $T_{\min}(n) \le T_{\mathrm{avg}}(n) \le T_{\max}(n)$, with the [worst case](/worst-case-analysis/) on the right and the [average case](/average-case-analysis/) in the middle.

To prove $T_{\min}(n) \le f(n)$, give one input of size $n$ with $t_A(x) \le f(n)$. To prove $T_{\min}(n) \ge g(n)$, show $t_A(x) \ge g(n)$ for every $x \in I_n$. This is the opposite of the worst case, where the upper bound needs all inputs and the lower bound needs one input. A statement such as $T_{\min}(n) = \Omega(g(n))$ (see [asymptotic notation](/asymptotic-notation/)) is a lower bound for every input.

### Why it is rarely useful

- It is not a guarantee. A system that has to meet a deadline needs a bound that holds for the inputs it receives.
- It is often tiny and far from typical. A lucky input can be a sorted array, a key in the first place or an empty graph.
- It does not compare algorithms well. An algorithm with a fast best case can be slower than another on every input that occurs in practice.

### The trap: a special check

Take any correct algorithm $A$ and, for each $n$, one fixed input $x_n$ with a known answer $y_n$. Define $A'$: compare the input with $x_n$, and if they are equal, output $y_n$; else run $A$. The best case of $A'$ is the cost of recognizing $x_n$. To accept $x_n$, the check must read all of $x_n$, so the best case of $A'$ is at least the cost of reading $x_n$. It does not depend on how good $A$ is. The worst case of $A'$ grows by at most the cost of the check.

For sorting, take $x_n$ to be the sorted order. Test whether the array is sorted: this takes at most $n - 1$ comparisons, and exactly $n - 1$ when it is sorted. Then any sorting algorithm, even a slow one, gets a best case of $n - 1$ comparisons, and its worst case grows by at most $n - 1$ comparisons. So a claim "best case $O(n)$" tells you about the algorithm only if the algorithm is built to be fast on a wide class of inputs, as in [adaptive sorting](/adaptive-sorting/), and not by a check for one input.

### Use of the best case

- **Which inputs are fast.** The best case names the inputs of the fast path. For insertion sort it is the sorted input, and the cost grows with the disorder of the input, as in an adaptive sort.
- **Equal best and worst case.** If $T_{\min}(n) = T_{\max}(n)$, the cost does not depend on the data. [Selection sort](/selection-sort/) makes $n(n-1)/2$ comparisons on every input of size $n$.
- **A lower bound for every input.** If an algorithm reads all its input, then $T_{\min}(n) = \Omega(n)$, and every input takes at least linear time.
- **A check on a claimed lower bound.** The lower bound for sorting, $\lceil \lg n! \rceil$ comparisons, is a worst-case bound for the problem. It does not apply to the best case of one algorithm: insertion sort makes $n - 1$ comparisons on sorted input, which is fewer than $\lceil \lg n! \rceil$ for $n \ge 3$ (for $n = 8$: 7 against 16).

### Pitfalls

- **Best case is not small input.** "The best case is the empty array" is wrong. The best case is a minimum over the inputs of one fixed size $n$, so it is a function of $n$.
- **Best case is not $\Omega$.** $\Omega$ is a kind of bound, and the best case is a function. The worst case has $\Omega$ bounds too, for example $T_{\max}(n) = \Omega(n^2)$ for insertion sort.
- **A best case for the algorithm is not a bound for the problem.** A fast best case does not contradict a lower bound for the problem, because such a bound is about the worst case of every algorithm.
- **Fast best case from a special test.** Before you quote a best case, check that it comes from a wide class of inputs and not from a test for one input, as in the trap above.

The notations $O$, $\Omega$ and $\Theta$ are about functions and not about cases. "The best case of insertion sort is $O(n)$" and "the best case of insertion sort is $\Omega(n)$" are both correct and say $T_{\min}(n) = \Theta(n)$. See [asymptotic notation](/asymptotic-notation/).

## Examples

- **[Linear search](/linear-search/).** The best case is a key in the first place: 1 comparison, for each $n \ge 1$. The worst case is $n$ comparisons.
- **[Binary search](/binary-search/).** With a three-way comparison at each probe, the best case is a key at the middle probe: 1 probe. The worst case is $\lfloor \lg n \rfloor + 1$ probes. The variant that tests only "less than" in the loop and leaves the equality test to the end makes $\lfloor \lg n \rfloor$ or $\lceil \lg n \rceil$ such tests and then one equality test, on every input. Its best case and its worst case differ by at most one comparison, so a fast best case is not a property of binary search itself but of the three-way version.
- **[Insertion sort](/insertion-sort/).** For $i = 2, \ldots, n$ the key $A[i]$ is compared with at least one item of the sorted part, so there are at least $n - 1$ comparisons. A sorted array, in which each key is not smaller than the item before it, gives exactly one comparison for each $i$. So $T_{\min}(n) = n - 1$ comparisons. For $n = 8$ this is 7, and the worst case is $n(n-1)/2 = 28$.
- **[Bubble sort](/bubble-sort/) with an early exit.** If a pass makes no swap, the algorithm stops. On a sorted array the first pass makes $n - 1$ comparisons and no swap, so $T_{\min}(n) = n - 1$. In the usual version without the early exit, the count is $n(n-1)/2$ on every input.
- **Top-down [merge sort](/merge-sort/).** A merge of two sorted runs with $a$ and $b$ items makes at least $\min(a, b)$ comparisons: each comparison moves one item to the output, and when one run is empty the other is copied without comparisons, so all items of the run that empties first were output by comparisons. This bound is reached when all items of the shorter run are smaller than all items of the longer one. If the array is split into runs of $\lceil n/2 \rceil$ and $\lfloor n/2 \rfloor$ items, the best case obeys $B(n) = B(\lceil n/2 \rceil) + B(\lfloor n/2 \rfloor) + \lfloor n/2 \rfloor$ with $B(1) = 0$. An input with distinct keys that reaches $B(n)$ for every $n$ exists: put the smallest $\lfloor n/2 \rfloor$ values in the right half and the others in the left half, and build each half in the same way. For $n$ equal to a power of 2 the sorted array reaches it, and $B(2^k) = k \, 2^{k-1}$. Proof by induction: $B(1) = 0$ and $B(2^k) = 2 B(2^{k-1}) + 2^{k-1} = (k-1) 2^{k-1} + 2^{k-1} = k \, 2^{k-1}$. So $B(8) = 12$, against 17 comparisons in the worst case. The best case is about half of the worst case, and both are $\Theta(n \log n)$: here the best case does not change the order of growth.
- **Non-example.** [Quicksort](/quicksort/) with the last item as pivot takes $\Theta(n^2)$ time on a sorted array, but this is the worst case and not the best case. The best case of quicksort is a pivot that splits the range in halves at every step, with $\Theta(n \log n)$ comparisons.

## Where it is used

Best-case bounds appear mainly as the lower end of a range, as in "insertion sort takes between $n - 1$ and $n(n-1)/2$ comparisons". They explain adaptive algorithms, whose cost depends on a property of the input such as the number of inversions. They give the cost of the fast path in a system that tests for a common case first. A worst-case or average-case bound is the right tool for a promise or a forecast. For a study of the inputs between the two extremes, see [average-case analysis](/average-case-analysis/).

## References
