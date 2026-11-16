---
tag: BNB7XF
kind: theorem
slug: ip-equals-pspace
name: IP = PSPACE
aliases:
- Shamir's theorem
area: complexity/complexity-classes
level: research
summary: "Interactive proofs with a randomized polynomial-time verifier decide exactly the languages in PSPACE. Proved with arithmetization by Lund, Fortnow, Karloff and Nisan and by Shamir."
prereqs: [interactive-proofs, pspace, qbf, polynomial-interpolation]
see_also: [interactive-proofs, model-counting, schwartz-zippel-lemma, relativization, algebrization-barrier, mip-equals-nexp, pcp-theorem, arthur-merlin]
sources:
  - paper: doi:10.1145/146585.146605
    title: Carsten Lund, Lance Fortnow, Howard Karloff and Noam Nisan, Algebraic methods for interactive proof systems, Journal of the ACM 39(4), 859 to 868 (1992)
    locator: the sum-check protocol and the interactive proof for the permanent, which puts P^#P in IP; preliminary version in FOCS 1990
  - paper: doi:10.1145/146585.146609
    title: Adi Shamir, IP = PSPACE, Journal of the ACM 39(4), 869 to 877 (1992)
    locator: the interactive proof for quantified Boolean formulas; preliminary version in FOCS 1990
  - paper: doi:10.1145/146585.146613
    title: Alexander Shen, IP = PSPACE, simplified proof, Journal of the ACM 39(4), 878 to 880 (1992)
    locator: the linearization operator that keeps the degrees small
  - paper: doi:10.1016/S0022-0000(05)80084-4
    title: Richard Chang, Benny Chor, Oded Goldreich, Juris Hartmanis, Johan Håstad, Desh Ranjan and Pankaj Rohatgi, The random oracle hypothesis is false, Journal of Computer and System Sciences 49(1), 24 to 39 (1994)
    locator: IP^A differs from PSPACE^A for almost every oracle A
  - paper: doi:10.1016/0020-0190(88)90199-8
    title: Lance Fortnow and Michael Sipser, Are there interactive protocols for co-NP languages?, Information Processing Letters 28(5), 249 to 251 (1988)
    locator: an oracle relative to which coNP has no interactive proof
  - paper: doi:10.1145/2049697.2049704
    title: Rahul Jain, Zhengfeng Ji, Sarvagya Upadhyay and John Watrous, QIP = PSPACE, Journal of the ACM 58(6) (2011)
    locator: the main theorem
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 8, Interactive proofs (the sum-check protocol, IP = PSPACE)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage (2013)
    locator: Section 10.4, Interactive proof systems (IP = PSPACE)
  - book: isbn:9780521884730
    title: Oded Goldreich, Computational Complexity, A Conceptual Perspective, Cambridge University Press (2008)
    locator: Chapter 9, Probabilistic proof systems (the power of interactive proofs)
---

The theorem IP = PSPACE says that the languages with an [interactive proof](/interactive-proofs/) are exactly the languages decidable in polynomial space. One direction is easy: the best prover can be found in polynomial space. The other direction was the surprise. Lund, Fortnow, Karloff and Nisan found the sum-check protocol, which gives an interactive proof for counting problems, and a few weeks later Shamir extended it to quantified Boolean formulas, which are complete for [PSPACE](/pspace/). Both proofs turn a formula into a polynomial over a finite field and let the verifier check the polynomial at random points.

## Statement

**Theorem.** $\mathsf{IP} = \mathsf{PSPACE}$.

Here IP is the class of languages with an interactive proof: a probabilistic polynomial-time verifier on a [multitape Turing machine](/multitape-turing-machine/), a prover with no bound on its power, polynomially many messages, completeness at least $2/3$ and soundness error at most $1/3$. PSPACE is the class of languages decided by a deterministic multitape machine in polynomial space. The proof gives more than the statement:

- Every language in PSPACE has an interactive proof with *perfect completeness* (the honest prover is accepted with probability $1$) and with *public coins* (the verifier sends its random bits in the open).
- The honest prover for a language in PSPACE can itself run in polynomial space.

## In plain words

