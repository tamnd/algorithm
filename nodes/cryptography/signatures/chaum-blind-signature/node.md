---
tag: BFYHY3
kind: algorithm
slug: chaum-blind-signature
name: Chaum's blind signature
aliases:
- RSA blind signature
- RSABSSA
- Blind RSA
area: cryptography/signatures
level: advanced
summary: "RSA-based blind signature: the client multiplies its encoded message by r^e, the signer applies d, and the client divides by r. RFC 9474 specifies it with PSS."
model: word-ram
complexity:
  vars: {k: the length of the modulus n in machine words}
  time: {worst: Θ(k^3), average: Θ(k^3), best: Θ(k^3)}
  space: {extra: Θ(k)}
properties: {deterministic: false, randomized: true}
history:
  year: 1982
  people: [David Chaum]
  note: Chaum presented blind signatures at Crypto 1982 for untraceable payments. RFC 9474 (October 2023) specifies the RSA scheme with PSS encoding as RSABSSA.
prereqs: [blind-signature, rsa-signature]
see_also: [rsa-blinding, rsa-pss, rsa-fdh, rsa-problem, random-oracle-model, bls-signature, digital-signature]
sources:
  - paper: doi:10.1007/978-1-4757-0602-4_18
    title: "David Chaum, Blind signatures for untraceable payments, Advances in Cryptology: Proceedings of Crypto 82, Plenum Press, 1983, pages 199 to 203"
    locator: the blind signature with the factor r^e, and the untraceable payment system built on it
  - url: "https://www.rfc-editor.org/rfc/rfc9474"
    title: "Frank Denis, Frederic Jacobs and Christopher A. Wood, RFC 9474, RSA Blind Signatures, October 2023"
    locator: Section 4 (Prepare, Blind, BlindSign, Finalize), Section 5 (the four named variants), Section 7 (security considerations) and Appendix A (test vectors)
  - paper: doi:10.1007/s00145-002-0120-1
    title: "Mihir Bellare, Chanathip Namprempre, David Pointcheval and Michael Semanko, The one-more-RSA-inversion problems and the security of Chaum's blind signature scheme, Journal of Cryptology 16(3), 2003, pages 185 to 215"
    locator: the one-more RSA inversion problems and the proof of one-more unforgeability of the FDH blind signature in the random oracle model
  - paper: doi:10.1007/978-3-031-31368-4_10
    title: "Anna Lysyanskaya, Security analysis of RSA-BSSA, PKC 2023"
    locator: one-more unforgeability of the RSABSSA variants and blindness of the randomized variants
  - url: "https://www.rfc-editor.org/rfc/rfc8017"
    title: "Kathleen Moriarty, Burt Kaliski, Jakob Jonsson and Andreas Rusch, RFC 8017, PKCS #1: RSA Cryptography Specifications Version 2.2, November 2016"
    locator: Section 8.1 (RSASSA-PSS), Section 9.1 (EMSA-PSS) and Appendix B.2.1 (MGF1)
  - url: "https://www.rfc-editor.org/rfc/rfc9578"
    title: "Sofía Celi, Alex Davidson, Steven Valdez and Christopher A. Wood, RFC 9578, Privacy Pass Issuance Protocols, June 2024"
    locator: Section 6 (publicly verifiable tokens with blind RSA, token type 0x0002)
---

Chaum's blind signature is the RSA construction of a [blind signature](/blind-signature/): a client gets an RSA signature on a message, and the signer never sees the message. The client multiplies the encoded message $m$ by $r^e$ for a random $r$, the signer raises the product to its private exponent $d$, and the client divides the answer by $r$. What remains is $m^d \bmod n$, an ordinary [RSA signature](/rsa-signature/) that anyone checks with the public key. The signer sees only a uniformly random number, so it cannot later link a signature to the session that made it. RFC 9474 (2023) specifies the scheme with [RSA-PSS](/rsa-pss/) encoding as RSABSSA, so that the output is a standard RSASSA-PSS signature.

## In plain words

You want a bank to sign a note, but you do not want the bank to know which note it signed. You put the note in an envelope lined with carbon paper. The bank signs the outside of the envelope, and the carbon copies the signature onto the note. You open the envelope and have a signed note that the bank never saw.

In RSA, the envelope is a random number. You multiply your note by a random value in a special form before you send it. The bank signs that product. Then you divide out your random value, and the bank's signature on the note itself remains. Each envelope looks like random noise to the bank, so it cannot tell later which note came from which visit.

## The problem

The signer has an RSA key $(n, e, d)$ and the client has a message $msg$. The client must end with a valid RSA signature on $msg$ (or on a randomized form of it), and the signer must learn nothing about $msg$ or about the final signature. The signer must also be sure that each session gives the client at most one signature. The general problem and its security notions are on the [blind signature](/blind-signature/) page; this page is about the RSA scheme.

