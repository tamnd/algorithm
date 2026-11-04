---
tag: 8ASYMP
kind: definition
slug: asymptotic-notation
name: Asymptotic notation
aliases: [big O notation, Landau notation, big Theta, big Omega, little o, little omega]
area: foundations/asymptotic-analysis
level: intro
summary: The notations O, Ω, Θ, o and ω compare the growth of two functions for large inputs and ignore constant factors.
prereqs: []
see_also: [order-of-growth, time-complexity, tilde-notation, comparing-growth-by-limits, multivariate-asymptotic-notation]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 3
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 9.2
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.11.1
  - paper: doi:10.1145/1008328.1008329
    title: Donald E. Knuth, Big Omicron and big Omega and big Theta, SIGACT News 8(2) (1976)
---

Asymptotic notation compares the growth of two functions when the argument becomes large. The statement $f(n) = O(g(n))$ says that $f$ grows at most as fast as $g$, up to a constant factor. $\Omega$ gives a lower bound in the same way, $\Theta$ gives both bounds, and $o$ and $\omega$ give strict bounds. Each cost on this site uses this notation, because it ignores the constant factors that change from one machine and one compiler to another.

## Definition

Let $g$ be a function from the natural numbers to the real numbers that is non-negative for all large $n$. Each notation is a set of functions $f$ that are also non-negative for all large $n$.

$$O(g) = \{ f : \exists c > 0 \ \exists n_0 \ \forall n \ge n_0 : \ f(n) \le c \, g(n) \}$$

$$\Omega(g) = \{ f : \exists c > 0 \ \exists n_0 \ \forall n \ge n_0 : \ f(n) \ge c \, g(n) \}$$

$$\Theta(g) = O(g) \cap \Omega(g)$$

$$o(g) = \{ f : \forall c > 0 \ \exists n_0 \ \forall n \ge n_0 : \ f(n) < c \, g(n) \}$$

$$\omega(g) = \{ f : \forall c > 0 \ \exists n_0 \ \forall n \ge n_0 : \ f(n) > c \, g(n) \}$$

So $f \in \Theta(g)$ when there are constants $c_1, c_2 > 0$ and $n_0$ with $c_1 g(n) \le f(n) \le c_2 g(n)$ for each $n \ge n_0$. The difference between $O$ and $o$ is the quantifier on $c$: for $O$ one constant must work, and for $o$ each constant must work. When $g(n) > 0$ for all large $n$, $f \in o(g)$ exactly when $f(n)/g(n) \to 0$, and $f \in \omega(g)$ exactly when $f(n)/g(n) \to \infty$.

The usual way to write $f \in O(g)$ is $f(n) = O(g(n))$. This "equals" sign is one way only. It means "is a member of", and $O(n) = O(n^2)$ is true while $O(n^2) = O(n)$ is false.

### Notation inside a formula

A notation inside a formula stands for an anonymous function of that set. For example, $T(n) = 2T(n/2) + \Theta(n)$ means that $T(n) = 2T(n/2) + h(n)$ for some function $h \in \Theta(n)$. When notations are on both sides, as in $2n^2 + \Theta(n) = \Theta(n^2)$, the statement means: for each function on the left side, there is a choice on the right side that makes the equation true.

### Rules

These rules follow from the definition. Let $f$, $g$ and $h$ be non-negative for all large $n$.

- **Transitive.** If $f = O(g)$ and $g = O(h)$, then $f = O(h)$. The same rule is true for $\Omega$, $\Theta$, $o$ and $\omega$. Proof for $O$: from $f(n) \le c_1 g(n)$ for $n \ge n_1$ and $g(n) \le c_2 h(n)$ for $n \ge n_2$, we get $f(n) \le c_1 c_2 h(n)$ for $n \ge \max(n_1, n_2)$.
- **Reflexive.** $f = \Theta(f)$, so also $f = O(f)$ and $f = \Omega(f)$.
- **Symmetric.** $f = \Theta(g)$ if and only if $g = \Theta(f)$.
- **Transpose.** $f = O(g)$ if and only if $g = \Omega(f)$, and $f = o(g)$ if and only if $g = \omega(f)$.
- **Constant factors.** $c \cdot f = \Theta(f)$ for each constant $c > 0$.
- **Sums.** $f + g = \Theta(\max(f, g))$. Proof: $\max(f, g) \le f + g \le 2 \max(f, g)$. So a sum of a fixed number of terms has the order of its largest term.
- **Products.** If $f_1 = O(g_1)$ and $f_2 = O(g_2)$, then $f_1 f_2 = O(g_1 g_2)$.
- **Limits.** If $g(n) > 0$ for all large $n$ and $\lim f(n)/g(n) = L$ exists, then $L = 0$ gives $f = o(g)$, $0 < L < \infty$ gives $f = \Theta(g)$, and $L = \infty$ gives $f = \omega(g)$. For $o$ and $\omega$ the converse is also true, but for $\Theta$ it is false: $f = \Theta(g)$ does not need the limit to exist. For example, $f(n) = (2 + (-1)^n) \, n$ is $\Theta(n)$, but $f(n)/n$ alternates between 1 and 3. See [comparing growth by limits](/comparing-growth-by-limits/).

