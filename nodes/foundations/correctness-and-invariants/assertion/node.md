---
tag: M18TVM
kind: definition
slug: assertion
name: Assertion
aliases:
- Assert statement
- Runtime assertion
area: foundations/correctness-and-invariants
level: intro
summary: A condition on the program state, attached to a point of the program, that must be true each time control reaches that point. It can be a claim in a proof or a check in code.
prereqs: [precondition, postcondition]
see_also: [loop-invariant, hoare-triple, design-by-contract, floyd-inductive-assertions, inductive-invariant, property-based-testing]
sources:
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32, propositions on the connections of a flowchart and the verification of each command
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.1 (the assertions on the flowchart of Algorithm E)
  - url: https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement
    title: The Python Language Reference
    locator: Section 7.3, The assert statement
---

An assertion is a condition on the state of a program, attached to a point of the program, that must be true each time control reaches that point. As a logical claim, it is a step of a proof: the [precondition](/precondition/), the [postcondition](/postcondition/) and the [loop invariant](/loop-invariant/) are assertions. As a statement in code, such as `assert` in Python, it is tested at run time when checks are on, and a false assertion stops the run with an error.

## Definition

### Valid assertions

A program point is a place before, between or after the statements of a program. Let a run of the program be a sequence of states $\sigma_0, \sigma_1, \ldots$, and let $pc(\sigma_t)$ be the program point of $\sigma_t$. An **assertion** at a point $p$ is a predicate $A$ on states. It is **valid** for the precondition $P$ of the program when

$$\forall \text{ runs } \sigma_0, \sigma_1, \ldots \text{ with } \sigma_0 \models P, \ \forall t : \ pc(\sigma_t) = p \Rightarrow \sigma_t \models A.$$

The definition says nothing about runs that start outside $P$, and nothing about a point that control never reaches: an assertion at an unreachable point is valid, even $\mathrm{false}$.

### Inductive assertions

Validity is a claim about all runs, which a proof cannot list. Floyd (1967) reduced it to local checks. Attach an assertion $A_p$ to a set of points that includes the entry, the exit, and at least one point on each loop. A **path** is a piece of a run from one such point to the next, with no such point in between; since each loop contains a point, a path does not repeat a loop and is a straight-line piece of code with branch tests. The family $(A_p)$ is **inductive** when

1. $P \Rightarrow A_{\mathrm{entry}}$; and
2. for each path from $p$ to $q$, if the path starts in a state of $A_p$ and its branch tests are true, it ends in a state of $A_q$.

**Claim.** If the family is inductive, each $A_p$ is valid.

*Proof.* Take a run from $\sigma_0 \models P$ and list the times at which it is at an annotated point: $t_0 = 0 < t_1 < t_2 < \cdots$. By induction on $k$, $\sigma_{t_k}$ satisfies the assertion of its point. For $k = 0$ this is check 1. For the step, the part of the run from $t_k$ to $t_{k+1}$ is a path, it starts in a state of the assertion at its start by the hypothesis, and check 2 gives the assertion at its end. $\square$

Each check of type 2 is a [Hoare triple](/hoare-triple/) for straight-line code, which the assignment axiom turns into one implication. A valid assertion need not be inductive on its own: a proof often needs a stronger assertion that is inductive. The assertion at the exit is the postcondition, so its validity is [partial correctness](/partial-correctness/). Floyd attached the assertions to the edges of a flowchart; Hoare (1969) wrote them around the statements of a program text.

### Two forms

- **Logical assertion.** A formula that may use quantifiers, sets and mathematical integers. A proof establishes it.
- **Executable assertion.** A Boolean expression of the programming language in an assertion statement. When it is true, the run goes on; when it is false, the run stops with an error. Only computable conditions can be written this way: "for each index $i$ of this array" can be checked, "for each integer $k$" cannot.

In Python, `assert e` raises `AssertionError` when `e` is false, and the interpreter removes all `assert` statements when it runs with the option `-O`, in which the built-in constant `__debug__` is false (Python Language Reference, Section 7.3). In C, the macro `assert` of `<assert.h>` does nothing when `NDEBUG` is defined. In Java, assertions are off unless the program runs with the option `-ea`. So an executable assertion must never be the only code that enforces a condition.

