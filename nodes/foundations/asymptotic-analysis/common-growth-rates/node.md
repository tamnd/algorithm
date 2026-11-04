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
    locator: Chapter 3 (characterizing running times, standard functions) and Chapter 19 (disjoint sets, the inverse Ackermann function)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 9.1, A Hierarchy
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 2.4, A Survey of Common Running Times
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms (order-of-growth classifications and the doubling ratio)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11.1, The O-notation
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.1 (Gray codes) and Section 7.2.1.2 (generating all permutations, Heap's method)
  - paper: doi:10.1145/321879.321884
    title: Robert E. Tarjan, Efficiency of a good but not linear set union algorithm, Journal of the ACM 22(2), 215 to 225 (1975)
    locator: the main theorem
---

The common growth rates are the few functions that describe the running times of almost all algorithms in practice: constant, logarithmic, polylogarithmic, square root, linear, linearithmic, quadratic, cubic, exponential and factorial. Each is the [order of growth](/order-of-growth/) of a simple function, and each is $o$ of the next one in the list. This page gives the list with a proof of the order, one real algorithm for each class with its exact count, the effect of a larger input, and the pitfalls of using a class without a model, a case and a measure of input size.

## In plain words

Most algorithms fall into a short list of speeds. Some take the same time for any input. Some grow very slowly, by one step each time the input doubles. Some grow in step with the input, some a little faster, and some with the square or the cube of the input. At the end of the list are the methods that try all subsets or all orders of the items. They work only for a few dozen items.

If you know the class of an algorithm, you know what happens when the input becomes ten or a hundred times larger, and you know if it can work at all for the size you need. The class says nothing about small inputs, and it depends on how you count the size of the input.

## The idea

### The ladder

Write $f \prec g$ when $f(n) = o(g(n))$, that is, $f(n)/g(n) \to 0$. For each two neighbors in the list below, the first is $o$ of the second. The relation is transitive, so it holds for each pair in the list.

$$1 \prec \alpha(n) \prec \lg \lg n \prec \lg n \prec \lg^2 n \prec \sqrt{n} \prec n \prec n \lg n \prec n^2 \prec n^3 \prec 2^n \prec n! \prec n^n$$

Here $\lg^2 n$ means $(\lg n)^2$ and $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/), which tends to infinity but is at most 4 for each $n$ that can occur in practice (CLRS, Chapter 19). The proofs of the steps:

- $1 \prec \alpha(n)$ and $1 \prec \lg \lg n$, because both tend to infinity. That $\alpha(n) \prec \lg \lg n$ follows because $\alpha(n)$ is at most the [iterated logarithm](/iterated-logarithm/) $\lg^* n$ for large $n$, and $\lg^* n \le \lg \lg n$ for large $n$.
- $\lg \lg n \prec \lg n$: put $m = \lg n$. The ratio is $\lg m / m \to 0$.
- $\lg^k n \prec n^\varepsilon$ for each $k$ and each $\varepsilon > 0$, see [comparing growth by limits](/comparing-growth-by-limits/). With $k = 2$ and $\varepsilon = 1/2$ this gives $\lg^2 n \prec \sqrt n$. The other steps up to $n^3$ follow from $n^a \prec n^b$ for $a < b$, and $n \prec n \lg n \prec n^2$ because $\lg n \to \infty$ and $\lg n / n \to 0$.
- $n^3 \prec 2^n$: each polynomial is $o(2^n)$, see [asymptotic notation](/asymptotic-notation/).
- $2^n \prec n!$: $n!/2^n = \prod_{i=1}^{n} (i/2)$ has the factors $1/2$, $1$, $3/2$, and then $n - 3$ factors that are each at least 2. So $n!/2^n \ge (3/4)\,2^{n-3} \to \infty$.
- $n! \prec n^n$: $n!/n^n = \prod_{i=1}^{n} (i/n) \le 1/n$ for $n \ge 2$, because the factor with $i = 1$ is $1/n$ and the others are at most 1.

The base matters for an exponential: $2^n \prec 3^n$, because $(3/2)^n \to \infty$. It does not matter for a logarithm, because $\log_b n = \lg n / \lg b$, see [logarithms](/logarithms/). Graham, Knuth and Patashnik (Section 9.1) give a longer ladder of this kind.

### The classes, with real algorithms

