---
tag: 1CM1NZ
kind: algorithm
slug: scrypt
name: scrypt
aliases:
- ROMix
- SMix
area: cryptography/hash-functions
level: advanced
summary: "A memory-hard password hash: fill N blocks of 128r bytes in sequence, then read them back at password-dependent places. Less memory costs more time, so custom hardware gains little."
model: word-ram
complexity:
  vars: {N: the CPU and memory cost parameter, r: the block size parameter, p: the parallelization parameter}
  time: {worst: Θ(N r p), average: Θ(N r p), best: Θ(N r p)}
  space: {extra: Θ(N r)}
properties: {deterministic: true}
history:
  year: 2009
  people: [Colin Percival]
  note: "Designed for the Tarsnap backup service and presented at BSDCan 2009; published as RFC 7914 with Simon Josefsson in 2016."
prereqs: [pbkdf2, salsa20, memory-hard-function]
see_also: [argon2, bcrypt, password-hashing, pebbling-lower-bound, time-memory-tradeoff, hmac, proof-of-work, cryptographic-hash-function]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc7914"
    title: Colin Percival and Simon Josefsson, RFC 7914, The scrypt Password-Based Key Derivation Function, August 2016
    locator: Section 2 (parameters), Sections 3 to 6 (Salsa20/8 core, scryptBlockMix, scryptROMix, scrypt), Sections 8 to 12 (test vectors), Section 14 (security considerations)
  - url: "https://www.tarsnap.com/scrypt/scrypt.pdf"
    title: Colin Percival, Stronger key derivation via sequential memory-hard functions, BSDCan 2009
    locator: Definition 2 (sequential memory-hard), Theorem 1 (ROMix is sequential memory-hard in the random oracle model), Theorem 2 (4Nr Salsa20/8 calls and 1024Nr bits), Conjecture 1, Section 8 and Table 1 (hardware cost estimates)
  - paper: "Joël Alwen, Binyi Chen, Krzysztof Pietrzak, Leonid Reyzin and Stefano Tessaro, Scrypt is maximally memory-hard, EUROCRYPT 2017, LNCS 10212"
    locator: the main theorem, cumulative memory complexity of scrypt of order N^2 w in the parallel random oracle model
  - url: "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"
    title: OWASP Password Storage Cheat Sheet
    locator: section scrypt (N = 2^17, r = 8, p = 1 as a minimum)
---

scrypt is a password-based key derivation function that is *memory hard*: computing it with $N$ blocks of memory takes about $2N$ steps, and computing it with much less memory takes much more time. Colin Percival designed it in 2009 because PBKDF2 and bcrypt need almost no memory, so an attacker can put thousands of cheap cores on one chip and test passwords in parallel. Memory costs chip area, so a function that needs 128 MiB per guess makes each parallel core much more expensive. scrypt is RFC 7914, and it is used by Tarsnap, by several disk and wallet encryption tools, and as the proof of work of Litecoin.

**Notation.** $P$ is the password, $S$ the salt, $N$ the cost parameter (a power of 2), $r$ the block size parameter, $p$ the parallelization parameter, and $\mathit{dkLen}$ the output length in bytes. A *block* in ROMix has $128 r$ bytes and is made of $2r$ chunks of 64 bytes. $\oplus$ is xor and $\|$ is concatenation. Cost is counted in calls to the Salsa20/8 core and in bytes of memory. The security model is the parallel random oracle model, with BlockMix treated as a random oracle; the bound of Alwen et al. is tight up to constant factors.

## In plain words

scrypt first stretches the password and salt into a long block with [PBKDF2](/pbkdf2/). Then it makes a long list: each entry is a scramble of the one before. Then it walks $N$ steps more, and at each step it jumps to an entry of the list chosen by the current value, mixes that entry in, and scrambles again. Finally it compresses the result with PBKDF2 again.

The jumps cannot be predicted, because they depend on the values. So you must keep the whole list, or keep a few entries and rebuild the others when you need them, which costs time. Either way, the product of memory and time stays large, and that is what makes custom hardware expensive.

## The problem

Given $P$, $S$ and the cost parameters, compute a key $\mathit{DK}$ of $\mathit{dkLen}$ bytes such that each evaluation, by the user or by an attacker, needs about $128 r N$ bytes of memory for about $4 N r$ Salsa20/8 calls, with no cheaper way to trade one for the other. The function must be deterministic and must behave like a random function of $(P, S)$.

## The algorithm

