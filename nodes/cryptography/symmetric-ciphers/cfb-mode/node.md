---
tag: MXBPBC
kind: technique
slug: cfb-mode
name: Cipher feedback mode
aliases:
- CFB
area: cryptography/symmetric-ciphers
level: core
summary: Turn a block cipher into a self-synchronizing stream cipher. Each keystream segment is the encryption of the last ciphertext bits, so a lost segment heals after one block.
prereqs: [block-cipher, initialization-vector, cbc-mode]
see_also: [ofb-mode, cbc-mode, ctr-mode, stream-cipher, ecb-mode, prp-prf-switching-lemma]
sources:
  - url: "https://doi.org/10.6028/NIST.SP.800-38A"
    title: Morris Dworkin, NIST Special Publication 800-38A, Recommendation for Block Cipher Modes of Operation, Methods and Techniques, 2001
    locator: Section 6.3 (CFB), Section 5.3 (IVs must be unpredictable for CFB), Appendix D (error properties) and Appendix F.3 (CFB example vectors)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 7.2.2 (CFB mode, error propagation and self-synchronization)
  - url: "https://cseweb.ucsd.edu/~mihir/papers/sym-enc.html"
    title: Mihir Bellare, Anand Desai, Eron Jokipii and Phillip Rogaway, A concrete security treatment of symmetric encryption, FOCS 1997 (full version on the authors' pages)
    locator: Section 2 (the left-or-right and real-or-random definitions used in the proof sketch)
---

Cipher feedback (CFB) mode turns a [block cipher](/block-cipher/) into a self-synchronizing [stream cipher](/stream-cipher/). It encrypts a shift register that holds the last $n$ bits of ciphertext, and XORs the first $s$ bits of the result into the next $s$ bits of plaintext. NIST defines CFB in SP 800-38A, Section 6.3, for segment sizes $s = 1$, $8$ and $128$ bits with AES (any $1 \le s \le n$ is allowed). Its special property: if ciphertext bits are lost or changed, decryption goes wrong for about one block and then recovers by itself.

**Notation.** $E_K$ is a block cipher with key $K$ and block length $n$ bits, $s$ is the segment size in bits, $P^\#_j$ and $C^\#_j$ are the $j$-th plaintext and ciphertext segments, $I_j$ is the $j$-th input block, $\mathrm{MSB}_s$ and $\mathrm{LSB}_s$ take the $s$ leftmost and rightmost bits. $\sigma$ is the number of block cipher calls in an attack.

## In plain words

CFB makes a stream of random-looking bits and XORs it with the message. The stream does not come from a counter. It comes from the ciphertext itself: the mode keeps the last 16 bytes of ciphertext in a window, encrypts the window, and uses the first bytes of the result to hide the next bytes of the message. Then the new ciphertext bytes slide into the window.

The receiver keeps the same window from the ciphertext it receives, so it makes the same stream. If a byte of ciphertext is lost on the line, the receiver's window is wrong only until 16 good bytes have passed through it. After that, both windows hold the same bytes again, and decryption is correct. This is why CFB is called self-synchronizing.

## When it applies

- **Character streams on a noisy or lossy line.** CFB-8 can encrypt one byte at a time and heals after the loss of whole bytes. This suited serial terminal links, the original use of the mode.
- **Only the forward cipher is available.** Encryption and decryption both use $E_K$, never $D_K$. So CFB works with a one-way keyed function and needs no inverse code.
- **No padding.** CFB-8 encrypts messages of any number of bytes. Full-block CFB needs whole segments, as specified, but many libraries also allow a short last segment.
- **Not when speed matters.** CFB-$s$ makes one cipher call for each $s$ bits, so CFB-8 is 16 times slower than CFB-128 with AES. Encryption is sequential. For new designs with no loss of data, use [CTR](/ctr-mode/) inside an AEAD mode.

## The template

```pseudo id=main
CFB-ENCRYPT(K, IV, P#[1 .. m], s)          ▷ each P#[j] has s bits; IV is n bits
L1  I ← IV                                 ▷ IV: unpredictable (SP 800-38A, Section 5.3)
L2  for j ← 1 to m do
L3      O ← E_K(I)
L4      C#[j] ← P#[j] ⊕ MSB_s(O)
L5      I ← LSB_(n − s)(I) ‖ C#[j]          ▷ shift the new ciphertext segment in
L6  return C#[1 .. m]
```

Decryption runs the same loop with $P^\#_j \leftarrow C^\#_j \oplus \mathrm{MSB}_s(O)$ in line L4, and it still shifts the *ciphertext* segment $C^\#_j$ into the register in line L5. So the input blocks $I_j$ are the same on both sides, and $C^\#_j \oplus \mathrm{MSB}_s(E_K(I_j)) = P^\#_j$. This proves that decryption inverts encryption. The holes are the cipher $E$, the segment size $s$ and the IV.

**Cost.** CFB-$s$ makes $\lceil \ell / s \rceil$ cipher calls for an $\ell$-bit message. Encryption is sequential, because $I_{j+1}$ needs $C^\#_j$. Decryption can run in parallel: each $I_j$ is known from the ciphertext alone. For $s = n$ the cost is one call per block, as in [CBC](/cbc-mode/).

**About the code.** The Python code of this page, with its own AES, supports $s = 8, 16, \ldots, 128$ (whole bytes); it does not implement CFB-1. It is for study only, it is not constant time, and it must not be used to protect real data. Use an AEAD from a FIPS 140 validated module or libsodium.

### Error propagation and self-synchronization

Let one bit of $C^\#_j$ change, and let $k = \lceil n / s \rceil$.

- $P^\#_j$ gets the same one-bit change, because line L4 is an XOR. So an attacker can flip chosen plaintext bits in the segment, as with any stream cipher.
- The wrong segment stays in the register for the next $k$ segments, so $P^\#_{j+1}, \ldots, P^\#_{j+k}$ are garbled (each wrong with high probability).
- From segment $j + k + 1$ on, the register holds only correct ciphertext, and decryption is correct again.

If whole segments are lost or inserted, the same argument holds: after $k$ correct segments the register of the receiver equals the register of the sender at that point. With CFB-8 and AES, $k = 16$: one lost byte garbles the next 16 bytes, and the rest is correct. With CFB-128, a lost byte is not healed, because the segment borders shift; only the loss of a whole 16-byte segment is healed. SP 800-38A, Appendix D, describes these properties.

### Security with a random IV

**Claim (full-block CFB, $s = n$).** Replace $E_K$ by a uniformly random function $f$. If the encryption algorithm draws each IV uniformly at random, then any adversary that sees the encryptions of chosen messages with $\sigma$ blocks in total distinguishes them from uniformly random strings of the same lengths with advantage at most $\sigma(\sigma - 1) / 2^{n+1}$.

*Proof.* The inputs to $f$ are the IV of each message and the ciphertext blocks $C_1, \ldots, C_{m-1}$ of each message, $\sigma$ inputs in all. Consider the inputs in the order in which they are formed. As long as all inputs so far are distinct, each output of $f$ is uniform and independent of everything before it, so each ciphertext block $C_j = P_j \oplus f(I_j)$ is uniform and independent of the plaintext, and the next input (a fresh IV or this $C_j$) is a fresh uniform block. A fresh uniform block equals one given earlier input with probability $2^{-n}$. By the union bound over the $\binom{\sigma}{2}$ pairs, some two inputs collide with probability at most $\sigma(\sigma - 1)/2^{n+1}$. If no collision happens, the whole transcript is uniform, exactly as in the random world. $\blacksquare$

With $E_K$ a [pseudorandom permutation](/pseudorandom-permutation/), the [PRP/PRF switching lemma](/prp-prf-switching-lemma/) adds $\mathrm{Adv}^{\text{prp}}_E + \sigma(\sigma - 1)/2^{n+1}$. Real-or-random security implies IND-CPA with a factor of 2 in the advantage (the reductions of Bellare, Desai, Jokipii and Rogaway). So CFB-128 with a random IV is IND-CPA secure up to about $\sigma^2 / 2^n$, the same order as CBC. The IV must be unpredictable, not only unique: as in CBC, an attacker who knows the next IV can choose a plaintext whose first ciphertext block equals a cipher input of an earlier message.

## Classic examples

### CFB-128, SP 800-38A F.3.13

With the AES-128 key `2b7e151628aed2a6abf7158809cf4f3c` and IV `000102030405060708090a0b0c0d0e0f`, the four plaintext blocks of Appendix F encrypt to `3b3fd92eb72dad20333449f8e83cfb4a`, `c8a64537a0b3a93fcde3cdad9f1ce58b`, `26751f67a3cbb140b1808cf187a4f4df` and `c04b05357c5d1c0eeac4c66f9ff7f2e6`. The first block is $P_1 \oplus E_K(IV)$, the same as in [OFB](/ofb-mode/) F.4.1. From the second block on the two modes differ, because CFB feeds back the ciphertext and OFB feeds back the cipher output.

### CFB-8, SP 800-38A F.3.7

The same key and IV with $s = 8$. Each row is one segment of one byte; the input block drops its first byte and appends the last ciphertext byte.

| $j$ | input block $I_j$ | $\mathrm{MSB}_8(E_K(I_j))$ | $P^\#_j$ | $C^\#_j$ |
|---|---|---|---|---|
| 1 | `000102030405060708090a0b0c0d0e0f` | `50` | `6b` | `3b` |
| 2 | `0102030405060708090a0b0c0d0e0f3b` | `b8` | `c1` | `79` |
| 3 | `02030405060708090a0b0c0d0e0f3b79` | `fc` | `be` | `42` |
| 4 | `030405060708090a0b0c0d0e0f3b7942` | `ae` | `e2` | `4c` |

The full ciphertext of the 18 bytes `6bc1bee22e409f96e93d7e117393172aae2d` is `3b79424c9c0dd436bace9e0ed4586a4f32b9`. In the test of this page, deleting the ciphertext byte at position 30 of an 80-byte message garbles the 16 decrypted bytes after it, and every later byte decrypts correctly.

### CFB in other systems

OpenPGP (RFC 4880, Section 13.9) uses a variant of full-block CFB with a zero IV and a random first block. Old terminal encryptors used CFB-8 or CFB-1 for their resistance to lost characters.

## Variations

- **CFB-1, CFB-8, CFB-64, CFB-128.** SP 800-38A gives example vectors for $s = 1$, $8$ and $128$ with AES. A smaller $s$ costs more cipher calls but heals at a finer grain.
- **Full-block CFB with a short last segment.** Libraries often encrypt a final partial block by truncating the last keystream block, so no padding is needed.
- **OpenPGP CFB.** A random prefix block plus a repeat of its last two bytes stands in for a random IV. The quick check of those two bytes leaked information in an attack by Mister and Zuccherato (2005).

## Pitfalls

- **Predictable IV.** CFB needs an unpredictable IV, like CBC. A counter IV is not enough (SP 800-38A, Section 5.3).
- **Expecting integrity.** A bit flip in the ciphertext flips the same plaintext bit. Use a MAC or an AEAD.
- **Decrypting with the wrong feedback.** The register must be fed the ciphertext segment in both directions. Feeding the plaintext on decryption gives wrong output after the first segment.
- **Choosing a small $s$ for speed.** CFB-8 makes 16 times as many cipher calls as CFB-128.

## Exercises

1. Show that CFB-$n$ decryption of $m$ blocks can run with span one block call in parallel.
2. In CFB-8 with AES, one ciphertext byte is inserted. How many plaintext bytes are wrong?
3. Show an attack on CFB-128 with a predictable IV, in the style of the CBC attack.
4. Compare the error propagation of CFB-128 and CBC for one flipped bit.

## References
