---
tag: FBNKA4
kind: problem
slug: automated-program-repair
name: Automated program repair
aliases:
- program repair
- automatic bug fixing
area: compilers-and-program-analysis/verification-and-synthesis
level: research
summary: Given a program and tests some of which fail, find a small change to the program that makes all tests pass.
prereqs: [program-synthesis]
see_also: [genetic-programming, symbolic-execution, cegis, smt-problem, delta-debugging, equivalence-modulo-inputs, sat, rice-theorem]
sources:
  - paper: doi:10.1109/TSE.2011.104
    title: Claire Le Goues, ThanhVu Nguyen, Stephanie Forrest and Westley Weimer, GenProg, a generic method for automatic software repair, IEEE Transactions on Software Engineering 38(1), 2012
    locator: pp. 54 to 72, the representation, the fault localization weights, the mutation and crossover operators and the evaluation
  - paper: doi:10.1109/ICSE.2013.6606623
    title: Hoang Duong Thien Nguyen, Dawei Qi, Abhik Roychoudhury and Satish Chandra, SemFix, program repair via semantic analysis, Proceedings of ICSE 2013
    locator: pp. 772 to 781, repair constraints from symbolic execution and component-based synthesis of the fix
  - paper: doi:10.1145/2771783.2771791
    title: Zichao Qi, Fan Long, Sara Achour and Martin Rinard, An analysis of patch plausibility and correctness for generate-and-validate patch generation systems, Proceedings of ISSTA 2015
    locator: pp. 24 to 36, plausible against correct patches and the Kali system
  - paper: doi:10.1145/2786805.2786825
    title: Edward K. Smith, Earl T. Barr, Claire Le Goues and Yuriy Brun, Is the cure worse than the disease? Overfitting in automated program repair, Proceedings of ESEC/FSE 2015
    locator: pp. 532 to 543, overfitting to the test suite measured with independent tests
  - paper: doi:10.1145/2884781.2884807
    title: Sergey Mechtaev, Jooyong Yi and Abhik Roychoudhury, Angelix, scalable multiline program patch synthesis via symbolic analysis, Proceedings of ICSE 2016
    locator: pp. 691 to 701, angelic values and the angelic forest
  - paper: doi:10.1145/2837614.2837617
    title: Fan Long and Martin Rinard, Automatic patch generation by learning correct code, Proceedings of POPL 2016
    locator: pp. 298 to 312, Prophet and the learned ranking of candidate patches
  - paper: doi:10.1145/3318162
    title: Claire Le Goues, Michael Pradel and Abhik Roychoudhury, Automated program repair, Communications of the ACM 62(12), 2019
    locator: pp. 56 to 65, the overview of search-based, semantic and learning-based repair
  - paper: doi:10.1109/ICSE-SEIP.2019.00039
    title: Alexandru Marginean, Johannes Bader, Satish Chandra, Mark Harman, Yue Jia, Ke Mao, Alexander Mols and Andrew Scott, SapFix, automated end-to-end repair at scale, Proceedings of ICSE-SEIP 2019
    locator: pp. 269 to 278, the deployment at Facebook
---

Automated program repair asks for a change to a program that removes a bug. The usual statement is test-based: the input is a program and a test suite on which some tests fail, and the output is a small edit after which all tests pass. Such an edit is called a *plausible* patch. It is not always a *correct* one, because a test suite specifies the intended behavior only on its own inputs. With a full specification instead of tests, the problem becomes a case of [program synthesis](/program-synthesis/) and is undecidable in general; with tests, a finite set of allowed edits and bounded runs, it is decidable by trying every edit, but the search space grows fast and is NP-hard to search for edits with many parts.

## In plain words

A program has a bug, and some of its tests fail. We want the computer to change the program a little so that every test passes. The computer guesses where the bug is, usually from the code that the failing tests run and the passing tests do not. It then tries changes at those places: delete a line, copy a line from elsewhere, change a comparison, put in a new condition. After each change it runs all the tests again. A change that makes every test pass is a candidate fix. The hard part is that tests show only some cases. A change can pass every test and still be wrong, for example by returning exactly the answer that one test expects, or by switching off the feature that a failing test checks. A person must still review the fix.

