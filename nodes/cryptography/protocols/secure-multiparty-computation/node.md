---
tag: RFTBQB
kind: problem
slug: secure-multiparty-computation
name: Secure multiparty computation
aliases:
- MPC
- secure function evaluation
area: cryptography/protocols
level: advanced
summary: n parties compute f(x1, ..., xn) on private inputs and learn only the output. Security means a real run can be simulated from an ideal run with a trusted party.
history:
  year: 1987
  people: [Andrew Chi-Chih Yao, Oded Goldreich, Silvio Micali, Avi Wigderson]
  note: Yao posed two-party secure computation in 1982. Goldreich, Micali and Wigderson gave the first protocol for any function and any number of parties at STOC 1987.
prereqs: [one-way-function, boolean-circuit]
see_also: [semi-honest-model, malicious-adversary-model, universal-composability, yao-garbled-circuits, gmw-protocol, bgw-protocol, oblivious-transfer, secret-sharing]
sources:
  - paper: doi:10.1145/28395.28420
    title: "Oded Goldreich, Silvio Micali and Avi Wigderson, How to play any mental game, or a completeness theorem for protocols with honest majority, STOC 1987, pages 218 to 229"
    locator: the main theorems (any function for semi-honest parties, and for malicious parties with an honest majority)
  - book: isbn:9780521830843
    title: Oded Goldreich, Foundations of Cryptography, Volume 2, Basic Applications, Cambridge University Press, 2004
    locator: Chapter 7, General Cryptographic Protocols (the ideal/real definitions, the semi-honest and malicious models, the compiler, and the multiparty case)
  - paper: doi:10.1145/62212.62213
    title: "Michael Ben-Or, Shafi Goldwasser and Avi Wigderson, Completeness theorems for non-cryptographic fault-tolerant distributed computation, STOC 1988, pages 1 to 10"
    locator: the main theorems (perfect security for t < n/2 semi-honest and t < n/3 malicious, and their optimality)
  - paper: doi:10.1145/62212.62214
    title: "David Chaum, Claude Crepeau and Ivan Damgard, Multiparty unconditionally secure protocols, STOC 1988, pages 11 to 19"
    locator: the main theorem (unconditional security with t < n/3)
  - paper: doi:10.1145/73007.73014
    title: "Tal Rabin and Michael Ben-Or, Verifiable secret sharing and multiparty protocols with honest majority, STOC 1989, pages 73 to 85"
    locator: the main theorem (statistical security for t < n/2 with a broadcast channel)
  - paper: doi:10.1145/12130.12168
    title: "Richard Cleve, Limits on the security of coin flips when half the processors are faulty, STOC 1986, pages 364 to 369"
    locator: the main theorem (an r-round coin flip can be biased by about 1/r when half the parties are faulty)
  - paper: doi:10.1007/978-3-642-32009-5_38
    title: "Ivan Damgard, Valerio Pastro, Nigel Smart and Sarah Zakarias, Multiparty computation from somewhat homomorphic encryption, CRYPTO 2012, LNCS 7417, pages 643 to 662"
    locator: the preprocessing model, the MACs on shares and the online phase (SPDZ)
  - paper: doi:10.1561/3300000019
    title: "David Evans, Vladimir Kolesnikov and Mike Rosulek, A pragmatic introduction to secure multi-party computation, Foundations and Trends in Privacy and Security 2(2-3), 2018"
    locator: Chapters 2 and 3 (definitions, and the fundamental protocols Yao, GMW, BGW)
---

