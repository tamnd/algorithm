---
tag: 6J2DGY
kind: model
slug: random-oracle-model
name: Random oracle model
aliases:
- random oracle
area: cryptography/hash-functions
level: advanced
summary: A model where every party, honest or not, can only query the hash as a uniformly random function. Proofs in it count oracle queries and may watch or program them.
history:
  year: 1993
  people: [Mihir Bellare, Phillip Rogaway]
  note: Bellare and Rogaway made the random oracle paradigm explicit at ACM CCS 1993, after its informal use by Fiat and Shamir (1986) and others.
prereqs: [cryptographic-hash-function]
see_also: [indifferentiability-framework, ideal-cipher-model, rsa-fdh, rsa-oaep, fiat-shamir-heuristic, schnorr-signature, length-extension-attack, sponge-construction]
sources:
  - paper: doi:10.1145/168588.168596
    title: "Mihir Bellare and Phillip Rogaway, Random oracles are practical: a paradigm for designing efficient protocols, ACM CCS 1993, pages 62 to 73"
    locator: Sections 1 and 2 (the paradigm and the model), and the encryption and signature schemes of Sections 3 to 5
  - paper: doi:10.1145/1008731.1008734
    title: "Ran Canetti, Oded Goldreich and Shai Halevi, The random oracle methodology, revisited, Journal of the ACM 51(4), 2004, pages 557 to 594"
    locator: the main theorem, a signature and an encryption scheme that are secure with a random oracle but insecure with every efficient hash; first at STOC 1998
  - paper: doi:10.1007/s001450010003
    title: "David Pointcheval and Jacques Stern, Security arguments for digital signatures and blind signatures, Journal of Cryptology 13(3), 2000, pages 361 to 396"
    locator: the forking lemma, used for Schnorr signatures in the random oracle model
  - paper: "Mihir Bellare and Phillip Rogaway, The exact security of digital signatures: how to sign with RSA and Rabin, EUROCRYPT 1996, LNCS 1070, pages 399 to 416"
    locator: the full domain hash and PSS, with exact reductions to RSA
  - paper: "Eiichiro Fujisaki, Tatsuaki Okamoto, David Pointcheval and Jacques Stern, RSA-OAEP is secure under the RSA assumption, CRYPTO 2001, LNCS 2139, pages 260 to 274"
    locator: the proof of RSA-OAEP against chosen ciphertext attacks in the random oracle model
  - paper: doi:10.1007/s00145-005-0432-z
    title: "Neal Koblitz and Alfred J. Menezes, Another look at provable security, Journal of Cryptology 20(1), 2007, pages 3 to 37"
    locator: the discussion of random oracle proofs, tightness and their meaning in practice
  - paper: "Dan Boneh, Ozgur Dagdelen, Marc Fischlin, Anja Lehmann, Christian Schaffner and Mark Zhandry, Random oracles in a quantum world, ASIACRYPT 2011, LNCS 7073, pages 41 to 69"
    locator: the quantum random oracle model, and a separation from the classical model
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography
    locator: Section 8.10 (the random oracle model) and the chapters on signatures that use it
---

The random oracle model is an idealized model for proofs about schemes that use a hash function. In it, the hash $H$ is a function chosen uniformly at random from all functions with the given domain and range. No party has a description of $H$. Each party, honest or not, can only send an input to an oracle and get back $H(x)$. A proof in the model bounds the success of an adversary in terms of the number $q$ of oracle queries and a hard problem, such as RSA or the discrete logarithm. Bellare and Rogaway made the model explicit in 1993, and it gave the first proofs for practical schemes such as the full domain hash, OAEP and Schnorr signatures. The model is a heuristic. Canetti, Goldreich and Halevi showed in 1998 that some schemes are secure in it but insecure with every real hash.

## The machine

**The oracle.** For a domain $X$ (often all bit strings) and a range $Y = \{0,1\}^n$, the oracle holds a function $H$ drawn uniformly from all functions $X \to Y$. On query $x$ it returns $H(x)$. The same query always gets the same answer, and different queries get independent uniform answers.

