---
tag: EASH3X
kind: model
slug: malicious-adversary-model
name: Malicious adversary model
aliases:
- active adversary model
area: cryptography/protocols
level: advanced
summary: Corrupted parties may deviate from the protocol in any way. Security compares a real run with an ideal world in which they may only change inputs and, in some versions, abort.
history:
  year: 1987
  people: [Oded Goldreich, Silvio Micali, Avi Wigderson]
  note: GMW 1987 gave the compiler from semi-honest to malicious security with commitments, zero-knowledge proofs and coin tossing.
prereqs: [semi-honest-model, commitment-scheme, zero-knowledge-proof]
see_also: [secure-multiparty-computation, universal-composability, cut-and-choose, bgw-protocol, oblivious-transfer-extension, byzantine-failure-model, fair-coin-flipping]
sources:
  - paper: doi:10.1145/28395.28420
    title: "Oded Goldreich, Silvio Micali and Avi Wigderson, How to play any mental game, or a completeness theorem for protocols with honest majority, STOC 1987, pages 218 to 229"
    locator: the compiler from semi-honest to malicious security and the honest majority theorem
  - book: isbn:9780521830843
    title: Oded Goldreich, Foundations of Cryptography, Volume 2, Basic Applications, Cambridge University Press, 2004
    locator: Chapter 7, the malicious model (the ideal model with abort, the compiler with input commitment, coin tossing into the well and authenticated computation, and the multiparty case)
  - book: isbn:9783642143021
    title: Carmit Hazay and Yehuda Lindell, Efficient Secure Two-Party Protocols, Techniques and Constructions, Springer, 2010
    locator: Chapter 2 (security with abort, the covert model, and the relation between the models)
  - paper: doi:10.1145/12130.12168
    title: "Richard Cleve, Limits on the security of coin flips when half the processors are faulty, STOC 1986, pages 364 to 369"
    locator: the main theorem (no fair coin flip with a dishonest majority)
  - paper: doi:10.1007/978-3-642-32009-5_38
    title: "Ivan Damgard, Valerio Pastro, Nigel Smart and Sarah Zakarias, Multiparty computation from somewhat homomorphic encryption, CRYPTO 2012, LNCS 7417, pages 643 to 662"
    locator: the representation of shared values with MACs and the MAC check protocol of the online phase
  - paper: "Ran Canetti, Uriel Feige, Oded Goldreich and Moni Naor, Adaptively secure multi-party computation, STOC 1996"
    locator: the adaptive corruption model and the use of non-committing encryption
---

The malicious adversary model lets corrupted parties do anything: send wrong messages, change their inputs, wait to see the honest messages of a round before they send their own, collude, and stop at any time. A protocol for [secure multiparty computation](/secure-multiparty-computation/) is secure in this model if every such attack can be simulated in an ideal world where the corrupted parties can only choose their inputs and, depending on the version, abort. It is also called the active model. It is stronger than the [semi-honest model](/semi-honest-model/), where corrupted parties follow the protocol, and Goldreich, Micali and Wigderson showed in 1987 how to compile any semi-honest protocol into a malicious one.

**Notation.** $n$ parties, at most $t$ corrupted, coalition $I$, functionality $f$, protocol $\pi$, real adversary $\mathcal{A}$, simulator $\mathcal{S}$, security parameter $\lambda$, statistical security parameter $s$ (the cheating probability is at most about $2^{-s}$), and $p$ a prime for the field $\mathbb{F}_p$.

## The machine

**The adversary.** $\mathcal{A}$ is a probabilistic polynomial time machine (or unbounded, for information-theoretic results) that controls the parties in $I$. It sees their inputs, random tapes and received messages, and it chooses every message they send, as any function of everything it has seen. It is *rushing*: in each round it may wait for the messages of the honest parties before it sends its own. It may stop sending at any point.

**Corruption.** In the *static* model, $I$ is fixed before the run. In the *adaptive* model, $\mathcal{A}$ may corrupt parties during the run and then sees their whole past state; the simulator must then explain the past messages of a newly corrupted party with an input it learns only at that time, which needs tools such as non-committing encryption (Canetti, Feige, Goldreich and Naor 1996).

**The ideal worlds.** The trusted party computes $f$, and the simulator $\mathcal{S}$ controls the parties in $I$. Three versions:

- *Full security (guaranteed output).* $\mathcal{S}$ chooses inputs $x_I'$ for the coalition (if it sends nothing, a default input is used). Every party gets its output.
- *Fairness.* Either all parties get the output, or none does.
- *Security with abort.* $\mathcal{S}$ chooses $x_I'$, receives the coalition's outputs, and then tells the trusted party either to deliver the honest outputs or to send them $\bot$. A variant with *identifiable abort* also names one corrupted party when it aborts.

$\pi$ is secure if for every $\mathcal{A}$ there is an $\mathcal{S}$ such that the joint distribution of $\mathcal{A}$'s output and the honest outputs is indistinguishable in the two worlds, for every input and every $I$ with $|I| \le t$. The honest outputs are in the distribution, so an attack that changes the output of the honest parties to a value that $f$ never gives breaks the definition.

**What the ideal world allows.** Input substitution and abort cannot be prevented by any protocol, so they are allowed. A malicious party may claim a salary of 0 in a sum. The definition guarantees that this is all it can do.

**Attacks on a semi-honest protocol.** In the additive sharing sum, each party $j$ adds the shares it holds and broadcasts the partial sum. Three attacks by one malicious party:

