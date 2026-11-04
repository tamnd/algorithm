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
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 9, Asymptotics
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11 (Asymptotic representations)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4 (tilde notation)
---

Two functions $f$ and $g$ are asymptotically equivalent, written $f \sim g$, when the relative error $|f - g|/|g|$ of $g$ as an approximation of $f$ tends to zero. For functions that are not zero for large arguments, this means that the ratio $f(n)/g(n)$ tends to 1. The relation is an [equivalence relation](/equivalence-relation/), and it is finer than [$\Theta$](/asymptotic-notation/): it fixes the constant factor. This page treats the relation as a tool of analysis. The use of the same relation to state the cost of an algorithm is in [tilde notation](/tilde-notation/).

## Definition

Let $f, g : \mathbb{N} \to \mathbb{R}$. Then $f \sim g$ means
$$\forall \varepsilon > 0 \ \exists n_0 \ \forall n \ge n_0 : \ |f(n) - g(n)| \le \varepsilon \, |g(n)|.$$
Equivalent forms:

- If $g(n) \ne 0$ for all large $n$: $\lim_{n \to \infty} f(n)/g(n) = 1$.
- $f = g \, (1 + o(1))$, that is, $f(n) = g(n)(1 + \delta(n))$ with $\delta(n) \to 0$.
- $f = g + o(g)$, where $o(g)$ stands for a function of the class [$o(g)$](/asymptotic-notation/) in absolute value.

The form with $\varepsilon$ also covers functions that are zero at some points. In that form $f \sim 0$ holds exactly when $f(n) = 0$ for all large $n$.

### It is an equivalence relation

It is enough to consider $\varepsilon \in (0, 1]$, because a larger $\varepsilon$ gives a weaker condition.

- Reflexive: $|f - f| = 0 \le \varepsilon |f|$.
- Symmetric: let $f \sim g$. Given $\varepsilon \in (0,1]$, take $n_0$ for $\varepsilon/2$, so that $|f - g| \le (\varepsilon/2)|g|$ for $n \ge n_0$. Then $|g| \le |f| + (\varepsilon/2)|g|$, so $|g| (1 - \varepsilon/2) \le |f|$, and since $1 - \varepsilon/2 \ge 1/2$ we get $|g| \le 2|f|$. Hence $|f - g| \le (\varepsilon/2) |g| \le \varepsilon |f|$. This is $g \sim f$.
- Transitive: let $f \sim g$ and $g \sim h$. Given $\varepsilon \in (0,1]$, take $\delta = \varepsilon/3$ and $n_0$ such that $|f - g| \le \delta |g|$ and $|g - h| \le \delta |h|$ for $n \ge n_0$. Then $|g| \le (1 + \delta)|h|$, and $|f - h| \le |f - g| + |g - h| \le \delta(1+\delta)|h| + \delta |h| = \delta (2 + \delta) |h| \le 3\delta |h| = \varepsilon |h|$.

### Rules

Let $f_1 \sim g_1$ and $f_2 \sim g_2$, where $g_1$ and $g_2$ are non-zero for all large $n$. Write $r_i = f_i / g_i$, so $r_i \to 1$.

- **Products and quotients.** $f_1 f_2 \sim g_1 g_2$, because $f_1 f_2 / (g_1 g_2) = r_1 r_2 \to 1$. Also $f_1/f_2 \sim g_1/g_2$, because $f_2 \ne 0$ for large $n$ (as $r_2 \to 1$) and $(f_1/f_2)/(g_1/g_2) = r_1/r_2 \to 1$.
- **Powers.** If $f_1$ and $g_1$ are positive for large $n$, then $f_1^c \sim g_1^c$ for each real $c$, because $r_1^c \to 1$ by continuity of $x \mapsto x^c$ at $1$. For example, $\sqrt{n^2 + n} \sim n$.
- **Sums.** If all four functions are non-negative, then $f_1 + f_2 \sim g_1 + g_2$ (proof in [tilde notation](/tilde-notation/)). This fails when the signs differ. We have $n^2 + n \sim n^2$ and $-n^2 \sim -n^2$, but the sum of the left sides is $n$, the sum of the right sides is $0$, and $n \not\sim 0$. Differences fail for the same reason.
- **Exponentials.** For real functions, $e^{f} \sim e^{g}$ if and only if $f - g \to 0$, because $e^{f}/e^{g} = e^{f - g}$, and $e^x \to 1$ exactly when $x \to 0$. So $f \sim g$ does not give $e^f \sim e^g$. Example: $n + \sqrt{n} \sim n$, but $e^{n + \sqrt{n}}/e^{n} = e^{\sqrt{n}} \to \infty$. A second example: $\ln\left((1 + 1/n)^{n^2}\right) = n^2 \ln(1 + 1/n) = n - 1/2 + O(1/n)$ by the series $\ln(1+x) = x - x^2/2 + O(x^3)$, so $(1 + 1/n)^{n^2} \sim e^{n - 1/2}$, which is not $\sim e^n$ (the ratio tends to $e^{-1/2} \approx 0.607$).
- **Logarithms.** For positive functions, $f \sim g$ if and only if $\ln f - \ln g \to 0$ (the same fact as for exponentials, since $\ln$ and $\exp$ are continuous and inverse). So, if $f \sim g$ and $g(n) \to \infty$, then $\ln f = \ln g + o(1)$ and $\ln f \sim \ln g$. The converse is false: $\ln 2^{n+1} \sim \ln 2^n$ but $2^{n+1} \not\sim 2^n$.
- **Substitution into the argument.** If $f \sim g$ and $h : \mathbb{N} \to \mathbb{N}$ has $h(n) \to \infty$, then $f(h(n)) \sim g(h(n))$. Given $\varepsilon$, take $n_0$ from the definition. Then $h(n) \ge n_0$ for large $n$, and the condition holds at the point $h(n)$.
- **Limits and orders.** If $f \sim g$ and $g(n) \to L$ for some $L \in [-\infty, \infty]$, then $f(n) \to L$, since $f = g(1 + \delta)$ with $\delta \to 0$. A constant $c \ne 0$ satisfies $f \sim c$ exactly when $f \to c$. If $g$ is eventually positive, then $f = \Theta(g)$, and $f$ and $g$ lie in the same classes $O(h)$, $\Omega(h)$, $o(h)$ for each $h$. The converse is false: $2n = \Theta(n)$, but $2n \not\sim n$. Also, $f \sim g$ bounds the relative error and not the absolute error. It does not imply $f - g \to 0$: $n + \sqrt{n} \sim n$, but the difference $\sqrt{n}$ tends to infinity.

