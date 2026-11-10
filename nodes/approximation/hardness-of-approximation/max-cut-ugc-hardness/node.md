---
tag: JSD822
kind: theorem
slug: max-cut-ugc-hardness
name: Max-Cut UGC hardness
aliases:
- UGC hardness of Max-Cut
- KKMO theorem
- optimality of Goemans-Williamson
area: approximation/hardness-of-approximation
level: research
summary: If the Unique Games Conjecture holds, approximating Max-Cut within α_GW + ε ≈ 0.8786 + ε is NP-hard for every ε > 0, so the Goemans-Williamson algorithm is optimal.
prereqs: [unique-games-conjecture, maximum-cut, dictatorship-test, fourier-analysis-of-boolean-functions]
see_also: [raghavendra-theorem, semidefinite-programming, integrality-gap, long-code, hastad-3bit-pcp, approximation-resistance, approximation-threshold]
sources:
  - paper: doi:10.1137/S0097539705447372
    title: Subhash Khot, Guy Kindler, Elchanan Mossel and Ryan O'Donnell, Optimal inapproximability results for MAX-CUT and other 2-variable CSPs?, SIAM Journal on Computing 37(1), 319 to 357, 2007 (FOCS 2004)
    locator: the reduction from unique games to max cut, the noise test, and the hardness curve conditional on Majority Is Stablest
  - paper: doi:10.4007/annals.2010.171.295
    title: Elchanan Mossel, Ryan O'Donnell and Krzysztof Oleszkiewicz, Noise stability of functions with low influences, invariance and optimality, Annals of Mathematics 171(1), 295 to 341, 2010
    locator: the proof of the Majority Is Stablest theorem by the invariance principle
  - book: isbn:9781107038325
    title: Ryan O'Donnell, Analysis of Boolean Functions, Cambridge University Press, 2014
    locator: Section 7.4 (Theorem 7.40, UG-hardness from Dictator-vs.-No-Notables tests) and Section 11.7 (Theorems 11.72 and 11.74, Example 11.73, Remarks 11.75 and 11.76)
  - paper: "Michel X. Goemans and David P. Williamson, Improved approximation algorithms for maximum cut and satisfiability problems using semidefinite programming, Journal of the ACM 42(6), 1115 to 1145, 1995"
    locator: the SDP rounding algorithm and the constant 0.878
  - paper: "Ryan O'Donnell and Yi Wu, An optimal SDP algorithm for Max-Cut, and equally optimal Long Code tests, Proceedings of the 40th ACM Symposium on Theory of Computing (STOC), 2008"
    locator: the full curve of completeness against soundness, including completeness below 0.845
---

Khot, Kindler, Mossel and O'Donnell (KKMO, 2004) proved that if the [Unique Games Conjecture](/unique-games-conjecture/) holds, then for every $\varepsilon > 0$ it is NP-hard to approximate [max cut](/maximum-cut/) within $\alpha_{\mathrm{GW}} + \varepsilon$, where $\alpha_{\mathrm{GW}} \approx 0.87856$ is the ratio of the Goemans-Williamson algorithm. Their proof used the Majority Is Stablest conjecture, which Mossel, O'Donnell and Oleszkiewicz proved in 2005. The core of the proof is a two-query [dictatorship test](/dictatorship-test/) that checks whether a cut of the hypercube is a dictator cut, and the analysis of that test is a statement about noise stability. The result says that a simple [semidefinite program](/semidefinite-programming/) with random hyperplane rounding is the best possible polynomial-time method for max cut, if the conjecture holds.

## Statement

On this page a maximization ratio means $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$. An instance of max cut is a graph with nonnegative edge weights that sum to $1$, and its value is the largest total weight of edges cut by a partition $F : V \to \{-1, 1\}$. "UG-hard" means NP-hard if the Unique Games Conjecture holds.

**Theorem (KKMO 2007, with MOO 2010).** Let $\theta \in (\tfrac{\pi}{2}, \pi)$ and $\delta > 0$. It is UG-hard to tell max cut instances of value at least $\tfrac12 - \tfrac12 \cos\theta$ from instances of value at most $\tfrac{\theta}{\pi} + \delta$.

