---
tag: MTK60C
kind: theorem
slug: risch-structure-theorem
name: Risch structure theorem
area: algebra/computer-algebra
level: research
summary: Describes the transcendental extensions needed to express elementary integrals, the basis of the Risch algorithm.
prereqs: [liouville-theorem, polynomial-gcd]
see_also: [risch-algorithm, liouville-theorem, risch-norman-heuristic, symbolic-integration, richardson-theorem, constant-problem, hermite-reduction, differential-galois-theory]
sources:
  - paper: doi:10.2307/2373917
    title: Robert H. Risch, Algebraic properties of the elementary functions of analysis, American Journal of Mathematics 101(4), 1979
    locator: pp. 743 to 759 (the structure theorem for towers of exponentials, logarithms and algebraic functions)
  - paper: doi:10.1137/0208028
    title: Michael Rothstein and B. F. Caviness, A structure theorem for exponential and primitive functions, SIAM Journal on Computing 8(3), 1979
    locator: pp. 357 to 367 (the form with rational linear combinations, and its use for simplification)
  - book: isbn:9783540214939
    title: Manuel Bronstein, Symbolic Integration I, Transcendental Functions, second edition, Springer, 2005
    locator: Chapter 9, Structure Theorems, and Chapter 5 for monomials and the tower of a Risch integration
  - paper: doi:10.2140/pjm.1976.65.485
    title: Maxwell Rosenlicht, On Liouville's theory of elementary functions, Pacific Journal of Mathematics 65(2), 1976
    locator: pp. 485 to 492 (algebraic relations between exponentials and logarithms)
  - paper: doi:10.1007/BF02421605
    title: Alexandre Ostrowski, Sur les relations algébriques entre les intégrales indéfinies, Acta Mathematica 78, 1946
    locator: pp. 315 to 318 (the earlier result for integrals, later extended by Kolchin)
  - paper: doi:10.2307/1970774
    title: James Ax, On Schanuel's conjectures, Annals of Mathematics 93(2), 1971
    locator: pp. 252 to 268 (the differential form of Schanuel's conjecture)
  - paper: doi:10.1016/j.jsc.2007.04.003
    title: Manuel Bronstein, Structure theorems for parallel integration, Journal of Symbolic Computation 42(7), 2007
    locator: pp. 757 to 769
---

## Statement

All fields have characteristic $0$. A *differential field* is a field with a derivation $u \mapsto u'$, and its *constants* are the elements with $u' = 0$. Let $C$ be a field and $k = C(x)$ with $x' = 1$, so $C$ is the field of constants of $k$. Let
$$k = K_0 \subset K_1 \subset \cdots \subset K_n = K, \qquad K_i = K_{i-1}(t_i),$$
be a tower of differential fields in which every $t_i$ is transcendental over $K_{i-1}$ and is either

- a *logarithm*: $t_i' = a_i' / a_i$ for some $a_i \in K_{i-1}^*$, written $t_i = \log a_i$; the set of such $i$ is $L$; or
- an *exponential*: $t_i' = b_i' \, t_i$ for some $b_i \in K_{i-1}$, written $t_i = \exp b_i$; the set of such $i$ is $E$.

Assume that $K$ has no new constants: the constants of $K$ are exactly $C$.

**Theorem (Risch structure theorem).**

(a) Let $f \in K$. There is a nonzero $\theta$, algebraic over $K$ in some differential extension, with $\theta' = f' \theta$ (that is, $\exp f$ is algebraic over $K$) if and only if
$$f = c + \sum_{i \in L} r_i\, t_i + \sum_{j \in E} r_j\, b_j \quad \text{with } c \in C \text{ and } r_i, r_j \in \mathbb{Q}.$$

(b) Let $g \in K^*$. There is $\theta$, algebraic over $K$ in some differential extension, with $\theta' = g' / g$ (that is, $\log g$ is algebraic over $K$) if and only if
$$\frac{g'}{g} = \sum_{i \in L} r_i\, \frac{a_i'}{a_i} + \sum_{j \in E} r_j\, b_j' \quad \text{with } r_i, r_j \in \mathbb{Q}.$$
In that case $\log g$ lies in $K$: it is $\sum_{i \in L} r_i t_i + \sum_{j \in E} r_j b_j$, up to a constant.

So a new exponential or logarithm is either a new transcendental, or it is given by a rational linear combination of the logarithms and the exponents already in the tower. This is the form of Rothstein and Caviness (1979). Risch (1979) proved a version that also allows algebraic $t_i$, and Bronstein (Symbolic Integration I, Chapter 9) gives versions over a general differential base field.

## In plain words

When you build a formula from exponentials and logarithms, a new exponential or logarithm can be truly new, or it can secretly be a combination of the ones you already have. For example, the logarithm of the square of a function is twice its logarithm, and the exponential of half a logarithm is a square root. The theorem says that such hidden relations come only from simple rules of this kind, with whole numbers or fractions as multipliers. So a program can decide whether a new function adds something new by checking a linear system with rational unknowns. Integration programs need this, because they must know that the functions in a formula are independent before they can reason about it.

## Proof

The two "if" directions are direct. For (a), let $M$ be a common denominator of the $r$'s, with $r = n / M$, and let $\theta$ be a root of $\theta^M = \prod_{i \in L} a_i^{n_i} \prod_{j \in E} t_j^{n_j}$ in an algebraic extension. The derivation extends uniquely to it, and $M \theta' / \theta = \sum n_i a_i' / a_i + \sum n_j t_j' / t_j = M f'$. For (b), take $\theta = \sum r_i t_i + \sum r_j b_j \in K$; then $\theta' = g' / g$.

For the "only if" directions, write $\lambda(U) = \sum_{i \in L} n_i t_i + \sum_{j \in E} n_j b_j$ for a formal product $U = \prod_{i \in L} a_i^{n_i} \prod_{j \in E} t_j^{n_j}$ with integer exponents. Then $\lambda(U)' = U' / U$, since $t_i' = a_i' / a_i$ and $b_j' = t_j' / t_j$. The core is the following lemma.

**Main lemma.** Let $u_1, \ldots, u_r \in K^*$, let $s_1, \ldots, s_r \in C$ be linearly independent over $\mathbb{Q}$, and let $v \in K$ with
$$\sum_{m=1}^{r} s_m \frac{u_m'}{u_m} = v'. \tag{1}$$
Then there are an integer $M \ge 1$, constants $c_m \in C^*$, $c \in C$ and formal products $U_m$ as above with $u_m^M = c_m U_m$ for every $m$, and $v = c + \frac{1}{M} \sum_m s_m \lambda(U_m)$. (For $r = 0$ the claim is that $v \in C$.)

*Proof.* Induction on $n$. We use two facts about a monic irreducible $p$ in $F[t]$, where $F = K_{n-1}$ and $t = t_n$.

*Fact 1.* If $p \nmid p'$, then for $w \in F(t)$ with $p$-adic valuation $\nu_p(w) = -e < 0$, we have $\nu_p(w') = -e - 1$. Indeed, write $w = A / (p^e B)$ with $p \nmid A B$. Then $w' = (A' p B - A(e p' B + p B')) / (p^{e+1} B^2)$, and the numerator is $-e A p' B \not\equiv 0 \bmod p$. Also $\nu_p(u'/u) \ge -1$ for every $u \in F(t)^*$, and the part of $u'/u$ with a pole at $p$ is $\nu_p(u)\, p'/p$.