## Definition

Fix a programming language with a deterministic semantics, and write $P(i)$ for the outcome of the program $P$ on the input $i$, including traps and running out of a fixed budget of steps.

- An **edit space** $E(P)$ is a set of programs obtained from $P$ by allowed edits, for example the replacement of one operand, the deletion or insertion of one statement, or the filling of a hole with an expression from a grammar. Each program in it has an *edit distance* from $P$, the number of elementary edits.
- A **test suite** is a finite set $T = \{(i_1, o_1), \dots, (i_n, o_n)\}$ of inputs and expected outcomes. $P$ *passes* $(i, o)$ when $P(i) = o$. $T$ splits into the passing tests $T_+$ and the failing tests $T_-$ of $P$, and $T_- \ne \emptyset$.

**Test-based repair.** Given $P$, $E(P)$ and $T$, find $P' \in E(P)$ that passes every test of $T$, a **plausible patch**, preferably of least edit distance, or report that none exists.

**Specification-based repair.** Given $P$, $E(P)$ and a specification $\varphi$ of the intended input and output relation, find $P' \in E(P)$ that satisfies $\varphi$ on every input.

A patch is **correct** when it satisfies the specification that the developer intended. In test-based repair this specification is not part of the input, so correctness cannot be checked by the repair tool. A plausible patch that is not correct **overfits** the test suite.

## Variants

- **Single-location and multi-location repair.** Most bugs that tools fix need one edit at one place. Multi-location repair, as in Angelix, needs a combined search over several places.
- **Repair with fault localization.** The tool first ranks program locations by how much more often the failing tests run them than the passing tests, and then edits the top-ranked locations first. GenProg weights its mutations this way.
- **Repair templates.** Fixes for known bug classes, such as a missing null check, an off-by-one bound or an [integer overflow](/integer-overflow/), come from a fixed list of patterns.
- **Repair of compilation errors and of student programs.** The tests are the compiler or a reference solution, and the edit space is small syntax changes.
- **Repair under a full specification.** For programs with contracts or assertions, a verifier is the oracle, and the problem is close to program synthesis with a sketch.

## Examples

**A plausible but wrong patch.** The program below should return the larger of $a$ and $b$. The block `l` returns the wrong variable.

```
# params: a, b
entry:
  t = a < b
  br t l r
l:
  ret a
r:
  ret a
```

The test suite is $(1, 2) \mapsto 2$, $(2, 1) \mapsto 2$ and $(3, 3) \mapsto 3$, and the first test fails. Take as the edit space every single change of one operand to $a$, $b$, $t$ or a constant from $-8$ to $8$, of the comparison operator to one of $<, \le, =, \ne$, of the condition of the branch, and the swap of the two branch targets. That gives 99 candidate programs. Exactly two of them pass all three tests: `ret b` in block `l`, which is correct, and `ret 2` in block `l`, which passes because the only test that reaches `l` expects 2. Over all inputs in $[-8, 8]^2$ the second one is wrong on most pairs with $a < b$. A tool that stops at the first plausible patch returns either one, depending on its search order.

**Deleting functionality.** Qi, Long, Achour and Rinard analysed the patches reported for GenProg and two related systems. Most of them did not pass the tests that the authors intended them to pass, and of those that did, many were equivalent to deleting the code that a failing test exercised. Their system Kali, which only deletes code or skips statements, produced about as many plausible and correct patches on the same benchmark.

**A semantic repair.** For a wrong condition such as `if (x > y)` that should be `if (x >= y)`, SemFix replaces the condition by an unknown function of the variables in scope, runs [symbolic execution](/symbolic-execution/) on each test to collect the values the condition must take, and synthesizes an expression from a set of components that meets all these constraints.

## Known algorithms