**The parties.** The scheme, the adversary and the security game are oracle machines. They compute freely, and they get $H$ only through queries. The adversary may be unbounded in time when a result is information theoretic, as for the bounds below, or polynomial time when the proof is a reduction to a hard problem.

**Lazy sampling.** A function from all bit strings is an infinite object. A simulator need not choose it in advance. It keeps a table of the answers given so far. On a new query it draws a fresh uniform value, stores it and returns it. On a repeated query it returns the stored value. The view of every party is then the same as with a fully random $H$, since in both cases the answers to distinct queries are independent and uniform.

**The two powers of a reduction.** A reduction runs the adversary and plays the oracle for it with lazy sampling. This gives it two powers that a real hash does not give.

- *Extractability.* The reduction sees every query of the adversary. If the adversary outputs a valid signature or decrypts a message, it must, except with small probability, have queried $H$ at a point that the reduction can read from its log.
- *Programmability.* The reduction may fix $H(x)$ to a value of its choice before anyone queries $x$, as long as the value is uniform from the view of the adversary. It may not change an answer that it has already given.

**A worked example: signatures with no secret key.** The Schnorr signature over a group with generator $g$ of prime order $q$ and public key $y = g^x$ is a pair $(c, s)$ with $c = H(R \,\|\, m)$ and $R = g^s y^{-c}$. The signer picks $k$, sets $R = g^k$, $c = H(R \,\|\, m)$ and $s = k + cx \bmod q$. A simulator that controls $H$ can sign with no knowledge of $x$. It picks $c$ and $s$ at random, sets $R = g^s y^{-c}$, and programs $H(R \,\|\, m) = c$. If $H$ is already defined at that point, it tries again. The pair $(c, s)$ is then valid, and it has the same distribution as a real signature. This is the zero-knowledge simulator from the security proof of Schnorr signatures. It does not break the scheme, because no real party can program SHA-256.

The page's code does this in a toy group with $p = 2039$, $q = 1019$ and $g = 4$. With seed 2024 the key is $x = 482$, $y = 1666$, and a real signature on `hello` is $(745, 589)$. A simulator, using only $y$, picked $(c, s) = (812, 587)$, set $R = 579$, and programmed $H$ there. The verifier accepted it, and the oracle log shows the single query of the verifier. The test signs 50 messages with the key and 200 messages with the simulator, and all verify. It also checks the lazy oracle with a chi-square test, $\chi^2 < 37.7$ over 16000 queries into 16 bins. The code is for study only and not constant time. A real system hashes with SHA-256 or SHA-3 from the standard library, a FIPS 140 validated module or libsodium, and uses a reviewed signature library.

## What it counts

The main cost is the number $q$ of oracle queries made by the adversary, often split into $q_H$ hash queries and $q_S$ signing or decryption queries. Local computation is free in information theoretic statements and polynomial in reductions. A result has the form

$$\mathrm{Adv}(\mathcal{A}) \le \epsilon(q_H, q_S) \cdot \mathrm{Adv}^{\text{hard problem}} + \delta(q_H, q_S, n),$$

and its quality is judged by the loss. A proof is *tight* when $\epsilon$ is a small constant. Koblitz and Menezes stress that a loose proof, with a factor $q_H$ or $q_S$, says little about real key sizes unless the parameters are raised to absorb the loss.

## Relation to other models

