---
tag: TGN83V
kind: concept
slug: common-growth-rates
name: Common growth rates
aliases:
- growth-rate hierarchy
area: foundations/asymptotic-analysis
level: intro
summary: The standard hierarchy of functions (constant, logarithmic, linear, linearithmic, quadratic, cubic, exponential) used to classify running times.
prereqs: [asymptotic-notation, order-of-growth]
see_also: [constant-time, logarithmic-time, linear-time, linearithmic-time, quadratic-time, polynomial-time, comparing-growth-by-limits, doubling-hypothesis]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 3
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11.1
---

The common growth rates are the few classes of running time that cover almost all algorithms in practice: constant, logarithmic, linear, linearithmic, quadratic, cubic, exponential and factorial. Each class is the [order of growth](/order-of-growth/) of a simple function, and each is $o$ of the next one in the list. This page gives the list, one example for each class, and the effect of doubling the input.

## In plain words

Most algorithms fall into a short list of speeds. Some take the same time for any input. Some grow very slowly, by one step each time the input doubles. Some grow in step with the input, some a little faster, and some grow with the square or the cube of the input. At the end of the list are the algorithms that try all subsets or all orders of the items. Their time grows so fast that they work only for inputs of a few dozen items.

The list is useful for a quick judgment. If you know the class of an algorithm, you know what happens when the input becomes ten or a hundred times larger, and you know if the algorithm can work at all for the size you need.

## The idea

### The ladder

For each two neighbors in the list below, the first function is $o$ of the second: the ratio of the first to the second tends to 0. The relation is transitive, so it holds for each pair that is not neighbors.

$$1 \ \prec \ \lg n \ \prec \ \lg^2 n \ \prec \ \sqrt{n} \ \prec \ n \ \prec \ n \lg n \ \prec \ n^2 \ \prec \ n^3 \ \prec \ 2^n \ \prec \ n! \ \prec \ n^n$$

Here $\lg^2 n$ means $(\lg n)^2$. The proofs use the limit rules of [asymptotic notation](/asymptotic-notation/) and [comparing growth by limits](/comparing-growth-by-limits/). The facts that a power of a logarithm is $o(n^\varepsilon)$ for each $\varepsilon > 0$ and a polynomial is $o(2^n)$ are on the page of asymptotic notation. For the last two steps: $n!/2^n = \prod_{i=1}^{n} (i/2)$ has the factors $1/2$, $1$, $3/2$ and then $n - 3$ factors that are each at least $2$, so $n!/2^n \ge 2^{n-3} \cdot 3/4 \to \infty$ for $n \ge 3$. And $n!/n^n = \prod_{i=1}^{n} (i/n) \le 1/n$ for $n \ge 2$, because the factor with $i = 1$ is $1/n$ and the others are at most $1$. The first function in each pair is therefore $o$ of the second. The base matters for an exponential: $2^n \prec 3^n$, because $(3/2)^n \to \infty$. It does not matter for a logarithm, see [logarithms](/logarithms/).

### The classes

| Class | Typical function | Example algorithm and case | Page |
| --- | --- | --- | --- |
| Constant | $1$ | Read `A[i]` in an array: worst case | [constant time](/constant-time/) |
| Logarithmic | $\lg n$ | [Binary search](/binary-search/) in a sorted array: worst case | [logarithmic time](/logarithmic-time/) |
| Polylogarithmic | $\lg^k n$ | A range-sum query in a two-dimensional [Fenwick tree](/fenwick-tree/): $O(\lg^2 n)$ when the sides are of size $n$ | [polylogarithmic time](/polylogarithmic-time/) |
| Square root | $\sqrt{n}$ | A range query on an array of $n$ items with [square root decomposition](/square-root-decomposition/) takes $O(\sqrt{n})$ time | [sublinear time](/sublinear-time/) |
| Linear | $n$ | Find the maximum of an array: $n - 1$ comparisons in each case | [linear time](/linear-time/) |
| Linearithmic | $n \lg n$ | [Merge sort](/merge-sort/): worst case | [linearithmic time](/linearithmic-time/) |
| Quadratic | $n^2$ | [Insertion sort](/insertion-sort/): worst case | [quadratic time](/quadratic-time/) |
| Cubic | $n^3$ | [Naive matrix multiplication](/naive-matrix-multiplication/) of two $n \times n$ matrices: $n^3$ multiplications | [cubic time](/cubic-time/) |
| Exponential | $2^n$ | List all subsets of a set of $n$ items | none (compare [polynomial time](/polynomial-time/)) |
| Exponential, base other than 2 | $\varphi^n$ | The recursion $F(n) = F(n-1) + F(n-2)$ for the [Fibonacci numbers](/fibonacci-numbers/), without a table, makes $2F(n+1) - 1$ calls, which is $\Theta(\varphi^n)$ with $\varphi = (1 + \sqrt{5})/2$ | none |
| Factorial | $n!$ | List all orders of $n$ items; brute-force search of the shortest tour through $n$ cities, which examines $(n-1)!$ tours | none |

