---
tag: EZD2B7
kind: definition
slug: zero-knowledge-proof
name: Zero-knowledge proof
aliases:
- ZKP
- zero-knowledge argument
area: cryptography/protocols
level: intro
summary: A prover convinces a verifier a statement is true while revealing nothing beyond its truth.
prereqs: [interactive-proofs, np, commitment-scheme, computational-indistinguishability]
see_also: [proof-of-knowledge, sigma-protocol, fiat-shamir-heuristic, zk-snark, zk-stark, graph-isomorphism-problem, three-coloring, secure-multiparty-computation]
sources:
  - paper: doi:10.1137/0218012
    title: Shafi Goldwasser, Silvio Micali and Charles Rackoff, The knowledge complexity of interactive proof systems, SIAM Journal on Computing 18(1), 1989, 186-208 (STOC 1985)
    locator: Section 1 (interactive proof systems, completeness and soundness) and the definition of zero knowledge by a simulator, with the perfect, statistical and computational forms
  - paper: doi:10.1145/116825.116852
    title: Oded Goldreich, Silvio Micali and Avi Wigderson, Proofs that yield nothing but their validity or all languages in NP have zero-knowledge proof systems, Journal of the ACM 38(3), 1991, 690-728 (FOCS 1986)
    locator: the perfect zero-knowledge proof for graph isomorphism and the computational zero-knowledge proof for graph 3-colorability with commitments
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Chapter 4, Zero-Knowledge Proof Systems (interactive proofs, zero knowledge, auxiliary input, composition, NP in zero knowledge, arguments)
  - paper: "Oded Goldreich and Yair Oren, Definitions and properties of zero-knowledge proof systems, Journal of Cryptology 7(1), 1994, 1-32"
    title: Oded Goldreich and Yair Oren, Definitions and properties of zero-knowledge proof systems
    locator: auxiliary-input zero knowledge and its closure under sequential composition
  - paper: "Oded Goldreich and Hugo Krawczyk, On the composition of zero-knowledge proof systems, SIAM Journal on Computing 25(1), 1996, 169-192"
    title: Oded Goldreich and Hugo Krawczyk, On the composition of zero-knowledge proof systems
    locator: zero knowledge is not closed under parallel composition, and three-round black-box zero-knowledge proofs exist only for languages in BPP
  - paper: "Gilles Brassard, David Chaum and Claude Crepeau, Minimum disclosure proofs of knowledge, Journal of Computer and System Sciences 37(2), 1988, 156-189"
    title: Gilles Brassard, David Chaum and Claude Crepeau, Minimum disclosure proofs of knowledge
    locator: arguments, with soundness only against provers of bounded power and perfect zero knowledge
  - paper: "Lance Fortnow, The complexity of perfect zero-knowledge, STOC 1987, 204-209"
    title: Lance Fortnow, The complexity of perfect zero-knowledge
    locator: languages with statistical zero-knowledge proofs lie in co-AM
  - url: https://people.cs.georgetown.edu/jthaler/ProofsArgsAndZK.html
    title: Justin Thaler, Proofs, Arguments, and Zero-Knowledge, monograph, 2022
    locator: the chapters on zero-knowledge proofs and arguments, sigma protocols and commitments
---

A zero-knowledge proof is an [interactive proof](/interactive-proofs/) in which the verifier becomes convinced that a statement is true and learns nothing else. "Learns nothing" has an exact meaning: whatever the verifier sees in the interaction, it could have produced alone, by a program called a simulator that does not know the secret. Goldwasser, Micali and Rackoff gave the definition in 1985. Goldreich, Micali and Wigderson showed in 1986 that, if one-way functions exist, every language in [NP](/np/) has a zero-knowledge proof.

## Definition

**Notation.** $L$ is a language in [NP](/np/) with a relation $R$: $x \in L$ if and only if $(x, w) \in R$ for some witness $w$. $(P, V)$ is a pair of interactive programs; $P$ gets $(x, w)$ and $V$ gets $x$. $\langle P(w), V \rangle(x)$ is the output bit of $V$ (1 is accept). $\mathrm{view}_{V^*}(x)$ is everything a verifier $V^*$ sees: its random coins, its auxiliary input $z$, and all messages from $P$. "Negligible" means smaller than $1/n^c$ for each $c$ and large $n = |x|$. "Efficient" means probabilistic polynomial time (PPT).

**Interactive proof.** $(P, V)$ is an interactive proof for $L$ with soundness error $\varepsilon$ if $V$ is efficient and:

1. **Completeness.** For each $(x, w) \in R$, $\Pr[\langle P(w), V \rangle(x) = 1] \ge 1 - \mathrm{negl}(n)$. It has perfect completeness if the probability is 1.
2. **Soundness.** For each $x \notin L$ and each prover $P^*$, even one of unbounded power, $\Pr[\langle P^*, V \rangle(x) = 1] \le \varepsilon$.

Repetition makes $\varepsilon$ small: $k$ sequential runs, with acceptance only if all accept, have error $\varepsilon^k$.

**Zero knowledge.** $(P, V)$ is zero knowledge if for each efficient verifier $V^*$ there is a simulator $S$, which runs in expected polynomial time and does not get $w$, with
$$\{S(x, z)\}_{x \in L} \approx \{\mathrm{view}_{V^*(z)}(x)\}_{x \in L}$$
for each auxiliary input $z$. The strength of $\approx$ gives three forms:

- **Perfect zero knowledge.** The two distributions are equal.
- **Statistical zero knowledge.** Their statistical distance is negligible.
- **Computational zero knowledge.** No efficient distinguisher tells them apart with more than negligible advantage ([computational indistinguishability](/computational-indistinguishability/)).

**Honest-verifier zero knowledge (HVZK).** The weaker property in which a simulator only needs to exist for the honest $V$. Many efficient protocols, such as [sigma protocols](/sigma-protocol/) with a large challenge space, are only known to be HVZK.

**Argument.** If soundness holds only against efficient provers, $(P, V)$ is an argument, or a zero-knowledge argument. Arguments can have perfect zero knowledge for all of NP (Brassard, Chaum and Crépeau 1988); [zk-SNARKs](/zk-snark/) and [zk-STARKs](/zk-stark/) are arguments.

### Basic facts

1. **Auxiliary input gives composition.** With auxiliary input in the definition, zero knowledge is closed under sequential composition (Goldreich and Oren 1994). This is why the definition includes $z$.
2. **Parallel composition can fail.** Zero knowledge is not closed under parallel composition in general, and only languages in BPP have three-round black-box zero-knowledge proofs (Goldreich and Krawczyk 1996).
3. **NP in zero knowledge.** If one-way functions exist, each language in NP has a computational zero-knowledge proof (GMW 1991), by a reduction to 3-colorability and [commitments](/commitment-scheme/).
4. **Limits of statistical zero knowledge.** Languages with statistical zero-knowledge proofs lie in AM ∩ co-AM (Fortnow 1987, with Aiello and Håstad). So an NP-complete language has no such proof unless the polynomial hierarchy collapses.
5. **Zero knowledge needs interaction or a setup.** Without a common reference string or a [random oracle](/random-oracle-model/), only languages in BPP have non-interactive zero-knowledge proofs. The [Fiat-Shamir heuristic](/fiat-shamir-heuristic/) removes interaction in the random oracle model.
6. **Zero knowledge is not knowledge soundness.** Soundness says that a false statement is rejected. A [proof of knowledge](/proof-of-knowledge/) says more: a prover that is accepted knows a witness.

## Examples and non-examples

**Graph isomorphism, perfect zero knowledge.** The common input is two graphs $G_0, G_1$ on $n$ vertices. The prover knows $\pi$ with $G_1 = \pi(G_0)$. In a round, the prover sends $H = \sigma(G_1)$ for a uniform permutation $\sigma$. The verifier sends a uniform bit $b$. The prover answers $\tau = \sigma$ if $b = 1$ and $\tau = \sigma \circ \pi$ if $b = 0$. The verifier accepts if $\tau(G_b) = H$.

- *Completeness.* $\sigma(\pi(G_0)) = \sigma(G_1) = H$.
- *Soundness error $1/2$.* If $G_0 \not\cong G_1$, a graph $H$ is isomorphic to at most one of them, so at most one bit can be answered.
- *Simulator.* For an honest verifier: pick $b$ and $\tau$ uniform, output $(\tau(G_b), b, \tau)$. In the real run, $\tau$ is uniform for each $b$, because $\sigma \mapsto \sigma \circ \pi$ is a bijection, and $H = \tau(G_b)$. The two distributions are equal. For a cheating verifier $V^*$ that picks $b$ from $H$: guess $b'$, make $H = \tau(G_{b'})$, run $V^*$ on $H$, and keep the output if $V^*$ says $b'$; else rewind and try again. $H$ does not depend on $b'$, so each try succeeds with probability $1/2$, and the expected number of tries is 2.

A worked round with $n = 4$. $G_0$ is the path $\{01, 12, 23\}$ and $\pi = (2, 0, 3, 1)$ (vertex $v$ goes to $\pi[v]$), so $G_1 = \{02, 03, 13\}$. With $\sigma = (1, 2, 3, 0)$ the prover sends $H = \{01, 02, 13\}$. If $b = 1$, $\tau = (1, 2, 3, 0)$ and $\tau(G_1) = H$. If $b = 0$, $\tau = \sigma \circ \pi = (3, 1, 0, 2)$, and $\tau(G_0) = \{13, 01, 02\} = H$.

