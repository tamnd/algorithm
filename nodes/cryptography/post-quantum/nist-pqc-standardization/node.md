---
tag: 5GPRSG
kind: concept
slug: nist-pqc-standardization
name: NIST post-quantum standardization
aliases:
- NIST PQC competition
- NIST PQC standards process
area: cryptography/post-quantum
level: intro
summary: "The public multi-round process (2016 to 2025 and on) in which NIST chose ML-KEM, ML-DSA, SLH-DSA, FN-DSA and HQC from 69 first round submissions, and now tests more signatures."
prereqs: [post-quantum-cryptography]
see_also: [nist-security-levels, crystals-kyber, crystals-dilithium, sphincs-plus, falcon, hqc, sidh, picnic-signature]
sources:
  - url: "https://csrc.nist.gov/CSRC/media/Projects/Post-Quantum-Cryptography/documents/call-for-proposals-final-dec-2016.pdf"
    title: "NIST, Submission Requirements and Evaluation Criteria for the Post-Quantum Cryptography Standardization Process, December 2016"
    locator: Section 4 (evaluation criteria), Section 4.A.5 (the five security strength categories)
  - paper: doi:10.6028/NIST.IR.8240
    title: "Gorjan Alagic et al., NIST IR 8240, Status Report on the First Round of the NIST Post-Quantum Cryptography Standardization Process, January 2019"
    locator: Sections 1 and 3 (the 69 first round candidates and the 26 that advanced)
  - paper: doi:10.6028/NIST.IR.8309
    title: "Gorjan Alagic et al., NIST IR 8309, Status Report on the Second Round of the NIST Post-Quantum Cryptography Standardization Process, July 2020"
    locator: Section 1 and Table 1 (the 7 finalists and 8 alternates)
  - paper: doi:10.6028/NIST.IR.8413
    title: "Gorjan Alagic et al., NIST IR 8413, Status Report on the Third Round of the NIST Post-Quantum Cryptography Standardization Process, July 2022 (updated September 2022 as 8413-upd1)"
    locator: Section 1 (the four selected algorithms and the four round 4 candidates) and Section 4 (the reasons for each decision)
  - paper: doi:10.6028/NIST.IR.8545
    title: "NIST IR 8545, Status Report on the Fourth Round of the NIST Post-Quantum Cryptography Standardization Process, March 2025"
    locator: the abstract and Section 1 (HQC is the only fourth round KEM to be standardized)
  - paper: doi:10.6028/NIST.IR.8528
    title: "NIST IR 8528, Status Report on the First Round of the Additional Digital Signature Schemes for the NIST Post-Quantum Cryptography Standardization Process, October 2024"
    locator: the abstract and Section 1 (40 first round candidates, 14 advanced)
  - paper: doi:10.6028/NIST.IR.8610
    title: "NIST IR 8610, Status Report on the Second Round of the Additional Digital Signature Schemes for the NIST Post-Quantum Cryptography Standardization Process, May 2026"
    locator: the abstract (the nine third round candidates)
  - paper: doi:10.6028/NIST.FIPS.203
    title: "NIST FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard, August 13, 2024"
    locator: the foreword and Section 1 (ML-KEM derived from CRYSTALS-Kyber); FIPS 204 and FIPS 205 of the same date for ML-DSA and SLH-DSA
---

The NIST post-quantum cryptography standardization process is the public, multi-round evaluation that NIST began in December 2016 to choose public-key algorithms that resist quantum computers. It had 69 complete first round submissions, cut them in three more rounds, and published the first standards, FIPS 203 (ML-KEM), FIPS 204 (ML-DSA) and FIPS 205 (SLH-DSA), on August 13, 2024. HQC followed as a second KEM in March 2025, FN-DSA from Falcon is still in progress, and a separate process for more signatures reached its third round in May 2026. This page is about the process. The page [post-quantum cryptography](/post-quantum-cryptography/) explains why the change is necessary and what it replaces.

## In plain words

NIST did not design the new algorithms itself. It asked the world for proposals, published all of them, and let anyone attack them. Each round, NIST read the attacks and the measurements, wrote a public report on its reasons, and kept the best candidates. Teams could tune their designs between rounds.

