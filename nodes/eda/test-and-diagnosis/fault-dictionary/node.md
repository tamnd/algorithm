---
tag: 4SH7E3
kind: data-structure
slug: fault-dictionary
name: Fault dictionary
aliases:
- cause-effect diagnosis
area: eda/test-and-diagnosis
level: core
summary: A table of the faulty responses of every modelled fault to the test set, compared with an observed failing response to name the likely faults.
model: word-ram
complexity:
  vars: {F: the number of faults, T: the number of tests, O: the number of primary outputs, L: the number of lines, P: the number of gate input pins, w: the word size in bits}
  time: {worst: O(F T (L + P)), average: O(F T (L + P)), best: O(F T (L + P))}
  space: {extra: "O(F T (O / w + 1))"}
properties: {deterministic: true, recursive: false}
prereqs: [fault-simulation, stuck-at-fault-model]
see_also: [effect-cause-diagnosis, fault-collapsing, ppsfp, hamming-distance, multiple-input-signature-register, fault-coverage, n-detect-test, automatic-test-pattern-generation]
sources:
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on logic-level diagnosis (fault dictionaries, their size, and matching an observed response)
  - paper: "I. Pomeranz and S. M. Reddy, On the generation of small dictionaries for fault location, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design, 272 to 279, 1992"
    title: I. Pomeranz and S. M. Reddy, On the generation of small dictionaries for fault location, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design, 272 to 279, 1992
    locator: dictionaries that keep only the output values needed to tell the faults apart
  - paper: "B. Chess and T. Larrabee, Creating small fault dictionaries, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 18(3), 346 to 356, 1999"
    title: B. Chess and T. Larrabee, Creating small fault dictionaries, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 18(3), 346 to 356, 1999
    locator: the sizes of full-response and pass-fail dictionaries, and smaller dictionaries with almost the full resolution
  - book: isbn:9780123705976
    title: Laung-Terng Wang, Cheng-Wen Wu and Xiaoqing Wen, VLSI Test Principles and Architectures, Morgan Kaufmann, 2006
    locator: the chapter on logic diagnosis (diagnosis with dictionaries and by effect-cause analysis)
---

A fault dictionary stores, for every modeled fault of a circuit, the response that the faulty circuit gives to a fixed test set. When a chip fails on the tester, its observed response is looked up in the table, and the faults stored under that response are the candidates for the defect. The table is built once per design by [fault simulation](/fault-simulation/) of every fault, so diagnosis of each failing chip is a cheap lookup. The full-response dictionary keeps every output of every test and needs $F \cdot T \cdot O$ bits for $F$ faults, $T$ tests and $O$ outputs. The pass-fail dictionary keeps only which tests fail, $F \cdot T$ bits, and tells fewer faults apart.

## In plain words

When a chip fails a test, the engineer wants to know where the defect is, so that the chip can be cut open at the right place.

A fault dictionary is prepared before any chip is made. A program breaks the circuit design in one place at a time, runs the tests on the broken design, and writes down how it fails: which tests fail and which outputs are wrong. One line of the table per kind of break.

When a real chip fails, its wrong outputs are looked up in the table. The breaks listed under the same failure are the suspects. A small table that keeps only which tests failed is cheaper to store but often lists more suspects.

## The abstract type

The dictionary is built over a fixed circuit $C$ with $O$ primary outputs and a fixed test set $t_0, \ldots, t_{T-1}$. For a fault $f$ and a test $t_j$, let the **error word** $R_j(f)$ be the $O$-bit word whose bit $k$ is 1 when output $k$ of the circuit with $f$ differs from the good circuit on $t_j$. The **full response** of $f$ is $R(f) = (R_0(f), \ldots, R_{T-1}(f))$, and its **pass-fail response** is $P(f) = \{ j : R_j(f) \ne 0 \}$, the set of failing tests.

The value is a set $D$ of faults. The operations are:

- `add_fault(f)`: add $f$ to $D$.
- `observe(z_0, ..., z_(T-1))`: turn the output vectors seen on the tester into error words.
- `lookup_full(r)`: return $\{ f \in D : R(f) = r \}$.
- `lookup_pass_fail(r)`: return $\{ f \in D : P(f) = \{ j : r_j \ne 0 \} \}$.
- `nearest(r)`: return the faults of $D$ whose full response is closest to $r$ in [Hamming distance](/hamming-distance/), and the distance.

## Representation

