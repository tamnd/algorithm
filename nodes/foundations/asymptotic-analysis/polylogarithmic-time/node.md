---
tag: 40MSAP
kind: definition
slug: polylogarithmic-time
name: Polylogarithmic time
aliases:
- polylog time
area: foundations/asymptotic-analysis
level: intro
summary: Running time bounded by a polynomial in log n.
prereqs: [asymptotic-notation, logarithms, time-complexity]
see_also: [logarithmic-time, constant-time, sublinear-time, polynomial-time, iterated-logarithm, nc, binary-search, common-growth-rates]
sources:
  - url: "https://en.wikipedia.org/wiki/Time_complexity"
    locator: section Polylogarithmic time
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 3 (standard notations, polylogarithmically bounded functions)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11.1
  - book: isbn:9780521424264
    title: Arora and Barak, Computational Complexity, A Modern Approach
    locator: Chapter 6 (the class NC)
---

An algorithm runs in polylogarithmic time when its worst-case [time](/time-complexity/) is $O((\log n)^k)$ for some constant $k$, where $n$ is the input size. The class contains [constant time](/constant-time/) and [logarithmic time](/logarithmic-time/), which are the cases $k = 0$ and $k = 1$. It is a subclass of [sublinear time](/sublinear-time/): a power of a logarithm grows more slowly than each power $n^{\varepsilon}$ with $\varepsilon > 0$. It appears in the query time of data structures and in the parallel time of the class [NC](/nc/).

## Definition

Let $f$ be a function from the natural numbers to the non-negative reals. The function $f$ is *polylogarithmic* when there are constants $k \ge 0$, $c > 0$ and $n_0 \ge 2$ such that

$$\forall n \ge n_0 : \ f(n) \le c\,(\lg n)^k.$$

In words, $f(n) = O((\log n)^k)$ for some constant $k$. The threshold $n_0 \ge 2$ keeps $\lg n$ positive. An algorithm runs in *polylogarithmic time* when its worst-case time in a stated model is a polylogarithmic function of the input size.

A polylogarithmic-time algorithm reads only a tiny part of its input, so the model must give random access to the input, for example the [random-access machine](/random-access-machine/) or a Turing machine with random access. A machine with a sequential tape needs $n$ steps just to reach the end of its input. For a data structure, $n$ is the number of stored items: the query time is polylogarithmic in $n$ after a preprocessing that reads all $n$ items.

The class is the union over $k$ of the classes $O((\log n)^k)$, and each class is contained in the next one, since $(\lg n)^k \le (\lg n)^{k+1}$ for $n \ge 2$. A real $k$ gives the same union as an integer $k$, because $(\lg n)^k \le (\lg n)^{\lceil k \rceil}$.

**The base does not matter.** For bases $a, b > 1$, $\log_a n = \log_b n / \log_b a$, so $(\log_a n)^k = (\log_b n)^k / (\log_b a)^k$, which differs from $(\log_b n)^k$ by a constant factor. So $O((\log_a n)^k) = O((\log_b n)^k)$, and the base needs no mention inside $O$. See [logarithms](/logarithms/).

**Notation.** The expression $\lg^k n$ means $(\lg n)^k$, the $k$-th power of the logarithm. It does not mean that the logarithm is applied $k$ times. That function is the *iterated logarithm* $\lg^{(k)} n$ with the number $k$ in parentheses, see [iterated logarithm](/iterated-logarithm/). Also $\log(n^k) = k \log n$ is $\Theta(\log n)$, and it is not $(\log n)^k$. For $n = 2^{20}$ we have $\lg^2 n = 400$, $\lg(n^2) = 40$ and $\lg \lg n = \lg 20 \approx 4.32$. The function $\lg \lg n$ is polylogarithmic, since $\lg \lg n \le \lg n$ for $n \ge 2$.

**Order.** For each constant $k$ and $\varepsilon > 0$, $(\lg n)^k = o(n^{\varepsilon})$, see [asymptotic notation](/asymptotic-notation/). To see this, put $n = 2^m$. Then $(\lg n)^k / n^{\varepsilon} = m^k / 2^{\varepsilon m}$, and this tends to 0 as $m \to \infty$, because an exponential function beats each power of $m$. The class $O((\log n)^k)$ is strictly inside $O((\log n)^{k+1})$, because $(\lg n)^{k+1} / (\lg n)^k = \lg n \to \infty$. So a polylogarithmic function is $o(n^{\varepsilon})$ for every $\varepsilon$, and it is sublinear.

The soft-O notation hides polylogarithmic factors: $\tilde O(f(n))$ means $O(f(n) (\log n)^k)$ for some constant $k$. For example, an $O(n \log^2 n)$ time is $\tilde O(n)$.

