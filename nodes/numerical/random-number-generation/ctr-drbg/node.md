---
tag: D8PPZT
kind: algorithm
slug: ctr-drbg
name: CTR_DRBG
aliases:
- CTR-DRBG
- counter mode deterministic random bit generator
area: numerical/random-number-generation
level: advanced
summary: The NIST SP 800-90A generator that encrypts a counter V under a secret AES key and returns the blocks, then derives a new key and counter from the next blocks of the same stream.
model: word-ram
complexity:
  vars: {m: the number of 128-bit output blocks in one request}
  time: {worst: Θ(m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, cryptographic: true}
history:
  year: 2006
  people: [Elaine Barker, John Kelsey]
  note: CTR_DRBG appeared in the first edition of NIST SP 800-90 in June 2006; SP 800-90A Revision 1 (2015) made the counter field length an implementation choice and kept AES and three-key TDEA.
prereqs: [cryptographically-secure-prng, block-cipher, ctr-mode]
see_also: [advanced-encryption-standard, hash-drbg, hmac-drbg, dual-ec-drbg, pseudorandom-permutation, cbc-mac, entropy-source, chacha20]
sources:
  - paper: doi:10.6028/NIST.SP.800-90Ar1
    title: Elaine Barker and John Kelsey, NIST Special Publication 800-90A Revision 1, Recommendation for Random Number Generation Using Deterministic Random Bit Generators, June 2015
    locator: Section 9 (instantiate, reseed and generate functions and prediction resistance), Section 10.2 with Table 3 (CTR_DRBG parameters), Section 10.2.1 (CTR_DRBG and CTR_DRBG_Update), Sections 10.3.2 and 10.3.3 (Block_Cipher_df and BCC)
  - url: https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Algorithm-Validation-Program/documents/drbg/drbgtestvectors.zip
    title: NIST Cryptographic Algorithm Validation Program, DRBG test vectors (CAVS 14.3)
    locator: CTR_DRBG.rsp in the no_reseed, pr_false and pr_true sets, sections AES-128 use df, AES-256 use df and AES-256 no df, used by the tests
  - paper: doi:10.6028/NIST.FIPS.197
    title: National Institute of Standards and Technology, FIPS 197, Advanced Encryption Standard (AES), November 2001
    locator: Appendix B (cipher example) and Appendix C (example vectors for AES-128, AES-192 and AES-256), used by the tests
  - paper: "Matthew J. Campagna, Security bounds for the NIST codebook-based deterministic random bit generator, Cryptology ePrint Archive, Report 2006/379, 2006"
    locator: the distinguishing bound for the output of CTR_DRBG when the block cipher is modelled as an ideal cipher
  - paper: "Joanne Woodage and Dan Shumow, An analysis of NIST SP 800-90A, EUROCRYPT 2019, Lecture Notes in Computer Science 11477, Springer, 2019"
    locator: the analysis of CTR_DRBG with state compromise and reseeding, and the remarks on long requests and on the derivation function
  - paper: "Shaanan Cohney, Andrew Kwong, Shahar Paz, Daniel Genkin, Nadia Heninger, Eyal Ronen and Yuval Yarom, Pseudorandom black swans: cache attacks on CTR_DRBG, IEEE Symposium on Security and Privacy, 2020"
    locator: the cache side-channel recovery of CTR_DRBG state and output from table-based AES implementations
---

CTR_DRBG is the block cipher generator of NIST SP 800-90A and, with AES, the most widely deployed of the three approved deterministic random bit generators. Its state is an AES key and a 128-bit counter $V$. A request returns $\mathrm{AES}_K(V+1), \mathrm{AES}_K(V+2), \ldots$, which is [counter mode](/ctr-mode/) encryption of nothing. When the request is done, the generator encrypts a few more counter values and takes the new key and counter from them, so the key that produced the output is overwritten. Seeding either XORs full-entropy input directly into the state or first passes the input through a derivation function built from [CBC-MAC](/cbc-mac/). Security rests on AES being a [pseudorandom permutation](/pseudorandom-permutation/). With AES instructions in hardware it produces output at a few cycles per byte.

## In plain words

A block cipher with a secret key turns any 16-byte block into a 16-byte block that looks random to anyone without the key. The generator keeps a key and a counter. To make output, it adds one to the counter and encrypts it, adds one again and encrypts that, and so on, and hands out the encrypted blocks. After the request, it encrypts two or three more counter values and uses those blocks as the new key and the new counter. The old key is thrown away, so someone who steals the new key cannot decrypt anything to learn what was handed out before.

## The problem

Turn a seed with enough [min-entropy](/min-entropy/) into a long pseudorandom stream with the properties of a [CSPRNG](/cryptographically-secure-prng/), using a [block cipher](/block-cipher/), because AES is fast in hardware and is often the only cryptographic primitive available in a device or a validated module.

In the notation of generators, the state is $s = (K, V, c)$ with $c$ the request counter. The output of a request of $m$ blocks is $\mathrm{AES}_K(V+1) \| \cdots \| \mathrm{AES}_K(V+m)$, with the additions modulo $2^{128}$. The transition is the Update at the end of the request. The cost model counts block cipher calls.

**Parameters (SP 800-90A Rev. 1, Table 3).** With AES, $\mathit{blocklen} = 128$, $\mathit{keylen} \in \{128, 192, 256\}$, and $\mathit{seedlen} = \mathit{keylen} + \mathit{blocklen}$, so 256, 320 or 384 bits. The security strength equals $\mathit{keylen}$. At most $2^{19}$ bits are returned per request and at most $2^{48}$ requests are allowed between reseeds. Revision 1 lets an implementation increment only the rightmost $\mathit{ctr\_len}$ bits of $V$, with $4 \le \mathit{ctr\_len} \le \mathit{blocklen}$; this page and the CAVP vectors use $\mathit{ctr\_len} = \mathit{blocklen}$. Three-key TDEA is also allowed by Revision 1, with smaller limits.

## The algorithm

**Update** (CTR_DRBG_Update, Section 10.2.1.2). With provided data $d$ of exactly $\mathit{seedlen}$ bits: compute $\mathit{temp} = \mathrm{AES}_K(V+1) \| \mathrm{AES}_K(V+2) \| \cdots$ until it has at least $\mathit{seedlen}$ bits, keep the leftmost $\mathit{seedlen}$ bits, XOR them with $d$, and set $K$ to the leftmost $\mathit{keylen}$ bits and $V$ to the rightmost $\mathit{blocklen}$ bits of the result. For AES-128 this costs 2 block encryptions, for AES-192 and AES-256 it costs 3.

**Block_Cipher_df** (Section 10.3.2). To derive $\ell$ bits from a string $x$: form $S = L \| N \| x \| \texttt{80}$, padded with zero bytes to a multiple of 16 bytes, where $L$ and $N$ are the byte lengths of $x$ and of the output as 32-bit integers. With the fixed key $\texttt{00 01 02} \ldots$ (keylen bits), compute the CBC-MAC (called BCC) of $i \| 0^{96} \| S$ for $i = 0, 1, 2$ until there are $\mathit{keylen} + 128$ bits. Use them as a new key $K'$ and a block $X$, and output the leftmost $\ell$ bits of $\mathrm{AES}_{K'}(X), \mathrm{AES}_{K'}(\mathrm{AES}_{K'}(X)), \ldots$

