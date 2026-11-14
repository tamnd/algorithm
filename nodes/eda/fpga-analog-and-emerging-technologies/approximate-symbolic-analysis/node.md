---
tag: 7FS1DW
kind: technique
slug: approximate-symbolic-analysis
name: Approximate symbolic analysis
aliases:
- simplification before generation
- simplification during generation
area: eda/fpga-analog-and-emerging-technologies
level: advanced
summary: Keeps only the dominant terms of a symbolic network function by pruning the matrix or the term generation under an error bound, so the formula stays readable.
prereqs: [symbolic-circuit-analysis, transfer-function]
see_also: [determinant-decision-diagram, ac-small-signal-analysis, poles-and-zeros, asymptotic-waveform-evaluation, pade-approximation, analog-circuit-sizing]
sources:
  - paper: "Georges Gielen, Herman Walscharts and Willy Sansen, ISAAC: a symbolic simulator for analog integrated circuits, IEEE Journal of Solid-State Circuits 24(6), 1587 to 1597, 1989"
    title: G. Gielen, H. Walscharts and W. Sansen, ISAAC, a symbolic simulator for analog integrated circuits, IEEE Journal of Solid-State Circuits 24(6), 1587 to 1597, December 1989
    locator: the pruning of the expanded network function at a nominal point with a user-given error
  - paper: "Piet Wambacq, Francisco V. Fernandez, Georges Gielen, Willy Sansen and Angel Rodriguez-Vazquez, Efficient symbolic computation of approximated small-signal characteristics of analog integrated circuits, IEEE Journal of Solid-State Circuits 30(3), 327 to 330, 1995"
    title: P. Wambacq, F. V. Fernandez, G. Gielen, W. Sansen and A. Rodriguez-Vazquez, Efficient symbolic computation of approximated small-signal characteristics of analog integrated circuits, IEEE Journal of Solid-State Circuits 30(3), 327 to 330, March 1995
    locator: generation of the terms of each coefficient in decreasing order of size, stopped when the error bound is met
  - paper: "Piet Wambacq, Georges Gielen and Willy Sansen, Symbolic network analysis methods for practical analog integrated circuits: a survey, IEEE Transactions on Circuits and Systems II 45(10), 1331 to 1341, 1998"
    title: P. Wambacq, G. Gielen and W. Sansen, Symbolic network analysis methods for practical analog integrated circuits, a survey, IEEE Transactions on Circuits and Systems II 45(10), 1331 to 1341, October 1998
    locator: the three classes of approximation (before, during and after the generation of the terms) and their error criteria
  - book: isbn:9780792391616
    title: Georges Gielen and Willy Sansen, Symbolic Analysis for Automated Design of Analog Integrated Circuits, Kluwer Academic Publishers, 1991
    locator: the chapter on the approximation of symbolic expressions
---

Approximate symbolic analysis is a technique that returns a short formula for a network function of a circuit, which keeps only the terms that are large at a nominal point of the element values, with a bound on the error at that point. Its topic is symbolic circuit analysis: it is the practical answer to the growth of the exact formula in [symbolic circuit analysis](/symbolic-circuit-analysis/), where the number of terms grows exponentially with the circuit. The pruning can act on the circuit or its matrix before the terms are made, on the search that makes them, or on the full list after it. The short formula is not exact, and its error bound holds only at the nominal point.

## In plain words

An exact formula for the gain of a real amplifier can have thousands of products of part values. Most of them are tiny next to a few big ones. A designer wants only the big ones, because they show what sets the gain.

Pick typical values for all parts. Now each product has a size. Drop the smallest products, as long as what you drop is a small fraction of the whole. The rest is a short formula that is close to the exact one for these values.

You can drop at three moments. Before you build the formula, by removing parts of the circuit that hardly matter. While you build it, by building the big products first and stopping early. After you build it, by sorting the full list and cutting its tail. The last way is simplest, but it needs the full list, which may be too long.

