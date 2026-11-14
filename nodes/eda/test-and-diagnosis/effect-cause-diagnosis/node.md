---
tag: 4MRNNQ
kind: algorithm
slug: effect-cause-diagnosis
name: Effect-cause diagnosis
aliases:
- effect-cause analysis
- Abramovici-Breuer diagnosis
area: eda/test-and-diagnosis
level: advanced
summary: Abramovici and Breuer's diagnosis that reasons back from the observed failing outputs to the lines that could explain them, with no precomputed dictionary.
model: word-ram
complexity:
  vars: {T: the number of tests, L: the number of lines, P: the number of gate input pins, K: the number of distinct failing outputs, C: the number of candidates simulated}
  time: {worst: "O((T + K + C T) (L + P))", average: "O((T + K + C T) (L + P))", best: "O(T (L + P))"}
  space: {extra: O(T L + P)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1980
  people: [Miron Abramovici, Melvin A. Breuer]
  note: Abramovici and Breuer introduced effect-cause analysis at the 1980 Design Automation Conference and in IEEE Transactions on Computers in 1980, for multiple stuck-at faults in combinational circuits, and extended it to sequential circuits in 1982.
prereqs: [fault-dictionary, fault-simulation]
see_also: [stuck-at-fault-model, critical-path-tracing, fault-collapsing, bridging-fault-model, set-cover, logic-simulation, ppsfp, scan-design]
sources:
  - paper: "M. Abramovici and M. A. Breuer, Multiple fault diagnosis in combinational circuits based on an effect-cause analysis, IEEE Transactions on Computers C-29(6), 451 to 460, 1980"
    title: M. Abramovici and M. A. Breuer, Multiple fault diagnosis in combinational circuits based on an effect-cause analysis, IEEE Transactions on Computers C-29(6), 451 to 460, 1980
    locator: the effect-cause approach, the deduction of internal values from the observed response and the lines found fault-free
  - paper: "M. Abramovici and M. A. Breuer, Fault diagnosis based on effect-cause analysis: an introduction, Proceedings of the 17th Design Automation Conference, 69 to 76, 1980"
    title: M. Abramovici and M. A. Breuer, Fault diagnosis based on effect-cause analysis, an introduction, Proceedings of the 17th Design Automation Conference, 69 to 76, 1980
    locator: the idea of diagnosis without a fault dictionary
  - paper: "J. A. Waicukauski and E. Lindbloom, Failure diagnosis of structured VLSI, IEEE Design and Test of Computers 6(4), 49 to 60, 1989"
    title: J. A. Waicukauski and E. Lindbloom, Failure diagnosis of structured VLSI, IEEE Design and Test of Computers 6(4), 49 to 60, 1989
    locator: tracing back from the failing outputs to candidate faults and simulating only the candidates
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on logic-level diagnosis (effect-cause analysis)
---

Effect-cause diagnosis finds the defect of a failing chip by starting from its effects, the outputs that were wrong on the tester, and reasoning back to the lines that could have caused them. It needs no [fault dictionary](/fault-dictionary/), the table of all faulty responses that is otherwise built in advance. Abramovici and Breuer (1980) introduced the approach for multiple stuck-at faults. The version on this page is the common single-fault form, close to the method of Waicukauski and Lindbloom (1989). A fault that explains the data must lie in the fan-in cone of every failing output, and it must be excited on every failing test. These two rules cut the 2L single stuck-at faults of a circuit with L lines down to a few candidates, and only those candidates are simulated. The answer is exactly the set of single stuck-at faults that reproduce the observed response, the same set that a full dictionary lookup would return.

## In plain words

A chip failed some tests, and we know which outputs were wrong. Instead of trying every possible break, we ask where a break could be. A break can only spoil outputs that it is wired to, so it must sit somewhere upstream of every wrong output. A break also does nothing on a test where the broken wire would have carried the stuck value anyway, so on every failed test the good value of that wire must be the opposite of the stuck value. This leaves a short list of suspects. We then try each suspect on the computer and keep the ones that fail in exactly the way the chip failed.

## The problem

The input is a combinational circuit $C$ with lines $\ell_1, \ldots, \ell_L$ (stems and fan-out branches), tests $t_0, \ldots, t_{T-1}$, and the output vectors $z_0, \ldots, z_{T-1}$ that a chip gave on them, with at least one test failing. The output is the set of single stuck-at faults $f$, from the [stuck-at fault model](/stuck-at-fault-model/), such that $C$ with $f$ gives exactly $z_j$ on every $t_j$. With [scan design](/scan-design/), a sequential circuit is tested as a combinational one, so this covers scan chips too.

## The algorithm

```pseudo id=main
EFFECT-CAUSE(C, the tests t_0, ..., t_(T-1), the observed outputs z_0, ..., z_(T-1))
L1  for j ← 0 to T − 1 do g_j ← the values of all lines of the good circuit on t_j
L2  FAIL ← the tests j whose outputs in g_j differ from z_j; if FAIL is empty, return the empty set
L3  S ← all lines
L4  for each output o that is wrong on some test of FAIL do
L5      S ← S ∩ (the fan-in cone of o)
L6  CAND ← the faults "ℓ stuck at 1 − v" for each ℓ in S whose good value is v on every test of FAIL
L7  KEPT ← empty; for each fault f in CAND do
L8      if C with f gives z_j on every t_j then add f to KEPT
L9  return KEPT
```

Line L1 is one [logic simulation](/logic-simulation/) of the good circuit per test. Line L2 compares it with the tester data. Lines L3 to L5 keep only the lines that reach every wrong output; a fan-in cone is found by a search backward from the output. Line L6 keeps one fault per surviving line, and only when the line holds the same good value on all failing tests. Lines L7 and L8 are the only fault simulation, one fault at a time on all tests, and they keep a candidate only when its response matches the chip on every test, passing tests included.

## Example

Take the circuit of the [fault dictionary](/fault-dictionary/) page: $z = a \wedge b$ and $y = b \vee c$, where $b$ has the branches $b{>}z$ and $b{>}y$, with the tests $abc = 110, 010, 100, 001$. The good values are below; each branch has the value of $b$.

| test | $a$ | $b$ | $c$ | $z$ | $y$ |
|---|---|---|---|---|---|
| 0: 110 | 1 | 1 | 0 | 1 | 1 |
| 1: 010 | 0 | 1 | 0 | 0 | 1 |
| 2: 100 | 1 | 0 | 0 | 0 | 0 |
| 3: 001 | 0 | 0 | 1 | 0 | 1 |

**A chip with $y$ wrong on tests 0, 1 and 3.** Line L2 gives FAIL = {0, 1, 3}, and the only wrong output is $y$. Lines L3 to L5 leave the cone of $y$: $b$, $b{>}y$, $c$, $y$. On the failing tests $b$ and $b{>}y$ take the values 1, 1, 0, and $c$ takes 0, 0, 1, so line L6 drops them. Only $y$ holds 1 on all three, so the one candidate is $y$/0. Line L8 simulates it, it matches, and the answer is $\{y/0\}$, after one fault simulation instead of 14.

**A chip with $z$ wrong on test 0 only.** FAIL = {0} and the wrong output is $z$, so S is the cone of $z$: $a$, $b$, $b{>}z$, $z$, all with value 1 on test 0. Line L6 gives four candidates, $a$/0, $b$/0, $b{>}z$/0 and $z$/0. In line L8, $b$/0 also makes $y$ wrong on tests 0 and 1, which the chip did not show, so it is dropped. The answer is $\{a/0, b{>}z/0, z/0\}$, three equivalent faults that no test can tell apart, and the same set as the dictionary lookup.

**A chip with $z$ wrong on test 0 and $y$ wrong on test 3.** The cones of $z$ and $y$ share $b$ only, and $b$ is 1 on test 0 and 0 on test 3, so line L6 gives no candidate and the answer is empty. No single stuck-at fault explains this chip.

On random circuits with fixed seeds, the number of candidates was small. For 10 circuits of 8 inputs and 40 gates with 24 random tests, and 30 random faults per circuit taken as the defect, line L8 simulated 12.1 faults on average, against 260.8 faults in the circuit, and kept 2.45. For 100 gates, 12 inputs and 40 tests it simulated 16.7 against 619.3 and kept 2.51. These are measurements on random netlists, not bounds.

## Correctness

The full proof is on the [proof page](proofs/correctness.md). It rests on two facts about a single stuck-at fault $f$ on a line $\ell$.

1. **Reach.** A line whose fan-in cone does not contain $\ell$ has the same value in the faulty and in the good circuit, on every test. So if $f$ changes an output, $\ell$ lies in the fan-in cone of that output.
2. **Excitation.** If the good value of $\ell$ on a test equals the stuck value, the faulty circuit equals the good circuit on that test, so the test passes.

Let $f$ = "$\ell$ stuck at $v$" reproduce the observed response. Every wrong output is changed by $f$, so by fact 1 $\ell$ survives lines L4 and L5. Every failing test is changed by $f$, so by fact 2 the good value of $\ell$ is $1 - v$ on each of them; that value is the same on all failing tests, and line L6 makes exactly the fault $f$. Line L8 then keeps it. Conversely, line L8 keeps only faults that reproduce the response. So the answer is exactly the set of single stuck-at faults with the observed response.

## Complexity

Line L1 costs $O(T (L + P))$ for $P$ gate input pins, and line L2 costs $O(T L)$. Each fan-in cone is a backward search in $O(L + P)$, so lines L3 to L5 cost $O(K (L + P))$ for $K$ distinct wrong outputs. Line L6 costs $O(L \cdot |FAIL|)$. Line L8 costs $O(T (L + P))$ per candidate, so $O(C T (L + P))$ for $C$ candidates. Since each line gives at most one candidate, $C \le L$, and the worst case is half the cost of simulating all $2L$ faults. In practice the cones of several failing outputs overlap little and C is far smaller than L, as in the measurements above. Space is $O(T L)$ for the good values plus $O(L + P)$ for the netlist and one cone.

## Properties

- **Exact for single stuck-at faults.** The answer equals the brute-force answer that simulates every fault, and the full dictionary answer.
- **No preparation.** Nothing is stored between chips, so a changed test set or netlist costs nothing.
- **Cost per chip.** Each chip needs its own simulations, so diagnosing many chips of one design can cost more than one dictionary.
- **Not robust as written.** If the defect is not a single stuck-at fault, the answer may be empty or wrong.

## Variants and improvements

- **Abramovici and Breuer (1980).** The original method allows multiple stuck-at faults. It processes the tests one by one and deduces, from the observed output values, the values that internal lines must have had in the chip. Lines whose deduced values show they are fault-free are removed, and the lines that remain are the possible fault sites, with no assumption that only one fault is present.
- **Path tracing.** Instead of whole fan-in cones, trace back from each wrong output only through lines whose change could propagate, as in [critical path tracing](/critical-path-tracing/). This gives a smaller S at the same exactness for the single fault model.
- **Scoring instead of exact match.** Waicukauski and Lindbloom (1989) score each candidate by how many failing bits it explains and how many it predicts wrongly, and report the best ones. This tolerates defects that behave like a stuck-at fault on some tests only, such as bridges from the [bridging fault model](/bridging-fault-model/).
- **Several defects.** Diagnose each wrong output separately, then choose a few candidates that together explain all failing bits, a [set cover](/set-cover/) problem.
- **Faster verification.** Simulate the candidates with a bit-parallel simulator such as [PPSFP](/ppsfp/), many tests per word.

## When to use it

Use it for large designs, where a [fault dictionary](/fault-dictionary/) of $F \cdot T \cdot O$ bits does not fit, for chips tested with a changing test set, and for failure analysis of a few chips at a time. Use a dictionary instead when the same small design is diagnosed very often and the table fits. Use the scoring variants when the defect may not be a stuck-at fault.

## Pitfalls

- **Intersecting cones with several defects.** Line L5 keeps only lines in the cone of every wrong output. With two defects, wrong outputs in two separate parts of the circuit leave S empty, and the answer is empty although both defects are visible. When the single fault assumption is in doubt, keep the candidates of each wrong output (the union over L4 to L6 per output) and solve a cover, instead of intersecting.
- **Requiring one good value in line L6.** A stuck-at fault fails only when its line holds the opposite value, so line L6 asks for one good value on all failing tests. A transition fault or a bridge fails with different values on different tests, and line L6 drops it. For those models, change line L6 to the excitation rule of that model.
- **Checking the failing tests only in line L8.** A candidate that matches the failing tests but fails a test that the chip passed is wrong, like $b$/0 in the example. Line L8 must compare all tests.
- **A partial tester log.** If the tester stopped after the first failures, the tests after that point have no data. Treating them as passes in line L8 rejects the true fault. Compare only the tests that were recorded.
- **Reading equivalent faults as poor resolution.** An answer of several faults may be one class of equivalent faults, which no test can split. Check the [fault collapsing](/fault-collapsing/) classes before adding tests.

## Implementations

## History

Fault dictionaries came first: simulate every fault ahead of time and look up the chip. Abramovici and Breuer (1980) proposed to work in the other direction, from the effects to the causes, so that no dictionary is needed and multiple faults can be handled. They presented the idea at the 1980 Design Automation Conference and the full method for combinational circuits in IEEE Transactions on Computers the same year, and extended it to sequential circuits in 1982. With scan design and large chips, the practical form became tracing back from the failing outputs and simulating only the candidates, described by Waicukauski and Lindbloom (1989), with a score in place of an exact match.

## References
