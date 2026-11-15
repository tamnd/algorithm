---
tag: 25NQX4
kind: algorithm
slug: delta-debugging
name: Delta debugging
aliases:
- ddmin
- test case minimization
area: compilers-and-program-analysis/verification-and-synthesis
level: core
summary: Shrinks a failing input to a 1-minimal failing one by testing subsets and complements of finer and finer partitions.
model: word-ram
complexity:
  vars: {N: the number of elements of the failing input, t: the cost of one test}
  time: {best: O((t + N) log N), worst: O(N^2 (t + N))}
  space: {extra: O(N)}
properties: {deterministic: true, recursive: false}
history:
  year: 2000
  people: [Ralf Hildebrandt, Andreas Zeller]
  note: Presented at ISSTA 2000 to simplify failure-inducing input, after Zeller's 1999 delta debugging of program changes; the journal version of 2002 is the standard reference.
prereqs: [binary-search]
see_also: [coverage-guided-fuzzing, grammar-based-fuzzing, equivalence-modulo-inputs, automated-program-repair, property-based-testing, differential-testing, local-search, abstract-syntax-tree]
sources:
  - paper: doi:10.1109/32.988498
    title: Andreas Zeller and Ralf Hildebrandt, Simplifying and isolating failure-inducing input, IEEE Transactions on Software Engineering 28(2), 2002
    locator: pp. 183 to 200; Definition 10 (n-minimal test case) on p. 186, Fig. 5 (ddmin) on p. 187, Propositions 11 to 13 on p. 188
  - paper: doi:10.1145/347324.348938
    title: Ralf Hildebrandt and Andreas Zeller, Simplifying failure-inducing input, Proceedings of ISSTA 2000
    locator: pp. 135 to 145, the first form of the minimizing algorithm
  - paper: doi:10.1145/318774.318946
    title: Andreas Zeller, Yesterday, my program worked. Today, it does not. Why?, Proceedings of ESEC/FSE 1999
    locator: pp. 253 to 267, delta debugging of the changes between two versions of a program
  - paper: doi:10.1145/1134285.1134307
    title: Ghassan Misherghi and Zhendong Su, HDD, hierarchical delta debugging, Proceedings of ICSE 2006
    locator: pp. 142 to 151, ddmin applied level by level to a syntax tree
  - paper: doi:10.1145/2254064.2254104
    title: John Regehr, Yang Chen, Pascal Cuoq, Eric Eide, Chucky Ellison and Xuejun Yang, Test-case reduction for C compiler bugs, Proceedings of PLDI 2012
    locator: pp. 335 to 346, the comparison of C-Reduce with delta debugging
---

Delta debugging, in the form of the algorithm ddmin of Zeller and Hildebrandt, takes an input that makes a test fail and removes parts of it while the test still fails. It treats the input as a list of elements, such as characters, lines, tokens or instructions, and needs only a test function that answers FAIL, PASS or UNRESOLVED. The result is *1-minimal*: removing any single element makes the failure go away. That is a local property. A 1-minimal input is not always a minimum one, and ddmin does not try to find the minimum, which can need exponentially many tests.

## In plain words

You have a long input that crashes a program, and you want a short one that a person can read. Cut the input in two halves and try each half. If a half still crashes, keep it and start again. If neither half crashes, cut into more, smaller pieces, and try each piece and each "everything but this piece". Whenever a try still crashes, keep it. When the pieces are single elements and no try crashes any more, stop. At that point no single element can be removed without losing the crash. Some tries give a broken input that the program rejects for another reason; those count as "no crash". The result is small, but another, smaller input that crashes for a different reason can still exist.

## The problem

The input is a list $c$ of $N$ elements and a test function $\mathit{test}$ from sub-lists of $c$ to $\{\mathrm{FAIL}, \mathrm{PASS}, \mathrm{UNRESOLVED}\}$, with $\mathit{test}(c) = \mathrm{FAIL}$ and $\mathit{test}([\,]) = \mathrm{PASS}$. A sub-list keeps the original order. The output is a sub-list $c'$ with $\mathit{test}(c') = \mathrm{FAIL}$ that is 1-minimal: for every element $\delta$ of $c'$, $\mathit{test}(c' - \delta) \ne \mathrm{FAIL}$.

