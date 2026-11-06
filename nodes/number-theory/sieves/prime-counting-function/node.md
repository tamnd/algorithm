---
tag: CKKM63
kind: problem
slug: prime-counting-function
name: Prime-counting function
aliases:
- counting primes
- pi function
- pi(x)
- computing pi(x)
area: number-theory/sieves
level: core
summary: pi(x) is the number of primes p <= x. Computing it exactly takes O(x^(2/3) / log^2 x) steps by combinatorial methods and O(x^(1/2 + ε)) by an analytic one, without listing the primes.
model: word-ram
complexity:
  vars: {x: the argument}
  time: {worst: O(x^(1/2 + ε))}
prereqs: [prime-number]
see_also: [primes-up-to-n, legendre-phi-function, meissel-lehmer-algorithm, lucy-hedgehog-prime-counting, prime-number-theorem, sieve-of-eratosthenes, primes-in-range, segmented-sieve]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 3.7, Counting primes (Section 3.7.1 on the combinatorial method and Section 3.7.2 on the analytic method)
  - paper: doi:10.1090/S0025-5718-96-00674-6
    title: M. Deléglise and J. Rivat, Computing pi(x), the Meissel, Lehmer, Lagarias, Miller, Odlyzko method, Mathematics of Computation 65(213), 1996
    locator: Section 1 (the history of the method and the computed values) and Sections 3 to 6 (the algorithm in O(x^(2/3) / log^2 x) time)
  - paper: doi:10.1016/0196-6774(87)90037-X
    title: J. C. Lagarias and A. M. Odlyzko, Computing pi(x), an analytic method, Journal of Algorithms 8(2), 1987
    locator: pages 173 to 191 (the analytic algorithm in O(x^(1/2 + ε)) time and O(x^(1/4 + ε)) space)
  - paper: doi:10.1215/ijm/1255631807
    title: J. Barkley Rosser and Lowell Schoenfeld, Approximate formulas for some functions of prime numbers, Illinois Journal of Mathematics 6(1), 1962
    locator: Theorem 1 and Corollary 1 (x / log x < pi(x) for x >= 17, and pi(x) < 1.25506 x / log x for x > 1)
  - paper: doi:10.1090/S0025-5718-1976-0457374-X
    title: Lowell Schoenfeld, Sharper bounds for the Chebyshev functions theta(x) and psi(x). II, Mathematics of Computation 30(134), 1976
    locator: Corollary 1 (|pi(x) - li(x)| < x^(1/2) log x / (8 pi) for x >= 2657, under the Riemann hypothesis)
---

The prime-counting function $\pi(x)$ is the number of [primes](/prime-number/) $p \le x$, for a real $x$; so $\pi(10) = 4$ and $\pi(100) = 25$. The computational problem is to find $\pi(x)$ exactly for a large $x$ without listing the primes: the [Meissel-Lehmer algorithm](/meissel-lehmer-algorithm/) and its descendants take about $x^{2/3}$ steps, and an analytic method of Lagarias and Odlyzko takes $x^{1/2 + \varepsilon}$, far less than the $x / \ln x$ primes a [sieve](/sieve-of-eratosthenes/) would list. The size of $\pi(x)$ is the subject of the [prime number theorem](/prime-number-theorem/), $\pi(x) \sim x / \ln x$.

## In plain words

Count the primes up to a bound. Up to ten there are four of them: two, three, five and seven. Up to one hundred there are twenty-five.

One way is to list all primes with a sieve and count them, but for a huge bound the list is far too long. The faster methods count without listing. They start from a simple count of the numbers that have no small prime factor, and correct it in clever ways, so the work grows much more slowly than the bound.

The count also has a famous size estimate: up to a bound, about one number in the natural logarithm of the bound is prime.

## Definition

**Input.** A real number $x$; in practice an integer $x \ge 0$, since $\pi(x) = \pi(\lfloor x \rfloor)$.

**Output.** $\pi(x) = \#\{p \le x : p \text{ prime}\}$. So $\pi(x) = 0$ for $x < 2$.

**Cost model.** The [word RAM](/word-ram/) with words of $\Theta(\log x)$ binary digits: arithmetic, comparisons and array access on numbers up to $x$ cost one step. Memory is counted in words. The input has only $\Theta(\log x)$ digits, so all known algorithms are exponential in the input size.

## Variants

