---
tag: ZVHPRZ
kind: concept
slug: divide-and-conquer-recurrence
name: Divide-and-conquer recurrence
aliases:
- T(n) = aT(n/b) + f(n)
- divide-and-conquer running-time recurrence
area: foundations/recurrences
level: intro
summary: The standard form T(n) = a T(n/b) + f(n) for an algorithm that splits a size-n problem into a subproblems of size n/b and spends f(n) to divide and combine.
prereqs: [recurrence-relation, recursion, asymptotic-notation, geometric-series]
see_also: [divide-and-conquer-paradigm, master-theorem, watershed-function, recursion-tree-method, akra-bazzi-theorem, smoothness-rules, merge-sort, karatsuba-multiplication]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 4, Divide-and-Conquer (introduction and Sections 4.1, 4.2, 4.4, 4.5)
  - book: isbn:9780321905758
    title: Robert Sedgewick and Philippe Flajolet, An Introduction to the Analysis of Algorithms, second edition
    locator: Section 2.6, Binary Divide-and-Conquer Recurrences and Binary Numbers; Section 2.7, General Divide-and-Conquer Recurrences
  - paper: doi:10.1145/1008861.1008865
    title: Jon L. Bentley, Dorothea Haken and James B. Saxe, A general method for solving divide-and-conquer recurrences, SIGACT News 12(3), 36 to 44 (1980)
---

A divide-and-conquer recurrence is a [recurrence relation](/recurrence-relation/) of the form $T(n) = aT(n/b) + f(n)$, where $a > 0$ and $b > 1$ are constants and $f$ is a non-negative function. It describes the cost of an algorithm of the [divide-and-conquer paradigm](/divide-and-conquer-paradigm/) that splits an input of size $n$ into $a$ subproblems of size $n/b$, solves them [recursively](/recursion/), and spends $f(n)$ to split and to combine. Its solution depends on how $f$ compares with $n^{\log_b a}$, the [watershed function](/watershed-function/), and the [master theorem](/master-theorem/) turns this comparison into an answer.

## In plain words

Many fast algorithms work in the same way. They cut the input into a few smaller pieces of equal size, solve each piece with the same algorithm, and then glue the answers together. The cost of the whole job is the cost of the pieces plus the cost of cutting and gluing.

Draw the calls as a tree. The top call does the gluing for the whole input. Its children do the gluing for the pieces, and so on, until the pieces are tiny. Each level of the tree has more calls, but each call is smaller. So the total work is a race between the number of calls, which grows from level to level, and the work per call, which shrinks. Either the top level wins, or the bottom level wins, or all levels tie. Each case gives a different answer.

## The idea

### Where each term comes from

For an algorithm on an input of size $n$:

- $a$ is the number of recursive calls that one call makes.
- $n/b$ is the size of the input of each recursive call. The integer version is $\lfloor n/b \rfloor$ or $\lceil n/b \rceil$.
- $f(n)$ is the cost of the work outside the recursive calls: the split, the combine, and the overhead of the call. It is called the *driving function* in CLRS and the *toll function* in the work of Roura.

The recurrence holds for $n \ge n_0$. For $n < n_0$ the algorithm solves the problem directly, in $\Theta(1)$ time. With this base case, the integer version reads

$$T(n) = a' \, T(\lfloor n/b \rfloor) + a'' \, T(\lceil n/b \rceil) + f(n) \quad (n \ge n_0), \qquad T(n) = \Theta(1) \quad (n < n_0),$$

with $a' + a'' = a$. Merge sort has $a' = a'' = 1$, $b = 2$, and $f(n) = \Theta(n)$.

### The exact solution on powers of b

Let $b \ge 2$ be an integer, $T(1) = t_1$, and $T(n) = aT(n/b) + f(n)$ for each $n = b^k$ with $k \ge 1$. Then for each $k \ge 0$,

$$T(b^k) = a^k \, t_1 + \sum_{j=0}^{k-1} a^j f(b^{k-j}).$$

Proof by induction on $k$. For $k = 0$ the sum is empty and $T(1) = t_1$. For $k \ge 1$, $T(b^k) = aT(b^{k-1}) + f(b^k) = a^k t_1 + \sum_{j=0}^{k-2} a^{j+1} f(b^{k-1-j}) + f(b^k)$, and the change of index $j \to j + 1$ turns the right side into the claimed sum, whose $j = 0$ term is $f(b^k)$.

The formula has a direct reading in the recursion tree. Level $j$ has $a^j$ calls on inputs of size $n/b^j$, so it costs $a^j f(n/b^j)$. The tree has $k = \log_b n$ levels of internal nodes and $a^k$ leaves. The identity $a^{\log_b n} = n^{\log_b a}$ (take $\log_b$ of both sides: each is $\log_b a \cdot \log_b n$) shows that the leaves cost $\Theta(n^{\log_b a})$. This is why the [watershed function](/watershed-function/) $n^{\log_b a}$ appears in each solution.

### The three regimes

Write $w = \log_b a$ and look at the cost $a^j f(n/b^j)$ of level $j$.

