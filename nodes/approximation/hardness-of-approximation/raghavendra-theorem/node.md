---
tag: 7X63ZF
kind: theorem
slug: raghavendra-theorem
name: Raghavendra's theorem
aliases:
- optimal CSP approximation under UGC
- Raghavendra's optimal algorithms theorem
- basic SDP optimality for CSPs
area: approximation/hardness-of-approximation
level: research
summary: For every Max-CSP, the integrality gap of the basic SDP equals the best ratio of any polynomial-time algorithm if the UGC holds, and a generic rounding of that SDP reaches it.
prereqs: [unique-games-conjecture, maximum-csp, semidefinite-programming, integrality-gap, dictatorship-test]
see_also: [max-cut-ugc-hardness, approximation-resistance, constraint-satisfaction-problem, boolean-constraint-satisfaction, max-2-sat, fourier-analysis-of-boolean-functions, approximation-threshold]
sources:
  - paper: doi:10.1145/1374376.1374414
    title: Prasad Raghavendra, Optimal algorithms and inapproximability results for every CSP?, Proceedings of the 40th ACM Symposium on Theory of Computing (STOC), 245 to 254, 2008
    locator: the main theorem (UG-hardness at the integrality gap of the basic SDP, and the matching rounding algorithm) and the conversion of integrality gaps into dictatorship tests
  - paper: "Prasad Raghavendra and David Steurer, How to round any CSP, Proceedings of the 50th IEEE Symposium on Foundations of Computer Science (FOCS), 2009"
    locator: the simpler rounding scheme that reaches the integrality gap, and the computation of the optimal ratio to any accuracy
  - paper: doi:10.4007/annals.2010.171.295
    title: Elchanan Mossel, Ryan O'Donnell and Krzysztof Oleszkiewicz, Noise stability of functions with low influences, invariance and optimality, Annals of Mathematics 171(1), 295 to 341, 2010
    locator: the invariance principle that the soundness analysis uses
  - book: isbn:9781107038325
    title: Ryan O'Donnell, Analysis of Boolean Functions, Cambridge University Press, 2014
    locator: Section 7.4 (Theorem 7.40, from Dictator-vs.-No-Notables tests to UG-hardness) and Section 11.7 (the max cut case, Theorems 11.72 and 11.74 and Example 11.73)
---

Raghavendra's theorem (2008) says that for every maximization [constraint satisfaction problem](/maximum-csp/) with a finite domain and predicates of bounded arity, one simple [semidefinite program](/semidefinite-programming/), the *basic SDP*, decides the best possible approximation. If the [Unique Games Conjecture](/unique-games-conjecture/) holds, no polynomial-time algorithm beats the [integrality gap](/integrality-gap/) of the basic SDP by any constant, and a generic rounding of that SDP reaches the gap up to any constant. So for every CSP the optimal approximation ratio under the UGC is the integrality gap of one fixed relaxation. Max cut, where the result recovers the [Goemans-Williamson constant](/max-cut-ugc-hardness/), is the first special case.

## Statement

On this page a maximization ratio means $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$. A *CSP* $\Lambda$ is a finite domain $[q]$ and a finite set of predicates $P : [q]^{r} \to \{0, 1\}$ with $r \le R$. An instance $\mathcal{I}$ is a weighted list of constraints, each a predicate of $\Lambda$ applied to a tuple of variables, and $\operatorname{OPT}(\mathcal{I})$ is the largest weight of satisfied constraints, with total weight $1$.

**The basic SDP.** For each variable $v$ and value $a \in [q]$ there is a vector $\mathbf{b}_{v,a}$, and for each constraint $C$ on a tuple $S_C$ there is a probability distribution $\mu_C$ on $[q]^{S_C}$. The constraints are

$$\langle \mathbf{b}_{v,a}, \mathbf{b}_{w,b} \rangle = \Pr_{x \sim \mu_C}[x_v = a,\ x_w = b] \quad \text{for all } C, \text{ all } v, w \in S_C, \text{ all } a, b \in [q],$$

