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
summary: A precise statement of what an algorithm must do, given as a precondition on the inputs and a postcondition that relates each input to the outputs that are right for it.
prereqs: []
see_also: [precondition, postcondition, correctness, hoare-triple, total-correctness, design-by-contract, refinement-calculus]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 1.1 (the sorting problem stated as an input and an output relation, and the definition of a correct algorithm)
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580
  - book: isbn:9780521543101
    title: Michael Huth and Mark Ryan, Logic in Computer Science, second edition, Cambridge University Press (2004)
    locator: Chapter 4, Sections 4.1 and 4.2 (why to specify code, Hoare triples, program and logical variables)
  - book: isbn:9780387964805
    title: David Gries, The Science of Programming, Springer (1981)
    locator: Part II (specifications as pairs of predicates, and the derivation of programs from them)
---

A specification is a precise statement of what a program or algorithm must do. It gives the legal inputs with a [precondition](/precondition/), and the right outputs for each legal input with a [postcondition](/postcondition/). A program is [correct](/correctness/) when it meets its specification. The specification says what to compute and not how, so many different programs can meet the same one.

## Definition

### Specifications of input and output

Let $X$ be a set of inputs and $Y$ a set of outputs. A **specification** is a pair $(P, Q)$ with $P \subseteq X$, the precondition, and $Q \subseteq X \times Y$, the postcondition. Write $P(x)$ for $x \in P$ and $Q(x, y)$ for $(x, y) \in Q$. A deterministic program $A$ **meets** $(P, Q)$ when

$$\forall x \in X : \ P(x) \Rightarrow \big( A \text{ stops on } x \ \wedge \ Q(x, A(x)) \big).$$

This is [total correctness](/total-correctness/). The program is **partially correct** for $(P, Q)$ when $\forall x \in X : \big( P(x) \wedge A \text{ stops on } x \big) \Rightarrow Q(x, A(x))$. Here the stop is a hypothesis and not a goal. See [partial correctness](/partial-correctness/).

The postcondition is a relation between the input and the output, not a function. For one input it can accept several outputs. A specification is **deterministic** when each $x$ with $P(x)$ has exactly one $y$ with $Q(x, y)$; then $Q$ defines a function on $P$. Otherwise it is **non-deterministic**, and a program may return any accepted output. Two programs that meet the same non-deterministic specification can return different outputs on the same input.

A specification is **satisfiable** (also called feasible or implementable) when

$$\forall x \in X : \ P(x) \Rightarrow \exists y \in Y : Q(x, y).$$

If it is not satisfiable, no program meets it: an input $x$ with $P(x)$ and no accepted output makes the formula of "meets" false for every program. The converse needs a remark. A satisfiable specification is met by some function from $P$ to $Y$, but that function may not be computable, so a satisfiable specification can still have no algorithm. The specification "on input a program text $x$, return 1 if $x$ stops on the empty input and 0 otherwise" is satisfiable and deterministic, and no algorithm meets it, because the [halting problem](/halting-problem/) is undecidable.

### Specifications of programs with state

A program that changes variables is specified over states. A state $\sigma$ gives a value to each variable. The precondition $P$ and the postcondition $Q$ are predicates on states, and the [Hoare triple](/hoare-triple/) $\{P\}\ S\ \{Q\}$ (partial) or $[P]\ S\ [Q]$ (total) states that the program text $S$ meets them. Two devices let a postcondition on states relate the output to the input.

- **Logical variables.** A variable such as $x_0$ that does not occur in $S$ names the start value: the precondition says $x = x_0$, and the postcondition can then use $x_0$. A program cannot change $x_0$, so the reference stays fixed. Huth and Ryan (Section 4.2.4) use this device.
- **Frame conditions.** A postcondition must say which variables keep their values. Without "$A = A_0$", a search routine that overwrites the array could meet the rest of its postcondition.

### The refinement order

A specification $(P_2, Q_2)$ **refines** $(P_1, Q_1)$ when

$$\forall x : \ P_1(x) \Rightarrow P_2(x) \qquad \text{and} \qquad \forall x, y : \ \big( P_1(x) \wedge Q_2(x, y) \big) \Rightarrow Q_1(x, y).$$

In words: the new specification accepts at least the old inputs, and on each old input it accepts only outputs that the old one accepts.

**Claim.** If $(P_2, Q_2)$ refines $(P_1, Q_1)$ and $A$ meets $(P_2, Q_2)$, then $A$ meets $(P_1, Q_1)$.

*Proof.* Take $x$ with $P_1(x)$. By the first condition, $P_2(x)$. Since $A$ meets $(P_2, Q_2)$, $A$ stops on $x$ and $Q_2(x, A(x))$. By the second condition with $y = A(x)$, $Q_1(x, A(x))$. So $A$ stops on $x$ with an output that $Q_1$ accepts. $\square$

The same proof works for partial correctness, with "if $A$ stops" as a hypothesis. So a weaker precondition and a stronger postcondition give a more demanding specification, and a program for it can replace a program for the old one at every call. This order is the base of the [refinement calculus](/refinement-calculus/) and of the rule for subtypes in [design by contract](/design-by-contract/).

## Examples and non-examples

### Integer square root

$X = Y = \mathbb{Z}$. $P(n)$ is $n \ge 0$. $Q(n, r)$ is $r^2 \le n < (r+1)^2$. This specification is deterministic: for each $n \ge 0$ exactly one integer $r$ satisfies $Q(n, r)$.

