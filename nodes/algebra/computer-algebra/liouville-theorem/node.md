---
tag: C2CAXP
kind: theorem
slug: liouville-theorem
name: Liouville's theorem on integration
aliases:
- Liouville's principle
- Liouville-Ostrowski-Rosenlicht theorem
- Liouville's theorem on elementary integrals
area: algebra/computer-algebra
level: advanced
summary: An elementary antiderivative, if one exists, has a form built from the integrand's elementary logarithms and exponentials.
prereqs: [integration-of-rational-functions, polynomial-ring]
see_also: [risch-algorithm, risch-structure-theorem, risch-norman-heuristic, differential-galois-theory, rothstein-trager, hermite-reduction, kovacic-algorithm]
sources:
  - book: isbn:9783540214939
    title: Manuel Bronstein, Symbolic Integration I, Transcendental Functions, second edition, Springer, 2005
    locator: Chapter 3 (differential fields and elementary extensions) and Chapter 5 (Liouville's theorem and the integration of transcendental elementary functions)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 12, The Risch integration algorithm (differential fields, elementary extensions and Liouville's principle)
  - paper: doi:10.2140/pjm.1968.24.153
    title: Maxwell Rosenlicht, Liouville's theorem on functions with elementary integrals, Pacific Journal of Mathematics 24(1), 153-161, 1968
    locator: the algebraic statement and proof
  - paper: "Maxwell Rosenlicht, Integration in finite terms, American Mathematical Monthly 79(9), 1972"
    locator: the expository proof and the example of exp(x^2)
---

## Statement

Notation: a *differential field* is a field $F$ with a derivation $' \colon F \to F$, an additive map with $(uv)' = u'v + uv'$. Its *constants* are the $c \in F$ with $c' = 0$. They form a subfield $C$. All fields here have characteristic $0$.

An extension $E \supseteq F$ of differential fields is *elementary* if there is a tower $F = F_0 \subseteq F_1 \subseteq \cdots \subseteq F_N = E$ with $F_{j+1} = F_j(\theta_j)$, where each $\theta = \theta_j$ is

- *algebraic* over $F_j$, or
- a *logarithm* over $F_j$: $\theta' = a'/a$ for some $a \in F_j^{*}$, written $\theta = \log a$, or
- an *exponential* over $F_j$: $\theta'/\theta = a'$ for some $a \in F_j$, written $\theta = \exp a$.

**Theorem (Liouville, in the form of Ostrowski and Rosenlicht).** Let $F$ be a differential field of characteristic $0$ whose constant field $C$ is algebraically closed, and let $f \in F$. Suppose $E \supseteq F$ is an elementary extension with the same constant field $C$, and $g \in E$ satisfies $g' = f$. Then there are $v \in F$, constants $c_1, \ldots, c_m \in C$ and $u_1, \ldots, u_m \in F^{*}$ with

$$f = v' + \sum_{i=1}^{m} c_i \frac{u_i'}{u_i}.$$

In words: $\int f = v + \sum_i c_i \log u_i$. If $f$ has an elementary integral at all, it has one that adds only constant multiples of logarithms of elements of $F$ to an element of $F$.

**Without algebraically closed constants.** If $C$ is any field of characteristic $0$ and $E$ adds only constants algebraic over $C$, the same holds with $c_i \in \overline{C}$ and $v, u_i \in F \cdot \overline{C}$, in fact with $u_i$ in $F(c_1, \ldots, c_m)$ and $v \in F$.

## In plain words

Suppose a function built from $x$, logarithms, exponentials and algebraic operations has an antiderivative of the same kind, maybe built from many new logarithms and exponentials. Liouville's theorem says the answer can always be simplified to a very particular shape: a function no more complicated than the integrand, plus a sum of constants times logarithms of such functions. New exponentials never help, and new logarithms appear only in the outermost layer, linearly. This turns "is there an elementary antiderivative?" into a question about one specific shape, which the Risch algorithm can then decide.

## Proof

Three facts about derivations are used throughout.

**(D1) Logarithmic derivatives.** For $u, w \neq 0$, $(uw)'/(uw) = u'/u + w'/w$ and $(u^e)'/u^e = e\, u'/u$ for $e \in \mathbb{Z}$. So a sum $\sum c_i u_i'/u_i$ can be rewritten using any factorization of the $u_i$, and terms with the same $u$ can be merged, since sums of constants are constants.

