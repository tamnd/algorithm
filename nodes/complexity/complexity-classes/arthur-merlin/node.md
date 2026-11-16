---
tag: 81M9Z4
kind: definition
slug: arthur-merlin
name: AM
aliases:
- Arthur-Merlin games
area: complexity/complexity-classes
level: research
summary: "Arthur-Merlin games: the verifier sends random coins in the open, the prover answers, and the verifier decides. A constant number of rounds gives the same class, which lies in Pi_2^p."
prereqs: [interactive-proofs, bpp, np, universal-hash-family]
see_also: [merlin-arthur, interactive-proofs, ip-equals-pspace, graph-isomorphism-problem, polynomial-hierarchy, sipser-gacs-theorem, pairwise-independence, hardness-versus-randomness]
sources:
  - paper: doi:10.1145/22145.22192
    title: László Babai, Trading group theory for randomness, Proceedings of the 17th Annual ACM Symposium on Theory of Computing, 421 to 429 (1985)
    locator: the definition of Arthur-Merlin games
  - paper: doi:10.1016/0022-0000(88)90028-1
    title: László Babai and Shlomo Moran, Arthur-Merlin games, a randomized proof system, and a hierarchy of complexity classes, Journal of Computer and System Sciences 36(2), 254 to 276 (1988)
    locator: the collapse AM[k] = AM for every constant k, and MA in AM
  - paper: doi:10.1145/12130.12137
    title: Shafi Goldwasser and Michael Sipser, Private coins versus public coins in interactive proof systems, Proceedings of the 18th Annual ACM Symposium on Theory of Computing, 59 to 68 (1986)
    locator: IP[k] in AM[k + 2] and the set lower bound protocol
  - paper: doi:10.1016/0020-0190(87)90232-8
    title: Ravi B. Boppana, Johan Håstad and Stathis Zachos, Does co-NP have short interactive proofs?, Information Processing Letters 25(2), 127 to 132 (1987)
    locator: if coNP is in AM then the polynomial hierarchy collapses, and the consequence for graph isomorphism
  - paper: doi:10.1145/116825.116852
    title: Oded Goldreich, Silvio Micali and Avi Wigderson, Proofs that yield nothing but their validity or all languages in NP have zero-knowledge proof systems, Journal of the ACM 38(3), 690 to 728 (1991)
    locator: the private-coin interactive proof for graph non-isomorphism
  - paper: doi:10.1007/s00037-005-0197-7
    title: Peter Bro Miltersen and N. V. Vinodchandran, Derandomizing Arthur-Merlin games using hitting sets, Computational Complexity 14(3), 256 to 279 (2005)
    locator: AM = NP if a language in NE intersected with coNE needs nondeterministic circuits of size 2^(epsilon n)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 8, Interactive proofs (public coins, the set lower bound protocol, AM and the polynomial hierarchy)
  - book: isbn:9780521884730
    title: Oded Goldreich, Computational Complexity, A Conceptual Perspective, Cambridge University Press (2008)
    locator: Chapter 9, Probabilistic proof systems (public-coin systems and perfect completeness)
---

AM is the class of languages that have an *Arthur-Merlin game*: an [interactive proof](/interactive-proofs/) in which the verifier (Arthur) only sends random bits in the open, and the prover (Merlin) sees them before it answers. In the basic form, Arthur sends one random string, Merlin sends one reply, and Arthur decides by a deterministic polynomial-time computation. Babai defined these games in 1985. Babai and Moran showed that any constant number of rounds gives the same class, and Goldwasser and Sipser showed that public coins are as strong as private coins up to two extra messages.

## Definition

**AM.** A language $L$ is in $\mathsf{AM}$ if there are polynomials $\ell$ and $q$ and a deterministic polynomial-time [multitape Turing machine](/multitape-turing-machine/) $V$ such that, for every input $x$ with $n = |x|$ and with $r$ uniform in $\{0,1\}^{\ell(n)}$:

$$x \in L \Rightarrow \Pr_r\big[\exists m \in \{0,1\}^{q(n)} : V(x, r, m) = 1\big] \ge \tfrac23, \qquad x \notin L \Rightarrow \Pr_r\big[\exists m \in \{0,1\}^{q(n)} : V(x, r, m) = 1\big] \le \tfrac13.$$

The string $r$ is Arthur's message and $m$ is Merlin's reply. Merlin chooses $m$ after it sees $r$. In the notation of [interactive proofs](/interactive-proofs/), this is a public-coin protocol with $2$ messages, Arthur first. Another way to say it: $L \in \mathsf{AM}$ if and only if there is a language $L' \in \mathsf{NP}$ of pairs such that $x \in L$ makes $(x, r) \in L'$ for most $r$, and $x \notin L$ makes $(x, r) \notin L'$ for most $r$. This is the class $\mathsf{BP} \cdot \mathsf{NP}$.

