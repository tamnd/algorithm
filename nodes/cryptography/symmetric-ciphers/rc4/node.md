---
tag: F9NPHX
kind: algorithm
slug: rc4
name: RC4
aliases:
- ARC4
- Rivest Cipher 4
area: cryptography/symmetric-ciphers
level: intro
summary: A byte-oriented stream cipher by Rivest (1987). A key schedule mixes a 256-byte permutation, then each step swaps two entries and outputs one. It is broken, and RFC 7465 prohibits it in TLS.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {k: the key length in bytes, m: the number of keystream bytes}
  time: {worst: Θ(m + 256), average: Θ(m + 256), best: Θ(m + 256)}
  space: {extra: Θ(256)}
properties: {deterministic: true}
history:
  year: 1987
  people: [Ron Rivest]
  note: Rivest designed RC4 in 1987 for RSA Data Security. It was a trade secret until its source code was posted anonymously to the Cypherpunks mailing list in September 1994.
prereqs: [stream-cipher]
see_also: [stream-cipher, chacha20, salsa20, one-time-pad, related-key-attack, ciphertext-only-attack, chacha20-poly1305]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc6229"
    title: Joachim Strombergson and Simon Josefsson, RFC 6229, Test Vectors for the Stream Cipher RC4, May 2011
    locator: Section 2 (test vectors for keys of 40 to 256 bits at offsets 0 to 4096)
  - url: "https://www.rfc-editor.org/rfc/rfc7465"
    title: Andrei Popov, RFC 7465, Prohibiting RC4 Cipher Suites, February 2015
    locator: Section 2 (TLS clients and servers must not negotiate RC4 cipher suites)
  - paper: "Itsik Mantin and Adi Shamir, A practical attack on broadcast RC4, Fast Software Encryption (FSE 2001), LNCS 2355"
    locator: the bias of the second output byte toward 0, with probability about 2/256
  - paper: "Scott Fluhrer, Itsik Mantin and Adi Shamir, Weaknesses in the key scheduling algorithm of RC4, Selected Areas in Cryptography (SAC 2001), LNCS 2259"
    locator: the invariance weakness and the related key attack when an IV is put before the secret key, as in WEP
  - paper: "Nadhem AlFardan, Daniel J. Bernstein, Kenneth G. Paterson, Bertram Poettering and Jacob C. N. Schuldt, On the security of RC4 in TLS, 22nd USENIX Security Symposium, 2013"
    locator: ciphertext-only plaintext recovery against TLS with RC4, from the single-byte and multi-byte keystream biases
  - book: isbn:9780471117094
    title: Bruce Schneier, Applied Cryptography, second edition, Wiley, 1996
    locator: Section 17.1 (RC4, its history and the 1994 posting of the source code)
---

RC4 is a [stream cipher](/stream-cipher/) that Ron Rivest designed in 1987. A key-scheduling algorithm (KSA) turns a key of 1 to 256 bytes into a permutation of the 256 byte values, and a pseudorandom generation algorithm (PRGA) then outputs one keystream byte per step. Encryption XORs the keystream with the plaintext. **RC4 is broken**: its output has strong biases, the WEP use of it falls to a key recovery attack, and RFC 7465 (2015) prohibits it in TLS.

## In plain words

Take a deck of 256 cards, numbered from 0 to 255, in order. The key tells you how to shuffle it: you walk through the deck one time, and for each position you swap the card there with a card at a place that the key and the cards choose. Then the cipher deals bytes. At each step it moves one pointer forward and the other pointer by the value of a card, swaps the two cards, and reads a third card at a place that the two values give. That card is the next byte of the keystream. The sender and the receiver shuffle with the same key, so they deal the same bytes. The sender XORs them into the message, and the receiver XORs them out again. The shuffle is too short and too regular, so some bytes come out more often than others.

## The problem

