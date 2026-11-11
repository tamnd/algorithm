---
tag: R8F0AW
kind: model
slug: universal-composability
name: Universal composability
aliases:
- UC framework
- UC security
area: cryptography/protocols
level: research
summary: A protocol UC-realizes an ideal functionality if no environment, talking to it during the whole run, can tell it from the functionality with a simulator. Security then survives any composition.
history:
  year: 2001
  people: [Ran Canetti]
  note: Canetti presented the framework at FOCS 2001. The full version, Cryptology ePrint Archive 2000/067, has been revised many times since.
prereqs: [secure-multiparty-computation, malicious-adversary-model]
see_also: [semi-honest-model, commitment-scheme, zero-knowledge-proof, oblivious-transfer, random-oracle-model, indifferentiability-framework]
sources:
  - paper: doi:10.1109/SFCS.2001.959888
    title: "Ran Canetti, Universally composable security: a new paradigm for cryptographic protocols, FOCS 2001, pages 136 to 145"
    locator: the model of execution with an environment, the definition of UC-realizing, the dummy adversary, and the composition theorem
  - paper: doi:10.1007/3-540-44647-8_2
    title: "Ran Canetti and Marc Fischlin, Universally composable commitments, CRYPTO 2001, LNCS 2139, pages 19 to 40"
    locator: the impossibility of UC commitments in the plain model and the constructions in the common reference string model
  - paper: doi:10.1145/509907.509980
    title: "Ran Canetti, Yehuda Lindell, Rafail Ostrovsky and Amit Sahai, Universally composable two-party and multi-party secure computation, STOC 2002, pages 494 to 503"
    locator: the main theorem (every functionality can be UC-realized in the common reference string model, for any number of corrupted parties)
  - paper: "Ran Canetti, Eyal Kushilevitz and Yehuda Lindell, On the limitations of universally composable two-party computation without set-up assumptions, EUROCRYPT 2003, LNCS 2656"
    locator: the impossibility of UC-realizing a large class of two-party functionalities without setup
  - paper: "Ran Canetti and Tal Rabin, Universal composition with joint state, CRYPTO 2003, LNCS 2729"
    locator: the JUC theorem (many sessions sharing one instance of a subroutine)
  - paper: "Eyal Kushilevitz, Yehuda Lindell and Tal Rabin, Information-theoretically secure protocols and security under composition, STOC 2006"
    locator: the result that perfect security with a straight-line black-box simulator implies UC security
  - url: "https://eprint.iacr.org/2000/067"
    title: "Ran Canetti, Universally composable security: a new paradigm for cryptographic protocols, Cryptology ePrint Archive 2000/067 (revised versions)"
    locator: the full definitions and proofs; the version numbers differ in details
---

Universal composability (UC) is a model for the security of cryptographic protocols in which security is kept when the protocol runs together with any other protocols, including copies of itself. A protocol $\pi$ *UC-realizes* an ideal functionality $\mathcal{F}$ if, for every adversary, a simulator exists such that no *environment* $\mathcal{Z}$ can tell a run of $\pi$ from a run of $\mathcal{F}$ with the simulator, where $\mathcal{Z}$ chooses the inputs, reads the outputs, and talks to the adversary during the whole run. Canetti introduced it at FOCS 2001 and proved the *composition theorem*: a UC-secure protocol can replace its ideal functionality inside any larger protocol. The cost is that many tasks, commitments first among them, are impossible in this model without a setup such as a common reference string.

**Notation.** $\lambda$ is the security parameter. $\mathcal{F}$ and $\mathcal{G}$ are ideal functionalities, $\pi$ and $\rho$ protocols, $\mathcal{A}$ a real adversary, $\mathcal{S}$ a simulator (the ideal adversary), $\mathcal{Z}$ an environment, $\mathcal{D}$ the dummy adversary, and $\mathrm{EXEC}_{\pi, \mathcal{A}, \mathcal{Z}}(\lambda, z)$ the output bit of $\mathcal{Z}$ after a run, with auxiliary input $z$. All machines run in polynomial time in $\lambda$. Session identifiers $sid$ tell instances apart.

## The machine