What is decidable here is simple: everything, because the search space is finite. The question is the number of tests. A *minimum* failing sub-list, one of the smallest size, can need $2^N - 2$ tests: if every test passes, no algorithm can claim that the full input is the smallest failing one until it has tried every other non-empty sub-list. 1-minimality is the relaxation that the paper adopts, and ddmin reaches it with $O(N^2)$ tests. The test function itself can be any program; ddmin does not need it to be monotone or consistent, and its guarantee holds for whatever answers the test gives.

## The algorithm

```pseudo id=main
DDMIN(c, test)
L1  n <- 2
L2  while |c| >= 2 do
L3      split c into n contiguous parts d_1 ... d_n whose sizes differ by at most 1
L4      if test(d_i) = FAIL for some i (trying i = 1 ... n in order) then
L5          c <- d_i; n <- 2
L6      else if n > 2 and test(c - d_i) = FAIL for some i (in order) then
L7          c <- c - d_i; n <- max(n - 1, 2)
L8      else if n < |c| then
L9          n <- min(2n, |c|)
L10     else
L11         stop
L12 return c
```

Lines L4 and L5 are "reduce to subset", lines L6 and L7 "reduce to complement", lines L8 and L9 "increase granularity", and line L11 "done", as in Fig. 5 of the paper. After a complement reduction, $n - 1$ parts keep the same granularity: the old parts other than $d_i$ are the natural parts of the new list. At $n = 2$ the two complements are the two subsets, so this implementation does not test them twice.

UNRESOLVED needs no special case. It is any outcome that is not FAIL: a sub-list that does not compile or that the parser rejects is treated like one that passes, and so is never kept.

## Example

The elements are $0, 1, \dots, 7$. The test fails when the list contains both 0 and 1, or contains 6.

| test | list | outcome | step |
|---|---|---|---|
| 1 | 0 1 2 3 | FAIL | reduce to subset, $n = 2$ |
| 2 | 0 1 | FAIL | reduce to subset, $n = 2$ |
| 3 | 0 | PASS | |
| 4 | 1 | PASS | $n = 2$ equals the size of $c$, done |

ddmin returns $[0, 1]$ after 4 tests. It is 1-minimal: $[0]$ and $[1]$ both pass. But $[6]$ fails and is smaller, so $[0, 1]$ is not a minimum. ddmin never sees 6 again after the first test, because the first half already failed. A brute-force search over all 256 sub-lists confirms that $[6]$ is the only failing list of size 1.

A second example uses the toy IR. A program of one block has 12 instructions and ends in a division by zero:

```
a = 5;  b = 3;  x = a * 7;  c = a - b;  y = x + b;  d = c * 2
e = b + 1;  z = y - 1;  f = d - 4;  w = z / e;  g = e / f;  h = g + a
```

The test builds a block from a sub-list, returns UNRESOLVED if an instruction reads a name that no earlier instruction defines, and FAIL if the run traps. ddmin needs 124 tests, most of them UNRESOLVED, and returns the 7 instructions that define $a, b, c, d, e, f$ and $g$. Here the result is also a minimum: the brute-force search over all 4096 sub-lists finds no failing list of fewer than 7 instructions.

## Correctness

The proof file has the details.

1. **The invariant.** At the start of each iteration, $\mathit{test}(c) = \mathrm{FAIL}$ and $2 \le n \le |c|$. Line L5 keeps a failing part; line L7 keeps a failing complement of $n - 1$ parts, each non-empty, so $n - 1 \le |c - d_i|$; line L9 caps $n$ at $|c|$.
2. **Termination.** Each iteration either makes $c$ shorter, or keeps $c$ and makes $n$ larger, or stops. $n \le |c|$, so the loop ends.
3. **1-minimality.** If the loop ends with $|c| = 1$, removing the element gives the empty list, which passes. If it ends at line L11, then $n = |c|$, so each part is one element. If $n > 2$, every complement $c - \delta$ was tested and did not fail. If $n = 2 = |c|$, the two complements are the two parts, which were tested and did not fail.

**What is not claimed.** The result is not a minimum, and different 1-minimal results can differ in size. The result depends on the order of the elements and on the order of the tests. With a test that is not consistent, for example a flaky one, 1-minimality holds only for the answers that the test happened to give.

## Complexity