Secure multiparty computation (MPC) is the problem where $n$ parties, each with a private input $x_i$, compute a function $f(x_1, \ldots, x_n)$ so that each party learns its output and nothing more. "Nothing more" is made exact by the ideal/real simulation paradigm of [Goldreich, Micali and Wigderson](/gmw-protocol/): whatever an adversary can do in a run of the protocol, it could also do in an *ideal world* where a trusted party gets all inputs and hands out the outputs. The problem has general solutions for every polynomial time $f$, and the open questions are about cost, the number of corrupted parties, and which guarantees (fairness, guaranteed output) are possible. This page states the problem and the map of results; [Yao's garbled circuits](/yao-garbled-circuits/), the [GMW protocol](/gmw-protocol/) and the [BGW protocol](/bgw-protocol/) are the classic solutions.

**Notation.** $\lambda$ is the security parameter, $n$ the number of parties $P_1, \ldots, P_n$, $t$ the largest number of corrupted parties, $I \subseteq [n]$ with $|I| \le t$ the corrupted set, $\mathcal{A}$ the real adversary and $\mathcal{S}$ the ideal adversary (the simulator). $f$ is given as a [Boolean circuit](/boolean-circuit/) or an arithmetic circuit $C$ with $|C|$ gates. $\approx_c$ means computationally indistinguishable, $\approx_s$ statistically close, and $\equiv$ identical.

## In plain words

Three friends want to know their average salary, but none of them wants to say their own salary. If they trusted a fourth person, each would whisper the number to that person, who would announce the average and forget the rest. Secure multiparty computation removes the trusted person. The friends exchange messages that look random, and at the end each knows the average and nothing else.

"Nothing else" has a careful meaning. The average itself tells you something: two friends who know their own salaries and the total can work out the third. That is allowed, because the trusted person would have told them the same total. A protocol is secure when everything a cheater sees in it could have been made up from what the trusted person would have told the cheater.

## Definition

**Functionality.** A (possibly randomized) function $f : (\{0,1\}^*)^n \to (\{0,1\}^*)^n$, with $f(x_1, \ldots, x_n) = (y_1, \ldots, y_n)$. Party $P_i$ has input $x_i$ and must get $y_i$.

**The ideal world.** Each honest party sends $x_i$ to a trusted party. The adversary $\mathcal{S}$ controls the parties in $I$; it may replace their inputs by any values $x_i'$ of its choice. The trusted party computes $y = f(x')$, gives $\mathcal{S}$ the outputs $y_I$ of the corrupted parties, and gives each honest party its $y_i$. In the version *with abort*, $\mathcal{S}$ first sees $y_I$ and then tells the trusted party to deliver or to send $\bot$ to the honest parties. $\mathrm{IDEAL}_{f, I, \mathcal{S}(z)}(x, \lambda)$ is the joint distribution of the outputs of the honest parties and of $\mathcal{S}$, where $z$ is an auxiliary input.

**The real world.** The parties run a protocol $\pi$ over the stated channels (point to point, private or authenticated, with or without broadcast). The adversary $\mathcal{A}$ controls the parties in $I$. $\mathrm{REAL}_{\pi, I, \mathcal{A}(z)}(x, \lambda)$ is the joint distribution of the outputs of the honest parties and of $\mathcal{A}$.

**Security.** $\pi$ $t$-securely computes $f$ if for every real adversary $\mathcal{A}$ in the class there is an ideal adversary $\mathcal{S}$ in the same class such that for every $I$ with $|I| \le t$,

$$\{\mathrm{IDEAL}_{f, I, \mathcal{S}(z)}(x, \lambda)\}_{x, z, \lambda} \approx_c \{\mathrm{REAL}_{\pi, I, \mathcal{A}(z)}(x, \lambda)\}_{x, z, \lambda}.$$

The class of $\mathcal{A}$ is the adversary model: [semi-honest](/semi-honest-model/) (follows the protocol) or [malicious](/malicious-adversary-model/) (deviates at will), static or adaptive, polynomial time or unbounded. Replacing $\approx_c$ by $\approx_s$ or $\equiv$ gives statistical or perfect security. The outputs of the honest parties are part of the distribution, so one definition gives both *privacy* and *correctness*: a protocol that leaks nothing but gives the honest parties a wrong answer fails it. Goldreich (Chapter 7) gives the full definitions.

**What the definition does not promise.** The ideal world still reveals $y_I$, and $y_I$ may tell a lot about the honest inputs. The definition also lets the adversary choose its own inputs freely, so it does not stop a party from lying about its input; it stops only everything beyond that.

## Variants