**Interactive Turing machines.** Every party, the adversary, the functionality and the environment are interactive Turing machines that activate one another by writing to tapes. Only one machine is active at a time. The framework fixes who may write to whom: $\mathcal{Z}$ writes inputs of the parties and reads their outputs, and $\mathcal{Z}$ and $\mathcal{A}$ exchange messages freely at any time.

**The real execution.** The parties run $\pi$. $\mathcal{A}$ controls the network (it sees, delays and drops messages, depending on the channel model) and the corrupted parties, which are chosen statically or adaptively as in the [malicious adversary model](/malicious-adversary-model/). $\mathcal{Z}$ starts the run, gives inputs, sees outputs, talks to $\mathcal{A}$, and in the end outputs one bit.

**The ideal execution.** The parties are *dummy parties*: each forwards its input to $\mathcal{F}$ and outputs what $\mathcal{F}$ returns. $\mathcal{F}$ is a program that states the task, including what it leaks to the adversary (for example the length of a message) and what the adversary may influence (for example the time of delivery). The simulator $\mathcal{S}$ talks to $\mathcal{F}$ in the name of the corrupted parties and to $\mathcal{Z}$ in the name of $\mathcal{A}$.

**The definition.** $\pi$ UC-realizes $\mathcal{F}$ if

$$\forall \mathcal{A}\ \exists \mathcal{S}\ \forall \mathcal{Z}: \quad \mathrm{EXEC}_{\pi, \mathcal{A}, \mathcal{Z}} \approx \mathrm{EXEC}_{\mathcal{F}, \mathcal{S}, \mathcal{Z}}.$$

Two features set it apart from the stand-alone definition of [secure multiparty computation](/secure-multiparty-computation/). First, $\mathcal{Z}$ is interactive: it may change the inputs of later sessions after it sees messages of earlier ones. Second, $\mathcal{S}$ cannot rewind $\mathcal{Z}$, since $\mathcal{Z}$ is an outside party that has already acted. Most stand-alone simulators rewind, so they do not give UC security.

**The dummy adversary.** It is enough to prove the definition for the dummy adversary $\mathcal{D}$, which forwards every message it sees to $\mathcal{Z}$ and sends every message $\mathcal{Z}$ tells it to send. Any other $\mathcal{A}$ can be absorbed into $\mathcal{Z}$. So the definition becomes: there is one $\mathcal{S}$ such that no $\mathcal{Z}$ can tell $(\pi, \mathcal{D})$ from $(\mathcal{F}, \mathcal{S})$.

**The composition theorem.** Let $\pi$ be a protocol that calls instances of $\mathcal{F}$ as subroutines (the $\mathcal{F}$-hybrid model), and let $\rho$ UC-realize $\mathcal{F}$. Let $\pi^{\rho/\mathcal{F}}$ be $\pi$ with each instance of $\mathcal{F}$ replaced by a separate instance of $\rho$. Then $\pi^{\rho/\mathcal{F}}$ UC-emulates $\pi$. In particular, if $\pi$ UC-realizes $\mathcal{G}$ in the $\mathcal{F}$-hybrid model, then $\pi^{\rho/\mathcal{F}}$ UC-realizes $\mathcal{G}$. *Proof idea (a sketch; Canetti gives the proof).* Suppose $\mathcal{Z}$ tells $\pi^{\rho/\mathcal{F}}$ from $\pi$. Order the instances of $\rho$ and replace them by $\mathcal{F}$ with the simulator one at a time (a hybrid argument). Two neighbouring hybrids differ in one instance, so some $\mathcal{Z}'$ that runs $\pi$ and all the other instances inside itself tells that one instance of $\rho$ from $\mathcal{F}$, which contradicts the security of $\rho$. The argument needs that $\mathcal{Z}'$ is a legal environment; this is why the environment in the definition must be able to do everything that the rest of the system can do.

**A toy model in code.** The page's Python file builds the experiment for secure message transmission of one byte. $\mathcal{F}_{\mathrm{SMT}}$ leaks only the length of $m$ to the adversary and delivers $m$. The protocol takes a uniform key $k$ from a key functionality and sends $c = m \oplus k$ on a channel that the dummy adversary reads and forwards to $\mathcal{Z}$. The simulator answers each length leak with a uniform byte. The code computes $\Pr[\mathcal{Z} \to 1]$ exactly in both worlds, over every key and every simulator coin.

