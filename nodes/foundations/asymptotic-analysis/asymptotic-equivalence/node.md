---
tag: 6FJR1J
kind: definition
slug: asymptotic-equivalence
name: Asymptotic equivalence
aliases:
- f ~ g
area: foundations/asymptotic-analysis
level: core
summary: Two functions are asymptotically equivalent when their ratio tends to one.
prereqs: [asymptotic-notation]
see_also: [tilde-notation, order-of-growth, comparing-growth-by-limits, stirling-approximation, harmonic-series, prime-number-theorem]
sources:
  - book: isbn:9780486642215
    title: N. G. de Bruijn, Asymptotic Methods in Analysis, Dover edition
    locator: Chapter 1, Introduction (the symbols O, o and ~)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 9, Asymptotics
  - book: isbn:9780321905758
    title: Robert Sedgewick and Philippe Flajolet, An Introduction to the Analysis of Algorithms, second edition
    locator: Chapter 4, Asymptotic Approximations
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms (tilde approximations)
---

Two functions $f$ and $g$ are asymptotically equivalent, written $f \sim g$, when the relative error $|f - g|/|g|$ of $g$ as an approximation of $f$ tends to zero. For functions that are non-zero for large arguments, this means that the ratio $f(n)/g(n)$ tends to 1. The relation is an [equivalence relation](/equivalence-relation/), and it is finer than [$\Theta$](/asymptotic-notation/): it fixes the constant factor. This page treats the relation as a tool of analysis, with its rules and their limits. The use of the same relation to state the cost of an algorithm is [tilde notation](/tilde-notation/).

## Definition

Let $f, g : \mathbb{N} \to \mathbb{R}$. Then $f \sim g$ means
$$\forall \varepsilon > 0 \ \exists n_0 \ \forall n \ge n_0 : \ |f(n) - g(n)| \le \varepsilon \, |g(n)|.$$
Three equivalent forms are in use.

- **Ratio.** If $g(n) \ne 0$ for all large $n$: $\lim_{n \to \infty} f(n)/g(n) = 1$. Divide the inequality by $|g(n)|$: it says $|f(n)/g(n) - 1| \le \varepsilon$, which is the definition of the limit.
- **Factor.** $f = g\,(1 + \delta)$ with $\delta(n) \to 0$. When $g(n) \ne 0$ put $\delta = f/g - 1$, and when $g(n) = 0$ the definition forces $f(n) = 0$ for $n \ge n_0$, so any $\delta(n)$ works there, for example $0$.
- **Error term.** $f - g \in o(g)$, where $o(g)$ is read with absolute values: $|f - g| \le \varepsilon|g|$ for large $n$, for each $\varepsilon > 0$. This is the definition word for word.

The form with $\varepsilon$ also covers functions with zeros. In that form $f \sim 0$ holds exactly when $f(n) = 0$ for all large $n$, since the condition is $|f(n)| \le 0$.

### It is an equivalence relation

It is enough to treat $\varepsilon \in (0, 1]$, because a larger $\varepsilon$ gives a weaker condition.

- **Reflexive.** $|f - f| = 0 \le \varepsilon |f|$.
- **Symmetric.** Let $f \sim g$ and $\varepsilon \in (0,1]$. Take $n_0$ for $\varepsilon/2$, so that $|f - g| \le (\varepsilon/2)|g|$ for $n \ge n_0$. Then $|g| \le |f| + |g - f| \le |f| + (\varepsilon/2)|g|$, so $|g|(1 - \varepsilon/2) \le |f|$. Since $1 - \varepsilon/2 \ge 1/2$, this gives $|g| \le 2|f|$. Hence $|f - g| \le (\varepsilon/2)|g| \le \varepsilon |f|$, which is $g \sim f$.
- **Transitive.** Let $f \sim g$ and $g \sim h$, and let $\varepsilon \in (0,1]$. Put $\delta = \varepsilon/3$, and take $n_0$ with $|f - g| \le \delta |g|$ and $|g - h| \le \delta |h|$ for $n \ge n_0$. Then $|g| \le (1 + \delta)|h|$, and $|f - h| \le |f - g| + |g - h| \le \delta(1+\delta)|h| + \delta |h| = \delta (2 + \delta) |h| \le 3\delta |h| = \varepsilon |h|$, because $\delta \le 1$.

### Rules

Let $f_1 \sim g_1$ and $f_2 \sim g_2$. Where a rule uses ratios, $g_1$ and $g_2$ are non-zero for all large $n$, and $r_i = f_i / g_i \to 1$.

