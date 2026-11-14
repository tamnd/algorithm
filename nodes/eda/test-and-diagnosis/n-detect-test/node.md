---
tag: B7563W
kind: concept
slug: n-detect-test
name: N-detect test
aliases:
- N-detection test set
- multiple detection
area: eda/test-and-diagnosis
level: advanced
summary: A test set that detects every stuck-at fault at least N times by different patterns, which raises the chance of catching unmodelled defects.
prereqs: [stuck-at-fault-model, fault-coverage]
see_also: [bridging-fault-model, static-test-compaction, williams-brown-defect-level, automatic-test-pattern-generation, fault-simulation, cell-aware-test, transition-fault-model, set-cover]
sources:
  - paper: "S. C. Ma, P. Franco and E. J. McCluskey, An experimental chip to evaluate test techniques: experiment results, Proceedings of the International Test Conference, 663 to 672, 1995"
    title: S. C. Ma, P. Franco and E. J. McCluskey, An experimental chip to evaluate test techniques, experiment results, Proceedings of the International Test Conference, 663 to 672, 1995
    locator: the Stanford test chip experiment, with the test sets applied to the defective chips and the chips each test set failed to catch
  - paper: "B. Benware, C. Schuermyer, S. Ranganathan, R. Madge, P. Krishnamurthy, N. Tamarapalli, K.-H. Tsai and J. Rajski, Impact of multiple-detect test patterns on product quality, Proceedings of the International Test Conference, 1031 to 1040, 2003"
    title: B. Benware, C. Schuermyer, S. Ranganathan, R. Madge, P. Krishnamurthy, N. Tamarapalli, K.-H. Tsai and J. Rajski, Impact of multiple-detect test patterns on product quality, Proceedings of the International Test Conference, 1031 to 1040, 2003
    locator: the production experiment that compares single-detect and multiple-detect pattern sets on shipped parts
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapters on fault modeling and combinational test generation (stuck-at tests and the defects they cover)
---

An N-detect test set detects every single stuck-at fault at least $N$ times, each time by a different vector. A fault with fewer than $N$ tests must be detected by all of them. The idea is that a real defect seldom behaves exactly like a stuck-at fault. It often behaves like one only when some other condition also holds, and a test set that hits the same fault with many different vectors meets that condition by chance more often. The price is a larger test set, roughly $N$ times larger for small $N$. N-detect test sets keep the cheap stuck-at machinery of test generation and [fault simulation](/fault-simulation/) and aim it at the defects the model does not describe.

## In plain words

A stuck-at test checks that a wire can carry both values. A real short between two wires shows up only when the two wires try to carry different values, and only one of the many tests for the stuck-at fault may set up that situation. If you test every wire once, you may pick the wrong test and miss the short.

So test every wire several times, with different patterns each time. Each extra pattern is another chance to set up the condition that makes the hidden defect visible. You do not need to know what the defect is. You only need enough variety.

## The idea

Fix a combinational circuit, its list $F$ of single [stuck-at faults](/stuck-at-fault-model/), and for each fault $f$ the set $T_f$ of input vectors that detect it. A test set $T$ is **N-detect** when
$$|T \cap T_f| \ \ge\ \min(N, |T_f|) \qquad \text{for every detectable } f \in F.$$
The N-detect [fault coverage](/fault-coverage/) of a set counts a fault as covered when this holds for it. A 1-detect set is an ordinary complete stuck-at test set.

**Why more detections help.** Many defects act like a stuck-at fault under a side condition. For a non-feedback wired-AND bridge between nets $x$ and $y$, the [bridging fault model](/bridging-fault-model/) page proves that a vector $t$ detects the bridge if and only if $t$ detects $x/0$ and $y(t) = 0$, or $t$ detects $y/0$ and $x(t) = 0$. So the tests of the bridge are the tests of $x/0$ that also set $y$ to 0, plus the symmetric ones. A test set that detects $x/0$ once picks one vector of $T_{x/0}$, and the side condition $y = 0$ may fail on it. More vectors from $T_{x/0}$ give more chances. A simple model makes this a number. Suppose the side condition holds on a fraction $p$ of the tests of the fault, and suppose the $N$ tests are drawn independently and uniformly from them. Then all $N$ miss the defect with probability $(1 - p)^N$. The two suppositions are modelling choices, not facts about real test generators, which pick tests in a biased way. The model only shows why the escape rate falls quickly with $N$.

**What is proved.**

- *N-detect sets nest.* An N-detect set is an M-detect set for every $M \le N$, since $\min(M, |T_f|) \le \min(N, |T_f|)$.
- *Large N catches every defect that acts through a stuck-at test.* If $N \ge \max_f |T_f|$, an N-detect set contains every vector that detects any stuck-at fault. So it detects every defect $D$ that has at least one test that also detects some stuck-at fault. By the bridge result above, every detectable non-feedback wired-AND or wired-OR bridge is such a defect. For smaller $N$ there is no such guarantee, as the example shows.
- *A lower bound on the size.* Call faults independent when no vector detects two of them. If $F$ has $r$ pairwise independent faults, each with at least $N$ tests, every N-detect set has at least $rN$ vectors, because each vector counts toward at most one of them.
- *Finding a minimum N-detect set is NP-hard.* For $N = 1$ it is the minimum test set problem, which is NP-hard, as proved on the [static test compaction](/static-test-compaction/) page. In the set cover view of that page, an N-detect set is a set multicover: each fault must be covered $\min(N, |T_f|)$ times. The greedy algorithm for [set cover](/set-cover/) extends to it.

