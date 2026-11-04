---
tag: A5TSSS
kind: technique
slug: comparing-growth-by-limits
name: Comparing growth by limits
aliases:
- limit comparison of functions
area: foundations/asymptotic-analysis
level: core
summary: Decides the asymptotic relation between two functions by evaluating the limit of their ratio.
prereqs: [asymptotic-notation, order-of-growth, logarithms]
see_also: [common-growth-rates, tilde-notation, asymptotic-equivalence, stirling-approximation, integral-bounds-for-sums]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 3, Characterizing Running Times (asymptotic notation and its limit characterizations)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11.1, The O-notation
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 9, Asymptotics
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms
---

Comparing growth by limits is a technique that decides how two functions $f$ and $g$ compare in [asymptotic notation](/asymptotic-notation/) by computing the limit of $f(n)/g(n)$ as $n \to \infty$. A limit of 0 gives $f = o(g)$, a limit of $\infty$ gives $f = \omega(g)$, and a finite positive limit gives $f = \Theta(g)$. When the limit does not exist, the $\limsup$ and the $\liminf$ of the ratio still decide $O$, $\Omega$ and $\Theta$ exactly. The technique turns questions about the [order of growth](/order-of-growth/) into calculus.

## In plain words

To compare two cost functions, divide one by the other and look at what happens to the quotient when the input gets very large. If the quotient shrinks to nothing, the top function is smaller in the long run, and by any factor you like. If the quotient grows without limit, the top function is larger. If the quotient settles near a positive number, the two functions grow at the same speed and differ only by a constant factor.

A quotient may also swing up and down for ever. Then the two functions do not compare in the simple way, but the largest and the smallest values that the quotient keeps reaching still tell you the upper and the lower bound.

## When it applies

- You have two explicit functions of the input size, both positive for large inputs, and you want $o$, $O$, $\Theta$, $\Omega$ or $\omega$.
- The ratio can be simplified by algebra, or it has a known limit. Typical cases are polynomials, powers of logarithms, exponentials, and factorials.
- You want to place a function on the ladder of [common growth rates](/common-growth-rates/), for example to show that it is above every polynomial.
- It does not apply when the functions are not given by a formula, for example when only bounds on a recurrence are known. Then use the definition with constants $c$ and $n_0$, or a theorem on recurrences.

## The template

Let $f, g$ be real functions on the positive integers with $f(n) > 0$ and $g(n) > 0$ for all large $n$.

**Step 1.** Form the ratio $\rho(n) = f(n)/g(n)$ and simplify it. Cancel common factors. For polynomials divide by the highest power. For logarithms in different bases convert to one base, see [logarithms](/logarithms/).

**Step 2.** Find $\lim_{n\to\infty}\rho(n)$ if it exists. Use, in this order, algebra, known limits, L'Hôpital's rule on a real variable, the ratio test for sequences, or a logarithm of both sides.

**Step 3.** Read the result with the rule below.

**The limit rule.** Suppose $\lim_{n\to\infty} f(n)/g(n) = L$ with $L \in [0, \infty]$.

- If $L = 0$ then $f = o(g)$, and so $f = O(g)$ and $f \ne \Omega(g)$.
- If $0 < L < \infty$ then $f = \Theta(g)$.
- If $L = \infty$ then $f = \omega(g)$, and so $f = \Omega(g)$ and $f \ne O(g)$.

**The converses.** For $f, g$ eventually positive, the first and the third lines are equivalences. That is, $f = o(g)$ holds exactly when the limit exists and equals 0, and $f = \omega(g)$ holds exactly when the limit is $\infty$. For eventually positive functions these are equivalent to the definitions of $o$ and $\omega$ with constants, as the proof below shows. The second line is not an equivalence. If $f = \Theta(g)$, the limit need not exist. What is true is this: if $f = \Theta(g)$ and the limit exists, then $0 < L < \infty$.

