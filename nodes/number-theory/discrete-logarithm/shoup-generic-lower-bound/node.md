---
tag: Q58M0S
kind: theorem
slug: shoup-generic-lower-bound
name: Shoup's generic lower bound for discrete logarithms
aliases:
- Shoup's theorem
- Nechaev-Shoup bound
- birthday bound for the discrete logarithm
- generic lower bound for the DLP
area: number-theory/discrete-logarithm
level: research
summary: Any generic algorithm that solves the DLP in a group of prime order q with constant probability needs Omega(q^(1/2)) group operations.
prereqs: [generic-group-model, discrete-logarithm-problem, schwartz-zippel-lemma, union-bound]
see_also: [baby-step-giant-step, pollard-rho-discrete-logarithm, pohlig-hellman, computational-diffie-hellman, decisional-diffie-hellman, index-calculus, comparison-sort-lower-bound, birthday-paradox]
sources:
  - paper: doi:10.1007/3-540-69053-0_18
    title: Victor Shoup, Lower bounds for discrete logarithms and related problems, EUROCRYPT 1997, Lecture Notes in Computer Science 1233
    locator: pages 256 to 266 (the model with random encodings, the bound O(m^2/q) for discrete logarithms in a group whose largest prime factor of the order is q, and the bounds for the Diffie-Hellman problems)
  - paper: doi:10.1007/bf02113297
    title: V. I. Nechaev, Complexity of a determinate algorithm for the discrete logarithm, Mathematical Notes 55(2), 1994
    locator: pages 165 to 172 (the square root lower bound for deterministic algorithms with free equality tests)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 13, Section 13.4 (Definition 13.4.1 of Shoup's model, Section 13.4.2 on Maurer's model, Lemma 13.4.4, Theorem 13.4.5 with the bound (m + 2)^2/(2r), and Corollary 13.4.7)
  - paper: doi:10.1007/11586821_1
    title: Ueli Maurer, Abstract models of computation in cryptography, Cryptography and Coding 2005, Lecture Notes in Computer Science
    locator: pages 1 to 12 (the model without encodings, with registers and an equality oracle, and the lower bounds in it)
  - paper: doi:10.1007/978-3-319-78375-8_14
    title: Henry Corrigan-Gibbs and Dmitry Kogan, The discrete-logarithm problem with preprocessing, EUROCRYPT 2018, Lecture Notes in Computer Science
    locator: pages 415 to 447 (generic algorithms that may use advice computed in advance, and the matching lower bound)
  - paper: doi:10.1007/978-3-642-34931-7_19
    title: Daniel J. Bernstein and Tanja Lange, Computing small discrete logarithms faster, INDOCRYPT 2012, Lecture Notes in Computer Science
    locator: pages 317 to 338 (a precomputed table of distinguished points that makes each later logarithm cost about the cube root of the group order)
  - paper: doi:10.1007/3-540-36178-2_6
    title: Alexander W. Dent, Adapting the weaknesses of the random oracle model to the generic group model, ASIACRYPT 2002, Lecture Notes in Computer Science
    locator: pages 100 to 109 (a scheme that is secure in the generic group model but insecure for every concrete encoding)
---

Shoup's theorem says that a [generic algorithm](/generic-group-model/), one that treats group elements as opaque labels and only multiplies and compares them, cannot solve the [discrete logarithm problem](/discrete-logarithm-problem/) quickly. In a cyclic group of prime order $q$, an algorithm that makes $m$ group operations finds the logarithm with probability at most $(m + 2)^2 / (2q)$, so a constant success probability needs $\Omega(\sqrt q)$ operations. [Baby-step giant-step](/baby-step-giant-step/) and [Pollard's rho](/pollard-rho-discrete-logarithm/) reach this bound, so they are optimal among generic algorithms. Nechaev proved the first such bound in 1994 for deterministic algorithms, and Shoup in 1997 gave the model with random encodings, which covers randomized algorithms and extends to the Diffie-Hellman problems. The theorem is the formal reason why groups of prime order near $2^{256}$ are said to give $128$ bits of security when no better than generic attack is known, as for most elliptic curves.