*Proof.* Each solution is non-negative: $r^2 \le n < (r+1)^2$ gives $r^2 < (r+1)^2$, so $0 < 2r + 1$ and $r \ge 0$. Existence: the set $\{ r \in \mathbb{Z} : r \ge 0, \ r^2 \le n \}$ contains $0$, and each element is at most $n$, because $r \le r^2 \le n$ for $r \ge 1$. A finite non-empty set of integers has a largest element $r$. Then $r + 1$ is not in the set, so $(r+1)^2 > n$. Uniqueness: if $0 \le r_1 < r_2$ both satisfied $Q$, then $r_1 + 1 \le r_2$, so $(r_1+1)^2 \le r_2^2 \le n < (r_1+1)^2$, a contradiction. $\square$

For $n = 10$ the output is $3$, since $9 \le 10 < 16$. The program ISQRT on the page [correctness](/correctness/) meets the specification.

### Sorting

$X = Y$ is the set of finite sequences over a totally ordered set. $P$ is true. $Q(A, B)$ holds when $B$ is a permutation of $A$ and $B[0] \le B[1] \le \cdots \le B[m-1]$, where $m$ is the length. CLRS (Section 1.1) states the [sorting problem](/sorting-problem/) in this form. The specification is deterministic: each sequence has exactly one non-decreasing permutation. Both parts of $Q$ are needed.

- Drop "is a permutation of $A$". The program that returns the empty sequence, or $m$ copies of $0$, meets the rest for each input.
- Drop "non-decreasing". The identity program meets the rest.

A **stable** sort has a stronger specification: the items carry keys, and items with equal keys keep their input order. The new $Q$ implies the old one, so the stable specification refines the plain one, and each stable sort is a sort. The converse fails: on input $[(1, a), (1, b)]$, sorted by the first component, the plain specification accepts $[(1, b), (1, a)]$ and the stable one does not.

### Search: a non-deterministic specification

$P(A, k)$: the array $A$ of length $m$ is non-decreasing. $Q((A, k), i)$: either $0 \le i < m$ and $A[i] = k$, or $i = -1$ and $k$ does not occur in $A$. For $A = [1, 3, 3, 5]$ and $k = 3$, both $i = 1$ and $i = 2$ are accepted. The [binary search](/binary-search/) of this site returns $2$, and a [linear search](/linear-search/) returns $1$. Both programs meet the specification.

The specification "return the least $i$ with $A[i] \ge k$, or $m$ if none exists" is deterministic. Its precondition is the same. A program for it, followed by the test "if $i < m$ and $A[i] = k$ then return $i$, else return $-1$", meets the search specification, and on $[1, 3, 3, 5]$ with $k = 3$ it returns $1$.

### Non-examples

- **Too weak.** $Q(n, r)$: $r^2 \le n$. The constant program $r = 0$ meets it for each $n \ge 0$. The pair is a specification in the formal sense, but not of the integer square root. For $n = 10$, each of the seven integers $-3$ to $3$ is accepted, and only $3$ is right.
- **Not satisfiable.** Take $P$ true and $Q(n, r)$: $r^2 \le n < (r+1)^2$ over $\mathbb{Z}$. For $n = -1$ no integer $r$ has $r^2 \le -1$, so no program meets the pair. The precondition $n \ge 0$ is the exact repair: $Q(n, r)$ implies $0 \le r^2 \le n$, so every satisfiable precondition for this $Q$ implies $n \ge 0$.
- **Not precise.** "Return a number close to $\sqrt n$" is not a specification. No test and no proof can decide whether $r = 2$ is close enough for $n = 10$. The version "$|r - \sqrt n| \le 1$" is precise, and non-deterministic: for $n = 10$ it accepts $3$ and $4$, because $\sqrt{10} \approx 3.162$.
- **A method, not a specification.** "Find $r$ by halving an interval" describes an algorithm. It says nothing about the result that a different algorithm must give.

### Pitfalls

- **Forgetting the frame.** A postcondition on the outputs alone lets the program change other data. State what stays unchanged.
- **Using a program variable for the old value.** After $x \leftarrow x + 1$, the postcondition $x = x + 1$ is false in every state. Name the start value with a logical variable: $x = x_0 + 1$.
- **Specifying the method.** A specification that says "use binary search" excludes correct programs and makes proofs harder. Put the method in the program, and the result in the specification.
- **Silent preconditions.** A routine that needs a sorted array, a non-zero divisor or a non-empty input must say so in $P$. A hidden assumption is still an assumption, and callers break it.
- **Floating point.** A postcondition such as $y = \sqrt x$ is not satisfiable with floating-point outputs for most $x$. State the allowed error.

## Related definitions

- [Precondition](/precondition/): the first half, the assumption on the input.
- [Postcondition](/postcondition/): the second half, the guarantee on the output.
- [Hoare triple](/hoare-triple/): a specification attached to a program text, $\{P\}\ S\ \{Q\}$ or $[P]\ S\ [Q]$.
- [Partial correctness](/partial-correctness/) and [total correctness](/total-correctness/): the two ways in which a program can meet a specification.
- [Weakest precondition](/weakest-precondition/): for a fixed program and postcondition, the largest precondition under which the program meets the pair.
- [Design by contract](/design-by-contract/): the specification of each routine is written in its code.
- [Refinement calculus](/refinement-calculus/): a method that turns a specification into a program by steps of refinement.
- [Representation invariant](/representation-invariant/) and [abstraction function](/abstraction-function/): how a specification over abstract values applies to a concrete data structure.

## References