- **Products and quotients.** $f_1 f_2 \sim g_1 g_2$, because the ratio is $r_1 r_2 \to 1$. Also $f_1/f_2 \sim g_1/g_2$: since $r_2 \to 1$, $f_2 \ne 0$ for large $n$, and the ratio is $r_1/r_2 \to 1$.
- **Powers.** If $f_1$ and $g_1$ are positive for large $n$, then $f_1^c \sim g_1^c$ for each real constant $c$, because $r_1^c \to 1$ by the continuity of $x \mapsto x^c$ at 1. For example, $\sqrt{n^2 + n} \sim n$. The exponent must be a constant: $n + 1 \sim n$, but $(n+1)^n/n^n = (1 + 1/n)^n \to e$.
- **Sums of non-negative functions.** If $g_1, g_2 \ge 0$ for large $n$, then $f_1 + f_2 \sim g_1 + g_2$. *Proof.* For large $n$, $|f_i - g_i| \le \varepsilon g_i$. Adding gives $|(f_1 + f_2) - (g_1 + g_2)| \le \varepsilon (g_1 + g_2)$. $\square$ Only $g_1$ and $g_2$ need a sign condition. The rule fails when the signs differ: $n^2 + n \sim n^2$ and $-n^2 \sim -n^2$, but the sums are $n$ and $0$, and $n \not\sim 0$. Differences fail for the same reason.
- **Exponentials.** For real functions, $e^{f} \sim e^{g}$ if and only if $f - g \to 0$, because $e^{f}/e^{g} = e^{f - g}$, and $e^x \to 1$ exactly when $x \to 0$. So $f \sim g$ does not give $e^f \sim e^g$. For example, $n + \sqrt{n} \sim n$, but $e^{n + \sqrt{n}}/e^{n} = e^{\sqrt{n}} \to \infty$. A second example: by the series $\ln(1+x) = x - x^2/2 + O(x^3)$, we get $n^2 \ln(1 + 1/n) = n - \frac12 + O(1/n)$, so $(1 + 1/n)^{n^2} \sim e^{n - 1/2}$. It is not $\sim e^n$: the ratio tends to $e^{-1/2} = 0.6065\ldots$
- **Logarithms.** For positive functions, $f \sim g$ if and only if $\ln f - \ln g \to 0$, by the exponential rule applied to $\ln f$ and $\ln g$. So, if $f \sim g$ and $g(n) \to \infty$, then $\ln f = \ln g + o(1)$, and $\ln f \sim \ln g$. The converse is false: $\ln 2^{n+1} \sim \ln 2^n$, but $2^{n+1} \not\sim 2^n$.
- **Substitution into the argument.** If $f \sim g$ and $h : \mathbb{N} \to \mathbb{N}$ has $h(n) \to \infty$, then $f(h(n)) \sim g(h(n))$. Given $\varepsilon$, take $n_0$ from the definition. Then $h(n) \ge n_0$ for large $n$, and the inequality holds at the point $h(n)$.
- **Limits.** If $f \sim g$ and $g(n) \to L$ for some $L \in [-\infty, \infty]$, then $f(n) \to L$, since $f = g(1 + \delta)$ with $\delta \to 0$. A constant $c \ne 0$ satisfies $f \sim c$ exactly when $f \to c$.
- **Orders of growth.** If $f \sim g$ and $g$ is positive for large $n$, then $\frac12 g \le f \le 2g$ for large $n$, so $f = \Theta(g)$. Hence $f$ and $g$ lie in the same classes $O(h)$, $\Omega(h)$, $o(h)$ and $\omega(h)$ for each $h$. The converse is false: $2n = \Theta(n)$, but $2n \not\sim n$.

## Examples and non-examples

The numbers below are computed with exact integers or with double precision, and rounded.

