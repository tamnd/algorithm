---
tag: 28CQWC
kind: theorem
slug: closed-testing-principle
name: Closed testing principle
aliases:
- closure principle
- Marcus-Peritz-Gabriel closed testing
area: statistics-and-inference/hypothesis-testing
level: advanced
summary: Reject an elementary hypothesis when every intersection hypothesis that contains it is rejected by a level-alpha test. This controls the FWER strongly, and Holm is a case.
prereqs: [family-wise-error-rate, bonferroni-correction, holm-bonferroni-method]
see_also: [hochberg-procedure, westfall-young-procedure, multiple-comparisons-problem, fisher-combined-probability-test, permutation-test, post-selection-inference, benjamini-hochberg-procedure]
sources:
  - paper: doi:10.1093/biomet/63.3.655
    title: Ruth Marcus, Eric Peritz and K. R. Gabriel, On closed testing procedures with special reference to ordered analysis of variance, Biometrika 63(3) (1976), pages 655 to 660
    locator: the definition of a closed testing procedure and the theorem that it controls the family-wise error rate strongly
  - paper: doi:10.1002/bimj.200810462
    title: Eckart Sonnemann, General solutions to multiple testing problems, Biometrical Journal 50(5) (2008), pages 641 to 656
    locator: English translation of the 1982 paper; every coherent multiple test with strong control of the family-wise error rate is a closed test
  - paper: doi:10.1093/biomet/75.2.383
    title: G. Hommel, A stagewise rejective multiple test procedure based on a modified Bonferroni test, Biometrika 75(2) (1988), pages 383 to 386
    locator: closed testing with Simes local tests
  - paper: doi:10.1214/11-STS356
    title: Jelle J. Goeman and Aldo Solari, Multiple testing for exploratory research, Statistical Science 26(4) (2011), pages 584 to 597
    locator: closed testing gives simultaneous confidence bounds for the number of false hypotheses in every set
  - book: isbn:9780387988641
    title: E. L. Lehmann and Joseph P. Romano, Testing Statistical Hypotheses, third edition, Springer, 2005
    locator: Chapter 9 (multiple testing; the closure method and its strong control of the family-wise error rate)
---

