---
tag: 6DHY04
kind: concept
slug: asymptotic-optimality
name: Asymptotic optimality
aliases:
- optimal up to constant factors
area: foundations/asymptotic-analysis
level: core
summary: An algorithm is asymptotically optimal when its running time matches a lower bound up to constant factors.
prereqs: [asymptotic-notation, worst-case-analysis, lower-bound]
see_also: [comparison-sort-lower-bound, merge-sort-optimality, comparison-model, word-ram, upper-bound, trivial-lower-bound, radix-sort, order-of-growth]
sources:
  - url: "https://en.wikipedia.org/wiki/Computational_complexity_of_matrix_multiplication"
    locator: article Computational complexity of matrix multiplication (best known exponent)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.1, Lower bounds for sorting (asymptotically optimal comparison sorts)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1, Minimum-comparison sorting
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.2, Mergesort (complexity of sorting)
---

An algorithm is asymptotically optimal for a problem in a model of computation when its worst-case cost is $O(L(n))$, where $L(n)$ is a lower bound that holds for every algorithm for that problem in that model. Its cost is then $\Theta(L(n))$, and no algorithm of the model can beat it by more than a constant factor. [Merge sort](/merge-sort/) is asymptotically optimal for sorting in the [comparison model](/comparison-model/).

## In plain words

Think of a race on a fixed track. An upper bound is the time of one runner. A lower bound is a rule of the track: nobody can finish faster than some time. If a runner is as fast as that limit, up to a constant factor, no runner can be much faster, and we call the runner optimal. The claim is only about the runners allowed on that track.

For sorting by comparisons, the track rule is a counting argument. A sort must tell apart all the possible orders of the input, and each comparison has only two answers. So the number of comparisons is at least the logarithm of the number of orders. Merge sort uses about that many, so it is optimal on this track. A sort that may look at the digits of the keys is not on this track, and it can be faster.

## The idea

**The definition.** Fix a problem $P$, a model of computation $M$ (what an algorithm is and what one step costs), and a measure of cost. For an algorithm $B$ in $M$ that solves $P$, let $W_B(n)$ be its cost in the worst case on inputs of size $n$ (see [worst-case analysis](/worst-case-analysis/)).

- A function $L$ is a *lower bound* for $P$ in $M$ if there are constants $c > 0$ and $n_0$, which do not depend on the algorithm, such that $W_B(n) \ge c\,L(n)$ for each algorithm $B$ in $M$ that solves $P$ and for each $n \ge n_0$.
- An algorithm $A$ is *asymptotically optimal* for $P$ in $M$ if $W_A(n) = O(L(n))$ for some lower bound $L$. Then $W_A(n) = \Theta(L(n))$, because $A$ is itself an algorithm in $M$ and so $W_A(n) \ge c\,L(n)$.

The four parts, problem, model, cost measure and case (worst or average), are all in the claim. A statement such as "algorithm $A$ is optimal" is incomplete without them. The cost measure may be comparisons, memory accesses or space, if the lower bound is for the same resource. The definition above uses the worst case. An average-case version replaces $W_B$ by the average cost and uses an average-case lower bound.

**A sharper sense.** Some authors call $A$ asymptotically optimal when $W_A(n) \sim L(n)$, that is, when the ratio tends to 1. This is a stronger claim than $\Theta$, and a page that uses it says so. See [tilde notation](/tilde-notation/).

**Upper and lower bound.** An upper bound comes from an algorithm and its analysis. A lower bound comes from an argument about all algorithms of the model, for example a counting argument ([information-theoretic bound](/information-theoretic-bound/)), an adversary, or a reduction. See [lower bound](/lower-bound/) and [upper bound](/upper-bound/). Optimality needs both, and they must have the same order. When they differ, as for multiplying two $n \times n$ matrices with arithmetic operations, where the best known exponent is about 2.37 and the best known lower bound is the trivial $\Omega(n^2)$ (see [trivial lower bound](/trivial-lower-bound/)), no algorithm is known to be optimal and the gap is a research question.

## Examples

