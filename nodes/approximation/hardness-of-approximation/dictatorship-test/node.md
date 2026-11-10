---
tag: J899Z1
kind: concept
slug: dictatorship-test
name: Dictatorship test
aliases:
- dictator test
- dictator-vs-no-notables test
area: approximation/hardness-of-approximation
level: research
summary: A test that reads a Boolean function at a few correlated random points, accepts every dictator with high probability, and accepts functions with no influential coordinate with lower probability.
prereqs: [fourier-analysis-of-boolean-functions, long-code, linearity-test]
see_also: [hastad-3bit-pcp, max-cut-ugc-hardness, unique-games-conjecture, raghavendra-theorem, approximation-resistance, label-cover, maximum-csp]
sources:
  - book: isbn:9781107038325
    title: Ryan O'Donnell, Analysis of Boolean Functions, Cambridge University Press, 2014
    locator: Section 7.1 (dictator testing), Section 7.4 (Definition 7.37 of a Dictator-vs.-No-Notables test, Theorem 7.40 on UG-hardness from such a test, Theorem 7.42 for 3-variable linear equations) and Section 11.7 (the max cut test and Majority Is Stablest)
  - paper: doi:10.1145/502090.502098
    title: Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48(4), 798 to 859, 2001
    locator: the three-query long code test with noise for Max 3LIN and its Fourier analysis
  - paper: doi:10.1137/S0097539705447372
    title: Subhash Khot, Guy Kindler, Elchanan Mossel and Ryan O'Donnell, Optimal inapproximability results for MAX-CUT and other 2-variable CSPs?, SIAM Journal on Computing 37(1), 319 to 357, 2007
    locator: the noise-sensitivity test for max cut and the reduction from unique games
---

A dictatorship test is a randomized procedure that reads a function $f : \{-1,1\}^n \to \{-1,1\}$ at a few correlated random points and accepts or rejects based on a fixed predicate of the values it reads. It accepts each dictator $f(x) = x_i$ with probability at least $c$, and it accepts each function that has no influential coordinate with probability at most $s + o(1)$, where $s < c$. The dictators are the code words of the [long code](/long-code/), so a dictatorship test is a test for that code with $c$ and $s$ as the completeness and soundness. Composed with [label cover](/label-cover/) or [unique games](/unique-games-conjecture/), a test with predicate $P$ gives the hardness of approximating the CSP of $P$ within $s/c$.

## In plain words

A dictator is a function of many yes or no inputs that copies one input and ignores the rest. A dictatorship test is a short random quiz for a function given as a black box. It asks the function a few related questions and checks one simple rule on the answers. Each dictator passes the quiz often. A function that spreads its attention over many inputs, such as a vote of the majority, passes less often. In a hardness proof, each possible answer of a puzzle is hidden inside a dictator. A cheater who does not have a good answer must hand in tables that are not close to dictators, and the quiz catches that. The pass rates of the quiz on the two kinds of functions become the hardness ratio for the problem.

## The idea

**Definition.** Let $P : \{-1,1\}^k \to \{0,1\}$ be a predicate. A *dictatorship test with predicate $P$* picks a random $k$-tuple of points $x^{(1)}, \ldots, x^{(k)} \in \{-1,1\}^n$ from a distribution whose coordinates are independent and identically distributed across $i \in [n]$, and accepts when $P(f(x^{(1)}), \ldots, f(x^{(k)})) = 1$. It has completeness $c$ if every dictator is accepted with probability at least $c$. It has soundness $s$ if for every $\eta > 0$ there are $\varepsilon > 0$ and $d$ such that every $f$ with

$$\operatorname{Inf}_i^{\le d}[f] = \sum_{S \ni i,\ |S| \le d} \hat f(S)^2 \le \varepsilon \quad \text{for all } i$$

is accepted with probability at most $s + \eta$. O'Donnell (Definition 7.37) uses a closely related form with the noisy influences $\sum_{S \ni i} (1-\varepsilon)^{|S|-1} \hat f(S)^2$, writes the pair as $(s, c)$, and calls this a Dictator-vs.-No-Notables test. Some papers ask instead that functions far from every junta be rejected. The low-degree influence form is the one that a [unique games](/unique-games-conjecture/) reduction can decode, because a function with a coordinate of large low-degree influence has only a few such coordinates: there are at most $d/\varepsilon$ of them, since $\sum_i \operatorname{Inf}_i^{\le d}[f] \le d$.

