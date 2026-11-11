---
tag: 60YSZW
kind: algorithm
slug: rsa-oaep
name: RSA-OAEP
aliases:
- optimal asymmetric encryption padding
- OAEP
area: cryptography/public-key
level: core
summary: "RSA with the OAEP padding of Bellare and Rogaway: two Feistel rounds with a hash and a mask function. IND-CCA2 secure in the random oracle model, with a loose reduction."
solves: [public-key-encryption]
model: word-ram
complexity:
  vars: {b: the number of binary digits of the modulus, k: the number of octets of the modulus, h: the number of octets of the hash output}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^3)}
  space: {extra: Θ(b)}
properties: {deterministic: false, randomized: true}
history:
  year: 1994
  people: [Mihir Bellare, Phillip Rogaway]
  note: Published at Eurocrypt 1994 and standardized in PKCS #1 v2.0 in 1998. Shoup found a gap in the 1994 proof in 2001, and Fujisaki, Okamoto, Pointcheval and Stern gave a proof under the RSA assumption in the same year.
prereqs: [rsa-cryptosystem, cryptographic-hash-function]
see_also: [rsa-pkcs1-v1-5-encryption, rsa-cryptosystem, ind-cca-security, random-oracle-model, padding-oracle-attack, fujisaki-okamoto-transform, key-encapsulation-mechanism, rsa-problem]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc8017"
    title: Kathleen Moriarty, Burt Kaliski, Jakob Jonsson and Andreas Rusch, RFC 8017, PKCS #1, RSA Cryptography Specifications Version 2.2, 2016
    locator: Section 7.1 (RSAES-OAEP), Section 7.1.1 (the encoding), Section 7.1.2 (the decoding and the note on error messages) and Appendix B.2.1 (MGF1)
  - paper: "Mihir Bellare and Phillip Rogaway, Optimal asymmetric encryption, how to encrypt with RSA, EUROCRYPT 1994, LNCS 950, pages 92 to 111"
    locator: Section 4 (the construction with two hash functions G and H, and the plaintext awareness argument)
  - url: "https://eprint.iacr.org/2000/060"
    title: Victor Shoup, OAEP reconsidered, CRYPTO 2001, LNCS 2139, pages 239 to 259
    locator: Sections 1 and 3 (the gap in the 1994 proof, the oracle separation, and OAEP+)
  - url: "https://eprint.iacr.org/2000/061"
    title: Eiichiro Fujisaki, Tatsuaki Okamoto, David Pointcheval and Jacques Stern, RSA-OAEP is secure under the RSA assumption, CRYPTO 2001, LNCS 2139, pages 260 to 274
    locator: the main theorem (IND-CCA2 in the random oracle model from partial domain one-wayness) and the lemma that partial domain and full domain one-wayness of RSA are equivalent
  - paper: "James Manger, A chosen ciphertext attack on RSA optimal asymmetric encryption padding (OAEP) as standardized in PKCS #1 v2.0, CRYPTO 2001, LNCS 2139, pages 230 to 238"
    locator: Sections 2 and 3 (the oracle that separates the integer too large error from the decoding error, and the query count near 1100 for a modulus of 1024 binary digits)
  - url: "https://raw.githubusercontent.com/pyca/cryptography/main/vectors/cryptography_vectors/asymmetric/RSA/pkcs-1v2-1d2-vec/oaep-vect.txt"
    title: RSA Laboratories, PKCS #1 v2.1 test vectors, file oaep-vect.txt of the archive pkcs-1v2-1-vec.zip, copy in the pyca/cryptography test vectors
    locator: Example 1.1 and Example 1.2 (key 1 of 1024 binary digits, SHA-1, MGF1 with SHA-1, empty label)
---