- **Generate and validate with genetic programming.** GenProg represents a candidate as a list of edits on the syntax tree: delete a statement, insert a statement copied from elsewhere in the program, or replace one statement by such a copy. It weights the statements by fault localization and evolves a population with mutation and crossover, with the number of passed tests as the fitness, as in [genetic programming](/genetic-programming/). It assumes that a fix can often be built from code that already exists in the program.
- **Exhaustive search over a template space.** SPR and Prophet enumerate candidate patches from transformation schemas at ranked locations. Prophet ranks them with a model learned from human patches, so that a correct patch is tried before plausible wrong ones.
- **Semantic repair.** SemFix and Angelix turn the repair into constraints: symbolic execution of each test gives the values that the code at a suspicious location must produce, and a solver for the [SMT problem](/smt-problem/) synthesizes an expression that produces them. Angelix extracts compact constraints, the angelic forest, which lets it repair several locations in large programs.
- **Counterexample-guided repair.** With a verifier as the oracle, a [CEGIS](/cegis/) loop proposes a fix that passes the current tests, asks the verifier for an input that breaks it, and adds that input as a test.
- **Learning-based repair.** Models trained on large sets of human patches propose edits directly; the validation step with the tests is the same.
- **Reduction of the tests.** [Delta debugging](/delta-debugging/) shrinks the failing input first, which makes the failing test faster and the fault localization sharper.

## Bounds

- **Undecidable with a full specification.** Whether a candidate program satisfies a nontrivial semantic property on all inputs is undecidable by [Rice's theorem](/rice-theorem/), so specification-based repair over a programming language with unbounded loops and integers has no general algorithm, even for a single candidate.
- **Decidable with tests and a finite edit space.** With a finite $E(P)$ and a step budget for each run, trying every candidate decides test-based repair with at most $|E(P)| \cdot |T|$ runs.
- **NP-hard for many simultaneous edits.** Take a CNF formula over $x_1, \dots, x_n$. Build a toy IR program with no parameters that sets $x_j = 0$ for each $j$, then computes each clause with or, and the conjunction of all clauses with and, and returns the result. The single test expects 1, and the edit space changes any subset of the $n$ constants to 1. A plausible patch exists if and only if the formula is satisfiable, so test-based repair with unbounded edit distance is NP-hard, by reduction from [SAT](/sat/). With runs of polynomial length it is in NP, because a patch is a certificate that is checked by running the test. With the edit distance bounded by a constant $d$ and $m$ elementary edits, there are $O(m^d)$ candidates, which is polynomial but already too many for slow test suites.
- **Plausibility does not imply correctness.** If the edit space holds two programs that agree on the test inputs and differ elsewhere, both are plausible or neither is, and no algorithm that sees only the tests can tell which one is correct. The example above is such a pair. Smith, Barr, Le Goues and Brun measured this overfitting with independent test suites.

## Reductions

- **To program synthesis.** Specification-based repair is synthesis of a program close to $P$: the edit space is a sketch with holes at the suspicious locations, and the specification is the property to meet. Test-based repair is synthesis from examples with the same sketch.
- **To SAT and SMT.** Semantic repair encodes each hole as an unknown term, each test as a constraint on the values at the hole, and asks a solver for a model, as SemFix and Angelix do.
- **From SAT.** As in the bounds above, satisfiability reduces to test-based repair with many simultaneous edits.
- **To search.** Generate-and-validate repair is a search in the edit space, with the number of passed tests as the objective, which is why tools use genetic programming, random search and ranked enumeration.

## Applications

- **Fixing crashes in continuous integration.** SapFix at Facebook generates fixes for crashes found by automated testing, validates them on the tests, and sends them to engineers, who review and accept or reject each one.
- **Security patching.** Templates for overflow checks, bounds checks and null checks give quick temporary patches for vulnerabilities until a developer writes a full fix.
- **Programming education.** Repair of student submissions against a reference solution gives each student a concrete hint.
- **Compiler and build errors.** Small syntax and type repairs keep a build going and suggest fixes in an editor.

## References