**Sorting by comparisons.** In the comparison model, a sort of $n$ distinct keys makes at least $\lceil \lg n!\,\rceil$ comparisons in the worst case, see the [comparison sorting lower bound](/comparison-sort-lower-bound/). By [Stirling's approximation](/stirling-approximation/), $\lg n! = n\lg n - n\lg e + O(\log n)$, so the lower bound is $L(n) = n\lg n$ up to a constant. Merge sort makes at most $n\lceil\lg n\rceil - 2^{\lceil\lg n\rceil} + 1 \le n\lg n$ comparisons, which is $O(L(n))$. So merge sort is asymptotically optimal, and so is [heapsort](/heapsort/), whose worst-case time is also $\Theta(n\log n)$. The exact numbers:

| $n$ | lower bound $\lceil\lg n!\rceil$ | merge sort, worst case | ratio |
| --- | --- | --- | --- |
| 10 | 22 | 25 | 1.136 |
| 100 | 525 | 573 | 1.091 |
| 1000 | 8530 | 8977 | 1.052 |
| $10^6$ | 18 488 885 | 18 951 425 | 1.025 |

The ratio tends to 1, so merge sort is also optimal in the sharper sense for the count of comparisons. See [merge sort optimality](/merge-sort-optimality/).

**Exactly optimal.** Finding the maximum of $n$ keys by comparisons takes exactly $n-1$ comparisons in the worst case, and an algorithm that scans the array once meets it ([maximum finding lower bound](/max-finding-lower-bound/)). Here the bounds match with no constant gap. Asymptotic optimality is the weaker claim that they match up to a factor.

**Not optimal in the worst case.** [Quicksort](/quicksort/) takes $n(n-1)/2$ comparisons on an adversarial input, which is $\Theta(n^2)$, so it is not worst-case optimal in the comparison model. On a uniformly random permutation its expected number of comparisons is $2(n+1)H_n - 4n \approx 1.39\,n\lg n$, which is $\Theta(n\log n)$ (see the [expected running time of quicksort](/quicksort-expected-running-time/)). The same expectation holds for every input when the pivot is chosen at random (see [randomized quicksort](/randomized-quicksort/)). The average of the number of comparisons of any comparison sort over the $n!$ permutations is also at least $\lg n!$, because a binary tree with $N$ leaves has average leaf depth at least $\lg N$ (Knuth, Volume 3, Section 5.3.1). So quicksort is optimal for the average over random permutations. The case is part of the claim: for $n = 10^6$ the worst case is about $5 \times 10^{11}$ compares and the average is $2.5 \times 10^7$.

**Outside the model.** The bound $\Omega(n\log n)$ is a statement about the comparison model. [Radix sort](/radix-sort/) does not compare keys. It reads their digits. On the [word RAM](/word-ram/), LSD radix sort on $n$ keys that are $d$-digit numbers in base $b$ takes $\Theta(d(n+b))$ time. For $n$ keys in the range $0$ to $n^c - 1$, with $c$ a constant, take $b = n$ and $d = c$: the time is $\Theta(cn) = \Theta(n)$. For 32-bit keys, base $b = 256$ and four passes, the time is $4(n + 256)$ steps, and this is $4\,001\,024$ for $n = 10^6$. The units are different from the comparisons above, so the numbers are not a ratio, but the order of growth shows the point: the lower bound does not apply, because a radix sort is not an algorithm of the comparison model.

### Common errors

- **A bound without a lower bound.** "Algorithm $A$ runs in $O(n\log n)$, so it is optimal" is wrong. Optimal needs a lower bound of the same order. Without one, a faster algorithm may exist.
- **No model.** The lower bound holds for the algorithms of one model. A different model can have a different bound, as radix sort shows. An algorithm that is optimal on the comparison model has no claim on the word RAM.
- **Constants.** Asymptotic optimality ignores constant factors. An algorithm with $100\,n\lg n$ comparisons is as optimal as merge sort, yet it is a hundred times slower in the model. Two optimal algorithms can differ a lot in practice, and a non-optimal one can win at all sizes in use. See [empirical analysis of algorithms](/empirical-analysis-of-algorithms/).
- **The case.** Optimal in the worst case does not mean best on every input. Merge sort is worst-case optimal but it makes about $\frac12 n\lg n$ compares on a sorted input, while [insertion sort](/insertion-sort/) takes $n - 1$ compares there. An algorithm that adapts to the input can do better than the worst-case bound on easy inputs.
- **Other resources and lower-order terms.** The claim is about one resource. It also says nothing about lower-order terms, such as the $n\lg e$ term that separates merge sort from $\lg n!$. Merge sort is optimal in comparisons, but it uses $\Theta(n)$ extra space, while [heapsort](/heapsort/) sorts with $O(1)$ extra space. So merge sort is not optimal in space.
- **A lower bound for the wrong problem.** The bound $\Omega(n\log n)$ is for sorting. It is not a bound for finding the maximum, for merging two sorted lists, or for searching a sorted array. See the lower bound for [searching a sorted array](/sorted-search-lower-bound/).

## Where it is used

- **Closing a problem.** When an upper bound meets a lower bound, the complexity of the problem in the model is known up to a constant, and the search for a faster algorithm in that model ends. The pages of the problems in this site list the best upper bounds and the lower bounds side by side.
- **Reading the gap.** When the two bounds differ, the gap is the open part of the problem. Work on algorithms lowers the upper bound, and work on lower bounds raises the other.
- **Choosing a model.** To beat an optimal algorithm one must change the model (allow arithmetic on keys, or a larger word), the case, or the class of inputs. Randomness alone does not help for sorting, because the $\Omega(n\log n)$ bound also holds for the expected cost of randomized comparison sorts. [Radix sort](/radix-sort/) and [counting sort](/counting-sort/) are the standard examples for sorting.
- **Comparing algorithms.** Among algorithms in one model, the optimal ones form a class. Within the class, constants, memory use and stability decide.

## References
