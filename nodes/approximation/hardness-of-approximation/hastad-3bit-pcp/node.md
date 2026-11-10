---
tag: BM7PCM
kind: theorem
slug: hastad-3bit-pcp
name: Håstad's 3-bit PCP
aliases:
- Håstad 3-bit PCP theorem
- Håstad's 3-query PCP
- optimal inapproximability of Max 3LIN
area: approximation/hardness-of-approximation
level: research
summary: NP has PCPs that read 3 bits, check one linear equation, and have completeness 1 - ε and soundness 1/2 + ε; so Max 3LIN within 1/2 + ε and Max 3SAT within 7/8 + ε are NP-hard.
prereqs: [pcp-theorem, label-cover, long-code, dictatorship-test, fourier-analysis-of-boolean-functions]
see_also: [parallel-repetition-theorem, max-3sat-inapproximability, approximation-resistance, linearity-test, two-prover-one-round-game, approximation-threshold, gap-preserving-reduction, random-assignment-max-3-sat]
sources:
  - paper: doi:10.1145/502090.502098
    title: Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48(4), 798 to 859, 2001 (STOC 1997)
    locator: the 3-query PCP with a linear test, the hardness of Max E3LIN and Max E3SAT, and the gadget results for other CSPs
  - book: isbn:9781107038325
    title: Ryan O'Donnell, Analysis of Boolean Functions, Cambridge University Press, 2014
    locator: Section 7.4 (Highlight, Håstad's hardness theorems, Theorems 7.41 and 7.42 and their dictator tests)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 22, Sections 22.4 to 22.7 (Håstad's 3-bit PCP, the Fourier technique, the long code and the proof of the theorem)
  - paper: "Mihir Bellare, Oded Goldreich and Madhu Sudan, Free bits, PCPs, and nonapproximability, towards tight results, SIAM Journal on Computing 27(3), 804 to 915, 1998"
    locator: the long code and its use in PCPs
---

Håstad's 3-bit PCP theorem says that for every $\varepsilon > 0$, every language in NP has a [probabilistically checkable proof](/probabilistically-checkable-proof/) whose verifier uses $O(\log n)$ random bits, reads $3$ bits of the proof, accepts when their sum modulo $2$ equals a fixed bit, accepts some proof of each true statement with probability at least $1 - \varepsilon$, and accepts every proof of a false statement with probability at most $\tfrac12 + \varepsilon$. As a gap result, it is NP-hard to approximate Max 3LIN within $\tfrac12 + \varepsilon$ and [Max 3SAT](/max-3sat-inapproximability/) within $\tfrac78 + \varepsilon$. Both bounds match what a random assignment achieves, so they are tight. Johan Håstad proved the theorem in 1997 by composing [label cover](/label-cover/) with the [long code](/long-code/) and analyzing a [dictatorship test](/dictatorship-test/) by [Fourier analysis](/fourier-analysis-of-boolean-functions/).

## Statement

On this page a maximization ratio means $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$. Max 3LIN is the problem: given a system of linear equations over $\mathbb{F}_2$, each of the form $x_i + x_j + x_k = b$, find an assignment that satisfies as many equations as possible.

**Theorem (Håstad 2001).** For every $\varepsilon \in (0, \tfrac12)$,

$$\mathrm{NP} = \mathrm{PCP}_{1 - \varepsilon,\ 1/2 + \varepsilon}[O(\log n), 3],$$

and the verifier is nonadaptive and accepts exactly when the three bits it reads satisfy one linear equation over $\mathbb{F}_2$. Equivalently, it is NP-hard to tell instances of Max 3LIN in which some assignment satisfies at least a $1 - \varepsilon$ fraction of the equations from instances in which every assignment satisfies at most a $\tfrac12 + \varepsilon$ fraction.

**Corollary (Max 3SAT).** For every $\varepsilon > 0$ it is NP-hard to approximate Max 3SAT within a ratio $\tfrac78 + \varepsilon$.

The inclusion $\supseteq$ holds for every PCP with $O(\log n)$ random bits, by trying all random strings. The content is $\subseteq$.

## In plain words

A proof is written so that a checker can read only three of its symbols, add them, and compare the sum with a fixed value. If the claim is true, an honest proof passes almost every time. If the claim is false, every proof passes only a little more than half of the time, which is what blind guessing already gets. Since each check is a simple sum of three yes or no values, this says that for such systems of sums it is hard even to beat random guessing by a fixed margin. Turning each sum into four short or clauses gives the same message for satisfying clauses with three parts. The proof hides each answer of a hard puzzle inside a huge table and tests that table with a noisy random check.

## Proof

The full argument, from a cited hardness of label cover, is in [proofs/main.md](proofs/main.md). It is a complete proof of the long code part. The outer input, that label cover with value $1$ versus value at most $\gamma$ is NP-hard for every constant $\gamma > 0$, comes from the [PCP theorem](/pcp-theorem/) and the [parallel repetition theorem](/parallel-repetition-theorem/) and is cited.

The verifier picks a random edge $(u, v)$ with projection $\pi : [L] \to [R]$ of the label cover instance. The proof contains a folded table $f_u$ on $\{-1,1\}^L$ for each $u$ and $g_v$ on $\{-1,1\}^R$ for each $v$, which are meant to be the long codes of the labels. The verifier picks $x \in \{-1,1\}^R$ and $y \in \{-1,1\}^L$ uniformly and a noise vector $z$ whose coordinates are $-1$ with probability $\delta$, and accepts when

