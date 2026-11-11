---
tag: YRNRA5
kind: algorithm
slug: blowfish
name: Blowfish
area: cryptography/symmetric-ciphers
level: intro
summary: A 16-round Feistel cipher on 64-bit blocks with a key of 32 to 448 bits and key-dependent S-boxes, by Schneier in 1993. Its 64-bit block makes it unfit for new designs.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {b: the number of 8-byte blocks}
  time: {worst: Θ(b), average: Θ(b), best: Θ(b)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 1993
  people: [Bruce Schneier]
  note: Schneier presented Blowfish at the Cambridge Security Workshop on fast software encryption in December 1993, as a free replacement for DES.
prereqs: [feistel-network, s-box, key-schedule]
see_also: [bcrypt, twofish, data-encryption-standard, advanced-encryption-standard, birthday-attack, block-cipher, cbc-mode]
sources:
  - paper: doi:10.1007/3-540-58108-1_24
    title: Bruce Schneier, Description of a new variable-length key, 64-bit block cipher (Blowfish), Fast Software Encryption, Cambridge Security Workshop 1993, LNCS 809, Springer, 1994
    locator: pp. 191-204, the description of the cipher, the function F, the generation of the subkeys and the design decisions
  - url: "https://www.schneier.com/wp-content/uploads/2015/12/vectors-2.txt"
    title: Eric Young, Blowfish test vectors, published on Bruce Schneier's web site
    locator: the ecb test data, the set_key test data and the chaining mode test data
  - paper: doi:10.1007/3-540-60865-6_39
    title: Serge Vaudenay, On the weak keys of Blowfish, Fast Software Encryption 1996, LNCS 1039, Springer, 1996
    locator: pp. 27-32
  - paper: doi:10.1145/2976749.2978423
    title: "Karthikeyan Bhargavan and Gaëtan Leurent, On the practical (in-)security of 64-bit block ciphers: collision attacks on HTTP over TLS and OpenVPN, ACM CCS 2016"
    locator: the birthday attack on CBC with a 64-bit block (Sweet32) and the attack on OpenVPN with Blowfish
  - url: "https://www.usenix.org/legacy/events/usenix99/provos.html"
    title: Niels Provos and David Mazières, A future-adaptable password scheme, USENIX Annual Technical Conference 1999
    locator: the Eksblowfish key setup used by bcrypt
---

Blowfish is a [block cipher](/block-cipher/) on 64-bit blocks with a key of 32 to 448 bits, built as a 16-round [Feistel network](/feistel-network/). Bruce Schneier published it in 1993 as a fast, free cipher for 32-bit processors. Its [S-boxes](/s-box/) are not fixed tables: the [key schedule](/key-schedule/) fills them with values that depend on the key. No attack on the full 16 rounds faster than [exhaustive search](/exhaustive-key-search/) is published, but the 64-bit block makes it unsafe for large amounts of data under one key, so new systems use [AES](/advanced-encryption-standard/).

**Notation.** A block is two 32-bit words $x_L \| x_R$, read big-endian. $P_1, \ldots, P_{18}$ is the P-array of 32-bit subkeys and $S_1, \ldots, S_4$ are four S-boxes, each with 256 entries of 32 bits. $\oplus$ is XOR and $+$ is addition modulo $2^{32}$. $K$ is the key and $b$ is the number of blocks.

## In plain words

Blowfish cuts a block into a left half and a right half. In each of 16 rounds, it mixes a secret word into the left half. Then it sends the left half through a small function that looks up four tables, one for each byte, and combines the four results with additions and an XOR. The output changes the right half. Then the halves trade places.

The tables are the special part. They start as the digits of pi. To set up a key, Blowfish mixes the key into the first secret words and then encrypts a block of zeros again and again with its own rules. Each output replaces two entries, until all the tables hold values that depend on the key. This setup is slow on purpose, and it is the reason that the password hash bcrypt is built on Blowfish.

## The problem

Blowfish computes a permutation $E_K$ of $\{0,1\}^{64}$ for each key $K$ of 4 to 56 bytes, and its inverse $D_K$. Messages longer than one block need a mode of operation such as [CBC](/cbc-mode/) or [CTR](/ctr-mode/). The security goal is that $E_K$ is a [pseudorandom permutation](/pseudorandom-permutation/) (PRP): an attacker who does not know $K$ cannot tell $E_K$ from a random permutation with a useful advantage. There is no proof of this for Blowfish: its security rests on the absence of a known attack.

## The algorithm

```pseudo id=main
BLOWFISH-ENCRYPT(P, S, x)
L1  (xL, xR) ← x, as two 32-bit words
L2  for i ← 1 to 16 do
L3      xL ← xL ⊕ P[i]
L4      xR ← F(xL) ⊕ xR
L5      swap xL and xR
L6  swap xL and xR                          ▷ undo the last swap
L7  xR ← xR ⊕ P[17]
L8  xL ← xL ⊕ P[18]
L9  return xL ‖ xR

F(x)                                        ▷ x = a ‖ b ‖ c ‖ d, four bytes, a the highest
L10 return ((S1[a] + S2[b]) ⊕ S3[c]) + S4[d]

KEY-SETUP(K)
L11 P[1..18], S1, S2, S3, S4 ← the hex digits of the fraction of π, in this order
L12 for i ← 1 to 18 do
L13     P[i] ← P[i] ⊕ (the next 4 bytes of K, read big-endian, with K repeated cyclically)
L14 z ← 0 (64 bits)
L15 for each pair (P[1], P[2]), ..., (P[17], P[18]), (S1[0], S1[1]), ..., (S4[254], S4[255]) do
L16     z ← BLOWFISH-ENCRYPT(P, S, z)
L17     replace the pair with the two halves of z
```

BLOWFISH-DECRYPT is BLOWFISH-ENCRYPT with the P-array in reverse order, $P_{18}, P_{17}, \ldots, P_1$. Line L11 uses 1042 words of 32 bits, so it needs the first 8336 hex digits of $\pi - 3$; $P_1$ = 243F6A88 and $P_2$ = 85A308D3. The loop of line L15 runs 9 times for the P-array and 512 times for the S-boxes, so key setup costs 521 encryptions. Each call in line L16 uses the subkeys that the earlier calls have already replaced.

The Python code for this page is for study only. It is not constant time, because each S-box lookup uses a secret index. Do not use it to protect real data. Use AES or ChaCha20 from a FIPS 140 validated module, or libsodium, instead.

## Example

Take the first row of Eric Young's test data: the key is eight zero bytes and the plaintext is 0000000000000000. Line L13 changes nothing, because the key is zero. After the 521 encryptions of key setup, $P_1$ = 706D9FCC, $P_2$ = 1792D23A, $P_{17}$ = 7361E6A1 and $P_{18}$ = 196A7C43.

| step | $x_L$ | $x_R$ |
|---|---|---|
| start | 00000000 | 00000000 |
| round 1: $x_L \oplus P_1$ = 706D9FCC, $F$ = 73DB3280, swap | 73DB3280 | 706D9FCC |
| round 2 | EB359563 | 6449E0BA |
| round 16 | 12F93BD9 | 5793EB06 |
| line L6, undo the swap | 5793EB06 | 12F93BD9 |
| lines L7 and L8 | 4EF99745 | 6198DD78 |

The ciphertext 4EF997456198DD78 is the value in the test data. The test file checks all 34 rows of the ECB data in both directions, the set_key data (for example, the first byte F0 of the key alone gives FEDCBA9876543210 to F9AD597C49DB005E), and the chaining mode data in CBC.

## Correctness

BLOWFISH-DECRYPT inverts BLOWFISH-ENCRYPT for every P-array and every set of S-boxes. The function F need not be invertible: the rounds form a Feistel network, and the subkey $P_{i}$ in line L3 goes into the half that is the input of F in the same round. Write $a_1, \ldots, a_{17}$ for the words that the rounds feed to F, then encryption satisfies $a_{i+1} = a_{i-1} \oplus F(a_i) \oplus P_{i+1}$, and this recurrence can be run backwards with the keys in reverse order. The [proof](proofs/correctness.md) gives each step.

## Complexity

One block costs 16 rounds. A round costs one XOR with a subkey and one call of F, which is 4 S-box lookups, 2 additions and 1 XOR, plus the XOR into the other half. So a block costs 64 S-box lookups and 18 subkey XORs, and $b$ blocks cost $\Theta(b)$ time. The key state is $18 + 4 \cdot 256 = 1042$ words, which is 4168 bytes, independent of the message.

Key setup costs 521 block encryptions, more than 500 times the cost of one block. This is cheap for a long message, but expensive when the key changes for each short message. bcrypt uses this cost on purpose.

The best published attacks do not reach the full cipher. Vaudenay (1996) showed that some keys give S-boxes with two equal entries, and that for such weak keys a differential attack works on versions with fewer rounds; with the full 16 rounds, the attack does not beat exhaustive search. The limit in practice is the block size: by the [birthday bound](/birthday-attack/), two ciphertext blocks of CBC collide after about $2^{32}$ blocks (32 GiB), and each collision gives the XOR of two plaintext blocks. Bhargavan and Leurent (2016) used this, the Sweet32 attack, against OpenVPN, whose default cipher was Blowfish in CBC mode.

## Properties

- **Feistel structure.** Decryption uses the same round code with the P-array reversed, and F does not need an inverse.
- **Key-dependent S-boxes.** The attacker does not know the tables, so a differential or linear attack cannot be planned from fixed S-box tables. This is the main design idea.
- **Avalanche.** With the zero key, a one-bit change of the plaintext changes on average 31.96 of the 64 ciphertext bits over 2000 random trials. The ideal value is 32. See [avalanche effect](/avalanche-effect/).
- **Key length.** Schneier allows 32 to 448 bits (4 to 56 bytes). Many implementations, and the code for this page, also accept 1 to 72 bytes, the size of the P-array, but such keys are outside the specification.
- **No proof.** Like DES, Blowfish has no proof of security. Confidence comes from more than 30 years without a practical attack on the full cipher.

## Variants and improvements

- **Eksblowfish and bcrypt.** Provos and Mazières (1999) made the key setup slow on purpose, with a cost parameter and a salt, and used it as the [password hash](/password-hashing/) [bcrypt](/bcrypt/).
- **[Twofish](/twofish/).** The successor of Blowfish by Schneier and others, a 128-bit block AES finalist that keeps the key-dependent S-boxes.
- **Reduced rounds.** Versions with fewer than 16 rounds are used only in cryptanalysis.

## When to use it

Do not use Blowfish in new designs. Its 64-bit block limits the safe data under one key to far less than $2^{32}$ blocks, and its key setup makes key changes slow. Use AES-GCM or ChaCha20-Poly1305 instead. Use Blowfish only to read old data, to work with old systems, or through bcrypt for passwords, where bcrypt is still accepted.

## Pitfalls

- **Large data under one key.** With a 64-bit block, rekey long before $2^{32}$ blocks. The Sweet32 attack needs only enough traffic for a collision.
- **Byte order.** The words are big-endian. A little-endian load gives a cipher that decrypts what it encrypts, but fails the test vectors.
- **Key setup uses the cipher being built.** Each encryption in line L16 must use the subkeys as they are at that moment, not the initial ones and not the final ones.
- **The final swap.** Lines L6 to L8 undo the last swap before the two final XORs. Without line L6, the test vectors fail.
- **Table lookups and timing.** An S-box lookup at a secret index can leak through the cache, and the S-boxes are secret here.

## Implementations

## History

Schneier presented Blowfish at the Cambridge workshop on fast software encryption in December 1993, and the paper appeared in LNCS 809 in 1994. He wanted a free, unpatented cipher that was faster than DES in software and allowed long keys. Blowfish went into many products and libraries in the 1990s, and OpenVPN used it as its default cipher. Schneier and others later designed Twofish for the AES competition. Bhargavan and Leurent showed in 2016 with Sweet32 that 64-bit block ciphers fail in practice when long sessions use one key.

## References
