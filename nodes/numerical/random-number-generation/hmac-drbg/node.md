---
tag: 8PDZN0
kind: algorithm
slug: hmac-drbg
name: HMAC_DRBG
aliases:
- HMAC-DRBG
- HMAC-based deterministic random bit generator
area: numerical/random-number-generation
level: advanced
summary: The NIST SP 800-90A generator that keeps an HMAC key K and a value V, outputs V = HMAC(K, V) repeatedly, and after each request replaces both K and V with HMACs of the old state.
model: word-ram
complexity:
  vars: {m: the number of HMAC output blocks in one request}
  time: {worst: Θ(m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, cryptographic: true}
history:
  year: 2006
  people: [Elaine Barker, John Kelsey]
  note: HMAC_DRBG appeared in the first edition of NIST SP 800-90 in June 2006 and is unchanged in substance in SP 800-90A Revision 1 (2015); RFC 6979 reused it in 2013 to derive deterministic signature nonces.
prereqs: [cryptographically-secure-prng, hmac, entropy-source]
see_also: [hash-drbg, ctr-drbg, dual-ec-drbg, pseudorandom-function, ecdsa, hkdf, min-entropy, sha-2]
sources:
  - paper: doi:10.6028/NIST.SP.800-90Ar1
    title: Elaine Barker and John Kelsey, NIST Special Publication 800-90A Revision 1, Recommendation for Random Number Generation Using Deterministic Random Bit Generators, June 2015
    locator: Section 9 (instantiate, reseed and generate functions and prediction resistance), Section 10.1 with Table 2 (security strengths and limits), Section 10.1.2 (HMAC_DRBG and HMAC_DRBG_Update)
  - url: https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Algorithm-Validation-Program/documents/drbg/drbgtestvectors.zip
    title: NIST Cryptographic Algorithm Validation Program, DRBG test vectors (CAVS 14.3)
    locator: HMAC_DRBG.rsp in the no_reseed, pr_false and pr_true sets, used by the tests
  - paper: doi:10.17487/RFC6979
    title: Thomas Pornin, RFC 6979, Deterministic Usage of the Digital Signature Algorithm (DSA) and Elliptic Curve Digital Signature Algorithm (ECDSA), August 2013
    locator: Section 3.2 (generation of k with HMAC_DRBG) and Appendix A.2.5 (ECDSA over P-256 test vectors, used by the tests)
  - paper: "Shoichi Hirose, Security analysis of DRBG using HMAC in NIST SP 800-90, Information Security Applications (WISA 2008), Lecture Notes in Computer Science 5379, Springer, 2009"
    locator: the proof that HMAC_DRBG output is pseudorandom and backtracking resistant if HMAC is a pseudorandom function
  - paper: "Joanne Woodage and Dan Shumow, An analysis of NIST SP 800-90A, EUROCRYPT 2019, Lecture Notes in Computer Science 11477, Springer, 2019"
    locator: the robustness analysis of HMAC_DRBG with state compromise and reseeding, and the remarks on long requests
  - paper: "Katherine Q. Ye, Matthew Green, Naphat Sanguansin, Lennart Beringer, Adam Petcher and Andrew W. Appel, Verified correctness and security of mbedTLS HMAC-DRBG, ACM Conference on Computer and Communications Security (CCS), 2017"
    locator: the machine-checked proof that a C implementation meets the specification and that the generator is pseudorandom under the PRF assumption
---

HMAC_DRBG is one of the three deterministic random bit generators approved in NIST SP 800-90A, and the one with the simplest security argument. Its state is an [HMAC](/hmac/) key $K$ and a value $V$, both as long as the hash output. To produce output it iterates $V \leftarrow \mathrm{HMAC}(K, V)$ and returns the successive values of $V$. After every request it replaces $K$ and $V$ by HMACs of the old state and any additional input, so the key that produced the output is gone. If HMAC is a [pseudorandom function](/pseudorandom-function/), the output is pseudorandom and earlier output stays secret after the state leaks. RFC 6979 uses the same construction to derive the secret nonce of [ECDSA](/ecdsa/) signatures from the private key and the message.

## In plain words

HMAC is a keyed scrambler: without the key, its outputs look random. The generator keeps a secret key and a running value. To make output it scrambles the running value with the key, hands the result out, scrambles it again, hands that out, and so on. When the request is finished it uses the scrambler once more to make a brand new key and a new running value, and forgets the old ones. Someone who steals the new key cannot run the scrambler backwards to recover the old key, so the output already handed out stays secret.

Seeding, reseeding and extra input all go through the same step, called Update, which mixes the new material into both the key and the value.

## The problem

Turn a seed with enough [min-entropy](/min-entropy/) into a long pseudorandom stream with the properties of a [CSPRNG](/cryptographically-secure-prng/): output indistinguishable from uniform, backtracking resistance after a state compromise, and recovery through reseeding. Do it with nothing more than HMAC with an approved hash function, so that the security reduces to a single standard assumption about HMAC.

In the notation of generators, the state is $s = (K, V, c)$ with $c$ the request counter. The output of a request of $m$ blocks is $V_1 \| \cdots \| V_m$ with $V_j = \mathrm{HMAC}(K, V_{j-1})$ and $V_0 = V$. The transition is the Update at the end of the request. The cost model counts hash compression calls.

**Parameters (SP 800-90A Rev. 1, Table 2).** $K$ and $V$ have $\mathit{outlen}$ bits, the hash output length (160 for SHA-1, 256 for SHA-256, 512 for SHA-512). The security strength is 128 for SHA-1, 192 for SHA-224 and SHA-512/224, and 256 for SHA-256, SHA-512/256, SHA-384 and SHA-512. At most $2^{19}$ bits are returned per request, and at most $2^{48}$ requests are allowed between reseeds.

## The algorithm

**Update** (HMAC_DRBG_Update, Section 10.1.2.2). With provided data $d$, which may be empty:

1. $K \leftarrow \mathrm{HMAC}(K, V \| \texttt{00} \| d)$, then $V \leftarrow \mathrm{HMAC}(K, V)$.
2. If $d$ is empty, stop.
3. $K \leftarrow \mathrm{HMAC}(K, V \| \texttt{01} \| d)$, then $V \leftarrow \mathrm{HMAC}(K, V)$.

**Instantiate.** With entropy input $e$, nonce $\nu$ and optional personalization string $\pi$: set $K \leftarrow \texttt{00} \cdots \texttt{00}$ and $V \leftarrow \texttt{01} \cdots \texttt{01}$ ($\mathit{outlen}/8$ bytes each), run Update with $d = e \| \nu \| \pi$, and set $c \leftarrow 1$.

**Reseed.** With fresh entropy $e$ and optional additional input $a$: run Update with $d = e \| a$, and set $c \leftarrow 1$.

**Generate.**

```pseudo id=main
HMAC-DRBG-GENERATE(K, V, c, n, a)      ▷ state (K, V, c); n output bits; optional additional input a
L1  if c > reseed_interval then return "reseed required"
L2  if a is not empty then (K, V) ← UPDATE(a, K, V)
L3  W ← empty string
L4  while |W| < n
L5      V ← HMAC(K, V); W ← W ‖ V
L6  (K, V) ← UPDATE(a, K, V)
L7  c ← c + 1
L8  return the leftmost n bits of W, with the new state (K, V, c)
```

**Prediction resistance.** When it is requested, the generator first reseeds with fresh entropy and the additional input, and then runs the generate algorithm with empty additional input (SP 800-90A, Section 9.3.1).

**RFC 6979.** To sign a message with hash $h$ under the private key $x$ of a group of prime order $q$, instantiate HMAC_DRBG with entropy input $x$ and nonce $h \bmod q$, each encoded in $\lceil \log_2 q \rceil$ bits rounded up to bytes; take the leftmost $\lceil \log_2 q \rceil$ bits of each generate call as a candidate $k$, and return the first candidate in $[1, q-1]$. A rejected candidate is followed by an Update with empty data, which is exactly what the generate call does at line L6.

## Example

SHA-256, entropy input $\texttt{00 01} \ldots \texttt{1f}$ (32 bytes), nonce $\texttt{20 21} \ldots \texttt{2f}$ (16 bytes), no personalization string. Instantiation gives

- $K$ = `345c7f099d0c4adce91379b6e2e03edfd4c2fa0b874e7a5b3cf24fb11f6ed4f1`
- $V$ = `976b4836a5b3d828293e26900371f2d49e5a11754c0a45c9cc4c8fe921014a03`

The first request for 256 bits returns $\mathrm{HMAC}(K, V)$ = `0ffb80875a3e9022a4941a3fa1b0d3611df14e1cf651a73ce9229b9f3ad56887`. Update with empty data then sets $K$ to a value beginning `55db9b6aff9a5b99` and $V$ to a value beginning `a12b960ce3ae61cc`, and $c = 2$. The second request returns `08767656d3e9669eb668d1e1f5b80d27bb1aee12ff719eeb83e3dce006718c16`.

**Known answers.** The tests reproduce eight NIST CAVP vectors (SHA-1, SHA-256 and SHA-512, with and without reseeding, personalization string, additional input and prediction resistance) and the two ECDSA nonces of RFC 6979, Appendix A.2.5, for P-256 with SHA-256: with private key `c9afa9d8…2b120f6721`, the message "sample" gives $k$ = `a6e3c57d…493d8aad60` and the message "test" gives $k$ = `d16b6ae8…caee0008e0`.

## Correctness

Within a request the output is the chain $V_1 = \mathrm{HMAC}(K', V')$, $V_j = \mathrm{HMAC}(K', V_{j-1})$, where $(K', V')$ is the state after line L2, and the request ends with an Update keyed by $K'$ that produces a fresh key. The proof page checks the pseudocode against the specification and shows that Update with empty data performs exactly one round.

**Security (Hirose 2008; Woodage and Shumow 2019).** Model $\mathrm{HMAC}(K, \cdot)$ with a secret uniform $K$ as a [pseudorandom function](/pseudorandom-function/). Then the outputs of a request are a PRF applied to the inputs $V', V_1, \ldots, V_{m-1}$; replacing the PRF by a random function makes them independent uniform strings as long as no input repeats, and a repeat among $m$ uniform $\mathit{outlen}$-bit values has probability at most $m^2 / 2^{\mathit{outlen}+1}$. The new key is the PRF applied to $V_m \| \texttt{00} \| a$, an input distinct from the output inputs because it is longer, so it too is uniform and independent of the outputs. This gives pseudorandomness and backtracking resistance between requests, with a hybrid argument across requests. The step that turns the entropy input into a uniform key requires an extra assumption on HMAC as a randomness extractor (or a random oracle), and that is where the published analyses differ in their models.

## Complexity

Each HMAC call on a short message costs four compression calls, two of which (the hashes of the padded key) can be cached per key. A request of $m$ blocks costs $m$ HMAC calls for the output and 2 or 4 more for the Update (4 more again for additional input), so $\Theta(m)$ HMAC calls and $\Theta(m)$ word operations for a fixed hash. Since the key changes once per request, the key schedule is amortized over the whole request. The state is two $\mathit{outlen}$-bit strings and a counter. HMAC_DRBG is roughly two to four times slower per byte than [Hash_DRBG](/hash-drbg/) with the same hash, because each output block takes two compression calls instead of one.

## Properties

- **Approved by NIST** for security strengths up to 256 bits.
- **Security from a PRF assumption on HMAC**, a standard assumption that is widely used elsewhere (TLS, [HKDF](/hkdf/)).
- **Backtracking resistance between requests**, because the key is replaced at the end of every request.
- **Prediction resistance** on request, by reseeding first.
- **Small and easy to implement.** The whole generator is the Update step and a loop; a formally verified implementation exists (Ye et al. 2017).

## Variants and improvements

- **[Hash_DRBG](/hash-drbg/)** is faster with the same hash but has a weaker, random-oracle based argument.
- **[CTR_DRBG](/ctr-drbg/)** uses a block cipher in counter mode and is faster on hardware with AES instructions.
- **RFC 6979 nonces.** Deterministic ECDSA and DSA use HMAC_DRBG to derive the per-signature secret from the private key and the message, which removes the catastrophic failure of reusing a random nonce.
- **[HKDF](/hkdf/)** is a related HMAC construction for one-shot key derivation; it has an explicit extract step and no reseeding.

## When to use it

Use it when a NIST-approved generator is required and only a hash function is available, or when the strongest standard-model argument among the SP 800-90A generators matters. It is a common choice in embedded TLS libraries such as mbedTLS. For deterministic signature nonces, RFC 6979 prescribes it. For general application code the operating system generator is the right interface.

## Pitfalls

- **Entropy is the real requirement.** The DRBG adds none, and its security strength cannot exceed the min-entropy of its seed.
- **Compromise during a long request.** The key $K'$ is the same for all blocks of one request, so an attacker who captures it in the middle of a request recovers the blocks already returned in that request. Backtracking resistance holds between requests only.
- **Duplicated state.** Virtual machine snapshots and `fork` copy the state, and both copies produce the same stream unless something is mixed in.
- **RFC 6979 is not a general generator.** Its entropy input is the private key and its nonce is the message hash; reusing that construction with low-entropy keys or attacker-chosen inputs outside signing is unsafe.
- **Details.** The separator bytes 00 and 01, the one-round Update for empty data and the initial values of $K$ and $V$ must match the standard; only known-answer tests catch errors here.

## Implementations

## History

HMAC_DRBG was specified by Elaine Barker and John Kelsey in the first edition of NIST SP 800-90 (June 2006), next to Hash_DRBG, CTR_DRBG and Dual_EC_DRBG, and was kept in SP 800-90A (2012) and Revision 1 (2015). Hirose (2008) proved it pseudorandom under the PRF assumption on HMAC. Thomas Pornin's RFC 6979 (2013) adopted it to derive deterministic DSA and ECDSA nonces. Ye, Green, Sanguansin, Beringer, Petcher and Appel (2017) verified the mbedTLS implementation in Coq, and Woodage and Shumow (2019) analysed it with state compromise and reseeding.

## References