## When it applies

- The circuit is linear or linearized at an operating point, so the network function is a ratio $H = N/D$ of polynomials in $s$ and the element values.
- A nominal value of each element is known, for example from a simulation of the operating point. The approximation is made at this point.
- The user gives an error $\varepsilon$ and an error measure: on each coefficient of each power of $s$, or on $|H(j\omega)|$ and its phase over a band of frequencies.
- The goal is insight or a fast model near the nominal point, not an exact answer for all values.

## The template

Write the numerator and the denominator by powers of $s$: $N = \sum_k a_k s^k$ and $D = \sum_k b_k s^k$, where each coefficient is a sum of terms, $a_k = \sum_{t \in T_k} t$, and each term is a signed product of element values. At the nominal point, each term has a number.

1. **Choose the error measure.** The usual measure on coefficients asks, for each $k$, that the kept part $\hat a_k$ satisfy $|a_k - \hat a_k| \le \varepsilon \, |a_k|$ at the nominal point.
2. **Simplify before generation (SBG).** Remove elements of the circuit, or entries of the matrix, whose effect on $H$ at the nominal point, over the band of interest, is below a part of the budget. The check uses numeric analysis of the full and the reduced circuit. Then expand the smaller problem.
3. **Simplify during generation (SDG).** For each coefficient, generate its terms in decreasing order of size, and stop as soon as the kept terms meet the bound. This needs a generator that gives the terms in that order, and a way to bound the part not yet generated (Wambacq et al. 1995).
4. **Simplify after generation (SAG).** Generate all terms of each coefficient, sort them by size, and drop the smallest while the dropped total stays within the bound. ISAAC used this step (Gielen, Walscharts and Sansen 1989).
5. **Check.** Evaluate $\hat H(j\omega)$ against a numeric AC analysis over the band, because a bound on the coefficients is not a bound on $H$.

**Two facts about step 4.**

*Fact 1 (same signs).* Let all terms of $a_k$ have the same sign, and let $R$ be the dropped set. Then $|a_k - \hat a_k| = \sum_{t \in R} |t|$ and $|a_k| = \sum_{t \in T_k} |t|$. So the rule "drop while $\sum_{t \in R} |t| \le \varepsilon \sum_{t \in T_k} |t|$" meets the bound. If the signs are mixed, $|a_k|$ can be much less than $\sum |t|$, because large terms cancel. Then the same rule can give a large relative error, and the test must use $|a_k|$ with the signs.

*Fact 2 (smallest first is best in the count).* Under the budget $\sum_{t \in R} |t| \le B$, dropping the terms in increasing order of size, until the next one does not fit, drops the largest possible number of terms. Proof: let the sizes be $u_1 \le u_2 \le \cdots$, and let the greedy rule drop the first $g$ of them. Any set of $g + 1$ terms has a total of at least $u_1 + \cdots + u_{g+1}$, because the $i$-th smallest member of the set is at least $u_i$. The greedy rule stopped because $u_1 + \cdots + u_{g+1} > B$. So no set of more than $g$ terms fits in the budget.

## Classic examples

**A two-node amplifier.** The common-source stage of [symbolic circuit analysis](/symbolic-circuit-analysis/) has

$$H(s) = \frac{-(g_m - s C_f)}{G_1 G_L + s \, (C_f G_1 + C_f G_L + C_f g_m)}.$$

At the nominal point $G_1 = 100\ \mu\mathrm{S}$, $G_L = 10\ \mu\mathrm{S}$, $g_m = 1\ \mathrm{mS}$ and $C_f = 1\ \mathrm{pF}$, the three terms of the coefficient of $s$ are $10^{-16}$, $10^{-17}$ and $10^{-15}$, with the sum $1.11 \times 10^{-15}$. With $\varepsilon = 0.1$, step 4 drops $C_f G_L$ (0.9 percent of the sum) and then $C_f G_1$ (9.9 percent together). The result is

