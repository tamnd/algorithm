---
tag: FEY9Z3
kind: theorem
slug: williams-brown-defect-level
name: Williams-Brown defect level formula
aliases:
- defect level formula
area: eda/test-and-diagnosis
level: core
summary: Williams and Brown's formula DL = 1 - Y^(1 - T) for the fraction of shipped chips that are bad, given the yield Y and the fault coverage T.
prereqs: [fault-coverage]
see_also: [poisson-yield-model, negative-binomial-yield-model, murphy-yield-model, critical-area, stuck-at-fault-model, n-detect-test, binomial-distribution]
sources:
  - paper: doi:10.1109/TC.1981.1675742
    title: T. W. Williams and N. C. Brown, Defect level as a function of fault coverage, IEEE Transactions on Computers C-30(12), 987 to 988, 1981
    locator: the formula DL = 1 - Y^(1 - T) and its assumptions
  - paper: "V. D. Agrawal, S. C. Seth and P. Agrawal, Fault coverage requirement in production testing of LSI circuits, IEEE Journal of Solid-State Circuits SC-17(1), 57 to 61, 1982"
    title: V. D. Agrawal, S. C. Seth and P. Agrawal, Fault coverage requirement in production testing of LSI circuits, IEEE Journal of Solid-State Circuits SC-17(1), 57 to 61, February 1982
    locator: a model with a distribution of the number of faults on a bad chip, which gives a lower defect level than the formula for the same coverage
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter on test economics and product quality (yield, defect level and the Williams-Brown formula)
---

The Williams-Brown formula gives the defect level $\mathrm{DL}$, the fraction of the chips that pass a test but are bad, as $\mathrm{DL} = 1 - Y^{1 - T}$, where $Y$ is the yield and $T$ the [fault coverage](/fault-coverage/) of the test. It follows exactly from a simple model: every fault is equally likely and the faults occur independently. It shows why test engineers ask for coverage very close to 100%: at a yield of 50%, a coverage of 99% still ships about 6900 bad chips per million.

## Statement

**Model.** A chip has a list of $n$ possible faults. Each fault is present with the same probability $p$, independently of the others. A chip is good if and only if no fault is present, so the yield is
$$Y = \Pr[\text{chip good}] = (1 - p)^n.$$
The test detects $m$ of the $n$ faults, and $T = m / n$ is its fault coverage. A chip fails the test if and only if at least one of the $m$ detected faults is present: a detected fault is never hidden by another fault on the same chip.

**Theorem (Williams and Brown, 1981).** In this model, with $0 < Y \le 1$, the probability that a chip passes the test is $Y^T$, and the defect level, the probability that a chip that passes is bad, is
$$\mathrm{DL} = 1 - Y^{1 - T}.$$

The fault count $n$ and the fault probability $p$ do not appear in the result. The formula has two inputs, and both come from outside the model. $Y$ is measured on the line, or predicted by a yield model such as the [Poisson yield model](/poisson-yield-model/). $T$ comes from [fault simulation](/fault-simulation/) of the test set. Nothing in the formula is fitted to the shipped chips.

## In plain words

Picture each chip as a set of places where something can break, each with the same small chance, each independent of the others. A chip is good when nothing broke. The test checks some of the places.

A chip passes when nothing broke at the checked places. Among the chips that pass, the bad ones are those where something broke at an unchecked place. The fewer places are left unchecked, the fewer bad chips get through. The rule depends only on the share of good chips and on the share of places that the test checks, not on how many places there are.

## Proof

Let $A$ be the event that the chip passes the test and $G$ the event that it is good. Then $G \subseteq A$, since a good chip has no fault and so no detected fault.

The chip passes if and only if none of the $m$ detected faults is present. These faults are independent and each is absent with probability $1 - p$, so
$$\Pr[A] = (1 - p)^m = \left((1 - p)^n\right)^{m / n} = Y^T.$$
Since $G \subseteq A$, $\Pr[G \mid A] = \Pr[G] / \Pr[A] = Y / Y^T = Y^{1 - T}$, which is well defined since $Y^T > 0$. The defect level is the probability that a passing chip is bad:
$$\mathrm{DL} = 1 - \Pr[G \mid A] = 1 - Y^{1 - T}. \qquad \square$$