- **Two-party computation (2PC).** $n = 2$, so there is no honest majority once one party is corrupt. [Yao's millionaires' problem](/yao-millionaires-problem/) is the first example.
- **Adversary power.** [Semi-honest](/semi-honest-model/) versus [malicious](/malicious-adversary-model/); static (fixed $I$ before the run) versus adaptive (corrupt during the run); computationally bounded versus unbounded. A *covert* adversary is malicious but does not want to be caught, so a protocol that catches cheating with a stated probability is enough.
- **Guarantees for the honest parties.** *Full security* gives every honest party its output. *Fairness* means that if the adversary gets output, so do the honest parties. *Security with abort* lets the adversary see its output and then stop the others.
- **Composition.** Stand-alone security covers one run; [universal composability](/universal-composability/) covers any number of concurrent runs inside any larger system.
- **Special functionalities.** [Oblivious transfer](/oblivious-transfer/), [private set intersection](/private-set-intersection/), [private information retrieval](/private-information-retrieval/) (a weaker notion: only the client is protected), [fair coin flipping](/fair-coin-flipping/), [threshold cryptography](/threshold-cryptography/) (the function is a decryption or a signature under a shared key).
- **Reactive functionalities.** The trusted party keeps a state across many calls, as in an auction or a secure database.

## Examples

**Sum of salaries.** Three parties with $x = (52, 61, 47)$ compute $x_1 + x_2 + x_3 \bmod 1000$ with additive secret sharing. Party 1 splits 52 into $(331, 970, 751)$, since $331 + 970 + 751 = 2052 \equiv 52$. Party 2 splits 61 into $(154, 404, 503)$ and party 3 splits 47 into $(666, 49, 332)$. Party $j$ receives the $j$-th share of each and adds them: party 1 gets $331 + 154 + 666 \equiv 151$, party 2 gets $970 + 404 + 49 \equiv 423$, party 3 gets $751 + 503 + 332 \equiv 586$. They broadcast these partial sums, and each computes $151 + 423 + 586 \equiv 160$. Each share that a party receives from another party is a uniform number, so one party alone sees only uniform numbers and the total. The protocol uses $2n(n-1) = 12$ messages in 2 rounds.

**What the output reveals.** With two parties and $f(x_1, x_2) = x_1 + x_2$, party 1 learns $x_2 = y - x_1$. This is not a flaw of any protocol: the ideal world gives the same knowledge. For $f = x_1 \wedge x_2$ on bits, a party with input 1 learns the other bit and a party with input 0 learns nothing.

**A non-example.** "Each party sends its input to party 1, who adds them" computes the right sum but is not secure: the view of party 1 contains $x_2$ and $x_3$, and no simulator can produce $x_2$ from $x_1$ and the sum alone when $n = 3$.

**The harness in the code.** The page's Python file runs the ideal functionality and the real two-round protocol on the same inputs and checks that every output agrees. The test does this on 600 random cases with 2 to 7 parties and moduli 2, 5, 97 and $2^{64}$, and checks the message count $2n(n-1)$ for $n = 2$ to 11. There are no official test vectors for MPC protocols, so the tests compare with the ideal functionality and check properties. The code is for study only and is not constant time; the parties are local objects. For real data, use a maintained MPC framework such as MP-SPDZ, and real channels with TLS.

## Known algorithms