Several candidates broke in public during the process, some within days and two very late. That was the point of the method: a scheme that survives years of open attack by many teams earns more trust than one that was only reviewed in private. At the end, NIST wrote the survivors as federal standards with new names, so that a product can claim to use exactly the standard version.

## The idea

**The call.** NIST published the call for proposals in December 2016, with a deadline of November 30, 2017 (the call document "Submission Requirements and Evaluation Criteria"). It asked for public-key encryption or key encapsulation mechanisms ([KEMs](/key-encapsulation-mechanism/)) and for digital signatures. Section 4 of the call set the criteria in this order:

1. **Security.** IND-CCA2 security for KEMs and encryption (IND-CPA was allowed for ephemeral use), EUF-CMA for signatures, with up to $2^{64}$ decryption or signing queries. Each parameter set had to claim one of five [security categories](/nist-security-levels/), defined by the cost of key search on AES and collision search on SHA-2 or SHA-3.
2. **Cost and performance.** Key sizes, ciphertext and signature sizes, and the speed of each operation on software and hardware.
3. **Algorithm and implementation characteristics.** Flexibility, simplicity, resistance to side channels, and freedom from patents.

NIST stated that the process was not a competition, because it could select more than one algorithm and because it did not rank the candidates against each other on one scale. Most people still call it a competition.

**The rounds.** Each cut came with a NIST Internal Report (NIST IR) that explained the decisions.

| date | step | candidates | report |
|---|---|---|---|
| December 2016 | call for proposals | | the call, Section 4 |
| November 30, 2017 | submission deadline | 82 received | |
| December 2017 | round 1 | 69 complete and proper submissions | |
| January 30, 2019 | round 2 | 26 (17 KEM or encryption, 9 signatures) | NIST IR 8240 |
| July 22, 2020 | round 3 | 7 finalists and 8 alternates | NIST IR 8309 |
| July 5, 2022 | first selections and round 4 | 4 selected, 4 to round 4 | NIST IR 8413 |
| August 24, 2023 | draft standards | FIPS 203, 204 and 205 drafts for comment | |
| August 13, 2024 | final standards | FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA) | |
| March 11, 2025 | end of round 4 | HQC selected | NIST IR 8545 |

The round 3 finalists were Classic McEliece, CRYSTALS-Kyber, NTRU and SABER (KEMs), and CRYSTALS-Dilithium, Falcon and Rainbow (signatures). The alternates were BIKE, FrodoKEM, HQC, NTRU Prime and SIKE (KEMs), and GeMSS, Picnic and SPHINCS+ (signatures). Finalists could be selected at the end of round 3. Alternates could only be selected after a further round.

**The selections of July 5, 2022 (NIST IR 8413).**

| selected | type | family | standard |
|---|---|---|---|
| [CRYSTALS-Kyber](/crystals-kyber/) | KEM | lattice (Module-LWE) | FIPS 203, ML-KEM |
| [CRYSTALS-Dilithium](/crystals-dilithium/) | signature | lattice (Module-LWE and Module-SIS) | FIPS 204, ML-DSA |
| [Falcon](/falcon/) | signature | lattice (NTRU) | planned FIPS 206, FN-DSA |
| [SPHINCS+](/sphincs-plus/) | signature | hash-based | FIPS 205, SLH-DSA |

NIST named Kyber and Dilithium as the primary algorithms. It kept Falcon for uses that need small signatures, and SPHINCS+ because its security rests only on hash functions and not on lattices. Of the lattice KEM finalists, NIST chose one; [SABER](/saber/) and [NTRU](/ntru-encrypt/) were not selected. [FrodoKEM](/frodokem/) and [NTRU Prime](/ntru-prime/) were not carried into round 4.

**Round 4.** Four KEMs on assumptions other than structured lattices went on: [BIKE](/bike/), [Classic McEliece](/mceliece-cryptosystem/), [HQC](/hqc/) and SIKE. Less than four weeks after the selection, Castryck and Decru published a key recovery attack on [SIDH](/sidh/), the core of SIKE (the [Castryck-Decru attack](/castryck-decru-attack/), July 2022). The SIKE team agreed that the scheme was broken, and it was withdrawn. NIST IR 8545 (March 2025) selected HQC as the only fourth round KEM to be standardized. HQC is code-based, so a break of Module-LWE would not affect it.

