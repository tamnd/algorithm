---
tag: 5ZVYZ8
kind: definition
slug: interactive-proofs
name: IP
aliases:
- interactive proof systems
area: complexity/complexity-classes
level: advanced
summary: "The languages with an interactive proof: a randomized polynomial-time verifier talks with a prover of unlimited power and errs with probability at most 1/3. IP = PSPACE."
prereqs: [np, bpp, probabilistic-turing-machine, polynomial-time-verifier]
see_also: [ip-equals-pspace, arthur-merlin, merlin-arthur, multi-prover-interactive-proofs, qma, zero-knowledge-proof, probabilistically-checkable-proof, graph-isomorphism-problem]
sources:
  - paper: doi:10.1137/0218012
    title: Shafi Goldwasser, Silvio Micali and Charles Rackoff, The knowledge complexity of interactive proof systems, SIAM Journal on Computing 18(1), 186 to 208 (1989)
    locator: Section 1 and the definition of interactive proof systems with completeness and soundness; preliminary version in STOC 1985, 291 to 304
  - paper: doi:10.1145/22145.22192
    title: László Babai, Trading group theory for randomness, Proceedings of the 17th Annual ACM Symposium on Theory of Computing, 421 to 429 (1985)
    locator: the Arthur-Merlin games, the public-coin form of the definition
  - paper: doi:10.1145/116825.116852
    title: Oded Goldreich, Silvio Micali and Avi Wigderson, Proofs that yield nothing but their validity or all languages in NP have zero-knowledge proof systems, Journal of the ACM 38(3), 690 to 728 (1991)
    locator: the interactive proof for graph non-isomorphism; preliminary version in FOCS 1986
  - paper: doi:10.1145/12130.12137
    title: Shafi Goldwasser and Michael Sipser, Private coins versus public coins in interactive proof systems, Proceedings of the 18th Annual ACM Symposium on Theory of Computing, 59 to 68 (1986)
    locator: the simulation of private coins by public coins with two extra rounds
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 8, Interactive proofs (deterministic verifiers, the class IP, graph non-isomorphism, public coins)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage (2013)
    locator: Section 10.4, Interactive proof systems (graph non-isomorphism, the definition of IP)
  - book: isbn:9780521884730
    title: Oded Goldreich, Computational Complexity, A Conceptual Perspective, Cambridge University Press (2008)
    locator: Chapter 9, Probabilistic proof systems (interactive proof systems)
---

IP is the class of [decision problems](/decision-problem/) that have an *interactive proof*: a randomized verifier that runs in polynomial time exchanges messages with a prover of unlimited power, and in the end it accepts or rejects. On a yes-instance some prover makes the verifier accept with probability at least $2/3$. On a no-instance every prover fails with probability at least $2/3$. Goldwasser, Micali and Rackoff defined the model in 1985, and Babai gave a public-coin form in the same year. The class turned out to be large: [IP = PSPACE](/ip-equals-pspace/).

## Definition

**Model.** The verifier $V$ is a [probabilistic Turing machine](/probabilistic-turing-machine/) with several tapes ([multitape Turing machine](/multitape-turing-machine/)). It reads the input $x$ and a random string $r$, and it runs in time polynomial in $|x|$ over the whole interaction. The prover $P$ is any function that maps $x$ and the messages so far to its next message. It has no bound on time or space, and it does not see $r$: the coins of the verifier are *private*. The verifier and the prover take turns, and the messages $m_1, m_2, \ldots, m_k$ form the *transcript*. At the end, $V$ computes a bit from $x$, $r$ and the transcript. The number of messages $k = k(|x|)$ is a polynomial, and each message has polynomial length, because $V$ must read it. Write $\langle V, P\rangle(x)$ for the output bit; it is a random variable over $r$. A randomized prover is never better than the best deterministic one, because its success probability is an average over its own coins, so we take $P$ deterministic.

**Definition (Goldwasser, Micali and Rackoff).** A language $L \subseteq \{0,1\}^*$ is in $\mathsf{IP}$ if there are a polynomial-time verifier $V$ and a polynomial $k$ such that, with $k(|x|)$ messages:

$$\textbf{completeness: } x \in L \Rightarrow \exists P : \Pr_r\big[\langle V, P\rangle(x) = 1\big] \ge \tfrac23, \qquad \textbf{soundness: } x \notin L \Rightarrow \forall P^* : \Pr_r\big[\langle V, P^*\rangle(x) = 1\big] \le \tfrac13.$$

$\mathsf{IP}[k]$ is the class with $k(n)$ messages, and $\mathsf{IP} = \bigcup_{c} \mathsf{IP}[n^c]$. The prover $P$ of the completeness condition is the *honest* prover. The prover $P^*$ of the soundness condition may do anything, so a proof of soundness must cover every strategy, not only small changes of the honest one.

**The constants $2/3$ and $1/3$ do not matter.** Run the protocol $t$ times in sequence with fresh coins and accept if the majority of the runs accept. Given any history, a run accepts a no-instance with probability at most $1/3$, whatever the prover does, so the number of accepting runs is dominated by a binomial variable with mean $t/3$. By the [Chernoff bound](/chernoff-bound/), both errors fall to $2^{-\Omega(t)}$, and the number of messages grows by the factor $t$. For several provers, repetition in parallel is harder; see the [parallel repetition theorem](/parallel-repetition-theorem/).

**Both kinds of randomness are needed.** Two variants of the definition collapse to [NP](/np/).

