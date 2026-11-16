---
tag: 3RKDMH
kind: definition
slug: merlin-arthur
name: MA
aliases:
- Merlin-Arthur games
area: complexity/complexity-classes
level: research
summary: "Merlin-Arthur: the prover sends one proof, then the verifier tosses coins and checks it in polynomial time with bounded error. Contains NP and BPP and lies in AM."
prereqs: [np, bpp, interactive-proofs]
see_also: [arthur-merlin, qma, sipser-gacs-theorem, polynomial-identity-testing, schwartz-zippel-lemma, impagliazzo-wigderson-theorem, polynomial-hierarchy, interactive-proofs]
sources:
  - paper: doi:10.1145/22145.22192
    title: László Babai, Trading group theory for randomness, Proceedings of the 17th Annual ACM Symposium on Theory of Computing, 421 to 429 (1985)
    locator: the definition of Merlin-Arthur and Arthur-Merlin games
  - paper: doi:10.1016/0022-0000(88)90028-1
    title: László Babai and Shlomo Moran, Arthur-Merlin games, a randomized proof system, and a hierarchy of complexity classes, Journal of Computer and System Sciences 36(2), 254 to 276 (1988)
    locator: MA in AM, and the hierarchy of Arthur-Merlin classes
  - paper: doi:10.1016/0020-0190(83)90044-3
    title: Clemens Lautemann, BPP and the polynomial hierarchy, Information Processing Letters 17(4), 215 to 217 (1983)
    locator: the random shifts argument, used here for perfect completeness
  - paper: doi:10.1145/258533.258590
    title: Russell Impagliazzo and Avi Wigderson, P = BPP if E requires exponential circuits, derandomizing the XOR lemma, Proceedings of the 29th Annual ACM Symposium on Theory of Computing, 220 to 229 (1997)
    locator: the pseudorandom generator from a function in E with circuit complexity 2^(Omega(n))
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 8, Interactive proofs (the classes AM and MA)
  - book: isbn:9780521884730
    title: Oded Goldreich, Computational Complexity, A Conceptual Perspective, Cambridge University Press (2008)
    locator: Chapter 9, Probabilistic proof systems (Arthur-Merlin games)
---

Merlin-Arthur (MA) is the class of languages that have a one-message randomized proof: the prover (Merlin) sends a proof string, and then the verifier (Arthur) tosses coins and checks the proof in polynomial time with bounded error. It is the randomized version of [NP](/np/), in the same way that [BPP](/bpp/) is the randomized version of P. Babai defined it in 1985 together with [AM](/arthur-merlin/), where Arthur speaks first. MA contains NP and BPP, it is a subset of AM, and it lies in the second level of the [polynomial hierarchy](/polynomial-hierarchy/).

## Definition

**MA.** A language $L$ is in $\mathsf{MA}$ if there are a polynomial $q$ and a probabilistic polynomial-time [multitape Turing machine](/multitape-turing-machine/) $V$ ([probabilistic Turing machine](/probabilistic-turing-machine/)) such that for every input $x$:

$$x \in L \Rightarrow \exists w \in \{0,1\}^{q(|x|)} : \Pr_r\big[V(x, w, r) = 1\big] \ge \tfrac23, \qquad x \notin L \Rightarrow \forall w \in \{0,1\}^{q(|x|)} : \Pr_r\big[V(x, w, r) = 1\big] \le \tfrac13.$$

The string $w$ is Merlin's proof and $r$ is Arthur's coin string. Merlin does not see $r$, because $r$ is chosen after $w$ is sent. With a deterministic $V$ the definition is the verifier definition of NP, and with $q = 0$ it is the definition of BPP. So $\mathsf{NP} \cup \mathsf{BPP} \subseteq \mathsf{MA}$.

**Error reduction.** Arthur runs $V(x, w, \cdot)$ $t$ times on the same $w$ with fresh coins and takes the majority. For each fixed $w$ this is ordinary amplification, so by the [Chernoff bound](/chernoff-bound/) both errors fall to $2^{-\Omega(t)}$, and the proof $w$ does not grow.

**Perfect completeness.** Every $L \in \mathsf{MA}$ has a game in which Arthur always accepts a yes-instance with the right proof. Proof: reduce the error to $\delta < 1/\ell$, where $\ell$ is the number of coins, as in the [Sipser-Gács theorem](/sipser-gacs-theorem/). The new proof is $w$ together with $\ell$ shifts $s_1, \ldots, s_\ell \in \{0,1\}^\ell$. Arthur picks $r$ and accepts if $V(x, w, r \oplus s_i) = 1$ for some $i$. If $x \in L$ and $w$ is a good proof, the accepting set of $V(x, w, \cdot)$ has density at least $1 - \delta$, and by Lautemann's argument some shifts cover all of $\{0,1\}^\ell$, so Arthur accepts for every $r$. If $x \notin L$, every accepting set has density at most $\delta$, and for any proof the probability of acceptance is at most $\ell \delta < 1$, which repetition makes small.

**MA is in the second level.** The game with perfect completeness gives

$$x \in L \iff \exists w, s_1, \ldots, s_\ell\; \forall r : \bigvee_{i=1}^{\ell} V(x, w, r \oplus s_i) = 1,$$