**(D2) Algebraic extensions.** If $L \supseteq F$ is algebraic, the derivation of $F$ extends uniquely to $L$. Differentiating $\mu(\theta) = 0$ for the minimal polynomial $\mu$ of $\theta$ forces the value of $\theta'$, because $\mu'(\theta) \ne 0$ in characteristic $0$. So every $F$-embedding $\sigma$ of $L$ into a differential field extending $F$ commutes with the derivation: $\sigma(x') = \sigma(x)'$, since $\sigma^{-1} \circ {}' \circ \sigma$ is another extension.

**(D3) Poles.** Let $\theta$ be transcendental over $F$ and $p \in F[\theta]$ monic irreducible with $p \nmid p'$. If $v \in F(\theta)$ has a pole of order $e \ge 1$ at $p$, then $v'$ has a pole of order exactly $e + 1$ at $p$. Write $v = w/p^e$ with $w$ having neither zero nor pole at $p$. Then $w'$ has no pole at $p$, and $v' = (p\, w' - e\, w\, p')/p^{e+1}$, where $p \nmid e\, w\, p'$. Also, for $u \in F(\theta)^{*}$, $u'/u$ has at most a simple pole at $p$, with numerator $e\, p'$ modulo $p$ if $p$ divides $u$ exactly $e$ times.

**The induction.** Call $f$ *of Liouville form over* a differential field $L$ if $f = v' + \sum_i c_i u_i'/u_i$ with $v, u_i \in L$ and $c_i \in C$. Since $f = g'$ with $g \in E$, $f$ is of Liouville form over $E = F_N$, with $m = 0$. It suffices to show the following step lemma and to apply it for $j = N - 1, \ldots, 0$.

*Step lemma.* Let $L = M(\theta)$ be one step of the tower, with the same constants $C$, and $f \in M$. If $f$ is of Liouville form over $L$, it is of Liouville form over $M$.

**Case 1: $\theta$ is algebraic over $M$.** Let $n = [L : M]$, let $N \supseteq L$ be a normal closure, with the derivation from (D2), and let $\sigma_1, \ldots, \sigma_n$ be the distinct $M$-embeddings of $L$ into $N$. Apply each $\sigma_j$ to $f = v' + \sum_i c_i u_i'/u_i$. By (D2), and since $\sigma_j$ fixes $f$ and the $c_i$, $f = \sigma_j(v)' + \sum_i c_i \sigma_j(u_i)'/\sigma_j(u_i)$. Sum over $j$, use (D1), and divide by $n$:

$$f = \Bigl( \tfrac{1}{n} \operatorname{Tr}(v) \Bigr)' + \sum_i \frac{c_i}{n} \frac{\operatorname{N}(u_i)'}{\operatorname{N}(u_i)},$$

where $\operatorname{Tr}(v) = \sum_j \sigma_j(v)$ and $\operatorname{N}(u) = \prod_j \sigma_j(u)$ lie in $M$. This is a Liouville form over $M$.

In the transcendental cases, $L = M(\theta) \cong M(T)$ is a rational function field. By (D1) each $u_i$ can be replaced by its factors: an element of $M^{*}$ and monic irreducible polynomials of $M[\theta]$. So assume $f = v' + \sum_i c_i p_i'/p_i + \sum_j d_j w_j'/w_j$, with distinct monic irreducible $p_i \in M[\theta]$, nonzero $c_i, d_j \in C$, and $w_j \in M^{*}$.

**Case 2: $\theta = \log a$ is transcendental, $\theta' = a'/a \in M$.** For a monic $p = \theta^k + b_{k-1}\theta^{k-1} + \cdots$ with $k \ge 1$, $p' = (b_{k-1}' + k\theta')\theta^{k-1} + \cdots$ has degree less than $k$. It is nonzero, since otherwise $p$ would be a constant, hence in $C \subseteq M$. So $p \nmid p'$ for every such $p$, and (D3) applies at every $p$. If $v$ had a pole at some $p$, $v'$ would have a pole of order at least $2$ there, which no other term has, while $f \in M$ has no pole. So $v \in M[\theta]$. Then at $p_i$, only $c_i p_i'/p_i$ has a pole, a simple one with nonzero numerator. So there are no $p_i$, and $f = v' + \sum_j d_j w_j'/w_j$ with $v = \sum_{k=0}^{K} b_k \theta^k \in M[\theta]$. The coefficient of $\theta^K$ in $v'$ is $b_K'$, and $f$, $w_j'/w_j$ lie in $M$. If $K \ge 1$, then $b_K' = 0$, so $b_K \in C$. If $K \ge 2$, the coefficient of $\theta^{K-1}$ gives $b_{K-1}' + K b_K \theta' = 0$, that is, $(b_{K-1} + K b_K \theta)' = 0$. Then $b_{K-1} + K b_K \theta \in C \subseteq M$, so $\theta \in M$, a contradiction. Hence $v = c\theta + b$ with $c \in C$, $b \in M$, and

$$f = b' + c\, \frac{a'}{a} + \sum_j d_j \frac{w_j'}{w_j},$$

a Liouville form over $M$.

**Case 3: $\theta = \exp a$ is transcendental, $\theta' = a'\theta$.** First, $p \nmid p'$ for monic irreducible $p = \sum_{j=0}^{k} q_j \theta^j \ne \theta$ with $q_k = 1$. Here $p' = \sum_j (q_j' + j a' q_j)\theta^j$ has degree at most $k$ and leading coefficient $k a'$. So $p \mid p'$ would mean $p' = k a' p$, that is $q_j' + (j - k) a' q_j = 0$, or $(q_j \theta^{j-k})' = 0$, for each $j$. Since $p$ is irreducible and $p \ne \theta$, $q_0 \ne 0$, so $q_0 \theta^{-k}$ is a constant $\gamma \ne 0$, and $\theta^k = q_0 / \gamma \in M$. This contradicts the transcendence of $\theta$. So (D3) applies at every $p \ne \theta$. As in Case 2, $v$ has no poles except possibly at $\theta$, and no $p_i \ne \theta$ occurs. So $v = \sum_{k} b_k \theta^k \in M[\theta, \theta^{-1}]$, and the only logarithmic term left in $\theta$ is $c\, \theta'/\theta = c\, a' \in M$. The coefficient of $\theta^k$ in $f$ is $(b_k \theta^k)'/\theta^k = b_k' + k a' b_k$, which must vanish for $k \ne 0$. If $b_k \ne 0$ for some $k \ne 0$, then $b_k \theta^k \in C \subseteq M$, so $\theta^k \in M$, a contradiction. Hence $v = b_0 \in M$, and

$$f = (b_0 + c\, a)' + \sum_j d_j \frac{w_j'}{w_j},$$