**AM[k].** $\mathsf{AM}[k]$ allows $k$ messages that alternate between Arthur and Merlin, Arthur first. Arthur's messages are fresh uniform strings, and Arthur's final decision is a deterministic polynomial-time function of $x$ and the whole transcript. Then:

- $\mathsf{AM}[k] = \mathsf{AM}[2] = \mathsf{AM}$ for every constant $k \ge 2$ (Babai and Moran 1988). So a constant number of rounds adds nothing.
- $\mathsf{IP}[k] \subseteq \mathsf{AM}[k + 2]$ for every $k$ (Goldwasser and Sipser 1986). So private coins can be replaced by public coins.
- With polynomially many messages, $\mathsf{AM}[\mathrm{poly}] = \mathsf{IP} = \mathsf{PSPACE}$, because the protocol for [IP = PSPACE](/ip-equals-pspace/) uses public coins.

**Error reduction.** Arthur sends $t$ independent strings $r_1, \ldots, r_t$ at once, Merlin answers $m_1, \ldots, m_t$, and Arthur accepts if $V(x, r_j, m_j) = 1$ for a majority of $j$. Merlin can do no better than to answer each $r_j$ on its own, so the number of good $j$ is a sum of independent indicators, and by the [Chernoff bound](/chernoff-bound/) both errors fall to $2^{-\Omega(t)}$ with the same two messages. Fürer, Goldreich, Mansour, Sipser and Zachos (1989) showed that the completeness error can be made $0$: every language in AM has a game in which Merlin always wins on yes-instances.

**AM is in the second level of the hierarchy.** $\mathsf{NP} \cup \mathsf{BPP} \subseteq \mathsf{MA} \subseteq \mathsf{AM} \subseteq \Pi_2^p$.

*Proof of the last inclusion.* Reduce the error to $\delta$ with $\ell$ coins and $\delta < 1/\ell$; this is possible because $\ell$ grows linearly in $t$ and $\delta$ falls exponentially in $t$. Let $A_x = \{r : \exists m\, V(x, r, m) = 1\}$ and let $B_x$ be its complement, the set of $r$ such that $V(x, r, m) = 0$ for every $m$. If $x \notin L$, then $|B_x| \ge (1 - \delta) 2^\ell$, and as in the proof of the [Sipser-Gács theorem](/sipser-gacs-theorem/), some $\ell$ shifts $s_1, \ldots, s_\ell$ make the sets $B_x \oplus s_i$ cover $\{0,1\}^\ell$. If $x \in L$, then $|B_x| \le \delta 2^\ell$, and $\ell$ shifts cover at most $\ell \delta 2^\ell < 2^\ell$ strings. So

$$x \notin L \iff \exists s_1, \ldots, s_\ell\; \forall r\; \bigvee_{i=1}^{\ell} \big[\forall m : V(x, r \oplus s_i, m) = 0\big].$$

The disjunction of $\ell$ statements "for all $m$" is the statement "for all $m_1, \ldots, m_\ell$, some $i$ has $V(x, r \oplus s_i, m_i) = 0$". So the right side is "exists $s_1, \ldots, s_\ell$, for all $r$ and $m_1, \ldots, m_\ell$, a polynomial-time predicate holds", with all strings of polynomial length. So $\overline{L} \in \Sigma_2^p$ and $L \in \Pi_2^p$. $\square$

The inclusion $\mathsf{MA} \subseteq \mathsf{AM}$ is on the page of [MA](/merlin-arthur/). NP is in AM with an Arthur who ignores its coins, and BPP is in AM with a Merlin who is ignored.

## Examples and non-examples

**Examples.**

- *Graph non-isomorphism (GNI).* The private-coin protocol on [IP](/interactive-proofs/) fails with public coins, because Merlin then knows Arthur's secret bit. Goldwasser and Sipser gave a public-coin protocol with a *set lower bound*. For graphs $G_0, G_1$ on $n$ vertices, let

$$S = \{(H, \pi) : H \cong G_0 \text{ or } H \cong G_1,\ \pi \in \mathrm{Aut}(H)\}.$$

A graph $G$ has $n!/|\mathrm{Aut}(G)|$ labeled copies, each with $|\mathrm{Aut}(G)|$ automorphisms, so it contributes $n!$ pairs. Thus $|S| = 2 \cdot n!$ if the graphs are not isomorphic and $|S| = n!$ if they are. Membership in $S$ has a short certificate: an isomorphism from some $G_b$ to $H$, plus a check that $\pi$ maps $H$ to itself.

