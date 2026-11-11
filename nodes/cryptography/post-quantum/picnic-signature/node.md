---
tag: CCDYS8
kind: algorithm
slug: picnic-signature
name: Picnic signature
aliases:
- Picnic
- ZKB++ signature
- MPC-in-the-head signature
area: cryptography/post-quantum
level: research
summary: "Signature (Chase et al., 2017) that proves knowledge of a LowMC key by MPC-in-the-head (ZKB++, later KKW) and Fiat-Shamir. A NIST round 3 alternate, not selected."
model: word-ram
complexity:
  vars: {t: "the number of parallel repetitions", g: "the number of gates in the circuit of the cipher", a: "the number of AND gates"}
  time: {worst: Θ(t g), average: Θ(t g), best: Θ(t g)}
  space: {extra: Θ(t a)}
properties: {deterministic: false, randomized: true}
history:
  year: 2017
  people: [Melissa Chase, David Derler, Steven Goldfeder, Claudio Orlandi, Sebastian Ramacher, Christian Rechberger, Daniel Slamanig, Greg Zaverucha]
  note: Presented at ACM CCS 2017 and submitted to the NIST process the same year. It was an alternate in round 3 and was not selected in 2022.
prereqs: [digital-signature, zero-knowledge-proof, fiat-shamir-heuristic, secure-multiparty-computation]
see_also: [secret-sharing, commitment-scheme, sigma-protocol, sphincs-plus, unbalanced-oil-and-vinegar, nist-pqc-standardization, quantum-random-oracle-model, shake]
sources:
  - paper: "Melissa Chase, David Derler, Steven Goldfeder, Claudio Orlandi, Sebastian Ramacher, Christian Rechberger, Daniel Slamanig and Greg Zaverucha, Post-quantum zero-knowledge and signatures from symmetric-key primitives, ACM CCS 2017"
    locator: ZKB++, its (2,3)-decomposition and AND gate, the Fiat-Shamir and Unruh signatures, and the choice of LowMC
  - paper: "Yuval Ishai, Eyal Kushilevitz, Rafail Ostrovsky and Amit Sahai, Zero-knowledge from secure multiparty computation, STOC 2007"
    locator: the MPC-in-the-head construction of a zero-knowledge proof from a protocol among virtual players
  - paper: "Irene Giacomelli, Jesper Madsen and Claudio Orlandi, ZKBoo: faster zero-knowledge for Boolean circuits, USENIX Security 2016"
    locator: the 3-player decomposition with XOR shares, the AND gate formula, and soundness 2/3 per repetition
  - paper: "Jonathan Katz, Vladimir Kolesnikov and Xiao Wang, Improved non-interactive zero knowledge with applications to post-quantum signatures, ACM CCS 2018"
    locator: MPC-in-the-head with preprocessing and many players (KKW), the basis of Picnic2 and Picnic3
  - paper: "Martin R. Albrecht, Christian Rechberger, Thomas Schneider, Tyge Tiessen and Michael Zohner, Ciphers for MPC and FHE, EUROCRYPT 2015, LNCS 9056"
    locator: the block cipher LowMC with a partial S-box layer and few AND gates
  - paper: "Daniel Kales and Greg Zaverucha, Improving the performance of the Picnic signature scheme, IACR TCHES 2020(4)"
    locator: the Picnic3 parameters (16 players, 252 executions, 36 opened, LowMC with n = 129 and 4 rounds) and the measured sizes of Picnic-L1-FS and Picnic3-L1
  - url: "https://github.com/microsoft/Picnic/tree/master/spec"
    title: Greg Zaverucha and others, The Picnic signature algorithm, specification version 3.0, 2020
    locator: the parameter sets, key and signature sizes, and the serialization
  - paper: doi:10.6028/NIST.IR.8413
    title: NIST, Status report on the third round of the NIST post-quantum cryptography standardization process, NIST IR 8413, 2022
    locator: the selection of ML-DSA, Falcon and SPHINCS+ and the status of Picnic as an alternate that was not selected
  - paper: doi:10.6028/NIST.IR.8528
    title: NIST, Status report on the first round of the additional digital signature schemes for the NIST post-quantum cryptography standardization process, NIST IR 8528, October 2024
    locator: the 14 schemes that moved to round 2
  - paper: doi:10.6028/NIST.IR.8610
    title: NIST, Status report on the second round of the additional digital signature schemes for the NIST post-quantum cryptography standardization process, NIST IR 8610, May 2026
    locator: the 9 schemes that moved to round 3
  - paper: "Carsten Baum, Lennart Braun, Cyprien Delpech de Saint Guilhem, Michael Klooss, Emmanuela Orsini, Lawrence Roy and Peter Scholl, Publicly verifiable zero-knowledge and post-quantum signatures from VOLE-in-the-head, CRYPTO 2023"
    locator: VOLE-in-the-head and the FAEST signature from AES
  - paper: "Thibauld Feneuil, Antoine Joux and Matthieu Rivain, Syndrome decoding in the head: shorter signatures from zero-knowledge proofs, CRYPTO 2022"
    locator: MPC-in-the-head for the syndrome decoding problem, the basis of SDitH