*Fact 2.* If $t$ is a logarithm, every $p$ of degree $d \ge 1$ has $p \nmid p'$. If $t$ is an exponential, every $p \ne t$ of degree $d \ge 1$ has $p \nmid p'$. For a logarithm, $p'$ has degree less than $d$ and its coefficient of $t^{d-1}$ is $(d t + p_{d-1})'$; if this were $0$, then $d t + p_{d-1}$ would be a constant, so in $C \subset F$, and $t \in F$. So $p' \ne 0$ has lower degree than $p$. For an exponential, $p'$ has degree $d$ with leading coefficient $d b'$, so $p \mid p'$ means $p' = d b' p$. Then the constant coefficient $p_0 \ne 0$ satisfies $p_0' = d b' p_0$, so $(t^d / p_0)' = 0$ and $t^d \in C p_0 \subset F$, which contradicts the transcendence of $t$.

*Base case* $n = 0$, $K = C(x)$. Here $x' = 1$ and every irreducible $p \in C[x]$ has $p' \ne 0$ of lower degree, so Fact 1 applies to all $p$. By Fact 1, $v$ has no pole at any $p$, since the left side of (1) has at most simple poles. So $v \in C[x]$ and the left side has no pole. Its pole part at $p$ is $\bigl(\sum_m s_m \nu_p(u_m)\bigr) p' / p$, so $\sum_m s_m \nu_p(u_m) = 0$, and by the linear independence all $\nu_p(u_m) = 0$. So $u_m \in C^*$, the left side is $0$, and $v \in C$. Take $M = 1$ and empty products.

