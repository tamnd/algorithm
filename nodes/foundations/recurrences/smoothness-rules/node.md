---
tag: T46K7R
kind: theorem
slug: smoothness-rules
name: Smoothness rules
aliases:
- smoothness condition
area: foundations/recurrences
level: advanced
summary: Rules that justify ignoring floors and ceilings in the arguments of a recurrence whose driving function is smooth.
prereqs: [asymptotic-notation, divide-and-conquer-recurrence, induction]
see_also: [master-theorem, akra-bazzi-theorem, iteration-method, substitution-method, merge-sort, binary-search]
sources:
  - book: isbn:9780133350685
    title: Gilles Brassard and Paul Bratley, Fundamentals of Algorithmics
    locator: Section 3.4, Conditional asymptotic notation (smooth functions and the smoothness rule); Problem 3.29
  - book: isbn:9780132316811
    title: Anany Levitin, Introduction to the Design and Analysis of Algorithms, third edition
    locator: Appendix B, Short Tutorial on Recurrence Relations (smooth functions and the smoothness rule)
  - url: "https://courses.csail.mit.edu/6.046/spring04/handouts/akrabazzi.pdf"
    locator: Tom Leighton, Notes on Better Master Theorems for Divide-and-Conquer Recurrences, MIT, October 9, 1996 (the polynomial-growth condition and Theorem 2)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 4, Divide-and-Conquer (algorithmic recurrences, floors and ceilings)
---

The smoothness rules let you solve a recurrence only for $n$ a power of a base $b$, where floors and ceilings disappear, and then conclude the same order of growth for every $n$. The main rule says: if $t$ is eventually non-decreasing, $f$ is smooth (eventually non-decreasing with $f(2n) = O(f(n))$), and $t(n) = \Theta(f(n))$ for $n$ a power of $b$, then $t(n) = \Theta(f(n))$ for all $n$. The rule is due in this form to Brassard and Bratley, and it is the usual justification for the phrase "assume that $n$ is a power of 2".

## Statement

All functions map the natural numbers to the non-negative reals.

**Definitions.**

- $f$ is *eventually non-decreasing* if there is an $n_0$ such that $f(n) \le f(n+1)$ for each $n \ge n_0$.
- For an integer $b \ge 2$, $f$ is *$b$-smooth* if it is eventually non-decreasing and $f(bn) = O(f(n))$.
- $f$ is *smooth* if it is $b$-smooth for each integer $b \ge 2$.
- For an integer $b \ge 2$, $t(n) = \Theta(f(n) \mid n \text{ a power of } b)$ means that there are constants $c, d > 0$ and $k_0$ such that $c f(b^k) \le t(b^k) \le d f(b^k)$ for each $k \ge k_0$. The same conditional form is used with $O$ and $\Omega$.

**Lemma (one base is enough).** If $f$ is $b$-smooth for one integer $b \ge 2$, then $f$ is smooth.

**Smoothness rule.** Let $b \ge 2$ be an integer, $f$ smooth, and $t$ eventually non-decreasing. If $t(n) = \Theta(f(n) \mid n \text{ a power of } b)$, then $t(n) = \Theta(f(n))$. The same holds with $O$ in place of $\Theta$ in both places, and with $\Omega$ in place of $\Theta$ in both places.

Levitin defines smoothness with $f(2n) = \Theta(f(n))$. For an eventually non-decreasing $f$ this is the same condition, since $f(2n) \ge f(n)$ for large $n$ holds anyway.

## In plain words

Recurrences with halving are easy to solve when the input size is a power of two, because the halves are always whole numbers. For other sizes, the rounding up and down makes the exact answer messy. The rule tells you when the messy sizes cannot behave differently.

Two conditions are needed. First, the true cost must never go down when the input grows, which is true for the running time of most algorithms. Second, the answer you found must not jump when the input doubles. Under these conditions, each size sits between two powers of two, its cost sits between their costs, and those two costs differ by at most a constant factor. So the answer for powers of two holds for all sizes, up to a constant factor.

## Proof

### The lemma

Let $f$ be $b$-smooth: $f(n) \le f(n+1)$ for $n \ge n_0$, and $f(bn) \le C f(n)$ for $n \ge n_1$. Let $c \ge 2$ be an integer, and let $i$ be such that $b^i \ge c$. For $n \ge \max(n_0, n_1)$,

$$f(cn) \le f(b^i n) \le C f(b^{i-1} n) \le \cdots \le C^i f(n).$$

The first step uses that $f$ is non-decreasing from $n_0$ on and $cn \le b^i n$; the other steps apply $f(bm) \le C f(m)$ at $m = b^{i-1}n, \ldots, n$, each at least $n_1$. So $f(cn) = O(f(n))$, and $f$ is $c$-smooth. $\square$

### The rule

Choose $n_0$ such that $t$ and $f$ are non-decreasing on $[n_0, \infty)$, $f(bm) \le D f(m)$ for $m \ge n_0$, and the conditional bounds $c f(b^k) \le t(b^k) \le d f(b^k)$ hold for $b^k \ge n_0$. Let $n \ge b n_0$, and let $k$ be the integer with $b^k \le n < b^{k+1}$. Then $b^k > n/b \ge n_0$.

*Upper bound.* Since $t$ and $f$ are non-decreasing from $n_0$ on,

$$t(n) \le t(b^{k+1}) \le d f(b^{k+1}) = d f(b \cdot b^k) \le dD f(b^k) \le dD f(n).$$

*Lower bound.* In the same way, $f(n) \le f(b^{k+1}) \le D f(b^k)$, so

$$t(n) \ge t(b^k) \ge c f(b^k) \ge \frac{c}{D} f(n).$$

