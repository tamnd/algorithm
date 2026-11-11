---
tag: ZGS9FV
kind: technique
slug: ctr-mode
name: Counter mode
aliases:
- CTR
area: cryptography/symmetric-ciphers
level: core
summary: Encrypt distinct counter blocks to make a keystream and XOR it with the message. Parallel, random access, IND-CPA up to about σ²/2^n, but a repeated counter leaks the XOR of plaintexts.
prereqs: [block-cipher, nonce]
see_also: [prp-prf-switching-lemma, ofb-mode, cbc-mode, gcm-mode, ccm-mode, stream-cipher, one-time-pad, ctr-drbg]
sources:
  - url: "https://doi.org/10.6028/NIST.SP.800-38A"
    title: Morris Dworkin, NIST Special Publication 800-38A, Recommendation for Block Cipher Modes of Operation, Methods and Techniques, 2001
    locator: Section 6.5 (CTR), Appendix B (generation of counter blocks) and Appendix F.5 (CTR example vectors)
  - url: "https://cseweb.ucsd.edu/~mihir/papers/sym-enc.html"
    title: Mihir Bellare, Anand Desai, Eron Jokipii and Phillip Rogaway, A concrete security treatment of symmetric encryption, FOCS 1997 (full version on the authors' pages)
    locator: Section 5 of the full version (Proposition 9, Lemma 10 and Theorem 11 on the randomized XOR scheme; Lemma 12 and Theorem 13 on stateful CTR)
  - url: "https://www.rfc-editor.org/rfc/rfc3686"
    title: Russ Housley, RFC 3686, Using Advanced Encryption Standard (AES) Counter Mode With IPsec Encapsulating Security Payload (ESP), 2004
    locator: Section 4 (the counter block of a 32-bit nonce, a 64-bit IV and a 32-bit block counter)
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 3, the section on modes of operation (randomized counter mode is CPA-secure)
---

Counter (CTR) mode turns a [block cipher](/block-cipher/) into a stream cipher. It encrypts a sequence of distinct counter blocks and XORs the outputs with the message. NIST defines CTR in SP 800-38A, Section 6.5, and Appendix B of that document says how to form the counter blocks so that no block is ever used twice under one key. Every block of keystream depends only on its own counter, so encryption and decryption run in parallel and can start at any block. With distinct counters CTR is IND-CPA secure up to about $\sigma^2/2^n$, where $\sigma$ is the number of blocks; with a repeated counter it is a two-time pad.

**Notation.** $E_K$ is a block cipher with key $K$ and block length $n$ bits, $T_1, T_2, \ldots$ are the counter blocks, $O_j = E_K(T_j)$ the output blocks, $P_j$ and $C_j$ the plaintext and ciphertext blocks. $\sigma$ is the total number of blocks encrypted under one key, and $m$ is the number of bits of the counter field.

## In plain words

CTR mode counts: 1, 2, 3, and so on. It encrypts each number with the key, and the results form a long stream of random-looking bytes. The message is XOR-ed with this stream. The receiver counts the same way, makes the same stream, and XORs again to get the message back.

Because block 1000 needs only the number 1000, a computer can make many blocks at the same time, and a reader can decrypt block 1000 without the 999 blocks before it. The one rule is strict: a number must never be encrypted twice under the same key, in this message or in any other. If it is, two messages share stream bytes, and an attacker gets the XOR of the two messages with no key.

## When it applies

- **Any stream of data that needs confidentiality only, or that a MAC will protect.** CTR is the encryption part of [GCM](/gcm-mode/), [CCM](/ccm-mode/), [EAX](/eax-mode/) and SIV.
- **Parallel hardware and software.** All block calls are independent, so pipelines and vector units run at full speed.
- **Random access.** Disk images, media files and network protocols can decrypt one block from its index.
- **Precomputation.** The keystream does not depend on the data, so it can be computed before the data arrives.
- **Only the forward cipher.** CTR never calls $D_K$, so $E_K$ need not be a permutation: any [pseudorandom function](/pseudorandom-function/) works.
- **Not without a unique counter source.** If the sender cannot be sure that counters never repeat (for example after a reboot that resets state), use a misuse resistant AEAD such as SIV or AES-GCM-SIV.

## The template

```pseudo id=main
CTR(K, T₁, X[1 .. m])                     ▷ encryption and decryption are the same
L1  for j ← 1 to m do                      ▷ each iteration is independent
L2      T ← T₁ + (j − 1) mod 2^m in the low m bits     ▷ the counter block T_j
L3      O ← E_K(T)
L4      Y[j] ← X[j] ⊕ MSB_|X[j]|(O)          ▷ the last block may be partial
L5  return Y[1 .. m]
```

The holes are the cipher $E$ and the rule that makes $T_1$. Line L2 is the standard incrementing function of SP 800-38A, Appendix B.1: it adds one to the rightmost $m$ bits modulo $2^m$ and leaves the other $n - m$ bits alone. Decryption is the same procedure, because $(P_j \oplus O_j) \oplus O_j = P_j$. A final partial block uses only the leftmost bits of $O_m$, so there is no padding, and the ciphertext has the length of the plaintext.

**Cost.** $\lceil \ell / n \rceil$ cipher calls for an $\ell$-bit message, all independent, so the depth with $p$ processors is $\lceil \ell / (np) \rceil$ calls. Random access to block $j$ costs one cipher call.

**About the code.** The Python code of this page, with its own AES, is for study only. It is not constant time, and it must not be used to protect real data. It refuses to let the counter field wrap. Use AES-GCM from a FIPS 140 validated module, or ChaCha20-Poly1305 from libsodium.

### Counter block formats

SP 800-38A, Appendix B, gives the requirement: every counter block, in every message under one key, must be distinct. It suggests two ways to meet it.

- **One counter for all messages (B.2, first approach).** Keep one $n$-bit counter for the key. The first block of the next message is the block after the last block of the previous one. The key can encrypt at most $2^m$ blocks in total.
- **A nonce and a block counter (B.2, second approach).** Split the block into a per-message nonce of $n - m$ bits and a block counter of $m$ bits that starts at a fixed value. Messages must have distinct nonces, and each message can have at most $2^m$ blocks. A common split for $n = 128$ is a 96-bit nonce and $m = 32$.

Deployed formats follow the second approach. RFC 3686 (AES-CTR in IPsec ESP) uses a 32-bit nonce from the key exchange, a 64-bit per-packet IV and a 32-bit block counter that starts at 1. [GCM](/gcm-mode/) uses a 96-bit IV and a 32-bit counter with the function inc32, which increments only the last 32 bits. The danger in the second approach is the wrap: if a message has more than $2^m$ blocks, the counter comes back to its start and the keystream repeats inside the message. The code of this page raises an error instead.

### IND-CPA security, proved with the switching lemma

**Claim.** Let $E$ be a block cipher with $n$-bit blocks, and let CTR use counter blocks that are all distinct over every query (stateful CTR). Let $\mathcal{A}$ be an adversary in the left-or-right game that makes queries with $\sigma$ blocks in total. Then there are adversaries $\mathcal{B}_0, \mathcal{B}_1$ against $E$ as a [pseudorandom permutation](/pseudorandom-permutation/), each making $\sigma$ queries and running in about the time of $\mathcal{A}$, with

$$\mathrm{Adv}^{\mathrm{lor\text{-}cpa}}_{\mathrm{CTR}[E]}(\mathcal{A}) \le \mathrm{Adv}^{\mathrm{prp}}_E(\mathcal{B}_0) + \mathrm{Adv}^{\mathrm{prp}}_E(\mathcal{B}_1) + \frac{\sigma(\sigma - 1)}{2^n}.$$

Here $\mathrm{Adv}^{\mathrm{lor\text{-}cpa}} = \Pr[\mathcal{A} \Rightarrow 1 \mid \text{right}] - \Pr[\mathcal{A} \Rightarrow 1 \mid \text{left}]$: the oracle takes two messages of equal length and encrypts the left one in one world and the right one in the other.

**Proof.** Fix a world $b \in \{\text{left}, \text{right}\}$ and consider three games.

- $G_0^b$: the oracle uses $E_K$ with a random key $K$.
- $G_1^b$: the oracle uses a uniformly random permutation $\pi$ of $\{0,1\}^n$.
- $G_2^b$: the oracle uses a uniformly random function $\rho : \{0,1\}^n \to \{0,1\}^n$.

From $G_0^b$ to $G_1^b$. The adversary $\mathcal{B}_b$ has an oracle that is $E_K$ or $\pi$. It runs $\mathcal{A}$, answers each query by computing the counter blocks, calling its oracle on each one and XOR-ing the outputs with the message of world $b$, and outputs what $\mathcal{A}$ outputs. Its view is exactly $G_0^b$ or $G_1^b$, so $|\Pr[G_0^b \Rightarrow 1] - \Pr[G_1^b \Rightarrow 1]| \le \mathrm{Adv}^{\mathrm{prp}}_E(\mathcal{B}_b)$, with $\sigma$ oracle queries.

From $G_1^b$ to $G_2^b$. The games differ only in the oracle, which is queried on $\sigma$ inputs. By the [PRP/PRF switching lemma](/prp-prf-switching-lemma/), no algorithm that makes $\sigma$ queries tells a random permutation from a random function with advantage more than $\sigma(\sigma-1)/2^{n+1}$. So $|\Pr[G_1^b \Rightarrow 1] - \Pr[G_2^b \Rightarrow 1]| \le \sigma(\sigma-1)/2^{n+1}$.

In $G_2^b$. The counter blocks $T_1, \ldots, T_\sigma$ are distinct, so $\rho(T_1), \ldots, \rho(T_\sigma)$ are independent and uniform. Every ciphertext block is a message block XOR an independent uniform block, so it is uniform and independent of everything else, whatever $b$ is. The counter values sent with the ciphertexts do not depend on $b$ either. So $\Pr[G_2^{\text{left}} \Rightarrow 1] = \Pr[G_2^{\text{right}} \Rightarrow 1]$: this is Lemma 12 of Bellare, Desai, Jokipii and Rogaway.

Add the two worlds. By the triangle inequality the advantage is at most the sum of the four hop terms, which is the bound of the claim. $\blacksquare$

**Model and tightness.** The model is chosen-plaintext attack in the left-or-right sense, which implies [IND-CPA](/ind-cpa-security/) with one challenge. The reduction to the PRP term is tight: $\mathcal{B}_b$ makes $\sigma$ queries and loses no factor. The birthday term is tight up to a constant. An adversary asks to encrypt $\sigma$ blocks of zeros (left) or $\sigma$ random blocks (right). With a random permutation the left ciphertext blocks are outputs of $\pi$ on distinct inputs and never collide, while the right ones collide with probability about $\sigma^2/2^{n+1}$. So with $n = 128$, one key must encrypt far fewer than $2^{64}$ blocks. If $E$ is modeled as a PRF instead of a PRP, the birthday term goes away: Bellare, Desai, Jokipii and Rogaway prove $\mathrm{Adv}^{\mathrm{lor\text{-}cpa}}_{\mathrm{CTR}[F]} \le 2 \cdot \mathrm{Adv}^{\mathrm{prf}}_F$ (Theorem 13). For the randomized variant, which picks a fresh random start counter for each message, they prove a birthday term of $\mu_e(q_e - 1)/(L \cdot 2^l)$, where $\mu_e/L$ is the number of blocks and $q_e$ the number of queries (Theorem 11), and they show it is tight up to a factor of about 0.316 (Proposition 9). The random start can make the ranges of two messages overlap; the stateful counter cannot.

### The two-time pad when a counter repeats

Suppose two messages $P$ and $P'$ are encrypted under one key with the same initial counter block. Then they use the same output blocks, and on their common length

$$C \oplus C' = (P \oplus O) \oplus (P' \oplus O) = P \oplus P'.$$

