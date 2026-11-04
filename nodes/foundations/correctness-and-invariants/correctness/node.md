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
summary: An algorithm is correct if it returns a valid output for every legal input; correctness is proved, not tested.
prereqs: [loop-invariant]
see_also: [specification, hoare-triple, partial-correctness, total-correctness, assertion, termination-proof, program-verification, property-based-testing]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.1
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.1
---

An algorithm is correct with respect to a [specification](/specification/) when, for every input that the specification allows, it stops and gives an output that the specification accepts. Correctness is a claim about all legal inputs. There are usually infinitely many of them, or too many to try, so a finite set of tests cannot prove it. A proof can. It has two parts: [partial correctness](/partial-correctness/) (the output is right if the algorithm stops) and termination (the algorithm does stop). Together they give [total correctness](/total-correctness/).

## In plain words

You cannot call an algorithm correct until you say what it must do. The statement of that task is the specification. It says which inputs are legal and which outputs are right for each of them.

An algorithm is then correct when two things hold for every legal input. It stops, and its output is right. A test runs the algorithm on a few inputs. A failed test shows a bug. A passed test shows nothing about the inputs that you did not try. A proof covers all inputs at once, and it explains why the algorithm works.

Most of the work in a proof is about loops and recursion. For a loop you find a fact that stays true at each step, and you show that this fact gives the right output when the loop ends. You also show that the loop does end.

## The idea

Let $X$ be the set of inputs and $Y$ the set of outputs. A specification is a pair of predicates: a precondition $P(x)$ on inputs and a postcondition $Q(x, y)$ on an input and an output. An algorithm $A$ is correct for $(P, Q)$ when

$$\forall x \in X : \ P(x) \Rightarrow \big( A \text{ stops on } x \ \wedge \ Q(x, A(x)) \big).$$

The statement has two parts. The part "$A$ stops on $x$" is termination. The part "$Q(x, A(x))$ whenever $A$ stops" is partial correctness. A proof of each part is a different task, with different tools. Partial correctness uses [loop invariants](/loop-invariant/), or more generally [Floyd's inductive assertions](/floyd-inductive-assertions/) and [Hoare triples](/hoare-triple/). Termination uses a [variant function](/variant-function/): a quantity with values in a well-founded set, usually a non-negative integer, that drops strictly at each step. See [termination proof](/termination-proof/).

For a recursive algorithm, partial correctness is proved by [strong induction](/induction/) on a measure of the input that has no infinite decreasing sequence, for example its size. The induction hypothesis is that every recursive call on a smaller input meets the specification. The base cases are checked directly. Termination follows because every call is on a strictly smaller measure. For example, [merge sort](/merge-sort/) is correct on all arrays of length $n$ by strong induction on $n$.

The statement says nothing about inputs outside $P$. The algorithm may stop, fail or loop on them. This is why the [precondition](/precondition/) is part of the specification.

No algorithm decides, for every program and every specification, whether the program is totally correct (this follows from Rice's theorem). So each proof is built for its own algorithm. For a randomized algorithm the claim changes. A Monte Carlo algorithm is correct with probability at least $1 - \delta$ for a stated $\delta$. A Las Vegas algorithm is always correct, and its running time is random.

Testing and proof answer different questions. A test checks the formula above for one chosen $x$. If $A$ gives a wrong output on that $x$, the test finds a counterexample. If $A$ gives a right output, the formula is still open for every other $x$. A proof covers all $x \in X$ with $P(x)$. A proof is also a proof about a model: it uses mathematical integers, and a program on a real machine can differ from the model, for example through integer overflow.

## Examples

The running example of this group of pages is integer square root. The specification is: the input is an integer $n \ge 0$, and the output is the integer $r$ with $r^2 \le n < (r+1)^2$. For each $n \ge 0$ exactly one such $r$ exists, namely $\lfloor \sqrt n \rfloor$. The algorithm is a [binary search](/binary-search/) on the answer, see also [integer square root](/integer-square-root/).

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

**Why it is correct.** The loop invariant is $I$: $0 \le lo < hi$ and $lo^2 \le n < hi^2$.

1. Start. After L1 and L2, $lo = 0$ and $hi = n + 1$. Then $0 < n + 1$, and $0 \le n < (n+1)^2$ because $(n+1)^2 = n^2 + 2n + 1 > n$ for $n \ge 0$. So $I$ holds.
2. Step. Assume $I$ and $hi - lo > 1$. Put $g = hi - lo \ge 2$. Then $mid - lo = \lfloor g/2 \rfloor \ge 1$ and $hi - mid = g - \lfloor g/2 \rfloor \ge 1$, so $lo < mid < hi$. If $mid^2 \le n$, the new pair $(mid, hi)$ satisfies $I$. Otherwise $n < mid^2$, and the new pair $(lo, mid)$ satisfies $I$.
3. End. When the loop stops, $hi - lo \le 1$. With $lo < hi$ this gives $hi = lo + 1$. Then $I$ says $lo^2 \le n < (lo+1)^2$, and L7 sets $r = lo$. This is the postcondition.
4. Termination. The new gap is $hi - mid = g - \lfloor g/2 \rfloor$ or $mid - lo = \lfloor g/2 \rfloor$. Both are at most $g - 1$ when $g \ge 2$. So the integer $hi - lo$ drops by at least 1 at each step, and it stays at least 1. The loop runs a finite number of times.

For $n = 10$ the loop runs four times:

| step | lo | hi | hi − lo | mid | mid² ≤ 10 |
|---|---|---|---|---|---|
| 1 | 0 | 11 | 11 | 5 | no |
| 2 | 0 | 5 | 5 | 2 | yes |
| 3 | 2 | 5 | 3 | 3 | yes |
| 4 | 3 | 5 | 2 | 4 | no |

After step 4 the pair is $(3, 4)$, so $r = 3$, and $3^2 = 9 \le 10 < 16 = 4^2$.

**A bug that tests can miss.** Start with $hi \leftarrow n$ instead of $n + 1$. The invariant now fails at the start for $n = 1$, because $1 < 1^2$ is false. For $n = 1$ the loop does not run, and the result is $0$, but the right value is $1$. For every $n$ other than 1 the buggy program returns the right value, because $n < n^2$ once $n \ge 2$. So a test set of thousands of inputs that leaves out $n = 1$ passes. A proof attempt fails at once in the start step, for $n = 0$ and for $n = 1$, and this points straight to the boundary.

**A specification that is too weak.** Take the postcondition $r^2 \le n$ alone. The program that always returns $r = 0$ meets it, and it is useless. A specification must be strong enough to exclude every wrong answer that you care about. See [postcondition](/postcondition/).

## Where it is used

Correctness proofs are the basis of the proof pages on this site. They are also the base of [program verification](/program-verification/) tools, and of [design by contract](/design-by-contract/), where preconditions and postconditions are checked at run time as [assertions](/assertion/). Where a proof is too costly, [property-based testing](/property-based-testing/) and [differential testing](/differential-testing/) check the specification on many generated inputs. They find bugs and do not prove their absence.

## References