| protocol | adversary and threshold | security | rounds | main cost |
|---|---|---|---|---|
| [Yao's garbled circuits](/yao-garbled-circuits/) | semi-honest, 2 parties | computational | constant | $O(\lambda \lvert C \rvert)$ bits, one [OT](/oblivious-transfer/) per input bit of the evaluator |
| [GMW](/gmw-protocol/) | semi-honest, $t < n$ | computational (needs OT) | $O(d)$, $d$ the AND depth | one OT per pair of parties per AND gate |
| GMW with the compiler | malicious, $t < n/2$ full security; $t < n$ with abort | computational | $O(d)$ plus the proofs | [zero-knowledge proofs](/zero-knowledge-proof/) for each step |
| [BGW](/bgw-protocol/) | semi-honest $t < n/2$; malicious $t < n/3$ | perfect | $O(d)$ | $O(n^2)$ field elements per multiplication |
| Chaum, Crepeau and Damgard (CCD) | malicious, $t < n/3$ | unconditional, small error | $O(d)$ | per gate, with commitments built from sharing |
| Rabin and Ben-Or | malicious, $t < n/2$, with broadcast | statistical | $O(d)$ | per gate, with [verifiable secret sharing](/verifiable-secret-sharing/) |
| SPDZ | malicious, $t < n$, with abort | computational preprocessing, information-theoretic online phase | $O(d)$ online | a few field elements per multiplication online |

**SPDZ and the preprocessing model.** Damgard, Pastro, Smart and Zakarias (2012) split the work into two phases. An offline phase, run before the inputs are known, uses somewhat [homomorphic encryption](/homomorphic-encryption/) to make *Beaver triples*: additive sharings of random $a$, $b$ and $c = ab$. Every shared value also carries an additive sharing of $\alpha \cdot$ value, where $\alpha$ is a secret global MAC key that no one knows. The online phase uses only additions, one triple per multiplication, and a MAC check when values are opened. It is secure with abort against $n - 1$ malicious parties, and its online cost is close to that of the semi-honest protocol. The [malicious adversary model](/malicious-adversary-model/) page shows the MAC check on a toy sum.

## Bounds

**Feasibility.** Under standard assumptions (enhanced trapdoor permutations, or any assumption that gives [oblivious transfer](/oblivious-transfer/)):

- Semi-honest, any $t < n$: every polynomial time $f$ is computable (Yao for two parties, GMW 1987 for $n$ parties).
- Malicious, $t < n/2$: every $f$, with full security (fairness and guaranteed output), given a broadcast channel (GMW 1987).
- Malicious, any $t < n$: every $f$, with abort (GMW 1987 with the compiler; Goldreich, Chapter 7).

With private channels and no assumption:

- Perfect security for $t < n/2$ semi-honest and $t < n/3$ malicious (BGW 1988); unconditional security for $t < n/3$ (CCD 1988).
- Statistical security for $t < n/2$ malicious if a broadcast channel is given (Rabin and Ben-Or 1989).

**Impossibility.**

- *Fairness with a dishonest majority.* Cleve (1986) proved that in any $r$-round protocol for flipping a coin between two parties, one party can bias the outcome by $\Omega(1/r)$. So full security for all functions is impossible when $t \ge n/2$, and the best one can get there in general is security with abort.
- *Perfect security.* BGW show that their thresholds are optimal: $t < n/2$ for semi-honest and $t < n/3$ for malicious parties, for perfect security of general functions. The $n/3$ bound is related to the [bound for Byzantine agreement](/byzantine-resilience-bound/) without signatures.
- *Two parties without assumptions.* With $n = 2$ and $t = 1$ there is no honest majority, so by the same optimality result some functions have no information-theoretically secure 2PC protocol even against a semi-honest party. This is why 2PC needs OT or another computational tool.

## Reductions

- **OT is complete.** Kilian (1988) showed that any function can be computed securely given an ideal [oblivious transfer](/oblivious-transfer/), with no other assumption. Conversely, OT is a two-party function, so a general MPC protocol gives OT. So general 2PC and OT are equivalent.
- **Semi-honest to malicious.** The GMW compiler turns a semi-honest protocol into one secure against malicious parties, using [commitments](/commitment-scheme/), [zero-knowledge proofs](/zero-knowledge-proof/) and a coin tossing protocol. See the [malicious adversary model](/malicious-adversary-model/).
- **Circuit size.** All the general protocols cost at least linear in the size of the circuit of $f$, so a function with a small circuit is cheap and a RAM program first becomes a circuit (or uses ORAM based protocols).

## Applications

Private statistics over data held by many companies (sums, averages, regressions); [private set intersection](/private-set-intersection/) for contact discovery and ad conversion measurement; [threshold](/threshold-cryptography/) key management, where a signing key is never held in one place; sealed-bid auctions; and private machine learning inference.

## References
