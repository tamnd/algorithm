---
tag: XA5DGP
kind: technique
slug: change-of-variables
name: Change of variables for recurrences
aliases:
- variable substitution for recurrences
area: foundations/recurrences
level: core
summary: Rewrite a recurrence in a new variable, such as m = log n, so that it takes a standard form.
prereqs: [recurrence-relation, logarithms, divide-and-conquer-recurrence, master-theorem]
see_also: [iteration-method, substitution-method, linear-recurrences-with-constant-coefficients, smoothness-rules, telescoping-sum, closed-form-solution]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 4.3, The substitution method for solving recurrences (the subsection Changing variables)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 2.2, Sums and Recurrences (summation factors)
  - book: isbn:9780321905758
    title: Robert Sedgewick and Philippe Flajolet, An Introduction to the Analysis of Algorithms, second edition
    locator: Section 2.2, First-Order Recurrences; Section 2.3, Nonlinear First-Order Recurrences
---

A change of variables rewrites a [recurrence relation](/recurrence-relation/) in terms of a new index or a new unknown, chosen so that the result has a form you can already solve. The two common moves are a change of the index, such as $m = \lg n$, which turns repeated square roots into halving and halving into subtracting one, and a change of the values, such as $S = T/n$ or $S = \lg T$, which turns a product or a multiplicative factor into a sum. After the new recurrence is solved, the substitution is undone to give the answer in the original variable.

## In plain words

Some recurrences look hard only because they are written in an awkward way. A recurrence that takes square roots of its input, for example, does not fit the usual rules for halving. But if you look at the number of digits of the input instead of the input itself, a square root just halves the number of digits. In that view the recurrence becomes a familiar one.

The same trick works on the values. If the values multiply at each step, their logarithms add, and a sum is easier to handle than a product. If each value carries a growing factor, divide it out first.

So the method is: find a new way to measure the input or the output in which the recurrence looks standard, solve it there, and translate back.

## When it applies

- The argument shrinks by a power, $n \mapsto n^{1/k}$, as in recursions on the bits of a key or on a universe of size $u$ split into $\sqrt u$ parts. Use $m = \lg n$.
- The argument shrinks by a factor and you want an ordinary sequence: $n = b^m$ turns $T(n/b)$ into $S(m - 1)$.
- The values grow by a known factor at each step: $T(n) = 2T(n/2) + n$ or $T_n = nT_{n-1} + n!$. Divide by that factor.
- The recurrence multiplies or divides values: $a_n = a_{n-1}^2$, $a_n = a_{n-1} a_{n-2}$. Take logarithms.
- The recurrence is a ratio of linear expressions in the previous value, such as $x_n = x_{n-1}/(1 + x_{n-1})$. Use reciprocals.

## The template

1. **Find the awkward part.** Is it the way the argument shrinks, or the way the values combine?
2. **Choose the substitution.** For the index, take $m = g(n)$ with $g$ such that the argument map becomes $m \mapsto m/2$ or $m \mapsto m - 1$. For the values, take $S = T/h$ or $S = \lg T$ or $S = 1/T$.
3. **Write the new recurrence**, including its base case, and check that it is equivalent: each value of the old sequence must correspond to exactly one value of the new one.
4. **Solve the new recurrence** with the [master theorem](/master-theorem/), the [iteration method](/iteration-method/), or the [characteristic polynomial](/linear-recurrences-with-constant-coefficients/).
5. **Translate back**, and state for which $n$ the answer is exact (for example, $n = 2^{2^k}$) and how it extends to other $n$.

## Classic examples

### $T(n) = 2T(\sqrt n) + \lg n$

This is the example of CLRS, third edition, Section 4.3. Let $m = \lg n$, so $\sqrt n = 2^{m/2}$, and let $S(m) = T(2^m)$. Then

$$S(m) = 2S(m/2) + m,$$

which is the merge sort recurrence. With the base case $T(2) = 1$, that is $S(1) = 1$, and $m$ a power of 2, $S(m) = m\lg m + m$. Translating back,

$$T(n) = \lg n \,\lg\lg n + \lg n \quad \text{for } n = 2^{2^k},$$

so $T(n) = \Theta(\log n \log\log n)$. Directly from the recurrence, $T(2^{2^k}) = (k + 1)2^k$, which is the same: $1, 4, 12, 32, 80$ for $k = 0, \ldots, 4$.

### $T(n) = T(\sqrt n) + 1$

With $m = \lg n$, $S(m) = S(m/2) + 1$, so $S(m) = \lg m + O(1)$ and $T(n) = \Theta(\log\log n)$. This is the shape of the query time of the van Emde Boas tree on a universe of size $u$: one recursive call on a universe of size $\sqrt u$ plus constant work, so $\Theta(\log\log u)$.

### $T(n) = \sqrt n\, T(\sqrt n) + n$

Change both the values and the index. Let $U(n) = T(n)/n$. Dividing the recurrence by $n$ gives $U(n) = U(\sqrt n) + 1$, so by the previous example $U(n) = \Theta(\log\log n)$ and $T(n) = \Theta(n\log\log n)$. With $T(2) = 2$, exactly $T(n) = n(k + 1) = n(\lg\lg n + 1)$ for $n = 2^{2^k}$.

### Dividing out a factor: $T(n) = 2T(n/2) + n$