This is the two-time pad: the attacker learns the XOR of the plaintexts without the key, and any known part of one message gives the same part of the other. A partial overlap is enough. If the second message starts with the counter block of block 2 of the first, then block 1 of the second shares its keystream with block 2 of the first. Bit flips are also free: flipping bit $i$ of $C_j$ flips bit $i$ of $P_j$ and nothing else. This is why every AEAD built on CTR adds a MAC, and why a nonce repeat in [GCM](/gcm-mode/) is a disaster.

### CTR runs in parallel

Block $j$ needs only $T_j$, and $T_j$ is $T_1$ plus $j - 1$ in the counter field. So $C_j = P_j \oplus E_K(T_1 + j - 1)$ can be computed alone, in any order, by any number of workers. The tests of this page decrypt each block of the SP 800-38A vector on its own and check that the result equals the sequential one. Compare [CBC](/cbc-mode/), whose encryption is a chain, and [OFB](/ofb-mode/), whose keystream is a chain.

## Classic examples

### SP 800-38A F.5.1

AES-128 key `2b7e151628aed2a6abf7158809cf4f3c`, initial counter block `f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff`, with $m = 128$ so the carry runs into the higher bytes.

| $j$ | counter block $T_j$ | output block $O_j$ | ciphertext $C_j$ |
|---|---|---|---|
| 1 | `f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff` | `ec8cdf7398607cb0f2d21675ea9ea1e4` | `874d6191b620e3261bef6864990db6ce` |
| 2 | `f0f1f2f3f4f5f6f7f8f9fafbfcfdff00` | `362b7c3c6773516318a077d7fc5073ae` | `9806f66b7970fdff8617187bb9fffdff` |
| 3 | `f0f1f2f3f4f5f6f7f8f9fafbfcfdff01` | `6a2cc3787889374fbeb4c81b17ba6c44` | `5ae4df3edbd5d35e5b4f09020db03eab` |
| 4 | `f0f1f2f3f4f5f6f7f8f9fafbfcfdff02` | `e89c399ff0f198c6d40a31db156cabfe` | `1e031dda2fbe03d1792170a0f3009cee` |

