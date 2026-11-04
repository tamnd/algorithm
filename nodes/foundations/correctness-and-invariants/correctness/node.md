---
tag: KMBB0X
kind: concept
slug: correctness
name: Algorithm correctness
aliases:
- Correctness of algorithms
- Partial and total correctness
area: foundations/correctness-and-invariants
level: intro
summary: An algorithm is correct for a specification when, on every input that the precondition allows, it stops with an output that the postcondition accepts.
prereqs: [loop-invariant, specification]
see_also: [hoare-triple, partial-correctness, total-correctness, termination-proof, variant-function, hoare-logic, program-verification, property-based-testing]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 1.1 (the definition of a correct algorithm) and Section 2.1 (loop invariants, with initialization, maintenance and termination)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.1 (the finiteness of an algorithm) and Section 1.2.1 (the proof of Algorithm E by assertions)
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580
  - book: isbn:9780521543101
    title: Michael Huth and Mark Ryan, Logic in Computer Science, second edition, Cambridge University Press (2004)
    locator: Chapter 4, Sections 4.1 and 4.2.3 (why to specify and verify code, partial and total correctness)
---

An algorithm is correct with respect to a [specification](/specification/) when, for every input that the [precondition](/precondition/) allows, it stops and its output satisfies the [postcondition](/postcondition/). The claim is about all legal inputs at once, so a finite set of tests can refute it but cannot establish it. A proof has two parts: [partial correctness](/partial-correctness/) (if the algorithm stops, the output is right) and termination (the algorithm stops). Together they give [total correctness](/total-correctness/).

## In plain words

You cannot call an algorithm correct until you say what it must do. That statement is the specification. It says which inputs are legal, and which outputs are right for each legal input.

The algorithm is correct when two things hold for every legal input: it stops, and its output is right. A test runs the algorithm on a few inputs. A failed test shows a bug. A passed test says nothing about the inputs that you did not try. A proof covers every input at once.

Most of the work of a proof is about loops and recursion. For a loop, you find a fact that stays true at each pass and gives the right answer when the loop ends. Then you find a count that goes down at each pass and cannot go down forever, so the loop ends.

## The idea

### The statement

Let $X$ be the set of inputs and $Y$ the set of outputs. A specification is a pair $(P, Q)$: a precondition $P(x)$ on inputs and a postcondition $Q(x, y)$ on an input and an output. A deterministic algorithm $A$ is totally correct for $(P, Q)$ when

$$\forall x \in X : \ P(x) \Rightarrow \big( A \text{ stops on } x \ \wedge \ Q(x, A(x)) \big).$$

The formula is the conjunction of two statements, and each one has its own proof method.