---

Picnic is a [digital signature](/digital-signature/) whose security rests only on a block cipher and a hash function. The public key is a pair $(p, y)$ with $y = E_k(p)$ for the block cipher LowMC, and the secret key is the cipher key $k$. A signature is a non-interactive [zero-knowledge proof](/zero-knowledge-proof/) that the signer knows $k$, made with the MPC-in-the-head method and the [Fiat-Shamir heuristic](/fiat-shamir-heuristic/), with the message mixed into the hash. Chase and others introduced it at CCS 2017 with the proof system ZKB++. Later versions used the KKW proof system. Picnic was an alternate in round 3 of the [NIST process](/nist-pqc-standardization/) and was not selected, but its method led to several schemes in the later NIST call for additional signatures.

**Notation.** $\oplus$ is XOR and $\wedge$ is AND, on bits or bitwise on words. $E_k(p)$ is a block cipher. A value $v$ is shared among three players as $v = v_0 \oplus v_1 \oplus v_2$. Player indices are taken mod 3, and $e$ is a challenge in $\{0, 1, 2\}$. $t$ is the number of parallel repetitions and $H$ is a hash function, here [SHAKE](/shake/).

## In plain words

The signer knows a secret key that turns a public input into a public output under a cipher. She wants to prove that she knows the key without showing it.

She imagines three helpers. She splits the key into three random pieces that combine to the real key, and gives one to each helper. The helpers compute the cipher together, each seeing only their own piece and the messages between them. She writes down what each helper saw and seals each record.

A hash of the message and the sealed records then picks two of the three helpers. She opens their records. A checker replays those two helpers and checks that they agree with each other and with the public output. Two records show nothing about the key. A cheater is caught with chance one in three each time, so the signer repeats this a few hundred times at once.

## The problem

The goal is a signature that stays secure against quantum computers and needs no number theory or new hard problem, only a one-way function. Any one-way function $f$ gives a signature: the public key is $f(k)$, and a signature is a proof of knowledge of $k$, made non-interactive with a hash. The cost is the size of the proof, which grows with the number of AND gates in the circuit of $f$. Picnic takes $f(k) = E_k(p)$ for a fixed $p$, with LowMC, a cipher made to have few AND gates.

**MPC-in-the-head.** Ishai, Kushilevitz, Ostrovsky and Sahai (STOC 2007) showed that a [secure multiparty computation](/secure-multiparty-computation/) protocol gives a zero-knowledge proof. The prover runs all players "in her head", [commits](/commitment-scheme/) to each player's view, and opens the views that the verifier asks for. If the protocol keeps the input private against the opened players, the proof is zero-knowledge. If the views of the opened players must agree, a cheating prover is caught with fixed probability. ZKBoo (Giacomelli, Madsen and Orlandi, 2016) made this practical for Boolean circuits with three players, and ZKB++ cut the proof size by about half.

## The algorithm

**The 3-player protocol.** The key is shared as $k = k_0 \oplus k_1 \oplus k_2$. Players 0 and 1 derive their shares and random tapes from seeds; $k_2$ is fixed by the key. An XOR gate is computed locally on the shares, and a public constant is XORed into share 0 only. For an AND gate $c = a \wedge b$, player $i$ computes

$$c_i = (a_i \wedge b_i) \oplus (a_{i+1} \wedge b_i) \oplus (a_i \wedge b_{i+1}) \oplus R_i \oplus R_{i+1},$$

where $R_i$ is the next bit of its random tape. The XOR of the three $c_i$ has every product $a_i \wedge b_j$ once and every $R_i$ twice, so it equals $a \wedge b$. Player $i$ needs the shares of player $i + 1$, so the view of player $i$ is its seed and its AND outputs, and views $e$ and $e + 1$ together let a verifier recompute all of view $e$.

