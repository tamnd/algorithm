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
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 3.3, Standard notations and common functions (polylogarithmically bounded functions, the notation lg^k n)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11.1, The O-notation
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 5, Orthogonal Range Searching (range trees)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity
    locator: Chapter 15, Parallel Computation (the class NC)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 6, Boolean Circuits (the classes NC and AC)
---

An algorithm runs in polylogarithmic time when its worst-case [time](/time-complexity/) is $O((\log n)^k)$ for some constant $k$, where $n$ is the [input size](/input-size/) or, for a data structure, the number of stored items. The class contains [constant time](/constant-time/) and [logarithmic time](/logarithmic-time/), the cases $k = 0$ and $k = 1$. It is a subclass of [sublinear time](/sublinear-time/), because each power of a logarithm grows more slowly than each power $n^{\varepsilon}$ with $\varepsilon > 0$. It is the usual query time of data structures and the parallel time of the class [NC](/nc/).

## Definition

Let $f$ be a function from the positive integers to the non-negative reals. The function $f$ is *polylogarithmic* when there are constants $k \ge 0$, $c > 0$ and $n_0 \ge 2$ such that

$$\forall n \ge n_0 : \ f(n) \le c\,(\lg n)^k.$$

That is, $f(n) = O((\log n)^k)$ for some constant $k$. The threshold $n_0 \ge 2$ keeps $\lg n$ positive. An algorithm runs in *polylogarithmic time* when its worst-case time in a stated model is a polylogarithmic function of $n$. For an expected or amortized bound, the case must be named.

**The model must give random access.** In $O((\log n)^k)$ steps an algorithm reads only a vanishing part of its input. On a Turing machine with one sequential input tape the head cannot even reach position $n$ in fewer than $n - 1$ steps. So the definition needs a [random-access machine](/random-access-machine/), a [word RAM](/word-ram/), or a Turing machine with an index tape that addresses the input. For a data structure, $n$ is the number of stored items, and the bound is the time of one query or update after a preprocessing that reads all $n$ items.

**The union over $k$.** The class is $\bigcup_{k \ge 0} O((\log n)^k)$. Each class is contained in the next one, since $(\lg n)^k \le (\lg n)^{k+1}$ for $n \ge 2$. A real exponent $k$ gives the same union as an integer one, because $(\lg n)^k \le (\lg n)^{\lceil k \rceil}$ for $n \ge 2$.

**The base does not matter.** For bases $a, b > 1$, $(\log_a n)^k = (\log_b n)^k / (\log_b a)^k$, a constant multiple of $(\log_b n)^k$. So $O((\log_a n)^k) = O((\log_b n)^k)$. See [logarithms](/logarithms/).

**Notation.** The expression $\lg^k n$ means $(\lg n)^k$. It does not mean that the logarithm is applied $k$ times: that is the *iterated logarithm* $\lg^{(k)} n$, see [iterated logarithm](/iterated-logarithm/). Also $\lg(n^k) = k \lg n$ is $\Theta(\log n)$, not $(\lg n)^k$. For $n = 2^{20}$, $\lg^2 n = 400$, $\lg(n^2) = 40$ and $\lg \lg n = \lg 20 \approx 4.32$. The function $\lg \lg n$ is polylogarithmic, since $\lg \lg n \le \lg n$ for $n \ge 2$.

**Order.** *Claim.* For each constant $k \ge 0$ and $\varepsilon > 0$, $(\lg n)^k = o(n^{\varepsilon})$.

*Proof.* Put $m = \lg n$, so $n^{\varepsilon} = 2^{\varepsilon m}$, and the ratio is $m^k / 2^{\varepsilon m}$. Let $a_m = m^k / 2^{\varepsilon m}$ for real $m \ge 1$. The ratio $a_{m+1}/a_m = (1 + 1/m)^k \, 2^{-\varepsilon}$ tends to $2^{-\varepsilon} < 1$, so there are $r < 1$ and $M$ with $a_{m+1} \le r\,a_m$ for all $m \ge M$. Then $a_{M + j + t} \le r^j a_{M+t}$ for $t \in [0, 1]$, and $a$ is bounded on $[M, M+1]$, so $a_m \to 0$ as $m \to \infty$. $\square$

The inclusions between the levels are strict: $(\lg n)^{k+1}/(\lg n)^k = \lg n \to \infty$, so $(\lg n)^{k+1} \ne O((\lg n)^k)$.

**Soft-O.** The notation $\tilde O(g(n))$ hides polylogarithmic factors: it means $O(g(n)\,(\log n)^k)$ for some constant $k$. For example, $O(n \lg^2 n)$ is $\tilde O(n)$.

## Examples and non-examples