OAEP is the padding that makes [RSA](/rsa-cryptosystem/) encryption chosen ciphertext secure. Bellare and Rogaway built it in 1994 as two Feistel rounds with a hash function: the message, with a label hash and a block of zero octets, is masked with a function of a random seed, and the seed is then masked with a function of the masked block. The result is one integer below the modulus, which the RSA primitive encrypts. RFC 8017 Section 7.1 is the current specification, and it says that new applications must use OAEP and not [PKCS #1 v1.5](/rsa-pkcs1-v1-5-encryption/).

**Notation.** $N$ is the modulus with $k = \lceil \log_{256} N \rceil$ octets, $\mathrm{Hash}$ is the hash function with an output of $h$ octets, $L$ is the label, $M$ the message of $\mathrm{mLen}$ octets, $\mathrm{DB}$ the data block of $k - h - 1$ octets and $\mathrm{EM}$ the encoded message of $k$ octets. RFC 8017 writes $\mathrm{hLen}$ for $h$ and $\mathrm{lHash}$ for $\mathrm{Hash}(L)$. $\mathrm{MGF1}$ is the mask generation function of Appendix B.2.1.

## In plain words

Plain RSA gives the same ciphertext for the same message, and a ciphertext can be changed in useful ways. OAEP removes both problems with a reversible scramble.

The sender draws a random seed, as long as one hash output. It builds a block that holds a hash of the label, a run of zero bytes, a single one byte and the message. It masks the block with a long stream made from the seed, and masks the seed with a short stream made from the masked block. Both streams are hash output, so each looks random.

The receiver undoes the two masks in the other order, checks the label hash and finds the one byte. If anything is wrong it reports one error and says nothing about what failed. One changed bit of the ciphertext changes the whole block, so a wrong ciphertext is almost never accepted.

## The problem

OAEP solves [public-key encryption](/public-key-encryption/) for messages of up to $k - 2h - 2$ octets, with [IND-CCA2](/ind-cca-security/) security in the [random oracle model](/random-oracle-model/). Longer data goes through [hybrid encryption](/hybrid-encryption/): OAEP carries a symmetric key, and an [authenticated cipher](/authenticated-encryption/) carries the data.

## The algorithm

```pseudo id=main
MGF1(seed, len, Hash)                    ▷ Appendix B.2.1; len ≤ 2^32·hLen
L1  T ← empty string
L2  for counter ← 0 to ⌈len/hLen⌉ − 1 do T ← T ‖ Hash(seed ‖ I2OSP(counter, 4))
L3  return the first len octets of T

EME-OAEP-ENCODE(M, L, k, Hash)           ▷ Section 7.1.1 step 2
L4  if |M| > k − 2hLen − 2 then return "message too long"
L5  lHash ← Hash(L),  PS ← a string of k − |M| − 2hLen − 2 zero octets
L6  DB ← lHash ‖ PS ‖ 0x01 ‖ M
L7  seed ← hLen random octets
L8  maskedDB ← DB ⊕ MGF1(seed, k − hLen − 1, Hash)
L9  maskedSeed ← seed ⊕ MGF1(maskedDB, hLen, Hash)
L10 return 0x00 ‖ maskedSeed ‖ maskedDB

RSAES-OAEP-ENCRYPT((N, e), M, L)
L11 EM ← EME-OAEP-ENCODE(M, L, k, Hash),  return I2OSP(OS2IP(EM)^e mod N, k)

RSAES-OAEP-DECRYPT(private key, C, L)    ▷ Section 7.1.2
L12 if |C| ≠ k or k < 2hLen + 2 then return "decryption error"
L13 EM ← I2OSP(RSADP(OS2IP(C)), k),  write EM as Y ‖ maskedSeed ‖ maskedDB
L14 seed ← maskedSeed ⊕ MGF1(maskedDB, hLen, Hash)
L15 DB ← maskedDB ⊕ MGF1(seed, k − hLen − 1, Hash)
L16 write DB as lHash' ‖ rest
L17 if Y ≠ 0x00, or lHash' ≠ Hash(L), or rest is not 0x00...0x00 ‖ 0x01 ‖ M
        then return "decryption error"
L18 return M
```

Lines L1 to L3 are the mask generation function: a counter mode over the hash, so the mask is as long as needed and the first octets of a long mask are the whole of a short one. Lines L8 and L9 are the two Feistel rounds. The order matters: the sender masks the block first and the seed second, so the receiver can undo the seed first on line L14 and then the block on line L15.

Line L6 is the only place where structure enters the plaintext. The label hash binds the ciphertext to a context, the zero octets of $\mathrm{PS}$ give the redundancy that a chosen ciphertext must forge, and the single $\texttt{0x01}$ octet marks where the message starts, so a message of any length up to the limit fits with no length field. RFC 8017 fixes $L$ to the empty string in this version of the standard, and $\mathrm{Hash}(\varepsilon)$ for SHA-1 is the constant `da39a3ee5e6b4b0d3255bfef95601890afd80709`.

Line L10 sets the leading octet to zero, so $\mathrm{OS2IP}(\mathrm{EM}) < 2^{8(k-1)} \le N$ and the RSA step on line L11 never needs a reduction. Line L17 is the one error of the standard: the three failures must give the same message and, as far as possible, the same timing. Line L13 must also reject a ciphertext integer that is not below $N$.

**About the code.** The Python code of this page is for study only. It is not constant time, it has no blinding, and it must not be used to protect real data. It is checked against Examples 1.1 and 1.2 of the official PKCS #1 v2.1 vector file oaep-vect.txt.

## Example

This is Example 1.1 of oaep-vect.txt: key 1 of 1024 binary digits, so $k = 128$, with SHA-1, so $h = 20$, and the empty label. The message has $\mathrm{mLen} = 28$ octets, so $\mathrm{PS}$ has $128 - 28 - 40 - 2 = 58$ zero octets.

| step | value (hexadecimal, shortened) |
|---|---|
| $M$ | `6628194e12073db03ba94cda9ef9532397d50dba79b987004afefe34` |
| seed | `18b776ea21069d69776a33e96bad48e1dda0a5ef` |
| $\mathrm{lHash} = \mathrm{SHA\text{-}1}(\varepsilon)$ | `da39a3ee5e6b4b0d3255bfef95601890afd80709` |
| $\mathrm{DB}$, L6, 107 octets | `da39a3ee...afd80709` ‖ 58 zero octets ‖ `01` ‖ $M$ |
| $\mathrm{maskedDB}$, L8 | `691f90e4dbabb03f76003765f55b7ed7a202635e` ... `4f392e738c703dc876e402ee16542095b77a6994` |
| $\mathrm{maskedSeed}$, L9 | `1016e93a98ac3af3a8c48fc01e87bd7000db8bdf` |
| $\mathrm{EM}$, L10, 128 octets | `00` ‖ $\mathrm{maskedSeed}$ ‖ $\mathrm{maskedDB}$ |
| $C$, L11 | `354fe67b4a126d5d35fe36c777791a3f` ... `0035d47ac72e8a` |

Decryption runs the table upward. Line L14 recovers the seed from $\mathrm{maskedSeed}$ and $\mathrm{maskedDB}$, line L15 recovers $\mathrm{DB}$, line L16 splits off the first 20 octets, which equal $\mathrm{lHash}$, and line L17 finds 58 zero octets and then $\texttt{0x01}$, so line L18 returns the 28 octets of $M$. The test file checks the two directions against the file, and also against Example 1.2 of the same key.

A changed ciphertext fails. If one octet of $\mathrm{maskedDB}$ changes, then $\mathrm{MGF1}(\mathrm{maskedDB}, 20)$ changes, so the recovered seed changes, so the whole of $\mathrm{DB}$ changes, so $\mathrm{lHash}'$ is wrong with probability $1 - 2^{-160}$. The test file flips one bit 20 times and gets 20 errors.

## Correctness

Encoding and decoding are inverse for every message of at most $k - 2h - 2$ octets: the two masks are applied in one order and removed in the other, so $\mathrm{DB}$ and the seed come back exactly, and the parse of line L17 is unique because every octet of $\mathrm{PS}$ is zero and the next octet is $\texttt{0x01}$. The RSA step is correct because the leading zero octet of line L10 keeps $\mathrm{OS2IP}(\mathrm{EM})$ below $N$. The full statement, with the bound and the uniqueness of the parse, is in the proof below.

## Complexity

Let $b$ be the number of binary digits of $N$ and $k = \lceil b/8 \rceil$.

- **Encoding**: $\lceil (k - h - 1)/h \rceil + 2$ hash calls, each on a short input, plus $O(k)$ octet operations. For $b = 2048$ and SHA-256 this is 9 hash calls.
- **Encryption**: the encoding plus one public [modular exponentiation](/modular-exponentiation/), $\Theta(b^2)$ for $e = 65537$.
- **Decryption**: one private exponentiation, $\Theta(b^3)$, which is about a quarter of that with the [CRT](/chinese-remainder-theorem/) form, plus the same hash work as the encoding.
- **Message limit**: $k - 2h - 2$ octets. A 2048 digit modulus with SHA-256 carries 190 octets, and with SHA-1 it carries 214.
- **Ciphertext size**: $k$ octets, so the expansion over the message is $2h + 2$ octets.
- **Space**: $\Theta(b)$.

The hash work is small next to the exponentiation. OAEP costs the same as v1.5 for all practical purposes.

## Properties

- **IND-CCA2 in the random oracle model.** Under the [RSA assumption](/rsa-problem/), with $G$ and $H$ modelled as random oracles (in practice MGF1 with a hash). This is the theorem of Fujisaki, Okamoto, Pointcheval and Stern (2001). The reduction is not tight: an adversary with advantage $\varepsilon$ gives an RSA inverter with success probability of order $\varepsilon^2/4$, in time of order $2t + q_H(q_H + 2q_G) \cdot O(b^3)$, where $q_G$ and $q_H$ count the hash queries. The square comes from the step that turns partial domain one-wayness into full domain one-wayness. So a proof at the 128 bit level needs a modulus larger than the tight reading of the bound suggests, and this looseness is one reason that modern designs prefer a [KEM](/key-encapsulation-mechanism/) with a tight proof.
- **The 1994 proof had a gap.** Bellare and Rogaway argued plaintext awareness and concluded chosen ciphertext security for any trapdoor permutation. Shoup showed in 2001 that the argument only gives security against a non adaptive attack, and that, relative to an oracle, there is a trapdoor permutation for which OAEP is not IND-CCA2. The scheme is fine for RSA; the general claim is not.
- **Randomized and non malleable.** Different seeds give different ciphertexts, and the redundancy of $\mathrm{PS}$ and $\mathrm{lHash}$ makes the scheme [non-malleable](/non-malleability/) in the model above.
- **Not a KEM and not an AEAD.** OAEP carries a short message. It has no integrity tag for long data and no streaming mode.
- **The label is not secret.** It is hashed, so both sides must know it. It binds a ciphertext to a context, for example a protocol version or a recipient name.
- **No standard vector for SHA-256.** The official file oaep-vect.txt only covers SHA-1, so the SHA-256 use of the code on this page is checked by round trip only.

## Variants and improvements

- **OAEP+** (Shoup 2001) adds a third hash $H'(M, \text{seed})$ inside the block and has a proof for every trapdoor permutation. It is not in PKCS #1, so it is rarely deployed.
- **SAEP and SAEP+** (Boneh 2001) drop one Feistel round and keep a proof for RSA with $e = 3$ and for [Rabin](/rabin-cryptosystem/). They are simpler but they lose the generic shape.
- **Other hashes.** RFC 8017 allows any hash in Appendix B.1 for both the label hash and MGF1, and the two may differ. SHA-256 is the common modern choice; SHA-1 is still the default in some libraries, which is a compatibility trap.
- **[Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) and KEM-DEM.** The modern way to reach IND-CCA2 is a KEM with implicit rejection: re-encrypt during decapsulation and return a pseudorandom key on failure. RSA-KEM (RFC 5990) does this for RSA and needs no padding check at all.
- **Standard model results.** Kiltz, O'Neill and Smith (2010) proved RSA-OAEP IND-CPA secure in the standard model under a lossy trapdoor assumption on RSA. No standard model IND-CCA2 proof is known.

## When to use it

Use OAEP when you must use RSA for key transport, for example with a standard or a device that names it. Pick SHA-256 for both the hash and MGF1, use the label if the protocol gives you one, and never use the same key for encryption and for [signatures](/rsa-pss/). For new designs prefer a KEM: [ECIES](/ecies/) or ML-KEM give shorter keys at the same level, and a post-quantum KEM is the only answer to [Shor's algorithm](/shor-algorithm/). Do not choose OAEP for bulk data: it carries at most $k - 2h - 2$ octets, so use it over a symmetric key.

## Pitfalls

- **Two error paths.** An implementation that says "integer too large" when $\mathrm{OS2IP}(C) \ge N$ at line L13, and "decryption error" at line L17, gives Manger's oracle: about 1100 chosen ciphertexts recover a plaintext for a 1024 digit modulus. Return the one error of line L17 and nothing else.
- **A timing difference in the check.** Lines L17 and L18 must not branch on the failure reason, and the work after a failure must match the work after a success. This is the same lesson as the [padding oracle](/padding-oracle-attack/) pages.
- **Truncating the encoded message.** $\mathrm{EM}$ has exactly $k$ octets, with the leading zero. Code that drops the leading zero and sends $k-1$ octets, or that forgets to pad a short RSA output back to $k$ octets at line L13, breaks interoperability and can create a length oracle.
- **A wrong or missing label.** Line L17 fails if the two sides disagree on $L$, and the error looks like a corrupt ciphertext. Fix the label in the protocol, not in the application code.
- **Mixing the hash and the mask function.** Line L5 and lines L8 and L9 may use different hashes, and a library default of SHA-1 for MGF1 with SHA-256 for the label hash is a common mismatch. State both.
- **Reusing the seed.** Line L7 must draw a fresh seed from the system random source for every message. A repeated seed with the same key and message gives the same ciphertext, which loses IND-CPA security.
- **Trusting OAEP to stop a side channel.** OAEP has no answer for a fault during the private exponentiation or a timing leak in it. See [RSA blinding](/rsa-blinding/), the [timing attack](/timing-attack/) page and the [fault attack](/rsa-fault-attack/) page.

## Implementations

## History

Bellare and Rogaway presented OAEP at Eurocrypt 1994 as the first RSA padding with a security argument, under the name "optimal asymmetric encryption". RSA Laboratories put it in PKCS #1 v2.0 in 1998, a few months after Bleichenbacher broke the v1.5 padding in protocols, and RFC 2437 wrote it up. The standard has been stable since: PKCS #1 v2.1 (RFC 3447, 2003) added the label and the current MGF1 text, and RFC 8017 (2016) is the same scheme.

The year 2001 brought three results at the same CRYPTO. Manger showed that a receiver which separates the "integer too large" error from the decoding error leaks the plaintext in about 1100 queries, so the error handling of v2.0 needed a note, which v2.1 has. Shoup showed that the 1994 proof does not give adaptive chosen ciphertext security for a general trapdoor permutation, and gave OAEP+ with a correct proof. Fujisaki, Okamoto, Pointcheval and Stern then proved that RSA-OAEP is IND-CCA2 in the random oracle model under the RSA assumption, through partial domain one-wayness, with a loose reduction. The scheme survived, and the episode is the standard example of how hard a padding proof is to get right.

## References