because on a no-instance some $r$ makes Arthur reject. So $\mathsf{MA} \subseteq \Sigma_2^p$. Together with $\mathsf{MA} \subseteq \mathsf{AM} \subseteq \Pi_2^p$ this gives $\mathsf{MA} \subseteq \Sigma_2^p \cap \Pi_2^p$.

**MA is a subset of AM.** Reduce the error of the MA game to $\delta < 2^{-q}/3$, where $q$ is the length of the proof; repetition on the same proof keeps $q$ fixed. Now let Arthur send $r$ first and let Merlin answer with $w$; Arthur accepts if $V(x, w, r) = 1$. If $x \in L$, Merlin sends the good proof and is accepted with probability at least $1 - \delta$. If $x \notin L$, then for each $w$ the set of bad $r$ has probability at most $\delta$, and by the [union bound](/union-bound/) over the $2^q$ proofs, $\Pr_r[\exists w : V(x, w, r) = 1] \le 2^q \delta < 1/3$. $\square$

## Examples and non-examples

**Examples.**

- *Every language in NP and every language in BPP.*
- *Existential polynomial identity testing.* The input is a polynomial $C(x_1, \ldots, x_a, y_1, \ldots, y_b)$ over a prime field $\mathbb{F}_p$, given by an arithmetic formula of total degree $d$ with $3d < p$. The question is whether some Boolean $x \in \{0,1\}^a$ makes $C(x, y)$ a nonzero polynomial in $y$. Merlin sends $x$. Arthur picks $y$ uniformly in $\mathbb{F}_p^b$ and accepts if $C(x, y) \ne 0$. If $C(x, \cdot)$ is nonzero, it is accepted with probability at least $1 - d/p > 2/3$ by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/). If $C(x, \cdot)$ is the zero polynomial for every Boolean $x$, Arthur never accepts. The problem is NP-hard: for a CNF formula $\varphi$, the formula $\tilde\varphi(x) \cdot y_1$, with the arithmetization of $\varphi$ from [IP = PSPACE](/ip-equals-pspace/), is nonzero in $y$ exactly when $x$ satisfies $\varphi$. It is in NP if [polynomial identity testing](/polynomial-identity-testing/) has a deterministic polynomial-time algorithm, which is not known.
- *A worked case.* Over $\mathbb{F}_{11}$, let $F(x_1, x_2, y) = (x_1 + x_2 - 1)(y^2 - 3y + 2)$. For $x = (0, 0)$ or $x = (1, 1)$, the first factor is $\mp 1$, and $y^2 - 3y + 2 = (y - 1)(y - 2)$ vanishes only at $y = 1, 2$, so Arthur accepts with probability $9/11$. For $x = (0, 1)$ or $(1, 0)$ the polynomial is $0$ and Arthur never accepts. So $F$ is a yes-instance with proof $(0, 0)$. For $G(x_1, x_2, y) = (x_1 - x_2)(x_1 + x_2 - 1)(y + 5)$, one factor vanishes for every Boolean $x$, so $G$ is a no-instance and no proof is ever accepted. If Arthur tests the same $x$ at $k$ independent points and accepts when one value is nonzero, the completeness error for $F$ is $(2/11)^k$: about $0.182$, $0.0331$ and $0.00601$ for $k = 1, 2, 3$.

**Non-examples.**

- *coNP-complete problems, unless the hierarchy collapses.* $\mathsf{MA} \subseteq \mathsf{AM}$, and $\mathsf{coNP} \subseteq \mathsf{AM}$ would collapse the polynomial hierarchy to its second level (Boppana, Håstad and Zachos 1987; see [AM](/arthur-merlin/)).
- *PSPACE-complete problems, unless $\mathsf{PSPACE} = \Sigma_2^p$*, since MA lies in $\Sigma_2^p$.
- *Graph non-isomorphism is in AM but not known to be in MA.* Its public-coin protocol needs Arthur's coins before Merlin's message.

## Related definitions

- [AM](/arthur-merlin/) is the class with the opposite order: Arthur's coins first, then Merlin's message. $\mathsf{MA} \subseteq \mathsf{AM}$, and the converse is open.
- *Derandomization.* If some language in $\mathsf{E} = \mathsf{DTIME}(2^{O(n)})$ needs circuits of size $2^{\varepsilon n}$ for some $\varepsilon > 0$, then the generator of Impagliazzo and Wigderson ([Impagliazzo-Wigderson theorem](/impagliazzo-wigderson-theorem/)) has seeds of $O(\log n)$ bits and fools every polynomial-size circuit. For fixed $x$ and $w$, the test $r \mapsto V(x, w, r)$ is such a circuit, so an NP machine can guess $w$ and try all seeds. Then $\mathsf{MA} = \mathsf{NP}$. Without such an assumption, it is not known whether $\mathsf{MA} = \mathsf{NP}$.
- [QMA](/qma/) is the quantum version: the proof is a quantum state and Arthur is a quantum circuit. $\mathsf{MA} \subseteq \mathsf{QMA}$.
- [BPP](/bpp/) is MA without Merlin, and [NP](/np/) is MA without coins.
- The [Sipser-Gács theorem](/sipser-gacs-theorem/) gives the covering argument used above for perfect completeness and for $\mathsf{MA} \subseteq \Sigma_2^p$.

## References
