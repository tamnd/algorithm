---
tag: 6K1QN6
kind: concept
slug: post-quantum-cryptography
name: Post-quantum cryptography
aliases:
- PQC
- quantum-resistant cryptography
- quantum-safe cryptography
area: cryptography/post-quantum
level: intro
summary: "Public-key cryptography that runs on classical computers and resists attacks by quantum computers: Shor's algorithm breaks RSA, DH and ECC, so lattice, code and hash schemes replace them."
prereqs: [public-key-cryptography, shor-algorithm, grover-search]
see_also: [nist-pqc-standardization, nist-security-levels, harvest-now-decrypt-later, crypto-agility, hybrid-key-exchange, lattice-based-cryptography, hash-based-signatures, isogeny-based-cryptography]
sources:
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5), 1997, pages 1484 to 1509"
    locator: the whole paper (factoring by order finding, and discrete logarithms in a group); first at FOCS 1994
  - paper: doi:10.1145/237814.237866
    title: "Lov K. Grover, A fast quantum mechanical algorithm for database search, STOC 1996, pages 212 to 219"
    locator: the search of N items with about the square root of N oracle queries
  - paper: doi:10.6028/NIST.FIPS.203
    title: "NIST FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard, August 13, 2024"
    locator: Section 1 and Table 2 (the parameter sets ML-KEM-512, ML-KEM-768 and ML-KEM-1024 and their security categories), Table 3 (sizes)
  - paper: doi:10.6028/NIST.FIPS.204
    title: "NIST FIPS 204, Module-Lattice-Based Digital Signature Standard, August 13, 2024"
    locator: Section 4, Tables 1 and 2 (the parameter sets ML-DSA-44, ML-DSA-65 and ML-DSA-87, key and signature sizes)
  - paper: doi:10.6028/NIST.FIPS.205
    title: "NIST FIPS 205, Stateless Hash-Based Digital Signature Standard, August 13, 2024"
    locator: Section 11, Table 2 (the twelve SLH-DSA parameter sets and their sizes)
  - paper: doi:10.6028/NIST.IR.8547
    title: "Dustin Moody, Ray Perlner, Andrew Regenscheid, Angela Robinson and David Cooper, NIST IR 8547, Transition to Post-Quantum Cryptography Standards, initial public draft November 2024, final October 2026"
    locator: Section 4.1, Tables 2 and 4 (quantum-vulnerable algorithms deprecated after 2030 and disallowed after 2035), Section 4.1.3 (symmetric primitives with 128 bits of classical security meet category 1)
  - paper: doi:10.6028/NIST.IR.8545
    title: "NIST IR 8545, Status Report on the Fourth Round of the NIST Post-Quantum Cryptography Standardization Process, March 2025"
    locator: the abstract and the conclusion (HQC selected for standardization)
  - paper: doi:10.22331/q-2021-04-15-433
    title: "Craig Gidney and Martin Ekera, How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits, Quantum 5, 433, 2021"
    locator: the abstract and the cost tables (a resource estimate for Shor's algorithm on RSA-2048)
  - paper: "Ward Beullens, Breaking Rainbow takes a weekend on a laptop, CRYPTO 2022, LNCS 13508"
    locator: the abstract and Section 1 (key recovery for the Rainbow category 1 parameters)
  - book: isbn:9783540887010
    title: "Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009"
    locator: Chapter 1 (Bernstein, Introduction to post-quantum cryptography) and the survey chapters on each family
---

Post-quantum cryptography is [public-key cryptography](/public-key-cryptography/) that runs on ordinary computers and that is believed to resist attacks by large quantum computers. [Shor's algorithm](/shor-algorithm/) factors integers and computes discrete logarithms in polynomial time on a quantum computer, so it breaks [RSA](/rsa-cryptosystem/), [Diffie-Hellman](/diffie-hellman/) and [elliptic curve cryptography](/elliptic-curve-cryptography/). Post-quantum schemes replace them with problems from lattices, codes, hash functions, multivariate polynomials and isogenies, for which no fast quantum algorithm is known. NIST published the first three standards, FIPS 203, 204 and 205, on August 13, 2024.

## In plain words

Most of the public-key cryptography in use today rests on two problems: factoring a large number, and finding a hidden exponent in a group. A large quantum computer of the right kind would solve both problems fast. Such a computer does not exist yet. But data that is encrypted today can be recorded and kept until it does.

Post-quantum cryptography is the answer that needs no quantum hardware. It uses other hard problems, which quantum computers do not seem to solve fast either: finding a short vector in a lattice, decoding a random linear code, inverting a hash function. The new schemes run on the same computers and in the same protocols as the old ones. They have larger keys or larger signatures, and their security is younger, so the change is slow and careful.

## The idea

**What a quantum computer breaks.** Shor's algorithm finds the period of a function $x \mapsto a^x \bmod N$ with a quantum Fourier transform. From the period it factors $N$, and the same method computes discrete logarithms in any group with an efficient group law ([Shor 1997](/shor-algorithm/), first at FOCS 1994). The cost is a polynomial in the bit length $n$ of the modulus, about $O(n^3)$ gates with schoolbook arithmetic. So each scheme whose security reduces to factoring, the [RSA problem](/rsa-problem/), the [discrete logarithm problem](/discrete-logarithm-problem/) or the [elliptic curve discrete logarithm](/elliptic-curve-discrete-logarithm-problem/) is broken in polynomial time, at every key size. Larger keys do not help: they cost the defender more than the attacker. This covers RSA encryption and signatures, finite field and elliptic curve Diffie-Hellman, DSA, ECDSA and EdDSA. The attack needs a fault tolerant machine. Gidney and Ekerå (2021) estimate that RSA-2048 falls in about 8 hours on 20 million noisy physical qubits under their hardware assumptions. Later papers lower the qubit count further; the estimates move, and the direction so far has been down.

**What a quantum computer only weakens.** [Grover's algorithm](/grover-search/) finds one marked item among $N$ with about $\frac{\pi}{4}\sqrt{N}$ oracle calls, and this is optimal for unstructured search. Applied to [exhaustive key search](/exhaustive-key-search/) on a $k$-bit key it needs about $\frac{\pi}{4} 2^{k/2}$ sequential evaluations of the cipher inside a quantum circuit: $2^{63.7}$ for $k = 128$, $2^{95.7}$ for $k = 192$ and $2^{127.7}$ for $k = 256$. The common advice is therefore to double the key length: AES-256 for keys, and SHA-384 or more where a hash must give a 192-bit or higher margin. NIST takes a less strict view. Grover's iterations must run one after the other, and splitting the search over $S$ machines only saves a factor $\sqrt{S}$ in time. The NIST [security categories](/nist-security-levels/) take this into account, and NIST IR 8547 (Section 4.1.3) states that all approved symmetric primitives with at least 128 bits of classical security, AES-128 included, are believed to meet category 1. The quantum collision search of Brassard, Høyer and Tapp ([BHT](/brassard-hoyer-tapp-collision/)) needs about $2^{n/3}$ queries for an $n$-bit hash, but it also needs that much memory with quantum access, and the best known analyses do not make it cheaper than classical collision search in practice.

**The families.** Each family rests on a problem with no known polynomial time quantum algorithm.

| family | hard problem | standard or main example | typical size (bytes) |
|---|---|---|---|
| [lattice](/lattice-based-cryptography/) | [Module-LWE](/module-learning-with-errors/), Module-SIS, [NTRU](/ntru-problem/) | [ML-KEM](/crystals-kyber/) (FIPS 203), [ML-DSA](/crystals-dilithium/) (FIPS 204), [FN-DSA](/falcon/) | ML-KEM-768: public key 1184, ciphertext 1088. ML-DSA-65: public key 1952, signature 3309 |
| [hash-based](/hash-based-signatures/) | second preimage and related properties of a hash | [SLH-DSA](/sphincs-plus/) (FIPS 205), [XMSS](/xmss/) and [LMS](/leighton-micali-signature/) (SP 800-208) | SLH-DSA-SHA2-128s: public key 32, signature 7856 |
| [code-based](/code-based-cryptography/) | [syndrome decoding](/syndrome-decoding-problem/) of a random-looking code | [HQC](/hqc/) (selected March 2025), [Classic McEliece](/mceliece-cryptosystem/), [BIKE](/bike/) | Classic McEliece has public keys of hundreds of kilobytes |
| [multivariate](/multivariate-cryptography/) | [solving quadratic systems](/multivariate-quadratic-problem/) | [UOV](/unbalanced-oil-and-vinegar/), MAYO; [Rainbow](/rainbow-signature/) was broken in 2022 | UOV: short signatures, large public keys |
| [isogeny](/isogeny-based-cryptography/) | paths between supersingular curves | SQIsign; [SIDH](/sidh/) and SIKE were broken in 2022 | SQIsign: the smallest public key plus signature of the family |
| symmetric (MPC-in-the-head) | one-wayness of a block cipher | [Picnic](/picnic-signature/) (not selected), FAEST | signatures of several kilobytes |

**Encryption moves first.** A key exchange that is recorded today can be decrypted when a quantum computer exists. This is the [harvest now, decrypt later](/harvest-now-decrypt-later/) threat. A signature must be forged before it is verified, so a future quantum computer cannot forge the signatures of the past in the same way. Most deployments therefore started with key exchange, as a [hybrid](/hybrid-key-exchange/) of a classical group and a post-quantum [KEM](/key-encapsulation-mechanism/). The shared secret stays safe if either part holds.

**Standards and dates.** The standards came out of the [NIST process](/nist-pqc-standardization/) that started in 2016.

| date | event |
|---|---|
| August 13, 2024 | FIPS 203 (ML-KEM, from CRYSTALS-Kyber), FIPS 204 (ML-DSA, from CRYSTALS-Dilithium) and FIPS 205 (SLH-DSA, from SPHINCS+) |
| November 2024 | NIST IR 8547 initial public draft: deprecate 112-bit classical schemes after 2030, disallow quantum-vulnerable schemes after 2035 |
| March 11, 2025 | NIST IR 8545: HQC is selected as a second KEM, on a different assumption from ML-KEM |
| October 2026 | NIST IR 8547 final: all quantum-vulnerable public-key schemes are deprecated after 2030 and disallowed after 2035, whatever the key size |
| in progress | FN-DSA (from Falcon), planned as FIPS 206; no draft had been published when this page was written (November 2026) |

The final IR 8547 is stricter than its draft. The draft deprecated only the parameter sets with 112 bits of classical security after 2030, so RSA-3072 or P-256 seemed allowed until 2035. The final text (Tables 2 and 4) deprecates every approved quantum-vulnerable signature and key establishment scheme, at 112 bits of classical security or more, after 2030.

**Security proofs.** The new schemes come with proofs in the [quantum random oracle model](/quantum-random-oracle-model/), where the adversary can query the hash in superposition. The classical proofs of the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) and of the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/) do not carry over directly, and the quantum proofs often lose more in the reduction.

**What post-quantum cryptography is not.** It is not quantum cryptography. Quantum key distribution needs quantum channels and special hardware, and it gives no signatures. Post-quantum schemes are ordinary software.

## Examples

**Which current schemes break.** With a cryptographically relevant quantum computer:

| scheme | attack | effect |
|---|---|---|
| RSA-2048 and RSA-3072 (encryption, signatures) | Shor (factoring) | broken at every size |
| finite field DH, DSA | Shor (discrete log in $\mathbb{Z}_p^*$) | broken |
| X25519, ECDH P-256, ECDSA, Ed25519 | Shor (elliptic curve discrete log) | broken |
| AES-128 | Grover, about $2^{64}$ sequential cipher calls | weakened; NIST still counts it as category 1 |
| AES-256 | Grover, about $2^{128}$ sequential cipher calls | the margin advised for long term secrets |
| SHA-256 collisions | BHT in theory, $2^{85}$ queries and as much quantum memory | no practical gain known |
| HMAC-SHA-256, SHA-256 preimages | Grover, about $2^{128}$ | safe |

**The cost of the change in bytes.** A TLS 1.3 handshake with X25519 sends 32 bytes in each direction for the key exchange. The hybrid X25519MLKEM768 sends $32 + 1184 = 1216$ bytes from the client and $32 + 1088 = 1120$ bytes from the server. The signature side costs more: a certificate chain with ML-DSA-65 has a 1952-byte public key and a 3309-byte signature at each level, against 32 and 64 bytes for Ed25519.

**A failed family.** The knapsack schemes of the late 1970s and 1980s were once candidates for a future without factoring. Lattice reduction broke all of them. The page [knapsack cryptosystems after Merkle-Hellman](/merkle-hellman-knapsack/) tells that story, and the lesson it left for lattice schemes: the instances must be hard on average, with an argument, and not only hard in the worst case.

**Two breaks during the NIST process.** Rainbow, a multivariate finalist, fell to Beullens' key recovery attack in 2022 (a weekend on a laptop for the category 1 parameters). SIKE, an isogeny candidate of round 4, fell to the [Castryck-Decru attack](/castryck-decru-attack/) in July 2022. These breaks are the main argument for [crypto agility](/crypto-agility/) and for hybrid deployments.

## Where it is used

- **TLS.** Chrome enabled the hybrid X25519Kyber768 by default on desktop in version 124 (April 2024) and moved to X25519MLKEM768 in version 131. Firefox, Cloudflare and other large servers support the same hybrid. See [hybrid key exchange](/hybrid-key-exchange/).
- **SSH.** OpenSSH uses the hybrid `sntrup761x25519-sha512` by default since version 9.0 (April 2022), and the hybrid `mlkem768x25519-sha256` by default since version 10.0 (April 2025).
- **Messaging.** Signal added PQXDH (an ML-KEM based extension of [X3DH](/x3dh/)) in 2023, and Apple added PQ3 to iMessage in 2024. Both are discussed in [harvest now, decrypt later](/harvest-now-decrypt-later/).
- **Firmware and long-lived signatures.** The stateful hash-based schemes [XMSS](/xmss/) and [LMS](/leighton-micali-signature/) (NIST SP 800-208) sign firmware where a signing counter can be kept safely.
- **Policy.** NIST IR 8547 sets the end dates for the old schemes. The [security categories](/nist-security-levels/) define how each new parameter set compares with AES and SHA-2.

## References
