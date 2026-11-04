---
tag: Y8RFMF
kind: concept
slug: recurrence-relation
name: Recurrence relation
aliases:
- recurrence
- recursive equation
area: foundations/recurrences
level: intro
summary: An equation that defines a function's value at n in terms of its values at smaller inputs, often used for running times.
prereqs: [recursion, induction, asymptotic-notation]
see_also: [closed-form-solution, divide-and-conquer-recurrence, linear-recurrences-with-constant-coefficients, substitution-method, recursion-tree-method, iteration-method, master-theorem, generating-functions]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 4, Divide-and-Conquer (introduction, the subsection on recurrences and algorithmic recurrences)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 1, Recurrent Problems; Section 2.2, Sums and Recurrences
  - book: isbn:9780321905758
    title: Robert Sedgewick and Philippe Flajolet, An Introduction to the Analysis of Algorithms, second edition
    locator: Chapter 2, Recurrence Relations (Sections 2.1 to 2.4)
---

A recurrence relation is an equation that gives the value of a function at an argument $n$ in terms of its values at smaller arguments, together with initial values that start the chain. It is the natural description of the cost of a [recursive](/recursion/) algorithm and of many counting problems. To solve a recurrence is to find a [closed form](/closed-form-solution/) or an asymptotic estimate of its solution, and most pages of this area are methods to do that.

## In plain words

A recurrence is a rule that tells you how to get the next value of a sequence from the values you already have. With the first few values given, you can apply the rule again and again and fill in the whole sequence, one value at a time.

For a recursive program, the rule says that the work on a big input is the work on the smaller inputs it hands to itself, plus the work it does on its own. That rule is easy to write down by reading the program. What the rule does not tell you at once is how fast the values grow. Finding that out, either exactly or up to a constant factor, is called solving the recurrence.

## The idea

### Definition

Let $n_0$ be an integer. A recurrence relation for a sequence $(a_n)_{n \ge 0}$ of numbers is a family of equations

$$a_n = \Phi_n(a_0, a_1, \ldots, a_{n-1}) \qquad \text{for each } n \ge n_0,$$

where each $\Phi_n$ is a known function. The values $a_0, \ldots, a_{n_0 - 1}$ are the initial values. By strong [induction](/induction/) on $n$, the initial values and the recurrence determine exactly one sequence: $a_n$ for $n < n_0$ is given, and $a_n$ for $n \ge n_0$ is a function of values with smaller index, which are already determined. The same is true for a function $T$ on the positive reals when each argument on the right side is at most $n - c$ for a fixed $c > 0$, or at most $n/b$ for a fixed $b > 1$ with a base region that contains $(0, n_0)$: in both cases each chain of arguments reaches the base region after finitely many steps.

### Kinds of recurrences

- **Order.** A recurrence of order $k$ uses only $a_{n-1}, \ldots, a_{n-k}$. The Fibonacci recurrence $F_n = F_{n-1} + F_{n-2}$ has order 2.
- **Full history.** A full-history recurrence uses all earlier values. The average number of comparisons of quicksort satisfies $C_n = n + 1 + \frac{2}{n} \sum_{k=0}^{n-1} C_k$ for $n \ge 1$, with $C_0 = 0$.
- **Linear.** The right side is a linear combination of earlier values plus a term that does not depend on them: $a_n = \sum_{i=1}^{k} c_i(n) \, a_{n-i} + g(n)$. It is homogeneous when $g = 0$, and it has constant coefficients when each $c_i$ is a constant. The constant-coefficient case is solved exactly by [the characteristic polynomial](/linear-recurrences-with-constant-coefficients/).
- **Nonlinear.** Examples are $a_n = a_{n-1}^2$ and the Catalan recurrence $C_{n+1} = \sum_{i=0}^{n} C_i C_{n-i}$.
- **Divide and conquer.** The arguments on the right side are fractions of $n$, as in $T(n) = aT(n/b) + f(n)$. These are the [divide-and-conquer recurrences](/divide-and-conquer-recurrence/), solved by the [master theorem](/master-theorem/) and the [Akra-Bazzi theorem](/akra-bazzi-theorem/).
- **Several variables.** The binomial coefficients satisfy $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$, with $\binom{n}{0} = \binom{n}{n} = 1$.

### Recurrence inequalities

A running time is rarely known exactly. An analysis usually gives an inequality such as $T(n) \le 2T(\lfloor n/2 \rfloor) + cn$ for $n \ge 2$. Each function that satisfies the inequality is bounded by the solution of the equation with the same initial values, by induction on $n$, as long as the right side is non-decreasing in each earlier value. For this reason books write $T(n) = 2T(n/2) + \Theta(n)$ and treat the $\Theta$ as an anonymous function, as on the page about [asymptotic notation](/asymptotic-notation/). CLRS calls a recurrence *algorithmic* when, for each large enough threshold $n_0 > 0$, its value is $\Theta(1)$ for each $n < n_0$, and each chain of recursive calls from an $n \ge n_0$ reaches such a base case after finitely many steps (Chapter 4). Under this convention, the base cases do not change the order of growth, and the analysis can leave them out.

