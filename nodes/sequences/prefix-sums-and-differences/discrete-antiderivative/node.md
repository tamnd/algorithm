---
tag: QGNM5C
kind: concept
slug: discrete-antiderivative
name: Discrete antiderivative
aliases:
- antidifference
- indefinite sum
- discrete integral
area: sequences/prefix-sums-and-differences
level: advanced
summary: A sequence F with Delta F = f, the discrete counterpart of an indefinite integral; the sum of f is F(b)-F(a).
prereqs: [finite-differences, telescoping-sum]
see_also: [prefix-sums, difference-array, abel-summation, indefinite-summation, gosper-algorithm, euler-maclaurin-formula, stirling-numbers, polynomial]
sources:
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 2.6, Finite and infinite calculus (the operator Delta, falling factorial powers, the indefinite sum and the table of differences), and Section 5.7, Partial hypergeometric sums
  - paper: doi:10.1073/pnas.75.1.40
    title: R. William Gosper, Jr., Decision procedure for indefinite hypergeometric summation, Proceedings of the National Academy of Sciences 75(1), 1978
    locator: the algorithm that finds a hypergeometric antidifference or proves that none exists
  - book: isbn:9781568810638
    title: Petkovsek, Wilf and Zeilberger, A = B
    locator: Chapter 5, Gosper's algorithm
---

A discrete antiderivative, or antidifference, of a sequence $f$ is a sequence $F$ whose forward difference is $f$, that is, $F(k+1) - F(k) = f(k)$ for every $k$. It plays the role for sums that an indefinite integral plays for integrals: once an antiderivative is known, every sum of consecutive terms of $f$ is a difference of two values of $F$, by the [telescoping sum](/telescoping-sum/) identity. The [prefix sum](/prefix-sums/) array of an array is its antiderivative, and the [difference array](/difference-array/) is its derivative.

## In plain words

Think of a running total. If you know the running total at every point, then the sum of any stretch of values is the total at the end of the stretch minus the total at the start. The running total is what this page calls an antiderivative: a second list whose steps from one entry to the next are exactly the values of the first list.

Many lists have a running total that you can write as a short formula. For the numbers 0, 1, 2, 3 and so on, the running total is a formula of the second degree. For the powers of two, the running total is again a power of two, less one. Finding such a formula is how sums in the analysis of algorithms get exact answers. Some lists have no short formula of a given kind, and there are methods that can prove this.

## The idea

**Differences and antidifferences.** For a function $f$ on the integers, the forward difference is $\Delta f(k) = f(k+1) - f(k)$, as on the page on [finite differences](/finite-differences/). A function $F$ is an *antidifference* of $f$ when $\Delta F = f$. Graham, Knuth and Patashnik write this as an indefinite sum, $\sum f(k)\, \delta k = F(k) + C$, in parallel with $\int f(x)\, dx = F(x) + C$.

**Existence and uniqueness.** On the integers every $f$ has an antidifference: fix a base point $a$ and take the running sum

$$S(k) = \sum_{a \le j < k} f(j) \quad (k \ge a), \qquad S(k) = -\sum_{k \le j < a} f(j) \quad (k < a).$$

Two antidifferences $F$ and $G$ of the same $f$ satisfy $\Delta(F - G) = 0$, so $F(k+1) - G(k+1) = F(k) - G(k)$ for all $k$, and $F - G$ is a constant. (For functions on the real line the difference need only be periodic with period $1$; on the integers that is the same as a constant.) So the antidifference is unique up to an additive constant, just like an indefinite integral.

**The fundamental theorem.** If $\Delta F = f$, then for integers $a \le b$,

$$\sum_{a \le k < b} f(k) = \sum_{a \le k < b} \big(F(k+1) - F(k)\big) = F(b) - F(a).$$

The sum is over the half-open range $a \le k < b$, the same convention as for prefix sums: the range sum $\sum_{l \le k < r} x_k$ is $P_r - P_l$, where $P$ is the prefix sum array. Graham, Knuth and Patashnik write this definite sum as $\sum_a^b f(k)\, \delta k$.

**Falling powers.** Ordinary powers have messy differences: $\Delta k^2 = 2k + 1$. The falling factorial power $k^{\underline{m}} = k (k-1) \cdots (k - m + 1)$ behaves like $x^m$ under the derivative:

$$\Delta k^{\underline{m}} = (k+1)^{\underline{m}} - k^{\underline{m}} = m\, k^{\underline{m-1}}.$$

So an antidifference of $k^{\underline{m}}$ is $k^{\underline{m+1}}/(m+1)$. With the extension $k^{\underline{-1}} = 1/(k+1)$, the case $m = -1$ plays the role of $1/x$, and its antidifference is the harmonic number $H_k = 1 + 1/2 + \dots + 1/k$, the discrete logarithm. The [Stirling numbers](/stirling-numbers/) of the second kind convert ordinary powers into falling powers, $k^m = \sum_j {m \brace j} k^{\underline{j}}$, so every [polynomial](/polynomial/) of degree $d$ has a polynomial antidifference of degree $d + 1$.

