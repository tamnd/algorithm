---
tag: NY3QP4
kind: concept
slug: verifiable-random-function
name: Verifiable random function
aliases:
- VRF
- ECVRF
area: cryptography/protocols
level: research
summary: A keyed function whose output looks random to anyone without the secret key, and comes with a proof that anyone can check against the public key. Micali, Rabin and Vadhan 1999; ECVRF in RFC 9381.
prereqs: [pseudorandom-function, digital-signature, decisional-diffie-hellman]
see_also: [ed25519, random-oracle-model, schnorr-signature, sigma-protocol, zero-knowledge-proof, bls-signature, threshold-cryptography, proof-of-stake]
sources:
  - paper: doi:10.1109/SFFCS.1999.814584
    title: Silvio Micali, Michael O. Rabin and Salil P. Vadhan, Verifiable random functions, 40th IEEE Symposium on Foundations of Computer Science (FOCS 1999), pages 120 to 130
    locator: the definition (provability, uniqueness, pseudorandomness) and the first construction, from an RSA-type assumption
  - url: "https://www.rfc-editor.org/rfc/rfc9381"
    title: Sharon Goldberg, Leonid Reyzin, Dimitrios Papadopoulos and Jan Včelák, RFC 9381, Verifiable Random Functions (VRFs), August 2023
    locator: Section 3 (security properties), Section 5 (ECVRF), Section 5.4.1.1 (try and increment), Section 5.5 (ciphersuites), Section 7 (security considerations), Appendix B.3 (test vectors, used by the code)
  - url: "https://eprint.iacr.org/2017/099"
    title: Dimitrios Papadopoulos, Duane Wessels, Shumon Huque, Moni Naor, Jan Včelák, Leonid Reyzin and Sharon Goldberg, Making NSEC5 practical for DNSSEC, Cryptology ePrint Archive 2017/099
    locator: the security proofs of the ECVRF in the random oracle model under DDH
  - paper: doi:10.1145/3132747.3132757
    title: Yossi Gilad, Rotem Hemo, Silvio Micali, Georgios Vlachos and Nickolai Zeldovich, Algorand, scaling Byzantine agreements for cryptocurrencies, SOSP 2017, pages 51 to 68
    locator: cryptographic sortition with a VRF (Section 5)
  - paper: "Sharon Goldberg, Moni Naor, Dimitrios Papadopoulos, Leonid Reyzin, Sachin Vasant and Asaf Ziv, NSEC5, provably preventing DNSSEC zone enumeration, NDSS 2015"
    locator: the use of a VRF to give authenticated denial of existence without zone enumeration
  - paper: "Yevgeniy Dodis and Aleksandr Yampolskiy, A verifiable random function with short proofs and keys, PKC 2005, LNCS 3386, pages 416 to 431"
    locator: a VRF in bilinear groups under the q-DBDHI assumption
  - url: "https://www.rfc-editor.org/rfc/rfc8032"
    title: Simon Josefsson and Ilari Liusvaara, RFC 8032, Edwards-Curve Digital Signature Algorithm (EdDSA), January 2017
    locator: Section 5.1.3 (point decoding), Section 5.1.4 (point addition), Section 5.1.5 (key generation), Section 7.1 (the secret keys reused by RFC 9381)
---

A verifiable random function (VRF) is a keyed function $F_{sk}$ with a public key $pk$ and a proof: on input $\alpha$, the holder of $sk$ computes an output $\beta = F_{sk}(\alpha)$ and a proof $\pi$, and anyone with $pk$ can check that $\beta$ is the correct output. To anyone who has not seen a proof for $\alpha$, $\beta$ looks random, as the output of a [pseudorandom function](/pseudorandom-function/) does. Unlike a [digital signature](/digital-signature/), a VRF has exactly one valid output for each input and key, so the key holder cannot choose among outputs. Micali, Rabin and Vadhan defined VRFs in 1999, and RFC 9381 (2023) standardizes the ECVRF, which this page implements on edwards25519.

**Notation.** $\lambda$ is the security parameter. $G$ is a group of prime order $q$ with generator $B$, written additively; for edwards25519 the full curve group has order $8q$, and $8$ is the cofactor. $\mathrm{Hash}$ is SHA-512. An adversary is $A$, and $\mathrm{Adv}$ is its advantage in a named game. Points are encoded to 32 bytes as in RFC 8032.

## In plain words

A lottery machine is run by one person. The players want two things. The numbers must be impossible to guess in advance. And the person who runs the machine must not be able to pick a number that suits them.

A verifiable random function gives both. The owner of a secret key feeds a ticket name into the function and gets a number that looks random to everyone else. With the number comes a short proof. Anyone who has the owner's public key can check the proof, and so can check that the number is the only one that the key allows for that ticket. The owner cannot make a second number that also passes the check, so they cannot cheat by trying many numbers and showing the best one.

## The idea

### The definition