**Instantiate.** Set $K \leftarrow 0^{\mathit{keylen}}$, $V \leftarrow 0^{128}$, compute the seed material, run Update with it, and set $c \leftarrow 1$. The seed material is:

- with the derivation function: $\mathrm{Block\_Cipher\_df}(e \| \nu \| \pi, \mathit{seedlen})$ for entropy input $e$, nonce $\nu$ and personalization string $\pi$;
- without it: $e \oplus \pi$, where $e$ must be exactly $\mathit{seedlen}$ bits of full entropy and $\pi$ is padded with zeros to $\mathit{seedlen}$ bits. No nonce is used.

**Reseed.** The seed material is $\mathrm{Block\_Cipher\_df}(e \| a, \mathit{seedlen})$ with the derivation function, or $e \oplus a$ (with $a$ padded) without it; run Update with it and set $c \leftarrow 1$.

**Generate.**

```pseudo id=main
CTR-DRBG-GENERATE(K, V, c, n, a)       ▷ state (K, V, c); n output bits; optional additional input a
L1  if c > reseed_interval then return "reseed required"
L2  if a is not empty then a ← DF(a) (or a padded with zeros); (K, V) ← UPDATE(a, K, V) else a ← 0^seedlen
L3  W ← empty string
L4  while |W| < n
L5      V ← (V + 1) mod 2^blocklen; W ← W ‖ AES(K, V)
L6  (K, V) ← UPDATE(a, K, V)
L7  c ← c + 1
L8  return the leftmost n bits of W, with the new state (K, V, c)
```