**The exact criteria without a limit.** For $f, g$ eventually positive, let $\rho = f/g$. Then
$$ f = O(g) \iff \limsup_{n\to\infty}\rho(n) < \infty, \qquad f = \Omega(g) \iff \liminf_{n\to\infty}\rho(n) > 0, $$
and so $f = \Theta(g) \iff 0 < \liminf\rho \le \limsup\rho < \infty$.

*Proof.* Suppose $f = O(g)$ with constants $c, n_0$: $\rho(n) \le c$ for $n \ge n_0$. Then $\limsup\rho \le c < \infty$. Conversely, if $S = \limsup\rho < \infty$, then $\rho(n) \le S + 1$ for all large $n$, which is the definition of $O(g)$ with $c = S+1$. For $\Omega$: if $f(n) \ge c\,g(n)$ for $n \ge n_0$, with $c > 0$, then $\liminf\rho \ge c > 0$. Conversely, if $I = \liminf\rho > 0$ (possibly $\infty$), then $\rho(n) \ge \min(I, 1)/2 > 0$ for all large $n$. The criterion for $\Theta$ is the two together. $\square$

*Proof of the limit rule.* The line $L=0$ says: for each $\varepsilon > 0$ there is $n_0$ with $\rho(n) < \varepsilon$ for $n \ge n_0$. This is $f(n) < \varepsilon g(n)$, which is the definition of $f = o(g)$. The line $L = \infty$ says: for each $c > 0$ there is $n_0$ with $\rho(n) > c$ for $n \ge n_0$, which is the definition of $f = \omega(g)$. If $0 < L < \infty$, then $\limsup\rho = \liminf\rho = L$, so $f = \Theta(g)$ by the criterion above. The claims on $O$ and $\Omega$ follow in the same way: $f \ne \Omega(g)$ when $L = 0$ because $\liminf\rho = 0$, and $f \ne O(g)$ when $L = \infty$ because $\limsup\rho = \infty$, by the criterion above. $\square$

## Classic examples

**A power of a logarithm against a power of $n$.** For constants $k \ge 1$ and $\varepsilon > 0$, $(\lg n)^k = o(n^{\varepsilon})$. The base of the logarithm gives only a constant factor, so we use $\ln$ and the real variable $x$. Apply L'Hôpital's rule $k$ times to $(\ln x)^k / x^\varepsilon$. At each step the numerator and denominator tend to $\infty$, and the derivative of the denominator is not 0:
$$ \frac{(\ln x)^k}{x^{\varepsilon}} \to \frac{k(\ln x)^{k-1}}{\varepsilon\, x^{\varepsilon}} \to \cdots \to \frac{k!}{\varepsilon^k x^{\varepsilon}} \to 0. $$
So $(\lg n)^k = o(n^{\varepsilon})$ for each such $k$ and $\varepsilon$. The limit is 0 for each fixed $\varepsilon$, but it may be reached late. For $k = 3$ and $\varepsilon = \frac12$: $(\lg n)^3 \ge \sqrt n$ for all $n$ from 3 to $621\,201\,921$, and $(\lg n)^3 < \sqrt n$ for larger $n$. At $n = 10^6$, $(\lg n)^3 = 7\,918$ and $\sqrt n = 1\,000$.

**A polynomial against an exponential.** For constants $k$ and $c > 1$, $n^k = o(c^n)$. Let $a_n = n^k/c^n$. Then $a_{n+1}/a_n = (1 + 1/n)^k / c \to 1/c < 1$. Choose $q$ with $1/c < q < 1$. Then $a_{n+1} \le q\,a_n$ for all $n \ge N$, so $a_n \le a_N q^{n-N} \to 0$. For $k = 10$ and $c = 2$: $2^n > n^{10}$ holds for each $n \ge 59$ (at $n = 58$, $2^{58} = 2.88 \times 10^{17}$ is less than $58^{10} = 4.31 \times 10^{17}$, and at $n = 59$ it is $5.76 \times 10^{17}$ against $5.11 \times 10^{17}$). From 59 on it stays true, because each step multiplies $2^n$ by 2 and $n^{10}$ by at most $(60/59)^{10} \approx 1.18$.

