---
tag: ZHSBS2
kind: model
slug: semi-honest-model
name: Semi-honest adversary model
aliases:
- honest-but-curious model
- passive adversary model
area: cryptography/protocols
level: advanced
summary: The adversary runs the protocol exactly as written and then studies its view. Security means a simulator can produce that view from the party's own input and output.
history:
  year: 1987
  people: [Oded Goldreich, Silvio Micali, Avi Wigderson]
  note: GMW 1987 first built protocols for semi-honest parties and then compiled them for malicious ones. Goldreich's 2004 book gives the standard definitions.
prereqs: [secure-multiparty-computation]
see_also: [malicious-adversary-model, universal-composability, gmw-protocol, yao-garbled-circuits, bgw-protocol, oblivious-transfer]
sources:
  - book: isbn:9780521830843
    title: Oded Goldreich, Foundations of Cryptography, Volume 2, Basic Applications, Cambridge University Press, 2004
    locator: Chapter 7, the definitions of security in the semi-honest model (the view, privacy for deterministic and for randomized functionalities, and the composition theorem for semi-honest protocols)
  - paper: doi:10.1145/28395.28420
    title: "Oded Goldreich, Silvio Micali and Avi Wigderson, How to play any mental game, or a completeness theorem for protocols with honest majority, STOC 1987, pages 218 to 229"
    locator: the protocol for semi-honest parties and the compilation to malicious parties
  - url: "https://eprint.iacr.org/2016/046"
    title: "Yehuda Lindell, How to simulate it, a tutorial on the simulation proof technique, Cryptology ePrint Archive 2016/046, also in Tutorials on the Foundations of Cryptography, Springer, 2017"
    locator: the sections on the semi-honest model and the worked simulation proofs (oblivious transfer and the GMW multiplication step)
  - book: isbn:9783642143021
    title: Carmit Hazay and Yehuda Lindell, Efficient Secure Two-Party Protocols, Techniques and Constructions, Springer, 2010
    locator: Chapter 2, the definitions of security in the semi-honest and the malicious models
  - paper: doi:10.1561/3300000019
    title: "David Evans, Vladimir Kolesnikov and Mike Rosulek, A pragmatic introduction to secure multi-party computation, Foundations and Trends in Privacy and Security 2(2-3), 2018"
    locator: Chapter 2 (semi-honest security) and Chapter 3 (semi-honest protocols)
---

The semi-honest model is the weakest standard adversary model for [secure multiparty computation](/secure-multiparty-computation/). A corrupted party follows the protocol exactly, with honestly chosen random coins, but it keeps a record of everything it sees and later tries to learn more from it. A protocol is secure in this model if the *view* of any allowed coalition can be produced by a simulator that knows only the coalition's inputs and outputs. It is also called the honest-but-curious or passive model. The [malicious adversary model](/malicious-adversary-model/) is the strong counterpart, in which corrupted parties may deviate from the protocol.

**Notation.** $\lambda$ is the security parameter, $n$ the number of parties, $f = (f_1, \ldots, f_n)$ the functionality, $\pi$ the protocol, $I \subseteq [n]$ the corrupted coalition with $|I| \le t$, $x_I$ its inputs and $f_I(x)$ its outputs. $\mathcal{S}$ is the simulator, $\approx_c$ computational indistinguishability and $\equiv$ identical distributions.

## The machine

**The parties.** Each party is an interactive probabilistic polynomial time machine with an input $x_i$, a random tape $r_i$ and the code of $\pi$. They send messages in rounds over private point-to-point channels (and a broadcast channel if $\pi$ uses one).

**The adversary.** Before the run, the adversary picks the coalition $I$ (static corruption). A corrupted party runs $\pi$ exactly: it uses its true input, its random tape is uniform, it sends exactly the messages $\pi$ says, and it does not stop early. The adversary gets the joint view of $I$ and may compute anything from it afterwards, in polynomial time (computational security) or with unbounded time (information-theoretic security). Coalition members pool their views.

**The view.** For party $i$,

$$\mathrm{view}_i^{\pi}(x) = (x_i, r_i, m_i^1, \ldots, m_i^k),$$

where $m_i^1, \ldots, m_i^k$ are the messages it received. The output of each party is a function of its view. $\mathrm{view}_I^\pi(x)$ is the tuple of the views of the parties in $I$.

**Security.** For a deterministic $f$, $\pi$ privately computes $f$ against coalitions of size at most $t$ if $\pi$ is correct (each party outputs $f_i(x)$) and there is a polynomial time $\mathcal{S}$ with

$$\{\mathcal{S}(I, x_I, f_I(x))\}_{x, \lambda} \approx_c \{\mathrm{view}_I^\pi(x)\}_{x, \lambda} \quad \text{for all } I, |I| \le t.$$

For a randomized $f$ the simulator's output must be indistinguishable *jointly with the outputs of all parties*:

$$\{(\mathcal{S}(I, x_I, f_I(x)), f(x))\} \approx_c \{(\mathrm{view}_I^\pi(x), \mathrm{output}^\pi(x))\}.$$