**Why the linearity test is not enough.** The [BLR test](/linearity-test/) accepts every parity $\chi_S$ with probability $1$, and a parity of many coordinates has no coordinate of low-degree influence. Dictatorship tests add noise: they multiply one query by a random vector that flips a few coordinates. A character $\chi_S$ survives the noise with a factor $(1 - 2\delta)^{|S|}$, so large parities fail and only small sets of coordinates keep their weight.

**From a test to hardness.** A reduction from unique games replaces each vertex of the outer instance by a long code table and runs the test across the tables of the two endpoints of a random constraint, with the coordinates permuted by the constraint. If the outer instance has a good labeling, the tables can be the dictators of the labels, and the test accepts with probability about $c$. If the test accepts with probability more than $s + \eta$, then many tables have coordinates of large low-degree influence, and these few coordinates give a labeling that satisfies a constant fraction of the constraints. O'Donnell (Theorem 7.40) states the result: a test with completeness $c$ and soundness $s$ using predicate $P$ makes it UG-hard to tell instances of Max-CSP($P$) with value at least $c - \delta$ from those with value at most $s + \delta$. On this site a maximization ratio means $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$, so the conclusion is UG-hardness of approximation within $s/c + \delta'$.

## Examples

### Håstad's test for three-variable linear equations

**The test.** Fix $\delta \in (0, \tfrac12)$. Pick $x, y$ uniformly and $z$ with independent coordinates, $z_i = -1$ with probability $\delta$. Accept when $f(x) f(y) f(x \circ y \circ z) = 1$, where $\circ$ is the coordinatewise product. The predicate is a linear equation over $\mathbb{F}_2$ on three values.

**Completeness.** For $f = x_i$ the product is $x_i y_i x_i y_i z_i = z_i$, which is $1$ with probability $1 - \delta$.

**The acceptance probability.** It is $\tfrac12 + \tfrac12 \mathbb{E}[f(x) f(y) f(x \circ y \circ z)]$. Expand the last factor. Since $\mathbb{E}[\chi_S(z)] = (1-2\delta)^{|S|}$ and $x$, $y$, $z$ are independent,

$$\mathbb{E}[f(x) f(y) f(x \circ y \circ z)] = \sum_S \hat f(S) \, \mathbb{E}[f(x)\chi_S(x)] \, \mathbb{E}[f(y)\chi_S(y)] \, (1-2\delta)^{|S|} = \sum_S \hat f(S)^3 (1-2\delta)^{|S|} .$$

**Soundness, in full.** Suppose $f$ is folded ($f(-x) = -f(x)$, so $\hat f(S) = 0$ for even $|S|$) and accepted with probability at least $\tfrac12 + \eta$. Then $\sum_S \hat f(S)^3 (1-2\delta)^{|S|} \ge 2\eta$. By Parseval, $\sum_S \hat f(S)^2 = 1$, so some $S$ has $\hat f(S) (1-2\delta)^{|S|} \ge 2\eta$. Both factors are at most $1$, so $\hat f(S) \ge 2\eta$ and $(1-2\delta)^{|S|} \ge 2\eta$. Since $\ln(1 - 2\delta) \le -2\delta$, the second gives $|S| \le \ln(1/(2\eta)) / (2\delta)$. The set $S$ is nonempty because it has odd size. So each $i \in S$ has $\operatorname{Inf}_i^{\le d}[f] \ge \hat f(S)^2 \ge 4\eta^2$ with $d = \ln(1/(2\eta))/(2\delta)$. So a folded $f$ whose low-degree influences with this $d$ are all below $4\eta^2$ passes with probability less than $\tfrac12 + \eta$: completeness $1 - \delta$ and soundness $\tfrac12$ on folded functions. $\square$