## Statement

**The model.** Let $G = \langle g \rangle$ be a cyclic group of prime order $q$, and let $S$ be a set of bit strings with $|S| \ge q$. An *encoding* is an injective map $\sigma : G \to S$. A generic algorithm $A$ receives $q$ and the list $(\sigma(g), \sigma(h))$. It has an oracle that takes two indices $i, j$ into its current list of encodings, $\sigma(u_i)$ and $\sigma(u_j)$, and appends $\sigma(u_i u_j^{-1})$ to the list. One oracle call is one *query*. From $\sigma(1) = $ the answer to $(i, i)$, it gets inverses, and products cost two queries. Apart from that, $A$ may do any computation on the strings it holds and use random coins. At the end it outputs an integer $b$.

**Theorem (Shoup, 1997; Galbraith, Theorem 13.4.5).** Let $A$ be a generic algorithm that makes at most $m$ queries. Let $x \in \mathbb{Z}/q\mathbb{Z}$ and the encoding $\sigma$ be chosen uniformly at random, independently of each other and of the coins of $A$, and let $h = g^x$. Then

$$\Pr[A(q; \sigma(g), \sigma(h)) = x] \le \frac{1}{q}\left(\binom{m + 2}{2} + 1\right) \le \frac{(m + 2)^2}{2q}.$$

**Corollary.** If $A$ succeeds with probability at least $\varepsilon$, then $m \ge \sqrt{2 \varepsilon q} - 2$. For $\varepsilon = 1/2$ this is $m \ge \sqrt q - 2$, and for $\varepsilon = 1/\log^c q$ it is $\Omega(\sqrt{q / \log^c q})$ (Galbraith, Corollary 13.4.7).

**Composite order.** Shoup states the bound for a cyclic group of any order $n$: if $q$ is the largest prime factor of $n$, the success probability is $O(m^2/q)$. So a generic algorithm needs $\Omega(\sqrt q)$ queries, and [Pohlig-Hellman](/pohlig-hellman/) with baby-step giant-step, which uses $O(\sqrt q \log n + \log^2 n)$, is optimal up to logarithmic factors.

The bound is over the random encoding and the random instance. It says nothing about one fixed group with its natural encoding, such as $(\mathbb{Z}/p\mathbb{Z})^*$ with integers, where [index calculus](/index-calculus/) is much faster. Such algorithms use the encoding, so they are not generic.

## In plain words

Imagine the group elements are locked boxes with random stickers. You can ask a clerk to combine two boxes into a new one, and you can see whether two boxes carry the same sticker, but you can never look inside. The only useful event is when two different recipes give the same box, because that equation reveals the secret exponent.

Each box you build is a recipe "so many copies of the base, so many copies of the target". Two different recipes give the same box only for one value of the secret. With $k$ boxes there are about $k^2/2$ pairs, so you catch the secret with chance about $k^2/(2q)$. Unless you get lucky, you learn nothing, and your final guess is right with chance only $1/q$. To have a fair chance you need about $\sqrt q$ boxes.

## Proof

Fix the coins of $A$; a bound that holds for every fixed choice of coins holds for their average. We write the group additively in the exponent: every element that $A$ holds is $g^{F(x)}$ for a polynomial $F(X) = \alpha + \beta X \in \mathbb{F}_q[X]$ that we can track. The two inputs are $F_1 = 1$ and $F_2 = X$, and a query on indices $i, j$ appends $F_t = F_i - F_j$. All these polynomials have degree at most $1$.

**Two games.** In the *real game*, $x$ is uniform in $\mathbb{F}_q$ and the answer to the query that appends $F_t$ is $\sigma(g^{F_t(x)})$ for a uniform injective $\sigma$. We generate $\sigma$ lazily: a random injective map can be sampled one value at a time, giving each new group element a string chosen uniformly among the strings not yet used. So in the real game, if $F_t(x) = F_s(x)$ for an earlier $s$, the answer is the string of $F_s$, and otherwise it is a fresh string. In the *formal game*, the answer for $F_t$ is the string of $F_s$ if $F_t = F_s$ as polynomials for an earlier $s$, and a fresh string otherwise; $x$ is chosen at the end. Run both games with the same sequence of fresh strings, so the $u$-th fresh string is the same in both.

