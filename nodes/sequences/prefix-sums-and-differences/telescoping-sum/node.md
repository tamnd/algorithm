---
tag: C9GGKD
kind: concept
slug: telescoping-sum
name: Telescoping sum
aliases:
- Telescoping sums
- telescoping product
- telescoping series
area: sequences/prefix-sums-and-differences
level: intro
summary: A sum of differences whose interior terms cancel, so the sum equals the difference of the endpoint terms.
prereqs: [induction, asymptotic-notation]
see_also: [prefix-sums, difference-array, discrete-antiderivative, abel-summation, potential-method, finite-differences, harmonic-series, geometric-series]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix A.1, Summation formulas and properties (telescoping series), and Section 16.3, The potential method
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 2.6, Finite and infinite calculus (the sum of a difference is the difference of the endpoint values)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.3, Sums and Products
---

A telescoping sum is a sum of the form $\sum_{k=m}^{n-1} \big(f(k+1) - f(k)\big)$, in which each term cancels part of the next, so that the whole sum equals $f(n) - f(m)$. The name comes from a folding telescope, whose many segments collapse into a short tube. The identity is the discrete form of the fundamental theorem of calculus, it is the reason why [prefix sums](/prefix-sums/) give range sums, and it is the step that turns the amortized costs of the [potential method](/potential-method/) into a bound on the actual cost.

## In plain words

Walk up a staircase and write down, at each step, how much higher you are than at the step before. Add up all these rises. The total is just the height of the top minus the height of the bottom. Every middle step appears twice, once as an end of a rise and once as a start, and the two cancel.

So when a long sum can be written as a list of "new value minus old value", only the first and the last values matter. Finding that way to write a sum is a common trick to get a short exact formula for it. The same idea works for products: a product of "new over old" ratios is the last value over the first.

## The idea

**The identity.** Let $f$ be a function from the integers to a commutative group, for example the real numbers under addition. For integers $m \le n$,

$$\sum_{k=m}^{n-1} \big(f(k+1) - f(k)\big) = f(n) - f(m).$$

*Proof.* By [induction](/induction/) on $n$. For $n = m$ the sum is empty, so it is $0 = f(m) - f(m)$. If the identity holds for $n$, then the sum up to $n$ is $\big(f(n) - f(m)\big) + \big(f(n+1) - f(n)\big) = f(n+1) - f(m)$. $\square$

In the notation of the difference operator, $\Delta f(k) = f(k+1) - f(k)$, the identity reads $\sum_{k=m}^{n-1} \Delta f(k) = f(n) - f(m)$. This is the discrete form of $\int_a^b F'(x)\,dx = F(b) - F(a)$, and $f$ is a [discrete antiderivative](/discrete-antiderivative/) of $\Delta f$.

**How it is used.** To find $\sum_{k=m}^{n-1} g(k)$, look for a function $f$ with $f(k+1) - f(k) = g(k)$. Then the sum is $f(n) - f(m)$. Partial fractions often give such an $f$ for rational $g$.

**Telescoping products.** If $f(k) \ne 0$ for all $k$ with $m \le k \le n$, then

$$\prod_{k=m}^{n-1} \frac{f(k+1)}{f(k)} = \frac{f(n)}{f(m)},$$

by the same induction in the multiplicative group. Taking logarithms of positive values turns a telescoping product into a telescoping sum.

**Telescoping series.** For an infinite series, $\sum_{k=m}^{n-1} (f(k+1) - f(k)) = f(n) - f(m)$ for each $n$, so the series converges if and only if $L = \lim_{n \to \infty} f(n)$ exists, and then $\sum_{k=m}^{\infty} (f(k+1) - f(k)) = L - f(m)$. The partial sums are the only safe way to argue: regrouping the terms of a divergent series can give any answer.

## Examples

**A rational sum.** Since $\frac{1}{k(k+1)} = \frac{1}{k} - \frac{1}{k+1}$, take $f(k) = -1/k$:

$$\sum_{k=1}^{n} \frac{1}{k(k+1)} = 1 - \frac{1}{n+1}.$$

