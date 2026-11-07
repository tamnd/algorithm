---
tag: 98FNCK
kind: theorem
slug: richardson-theorem
name: Richardson's theorem
aliases: [Richardson's undecidability theorem, undecidability of zero equivalence]
area: algebra/computer-algebra
level: advanced
summary: Zero equivalence is undecidable for real functions built from x, the rationals, pi, sin, exp and absolute value.
prereqs: [hilberts-tenth-problem, decision-problem]
see_also: [risch-algorithm, symbolic-integration, risch-structure-theorem, tarski-seidenberg-theorem, quantifier-elimination, liouville-theorem]
sources:
  - paper: doi:10.2307/2271358
    title: Daniel Richardson, Some undecidable problems involving elementary functions of a real variable, Journal of Symbolic Logic 33(4), 1968
    locator: pp. 514 to 520
  - paper: doi:10.1090/S0002-9939-02-06753-9
    title: Miklós Laczkovich, The removal of π from some undecidable problems involving elementary functions, Proceedings of the American Mathematical Society 131(7), 2003
    locator: pp. 2235 to 2240
  - paper: doi:10.1145/321574.321591
    title: Bob F. Caviness, On canonical forms and simplification, Journal of the ACM 17(2), 1970
    locator: pp. 385 to 396 (consequences for canonical simplification)
  - paper: doi:10.1006/jsco.1997.0157
    title: Daniel Richardson, How to recognize zero, Journal of Symbolic Computation 24(6), 1997
    locator: pp. 627 to 645 (zero recognition for exp-log constants, correct if Schanuel's conjecture holds)
  - paper: doi:10.1070/RM1972v027n05ABEH001386
    title: Yuri V. Matiyasevich, Diophantine sets, Russian Mathematical Surveys 27(5), 1972
    locator: pp. 124 to 164 (the negative solution of Hilbert's tenth problem)
  - book: isbn:9783540214939
    title: Manuel Bronstein, Symbolic Integration I, Transcendental Functions, second edition, Springer, 2005
    locator: Chapter 3 (the assumption that the constant field is computable, with zero recognition)
---

## Statement

Let $\mathcal{E}$ be the class of expressions in one real variable $x$ built from $x$, rational numbers and $\pi$ with $+$, $-$, $\cdot$, composition, $\sin$, $\exp$ and $|\cdot|$. Each expression defines a function $\mathbb{R} \to \mathbb{R}$. Let $\mathcal{E}_0 \subset \mathcal{E}$ be the expressions without $|\cdot|$.

**Theorem (Richardson 1968).**

1. There is no algorithm that decides, for $E \in \mathcal{E}_0$, whether $E(x) < 0$ for some real $x$.
2. There is no algorithm that decides, for $E \in \mathcal{E}$, whether $E(x) = 0$ for all real $x$.

So zero equivalence, the problem "is this expression identically zero?", is undecidable in $\mathcal{E}$, and so is the problem "is $E \ge 0$ everywhere?". Richardson's class also contains $\ln 2$, and his proof builds the dense curve of Step 2 from $x \sin x$ and $x \sin x^3$. The proof below uses $\exp$ there instead, because the density argument is shorter.

## In plain words

A computer algebra system often has to decide whether an expression is zero. If it cannot, it cannot simplify reliably, cannot divide safely, and cannot be sure that an answer is correct. Richardson showed that for expressions built from x, fractions, pi, sine, the exponential and absolute value, no program can always answer this question.

The proof turns a question about whole-number solutions of polynomial equations, which is known to be unsolvable by any program, into a question about the sign of one such expression. The sine of pi times x is zero only at whole numbers, so it can force a real variable to be a whole number, and functions like x times the sine of x let one real variable take the place of many.

## Proof

The proof reduces [Hilbert's tenth problem](/hilberts-tenth-problem/) to part 1, and part 1 to part 2.

**Step 0 (Matiyasevich 1970).** There is no algorithm that decides, for $P \in \mathbb{Z}[n_1, \ldots, n_k]$ with any $k$, whether $P$ has a zero in $\mathbb{Z}^k$. This is the negative solution of Hilbert's tenth problem by Matiyasevich, after Davis, Putnam and Robinson. We use it without proof.

**Step 1 (from integers to reals in $k$ variables).** Let $P$ have total degree $d \ge 1$ and let $S$ be the sum of the absolute values of its coefficients. Put

$$B(x) = d S (1 + x_1^2 + \cdots + x_k^2)^d, \qquad F(x) = P(x)^2 + \sum_{i=1}^k \sin^2(\pi x_i) \, B(x)^2, \qquad c_k = \frac{1}{4k^2}.$$

*Claim:* $P$ has a zero in $\mathbb{Z}^k$ exactly when $F(x) < c_k$ for some $x \in \mathbb{R}^k$.

If $P(n) = 0$ with $n \in \mathbb{Z}^k$, then $F(n) = 0 < c_k$. Conversely, suppose $P$ has no integer zero, and let $x \in \mathbb{R}^k$. Let $n$ be a nearest integer point and $\delta_i = |x_i - n_i| \le 1/2$. For $z$ in the box $|z_j - x_j| \le 1/2$, $|z_j| \le |x_j| + 1/2 \le 1 + x_j^2$, so each partial derivative satisfies $|\partial P/\partial z_i (z)| \le B(x)$: a monomial $c z^\alpha$ has derivative of absolute value at most $|c| \, d \, (1 + \sum_j x_j^2)^d$. Moving from $n$ to $x$ one coordinate at a time inside the box, the mean value theorem gives $|P(x) - P(n)| \le B(x) \sum_i \delta_i$. Since $P(n)$ is a nonzero integer, $|P(n)| \ge 1$. There are two cases.

- If $|P(x)| \ge 1/2$, then $F(x) \ge 1/4 \ge c_k$.
- Otherwise $B(x) \sum_i \delta_i \ge 1/2$, so $\delta_i B(x) \ge 1/(2k)$ for some $i$. Since $|\sin(\pi \delta)| \ge 2\delta$ for $0 \le \delta \le 1/2$ by concavity, and $\sin^2(\pi x_i) = \sin^2(\pi \delta_i)$, $F(x) \ge 4 \delta_i^2 B(x)^2 \ge 1/k^2 \ge c_k$.

So $F \ge c_k$ everywhere, which proves the claim.

**Step 2 (a dense curve).** Let $u(t) = t \sin t$. For an integer $m \ge 1$, on $I_m = [2\pi m - \pi/3, \, 2\pi m + \pi/3]$ we have $\cos t \ge 1/2$, so $u'(t) = \sin t + t \cos t \ge t/2 - 1 > 0$, and $u$ is increasing on $I_m$ from $-(2\pi m - \pi/3)\sqrt{3}/2$ or below to $(2\pi m - \pi/3)\sqrt 3/2$ or above. Since $(2\pi m - \pi/3)\sqrt 3/2 \ge 4m$ for $m \ge 1$, $u(I_m) \supseteq [-4m, 4m]$. So every real value is taken by $u$ at points $t$ as large as we like.

Define $\gamma_1(t) = u(t)$ and $\gamma_k(t) = \big(u(t), \, \gamma_{k-1}(u(e^t))\big)$ for $k \ge 2$. Each coordinate of $\gamma_k$ is in $\mathcal{E}_0$.

*Claim:* for every $k \ge 1$, every $T$, every $(a, b) \in \mathbb{R} \times \mathbb{R}^{k-1}$ and every $\varepsilon > 0$, there is $t \ge T$ with $|\gamma_k(t) - (a, b)| < 2\varepsilon$. In particular $\gamma_k(\mathbb{R})$ is dense in $\mathbb{R}^k$.

For $k = 1$ this is the last sentence of the previous paragraph. For $k \ge 2$, by induction $\gamma_{k-1}(\mathbb{R})$ is dense, so there is $s^*$ with $|\gamma_{k-1}(s^*) - b| < \varepsilon$. Choose $t_a \ge T$ in some $I_m$ with $u(t_a) = a$, with $m$ large; this is possible by the previous paragraph. Let $\eta = \min(1, \varepsilon/(t_a + 2))$. Since $|u'(t)| \le 1 + |t| \le t_a + 2$ near $t_a$, $|u(t) - a| < \varepsilon$ for $|t - t_a| < \eta$. On this interval, $e^t$ runs over an interval of length at least $2\eta e^{t_a - \eta} \ge 2 \varepsilon e^{t_a - 1}/(t_a + 2)$, with left end at least $e^{t_a - 1}$. For $m$ large, this interval has length more than $4\pi$ and left end more than $2\pi |s^*|$, so it contains a whole $I_{m'}$ with $4m' \ge |s^*|$, and so $u(e^t) = s^*$ for some $t$ with $|t - t_a| < \eta$. At this $t$, $|u(t) - a| < \varepsilon$ and $\gamma_{k-1}(u(e^t)) = \gamma_{k-1}(s^*)$ is within $\varepsilon$ of $b$. This proves the claim.

**Step 3 (part 1).** Given $P$, form $E(t) = F(\gamma_k(t)) - c_k$. It is in $\mathcal{E}_0$: $F$ uses only $+$, $\cdot$, integers, $\pi$ and $\sin$, and $\gamma_k$ uses $\sin$, $\exp$, $\cdot$ and composition. $F$ is continuous, so $\{x : F(x) < c_k\}$ is open. If it is not empty, it meets the dense set $\gamma_k(\mathbb{R})$, and $E(t) < 0$ for some $t$. If it is empty, $E \ge 0$ everywhere. By Step 1, $E(t) < 0$ for some $t$ exactly when $P$ has an integer zero. An algorithm for part 1 would therefore solve Hilbert's tenth problem, which contradicts Step 0.

**Step 4 (part 2).** For $E \in \mathcal{E}_0$, $Z = |E| - E$ is in $\mathcal{E}$, and $Z(x) = 0$ for all $x$ exactly when $E(x) \ge 0$ for all $x$. So an algorithm for part 2 would give one for part 1. $\blacksquare$

## Consequences

- **No canonical simplifier.** A canonical form maps equal functions to identical expressions, so it would decide zero equivalence by comparing with the form of $0$. Hence $\mathcal{E}$ has no computable canonical form, as Caviness (1970) observed, and simplifiers for such classes are heuristic or work in smaller classes.
- **Integration needs zero recognition.** The [Risch algorithm](/risch-algorithm/) and other methods of [symbolic integration](/symbolic-integration/) must decide if expressions are zero, for example to know the degree of a polynomial or if a residue is a constant. They are decision procedures only relative to an oracle for zero, or in classes where zero is decidable, such as towers of exponentials and logarithms over a computable constant field ([Risch structure theorem](/risch-structure-theorem/)).
- **Equations and inequalities with sine.** Since $\sin(\pi x) = 0$ defines $\mathbb{Z}$, the first-order theory of $(\mathbb{R}, +, \cdot, <, \sin)$ is undecidable, in contrast with the [Tarski-Seidenberg theorem](/tarski-seidenberg-theorem/) for the real field without $\sin$. Part 1 is a much stronger form: no quantifier alternation is needed, only one existential quantifier over one real variable.
- **Practical systems.** Computer algebra systems test zero by a mix of rewriting, evaluation at random points, and numerical bounds. Such tests can prove that an expression is not zero, but they cannot in general prove that it is zero.

## Tightness

- **Without $\sin$ and $|\cdot|$.** For expressions with $\exp$ and $\log$ but no periodic functions, zero equivalence of functions reduces to zero recognition of constants by the structure theorems for exp-log fields. Whether this is decidable is open. Richardson (1997) gave an algorithm for exp-log constants that is correct whenever it stops and that stops if Schanuel's conjecture holds.
- **The constant problem.** For constant expressions, with no variable, the theorem says nothing. The constant problem for $\mathcal{E}$ is not known to be undecidable, and it is decidable for the real algebraic numbers.
- **Without $\pi$.** Laczkovich (2003) showed that $\pi$ is not needed: the problems remain undecidable for expressions built from $x$ and the functions $\sin x^n$ and $\sin(x \sin x^n)$.
- **Without $\exp$.** Richardson's original proof uses $x \sin x$ and $x \sin x^3$ to make the dense curve, so $\exp$ is not needed either.
- **Polynomials only.** For expressions built from $x$, rationals, $+$ and $\cdot$, zero equivalence is decidable by expanding to a polynomial, and the sign questions are decidable by [quantifier elimination](/quantifier-elimination/). The source of undecidability is the integer structure that $\sin(\pi x)$ brings in.

## History

Hilbert's tenth problem was solved negatively by Matiyasevich in 1970, completing work of Davis, Putnam and Robinson. Richardson proved the theorem in 1968, building on the work of Davis, Putnam and Robinson; with Matiyasevich's theorem the proof can start from ordinary polynomial equations, as above. Caviness (1970) drew the consequences for simplification in computer algebra. Wang (1974) and Laczkovich (2003) sharpened the class of expressions, and Richardson later worked on positive results for zero recognition of constants.

## References
