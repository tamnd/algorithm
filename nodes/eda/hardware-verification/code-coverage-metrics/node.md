---
tag: SCJ6WT
kind: concept
slug: code-coverage-metrics
name: Code coverage metrics
aliases:
- statement coverage
- branch coverage
- toggle coverage
area: eda/hardware-verification
level: intro
summary: Measures of how much of an HDL description a test exercises, such as lines, branches, expressions and signal toggles, used to judge when simulation is done.
prereqs: [logic-simulation, control-flow-graph]
see_also: [fsm-coverage, functional-coverage, observability-based-coverage, fault-coverage, reachability-problem, greedy-set-cover, coverage-guided-fuzzing, constrained-random-stimulus-generation]
sources:
  - paper: doi:10.1109/54.936247
    title: Serdar Tasiran and Kurt Keutzer, Coverage metrics for functional validation of hardware designs, IEEE Design and Test of Computers 18(4), 36 to 45, 2001
    locator: the survey of code coverage metrics (line, branch, condition, expression and toggle), their relation to design errors, and their limits
  - book: isbn:9781402080258
    title: Andrew Piziali, Functional Verification Coverage Measurement and Analysis, Kluwer, 2004
    locator: the chapter on code coverage and the comparison of code coverage with functional coverage (general locator)
  - paper: doi:10.1049/sej.1994.0025
    title: John Joseph Chilenski and Steven P. Miller, Applicability of modified condition/decision coverage to software testing, Software Engineering Journal 9(5), 193 to 200, 1994
    locator: the definition of modified condition/decision coverage and its comparison with decision and condition coverage
---

Code coverage metrics measure which parts of the source text of a hardware description, in Verilog, SystemVerilog or VHDL, a set of simulation runs has exercised. The usual metrics count executed lines, outcomes of decisions (the arms of `if` and `case`), values of the conditions inside decisions, and bits of signals that rose and fell. Each metric is a ratio of covered items to coverable items, computed by an instrumented [logic simulator](/logic-simulation/). The metrics are conventions, not theorems: a full score says that the code ran, not that its results were right or that anyone looked at them. They differ from [FSM coverage](/fsm-coverage/), [functional coverage](/functional-coverage/) and [fault coverage](/fault-coverage/), which are other numbers.

## In plain words

A simulator runs the design description on chosen inputs. Code coverage keeps a tick mark for each line, each arm of each choice, each condition inside a choice and each wire, and ticks it when the run uses it. At the end, the share of ticked marks is the score.

A mark that is never ticked is useful news: that part of the design was never tried, so no test could have found a bug there. A ticked mark is weak news. The line ran, but maybe with values that hide the bug, and maybe the wrong result never reached a place where the test bench checks it. Missing logic has no line, so it has no mark at all. Engineers use the score to find parts that no test reaches and to decide when to stop, and use other measures to judge whether the tests check the right things.

## The idea

**The model.** A design is a set of processes (`always` blocks, `process` statements and continuous assignments). A process wakes on its sensitivity list and runs its body. A run is one simulation, and a suite $T$ is a set of runs. Each metric below fixes a finite set $I$ of *coverable items* in the source text and a predicate "run $\tau$ covers item $i$". The score of $T$ is

$$ \mathrm{cov}(T) = \frac{|\{ i \in I : \text{some } \tau \in T \text{ covers } i \}|}{|I|}. $$

So the score of a union of suites is computed from the union of covered items, never by averaging scores, and it can only grow when runs are added.

**Line coverage.** $I$ is the set of executable statements; a statement is covered when some run executes it at least once. Tools count lines or statements; the two differ when a line holds two statements.

**Decision coverage.** A *decision* is the expression that chooses a path: the condition of an `if` or `?:`, or the selector of a `case`. Its *outcomes* are true and false for an `if`, and the items of a `case`, with the `default` arm or an implicit "no item matched" outcome. $I$ is the set of all outcomes of all decisions; an outcome is covered when some run takes it. Tools report this per arm of `if` and `case`.

**Condition coverage.** A *condition* is an atomic Boolean operand inside a decision, such as `a` and `b` in `if (a && b)`. $I$ holds two items per condition, the values true and false; each is covered when the condition is evaluated with that value. Under short-circuit evaluation, a condition that is not evaluated takes no value. Most HDL tools also count the operands of logical expressions on right-hand sides of assignments in the same way.

**Expression coverage and MC/DC.** For a decision or a right-hand side $f(c_1, \ldots, c_k)$, the *modified condition/decision coverage* of Chilenski and Miller asks, for each condition $c_i$, for two evaluations in the suite in which $c_i$ differs, every other condition is the same (or masked), and $f$ differs. Such a pair shows that $c_i$ alone changes the result. MC/DC also requires every decision outcome and every condition value. HDL tools apply the same idea to right-hand sides of assignments under names such as focused expression coverage.

**Toggle counts.** For each bit of each net and register, there are two items: a rise from 0 to 1 and a fall from 1 to 0. A bit is fully toggled when the suite shows both. Transitions through X or Z count by tool convention, and the convention must be stated with the number.

**What each metric guarantees.** A covered item says only that the run executed it.