## Examples and non-examples

- **Binary search** in a sorted array takes at most $\lfloor \lg n \rfloor + 1$ comparisons. This is $\Theta(\log n)$, so $k = 1$. For $n = 10^6$ it is 20. See [binary search](/binary-search/).
- **Search trees and heaps.** A search, an insertion or a deletion in a balanced search tree such as an [AVL tree](/avl-tree/) takes $O(\log n)$ time, and the insertion in a [binary heap](/binary-heap/) takes $O(\log n)$ time, where $n$ is the number of stored items.
- **Range queries.** A [segment tree](/segment-tree/) or a [Fenwick tree](/fenwick-tree/) answers a range-sum query and takes a point update in $O(\log n)$ time, after a preprocessing of $O(n)$ time, where $n$ is the number of stored items.
- **A power of the logarithm.** A structure with query time $O(\log^2 n)$ is polylogarithmic with $k = 2$. Some structures for range queries in the plane have a query time of this form, where $n$ is the number of stored points.
- **Parallel time.** The sum of $n$ numbers takes $\lceil \lg n \rceil$ rounds when each round adds the numbers in pairs, in parallel, with $\lfloor n/2 \rfloor$ processors in the first round. The parallel time is $O(\log n)$ while the work is $\Theta(n)$.
- Non-example: $\sqrt{n}$, or $n^{\varepsilon}$ for a constant $\varepsilon > 0$. These are sublinear and not polylogarithmic.
- Non-example: $n / \log n$ is sublinear. It is not polylogarithmic, because it is not bounded by $c (\lg n)^k$ for any $k$.
- Non-example: $(\lg n)^{\lg n} = n^{\lg \lg n}$ grows faster than each $(\lg n)^k$, since for $n > 2^{k+1}$ the ratio $(\lg n)^{\lg n} / (\lg n)^k = (\lg n)^{\lg n - k}$ is at least $\lg n$, which grows without bound. It is *quasi-polynomial*, see [quasi-polynomial time](/quasi-polynomial-time/).
- Non-example: $2^{\sqrt{\lg n}}$ is not polylogarithmic. Its logarithm is $\sqrt{\lg n}$, and the logarithm of $c(\lg n)^k$ is $\lg c + k \lg \lg n$, which grows more slowly.
- Non-example: a time that is $\Theta(\log N)$ in the *value* $N$ of the input is linear in the length $b \approx \lg N$ of the input. The input size of an integer $N$ is $b \approx \lg N$ bits, so a time of $\log N$ steps is $\Theta(b)$ and not polylogarithmic in $b$. Fast exponentiation takes $O(\log e)$ multiplications for the exponent $e$, which is linear in the number of bits of $e$.

### A polylogarithm is not small for a small input

Constants and exponents matter for the input sizes of practice. At $n = 2^{16} = 65536$, $\lg^2 n = 256 = \sqrt n$. Let $\ell = \lg n$. Then $\sqrt{n} / \lg^2 n = 2^{\ell/2} / \ell^2$, and the logarithm of this ratio increases when $\ell > 4/\ln 2 \approx 5.77$. The ratio is 1 at $\ell = 16$, so $\lg^2 n < \sqrt n$ for each $n > 2^{16}$. For $n = 2^{20}$ the values are $\lg n = 20$, $\lg^2 n = 400$, $\lg^3 n = 8000$ and $\sqrt n = 1024$, so $\lg^3 n$ is still larger than $\sqrt n$. Asymptotic notation says nothing about a fixed $n$.

## Related definitions

- [Constant time](/constant-time/) is $O(1)$, the case $k = 0$. [Logarithmic time](/logarithmic-time/) is $O(\log n)$, the case $k = 1$.
- [Sublinear time](/sublinear-time/) is $o(n)$ and contains polylogarithmic time. [Polynomial time](/polynomial-time/) is $O(n^k)$ and contains it too.
- The class $\mathrm{NC}$ is the set of problems that are solvable in polylogarithmic *parallel* time with polynomially many processors, in the following circuit form. For $k \ge 1$, $\mathrm{NC}^k$ is the class of decision problems that uniform families of Boolean circuits decide, with fan-in 2, size polynomial in $n$ and depth $O((\log n)^k)$. The class $\mathrm{NC}$ is the union of $\mathrm{NC}^k$ over $k$. It is contained in [P](/p/). It is open whether the two are equal. See [NC](/nc/) and the class P in [polynomial time](/polynomial-time/).
- [Common growth rates](/common-growth-rates/) places the polylogarithmic functions between the constants and the powers of $n$.

## References