A prover wants to convince a verifier that a hard statement is true, for example a formula with many nested "for all" and "there exists" parts. The verifier is too slow to check the statement itself. So it turns the statement into a polynomial and asks the prover for a small piece of it, one variable at a time. The verifier checks that each piece fits the previous claim, then picks a random number and asks about that point next. A false claim can only survive if the random number hits one of the few places where a fake polynomial agrees with the true one. At the end, the verifier can compute the last value alone. The reverse direction is simpler: a machine with polynomial memory can try all prover answers one by one.

## Proof

### IP is a subset of PSPACE

Let $V$ be a verifier with $k$ messages that uses $\ell$ random bits, where $k$ and $\ell$ are polynomial in $n = |x|$. We show that the largest acceptance probability over all provers can be computed in polynomial space; then $x \in L$ if and only if this value is at least $2/3$.

For a partial transcript $h$, let $R(h)$ be the set of random strings $r \in \{0,1\}^\ell$ such that $V$, with input $x$ and coins $r$, would send exactly the verifier messages in $h$ when it receives the prover messages in $h$. Define $N(h)$ by recursion:

- if $h$ is complete, $N(h)$ is the number of $r \in R(h)$ such that $V$ accepts on $x$, $r$ and $h$;
- if the next message is from the prover, $N(h) = \max_m N(hm)$ over all messages $m$ of the allowed length;
- if the next message is from the verifier, $N(h) = \sum_m N(hm)$ over all messages $m$.

*Claim:* $\max_P \Pr_r[\langle V, P\rangle(x) = 1] = N(\varepsilon)/2^\ell$, where $\varepsilon$ is the empty transcript. Induction on the number of messages still to come shows that, for every $h$, no prover strategy that continues from $h$ makes more than $N(h)$ strings in $R(h)$ accept. At a verifier step the sets $R(hm)$ for different $m$ split $R(h)$, so the counts add. At a prover step the prover sees only $h$, not $r$, so it must send the same $m$ for all $r \in R(h)$, and the best it can do is the maximum. The prover that always sends a message that reaches the maximum is a valid strategy, because its choice depends only on $h$, and it reaches $N(h)$ exactly.

*Space.* The recursion has depth $k$. Each level stores one message and one counter of at most $\ell + 1$ bits. A leaf enumerates the $2^\ell$ strings $r$ one at a time and runs $V$ on each, which needs polynomial space and can reuse it. So the total space is polynomial in $n$. $\square$

### The sum-check protocol

Fix a prime $p$ and the field $\mathbb{F}_p$. Let $g(x_1, \ldots, x_n)$ be a polynomial over $\mathbb{F}_p$ of degree at most $d_i$ in $x_i$, and suppose that the verifier can compute $g$ at any point in polynomial time. The prover claims that

$$\sum_{b_1 \in \{0,1\}} \cdots \sum_{b_n \in \{0,1\}} g(b_1, \ldots, b_n) = K \pmod p.$$

**Protocol.** Set $c_0 = K$. In round $i = 1, \ldots, n$, the prover sends a univariate polynomial $s_i(X)$ of degree at most $d_i$, by its $d_i + 1$ coefficients. The honest choice is

$$s_i(X) = \sum_{b_{i+1}, \ldots, b_n \in \{0,1\}} g(r_1, \ldots, r_{i-1}, X, b_{i+1}, \ldots, b_n).$$

The verifier checks $s_i(0) + s_i(1) = c_{i-1}$ and rejects if the check fails. Then it picks $r_i \in \mathbb{F}_p$ uniformly, sends it, and sets $c_i = s_i(r_i)$. After round $n$ the verifier computes $g(r_1, \ldots, r_n)$ itself and accepts if it equals $c_n$.

**Completeness.** If the claim is true, the honest polynomials pass every check, so the verifier accepts with probability $1$.

**Soundness.** If the claim is false, the verifier accepts with probability at most $\sum_i d_i / p$. Let $s_i^*$ be the honest polynomial of round $i$, computed with the $r_j$ actually chosen. Suppose $c_{i-1}$ is false, that is $c_{i-1} \ne s_i^*(0) + s_i^*(1)$. If the prover sends $s_i = s_i^*$, the check of round $i$ fails. Otherwise $s_i - s_i^*$ is a nonzero polynomial of degree at most $d_i$, so it has at most $d_i$ roots, and $\Pr[s_i(r_i) = s_i^*(r_i)] \le d_i / p$. Outside this event, $c_i = s_i(r_i)$ is false again. If the claim $c_n$ is still false after round $n$, the final check fails. By the [union bound](/union-bound/), the probability that some round turns a false claim into a true one is at most $\sum_i d_i / p$. This is the one-variable case of the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), used once per round.