The input is a key $K$ of $k$ bytes, $1 \le k \le 256$, and a message $M$ of $m$ bytes. The output is $C = M \oplus Z$, where $Z = Z_1 Z_2 \ldots Z_m$ is the RC4 keystream of $K$. Decryption is the same operation. All arithmetic is modulo 256.

In the notation of this area, $K$ is the key, $A$ an adversary and $\mathrm{Adv}$ its advantage. The design goal of a stream cipher is that its keystream is a [pseudorandom generator](/pseudorandom-generator/) output: no efficient $A$ tells $Z$ apart from uniform bytes with a large advantage. RC4 does not meet this goal, because the biases below give a distinguisher with a small number of keys.

## The algorithm

```pseudo id=main
RC4-KSA(K)                                 ▷ K has k bytes, 1 ≤ k ≤ 256
L1  for i ← 0 to 255 do S[i] ← i
L2  j ← 0
L3  for i ← 0 to 255 do
L4      j ← (j + S[i] + K[i mod k]) mod 256
L5      swap S[i] and S[j]

RC4-PRGA(S, m)                             ▷ S is the output of RC4-KSA
L6  i ← 0, j ← 0
L7  repeat m times
L8      i ← (i + 1) mod 256
L9      j ← (j + S[i]) mod 256
L10     swap S[i] and S[j]
L11     output S[(S[i] + S[j]) mod 256]
```

The state is the permutation $S$ and the two indices $i$ and $j$: $256 \cdot 8 + 16 = 2064$ bits of storage, and $256! \cdot 256^2 \approx 2^{1700}$ possible states. The KSA makes one pass over $S$ (lines L3 to L5). The PRGA moves $i$ by one and $j$ by the value $S[i]$, swaps the two entries, and outputs the entry at index $S[i] + S[j]$. Encryption is $C_t = M_t \oplus Z_t$ and decryption is $M_t = C_t \oplus Z_t$.

The code on this page is for study only. It is not constant time, and it must not protect real data. Do not use RC4 at all: use ChaCha20-Poly1305 or AES-GCM from libsodium, OpenSSL or a FIPS 140 validated module.

## Example

Take the 40-bit key $K = $ 01 02 03 04 05 of RFC 6229. The KSA ends with $S[0 \ldots 7] = (1, 3, 8, 201, 21, 27, 35, 67)$. The first four steps of the PRGA are:

| step | $i$ | $j$ | $S[i]$ after swap | $S[j]$ after swap | $t = S[i] + S[j]$ | $Z = S[t]$ |
|---|---|---|---|---|---|---|
| 1 | 1 | 3 | 201 | 3 | 204 | 0xb2 |
| 2 | 2 | 11 | 89 | 8 | 97 | 0x39 |
| 3 | 3 | 14 | 31 | 3 | 34 | 0x63 |
| 4 | 4 | 35 | 26 | 21 | 47 | 0x05 |

The keystream starts b2 39 63 05, as in RFC 6229, Section 2, at offset 0. In step 1, $j = 0 + S[1] = 3$; the swap puts 201 at index 1 and 3 at index 3, and $201 + 3 = 204$.

## Correctness

Two facts make RC4 a correct cipher. First, lines L1, L5 and L10 keep $S$ a permutation of $\{0, \ldots, 255\}$: line L1 makes the identity, and a swap of two entries maps a permutation to a permutation. So each index in lines L4, L9 and L11 is in range. Second, the keystream depends only on $K$ and $m$, because the KSA and the PRGA are deterministic. So the receiver computes the same $Z$, and $(M \oplus Z) \oplus Z = M$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- The KSA does 256 iterations of lines L4 and L5, for any key length. Its cost is $\Theta(256)$ byte operations.
- The PRGA does a constant number of byte operations for each output byte. The time for $m$ bytes is $\Theta(m)$, so the total is $\Theta(m + 256)$.
- The state is 256 bytes plus two indices. There is no other memory.

RC4 was fast in software on the 8-bit and 32-bit machines of the 1990s, because each step is a few byte loads and stores. This, and the short code, made it popular.

## Properties