| Class | Function | Algorithm, case and exact count | Page |
| --- | --- | --- | --- |
| Constant | $1$ | Read `A[i]` in an array on the [word RAM](/word-ram/): one memory access | [constant time](/constant-time/) |
| Inverse Ackermann | $\alpha(n)$ | A sequence of $m \ge n$ operations on a [disjoint-set forest](/disjoint-set-forest/) of $n$ items with union by rank and path compression takes $O(m\,\alpha(n))$ time, so $O(\alpha(n))$ amortized per operation (Tarjan, 1975) | none |
| Double logarithmic | $\lg \lg n$ | [Interpolation search](/interpolation-search/) on $n$ keys drawn independently and uniformly: $O(\lg \lg n)$ probes in expectation, and $\Theta(n)$ in the worst case | none |
| Logarithmic | $\lg n$ | [Binary search](/binary-search/) in a sorted array: at most $\lfloor \lg n \rfloor + 1$ probes, 20 for $n = 10^6$ | [logarithmic time](/logarithmic-time/) |
| Polylogarithmic | $\lg^2 n$ | A prefix-sum query in a two-dimensional [Fenwick tree](/fenwick-tree/) of side $n$: $O(\lg^2 n)$ | [polylogarithmic time](/polylogarithmic-time/) |
| Square root | $\sqrt{n}$ | A range-sum query with [square root decomposition](/square-root-decomposition/) into blocks of about $\sqrt n$ items: $O(\sqrt{n})$ | [sublinear time](/sublinear-time/) |
| Linear | $n$ | The maximum of an array: $n - 1$ comparisons on each input | [linear time](/linear-time/) |
| Linearithmic | $n \lg n$ | [Merge sort](/merge-sort/): at most $n \lg n - n + 1$ comparisons for $n$ a power of 2 | [linearithmic time](/linearithmic-time/) |
| Quadratic | $n^2$ | [Insertion sort](/insertion-sort/) on the reversed array: $n(n-1)/2$ shifts | [quadratic time](/quadratic-time/) |
| Cubic | $n^3$ | [Naive matrix multiplication](/naive-matrix-multiplication/) of two $n \times n$ matrices: $n^3$ scalar multiplications | [cubic time](/cubic-time/) |
| Exponential | $2^n$ | Brute-force [subset sum](/subset-sum-problem/) that visits the subsets in [Gray code](/gray-code/) order: $2^n - 1$ steps, each of which adds or removes one item from a running sum | none |
| Exponential, other base | $\varphi^n$ | The plain recursion for the [Fibonacci numbers](/fibonacci-numbers/): $2F(n+1) - 1$ calls, $\Theta(\varphi^n)$ with $\varphi = (1 + \sqrt 5)/2$ | none |
| Factorial | $n!$ | [Heap's algorithm](/heaps-algorithm/) visits all $n!$ orders of $n$ items with $n! - 1$ swaps, one between each two orders | none |

Three notes on the table. First, a program that *prints* all subsets writes $\Theta(n\,2^n)$ symbols in total, and one that prints all orders writes $\Theta(n \cdot n!)$, so the Gray code and Heap's algorithm are the right examples for $2^n$ and $n!$: each step changes one item. Second, the Fibonacci count follows from $C(0) = C(1) = 1$ and $C(n) = 1 + C(n-1) + C(n-2)$. Then $C(n) + 1$ satisfies the Fibonacci recurrence with the start values $2 = 2F(1)$ and $2 = 2F(2)$, so $C(n) + 1 = 2F(n+1)$. This gives 21891 calls for $n = 20$ and 2692537 for $n = 30$. Third, the rows down to the cubic are bounded by a polynomial of fixed degree, so they are [polynomial time](/polynomial-time/). The rows from the exponential on are not.

### When the input grows

Let $T$ be the exact running time. A larger input changes it as follows.

| Class | $T(n)$ | $T(2n)$ | Effect of $n \to n + 1$ |
| --- | --- | --- | --- |
| Constant | $c$ | $T(n)$ | none |
| Logarithmic | $a \lg n$ | $T(n) + a$ | tends to none |
| Square root | $a \sqrt{n}$ | $\sqrt{2}\,T(n)$, about 1.41 times | tends to none |
| Linear | $a n$ | $2 T(n)$ | $+a$ |
| Linearithmic | $a n \lg n$ | $2 T(n)(1 + 1/\lg n)$ | about $+a \lg n$ |
| Quadratic | $a n^2$ | $4 T(n)$ | about $+2an$ |
| Cubic | $a n^3$ | $8 T(n)$ | about $+3an^2$ |
| Exponential | $a\,2^n$ | $2^n\,T(n)$ | $\times 2$ |
| Factorial | $a\,n!$ | $\frac{(2n)!}{n!}\,T(n)$, more than $n^n\,T(n)$ | $\times (n+1)$ |

The factor $(2n)!/n! = (n+1)(n+2) \cdots (2n)$ has $n$ factors that are each larger than $n$. For a power law $T(n) \sim a n^b$, the ratio $T(2n)/T(n)$ tends to $2^b$ ([tilde notation](/tilde-notation/)), which is the basis of the [doubling hypothesis](/doubling-hypothesis/). A bound $\Theta(n^b)$ alone gives only that the ratio stays between two positive constants. For the exponential, the natural step is "add one", not "double".

### What the classes mean in time

Assume $10^9$ simple steps in each second and a running time of exactly $f(n)$ steps.

| $n$ | $n^2$ | $2^n$ | $n!$ |
| --- | --- | --- | --- |
| 20 | 400 steps, 0.4 microseconds | 1048576 steps, about 1.05 milliseconds | $2.43 \times 10^{18}$ steps, about 77 years |
| 50 | 2500 steps, 2.5 microseconds | $1.13 \times 10^{15}$ steps, about 13 days | $3.04 \times 10^{64}$ steps |

The step from $n = 20$ to $n = 50$ costs a factor of 6.25 for the quadratic function, $2^{30} \approx 1.07 \times 10^9$ for the exponential one, and about $1.25 \times 10^{46}$ for the factorial one.

The largest $n$ with $f(n) \le 10^9$, which is one second in this model:

| $f(n)$ | $n$ | $n \lg n$ | $n^2$ | $n^3$ | $2^n$ | $n!$ |
| --- | --- | --- | --- | --- | --- | --- |
| largest $n$ | $10^9$ | 39620077 | 31622 | 1000 | 29 | 12 |

A computer that is 1000 times faster multiplies the first column by 1000, the third by about 31.6 and the fourth by 10, but it adds only about 10 to the column of $2^n$ and 2 to the column of $n!$.

### Pitfalls

- **A class names a function, not an algorithm.** An algorithm has a cost for each case, each model and each measure of input size. Insertion sort is linear in the best case and quadratic in the worst case. Interpolation search is $O(\lg \lg n)$ in expectation on uniform keys and linear in the worst case. The union-find bound is amortized over a sequence. State the case with the class.
- **The model of computation.** "Constant time" for an array access or an addition holds on the word RAM, where a word has about $\lg n$ bits. If numbers grow without a bound, as in repeated squaring, a unit cost for each arithmetic operation hides an exponential number of bit operations. See [unit-cost model](/unit-cost-model/) and [word RAM](/word-ram/).
- **The measure of input size.** The classes depend on what $n$ counts. Naive matrix multiplication is cubic in the side $n$ but $\Theta(N^{3/2})$ in the number $N = n^2$ of entries. An algorithm that is quadratic in the number of vertices of a dense graph is linear in the size of its adjacency matrix. See [input size](/input-size/).
- **Value or length.** A loop that runs up to the value $N$ of a number in the input is linear in $N$ but exponential in the $\lfloor \lg N \rfloor + 1$ bits of $N$. Trial division and the table for subset sum are of this kind. Their times are [pseudo-polynomial](/pseudo-polynomial-time/), not polynomial.
- **Constants and small inputs.** The ladder describes large $n$. An algorithm of a higher class with a small constant can be faster for small inputs, and a library sort uses insertion sort on short ranges for this reason.
- **The ladder is not complete.** There are classes between the rungs, for example $n^{\lg 3}$ for [Karatsuba multiplication](/karatsuba-multiplication/), $n^{\lg 7}$ for Strassen's algorithm, and the [quasi-polynomial](/quasi-polynomial-time/) $n^{\lg n} = 2^{\lg^2 n}$ between the polynomials and $2^n$. Some pairs of functions cannot be compared at all, see [asymptotic notation](/asymptotic-notation/).
- **Constants in exponents count.** $\Theta(\log_2 n) = \Theta(\log_{10} n)$, but $2^n \prec 2^{2n} = 4^n$, and $n^2 \prec n^3$.

## Examples

- Doubling an array of $10^6$ items makes a linear scan take twice as long, a linearithmic sort about $2(1 + 1/\lg 10^6) \approx 2.10$ times as long, and a quadratic comparison of all pairs four times as long.
- A set of 30 items has $2^{30} = 1073741824$ subsets. A brute-force subset sum with the Gray code makes $2^{30} - 1$ updates of the running sum, about one second at $10^9$ steps per second. With 31 items it takes twice as long.
- Brute-force search for the shortest tour through $n$ cities ([traveling salesman problem](/traveling-salesman-problem/)) fixes the first city and tries the $(n-1)!$ orders of the others. With $O(n)$ work for each tour this is $O(n!)$, and for $n = 13$ there are $12! = 479001600$ tours.
- The plain Fibonacci recursion makes 2692537 calls for $n = 30$, while a loop makes 29 additions. The same problem has an exponential and a linear algorithm.
- Non-example: $n^{\lg n} = 2^{\lg^2 n}$ is neither polynomial nor exponential. It is $\omega(n^k)$ for each constant $k$ and $o(2^{\varepsilon n})$ for each constant $\varepsilon > 0$, because $\lg^2 n - \varepsilon n \to -\infty$.
- Non-example: listing all subsets of $n$ items with each subset written out is $\Theta(n\,2^n)$, not $\Theta(2^n)$.

## Where it is used

The ladder is the vocabulary of every page that states a bound, and the page of each class gives its definition, its proofs and its typical algorithms. In design, the ladder tells which improvements matter: a step from $n^2$ to $n \lg n$ changes the largest feasible input from about 31622 to about 40 million at $10^9$ steps, while a faster computer moves the limit of a $2^n$ algorithm only by a few items. In complexity theory, the line between the polynomial rows and the exponential rows is the formal line between feasible and infeasible in the worst case, see [polynomial time](/polynomial-time/).

## References