Each class down to the cubic is bounded by a polynomial of fixed degree, so it is [polynomial time](/polynomial-time/). The classes from exponential on are not. A polynomial of any fixed degree is $o(2^n)$.

### When the input doubles

Let $T$ be the exact running time and compare $T(2n)$ with $T(n)$.

| Class | $T(n)$ | $T(2n)$ in terms of $T(n)$ |
| --- | --- | --- |
| Constant | $c$ | the same |
| Logarithmic | $a \lg n$ | $T(n) + a$ |
| Square root | $a \sqrt{n}$ | $\sqrt{2} \, T(n)$, about $1.41$ times |
| Linear | $a n$ | $2 T(n)$ |
| Linearithmic | $a n \lg n$ | $2 T(n) (1 + 1/\lg n)$, a little more than $2$ times |
| Quadratic | $a n^2$ | $4 T(n)$ |
| Cubic | $a n^3$ | $8 T(n)$ |
| Exponential | $a \, 2^n$ | $2^n \, T(n)$: the time is multiplied by $2^n$ |
| Factorial | $a \, n!$ | $\frac{(2n)!}{n!} T(n)$, which is more than $n^n \, T(n)$, because $(2n)!/n! = (n+1)(n+2) \cdots (2n)$ has $n$ factors that are each larger than $n$ |

For a power law $T(n) \sim a n^b$ the ratio $T(2n)/T(n)$ tends to $2^b$ (see [tilde notation](/tilde-notation/)). This is the basis of the [doubling hypothesis](/doubling-hypothesis/). A bound $\Theta(n^b)$ alone gives only that the ratio stays between two positive constants. For the exponential, an increase of $n$ by 1 multiplies the time by 2, so the natural step is "add one", not "double".

### What the classes mean in time

Assume $10^9$ simple steps in each second and a running time of exactly $f(n)$ steps.

| $n$ | $n^2$ | $2^n$ | $n!$ |
| --- | --- | --- | --- |
| 20 | 400 steps, under 1 microsecond | about 1.05 million steps, about 1 millisecond | $2.43 \times 10^{18}$ steps, about 77 years |
| 50 | 2500 steps, about 2.5 microseconds | $1.13 \times 10^{15}$ steps, about 13 days | $3.04 \times 10^{64}$ steps |

The step from $n = 20$ to $n = 50$ costs a factor of 6.25 for the quadratic algorithm, a factor of about $10^9$ for the exponential one, and a factor of about $10^{46}$ for the factorial one. See [order of growth](/order-of-growth/) for the largest input that each class can solve in a fixed budget.

### Pitfalls

- **A class names a function, not an algorithm.** An algorithm has a class for each case and each model. Insertion sort is linear in the best case and quadratic in the worst case.
- **Constants and small inputs.** The ladder describes large $n$. An algorithm of a higher class with a small constant can be faster for small inputs.
- **Other classes exist.** The ladder is not complete. There are classes between the rungs, for example $n^{3/2}$ or $n^{\lg 3}$ (the cost of Karatsuba multiplication), and $2^{\sqrt{n}}$ between polynomial and exponential. There are also pairs of functions that cannot be compared, see [asymptotic notation](/asymptotic-notation/).
- **Size or value.** An algorithm that is linear in the value $N$ of a number is exponential in the number of bits of $N$. See [input size](/input-size/).
- **Log base and constants in exponents.** $\Theta(\log_2 n) = \Theta(\log_{10} n)$, but $2^n$ and $2^{2n}$ are different classes.

## Examples

- Doubling an array of $10^6$ items makes a linear scan take twice as long, a linearithmic sort a little over twice as long (the factor is $2(1 + 1/\lg n)$, about $2.1$ for $n = 10^6$), and a quadratic comparison of all pairs four times as long.
- The number of subsets of a set of 30 items is $2^{30} = 1073741824$. For 31 items it is twice that.
- Non-example: $n^{\lg n} = 2^{\lg^2 n}$ is not polynomial and not exponential. It is $\omega(n^k)$ for each constant $k$, and it is $o(2^{\varepsilon n})$ for each constant $\varepsilon > 0$, because $\lg^2 n - \varepsilon n \to -\infty$. See [quasi-polynomial time](/quasi-polynomial-time/).

## Where it is used

The ladder is the vocabulary of every page that states a bound. The page of each class gives its definition and typical algorithms. The class [polynomial time](/polynomial-time/) is the base of the study of tractable problems, and the step from polynomial to exponential is the line that complexity theory draws between feasible and infeasible in the worst case.

## References
