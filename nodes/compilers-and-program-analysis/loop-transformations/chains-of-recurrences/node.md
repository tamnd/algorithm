---
tag: 2XRK3A
kind: technique
slug: chains-of-recurrences
name: Chains of recurrences
aliases:
- scalar evolution
area: compilers-and-program-analysis/loop-transformations
level: advanced
summary: Represents the values of an induction variable over iterations as a chain of add or multiply recurrences, closed under arithmetic.
prereqs: [induction-variable-analysis, finite-differences, binomial-coefficient]
see_also: [strength-reduction, operator-strength-reduction, polynomial-evaluation, horner-rule, dependence-testing, practical-dependence-tests, integer-overflow, newton-interpolation]
sources:
  - paper: doi:10.1145/190347.190423
    title: Olaf Bachmann, Paul S. Wang and Eugene V. Zima, Chains of recurrences, a method to expedite the evaluation of closed-form functions, ISSAC 1994, pages 242 to 249
    locator: the definition of a chain of recurrences, the algebraic rules, and the evaluation of a function on a regular grid
  - paper: doi:10.1007/3-540-45306-7_9
    title: Robert A. van Engelen, Efficient symbolic analysis for optimizing compilers, CC 2001, LNCS 2027, pages 118 to 132
    locator: the use of chains of recurrences to recognize induction variables in a compiler, and the comparison with symbolic differencing
  - paper: "Eugene V. Zima, On computational properties of chains of recurrences, ISSAC 2001"
    locator: the closed forms of pure sum and pure product chains and the cost of evaluation
  - paper: "Michael P. Gerlek, Eric Stoltz and Michael Wolfe, Beyond induction variables: detecting and classifying sequences using a demand-driven SSA form, ACM Transactions on Programming Languages and Systems 17(1), 1995"
    locator: the classes of sequences (linear, polynomial, geometric) that the chains represent
  - book: isbn:0201558025
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition, Addison-Wesley, 1994
    locator: Section 5.1 (Pascal's rule and the summation of binomial coefficients on the upper index) and Section 2.6 (finite differences)
---

## In plain words

A loop variable often follows a simple rule: start at some value, then add a fixed amount each time, or add an amount that itself grows by a fixed amount, or multiply by a fixed factor. A chain of recurrences writes this rule as a short list: the start value, then the first step, then the step of the step, and so on, with a plus or a times between them. The list is enough to compute every value with a few additions per iteration, and it has a closed formula in the iteration number. Sums and products of such lists are again such lists, by simple rules, so a compiler can describe every expression of a loop that is built from counters. LLVM calls its version of this analysis scalar evolution.

## When it applies

Use a chain of recurrences (CR) when a value is a function of the iteration number $i = 0, 1, 2, \dots$ of a loop and is built from:

- the loop counter and loop-invariant values,
- additions, subtractions and multiplications by loop-invariant values or by other chains of the same loop,
- loop-carried updates of the form `v = v + e` or `v = c * v`, where `e` is itself a chain or invariant and `c` is invariant.

The chains then describe exactly the polynomial sequences (pure sums), the geometric sequences and their generalizations $\prod_j \varphi_j^{\binom{i}{j}}$ (pure products), and mixtures of them. Two uses are common. A compiler uses the chain to recognize and classify [induction variables](/induction-variable-analysis/), to get closed forms for [dependence testing](/dependence-testing/) and trip counts, and to replace multiplications by additions ([strength reduction](/strength-reduction/)). A numerical program uses the chain to evaluate a function on a regular grid $x_0, x_0 + h, x_0 + 2h, \dots$ with a few additions per point instead of a full [polynomial evaluation](/polynomial-evaluation/) at each point, which was the original aim of Bachmann, Wang and Zima.

It does not apply to values that change under a condition, values read from memory, or sequences with no closed form of these shapes. A compiler marks those as unknown.

## The template

**Notation.** A chain of recurrences is

$$\Phi = \{\varphi_0, \odot_1, \varphi_1, \odot_2, \dots, \odot_k, \varphi_k\}, \qquad \odot_j \in \{+, *\},$$

where the $\varphi_j$ do not depend on $i$. The number $k$ is the length. The tail $\Phi_j = \{\varphi_j, \odot_{j+1}, \dots, \varphi_k\}$ is again a chain, and $\Phi_k$ is the constant $\varphi_k$. The value at $i$ is defined from the tail:

$$\{\varphi_0, +, \Phi_1\}(i) = \varphi_0 + \sum_{m=0}^{i-1} \Phi_1(m), \qquad \{\varphi_0, *, \Phi_1\}(i) = \varphi_0 \cdot \prod_{m=0}^{i-1} \Phi_1(m).$$

So $\Phi(0) = \varphi_0$ and $\Phi(i+1) = \Phi(i) \odot_1 \Phi_1(i)$. A chain with only $+$ is a **pure sum**, one with only $*$ is a **pure product**. In a compiler a chain belongs to one loop $L$, written $\{\varphi_0, +, \varphi_1\}_L$ (LLVM prints `{start,+,step}<loop>`), and a coefficient may be a chain of an outer loop, which is invariant in $L$.

**Evaluation.** Keep one register per coefficient and update the registers from left to right:

```pseudo id=main
EVAL-CR(φ[0..k], op[1..k], N)
L1  r ← copy of φ[0..k]
L2  for n ← 0 to N − 1
L3      output r[0]
L4      for j ← 0 to k − 1
L5          r[j] ← r[j] op[j+1] r[j+1]
```

Before iteration $n$ of the outer loop, $r[j] = \Phi_j(n)$ for every $j$. Line L5 reads $r[j+1]$ before it is changed, because the updates go from left to right, so it sets $r[j]$ to $\Phi_j(n) \odot_{j+1} \Phi_{j+1}(n) = \Phi_j(n+1)$. The loop outputs $\Phi(0), \dots, \Phi(N-1)$ with $k$ operations per value.

**Closed forms.** For a pure sum and a pure product,

$$\{\varphi_0, +, \varphi_1, +, \dots, +, \varphi_k\}(i) = \sum_{j=0}^{k} \varphi_j \binom{i}{j}, \qquad \{\varphi_0, *, \varphi_1, *, \dots, *, \varphi_k\}(i) = \prod_{j=0}^{k} \varphi_j^{\binom{i}{j}}.$$

*Proof.* Induction on $k$. For $k = 0$ both sides are $\varphi_0$, because $\binom{i}{0} = 1$. For $k \ge 1$, the tail $\Phi_1$ has length $k - 1$, so by the induction hypothesis $\Phi_1(m) = \sum_{j=1}^{k} \varphi_j \binom{m}{j-1}$. Then

$$\Phi(i) = \varphi_0 + \sum_{m=0}^{i-1} \sum_{j=1}^{k} \varphi_j \binom{m}{j-1} = \varphi_0 + \sum_{j=1}^{k} \varphi_j \sum_{m=0}^{i-1} \binom{m}{j-1} = \varphi_0 + \sum_{j=1}^{k} \varphi_j \binom{i}{j}.$$

The last step is the identity $\sum_{m=0}^{i-1} \binom{m}{j-1} = \binom{i}{j}$ for $j \ge 1$. It follows from Pascal's rule $\binom{m+1}{j} = \binom{m}{j} + \binom{m}{j-1}$: summing $\binom{m+1}{j} - \binom{m}{j} = \binom{m}{j-1}$ over $m = 0, \dots, i-1$ telescopes to $\binom{i}{j} - \binom{0}{j} = \binom{i}{j}$, since $\binom{0}{j} = 0$ for $j \ge 1$. The product form has the same proof with sums of exponents in place of sums, when all $\varphi_j \ne 0$. $\square$

So a pure sum of length $k$ is a polynomial of degree at most $k$ in $i$, and the coefficients $\varphi_j$ are the forward differences $\Delta^j \Phi(0)$ of the sequence ([finite differences](/finite-differences/), Newton's forward formula of [Newton interpolation](/newton-interpolation/)). Conversely, every polynomial $p$ of degree $k$ is the pure sum $\{\Delta^0 p(0), +, \Delta^1 p(0), +, \dots, +, \Delta^k p(0)\}$.

**Rules.** Let $c$ be invariant, $\Phi = \{\varphi_0, +, \Phi_1\}$ and $\Psi = \{\psi_0, +, \Psi_1\}$ pure sums of the same loop. Each rule follows from the closed form or from $\Phi(i+1) = \Phi(i) + \Phi_1(i)$:

| expression | chain |
|---|---|
| $c + \Phi$ | $\{\varphi_0 + c, +, \varphi_1, \dots, +, \varphi_k\}$ |
| $c \cdot \Phi$ | $\{c\varphi_0, +, c\varphi_1, \dots, +, c\varphi_k\}$ |
| $\Phi + \Psi$ | add the coefficients term by term, after padding the shorter chain with zeros |
| $\Phi \cdot \Psi$ | $\{\varphi_0\psi_0, +, \Phi\Psi_1 + \Phi_1\Psi + \Phi_1\Psi_1\}$, flattened |
| $\{a, +, b\} \cdot \{c, +, d\}$ | $\{ac, +, ad + bc + bd, +, 2bd\}$ |
| $c^{\Phi}$ | $\{c^{\varphi_0}, *, c^{\varphi_1}, \dots, *, c^{\varphi_k}\}$ |
| $\{a, *, r\} \cdot \{b, *, s\}$ | $\{ab, *, rs\}$ |
| $\Phi(i+1)$ | $\{\varphi_0 + \varphi_1, +, \varphi_1 + \varphi_2, \dots, +, \varphi_k\}$ |

The product rule comes from $(\Phi\Psi)(i+1) = (\Phi + \Phi_1)(\Psi + \Psi_1)(i)$, so the step of $\Phi\Psi$ is $\Phi\Psi_1 + \Phi_1\Psi + \Phi_1\Psi_1$, which is shorter in total length, so the recursion stops. For two chains of length 1: $(a + bi)(c + di) = ac + (ad + bc)i + bd\,i^2$, and $ac + (ad + bc + bd)\binom{i}{1} + 2bd\binom{i}{2}$ is the same polynomial.

**Building the chains of a loop (compiler use).**

1. The normalized counter of loop $L$ is $\{0, +, 1\}_L$. A loop-invariant value $c$ is the chain $c$ of length 0.
2. Visit the SSA names of the loop so that operands come before uses, and handle each cycle through a header φ as one unit (the strongly connected components of [induction variable analysis](/induction-variable-analysis/)).
3. For a header φ `v = φ(init, v + e)` where $e$ has the chain $E$, set $v = \{init, +, E\}$, flattened: if $E = \{e_0, +, \dots\}$ then $v = \{init, +, e_0, +, \dots\}$. For `v = φ(init, c * v)`, set $v = \{init, *, c\}$.
4. For other operations, apply the rules. A name defined after the update in the same iteration, such as `i2 = i1 + 1`, gets the shifted chain $\{1, +, 1\}$.
5. Where no rule applies, mark the name as unknown, and every expression that uses it too.
6. Use the chain: read the closed form, evaluate it at the last iteration for a trip count or an exit value, or emit the registers of EVAL-CR as new induction variables.

## Classic examples

**Evaluating a polynomial on a grid.** Let $p(n) = 3n^2 + 2n + 1$. With $n = \{0, +, 1\}$, the rules give $n^2 = \{0, +, 1\} \cdot \{0, +, 1\} = \{0, +, 1, +, 2\}$, so $3n^2 = \{0, +, 3, +, 6\}$, $2n = \{0, +, 2\}$, and

$$p = \{1, +, 5, +, 6\}.$$

EVAL-CR starts with the registers $(1, 5, 6)$ and outputs $1, 6, 17, 34, 57, 86$, with two additions per value and no multiplication. These are $p(0), \dots, p(5)$, and $1, 5, 6$ are $p(0)$, $\Delta p(0) = 5$ and $\Delta^2 p(0) = 6$. In the same way $n^3 = \{0, +, 1, +, 6, +, 6\}$; the closed form gives $n + 6\binom{n}{2} + 6\binom{n}{3} = n^3$.

**The loop of the induction variable page.** In the example loop of [induction variable analysis](/induction-variable-analysis/):

| SSA name | definition | chain | closed form |
|---|---|---|---|
| `i1` | `φ(0, i1 + 1)` | $\{0, +, 1\}$ | $n$ |
| `t` | `4 * i1 + 8` | $\{8, +, 4\}$ | $4n + 8$ |
| `j1` | `φ(5, j1 + i1)` | $\{5, +, 0, +, 1\}$ | $5 + \binom{n}{2}$ |
| `k1` | `φ(1, 2 * k1)` | $\{1, *, 2\}$ | $2^n$ |
| `x1` | `φ(1, 2 * x1 + 1)` | $\{1, +, 2, *, 2\}$ | $2^{n+1} - 1$ |

The values of `j1` are $5, 5, 6, 8, 11, 15$. The last row is a mixed chain: its step $\{2, *, 2\}$ is $2^{n+1}$, so $x(n) = 1 + \sum_{m < n} 2^{m+1} = 2^{n+1} - 1$, which gives $1, 3, 7, 15, 31, 63$.

**Two nested loops.** For `for i in 0..M: for j in 0..N: A[i*N + j]`, the subscript is $\{\{0, +, N\}_{L_1}, +, 1\}_{L_2}$. The start value of the inner chain is a chain of the outer loop, and both are pure sums with invariant coefficients, so the subscript is affine in $(i, j)$ and the [practical dependence tests](/practical-dependence-tests/) apply. With $N = 5$ the inner loop starts at $0, 5, 10, \dots$ and steps by 1.

**Strength reduction.** The chain $\{8, +, 4\}$ of `t` says that `t` can be its own register, set to 8 before the loop and increased by 4 at the end of each iteration, as in [operator strength reduction](/operator-strength-reduction/). For $\{5, +, 0, +, 1\}$ two registers do the job, and no multiplication is needed for a polynomial of any degree.

## Variations

- **Mixed chains.** Chains with both $+$ and $*$, such as $\{1, +, 2, *, 2\}$ above, describe sums of polynomials times geometric terms. Their closed forms are found by the definition, one level at a time, and do not have the single binomial formula.
- **Multivariate chains.** A chain whose coefficients are chains of outer loops, as in the nested example, describes a function of all loop counters of a nest. Later work on chains uses the same idea to evaluate functions of two variables on a grid, for example to plot surfaces.
- **Symbolic coefficients.** A coefficient can be an invariant name such as $N$. The rules stay the same, with symbolic arithmetic in the coefficients, as in a computer algebra system.
- **Monotonic ranges.** If $\varphi_1, \dots, \varphi_k \ge 0$ in a pure sum, then $\Phi(i+1) - \Phi(i) = \Phi_1(i) = \sum_{j \ge 1} \varphi_j \binom{i}{j-1} \ge 0$, so the sequence is nondecreasing, and its range over $0 \le i < N$ is $[\Phi(0), \Phi(N-1)]$. Bounds of this kind let a dependence test handle some nonlinear subscripts.
- **Scalar evolution in LLVM.** LLVM's ScalarEvolution builds add recurrences `{start,+,step}<loop>`, with more operands for higher degree, together with flags that say whether the arithmetic can wrap. It uses them for trip counts, exit values, and the subscripts of its dependence analysis. The alias "scalar evolution" on this page is that name; it is the compiler analysis built on chains, not a different mathematical object.
- **Periodic and wrap-around values.** Plain chains do not describe a value that flips between two states or has one special first value. Later work extends the notation for these cases, or peels the first iteration so that the rest is a chain.

## Pitfalls

- **Machine integers.** EVAL-CR uses only additions and multiplications, so on $w$-bit integers it computes $\Phi(i) \bmod 2^w$ exactly. The closed form does not: $\binom{i}{j}$ has a division by $j!$, which must happen before the reduction. On 8 bits, $\binom{23}{2} = 253$, but $(23 \cdot 22 \bmod 256) / 2 = 125$. For signed types in C, an overflow is undefined behavior, which lets a compiler assume no wrap; for unsigned types the wrap is defined and the chain only holds modulo $2^w$. Check for [integer overflow](/integer-overflow/) before a closed form is used for a trip count or a dependence test.
- **Iteration numbering.** The chain gives the value at the start of iteration $i$ for a header φ. A name defined after the update, such as `i2 = i1 + 1`, has the chain $\{1, +, 1\}$, not $\{0, +, 1\}$. Mixing the two numberings shifts every subscript by one step.
- **Chains are not unique as written.** $\{0, +, 1, +, 0\}$ and $\{0, +, 1\}$ are the same function, and so are $\{a, *, 1\}$ and $a$. Remove trailing zeros (in sums) and trailing ones (in products) before comparing two chains.
- **The step must be invariant or a chain of the same loop.** `v = v + x` with an `x` that is loaded from memory in each iteration is not a chain. Building a chain from it gives a wrong closed form, not just a weak one.
- **Products grow the chain.** The product of chains of lengths $k$ and $l$ has length $k + l$, and $n^d$ has length $d$. Repeated products give long chains with large coefficients; compilers stop at a fixed length and mark the rest as unknown.
- **Floating point.** With floating-point coefficients, EVAL-CR adds a rounding error at each step and the errors build up over many iterations. For long runs, compute some values again from the closed form, or use exact or wider arithmetic for the registers.
- **A product chain with a zero coefficient.** In $\{a, *, 0\}$ every value after the first is 0. The closed form $\prod \varphi_j^{\binom{i}{j}}$ is still correct with the rule $0^0 = 1$, but code that takes logarithms of the coefficients fails.

## Exercises

1. Find the pure sum chain of $n^3$ in two ways: from the forward differences of $0, 1, 8, 27$, and from the product rule applied to $n^2 = \{0, +, 1, +, 2\}$ and $n = \{0, +, 1\}$.
   <details><summary>Hint</summary>Both give $\{0, +, 1, +, 6, +, 6\}$. Check it with $n + 6\binom{n}{2} + 6\binom{n}{3}$.</details>
2. Prove the rule $\{a, +, b\} \cdot \{c, +, d\} = \{ac, +, ad + bc + bd, +, 2bd\}$ from the closed form of a pure sum.
3. Prove the closed form of a pure product chain by induction on its length, and say where the proof needs nonzero coefficients.
   <details><summary>Hint</summary>Take logarithms, or repeat the proof of the pure sum with products of powers. The case with a zero coefficient needs a separate check of $0^0 = 1$.</details>
4. A loop runs `s = φ(0, s + t)` and `t = φ(1, t + 2)`. Give the chains of `t` and `s`, their closed forms, and the values for $n = 0, \dots, 5$.
   <details><summary>Hint</summary>$t = \{1, +, 2\} = 2n + 1$ and $s = \{0, +, 1, +, 2\} = n^2$: the sum of the first $n$ odd numbers.</details>
5. On 8-bit unsigned integers, run EVAL-CR for $\{0, +, 0, +, 1\}$ for 30 steps and compare each value with $\binom{n}{2} \bmod 256$ and with $(n(n-1) \bmod 256) / 2$. At which $n$ does the second formula first differ?
6. Show that a pure sum chain with $\varphi_1 \ge 0, \dots, \varphi_k \ge 0$ is nondecreasing, and give a chain with $\varphi_1 < 0$ that is still nondecreasing for all $n \ge 1$.

## References