- *The set lower bound protocol.* Let $K = 2 \cdot n!$ and choose $k$ with $2^{k-2} \le K \le 2^{k-1}$. Arthur picks a hash function $h : \{0,1\}^M \to \{0,1\}^k$ from a [pairwise independent](/pairwise-independence/) family ([universal hash family](/universal-hash-family/)) and a uniform $y \in \{0,1\}^k$, and sends both. Merlin replies with some $s \in S$ and its certificate. Arthur accepts if the certificate is valid and $h(s) = y$. Write $p^* = K/2^k$, which is between $1/4$ and $1/2$.
  - If $|S| \ge K$, take a subset $S'$ of exactly $K$ elements. By inclusion and exclusion, $\Pr[\exists s \in S' : h(s) = y] \ge K/2^k - \binom{K}{2}/2^{2k} \ge p^* (1 - K/2^{k+1}) \ge \tfrac34 p^*$.
  - If $|S| \le K/2$, then by the union bound $\Pr[\exists s \in S : h(s) = y] \le |S|/2^k \le \tfrac12 p^*$.

  The gap between $\tfrac34 p^*$ and $\tfrac12 p^*$ is a constant, and parallel repetition with a threshold between the two values makes the errors small. So $\mathrm{GNI} \in \mathsf{AM}$, that is, graph isomorphism is in $\mathsf{coAM}$.

- *A worked case.* Take $n = 4$, so $n! = 24$ and $K = 48$, and $k = 7$, since $32 \le 48 \le 64$. Then $p^* = 48/128 = 0.375$, the lower bound is $0.28125$ and the upper bound is $0.1875$. For the path $1{-}2{-}3{-}4$ against the star with center $1$, which are not isomorphic, $|S| = 12 \cdot 2 + 4 \cdot 6 = 48$. For the path against the isomorphic path $3{-}1{-}4{-}2$, $|S| = 24$. Encode each pair $(H, \pi)$ as $11$ bits ($6$ edge bits and a $5$-bit index of $\pi$) and use $h(s) = As$ with a uniform $7 \times 11$ matrix $A$ over $\mathrm{GF}(2)$, which is pairwise independent on nonzero vectors. With $20000$ random matrices from a fixed seed, and the exact probability over $y$ for each matrix, the acceptance probability is about $0.3138$ for the non-isomorphic pair and $0.1717$ for the isomorphic pair. By Hoeffding's inequality, each estimate is within $0.012$ of the true value with probability at least $0.99$, so both lie on the correct side of the bounds.

- *Every language in NP and in BPP*, and every language in [MA](/merlin-arthur/).

**Non-examples.**

- *coNP-complete problems, unless the hierarchy collapses.* Boppana, Håstad and Zachos (1987) proved that if $\mathsf{coNP} \subseteq \mathsf{AM}$, then the [polynomial hierarchy](/polynomial-hierarchy/) collapses to its second level, $\Sigma_2^p = \Pi_2^p = \mathsf{AM}$. With $\mathrm{GNI} \in \mathsf{AM}$ this gives: if the [graph isomorphism problem](/graph-isomorphism-problem/) were NP-complete under polynomial-time many-one reductions, then GNI would be coNP-complete, $\mathsf{coNP} \subseteq \mathsf{AM}$, and the hierarchy would collapse. This is the main evidence that graph isomorphism is not NP-complete. It is not a proof, since the collapse is not known to be false.
- *PSPACE-complete problems, unless the hierarchy collapses.* Since $\mathsf{AM} \subseteq \Pi_2^p$, a PSPACE-complete problem in AM would give $\mathsf{PSPACE} = \Pi_2^p$. Such problems need polynomially many rounds.
- *A protocol with a secret coin.* The GNI protocol of Goldreich, Micali and Wigderson is not an Arthur-Merlin game, because its correctness depends on the prover not seeing the verifier's bit.

## Related definitions

- [MA](/merlin-arthur/) reverses the order: Merlin sends a proof first, then Arthur tosses coins. $\mathsf{MA} \subseteq \mathsf{AM}$, and $\mathsf{MAM} = \mathsf{AM}$.
- [IP](/interactive-proofs/) allows private coins and polynomially many rounds. With a constant number of rounds, IP and AM are the same class by Goldwasser and Sipser.
- [QMA](/qma/) is a quantum analogue of MA. The quantum analogue of AM is QAM, studied by Marriott and Watrous.
- *Derandomization.* Under circuit lower bounds, AM collapses to NP. Miltersen and Vinodchandran (2005) proved $\mathsf{AM} = \mathsf{NP}$ if some language in $\mathsf{NE} \cap \mathsf{coNE}$ needs nondeterministic circuits of size $2^{\varepsilon n}$ for some $\varepsilon > 0$, which would put GNI in NP. See [hardness versus randomness](/hardness-versus-randomness/).
- The [Sipser-Gács theorem](/sipser-gacs-theorem/) is the special case without Merlin: $\mathsf{BPP} \subseteq \Sigma_2^p \cap \Pi_2^p$.

## References
