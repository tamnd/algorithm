---
tag: XRKXB7
kind: model
slug: quantum-random-oracle-model
name: Quantum random oracle model
aliases:
- QROM
area: cryptography/post-quantum
level: advanced
summary: "The random oracle model with a quantum adversary that may query the hash in superposition. Lazy sampling, programming and rewinding need new tools, and bounds often lose a square root."
history:
  year: 2011
  people: [Dan Boneh, Ozgur Dagdelen, Marc Fischlin, Anja Lehmann, Christian Schaffner, Mark Zhandry]
  note: Boneh and others defined the model at Asiacrypt 2011, because a quantum attacker who has the code of a real hash can run it on a superposition of inputs.
prereqs: [random-oracle-model, quantum-oracle, grover-search]
see_also: [fujisaki-okamoto-transform, fiat-shamir-heuristic, fiat-shamir-with-aborts, grover-optimality, crystals-kyber, crystals-dilithium, picnic-signature, post-quantum-cryptography]
sources:
  - paper: "Dan Boneh, Ozgur Dagdelen, Marc Fischlin, Anja Lehmann, Christian Schaffner and Mark Zhandry, Random oracles in a quantum world, ASIACRYPT 2011, LNCS 7073, pages 41 to 69"
    locator: Section 3 (the model), the separation of the classical and the quantum random oracle model, and the history-free reductions for GPV-style signatures and hybrid encryption
  - paper: "Mark Zhandry, Secure identity-based encryption in the quantum random oracle model, CRYPTO 2012, LNCS 7417"
    locator: the result that a q-query quantum algorithm cannot tell a random oracle from a 2q-wise independent function, used to simulate the oracle efficiently
  - paper: "Mark Zhandry, How to record quantum queries, and applications to quantum indifferentiability, CRYPTO 2019, LNCS 11693"
    locator: the compressed oracle (the purified oracle in the Fourier basis with a database of queried points) and its use for collision bounds
  - paper: "Dominique Unruh, Revocable quantum timed-release encryption, Journal of the ACM 62(6), 2015"
    locator: the one-way to hiding (O2H) lemma
  - paper: "Andris Ambainis, Mike Hamburg and Dominique Unruh, Quantum security proofs using semi-classical oracles, CRYPTO 2019, LNCS 11693"
    locator: the semi-classical O2H theorems with bounds in terms of the query depth
  - paper: "Dennis Hofheinz, Kathrin Hovelmanns and Eike Kiltz, A modular analysis of the Fujisaki-Okamoto transformation, TCC 2017, LNCS 10677"
    locator: the QROM theorems for the transforms with implicit rejection, with their square-root loss
  - paper: "Haodong Jiang, Zhenfeng Zhang, Long Chen, Hong Wang and Zhi Ma, IND-CCA-secure key encapsulation mechanism in the quantum random oracle model, revisited, CRYPTO 2018, LNCS 10993"
    locator: the QROM proofs of the FO variants with implicit rejection used by Kyber and others
  - paper: "Jelle Don, Serge Fehr, Christian Majenz and Christian Schaffner, Security of the Fiat-Shamir transformation in the quantum random-oracle model, CRYPTO 2019, LNCS 11693"
    locator: the measure-and-reprogram theorem and its application to Fiat-Shamir signatures
  - paper: "Qipeng Liu and Mark Zhandry, Revisiting post-quantum Fiat-Shamir, CRYPTO 2019, LNCS 11693"
    locator: the QROM security of Fiat-Shamir for sigma protocols with collapsing or lossy properties
---

The quantum random oracle model (QROM) is the [random oracle model](/random-oracle-model/) in which the adversary may query the oracle on a quantum superposition of inputs. Boneh, Dagdelen, Fischlin, Lehmann, Schaffner and Zhandry defined it in 2011, because an attacker with a quantum computer who has the code of SHA-3 can evaluate it as a quantum circuit. Most proofs for post-quantum schemes that use hash functions, such as the Fujisaki-Okamoto proofs for ML-KEM and the Fiat-Shamir proofs for ML-DSA, are proofs in the QROM. The model is harder to work in than the classical one: the reduction cannot simply look at the queries, change answers or rewind the adversary, and the bounds often lose a square root.