*Logarithmic step*, $t = t_n = \log a$. By Facts 1 and 2, exactly as in the base case, $v \in F[t]$ and every $u_m = h_m \in F^*$. Then $v' = \sum s_m h_m' / h_m \in F$. Write $v = \sum_{l=0}^{e} v_l t^l$. The coefficient of $t^e$ in $v'$ is $v_e'$, so $v_e \in C$ if $e \ge 1$. If $e \ge 2$, the coefficient of $t^{e-1}$ is $(e v_e t + v_{e-1})' = 0$, and as in Fact 2 this gives $t \in F$. So $v = s t + w$ with $s \in C$ and $w \in F$, and
$$\sum_m s_m \frac{h_m'}{h_m} - s \frac{a'}{a} = w'. \tag{2}$$
Suppose $s$ is not in the $\mathbb{Q}$-span of $s_1, \ldots, s_r$. Then $s \ne 0$, and $s_1, \ldots, s_r, -s$ are linearly independent over $\mathbb{Q}$. The induction hypothesis for $F$ applied to (2) gives $a^{M'} = c' U$ for a formal product $U$ over the first $n - 1$ levels. Then $t' = a'/a = (\lambda(U) / M')'$, so $t - \lambda(U) / M'$ is a constant, in $C \subset F$, and $t \in F$: a contradiction. So $s = \sum_m q_m s_m$ with $q_m \in \mathbb{Q}$. Let $M_0 \ge 1$ be a common denominator of the $q_m$. Then (2) reads $\sum_m (s_m / M_0)\, \tilde{u}_m' / \tilde{u}_m = w'$ with $\tilde{u}_m = h_m^{M_0} a^{-M_0 q_m} \in F^*$, and the $s_m / M_0$ are still independent. By induction, $\tilde{u}_m^{M'} = c_m \tilde{U}_m$ and $w = c + \frac{1}{M'} \sum_m (s_m / M_0) \lambda(\tilde{U}_m)$. Put $M = M_0 M'$ and $U_m = \tilde{U}_m\, a^{M q_m}$, a formal product that now uses $a = a_n$. Then $u_m^M = h_m^M = c_m U_m$, and $\lambda(U_m) = \lambda(\tilde{U}_m) + M q_m t$, so
$$\frac{1}{M} \sum_m s_m \lambda(U_m) = (w - c) + \sum_m s_m q_m\, t = v - c.$$

*Exponential step*, $t = t_n = \exp b$. By Facts 1 and 2, $v$ has no pole at any $p \ne t$, and every $u_m = h_m t^{k_m}$ with $h_m \in F^*$ and $k_m \in \mathbb{Z}$. So $v = \sum_l v_l t^l$ is a Laurent polynomial, and $v' = \sum_l (v_l' + l b' v_l) t^l$. The left side of (1) is $\sum_m s_m (h_m' / h_m + k_m b') \in F$. For $l \ne 0$, the coefficient $v_l' + l b' v_l = (v_l t^l)' / t^l$ must be $0$, so $v_l t^l$ is a constant, and if $v_l \ne 0$ then $t^l \in F$, which is false. So $v = v_0 \in F$ and, with $\sigma = \sum_m s_m k_m$,
$$\sum_m s_m \frac{h_m'}{h_m} = (v_0 - \sigma b)'.$$
By induction, $h_m^M = c_m \tilde{U}_m$ and $v_0 - \sigma b = c + \frac{1}{M} \sum_m s_m \lambda(\tilde{U}_m)$. Put $U_m = \tilde{U}_m t^{M k_m}$. Then $u_m^M = c_m U_m$ and $\lambda(U_m) = \lambda(\tilde{U}_m) + M k_m b$, so $\frac{1}{M} \sum_m s_m \lambda(U_m) = v_0 - \sigma b - c + \sigma b = v - c$. $\square$

*Proof of the "only if" directions.* Let $\theta$ be algebraic over $K$ of degree $N$, let $\mathrm{Tr}$ and $\mathrm{Nm}$ be the trace and norm from $K(\theta)$ to $K$. The derivation commutes with every embedding of $K(\theta)$ over $K$ into a normal closure (the extension of a derivation to an algebraic extension is unique), so $\mathrm{Tr}(\eta)' = \mathrm{Tr}(\eta')$ and $\mathrm{Nm}(\eta)' / \mathrm{Nm}(\eta) = \mathrm{Tr}(\eta' / \eta)$.

For (a), $\theta' / \theta = f' \in K$ gives $u'/u = \mathrm{Tr}(f') = (N f)'$ for $u = \mathrm{Nm}(\theta) \in K^*$. The main lemma with $r = 1$, $s_1 = 1$ and $v = N f$ gives $N f = c + \frac{1}{M} \lambda(U)$, which is the claimed form of $f$ with $r = n / (M N)$.