### What a solution is

There are three levels of answer.

1. An exact [closed form](/closed-form-solution/), such as $T(n) = 2^n - 1$ for $T(n) = 2T(n-1) + 1$ with $T(0) = 0$.
2. An asymptotic equivalent, such as $C_n \sim 2n \ln n$ for the quicksort recurrence above. See [tilde notation](/tilde-notation/).
3. An order of growth, such as $T(n) = \Theta(n \log n)$ for merge sort.

The methods are the [iteration method](/iteration-method/) (unroll and sum), the [substitution method](/substitution-method/) (guess and prove by induction), the [recursion-tree method](/recursion-tree-method/), the [master theorem](/master-theorem/) and its generalizations, the [characteristic polynomial](/linear-recurrences-with-constant-coefficients/), [generating functions](/generating-functions/), and a [change of variables](/change-of-variables/) that turns one form into another.

## Examples

- **Tower of Hanoi.** $T_0 = 0$ and $T_n = 2T_{n-1} + 1$ for $n \ge 1$. The values are 0, 1, 3, 7, 15, and $T_n = 2^n - 1$. Proof by induction: $2(2^{n-1} - 1) + 1 = 2^n - 1$.
- **Merge sort, exact count.** The worst-case number of comparisons is $W(1) = 0$ and $W(n) = W(\lceil n/2 \rceil) + W(\lfloor n/2 \rfloor) + n - 1$. Its solution is $W(n) = n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$ for each $n \ge 1$. For example $W(7) = 14$, $W(10) = 25$ and $W(1000) = 8977$. See [merge sort](/merge-sort/).
- **Quicksort, average case.** The recurrence $C_0 = 0$, $C_n = n + 1 + \frac{2}{n} \sum_{k=0}^{n-1} C_k$ has the solution $C_n = 2(n+1)H_n - 2n$, where $H_n$ is the $n$-th [harmonic number](/harmonic-series/). The first values are $C_1 = 2$, $C_2 = 5$ and $C_3 = 26/3$. Concrete Mathematics solves it in Section 2.2: multiply by $n$, subtract the same equation for $n-1$ to get $nC_n = (n+1)C_{n-1} + 2n$, then divide by $n(n+1)$ and sum. With the toll $n - 1$ in place of $n + 1$, which counts the comparisons of the usual partition, the solution is $2(n+1)H_n - 4n$. See [quicksort expected running time](/quicksort-expected-running-time/).
- **Catalan numbers.** $C_0 = 1$ and $C_{n+1} = \sum_{i=0}^{n} C_i C_{n-i}$ give 1, 1, 2, 5, 14, 42, 132, 429, 1430. The closed form $C_n = \frac{1}{n+1}\binom{2n}{n}$ comes from a [generating function](/generating-functions/). See [Catalan numbers](/catalan-numbers/).
- **Binary search.** $T(1) = 1$ and $T(n) = T(\lfloor n/2 \rfloor) + 1$ give $T(n) = \lfloor \lg n \rfloor + 1$, the number of bits of $n$.
- **Non-example: no initial value.** $a_n = 2a_{n-1}$ alone is satisfied by $a_n = c \cdot 2^n$ for each $c$. A recurrence of order $k$ needs $k$ initial values.
- **Non-example: a self-reference that does not go down.** $T(n) = T(n) + 1$ has no solution, and $T(n) = T(n+1) - 1$ does not determine $T$ from smaller arguments. Neither is a recurrence in the sense above.

### Pitfalls

- **A constant hidden in $O$ that changes with $n$.** Unrolling $T(n) = T(n-1) + O(1)$ as "$O(1) + O(1) + \cdots = O(1)$" is wrong. Each of the $n$ terms is at most a fixed $c$, so the sum is at most $cn$.
- **Ignoring floors and ceilings without a reason.** For most recurrences of algorithms they do not change the order of growth, but this needs a proof. See [smoothness rules](/smoothness-rules/).
- **Using the wrong initial values.** Two initial values that differ by a constant can change the leading constant of the solution, and in a recurrence such as $T(n) = 2T(n-1)$ they change everything.

## Where it is used

- **Running time of recursive algorithms.** Each recursive algorithm has a recurrence for its time, read off the code. See [divide-and-conquer recurrence](/divide-and-conquer-recurrence/).
- **Average-case analysis.** Full-history recurrences describe the average cost of quicksort, of [quickselect](/quickselect/) and of searches in a [random binary search tree](/random-binary-search-tree/).
- **Counting.** The number of binary trees, of tilings, of strings that avoid a pattern, and many other counts satisfy recurrences.
- **Dynamic programming.** A dynamic program evaluates a recurrence over a table of subproblems.
- **Numerical methods and signals.** Linear recurrences with constant coefficients are the difference equations of digital filters, analyzed with the [z-transform](/z-transform/).

## References