**Arithmetization of a CNF formula.** For a CNF formula $\varphi$ with $m$ clauses, replace a literal $x$ by $x$, a literal $\lnot x$ by $1 - x$, a clause $\ell_1 \lor \cdots \lor \ell_t$ by $1 - (1 - \ell_1) \cdots (1 - \ell_t)$, and the conjunction by the product. The result $\tilde\varphi$ equals $\varphi$ on every point of $\{0,1\}^n$, its degree in $x_i$ is at most the number of clauses that contain $x_i$, and the verifier can evaluate it in time polynomial in the size of $\varphi$. The sum of $\tilde\varphi$ over $\{0,1\}^n$ is the number of satisfying assignments ([model counting](/model-counting/)). With a prime $p > 2^n$, this number is less than $p$, so the claim modulo $p$ fixes it. The prover sends $p$ and the verifier checks that it is prime in polynomial time with the [AKS primality test](/aks-primality-test/). The soundness error is then at most $\sum_i d_i / p \le 3m / 2^n$ for a 3-CNF formula, which is small for $n$ large. This puts the counting problem, and with it $\mathsf{coNP}$ and $\mathsf{P}^{\#\mathsf{P}}$, in IP.

**Worked example.** Take $\varphi = (x_1 \lor x_2 \lor \lnot x_3) \land (\lnot x_1 \lor x_3) \land (x_2 \lor x_3)$ and $p = 97$. Then

$$\tilde\varphi = \big(1 - (1 - x_1)(1 - x_2)\,x_3\big)\big(1 - x_1 (1 - x_3)\big)\big(1 - (1 - x_2)(1 - x_3)\big).$$

On $\{0,1\}^3$ it is $1$ exactly at $(0,1,0)$, $(0,1,1)$, $(1,0,1)$ and $(1,1,1)$, so the true count is $K = 4$. The degrees are $d_1 = 2$, $d_2 = 2$ and $d_3 = 3$, because $x_3$ occurs in all three clauses. A run of the protocol with the honest prover and random choices from a fixed seed:

| round | prover sends $s_i(X)$ | check $s_i(0) + s_i(1)$ | $r_i$ | new claim $c_i$ |
|---|---|---|---|---|
| 1 | $2$ | $4 = c_0$ | $17$ | $2$ |
| 2 | $17 + 65X$ | $99 \equiv 2 = c_1$ | $72$ | $41$ |
| 3 | $12 + 77X + 77X^2 + 57X^3$ | $235 \equiv 41 = c_2$ | $8$ | $14$ |

The verifier then computes $\tilde\varphi(17, 72, 8) \bmod 97 = 14$ and accepts. Now let a cheating prover claim $K = 5$. In each round where its current claim is false, it sends the honest polynomial plus $c\,(X - 3)(X - 4)$, or $c\,(X - 3)(X - 4)(X - 5)$ in round 3, with $c$ chosen so that the check passes. Its claim becomes true only if $r_i$ hits one of these roots, so it wins with probability $1 - (95/97)^2 (94/97) = 64323/912673 \approx 0.0705$, just under the bound $\sum_i d_i / p = 7/97 \approx 0.0722$.

### PSPACE is a subset of IP

The problem TQBF of deciding a fully quantified Boolean formula ([QBF](/qbf/)) is PSPACE-complete under polynomial-time many-one reductions, and IP is closed under these reductions: the verifier computes the reduction and runs the protocol on the image. So it suffices to give an interactive proof for TQBF. Let

$$\Psi = Q_1 x_1\, Q_2 x_2 \cdots Q_n x_n\; \varphi(x_1, \ldots, x_n), \qquad Q_i \in \{\forall, \exists\},$$

with $\varphi$ a 3-CNF formula with $m$ clauses.

**Operators.** For a polynomial $f$ and a variable $x$, define

$$\forall_x f = f|_{x=0} \cdot f|_{x=1}, \qquad \exists_x f = 1 - (1 - f|_{x=0})(1 - f|_{x=1}), \qquad L_x f = (1 - x)\, f|_{x=0} + x\, f|_{x=1}.$$

On inputs in $\{0,1\}$, $\forall_x$ is the AND and $\exists_x$ is the OR of the two values. The *linearization* $L_x f$ is linear in $x$ and agrees with $f$ when $x \in \{0,1\}$. Without it, each $\forall_x$ can double the degree of the remaining variables, and $n$ nested products give degree up to $2^n$, so the prover could not send the polynomials.

**The expression.** Following Shen, consider

$$Q_1 x_1\, L_{x_1}\; Q_2 x_2\, L_{x_1} L_{x_2}\; Q_3 x_3\, L_{x_1} L_{x_2} L_{x_3} \cdots Q_n x_n\, L_{x_1} \cdots L_{x_n}\; \tilde\varphi,$$

where each $Q_i x_i$ is the operator $\forall_{x_i}$ or $\exists_{x_i}$ and the operators apply from right to left. Its value is a constant, since every variable is bound. On Boolean values the $L$ operators change nothing and the quantifier operators compute AND and OR, so the value is $1$ if $\Psi$ is true and $0$ if it is false. There are $k = n + n(n+1)/2$ operators. After each $L$ the polynomial is linear in that variable, and a $\forall$ or $\exists$ of polynomials linear in the other variables has degree at most $2$ in each of them. So every univariate polynomial in the protocol has degree at most $D = \max(2, m)$, where $m$ bounds the degree of $\tilde\varphi$ in one variable.

**Protocol.** The prover claims that the value is $1$. The verifier removes the operators one at a time, from the outside in, and keeps a claim of the form "the expression that remains, at the current point, has value $c$". Let the next operator act on $x_i$, and let $f$ be the expression after it. The prover sends $s(X)$, which it claims is $f$ with $x_i = X$ and the other free variables at their current values. The verifier checks

$$s(0)\, s(1) = c \;\text{ for } \forall, \qquad 1 - (1 - s(0))(1 - s(1)) = c \;\text{ for } \exists, \qquad (1 - a_i)\, s(0) + a_i\, s(1) = c \;\text{ for } L_{x_i},$$

where $a_i$ is the current value of the free variable $x_i$. Then it picks $z \in \mathbb{F}_p$ uniformly, sets $x_i := z$ and $c := s(z)$. After the last operator it evaluates $\tilde\varphi$ at the current point and compares with $c$.

**Analysis.** The honest prover passes every check, so completeness is $1$. The soundness argument is the same as for sum-check: in each round a false claim stays false unless $z$ is a root of the nonzero difference $s - s^*$, which has probability at most $D/p$. So a false formula is accepted with probability at most $kD/p$. Any prime $p > 3kD$, which has $O(\log n + \log m)$ bits, gives soundness error at most $1/3$. The values $0$ and $1$ differ modulo every prime, so a small field suffices. The verifier sends only its random field elements, so the coins are public. The honest prover needs to evaluate the expression at points of $\mathbb{F}_p$, which it can do by recursion in polynomial space. $\square$

**Worked example.** Take $\Psi = \forall x\, \exists y\; (x \lor y) \land (\lnot x \lor \lnot y)$, which is true (choose $y = \lnot x$). Here $\tilde\varphi = (x + y - xy)(1 - xy)$, with $\tilde\varphi(x, 0) = x$ and $\tilde\varphi(x, 1) = 1 - x$. The operator $\exists_y$ gives $1 - (1 - x)\,x = 1 - x + x^2$. This has degree $2$ but equals $1$ at $x = 0$ and $x = 1$, and $L_x$ turns it into the constant $1$, so $\forall_x$ gives $1$. A run of the protocol on $\forall_x L_x \exists_y L_x L_y \tilde\varphi$ with $p = 97$ and a fixed seed:

| step | operator | $s(0), s(1), s(2)$ | check | $z$ | new claim |
|---|---|---|---|---|---|
| 1 | $\forall_x$ | $1, 1, 1$ | $1 \cdot 1 = 1$ | $x := 7$ | $1$ |
| 2 | $L_x$ | $1, 1, 3$ | $(1 - 7) \cdot 1 + 7 \cdot 1 = 1$ | $x := 11$ | $14$ |
| 3 | $\exists_y$ | $11, 87, 66$ | $1 - (1 - 11)(1 - 87) \equiv 14$ | $y := 10$ | $92$ |
| 4 | $L_x$ | $10, 88, 69$ | $(1 - 11) \cdot 10 + 11 \cdot 88 \equiv 92$ | $x := 46$ | $9$ |
| 5 | $L_y$ | $46, 52, 27$ | $(1 - 10) \cdot 46 + 10 \cdot 52 \equiv 9$ | $y := 21$ | $64$ |

In step 2 the prover sends $1 - X + X^2$, and its value at $11$ is $111 \equiv 14$. In step 3 the polynomial in $y$ is linear, $11 + 76Y$. At the end the verifier computes $\tilde\varphi(46, 21) \bmod 97 = 64$ and accepts. Each polynomial has degree at most $2$, so the soundness error of this run is at most $5 \cdot 2 / 97 = 10/97$.

## Consequences

- *Perfect completeness and public coins.* Every language in IP has a public-coin protocol with perfect completeness, so IP equals the class of [Arthur-Merlin](/arthur-merlin/) games with polynomially many rounds.
- *Counting and the hierarchy.* $\mathsf{coNP} \subseteq \mathsf{IP}$ and $\mathsf{P}^{\#\mathsf{P}} \subseteq \mathsf{IP}$. By [Toda's theorem](/toda-theorem/), the whole [polynomial hierarchy](/polynomial-hierarchy/) is in IP; IP = PSPACE gives this directly as well.
- *A technique that does not relativize.* Fortnow and Sipser (1988) gave an oracle $A$ with $\mathsf{coNP}^A \not\subseteq \mathsf{IP}^A$, and Chang and others (1994) showed that $\mathsf{IP}^A \ne \mathsf{PSPACE}^A$ for almost every oracle $A$. So the proof cannot [relativize](/relativization/). Arithmetization was the first strong nonrelativizing technique, and the [algebrization barrier](/algebrization-barrier/) of Aaronson and Wigderson describes its limits.
- *Multi-prover proofs and PCPs.* The same tools, with several provers or with a fixed proof string, give [MIP = NEXP](/mip-equals-nexp/) and later the [PCP theorem](/pcp-theorem/).
- *Quantum provers.* The quantum analogue QIP also equals PSPACE (Jain, Ji, Upadhyay and Watrous 2011).

## Tightness

- *Many rounds are needed unless the hierarchy collapses.* With a constant number of messages, an interactive proof gives only languages in AM, and $\mathsf{AM} \subseteq \Pi_2^p$. So if PSPACE had constant-round interactive proofs, then $\mathsf{PSPACE} = \Pi_2^p$ and the polynomial hierarchy would collapse to its second level. The protocol above uses $O(n^2)$ rounds.
- *The power of the prover.* The honest prover of the TQBF protocol evaluates expressions whose values decide a PSPACE-complete problem, and for the counting problem a $\#\mathsf{P}$ oracle suffices. A prover that runs in polynomial time can only prove statements that it can decide, so the theorem is about provers of unbounded power.
- *The field size.* The soundness bound $kD/p$ needs $p$ larger than the total degree that the rounds can lose. In the sum-check example, $p = 97$ gives about $7\%$ error for one run, and a larger prime or repetition makes it smaller.

## History

Goldwasser, Micali and Rackoff and Babai defined interactive proofs in 1985, and the inclusion $\mathsf{IP} \subseteq \mathsf{PSPACE}$ followed from the definition. Fortnow and Sipser (1988) gave an oracle relative to which coNP has no interactive proofs, so many expected that coNP is not in IP. In late 1989 Nisan showed that the permanent has a multi-prover proof, and within weeks Lund, Fortnow and Karloff joined him to give a one-prover proof for the permanent, which puts $\mathsf{P}^{\#\mathsf{P}}$ in IP. Shamir then extended the method to quantified Boolean formulas. Both papers appeared at FOCS 1990 and in the same issue of the Journal of the ACM in 1992, together with Shen's note that introduced the linearization operator used above.

## References