- If $f(n) = n^{w - \varepsilon}$ for some $\varepsilon > 0$, the level costs grow geometrically from the top to the bottom, by the factor $b^{\varepsilon}$ at each level, and the leaves win: $T(n) = \Theta(n^w)$.
- If $f(n) = n^w$, each level costs exactly $n^w$, and there are about $\log_b n$ levels: $T(n) = \Theta(n^w \log n)$.
- If $f(n) = n^{w + \varepsilon}$, the level costs shrink geometrically, and the root wins: $T(n) = \Theta(f(n))$.

The [master theorem](/master-theorem/) makes these three cases exact, with the hypotheses that they need. The [recursion-tree method](/recursion-tree-method/) is the same computation done by hand.

### More general forms

- **Unequal parts.** $T(n) = \sum_{i=1}^{k} a_i T(b_i n) + g(n)$ with $0 < b_i < 1$. The [Akra-Bazzi theorem](/akra-bazzi-theorem/) solves it.
- **Random parts.** Quicksort splits at a random position, which gives the full-history recurrence $C_n = n - 1 + \frac{2}{n}\sum_{k<n} C_k$. The [continuous master theorem](/continuous-master-theorem/) of Roura solves this kind.
- **Other changes of size.** $T(n) = 2T(\sqrt n) + \lg n$ is solved by a [change of variables](/change-of-variables/) to $S(m) = 2S(m/2) + m$.
- **Subtract instead of divide.** $T(n) = T(n-1) + n$ (the worst case of quicksort) is not of divide-and-conquer form. The [iteration method](/iteration-method/) gives $\Theta(n^2)$.

## Examples

All examples use $\lg = \log_2$. The exact values are for $T(1) = 1$ and $n$ a power of $b$.

| Algorithm | Recurrence | $n^{\log_b a}$ | Solution | Exact on powers of $b$ |
|---|---|---|---|---|
| [Binary search](/binary-search/) | $T(n/2) + 1$ | $1$ | $\Theta(\log n)$ | $\lg n + 1$ |
| [Merge sort](/merge-sort/) | $2T(n/2) + n$ | $n$ | $\Theta(n \log n)$ | $n\lg n + n$ |
| [Karatsuba](/karatsuba-multiplication/) | $3T(n/2) + n$ | $n^{\lg 3} \approx n^{1.585}$ | $\Theta(n^{\lg 3})$ | $3n^{\lg 3} - 2n$ |
| [Strassen](/strassen-algorithm/) | $7T(n/2) + n^2$ | $n^{\lg 7} \approx n^{2.807}$ | $\Theta(n^{\lg 7})$ | |
| [Matrix product by blocks](/divide-and-conquer-matrix-multiplication/) | $8T(n/2) + n^2$ | $n^3$ | $\Theta(n^3)$ | $2n^3 - n^2$ |
| [Stooge sort](/stooge-sort/) | $3T(2n/3) + 1$ | $n^{\log_{3/2} 3} \approx n^{2.710}$ | $\Theta(n^{\log_{3/2} 3})$ | |
| A root-heavy case | $2T(n/2) + n^2$ | $n$ | $\Theta(n^2)$ | $2n^2 - n$ |

The exact column follows from the formula on powers of $b$. For Karatsuba: $T(2^k) = 3^k + \sum_{j=0}^{k-1} 3^j 2^{k-j} = 3^k + 2^k \cdot 2((3/2)^k - 1) = 3 \cdot 3^k - 2 \cdot 2^k$, and $3^k = n^{\lg 3}$.

Two more examples with unequal parts:

- **Selection in linear time.** The [median of medians](/median-of-medians/) algorithm gives $T(n) \le T(\lceil n/5 \rceil) + T(7n/10 + 6) + O(n)$. The parts have total fraction $1/5 + 7/10 = 9/10 < 1$, so the level costs shrink by the factor $9/10$ and $T(n) = O(n)$.
- **Closest pair.** The [divide-and-conquer closest pair](/closest-pair-divide-and-conquer/) algorithm with presorting gives $T(n) = 2T(n/2) + O(n)$, so $O(n \log n)$.

### Pitfalls

- **Counting the parts wrong.** Strassen's algorithm makes 7 products of half size, not 8. The constant $a$ is the number of recursive calls, not the number of parts of the input.
- **A subproblem that does not shrink by a constant factor.** A split into parts of size $n - 1$ and $1$ is not of this form, and its cost can be quadratic.
- **Forgetting the cost of the split.** Copying the input into the subproblems costs $\Theta(n)$ per call. It belongs in $f(n)$.
- **Treating $a$ and $b$ as related.** $a$ need not equal $b$: binary search has $a = 1$, $b = 2$, and Stooge sort has $a = 3$, $b = 3/2$.

## Where it is used

- The time of each divide-and-conquer algorithm: sorting, selection, multiplication of integers, polynomials and matrices, the [fast Fourier transform](/fast-fourier-transform/), and the problems of computational geometry.
- The span (critical path) of parallel algorithms, where the subproblems run at the same time: a parallel merge sort whose merge has span $\Theta(\log^2 n)$ has span $T_\infty(n) = T_\infty(n/2) + \Theta(\log^2 n) = \Theta(\log^3 n)$, for example.
- The number of cache misses of cache-oblivious algorithms, where the recursion stops at the size of the cache instead of at size 1.
- The design of algorithms: lowering $a$ by one, as Karatsuba and Strassen do, lowers the exponent of the [watershed function](/watershed-function/), and this is often the whole gain.

## References