- **Partial correctness:** $\forall x \in X : \big( P(x) \wedge A \text{ stops on } x \big) \Rightarrow Q(x, A(x))$. The tool for a loop is a [loop invariant](/loop-invariant/). In general it is a set of [assertions](/assertion/) at the points of the program, as in [Floyd's inductive assertions](/floyd-inductive-assertions/) or in the rules of [Hoare logic](/hoare-logic/). The statement is written as the [Hoare triple](/hoare-triple/) $\{P\}\ A\ \{Q\}$.
- **Termination:** $\forall x \in X : P(x) \Rightarrow A \text{ stops on } x$. The tool is a [variant function](/variant-function/): a quantity in a set with a [well-founded relation](/well-founded-relation/), usually a non-negative integer, that becomes smaller at each pass of a loop or at each recursive call. See [termination proof](/termination-proof/).

The page on [total correctness](/total-correctness/) proves that, for a deterministic program, the conjunction of the two is equivalent to the formula above. CLRS (Section 1.1) gives the same definition in words: a correct algorithm halts on every input instance with the correct output.

The formula says nothing about inputs outside $P$. On them the algorithm may stop with any output, fail or run forever. So the precondition is part of the claim. "ISQRT is correct" is meaningless; "ISQRT is correct for $n \ge 0$ and $r^2 \le n < (r+1)^2$" is a claim that a proof can establish.

### Recursion

For a recursive algorithm, the proof is a [strong induction](/induction/) on a measure of the input with values in $\mathbb{N}$, or more generally in a well-founded set. The induction hypothesis is that every call on an input with a smaller measure meets the specification. The proof then checks two things: the base cases meet the specification directly, and each recursive call is on an input with a smaller measure that satisfies the precondition of the call. The second check gives termination as well. For example, [merge sort](/merge-sort/) on a range of length $m \ge 2$ calls itself on two ranges of lengths $\lfloor m/2 \rfloor$ and $\lceil m/2 \rceil$, both less than $m$, so it is correct for all lengths by strong induction on $m$.

### Why testing is not enough

A test checks the formula for one chosen $x$. A wrong output on $x$ is a counterexample, and the claim is false. A right output on $x$ leaves the claim open for every other input. When the input set is finite and small, an exhaustive test is a proof. For a 32-bit input there are $2^{32} = 4294967296$ cases, which a computer can try. For two 64-bit inputs there are $2^{128}$ cases, which no computer can try. [Property-based testing](/property-based-testing/) and [differential testing](/differential-testing/) choose many inputs at random or by a rule. They find bugs fast, but they do not prove that no bug is left. The bug in the examples below shows how a single bad input can hide among millions of good ones.

### No general method

No algorithm takes any program and any specification and decides whether the program is correct. Proof: let $H_w$ be the program that ignores its input, runs a given program $M$ on a fixed input $w$, and then returns $0$. Then $H_w$ is totally correct for $(\mathrm{true}, \ y = 0)$ exactly when $M$ stops on $w$. A decision method for total correctness would decide the [halting problem](/halting-problem/), which is undecidable. For partial correctness the same program gives a stronger result: $H_w$ is partially correct for $(\mathrm{true}, \ \mathrm{false})$ exactly when $M$ does not stop on $w$. So the set of true partial correctness claims is not even recursively enumerable. Both facts are also instances of [Rice's theorem](/rice-theorem/). In practice, a person or a tool finds the invariants and the variants for each algorithm, and a checker verifies the steps.

### Other notions of correctness

- **Randomized algorithms.** A [Monte Carlo algorithm](/monte-carlo-algorithm/) is correct with error probability at most $\delta$: for each legal input $x$, $\Pr[Q(x, A(x))] \ge 1 - \delta$, where the probability is over the random choices of $A$ only, not over the inputs. A [Las Vegas algorithm](/las-vegas-algorithm/) always gives a right output, and its running time is a random variable.
- **Approximation and numerical algorithms.** The postcondition states the allowed error, for example $|y - f(x)| \le \varepsilon\,|f(x)|$. The proof is then about the error bound.
- **Reactive systems.** A server or an operating system is not meant to stop. Its specification is a property of its infinite runs, such as "each request gets an answer", and the methods are different. This page is about algorithms that take an input and stop.

### Pitfalls

- **A proof about the wrong model.** A proof with mathematical integers does not cover a program with 64-bit integers. In ISQRT below, for the largest signed 64-bit value $n = 2^{63} - 1$, the start value $hi = n + 1 = 2^{63}$ is out of range, and the first midpoint $2^{62}$ has the square $2^{124}$. Both overflow. See [integer overflow](/integer-overflow/). The proof must state the model, or the program must restrict its inputs.
- **A specification that is too weak.** A proof that a program meets a weak specification is worth little. The examples below show a postcondition that the constant program $r = 0$ meets.
- **A proof of partial correctness only.** The invariant method alone says nothing about termination. A loop whose test can never become false keeps every invariant and gives no answer.
- **An invariant that holds only for the tested inputs.** The start step of an invariant proof must hold for every input that the precondition allows, including the boundary inputs $0$ and $1$.

## Examples

### Integer square root

The running example of this group of pages is the integer square root. The specification is: the input is an integer $n \ge 0$, and the output is the integer $r$ with $r^2 \le n < (r+1)^2$. For each $n \ge 0$ exactly one such $r$ exists, namely $\lfloor \sqrt n \rfloor$. The page on [specification](/specification/) proves this. The algorithm is a [binary search](/binary-search/) on the answer. See also [integer square root](/integer-square-root/).

```pseudo id=main
ISQRT(n)                                   ▷ n is an integer with n ≥ 0
L1  lo ← 0
L2  hi ← n + 1
L3  while hi − lo > 1 do
L4      mid ← lo + ⌊(hi − lo) / 2⌋
L5      if mid · mid ≤ n then lo ← mid
L6      else hi ← mid
L7  r ← lo                                 ▷ r is the result
```

**Partial correctness.** The loop invariant is $I$: $0 \le lo < hi$ and $lo^2 \le n < hi^2$.

1. Start. After L1 and L2, $lo = 0$ and $hi = n + 1$. Then $0 < n + 1$ because $n \ge 0$, and $0 \le n < (n+1)^2$ because $(n+1)^2 = n^2 + 2n + 1 > n$. So $I$ holds.
2. Step. Assume $I$ and $hi - lo > 1$. Put $g = hi - lo \ge 2$. Then $mid - lo = \lfloor g/2 \rfloor \ge 1$ and $hi - mid = g - \lfloor g/2 \rfloor = \lceil g/2 \rceil \ge 1$, so $lo < mid < hi$. If $mid^2 \le n$, the new pair $(mid, hi)$ satisfies $I$, because $0 \le lo < mid$. Otherwise $n < mid^2$, and the new pair $(lo, mid)$ satisfies $I$.
3. Exit. When the test fails, $hi - lo \le 1$. With $lo < hi$ this gives $hi = lo + 1$. Then $I$ says $lo^2 \le n < (lo+1)^2$, and L7 sets $r = lo$. This is the postcondition.

**Termination.** Take the variant $t = hi - lo$, an integer. While the test holds, $t \ge 2$. One pass replaces $t = g$ by $\lfloor g/2 \rfloor$ or $\lceil g/2 \rceil$. For $g \ge 2$ both are at most $g - 1$, so $t$ drops by at least 1 at each pass. A non-negative integer cannot drop by 1 more than its start value times, so the loop stops after at most $n + 1$ passes. A sharper count: if $g \le 2^k$ with $k \ge 1$, then $\lceil g/2 \rceil \le 2^{k-1}$. The start gap $n + 1$ is at most $2^K$ with $K = \lceil \lg(n+1) \rceil$, so after $K$ passes the gap is at most 1. The loop runs at most $\lceil \lg(n+1) \rceil$ times.

For $n = 10$ the loop runs four times, and $\lceil \lg 11 \rceil = 4$:

| pass | lo | hi | hi − lo | mid | mid² ≤ 10 |
|---|---|---|---|---|---|
| 1 | 0 | 11 | 11 | 5 | no |
| 2 | 0 | 5 | 5 | 2 | yes |
| 3 | 2 | 5 | 3 | 3 | yes |
| 4 | 3 | 5 | 2 | 4 | no |

After pass 4 the pair is $(3, 4)$, so $r = 3$, and $3^2 = 9 \le 10 < 16 = 4^2$. For $n = 10^{20}$ the loop runs 66 times and returns $10^{10}$. For each $n$ from 0 to 99999 the result equals $\lfloor \sqrt n \rfloor$, and the number of passes is at most $\lceil \lg(n+1) \rceil$; the bound is reached for 58244 of these values.

### A bug that tests miss

Change L2 to $hi \leftarrow n$. Among all $n$ from 0 to 99999, the changed program is wrong only for $n = 1$: the loop does not run, and the result is $0$ where the right value is $1$. For $n = 0$ the result $0$ is right, and for each $n \ge 2$ the start state satisfies $I$ because $n < n^2$, so the proof above applies. A test set that leaves out $n = 1$ passes. A proof attempt fails in step 1 at once: $I$ needs $n < hi^2 = n^2$, which is false for $n = 0$ and for $n = 1$. The failed step points to the boundary.

### A loop that keeps its invariant and never stops

Change L3 to `while hi − lo ≥ 1 do`. Steps 1 and 2 of the proof still hold, and the step case does not even need $g \ge 2$: for $g = 1$, $mid = lo$ and $mid^2 = lo^2 \le n$, so L5 sets $lo \leftarrow lo$. The state no longer changes, and the test $hi - lo \ge 1$ is true forever, because $I$ contains $lo < hi$. The changed program is partially correct and not totally correct. The variant $t = hi - lo$ shows where the termination proof fails: at $t = 1$ a pass does not make $t$ smaller.

### A specification that is too weak

Take the postcondition $r^2 \le n$ alone. The program that always returns $r = 0$ meets it for each $n \ge 0$, and it is useless. For $n = 10$ the seven integers $-3$ to $3$ all meet it. A specification must exclude each wrong answer that matters. See [postcondition](/postcondition/).

### Euclid's algorithm

For $a, b \ge 0$, not both zero, the loop `while b ≠ 0: (a, b) ← (b, a mod b)` returns $\gcd$ of the inputs. The invariant is $\gcd(a, b) = \gcd(a_0, b_0)$, kept because $\gcd(a, b) = \gcd(b, a \bmod b)$. At exit $b = 0$ and $\gcd(a, 0) = a$. The variant is $b$: for $b > 0$, $0 \le a \bmod b < b$, so $b$ drops by at least 1. Knuth (Volume 1, Section 1.2.1) proves this algorithm with assertions on the flowchart, in the style of Floyd. See [Euclidean algorithm](/euclidean-algorithm/).

## Where it is used

- **Proofs of algorithms.** Each correctness proof on this site follows the pattern above: an invariant for each loop, a variant for termination, and strong induction for recursion. CLRS (Section 2.1) uses the same three steps (initialization, maintenance, termination) for insertion sort.
- **Program verifiers.** Tools such as Dafny, Why3 and Frama-C take the specification and the invariants as annotations, generate the proof obligations, and send them to an automatic prover. See [program verification](/program-verification/) and [weakest precondition](/weakest-precondition/).
- **Contracts and assertions.** In [design by contract](/design-by-contract/), the precondition and the postcondition are written in the code and checked at run time as [assertions](/assertion/). This finds a broken contract when it happens, and it does not prove that it never happens.
- **Certifying algorithms.** A [certifying algorithm](/certifying-algorithms/) returns a witness with its output, and a small checker verifies the output for that one input. This moves the trust from a large program to a small checker.
- **Testing.** Where a proof costs too much, [property-based testing](/property-based-testing/) and [differential testing](/differential-testing/) check the specification on many generated inputs.

## References