**Corollary.** For every $\varepsilon > 0$ it is UG-hard to approximate max cut within $\alpha_{\mathrm{GW}} + \varepsilon$, where

$$\alpha_{\mathrm{GW}} = \min_{0 < \theta \le \pi} \frac{\theta / \pi}{\tfrac12 - \tfrac12 \cos\theta} \approx 0.8785672 .$$

The minimum is at $\theta^* \approx 2.33112$ (about $0.742\pi$), the positive solution of $\tan(\theta/2) = \theta$. There the completeness is $\tfrac12 - \tfrac12\cos\theta^* \approx 0.84458$ and the soundness is $\theta^*/\pi \approx 0.74202$. The corollary follows from the theorem with $\theta = \theta^*$ and $\delta$ small, since $\frac{\theta^*/\pi + \delta}{1/2 - (\cos\theta^*)/2} < \alpha_{\mathrm{GW}} + \varepsilon$.

**The matching algorithm (Goemans-Williamson 1995, cited).** For $\theta \in [\theta^*, \pi]$, on every graph whose SDP value is at least $\tfrac12 - \tfrac12\cos\theta$, random hyperplane rounding finds a cut of expected value at least $\theta/\pi$ (O'Donnell, Theorem 11.72). So for these $\theta$ the theorem is tight.

## In plain words

Max cut asks to split the points of a network into two groups so that as many links as possible go between the groups. A known method based on placing points on a sphere and cutting the sphere with a random flat sheet always gets at least about 88 percent of the best answer. This theorem says that, if a well-known guess about a puzzle called unique games is true, then no fast method can promise even a little more than that. The proof builds a test that looks at two nearby, mostly opposite points of a huge cube and checks that a split of the cube puts them in different groups. Splits that follow one direction pass often. Splits that spread their attention over many directions pass less often, and the best of those is the majority vote.

## Proof

The full analysis of the dictatorship test, given the Majority Is Stablest theorem, and a sketch of the composition with unique games, are in [proofs/sketch.md](proofs/sketch.md). The file is marked as a sketch because two inputs are cited and not proved: the Majority Is Stablest theorem, and the general composition step of O'Donnell, Theorem 7.40.

The test for a function $f : \{-1,1\}^n \to \{-1,1\}$, with $\rho = \cos\theta \in (-1, 0)$, picks a uniform $x$ and a $\rho$-correlated $x'$ (flip each bit of $x$ with probability $\tfrac12 - \tfrac12\rho$) and accepts if $f(x) \ne f(x')$. Its acceptance probability is

$$\Pr[\text{accept}] = \tfrac12 - \tfrac12 \operatorname{Stab}_\rho[f] .$$

- *Dictators.* For $f = x_i$ the test accepts exactly when bit $i$ flips, with probability $\tfrac12 - \tfrac12 \cos\theta$.
- *Functions with small influences.* Because $\rho < 0$, the even levels of the Fourier weight only lower the acceptance probability, so $\Pr[\text{accept}] \le \tfrac12 + \tfrac12 \operatorname{Stab}_{-\rho}[f^{\mathrm{odd}}]$, where $f^{\mathrm{odd}}$ keeps the odd levels. The function $f^{\mathrm{odd}}$ has mean $0$ and small influences, and $-\rho = \cos(\pi - \theta) \in (0,1)$, so Majority Is Stablest gives $\operatorname{Stab}_{-\rho}[f^{\mathrm{odd}}] \le 1 - \tfrac{2}{\pi}(\pi - \theta) + o(1) = \tfrac{2\theta}{\pi} - 1 + o(1)$. So the test accepts with probability at most $\tfrac{\theta}{\pi} + o(1)$.

Composition with a unique game puts a [long code](/long-code/) table at each vertex of one side and runs the test on two tables at a time, with the two points permuted by the bijections of the unique game. Each test is one edge of the output graph. Completeness comes from dictators of a good labeling, and soundness decodes a labeling from the coordinates of large low-degree influence.

## Consequences

