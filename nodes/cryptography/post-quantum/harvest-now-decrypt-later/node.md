---
tag: 5T7EBA
kind: concept
slug: harvest-now-decrypt-later
name: Harvest now, decrypt later
aliases:
- store-now-decrypt-later
- HNDL
area: cryptography/post-quantum
level: intro
summary: "An adversary records encrypted traffic today and decrypts it when a quantum computer can break the key exchange. Mosca's inequality x + y > z says when to act."
prereqs: [post-quantum-cryptography, diffie-hellman, perfect-forward-secrecy]
see_also: [hybrid-key-exchange, tls-handshake, crypto-agility, nist-pqc-standardization, shor-algorithm, crystals-kyber, ntru-prime, key-transport-problem]
sources:
  - paper: doi:10.1109/MSP.2018.3761723
    title: "Michele Mosca, Cybersecurity in an era with quantum computers: will we be ready?, IEEE Security and Privacy 16(5), 2018 (preprint IACR ePrint 2015/1075)"
    locator: the section with the inequality x + y > z and the figure of the security shelf life, the migration time and the collapse time
  - paper: doi:10.6028/NIST.IR.8547
    title: "NIST IR 8547, Transition to Post-Quantum Cryptography Standards, final version, October 2026"
    locator: Section 1 (the harvest now, decrypt later threat), Section 3 (Mosca's theorem and the remark that signatures are not vulnerable to it), Section 3.1 on key establishment, and Section 4.1.2
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5), 1997"
    locator: the algorithms for factoring and for discrete logarithms that make recorded RSA and Diffie-Hellman traffic readable
  - url: "https://www.rfc-editor.org/rfc/rfc8446"
    title: "Eric Rescorla, RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3, 2018"
    locator: Section 1.2 (static RSA and Diffie-Hellman cipher suites removed; all public-key exchange gives forward secrecy) and Section 4.2.8 (key_share)
  - url: "https://signal.org/docs/specifications/pqxdh/"
    title: "Ehren Kret and Rolfe Schmidt, The PQXDH Key Agreement Protocol, Signal, 2023"
    locator: Sections 1 and 2 (X25519 combined with a post-quantum KEM to protect against harvest now, decrypt later)
  - url: "https://security.apple.com/blog/imessage-pq3/"
    title: "Apple Security Engineering and Architecture, iMessage with PQ3: The new state of the art in quantum-secure messaging at scale, February 2024"
    locator: the sections on the threat of harvest now, decrypt later and on the initial key establishment and rekeying with Kyber
  - url: "https://www.openssh.com/txt/release-9.0"
    title: "OpenSSH 9.0 release notes, April 2022"
    locator: the note that the default key exchange is now the hybrid sntrup761x25519-sha512@openssh.com, to resist capture now, decrypt later attacks
---