- Line coverage of 100 percent: every statement ran at least once. Any bug that needs only the execution of a wrong statement, with any values, had a chance to show.
- Decision coverage of 100 percent: every arm of every choice ran. If every statement sits in an arm of some decision or at the top of a process that runs, and no arm stops early (no `wait`, `return` or `disable` inside it), then full decision coverage implies full line coverage, because a statement in an arm runs whenever its arm is taken.
- Condition coverage of 100 percent: each condition took both values. This does not imply full decision coverage: `if (a && b)` with $(a, b) = (1, 0)$ and $(0, 1)$ gives both values to both conditions, and the decision is false both times. Decision coverage does not imply condition coverage either: `if (a || b)` with $(1, 0)$ and $(0, 0)$ takes both outcomes, and $b$ is never 1.
- MC/DC of 100 percent: each condition was shown to change its decision with the others fixed. In the unique-cause form, a decision with $k$ conditions needs at least $k + 1$ distinct evaluations: the $k$ pairs are edges of the cube $\{0, 1\}^k$ in $k$ different directions, a cycle of cube edges uses each direction an even number of times, so the pairs form a forest, and a forest with $k$ edges has at least $k + 1$ vertices.
- Toggle counts of 100 percent: every bit moved both ways. This says that no bit is stuck in the runs, and nothing about the order or meaning of the values.

**What no code metric guarantees.**

- *Correct values.* A statement can run with values for which the bug and the intended code agree.
- *Observation.* A wrong value can be overwritten or masked before it reaches an output or a checker. [Observability-based coverage](/observability-based-coverage/) counts an item only when an error at it would reach an output.
- *Missing code.* A forgotten case, reset or check has no line, no decision and no condition, so it is never an uncovered item.
- *Sequences.* The metrics count single events. Two arms that must run in a given order, or a value that must hold for several cycles, need [FSM coverage](/fsm-coverage/), [functional coverage](/functional-coverage/) or [assertions](/assertion-based-verification/).

**Denominators and dead code.** Some items cannot be covered by any input: an arm that the reset logic or the surrounding design makes impossible, or a bit tied to a constant. Whether an item can be covered is a [reachability](/reachability-problem/) question on the design, PSPACE-hard in general for sequential designs. In practice engineers exclude items by review or by a formal proof that they are unreachable, and the reported number must say which items were excluded.

## Examples

**Full coverage that misses a bug.** The specification says `y = a & b` when `en` is 1 and `y = 0` otherwise. The code is

```
always @* begin
  if (en) y = a | b;   // bug: the specification says a & b
  else    y = 1'b0;
end
```

Run the four vectors $(en, a, b) = (1,0,0), (1,1,1), (0,1,1), (1,0,0)$ in this order. The code gives $y = 0, 1, 0, 0$, and the specification gives the same four values.

| metric | items | covered |
|---|---|---|
| line | the two assignments | 2 of 2 |
| decision | `en` true, `en` false | 2 of 2 |
| condition | `en`, and the operands `a`, `b` of the right-hand side, each true and false | 6 of 6 |
| toggle | rise and fall of `en`, `a`, `b`, `y` | 8 of 8 |

Every score is 100 percent and the bug is not seen, because $a = b$ in every vector, and `a | b` and `a & b` agree whenever $a = b$. MC/DC on `a | b` is not complete: no pair of vectors differs in `a` alone. The pair $(1,0,0), (1,1,0)$ would complete it for `a`, and the vector $(1,1,0)$ gives $y = 1$ where the specification says 0.

**Condition coverage without decision coverage.** For `if (a && b) x = 1;`, the vectors $(a, b) = (1, 0)$ and $(0, 1)$ cover all four condition items. The assignment never runs, so line coverage is 0 of 1 and decision coverage is 1 of 2.

**A bug that no metric sees.** The specification says that a counter clears on `rst`. The code has no reset arm. Every item of every metric can be covered, and the missing arm is not an item.

**Toggle without meaning.** A 4-bit bus that counts 0, 15, 0 toggles all its bits both ways in two cycles. The values 1 to 14 never occur, and a bug on any of them is not exercised.

## Where it is used

- **Finding untested parts.** An uncovered item is a certain hole: no run exercised it. Engineers read the uncovered items after each regression and write tests or [constraints](/constrained-random-stimulus-generation/) to reach them.
- **Sign-off.** Many projects require a stated level of line, decision and condition coverage, with each exclusion reviewed, as one condition to finish verification. It is a necessary condition, not a sufficient one, and is used together with functional coverage.
- **Dead code.** An item that no test reaches may be unreachable. A formal check of reachability either finds a run or proves the item dead, and dead code is often a bug in itself.
- **Test selection.** Choosing the fewest runs of a regression that keep the same covered items is a [set cover](/set-cover/) problem; regression tools rank tests with the [greedy](/greedy-set-cover/) method.
- **Software analogues.** The same metrics come from software testing, where MC/DC is used for avionics software. [Coverage-guided fuzzing](/coverage-guided-fuzzing/) uses edge counts of the [control-flow graph](/control-flow-graph/) as feedback for its inputs.

## References
