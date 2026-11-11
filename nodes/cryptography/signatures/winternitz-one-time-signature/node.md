---
tag: 39CCX3
kind: algorithm
slug: winternitz-one-time-signature
name: Winternitz one-time signature
aliases:
- WOTS
- WOTS+
- Winternitz OTS
- W-OTS
- Winternitz signature
area: cryptography/signatures
level: advanced
summary: "One-time signature that signs several digest bits per hash chain. A checksum stops forward walks. WOTS+ adds bitmasks so that second preimage resistance is enough."
model: word-ram
complexity:
  vars: {l: the number of chains, w: the chain length}
  time: {worst: Θ(l·w), average: Θ(l·w), best: Θ(l·w)}
  space: {extra: Θ(l)}
properties: {deterministic: true}
history:
  year: 1989
  people: [Ralph Merkle, Robert Winternitz, Andreas Hülsing]
  note: Merkle published the method in A certified digital signature (CRYPTO 1989) and credits it to Winternitz. Hülsing gave WOTS+ at AFRICACRYPT 2013.
prereqs: [lamport-signature, hash-chain]
see_also: [merkle-signature-scheme, leighton-micali-signature, xmss, sphincs-plus, hash-based-signatures, second-preimage-resistance, one-way-function, existential-unforgeability]
sources:
  - paper: "Ralph C. Merkle, A certified digital signature, CRYPTO 1989, LNCS 435, Springer, 1990, pages 218 to 238"
    locator: the improvement of one-time signatures that signs several bits with repeated hashing, credited to Winternitz
  - paper: doi:10.1007/978-3-642-38553-7_10
    title: "Andreas Hülsing, W-OTS+: Shorter signatures for hash-based signature schemes, AFRICACRYPT 2013, LNCS 7918, pages 173 to 188"
    locator: the chaining function with bitmasks, the parameters len1 and len2, and Theorem 1 (EU-CMA from one-wayness, second preimage resistance and undetectability)
  - url: "https://arxiv.org/abs/2002.07419"
    title: "Mikhail A. Kudinov, Evgeniy O. Kiktenko and Aleksey K. Fedorov, Security analysis of the W-OTS+ signature scheme: Updating security bounds, 2020"
    locator: Theorem 1 (the corrected bound) and Section 3.2 (the flaw in the original proof)
  - paper: "Johannes Buchmann, Erik Dahmen, Sarah Ereth, Andreas Hülsing and Markus Rückert, On the security of the Winternitz one-time signature scheme, AFRICACRYPT 2011, LNCS 6737"
    locator: the proof of classic WOTS from a pseudorandom function family (W-OTS with a PRF)
  - url: "https://www.rfc-editor.org/rfc/rfc8391"
    title: "RFC 8391, XMSS: eXtended Merkle Signature Scheme, 2018"
    locator: Section 3.1 (WOTS+ one-time signatures, the parameter w, base_w and the checksum)
  - url: "https://www.rfc-editor.org/rfc/rfc8554"
    title: "RFC 8554, Leighton-Micali Hash-Based Signatures, 2019"
    locator: Section 4 (LM-OTS, where w is the number of bits per digit)
  - book: isbn:9783540887010
    title: Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009
    locator: chapter Hash-based Digital Signature Schemes by Johannes Buchmann, Erik Dahmen and Michael Szydlo, section on the Winternitz one-time signature scheme
---

The Winternitz one-time signature (WOTS) is a [hash-based](/hash-based-signatures/) one-time signature that signs several bits of the message digest with one secret value. It cuts the signature of the [Lamport scheme](/lamport-signature/) by a factor of about $\lg w$, and pays with more hashing. Each secret value starts a [hash chain](/hash-chain/) of length $w$, the public key is the end of each chain, and the signature for a digit $b$ is the value $b$ steps up the chain. A checksum, signed in the same way, stops a forger from walking chains forward. WOTS+ adds a random bitmask to each step, so that the proof needs only second preimage resistance of the hash. WOTS+ is the one-time signature inside [XMSS](/xmss/) and SLH-DSA ([SPHINCS+](/sphincs-plus/)), and the close relative LM-OTS is inside [LMS](/leighton-micali-signature/).