For $n = 10$ the sum is $10/11$. As $n \to \infty$ the series converges to 1.

**A sum of a higher order.** From $\frac{1}{k(k+1)(k+2)} = \frac{1}{2}\left(\frac{1}{k(k+1)} - \frac{1}{(k+1)(k+2)}\right)$,

$$\sum_{k=1}^{n} \frac{1}{k(k+1)(k+2)} = \frac{1}{4} - \frac{1}{2(n+1)(n+2)}.$$

For $n = 10$ this is $\frac14 - \frac{1}{264} = \frac{65}{264}$.

**Factorials.** Since $k \cdot k! = (k+1)! - k!$, the sum $\sum_{k=1}^{n} k \cdot k! = (n+1)! - 1$. For $n = 5$ it is $1 + 4 + 18 + 96 + 600 = 719 = 6! - 1$.

**The sum of the first integers.** Since $(k+1)^2 - k^2 = 2k + 1$, summing over $k = 0, \ldots, n-1$ gives $n^2 = 2 \sum_{k=0}^{n-1} k + n$, so $\sum_{k=0}^{n-1} k = n(n-1)/2$.

**A product.** Since $1 - \frac{1}{k^2} = \frac{k-1}{k} \cdot \frac{k+1}{k}$, the product $\prod_{k=2}^{n} \left(1 - \frac{1}{k^2}\right)$ splits into two telescoping products, $\frac{1}{n}$ and $\frac{n+1}{2}$, so it equals $\frac{n+1}{2n}$. For $n = 10$ this is $\frac{11}{20}$.

**Range sums.** With $P[i] = a[0] + \cdots + a[i-1]$, each item is $a[k] = P[k+1] - P[k]$, so $\sum_{k=l}^{r-1} a[k] = P[r] - P[l]$. This is the whole content of the [prefix sums](/prefix-sums/) technique.

**Non-example.** Grouping the series $1 - 1 + 1 - 1 + \cdots$ as $(1 - 1) + (1 - 1) + \cdots$ gives 0, and as $1 + (-1 + 1) + \cdots$ gives 1. The terms are $(-1)^k = f(k+1) - f(k)$ for $f(k) = -(-1)^k/2$, so the partial sum of the first $n$ terms is $f(n) - f(0) = (1 - (-1)^n)/2$, which alternates between 1 and 0, and $\lim f(n)$ does not exist. So the series diverges, and neither grouping is a sum.

## Where it is used

- **[Prefix sums](/prefix-sums/) and [difference arrays](/difference-array/).** A range sum is a telescoping sum of prefix sums, and an array is a telescoping sum of its differences.
- **The [potential method](/potential-method/).** If the amortized cost of operation $i$ is $\hat c_i = c_i + \Phi(D_i) - \Phi(D_{i-1})$, then $\sum_{i=1}^{n} \hat c_i = \sum_{i=1}^{n} c_i + \Phi(D_n) - \Phi(D_0)$. The potential terms telescope, so a potential with $\Phi(D_n) \ge \Phi(D_0)$ makes the total amortized cost an upper bound on the total actual cost.
- **Analysis of algorithms.** Unrolled recurrences such as $T(n) - T(n-1) = g(n)$ give $T(n) = T(0) + \sum_{k=1}^{n} g(k)$; in the average-case analysis of quicksort, subtracting two instances of the recurrence and dividing by $n(n+1)$ makes it telescope.
- **[Summation by parts](/abel-summation/).** Abel's formula comes from the telescoping of $\Delta(A_k b_k)$.
- **[Discrete antiderivatives](/discrete-antiderivative/).** Finding an $f$ with $\Delta f = g$ is the discrete analogue of integration, and [Gosper's algorithm](/gosper-algorithm/) decides when such an $f$ exists among hypergeometric terms.
- **Bounds on series.** Comparing $1/k^2$ with $\frac{1}{k(k-1)}$ gives $\sum_{k=2}^{\infty} 1/k^2 < 1$ by a telescoping sum; comparisons of this kind bound [harmonic](/harmonic-series/) and related sums.

## References