```pseudo id=main
SIGN(k, (p, y), m, t)
L1  for j ← 1 to t do
L2      seed_0, seed_1, seed_2 ← random; k_0, k_1 ← shares from seed_0, seed_1; k_2 ← k ⊕ k_0 ⊕ k_1
L3      run the 3-player protocol for E_k(p); view_i ← (seed_i, the AND outputs c_i of player i)
L4      y_i ← output share of player i; C_i ← H(view_i, and k_2 if i = 2)     ▷ commitments, i = 0, 1, 2
L5  (e_1, …, e_t) ← values in {0, 1, 2} from H(p, y, m, all y_i and C_i)        ▷ Fiat-Shamir
L6  for j ← 1 to t do
L7      π_j ← (seed_e, seed_{e+1}, k_2 if player 2 is opened, the AND outputs of player e + 1, C_{e+2}), with e = e_j
L8  return σ = (e_1, …, e_t, π_1, …, π_t)

VERIFY((p, y), m, σ)
L9  for j ← 1 to t do
L10     from π_j, recompute views e and e + 1, the shares y_e, y_{e+1}, and C_e, C_{e+1}
L11     y_{e+2} ← y ⊕ y_e ⊕ y_{e+1}
L12 accept if and only if (e_1, …, e_t) = values from H(p, y, m, all y_i and C_i)
```

Line L10 runs player $e$ in full, from its own seed and the shares of player $e + 1$, and takes the AND outputs of player $e + 1$ from the proof. Line L11 is the ZKB++ trick: the third output share is not sent but recomputed, so the hash at line L12 matches only if the three shares XOR to $y$. Picnic-L1-FS uses LowMC with a 128-bit block, 10 S-boxes per round and 20 rounds, which is 600 AND gates, and $t = 219$ because $(2/3)^{219} < 2^{-128}$. The public key is 32 bytes and the secret key 16 bytes.

## Example

The code with this page follows ZKB++ exactly as above, but **it is not the Picnic specification with LowMC**. Its one-way function is a toy cipher on 32-bit words: $s \leftarrow p \oplus k$, then four rounds of $s \leftarrow s \oplus (\mathrm{rotl}(s, 1) \wedge \mathrm{rotl}(s, 2))$ and $s \leftarrow \mathrm{rotl}(s, 5) \oplus RC_r \oplus k$. That is 128 AND gates. A key of 32 bits falls to brute force, so this is a toy. The code does not use Picnic's serialization, seed tree or KDF, so it does not reproduce the Picnic test vectors.

With seed 2024 the secret key is $k = \texttt{7857dd86}$, the public key is $p = \texttt{2e84496e}$, $y = \texttt{eb8addd7}$, and the message is `hello`.

1. The signer runs 219 repetitions of the protocol and commits to the three views of each.
2. The hash gives 219 challenges; the first twelve are $2, 0, 1, 0, 2, 0, 1, 0, 1, 2, 1, 2$, and over all rounds the values 0, 1 and 2 occur 71, 84 and 64 times.
3. In the first repetition, $e = 2$, so the proof opens players 2 and 0. It holds both seeds, the share $k_2 = \texttt{58878087}$, the four AND output words of player 0, which are $\texttt{691a1fb9}$, $\texttt{31f606e7}$, $\texttt{7a9657ac}$ and $\texttt{4abeb490}$, and the commitment of player 1.
4. The verifier replays players 2 and 0, gets $y_2$ and $y_0$, sets $y_1 = y \oplus y_2 \oplus y_0$, recomputes the commitments, and gets the same 219 challenges. The signature has 18,167 bytes.

The tests change one AND output, one seed, the closed commitment, the share $k_2$ or one challenge, and each change makes the signature fail. They also show the simplest cheat. A prover with a wrong key runs the protocol honestly and changes $y_2$ so that the shares XOR to $y$; this passes only when the challenge is 0, the one case in which player 2 stays closed. The code is for study only and is not constant time. For real signatures use ML-DSA ([CRYSTALS-Dilithium](/crystals-dilithium/)) or SLH-DSA ([SPHINCS+](/sphincs-plus/)) from a FIPS 140 validated module.

## Correctness

If the signer is honest, the three output shares XOR to $E_k(p) = y$, by the AND gate identity above and because XOR gates act on each share. The verifier recomputes view $e$ exactly, because it depends only on the seeds and shares of players $e$ and $e + 1$ and on the AND outputs of player $e + 1$, which are in the proof. The recomputed $y_{e+2}$ equals the true one, the recomputed commitments equal the committed ones, and so the hash gives the same challenges. Soundness and zero knowledge are the other two properties of the proof; the [full proof](proofs/correctness.md) states them and proves completeness.

## Complexity

Signing runs the three players $t$ times over the circuit: $\Theta(t g)$ bit operations, plus hashing of the views, which is $\Theta(t a)$. Verification costs about two thirds of that. The signature holds, per repetition, two seeds, one commitment, the AND outputs of one player and sometimes the share $k_2$: $\Theta(t a)$ bits, with a constant of one bit per AND gate. For Picnic-L1-FS this gave signatures of up to 34,032 bytes, with a measured average of about 32,900 bytes; Picnic3-L1 cut this to about 12,600 bytes. Signing and verification take a few milliseconds.

