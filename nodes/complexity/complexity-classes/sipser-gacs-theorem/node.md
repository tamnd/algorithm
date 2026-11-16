---
tag: V8KBN4
kind: theorem
slug: sipser-gacs-theorem
name: Sipser-Gács theorem
aliases:
- BPP in Sigma2 and Pi2
area: complexity/complexity-classes
level: advanced
summary: BPP is in the second level of the polynomial hierarchy. A few random shifts of the accepting coin strings cover all strings when the input is in the language and cannot when it is not.
prereqs: [bpp, polynomial-hierarchy, union-bound, error-amplification]
see_also: [bpp, adleman-theorem, polynomial-hierarchy, merlin-arthur, arthur-merlin, toda-theorem, karp-lipton-theorem, probabilistic-method]
sources:
  - paper: doi:10.1145/800061.808762
    title: Michael Sipser, A complexity theoretic approach to randomness, Proceedings of the 15th Annual ACM Symposium on Theory of Computing, 330 to 335 (1983)
    locator: BPP in the polynomial hierarchy, with the improvement to the second level credited to Gács
  - paper: doi:10.1016/0020-0190(83)90044-3
    title: Clemens Lautemann, BPP and the polynomial hierarchy, Information Processing Letters 17(4), 215 to 217 (1983)
    locator: the proof by random shifts
  - paper: doi:10.1007/s000370050007
    title: Alexander Russell and Ravi Sundaram, Symmetric alternation captures BPP, Computational Complexity 7(2), 152 to 162 (1998)
    locator: the inclusion of BPP in S2^p
  - paper: doi:10.1016/j.jcss.2003.07.015
    title: Jin-Yi Cai, S2^p is a subset of ZPP^NP, Journal of Computer and System Sciences 73(1), 25 to 35 (2007)
    locator: the main theorem
  - paper: doi:10.1137/0220053
    title: Seinosuke Toda, PP is as hard as the polynomial-time hierarchy, SIAM Journal on Computing 20(5), 865 to 877 (1991)
    locator: the main theorem (PH in P^PP)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 7, Randomized computation (BPP and the polynomial hierarchy)
  - book: isbn:9780521884730
    title: Oded Goldreich, Computational Complexity, A Conceptual Perspective, Cambridge University Press (2008)
    locator: Chapter 6, Randomness and counting (BPP and the polynomial hierarchy)
---

The Sipser-Gács theorem says that $\mathsf{BPP} \subseteq \Sigma_2^p \cap \Pi_2^p$: every language that a probabilistic machine decides in polynomial time with bounded error is in the second level of the [polynomial hierarchy](/polynomial-hierarchy/). Sipser proved in 1983 that [BPP](/bpp/) is in the hierarchy, and Gács improved the level to the second. The short proof that most texts use is by Lautemann (1983): if the input is in the language, a few shifts of the set of accepting coin strings cover all strings, and if it is not, no such shifts do. One consequence is that $\mathsf{P} = \mathsf{NP}$ implies $\mathsf{P} = \mathsf{BPP}$.

## Statement

**Theorem.** Let $L \in \mathsf{BPP}$, decided by a probabilistic polynomial-time [multitape Turing machine](/multitape-turing-machine/) with bounded two-sided error. Then $L \in \Sigma_2^p \cap \Pi_2^p$.

In the form of the proof: there are a polynomial $m$ and a polynomial-time machine $M'$ such that for every $x$ of length $n$,

$$x \in L \iff \exists s_1, \ldots, s_m \in \{0,1\}^m \;\; \forall r \in \{0,1\}^m : \bigvee_{i=1}^{m} M'(x, r \oplus s_i) = 1,$$

where $m = m(n)$ and $\oplus$ is the bitwise exclusive or.

## In plain words

Look at the set of coin sequences that make the algorithm say yes. When the answer is yes, this set is almost everything. When the answer is no, it is a tiny part. A large set can be moved around a few times so that the copies together cover every sequence, and a random choice of moves works. A tiny set cannot do this with so few copies, because the copies together are still too small. So the question becomes: are there a few moves such that every sequence is covered? This has the form "there exists something such that for all things a fast check passes", which is the second level of the polynomial hierarchy.

## Proof

Let $M$ decide $L$ with error at most $1/3$. By [error amplification](/error-amplification/), run $M$ for $k$ times and take the majority. This gives a machine $M'(x, r)$ with $m$ coins and error $\delta$ on every input, where $m$ grows linearly in $k$ and $\delta \le e^{-k/18}$ falls exponentially in $k$. So a polynomial $k$ gives $\delta < 1/m$. Fix $x$ of length $n$ and let $A = \{r \in \{0,1\}^m : M'(x, r) = 1\}$. For a string $s$, let $A \oplus s = \{a \oplus s : a \in A\}$; it has the same size as $A$.

*If $x \in L$, then $|A| \ge (1 - \delta) 2^m$, and some $m$ shifts cover $\{0,1\}^m$.* Choose $s_1, \ldots, s_m$ independently and uniformly. For a fixed $r$, the string $r \oplus s_i$ is uniform, so $\Pr[r \oplus s_i \notin A] \le \delta$, and these events are independent over $i$. So

$$\Pr\big[r \notin \textstyle\bigcup_i (A \oplus s_i)\big] = \Pr[\forall i : r \oplus s_i \notin A] \le \delta^m.$$