**Notation.** $w$ is the chain length, a power of 2 (4 or 16 in RFC 8391, 16 in FIPS 205), and each digit has $\lg w$ bits. The message digest has $8m$ bits, so it has $\ell_1 = \lceil 8m / \lg w \rceil$ digits. The checksum $C = \sum_{i=1}^{\ell_1} (w - 1 - d_i)$ has $\ell_2 = \lfloor \lg(\ell_1 (w-1)) / \lg w \rfloor + 1$ digits, and $\ell = \ell_1 + \ell_2$ is the number of chains. $c^j(x)$ is the value after $j$ chain steps from $x$. $n$ is the byte length of chain values. The security notion is one-time existential unforgeability under chosen message attack (EUF-1-CMA), in the standard model. LMS (RFC 8554) uses $w$ for the number of bits per digit instead, so its $w = 4$ is chain length 16 here.

## In plain words

Lamport's scheme spends one secret on each bit of the digest. Winternitz spends one secret on a group of bits, say 4 bits, which is a number from 0 to 15.

For each group, take a secret and hash it 15 times in a row. The last hash goes into the public key. To sign the number 6, show the value after 6 hashes. The verifier hashes it 9 more times and checks that the result is the public value.

There is a weakness. Anyone can hash a shown value further, so a forger can turn a 6 into a 7. To stop this, the signer also signs a checksum: the sum of how far each number is from 15. If a forger raises a number, the checksum must go down, and going down needs a value before the shown one, which nobody but the signer has.

## The problem

The scheme is a one-time [signature scheme](/signature-scheme/): one key pair signs one message, and no efficient adversary that sees one signature on a message of its choice can sign another message. It needs only a hash function. Compared with the Lamport scheme, the goal is a shorter signature and public key for the same security, at the cost of more hash calls. Like the Lamport scheme, it does not sign many messages; a [Merkle signature scheme](/merkle-signature-scheme/) puts many WOTS keys under one root.

## The algorithm

```pseudo id=main
DIGITS(M)
L1  d ← the ℓ1 base-w digits of the digest of M          ▷ most significant first
L2  e ← the ℓ2 base-w digits of C = Σ (w − 1 − d[i])
L3  return b = d ‖ e                                       ▷ ℓ digits

CHAIN(x, a, s)                                             ▷ steps a+1 .. a+s
L4  for j ← a + 1 to a + s do x ← F_k(x ⊕ r[j])           ▷ classic WOTS: x ← H(x)
L5  return x

KEYGEN()
L6  for i ← 1 to ℓ: sk[i] ← random value of n bytes
L7  k ← random key; r[1..w−1] ← random bitmasks           ▷ WOTS+ only
L8  for i ← 1 to ℓ: pk[i] ← CHAIN(sk[i], 0, w − 1)
L9  return sk, (pk, k, r)

SIGN(sk, M)
L10 b ← DIGITS(M)
L11 return σ = (CHAIN(sk[i], 0, b[i]) for i ← 1 to ℓ)

VERIFY(pk, M, σ)
L12 b ← DIGITS(M)
L13 return CHAIN(σ[i], b[i], w − 1 − b[i]) = pk[i] for every i
```

Lines L1 to L3 split the digest into digits and append the checksum digits. The checksum is the total distance of the message digits from the top of their chains, so it is large when the digits are small. Line L4 is one chain step: classic WOTS hashes the value, and WOTS+ XORs the bitmask of the step and then applies the keyed function $F_k$. Key generation walks every chain to its end. Signing stops each chain at its digit, and verification finishes each walk and compares the end with the public key.

In WOTS+ the public key holds $k$ and the $w - 1$ bitmasks as in the 2013 paper. XMSS and SLH-DSA instead derive them, and the secret values, from short seeds with a pseudorandom function and an address of the chain, so that keys are a few seeds. The code keeps the 2013 form, with $F_k(x) = $ SHA-256$(0 \| k \| x)$.

## Example

Take a toy digest of $m = 1$ byte and $w = 4$, so each digit has 2 bits, $\ell_1 = 4$, the largest checksum is $4 \cdot 3 = 12$, $\ell_2 = 2$, and $\ell = 6$ chains. The digest of "hi" is the first byte of SHA-256, `8f` = `10 00 11 11`.

| chain $i$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| digit $b_i$ | 2 | 0 | 3 | 3 | 1 | 0 |
| signature value | $c^2(x_1)$ | $x_2$ | $c^3(x_3)$ | $c^3(x_4)$ | $c^1(x_5)$ | $x_6$ |
| verifier steps | 1 | 3 | 0 | 0 | 2 | 3 |