- **The second byte bias.** Mantin and Shamir (FSE 2001) showed that $\Pr[Z_2 = 0] \approx 2/256$ for a random key, twice the uniform value. The reason: suppose that after the KSA $S[2] = 0$ and $S[1] = X \ne 2$. Step 1 sets $j = X$ and swaps, so $S[X] = X$. Step 2 sets $j = X + S[2] = X$, swaps $S[2]$ and $S[X]$, so $S[2] = X$ and $S[X] = 0$, and outputs $S[X + 0] = 0$. If $S$ were a uniform permutation, this event has probability about $1/256$, and in the other cases $Z_2 = 0$ with probability about $1/256$. The sum is about $2/256$. With $q$ keys, the number of zeros at position 2 has mean about $2q/256$ instead of $q/256$, so a distinguisher that counts them has a large advantage after a few thousand keys. The test file measures this: 20000 random 16-byte keys give 161 zeros, a rate of $2.06/256$.
- **Broadcast attack.** If one plaintext goes out under many keys, the bias reveals its second byte: the most frequent value of $C_2$ is $M_2$.
- **Weak key scheduling.** Fluhrer, Mantin and Shamir (SAC 2001) showed that the first output bytes leak key bytes when the key is a known IV followed by a fixed secret, the WEP layout. An eavesdropper recovers the WEP secret key from enough packets.
- **Biases in TLS.** AlFardan, Bernstein, Paterson, Poettering and Schuldt (USENIX Security 2013) used the single-byte biases of the first 256 output bytes, and biases between consecutive bytes, to recover plaintext such as a cookie that is sent in many TLS sessions. RFC 7465 then prohibited RC4 cipher suites in TLS.
- **No nonce.** RC4 takes only a key. Protocols mix a nonce into the key themselves, and each mix (the WEP prefix, a hash) is a new design with its own risk.

## Variants and improvements

- **RC4-drop[n].** Discard the first $n$ output bytes (for example 768 or 3072) to skip the worst biases. This does not remove the long-term biases, and it does not save RC4.
- **Modern replacements.** [ChaCha20](/chacha20/) and [Salsa20](/salsa20/) are fast in software, take a nonce, and have no known practical attack. Use them in an AEAD such as [ChaCha20-Poly1305](/chacha20-poly1305/).

## When to use it

Do not use RC4 in new systems. Use it only to read old data, to interoperate with a legacy system during a migration, or to teach. For a fast software stream cipher, use ChaCha20 in ChaCha20-Poly1305.

## Pitfalls

- **Reusing a key.** RC4 has no nonce. Two messages under one key give $C \oplus C' = M \oplus M'$, the two-time pad of the [stream cipher](/stream-cipher/) page. Each message needs its own key.
- **Prefixing an IV to the key.** WEP used $K = IV \Vert K_{\text{secret}}$ in line L4. With a known and changing prefix, the first bytes leak the secret (Fluhrer, Mantin and Shamir).
- **Using the first bytes.** The early bytes are the most biased (line L11 in the first steps). Dropping them is not a fix, but using them makes the attacks cheaper.
- **No integrity.** RC4 encryption is malleable: flipping bit $b$ of $C_t$ flips bit $b$ of $M_t$. Without a MAC, an attacker changes "PAY 100" into "PAY 900" without the key.
- **Index arithmetic.** Lines L4, L9 and L11 must reduce modulo 256. In a language with wider integers, a missing mask reads past the table.

## Implementations

## History

Ron Rivest designed RC4 in 1987 for RSA Data Security, and the company kept it as a trade secret. In September 1994 its source code was posted anonymously to the Cypherpunks mailing list, and the name ARC4 ("alleged RC4") came into use for the leaked design. RC4 went into WEP, SSL and TLS, and many other products. Fluhrer, Mantin and Shamir broke WEP in 2001, and Mantin and Shamir found the second byte bias in the same year. After the attacks of AlFardan et al. in 2013, RFC 7465 prohibited RC4 in TLS in February 2015.

## References