**Identical until bad.** Let $E$ be the event that the formal game produces two polynomials $F_s \ne F_t$ with $F_s(x) = F_t(x)$. If $E$ does not happen, then for every query, $F_t(x)$ equals an earlier value $F_s(x)$ exactly when $F_t = F_s$, so the two games give the same answer at every step, by induction on the queries, and $A$ outputs the same $b$ in both. Hence

$$\Pr[\text{real win}] \le \Pr[E] + \Pr[\text{real win} \wedge \neg E] = \Pr[E] + \Pr[\text{formal win} \wedge \neg E] \le \Pr[E] + \Pr[\text{formal win}].$$

**The guess.** In the formal game the answers, and therefore the output $b$, do not depend on $x$, because $x$ is chosen after $A$ stops. So $\Pr[\text{formal win}] = \Pr[b = x] = 1/q$.

**The bad event.** The formal game produces a list of polynomials that does not depend on $x$, and it has at most $k \le m + 2$ distinct members: the two inputs and one per query. For each pair $F_s \ne F_t$, the difference $F_s - F_t$ is a nonzero polynomial of degree at most $1$, which has at most one root in $\mathbb{F}_q$, so $\Pr[F_s(x) = F_t(x)] \le 1/q$; this is the case $d = 1$ of the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/). By the [union bound](/union-bound/) over the $\binom{k}{2}$ pairs, $\Pr[E] \le \binom{m + 2}{2}/q$.

**Conclusion.** Adding the two parts gives $\Pr[\text{real win}] \le (\binom{m + 2}{2} + 1)/q$. Finally $\binom{m + 2}{2} + 1 = ((m + 2)(m + 1) + 2)/2 \le (m + 2)^2/2$, because $(m + 2)(m + 1) + 2 \le (m + 2)^2$ is equivalent to $2 \le m + 2$. The corollary follows by solving $(m + 2)^2/(2q) \ge \varepsilon$ for $m$. $\blacksquare$

The proof uses only that every value $A$ sees is a fixed linear form in $x$, so it also bounds algorithms that receive more inputs, as long as each input is $g^{F(x)}$ for a known polynomial of low degree. This is how the same argument gives bounds for the [computational](/computational-diffie-hellman/) and [decisional Diffie-Hellman](/decisional-diffie-hellman/) problems. There the inputs are $1, X, Y$ (and a third element for the decision problem), the polynomials have two or three variables, and the target $XY$ has degree $2$, so the Schwartz-Zippel lemma is used with degree at most $2$.

## Consequences

- **Optimality of the square root algorithms.** Baby-step giant-step uses about $2\sqrt q$ group operations in the worst case, and Pollard's rho about $\sqrt{\pi q / 2}$ in expectation under the random walk heuristic, so both are optimal for generic algorithms up to a constant factor.
- **Security levels.** For $q \approx 2^{256}$ and $m = 2^{100}$ queries, the success probability is at most $(2^{100} + 2)^2/2^{257} \approx 2^{-57}$. Success $1/2$ needs about $2^{128}$ queries. This is the source of the rule that a prime order group gives half its bit length in security, when the best attack is generic.
- **Group order.** Since the bound depends on the largest prime factor of the order, groups for cryptography have a large prime order, and Pohlig-Hellman shows that nothing more is needed against generic attacks.
- **Diffie-Hellman.** Shoup proved $\Omega(\sqrt q)$ bounds also for computing $g^{xy}$ from $g^x, g^y$ and for distinguishing it from a random element, so in the generic model the Diffie-Hellman problems are as hard as the logarithm.
- **What the bound does not say.** It does not rule out faster algorithms for any concrete group. Index calculus and the number field sieve beat it in $(\mathbb{Z}/p\mathbb{Z})^*$, and the [MOV reduction](/menezes-okamoto-vanstone-reduction/) beats it on curves of small embedding degree, because they use the representation of the elements. Dent (ASIACRYPT 2002) built schemes that are secure in the generic model but insecure for every concrete encoding, so a proof in the model is a heuristic argument about real groups.