The checksum is $C = (3 - 2) + (3 - 0) + 0 + 0 = 4$, which is `10` in base 4, so the last two digits are 1 and 0. The verifier walks each value up by $3 - b_i$ steps and compares it with $pk_i = c^3(x_i)$.

A forger wants to raise digit 2 from 0 to 1. Without the checksum this is easy: it hashes $x_2$ once. With the checksum, the new checksum is 3 = `03` in base 4, and chain 5 would need $c^0(x_5)$, one step below the shown value $c^1(x_5)$. That is a preimage, so the forgery fails.

## Correctness

**Correctness.** Chain steps compose: walking $s$ steps from position $a$ and then $t$ more is the same as walking $s + t$ steps from position $a$. The signature value is $c^{b_i}(sk_i)$, and the verifier walks it $w - 1 - b_i$ more steps to $c^{w-1}(sk_i) = pk_i$.

**The checksum lemma.** If $b \ne b'$ are the digit strings (with checksums) of two digests, then $b'_i < b_i$ for some $i$. If every message digit of $b'$ is at least the one of $b$, and one is larger, the checksum of $b'$ is smaller, and two numbers written with the same number of base $w$ digits differ first at a digit where the smaller number has the smaller digit. So a forgery for a new digest must reveal a value below a shown value, on some chain.

**Security.** For WOTS+, Hülsing (2013) bounds the forging chance by terms in the one-wayness, the second preimage resistance and the undetectability of the keyed function family. At the chain where the forgery goes below the shown value, either the forger found the honest chain value (it inverted a step) or its walk meets the honest walk at some step with a different input (it found a second preimage). The bitmask lets the reduction put a second preimage challenge $x_c$ at a chosen step, by setting $r_j = c^{j-1}(sk_i) \oplus x_c$, and this bitmask is still uniform. Kudinov, Kiktenko and Fedorov (2020) found a flaw in the original analysis and proved a corrected bound of the same kind. The full lemmas and the proof idea are below.

### Why the checksum is needed

Without the checksum, a forger who sees one signature can sign every message whose digits are all at least the signed digits. For $w = 16$ and random digits, one digit of a random message is at least the signed one with chance $17/32$, so a random message is forgeable with chance $(17/32)^{64} \approx 2^{-58.4}$ for a 256-bit digest. This is already far too high, and the signer may also be tricked into signing a message with small digits, which makes almost every message forgeable. The test file finds a forgery on a toy digest of 16 bits ($w = 16$, four digits):

```python
sig = sign(p, sk, pk, m1)
msg1 = digits(p, m1)[: p.len1]
for i in range(1 << 16):                 # a message with larger digits
    cand = b"pay Eve %d" % i
    b2 = digits(p, cand)
    if b2[: p.len1] != msg1 and all(x >= y for x, y in zip(b2, msg1)):
        break
forged = [chain(p, pk, sig[j], msg1[j], b2[j] - msg1[j]) for j in range(p.len1)]
```

The forged message chains verify, and the test checks that some checksum digit of the new message is lower than the signed one. A second test counts all $2^{16}$ digests: 7487 of them are forgeable from the signed digits $(3, 0, 12, 7)$ without the checksum, and none with it.

## Complexity

Count calls of the chain function. Key generation walks every chain to the end, $\ell(w-1)$ calls. Signing walks chain $i$ to $b_i$ and verification walks the rest, so signing plus verification is also exactly $\ell(w-1)$ calls; on average each takes half. All operations are $\Theta(\ell w)$, and $\ell \approx 8m / \lg w$. The values for $n = m = 32$ bytes:

| $w$ | $\ell_1$ | $\ell_2$ | $\ell$ | signature (bytes) | key generation calls | signing calls (average) |
|---|---|---|---|---|---|---|
| 4 | 128 | 5 | 133 | 4256 | 399 | 200 |
| 16 | 64 | 3 | 67 | 2144 | 1005 | 503 |
| 256 | 32 | 2 | 34 | 1088 | 8670 | 4335 |

The Lamport scheme with the same digest needs 8192 bytes. Each doubling of $\lg w$ about halves the signature and about squares the number of steps per chain, so $w = 16$ is the usual choice. The public key is $\ell$ values, or one hash of them in practice (an L-tree in XMSS, a single hash in LMS and SLH-DSA). WOTS+ adds the key and $w - 1$ bitmasks to the public key, or one seed when they are derived.