**A short table.**

| $f(k)$ | antidifference $F(k)$ |
|---|---|
| $k^{\underline{m}}$, $m \ne -1$ | $k^{\underline{m+1}}/(m+1)$ |
| $1/(k+1)$ | $H_k$ |
| $c^k$, $c \ne 1$ | $c^k/(c - 1)$ |
| $\binom{k}{m}$ | $\binom{k}{m+1}$ |
| $k \cdot k!$ | $k!$ |

Each row is checked by taking the difference of the right column. The rule $\Delta \binom{k}{m+1} = \binom{k}{m}$ is Pascal's rule.

**Rules.** The antidifference is linear: an antidifference of $\alpha f + \beta g$ is $\alpha F + \beta G$. The product rule $\Delta(uv) = u\, \Delta v + (Ev)\, \Delta u$, where $Ev(k) = v(k+1)$, gives summation by parts, $\sum u\, \Delta v\, \delta k = uv - \sum (Ev)\, \Delta u\, \delta k$, which is the [Abel summation formula](/abel-summation/). There is no general chain rule, and so there is no discrete analogue of substitution.

**When there is no closed form.** Every $f$ has an antidifference, but often not one of a given simple kind. The [indefinite summation](/indefinite-summation/) problem asks for one in a fixed class of closed forms. For [hypergeometric terms](/hypergeometric-term/), where $f(k+1)/f(k)$ is a rational function of $k$, [Gosper's algorithm](/gosper-algorithm/) decides whether a hypergeometric antidifference exists and finds it when it does. For $f(k) = 1/(k+1)$ it reports that none exists, which is one way to say that $H_k$ has no closed form of this kind. For the continuous side, the [Euler-Maclaurin formula](/euler-maclaurin-formula/) expresses an antidifference of a smooth $f$ through its integral and its derivatives at the endpoints.

## Examples

**Sum of squares.** Write $k^2 = k^{\underline{2}} + k^{\underline{1}}$. An antidifference is $k^{\underline{3}}/3 + k^{\underline{2}}/2$, so

$$\sum_{0 \le k < n} k^2 = \frac{n(n-1)(n-2)}{3} + \frac{n(n-1)}{2} = \frac{n(n-1)(2n-1)}{6}.$$

For $n = 4$ this is $0 + 1 + 4 + 9 = 14$, and the formula gives $4 \cdot 3 \cdot 7 / 6 = 14$.

**Sum of cubes.** The Stirling numbers give $k^3 = k^{\underline{3}} + 3 k^{\underline{2}} + k^{\underline{1}}$, so an antidifference is $k^{\underline{4}}/4 + k^{\underline{3}} + k^{\underline{2}}/2$. For $n = 5$ this gives $30 + 60 + 10 = 100 = 0 + 1 + 8 + 27 + 64$.

**A geometric sum.** An antidifference of $2^k$ is $2^k$, so $\sum_{0 \le k < n} 2^k = 2^n - 1$. With summation by parts, $\sum_{0 \le k < n} k\, 2^k = (n - 2) 2^n + 2$; see the [Abel summation formula](/abel-summation/).

**Factorials.** Since $\Delta k! = (k+1)! - k! = k \cdot k!$, the sum $\sum_{0 \le k < n} k \cdot k!$ is $n! - 1$. In contrast, $\sum_{0 \le k < n} k!$ has no hypergeometric closed form, and Gosper's algorithm proves this.

**Arrays.** For an array $x_0, \dots, x_{n-1}$, the prefix sum array $P_0 = 0$, $P_{i+1} = P_i + x_i$ is the antidifference with $P_0 = 0$, and $\Delta P = x$. The difference array $d_i = x_i - x_{i-1}$ is $\Delta$ applied in the other direction, and taking prefix sums of $d$ gives $x$ back. The two operations are inverse to each other up to the base value, which is the whole content of the [difference array](/difference-array/) technique.

## Where it is used

- **Running time sums.** The cost of a loop is a sum over its iterations. An antidifference of the cost per iteration turns the sum into a closed form, for example $\sum_{0 \le i < n} i = n^{\underline{2}}/2$ for a double loop over pairs.
- **Range queries.** A [prefix sum](/prefix-sums/) array stores an antidifference, so each range sum is one subtraction. Its two-dimensional form does the same with a double antidifference.
- **Symbolic summation.** Computer algebra systems search for antidifferences with Gosper's algorithm and its relatives, and use [Zeilberger's algorithm](/zeilberger-algorithm/) for definite sums whose indefinite sum has no closed form.
- **Recurrences.** A first-order recurrence $T(k+1) = T(k) + f(k)$ says that $T$ is an antidifference of $f$, so $T(n) = T(0) + \sum_{0 \le k < n} f(k)$, and a closed form for the antidifference solves the recurrence.
- **Interpolation.** Newton's forward-difference formula writes a polynomial through its differences in the basis $\binom{k}{j}$, and the antidifference shifts each basis term up by one, $\binom{k}{j} \mapsto \binom{k}{j+1}$.

## References