A true executable assertion in one run shows that the condition held in that run. A proof of a logical assertion covers all runs. Verifiers such as Dafny prove the annotated assertions before the program runs, and then no run-time check is needed.

## Examples and non-examples

### ISQRT with its assertions

This is ISQRT from the page [correctness](/correctness/), in Python. The first `assert` is the precondition, the second is the loop invariant at the loop test, and the third is the postcondition.

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

For each $n$ from 0 to 4999 the run raises no error. The call `isqrt(-1)` raises `AssertionError` in the first line, which reports a caller that broke the precondition. Under `python -O` the same call returns $0$ with no error: the checks are gone, the loop does not run because $hi - lo = 0$, and the result is wrong. So use `assert` for conditions that only a bug in this program can break, and check input from outside callers with an explicit `if n < 0: raise ValueError(...)`.

The three assertions form an inductive family, with the loop test as the point on the loop: the paths are entry to loop test, loop test around the body back to the loop test, and loop test to exit. The page [correctness](/correctness/) proves the three checks. At the third test for $n = 10$ the state is $lo = 2$, $hi = 5$, and $0 \le 2 < 5$ and $4 \le 10 < 25$ hold.

### Valid but not inductive

Take the loop `i, s ← 0, 0; while i ≠ n do (i ← i + 1; s ← s + i)` with the precondition $n \ge 0$, and the assertion $s \ge 0$ at the loop test. It is valid: every reachable state has $0 \le i \le n$ and $s = i(i+1)/2 \ge 0$. It is not inductive on its own: the state $i = -5$, $s = 0$ satisfies $s \ge 0$ and the loop test, and one pass gives $i = -4$, $s = -4$. The stronger assertion $0 \le i \le n \wedge s = i(i+1)/2$ is inductive, and it implies $s \ge 0$. See [inductive invariant](/inductive-invariant/).

### Non-examples

- **A false claim at its point.** "$lo^2 = n$" at the loop test of ISQRT is not valid: for $n = 10$ the first state has $lo = 0$, and $0 \ne 10$.
- **A comment.** `# lo*lo <= n` states the same condition, and nothing checks it. It is not an executable assertion. It is a logical one only if a proof uses it.
- **An assertion with a side effect.** In `assert stack.pop() > 0`, the call changes the state. Under `python -O` the call disappears, and the program behaves differently. An executable assertion must not change the state.
- **Input validation.** `assert user_age >= 0` on data from a user is not an assertion in the sense above. Its truth does not follow from the program, so no proof can make it valid, and with checks off it does nothing.
- **A test is not a proof.** The 5000 runs above show that the assertions held in those runs. They do not show that the assertions hold for all $n$; the proof on the page [correctness](/correctness/) does.

### Pitfalls

- **A check that changes the complexity.** Asserting "$A$ is sorted" at the entry of [binary search](/binary-search/) costs $\Theta(m)$ per call, and the search costs $O(\log m)$. Keep such checks for tests and debug builds.
- **Assertions as error handling.** Checks that can be turned off cannot handle errors that a correct program must expect, such as bad input or a missing file.
- **Assertions that are too weak.** An assertion that holds in every state, such as $hi \ge lo - 1$ when the code already guarantees $lo < hi$, documents nothing. A useful assertion is one that a bug would break.
- **Floating point.** `assert x * x == y` can fail for a correct square root. State and check a tolerance.

## Related definitions

- [Precondition](/precondition/) and [postcondition](/postcondition/): the assertions at the entry and at the exit of a routine.
- [Loop invariant](/loop-invariant/): an assertion at the loop test that holds at each pass.
- [Inductive invariant](/inductive-invariant/): an assertion that each step keeps, which makes it provable by induction.
- [Hoare triple](/hoare-triple/): a statement with two assertions around a program text.
- [Floyd's inductive assertions](/floyd-inductive-assertions/): the method of the claim above, on flowcharts.
- [Design by contract](/design-by-contract/): routines state their pre- and postconditions as executable assertions.
- [Property-based testing](/property-based-testing/): executable assertions are tested on many generated inputs.

## References