For (b), $\theta' = g'/g \in K$ gives $v' = g' / g$ for $v = \mathrm{Tr}(\theta) / N \in K$. The main lemma with $u_1 = g$ and $s_1 = 1$ gives $g^M = c_1 U$, so $g'/g = \lambda(U)' / M$, which is the claimed rational combination. It also gives $v = c + \lambda(U) / M \in K$. $\blacksquare$

## Consequences

**Building the tower for integration.** The [Risch algorithm](/risch-algorithm/) works in a tower of monomials, so before it adds $\exp f$ or $\log g$ it must know whether the new function is transcendental. By the theorem this is a linear question: are there rationals $r$ with $f - \sum r_i t_i - \sum r_j b_j$ constant, or $g'/g = \sum r_i a_i' / a_i + \sum r_j b_j'$? If yes, the function is replaced by an expression in the tower. If no, it is a new monomial, and the tower still has no new constants.

**Examples.** Over $\mathbb{C}(x)$ with $t_1 = \log x$: $\log(x^2) = 2 t_1$ and $\exp(t_1 / 2) = \sqrt{x}$, which is algebraic. With $t_1 = \exp x$, $\exp(2x) = t_1^2$, but $\exp(\sqrt{2}\, x)$ is a new transcendental, since $\sqrt{2}\, x$ is not a rational multiple of $x$ plus a constant. With $t_1 = \log x$, $\log(x + 1)$ is new, since $1/(x+1)$ is not a rational multiple of $1/x$.

**Simplification and zero testing.** Rothstein and Caviness used the theorem to put elementary expressions built from $\exp$ and $\log$ into a form where every function is either independent of the others or rewritten in terms of them. Zero equivalence then reduces to zero equivalence of constants. This is the [constant problem](/constant-problem/), which is open in general. For larger classes of functions, [Richardson's theorem](/richardson-theorem/) shows that zero equivalence is undecidable.

**Algebraic independence.** If no relation of the two kinds holds, the $t_i$ are algebraically independent over $C(x)$. Results of this kind are related to the functional form of Schanuel's conjecture, which Ax (1971) proved for power series.

## Tightness

- **No new constants.** The hypothesis that $K$ has the constants $C$ is needed. Let $t_1$ be transcendental with $t_1' = 0$, formally $t_1 = \log 1$, so $t_1$ is a new constant. Then $f = t_1^2$ has $f' = 0$, and $\theta = 1$ satisfies $\theta' = f' \theta$, but $t_1^2$ is not of the form in (a).
- **Algebraic, not rational.** In (a) the rationals $r$ cannot be replaced by integers if one wants $\theta \in K$: $\exp(\frac{1}{2} \log x) = \sqrt{x}$ is algebraic over $\mathbb{C}(x, \log x)$, but not in it. Over $K$ itself, $\exp f \in K$ needs the product $\prod a_i^{r_i} \prod t_j^{r_j}$ to be in $K$, which depends on the $a_i$.
- **Rational, not arbitrary constants.** The coefficients are rational because only rational powers of the $a_i$ and $t_j$ are algebraic. A relation with an irrational constant coefficient, such as $\exp(\sqrt{2} \log x) = x^{\sqrt{2}}$, gives a transcendental function.
- **Transcendental monomials.** The tower must consist of transcendental $t_i$. Risch's 1979 form also allows algebraic steps, at the cost of a more complex statement.
- **Effectiveness.** The theorem gives a decision method only when one can compute in $C$ and decide whether an element of $K$ is constant. For $C$ a number field this holds. For $C = \mathbb{R}$ or $\mathbb{C}$ with transcendental constants, the step needs a zero test for constants.

## History

Liouville's work of the 1830s on integration in finite terms already used the fact that new exponentials and logarithms are independent of old ones unless they satisfy simple relations. Ostrowski (1946) proved that integrals $y_i$ with $y_i' \in K$ are algebraically dependent only through a linear relation with constant coefficients, and Kolchin extended this to exponentials in 1968. Risch (1969) needed such statements for his integration algorithm, and in 1979 he published the general structure theorem for elementary towers with algebraic steps. In the same year Rothstein and Caviness gave the form for exponentials and logarithms stated here, with an application to simplification. Rosenlicht (1976) gave an algebraic proof, and Bronstein's book (Chapter 9) gives the modern statements over a general differential base field. Bronstein (2007) extended the theorem to the setting of parallel integration.

## References