## Examples and non-examples

- $3n^2 + 10n + 7 = \Theta(n^2)$. For the upper bound take $c = 4$: then $3n^2 + 10n + 7 \le 4n^2$ exactly when $n^2 - 10n - 7 \ge 0$, which is true for each $n \ge 11$. For the lower bound take $c = 3$ and $n_0 = 1$.
- $n \lg n = O(n^2)$ and $n \lg n = o(n^2)$, because $\lg n / n \to 0$. Here $\lg n = \log_2 n$, see [logarithms](/logarithms/). So $n \lg n \ne \Omega(n^2)$.
- $\lg(n!) = \Theta(n \log n)$. The upper bound is $n! \le n^n$. For the lower bound, the largest $\lceil n/2 \rceil$ factors of $n!$ are each at least $n/2$, so $\lg(n!) \ge (n/2) \lg(n/2)$, and this is at least $(n \lg n)/4$ for each $n \ge 4$.
- $\log_a n = \Theta(\log_b n)$ for each two bases $a, b > 1$, because $\log_a n = \log_b n / \log_b a$. So $O(\log n)$ needs no base.
- $2^{n+1} = \Theta(2^n)$, because $2^{n+1} = 2 \cdot 2^n$. But $2^{2n} \ne O(2^n)$, because $2^{2n} / 2^n = 2^n \to \infty$. In an exponent, constant factors are important.
- $n^k = o(2^n)$ for each constant $k$, and $(\lg n)^k = o(n^{\varepsilon})$ for each constants $k$ and $\varepsilon > 0$. A polynomial grows slower than an exponential, and a power of a logarithm grows slower than a power of $n$.
- Non-example: $f(n) = n$ and $g(n) = n^{1 + \sin n}$ do not compare. Since $\pi$ is irrational, the values $n \bmod 2\pi$ are dense in $[0, 2\pi)$, so $\sin n \ge 1/2$ for infinitely many $n$ and $\sin n \le -1/2$ for infinitely many $n$. For the first set, $g(n) \ge n^{3/2}$, so $f \ne \Omega(g)$. For the second set, $g(n) \le n^{1/2}$, so $f \ne O(g)$. The [order of growth](/order-of-growth/) is not a total order.
- Non-example: $\Theta(1)$ is not the same as "fast". A step with cost $10^9$ is $\Theta(1)$.

### Common errors

- **O as a tight bound.** "[Merge sort](/merge-sort/) takes $O(n^2)$ time" is true, but it is not useful. Use $\Theta$ when the bound is tight, and $O$ when only the upper bound is known.
- **A worst case is not an upper bound.** $O$, $\Omega$ and $\Theta$ say nothing about which case is analyzed. "The worst-case time of [insertion sort](/insertion-sort/) is $\Omega(n^2)$" and "the best-case time of insertion sort is $O(n)$" are both correct. See [worst-case analysis](/worst-case-analysis/).
- **Constants that depend on $n$.** A proof by induction that "shows" $\sum_{i=1}^{n} i = O(n)$ by the steps $O(n-1) + n = O(n)$ is wrong, because the hidden constant grows at each step. Each step of an induction must use one fixed constant $c$.
- **Two meanings of $\Omega$.** In number theory, $f = \Omega(g)$ often has the meaning of Hardy and Littlewood: $f(n) \ge c \, g(n)$ for infinitely many $n$, not for all large $n$. A paper in number theory and a book on algorithms can use the same symbol for different statements.
- **Small inputs.** An algorithm with time $\Theta(n \log n)$ can be slower than one with time $\Theta(n^2)$ for each input of practical size, when its constant is large. The notation says nothing about a fixed $n$.

## Related definitions

- [Order of growth](/order-of-growth/) is the class $\Theta(g)$ of a function, and the [common growth rates](/common-growth-rates/) put the usual classes in order.
- [Tilde notation](/tilde-notation/) keeps the leading constant: $f \sim g$ means $f(n)/g(n) \to 1$.
- [Asymptotic equivalence](/asymptotic-equivalence/) is the same relation $\sim$, as it is used in analysis.
- [Multivariate asymptotic notation](/multivariate-asymptotic-notation/) applies the notation to costs such as $O(m + n)$ with two variables. The definition with two variables has traps that the definition with one variable does not have.
- [Time complexity](/time-complexity/) and [space complexity](/space-complexity/) are the functions that this notation describes on this site.

### History

Paul Bachmann used the symbol $O$ in 1894 in his book Die analytische Zahlentheorie, and Edmund Landau used it widely from 1909 in his Handbuch der Lehre von der Verteilung der Primzahlen, with the symbol $o$. Hardy and Littlewood used $\Omega$ in 1914 with a different meaning: $f = \Omega(g)$ when $f \ne o(g)$. In 1976 Knuth proposed the meanings of $\Omega$ and $\Theta$ that computer science uses today, in a letter to SIGACT News. TAOCP, Volume 1, Section 1.2.11.1 and the letter of 1976 give this history.

## References