and the objective is to maximize $\operatorname{SDP}(\mathcal{I}) = \mathbb{E}_C \Pr_{x \sim \mu_C}[C(x) = 1]$. Each assignment gives a feasible solution with one-hot vectors and point distributions, so $\operatorname{SDP}(\mathcal{I}) \ge \operatorname{OPT}(\mathcal{I})$.

**The integrality gap curve.** For $c \in [0, 1]$ let

$$S_\Lambda(c) = \inf \{ \operatorname{OPT}(\mathcal{I}) : \mathcal{I} \text{ an instance of } \Lambda \text{ with } \operatorname{SDP}(\mathcal{I}) \ge c \} .$$

**Theorem (Raghavendra 2008).** Let $\Lambda$ be a CSP, $c \in (0, 1]$ and $\eta > 0$.

1. *Hardness.* If the UGC holds, it is NP-hard to tell instances with $\operatorname{OPT} \ge c - \eta$ from instances with $\operatorname{OPT} \le S_\Lambda(c) + \eta$.
2. *Algorithm.* There is a polynomial-time algorithm that, on every instance with $\operatorname{SDP}(\mathcal{I}) \ge c$, outputs an assignment of value at least $S_\Lambda(c - \eta) - \eta$.

**Corollary.** Let $\alpha_\Lambda = \inf_{c > 0} S_\Lambda(c)/c$, the integrality gap of the basic SDP as a ratio. For every $\eta > 0$ there is a polynomial-time $(\alpha_\Lambda - \eta)$-approximation for $\Lambda$, and if the UGC holds, a polynomial-time $(\alpha_\Lambda + \eta)$-approximation exists only if P = NP.

The exact quantifiers in Raghavendra's paper differ slightly, for example in where the $\eta$ terms sit and in the running time, which is polynomial in the instance size for fixed $\Lambda$ and $\eta$.

## In plain words

A constraint problem asks to set many unknowns so that as many local rules as possible hold. There is one standard way to relax such a problem: replace each unknown by a set of arrows in a high-dimensional space and ask only that the arrows look right in pairs. This relaxed problem can be solved fast. On some inputs, the relaxed answer is much better than any real answer, and the worst such gap is a number fixed by the problem. The theorem says that this number is the whole story. A general method turns the arrows into a real answer that is almost as good as the gap allows. And if a well-known guess about unique games holds, then no fast method can do better than that number, for any problem of this kind.

## Proof

This section gives a sketch, not a full proof. The cited inputs are the invariance principle of Mossel, O'Donnell and Oleszkiewicz and the composition of a dictatorship test with a unique game (O'Donnell, Theorem 7.40, which extends to larger domains).

**From gaps to tests.** Take an instance $\mathcal{I}$ with $\operatorname{SDP}(\mathcal{I}) \ge c$ and $\operatorname{OPT}(\mathcal{I}) \le S_\Lambda(c) + \eta$. Build a [dictatorship test](/dictatorship-test/) on functions $F : [q]^n \to [q]$, one for each variable of $\mathcal{I}$, that does the following. Pick a constraint $C$ of $\mathcal{I}$, pick $n$ independent samples from the local distribution $\mu_C$, which gives one string in $[q]^n$ for each variable of $C$, add a little noise, and check $C$ on the values of the functions at these strings.

- *Completeness.* If every function is the same dictator $F(x) = x_i$, the test sees one sample from $\mu_C$ and accepts with probability $\Pr_{\mu_C}[C = 1]$ up to the noise. On average this is $\operatorname{SDP}(\mathcal{I}) \ge c$, less $O(\eta)$.
- *Soundness.* If the functions have small low-degree influences, the invariance principle says that their behavior on these correlated strings is close to their behavior on correlated Gaussian vectors with the same pairwise correlations, which are the inner products of the SDP vectors. A function of Gaussian vectors with those correlations is a rounding of the SDP solution of $\mathcal{I}$, so it satisfies at most $\operatorname{OPT}(\mathcal{I})$ of the weight. So the test accepts with probability at most $S_\Lambda(c) + O(\eta)$.