## Properties

- **One-time.** One key signs one message. A second signature on other digits reveals lower chain values on some chains, and the checksum argument fails.
- **The public key can be recomputed from a signature.** Verification computes candidate chain ends from the signature. Merkle trees use this: the verifier rebuilds the leaf and checks it against the root, so the public key need not be sent.
- **Deterministic.** The signature depends only on the key and the message.
- **Tunable.** $w$ trades signature size against hash work.
- **Assumption.** WOTS+ needs only second preimage resistance, one-wayness and undetectability of the function family, with no collision resistance. So a function with $n = \lambda$ bytes of output is enough for $\lambda$ bytes of security, which halves the signature compared with a proof that needs collision resistance.

## Variants and improvements

- **Classic WOTS (Merkle 1989).** Plain hash chains with no bitmask. Proofs need collision resistance of the hash or a random oracle, so values must be twice as long.
- **WOTS with a PRF (Buchmann, Dahmen, Ereth, Hülsing, Rückert 2011).** A chain step is a pseudorandom function keyed by the previous value; the proof needs a pseudorandom function family.
- **WOTS+ (Hülsing 2013).** The bitmask form of this page, used in XMSS (RFC 8391) and SLH-DSA (FIPS 205), where the bitmasks and keys come from a public seed and a hash address. Multi-target attacks across many chains are stopped by the address and seed in each call (WOTS-T, Hülsing, Rijneveld and Song, PKC 2016).
- **LM-OTS (RFC 8554).** Each step hashes the key identifier $I$, the leaf number $q$, the chain number and the step number with the value. The checksum is shifted left so that it fills whole digits. Its $w$ is the number of bits per digit: 1, 2, 4 or 8.
- **Constant-sum encodings.** Encodings where all digit strings have the same sum (WOTS with constant sum, and the checksum-free WOTS+C of SPHINCS+C) remove the checksum chains at the cost of a search during signing.

## When to use it

Use WOTS as the leaf signature of a many-time hash-based scheme: [MSS](/merkle-signature-scheme/), LMS, XMSS or SLH-DSA. Pick $w = 16$ unless the signature size or the signing time is critical. Do not build a scheme from it by hand for real data. Use LMS or XMSS (NIST SP 800-208) or SLH-DSA (FIPS 205), which fix the encodings and the domain separation.

## Pitfalls

- **No checksum, or a short checksum.** The forward walk forgery of the example. The checksum must have enough digits to hold $\ell_1(w-1)$.
- **Two messages with one key.** The two signatures together reveal the lower of the two values on each chain, so a forger can sign each message whose digits are all at least the minimum of the two.
- **Chain steps with no domain separation.** If every chain, step and key uses the same function, values can repeat across chains and keys, and an attacker gets many targets at once. Standards hash an address (key, leaf, chain, step) into each call.
- **Off by one in the chain length.** A chain has $w$ positions $0, \ldots, w-1$ and $w - 1$ steps. Mixing up the RFC 8391 meaning of $w$ (chain length) with the RFC 8554 meaning (bits per digit) gives wrong parameters.
- **Base $w$ with the wrong bit order.** The digits must be read most significant first, as the standards do, or the code will not match test vectors.

## Implementations

The Python code is for study only. It is not constant time, and it must not protect real data. It has classic WOTS and WOTS+ behind one flag, and takes SHA-256 from `hashlib` because the page is about the signature. WOTS+ as a stand-alone scheme has no official test vectors (RFC 8391 and FIPS 205 test it only inside XMSS and SLH-DSA), so the tests check the parameters, the round trip, the rejection of changes, and the checksum on a toy digest of 16 bits.

## History

Ralph Merkle described the method in "A certified digital signature", published at CRYPTO 1989, and credits it to Robert Winternitz of Stanford. Buchmann, Dahmen, Ereth, Hülsing and Rückert (2011) gave a security proof for a form with a pseudorandom function family. Andreas Hülsing introduced WOTS+ at AFRICACRYPT 2013, with a proof from second preimage resistance that allowed shorter values. RFC 8391 (2018) standardized WOTS+ inside XMSS, RFC 8554 (2019) standardized LM-OTS, and FIPS 205 (2024) uses WOTS+ inside SLH-DSA. In 2020 Kudinov, Kiktenko and Fedorov corrected the security bound of WOTS+.

## References