- **Listing.** Output the primes themselves: [listing primes up to n](/primes-up-to-n/), which needs at least $\pi(x)$ steps.
- **Primes in an interval.** Count $\pi(R) - \pi(L - 1)$ for an interval, with the [segmented sieve](/segmented-sieve/) when $R - L$ is small.
- **The $n$-th prime.** Find $p_n$, the inverse problem. Estimate it with $p_n \approx n \ln n$, compute $\pi$ there, and sieve the short gap that is left.
- **Prime sums.** Compute $\sum_{p \le x} p$ or $\sum_{p \le x} f(p)$ for a completely multiplicative $f$. [Lucy's method](/lucy-hedgehog-prime-counting/) handles these as easily as $\pi(x)$.
- **Primes in progressions.** Count $\pi(x; q, a)$, the primes $p \le x$ with $p \equiv a \pmod q$.

## Examples

| $x$ | $\pi(x)$ | $x / \ln x$ | $\mathrm{li}(x)$ |
|---|---|---|---|
| 10 | 4 | 4.3 | 6.2 |
| $10^3$ | 168 | 144.8 | 177.6 |
| $10^6$ | 78498 | 72382.4 | 78627.5 |
| $10^9$ | 50847534 | 48254942.4 | 50849235.0 |
| $10^{12}$ | 37607912018 | 36191206825.3 | 37607950280.8 |

Here $\mathrm{li}(x) = \int_0^x dt / \ln t$ is the logarithmic integral, a far better estimate than $x / \ln x$. Meissel computed $\pi(10^9)$ by hand in the nineteenth century and got a value too small by 56, as Deléglise and Rivat report.

## Known algorithms

| algorithm | time (word operations) | memory |
|---|---|---|
| sieve and count, with the [segmented sieve](/segmented-sieve/) | $O(x \log \log x)$ | $O(\sqrt x)$ |
| Legendre's formula with the [Legendre phi function](/legendre-phi-function/) | $O(x)$ | $O(\sqrt x)$ |
| [Lucy's method](/lucy-hedgehog-prime-counting/) | $O(x^{3/4} / \log x)$ | $O(\sqrt x)$ |
| [Meissel-Lehmer algorithm](/meissel-lehmer-algorithm/), as on its page | $O(x^{2/3} \log x)$ | $O(x^{2/3})$ |
| Lagarias, Miller and Odlyzko (1985) | $O(x^{2/3} / \log x)$ | $O(x^{1/3} \log^2 x)$ |
| Deléglise and Rivat (1996) | $O(x^{2/3} / \log^2 x)$ | $O(x^{1/3} \log^3 x \log \log x)$ |
| Lagarias and Odlyzko, analytic (1987) | $O(x^{1/2 + \varepsilon})$ | $O(x^{1/4 + \varepsilon})$ |

All bounds in the table are proved and depend on no conjecture; the analytic method uses the zeros of the Riemann zeta function, but its error control is rigorous. Both kinds of method have been used for record computations; the combinatorial ones are much simpler to implement.

## Bounds

**On the value.** Chebyshev proved that $\pi(x)$ has order $x / \log x$, and Hadamard and de la Vallée Poussin proved in 1896 that $\pi(x) \sim x / \ln x$, the [prime number theorem](/prime-number-theorem/). Explicit bounds with no conjecture are known: Rosser and Schoenfeld proved $x / \ln x < \pi(x)$ for $x \ge 17$ and $\pi(x) < 1.25506 \, x / \ln x$ for $x > 1$. The best possible error term depends on the Riemann hypothesis: if it holds, then $|\pi(x) - \mathrm{li}(x)| < \sqrt x \ln x / (8 \pi)$ for $x \ge 2657$ (Schoenfeld). For $x = 10^{12}$ this bound is about $1.1 \cdot 10^6$, and the true error is about $3.8 \cdot 10^4$.

**On the computation.** The best proved upper bound is $O(x^{1/2 + \varepsilon})$. No lower bound beyond reading the input is known, so it is open whether $\pi(x)$ can be computed in time polynomial in $\log x$.

## Reductions

- **From listing.** Any algorithm for [listing primes up to n](/primes-up-to-n/) gives $\pi(n)$ by counting, at the cost of the listing.
- **Through the Legendre function.** $\pi(x) = \phi(x, a) + a - 1 - P_2(x, a) - P_3(x, a) - \cdots$, where $a = \pi(y)$ for some $y$, $\phi(x, a)$ counts the $n \le x$ with no prime factor among the first $a$ primes, and $P_k$ counts those with exactly $k$ prime factors, all larger. With $y \ge x^{1/3}$ only $P_2$ is needed. This is the start of the [Meissel-Lehmer algorithm](/meissel-lehmer-algorithm/); see the [Legendre phi function](/legendre-phi-function/).
- **To the $n$-th prime.** The $n$-th prime reduces to $O(1)$ evaluations of $\pi$ near $n \ln n$ and a sieve of a short interval.

## Applications

- Checking the [prime number theorem](/prime-number-theorem/) and the Riemann hypothesis numerically, and finding where $\pi(x)$ and $\mathrm{li}(x)$ compare.
- Finding the $n$-th prime for large $n$.
- Counting problems in programming contests, such as the number of primes or the sum of primes up to $10^{11}$ or more.

## References
