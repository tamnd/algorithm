---
tag: 1H3ZJ5
kind: definition
slug: time-complexity
name: Time complexity
aliases:
- running time
- time bound
area: foundations/asymptotic-analysis
level: intro
summary: The function T(n) that gives the worst-case, best-case or average number of steps of an algorithm on inputs of size n, in a stated model of computation.
prereqs: [input-size, asymptotic-notation]
see_also: [worst-case-analysis, best-case-analysis, average-case-analysis, order-of-growth, space-complexity, word-ram, random-access-machine, amortized-cost]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2, Analyzing algorithms (the RAM model, running time, worst case and average case) and Section 3.1 (O, Omega and Theta applied to running times)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.10, Analysis of an Algorithm (minimum, maximum and average of the count of steps of Algorithm M)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms (cost models and order of growth)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 2.1, Computational Tractability (worst-case running times)
  - paper: doi:10.1016/S0019-9958(65)90399-2
    title: F. C. Hennie, One-tape, off-line Turing machine computations, Information and Control 8(6), 1965, pages 553 to 578
    locator: the quadratic lower bound by crossing sequences
---

The time complexity of an algorithm is the function $T$ that maps each [input size](/input-size/) $n$ to the number of steps that the algorithm takes on inputs of size $n$, counted in a stated [model of computation](/random-access-machine/). Because many inputs have the same size, the definition must also say which input it uses: the worst, the best, or an average under a stated distribution. The result is a function of $n$, and you describe its growth with [asymptotic notation](/asymptotic-notation/).

## Definition

**The model.** Fix a model of computation and a cost for each step. The usual model is the [random-access machine](/random-access-machine/) with [unit cost](/unit-cost-model/): each basic operation (an arithmetic operation on a word, a comparison, a read or a write of one memory cell, a jump) costs one step. Unit cost is fair when each word has $\Theta(\log n)$ bits: at least $\lg n$ bits, so that a word holds an index into the input, and not many more, so that one step cannot do the work of many. The [word RAM](/word-ram/) makes this precise. When numbers can grow without bound, use the [logarithmic cost model](/logarithmic-cost-model/), where an operation costs the number of bits of its operands.

**The step count of one input.** For an algorithm $A$ and an input $x$, let $t_A(x) \in \mathbb{N} \cup \{\infty\}$ be the number of steps that $A$ takes on $x$, with $t_A(x) = \infty$ when $A$ does not stop on $x$.

**The three cases.** Let $I_n$ be the set of inputs of size $n$. For each $n$ with $I_n \ne \emptyset$:

- The **worst-case time** is $T_{\max}(n) = \sup_{x \in I_n} t_A(x)$. When $I_n$ is finite, this is a maximum.
- The **best-case time** is $T_{\min}(n) = \min_{x \in I_n} t_A(x)$. The minimum exists because every non-empty set of values in $\mathbb{N} \cup \{\infty\}$ has a least element.
- The **average-case time** is $T_{\mathrm{avg}}(n) = \sum_{x \in I_n} \Pr[x] \, t_A(x)$ for a stated probability distribution on $I_n$ with countable support. For sorting, the usual choice makes each of the $n!$ relative orders of $n$ distinct keys equally likely.

For each $n$, $T_{\min}(n) \le T_{\mathrm{avg}}(n) \le T_{\max}(n)$, because a weighted mean of numbers lies between their minimum and their supremum.

When a page says "the time complexity" or "the running time" with no other word, it means $T_{\max}$. When $A$ stops on each input and $I_n$ is finite, each of the three is a function from the sizes $n$ to the non-negative reals, so you can write $T(n) = O(g(n))$, $T(n) = \Omega(g(n))$ or $T(n) = \Theta(g(n))$. These three notations are about the function $T$ of one fixed case. They are not the three cases. The sentence "the best-case time of [insertion sort](/insertion-sort/) is $O(n^2)$" is true, and it uses $O$ with the best case (CLRS, Section 3.1).

**What a bound says.** $T_{\max}(n) \le f(n)$ means that every input of size $n$ takes at most $f(n)$ steps. $T_{\max}(n) \ge g(n)$ means only that some input of size $n$ takes at least $g(n)$ steps. For the best case the roles swap: $T_{\min}(n) \ge g(n)$ is a statement about every input.

**Robustness under a change of cost.** Suppose that each kind of step costs between $c_1 > 0$ and $c_2$ units of real time on some machine. Then the real time of a run of $t$ steps lies between $c_1 t$ and $c_2 t$, and so the worst-case real time is between $c_1 T_{\max}(n)$ and $c_2 T_{\max}(n)$. So a change of the machine, of the compiler, or of the step costs changes $T$ by a constant factor only, and the $\Theta$-class of $T$ does not change. A change of the model can change more than a constant. A [single-tape Turing machine](/turing-machine/) needs $\Omega(n^2)$ steps to decide whether a string is a palindrome (Hennie, 1965), but a RAM does it in $O(n)$ steps. This is why each bound in this reference names its model.

