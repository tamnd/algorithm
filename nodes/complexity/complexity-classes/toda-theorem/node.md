---
tag: V5GD7A
kind: theorem
slug: toda-theorem
name: Toda's theorem
aliases:
- PH in P^#P
area: complexity/complexity-classes
level: research
summary: The whole polynomial hierarchy is contained in P with a PP oracle, equivalently with one query to a #P function. The proof combines random hashing with a counting trick modulo powers of 2.
prereqs: [polynomial-hierarchy, pp, valiant-vazirani-theorem]
see_also: [pp, polynomial-hierarchy, valiant-vazirani-theorem, model-counting, permanent-computation, sipser-gacs-theorem, karp-lipton-theorem, counting-problem]
sources:
  - paper: doi:10.1137/0220053
    title: Seinosuke Toda, PP is as hard as the polynomial-time hierarchy, SIAM Journal on Computing 20(5), 865 to 877 (1991)
    locator: the main theorem and the two lemmas (PH in BP.parityP, and BP.parityP in P^#P)
  - paper: doi:10.4086/toc.2009.v005a007
    title: Lance Fortnow, A simple proof of Toda's theorem, Theory of Computing 5, 135 to 140 (2009)
    locator: the short proof of the first step
  - paper: doi:10.1016/0304-3975(86)90135-0
    title: Leslie G. Valiant and Vijay V. Vazirani, NP is as easy as detecting unique solutions, Theoretical Computer Science 47, 85 to 93 (1986)
    locator: the isolation lemma by random hashing
  - paper: doi:10.1137/0221023
    title: Seinosuke Toda and Mitsunori Ogiwara, Counting classes are at least as hard as the polynomial-time hierarchy, SIAM Journal on Computing 21(2), 316 to 328 (1992)
    locator: the extension to other counting classes
  - paper: doi:10.1007/BF01263422
    title: Richard Beigel, Perceptrons, PP, and the polynomial hierarchy, Computational Complexity 4(4), 339 to 349 (1994)
    locator: the oracle relative to which P^NP is not in PP
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 17, Complexity of counting (Toda's theorem)
---

Toda's theorem says that a polynomial-time machine that may ask a counting oracle can decide every problem in the [polynomial hierarchy](/polynomial-hierarchy/): $\mathsf{PH} \subseteq \mathsf{P}^{\mathsf{PP}} = \mathsf{P}^{\#\mathsf{P}}$. The hierarchy uses any fixed number of alternating quantifiers, and the theorem says that counting the solutions of one formula is at least as hard as all of them. The proof has two steps. A randomized reduction with random hashing puts PH inside $\mathsf{BP} \cdot \oplus\mathsf{P}$, randomized algorithms with a parity oracle, and a counting step then removes both the randomness and the parity with one #P query. Toda published it in 1989, with the journal version in 1991, and received the 1998 Gödel Prize for it.

## Statement

**Classes.** #P is the class of functions $f : \{0,1\}^* \to \mathbb{N}$ such that $f(x)$ is the number of accepting paths of a polynomial-time [nondeterministic Turing machine](/nondeterministic-turing-machine/) on $x$. Its basic complete function is #SAT, the number of satisfying assignments of a formula ([model counting](/model-counting/)). [PP](/pp/) is the class of languages $\{x : f(x) > g(x)\}$ for #P functions $f, g$, and $\mathsf{P}^{\mathsf{PP}} = \mathsf{P}^{\#\mathsf{P}}$. The class $\oplus\mathsf{P}$ is the set of languages $\{x : f(x) \text{ is odd}\}$ for $f \in \#\mathsf{P}$. A language $L$ is in $\mathsf{BP} \cdot \oplus\mathsf{P}$ if there are a language $B \in \oplus\mathsf{P}$ and a polynomial $q$ with

$$\Pr_{r \in \{0,1\}^{q(|x|)}}\big[ (x, r) \in B \iff x \in L \big] \ge 2/3 \quad \text{for every } x.$$

**Theorem (Toda 1991).**

1. $\mathsf{PH} \subseteq \mathsf{BP} \cdot \oplus\mathsf{P}$.
2. $\mathsf{BP} \cdot \oplus\mathsf{P} \subseteq \mathsf{P}^{\#\mathsf{P}[1]}$, polynomial time with a single query to a #P function.

So $\mathsf{PH} \subseteq \mathsf{P}^{\#\mathsf{P}[1]} \subseteq \mathsf{P}^{\mathsf{PP}}$.

## In plain words

Questions in the polynomial hierarchy have the form "is there an x such that for all y there is a z such that ...". Toda showed that one count is enough to answer all of them: how many solutions does a certain formula have? First, random choices turn each "is there" into "is the number of solutions odd". This works with good probability, and the steps can be stacked for every quantifier. Then the count is taken over all random choices at once, and a polynomial trick makes each odd count and each even count look different in the low bits of a big number. The total then shows how many random choices give an odd count, and that number tells the answer. So counting is at least as hard as any fixed number of alternating quantifiers.

## Proof

The first part, $\mathsf{PH} \subseteq \mathsf{BP} \cdot \oplus\mathsf{P}$, is given as a sketch in [proofs/main.md](proofs/main.md). It uses the [Valiant-Vazirani theorem](/valiant-vazirani-theorem/) and induction on the number of quantifiers. The second part, the counting step, is proved here in full.

**Closure of #P.** If $f$ and $g$ are in #P, so are $f + g$ (a machine branches once and runs one of the two), $f \cdot g$ (it runs both in sequence and accepts if both accept), and $x \mapsto \sum_{r \in \{0,1\}^{q(|x|)}} f(x, r)$ (it guesses $r$ first). So for every polynomial $P$ with nonnegative integer coefficients whose degree is polynomial in $|x|$, the function $x \mapsto P(f(x))$ is in #P.

**Lemma (modulus amplification).** Let $p(m) = 3m^4 + 4m^3$. For every integer $j \ge 1$:

- if $m \equiv 0 \pmod{2^j}$, then $p(m) \equiv 0 \pmod{2^{2j}}$;
- if $m \equiv -1 \pmod{2^j}$, then $p(m) \equiv -1 \pmod{2^{2j}}$.

*Proof.* If $m = t 2^j$, then $p(m) = m^3 (3m + 4)$ is divisible by $2^{3j}$. If $m = t 2^j - 1$, expand modulo $2^{2j}$: $m^3 \equiv -1 + 3t 2^j$ and $m^4 \equiv 1 - 4t 2^j$, so $p(m) \equiv 3 - 12 t 2^j - 4 + 12 t 2^j = -1$. $\square$

An odd $m$ is $-1$ modulo $2$ and an even $m$ is $0$ modulo $2$. After $\ell$ applications of $p$, written $p^{(\ell)}$, an odd $m$ becomes $-1$ and an even $m$ becomes $0$ modulo $2^{2^\ell}$. For example, $p(5) = 2375 \equiv 3 \pmod 4$ and $p(3) = 351 \equiv 15 \pmod{16}$. Starting from $m = 1$, the values $p(m)$, $p(p(m))$ and $p(p(p(m)))$ are $3 \bmod 4$, $15 \bmod 16$ and $255 \bmod 256$. From $m = 6$ they are $0$ modulo $4$, $16$ and $256$.

**Theorem.** $\mathsf{BP} \cdot \oplus\mathsf{P} \subseteq \mathsf{P}^{\#\mathsf{P}[1]}$.

*Proof.* Let $L \in \mathsf{BP} \cdot \oplus\mathsf{P}$ with $B$ and $q$ as in the definition, and let $f \in \#\mathsf{P}$ with $(x, r) \in B$ if and only if $f(x, r)$ is odd. Fix $x$, let $q = q(|x|)$ and let $\ell = \lceil \log_2(q + 1) \rceil$, so that $M = 2^{2^\ell} \ge 2^{q+1}$. Define

$$g(x, r) = p^{(\ell)}(f(x, r)), \qquad G(x) = \sum_{r \in \{0,1\}^q} g(x, r).$$

The polynomial $p^{(\ell)}$ has nonnegative coefficients and degree $4^\ell \le 4 (q + 1)^2$, so $g$ and $G$ are in #P. By the lemma, $g(x, r) \equiv -1 \pmod M$ when $f(x, r)$ is odd and $g(x, r) \equiv 0$ when it is even. So

$$-G(x) \bmod M = \#\{ r : (x, r) \in B \} =: c(x),$$

because $0 \le c(x) \le 2^q < M$. The machine asks the oracle for $G(x)$, computes $c(x)$ from its last $2^\ell$ bits, and accepts if and only if $c(x) \ge \tfrac{2}{3} 2^q$. If $x \in L$, then $c(x) \ge \tfrac{2}{3} 2^q$. If $x \notin L$, then $c(x) \le \tfrac{1}{3} 2^q$. So the machine decides $L$ with one query. $\square$

**Example.** Take $q = 2$, so $4$ random strings and $\ell = \lceil \log_2 3 \rceil = 2$, $M = 16$. Let the values $f(x, r)$ for the four strings be $5, 3, 6, 1$. Then $p(p(m)) \bmod 16$ is $15, 15, 0, 15$, the sum $G(x)$ is $1625751443485437 \equiv 13 \pmod{16}$, and $-13 \equiv 3 \pmod{16}$: three of the four strings give an odd count, so $c(x) = 3 \ge \tfrac{2}{3} \cdot 4$ and the machine accepts. The oracle answer is a large number, but only its last $4$ bits matter.

Combining both parts, $\mathsf{PH} \subseteq \mathsf{BP} \cdot \oplus\mathsf{P} \subseteq \mathsf{P}^{\#\mathsf{P}[1]} \subseteq \mathsf{P}^{\mathsf{PP}}$. $\square$

## Consequences

- *PP is hard for PH.* If $\mathsf{PP} \subseteq \Sigma_k^p$ for some $k$, then $\mathsf{PH} \subseteq \mathsf{P}^{\Sigma_k^p} \subseteq \Sigma_{k+1}^p$, so PH collapses. Thus counting problems such as #SAT and MAJSAT are not in PH unless PH collapses.
- *The permanent.* The [permanent](/permanent-computation/) of a 0-1 matrix is #P-complete (Valiant 1979), so $\mathsf{PH} \subseteq \mathsf{P}^{\mathrm{PERM}}$. A polynomial-time algorithm for the permanent would put PH in P. This is part of why the permanent is believed much harder than the [determinant](/determinant/).
- *Parity is hard for PH under randomized reductions.* Part 1 gives $\mathsf{PH} \subseteq \mathsf{BPP}^{\oplus\mathsf{P}}$. So if $\oplus\mathsf{P} \subseteq \mathsf{BPP}$, then $\mathsf{PH} \subseteq \mathsf{BPP}$, and with the [Sipser-Gács theorem](/sipser-gacs-theorem/) PH collapses to $\Sigma_2^p$.
- *Approximate against exact counting.* Stockmeyer's approximate counting puts a $(1 + \varepsilon)$-approximation of a #P function in $\mathsf{FP}^{\Sigma_2^p}$, inside the second level. Toda's theorem shows that exact counting is far above that, unless PH collapses.
- *Quantum supremacy arguments.* Arguments that classical computers cannot sample from some quantum distributions use Toda's theorem: an efficient classical sampler, with Stockmeyer's approximate counting, would put a #P-hard problem in $\mathsf{BPP}^{\mathsf{NP}}$, and so PH would collapse.

## Tightness

- *One query is enough.* The theorem gives a single #P query, which cannot be removed: with no query, it would say $\mathsf{PH} \subseteq \mathsf{P}$.
- *PH and PP.* Whether $\mathsf{PH} \subseteq \mathsf{PP}$ is open. There is an oracle relative to which $\mathsf{P}^{\mathsf{NP}}$ is not in PP (Beigel 1994), so a relativizing proof cannot remove the outer P machine and replace it by a PP machine.
- *The randomness.* Part 1 uses a randomized reduction. Whether $\mathsf{PH} \subseteq \oplus\mathsf{P}$ holds without randomness is open. Strong enough lower bounds against circuits with $\oplus\mathsf{P}$ oracle gates would derandomize the $\mathsf{BP}$ operator, by the methods of [hardness versus randomness](/hardness-versus-randomness/), and give $\mathsf{PH} \subseteq \oplus\mathsf{P}$.
- *Other counting classes.* Parity is not special. Toda and Ogiwara (1992) proved that PH is inside $\mathsf{BP} \cdot \mathcal{C}$ for other counting classes $\mathcal{C}$, such as counting modulo other numbers.

## History

Toda presented the result at FOCS 1989, and the journal version "PP is as hard as the polynomial-time hierarchy" appeared in 1991. It answered whether counting classes are above the hierarchy, and it received the 1998 Gödel Prize. The first step builds on the isolation lemma of Valiant and Vazirani (1986). Toda and Ogiwara (1992) extended it to other counting classes. Fortnow (2009) gave a short proof of the first step that avoids the operator calculus of the original. Textbooks, including Arora and Barak, present the proof in the form above.

## References
