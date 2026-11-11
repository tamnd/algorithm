---
tag: 7NPNRH
kind: theorem
slug: prp-prf-switching-lemma
name: PRP-PRF switching lemma
aliases:
- PRP/PRF switching lemma
area: cryptography/symmetric-ciphers
level: research
summary: For any adversary with q queries, the PRP and PRF advantages of a block cipher on n-bit blocks differ by at most q(q-1)/2^(n+1), the chance of a collision among q random outputs.
prereqs: [pseudorandom-permutation, birthday-paradox, union-bound]
see_also: [pseudorandom-function, luby-rackoff-theorem, birthday-attack, ctr-mode, triple-des, hybrid-argument, random-permutation, block-cipher]
sources:
  - paper: "Mihir Bellare and Phillip Rogaway, The security of triple encryption and a framework for code-based game-playing proofs, Advances in Cryptology, EUROCRYPT 2006, LNCS 4004, Springer, 2006"
    locator: the fundamental lemma of game playing, the proof of the switching lemma by games, and the remark that the usual conditional-probability proof is wrong for adaptive adversaries
  - paper: doi:10.1006/jcss.1999.1694
    title: Mihir Bellare, Joe Kilian and Phillip Rogaway, The security of the cipher block chaining message authentication code, Journal of Computer and System Sciences 61(3), 2000
    locator: the concrete PRF and PRP definitions and an early statement of the switching bound
  - paper: "Victor Shoup, Sequences of games, a tool for taming complexity in security proofs, IACR Cryptology ePrint Archive, Report 2004/332, 2004"
    locator: the difference lemma for games that are identical until a failure event
---

The PRP-PRF switching lemma says that, to an adversary that makes $q$ queries, a uniformly random permutation of $\{0,1\}^n$ and a uniformly random function from $\{0,1\}^n$ to $\{0,1\}^n$ look the same except with probability at most $q(q-1)/2^{n+1}$. So a block cipher that is a good [pseudorandom permutation](/pseudorandom-permutation/) is also a good [pseudorandom function](/pseudorandom-function/), with a loss at the [birthday bound](/birthday-paradox/). Security proofs of modes such as [CTR](/ctr-mode/) and CBC use it to replace the cipher by a random function, which is easier to analyze. The usual short proof, by conditioning on distinct answers, is wrong for adaptive adversaries; Bellare and Rogaway pointed this out in 2006 and gave a correct proof by games.

## Statement

Let $N = 2^n$. Let $\rho$ be uniform in $\mathrm{Func}(n, n)$, the set of all functions $\{0,1\}^n \to \{0,1\}^n$, and let $\pi$ be uniform in $\mathrm{Perm}(n)$, the set of all permutations of $\{0,1\}^n$. Let $A$ be any adversary, possibly adaptive, unbounded in time, and randomized, that makes at most $q$ oracle queries and outputs a bit.

**Theorem 1.**
$$\bigl| \Pr[A^{\pi} = 1] - \Pr[A^{\rho} = 1] \bigr| \le \frac{q(q-1)}{2^{n+1}}.$$

**Corollary 2.** For every family $E : \{0,1\}^k \times \{0,1\}^n \to \{0,1\}^n$ of permutations and every $A$ as above,
$$\bigl| \mathrm{Adv}^{\mathrm{prp}}_E(A) - \mathrm{Adv}^{\mathrm{prf}}_E(A) \bigr| \le \frac{q(q-1)}{2^{n+1}}.$$

**Theorem 3 (the exact optimum).** For $q \le N$, the largest value of $\Pr[A^{\rho} = 1] - \Pr[A^{\pi} = 1]$ over all $A$ with $q$ queries is

$$C(N, q) = 1 - \prod_{i=0}^{q-1} \Bigl(1 - \frac{i}{N}\Bigr),$$

the probability that $q$ independent uniform values in a set of size $N$ are not all distinct. For $q > N$, the optimum is $C(N, N) = 1 - N!/N^N$.

## In plain words