The closed testing principle turns tests of intersection hypotheses into a multiple testing procedure with strong control of the [family-wise error rate](/family-wise-error-rate/). For hypotheses $H_1, \dots, H_m$ and each nonempty set $I$ of indices, let $H_I$ be the hypothesis that every $H_i$ with $i \in I$ is true, and let $\phi_I$ be any test of $H_I$ at level $\alpha$, called a local test. The closed procedure rejects $H_i$ when every $H_I$ with $i \in I$ is rejected by its local test. Marcus, Peritz and Gabriel (1976) proved that this controls the family-wise error rate at $\alpha$ under every configuration of true nulls, with no condition on the dependence. The proof takes two lines. The principle is a recipe: [Holm's method](/holm-bonferroni-method/) is closed testing with Bonferroni local tests, Hommel's method is closed testing with Simes local tests, and the converse also holds, since every procedure with strong control is closed testing for some choice of local tests.

## Statement

**Setting.** A model is a set $\mathcal P$ of distributions for the data $X$. Each elementary hypothesis $H_i$, $i = 1, \dots, m$, is a subset of $\mathcal P$. For a distribution $P \in \mathcal P$, the set of true nulls is $I_0(P) = \{i : P \in H_i\}$. For each nonempty $I \subseteq \{1, \dots, m\}$, the intersection hypothesis is $H_I = \bigcap_{i \in I}H_i$, so $P \in H_I$ exactly when $I \subseteq I_0(P)$. A local test $\phi_I$ is a function of $X$ with values in $\{0, 1\}$, where 1 means "reject $H_I$".

**Closed procedure.** For each nonempty $I$, the closed procedure rejects $H_I$ when $\phi_J = 1$ for every $J \supseteq I$. In particular it rejects the elementary $H_i$ when $\phi_J = 1$ for every $J \ni i$.

**Theorem (Marcus, Peritz and Gabriel, 1976).** Fix $0 \le \alpha \le 1$ and assume:
1. for every nonempty $I$ and every $P \in H_I$, $P(\phi_I = 1) \le \alpha$; that is, each local test has level $\alpha$ for its own intersection hypothesis;
2. if some $H_I$ is empty (the nulls in $I$ cannot all be true together), $\phi_I$ may be any test, for example $\phi_I = 1$.

Nothing is assumed about the joint law of the local tests. Then, for every $P \in \mathcal P$ with $I_0(P)$ nonempty,
$$P\big(\text{the closed procedure rejects } H_I \text{ for some nonempty } I \subseteq I_0(P)\big) \le \alpha.$$
In particular the probability that it rejects at least one true elementary null is at most $\alpha$: the family-wise error rate is controlled strongly, and the same holds for all intersection hypotheses at once.

**Theorem (completeness, after Sonnemann).** Let $R$ be any procedure that rejects a random set of elementary hypotheses and controls the family-wise error rate strongly at $\alpha$. Define $\psi_I = 1$ when $R$ rejects some $H_i$ with $i \in I$. Then each $\psi_I$ has level $\alpha$ for $H_I$, and the closed procedure built from the local tests $\psi_I$ rejects exactly the elementary hypotheses that $R$ rejects.

## In plain words

Suppose you want to claim that some specific effects are real, and you want a small chance of making even one false claim. Closed testing says: before you claim an effect, check every group of hypotheses that includes it, and for each group, run a test of "everything in this group is null". Claim the effect only if every one of those group tests says no. If some claims are false, the false ones form a group of their own, and that group of true nulls must have been rejected for any of them to be claimed. That happens with probability at most the level, so the whole set of claims is safe. Any group test with the right level works, which makes the rule a general way to build methods.

## Proof

**Strong control.** Fix $P$ and write $I_0 = I_0(P)$, which is nonempty. Suppose the closed procedure rejects $H_I$ for some nonempty $I \subseteq I_0$. By the definition of the closed procedure, $\phi_J = 1$ for every $J \supseteq I$, and $I_0$ is such a $J$. So the event in the theorem is contained in the event $\{\phi_{I_0} = 1\}$. Since $I \subseteq I_0$ means $P \in H_{I_0}$, condition 1 gives $P(\phi_{I_0} = 1) \le \alpha$. Hence the probability in the theorem is at most $\alpha$. A false rejection of an elementary $H_i$ is the case $I = \{i\}$ with $i \in I_0$. $\square$

The proof never looks at the local tests other than $\phi_{I_0}$, and it uses no independence: all other tests may depend on each other and on $\phi_{I_0}$ in any way. The set $I_0$ is unknown to the analyst, which is why every intersection must be tested.

**Completeness.** Fix a nonempty $I$ and $P \in H_I$, so $I \subseteq I_0(P)$. If $\psi_I = 1$, then $R$ rejects some $H_i$ with $i \in I \subseteq I_0(P)$, which is a false rejection. So $P(\psi_I = 1) \le P(R \text{ rejects a true null}) \le \alpha$ by the strong control of $R$, and $\psi_I$ has level $\alpha$. Now compare the rejections. If $R$ rejects $H_i$, then every $J \ni i$ has $\psi_J = 1$, witnessed by $i$ itself, so the closed procedure rejects $H_i$. If the closed procedure rejects $H_i$, then in particular $\psi_{\{i\}} = 1$, which means that $R$ rejects $H_i$. $\square$

Sonnemann (1982; English translation 2008) proved the stronger form of this result for procedures that also decide on intersection hypotheses and are coherent, which means that rejecting $H_I$ implies rejecting every $H_J$ with $J \supseteq I$. The short argument above covers procedures that decide only on the elementary hypotheses.

**Holm as a case.** With the Bonferroni local test, "$\phi_I = 1$ when $|I|\min_{i \in I}p_i \le \alpha$", each $\phi_I$ has level $\alpha$ by the union bound. Sort the p-values, $p_{(1)} \le \dots \le p_{(m)}$. For $I \ni (k)$, let $j \le k$ be the smallest rank in $I$; then $|I| \le m - j + 1$ and $\min_I p = p_{(j)}$, so $\phi_I = 1$ whenever $(m - j + 1)p_{(j)} \le \alpha$. The tail $\{(j), \dots, (m)\}$ attains this bound. So the closed procedure rejects $H_{(k)}$ exactly when $(m - j + 1)p_{(j)} \le \alpha$ for all $j \le k$, which is Holm's step-down rule. The [Holm-Bonferroni method](/holm-bonferroni-method/) page proves this equivalence in full, including the adjusted p-values.

## Consequences

**A worked closure.** Take $m = 3$, $p = (0.01, 0.04, 0.03)$ and $\alpha = 0.05$. The table lists all seven intersections, with the Bonferroni local test, $|I|\min_I p \le 0.05$, and the Simes local test, $p_{(j:I)} \le j \cdot 0.05/|I|$ for some $j$.

| $I$ | $\lvert I\rvert\min_I p$ | Bonferroni | sorted p-values in $I$ | Simes |
|---|---|---|---|---|
| {1} | 0.01 | reject | 0.01 | reject |
| {2} | 0.04 | reject | 0.04 | reject |
| {3} | 0.03 | reject | 0.03 | reject |
| {1, 2} | 0.02 | reject | 0.01, 0.04 | reject |
| {1, 3} | 0.02 | reject | 0.01, 0.03 | reject |
| {2, 3} | 0.06 | accept | 0.03, 0.04 | reject, since $0.04 \le 0.05$ |
| {1, 2, 3} | 0.03 | reject | 0.01, 0.03, 0.04 | reject |

With Bonferroni local tests, $H_1$ is rejected, since all four sets that contain 1 are rejected, while $H_2$ and $H_3$ are not, because {2, 3} is accepted. That is Holm's answer: $0.01 \le 0.05/3$, then $0.03 > 0.05/2$. With Simes local tests every intersection is rejected, so all three hypotheses are rejected; this is Hommel's method, and [Hochberg's](/hochberg-procedure/) step-up rule gives the same answer here, since $0.04 \le 0.05/1$.

**Procedures that are closed tests.** Each choice of local test gives a procedure with strong control, as long as the local tests have level $\alpha$:
- Bonferroni local tests give [Holm's method](/holm-bonferroni-method/), valid under any dependence. Weighted Bonferroni local tests give weighted Holm and the graphical procedures used for ordered end points in clinical trials.
- Simes local tests give Hommel's method, valid when the Simes inequality holds. [Hochberg's procedure](/hochberg-procedure/) rejects a subset of what Hommel's method rejects.
- Tests of the maximum statistic over $I$, calibrated by permutation, give the step-down maxT method of [Westfall and Young](/westfall-young-procedure/) when subset pivotality holds.
- [Fisher's method](/fisher-combined-probability-test/) on the p-values in $I$ gives a closed procedure that has good power when many effects are weak, but it has no fast shortcut in general.
- The local test "$p_{\min I} \le \alpha$", where $\min I$ is the smallest index in $I$, gives the fixed-sequence procedure: test $H_1, H_2, \dots$ in a fixed order, each at the full level $\alpha$, and stop at the first acceptance. Here $H_i$ is rejected exactly when $p_1, \dots, p_i$ are all at most $\alpha$.

**Shortcuts and consonance.** The closed procedure needs $2^m - 1$ local tests, which is too many beyond $m \approx 25$. A shortcut computes the same elementary rejections in polynomial time, as the sort in Holm's method does. A family of local tests is consonant when, whenever the closed procedure rejects $H_I$, it also rejects some elementary $H_i$ with $i \in I$. Bonferroni and maxT local tests are consonant, and their closures have step-down shortcuts with $m$ steps. Simes and Fisher local tests are not consonant: the closure can reject an intersection without rejecting any of its members, which is information about the set but not about a single hypothesis.

**Statements about sets.** Because the closed procedure controls the error for all intersections at once, it supports simultaneous statements such as "at least $k$ of the hypotheses in $S$ are false", for every set $S$ chosen after looking at the data. Goeman and Solari (2011) turned this into confidence bounds for the number of true discoveries in any set, which gives a link between error rates of the [FWER](/family-wise-error-rate/) kind and the selection questions of [post-selection inference](/post-selection-inference/).

**Adjusted p-values.** If each local test comes from a p-value $p_I$, rejecting when $p_I \le \alpha$, then the closed adjusted p-value of $H_i$ is $\max_{I \ni i}p_I$, and the closed procedure at level $\alpha$ rejects $H_i$ exactly when it is at most $\alpha$. For Bonferroni local tests this is Holm's adjusted p-value.

## Tightness

The level cannot be improved in general. With $m = 1$ the closed procedure is the local test itself, so its error rate equals the size of $\phi_{\{1\}}$, which can be exactly $\alpha$. For larger $m$, Holm's method, a closed procedure, has error rate exactly $\alpha$ under the law in which the $m$ null p-values are $(U + i/m) \bmod 1$ for one uniform $U$ and all hypotheses are true; the events $\{p_i \le \alpha/m\}$ are then disjoint, and the first step of Holm rejects with probability $m \cdot \alpha/m$.

Each condition is needed. If a local test has size $\alpha' > \alpha$, the guarantee fails: with $m = 1$ the closure is that test, with error rate $\alpha'$. If the closure step is dropped and each $H_i$ is tested only by its own $\phi_{\{i\}}$ at level $\alpha$, the error rate under the global null with independent tests is $1 - (1 - \alpha)^m$, which is 0.40 for $m = 10$ and $\alpha = 0.05$. The theorem controls the family-wise error rate only; it says nothing about the [false discovery rate](/false-discovery-rate/) beyond the bound FDR $\le$ FWER, and procedures that control the FDR, such as [Benjamini-Hochberg](/benjamini-hochberg-procedure/), are not closed tests at level $\alpha$.

## History

Marcus, Peritz and Gabriel introduced closed testing in 1976, for comparisons of ordered means in the analysis of variance, building on Gabriel's earlier work on simultaneous test procedures and coherence. Holm (1979) gave his step-down method as a simple sequentially rejective test, and it was soon recognized as the closure of Bonferroni tests. Sonnemann (1982) proved that every coherent multiple test with strong control is a closed test, a result that became widely known through its English translation in 2008. Hommel (1988) gave the closure of the Simes test, and Hochberg (1988) a step-up shortcut that is a little more conservative. Romano and Wolf (2005) connected closed testing with resampling step-down methods, and Goeman and Solari (2011) used it to give simultaneous bounds on the number of false hypotheses in every set.

## References
