---
tag: 154J38
kind: definition
slug: specification
name: Specification
aliases:
- Formal specification
- Problem specification
area: foundations/correctness-and-invariants
level: intro
summary: A precise statement of what an algorithm must do, relating inputs to required outputs.
prereqs: []
see_also: [precondition, postcondition, correctness, hoare-triple, total-correctness, design-by-contract]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 1.1
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580
---

A specification is a precise statement of what a program or algorithm must do. It lists the legal inputs with a [precondition](/precondition/) and it states the right outputs for each of them with a [postcondition](/postcondition/). A program is [correct](/correctness/) when it meets its specification.

## Definition

Let $X$ be a set of inputs and $Y$ a set of outputs. A specification is a pair $(P, Q)$ where $P \subseteq X$ is a precondition and $Q \subseteq X \times Y$ is a postcondition. Write $P(x)$ for $x \in P$ and $Q(x, y)$ for $(x, y) \in Q$. A program $A$ meets $(P, Q)$ when

$$\forall x \in X : \ P(x) \Rightarrow \big( A \text{ stops on } x \ \wedge \ Q(x, A(x)) \big).$$

This is [total correctness](/total-correctness/). The program is partially correct for $(P, Q)$ when $\forall x \in X : \big( P(x) \wedge A \text{ stops on } x \big) \Rightarrow Q(x, A(x))$. The stop is a hypothesis here and not a goal. See [partial correctness](/partial-correctness/). Total correctness is partial correctness plus termination on each $x$ with $P(x)$. A specification says what the program computes and does not say how. Many programs can meet the same specification.

The relation $Q$ may allow several outputs for one input. Then the specification is non-deterministic, and a program may return any of them. If for each $x$ with $P(x)$ there is exactly one $y$ with $Q(x, y)$, then $Q$ defines a function on $P$. The opposite case is a pitfall. If some $x$ with $P(x)$ has no $y$ with $Q(x, y)$, then no program meets $(P, Q)$. A good specification is satisfiable: $\forall x \,(P(x) \Rightarrow \exists y \, Q(x, y))$.

## Examples and non-examples

- **Integer square root.** $X = Y = \mathbb{Z}$. $P(n)$ is $n \ge 0$. $Q(n, r)$ is $r^2 \le n < (r+1)^2$. For each $n \ge 0$ there is exactly one such $r$. Proof. Each solution is non-negative: from $r^2 \le n < (r+1)^2$ we get $r^2 < (r+1)^2$, so $2r + 1 > 0$ and $r \ge 0$. Existence: the set of $r \ge 0$ with $r^2 \le n$ holds $0$, and each element is at most $\max(n, 1)$ because $r \le r^2$ for an integer $r \ge 1$, so the set has a largest element $r$. Then $r + 1$ is not in the set, so $(r+1)^2 > n$. Uniqueness: if $0 \le r_1 < r_2$ both satisfied $Q$ for $n$, then $r_1 + 1 \le r_2$ and $(r_1+1)^2 \le r_2^2 \le n < (r_1+1)^2$, a contradiction. The program ISQRT of the page on [correctness](/correctness/) meets it.
- **Sorting.** $X = Y$ is the set of finite arrays of numbers. $P$ is true. $Q(A, B)$ says that $B$ is a permutation of $A$ and $B[0] \le B[1] \le \cdots$. See the [sorting problem](/sorting-problem/).
- **Search in a sorted array (non-deterministic).** $P(A, key)$: $A$ is non-decreasing. $Q(A, key, i)$: either $0 \le i < m$ and $A[i] = key$ (with $m$ the length of $A$), or $i = -1$ and $key$ does not occur in $A$. When $key$ occurs twice, two outputs are right. The [binary search](/binary-search/) returns one of them.
- **Non-example: too weak.** $Q(n, r)$ is $r^2 \le n$. The constant program $r = 0$ meets it for each $n \ge 0$. The pair $(P, Q)$ is a specification in the sense above, but it does not describe integer square root. Compare $n = 10$: both $r = 0$ and $r = 3$ meet it, and only $r = 3$ meets the exact one.
- **Non-example: not satisfiable.** Take $P$ = true for integer square root, with the same $Q$. For $n = -1$ no $r$ has $r^2 \le -1$, so no program meets this pair. The precondition $n \ge 0$ removes the problem.
- **Non-example: not precise.** "Return a number close to $\sqrt n$" is not a specification. No test or proof can decide whether $r = 2$ is close enough for $n = 10$.
- **Non-example: a method.** "Search for $r$ by halving an interval" describes an algorithm. It does not say what the result must satisfy.

## Related definitions

- [Precondition](/precondition/): the first half of a specification, the assumption on the input.
- [Postcondition](/postcondition/): the second half, the guarantee on the output.
- [Hoare triple](/hoare-triple/): a specification written as $\{P\}\ S\ \{Q\}$ for a program text $S$.
- [Partial correctness](/partial-correctness/) and [total correctness](/total-correctness/): the two ways in which a program can meet a specification.
- [Design by contract](/design-by-contract/): a method where the specification of each routine is part of its code.
- [Weakest precondition](/weakest-precondition/): the largest precondition under which a program meets a given postcondition.

## References
