---
tag: V4BHB1
kind: algorithm
slug: siphash
name: SipHash
aliases:
- SipHash-2-4
- SipHash-1-3
- HalfSipHash
area: cryptography/hash-functions
level: advanced
summary: "A fast keyed PRF for short inputs: 128-bit key, 64-bit output, ARX rounds on four 64-bit words. SipHash-2-4 is the default; runtimes use it to stop hash flooding of hash tables."
solves: [message-authentication]
model: word-ram
complexity:
  vars: {n: the message length in bytes, c: the compression rounds per word, d: the finalization rounds}
  time: {worst: Θ(c n + d), average: Θ(c n + d), best: Θ(c n + d)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2012
  people: [Jean-Philippe Aumasson, Daniel J. Bernstein]
  note: Aumasson and Bernstein presented SipHash at INDOCRYPT 2012, after the hash flooding attacks of December 2011. Python, Perl, Ruby, Rust and Linux adopted it.
prereqs: [pseudorandom-function, hash-table]
see_also: [xxhash, universal-hashing, hash-collision, anti-hash-tests, hmac, poly1305, chacha20, blake2]
sources:
  - paper: "Jean-Philippe Aumasson and Daniel J. Bernstein, SipHash: a fast short-input PRF, INDOCRYPT 2012, LNCS 7668, pages 489 to 508"
    locator: Section 2 (specification of SipHash-c-d), Section 3 (expected strength), Section 5 (preliminary cryptanalysis), Section 7 (defense against hash flooding), Appendix A (test values)
  - url: "https://github.com/veorq/SipHash"
    title: Jean-Philippe Aumasson and Daniel J. Bernstein, SipHash reference implementation and README
    locator: vectors.h (vectors_sip64, vectors_hsip32), halfsiphash.c, and the README sections Variants and Security
  - paper: "Scott A. Crosby and Dan S. Wallach, Denial of service via algorithmic complexity attacks, 12th USENIX Security Symposium, 2003"
    locator: the attack on hash tables by colliding keys, with examples on Perl and Squid
  - url: "https://fahrplan.events.ccc.de/congress/2011/Fahrplan/events/4680.en.html"
    title: Alexander Klink and Julian Wälde, Efficient denial of service attacks on web application platforms, 28th Chaos Communication Congress (28C3), December 2011
    locator: the talk on hash flooding of web application platforms through POST parameters, as cited in Section 7 of the SipHash paper
  - url: "https://peps.python.org/pep-0456/"
    title: Christian Heimes, PEP 456, Secure and interchangeable hash algorithm, 2013
    locator: the choice of SipHash-2-4 for str and bytes in Python 3.4
  - paper: "Christoph Dobraunig, Florian Mendel and Martin Schläffer, Differential cryptanalysis of SipHash, Selected Areas in Cryptography (SAC 2014), LNCS 8781"
    locator: differential characteristics for reduced SipHash; no attack on SipHash-2-4
---

SipHash is a keyed [pseudorandom function](/pseudorandom-function/) for short inputs, designed by Jean-Philippe Aumasson and Daniel J. Bernstein (INDOCRYPT 2012). It takes a 128-bit secret key and a message of any length and returns 64 bits. Its rounds use only additions, rotations and XORs on four 64-bit words. Its main use is as the hash function of a [hash table](/hash-table/) that stores keys chosen by an attacker: with a secret key per process, the attacker cannot predict which keys collide, so it cannot flood one bucket. Python, Perl, Ruby, Rust and the Linux kernel use SipHash or its variants for this.

**Notation.** $k = (k_0, k_1)$ the key as two 64-bit little-endian words, $m$ the message of $n$ bytes, $v_0, v_1, v_2, v_3$ the 64-bit state words, $\boxplus$ addition modulo $2^{64}$, $\lll$ left rotation, $\oplus$ XOR. SipHash-$c$-$d$ does $c$ rounds per message word and $d$ rounds at the end. $A$ an adversary with $q$ queries; the security goal is PRF security, and through it MAC security (EUF-CMA).

## In plain words

A hash table puts each key in a bucket chosen by a hash of the key. If many keys land in the same bucket, each lookup must walk a long list, and the table becomes as slow as a plain list. If the hash function is public and simple, an attacker can compute thousands of keys with the same bucket and send them to a server in one web request. The server then spends seconds or minutes on that request. This is hash flooding.

SipHash makes the hash depend on a secret random key that the program picks when it starts. Without the key, the attacker cannot tell which keys collide, so its keys spread over the buckets like random keys. Even watching the outputs does not help to find the key. It is also fast on the short strings that hash tables usually store.

## The problem

The goal is a PRF $F_k : \{0,1\}^{*} \to \{0,1\}^{64}$ that is as fast as possible on inputs of 8 to 100 bytes. Security means that an adversary who asks $F_k$ on adaptively chosen messages cannot tell it from a random function, except by guessing the key or the output. Collision resistance is not a goal: with a 64-bit output, collisions exist and an attacker with the key finds them after about $2^{32}$ tries. Hash tables need only that collisions cannot be predicted without the key.

## The algorithm

```pseudo id=main
SIPHASH-c-d(k, m)                       ▷ k has 16 bytes; Aumasson and Bernstein, Section 2
L1  k0, k1 ← the two little-endian 64-bit words of k
L2  v0 ← k0 ⊕ 736f6d6570736575;  v1 ← k1 ⊕ 646f72616e646f6d
    v2 ← k0 ⊕ 6c7967656e657261;  v3 ← k1 ⊕ 7465646279746573
L3  cut m into 64-bit little-endian words m_1 .. m_w, w = ⌊n/8⌋ + 1;
    the last word holds the last n mod 8 bytes, zero bytes, and n mod 256 in its top byte
L4  for i ← 1 to w do: v3 ← v3 ⊕ m_i;  do c SIPROUNDs;  v0 ← v0 ⊕ m_i
L5  v2 ← v2 ⊕ ff
L6  do d SIPROUNDs
L7  return v0 ⊕ v1 ⊕ v2 ⊕ v3

SIPROUND
    v0 ← v0 ⊞ v1;  v1 ← (v1 ⋘ 13) ⊕ v0;  v0 ← v0 ⋘ 32
    v2 ← v2 ⊞ v3;  v3 ← (v3 ⋘ 16) ⊕ v2
    v0 ← v0 ⊞ v3;  v3 ← (v3 ⋘ 21) ⊕ v0
    v2 ← v2 ⊞ v1;  v1 ← (v1 ⋘ 17) ⊕ v2;  v2 ← v2 ⋘ 32
```

The four constants spell `somepseudorandomlygeneratedbytes` in ASCII. A message word enters $v_3$ before the rounds and $v_0$ after them, so it is XORed in on both sides of the rounds. The length byte in the last word separates messages that differ only by trailing zero bytes. The constant `ff` in line L5 separates the last compression from the finalization.

**About the code.** The Python code is for study only, is not constant time, and must not protect real data. Use the SipHash of your language runtime or `crypto_shorthash` of libsodium. The code implements SipHash-$c$-$d$ for any $c$ and $d$, and HalfSipHash with a 32-bit output.

## Example

Appendix A of the paper: SipHash-2-4 with the key `00 01 ... 0f` and the 15-byte message `00 01 ... 0e`. Then $k_0$ = `0706050403020100` and $k_1$ = `0f0e0d0c0b0a0908`, and the message gives two words.

| step | $v_0$ | $v_1$ | $v_2$ | $v_3$ |
|---|---|---|---|---|
| L2 | `7469686173716475` | `6b617f6d656e6665` | `6b7f62616d677361` | `7b6b696e727e6c7b` |
| L4, $m_1$ = `0706050403020100` into $v_3$ | `7469686173716475` | `6b617f6d656e6665` | `6b7f62616d677361` | `7c6d6c6a717c6d7b` |
| after 2 SipRounds | `4d07749cdd0858e0` | `0d52f6f62a4f59a4` | `634cb3577b01fd3d` | `a5224d6f55c7d9c8` |
| $m_1$ into $v_0$ | `4a017198de0a59e0` | `0d52f6f62a4f59a4` | `634cb3577b01fd3d` | `a5224d6f55c7d9c8` |
| L4 with $m_2$ = `0f0e0d0c0b0a0908`, then L5 | `3c85b3ab6f55be51` | `414fc3fb98efe374` | `ccf13ea527b9f442` | `5293f5da84008f82` |
| L6, after 4 SipRounds | `f6bcd53893fecff1` | `54b9964c7ea0d937` | `1b38329c099bb55a` | `1814bb89ad7be679` |

The second word is the last seven bytes `08 ... 0e` and the length 15 = `0f` in the top byte. Line L7 XORs the four words and returns `a129ca6149be45e5`. As bytes in little-endian order this is `e5 45 be 49 61 ca 29 a1`, which is entry 15 of `vectors_sip64` in the reference `vectors.h`. The whole computation takes $2 \cdot 2 + 4 = 8$ SipRounds.

**Flooding, in the tests.** With the toy hash "sum of the bytes", all 2275 distinct orderings of the bytes of `abcdefg` that the test draws share one hash value, so all of them land in one of 1024 buckets. With SipHash under a random key, no bucket gets 15 of them.

## Correctness

SipHash is a function, so its correctness is that the code computes the specified function: the tests check the full intermediate state of Appendix A and the reference vectors. The security claims are as follows.

**Claim of the designers** (Section 3). SipHash-$c$-$d$ with $c \ge 2$ and $d \ge 4$ is expected to give the maximum PRF security possible for a function with a 128-bit key and a 64-bit output. So an attacker who searches $2^s$ keys succeeds with probability about $2^{s - 128}$, and a MAC forger who tries $2^s$ tags succeeds with probability about $2^{s - 64}$. The goal does not cover related keys or leaked state. This is a conjecture backed by cryptanalysis, not a reduction: SipHash is a dedicated design, and there is no proof from a smaller assumption.

**Cryptanalysis.** The paper (Section 5) and Dobraunig, Mendel and Schläffer (SAC 2014) studied differential characteristics of reduced versions. No attack on SipHash-2-4 is known.

**Why a PRF stops flooding, and a universal hash may not.** Crosby and Wallach (2003) proposed secret [universal hash](/universal-hashing/) functions. Universal hashing bounds the expected chain length for keys chosen independently of the secret. A hash table leaks bits of the hash through timing and through the order of iteration, and an attacker can choose keys after it sees that leak. Aumasson and Bernstein (Section 7) show that for a linear hash $m_0 k_0 + m_1 k_1 + \cdots$ one collision found by timing gives many more by linearity, and a few more give the key by Gaussian elimination. A PRF gives no such structure: even full outputs reveal nothing that predicts other outputs.

## Complexity

A message of $n$ bytes has $w = \lfloor n/8 \rfloor + 1$ words, and SipHash-$c$-$d$ makes $c w + d$ SipRounds. Each SipRound has 4 additions, 4 XORs and 6 rotations of 64-bit words. SipHash-2-4 on an 8-byte input makes $2 \cdot 2 + 4 = 8$ rounds; SipHash-1-3 makes $2 + 3 = 5$. The paper (Section 6) reports 1.44 to 1.96 cycles per byte for SipHash-2-4 on long inputs on 64-bit CPUs of 2012, and about 140 cycles for a 16-byte input on an AMD FX-8150. Extra space is the 32-byte state.

## Properties

- **A PRF and a MAC**, with a 64-bit tag. A 64-bit tag is short for a MAC on a network, so SipHash fits short-lived checks and hash tables better than long-term authentication.
- **Not collision resistant** and not meant to be a hash without a key.
- **Fast on short inputs**: no key schedule, no block padding beyond one word, few rounds.
- **ARX design**, like [ChaCha20](/chacha20/) and [BLAKE2](/blake2/), so it runs in constant time on common CPUs when written in C.

## Variants and improvements

- **SipHash-1-3.** One compression round and three finalization rounds. Python since 3.11 (`sys.hash_info.algorithm` is `siphash13`) and the Rust standard `HashMap` use it for speed. It is outside the designers' claim of $c \ge 2$, $d \ge 4$. No attack on it is published, but it has had much less analysis than SipHash-2-4, and its users accept a smaller margin because flooding needs less than full PRF security.
- **SipHash-4-8.** The conservative version of the paper, about half the speed of SipHash-2-4.
- **SipHash-128.** A 128-bit output, defined in the reference code, not in the paper.
- **HalfSipHash.** 32-bit words, a 64-bit key, and a 32-bit or 64-bit output, for 32-bit CPUs. The Linux kernel uses it in `hsiphash` for hash tables on 32-bit machines. Its key and state are half the size, so its security is at most about $2^{64}$ against key search and $2^{32}$ against guessing a 32-bit output, and it is not described in the paper and has had much less public cryptanalysis. The kernel documentation warns to use it only for hash tables.

## When to use it

Use SipHash, or the runtime's default keyed hash, for hash tables that store attacker-controlled keys: request parameters, JSON object keys, header names, and so on. Use it for short-lived MACs and for checks inside a system where a 64-bit tag is enough, as the Linux kernel does for some network values. Do not use it where collision resistance or a long tag is needed; use [HMAC](/hmac/), [BLAKE2](/blake2/) in keyed mode or [Poly1305](/poly1305/) there. Where no attacker chooses the keys, a faster non-cryptographic hash such as [xxHash](/xxhash/) is fine.

## Pitfalls

- **A fixed or public key.** A key compiled into the program, or printed in a log, removes all protection. Pick it at random at process start.
- **Only randomizing the seed of a weak hash.** Aumasson, Bernstein and Boßlet showed at 29C3 (December 2012) multicollisions for MurmurHash2, MurmurHash3 and CityHash that work for every seed. A seed is not a key unless the function is a PRF.
- **Leaking the iteration order.** Even with SipHash, iteration order shows bits of hash values; this is fine only because the function is a PRF.
- **Treating 64 bits as a strong MAC.** An attacker who can try $2^{32}$ tags succeeds with probability $2^{-32}$.
- **Byte order.** The reference output is the 64-bit value written little-endian; printing the integer in hex gives the bytes in reverse order, as in the example.

## Implementations

The Python code gives `sipround`, `message_words` (line L3), `siphash_state` (lines L1 to L6), `siphash` (line L7), `siphash_bytes` and `halfsiphash32`. The tests check the full state trace and output of Appendix A, entries 0, 1, 15 and 63 of `vectors_sip64` and of `vectors_hsip32` from the reference `vectors.h`, that SipHash-1-3 differs from SipHash-2-4, that a key with one changed bit gives a different output, the role of the length byte, the avalanche of about 32 of 64 bits per changed input bit, and the flooding demonstration above. The reference repository has no official vectors for SipHash-1-3, so the tests do not check SipHash-1-3 against published values.

## History

Bernstein's dnscache of 1999 already limited chain lengths "to protect against hash flooding" (Section 7 of the paper). Crosby and Wallach (USENIX Security 2003) studied algorithmic complexity attacks on hash tables in Perl, Squid and other systems. In December 2011 Klink and Wälde showed at 28C3 that the attack still worked on common web platforms: 500 KB of chosen POST data kept a PHP5 server busy for a full minute of CPU time. Python 2.7.3 and 3.2.3 (April 2012) added a randomized hash, but Aumasson and Bernstein recovered its 128-bit key from two outputs (Section 7 and Appendix B of the paper). They designed SipHash in 2012 as a fast secure PRF for this use. Python adopted SipHash-2-4 with PEP 456 in Python 3.4, and Perl, Ruby, Rust and the Linux kernel followed. Python changed to SipHash-1-3 in version 3.11.

## References