## Properties

- **Minimal assumptions.** Security rests on the one-wayness of the cipher and on the hash, modeled as a random oracle. No algebraic structure is used.
- **Small keys, large signatures.** Keys are 32 and 16 bytes at category 1, but signatures are tens of kilobytes.
- **Soundness $2/3$ per repetition.** A cheater who knows the challenge in advance can make two views agree, so each repetition catches a cheater with probability only $1/3$, and $t$ grows with the security level.
- **Randomized.** Every signature uses fresh seeds.
- **Parallel.** The $t$ repetitions are independent.

## Variants and improvements

- **Picnic-UR.** Uses Unruh's transform in place of Fiat-Shamir, which gave a proof in the [quantum random oracle model](/quantum-random-oracle-model/) at the cost of larger signatures. Later QROM proofs for Fiat-Shamir made it less needed.
- **Picnic2 and Picnic3 (KKW).** Katz, Kolesnikov and Wang (CCS 2018) used many players with a preprocessing phase: the prover runs $M$ executions, opens the preprocessing of most of them, and runs the online phase for $\tau$ of them with $N$ players, of which $N - 1$ are opened. Picnic3-L1 uses $N = 16$, $M = 252$ and $\tau = 36$, with LowMC on 129 bits, 43 S-boxes and 4 rounds. Its signatures are about 12.6 KB.
- **Other ciphers.** BBQ, Banquet, Limbo and Helium prove knowledge of AES keys, so that no new cipher is needed.
- **Successors in the NIST additional signatures.** The method spread to other hard problems: SDitH (syndrome decoding), Mirath (MinRank, the merger of MIRA and MiRitH), PERK (permuted kernel), RYDE (rank syndrome decoding) and MQOM (multivariate quadratic equations), and to VOLE-in-the-head in FAEST (AES). The 14 schemes of round 2 (NIST IR 8528, 24 October 2024) were CROSS, FAEST, HAWK, LESS, MAYO, Mirath, MQOM, PERK, QR-UOV, RYDE, SDitH, SNOVA, SQIsign and UOV. The 9 schemes of round 3 (NIST IR 8610, 14 May 2026) are FAEST, HAWK, MAYO, MQOM, QR-UOV, SDitH, SNOVA, SQIsign and UOV ([UOV](/unbalanced-oil-and-vinegar/)), so FAEST, MQOM and SDitH carry the in-the-head line.

## When to use it

Picnic itself has no current use: it was not standardized, and its successors are smaller and faster. The method is the thing to learn. Use an in-the-head scheme when you want a signature whose only assumption is a cipher or a well-studied hard problem, and you can accept signatures of several kilobytes. For general use, the NIST standards ML-DSA and SLH-DSA are the choice.

## Pitfalls

- **Soundness with Fiat-Shamir.** An attacker can grind the hash, so the number of repetitions must give the full security level for the non-interactive proof, not just for one interactive run. For proofs with two challenge phases, such as KKW, Kales and Zaverucha (2020) showed that an attacker can split the grinding work between the phases, and parameters must count this.
- **A young cipher.** LowMC was designed for few AND gates, and its cryptanalysis was still moving during the NIST process, with new attacks on LowMC instances given only one or a few known plaintexts, which is the setting of Picnic. A scheme that uses AES avoids this risk at the cost of more AND gates.
- **Side channels.** Signing works on shares of the key, but the share $k_2$ and the cipher state are computed from the key, so an implementation still needs masking against power analysis.
- **Seeds must be fresh.** Reusing seeds across two signatures with different challenges opens all three views of a repetition, which reveals the key.

## Implementations

## History

Ishai, Kushilevitz, Ostrovsky and Sahai introduced MPC-in-the-head at STOC 2007. Giacomelli, Madsen and Orlandi made it practical with ZKBoo at USENIX Security 2016. Chase, Derler, Goldfeder, Orlandi, Ramacher, Rechberger, Slamanig and Zaverucha presented ZKB++ and the Picnic signature at CCS 2017 and submitted Picnic to the NIST process in November 2017. Katz, Kolesnikov and Wang gave the KKW proof at CCS 2018, which became Picnic2 and then Picnic3. Picnic was an alternate signature in round 3 (July 2020). In July 2022 NIST selected CRYSTALS-Dilithium, Falcon and SPHINCS+, and Picnic was not selected; SPHINCS+ became the standard signature that does not rest on lattices. NIST then opened a call for additional signatures, in which the in-the-head method returned in several schemes.

## References