A VRF is three algorithms. $\mathrm{Gen}(1^\lambda)$ outputs $(pk, sk)$. $\mathrm{Prove}(sk, \alpha)$ outputs a proof $\pi$, and the output is $\beta = \mathrm{ProofToHash}(\pi)$. $\mathrm{Verify}(pk, \alpha, \pi)$ outputs $\beta$ or INVALID. Micali, Rabin and Vadhan ask for three properties.

- **Provability.** For each $(pk, sk)$ from $\mathrm{Gen}$ and each $\alpha$, $\mathrm{Verify}(pk, \alpha, \mathrm{Prove}(sk, \alpha)) = F_{sk}(\alpha)$.
- **Uniqueness.** There are no $pk, \alpha, \pi_1, \pi_2$ such that $\mathrm{Verify}(pk, \alpha, \pi_1) = \beta_1$, $\mathrm{Verify}(pk, \alpha, \pi_2) = \beta_2$, both valid, and $\beta_1 \ne \beta_2$. RFC 9381 calls the computational form, where no efficient $A$ can find such values even for a $pk$ that $A$ chooses, *full uniqueness*. *Trusted uniqueness* asks this only for keys made by $\mathrm{Gen}$.
- **Pseudorandomness.** In the game, $A$ gets $pk$ and an oracle for $\mathrm{Prove}(sk, \cdot)$. It outputs a fresh input $\alpha^*$, gets either $F_{sk}(\alpha^*)$ or a random string of the same length, can make more queries other than $\alpha^*$, and guesses which one it got. $\mathrm{Adv}$ is $|\Pr[\text{guess correct}] - 1/2|$. *Selective* pseudorandomness makes $A$ name $\alpha^*$ before it sees $pk$.

Uniqueness is the property that a signature does not give. A randomized signature scheme has many valid signatures per message, so a hash of the signature is not a VRF output: the signer could sign many times and keep the signature whose hash it likes. A unique signature scheme, such as RSA full domain hash, gives a VRF by hashing the signature; RFC 9381 Section 4 defines RSA-FDH-VRF in this way.

### The ECVRF

The ECVRF of RFC 9381 Section 5 is a Diffie-Hellman value with a proof that it is correct. The secret key gives a scalar $x$ and $pk$ encodes $Y = xB$.

1. $H = \mathrm{EncodeToCurve}(pk, \alpha)$, a point in $G$ that depends only on the public key and the input.
2. $\Gamma = xH$. This is the VRF value. The output is $\beta = \mathrm{Hash}(\texttt{0x03} \,\|\, \texttt{0x03} \,\|\, \mathrm{enc}(8\Gamma) \,\|\, \texttt{0x00})$, where the first byte is the suite string.
3. A nonce $k$ is derived from $sk$ and $H$, as in [Ed25519](/ed25519/).
4. $c = \mathrm{Challenge}(Y, H, \Gamma, kB, kH)$, the first 16 bytes of a hash of the five points.
5. $s = (k + c x) \bmod q$, and $\pi = \mathrm{enc}(\Gamma) \,\|\, c \,\|\, s$, which is $32 + 16 + 32 = 80$ bytes.

Steps 3 to 5 are a non-interactive proof, with the Fiat-Shamir method, that $\log_B Y = \log_H \Gamma$. This is the Chaum-Pedersen equality of discrete logarithms, a [sigma protocol](/sigma-protocol/). The verifier recomputes $H$, then $U = sB - cY$ and $V = sH - c\Gamma$, and accepts when $\mathrm{Challenge}(Y, H, \Gamma, U, V) = c$. For an honest proof, $U = kB$ and $V = kH$, so the check passes.

**Why the output is unique.** Suppose that $(\Gamma, c, s)$ verifies and $\Gamma \ne xH$ in the prime order part. Then the proof shows an equality of discrete logarithms that is false, and the special soundness of the Chaum-Pedersen protocol bounds the chance of this by about $2^{-128}$ per hash query, since $c$ has 128 bits. RFC 9381 Section 7.2 gives the uniqueness level as about $8 \min(q_{len}, c_{len}) = 128$ bits. The output hashes $8\Gamma$, not $\Gamma$, so a change of $\Gamma$ by a point of small order does not change $\beta$.

**Why the output looks random.** Without $x$, the pair $(H, xH)$ for a fresh $H$ looks like a random pair, by the [decisional Diffie-Hellman](/decisional-diffie-hellman/) assumption, and the proof is simulated in the [random oracle model](/random-oracle-model/). Papadopoulos et al. prove full and selective pseudorandomness in the random oracle model for $\mathrm{Hash}$ and $\mathrm{EncodeToCurve}$. The reduction is tighter for selective pseudorandomness (RFC 9381 Section 7.3).

### Key validation

An honest $Y$ has order $q$. A cheating key holder can publish a $Y$ of small order (orders 1, 2, 4 or 8 on edwards25519). With $\mathrm{validate\_key}$ set, the verifier rejects a $Y$ with $8Y = 0$. RFC 9381 Section 5 states that the ECVRF has full uniqueness in any case, and gets full collision resistance and unpredictability under malicious key generation only when the verifier validates the key.

### Try and increment