Line L2 uses $\mathrm{Block\_Cipher\_df}(a, \mathit{seedlen})$ when the derivation function is in use; without it, $a$ may have at most $\mathit{seedlen}$ bits. The same transformed $a$ is reused at line L6.

**Prediction resistance.** When it is requested, the generator first reseeds with fresh entropy and the additional input, and then runs the generate algorithm with empty additional input (SP 800-90A, Section 9.3.1).

## Example

AES-128 with the derivation function, entropy input $\texttt{00 01} \ldots \texttt{0f}$ (16 bytes), nonce $\texttt{10 11} \ldots \texttt{17}$ (8 bytes), no personalization string. The derivation function maps the 24 input bytes to the 32-byte seed material `a4a3b6bbe11b1903561ad74ed03294e68d303770e0efc8229d96f87b49653149`. Update from $K = 0$, $V = 0$ gives

- $K$ = `fc414a751b6529626065ca1974d5d1bc`, $V$ = `8eb8edbe80596bb06ebe3ac238d7cf31`.

The first request for 256 bits returns $\mathrm{AES}_K(V+1) \| \mathrm{AES}_K(V+2)$:

`aeaa089103d8100cfeb0046a2dab8522dc1b469cdffe2d17687ae47dcbf0c7dc`

and Update, using $\mathrm{AES}_K(V+3) \| \mathrm{AES}_K(V+4)$, sets $K$ = `b2d1545f96ae418df043c6058bf3c2a2` and $V$ = `63e38d58bf6b8ca0603dd13c996f85bd`, with $c = 2$. The second request returns

`d711149144ed895474622e98af6828a0e91f4858446e161a30bbd4dd1e4fc6ee`.

**Known answers.** The tests check the pure Python AES against the FIPS 197 examples and against OpenSSL, then reproduce twelve NIST CAVP vectors (AES-128 and AES-256, with and without the derivation function, reseeding, personalization string, additional input and prediction resistance) and one ACVP vector for AES-256 without the derivation function with two 512-byte requests, taken from the Go standard library's FIPS 140 tests.

## Correctness

Within a request the output blocks are encryptions under one key $K'$ of the consecutive counters $V'+1, \ldots, V'+m$, where $(K', V')$ is the state after line L2, and the new state is the XOR of $a$ with the encryptions of the next two or three counters. The proof page checks this against the specification and shows that all counter values encrypted under $K'$ in one call are distinct.

