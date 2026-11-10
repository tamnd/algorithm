---
tag: NNGB8N
kind: technique
slug: low-degree-test
name: Low-degree test
aliases:
- polynomial test
- Rubinfeld-Sudan test
- line test
area: approximation/hardness-of-approximation
level: research
summary: A randomized test that reads a function on a few points of a random line and accepts a function far from every low-degree polynomial with noticeable probability.
prereqs: [reed-muller-code, schwartz-zippel-lemma, linearity-test]
see_also: [pcp-theorem, probabilistically-checkable-proof, polynomial-identity-testing, locally-decodable-codes, hastad-3bit-pcp, two-prover-one-round-game]
sources:
  - paper: doi:10.1137/S0097539793255151
    title: Ronitt Rubinfeld and Madhu Sudan, Robust characterizations of polynomials with applications to program testing, SIAM Journal on Computing 25(2), 252 to 271, 1996
    locator: the test on d + 2 points of a random line, its characterization of degree d polynomials and its robustness theorem
  - paper: "Sanjeev Arora, Carsten Lund, Rajeev Motwani, Madhu Sudan and Mario Szegedy, Proof verification and the hardness of approximation problems, Journal of the ACM 45(3), 501 to 555, 1998"
    locator: the use of low-degree polynomials and their test in the PCP theorem
  - paper: "Sanjeev Arora and Madhu Sudan, Improved low-degree testing and its applications, Combinatorica 23(3), 365 to 426, 2003"
    locator: the lines-versus-points test in the regime of small acceptance probability
  - paper: "Ran Raz and Shmuel Safra, A sub-constant error-probability low-degree test, and a sub-constant error-probability PCP characterization of NP, Proceedings of the 29th ACM Symposium on Theory of Computing (STOC), 1997"
    locator: the plane-versus-plane test and its soundness
---

A low-degree test is a randomized check that a function $f : \mathbb{F}^m \to \mathbb{F}$ over a finite field is close to a polynomial of total degree at most $d$, made by reading $f$ at only $d + 2$ points. The Rubinfeld-Sudan test picks a random line, reads $f$ at $d + 2$ equally spaced points on it, and checks that the values fit a univariate polynomial of degree at most $d$. It extends the [linearity test](/linearity-test/) from degree $1$ to degree $d$, and it is the step of the algebraic proof of the [PCP theorem](/pcp-theorem/) that forces a proof written as a [Reed-Muller](/reed-muller-code/) code word to be honest.

## In plain words

A polynomial in several variables has a strong local property: on any straight line through its domain, it looks like a polynomial in one variable of the same low degree. So a tester picks a random line, reads the table at a few points of the line, and checks that these values could come from a low-degree curve. A table that is a true polynomial always passes. A table that changes a few entries of a polynomial fails a little more often, in proportion to the number of changed entries. The deep part is the converse: if a table passes almost always, it must be close to a single polynomial. This lets a verifier trust a huge table after reading only a few entries of it.

## When it applies

Fix a prime field $\mathbb{F}_p$, a dimension $m$ and a degree $d$ with $p \ge d + 2$. Let $\mathcal{P}_d$ be the set of functions $\mathbb{F}_p^m \to \mathbb{F}_p$ given by polynomials of total degree at most $d$, and let $\operatorname{dist}(f, \mathcal{P}_d) = \min_{g \in \mathcal{P}_d} \Pr_x[f(x) \ne g(x)]$. The test applies when a proof or a code word is a table of values of $f$, too large to read, that is supposed to lie in $\mathcal{P}_d$. Two distinct polynomials of degree at most $d < p$ differ on at least a $1 - d/p$ fraction of points by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), so when $d$ is small compared with $p$ the code $\mathcal{P}_d$ has large distance and the nearest polynomial is unique.

Hardness pages on this site use the ratio convention $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$ for maximization. The low-degree test enters such results only inside a PCP verifier, where it controls the soundness.

## The template

**The test.** Let $\alpha_i = (-1)^i \binom{d+1}{i}$ for $i = 0, \ldots, d + 1$. Pick $x, h \in \mathbb{F}_p^m$ uniformly and independently. Query $f(x + i h)$ for $i = 0, \ldots, d + 1$. Accept if $\sum_{i=0}^{d+1} \alpha_i f(x + i h) = 0$.

**Completeness, in full.** If $f \in \mathcal{P}_d$, the test accepts with probability $1$. *Proof.* The function $g(t) = f(x + t h)$ is a polynomial in $t$ of degree at most $d$, say $g(t) = \sum_{k=0}^d c_k t^k$. Then $\sum_i \alpha_i g(i) = \sum_{k=0}^d c_k \sum_{i=0}^{d+1} (-1)^i \binom{d+1}{i} i^k$. Over the integers, $\sum_{i} (-1)^i \binom{d+1}{i} i^k$ is $(-1)^{d+1}$ times the $(d+1)$-th forward difference of $t^k$ at $t = 0$, and each forward difference lowers the degree by one, so this sum is $0$ for $k \le d$. An integer identity holds in every field, so the check holds. $\square$

**Why the field size matters.** In characteristic $p$ the points $x + i h$, $i = 0, \ldots, d+1$, are distinct for $h \ne 0$ only when $p \ge d + 2$. Over $\mathbb{F}_2$ with $d = 2$ the weights are $1, 1, 1, 1$ and the points are $x, x+h, x, x+h$, so the sum is always $0$ and the test accepts every function.