A permutation never gives the same answer twice. A random function sometimes does, but only rarely: among $q$ answers, the chance of a repeat is about $q^2/2^{n+1}$. As long as no repeat appears, the answers of a random function look exactly like those of a random permutation, one fresh value after another. So no test can tell them apart better than by waiting for a repeat. For a 128-bit block, the chance stays tiny for any practical number of queries. For a 64-bit block, it becomes large after about $2^{32}$ queries, which is the reason behind the Sweet32 attack on [Triple DES](/triple-des/).

## Proof

*Normal form.* We may assume that $A$ never repeats a query: an adversary that repeats a query can be changed to look up the earlier answer, and this changes nothing in either world, since both $\pi$ and $\rho$ are functions. So $A$ makes $q$ distinct queries $x_1, \ldots, x_q$, each chosen from the earlier answers and the coins of $A$.

*Two games.* Both games answer query $x_i$ by lazy sampling, with a set $Y$ of the answers given so far, empty at the start.

- Game G1: choose $y$ uniformly in $\{0,1\}^n$. If $y \in Y$, set bad $\leftarrow$ true. Add $y$ to $Y$ and return $y$.
- Game G0: choose $y$ uniformly in $\{0,1\}^n$. If $y \in Y$, set bad $\leftarrow$ true and then choose $y$ uniformly in $\{0,1\}^n \setminus Y$. Add $y$ to $Y$ and return $y$.

In G1 every answer is uniform and independent of the earlier ones, so G1 answers as $\rho$ does on distinct queries. In G0, the answer is uniform on $\{0,1\}^n \setminus Y$: if $y \notin Y$, it is uniform there; if $y \in Y$, the second choice is uniform there; and a mixture of two uniform distributions on the same set is uniform on it. So G0 answers as $\pi$ does, by lazy sampling of a random permutation. Hence $\Pr[A^{\pi} = 1] = \Pr[A^{G0} = 1]$ and $\Pr[A^{\rho} = 1] = \Pr[A^{G1} = 1]$.

*Identical until bad.* Run both games with the same coins of $A$ and the same first choices of $y$. The two games execute the same steps until the first time bad is set, so the event bad and the transcript up to that time are the same in both. In particular, $\Pr[\text{G0 sets bad}] = \Pr[\text{G1 sets bad}]$, and on runs where bad is never set, the outputs of $A$ are equal. So

$$\Pr[A^{G0} = 1 \wedge \neg \text{bad}] = \Pr[A^{G1} = 1 \wedge \neg \text{bad}],$$

and therefore

$$\bigl| \Pr[A^{G0} = 1] - \Pr[A^{G1} = 1] \bigr| = \bigl| \Pr[A^{G0} = 1 \wedge \text{bad}] - \Pr[A^{G1} = 1 \wedge \text{bad}] \bigr| \le \Pr[\text{G1 sets bad}].$$

The last step holds because both terms lie in $[0, \Pr[\text{bad}]]$. This is the fundamental lemma of game playing.

*Bounding bad in G1.* At query $i$, $|Y| \le i - 1$, and the uniform $y$ is independent of $Y$, of the earlier answers and of the choice of $x_i$. So $\Pr[y \in Y] \le (i-1)/2^n$. By the [union bound](/union-bound/),

$$\Pr[\text{G1 sets bad}] \le \sum_{i=1}^{q} \frac{i-1}{2^n} = \frac{q(q-1)}{2^{n+1}}.$$

This proves Theorem 1.

*Corollary 2.* Write $p_E = \Pr_K[A^{E_K} = 1]$, $p_\pi = \Pr[A^{\pi} = 1]$ and $p_\rho = \Pr[A^{\rho} = 1]$. Then $\mathrm{Adv}^{\mathrm{prp}} = |p_E - p_\pi|$ and $\mathrm{Adv}^{\mathrm{prf}} = |p_E - p_\rho|$, and by the triangle inequality their difference is at most $|p_\pi - p_\rho|$, which Theorem 1 bounds.

*Theorem 3.* Fix a deterministic $A$ with $q \le N$ distinct queries; a randomized $A$ is a mixture of deterministic ones and does no better. A transcript is the list of answers $(y_1, \ldots, y_q)$, since the queries are functions of earlier answers. Under $\rho$, each transcript has probability $N^{-q}$. Under $\pi$, a transcript with distinct answers has probability $1/(N(N-1) \cdots (N-q+1)) > N^{-q}$, and one with a repeat has probability 0. The best output rule says 1 exactly on the transcripts more likely under $\rho$, which are those with a repeat, and its advantage is the probability under $\rho$ of a repeat among $q$ independent uniform answers, $C(N, q)$. Every $A$ gets this same value, and no output rule does better, since the best advantage equals the total variation distance of the two transcript distributions. For $q > N$, at most $N$ queries are distinct. $\blacksquare$