```pseudo id=main
SCRYPT(P, S, N, r, p, dkLen)                           ▷ RFC 7914, Section 6
L1  B_0 ‖ … ‖ B_(p−1) ← PBKDF2-HMAC-SHA256(P, S, 1, 128·r·p)
L2  for i ← 0 to p − 1: B_i ← ROMIX(B_i, N)
L3  return PBKDF2-HMAC-SHA256(P, B_0 ‖ … ‖ B_(p−1), 1, dkLen)

ROMIX(B, N)                                            ▷ Section 5
L4  X ← B; for i ← 0 to N − 1: V_i ← X; X ← BLOCKMIX(X)
L5  for i ← 0 to N − 1: j ← INTEGERIFY(X) mod N; X ← BLOCKMIX(X ⊕ V_j)
L6  return X

BLOCKMIX(C_0 ‖ … ‖ C_(2r−1))                           ▷ Section 4, 64-byte chunks
L7  X ← C_(2r−1); for i ← 0 to 2r − 1: X ← SALSA20/8(X ⊕ C_i); Y_i ← X
L8  return Y_0 ‖ Y_2 ‖ … ‖ Y_(2r−2) ‖ Y_1 ‖ Y_3 ‖ … ‖ Y_(2r−1)
```

INTEGERIFY reads the last 64-byte chunk of $X$ as a little endian integer. Since $N$ is a power of 2, only its low bits matter. SALSA20/8 is the [Salsa20](/salsa20/) core with 8 rounds instead of 20 and with the input added back at the end. It maps 64 bytes to 64 bytes and is not a cryptographic hash, because it is not collision resistant (RFC 7914, Section 3). scrypt only needs it to mix well.

## Example

The first vector of RFC 7914, Section 12: $P$ and $S$ empty, $N = 16$, $r = 1$, $p = 1$, $\mathit{dkLen} = 64$.

1. Line L1 gives one block of 128 bytes, $B$ = `f7ce0b65 3d2d72a4 …`. RFC 7914, Section 10, gives this as the input of ROMix.
2. Line L4 stores $V_0 = B, V_1, \ldots, V_{15}$, with 16 BlockMix calls. The first one, BlockMix$(B)$ = `a41f859c 6608cc99 …`, is the vector of Section 9.
3. Line L5 makes 16 more BlockMix calls. The indices it reads are $j$ = 4, 2, 5, 7, 9, 1, 7, 2, 13, 2, 11, 10, 10, 15, 13, 2. These are computed by the code, not published; they show that the reads jump around and repeat.
4. ROMix returns `79ccc193 629debca …`, as in Section 10, and line L3 gives $\mathit{DK}$ = `77d65762 38657b20 3b19ca42 c18a0497 …`, as in Section 12.

**Trade-off.** With $N = 16$, full memory takes $2N = 32$ BlockMix calls. Storing every 4th entry (4 blocks instead of 16) takes 61 calls on this input, and storing only $V_0$ takes 145 calls. The time grows about as fast as the memory shrinks.

## Correctness

scrypt is a deterministic composition of PBKDF2, ROMix and PBKDF2, so the only claims to prove are about security. The output is pseudorandom if HMAC-SHA256 is a pseudorandom function, because line L3 is PBKDF2 keyed with $P$ on a salt that includes the output of ROMix.

**Memory hardness.** Percival's Theorem 1 says that in the random oracle model, any algorithm that stores $M$ of the $N$ values of line L4 needs about $N / M$ calls to rebuild each value read in line L5, so its space and time satisfy $S \cdot T = \Omega(N^2)$. The proofs file gives this argument.

The stronger measure is *cumulative memory complexity* (CMC), the sum of the memory in use over all steps of a parallel computation. It counts what an attacker with many cores really pays. Alwen, Chen, Pietrzak, Reyzin and Tessaro (2017) proved that in the parallel random oracle model the CMC of scrypt is $\Omega(N^2 w)$, where $w$ is the block size in bits. The honest algorithm uses about $N w$ bits for $2N$ steps, so its CMC is $O(N^2 w)$, and the bound is tight up to a constant. This is why the 2017 paper calls scrypt *maximally memory-hard*. The proof treats BlockMix as a random oracle; RFC 7914, Section 14, notes that the real assumption is that BlockMix with Salsa20/8 has no shortcuts.

## Complexity

ROMix makes $2N$ BlockMix calls, and each BlockMix makes $2r$ Salsa20/8 calls, so scrypt makes $4 N r p$ Salsa20/8 calls plus two PBKDF2 calls with one iteration each. Memory is $128 r N$ bytes for $V$, plus $128 r p$ bytes for $B$. The $p$ ROMix calls are independent and can run in parallel with $p$ times the memory, or one after another with the same memory. The OWASP minimum $N = 2^{17}$, $r = 8$, $p = 1$ uses 128 MiB and about $4.2$ million Salsa20/8 calls.