Two hash maps. The full map has the key $R(f)$, a tuple of $T$ error words, and the value is the list of faults with that response. The pass-fail map has the key $P(f)$, a $T$-bit mask, and the same kind of list. The good output vectors of all tests are stored once. Each fault sits in exactly one list of each map, the one under its own key. That is the invariant.

On disk, the full dictionary is a matrix with one row per fault and $T \cdot O$ bits per row, so $F \cdot T \cdot O$ bits, and the pass-fail dictionary has $T$ bits per row, so $F \cdot T$ bits.

## Operations

```pseudo id=main
BUILD(C, the tests t_0, ..., t_(T-1))
L1  for j ← 0 to T − 1 do G[j] ← the outputs of the good circuit on t_j
ADD-FAULT(f)
L2  R ← (R_0, ..., R_(T-1)), where for each test j
L3      R_j ← (the outputs of C with f on t_j) XOR G[j]
L4  P ← the set of j with R_j ≠ 0
L5  append f to FULL[R]
L6  append f to PF[P]
LOOKUP(the observed outputs z_0, ..., z_(T-1))
L7  r ← (z_0 XOR G[0], ..., z_(T-1) XOR G[T-1])
L8  return FULL[r]
L9  or, with the pass-fail dictionary, return PF[the set of j with r_j ≠ 0]
```

Line L1 runs once. Lines L2 to L6 simulate one fault on every test, which is the whole cost of the dictionary. Any fault simulator can do it, for example [PPSFP](/ppsfp/) with many tests per word. Lines L7 to L9 are the diagnosis of one chip: one pass over the tester data and one hash probe. A response that matches no key returns the empty list, and then `nearest` gives the closest stored responses.

## Example

Take the circuit $z = a \wedge b$, $y = b \vee c$ with the outputs $z$ and $y$. The input $b$ feeds two gates, so it has a stem $b$ and two branches, $b{>}z$ and $b{>}y$. That makes 7 lines and 14 single stuck-at faults. The tests are $abc = 110, 010, 100, 001$, and the good outputs $zy$ are 11, 01, 00, 01. The table shows the wrong outputs of each fault on each test, with a dash when the test passes.

| fault | 110 | 010 | 100 | 001 | failing tests |
|---|---|---|---|---|---|
| $a$/0, $b{>}z$/0, $z$/0 | $z$ | - | - | - | {0} |
| $a$/1 | - | $z$ | - | - | {1} |
| $b$/0 | $z, y$ | $y$ | - | - | {0, 1} |
| $b{>}y$/0 | $y$ | $y$ | - | - | {0, 1} |
| $b$/1 | - | - | $z, y$ | - | {2} |
| $b{>}z$/1 | - | - | $z$ | - | {2} |
| $b{>}y$/1, $c$/1, $y$/1 | - | - | $y$ | - | {2} |
| $c$/0 | - | - | - | $y$ | {3} |
| $z$/1 | - | $z$ | $z$ | $z$ | {1, 2, 3} |
| $y$/0 | $y$ | $y$ | - | $y$ | {0, 1, 3} |

The full dictionary has 10 classes and takes $14 \cdot 4 \cdot 2 = 112$ bits. The pass-fail dictionary has 7 classes and takes $14 \cdot 4 = 56$ bits. It merges $b$/0 with $b{>}y$/0, which fail the same tests on different outputs, and it merges the five faults that fail only test 2.

A chip that shows $z = 0$ on test 0 and passes the rest has the observed error words $(z, -, -, -)$, and the lookup returns $\{a/0, b{>}z/0, z/0\}$. No test can split this class: the three faults are equivalent, since each one makes $z = 0$ always, as on the [fault collapsing](/fault-collapsing/) page. The same holds for $\{b{>}y/1, c/1, y/1\}$. So here the full dictionary tells apart every pair of faults that any test set could tell apart. A chip with $z$ wrong on test 0 and $y$ wrong on test 3 matches no row: no single stuck-at fault explains it. Its nearest rows, at distance 1, are the class of $z$/0 and $c$/0, which hints at two defects.

## Correctness

The claims are proved on the [proof page](proofs/correctness.md).