$$\hat H(s) = \frac{-(g_m - s C_f)}{G_1 G_L + s \, C_f g_m},$$

the textbook Miller approximation, with the pole at $-G_1 G_L / (C_f g_m)$.

**The error moves to the pole.** For a denominator $b_0 + b_1 s$, the pole is $-b_0 / b_1$. If the approximation keeps $b_0$ and drops a fraction $\delta$ of $b_1$, the pole moves by the factor $1/(1 - \delta)$, a relative error of $\delta / (1 - \delta)$. In the example, $\delta = 0.099$, so the approximate pole $-1.0 \times 10^6$ rad/s is 11 percent away from the exact $-9.009 \times 10^5$ rad/s, more than the 10 percent bound on the coefficient.

**ISAAC.** The program of Gielen, Walscharts and Sansen made the full expanded network function of a small-signal circuit, and then pruned it at the nominal point with a user error, as in step 4.

**Generation in order of size.** Wambacq, Fernandez, Gielen, Sansen and Rodriguez-Vazquez generated the terms of each coefficient in decreasing order of size, so the expansion stops after the dominant terms, as in step 3. This makes circuits possible whose full expansion does not fit in memory.

**Shortest paths on a DDD.** In a [determinant decision diagram](/determinant-decision-diagram/), each term is a path. Give each hi edge out of a vertex the length $-\log |a_v|$ at the nominal point and each lo edge the length 0. Then a shortest path is a largest term, and the $k$ shortest paths of the acyclic graph are the $k$ largest terms. This is one way to get the order of step 3.

## Variations

- **Error on the response.** Bound $|H(j\omega) - \hat H(j\omega)|$ relative to $|H(j\omega)|$, and the phase error, on a grid of frequencies in a band. This is closer to what a designer needs, but it needs numeric evaluation at each step.
- **Pole and zero approximation.** Approximate each pole and zero separately, for example by the dominant-pole rule that splits widely spaced poles, and give each a short formula.
- **A range of nominal points.** Prune only the terms that are small at all points of a box of element values, so the result holds over the box.
- **Combined steps.** A tool can use SBG to remove the obvious parts, SDG to generate, and a final SAG pass.

## Pitfalls

- **Only at the nominal point.** The kept terms depend on the values. A new bias point can make a dropped term dominant. A formula from this technique is a local model.
- **Cancellation.** Two large terms of opposite sign can cancel. A rule based on term sizes then keeps them both, or drops one and makes a large error. Use the signed value of the coefficient in the test (Fact 1).
- **Coefficient error is not response error.** A small error on each coefficient can give a larger error on a pole or zero, as the example shows, and a large error on $|H(j\omega)|$ near a pole. Check the response.
- **Symbolic matching.** Setting matched devices equal ($g_{m1} = g_{m2}$) merges terms and changes their sizes. Do it before pruning, and say so.
- **Wrong nominal values.** The values must come from the real operating point. Values from a hand estimate give a formula for a different circuit.

## Exercises

1. For the amplifier above, find the largest $\varepsilon$ for which step 4 keeps all three terms of the coefficient of $s$. (Any $\varepsilon < 10^{-17} / (1.11 \times 10^{-15}) \approx 0.009$.)
2. Prove that, among all sets of $g$ terms, the set that the greedy rule of Fact 2 drops has the smallest total. Why is this the set with the smallest error when all terms have one sign?
3. The two-node ladder has $D = y_1 y_2 + y_1 g + y_2 g$. At $y_1 = y_2 = 1$ and $g = 0.01$, which terms does step 4 drop for $\varepsilon = 0.05$? What does the result say about the coupling of the two nodes? (It drops both terms with $g$, which have the total 0.02 out of 1.02, about 2 percent; the two nodes then look independent.)
4. Give a coefficient with three terms of mixed signs for which dropping a term of 1 percent of $\sum |t|$ gives a relative error of more than 50 percent.

## References
