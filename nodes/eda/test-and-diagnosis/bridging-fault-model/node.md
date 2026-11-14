---
tag: 8K4Y9H
kind: model
slug: bridging-fault-model
name: Bridging fault model
aliases:
- bridging fault
- wired-AND and wired-OR fault
area: eda/test-and-diagnosis
level: core
summary: A fault model of a short between two signal lines, as wired-AND, wired-OR or dominant bridge, often chosen from layout neighbours.
prereqs: [stuck-at-fault-model]
see_also: [critical-area, fault-coverage, redundant-fault, iddq-testing, cell-aware-test, n-detect-test, transition-fault-model, fault-simulation]
sources:
  - paper: doi:10.1109/T-C.1974.224020
    title: K. C. Y. Mei, Bridging and stuck-at faults, IEEE Transactions on Computers C-23(7), 720 to 727, 1974
    locator: the wired-AND and wired-OR models of a short between two lines, and which bridging faults the tests for stuck-at faults detect
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on fault modeling (bridging faults, feedback and non-feedback bridges)
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Fault Modeling (bridging faults and their logical models)
---

The bridging fault model describes a defect as an unwanted connection, a short, between two signal lines of a circuit. A logical rule says which value the two shorted lines take: the AND of the two values (wired-AND), their OR (wired-OR), or the value of one line forced on the other (dominant bridge). The model is closer to real spot defects than the [stuck-at fault model](/stuck-at-fault-model/), since extra metal between two wires is a common defect. Its cost is the number of candidate pairs, which grows with the square of the number of lines, so the list is taken from wires that run next to each other in the layout.

## The machine

The circuit is a combinational gate circuit $C$ with nets, where a net is the wire from one driver to all its sinks. A bridging fault is an unordered pair of distinct nets $\{x, y\}$ and a rule. Let $x_d$ and $y_d$ be the values that the drivers of $x$ and $y$ produce. With the fault, every sink of $x$ reads $\hat{x}$ and every sink of $y$ reads $\hat{y}$, where:

- **wired-AND:** $\hat{x} = \hat{y} = x_d \wedge y_d$;
- **wired-OR:** $\hat{x} = \hat{y} = x_d \vee y_d$;
- **$x$ dominates $y$:** $\hat{x} = x_d$ and $\hat{y} = x_d$.

The rule is an assumption about the technology. A wired-AND holds when the driver of a 0 is much stronger than the driver of a 1, a wired-OR in the opposite case, and a dominant bridge when one driver is much stronger than the other. The model assumes that one bridge is present and that the short has zero resistance.

The bridge is **non-feedback** if neither net lies in the fanout cone of the other, so that no path in $C$ leads from $x$ to $y$ or from $y$ to $x$. Then the faulty circuit is still combinational. Otherwise it is a **feedback** bridge, and the faulty circuit has a loop.

A vector $t$ detects the bridge if the faulty circuit, settled under $t$, gives a different value than $C$ at some primary output.

## What it counts

The model predicts which vectors detect each listed bridge, and from them the bridging [fault coverage](/fault-coverage/) of a test set. The list is the main choice. A circuit with $N$ nets has $N(N - 1)/2$ pairs, too many to simulate, and most of them cannot short since the wires are far apart. Tools extract the pairs of nets that run close together for some length in the layout, and weight them by their [critical area](/critical-area/), the area where a spot defect of a given size would connect them. The coverage is then a fraction of the extracted list, or of its total critical area, and a report should say which.

Take $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, so $z = ab + bc$, with a bridge between the inputs $a$ and $c$.

| rule | faulty output | vectors $abc$ that detect it |
|---|---|---|
| wired-AND | $z = b(ac) + b(ac) = abc$ | 011, 110 |
| wired-OR | $z = b(a + c) = ab + bc$ | none |
| $a$ dominates $c$ | $z = ab$ | 011 |

The same pair of nets gives a detectable fault under one rule and a [redundant](/redundant-fault/) one under another. The test set $\{110, 011\}$, which detects the wired-AND bridge, is also a test set for the stuck-at faults a/0 and c/0.

## Relation to other models

- **Stuck-at faults.** Under a vector where the bridged lines have equal values, a non-feedback bridge changes nothing. Where they differ, it acts as one line stuck at the value of the other (see the results below). So a bridge test is a stuck-at test with a condition on a second line. Mei studied in 1974 which bridges the tests for stuck-at faults detect.
- **Resistive bridges.** A short with resistance gives an intermediate voltage. Two gates that read the bridged net can then see different logic values, since their switching thresholds differ, and the bridge may only slow a transition. The logical rules above do not describe this case. [IDDQ testing](/iddq-testing/), which measures the supply current in the quiet state, detects many such bridges, since a bridge between nets at different values draws current.
- **Delay.** A weak bridge may give the correct final value too late, which makes it a delay fault. See the [transition fault model](/transition-fault-model/).
- **Shorts inside cells.** Bridges between nodes inside a library cell are the targets of [cell-aware tests](/cell-aware-test/).
- **Multiple detection.** A test set that detects each stuck-at fault many times, an [n-detect test](/n-detect-test/), meets the side condition of more bridges by chance.

## Known results in the model

- **Reduction to stuck-at for non-feedback bridges.** Let $\{x, y\}$ be a non-feedback wired-AND bridge. Then $t$ detects it if and only if either $x(t) = 1$, $y(t) = 0$ and $t$ detects $x/0$, or $x(t) = 0$, $y(t) = 1$ and $t$ detects $y/0$. *Proof.* If $x(t) = y(t)$, the AND of the two values equals each of them, so every sink reads its good value and the outputs do not change. Let $x(t) = 1$ and $y(t) = 0$. Since no path leads from $x$ to $y$, the driver value $y_d$ does not depend on the value of $x$, and it stays 0. So the sinks of $y$ read 0, their good value, and the sinks of $x$ read 0. This is the circuit with $x/0$ under $t$. The other case is symmetric. $\square$ Wired-OR is the same with $x/1$ and $y/1$, and a dominant bridge of $x$ over $y$ is detected when $x(t) \ne y(t)$ and $t$ detects $y$ stuck at $x(t)$.
- **Feedback bridges may oscillate.** Take $z = \mathrm{NAND}(a, b)$ with a wired-AND bridge between $b$ and $z$. The driver of $z$ computes $z_d = \mathrm{NAND}(a, b \wedge z_d)$. Under $a = b = 1$, this is $z_d = \lnot z_d$, which has no stable solution, so the circuit oscillates. Other feedback bridges create a latch that keeps its old value. A feedback bridge can thus need a sequence of vectors, and its effect can depend on the circuit delays.
- **Count.** A full list has $\binom{N}{2}$ pairs and three rules, so it is quadratic in the number of nets, against $2L$ stuck-at faults. Layout extraction keeps the list close to linear in practice, since each net has few close neighbours. This is an observation about layouts, not a theorem.
- **Redundant bridges.** As in the example, a bridge whose two lines feed symmetric logic can leave the function unchanged. Deciding whether a bridge is detectable is NP-hard, like the same question for stuck-at faults. Add to a circuit a net that is constant 0, such as $\mathrm{AND}(x_1, \lnot x_1)$, that feeds nothing. A wired-AND bridge between this net and a line $\ell$ acts as $\ell/0$, so the stuck-at question reduces to the bridge question.

## References