- **Polynomials.** A polynomial with leading coefficient $a_k \ne 0$ is equivalent to its leading term: $(a_k n^k + \cdots + a_0)/(a_k n^k) = 1 + \sum_{j<k} (a_j/a_k)\,n^{j-k} \to 1$. The sum of squares is $\sum_{i=1}^{n} i^2 = n(n+1)(2n+1)/6 \sim n^3/3$, because the ratio is $(1 + 1/n)(1 + 1/(2n)) \to 1$. At $n = 10$ the ratio is $385/(1000/3) = 1.155$.
- **Harmonic numbers.** $H_n = \sum_{k=1}^{n} 1/k \sim \ln n$. *Proof.* Comparison with the integral of $1/x$ gives $\ln(n+1) \le H_n \le 1 + \ln n$ (see [harmonic series](/harmonic-series/)). For $n \ge 2$ divide by $\ln n$. The lower ratio is $\ln(n+1)/\ln n \ge 1$, and the upper ratio is $1 + 1/\ln n \to 1$. So $H_n/\ln n \to 1$. $\square$ The convergence is slow, because $H_n - \ln n \to \gamma = 0.5772\ldots$, and the error is $\gamma/\ln n$ in relative terms: the ratio is $1.272$ at $n = 10$, $1.084$ at $n = 1000$ and $1.042$ at $n = 10^6$.
- **Stirling.** $n! \sim \sqrt{2\pi n}\,(n/e)^n$ (see [Stirling's approximation](/stirling-approximation/)). The ratio is $1.00837$ at $n = 10$ and $1.00083$ at $n = 100$. By the logarithm rule, $\ln n! \sim n\ln n - n + \frac12\ln(2\pi n) \sim n\ln n$.
- **Central binomial coefficient.** $\binom{2n}{n} \sim 4^n/\sqrt{\pi n}$. *Proof.* By Stirling and the rules for products and quotients, $\binom{2n}{n} = (2n)!/(n!)^2 \sim \sqrt{4\pi n}\,(2n/e)^{2n} / \left(2\pi n\,(n/e)^{2n}\right) = 4^{n} \cdot 2\sqrt{\pi n}/(2\pi n) = 4^n/\sqrt{\pi n}$. $\square$ The ratio of the two sides is $0.98758$ at $n = 10$ ($184\,756$ against $187\,079$) and $0.99875$ at $n = 100$.
- **Prime number theorem.** The number $\pi(x)$ of primes up to $x$ satisfies $\pi(x) \sim x/\ln x$ (see the [prime number theorem](/prime-number-theorem/)). The convergence is slow: the ratio is $1.160$ at $x = 10^3$ (168 primes), $1.104$ at $x = 10^5$ (9592 primes) and $1.071$ at $x = 10^7$ (664579 primes).
- **A limit of a sequence.** $(1 + 1/n)^n \sim e$, because the sequence tends to $e \ne 0$.
- **Non-examples.** $2n^2 \not\sim n^2$ (the ratio tends to 2). $\lg n \not\sim \ln n$ (the ratio is the constant $1/\ln 2 = 1.4427\ldots$). The function $(2 + \sin n)\,n$ is $\Theta(n)$ but is equivalent to no $c\,n$, because $(2 + \sin n)/c$ has no limit. The function $n$ is not equivalent to $n + (-1)^n n/2$, since the ratio alternates between $2/3$ and $2$.

### Pitfalls

- **Subtracting equivalents.** From $f \sim g$ you cannot conclude $f - h \sim g - h$. To find the second term of an expansion, compute the difference exactly, or use a form with an explicit error, such as $H_n = \ln n + \gamma + O(1/n)$.
- **Exponentiating equivalents.** $f \sim g$ does not give $e^f \sim e^g$ or $2^f \sim 2^g$. A tilde in an exponent needs the absolute error $f - g \to 0$.
- **Equivalence of logarithms.** $\ln f \sim \ln g$ is a much weaker statement than $f \sim g$. For example $\ln(n^2) \sim \ln(3n^2)$, while the ratio $3n^2/n^2$ is 3.
- **Dividing by a function with zeros.** The ratio form needs $g(n) \ne 0$ for large $n$. If $g$ has zeros at infinitely many $n$, use the form with $\varepsilon$, which then forces $f = 0$ at the same points.
- **Reading $\sim$ as a small difference.** $n + \sqrt n \sim n$, but the difference $\sqrt n$ tends to infinity. Equivalence bounds the relative error only.

## Related definitions

- [Tilde notation](/tilde-notation/) is the same relation used to state the cost of an algorithm with its leading constant.
- [$\Theta$ notation](/asymptotic-notation/) says that $f/g$ stays between two positive constants. Equivalence says that the ratio tends to 1. Little-$o$ gives the error term: $f \sim g$ if and only if $f - g \in o(g)$.
- [Comparing growth by limits](/comparing-growth-by-limits/) gives the limit tests that decide $f \sim g$, $f = o(g)$ and $f = \Theta(g)$.
- An asymptotic expansion refines $\sim$ with more terms and an explicit error, for example $H_n = \ln n + \gamma + \frac{1}{2n} + O(n^{-2})$. Concrete Mathematics, Chapter 9, and de Bruijn, Chapter 1, treat such expansions.
- [Order of growth](/order-of-growth/) is the class of functions that are $\Theta$ of one another. It is coarser than the class of functions equivalent to a given one.

## References