The plaintext blocks are the same four blocks as in every SP 800-38A example, starting with `6bc1bee22e409f96e93d7e117393172a`. The step from block 1 to block 2 shows the carry: `feff` becomes `ff00`.

### Nonce reuse in the tests

The tests encrypt `attack the north gate at dawn, then hold` and `retreat to the river before noon, all of` with the same key and initial counter, and check that the XOR of the ciphertexts equals the XOR of the plaintexts, so the first message gives the second at once.

## Variations

- **Randomized CTR.** Pick a random $T_1$ for each message and send it. This needs no state, but random starts can overlap, which adds a birthday term in the number of messages (Theorem 11 of BDJR).
- **CTR inside AEAD modes.** [GCM](/gcm-mode/) (inc32 from $J_0 + 1$), [CCM](/ccm-mode/) (counter blocks $A_i$ with a flags byte), [EAX](/eax-mode/) (the counter starts at an OMAC of the nonce) and SIV (the counter starts at the tag).
- **Stream ciphers with a counter input.** [ChaCha20](/chacha20/) and [Salsa20](/salsa20/) are keyed functions of a nonce and a block counter, used in the same way as CTR.
- **CTR-DRBG.** The NIST random bit generator [CTR-DRBG](/ctr-drbg/) runs a block cipher in counter mode to produce random bits.
- **Tweakable and wide-block modes.** For disk sectors, where no nonce space exists, use [XTS](/xts-mode/) instead.