1. **Invariant.** After any sequence of `add_fault` calls, every fault of $D$ is in exactly one list of each map, the list under $R(f)$ and the list under $P(f)$.
2. **The true fault is never lost.** If a chip behaves exactly like the circuit with a modeled fault $f \in D$, then `lookup_full` returns exactly the faults of $D$ that no test of the set tells apart from $f$, and $f$ is one of them. `lookup_pass_fail` returns a superset of it.
3. **Pass-fail is coarser.** Each class of the full dictionary lies inside one class of the pass-fail dictionary, so the pass-fail dictionary never has more classes. With $T$ tests it has at most $2^T$ classes, so it needs $T \ge \log_2 K$ tests to separate $K$ classes, while a full dictionary can separate up to $2^{T \cdot O}$.

The guarantee is for chips whose defect behaves like one modeled fault. A defect outside the model, such as a bridge between two lines or two faults at once, can match no row, or a wrong row.

## Complexity

Building takes one simulation of the good circuit per test and one simulation of each fault on each test. With plain simulation of $O(L + P)$ per vector, for $L$ lines and $P$ gate input pins, that is $O(F T (L + P))$ time. Bit-parallel simulators divide this by up to the word size, and fault dropping is not allowed: a dictionary needs the response of a fault to every test, not only to the first test that detects it.

Storage is $F \cdot T \cdot O$ bits for the full dictionary and $F \cdot T$ bits for the pass-fail one. For a design with $10^6$ faults, $10^4$ tests and $10^4$ observed scan cells, the full dictionary would need $10^{14}$ bits, about 12.5 terabytes, which is why full dictionaries are not stored for large designs.

A lookup reads the $T$ error words of the chip and makes one hash probe, so $O(T)$ expected word operations when $O \le w$, plus the size of the answer. `nearest` compares with every row, $O(F T)$.

## Variants

- **Drop on $n$ detections.** Simulate each fault only until it has been detected $n$ times. The table is smaller and faster to build, and it keeps the first failing tests, which are what a tester records when it stops after a few failures.
- **Small dictionaries.** Pomeranz and Reddy (1992) and Chess and Larrabee (1999) keep only the output bits, or the extra information beyond pass-fail, that are needed to tell the classes apart. Their tables are close to the pass-fail size with close to full resolution.
- **Signature dictionaries.** Store the [MISR](/multiple-input-signature-register/) signature of each faulty response instead of the response. This fits BIST, where only signatures are read, but aliasing can merge classes.
- **Matching with a score.** Real defects rarely match a row exactly. Score each fault by the number of failing bits it explains, the number it predicts but the chip did not show, and the number it misses, and rank the faults by the score.
- **No dictionary.** [Effect-cause diagnosis](/effect-cause-diagnosis/) starts from the failing outputs of the chip and simulates only the faults that could reach them, so it needs no table at all.

## When to use it

Use a dictionary when many chips of one design must be diagnosed and the design is small enough to store the table, or when only the pass-fail table or a small dictionary is needed. The cost moves from each diagnosis to one large simulation at the start. For large designs, or when the test set changes often, simulate on demand with [effect-cause diagnosis](/effect-cause-diagnosis/), which builds no table but simulates for each chip. To raise the resolution of either method, add tests that tell apart the faults in large classes.

## Pitfalls

- **Fault dropping in line L3.** A fault simulator used for [fault coverage](/fault-coverage/) stops simulating a fault once a test detects it. Used to build the table, it leaves the later tests of every fault blank, and two faults that differ only on later tests share a row. Line L3 must simulate every fault on every test, or the table must record which tests were simulated.
- **Exact match only in line L8.** Most real defects are not single stuck-at faults, so an exact lookup often returns nothing. Keep `nearest` or a score as the fallback, and report the distance, since a large distance means the fault model does not fit.
- **The tester stops early.** Testers often record only the first few failing cycles. The observed response is then partial, and comparing it with full rows in line L8 treats the missing tests as passes. Compare only the tests that were applied and recorded.
- **Equivalent faults look like a weak test.** A class of several faults may be a set of equivalent faults that no test can split. Collapse the fault list first, so that the class size reports real ambiguity.
- **The size grows with three factors.** $F \cdot T \cdot O$ grows quickly. Estimate it before choosing the full form.

## Implementations

## History

Fault dictionaries are the first form of logic diagnosis described in the test books: simulate every fault ahead of time and look up the failing response, starting from the causes rather than from the effects. The growth of $F \cdot T \cdot O$ with design size led to the pass-fail form and to the small dictionaries of Pomeranz and Reddy (1992) and of Chess and Larrabee (1999), and to the dictionary-free effect-cause methods that start from the observed failures.

## References