Each iteration at granularity $n$ makes at most $2n$ tests, $n$ subsets and $n$ complements. The proof file shows the worst-case total of $(3N - 2)(N - 1)$ tests for this implementation: in a phase at a fixed size $m$, the doublings of $n$ cost at most $4m - 8$ tests in total, the last iteration costs at most $2m$, and the size goes down by at least 1 from one phase to the next. The paper states $N^2 + 3N$ tests in the worst case for its version (Proposition 12), which also tests the complements at $n = 2$. Each test gets a list of at most $N$ elements, so building the lists costs $O(N)$ per test, and the total is $O(N^2 (t + N))$.

In the best case, when a single element causes the failure and every list that contains it fails, every iteration halves the list, as in [binary search](/binary-search/), and ddmin needs at most $2 \lceil \log_2 N \rceil$ tests (Proposition 13 of the paper). The space is $O(N)$.

The tests on this page run ddmin on every test function for $N \le 4$, and on random monotone and non-monotone test functions for $N \le 12$, and compare the result with a brute-force minimum.

## Properties

- **Black box.** ddmin needs only the test function, not the program or the structure of the input.
- **1-minimal, not minimum.** The output is a local minimum for the removal of one element.
- **Monotonicity not needed.** The guarantee holds for any test function; with a monotone test (every superset of a failing list fails), the subset steps behave like binary search.
- **Deterministic.** The same input and test give the same tests in the same order.
- **Order-sensitive.** Contiguous parts help when related elements are close together, as lines of one function are.

## Variants and improvements

- **Isolation (dd).** The second algorithm of the paper starts from a passing and a failing input and narrows the difference between them until a 1-minimal difference remains, with the same worst case.
- **Caching.** A table of the test outcomes avoids testing the same list twice, which happens after complement reductions.
- **Hierarchical delta debugging.** Misherghi and Su apply ddmin to the levels of a syntax tree, from the root down, so most tried inputs are syntactically valid and fewer tests are UNRESOLVED. See [abstract syntax tree](/abstract-syntax-tree/).
- **Domain-specific reducers.** C-Reduce of Regehr and others combines many program transformations, in a fixed-point loop, and produces much smaller C programs than a line-based delta tool for compiler bugs, such as those found by [equivalence modulo inputs](/equivalence-modulo-inputs/).
- **Trimming in fuzzers.** A [coverage-guided fuzzer](/coverage-guided-fuzzing/) shrinks each new input with a cheap relative of ddmin that keeps the coverage the same, instead of the failure.
- **Shrinking in property-based testing.** [Property-based testing](/property-based-testing/) libraries shrink a failing random value with type-specific moves, a greedy [local search](/local-search/) that, like ddmin, stops at a local minimum.

## When to use it

Use ddmin to reduce a crashing input, a failing test program for a compiler, or a sequence of user actions, before a person debugs it. It suits cases where a test is cheap compared with human time, and where the input has no structure that a better reducer knows. For structured inputs such as programs, start with a structure-aware reducer, and use plain ddmin on lines or tokens as a final pass.

## Pitfalls

- **Expecting a minimum.** The output is 1-minimal only. Run ddmin again on the result, or try other element orders, to get smaller results.
- **Changing failures.** A test that only checks "the program crashed" can lead to a different bug. Make the test check the exact error message or location.
- **Flaky tests.** A test that sometimes fails and sometimes passes breaks the guarantee and can give a result that does not fail on the next run.
- **Wrong granularity of elements.** Characters give many UNRESOLVED tests on structured input. Lines or tokens are usually better.
- **The empty list.** ddmin assumes that the empty list passes and never tests it. If the empty list fails, the result of size 1 is not 1-minimal.

## Implementations

## History

Zeller introduced delta debugging in 1999 to find the change, among the many changes between a working and a failing version of a program, that causes a failure. Hildebrandt and Zeller applied the idea to inputs at ISSTA 2000, with the minimizing algorithm ddmin, and the journal version of 2002 gives the definitions, the proof of 1-minimality and the bounds on the number of tests. Its case studies minimized a C program that crashed GCC and HTML input that crashed the Mozilla web browser. Misherghi and Su adapted it to syntax trees in 2006, and test-case reducers for compilers, such as C-Reduce, grew from it.

## References