## The machine

There is a function $H : X \to Y$, chosen uniformly from all functions, for example with $X = \{0,1\}^m$ and $Y = \{0,1\}^n$. Every party may evaluate it, but only through the oracle.

- **Quantum access for the adversary.** The adversary is a quantum algorithm. A query applies the unitary

$$O_H : |x\rangle|y\rangle \mapsto |x\rangle|y \oplus H(x)\rangle$$

to registers that it chooses. The input register may hold a superposition $\sum_x \alpha_x |x\rangle$, so one query touches all inputs at once, as in [Grover search](/grover-search/). See [quantum oracle](/quantum-oracle/).

- **Classical honest parties.** The scheme itself runs on classical computers and queries $H$ on classical inputs. The security game (the challenger, the signing oracle, the decryption oracle) is classical too, so only the adversary's access to $H$ is quantum.

- **The reduction.** A security proof is a quantum algorithm $B$ that runs the adversary $A$ as a subroutine and answers its oracle queries with a function that $B$ can compute, usually a function that it has set up so that a solution of a hard problem can be read from $A$'s output. $B$ must answer quantum queries, so its simulated oracle must be a function that it can evaluate in superposition, with no hidden state that the query would disturb.

## What it counts

- **Queries.** The cost of an adversary is the number $q$ of oracle queries (often $q_H$ for the random oracle and $q_S$ or $q_D$ for the signing or decryption oracle), and sometimes the query depth $d$, the number of rounds of parallel queries. Time and qubits outside the oracle count as in the quantum circuit model.
- **Advantage.** A proof bounds the adversary's advantage against the scheme by a function of its queries and of the advantage of some algorithm against a hard problem.
- **Reduction loss.** The factor between the two. The same proof can be tight in the classical model and lose a square root in the QROM. For example, the semi-classical O2H bound has the form $|\Pr[\text{left}] - \Pr[\text{right}]| \le 2\sqrt{(q+1)\Pr[\text{find}]}$. If a scheme's advantage is bounded by $2q\sqrt{\varepsilon}$ where $\varepsilon$ is the advantage against the underlying problem, then with $q = 2^{64}$ hash queries and $\varepsilon = 2^{-128}$ the bound is $2 \cdot 2^{64} \cdot 2^{-64} = 2$, which says nothing. A bound of $2^{-128}$ on the scheme would need $\varepsilon \le 2^{-386}$.

This is why reduction loss matters. Schemes such as ML-KEM and ML-DSA are not sized so that their QROM bounds are meaningful with the stated parameters; they are sized by the best known attacks. The QROM proof says that the generic structure has no flaw that a quantum attacker could use, but a loose bound does not give a concrete security level. A tight proof would.

## Relation to other models

- **[Random oracle model](/random-oracle-model/) (ROM).** The QROM gives the adversary more power, so a proof in the QROM implies a proof in the ROM with the same bound, but not the other way round. Boneh and others (2011) built an artificial identification scheme that is secure in the ROM and insecure in the QROM, because a quantum adversary finds collisions of the oracle faster than the protocol allows. For most natural schemes no such gap is known, and the question is whether the proof technique transfers.
- **Three classical tools that fail.**
  1. **Lazy sampling and recording queries.** In the ROM the reduction answers each new query with a fresh random value and keeps a table. In the QROM a query is a superposition over exponentially many inputs, and measuring it to learn the input would change the adversary's state. The reduction cannot see which inputs the adversary asked.
  2. **Programming.** In the ROM the reduction can set $H(x^*)$ to a chosen value at the point $x^*$ where it embeds a challenge, or where it answers a signing query. In the QROM, any input may have small amplitude in many queries, so changing $H$ at one point can change the adversary's behaviour in a way that the reduction does not see. Programming needs a bound on the total weight of the queries on the changed points.
  3. **Rewinding.** Proofs of Fiat-Shamir signatures use the forking lemma: run the adversary, rewind it to a query, change the answer, and get two transcripts. A quantum adversary's intermediate state cannot be copied, and measuring it to rewind disturbs it.
- **Standard model.** A proof with no random oracle at all holds in the QROM too, if the hard problem is hard for quantum algorithms.