## The algorithm

```pseudo id=main
PREPARE(msg)                                         ▷ client
L1  input_msg ← random(32) ‖ msg in the randomized variants, else msg

BLIND(pk = (n, e), input_msg)                        ▷ client
L2  EM ← EMSA-PSS-ENCODE(input_msg, |n| − 1) with a random salt; m ← OS2IP(EM)
L3  if gcd(m, n) ≠ 1 then fail
L4  r ← uniform unit in [1, n); inv ← r^(−1) mod n
L5  z ← m · r^e mod n; send z                         ▷ blinded_msg

BLINDSIGN(sk = (n, d), z)                            ▷ signer, sees only z
L6  s' ← z^d mod n
L7  if s'^e mod n ≠ z then fail; send s'             ▷ blind_sig

FINALIZE(pk, input_msg, s', inv)                     ▷ client
L8  s ← s' · inv mod n
L9  if RSASSA-PSS-VERIFY(pk, input_msg, s) fails then fail; output s

VERIFY(pk, input_msg, s)
L10 return RSASSA-PSS-VERIFY(pk, input_msg, s)
```

Chaum's paper has the same algebra: blind with $m' = m \cdot r^e$, sign $s' = (m')^d$, unblind $s = s' \cdot r^{-1}$. RFC 9474 adds the PSS encoding of line L2, the check of line L7 against fault attacks on the signer, the check of line L9 against a signer that answers wrongly, and the random prefix of line L1. The four named variants use SHA-384 and MGF1 with SHA-384 and differ in two choices: a 48-byte salt (PSS) or no salt (PSSZERO), and the randomized or the identity preparation.

## Example

A textbook key: $n = 61 \cdot 53 = 3233$, $e = 17$, $d = 413$ (the inverse of 17 modulo $\operatorname{lcm}(60, 52) = 780$). Take the encoded message $m = 65$ and the blinding factor $r = 5$.

| step | value |
|---|---|
| $r^e \bmod n$ | $5^{17} \bmod 3233 = 3086$ |
| blinded message $z = m \cdot r^e$ | $65 \cdot 3086 \bmod 3233 = 144$ |
| signer: $s' = z^d$ | $144^{413} \bmod 3233 = 2940$ |
| $r^{-1} \bmod n$ | $1940$ |
| unblind: $s = s' \cdot r^{-1}$ | $2940 \cdot 1940 \bmod 3233 = 588$ |
| check: $s^e \bmod n$ | $588^{17} \bmod 3233 = 65 = m$ |

The result is $65^{413} \bmod 3233 = 588$, the plain RSA signature of $m$. With $r = 7$ instead, the signer sees $z = 2034$ and answers $883$, and unblinding again gives $588$. The two sessions look unrelated to the signer, but they give the same signature.

## Correctness

The signer computes $z^d = m^d \cdot r^{ed} = m^d \cdot r \pmod n$, because $x^{ed} \equiv x$ for every $x$ modulo an RSA modulus. Multiplying by $r^{-1}$ leaves $m^d$, which is the RSASSA-PSS signature of $input\_msg$ with the salt the client chose, so a standard verifier accepts it.