The test checks one predicate of $\Lambda$ at a time, so the composition with a unique game gives an instance of $\Lambda$, with completeness $c - O(\eta)$ and soundness $S_\Lambda(c) + O(\eta)$. This is part 1.

**From tests to rounding.** The same soundness argument, run on the input instance itself, gives part 2. Round the SDP solution by projecting the vectors onto a few random Gaussian directions and applying a function of small influence to the projections. If every such rounding scheme had value well below $S_\Lambda(c - \eta)$ on some instance of SDP value $c$, the invariance argument would give that instance an integral value below the gap curve, a contradiction. The family of rounding functions can be replaced by a finite net whose size depends only on $\Lambda$ and $\eta$, and the algorithm tries all of them and keeps the best assignment. Raghavendra and Steurer (2009) give a simpler rounding with the same guarantee.

## Consequences

- **Max cut.** For max cut the basic SDP is the Goemans-Williamson SDP. Its gap curve is $S(\tfrac12 - \tfrac12\cos\theta) = \theta/\pi$ for $\theta$ from about $0.742\pi$ to $\pi$, where the lower bound is the Goemans-Williamson analysis (O'Donnell, Theorem 11.72) and the upper bound comes from known gap instances, and $\alpha = \alpha_{\mathrm{GW}} \approx 0.87856$. So the theorem contains the [UG-hardness of max cut](/max-cut-ugc-hardness/). Two small instances show points on the curve. On the triangle, vectors at angle $\tfrac{2\pi}{3}$ give SDP value $\tfrac34$ while the best cut is $\tfrac23$, a ratio of $\tfrac89$. On the 5-cycle, vectors at angle $\tfrac{4\pi}{5}$ give SDP value $\tfrac12 + \tfrac12\cos\tfrac{\pi}{5} \approx 0.9045$ while the best cut is $\tfrac45$, a ratio of about $0.8845$ (O'Donnell, Example 11.73).
- **Approximation resistance.** If $S_\Lambda(1 - \varepsilon)$ tends to the density of the predicate, the fraction of assignments it accepts, as $\varepsilon \to 0$, then random assignment is optimal and $\Lambda$ is [approximation resistant](/approximation-resistance/) under the UGC.
- **Computing the ratio.** Raghavendra and Steurer (2009) show that $\alpha_\Lambda$ can be computed to any accuracy $\eta$ in time that depends only on $\Lambda$ and $\eta$, so the optimal constant of each CSP is computable in this sense, even when no closed form is known.
- **One algorithm for all.** A single rounding procedure, with a net of rounding functions that depends on $\Lambda$, is optimal for every CSP at once if the UGC holds.

## Tightness

**Basic SDP versus stronger relaxations.** If the UGC holds, adding constraints to the SDP, or using any other polynomial-time relaxation, cannot beat the bound by a constant, by part 1. Without the conjecture this is not known, and a stronger relaxation that beats the basic SDP on some CSP would refute the UGC.

**The $\eta$ terms.** Both parts lose an additive $\eta$, and the curve $S_\Lambda$ may jump. The theorem does not decide the behavior exactly at the point $c$, and for satisfiable instances ($c = 1$) the hardness has completeness $1 - \eta$, not $1$. For example, satisfiable 3LIN instances can be solved by [Gaussian elimination](/gaussian-elimination/), while for $c = 1 - \eta$ the problem is hard.

**Running time.** The algorithm is polynomial for fixed $\Lambda$ and $\eta$, but the dependence on $1/\eta$ is very large, because it enumerates a net of rounding functions.

## History

Goemans and Williamson (1995) introduced SDP rounding for max cut. Khot, Kindler, Mossel and O'Donnell (2004) showed that, under the UGC, the Goemans-Williamson constant is optimal, and their proof already turned a dictatorship test into hardness. Raghavendra (STOC 2008) showed that every integrality gap of the basic SDP gives such a test, for every CSP. Raghavendra and Steurer simplified the rounding in 2009.

## References