With $M$ stored blocks, the attacker's cost is about $N^2 / M$ BlockMix calls, so the area-time product stays about $N^2$. Percival's Conjecture 1 states the hardware form: a circuit needs an area-time product of at least about $1024 N^2 r^2 p$ times the cost of one bit of memory and one Salsa20/8 call.

## Properties

- Memory hard: less memory costs proportionally more time, see Correctness.
- Data dependent: the reads of line L5 depend on the password, so the memory access pattern leaks information through cache timing.
- Deterministic: the same $(P, S, N, r, p, \mathit{dkLen})$ always gives the same key.
- Parallel only through $p$: inside one ROMix, each step needs the previous one.
- Output of any length up to $(2^{32} - 1) \cdot 32$ bytes, from PBKDF2.

## Variants and improvements

- **Argon2.** The winner of the Password Hashing Competition. [Argon2d](/argon2/) is data dependent like scrypt, Argon2i is data independent, and Argon2id mixes the two. Argon2 separates the memory and time parameters and uses many lanes; it is now the usual first choice.
- **yescrypt.** Solar Designer's extension of scrypt, a PHC finalist with special recognition, and the default password hash of several Linux distributions.
- **Litecoin and other coins** use scrypt with $N = 1024$, $r = 1$, $p = 1$ as a proof of work. With only 128 KiB per hash, dedicated ASICs appeared anyway.
- **Data-independent MHFs**, such as Argon2i and Balloon hashing, avoid the cache timing leak at the cost of weaker bounds against parallel attacks; see [memory-hard function](/memory-hard-function/).

## When to use it

Use scrypt when you need a memory-hard key derivation function and Argon2id is not available, or to read data encrypted with it. RFC 7914 recommends $r = 8$ and $p = 1$; choose $N$ as large as the time and memory budget allows. For new systems, OWASP and RFC 9106 point to Argon2id. On a server, also limit the parameters that clients can request, because large values are a denial-of-service risk (RFC 7914, Section 14).

## Pitfalls

- **Small $N$.** With $N = 1024$ and $r = 1$, as in Litecoin, scrypt uses 128 KiB and gives little protection against GPUs.
- **Raising $p$ instead of $N$.** A larger $p$ adds time but not memory per lane, so it does not add memory hardness.
- **Cache timing.** The password-dependent reads of line L5 can leak through a shared cache. An attacker who sees the access pattern can test passwords with little memory.
- **Garbage collection attacks.** Values of $V$ left in freed memory can help an attacker who reads memory later; RFC 7914, Section 14, advises protected memory.
- **Confusing Salsa20/8 with a hash.** RFC 7914, Section 3, says it is not collision resistant; only the composition is claimed to be secure.

## Implementations

The Python code is for study only. It is not constant time and must not protect real data. It is also about a thousand times slower than C. Use `hashlib.scrypt`, libsodium (`crypto_pwhash_scryptsalsa208sha256`) or the `scrypt` package instead, or better [Argon2id](/argon2/).

The code follows RFC 7914 line by line. `salsa20_8` runs the four column and four row quarter rounds of Salsa20 four times. `block_mix` is lines L7 and L8, and `ro_mix` is lines L4 to L6. PBKDF2 with one iteration and its HMAC-SHA256 are written out, with SHA-256 from hashlib. `ro_mix_low_memory` stores only every $k$-th entry of $V$ and rebuilds the others on demand, to show the trade-off.

The tests check, against RFC 7914, the Salsa20/8 core (Section 8), BlockMix (Section 9), ROMix (Section 10), the first PBKDF2 vector (Section 11) and the first scrypt vector (Section 12). They also check that PBKDF2 with one iteration of the empty password and salt gives the ROMix input of Section 10, as the RFC says. The other three scrypt vectors of Section 12 need about half a million Salsa20/8 calls or more and take minutes in pure Python, so the code is not run on them. Instead, the code is compared with `hashlib.scrypt` on three small parameter sets. Further tests check that the low memory ROMix gives the same output with more calls, that a wrong password, salt or parameter changes the key, that one changed bit changes about half the output bits, and that bad values of $N$ are rejected.

## History

Percival designed scrypt for Tarsnap, his online backup service, and presented it at BSDCan in 2009, with estimates that it made hardware attacks on interactive logins 35 times more expensive than bcrypt and 260 times more than PBKDF2. Litecoin adopted it as a proof of work in 2011. The Password Hashing Competition (2013 to 2015) ran in part to find a successor, and chose Argon2. RFC 7914, by Percival and Josefsson, specified scrypt in 2016. In 2017 Alwen, Chen, Pietrzak, Reyzin and Tessaro proved that it is maximally memory hard in the parallel random oracle model.

## References