Harvest now, decrypt later is the threat in which an adversary records encrypted traffic today, stores it, and decrypts it years later, when a quantum computer can run [Shor's algorithm](/shor-algorithm/) against the public-key exchange that protected it. The attack needs no quantum computer today, only storage, so data that must stay secret for many years is already at risk. Mosca's inequality turns this into a planning rule: if the years the data must stay secret plus the years the migration takes exceed the years until a quantum computer arrives, the migration is already late. The threat is the main reason why key exchange moves to post-quantum algorithms before signatures do.

## In plain words

Imagine someone copies every locked letter you send and keeps the copies in a warehouse. Today they cannot open them. But they know that a master key for this type of lock will exist in some years. On that day, every letter in the warehouse opens.

So the question is not "is there a quantum computer today?" It is "will my data still be secret when one exists?" A credit card number that expires next year is safe. A medical record, a state secret or the name of a source must stay secret for decades.

The answer is to change the lock on the letters now, before they are copied. This is why browsers, messaging apps and SSH added post-quantum key exchange years before a quantum computer exists.

## The idea

**The threat model.** The adversary is passive: it records ciphertexts and handshakes but does not change them. It has large storage and patience, which suits intelligence agencies with access to backbone links. Recording is cheap, and the adversary does not need to know which sessions matter; it can keep everything, or keep sessions to valuable targets. The attack succeeds on a recorded session if, at some later time, the adversary can get the session key. With classical key exchange there are two ways to get it:

1. **A leak of a long-term key.** If the session key was sent encrypted under the server's static RSA key (RSA key transport, as in TLS 1.2 RSA cipher suites), a later theft of that key opens every recorded session. Ephemeral [Diffie-Hellman](/diffie-hellman/) with erased exponents gives [forward secrecy](/perfect-forward-secrecy/) against this: a leak of the long-term signing key reveals nothing about past session keys.
2. **A quantum computer.** Shor's algorithm factors the RSA modulus and computes discrete logarithms in finite fields and on elliptic curves. The ephemeral Diffie-Hellman shares are on the wire, so the adversary recovers an exponent from a recorded share and computes the shared secret. Forward secrecy does not help: it protects against a key leak, not against a break of the underlying problem.

**Mosca's inequality.** Mosca (ePrint 2015/1075; IEEE Security and Privacy, 2018) defined three numbers of years:

- $x$, the **security shelf life**: how long the data must stay secret;
- $y$, the **migration time**: how long it takes to deploy quantum-safe cryptography in the systems that protect it;
- $z$, the **collapse time**: how long until a quantum computer can break the public-key cryptography in use.

If $x + y > z$, then data encrypted near the end of the migration must still be secret after the collapse, and the adversary who records it will read it. More exactly, data created at time $t$ with the old algorithm is exposed if $t + x > z$, and the old algorithm stays in use until $t = y$. So the data created in the interval $[\max(0, z - x), y]$ is exposed, and this interval is not empty exactly when $x + y > z$. The latest year to start a migration is $z - x - y$ from now; if this is negative, the start is already late. Nobody knows $z$, and $y$ for a large organization is often ten years or more, which is why NIST IR 8547 (Section 3) calls for action now even if quantum computers are a decade away.

**Why key exchange moves first.** A signature only has to be unforgeable when someone checks it. A future quantum computer cannot change the past: a TLS handshake signed with ECDSA in 2026 was checked in 2026, and forging that signature in 2040 deceives nobody. So signatures are not exposed to harvest now, decrypt later (NIST IR 8547, Section 3). Confidentiality is different, because a recorded ciphertext stays a ciphertext forever. The exceptions on the signature side are signatures that must be checked far in the future, such as root certificates, firmware and secure boot keys, and legal documents; these must move early for another reason, their long life.

**What is not affected.** Symmetric encryption with a pre-shared key that never crossed the network under public-key encryption is not exposed: Grover gives only a square root speedup, and AES-256, or even AES-128 under NIST's view (see [NIST security levels](/nist-security-levels/)), stays secure. Data at rest whose keys are wrapped under RSA or elliptic curve keys, such as OpenPGP or S/MIME email and encrypted backups, is exposed as soon as the ciphertext and the wrapped key are copied.

**The fix: post-quantum or hybrid key exchange.** The sender must protect the session key with a post-quantum key encapsulation mechanism, such as [ML-KEM](/crystals-kyber/) or [Streamlined NTRU Prime](/ntru-prime/). Most deployments use [hybrid key exchange](/hybrid-key-exchange/), which combines a classical exchange such as X25519 with the post-quantum KEM so that the session key stays secret if either one holds. A hybrid adds about 1 to 2 KB to a handshake; in TLS 1.3 the X25519MLKEM768 key share is 1216 bytes from the client and 1120 bytes from the server.

## Examples

**The toy recorder.** The code with this page records five toy sessions of each type, then gives the adversary one of two future events:

| key exchange | after a leak of the server's long-term key | after a quantum computer |
|---|---|---|
| static RSA key transport | all sessions readable | all sessions readable |
| ephemeral Diffie-Hellman, server share signed | no session readable | all sessions readable |

The quantum computer is a stand-in that factors a 31-bit RSA modulus by trial division and computes discrete logarithms in a 31-bit prime field by baby-step giant-step. The parameters are toy sizes, and the code is for study only, not constant time. In real systems, use TLS 1.3 with a hybrid post-quantum group from a maintained library, or a FIPS 140 validated module.

**Mosca's inequality with numbers.** Data that must stay secret for $x = 10$ years, a migration that takes $y = 5$ years, and a quantum computer in $z = 12$ years: $10 + 5 > 12$, so we must act. The data created between year 2 and year 5 is exposed, and the migration should have started three years ago. With $x = 5$, $y = 5$ and $z = 15$ there is no exposure, and the migration can wait five years. With $x = 25$ (for example, medical or classified data), any $y > 0$ and $z = 15$, the data created from today is exposed.

**Mosca's own estimate.** In the 2018 paper Mosca estimated a 1 in 7 chance that RSA-2048 is broken by 2026 and a 1 in 2 chance by 2031. Later estimates of the cost of breaking RSA-2048 fell, for example to about 20 million noisy qubits for 8 hours (Gidney and Ekerå, 2021), which shortens $z$.

**Deployments of post-quantum key exchange.**

| system | change | date |
|---|---|---|
| OpenSSH 9.0 | hybrid sntrup761x25519-sha512 as default key exchange | April 2022 |
| Chrome 116 | hybrid X25519Kyber768 in TLS, then default on desktop in Chrome 124 | August 2023, April 2024 |
| Signal | PQXDH: X25519 plus a Kyber-1024 KEM in the initial key agreement | September 2023 |
| Apple iMessage | PQ3: Kyber in the initial key establishment and periodic rekeying | February 2024 (iOS 17.4) |
| Chrome 131 | X25519MLKEM768 with the final ML-KEM in place of the draft Kyber | November 2024 |
| OpenSSH 10.0 | mlkem768x25519-sha256 as default key exchange | April 2025 |

The OpenSSH 9.0 release notes name the threat directly: the hybrid is the default "to resist capture now, decrypt later attacks". Cloudflare has offered hybrid post-quantum key agreement since 2022, and a large share of the TLS traffic it carries now uses it. In all these systems the signatures, and so the authentication, are still classical, because of the asymmetry above.

## Where it is used

- **Migration priority.** NIST IR 8547 and the US memorandum OMB M-26-15 tell agencies to put first the systems whose data must stay secret beyond 2030, and to move key establishment before the general deprecation of RSA and elliptic curves after 2030.
- **Protocol design.** TLS 1.3, SSH, IKEv2 and messaging protocols added hybrid key exchange first, and post-quantum authentication later. See [crypto-agility](/crypto-agility/).
- **Risk assessment.** Organizations classify data by shelf life $x$ and systems by migration time $y$, and use Mosca's inequality to rank them.
- **Long-lived secrets in transit.** Diplomatic and military links, health records, genomic data, and the identity of sources and dissidents are the usual examples of data with a long $x$.

## References