**What is measured, not proved.** Whether N-detect sets catch more defective chips is a question about real defects, and only silicon can answer it. Ma, Franco and McCluskey (1995) applied many kinds of test sets to the defective chips of the Stanford test chip experiment and compared which chips each set failed to catch, and their paper is the usual first citation for test sets that detect each fault several times. Benware and coauthors (2003) compared single-detect and multiple-detect pattern sets on production parts and report that the multiple-detect patterns caught defective parts that the single-detect patterns passed. The size of the gain depends on the chip, the process and the test generator, and this page gives no figure from those studies.

## Examples

**Two small cones.** Take $z = ab$ and $y = c + d$ with outputs $z$ and $y$. There are 6 nets and 12 stuck-at faults, all detectable. The faults $a$/0, $a$/1 and $b$/1 have the tests 11XX, 01XX and 10XX. On the other cone, $c$/0, $d$/0 and $c$/1 (with $d$/1 and $y$/1) have the tests XX10, XX01 and XX00. A minimum 1-detect set has 3 vectors: it pairs each of 11, 01, 10 on $ab$ with one of 00, 10, 01 on $cd$, so there are exactly 6 minimum 1-detect sets.

Now take the wired-AND bridge between $b$ and $c$. Its tests are the tests of $b$/0 with $c = 0$, which are 1100 and 1101, and the tests of $c$/0 with $b = 0$, which are 0010 and 1010. The minimum set $\{1100, 0110, 1001\}$ detects it with 1100. The minimum set $\{1110, 0100, 1001\}$ does not: it detects $b$/0 with 1110, where $c = 1$, and $c$/0 with 1110, where $b = 1$. Of the 6 minimum 1-detect sets, 4 detect the bridge and 2 miss it.

The circuit has 11 pairs of nets that are not in each other's fanout, so 22 non-feedback wired-AND and wired-OR bridges, of which 20 are detectable. (The wired-AND of $a$ and $b$ leaves $z = ab$ unchanged, and the wired-OR of $c$ and $d$ leaves $y$ unchanged.) Brute force over all subsets of the 16 vectors gives:

| $N$ | size of a minimum N-detect set | number of minimum sets | detectable bridges caught, average over the minimum sets | worst minimum set |
|---|---|---|---|---|
| 1 | 3 | 6 | 14.67 of 20 | 12 of 20 |
| 2 | 6 | 6 | 20 of 20 | 20 of 20 |
| 3 | 9 | 1 | 20 of 20 | 20 of 20 |
| 4 | 15 | 1 | 20 of 20 | 20 of 20 |

The faults $a$/0, $a$/1 and $b$/1 are pairwise independent and have 4 tests each, so the lower bound $3N$ gives 3, 6 and 9, which is exact for $N \le 3$. For $N = 4$ every fault with 4 tests needs all of them, which forces 15 of the 16 vectors, and the bound 12 is not tight.

**Random circuits.** These numbers come from toy inputs, not from benchmark circuits. With `random.Random(42)`, 150 random circuits of 4 or 5 inputs and 4 to 8 gates, and a test generator that takes the faults in random order and adds random tests of each fault until it has $\min(N, |T_f|)$ of them, the share of the 8254 detectable non-feedback bridges that the test sets caught was:

| $N$ | vectors in total | bridges caught |
|---|---|---|
| 1 | 901 | 94.91% |
| 2 | 1635 | 99.04% |
| 3 | 2146 | 99.78% |
| 5 | 2846 | 99.98% |
| 10 | 3441 | 100% |

The test set grows by less than a factor of $N$, because one vector often counts toward many faults, and the escapes fall quickly. Real circuits have many more tests per fault and defects that are less tied to single stuck-at faults, so these numbers say nothing about silicon.

## Where it is used

- **Production ATPG.** Test generators offer an N-detect mode with a small $N$, and some apply extra detections only to faults near layout features prone to defects, to limit the growth of the test set.
- **Defect level.** The [Williams-Brown formula](/williams-brown-defect-level/) estimates the defect level from fault coverage, assuming that the coverage of defects equals the coverage of faults. N-detect sets aim to close the gap between the two when defects are not stuck-at faults.
- **Compaction trade-off.** [Static test compaction](/static-test-compaction/) removes vectors that add no stuck-at detection, which removes exactly the extra chances that N-detect sets add. Compacting to an N-detect target keeps them.
- **Other fault models.** The same idea applies to [transition faults](/transition-fault-model/), with N different pairs per fault. [Cell-aware tests](/cell-aware-test/) attack the same problem from the other side, by modelling the defects inside cells instead of hoping to hit them.
- **Diagnosis.** Several different detections of each fault also help to tell faults apart, which a single detection often cannot.

## References