## Known results in the model

**Simulating the oracle.** Zhandry (2012) showed that a $q$-query quantum algorithm cannot tell a random function from a $2q$-wise independent function, for example a random polynomial of degree $2q - 1$. So a reduction can simulate $H$ efficiently, with no assumption, by a function that it can evaluate in superposition. Before this, Boneh and others (2011) had simulated $H$ with a quantum-secure pseudorandom function, and proved the full domain hash signatures of Gentry, Peikert and Vaikuntanathan secure in the QROM with "history-free" reductions, which answer each query by a fixed function and do not depend on earlier queries.

**Generic bounds.** A $q$-query quantum algorithm finds a preimage of a random oracle with probability $O(q^2/2^n)$, matched by Grover search (see [optimality of Grover search](/grover-optimality/)), and a collision with probability $O(q^3/2^n)$ (Zhandry 2015), matched by the Brassard, Hoyer and Tapp algorithm. The table is on the [random oracle model](/random-oracle-model/) page.

**The compressed oracle.** Zhandry (2019) gave a quantum form of lazy sampling. Purify the oracle: let the oracle's state be a uniform superposition over all functions, entangled with the adversary. In the Fourier basis this state is all zeros at the start, and each query changes it at only the inputs in superposition. Written in a "compressed" form, the oracle's state is a superposition of small databases of at most $q$ pairs $(x, y)$, and the reduction can inspect the database at the end. This gives the collision bound above by a direct count, the quantum indifferentiability of the Merkle-Damgard construction, and the base for many later proofs.

**One-way to hiding (O2H).** Unruh (2015) proved a lemma for the step "the adversary can only tell $H$ from $G$ if it queries a point where they differ". If $H$ and $G$ differ only on a set $S$, then

$$|\Pr[A^H \Rightarrow 1] - \Pr[A^G \Rightarrow 1]| \le 2q\sqrt{\Pr[B \text{ finds a point of } S]},$$

where $B$ runs $A$, picks one of its queries at random and measures it. Ambainis, Hamburg and Unruh (2019) gave semi-classical oracles, which only measure whether a query is in $S$, and improved the bound to $2\sqrt{(q+1)\Pr[\text{find}]}$, and to bounds in the query depth $d$ instead of $q$. The square root is the main source of loss in QROM proofs.

**The Fujisaki-Okamoto transform.** The [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) turns a passively secure encryption scheme into an IND-CCA2 KEM. Its classical proof watches the decryption queries, which fails in the QROM. Hofheinz, Hovelmanns and Kiltz (2017) split it into modules and proved QROM versions that add an extra hash of the message to the ciphertext, an idea of Targhi and Unruh, with a loss of about $q\sqrt{\varepsilon}$. Jiang, Zhang, Chen, Wang and Ma (2018) proved the variants with implicit rejection secure in the QROM without the extra hash, with a tighter bound. Kyber, and so ML-KEM, uses implicit rejection with no extra hash, which these proofs cover (see [CRYSTALS-Kyber](/crystals-kyber/)). Later work with semi-classical O2H and the compressed oracle tightened the bounds further, but none of the general proofs is tight.

**Fiat-Shamir.** Signatures built from identification protocols by the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/) were long without a QROM proof, because of rewinding. Don, Fehr, Majenz and Schaffner (2019) proved a measure-and-reprogram theorem: a reduction can measure one query at random, reprogram the oracle at that point, and lose only a factor $O(q^2)$. This gives QROM security for Fiat-Shamir signatures from sigma protocols with special soundness. Liu and Zhandry (2019), in the same proceedings, proved Fiat-Shamir secure in the QROM for protocols with a "collapsing" property, with the compressed oracle. Kiltz, Lyubashevsky and Schaffner (Eurocrypt 2018) had proved a QROM bound for signatures from lossy identification schemes, which covers Dilithium, and so ML-DSA (see [CRYSTALS-Dilithium](/crystals-dilithium/) and [Fiat-Shamir with aborts](/fiat-shamir-with-aborts/)). Unruh (Eurocrypt 2015) gave a different transform with a straight-line QROM proof, which one variant of [Picnic](/picnic-signature/) used.
## References