- *A fixed shift.* The party adds $e$ to its partial sum. With inputs $(52, 61, 47)$ and $e = 1000$, every honest party outputs 1160 instead of 160, and nothing in the protocol shows the change. For a plain sum this is no worse than the input $47 + 1000$, so input substitution covers it; on the shares of a product or a comparison the same change has no such excuse.
- *A forced output.* The party is rushing: it waits for all other partial sums and then sends the value that makes the total 0. The output is then 0 for every honest input. In the ideal world the cheater must fix its input before it learns anything, so the output would still depend on the honest inputs. No simulator can produce this, so the protocol is not secure in this model.
- *Split views.* Without a broadcast channel, the party sends different partial sums to different parties. With errors $(0, 5, 0)$ the three parties output 160, 165 and 160. In the ideal world all honest parties get the same value.

**The SPDZ style MAC check.** To stop such changes, every shared value $x$ carries additive shares $x_j$ of $x$ and $m_j$ of $\alpha x$, where $\alpha = \sum_j \alpha_j$ is a global key and party $j$ holds only $\alpha_j$. These sharings are linear, so sums and public constants are local. To open $x$:

1. Each party broadcasts $x_j$, and all compute $x' = \sum_j x_j$.
2. Each party computes $\sigma_j = m_j - \alpha_j x'$ and broadcasts a [commitment](/commitment-scheme/) to it.
3. All open their commitments. If $\sum_j \sigma_j \ne 0$, abort; else accept $x'$.

If a cheater broadcasts $x_c + e$, then $\sum_j \sigma_j = \alpha x - \alpha(x + e) = -\alpha e$, plus any change $\delta$ it makes to $\sigma_c$. It passes only if $\delta = \alpha e$. For $e \ne 0$ this needs $\alpha$, which is uniform and hidden from any coalition of at most $n - 1$ parties, so it passes with probability exactly $1/p$. The commitments matter: without them, the last party to speak sets $\sigma_c = -\sum_{j \ne c} \sigma_j$ and always passes.

The page's code runs this with a trusted dealer in place of the preprocessing phase. In $\mathbb{F}_{2^{61}-1}$, the fixed shift ($e = 1$, $1000$ or $p - 1$, by each of three parties) and the forced output are caught every time. In the toy field $p = 101$ with a random correction $\delta$, 307 of 30000 attacks passed, against an expected $30000/101 \approx 297.0$. Without commitments, a rushing party forces the output 1160 and passes. The code is for study only, is not constant time, and runs on toy fields with local simulated parties. Use a maintained framework such as MP-SPDZ for real data. There are no official test vectors for these protocols.

## What it counts

- **The overhead over the semi-honest protocol**, in rounds, communication and computation. For garbled circuits with [cut-and-choose](/cut-and-choose/) the factor is about the number $s$ of circuits; for SPDZ style protocols the online phase costs a small constant factor and the work moves to preprocessing.
- **The cheating probability**: the statistical error of the checks, stated as $2^{-s}$ with $s$ typically 40, or $1/p$ per MAC check.
- **The threshold** $t$ and the guarantee (full security, fairness, abort) that the protocol reaches for it.

## Relation to other models

- **Semi-honest model.** A semi-honest adversary is a malicious one that follows the protocol. Malicious security implies semi-honest security for the usual protocols, though not in general because the malicious simulator may change inputs (see the [semi-honest model](/semi-honest-model/)).
- **The GMW compiler.** It turns a protocol secure against semi-honest parties into one secure against malicious parties, in three parts. (1) *Input commitment:* each party commits to its input and proves in [zero knowledge](/zero-knowledge-proof/) that it knows the committed value. (2) *Coin tossing into the well:* for party $i$'s random tape, $i$ commits to $r_i$, the others send random $r_i'$ in the clear, and the tape is $r_i \oplus r_i'$; party $i$ knows it, it is uniform, and the others hold a commitment to it. (3) *Authenticated computation:* each message is sent with a zero-knowledge proof that it is the message $\pi$ prescribes for the committed input, the committed tape and the messages received so far. A cheater can then only change its input or stop, which is the augmented semi-honest behaviour. The compiler is general but costly; practical protocols use [cut-and-choose](/cut-and-choose/), MACs or checks of correlations instead of generic proofs.
- **Covert model.** The adversary may cheat, but it is caught with a stated probability $\varepsilon$, for example $1/2$. It sits between the two models and costs much less than full malicious security.
- **Byzantine faults.** Malicious parties in MPC are the [Byzantine](/byzantine-failure-model/) faults of distributed computing, with the added demand of privacy. Results on agreement carry over, as the $n/3$ bound below shows.
- **Universal composability.** The [UC framework](/universal-composability/) uses this adversary and adds an environment, so that security holds in any context.

## Known results in the model

- **Honest majority, computational.** Every functionality has a protocol with full security against $t < n/2$ malicious parties, given a broadcast channel and trapdoor permutations (GMW 1987).
- **Dishonest majority.** Every functionality has a protocol secure with abort against $t < n$ malicious parties (GMW 1987 with the compiler; Goldreich, Chapter 7). Fairness is not possible in general: Cleve (1986) proved that an $r$-round two-party coin flip can be biased by $\Omega(1/r)$, so a fair coin flip, and with it full security for all functions, needs an honest majority. Some special functions do have fair protocols, so the bound is about general functions.
- **Information-theoretic.** Perfect security for $t < n/3$ ([BGW](/bgw-protocol/)), which is optimal for perfect security; statistical security for $t < n/2$ with broadcast (Rabin and Ben-Or 1989).
- **Practical two-party protocols.** Garbled circuits with [cut-and-choose](/cut-and-choose/) (Lindell and Pinkas 2007, Lindell 2013); actively secure [OT extension](/oblivious-transfer-extension/) (KOS 2015) with a consistency check that stops the receiver from using different choice bits in different columns.
- **Practical multiparty protocols.** SPDZ (2012) and its successors: preprocessing of authenticated Beaver triples, an online phase secure with abort against $n - 1$ malicious parties, and the MAC check above.

## References