**The factorial against $n^n$ and against $c^n$.** For $n^n$: $n!/n^n = \prod_{j=1}^{n} (j/n)$. The factor $j = 1$ is $1/n$, and the other factors are at most 1, so $n!/n^n \le 1/n \to 0$ and $n! = o(n^n)$. The ratio test gives more: $a_n = n!/n^n$ has $a_{n+1}/a_n = (n/(n+1))^n \to 1/e$. With [Stirling's approximation](/stirling-approximation/), $n!/n^n \sim \sqrt{2\pi n}\,e^{-n}$, which is $3.60 \times 10^{-4}$ at $n = 10$ (the exact value is $3.63 \times 10^{-4}$). For $c^n$: $c^n/n!$ has successive ratio $c/(n+1) \to 0$, so $c^n/n! \to 0$ and $c^n = o(n!)$ for every constant $c$.

**Same order, different constants.** Take $f(n) = 3n^2 + 10n + 7$ and $g(n) = n^2$. Dividing by $n^2$ gives $3 + 10/n + 7/n^2 \to 3$. So $f = \Theta(g)$, and also $f \sim 3g$ in [tilde notation](/tilde-notation/). The limit is the constant of the tilde, which $\Theta$ alone hides.

**Taking logarithms of both sides.** To compare $n^{\lg n}$ with $2^n$ look at $\lg(f/g) = \lg f - \lg g = \lg^2 n - n$, which tends to $-\infty$. So $f/g \to 0$ and $n^{\lg n} = o(2^n)$. The step is exact because $\lg$ is increasing and $f/g = 2^{\lg f - \lg g}$.

**No limit.** Let $f(n) = (2 + \sin n)\,n$ and $g(n) = n$. The ratio $2 + \sin n$ has no limit. Since $\pi$ is irrational, $n \bmod 2\pi$ is dense in $[0, 2\pi)$ (as used on the page of [asymptotic notation](/asymptotic-notation/)), so $\limsup\rho = 3$ and $\liminf\rho = 1$. By the criterion, $f = \Theta(g)$, although the limit does not exist. For $f(n) = n$ and $g(n) = n^{1+\sin n}$ we have $\rho(n) = n^{-\sin n}$, with $\limsup\rho = \infty$ and $\liminf\rho = 0$. So $f \ne O(g)$ and $f \ne \Omega(g)$.

## Variations

**L'Hôpital's rule.** Let $a \in \mathbb R$ and let $f, g$ be differentiable on $(a, \infty)$ with $g'(x) \ne 0$ there. Assume that either $f(x) \to 0$ and $g(x) \to 0$, or $|g(x)| \to \infty$. If $f'(x)/g'(x) \to L$ with $L \in [-\infty, \infty]$ as $x \to \infty$, then $f(x)/g(x) \to L$. Restricting $x$ to the integers gives the same limit for $f(n)/g(n)$. The rule needs three checks: a real variable with differentiable extensions of the functions, a form $0/0$ or $\cdot/\infty$, and the existence of the limit of $f'/g'$.

**The ratio test for sequences.** Let $a_n > 0$. If $a_{n+1}/a_n \to \rho$ with $\rho < 1$, then $a_n \to 0$ (shown above). If $\rho > 1$, then $a_n \to \infty$ by the same argument applied to $1/a_n$. If $\rho = 1$, the test says nothing: $a_n = 1/n$ and $a_n = n$ both have $\rho = 1$. The ratio test works for functions such as $n!$ that have no natural derivative.

**Stirling's approximation.** For ratios that contain $n!$ and $\binom{2n}{n}$ the sharp form $n! \sim \sqrt{2\pi n}\,(n/e)^n$ turns the ratio into a ratio of elementary terms. The relation $\sim$ may be used inside a limit of a ratio, but not inside a difference.

**Dominant term for sums.** For a sum of a fixed number of terms from a ladder, divide by the growth function of the largest term, without its coefficient (for $3n^2 + 10n$, divide by $n^2$). Each other term over it tends to 0, so the quotient tends to the leading coefficient.

## Pitfalls

- **Dividing by zero or by a negative number.** The rule needs $f$ and $g$ positive for large $n$. For a function that may be 0 or negative, work with $|f|$, or say what you mean.
- **Treating $\Theta$ as an equivalence of limits.** The limit can fail to exist and $f = \Theta(g)$ can still hold, as in the example $(2 + \sin n)n$. A proof of "the limit does not exist, so $f \ne \Theta(g)$" is wrong. Use $\limsup$ and $\liminf$.
- **Mixing up $\Theta$ and $\sim$.** A limit of 1 gives $f \sim g$. A finite positive limit that is not 1 gives $\Theta$ but not $\sim$. Also $2^{n+1}/2^n = 2$, so $2^{n+1} = \Theta(2^n)$ but $2^{n+1} \not\sim 2^n$.
- **L'Hôpital without its conditions.** The converse is false: $f(x) = x + \sin x$ and $g(x) = x$ have $f/g \to 1$, but $f'/g' = 1 + \cos x$ has no limit. So if $f'/g'$ has no limit, the rule gives no information. Also, the rule does not apply to $(x+1)/(2 + 1/x)$, which tends to $\infty$ and has a denominator that tends to 2. Applying it anyway gives $1/(-1/x^2) = -x^2 \to -\infty$, which is wrong. The rule applies to functions of a real variable, not to a sequence like $n!$.
- **Logarithms hide constants and powers.** From $\ln f \sim \ln g$ you cannot conclude anything about $f/g$: $\ln(n\lg n) \sim \ln n$, but $n\lg n \ne O(n)$. Use $\ln f - \ln g$, as in the example above.
- **A small limit is not a small ratio at a given size.** $\lim(\lg n)^3/\sqrt n = 0$, yet the ratio is at least 1 for every $n$ from 3 to about $6.2 \times 10^8$. The limit tells you the order, not where the crossing happens.
- **Using a limit as a proof of a running time.** The limit compares two given functions. It does not tell you that the function is the cost of the algorithm.

## Exercises

1. Compare $n^2 \lg n$ and $n^{5/2}$.
2. Show that $\sqrt{n}\,\lg n = o(n)$ and give the limit of the ratio.
3. Show that $n^{\lg n}$ is not $O(n^{100})$, and that it is $o(2^n)$.
4. Find $f, g$ such that $f/g$ has no limit but $f = \Theta(g)$, and $f, g$ such that $f'/g'$ has no limit but $f/g$ has one.
5. Show that $2^n = o(n!)$ and compute the least $n$ at which $2^n < n!$.

<details>
<summary>Hints and answers</summary>

1. The ratio $n^2\lg n/n^{5/2} = \lg n/\sqrt n \to 0$ by the first classic example with $k=1$ and $\varepsilon = \frac12$. So $n^2\lg n = o(n^{5/2})$.
2. The ratio is $\lg n/\sqrt n \to 0$, so $\sqrt n\lg n = o(n)$.
3. For $n^{100}$: $\lg(n^{\lg n}/n^{100}) = \lg^2 n - 100\lg n \to \infty$, so $n^{\lg n} = \omega(n^{100})$ and it is not $O(n^{100})$. For $2^n$ see the example above.
4. The pair $(2+\sin n)\,n$ and $n$ for the first. The pair $x + \sin x$ and $x$ for the second.
5. The ratio $2^n/n!$ has successive ratio $2/(n+1) \to 0$. Since $2^3 = 8 > 6 = 3!$ and $2^4 = 16 < 24 = 4!$, the least $n$ with $2^n < n!$ is 4, and after that $2^n < n!$ for all $n \ge 4$, because each step multiplies $n!$ by $n+1 \ge 5$ and $2^n$ by 2.

</details>

## References
