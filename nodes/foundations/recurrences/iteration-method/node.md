---
tag: NQ45DG
kind: technique
slug: iteration-method
name: Iteration method
aliases:
- unrolling
- repeated substitution
- expansion method
area: foundations/recurrences
level: intro
summary: Repeatedly substitute a recurrence into itself to expose a sum of terms, then evaluate that sum.
prereqs: [recurrence-relation, induction, geometric-series, arithmetic-series]
see_also: [recursion-tree-method, substitution-method, closed-form-solution, harmonic-series, telescoping-sum, quicksort-expected-running-time]
sources:
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 1.1, The Tower of Hanoi; Section 2.2, Sums and Recurrences (summation factors and the quicksort recurrence)
  - book: isbn:9780321905758
    title: Robert Sedgewick and Philippe Flajolet, An Introduction to the Analysis of Algorithms, second edition
    locator: Section 2.2, First-Order Recurrences
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 5.1, A First Recurrence, The Mergesort Algorithm (unrolling the mergesort recurrence)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 4.4, The recursion-tree method for solving recurrences
---

The iteration method solves a [recurrence relation](/recurrence-relation/) by substituting the recurrence into itself again and again until the base case appears, which turns the recurrence into an explicit sum. Evaluating that sum, exactly or with bounds, gives the solution. It is the algebraic form of the [recursion-tree method](/recursion-tree-method/), and for first-order linear recurrences it is a complete method: with a summation factor, each such recurrence becomes a sum.

## In plain words

Write down the rule for the value at the current input. The rule mentions the value at a smaller input. Replace that value by its own rule, which mentions an even smaller input. Do it again a few times, and watch the expression. It becomes a growing sum, with one new term at each step, and the terms follow a pattern.

Once you see the pattern after a general number of steps, choose the number of steps that lands exactly on the smallest input, whose value you know. What is left is a sum of known terms. Many such sums have a formula; for the others, you can bound them from above and below.

## When it applies

- First-order recurrences, where $T(n)$ depends on one earlier value: $T(n) = x_n T(n-1) + y_n$, or $T(n) = aT(n/b) + f(n)$ along powers of $b$.
- Recurrences where the pattern of the unrolled expression is simple enough to state for a general number of steps $i$.
- It is awkward for recurrences with two or more different smaller arguments, such as $T(n/3) + T(2n/3)$: the number of terms doubles at each step. A [recursion tree](/recursion-tree-method/) organizes those terms better.
- For linear recurrences of higher order, such as Fibonacci, the [characteristic polynomial](/linear-recurrences-with-constant-coefficients/) is the right tool.

## The template

1. **Unroll a few times.** Substitute the recurrence into itself two or three times, and simplify after each step.
2. **Guess the pattern after $i$ steps.** Write $T(n)$ as (a coefficient) $\times$ $T$(argument after $i$ steps) $+$ (a sum of $i$ terms).
3. **Prove the pattern.** The pattern is a claim for each $i$, and it needs a proof by [induction](/induction/) on $i$. Usually the step is one more substitution.
4. **Reach the base case.** Choose $i$ so that the argument is the base case: $i = n$ for $T(n-1)$, or $i = \log_b n$ for $T(n/b)$ with $n$ a power of $b$.
5. **Evaluate the sum.** Use the [arithmetic series](/arithmetic-series/), the [geometric series](/geometric-series/), the [harmonic numbers](/harmonic-series/), a [telescoping sum](/telescoping-sum/), or [integral bounds](/integral-bounds-for-sums/).
6. **Handle the other $n$.** If step 4 needed $n$ to be a power of $b$, extend the result to each $n$ with the [smoothness rules](/smoothness-rules/) or by bounding the floors directly.

## Classic examples

### A sum: $T(n) = T(n-1) + n$