**The standards are not the submissions.** NIST changed details when it wrote the standards, so a round 3 implementation of Kyber does not interoperate with ML-KEM. FIPS 203, for example, changed the derivation of the shared secret (it no longer hashes the ciphertext into the key) and added input checks on the encapsulation and decapsulation keys. FIPS 204 and 205 add domain separation for a context string and define pre-hash variants. This is why deployments that started with draft Kyber in TLS had to move to a new code point when ML-KEM was final.

**Additional signatures.** All three signature standards rest either on structured lattices or on large hash-based signatures. In 2022 NIST asked for more signatures, mainly general purpose schemes not based on structured lattices, and schemes with short signatures and fast verification. The call came in September 2022 with a deadline of June 1, 2023.

| date | step | candidates | report |
|---|---|---|---|
| June 1, 2023 | deadline | 50 received | |
| July 17, 2023 | round 1 | 40 | |
| October 24, 2024 | round 2 | 14 | NIST IR 8528 |
| May 14, 2026 | round 3 | 9 | NIST IR 8610 |

The 14 second round candidates were CROSS, FAEST, HAWK, LESS, MAYO, Mirath (a merger of MIRA and MiRitH), MQOM, PERK, QR-UOV, RYDE, SDitH, SNOVA, SQIsign and UOV. The nine in round 3 are FAEST, HAWK, MAYO, MQOM, QR-UOV, SDitH, SNOVA, SQIsign and UOV. They cover multivariate schemes ([UOV](/unbalanced-oil-and-vinegar/), MAYO, QR-UOV, SNOVA), a lattice scheme (HAWK), an isogeny scheme (SQIsign, see [isogeny-based cryptography](/isogeny-based-cryptography/)), and proofs in the head built on a block cipher (FAEST) or on a hard problem (SDitH, MQOM), which descend from the MPC-in-the-head idea of [Picnic](/picnic-signature/).

## Examples

**A candidate that broke during evaluation.** Rainbow was a round 3 signature finalist. In February 2022 Beullens published a key recovery attack that takes about a weekend on a laptop for the category 1 parameters. NIST IR 8413 lists the attack as a reason that Rainbow was not selected. See [Rainbow](/rainbow-signature/).

**A candidate that broke after selection for a further round.** SIKE entered round 4 on July 5, 2022 with the smallest public keys of any KEM. On July 30, 2022 the first version of the Castryck-Decru paper reported that SIKEp434, the category 1 parameter set, falls in about an hour on one core; the revised version reports about ten minutes. No parameter change could save it, because the attack is polynomial time. The process caught this before any standard was written.

**A candidate that survived but was not chosen.** [Picnic](/picnic-signature/) stayed in round 3 as an alternate with no break, but its signatures were large and slow compared with Dilithium and Falcon, and SPHINCS+ already gave a scheme from symmetric primitives alone. NIST IR 8413 did not select it.

**How the categories shaped the choice.** ML-KEM-512, ML-KEM-768 and ML-KEM-1024 target categories 1, 3 and 5. NIST IR 8547 recommends ML-KEM-768 as the default. The category system is defined on the page [NIST security levels](/nist-security-levels/).

## Where it is used

- **Federal and FIPS 140 validation.** A product can be validated only for the standard versions (ML-KEM, ML-DSA, SLH-DSA), not for round 3 submissions.
- **Protocol standards.** TLS, SSH, IKEv2 and X.509 specify the standard names and code points, often for [hybrid key exchange](/hybrid-key-exchange/).
- **Transition plans.** NIST IR 8547 builds on these standards to set the dates for the end of RSA and elliptic curve cryptography in federal use (deprecated after 2030, disallowed after 2035). See [post-quantum cryptography](/post-quantum-cryptography/).
- **Other bodies.** Many national agencies and standards bodies follow the NIST selections, or add other schemes such as FrodoKEM and Classic McEliece through their own processes.

## References