a Liouville form over $M$.

This proves the step lemma, and with it the theorem. $\blacksquare$

## Consequences

**$e^{x^2}$ has no elementary antiderivative.** Take $F = \mathbb{C}(x, \theta)$ with $x' = 1$ and $\theta = \exp(x^2)$, which is transcendental over $\mathbb{C}(x)$. If $\int e^{x^2}$ were elementary, then $\theta = v' + \sum c_i u_i'/u_i$ with $v, u_i \in F$ by the theorem. The pole argument of Case 3, applied with $M = \mathbb{C}(x)$, uses only that $f$ has no pole at any $p \ne \theta$, so it applies to $f = \theta$ and shows $v \in M[\theta, \theta^{-1}]$ and the logarithmic terms lie in $M$. Comparing coefficients of $\theta^1$ gives $b_1' + 2x\, b_1 = 1$ for some $b_1 \in \mathbb{C}(x)$. If $b_1$ had a pole of order $e$ at some $\alpha$, then $b_1'$ would have one of order $e + 1$, and $2x b_1$ one of order at most $e$, so the left side would have a pole. So $b_1$ is a polynomial, and then $b_1' + 2x b_1$ has degree $\deg b_1 + 1 \ge 1$ (or is $0$ if $b_1 = 0$). Neither equals $1$. So the error function is not elementary. The same method shows that $\int e^x/x$ (the logarithmic integral after a substitution), $\int \sin x / x$ and $\int 1/\log x$ are not elementary.

**Rational functions.** For $F = C(x)$ with $C$ algebraically closed, the theorem gives the shape $\int A/D = v + \sum_i c_i \log u_i$ with $v, u_i \in C(x)$, which is the structure behind the [integration of rational functions](/integration-of-rational-functions/). The [Rothstein-Trager](/rothstein-trager/) resultant finds the $c_i$.

**The Risch algorithm.** For a tower of transcendental logarithms and exponentials over $C(x)$, the theorem reduces the integration problem to finding $v$ and the $c_i, u_i$ in the integrand's own field. The [Risch algorithm](/risch-algorithm/) does this level by level, by the same coefficient comparisons as in Cases 2 and 3. The [Risch structure theorem](/risch-structure-theorem/) decides whether a new $\theta$ is transcendental.

**Elementary solutions of differential equations.** The same proof technique underlies decision methods for elementary or Liouvillian solutions of linear differential equations, such as [Kovacic's algorithm](/kovacic-algorithm/), whose theory is [differential Galois theory](/differential-galois-theory/).

## Tightness

- **Logarithms are needed.** $f = 1/x$ in $F = \mathbb{C}(x)$ has no antiderivative $v \in F$, since a pole of $v$ of order $e$ gives a pole of $v'$ of order $e + 1 \ge 2$, and a polynomial $v$ gives a polynomial $v'$. So $m \ge 1$ is sometimes required, and $\int 1/x = \log x$.
- **Constants must be allowed to grow when $C$ is not algebraically closed.** For $F = \mathbb{Q}(x)$ and $f = 1/(x^2 - 2)$, every representation needs $c_i = \pm \sqrt{2}/4$, by the Rothstein-Trager theorem. So the statement over a non-closed $C$ must allow $c_i \in \overline{C}$.
- **The $u_i$ may not be avoidable even when $f$ is "simple".** $\int 1/(1 + x^2) = \arctan x$ is elementary over $\mathbb{C}$ only as $\frac{i}{2} \log \frac{x + i}{x - i}$, a logarithm with a non-real constant. Over $\mathbb{R}(x)$ with real constants, the theorem in the strict form fails, and arctangents are needed in a real-form answer.

## History

Liouville proved the first results on integration in finite terms in a series of memoirs from 1833 to 1841, including the non-elementarity of $\int e^{x^2}$ and the logarithmic form of elementary integrals of algebraic functions. Ostrowski (1946) recast the results in the language of differential fields. Ritt's book *Integration in Finite Terms* (1948) gave an analytic treatment. Rosenlicht (1968) gave the purely algebraic statement and proof followed above, and his 1972 Monthly article made it widely known. Risch (1969, 1970) turned the theorem into a decision procedure for transcendental elementary functions, and Bronstein's book is the modern account.

## References
