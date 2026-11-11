---
tag: K2XCQP
kind: technique
slug: ofb-mode
name: Output feedback mode
aliases:
- OFB
area: cryptography/symmetric-ciphers
level: core
summary: Make a keystream by encrypting the IV again and again, and XOR it with the message. Bit errors stay local, but a repeated IV repeats the keystream.
prereqs: [block-cipher, nonce]
see_also: [cfb-mode, ctr-mode, cbc-mode, stream-cipher, one-time-pad, nonce]
sources:
  - url: "https://doi.org/10.6028/NIST.SP.800-38A"
    title: Morris Dworkin, NIST Special Publication 800-38A, Recommendation for Block Cipher Modes of Operation, Methods and Techniques, 2001
    locator: Section 6.4 (OFB), Section 5.3 and Appendix C (the IV must be a nonce), Appendix D (error properties) and Appendix F.4 (OFB example vectors)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 7.2.2 (OFB mode, error propagation, and the short cycles of OFB with partial feedback)
  - paper: "Donald W. Davies and Graeme I. P. Parkin, The average cycle size of the key stream in output feedback encipherment, Advances in Cryptology, Proceedings of CRYPTO 82, Plenum Press, 1983"
    locator: the cycle length of OFB with full and with partial feedback
---

Output feedback (OFB) mode turns a [block cipher](/block-cipher/) into a synchronous [stream cipher](/stream-cipher/). It encrypts the [initialization vector](/initialization-vector/), then encrypts the result, and so on, and XORs the chain of outputs with the message. NIST defines OFB in SP 800-38A, Section 6.4, and requires the IV to be a [nonce](/nonce/): unique for each message under the key. The keystream does not depend on the message, so a bit error in the ciphertext changes only the same bit of the plaintext; but if an IV repeats, the keystream repeats, and the XOR of the two ciphertexts is the XOR of the two plaintexts.

**Notation.** $E_K$ is a block cipher with key $K$ and block length $n$ bits, $O_0 = IV$ and $O_j = E_K(O_{j-1})$ are the output blocks, $P_j$ and $C_j$ are the plaintext and ciphertext blocks. $\sigma$ is the total number of blocks encrypted under one key.

## In plain words

OFB makes a long stream of random-looking bytes from the key and a starting value. It encrypts the starting value, then encrypts that result, then encrypts the next result, and so on. The message is XOR-ed with this stream, byte by byte. The receiver makes the same stream from the same key and starting value, and XORs again to get the message back.

The stream does not depend on the message at all. So a sender can make the stream before the message is ready, and a damaged bit on the line damages only one bit of the message. The danger is the starting value. If two messages use the same key and the same starting value, they use the same stream, and an attacker who XORs the two encrypted messages gets the XOR of the two messages, with no key needed.

## When it applies

- **Noisy channels with no loss of bits.** One flipped bit on the line gives one flipped bit of plaintext, with no spread. This suits radio and satellite links where error correcting codes run on the plaintext.
- **Keystream before the data.** The keystream can be computed in advance and stored, so the encryption of the data itself is one XOR per byte.
- **Only the forward cipher.** Like [CFB](/cfb-mode/) and [CTR](/ctr-mode/), OFB never calls $D_K$.
- **Not when bits can be lost.** A lost or inserted bit shifts the alignment of the keystream for the rest of the message, and OFB never resynchronizes. Use [CFB](/cfb-mode/) if this matters.
- **Not when random access or parallel work matters.** Block $j$ of the keystream needs all $j$ blocks before it. [CTR](/ctr-mode/) gives the same stream cipher behavior with random access.

## The template

```pseudo id=main
OFB(K, IV, X[1 .. m])                      ▷ encryption and decryption are the same
L1  O ← IV                                 ▷ IV: a nonce, unique for each message under K
L2  for j ← 1 to m do
L3      O ← E_K(O)
L4      Y[j] ← X[j] ⊕ MSB_|X[j]|(O)          ▷ the last block may be partial
L5  return Y[1 .. m]
```

The holes are the cipher $E$ and the source of the IV. The same procedure decrypts, because $(P_j \oplus O_j) \oplus O_j = P_j$, and lines L1 and L3 produce the same $O_j$ on both sides. A final partial block uses only the leftmost bits of $O_m$, so no padding is needed and the ciphertext has the same length as the plaintext.

**Cost.** $\lceil \ell / n \rceil$ cipher calls for an $\ell$-bit message. The calls form a chain, so they are sequential, but they do not depend on the data. The XOR costs one operation per byte.

**About the code.** The Python code of this page, with its own AES, is for study only. It is not constant time, and it must not be used to protect real data. Use an AEAD from a FIPS 140 validated module or libsodium.

### Error propagation