- **Binary search**, $k = 1$. A search in a sorted array makes at most $\lfloor \lg n \rfloor + 1$ comparisons, which is 20 for $n = 10^6$. See [binary search](/binary-search/).
- **Balanced trees and heaps**, $k = 1$. Search, insertion and deletion in an [AVL tree](/avl-tree/), and insertion in a [binary heap](/binary-heap/), take $O(\log n)$ worst-case time for $n$ stored items.
- **Range trees**, $k = 2$. A two-dimensional range tree on $n$ points in the plane counts the points in an axis-parallel rectangle in $O(\lg^2 n)$ worst-case time, by a search over $O(\log n)$ canonical nodes of the first tree, each followed by a binary search of $O(\log n)$ steps in a sorted array of $y$-coordinates stored at that node. To report the points, the time is $O(\lg^2 n + r)$ for $r$ reported points (de Berg et al., Chapter 5), which is not polylogarithmic when $r$ is large.
- **A two-dimensional [Fenwick tree](/fenwick-tree/)**, $k = 2$. On an $N \times N$ grid, a prefix-sum query or a point update visits at most $\lfloor \lg N \rfloor + 1$ indices in each coordinate, so at most $(\lfloor \lg N \rfloor + 1)^2$ cells.
- **Parallel time.** The sum of $n$ numbers takes $\lceil \lg n \rceil$ rounds when each round adds the numbers in pairs, in parallel, with $\lfloor n/2 \rfloor$ processors in the first round. For $n = 10^6$ this is 20 rounds. The parallel time is $O(\log n)$, while the total work is $n - 1$ additions.
- Non-example: $\sqrt{n}$, or $n^{\varepsilon}$ for a constant $\varepsilon > 0$. These are sublinear and not polylogarithmic, by the claim above.
- Non-example: $n / \lg n$. It is sublinear, but $(n/\lg n)/(\lg n)^k = n / (\lg n)^{k+1} \to \infty$ for each $k$.
- Non-example: $(\lg n)^{\lg n} = n^{\lg \lg n}$. For $n > 2^{k+1}$ the ratio $(\lg n)^{\lg n}/(\lg n)^k = (\lg n)^{\lg n - k}$ is at least $\lg n$, because $\lg n - k > 1$ and $\lg n > 1$, and $\lg n$ grows without bound. It is [quasi-polynomial](/quasi-polynomial-time/).
- Non-example: $2^{\sqrt{\lg n}}$. Its logarithm is $\sqrt{\lg n}$, while the logarithm of $c(\lg n)^k$ is $\lg c + k \lg \lg n$, and $\sqrt{\lg n} - k \lg \lg n \to \infty$.
- Non-example: a time of $\Theta(\log N)$ steps on an input integer $N$. The input size is $\beta = \lfloor \lg N \rfloor + 1$ bits, so this time is $\Theta(\beta)$, linear in the input size and not polylogarithmic in it. Fast exponentiation with $O(\log e)$ multiplications is linear in the length of the exponent $e$. Confusing the value with the length is the same error that turns a [pseudo-polynomial](/pseudo-polynomial-time/) time into a false claim of polynomial time.

### A polylogarithm is not small for every input

Asymptotic notation says nothing about a fixed $n$. Let $\ell = \lg n$.

| $\ell = \lg n$ | $\lg^2 n$ | $\lg^3 n$ | $\sqrt n$ |
| --- | --- | --- | --- |
| 10 | 100 | 1000 | 32 |
| 16 | 256 | 4096 | 256 |
| 20 | 400 | 8000 | 1024 |
| 30 | 900 | 27000 | 32768 |

The ratio $\sqrt n / \lg^2 n = 2^{\ell/2}/\ell^2$ has logarithm $\ell/2 - 2\lg \ell$, whose derivative $1/2 - 2/(\ell \ln 2)$ is positive for $\ell > 4/\ln 2 \approx 5.77$. The ratio is 1 at $\ell = 16$, so $\lg^2 n < \sqrt n$ for each $n > 2^{16} = 65536$. The same computation with $\lg^3 n$ gives the derivative $1/2 - 3/(\ell \ln 2)$, positive for $\ell > 8.66$, and the first integer $\ell$ with $\ell^3 < 2^{\ell/2}$ is 30. So $\lg^3 n < \sqrt n$ only for $n \ge 2^{30}$, about $1.07 \times 10^9$. An $O(\lg^3 n)$ algorithm is not faster than an $O(\sqrt n)$ one on every input of practice, even with equal constants.

## Related definitions

- [Constant time](/constant-time/) is $O(1)$, the case $k = 0$. [Logarithmic time](/logarithmic-time/) is $O(\log n)$, the case $k = 1$.
- [Sublinear time](/sublinear-time/) is $o(n)$ and contains polylogarithmic time. [Polynomial time](/polynomial-time/) is $O(n^k)$ and also contains it.
- The [iterated logarithm](/iterated-logarithm/) $\lg^* n$ and the [inverse Ackermann function](/inverse-ackermann-function/) $\alpha(n)$ grow more slowly than $\lg \lg n$. Both are $O(\log n)$, so both are polylogarithmic.
- $\mathrm{NC}^k$, for $k \ge 1$, is the class of decision problems decided by uniform families of Boolean circuits with fan-in 2, size polynomial in $n$ and depth $O((\log n)^k)$. The class [NC](/nc/) is the union of the $\mathrm{NC}^k$. Its problems are solved in polylogarithmic *parallel* time with polynomially many processors. It is contained in [P](/p/), and whether $\mathrm{NC} = \mathrm{P}$ is open (Papadimitriou, Chapter 15; Arora and Barak, Chapter 6).
- [Common growth rates](/common-growth-rates/) places the polylogarithmic functions between the constants and the powers of $n$.

## References