## Tightness

**The exponent $1/2$ is tight.** The square root algorithms above match the bound up to a constant factor.

**The constant.** In the proof, a generic algorithm wins either through a collision, which reveals $x$, or through its final guess. An algorithm that holds $k$ elements whose pairwise differences have distinct roots, and guesses a value outside those roots, wins with probability exactly $(\binom{k}{2} + 1)/q$, so the first bound of the theorem is exact in terms of the number $k$ of distinct elements seen. The loss is in building elements with few queries. Baby-step giant-step with $b$ baby steps and $c$ giant steps uses about $b + c$ queries and covers $bc$ exponents, so with $m$ queries it wins with probability about $m^2/(4q)$, a factor $2$ below the bound. A random walk that subtracts one of a few precomputed random elements at each query makes one new element per query, and its pairwise roots are mostly distinct: in one run with $q = 1000003$, $32$ precomputed steps and $400$ points, the $79800$ pairs gave $73831$ distinct roots, about $92$ percent. So such walks reach about $0.9 \, m^2 / (2q)$, close to the bound.

**Small cases.** For $q = 101$, an exhaustive search over all query sequences gives the best possible number of winning values of $x$ for each budget $m$. Adaptivity does not help: until a collision the answers are fresh strings that carry no information, and at the first collision the algorithm already knows $x$.

| $m$ | best wins | $\binom{m+2}{2} + 1$ | $(m + 2)^2/2$ |
|---|---|---|---|
| 0 | 2 | 2 | 2 |
| 1 | 4 | 4 | 4.5 |
| 2 | 5 | 7 | 8 |
| 3 | 7 | 11 | 12.5 |
| 4 | 10 | 16 | 18 |

With no queries the algorithm wins on $x = 1$, where $h = g$, and on its guess. With four queries, one optimal sequence builds the exponents $1, X, X - 1, X - 2, -2, 3 - X$, whose $15$ pairs give $9$ distinct roots, and wins on those $9$ values and its guess.

**Preprocessing.** If the algorithm may keep advice of $S$ group elements that depends on $g$ but not on $h$, the bound changes. Bernstein and Lange showed that a table of about $q^{1/3}$ elements, computed once with about $q^{2/3}$ operations, allows each logarithm in about $q^{1/3}$ operations. Corrigan-Gibbs and Kogan proved that any generic algorithm with advice of size $S$, time $T$ and success probability $\varepsilon$ needs $S T^2 = \tilde\Omega(\varepsilon q)$, which this construction meets with $S = T = q^{1/3}$.

**Other models.** In Maurer's model, without encodings, the algorithm sees only the results of equality tests on its registers. A similar bound holds there if equality tests are not counted, or if an order relation on the registers is allowed (Galbraith, Section 13.4.3); baby-step giant-step and rho need such an order to sort or hash their elements. Nechaev's model has free equality tests and covers only deterministic algorithms.

## History

Babai and Szemerédi in 1984 introduced black box groups, with elements given as strings and the operations as oracles, to study matrix group problems. Nechaev in 1994 proved an $\Omega(\sqrt q)$ lower bound on time and space for deterministic algorithms that compute discrete logarithms by group operations and equality tests. Shoup in 1997 introduced random encodings, which allowed randomized algorithms, proved the bound $O(m^2/q)$ for the logarithm and for the Diffie-Hellman problems, and gave the proof by the polynomial argument used above, crediting the root bound to Schwartz. Maurer in 2005 gave the register model without encodings. The model and the bound became a standard tool for arguing the security of schemes in pairing groups and other settings where the problems are new, and Corrigan-Gibbs and Kogan in 2018 extended it to algorithms with preprocessing.

## References