**Security (cited).** If AES is a pseudorandom permutation, then the blocks of one request are indistinguishable from distinct random blocks, and by the PRP/PRF switching lemma from independent uniform blocks, up to an advantage of about $q^2 / 2^{129}$ for $q$ blocks in total. The new key is derived from blocks that are never output, so it is independent of the output under the same assumption, which gives backtracking resistance between requests. Campagna (2006) bounded the distinguishing advantage in the ideal cipher model; Woodage and Shumow (2019) analysed the generator with state compromise and reseeding. The step from entropy input to a uniform key relies on Block_Cipher_df acting as a randomness extractor, or, without it, on the input having full entropy.

## Complexity

A request of $m$ blocks costs $m$ AES encryptions for the output, 2 or 3 for the Update, one key expansion, and, with additional input and the derivation function, a constant number of further encryptions and key expansions. So the time is $\Theta(m)$ block cipher calls and $\Theta(m)$ word operations. The state is the key, one block and a counter. With AES-NI, AES-128 counter mode runs at well under one cycle per byte in bulk, so in practice CTR_DRBG is limited by the per-request overhead, not by the output loop.

## Properties

- **Approved by NIST** for security strengths 128, 192 and 256 with AES.
- **Security from the PRP assumption on AES**, the most studied assumption in symmetric cryptography.
- **No repeated block within a request**, since a permutation applied to distinct counters gives distinct outputs. This is a tiny statistical bias (no collisions among 128-bit blocks), detectable only after about $2^{64}$ blocks, which the request and reseed limits keep far away.
- **Backtracking resistance between requests**, from the rekeying Update.
- **Two seeding modes.** With full-entropy input the derivation function can be omitted, which is cheaper and simpler.

## Variants and improvements

- **[Hash_DRBG](/hash-drbg/)** and **[HMAC_DRBG](/hmac-drbg/)** are the hash-based alternatives in the same standard.
- **Fast key erasure.** The same pattern of generating a block of output and then replacing the key with keystream is used by many operating system generators with AES or [ChaCha20](/chacha20/) in place of the DRBG, often with a different, simpler interface.
- **Without the derivation function.** Common in hardware generators whose conditioned entropy source already delivers full-entropy blocks, such as the Intel DRNG behind RDRAND, which is documented as an AES-based CTR_DRBG.
- **Shorter counter field.** Revision 1 allows incrementing only part of $V$, which suits hardware implementations; it shortens the distance before the counter wraps within the field.

## When to use it

Use it when a NIST-approved generator is required and AES is available, especially with hardware AES; it is the default DRBG in many FIPS 140 validated modules. For general application code, the operating system generator is the right interface.

## Pitfalls

- **Entropy is the real requirement.** The DRBG adds none. Without the derivation function, the input must have full entropy, which a raw noise source does not.
- **Compromise during a long request.** The key is the same for all blocks of one request, so an attacker who learns it during the request can recompute the blocks already returned. Cohney et al. (2020) combined this with a cache side channel on table-based AES to recover keys generated in TLS implementations. Use constant-time AES and keep requests short.
- **No additional input in the update.** Without additional input, Update XORs zero, so the new state is a pure function of the old state; this is fine cryptographically but means that mixing in fresh input requires either additional input or reseeding.
- **Duplicated state.** Virtual machine snapshots and `fork` copy the state, and both copies produce the same stream.
- **Details.** The byte order of $V$, the counter field length, the padding in Block_Cipher_df and the XOR versus derivation path for each mode must match the standard; the CAVP vectors distinguish all of these.

## Implementations

## History

CTR_DRBG was specified by Elaine Barker and John Kelsey in the first edition of NIST SP 800-90 (June 2006), drawing on the ANSI X9.82 drafts, and kept in SP 800-90A (2012) and Revision 1 (2015). Campagna (2006) gave security bounds for it. Intel's Digital Random Number Generator, introduced with the Ivy Bridge processors in 2012, used an AES-based CTR_DRBG as its deterministic stage. Woodage and Shumow (2019) gave a fuller analysis with state compromise, and Cohney, Kwong, Paz, Genkin, Heninger, Ronen and Yarom (2020) showed how side channels on AES turn the long-request weakness into practical attacks.

## References