**Graph 3-coloring, computational zero knowledge.** The prover knows a proper coloring $c : V \to \{0, 1, 2\}$ of $G = (V, E)$. In a round it picks a uniform permutation $\phi$ of the three colors and commits to $\phi(c(v))$ for each vertex. The verifier picks a uniform edge $uv$. The prover opens the two commitments, and the verifier accepts if both open and the two colors are different.

- *Soundness.* If $G$ has no 3-coloring, each fixed list of committed colors has at least one bad edge, so a binding commitment gives acceptance at most $1 - 1/|E|$ per round. For $K_4$ the best cheater colors with one bad edge and passes with probability exactly $5/6$. After $k|E|$ rounds the error is at most $(1 - 1/|E|)^{k|E|} \le e^{-k}$.
- *Simulator.* Pick the edge $uv$ first, give $u$ and $v$ two uniform distinct colors, and commit to color 0 for each other vertex. The opened part of the view, (edge, color of $u$, color of $v$), has the same distribution as in the real run: uniform over edges times the 6 ordered pairs of distinct colors. The unopened commitments differ, so the two views are equal only up to the hiding of the commitment. With a computationally hiding commitment the protocol is computational zero knowledge. For a cheating verifier the simulator guesses the edge and rewinds, with about $|E|$ expected tries.

**Code.** The Python file `zero_knowledge_proof.py` runs both protocols with local simulated parties and SHA-256 commitments $H(r \,\|\, \text{color})$ with a 32-byte $r$. The tests check, by enumeration on toy graphs:

- For graph isomorphism on 4 vertices, the 48 real transcripts (24 values of $\sigma$ times 2 bits) and the 48 simulated transcripts are the same multiset. The rewinding simulator matches the view of a fixed cheating verifier exactly, with about 2 tries per transcript.
- The prover for the path against the star $K_{1,3}$, which is not isomorphic to it, passes exactly half of all (guess, $\tau$, $b$) choices.
- For the 4-cycle with a chord, the opened views of the real and simulated 3-coloring runs are the same 30 values, each once. For $K_4$ the exhaustive best cheater gets $5/6$.

There are no official test vectors for these protocols. The code is for study only, is not constant time and must not be used for real data. Real systems use reviewed libraries, for example arkworks or libsnark for proof systems, and libsodium or a FIPS 140 validated module for the underlying hash and group operations.

**Non-examples.**

- *Sending the witness.* The prover sends $\pi$ or the coloring. This is complete and sound, but the verifier learns $w$, which it could not compute alone if the problem is hard. Not zero knowledge.
- *Opening every vertex.* In the 3-coloring protocol, if the prover opens all commitments, the verifier learns a full coloring (up to a color permutation). Not zero knowledge.
- *No color permutation.* If the prover uses the same coloring in each round, the verifier collects the colors of all vertices over many rounds. Not zero knowledge.
- *Parallel repetition of the GI protocol.* $k$ copies in one round, with a $k$-bit challenge, are HVZK with error $2^{-k}$, but no simulator is known for a verifier that picks the challenge as a hash of the first messages. This is exactly the step that the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/) uses on purpose to make a signature.
- *Sound but trivial.* A protocol in which the verifier decides $x \in L$ alone is zero knowledge, but it is only possible for languages in BPP.

## Related definitions

- **[Interactive proofs](/interactive-proofs/).** The model of completeness and soundness that zero knowledge adds to.
- **[Commitment scheme](/commitment-scheme/).** The tool that hides the coloring until the challenge comes. Hiding gives zero knowledge and binding gives soundness.
- **[Proof of knowledge](/proof-of-knowledge/).** Adds an extractor: a prover that is accepted must know a witness.
- **[Sigma protocol](/sigma-protocol/).** The three-move form with special soundness and special honest-verifier zero knowledge, as in Schnorr's protocol.
- **[Fiat-Shamir heuristic](/fiat-shamir-heuristic/).** Replaces the verifier's challenge by a hash, which gives a non-interactive proof in the random oracle model.
- **[zk-SNARK](/zk-snark/) and [zk-STARK](/zk-stark/).** Non-interactive arguments with short proofs and fast verification.
- **Witness indistinguishability.** A weaker property: the view does not show which of several witnesses the prover used. It is closed under parallel composition.
- **[Secure multiparty computation](/secure-multiparty-computation/).** Uses zero-knowledge proofs to force malicious parties to follow the protocol (the GMW compiler).

## References