$$g_v(x) \cdot f_u(y) \cdot f_u((x \circ \pi) \circ y \circ z) = 1, \qquad (x \circ \pi)_i = x_{\pi(i)} .$$

- *Completeness.* Long codes of a satisfying labeling pass with probability $1 - \delta$: the product reduces to the noise bit $z_a$ at the label $a$ of $u$.
- *The exact formula.* For one edge the acceptance probability is $\tfrac12 + \tfrac12 \sum_S \hat g_v(\pi_2(S)) \hat f_u(S)^2 (1 - 2\delta)^{|S|}$, where $\pi_2(S)$ is the set of $j$ with an odd number of preimages in $S$.
- *Decoding.* Pick a label for $u$ by choosing $S$ with probability $\hat f_u(S)^2$ and then a random element of $S$, and a label for $v$ in the same way from $\hat g_v$. Cauchy-Schwarz and $(1-2\delta)^{2|S|} \le 1/(4\delta|S|)$ show that this random labeling satisfies at least a $16 \delta \eta^2$ fraction of the edges when the verifier accepts with probability $\tfrac12 + \eta$.

With $\delta = \eta = \varepsilon$ and label cover soundness $\gamma < 16\varepsilon^3$, the verifier has completeness $1 - \varepsilon$ and soundness below $\tfrac12 + \varepsilon$.

**From 3LIN to 3SAT, in full.** Replace each equation $x + y + z = 1$ by the four clauses $x \vee y \vee z$, $x \vee \bar y \vee \bar z$, $\bar x \vee y \vee \bar z$ and $\bar x \vee \bar y \vee z$. Each clause excludes one of the four assignments with even parity. An assignment that satisfies the equation has odd parity and satisfies all four clauses. One that violates it equals exactly one excluded assignment and satisfies exactly $3$ of the $4$. Equations $x + y + z = 0$ are handled in the same way with the odd assignments excluded. A system of $m$ equations becomes $4m$ clauses. If a $1 - \varepsilon$ fraction of the equations can be satisfied, at least $(4 - \varepsilon) m$ clauses can be. If at most a $\tfrac12 + \varepsilon$ fraction can, at most $(\tfrac72 + \varepsilon) m$ clauses can. The ratio $\frac{7/2 + \varepsilon}{4 - \varepsilon}$ tends to $\tfrac78$ as $\varepsilon \to 0$. For example it is $\tfrac{117}{133} \approx 0.8797$ at $\varepsilon = \tfrac{1}{100}$ and $\tfrac{1167}{1333} \approx 0.8755$ at $\varepsilon = \tfrac{1}{1000}$. $\square$

## Consequences

- **Max 3LIN and Max 3SAT.** The two bounds of the statement. In the terms of the [approximation threshold](/approximation-threshold/) page, the thresholds of Max 3LIN and Max E3SAT are $\tfrac12$ and $\tfrac78$ unless P = NP.
- **Approximation resistance.** Both predicates are [approximation resistant](/approximation-resistance/): no polynomial-time algorithm beats the random assignment by a constant, unless P = NP.
- **Other CSPs by gadgets.** Håstad combines the 3LIN result with gadgets to get NP-hardness of approximating Max Cut within $\tfrac{16}{17} + \varepsilon$ and Max 2SAT within $\tfrac{21}{22} + \varepsilon$. These are not known to be tight. The [UG-hardness of max cut](/max-cut-ugc-hardness/) gives the tight constant under a stronger assumption.
- **PCP parameters.** Three queries and soundness close to $\tfrac12$ is the best possible for nonadaptive verifiers with a linear test, because a random assignment satisfies half of any system of equations.

## Tightness

**Max 3LIN.** A uniformly random assignment satisfies each equation $x_i + x_j + x_k = b$ with probability exactly $\tfrac12$, so it satisfies half of the equations in expectation, and the method of conditional expectations finds such an assignment deterministically. So the soundness $\tfrac12 + \varepsilon$ cannot be lowered to $\tfrac12 - \varepsilon$.

**Max E3SAT.** A random assignment satisfies a clause with three distinct literals with probability $\tfrac78$ ([random assignment for Max 3SAT](/random-assignment-max-3-sat/)), which matches the $\tfrac78 + \varepsilon$ bound.

**Imperfect completeness is needed for 3LIN.** Deciding whether a system of linear equations over $\mathbb{F}_2$ is fully satisfiable takes polynomial time by [Gaussian elimination](/gaussian-elimination/). So the completeness $1 - \varepsilon$ cannot be raised to $1$ unless P = NP. For 3SAT this obstacle does not exist, and Håstad also proves the $\tfrac78 + \varepsilon$ bound for satisfiable instances, with a different test.

## History

Bellare, Goldreich and Sudan introduced the long code (journal version 1998) and used it in PCPs for hardness of approximation. Håstad presented the 3-bit PCP and the tight bounds for Max 3LIN and Max 3SAT at STOC 1997, and the journal version appeared in the Journal of the ACM in 2001. O'Donnell's book gives a short version of the dictatorship part, and Arora and Barak give the full proof from label cover.

## References