By the [union bound](/union-bound/) over the $2^m$ strings $r$, the probability that some $r$ is not covered is at most $2^m \delta^m = (2\delta)^m < 1$. So some choice of shifts covers every $r$. This is an instance of the [probabilistic method](/probabilistic-method/).

*If $x \notin L$, then $|A| \le \delta 2^m$, and no $m$ shifts cover $\{0,1\}^m$.* For any $s_1, \ldots, s_m$,

$$\Big|\bigcup_{i=1}^m (A \oplus s_i)\Big| \le m \delta 2^m < 2^m,$$

because $\delta < 1/m$. So some $r$ is not covered.

The two cases give the formula in the statement. The inner predicate computes $M'$ on $m$ inputs, which takes polynomial time, and all strings have polynomial length. So $L \in \Sigma_2^p$. BPP is closed under complement, so $\overline{L} \in \Sigma_2^p$ as well, and $L \in \Pi_2^p$. $\square$

**Example.** Take $m = 6$ coins, so there are $64$ coin strings. Suppose the accepting set $A$ on a yes-instance is all strings except the $4$ that begin with $0000$, so $|A| = 60$ and $\delta = 4/64 = 1/16 < 1/6$. The two shifts $000000$ and $100000$ already cover all $64$ strings: a string $r$ outside $A$ begins with $0$, and $r \oplus 100000$ begins with $1$, so it is in $A$. No single shift covers all strings, since $|A| < 64$. Of the $4096$ ordered pairs of shifts, $3840$, that is $15/16$, cover all strings. The bound of the proof for $6$ random shifts is $2^6 (1/16)^6 \approx 3.8 \cdot 10^{-6}$ for the probability of failure. Now suppose that on a no-instance $A$ is the $4$ strings that begin with $1111$. Any $6$ shifts cover at most $6 \cdot 4 = 24 < 64$ strings, so the formula is false, as it should be.

## Consequences

- *If P = NP, then P = BPP.* If $\mathsf{P} = \mathsf{NP}$, the polynomial hierarchy collapses to P, and $\mathsf{BPP} \subseteq \Sigma_2^p = \mathsf{P}$. So a proof that $\mathsf{P} \ne \mathsf{BPP}$ would also prove $\mathsf{P} \ne \mathsf{NP}$.
- *If NP is in BPP, the hierarchy collapses.* With $\mathsf{NP} \subseteq \mathsf{BPP}$, the class $\Sigma_2^p = \mathsf{NP}^{\mathsf{NP}}$ is in $\mathsf{BPP}^{\mathsf{BPP}} = \mathsf{BPP}$, and by induction the whole hierarchy is in BPP. Since $\mathsf{BPP} \subseteq \Sigma_2^p$, the hierarchy then collapses to $\Sigma_2^p$. [Adleman's theorem](/adleman-theorem/) with the [Karp-Lipton theorem](/karp-lipton-theorem/) gives the same collapse in another way.
- *Merlin-Arthur proofs.* The same covering argument, applied to the coins of the verifier after the message of the prover, puts the class [MA](/merlin-arthur/) in $\Sigma_2^p$.
- *Smaller classes.* Russell and Sundaram (1998) showed $\mathsf{BPP} \subseteq \mathsf{S}_2^p$, the class of symmetric alternation, and Cai (2007) showed $\mathsf{S}_2^p \subseteq \mathsf{ZPP}^{\mathsf{NP}}$. Together, $\mathsf{BPP} \subseteq \mathsf{S}_2^p \subseteq \mathsf{ZPP}^{\mathsf{NP}} \subseteq \Sigma_2^p \cap \Pi_2^p$.

## Tightness

- *The error gap is needed.* For [PP](/pp/), where the gap can be exponentially small, no such result is expected. By [Toda's theorem](/toda-theorem/), $\mathsf{PH} \subseteq \mathsf{P}^{\mathsf{PP}}$. If PP were in $\Sigma_k^p$ for some $k$, the hierarchy would collapse to $\Sigma_{k+1}^p$. The proof above fails for PP because $\delta < 1/m$ cannot be reached by amplification.
- *The condition $\delta < 1/m$.* With $m$ shifts, the no-case needs $m\delta < 1$. In the example, $\delta = 1/16$ and $m = 6$ satisfy it. If the accepting set on a no-instance had $16$ of $64$ strings, so $\delta = 1/4 > 1/6$, then $6$ shifts could cover up to $96 \ge 64$ strings, and the argument would give nothing.
- *Lower levels.* It is not known whether $\mathsf{BPP} \subseteq \mathsf{NP}$ or even whether $\mathsf{BPP} \subseteq \mathsf{P}^{\mathsf{NP}}$. Under the circuit lower bounds of [hardness versus randomness](/hardness-versus-randomness/), $\mathsf{BPP} = \mathsf{P}$, and then both hold.

## History

Sipser (1983) proved that BPP is in the polynomial hierarchy, at the fourth level, with a method based on hashing. In the same paper he gave the improvement to $\Sigma_2^p \cap \Pi_2^p$ found by Peter Gács. In the same year Lautemann (1983) gave the short proof by random shifts that is shown above. Later work moved BPP into smaller classes inside the second level: Russell and Sundaram (1998) put it in $\mathsf{S}_2^p$, and Cai's result (FOCS 2001, journal 2007) put $\mathsf{S}_2^p$ in $\mathsf{ZPP}^{\mathsf{NP}}$.

## References