A flipped bit in $C_j$ flips the same bit in $P_j$ and nothing else, because $O_j$ does not depend on the ciphertext. This also means an attacker can flip any plaintext bit that it chooses, without the key. A lost or extra bit or byte shifts the ciphertext against the keystream, so every later bit is wrong: unlike CFB, OFB does not heal. SP 800-38A, Appendix D, lists these properties.

### Keystream reuse when the IV repeats

If two messages $P$ and $P'$ use the same key and the same IV, then $C \oplus C' = P \oplus P'$ on their common length. This is the two-time pad: the attacker learns the XOR of the messages, and with any known or guessed part of one message, the same part of the other. A subtler overlap: if the IV of the second message equals some output block $O_i$ of the first message, then the keystream of the second message is the keystream of the first shifted by $i$ blocks. The test of this page checks both effects.

The IV need not be unpredictable, only unique (SP 800-38A, Section 5.3 and Appendix C). The reason: the attacker cannot choose plaintext that changes the keystream, so knowing the IV in advance does not help it, as long as the keystream never overlaps. In a model where $E_K$ is a random permutation, the chains of two messages overlap only if a cipher input of one chain equals a cipher input of another chain. With $\sigma$ blocks in total, this happens with probability at most about $\sigma^2 / 2^n$, the same order as for CBC and CFB.

### Cycle length

The sequence $O_0, O_1, O_2, \ldots$ walks along one cycle of the permutation $E_K$. For a random permutation of $2^n$ points, the cycle that contains a given point has length uniform on $1, \ldots, 2^n$, so its mean is about $2^{n-1}$, and a short cycle is very unlikely. Old OFB variants fed back only $s < n$ bits of the output; then the next state is not a permutation of the old one, and Davies and Parkin (1983) showed the mean cycle length falls to about $2^{n/2}$. SP 800-38A OFB always feeds back the full block.

## Classic examples

### SP 800-38A F.4.1

AES-128 key `2b7e151628aed2a6abf7158809cf4f3c`, IV `000102030405060708090a0b0c0d0e0f`.

| $j$ | output block $O_j$ | plaintext $P_j$ | ciphertext $C_j$ |
|---|---|---|---|
| 1 | `50fe67cc996d32b6da0937e99bafec60` | `6bc1bee22e409f96e93d7e117393172a` | `3b3fd92eb72dad20333449f8e83cfb4a` |
| 2 | `d9a4dada0892239f6b8b3d7680e15674` | `ae2d8a571e03ac9c9eb76fac45af8e51` | `7789508d16918f03f53c52dac54ed825` |
| 3 | `a78819583f0308e7a6bf36b1386abf23` | `30c81c46a35ce411e5fbc1191a0a52ef` | `9740051e9c5fecf64344f7a82260edcc` |
| 4 | `c6d3416d29165c6fcb8e51a227ba994e` | `f69f2445df4f9b17ad2b417be66c3710` | `304c6528f659c77866a510d9c1d6ae5e` |

Each output block is the encryption of the one above it; the first is the encryption of the IV. The first ciphertext block equals that of [CFB-128](/cfb-mode/) in F.3.13, because both modes compute $P_1 \oplus E_K(IV)$ first.

### A repeated IV

Encrypt `transfer 100 USD to account 7` and `transfer 999 USD to account 1` with the same key and IV. The XOR of the two ciphertexts is zero in every byte except bytes 9 to 11 and byte 28 (counting from 0), where it equals the XOR of `100` with `999` and of `7` with `1`. An attacker who knows the first message gets the second one by one more XOR. The keystream itself never appears, and no key search is needed.

## Variations

- **OFB with $s$-bit feedback.** Older standards (FIPS 81 for DES) allowed feedback of $s < n$ bits. This makes cycles short, about $2^{n/2}$, and is not in SP 800-38A.
- **CTR mode.** Replace the chain $O_j = E_K(O_{j-1})$ by $O_j = E_K(T_j)$ for distinct counter blocks $T_j$. This gives random access and parallel work, and a simpler proof. See [CTR mode](/ctr-mode/).
- **OFB with a separate integrity check.** As with any stream mode, add a MAC over the IV and ciphertext, or use an AEAD.

## Pitfalls

- **Repeating the IV.** It repeats the keystream and leaks the XOR of the plaintexts. A counter or random IV that is unique per message avoids it.
- **Treating OFB as integrity protection.** Flipped ciphertext bits flip plaintext bits with no error. Use a MAC.
- **Expecting resynchronization.** A lost byte destroys the rest of the message.
- **Partial feedback.** Feeding back fewer than $n$ bits gives short cycles.

## Exercises

1. Show that OFB with a repeated IV is not IND-CPA secure, with one oracle query.
2. An attacker knows the first 16 bytes of a message encrypted with OFB. Show how it changes them into any other 16 bytes.
3. Prove that if $IV' = O_i$ for a previous message, the keystream of the new message is the old one shifted by $i$ blocks.
4. For a random permutation on $N$ points, prove that the cycle that contains a fixed point has length uniform on $1, \ldots, N$.

## References