Hence $\frac{c}{D} f(n) \le t(n) \le dD f(n)$ for each $n \ge b n_0$, that is, $t(n) = \Theta(f(n))$. The upper bound uses only the $O$ half of the hypothesis and the lower bound only the $\Omega$ half, which proves the $O$ and $\Omega$ versions. $\blacksquare$

The smoothness of $f$ is used only for the base $b$ of the hypothesis. The lemma shows that the definition does not depend on this base.

## Consequences

### Merge sort for each n

Let $W(1) = 0$ and $W(n) = W(\lceil n/2 \rceil) + W(\lfloor n/2 \rfloor) + n - 1$ for $n \ge 2$, the worst-case number of comparisons of [merge sort](/merge-sort/).

1. *On powers of 2.* $W(2^k) = 2W(2^{k-1}) + 2^k - 1$, and the [iteration method](/iteration-method/) gives $W(n) = n\lg n - n + 1$. So $W(n) = \Theta(n\log n \mid n \text{ a power of } 2)$.
2. *$W$ is non-decreasing.* By strong induction on $n$: $W(1) = 0 \le W(2) = 1$, and for $n \ge 2$ the arguments satisfy $\lceil n/2 \rceil \le \lceil (n+1)/2 \rceil$ and $\lfloor n/2 \rfloor \le \lfloor (n+1)/2 \rfloor$, all at most $n$, so by the induction hypothesis $W(n+1) - W(n) \ge (n + 1 - 1) - (n - 1) = 1 > 0$.
3. *$n\lg n$ is smooth.* It is increasing, and $2n\lg(2n) = 2n\lg n + 2n \le 4n\lg n$ for $n \ge 2$.

By the rule, $W(n) = \Theta(n\log n)$ for each $n$. The exact value $W(n) = n\lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$ shows how the lower-order term varies. Write $n = 2^{\lceil \lg n \rceil} u$ with $\frac12 < u \le 1$; then $W(n) = n\lg n - \theta n + 1$ with $\theta = \frac1u + \lg u$. On $(\frac12, 1]$, $\theta$ is smallest at $u = \ln 2$, where it equals $\frac{1}{\ln 2} + \lg\ln 2 \approx 0.9139$, and largest, 1, at $u = 1$ and as $u \to \frac12$. The order is the same for each $n$, while the coefficient of $n$ oscillates.

### Binary search

$T(1) = 1$ and $T(n) = T(\lfloor n/2 \rfloor) + 1$ give $T(2^k) = k + 1$ and a non-decreasing $T$ (the same induction), and $\lg n$ is smooth, since $\lg(2n) = \lg n + 1 \le 2\lg n$ for $n \ge 2$. So $T(n) = \Theta(\log n)$; the exact value is $\lfloor \lg n \rfloor + 1$.

### Master theorem on powers of b

The cases of the [master theorem](/master-theorem/) give answers $n^w$, $n^w \lg^{k+1} n$ and, in case 3, $f(n)$. The first two are smooth when $w \ge 0$. So, for a recurrence whose solution is eventually non-decreasing, it suffices to solve it for $n$ a power of $b$. In case 3 the rule needs $f$ itself to be smooth.

### Which functions are smooth

- $n^k \lg^m n$ for $k \ge 0$, $m \ge 0$ with $k + m > 0$, and positive constants: smooth.
- $\lg\lg n$: smooth.
- $2^n$: not smooth, since $2^{2n}/2^n = 2^n$ is unbounded.
- $n^{\lg n}$: not smooth, since $(2n)^{\lg(2n)} = 2n \cdot (2n)^{\lg n} = 2n \cdot 2^{\lg n} \cdot n^{\lg n} = 2n^2 \cdot n^{\lg n}$, and the factor $2n^2$ is unbounded.
- $n!$: not smooth, since $(2n)!/n! \ge n^n$.

## Tightness

### Monotonicity of t is needed

Let $t(n) = n$ if $n$ is a power of 2 and $t(n) = n^2$ otherwise. Then $t(n) = \Theta(n \mid n \text{ a power of } 2)$, and $n$ is smooth, but $t(n) \ne O(n)$. The rule fails because $t$ is not eventually non-decreasing. Recurrences of algorithms can fail monotonicity too: a step that is cheap exactly on powers of 2 makes a cost of this kind.

### Smoothness of f is needed

Let $f(n) = 2^n$ and $t(n) = 2^{2^{\lceil \lg n \rceil}}$. Then $t$ is non-decreasing and $t(n) = f(n)$ on powers of 2. But at $n = 2^k + 1$, $t(n) = 2^{2^{k+1}}$ and $f(n) = 2^{2^k + 1}$, so $t(n)/f(n) = 2^{2^k - 1}$, which is unbounded. So $t(n) \ne O(f(n))$.

### Monotonicity can be hard to prove

The rule moves the work from the floors to a proof that $t$ is non-decreasing. For recurrences like $T(n) = T(\lfloor n/5 \rfloor) + T(\lfloor 7n/10 \rfloor + 6) + n$ the proof is not immediate. Other tools avoid this step: the [substitution method](/substitution-method/) works directly with the floors, and Leighton's form of the [Akra-Bazzi theorem](/akra-bazzi-theorem/) allows perturbations $h_i(n)$ of the arguments with $|h_i(n)| \le n/\lg^{1+\varepsilon} n$, under a polynomial-growth condition on the driving function in place of monotonicity of $T$.

## History

Brassard and Bratley state the smoothness rule, with $b$-smooth and smooth functions and the conditional asymptotic notation, in Section 3.4 of Fundamentals of Algorithmics, and leave the completion of its proof as Problem 3.29. Levitin's textbook gives the same rule with the base 2 in its definition of smoothness. Leighton's notes of 1996 handle floors and ceilings in a different way, inside a master theorem.

## References