## Examples and non-examples

- **Polynomials.** A polynomial is equivalent to its leading term: $a_k n^k + \cdots + a_0 \sim a_k n^k$ when $a_k \ne 0$. The sum of squares is $\sum_{i=1}^{n} i^2 = n(n+1)(2n+1)/6 \sim n^3/3$, because $(1 + 1/n)(1 + 1/(2n)) \to 1$. At $n = 10$ the ratio is $385/(1000/3) = 1.155$.
- **Harmonic numbers.** $H_n = \sum_{k=1}^{n} 1/k \sim \ln n$. Proof: comparing the sum with the integral of $1/x$ gives $\ln(n+1) \le H_n \le 1 + \ln n$ (see [harmonic series](/harmonic-series/)). Divide by $\ln n$, for $n \ge 2$. The left side is $1 + \ln(1 + 1/n)/\ln n \to 1$ and the right side is $1 + 1/\ln n \to 1$, so the ratio tends to 1. The convergence is slow, because $H_n = \ln n + \gamma + o(1)$ with $\gamma \approx 0.5772$: the ratio $H_n / \ln n$ is $1.042$ at $n = 10^6$.
- **Stirling.** $n! \sim \sqrt{2\pi n}\,(n/e)^n$ (see [Stirling's approximation](/stirling-approximation/)). The ratio is $1.0084$ at $n = 10$ and $1.00083$ at $n = 100$. By the log rule, since $\sqrt{2\pi n}\,(n/e)^n \to \infty$, $\ln n! \sim \ln\left(\sqrt{2\pi n}\,(n/e)^n\right) = n \ln n - n + \tfrac12 \ln(2\pi n) \sim n \ln n$.
- **Central binomial coefficient.** $\binom{2n}{n} \sim 4^n/\sqrt{\pi n}$. Proof: by Stirling and the product and quotient rules, $\binom{2n}{n} = (2n)!/(n!)^2 \sim \sqrt{4\pi n}\,(2n/e)^{2n} / \left(2\pi n\,(n/e)^{2n}\right) = 2^{2n} \cdot 2\sqrt{\pi n}/(2\pi n) = 4^n/\sqrt{\pi n}$. At $n = 100$ the ratio of the two sides is $0.99875$.
- **Prime number theorem.** The number $\pi(x)$ of primes up to $x$ satisfies $\pi(x) \sim x/\ln x$ (see the [prime number theorem](/prime-number-theorem/)). The convergence is slow: the ratio is $1.160$ at $x = 10^3$ ($168$ primes), $1.104$ at $x = 10^5$ and $1.071$ at $x = 10^7$ ($664579$ primes).
- **A limit of a function.** $(1 + 1/n)^n \sim e$, because the sequence tends to $e \ne 0$.
- **Non-examples.** $2n^2 \not\sim n^2$ (the ratio tends to 2). $\log_2 n \not\sim \ln n$ (the ratio tends to $1/\ln 2$). The function $(2 + \sin n)\,n$ is $\Theta(n)$ and is equivalent to no function $c\,n$ with a constant $c$, because the ratio $(2 + \sin n)/c$ does not converge to 1.

## Related definitions

- [Tilde notation](/tilde-notation/) is the same relation used to state the cost of an algorithm with its leading constant.
- [$\Theta$ notation](/asymptotic-notation/) says that $f/g$ stays between two positive constants. Equivalence says that the ratio tends to 1. Little-$o$ gives the error term: $f \sim g$ if and only if $f - g \in o(g)$.
- [Comparing growth by limits](/comparing-growth-by-limits/) gives the limit tests that decide $f \sim g$, $f = o(g)$ and $f = \Theta(g)$.
- An asymptotic expansion refines $\sim$ with more terms, for example $H_n = \ln n + \gamma + O(1/n)$. Concrete Mathematics, Chapter 9, treats such expansions.
- [Order of growth](/order-of-growth/) is the class of functions that are $\Theta$ of one another. It is coarser than $\sim$.

## References
