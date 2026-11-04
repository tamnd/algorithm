---
tag: F8QQWD
kind: technique
slug: integral-bounds-for-sums
name: Integral bounds for sums
aliases:
- integral test for sums
- integral method
area: foundations/asymptotic-analysis
level: core
summary: Bounds a sum of a monotone function by comparing it with the integral of that function.
prereqs: [asymptotic-notation, logarithms]
see_also: [harmonic-series, arithmetic-series, geometric-series, stirling-approximation, comparing-growth-by-limits, order-of-growth]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix A, Summations (approximation by integrals)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11.2, Euler's summation formula
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 9, Asymptotics (Euler's summation formula)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms (approximating sums by integrals)
---

Integral bounds for sums is a technique that bounds a sum $\sum_{k=a}^{b} f(k)$ of a monotone function $f$ by the integral $\int_a^b f(x)\,dx$ plus or minus an end term. It turns a sum with no closed form into an integral that you can compute, and it gives the order of growth of the sum, often with its leading constant. It proves that the [harmonic series](/harmonic-series/) is $\Theta(\log n)$, that $\sum k^p = \Theta(n^{p+1})$, and that $\lg n! = n\lg n - O(n)$.

## In plain words

A sum of values of a function is the area of a row of thin bars, one bar for each term. The integral is the area under the curve. If the curve only goes down, then each bar whose height is the value at the left end of its step lies above the curve, and each bar with the value at the right end lies below it. So the row of bars is above the area on one side and below it on the other.

This gives two bounds on the sum. The sum is more than the area by at most one bar, the first or the last. If the sum is large compared with one bar, then the area under the curve is a good estimate of the sum. For a curve that goes up, the same idea holds with the roles of the ends exchanged.

## When it applies

- The terms are $f(k)$ for a function $f$ that is monotone (non-decreasing or non-increasing) on the range of the sum, or that is monotone on a few pieces.
- The function has an integral that you can write in closed form: powers, logarithms, exponentials, and their simple products.
- You want the order of growth, or the leading term, or a bound that holds for every $n$ and not only in the limit.
- It is not the best tool when the terms form an [arithmetic series](/arithmetic-series/) or a [geometric series](/geometric-series/), which have exact closed forms. It is also not suited to a function that oscillates, such as $\sin^2(\pi x)$.

## The template

**Theorem (monotone sum bounds).** Let $a < b$ be integers and let $f$ be a real function that is monotone on $[a, b]$.

- If $f$ is non-increasing, then $\displaystyle f(b) + \int_a^b f(x)\,dx \;\le\; \sum_{k=a}^{b} f(k) \;\le\; f(a) + \int_a^b f(x)\,dx.$
- If $f$ is non-decreasing, then $\displaystyle f(a) + \int_a^b f(x)\,dx \;\le\; \sum_{k=a}^{b} f(k) \;\le\; f(b) + \int_a^b f(x)\,dx.$

In both cases the sum lies between $\int_a^b f + \min(f(a), f(b))$ and $\int_a^b f + \max(f(a), f(b))$, so it differs from the integral by at most $\max(|f(a)|, |f(b)|)$.

*Proof.* A monotone function on a closed interval is Riemann integrable, so the integrals exist. Let $f$ be non-increasing. For each integer $k$ with $a \le k \le b - 1$ and each $x \in [k, k+1]$ we have $f(k+1) \le f(x) \le f(k)$. Integrating over $[k, k+1]$, whose length is 1, gives $f(k+1) \le \int_k^{k+1} f \le f(k)$. Sum over $k = a, \ldots, b-1$. The integrals add to $\int_a^b f$, so
$$ \sum_{k=a+1}^{b} f(k) \;\le\; \int_a^b f \;\le\; \sum_{k=a}^{b-1} f(k). $$
Add $f(a)$ to the left inequality: $\sum_{k=a}^{b} f(k) \le f(a) + \int_a^b f$. Add $f(b)$ to the right inequality: $f(b) + \int_a^b f \le \sum_{k=a}^{b} f(k)$. This is the first claim. If $f$ is non-decreasing, then $-f$ is non-increasing. Apply the first claim to $-f$ and multiply by $-1$. $\square$

**The steps.**

1. Check that $f$ is monotone on the range. If it turns at an interior point, split the range there, and apply the theorem to each piece. The end terms of the pieces add up.
2. Pick the form of the theorem that matches the direction.
3. Compute $\int_a^b f$ in closed form.
4. Read off the order: the sum is $\int_a^b f + O(\max(|f(a)|, |f(b)|))$. If the integral is larger than the end terms by a factor that tends to infinity, then the sum is $\sim \int_a^b f$.
5. Compare with the exact values for a small case to catch a slip in the limits.

The error is at most one end term. When $f$ grows as fast as the sum, as with $2^k$, the end term is a constant fraction of the sum and the method gives only a weak bound. Use a closed form in that case.

## Classic examples

**The harmonic numbers.** The function $f(x) = 1/x$ is decreasing on $[1, n]$. The theorem gives
$$ \ln n + \frac1n \le H_n \le \ln n + 1, $$
since $\int_1^n dx/x = \ln n$, $f(1) = 1$ and $f(n) = 1/n$. So $H_n = \Theta(\log n)$. For $n = 10$: $2.4026 \le H_{10} = 2.9290 \le 3.3026$. For $n = 10^6$: $13.8155 \le H_n = 14.3927 \le 14.8155$. The page on the [harmonic series](/harmonic-series/) sharpens this to $H_n = \ln n + \gamma + O(1/n)$. The same bounds give the order of the average cost of [randomized quicksort](/randomized-quicksort/). When the partition of $m$ keys uses $m-1$ compares, the expected number of compares is $2(n+1)H_n - 4n$, see [expected running time of quicksort](/quicksort-expected-running-time/). The bounds on $H_n$ put it between $2(n+1)\ln n - 4n + 2 + 2/n$ and $2(n+1)\ln n - 2n + 2$, so it is $\Theta(n\log n)$. For $n = 1000$: $9831.3 \le 10985.9 \le 11831.3$.

**Sums of powers.** Let $p > 0$. The function $x^p$ is increasing, and $\int_1^n x^p\,dx = (n^{p+1} - 1)/(p+1)$. The theorem with $f(1) = 1$ and $f(n) = n^p$ gives
$$ \frac{n^{p+1} - 1}{p+1} + 1 \;\le\; \sum_{k=1}^{n} k^p \;\le\; \frac{n^{p+1} - 1}{p+1} + n^p. $$
So $\sum_{k=1}^n k^p = \frac{n^{p+1}}{p+1} + O(n^p)$, and in particular $\sum k^p = \Theta(n^{p+1})$ and $\sum k^p \sim n^{p+1}/(p+1)$. For $p = 2$ and $n = 100$: $333\,334 \le 338\,350 \le 343\,333$, and the exact value is $n(n+1)(2n+1)/6 = 338\,350$. For $p = 1$ the result is the [arithmetic series](/arithmetic-series/), $\sum k = n(n+1)/2 \sim n^2/2$, and it is exact.

For a decreasing power, $-1 < p < 0$, the function $x^p$ is decreasing, and the same steps give $\sum_{k=1}^n k^p = \frac{n^{p+1}}{p+1} + O(1)$. For $p = -\frac12$: $2\sqrt n - 2 + \frac1{\sqrt n} \le \sum_{k=1}^n k^{-1/2} \le 2\sqrt n - 1$, and at $n = 100$ the bounds are $18.1$ and $19$ for the true value $18.59$.

**The logarithm of the factorial.** The function $\lg x$ is increasing, and $\int_1^n \lg x\,dx = n\lg n - n\lg e + \lg e$, where $\lg e = 1.4427\ldots$. With $f(1) = 0$ and $f(n) = \lg n$:
$$ n\lg n - n\lg e + \lg e \;\le\; \lg n! = \sum_{k=1}^{n}\lg k \;\le\; n\lg n - n\lg e + \lg e + \lg n. $$
So $\lg n! = n\lg n - n\lg e + O(\log n) = n\lg n - \Theta(n)$. For $n = 100$ the bounds are $521.56$ and $528.20$, and $\lg 100! = 524.76$. This is the weak form of [Stirling's approximation](/stirling-approximation/). It gives the lower bound $\Omega(n\log n)$ for [comparison sorting](/comparison-sort-lower-bound/), and the page of Stirling's approximation shows how a concave-function argument halves the extra $\lg n$ term of the upper bound.

**A product of a power and a logarithm.** The function $x\ln x$ is increasing for $x \ge 1$, since its derivative is $\ln x + 1 > 0$. Its integral is $\int_1^n x\ln x\,dx = \frac{n^2}{2}\ln n - \frac{n^2}{4} + \frac14$. With $f(1) = 0$ and $f(n) = n\ln n$,
$$ \tfrac{n^2}{2}\ln n - \tfrac{n^2}{4} + \tfrac14 \le \sum_{k=1}^{n} k\ln k \le \tfrac{n^2}{2}\ln n - \tfrac{n^2}{4} + \tfrac14 + n\ln n. $$
So $\sum k\ln k \sim \frac{n^2}{2}\ln n$. For $n = 100$: $20\,526 \le 20\,757 \le 20\,987$.

## Variations

**The integral test.** Let $f \ge 0$ be non-increasing on $[1, \infty)$. Then $\sum_{k=1}^\infty f(k)$ converges if and only if $\int_1^\infty f$ converges. *Proof.* The partial sums are non-decreasing. By the theorem, $\int_1^n f \le \sum_{k=1}^{n} f(k) \le f(1) + \int_1^n f$ (the lower bound uses $f(n) \ge 0$). So the partial sums are bounded exactly when the integrals are bounded. $\square$ With $f = x^{-s}$ this shows that $\sum k^{-s}$ converges when $s > 1$ and diverges when $0 < s \le 1$. For $s \le 0$ the terms do not tend to 0, so the series diverges for a simpler reason. The same bounds give tails: $\sum_{k > n} f(k) \le \int_n^\infty f$. For example $\sum_{k=1}^{n} 1/k^2 \le 1 + \int_1^n x^{-2}dx = 2 - 1/n$, and at $n = 100$ the sum is $1.635$ against the bound $1.99$.

**Concave and convex functions.** Let $f$ be concave on $[a - \frac12, b + \frac12]$. Then $$ \int_{a-1/2}^{b+1/2} f(x)\,dx \;\le\; \sum_{k=a}^{b} f(k) \;\le\; \int_a^b f(x)\,dx + \frac{f(a) + f(b)}{2}. $$ The first inequality comes from the tangent line at $k$, which lies above $f$, so $\int_{k-1/2}^{k+1/2} f \le f(k)$ (the tangent has the value $f(k)$ at the middle of the interval, and its slope term integrates to 0). The second comes from the chord: $\int_k^{k+1} f \ge \frac12(f(k) + f(k+1))$, and the sum of these over $k = a, \ldots, b-1$ gives it. For convex $f$ both inequalities reverse. For $f = \ln$ and $a = 1$, $b = n$ these are $\ln n! \le n\ln n - n + 1 + \frac12\ln n$ and $\ln n! \ge \int_{1/2}^{n+1/2}\ln x\,dx$. For $n = 10$ the bounds are $15.036 \le \ln 10! = 15.104 \le 15.177$. The proof of the upper bound on the page of [Stirling's approximation](/stirling-approximation/) is this chord argument.

**Euler-Maclaurin summation.** The formula of [Euler and Maclaurin](/euler-maclaurin-formula/) writes $\sum_{k=a}^b f(k)$ as $\int_a^b f$ plus $\frac12(f(a) + f(b))$ plus a series of terms with the derivatives of $f$ at the ends, and an exact remainder. It gives as many terms as you need, for example the expansion of $H_n$ and the constant $\gamma$. See Knuth, Volume 1, Section 1.2.11.2, and Concrete Mathematics, Chapter 9.

**Functions with a turning point.** If $f$ is increasing on $[a, c]$ and decreasing on $[c, b]$ for an integer $c$, apply the theorem to each piece. The sum over $[a, b]$ is the sum over the pieces, with the term $f(c)$ counted once. The error is at most the sum of the end terms of the pieces.

## Pitfalls

- **A function that is not monotone.** Take $f(x) = \sin^2(\pi x)$ on $[0, n]$. Then $f(k) = 0$ for each integer $k$, so the sum is 0, but $\int_0^n f = n/2$. The inequalities fail. Check monotonicity on the whole range, or split the range.
- **A function that is not defined or not monotone near the start.** The function $1/x$ is not defined at 0, so a sum that starts at $k = 0$ needs its first term outside the integral. Start the integral at the first index where the function is defined and monotone.
- **Wrong end terms.** The decreasing case has $f(b)$ at the bottom and $f(a)$ at the top, and the increasing case has them the other way. A sketch with two bars catches the swap. Another common slip is the limits of the integral: the form above uses $\int_a^b$ with the end terms added, while the form $\int_{a-1}^{b}$ and $\int_a^{b+1}$ has no end terms but needs $f$ outside $[a, b]$.
- **The error is not small when the terms grow fast.** For $f(k) = 2^k$ and $n = 10$ the bounds are $1476$ and $2498$, while the sum is $2046$. The bounds are correct, but they are loose, because the last term is half of the sum.
- **Mixing a bound with an asymptotic form.** The theorem gives a bound for each $n$ with explicit constants. A statement like $\sum k^p \sim n^{p+1}/(p+1)$ is true for every $p > -1$, but it needs the argument that the end term is $o(n^{p+1})$.
- **Constants from the base of the logarithm.** The integral of $\lg x$ has the factor $\lg e = 1/\ln 2$. With $\ln$ the formula is $n\ln n - n + 1$. Use one base throughout.

## Exercises

1. Bound $\sum_{k=1}^{n} 1/\sqrt{k}$ above and below, and compute the bounds for $n = 100$.
2. Show that $\sum_{k=1}^{n} 1/k^2 \le 2 - 1/n$ for each $n \ge 1$.
3. Show that $\sum_{k=1}^{n} k\lg k = \Theta(n^2\log n)$.
4. Show that $\sum_{k=1}^{n} \lg k = n\lg n - \Theta(n)$ and that $\sum_{k=1}^{n}\frac{1}{k\ln(k+1)}$ diverges.
5. Give a non-monotone $f$ for which the bounds of the theorem fail, and say which hypothesis the proof uses.

<details>
<summary>Hints and answers</summary>

1. The function is decreasing and $\int_1^n x^{-1/2}dx = 2\sqrt n - 2$. So $2\sqrt n - 2 + 1/\sqrt n \le \sum \le 2\sqrt n - 1$. For $n = 100$: $18.1 \le 18.59 \le 19$.
2. The function $x^{-2}$ is decreasing. The upper bound is $1 + \int_1^n x^{-2}dx = 1 + 1 - 1/n$.
3. Use the example of $x\ln x$ above, and the factor $\lg x = \ln x/\ln 2$. The sum is $\sim \frac{n^2}{2}\lg n$.
4. The first follows from the example of $\lg n!$: the bounds differ from $n\lg n$ by about $n\lg e$. For the second, $1/(x\ln(x+1))$ is decreasing and positive, and $\int_1^n \frac{dx}{x\ln(x+1)} \ge \int_1^n \frac{dx}{(x+1)\ln(x+1)} = \ln\ln(n+1) - \ln\ln 2$, which tends to infinity. The integral test then shows divergence.
5. The function $\sin^2(\pi x)$. The proof uses $f(k+1) \le f(x) \le f(k)$ on each interval $[k, k+1]$, which needs monotonicity.

</details>

## References