## Pitfalls

- **Repeating a counter block.** Restarting a counter at zero after a reboot, using a fixed nonce, or using random 96-bit nonces for too many messages all repeat keystream. See [nonce](/nonce/).
- **Counter wrap inside a message.** With a 32-bit counter field, a message longer than $2^{32}$ blocks (64 GiB with AES) repeats its own keystream.
- **Mismatched increment.** One side increments the low 32 bits and the other the full 128 bits; the two agree until the low 32 bits overflow, then diverge.
- **No integrity.** CTR ciphertext is perfectly malleable: any chosen bit of plaintext can be flipped. Always add a MAC, or use an AEAD.
- **Too much data under one key.** The bound $\sigma^2/2^n$ limits AES to well under $2^{64}$ blocks per key; with a 64-bit block cipher such as [Triple DES](/triple-des/) the limit is about $2^{32}$ blocks.

## Exercises

1. Show that CTR with a fixed initial counter block for every message is not IND-CPA secure, with two oracle queries.
2. In randomized CTR with $q$ messages of $\ell$ blocks each and random starts, bound the probability that two messages use a common counter block.
3. Show that the CTR keystream for a random function is uniform even if the adversary picks the messages after seeing earlier ciphertexts, as long as the counters are distinct.
4. A sender uses a 96-bit random nonce and a 32-bit counter. For how many messages is the chance of a repeated nonce below $2^{-32}$?

## References