Blindness: for a valid key, $r \mapsto m \cdot r^e$ is a bijection on the units modulo $n$, so $z$ is uniform whatever the message is. For any session view $(z, s')$ and any later signature $(M^*, s^*)$, the factor $r^* = s' / s^*$ fits both, so the view cannot tell which signature came from which session. The full proof is in [proofs/correctness.md](proofs/correctness.md).

One-more unforgeability: Bellare, Namprempre, Pointcheval and Semanko (2003) proved it for Chaum's scheme with a full-domain hash in the [random oracle model](/random-oracle-model/) (hash functions modelled as truly random functions), under the one-more RSA inversion assumption: given $q + 1$ random targets and $q$ calls to an $e$-th root oracle, nobody can find all $q + 1$ roots. Lysyanskaya (PKC 2023) proved it for the RFC 9474 variants.

## Complexity

For a modulus of $k$ machine words, the signer does one full exponentiation, $\Theta(k^3)$ with schoolbook arithmetic (about $k^{2.58}$ with Karatsuba), plus one exponentiation by $e$ for the check. The client does an exponentiation by the small $e = 65537$ ($\Theta(k^2)$: 16 squarings and one multiplication), one modular inverse ($\Theta(k^2)$), two multiplications, a PSS encoding of $O(k)$ hash blocks, and one verification. The messages are $k$ words each way, in one round trip.

## Properties

- **Standard output.** The final signature is an RSASSA-PSS signature; verifiers need no new code.
- **Perfect blindness for an honest key.** The blinded message is uniform, so even an unbounded signer learns nothing about the message.
- **One round.** One message from the client and one from the signer.
- **Concurrent sessions are safe.** Unlike the Schnorr blind signature, many parallel sessions do not help the client forge, under the one-more RSA inversion assumption.
- **Randomized or deterministic.** PSS with a salt and the random prefix gives a fresh signature each time. RSABSSA-SHA384-PSSZERO-Deterministic gives one signature per message, which some protocols need.
- **Not post-quantum.** Shor's algorithm factors $n$.

## Variants and improvements

- **RSA-FDH blind signature.** Chaum's form with a full-domain hash instead of PSS; the analysis of Bellare et al. is for this form. RFC 9474 chose PSS because standard libraries verify it.
- **Randomized preparation.** The 32-byte prefix of line L1 protects the client from a signer with a malformed key: Lysyanskaya showed blindness of these variants, while the identity variants need high-entropy messages (RFC 9474, Section 7.3).
- **Partially blind signatures.** The signer and the client agree on public information, such as an expiry date or a value, that is part of the signed message. RSA variants exist, but simple ones need care.
- **Other algebra.** The same idea works in pairing groups with [BLS signatures](/bls-signature/) (blind by multiplying the hash point by $g^r$), and in prime-order groups with the Schnorr blind signature, which the ROS attack breaks under concurrency.

## When to use it

Use RSABSSA when a server must issue tokens that cannot be linked to their issuance and that anyone can verify with a public key: anonymous access tokens, rate-limit tokens and e-cash style coins. Privacy Pass (RFC 9578) uses it for its publicly verifiable token type 0x0002, with a 2048-bit key and the deterministic variants, where the token input holds a 32-byte random nonce. Apple's iCloud Private Relay and Google's VPN service use RSA blind signatures for access tokens (RFC 9474, Section 1). If only the issuer verifies, an oblivious pseudorandom function is cheaper.

## Pitfalls

- **Not the same as RSA blinding.** [RSA blinding](/rsa-blinding/) (a defence that multiplies the input of the private-key operation by $r^e$ so that its timing does not depend on attacker data) uses the same algebra for a different goal: the signer blinds its own input to protect its key, and the result is never seen blinded. In a blind signature the client blinds the input to hide the message from the signer. The two combine: RFC 9474, Section 7.1, says the signer should also use RSA blinding inside BlindSign.
- **The signer is a raw RSA oracle.** BlindSign computes $z^d$ for any $z$ the client sends. If the key also signs or decrypts in another protocol, a client can get a signature on any encoded message, or decrypt any ciphertext. RFC 9474, Section 6.2, therefore says the key must not be used for any other protocol or for another encoding option.
- **Check the signer's answer.** Without the check of line L9, a cheating signer can return a wrong value that later marks the client; without the check of line L7, one fault in a CRT signer leaks a factor of $n$.
- **Malicious keys and low-entropy messages.** A signer with a malformed key, for example one on which $x \mapsto x^e$ is not a permutation, can learn which of a few likely messages the client blinds (RFC 9474, Section 7.3). Use the randomized variants, or get a proof that the key is well formed.
- **Bad randomness in $r$.** A predictable $r$ removes blindness, since the signer can divide it out. The salt and the prefix must be random too, or they can carry tracking data.
- **Uniform $r$.** Take $r$ uniform modulo $n$ by rejection sampling, not by reducing a short random string.

## Implementations

The Python code is for study only: it is not constant time, does no RSA blinding inside BlindSign, and must not protect real data. It implements the four RSABSSA variants with EMSA-PSS and MGF1 over SHA-384 from hashlib. The tests run all four test vectors of RFC 9474, Appendix A (one 4096-bit key), checking the PSS encoding, the blinded message, the blind signature and the final signature by their SHA-256 digests, and they check that every session view fits every output signature with some blinding factor.

## History

David Chaum introduced blind signatures at Crypto 1982 with this RSA construction, as the basis for untraceable electronic payments, and his company DigiCash ran an eCash system on it in the 1990s. Chaum, Fiat and Naor (Crypto 1988) built offline e-cash on top of it. The scheme had no proof for two decades: Bellare, Namprempre, Pointcheval and Semanko defined the one-more RSA inversion problems (Financial Cryptography 2001, Journal of Cryptology 2003) and proved its security in the random oracle model. Interest returned with Privacy Pass, whose first token types used oblivious pseudorandom functions that only the issuer can verify. Denis, Jacobs and Wood specified RSABSSA in the IRTF Crypto Forum Research Group, published as RFC 9474 in October 2023, and Privacy Pass adopted it in RFC 9578 in June 2024.

## References