Let $n = 2^m$ and $S(m) = T(2^m)/2^m$. Dividing by $2^m$ gives $S(m) = S(m - 1) + 1$, so $S(m) = S(0) + m$ and $T(n) = n(T(1) + \lg n)$. The same division by $a^m$ turns $T(n) = aT(n/b) + f(n)$, on $n = b^m$, into $S(m) = S(m-1) + f(b^m)/a^m$, a sum.

### A summation factor: $T_n = nT_{n-1} + n!$

Let $S_n = T_n/n!$. Then $S_n = S_{n-1} + 1$, so with $T_0 = 0$, $S_n = n$ and $T_n = n \cdot n!$. Dividing by the product of the coefficients is the summation factor of Concrete Mathematics, Section 2.2; see the [iteration method](/iteration-method/).

### Logarithms: $a_n = a_{n-1}^2$ and $a_n = a_{n-1}a_{n-2}$

For $a_0 = 2$ and $a_n = a_{n-1}^2$, let $b_n = \lg a_n$. Then $b_n = 2b_{n-1}$, $b_0 = 1$, so $b_n = 2^n$ and $a_n = 2^{2^n}$.

For $a_0 = 1$, $a_1 = 2$ and $a_n = a_{n-1}a_{n-2}$, the logarithms satisfy $b_n = b_{n-1} + b_{n-2}$ with $b_0 = 0$, $b_1 = 1$. These are the [Fibonacci numbers](/fibonacci-numbers/), so $a_n = 2^{F_n}$: $1, 2, 2, 4, 8, 32, 256, \ldots$

### Reciprocals: $x_n = x_{n-1}/(1 + x_{n-1})$

For $x_0 > 0$, let $y_n = 1/x_n$. Then $y_n = (1 + x_{n-1})/x_{n-1} = y_{n-1} + 1$, so $y_n = y_0 + n$ and

$$x_n = \frac{x_0}{1 + n x_0}.$$

For $x_0 = 3$, $x_7 = 3/22$.

## Variations

- **Domain and range changes together.** As in $\sqrt n\,T(\sqrt n) + n$, first remove the factor from the values, then change the index.
- **Shifting the values.** A nonhomogeneous term can sometimes be removed by a shift: for $T_n = 2T_{n-1} + 1$, the values $T_n + 1$ double, so $T_n = 2^n(T_0 + 1) - 1$.
- **Trigonometric substitutions.** For $x_{n+1} = 4x_n(1 - x_n)$ with $x_0 = \sin^2\theta$, the substitution $x_n = \sin^2\theta_n$ gives $\theta_{n+1} = 2\theta_n$, by $\sin^2 2\theta = 4\sin^2\theta\cos^2\theta$. So $x_n = \sin^2(2^n\theta)$.
- **Bit representations.** Concrete Mathematics solves the Josephus recurrence by writing $n$ in binary: the recurrence becomes a cyclic shift of the bits. See [closed-form solution](/closed-form-solution/).

## Pitfalls

- **A base case that the new recurrence never reaches.** The map $n \mapsto \sqrt n$ never reaches 1 from a real $n > 1$, and it fixes 1. Take the base case at $n \le 2$ (that is $m \le 1$), not at $n = 1$ ($m = 0$), or the recursion does not end.
- **Exact only on a sparse set.** The values $T(2), T(4), T(16), T(256), \ldots$ are those at $n = 2^{2^k}$, a set much sparser than the powers of 2, so the [smoothness rules](/smoothness-rules/) do not apply as stated. If $T$ is non-decreasing, the same sandwich works: for $2^{2^k} \le n < 2^{2^{k+1}}$, $(k+1)2^k \le T(n) \le (k+2)2^{k+1}$, and both bounds are within a constant factor of $\lg n\lg\lg n$ for $k \ge 1$. Without monotonicity, bound the values for other $n$ directly.
- **Floors and ceilings.** $\lfloor \sqrt n \rfloor$ is not $2^{m/2}$ in general. CLRS, third edition, ignores this rounding in the example above. A careful proof bounds the floors, as in the [substitution method](/substitution-method/).
- **Logarithms of non-positive values.** $b_n = \lg a_n$ needs $a_n > 0$. A recurrence such as $a_n = a_{n-1}a_{n-2}$ with $a_0 = 0$ is zero from then on.
- **Reciprocals of zero.** $y_n = 1/x_n$ needs $x_n \ne 0$ and $1 + x_{n-1} \ne 0$ for each $n$. For $x_0 = -\frac12$, $x_1 = -1$ and $x_2$ is undefined; the formula $x_0/(1 + nx_0)$ has its pole at $n = 2$ as well.

## Exercises

1. Solve $T(n) = 4T(\sqrt n) + \lg^2 n$. (With $m = \lg n$, $S(m) = 4S(m/2) + m^2$, so $\Theta(\lg^2 n \lg\lg n)$.)
2. Solve $T(n) = 2T(\sqrt n) + 1$. (Answer: $\Theta(\log n)$.)
3. Solve $a_n = 3a_{n-1}^2$ with $a_0 = 1$, by taking logarithms base 3. (Answer: $a_n = 3^{2^n - 1}$.)
4. Solve $T_n = \frac{n+1}{n}T_{n-1} + 2$, $T_0 = 0$, by dividing by $n + 1$. (Answer: $2(n+1)(H_{n+1} - 1)$.)
5. Show that $x_n = \frac{2x_{n-1}}{1 + x_{n-1}}$ with $x_0 > 0$ becomes linear after $y_n = 1/x_n$, and find the limit of $x_n$. (Answer: $y_n - 1 = 2^{-n}(y_0 - 1)$, and $x_n \to 1$.)

## References