With $T(0) = 0$: $T(n) = n + T(n-1) = n + (n-1) + T(n-2) = \cdots$. After $i$ steps, $T(n) = \sum_{k=n-i+1}^{n} k + T(n - i)$. Induction on $i$: one more step replaces $T(n-i)$ by $(n - i) + T(n - i - 1)$. With $i = n$, $T(n) = \sum_{k=1}^{n} k = n(n+1)/2$. This is the worst case of quicksort and of insertion sort.

### A doubling: $T(n) = 2T(n-1) + 1$

With $T(0) = 0$: after $i$ steps, $T(n) = 2^i T(n - i) + \sum_{k=0}^{i-1} 2^k = 2^i T(n-i) + 2^i - 1$. With $i = n$, $T(n) = 2^n - 1$. This is the [Tower of Hanoi](/tower-of-hanoi/).

### Halving: $T(n) = 2T(n/2) + n$

Let $n = 2^k$ and $T(1) = t_1$. After $i$ steps,

$$T(n) = 2^i T(n/2^i) + i \cdot n.$$

Induction: $2^i\left(2T(n/2^{i+1}) + n/2^i\right) + in = 2^{i+1}T(n/2^{i+1}) + (i + 1)n$. With $i = k = \lg n$: $T(n) = t_1 n + n\lg n$.

### Floors that compose: $T(n) = 3T(\lfloor n/4 \rfloor) + n$

Let $T(0) = 0$ and the recurrence hold for $n \ge 1$. Unrolling needs the fact that $\lfloor \lfloor n/a \rfloor / b \rfloor = \lfloor n/(ab) \rfloor$ for each integer $n \ge 0$ and positive integers $a, b$. Proof: let $m = \lfloor n/(ab) \rfloor$. Then $mab \le n < (m+1)ab$, so $mb \le n/a < (m+1)b$. Since $mb$ and $(m+1)b$ are integers, $mb \le \lfloor n/a \rfloor < (m+1)b$, so $\lfloor \lfloor n/a \rfloor / b \rfloor = m$.

With this fact, after $i$ steps $T(n) = \sum_{j=0}^{i-1} 3^j \lfloor n/4^j \rfloor + 3^i T(\lfloor n/4^i \rfloor)$, and once $4^i > n$ the last term is $3^i T(0) = 0$. So, exactly,

$$T(n) = \sum_{j \ge 0} 3^j \left\lfloor \frac{n}{4^j} \right\rfloor.$$

Each term is at most $(3/4)^j n$, so $T(n) \le n \sum_{j \ge 0}(3/4)^j = 4n$, and $T(n) \ge n$ from $j = 0$. So $T(n) = \Theta(n)$. For example $T(1000) = 2956$, and $T(n)/n$ stays below 3.7 for each $n \le 200{,}000$.

### First-order linear recurrences and summation factors

Let $T_0$ be given and $T_n = x_n T_{n-1} + y_n$ for $n \ge 1$, with each $x_n \ne 0$. Let $P_n = \prod_{i=1}^{n} x_i$, with $P_0 = 1$. Divide the recurrence by $P_n$:

$$\frac{T_n}{P_n} = \frac{T_{n-1}}{P_{n-1}} + \frac{y_n}{P_n}.$$

The left side minus the first term on the right is a difference of consecutive terms, so the sum over $n = 1, \ldots, N$ [telescopes](/telescoping-sum/):

$$T_N = P_N\left(T_0 + \sum_{k=1}^{N}\frac{y_k}{P_k}\right).$$

The factor $1/P_n$ is the summation factor of Concrete Mathematics, Section 2.2. Both earlier examples are special cases: $x_n = 2$, $y_n = 1$ gives $T_N = 2^N \sum_{k=1}^{N} 2^{-k} = 2^N - 1$.

### Quicksort on average

The average number of comparisons of quicksort, in the model of Concrete Mathematics, satisfies $C_0 = 0$ and $C_n = n + 1 + \frac{2}{n}\sum_{k=0}^{n-1}C_k$ for $n \ge 1$. This is a full-history recurrence, so first reduce it to first order. Multiply by $n$, write the same equation for $n - 1$, and subtract:

$$nC_n - (n-1)C_{n-1} = 2n + 2C_{n-1}, \quad\text{so}\quad nC_n = (n+1)C_{n-1} + 2n \quad (n \ge 1).$$

Here $x_n = (n+1)/n$, $P_n = n + 1$, and $y_n = 2$. The summation factor gives

$$C_n = (n+1)\sum_{k=1}^{n}\frac{2}{k+1} = 2(n+1)(H_{n+1} - 1) = 2(n+1)H_n - 2n,$$

where the last step uses $H_{n+1} = H_n + \frac{1}{n+1}$. The values are $C_1 = 2$, $C_2 = 5$, $C_3 = 26/3$, and $C_{10} \approx 44.437$. Since $H_n = \ln n + O(1)$, $C_n \sim 2n\ln n \approx 1.386\, n\lg n$. See [quicksort expected running time](/quicksort-expected-running-time/).

## Variations

- **Recursion tree.** For $T(n) = aT(n/b) + f(n)$, the unrolled sum $\sum_j a^j f(n/b^j)$ is the sum of the levels of the [recursion tree](/recursion-tree-method/).
- **Reduce the order first.** As in the quicksort example, a full-history recurrence with a sum of all earlier values often becomes first order after subtracting two consecutive instances.
- **Change of variables.** $T(n) = T(\sqrt n) + 1$ unrolls to $T(n) = i + T(n^{1/2^i})$, which reaches a constant after $\lg\lg n$ steps. See [change of variables](/change-of-variables/).
- **Bounds instead of equalities.** For an inequality $T(n) \le aT(n/b) + f(n)$, the same unrolling gives an upper bound.

## Pitfalls

- **An unproved pattern.** Three unrolled steps suggest a pattern, but they do not prove it. Step 3 of the template is the proof, and it is usually one line.
- **An off-by-one in the number of steps.** For $T(n) = 2T(n/2) + n$ with base case $T(1)$, there are $\lg n$ steps, not $\lg n + 1$, and the result is $n\lg n + n\,T(1)$. Check the formula at $n = 1$ and $n = 2$.
- **Floors that do not compose.** $\lfloor\lfloor n/2 \rfloor/2\rfloor = \lfloor n/4 \rfloor$, but $\lceil\lceil n/2 \rceil/3\rceil = \lceil n/6 \rceil$ needs the same kind of proof, and $\lfloor\sqrt{\lfloor\sqrt n\rfloor}\rfloor = \lfloor n^{1/4} \rfloor$ is true but needs its own argument. Do not merge floors without one.
- **Constants hidden in $O$ across many steps.** Unrolling $T(n) = T(n-1) + O(1)$ $n$ times gives $O(n)$ only because each step adds at most the same constant $c$. Write $c$ explicitly when unrolling.

## Exercises

1. Unroll $T(n) = T(n/2) + 1$, $T(1) = 1$, for $n = 2^k$. (Answer: $\lg n + 1$.)
2. Unroll $T(n) = 2T(n-1) + n$, $T(0) = 0$, and prove $T(n) = 2^{n+1} - n - 2$.
3. Solve $T_n = nT_{n-1} + n!$, $T_0 = 0$, with a summation factor. (Answer: $T_n = n \cdot n!$.)
4. Show that $T(n) = 4T(\lfloor n/2 \rfloor) + n$, $T(0) = 0$, equals $\sum_{j \ge 0} 4^j\lfloor n/2^j\rfloor$, and that it is $\Theta(n^2)$.
5. With the summation factor, solve the recurrence $D_n = n - 1 + \frac{2}{n}\sum_{k<n} D_k$, $D_0 = 0$, for the comparisons of the usual partition. (Answer: $2(n+1)H_n - 4n$.)

## References