- **Goemans-Williamson is optimal under the UGC.** No polynomial-time algorithm has ratio $\alpha_{\mathrm{GW}} + \varepsilon$ unless the conjecture fails or P = NP.
- **The whole curve.** For each completeness $\beta = \tfrac12 - \tfrac12\cos\theta \in [0.845, 1)$, the best soundness is $\theta/\pi = \arccos(1 - 2\beta)/\pi$. For example, at $\theta = \tfrac{2\pi}{3}$ the completeness is $\tfrac34$ and the soundness is $\tfrac23$, a ratio of $\tfrac89$. At $\theta = \tfrac{3\pi}{4}$ the completeness is $\tfrac12 + \tfrac{\sqrt2}{4} \approx 0.8536$ and the soundness is $\tfrac34$, a ratio of about $0.8787$ (O'Donnell, Remark 11.76).
- **Near-bipartite graphs.** As $\theta \to \pi$, with completeness $1 - \varepsilon$, the soundness is $1 - \tfrac{2}{\pi}\sqrt{\varepsilon} + O(\varepsilon)$. So on graphs where a cut of weight $1 - \varepsilon$ exists, it is UG-hard to find a cut of weight $1 - c\sqrt{\varepsilon}$ for a suitable constant $c$, and Goemans-Williamson finds a cut of weight $1 - O(\sqrt{\varepsilon})$.
- **Other 2-variable problems.** The same paper gives UG-hardness for Max-2LIN modulo $q$ and related problems. [Raghavendra's theorem](/raghavendra-theorem/) extends the pattern to every CSP: the [integrality gap](/integrality-gap/) of the basic SDP is the UG-hardness threshold.

## Tightness

**Integrality gap of the 5-cycle.** The SDP cannot certify better than $\alpha_{\mathrm{GW}}$ on all graphs, and the 5-cycle shows the pattern at one point. Place vertex $v \in \mathbb{Z}_5$ at the unit vector $(\cos\frac{4\pi v}{5}, \sin\frac{4\pi v}{5})$. Adjacent vertices are at angle $\frac{4\pi}{5}$, so the SDP value is at least $\tfrac12 - \tfrac12\cos\frac{4\pi}{5} = \tfrac12 + \tfrac12\cos\frac{\pi}{5} \approx 0.9045$, while the best cut has value $\tfrac45$. The ratio is about $0.8845$, which equals $\frac{\theta/\pi}{1/2 - (\cos\theta)/2}$ at $\theta = \tfrac{4\pi}{5}$ (O'Donnell, Example 11.73). Feige and Schechtman showed that the gap reaches $\alpha_{\mathrm{GW}}$ in the limit on other graphs.

**Majority attains the bound.** For $\theta = \tfrac{2\pi}{3}$, so $\rho = -\tfrac12$, the test accepts $\mathrm{Maj}_1$, $\mathrm{Maj}_3$ and $\mathrm{Maj}_5$ with probabilities $\tfrac34$, $\tfrac{45}{64} \approx 0.703$ and $\tfrac{2817}{4096} \approx 0.688$, and the limit as $n \to \infty$ is $\tfrac{\theta}{\pi} = \tfrac23$ by Sheppard's formula. So the bound $\theta/\pi$ for functions with small influences cannot be lowered.

**Low completeness.** For $\theta \in (\tfrac{\pi}{2}, \theta^*)$, that is completeness between $\tfrac12$ and about $0.8446$, the hardness of the theorem and the guarantee of plain hyperplane rounding do not match. O'Donnell and Wu (2008) close this gap with a modified rounding and a matching test (O'Donnell, Remark 11.75).

**Without the conjecture.** The best NP-hardness known is Håstad's bound $\tfrac{16}{17} + \varepsilon \approx 0.941$, obtained from the [3-bit PCP](/hastad-3bit-pcp/) with a gadget. The gap between $0.879$ and $0.941$ is open without the UGC.

## History

Goemans and Williamson gave the SDP algorithm in 1994 (journal version 1995). KKMO presented the reduction at FOCS 2004, and stated the hardness conditional on both the Unique Games Conjecture and the Majority Is Stablest conjecture. Mossel, O'Donnell and Oleszkiewicz proved Majority Is Stablest in 2005 by the invariance principle, which reduces it to Borell's isoperimetric theorem in Gaussian space. The journal versions appeared in 2007 and 2010.

## References