The same value follows by counting faults. The number $K$ of faults on a chip has the [binomial distribution](/binomial-distribution/) with parameters $n$ and $p$, and given $K = k$, the set of faults present is a uniform random $k$-subset of the list. A chip with $k$ faults passes with probability $\binom{n - m}{k} / \binom{n}{k}$, and
$$\sum_{k} \binom{n}{k} p^k (1 - p)^{n - k} \frac{\binom{n - m}{k}}{\binom{n}{k}} = (1 - p)^m \sum_{k} \binom{n - m}{k} p^k (1 - p)^{n - m - k} = (1 - p)^m.$$

## Consequences

- **Ends of the range.** With no test, $T = 0$ and $\mathrm{DL} = 1 - Y$, the fraction of bad chips made. With full coverage, $T = 1$ and $\mathrm{DL} = 0$. In between, $\mathrm{DL}$ falls as $T$ grows, and for $T$ near 1, $\mathrm{DL} \approx (1 - T)\ln(1 / Y)$.
- **Numbers.** These values follow from the formula, not from measurement.

| yield $Y$ | coverage $T$ | $\mathrm{DL}$ | bad chips per million shipped |
|---|---|---|---|
| 0.5 | 0.90 | 0.0670 | 66967 |
| 0.5 | 0.99 | 0.00691 | 6908 |
| 0.5 | 0.999 | 0.000693 | 693 |
| 0.1 | 0.99 | 0.0228 | 22763 |
| 0.9 | 0.99 | 0.00105 | 1053 |

- **Required coverage.** Solving for $T$ gives $T = 1 - \ln(1 - \mathrm{DL}) / \ln Y$. For 100 bad chips per million at $Y = 0.5$, the coverage must be at least 99.986%. A low yield needs a higher coverage for the same defect level.
- **Passing fraction.** The fraction of chips that pass, $Y^T$, is above the true yield. Measuring it at two coverages, for example after part of the test program, gives a way to estimate $Y$.
- **With the Poisson yield model.** If $Y = e^{-AD}$ for the [critical area](/critical-area/) $A$ and the defect density $D$, then $\mathrm{DL} = 1 - e^{-(1 - T) A D}$: the test acts as if it removed a fraction $T$ of the defects.

## Tightness

The formula is exact in its model, so any error comes from the assumptions.

**Unequal fault probabilities.** Take two faults with probabilities $p_1 = 0.5$ and $p_2 = 0.01$, independent, so $Y = 0.495$. A test that detects only the second fault has $T = 0.5$, and the formula gives $1 - 0.495^{0.5} \approx 0.296$. The true defect level is $p_1 = 0.5$, since a passing chip has no second fault and is bad exactly when it has the first. A test that detects only the first fault has the same $T$ and the same predicted value, but the true defect level is $p_2 = 0.01$. Coverage counts faults, not their probabilities, so the formula can be wrong in both directions.

**Clustered defects.** Suppose the fault probability $p$ varies from chip to chip, as when defects cluster on parts of a wafer, while on each chip the model above holds. Then $Y = \mathbb{E}[(1 - p)^n]$, and the chip passes with probability $\mathbb{E}[(1 - p)^m] = \mathbb{E}[X^T]$ with $X = (1 - p)^n$. The function $x \mapsto x^T$ is concave for $0 \le T \le 1$, so by Jensen's inequality $\mathbb{E}[X^T] \le (\mathbb{E}[X])^T = Y^T$. Hence the true defect level $1 - Y / \mathbb{E}[X^T]$ is at most $1 - Y^{1 - T}$. With clustering, bad chips tend to carry several faults, a test that misses one often catches another, and the formula is an upper bound. Clustered yield models, such as the [negative binomial yield model](/negative-binomial-yield-model/), describe this case.

**Masking.** If a detected fault can be hidden by another fault on the same chip, the chip may pass although it holds a detected fault, and the true defect level is above the model's value.

## History

T. W. Williams and N. C. Brown published the formula in IEEE Transactions on Computers in December 1981, as a short note that tied the fault coverage of a test to the quality of shipped parts. In 1982, Agrawal, Seth and Agrawal gave a model with a distribution of the number of faults on a bad chip. When bad chips carry more than one fault on average, it gives a lower defect level than the Williams-Brown formula for the same coverage, in the same direction as the bound for clustered defects above. Both formulas use the single stuck-at coverage as a stand-in for the probability of catching a defect, and later work on [n-detect tests](/n-detect-test/) and other fault models tries to close the gap between the two.

## References