- **The standard model.** Here the hash is a real, public function, and proofs rely only on stated properties such as [collision resistance](/collision-resistance/). Every scheme proven in the standard model is also secure in the random oracle model, but not the other way round.
- **The uninstantiability result.** Canetti, Goldreich and Halevi built a signature scheme and an encryption scheme that are secure with a random oracle and insecure for every efficient function family that replaces it. The schemes are contrived: they check whether an input is the code of the hash itself. So a random oracle proof is evidence about generic attacks, not a proof about SHA-256.
- **Real hashes.** A [Merkle-Damgard](/merkle-damgard-construction/) hash such as SHA-256 is not even close to a random oracle in one plain sense: given $H(m)$ and the length of $m$, anyone can compute $H(m \,\|\, \mathrm{pad} \,\|\, m')$, which a random oracle does not allow. This is the [length extension attack](/length-extension-attack/). The [indifferentiability framework](/indifferentiability-framework/) gives the right notion of a construction that behaves like a random oracle. Sponges such as SHA-3 and prefix-free Merkle-Damgard variants meet it, given an ideal inner permutation or compression function.
- **The ideal cipher model.** The [ideal cipher model](/ideal-cipher-model/) gives every key an independent random permutation, with oracles for both directions. It is used for block cipher based hashes such as Davies-Meyer. Coron, Patarin and Seurin (2008) showed that a 6-round Feistel network with random oracles as round functions is indifferentiable from a random permutation, and Holenstein, Kunzler and Tessaro (2011) proved it for 14 rounds after a gap in the earlier proof was found.
- **Variants of the oracle.** A non-programmable random oracle forbids the reduction to choose answers. Fischlin and others (2010) showed that some schemes, such as FDH, have no proof in that weaker model with certain reductions.
- **The quantum random oracle model (QROM).** An adversary with a quantum computer can evaluate a real hash on a superposition of inputs. So the oracle must accept quantum queries. Boneh and others (2011) defined this model and showed that some classical proofs fail in it, because the reduction can no longer simply record and program queries. Zhandry (2019) gave the compressed oracle, a quantum form of lazy sampling that restores recording in many proofs.

## Known results in the model

For a random oracle with $n$ output bits and an adversary that makes $q$ queries:

| Task | Classical bound on success | Quantum bound on success |
|---|---|---|
| find a preimage of a given value | $q / 2^n$ | $O(q^2 / 2^n)$, met by Grover search |
| find a collision | $q(q-1)/2^{n+1}$ | $O(q^3 / 2^n)$, met by Brassard, Hoyer and Tapp |
| find a second preimage | $q / 2^n$ | $O(q^2 / 2^n)$ |

The classical bounds follow from lazy sampling: each fresh answer is uniform and independent of all earlier ones. They match the generic attacks on the [preimage](/preimage-finding/) and [collision](/collision-finding/) pages. The quantum collision bound is due to Zhandry (2015).

Schemes with proofs in the model:

- **Full domain hash.** RSA-FDH signs $H(m)^d \bmod N$ with $H$ onto $\mathbb{Z}_N$. Bellare and Rogaway proved it secure under the RSA assumption. Coron (2000) brought the loss down to a factor about $q_S$, the number of signatures. PSS adds a random salt and has a tight proof. See [RSA-FDH](/rsa-fdh/).
- **OAEP.** Bellare and Rogaway (1994) proposed OAEP padding for RSA encryption. Shoup (2001) found a gap in the original proof for chosen ciphertext attacks. Fujisaki, Okamoto, Pointcheval and Stern (2001) then proved RSA-OAEP secure under the RSA assumption, with a loose reduction. See [RSA-OAEP](/rsa-oaep/).
- **The Fiat-Shamir transform.** Fiat and Shamir (1986) turned a three-move identification scheme into a signature by replacing the random challenge of the verifier with $H(\text{commitment} \,\|\, m)$. Pointcheval and Stern (1996, journal version 2000) proved such signatures secure in the model with the forking lemma: run the adversary twice with the same random tape and a reprogrammed oracle, and extract the key from two answers to the same commitment. The loss is about a factor $q_H$. See [the Fiat-Shamir heuristic](/fiat-shamir-heuristic/) and [Schnorr signatures](/schnorr-signature/).
- **Key derivation and hybrid encryption.** Many key encapsulation schemes and the Fujisaki-Okamoto transform hash a shared secret into a key, and are proven in the random oracle model. Post-quantum schemes such as ML-KEM use proofs in the QROM.

Few attacks are known on natural schemes with such proofs when the oracle is replaced by a modern hash with domain separation. Most known failures use schemes built to fail, such as those of Canetti, Goldreich and Halevi, or the Fiat-Shamir counterexample of Goldwasser and Kalai (2003). This is why the model remains the usual basis for the analysis of practical signatures and encryption, together with a plain statement that the result is a heuristic.

## References
