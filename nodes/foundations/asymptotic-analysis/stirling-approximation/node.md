---
tag: CZWG27
kind: theorem
slug: stirling-approximation
name: Stirling's approximation
aliases:
- Stirling's formula
area: foundations/asymptotic-analysis
level: core
summary: Gives n! asymptotically as sqrt(2 pi n) (n/e)^n, which yields the log n! = Theta(n log n) bound.
prereqs: [asymptotic-notation, tilde-notation, logarithms, integral-bounds-for-sums]
see_also: [comparison-sort-lower-bound, merge-sort, harmonic-series, factorial, binomial-coefficient-bounds, common-growth-rates]
sources:
  - url: "https://en.wikipedia.org/wiki/Stirling%27s_approximation"
    locator: sections History and Speed of convergence and error estimates
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 3.3, Standard notations and common functions (factorials)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11.2, Euler's summation formula (Stirling's approximation)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 9, Asymptotics (Stirling's approximation)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms (commonly encountered functions)
  - paper: "Herbert Robbins, A remark on Stirling's formula, American Mathematical Monthly 62 (1955), pages 26 to 29"
    locator: the bounds 1/(12n+1) < r_n < 1/(12n)
---

Stirling's approximation says that the [factorial](/factorial/) $n! \sim \sqrt{2\pi n}\,(n/e)^n$: the ratio of the two sides tends to 1 as $n \to \infty$. It turns the product $n!$ into a closed form that you can compare with other functions by [asymptotic notation](/asymptotic-notation/). Its weaker consequence, $\lg(n!) = n \lg n - n \lg e + O(\log n)$, gives the bound $\Omega(n \log n)$ for [comparison sorting](/comparison-sort-lower-bound/).

## Statement

For each integer $n \ge 1$ there is a real number $r_n$ such that
$$ n! = \sqrt{2\pi n}\,\left(\frac{n}{e}\right)^{n} e^{r_n}, \qquad \frac{1}{12n+1} < r_n < \frac{1}{12n}. $$
The upper bound and the positivity of $r_n$ are proved below. The lower bound $\frac{1}{12n+1} < r_n$ is Robbins' (1955). So $n! \sim \sqrt{2\pi n}\,(n/e)^n$ in the sense of [tilde notation](/tilde-notation/), and $\ln n! = n\ln n - n + \tfrac12\ln n + \tfrac12\ln(2\pi) + r_n$. The same asymptotic holds for $\Gamma(x+1)$ as $x \to \infty$ through the reals.

The weaker form has a short proof. For each integer $n \ge 1$,
$$ \left(\frac{n}{e}\right)^{n} \le n! \le e\sqrt{n}\,\left(\frac{n}{e}\right)^{n}, $$
and so $n\ln n - n \le \ln n! \le n\ln n - n + \tfrac12\ln n + 1$. In base 2, with $\lg e = 1.4427\ldots$, we get $n\lg n - n\lg e \le \lg n! \le n\lg n - n\lg e + \tfrac12\lg n + \lg e$.

## In plain words

The number $n!$ is the product of the first $n$ whole numbers. It grows very fast, and the product has no simple form. Stirling's formula gives a simple expression that is close to it. The expression is about the number of items raised to its own power, divided by a power of a fixed constant, times a factor that grows only like the square root of the number.

The formula has two uses. A rough use only needs the size of the logarithm of the product: it is about the number of items times the logarithm of the number of items. This is what the lower bound for sorting needs. A sharp use needs the correction factor too. It says, for example, how many ways there are to choose half of the items, and it does so with a relative error that shrinks as the number of items grows.

## Proof

**Weak form.** We prove $(n/e)^n \le n! \le e\sqrt n\,(n/e)^n$ for each integer $n \ge 1$.

*Lower bound.* The series $e^n = \sum_{k \ge 0} n^k/k!$ has positive terms, so $e^n \ge n^n/n!$. Hence $n! \ge n^n e^{-n} = (n/e)^n$.

*Upper bound.* The function $\ln$ is concave on $(0, \infty)$, so on $[k, k+1]$ it lies above its chord: $\ln x \ge \ln k + (x - k)(\ln(k+1) - \ln k)$. Integrating over $[k, k+1]$ gives $\int_k^{k+1}\ln x\,dx \ge \frac12(\ln k + \ln(k+1))$. Add this for $k = 1, \ldots, n-1$:
$$ \int_1^{n}\ln x\,dx \ge \tfrac12\sum_{k=1}^{n-1}\ln k + \tfrac12\sum_{k=2}^{n}\ln k = \ln n! - \tfrac12\ln n, $$
where we used $\ln 1 = 0$. The integral is $n\ln n - n + 1$. So $\ln n! \le n\ln n - n + 1 + \tfrac12\ln n$, which is the upper bound. $\square$

This is the technique of [integral bounds for sums](/integral-bounds-for-sums/). It shows that $\ln n! = n\ln n - n + O(\log n)$, with the error between $0$ and $1 + \frac12\ln n$.

**Sharp form.** The proof that $r_n$ exists, that $0 < r_n < \frac{1}{12n}$, and that the constant is $\sqrt{2\pi}$ is in [the proof of the sharp form](proofs/stirling-formula.md). It shows that $a_n = \ln n! - (n + \frac12)\ln n + n$ decreases, and that $a_n - \frac{1}{12n}$ increases, so both converge to the same limit. It finds the limit with the Wallis integrals $\int_0^{\pi/2}\sin^m x\,dx$. The lower bound $r_n > \frac1{12n+1}$ is Robbins' result (1955), and the page does not prove it.

## Consequences

**The sorting lower bound.** A comparison sort on $n$ distinct keys needs a [decision tree](/decision-tree-model/) with at least $n!$ leaves, so its worst case is at least $\lceil \lg n!\rceil$ comparisons, see the [comparison sorting lower bound](/comparison-sort-lower-bound/). By the weak form, $\lceil\lg n!\rceil \ge n\lg n - n\lg e \ge n\lg n - 1.4427\,n$. So the bound is $\Omega(n\log n)$. The sharp form gives $\lg n! = n\lg n - n\lg e + \tfrac12\lg n + \tfrac12\lg(2\pi) + O(1/n)$, with $\tfrac12\lg(2\pi) = 1.3257\ldots$.

The table shows the exact value of $\lg n!$, the bound $n\lg n - n\lg e$, and the worst-case comparison count $n\lceil\lg n\rceil - 2^{\lceil\lg n\rceil} + 1$ of [merge sort](/merge-sort/).

| $n$ | $\lg n!$ | $\lceil \lg n! \rceil$ | $n\lg n - n\lg e$ | merge sort, worst case |
| --- | --- | --- | --- | --- |
| 10 | 21.79 | 22 | 18.79 | 25 |
| 100 | 524.76 | 525 | 520.12 | 573 |
| 1000 | 8529.40 | 8530 | 8523.09 | 8977 |
| $10^6$ | 18488884.82 | 18488885 | 18488873.53 | 18951425 |

At $n = 10^6$ merge sort is about 2.5 percent above the lower bound. The gap between $\lg n!$ and $n\lg n - n\lg e$ is $\frac12\lg n + 1.3257 + o(1)$: it is 6.3 at $n = 1000$ and 11.3 at $n = 10^6$.

**$\lg n! = \Theta(n\log n)$.** The upper bound is $\lg n! \le n\lg n$. For the lower bound, $n\lg n - n\lg e \ge \frac12 n\lg n$ exactly when $\lg n \ge 2\lg e$, that is $n \ge e^2 = 7.39\ldots$. So $\frac12 n\lg n \le \lg n! \le n\lg n$ for each $n \ge 8$. The simpler argument for this fact, which does not need Stirling's formula, is on the page of [asymptotic notation](/asymptotic-notation/).

**The central binomial coefficient.** Step 6 and Step 7 of the sharp proof give $\binom{2n}{n} \sim 4^n/\sqrt{\pi n}$. For $n = 10$ this is $187079$ against the true value $184756$. See also [binomial coefficient bounds](/binomial-coefficient-bounds/).

**Orders of growth.** Since $n! \ge (n/e)^n$ and $(n/e)^n/c^n = (n/(ec))^n \to \infty$ for each constant $c$, the factorial grows faster than each exponential $c^n$. Since $n^n/n! \sim e^n/\sqrt{2\pi n} \to \infty$, it also grows slower than $n^n$. So $n! = o(n^n)$, and $n!$ is not $\Theta(n^n)$. For $n = 10$, $n^n/n! = 2755.7$ and $e^n/\sqrt{2\pi n} = 2778.8$.

## Tightness

The constant $\sqrt{2\pi}$ and the exponent $\frac12$ of $n$ cannot change: they are the exact limit. The weak upper bound is off by a bounded factor, but the weak lower bound is not. Its upper bound $e\sqrt n\,(n/e)^n$ exceeds the truth by the factor $e/\sqrt{2\pi} = 1.0844\ldots$ in the limit, and its lower bound $(n/e)^n$ is short by the unbounded factor $\sqrt{2\pi n}$. So the error term $O(\log n)$ in $\ln n! = n\ln n - n + O(\log n)$ cannot be improved to $O(1)$: the true error is $\frac12\ln n + 0.9189\ldots + O(1/n)$.

The error exponent $r_n$ is $\sim \frac{1}{12n}$, by the two-sided bound in the statement. Finer terms are known from the Stirling series:
$$ n! \sim \sqrt{2\pi n}\left(\frac ne\right)^n\left(1 + \frac{1}{12n} + \frac{1}{288n^2} - \frac{139}{51840n^3} + \cdots\right). $$
For $n = 10$ the factor $\sqrt{2\pi n}(n/e)^n$ is $3598695.6$, and $10! = 3628800$. With one, two and three correction terms the value is $3628684.7$, $3628809.7$ and $3628800.05$. The series is asymptotic and does not converge for any $n$.

Two warnings. First, $\sim$ does not mean that the difference is small: $n! - \sqrt{2\pi n}(n/e)^n$ is about $\sqrt{2\pi n}\,(n/e)^n/(12n)$, which grows without bound. Second, $\ln n! \sim n\ln n$ does not give $n! \sim n^n$. Taking a logarithm hides a factor of size $e^{-n}$, as the paragraph on orders of growth shows.

## History

The formula is named for James Stirling, who gave it with the constant $\sqrt{2\pi}$ in his book Methodus Differentialis (1730). Abraham de Moivre found the form $n! \sim C\sqrt n\,(n/e)^n$ with the constant $C$ only as a numerical series (Miscellanea Analytica, 1730). Stirling showed that $C = \sqrt{2\pi}$. Robbins proved the two-sided bound $\frac{1}{12n+1} < r_n < \frac{1}{12n}$ in 1955. Knuth, Volume 1, Section 1.2.11.2, and Graham, Knuth and Patashnik, Chapter 9, derive the formula with the Euler summation formula, and they give the series.

## References