The joint form is necessary. Take the functionality "party 1 gets a random bit, party 2 gets nothing", and the protocol "party 1 picks a bit, outputs it, and sends it to party 2". The view of party 2 alone is a uniform bit, so the first condition holds with a simulator that outputs a random bit. But in the real world the view of party 2 always equals the output of party 1, and in the ideal world it equals it with probability $1/2$. The joint condition catches this leak. Goldreich (Chapter 7) gives both definitions and shows that the simple form is enough for deterministic $f$.

**A worked simulation.** In the two-round additive sharing sum (see [secure multiparty computation](/secure-multiparty-computation/)), the view of party $j$ is its input, its own $n - 1$ random shares, the $n$ shares it received, and the $n$ broadcast partial sums. A simulator for a coalition $I$ with at least one honest party outside it, given $x_I$ and the sum $y$, does this:

1. Pick the coalition's own coins as in the protocol.
2. Pick each share from an honest party to a coalition member uniformly at random.
3. Compute the coalition's partial sums from steps 1 and 2. Pick the partial sums of all honest parties but one uniformly, and set the last so that all partial sums add up to $y$.

Each share that an honest party sends to the coalition is uniform and independent of the rest of the coalition's view, because the honest party keeps at least one share. The honest partial sums are uniform subject to the total $y$. So the simulated view has exactly the real distribution. The page's code checks this by enumeration over $\mathbb{Z}_3$ with three parties: for one corrupted party both distributions put probability $1/243$ on each of 243 views, and for a coalition of two they put $1/729$ on each of 729 views, and the tables are equal for every input tried.

**A non-example.** In the ring protocol, party 1 sends $x_1$ to party 2, party 2 sends $x_1 + x_2$ to party 3, and party 3 announces the sum. It is correct, but with inputs $(1, 0, 2)$ and $(2, 0, 1)$ party 2 has the same input 0 and the same output 3, while its view holds 1 in the first run and 2 in the second. A simulator gets the same arguments in both runs, so it cannot match both views. The protocol leaks $x_1$ to a single semi-honest party.

The code is for study only, is not constant time, and runs all parties as local objects. Use a maintained MPC framework for real data. There are no official test vectors for these simulations; the tests compare exact distributions.

## What it counts

The model fixes what "secure" means. The cost of a protocol in it is counted in:

- **rounds** of interaction, which dominate on a network with high latency;
- **communication**, in bits or field elements;
- **cryptographic operations**: [oblivious transfers](/oblivious-transfer/) (base OTs are public-key operations, extended OTs are hash calls), hash or block cipher calls for garbling, and field multiplications;
- **the threshold** $t$: the largest coalition for which the view stays simulatable.

Semi-honest protocols are the cheapest secure protocols, so their costs are the baseline that malicious protocols are measured against.

## Relation to other models

- **Malicious model.** A semi-honest adversary is a malicious adversary that happens to follow the protocol, so one expects malicious security to imply semi-honest security. In general it does not: the simulator of the malicious model may replace the corrupted party's input, and the semi-honest ideal world does not allow that (Hazay and Lindell discuss this in Chapter 2). For the usual protocols both hold. The converse fails plainly: a party in the additive sum that adds an error to one share changes the output and is not detected. The [malicious adversary model](/malicious-adversary-model/) page shows this attack and a MAC check that catches it. The GMW compiler turns a semi-honest protocol into a malicious one.
- **Augmented semi-honest model.** Goldreich also defines a semi-honest adversary that may replace its input before the start and may abort. The compiler forces a malicious party to act like this kind of party, so the semi-honest protocol must be secure in the augmented sense.
- **Covert model.** Between the two: the adversary may cheat, but it is caught with a stated probability, such as 1/2.
- **Universal composability.** The semi-honest model can be stated inside the [UC framework](/universal-composability/) with an environment; the plain definition here is stand-alone.
- **Semi-honest versus "privacy only".** A protocol whose messages hide the inputs can still be insecure if it is not correct. The definition above requires both.

## Known results in the model

- **Any function, any coalition, computational.** With [oblivious transfer](/oblivious-transfer/), every polynomial time functionality has a protocol secure against $t < n$ semi-honest parties: [Yao's garbled circuits](/yao-garbled-circuits/) for two parties in a constant number of rounds, and the [GMW protocol](/gmw-protocol/) for $n$ parties with rounds that grow with the depth of the circuit.
- **Any function, honest majority, perfect.** The [BGW protocol](/bgw-protocol/) is perfectly secure against $t < n/2$ semi-honest parties with private channels and no assumption. BGW show that $n/2$ is the best threshold for perfect security of general functions.
- **Composition.** If $\pi$ privately computes $g$ using an ideal oracle for $f$, and $\rho$ privately computes $f$, then $\pi$ with each oracle call replaced by $\rho$ privately computes $g$ (Goldreich, Chapter 7). This is how GMW is proved: first in the OT-hybrid model, then with a real OT.
- **Simulation proofs of standard protocols.** Semi-honest security of the RSA based [Even, Goldreich and Lempel OT](/oblivious-transfer/), of [IKNP OT extension](/oblivious-transfer-extension/), and of the [DH based PSI](/private-set-intersection/) are standard exercises in this model (Lindell's tutorial works several through).
- **Limits.** Semi-honest security says nothing about a party that sends wrong messages, so it fits settings where the parties are audited, the software is trusted, or the main threat is a later breach of stored transcripts.

## References