- With a fresh key for each session, the advantage of every environment tried is exactly 0, for one and for two sessions.
- With one key shared by all sessions, each session alone still has advantage 0, but the environment that sends $m_1 = \texttt{0x41}$ and $m_2 = \texttt{0x42}$ and tests $c_1 \oplus c_2 = m_1 \oplus m_2$ outputs 1 with probability 1 in the real world and $1/256$ in the ideal world: advantage $255/256$.

The second case is not a failure of the composition theorem. The theorem replaces each instance of $\mathcal{F}$ by its *own* instance of $\rho$, and sharing the key between sessions breaks that hypothesis. Shared state needs the joint-state theorem of Canetti and Rabin (2003), and its own proof.

What the code can and cannot show: it runs a finite list of environments against one fixed simulator. A positive result for UC security is a statement about *all* polynomial time environments and needs a proof; the code can only find attacks and check the bookkeeping of a proof. The code is for study only and is not constant time. There are no official test vectors for UC proofs.

## What it counts

The model counts what any security model counts: the running time of $\mathcal{A}$, $\mathcal{S}$ and $\mathcal{Z}$ (polynomial in $\lambda$), and the distinguishing advantage of $\mathcal{Z}$. A concrete statement bounds the advantage of every $\mathcal{Z}$ that runs in time $t$ and starts at most $q$ sessions. Protocols are compared on the usual costs (rounds, communication, public-key operations) and, in addition, on the *setup* they need: none, a common reference string, a random oracle, or a public-key infrastructure.

## Relation to other models

- **Stand-alone security.** The ideal/real definition of Goldreich and others is the special case where $\mathcal{Z}$ gives the inputs at the start and reads the outputs at the end, with no interaction in between. It composes *sequentially*: one protocol after another. It does not, in general, survive concurrent runs. UC security implies stand-alone security.
- **Semi-honest and malicious adversaries.** UC is defined for either kind of corruption. Most results in the model are for [malicious](/malicious-adversary-model/) adversaries, static or adaptive.
- **Zero knowledge.** A UC zero-knowledge functionality forces the simulator to extract the witness without rewinding, so UC zero knowledge is a proof of knowledge with a straight-line extractor, which needs a setup.
- **Random oracles.** A [random oracle](/random-oracle-model/) can serve as the setup: the simulator sees and programs the queries. Several efficient UC protocols, such as the "simplest" [oblivious transfer](/oblivious-transfer/) of Chou and Orlandi, are stated in this setting.
- **Indifferentiability.** The [indifferentiability framework](/indifferentiability-framework/) applies the same idea (a simulator and a distinguisher that sees everything) to the construction of a random oracle from an ideal primitive.
- **Joint state.** Canetti and Rabin (2003) proved a version of the theorem for sessions that share one instance of a subroutine, such as one signing key for many sessions.

## Known results in the model

- **Commitments are impossible in the plain model.** Canetti and Fischlin (2001) proved that there is no two-party protocol that UC-realizes the commitment functionality without setup. The reason: for a corrupted committer the simulator must *extract* the committed value from the protocol messages at commit time, without rewinding, and for a corrupted receiver it must be able to open a commitment to any value (*equivocate*). If the simulator can do this using only the messages, so can a real party in the same position, which breaks hiding or binding. The same paper builds UC commitments in the common reference string (CRS) model.
- **A wide impossibility.** Canetti, Kushilevitz and Lindell (2003) extended this to most two-party functionalities, including [oblivious transfer](/oblivious-transfer/) and [zero knowledge](/zero-knowledge-proof/), whenever there is no honest majority and no setup.
- **Feasibility with a CRS.** Canetti, Lindell, Ostrovsky and Sahai (2002) UC-realized every functionality in the CRS model, for any number of corrupted parties, static or adaptive, under standard assumptions.
- **Honest majority.** The impossibility proofs need a corrupted party that can act as the simulator does. With an honest majority and private channels, perfectly secure protocols with straight-line simulators, as in the style of [BGW](/bgw-protocol/), are UC secure without setup (Kushilevitz, Lindell and Rabin 2006).
- **Practice.** Many deployed MPC components are proved in the model, often with a random oracle or a CRS as setup: oblivious transfer, [OT extension](/oblivious-transfer-extension/), commitment functionalities, and SPDZ style protocols, which are stated in hybrid models with an ideal preprocessing functionality.

## References
