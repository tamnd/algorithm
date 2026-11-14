---
tag: SS7SJX
kind: definition
slug: fault-coverage
name: Fault coverage
aliases:
- test coverage
- fault efficiency
area: eda/test-and-diagnosis
level: intro
summary: The fraction of the faults of a fault list that a test set detects, with two related ratios that credit or exclude the faults proved undetectable.
prereqs: [stuck-at-fault-model, fault-simulation]
see_also: [redundant-fault, fault-collapsing, williams-brown-defect-level, automatic-test-pattern-generation, transition-fault-model, n-detect-test, parallel-fault-simulation, ppsfp]
sources:
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapters Fault Modeling and Logic and Fault Simulation (fault coverage, its ratios and the fault list they use)
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapters on fault simulation and test generation (fault coverage, undetectable faults and test quality)
  - paper: doi:10.1109/TC.1981.1675742
    title: T. W. Williams and N. C. Brown, Defect level as a function of fault coverage, IEEE Transactions on Computers C-30(12), 987 to 988, 1981
    locator: the use of fault coverage to predict the fraction of bad chips that pass the test
---

Fault coverage is the fraction of the faults of a fault list that a test set detects. It is the main number that [fault simulation](/fault-simulation/) gives, and the main measure of the quality of a manufacturing test. Two related ratios treat the faults that no test can detect in a different way: one counts the faults proved undetectable as covered, and one removes the undetectable faults from the count. A coverage number means little unless it says which ratio it is and which fault list it counts.

## Definition

Let $C$ be a circuit, $\Phi$ a finite list of faults of one fault model, for example the single stuck-at faults of the [stuck-at fault model](/stuck-at-fault-model/), and $T$ a set of tests. A test is an input vector for stuck-at faults, or a pair of vectors for delay faults. Write $D(T) \subseteq \Phi$ for the faults that some test of $T$ detects. Let $R \subseteq \Phi$ be the faults that a tool has proved [redundant](/redundant-fault/), that is undetectable by any test, and let $U \subseteq \Phi$ with $R \subseteq U$ be the faults that the tool classes as untestable for any reason, for example proved redundant or blocked by a constraint of the test setup.

The **fault coverage** of $T$ is
$$\mathrm{FC}(T) = \frac{|D(T)|}{|\Phi|}.$$

Two related ratios are in common use.

- The ratio that credits proved redundancy is $\dfrac{|D(T)| + |R|}{|\Phi|}$. It reaches 1 exactly when every fault is either detected or proved undetectable, so it measures how complete the work of the test generator is.
- The ratio over the testable faults is $\dfrac{|D(T)|}{|\Phi| - |U|}$. It removes the untestable faults from the denominator, so it measures how many of the faults that a test could find were found.

For the same $T$, the fault coverage is never above either of the two others, since $|D(T)| \le |D(T)| + |R|$ and $|\Phi| - |U| \le |\Phi|$. The three are equal when $U$ is empty. The names of the two related ratios are not the same in all tools and books, so a report should give the formula or the counts, not only a name.

The value also depends on the fault list $\Phi$. After [fault collapsing](/fault-collapsing/), $\Phi$ holds one fault per class of equivalent faults, and each class counts once. A class with many faults weighs as much as a class with one, so the collapsed and the uncollapsed coverage of the same test set differ.

## Examples and non-examples

**Same tests, two lists.** Take $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$ with the stem $b$ and the branches $b_g$ and $b_h$, which has 8 lines and 16 single stuck-at faults. The test set $\{110, 011\}$ detects a/0, $b_g$/0, g/1, $b_h$/0, c/0, h/1, b/0 and z/0, so $\mathrm{FC} = 8/16 = 50\%$. At each NAND gate, an input stuck at 0 is equivalent to the output stuck at 1, which gives three classes of three faults: {a/0, $b_g$/0, g/1}, {$b_h$/0, c/0, h/1} and {g/0, h/0, z/1}. The collapsed list has $16 - 6 = 10$ classes. The same test set detects 4 of them, so its collapsed coverage is $4/10 = 40\%$.

**Redundant faults.** The circuit $p = \mathrm{AND}(a, b)$, $q = \mathrm{AND}(\lnot a, c)$, $r = \mathrm{AND}(b, c)$, $z = \mathrm{OR}(p, q, r)$ computes $z = ab + \bar{a}c + bc$, and the term $bc$ is the consensus of the two others. It has 14 lines and 28 faults. The faults r/0, $b_r$/0 and $c_r$/0 make $r = 0$, and $z$ stays the same function, so they are redundant. All 8 input vectors together detect the other 25 faults, and the four vectors 001, 010, 101 and 110 detect them too.

| tests | $\lvert D \rvert$ | $\lvert R \rvert$ | $\lvert U \rvert$ | fault coverage | credit for $R$ | over testable |
|---|---|---|---|---|---|---|
| {110, 001} | 12 | 2 | 2 | 12/28 = 42.9% | 14/28 = 50.0% | 12/26 = 46.2% |
| {001, 010, 101, 110} | 25 | 2 | 2 | 25/28 = 89.3% | 27/28 = 96.4% | 25/26 = 96.2% |
| {001, 010, 101, 110} | 25 | 3 | 3 | 25/28 = 89.3% | 28/28 = 100% | 25/25 = 100% |

The first two rows assume that the tool proved r/0 and $b_r$/0 redundant but stopped on $c_r$/0 before a proof. The complete test set has a fault coverage below 100% in every row, because 100% is not reachable for this circuit. So a fault coverage below 100% does not mean that a test is missing.

**Non-example: the fraction of vectors.** The number of distinct vectors applied, divided by $2^n$, is not a coverage. In the consensus circuit, 4 of the 8 vectors already detect every detectable fault.

**Non-example: a fault list of another model.** A test set with 100% stuck-at coverage can have a low coverage of [transition faults](/transition-fault-model/), since a single vector does not launch a transition. A coverage number holds for one fault model only.

## Related definitions

- **Detected fault.** A fault $f$ is detected by a test if the good circuit and the circuit with $f$ give different values at some primary output. For a pair of vectors, the second vector is the one that is observed.
- **Redundant fault.** A fault that no test detects. See [redundant fault](/redundant-fault/). Proving a fault redundant is as hard as [automatic test pattern generation](/automatic-test-pattern-generation/), so $R$ is often smaller than the set of all redundant faults.
- **Aborted fault.** A fault for which the test generator stopped, after a work limit, with neither a test nor a proof. It is in neither $D(T)$ nor $R$, and it lowers all three ratios.
- **Multiple detection.** The $n$-detect coverage counts a fault as detected only if at least $n$ different tests detect it. See [n-detect test](/n-detect-test/).
- **Defect level.** The fraction of shipped chips that are bad. The [Williams-Brown formula](/williams-brown-defect-level/) gives it from the yield and the fault coverage, under the assumption that every fault is equally likely.

## References
