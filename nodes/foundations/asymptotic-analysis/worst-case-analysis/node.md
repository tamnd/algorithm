---
tag: B5285R
kind: concept
slug: worst-case-analysis
name: Worst-case analysis
aliases:
- worst-case running time
area: foundations/asymptotic-analysis
level: intro
summary: Bounds the running time over all inputs of a given size, giving a guarantee that holds for every input.
prereqs: [time-complexity, input-size]
see_also: [best-case-analysis, average-case-analysis, amortized-vs-worst-case, order-of-growth, linear-search, insertion-sort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4
  - book: isbn:9780321295354
    title: Kleinberg and Tardos, Algorithm Design
    locator: Chapter 2
  - paper: "Daniel A. Spielman and Shang-Hua Teng, Smoothed analysis of algorithms: why the simplex algorithm usually takes polynomial time, Journal of the ACM 51 (2004)"
    locator: Introduction
---

Worst-case analysis measures the running time of an algorithm as the largest time over all inputs of the same size. The result is a function $T_{\max}(n)$ and a guarantee: no input of size $n$ makes the algorithm slower. It is the default way to state a [time complexity](/time-complexity/).

## In plain words

An algorithm can be fast on one input and slow on another input of the same size. For example, you look for a name in a list. If the name is first, you stop at once. If the name is not in the list, you must read every entry. Worst-case analysis asks: what is the slowest case for a list of this length? The answer is a promise. No list of this length can take longer.

This is why the worst case is the usual choice. The promise holds for any input, even one that an enemy chooses on purpose. You do not need to know what inputs will come. The worst case can be too pessimistic for inputs that you really meet. In that case, other kinds of analysis help.

## The idea

For an algorithm $A$ on a set $I_n$ of inputs of [size](/input-size/) $n$, with $t_A(x)$ the number of steps on input $x$ in a stated model:

$$T_{\max}(n) = \max_{x \in I_n} t_A(x).$$

To prove a bound $T_{\max}(n) \le f(n)$, you show $t_A(x) \le f(n)$ for each $x \in I_n$. To prove $T_{\max}(n) \ge g(n)$, you give one input $x_n \in I_n$ for each $n$ with $t_A(x_n) \ge g(n)$. The first proof is an upper bound for all inputs. The second proof needs one bad input only. If the two bounds are equal up to a constant, you can write $T_{\max}(n) = \Theta(f(n))$, and $f$ gives the [order of growth](/order-of-growth/) of the worst case.

**Why it is the default.**

- It is a guarantee. A system with a deadline needs a bound that holds for every input.
- It does not need a model of the inputs. Average-case analysis needs a probability distribution, and a wrong distribution gives a wrong result.
- It is often easier to compute than the average.
- For many algorithms the worst case happens often, or it is close to the typical case. [Linear search](/linear-search/) for an absent key is one example.

**Contrast with the other costs.**

- The [best case](/best-case-analysis/) is the minimum over $I_n$. It is a lower bound on the time of the algorithm, not a promise. A statement such as "insertion sort takes $n-1$ comparisons" holds only for special inputs, such as a sorted input. It is not a bound for every input.
- The [average case](/average-case-analysis/) is a mean over a distribution on $I_n$. It tells you the typical cost when you trust the distribution.
- The [amortized](/amortized-cost/) cost is a bound on the mean cost per operation in a sequence of operations, for the worst sequence. One operation can cost more than the amortized bound, but the sequence as a whole cannot. The input is a sequence, not one instance, and no probability is used.
- The [expected time](/expected-running-time/) of a randomized algorithm is a mean over its own random choices, for the worst input. It is a worst case over inputs and an average over coin flips. [Randomized quicksort](/randomized-quicksort/) makes $O(n \log n)$ expected comparisons on each input of $n$ distinct keys, but one unlucky run can still make $n(n-1)/2$ comparisons.

Always $T_{\min}(n) \le T_{\mathrm{avg}}(n) \le T_{\max}(n)$, for any distribution.

**A limit.** The worst-case function can be far above the cost on inputs that occur in practice. In such a case the worst-case bound is still true, but it does not predict the time that you see in practice. Two classic cases:

- [Quicksort](/quicksort/) with the first item as the pivot makes $\Theta(n^2)$ comparisons on a sorted array ($n(n-1)/2$ with Lomuto partitioning), so its worst case is $\Theta(n^2)$. Its average over random orders is $\Theta(n \log n)$.
- The [simplex method](/simplex-method/) with Dantzig's pivot rule needs an exponential number of steps on the cubes of Klee and Minty (1972), and similar inputs are known for most other standard rules. But it is fast on most inputs that occur in practice. [Smoothed analysis](/smoothed-analysis/), by Spielman and Teng, explains this gap: it measures the worst case of the expected time after a small random change of the input.

### Pitfalls

- **A worst-case $\Theta$ is not a statement about each input.** "The worst-case time of insertion sort is $\Theta(n^2)$" does not say that insertion sort takes quadratic time on each input. On a sorted input it takes linear time.
- **A bare $O$.** When a source writes "the algorithm runs in $O(f(n))$ time" and names no case, it means a worst-case upper bound. A bare $\Omega$ or $\Theta$ claims the bound for every input. So "insertion sort runs in $\Theta(n^2)$ time" is false, and "its worst-case time is $\Theta(n^2)$" is true. Name the case when you use $\Theta$.
- **One bad input is enough for a lower bound, not for an upper bound.** To show $T_{\max}(n) = O(f(n))$ you must cover every input of size $n$. Tests on many inputs do not prove it.

## Examples

**Linear search.** The array $A[1 \ldots n]$ and a key $k$ are the input. The algorithm compares $k$ with $A[1], A[2], \ldots$ in this order, and it stops at the first match or after $A[n]$. Count each comparison as one step.

- Best case: $k = A[1]$. The count is $1$.
- Worst case: $k$ is absent or $k$ is only at $A[n]$. The count is $n$. Each input of size $n$ makes at most $n$ comparisons, because the loop has $n$ passes at most. So $T_{\max}(n) = n$ exactly.
- Average case, when $k$ is in the array, the keys are distinct, and the place of $k$ is uniform on $1, \ldots, n$: the count is $(1 + 2 + \cdots + n)/n = (n+1)/2$.

So $T_{\max}(n) = \Theta(n)$, and the average is half of the worst case. The factor $1/2$ does not change the order of growth.

**Insertion sort.** Count the comparisons between a key and an item of the sorted part. Insertion sort puts item $i$ (for $i = 2, \ldots, n$) in its place in the sorted part $A[1 \ldots i-1]$, and it compares the key with the items from right to left until an item is not larger than the key, or the part is empty.

- The key at step $i$ is compared at least once and at most $i-1$ times. So the total is at least $n-1$ and at most $\sum_{i=2}^{n}(i-1) = n(n-1)/2$.
- The upper bound is reached by the reverse-sorted input (all items distinct): each key is smaller than all items before it, so step $i$ makes exactly $i-1$ comparisons.
- The lower bound is reached by the sorted input: each key is compared once.

So, in comparisons, $T_{\max}(n) = n(n-1)/2 = \Theta(n^2)$ and $T_{\min}(n) = n - 1$. For $n = 8$ the two counts are $28$ and $7$. For the average over the $24$ orders of $4$ distinct items the count is $59/12 \approx 4.92$, between $3$ and $6$. See [insertion sort](/insertion-sort/) for the algorithm and its proof.

## Where it is used

Worst-case bounds are the standard statement for sorting, searching and graph algorithms, and the bounds on this site name the case. They are the base of real-time systems, where a late answer is a failure. They are also the base of lower bounds: a lower bound for a problem in a model, such as the bound for [comparison sorting](/comparison-model/), is a statement about the worst case of every algorithm. When the worst case is too pessimistic, the next tools are [average-case analysis](/average-case-analysis/) and [amortized analysis](/amortized-cost/).

## References