The suite ECVRF-EDWARDS25519-SHA512-TAI maps $\alpha$ to a point by hashing $\texttt{0x03} \,\|\, \texttt{0x01} \,\|\, pk \,\|\, \alpha \,\|\, ctr \,\|\, \texttt{0x00}$ for $ctr = 0, 1, 2, \ldots$, until the first 32 bytes of the hash decode to a curve point, and then multiplies the point by the cofactor 8. About half of the 32-byte strings decode, so the expected number of tries is about 2. The running time depends on $\alpha$, so RFC 9381 Section 5.4.1.1 says that this suite should be avoided when $\alpha$ must stay secret. The suite ECVRF-EDWARDS25519-SHA512-ELL2 uses the Elligator 2 map of RFC 9380 and has no such leak.

### Cost

Proving costs 4 scalar multiplications ($xB$ once per key, $xH$, $kB$, $kH$) and about 2 SHA-512 calls for the encode step on average, plus 2 more for the nonce and the challenge. Verifying costs 4 scalar multiplications ($sB$, $cY$, $sH$, $c\Gamma$) and one more by the cofactor, the same hash calls, and no secret. A proof is 80 bytes and an output is 64 bytes.

## Examples

**The RFC vectors.** RFC 9381 Appendix B.3, Example 16, uses the Ed25519 key of RFC 8032 TEST 1, with $pk$ = `d75a9801...f707511a` and the empty input. Try and increment succeeds at $ctr = 0$, and the proof begins with $\mathrm{enc}(\Gamma)$ = `86571066...f26f723f`. In Example 17, with input `72`, the first hash does not decode, and try and increment succeeds at $ctr = 1$. The code below reproduces the secret scalar $x$, $H$, $k$, $U = kB$, $V = kH$, $\pi$ and $\beta$ of Examples 16, 17 and 18 exactly.

**How many tries.** For the key of Example 16 and the 400 inputs of two bytes $0, 1, \ldots, 399$, try and increment stopped at $ctr = 0$ for 178 inputs, at $ctr = 1$ for 104 and at $ctr = 2$ for 63, with a largest value of 9. The counts fall by about a half at each step, as the one half chance of a decode predicts.

**A lottery with a VRF.** Read the 64-byte $\beta$ as a fraction $\beta / 2^{512}$. The outputs of Examples 16, 17 and 18 give 0.566, 0.919 and 0.392. With a rule "selected when the fraction is below 0.5", only the key of Example 18 is selected for its input, and anyone who has the three proofs can check this. This is the idea of the cryptographic sortition of Algorand.

**A non-example.** Take an [ECDSA](/ecdsa/) signature $\sigma$ on $\alpha$ and set $\beta = \mathrm{SHA\text{-}512}(\sigma)$. The verifier can check $\sigma$, and $\beta$ is unpredictable to others. But the signer can make as many valid signatures as it wants, with new nonces, and publish the one with the smallest $\beta$. Uniqueness fails, so this is not a VRF. A deterministic nonce (RFC 6979) does not help, because the verifier cannot check that the signer used it.

**The code.** The Python code implements ECVRF-EDWARDS25519-SHA512-TAI with its own edwards25519 arithmetic, after RFC 8032 Sections 5.1.3 and 5.1.4. The tests check the three vectors of RFC 9381 Appendix B.3, copied by hand, with all their intermediate values. They also check that a changed input, key or proof byte fails, that a non-reduced $s$ fails, and that a key of order 2 fails when the key is validated. The code is for study only. It is not constant time: the scalar multiplication branches on the secret bits and try and increment leaks the number of tries. It must not protect real data. Use a maintained implementation, for example the reference code of the RFC authors or a library that implements RFC 9381.

## Where it is used

- **Leader and committee election.** Algorand uses a VRF for cryptographic sortition: each user evaluates the VRF on a public seed and role, and is selected with a chance that is proportional to its stake. Other [proof of stake](/proof-of-stake/) chains elect block producers in a similar way. This replaces the random choice of a trusted dealer in [Byzantine agreement](/byzantine-fault-tolerance/) protocols.
- **DNSSEC without zone walking.** NSEC5 lets a name server prove that a name does not exist without the signed chain of NSEC records that lets anyone list the whole zone. The server answers with the VRF output of the queried name and the neighbouring outputs, which only the key holder can compute.
- **Key transparency.** CONIKS and similar directories place each user name at the VRF output of the name in a Merkle tree, so that a proof for one user does not show the names of the others (see [secure messaging](/secure-messaging/)).
- **Randomness beacons and lotteries.** A key holder whose key is fixed in advance can publish VRF outputs on round numbers as a public random source. A [threshold](/threshold-cryptography/) version, such as one based on [BLS signatures](/bls-signature/), which are unique, removes the single key holder.
- **Relation to other pages.** A VRF is a [pseudorandom function](/pseudorandom-function/) with proofs. It is a unique [digital signature](/digital-signature/) that is also pseudorandom. Its proof is a [zero-knowledge](/zero-knowledge-proof/) style proof of equal discrete logarithms in the [random oracle model](/random-oracle-model/).

## References