**Folding matters.** The constant function $1$ passes this test with probability $1 - \delta$ and has no influential coordinate, so the soundness holds only for folded functions. A reduction reads the tables in folded form, as on the [long code](/long-code/) page. O'Donnell's version of the test (proof of Theorem 7.42) builds the folding into the test: it multiplies $x \circ y$ by a random sign $b$ and accepts when the product of the three values is $b$, which gives completeness $1 - \delta/2$ for a noise rate $\delta$ in his parametrization, and soundness $\tfrac12$ for all functions.

**Numbers for $n = 3$ and $\delta = \tfrac{1}{10}$.** A dictator passes with probability $\tfrac{9}{10}$. The parity $x_1 x_2 x_3$ passes with $\tfrac12 + \tfrac12 (0.8)^3 = \tfrac{189}{250} = 0.756$, and $\operatorname{Maj}_3$ passes with $\tfrac12 + \tfrac12 (3 \cdot \tfrac18 \cdot 0.8 - \tfrac18 \cdot 0.512) = \tfrac{309}{500} = 0.618$. For large $n$, majority passes with probability close to $\tfrac12$, since $\sum_S |\hat f(S)|^3 \le \max_S |\hat f(S)|$ and every coefficient of $\operatorname{Maj}_n$ tends to $0$.

The NP-hardness proof of [Håstad's 3-bit PCP](/hastad-3bit-pcp/) uses a two-table version of this test across a projection constraint, with the same decoding step.

### The noise test for max cut

**The test.** Fix $\rho \in (-1, 0)$. Pick $x$ uniformly and a $\rho$-correlated copy $y$ (each $y_i = x_i$ with probability $\tfrac{1+\rho}{2}$, else $-x_i$). Accept when $f(x) \ne f(y)$. The predicate is the cut predicate on two values.

**Acceptance.** By the noise stability formula, the test accepts with probability $\tfrac12 - \tfrac12 \sum_S \rho^{|S|} \hat f(S)^2$. A dictator passes with probability $\tfrac{1-\rho}{2}$.

**Soundness (cited).** For a function with no coordinate of large low-degree influence the acceptance is at most $\tfrac{1}{\pi}\arccos \rho + o(1)$. This is the Majority Is Stablest theorem of Mossel, O'Donnell and Oleszkiewicz, applied to the odd part of $f$, and is proved on the [max cut UGC hardness](/max-cut-ugc-hardness/) page from that theorem. Majority shows that the bound is tight.

**Numbers at $\rho = -\tfrac12$.** A dictator passes with probability $\tfrac34$. $\operatorname{Maj}_3$ passes with $\tfrac{45}{64} \approx 0.703$, $\operatorname{Maj}_5$ with $\tfrac{2817}{4096} \approx 0.688$, and large majorities tend to $\tfrac1\pi \arccos(-\tfrac12) = \tfrac23$. The ratio $\tfrac{2/3}{3/4} = \tfrac89$ is one point of the curve whose minimum over $\rho$ is the Goemans-Williamson constant $0.878567$.

## Where it is used

- **Tight NP-hardness.** Håstad's tests with long codes and [label cover](/label-cover/) give $\tfrac12 + \varepsilon$ for Max 3LIN and $\tfrac78 + \varepsilon$ for [Max 3SAT](/max-3sat-inapproximability/) ([Håstad's 3-bit PCP](/hastad-3bit-pcp/)).
- **UG-hardness of 2-variable CSPs.** The noise test gives the optimality of $\alpha_{\mathrm{GW}}$ for [max cut](/max-cut-ugc-hardness/) under the UGC. A test with the vertex cover predicate gives Khot and Regev's $2 - \varepsilon$ for [vertex cover](/vertex-cover-inapproximability/) under the UGC.
- **Every CSP.** [Raghavendra's theorem](/raghavendra-theorem/) turns any integrality gap instance of the basic SDP into a dictatorship test with the same completeness and soundness, so the SDP is optimal for every CSP under the UGC.
- **Approximation resistance.** A dictatorship test whose soundness equals the random-assignment value of the predicate gives [approximation resistance](/approximation-resistance/). Austrin and Mossel build such tests from pairwise independent distributions.

## References