**Other kinds of bound.** An [amortized](/amortized-cost/) bound is a bound on the mean cost of an operation over a worst-case sequence of operations. An [expected](/expected-running-time/) bound is a mean over the random choices of a randomized algorithm, for the worst input. Neither is one of the three cases above, but both use the same notation.

## Examples and non-examples

**Finding the maximum (Knuth, Volume 1, Section 1.2.10).** Scan $n$ distinct keys from left to right, and update the current maximum when a larger key appears. Count the updates. The minimum is 0, when the first key is the largest. The maximum is $n - 1$, on the increasing order. Under the uniform distribution on the $n!$ orders, the key at position $i$ is the largest of the first $i$ keys with probability $1/i$, so the expected number of updates is $\sum_{i=2}^{n} 1/i = H_n - 1$, where $H_n$ is the [harmonic number](/harmonic-series/). For $n = 4$ the three values are 0, 3 and $13/12$. A program also makes $n - 1$ comparisons on every input, so the comparisons have the same best, worst and average case.

**Linear search.** Search for a key in an array of $n \ge 1$ items, and count the comparisons with the key. $T_{\min}(n) = 1$, when the key is first. $T_{\max}(n) = n$, when the key is last or absent. If the key is present at a uniformly random place, $T_{\mathrm{avg}}(n) = (1 + 2 + \cdots + n)/n = (n+1)/2$. So $T_{\max}(n) = \Theta(n)$ and $T_{\min}(n) = \Theta(1)$. See [linear search](/linear-search/).

**Insertion sort.** Count the comparisons between keys. Step $i$ (for $i = 2, \ldots, n$) compares the new key with the sorted part from right to left. It makes one comparison per larger key, plus one more comparison that stops the scan, except when the new key is smaller than all keys before it.

- $T_{\min}(n) = n - 1$, on the sorted array.
- $T_{\max}(n) = n(n-1)/2$, on the reverse-sorted array.
- $T_{\mathrm{avg}}(n) = n(n-1)/4 + n - H_n$ under the uniform distribution on orders. The number of pairs out of order ([inversions](/inversion/)) has mean $n(n-1)/4$. The extra comparisons are $n - 1$ minus the number of positions $i \ge 2$ whose key is smaller than all keys before it, and that number has mean $H_n - 1$ by the argument of the previous example.

For $n = 8$ the three values are 7, 28 and $5399/280 \approx 19.28$. For $n = 4$ they are 3, 6 and $59/12 \approx 4.92$.

**A trap with the size.** [Trial division](/trial-division/) tests whether $N$ is prime with up to about $\sqrt{N}$ divisions. This looks small, but the input size is the number of bits $b = \lfloor \lg N \rfloor + 1$, and $\sqrt{N} \ge 2^{(b-1)/2}$. So the worst-case time is exponential in $b$. A bound that is polynomial in the value of a number but not in its length is [pseudo-polynomial](/pseudo-polynomial-time/).

**Non-example: one measurement.** "The algorithm takes 3 seconds" is one measurement on one machine and one input. It is not a function of $n$, so it is not a time complexity.

**Non-example: no case and no model.** "The algorithm is fast on most inputs" does not define a function.

**Non-example: an algorithm that does not stop.** A loop that runs until a value is found, on an input where the value never occurs, has $t_A(x) = \infty$. Then $T_{\max}(n) = \infty$, and no $O$ bound holds. An algorithm must stop on each input of $I_n$ to have a finite worst-case time.

### Pitfalls

- **A bare $\Theta$ for the whole algorithm.** "Insertion sort runs in $\Theta(n^2)$ time" is false as a statement about every input: on the sorted array it takes linear time. "Its worst-case time is $\Theta(n^2)$" is true.
- **Confusing the case with the notation.** $O$ is not "the worst case" and $\Omega$ is not "the best case". Each case is a function, and each function has its own $O$, $\Omega$ and $\Theta$ bounds.
- **Measuring the size by the value.** For numeric input, $n$ is the number of bits, not the value. See [input size](/input-size/).
- **Unit cost with huge numbers.** An algorithm that starts from 2 and squares the number $n$ times builds $2^{2^n}$, a number of $2^n + 1$ bits, in $n$ unit-cost steps. Unit cost is fair only when the numbers fit in $O(1)$ words.
- **An average without a distribution.** An average-case time is meaningless until you state the distribution. Inputs in practice are often far from uniform, for example nearly sorted.

## Related definitions

- [Worst-case analysis](/worst-case-analysis/) studies $T_{\max}$. [Best-case analysis](/best-case-analysis/) studies $T_{\min}$. [Average-case analysis](/average-case-analysis/) studies $T_{\mathrm{avg}}$.
- [Order of growth](/order-of-growth/) is the $\Theta$-class of $T$, what remains when you drop constant factors and lower-order terms.
- [Space complexity](/space-complexity/) is the same idea for the number of memory cells.
- The [comparison model](/comparison-model/) counts only the comparisons between items, as in the examples above.
- [Input size](/input-size/) fixes what $n$ means. For a graph, the time is often a function of two numbers, the count of vertices and the count of edges. See [multivariate asymptotic notation](/multivariate-asymptotic-notation/).

## References
