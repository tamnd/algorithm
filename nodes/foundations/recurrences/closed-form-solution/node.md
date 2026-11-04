---
tag: 85XAR0
kind: definition
slug: closed-form-solution
name: Closed-form solution
aliases:
- closed form
area: foundations/recurrences
level: intro
summary: A non-recursive expression for the value of a recurrence in terms of n, free of references to earlier values.
prereqs: [recurrence-relation]
see_also: [iteration-method, substitution-method, linear-recurrences-with-constant-coefficients, binet-formula, generating-functions, harmonic-series, asymptotic-notation]
sources:
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 1, Recurrent Problems (Tower of Hanoi and the Josephus problem); Chapter 2, Sums (the notion of a closed form)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 4, Divide-and-Conquer; Appendix A, Summations
  - book: isbn:9780321905758
    title: Robert Sedgewick and Philippe Flajolet, An Introduction to the Analysis of Algorithms, second edition
    locator: Chapter 2, Recurrence Relations
---

A closed-form solution of a [recurrence relation](/recurrence-relation/) is an expression for its $n$-th value that you can evaluate with a fixed number of standard operations, with no reference to earlier values of the sequence and no sum or product whose number of terms grows with $n$. The formula $2^n - 1$ for the Tower of Hanoi recurrence $T_n = 2T_{n-1} + 1$, $T_0 = 0$, is the standard example. A closed form gives the exact value, and from it the [order of growth](/order-of-growth/) and the leading constant.

## Definition

Let $(a_n)_{n \ge n_0}$ be the solution of a recurrence with its initial values. A *closed form* for $a_n$ is an expression $E(n)$ such that

1. $a_n = E(n)$ for each integer $n \ge n_0$, and
2. $E(n)$ is built from $n$ and fixed constants by a fixed, finite number of operations from an agreed set, and this number does not depend on $n$.

The agreed set is a convention, not a theorem. Concrete Mathematics, Chapter 2, uses the informal rule that a closed form is computed by at most a fixed number of "well-known" standard operations, independent of $n$. In the analysis of algorithms the usual set is: the four arithmetic operations, powers and roots, $\exp$ and $\log$, factorials and binomial coefficients, and the floor and ceiling functions. A sum $\sum_{k=1}^{n}$ or a product $\prod_{k=1}^{n}$ whose number of terms grows with $n$ is not allowed: it is itself a recurrence in disguise.

Two remarks make the definition usable.

- **Naming a function enlarges the set.** When a sum without a closed form appears often, it gets a name, and the name is then used as a standard function. The [harmonic number](/harmonic-series/) $H_n = \sum_{k=1}^{n} 1/k$ is the main example. With this convention, $C_n = 2(n+1)H_n - 2n$ is the closed form of the quicksort recurrence $C_n = n + 1 + \frac{2}{n}\sum_{k<n} C_k$, $C_0 = 0$.
- **Exact and asymptotic answers are different.** $\Theta(n \log n)$ and $\sim 2n\ln n$ are asymptotic solutions, not closed forms. They say how fast the sequence grows, but they do not give its values.

A closed form is checked in two steps: compute a few values from the recurrence and from $E(n)$ and compare them, then prove $a_n = E(n)$ for each $n$ by [induction](/induction/), which is the [substitution method](/substitution-method/) with an exact guess. The first step only finds errors. The second step is the proof.

## Examples and non-examples

- **Tower of Hanoi.** $T_0 = 0$, $T_n = 2T_{n-1} + 1$. The closed form is $T_n = 2^n - 1$. Proof: $T_0 = 2^0 - 1$, and $2(2^{n-1} - 1) + 1 = 2^n - 1$.
- **A sum.** $S_0 = 0$, $S_n = S_{n-1} + n$. The closed form is $S_n = n(n+1)/2$, the [arithmetic series](/arithmetic-series/).
- **Fibonacci numbers.** $F_0 = 0$, $F_1 = 1$, $F_n = F_{n-1} + F_{n-2}$. The closed form is [Binet's formula](/binet-formula/) $F_n = (\varphi^n - \psi^n)/\sqrt{5}$ with $\varphi = (1 + \sqrt 5)/2$ and $\psi = (1 - \sqrt 5)/2$. The [characteristic polynomial](/linear-recurrences-with-constant-coefficients/) gives a closed form of this kind for each linear recurrence with constant coefficients.
- **A closed form with floors.** The Josephus problem of Concrete Mathematics, Section 1.3, with every second person removed, has the recurrence $J(1) = 1$, $J(2n) = 2J(n) - 1$, $J(2n+1) = 2J(n) + 1$. Its closed form is $J(n) = 2(n - 2^{\lfloor \lg n \rfloor}) + 1$. For example $J(10) = 5$ and $J(41) = 19$. See [Josephus problem](/josephus-problem/).
- **Merge sort comparisons.** $W(1) = 0$ and $W(n) = W(\lceil n/2 \rceil) + W(\lfloor n/2 \rfloor) + n - 1$ have the closed form $W(n) = n\lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$. For $n = 1000$ this gives $1000 \cdot 10 - 1024 + 1 = 8977$. On powers of 2 it reduces to $n\lg n - n + 1$.
- **Rounding is a standard operation.** $F_n$ is the integer nearest to $\varphi^n/\sqrt 5$ for each $n \ge 0$, because $|\psi^n/\sqrt5| \le 1/\sqrt 5 < 1/2$. This is also a closed form.
- **Non-example: a sum that grows with $n$.** $\sum_{k=1}^{n} 1/k$ is not a closed form in the strict sense. No expression for $H_n$ in the elementary operations above is known, which is why it has its own name and its own asymptotic expansion $H_n = \ln n + \gamma + O(1/n)$.
- **Non-example: an asymptotic bound.** For $T(n) = 2T(\lfloor n/2 \rfloor) + n$ with $T(1) = 1$, the statement $T(n) = \Theta(n \log n)$ is a solution up to constant factors, not a closed form. On powers of 2 the closed form is $T(n) = n\lg n + n$. For other $n$ the floors make the exact form more complex.
- **Non-example: a formula with a hidden recurrence.** "$a_n = 2a_{n-1}$ where $a_{n-1}$ is computed by the same rule" is the recurrence again. An expression that refers to earlier terms is not a closed form, however short.
- **Non-example: a nonlinear recurrence.** The logistic recurrence $x_{n+1} = 4x_n(1 - x_n)$ does have the closed form $x_n = \sin^2(2^n \theta)$ with $x_0 = \sin^2\theta$. But for $x_{n+1} = r x_n(1 - x_n)$ with most values of $r$, no closed form is known. Most nonlinear recurrences have none, and their analysis aims at bounds.

## Related definitions

- A [recurrence relation](/recurrence-relation/) is the object that a closed form solves.
- An asymptotic solution gives the [order of growth](/order-of-growth/) in [asymptotic notation](/asymptotic-notation/), or the leading term in [tilde notation](/tilde-notation/). The [master theorem](/master-theorem/) and the [Akra-Bazzi theorem](/akra-bazzi-theorem/) give asymptotic solutions only.
- The [iteration method](/iteration-method/) unrolls a recurrence into a sum, and a closed form of the sum, as in the [geometric series](/geometric-series/), is then a closed form of the recurrence.
- [Generating functions](/generating-functions/) give closed forms for linear recurrences and for many convolution recurrences, such as the Catalan numbers $\frac{1}{n+1}\binom{2n}{n}$.

## References