**The flaw in the earlier proof.** The common argument was: let Dist be the event that the answers are distinct; then $\Pr[A^{\rho} = 1 \mid \text{Dist}] = \Pr[A^{\pi} = 1]$, and the bound follows. Bellare and Rogaway (2006) showed that the equation is false when $A$ is adaptive, because the number of queries, and so the event Dist, depends on the answers. Their example, with $n = 2$: ask $f(0)$ and output 1 if $f(0) = 0$; otherwise ask $f(1)$ and output 1 if $f(1) = 1$. The exact values are $\Pr[A^{\pi} = 1] = 5/12$, but $\Pr[A^{\rho} = 1 \mid \text{Dist}] = 6/13$. The game proof above avoids conditioning.

## Consequences

- **Block ciphers as PRFs.** If AES is a $(t, q, \varepsilon)$-PRP, it is a $(t, q, \varepsilon + q^2/2^{129})$-PRF. For $q = 2^{40}$ blocks, the extra term is $2^{-49}$.
- **Modes of operation.** Proofs of CTR, CBC, CMAC and GCM first replace $E_K$ by $\pi$ (cost: the PRP advantage), then $\pi$ by $\rho$ (cost: this lemma), then analyze $\rho$. The birthday terms $q^2/2^n$ in their bounds come partly from here. This is why NIST limits the data under one Triple DES key, whose block has 64 bits.
- **A PRF from a PRP.** The lemma shows that the identity map from PRPs to PRFs works up to the birthday bound. Constructions such as the sum of two permutations, $\pi_1(x) \oplus \pi_2(x)$, reach PRF security beyond it.
- **Game playing.** The proof is the standard first example of the identical-until-bad method, used again in the [Luby-Rackoff theorem](/luby-rackoff-theorem/) and in the analysis of triple encryption.

## Tightness

The adversary that asks $q$ distinct points and outputs 1 if two answers are equal reaches $C(N, q)$, which is the exact optimum by Theorem 3. For $1 \le q \le \sqrt{2N}$, $C(N, q) \ge (1 - 1/e)\,q(q-1)/(2N)$, so the bound of Theorem 1 is tight up to the factor $1 - 1/e \approx 0.63$ in this range. For $q = 2$ it is exact: $C(N, 2) = 1/N = 2 \cdot 1/2^{n+1}$.

The implementation with this page computes the best advantage over all adaptive deterministic adversaries by dynamic programming over transcripts, with exact fractions, for tiny $n$. It is for study only, encrypts nothing and is not constant time. The results agree with Theorem 3.

| $n$ | $q$ | exact optimum | bound $q(q-1)/2^{n+1}$ |
|---|---|---|---|
| 1 | 2 | 1/2 | 1/2 |
| 1 | 3 | 1/2 | 3/2 |
| 2 | 2 | 1/4 | 1/4 |
| 2 | 3 | 5/8 | 3/4 |
| 2 | 4 | 29/32 | 3/2 |
| 2 | 5 | 29/32 | 5/2 |
| 3 | 2 | 1/8 | 1/8 |
| 3 | 3 | 11/32 | 3/8 |

For $q > N$ the bound exceeds 1 and says nothing, while the optimum stops growing at $C(N, N)$, as the rows for $q = 3$ with $n = 1$ and $q = 5$ with $n = 2$ show.

## History

The lemma was folklore in the early 1990s and appears with a proof in the work of Bellare, Kilian and Rogaway on CBC-MAC (1994, journal version 2000). The usual proof conditioned on the event that the answers are distinct. In their 2006 paper on triple encryption, Bellare and Rogaway showed that this step fails for adaptive adversaries, gave the counterexample above, and proved the lemma with code-based games and the fundamental lemma of game playing. Shoup's 2004 tutorial on sequences of games gives the same proof in the form of the difference lemma.

## References