**The local characterization.** Over $\mathbb{F}_p$ with $p \ge d + 2$, a function that passes the check for all $x$ and $h$ lies in $\mathcal{P}_d$. For one variable the proof is short: a function $\mathbb{F}_p \to \mathbb{F}_p$ is a polynomial of degree at most $p - 1$, and the difference operator $g(t) \mapsto g(t+1) - g(t)$ maps a polynomial of degree $k$ with $1 \le k \le p - 1$ to one of degree exactly $k - 1$, because the new leading coefficient is $k$ times the old one and $k \ne 0$ in $\mathbb{F}_p$. So if the $(d+1)$-th difference is $0$, the degree is at most $d$. The extension from lines to $\mathbb{F}_p^m$ is part of the Rubinfeld-Sudan paper and is cited here.

**Soundness (cited).** Rubinfeld and Sudan prove a robust form: there is a threshold, depending only on $d$, such that if the test rejects $f$ with probability $\varepsilon$ below the threshold, then $\operatorname{dist}(f, \mathcal{P}_d)$ is at most a constant times $\varepsilon$. The exact threshold and constant are in their paper. This page does not prove it.

**An upper bound on the rejection, in full.** If $\operatorname{dist}(f, \mathcal{P}_d) = \delta$, the test rejects with probability at most $(d+2)\delta$. *Proof.* Let $g \in \mathcal{P}_d$ be at distance $\delta$. If $f = g$ at all $d + 2$ queried points, the check holds by completeness for $g$. For each fixed $i$, the point $x + ih$ is uniform because $x$ is uniform. The union bound over the $d + 2$ points gives the claim. $\square$

## Classic examples

**A polynomial over $\mathbb{F}_7$.** Take $p = 7$, $m = 2$, $d = 2$, so the weights are $1, -3, 3, -1$. The function $x_1^2 + 3 x_1 x_2 + 5$ is rejected with probability $0$.

**One wrong entry.** Change that polynomial at the single point $(0, 0)$, so the distance is $1/49$. For $h = 0$ all four queries hit the same point and the check holds because $\sum_i \alpha_i = 0$. For each of the $48$ nonzero $h$ and each of the $4$ positions $i$, exactly one $x$ puts $x + ih$ at the changed point, and then exactly one of the four values is off, so the check fails. The rejection probability is $4 \cdot 48 / 7^4 = 192/2401 \approx 0.0800$, just below the upper bound $4 \cdot \tfrac{1}{49} \approx 0.0816$.

**A polynomial of too high a degree.** For $f(x_1, x_2) = x_1^3$ and $d = 2$, the restriction to a line is $(x_1 + t h_1)^3$, whose third difference with step $1$ in $t$ is $6 h_1^3$. The check fails exactly when $h_1 \ne 0$, so the rejection probability is $6/7$.

**The algebraic PCP.** In the proofs of Arora and Safra and of Arora, Lund, Motwani, Sudan and Szegedy, the prover writes an assignment as the table of a low-degree polynomial on $\mathbb{F}^m$, with $|\mathbb{F}|$ polylogarithmic in the input size and $m$ about $\log n / \log \log n$, so that the table has polynomial size. The verifier runs a low-degree test on the table and then checks the constraints of the instance through further polynomial identities, reading the values it needs at random points. The low-degree test is what lets the verifier treat the table as a true polynomial.

## Variations

- **Lines versus points.** The proof contains a table of $f$ and, for each line, a univariate polynomial of degree at most $d$ claimed to be $f$ on that line. The verifier picks a random line and a random point on it and checks that the two tables agree. Arora and Sudan analyze this test when the acceptance probability is small, which the PCP theorem with small soundness needs.
- **Planes versus points or planes versus planes.** Raz and Safra (STOC 1997) analyze a test on random planes and prove soundness that falls polynomially in the field size. Such tests give PCPs with low soundness error and few queries.
- **Degree $1$.** With $d = 1$ and no constant term the test is the [BLR linearity test](/linearity-test/).
- **Testing in each variable.** A table can also be checked for low individual degree, line by line along the coordinate axes. This is used in the sum-check protocol of [interactive proofs](/interactive-proofs/).

## Pitfalls

- **Small characteristic.** The test needs $p \ge d + 2$ (or a field whose characteristic exceeds $d + 1$). Otherwise some weights vanish or points repeat, and the test accepts functions far from $\mathcal{P}_d$.
- **Total degree versus individual degree.** A polynomial of individual degree $d$ in each of $m$ variables can have total degree $md$. Use the degree that the encoding promises.
- **Distance needs $d$ much smaller than $p$.** The Schwartz-Zippel bound $1 - d/p$ is useful only for $d < p$, and decoding to a unique polynomial needs the distance of $f$ to be below half of that.
- **High versus low acceptance.** The robust characterization applies when the test passes with probability close to $1$. When it passes with small probability only, a different test (lines versus points) and a list of nearby polynomials are needed.
- **The queries are not independent.** The $d+2$ points lie on one line, so a bound that treats them as independent samples is wrong. Only each single point is uniform.

## Exercises

1. Prove that $\sum_{i=0}^{d+1} (-1)^i \binom{d+1}{i} i^k = 0$ over the integers for $0 \le k \le d$ and that it is nonzero for $k = d + 1$.
2. Show that over $\mathbb{F}_p$ with $p \ge d+2$ the rejection probability of the test on a function that differs from a polynomial at one point is $(d+2)(p^m - 1)/p^{2m}$.
3. Compute the rejection probability of the test with $d = 1$ on $f(x) = x_1^2$ over $\mathbb{F}_5$ with $m = 1$.
4. Show that two distinct polynomials of total degree at most $d$ on $\mathbb{F}_p^m$ differ on at least a $1 - d/p$ fraction of points.
5. Explain why the low-degree extension of a string of length $n$ to $\mathbb{F}^m$ with $|H|^m \ge n$ for a subset $H \subseteq \mathbb{F}$ has individual degree at most $|H| - 1$.

## References
