---
tag: M18TVM
kind: definition
slug: assertion
name: Assertions
aliases:
- Assert statement
- Runtime assertion
area: foundations/correctness-and-invariants
level: intro
summary: Boolean conditions placed in code to document and check invariants, pre- and postconditions at run time.
prereqs: [precondition, postcondition]
see_also: [loop-invariant, hoare-triple, design-by-contract, floyd-inductive-assertions, property-based-testing]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.1
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580
---

An assertion is a Boolean statement about the state of a program, attached to a point of the program, that is meant to be true each time control reaches that point. It has two uses. As a logical statement it is part of a proof, for example the [precondition](/precondition/), the [postcondition](/postcondition/) or a [loop invariant](/loop-invariant/). As a statement in code, such as `assert`, it is checked at run time when checks are on, and when it is false it raises an error (in Python an `AssertionError`) that normally ends the run.

## Definition

A program point is a place before, between or after the statements of a program. An assertion at a program point is a predicate $A$ on the program state. It is valid at that point when, in each run that starts in a state of the [precondition](/precondition/) of the program, $A$ is true in the state at each moment when control is at that point. In symbols, $A$ is valid at $p$ when for every run $\sigma_0, \sigma_1, \dots$ with $\sigma_0 \models P$ and every $t$ with $pc(\sigma_t) = p$, we have $\sigma_t \models A$. Here $pc$ gives the program point of a state. R. W. Floyd (1967) attached such assertions to the edges of a flowchart. Hoare (1969) wrote them around the statements of a program, in the [Hoare triple](/hoare-triple/) $\{P\}\ S\ \{Q\}$.

There are two forms.

- **Logical assertion.** A formula, which can use quantifiers, sets and mathematical integers. It is a claim that a proof must establish. The invariant of a loop is a logical assertion at the loop test.
- **Executable assertion.** A Boolean expression of the programming language in an `assert` statement. When it is true, the program goes on. When it is false, the program stops with an error (in Python, an `AssertionError`). The check is useful only for what the code can compute, so a formula such as "for each integer $k$" cannot be checked, but "for each index $i$ of this array" can.

A true executable assertion in one run shows that the assertion held in that run. A logical assertion with a proof holds in all runs. Tools such as Dafny prove assertions before the program runs, so no run-time check is needed.

## Examples and non-examples

The program is ISQRT of the page on [correctness](/correctness/), in Python. The first assert is the precondition, the second is the loop invariant at the loop test, and the third is the postcondition.

```python
def isqrt(n):
    assert n >= 0
    lo, hi = 0, n + 1
    while True:
        assert 0 <= lo < hi and lo * lo <= n < hi * hi
        if hi - lo <= 1:
            break
        mid = lo + (hi - lo) // 2
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid
    r = lo
    assert r * r <= n < (r + 1) * (r + 1)
    return r
```

For each $n$ from 0 to 4999 no assertion fails. The call `isqrt(-1)` raises an `AssertionError` at the first line, which signals a caller that broke the precondition. With the option `-O` the check is removed and `isqrt(-1)` returns $0$. So use `assert` for conditions that only a bug can break, and check input from outside callers with an explicit `if n < 0: raise ValueError`.

- The logical assertion $lo^2 \le n < hi^2$ at the loop test of ISQRT is valid. At the third pass for $n = 10$, the state is $lo = 2$, $hi = 5$, and $4 \le 10 < 25$.
- The logical assertion $r^2 \le n < (r+1)^2$ after the loop is valid when $n \ge 0$.
- In a [Hoare triple](/hoare-triple/), the formulas $P$ and $Q$ are assertions, at the start and at the end of $S$.
- **Non-example: a false claim at its point.** "$lo^2 = n$" at the loop test is not valid. For $n = 10$ the first state is $lo = 0$, and $0 \ne 10$. A false assertion is a wrong claim, and in code it stops the run.
- **Non-example: a comment.** The comment `# lo*lo <= n` has the same words but nothing checks it. It is not an executable assertion. It can be a logical one if a proof uses it.
- **Non-example: a check with a side effect.** In `assert pop() > 0`, the call to `pop` changes the state. Python skips `assert` statements when it runs with the option `-O`, so the program then behaves differently. An assertion must not change the state.
- **Not a proof.** The run above checks the invariant for 5000 values of $n$. This does not show that it holds for all $n$. The proof on the page for [correctness](/correctness/) does.

## Related definitions

- [Precondition](/precondition/) and [postcondition](/postcondition/): assertions at the start and at the end of a routine.
- [Loop invariant](/loop-invariant/): an assertion at the loop test, true at each pass.
- [Hoare triple](/hoare-triple/): a statement with two assertions around a program.
- [Floyd's inductive assertions](/floyd-inductive-assertions/): the method of assertions on the edges of a flowchart.
- [Design by contract](/design-by-contract/): a style in which routines check their pre- and postconditions as assertions.
- [Property-based testing](/property-based-testing/): the assertions are checked on many generated inputs.

## References