- *Deterministic verifier.* If $V$ uses no coins, then $L \in \mathsf{NP}$. Proof: with fixed $x$, the messages of $V$ are functions of the earlier messages of the prover, so acceptance has probability $0$ or $1$. Soundness at most $1/3$ then means probability $0$. An NP machine guesses the whole transcript, computes the messages of $V$ to check that the transcript is consistent, and accepts if $V$ accepts. If $x \in L$, the honest transcript is a valid guess. If $x \notin L$ and some consistent transcript made $V$ accept, the prover that sends those messages would win with probability $1$. The converse $\mathsf{NP} \subseteq \mathsf{IP}$ is the one-message protocol in which the prover sends a [certificate](/certificate/).
- *Perfect soundness.* If no-instances are accepted with probability $0$, then $L \in \mathsf{NP}$, even with a randomized verifier. The NP machine guesses $r$ and the prover's messages and simulates $V$. A guessed pair that makes $V$ accept on a no-instance would give a prover that wins with positive probability: send the guessed messages whatever $V$ says.

Perfect completeness, in contrast, costs nothing: every language in IP has a protocol in which the honest prover is accepted with probability $1$. This follows from IP = PSPACE, because the protocol for PSPACE has this property.

**Upper bound.** $\mathsf{IP} \subseteq \mathsf{PSPACE}$: the best success probability of any prover can be computed in polynomial space by a recursion over the transcript. The proof, and the protocol for the converse, are on [IP = PSPACE](/ip-equals-pspace/).

## Examples and non-examples

**Examples.**

- *Every language in NP.* The prover sends a certificate and $V$ runs the [polynomial-time verifier](/polynomial-time-verifier/). No randomness is used.
- *Every language in BPP.* The verifier ignores the prover and runs the [BPP](/bpp/) machine. No messages are used.
- *Graph non-isomorphism (GNI).* The input is two graphs $G_0, G_1$ on the vertex set $\{1, \ldots, n\}$, and the question is whether they are *not* isomorphic. GNI is the complement of the [graph isomorphism problem](/graph-isomorphism-problem/), so it is in [coNP](/co-np/), but it is not known to be in NP. The protocol of Goldreich, Micali and Wigderson: $V$ picks a secret bit $b$ and a uniform random permutation $\pi$ of the vertices, and sends $H = \pi(G_b)$. The prover answers a bit $b'$, and $V$ accepts if $b' = b$. If the graphs are not isomorphic, $H$ is isomorphic to exactly one of them, and the honest prover finds $b$ by testing both, which needs no bound on its time. If the graphs are isomorphic, $\pi(G_0)$ and $\pi(G_1)$ have the same distribution, so $b$ is independent of $H$ and every prover is right with probability exactly $1/2$. Two runs in sequence bring the soundness error to $1/4$, and $k$ runs to $2^{-k}$.
- *A worked case of GNI.* Take $n = 4$, $G_0$ the path $1{-}2{-}3{-}4$ and $G_1$ the star with center $1$. The $24$ permutations give $12$ labeled paths (the path has $2$ automorphisms) and $4$ labeled stars (the star has $6$ automorphisms). These $16$ graphs are distinct, so $H$ always reveals $b$, and the honest prover wins with probability $1$. Now take $G_1$ to be the path $3{-}1{-}4{-}2$ instead, which is isomorphic to $G_0$. Each of the $12$ labeled paths arises from $2$ permutations when $b = 0$ and from $2$ permutations when $b = 1$, so the best prover wins with probability $24/48 = 1/2$.
- *Counting and quantified formulas.* The number of satisfying assignments of a CNF formula and the truth of a quantified Boolean formula ([QSAT](/qsat/)) have interactive proofs. These are the sum-check protocol of Lund, Fortnow, Karloff and Nisan and the protocol of Shamir, both on [IP = PSPACE](/ip-equals-pspace/). The second one puts all of PSPACE in IP.

**Non-examples.**

- *The GNI protocol with public coins.* If the prover could see $b$, it would always answer correctly, and the protocol would accept isomorphic pairs too. Private coins matter for this protocol. GNI still has a public-coin protocol, but it uses a different idea (see [AM](/arthur-merlin/)).
- *Problems outside PSPACE.* A language that is complete for EXPSPACE is not in IP, because $\mathsf{IP} = \mathsf{PSPACE}$ and PSPACE is a proper subset of [EXPSPACE](/expspace/) by the [space hierarchy theorem](/space-hierarchy-theorem/). An undecidable language such as the [halting problem](/halting-problem/) is not in IP either.
- *Arguments.* If soundness is required only against provers that run in polynomial time, the protocol is an *argument*, not an interactive proof. Arguments can rest on cryptographic assumptions and are a different notion.

## Related definitions

- [AM](/arthur-merlin/) and [MA](/merlin-arthur/) are the classes with public coins and a constant number of messages. Goldwasser and Sipser (1986) proved $\mathsf{IP}[k] \subseteq \mathsf{AM}[k + 2]$, so private coins can be replaced by public coins with two more messages.
- [MIP](/multi-prover-interactive-proofs/) has two or more provers that cannot talk to each other during the protocol. It equals NEXP ([MIP = NEXP](/mip-equals-nexp/)).
- A [probabilistically checkable proof](/probabilistically-checkable-proof/) is a fixed proof string that the verifier reads at a few random places. A fixed string cannot change its answers after it sees the questions, which is the main difference from a prover.
- [QMA](/qma/) is the quantum analogue of MA. The quantum analogue of IP is QIP, and it also equals PSPACE (Jain, Ji, Upadhyay and Watrous 2011).
- A [zero-knowledge proof](/zero-knowledge-proof/) is an interactive proof in which the verifier learns nothing except that the statement is true. The GNI protocol above has this property for an honest verifier.
- In [NP](/np/), the proof is a [certificate](/certificate/) that a deterministic verifier reads in full. IP replaces the certificate by a conversation and allows a small error.

## References
