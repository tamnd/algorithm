---
tag: XX9PAT
kind: algorithm
slug: hash-drbg
name: Hash_DRBG
aliases:
- Hash-DRBG
- hash-based deterministic random bit generator
area: numerical/random-number-generation
level: advanced
summary: The NIST SP 800-90A generator that outputs Hash(V), Hash(V+1), ... from a secret seedlen-bit counter V, then moves V forward by a hash of V, a secret constant C and the request count.
model: word-ram
complexity:
  vars: {m: the number of hash output blocks in one request}
  time: {worst: Θ(m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, cryptographic: true}
history:
  year: 2006
  people: [Elaine Barker, John Kelsey]
  note: Hash_DRBG appeared in the first edition of NIST SP 800-90 in June 2006 and was kept unchanged in substance in SP 800-90A (2012) and its Revision 1 (2015).
prereqs: [cryptographically-secure-prng, cryptographic-hash-function, entropy-source]
see_also: [hmac-drbg, ctr-drbg, dual-ec-drbg, sha-2, min-entropy, true-random-number-generator, hkdf, random-oracle-model]
sources:
  - paper: doi:10.6028/NIST.SP.800-90Ar1
    title: Elaine Barker and John Kelsey, NIST Special Publication 800-90A Revision 1, Recommendation for Random Number Generation Using Deterministic Random Bit Generators, June 2015
    locator: Section 9 (instantiate, reseed and generate functions and prediction resistance), Section 10.1 with Table 2 (seedlen, reseed_interval and request limits), Section 10.1.1 (Hash_DRBG), Section 10.3.1 (Hash_df)
  - url: https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Algorithm-Validation-Program/documents/drbg/drbgtestvectors.zip
    title: NIST Cryptographic Algorithm Validation Program, DRBG test vectors (CAVS 14.3)
    locator: Hash_DRBG.rsp in the no_reseed, pr_false and pr_true sets, used by the tests
  - paper: "Joanne Woodage and Dan Shumow, An analysis of NIST SP 800-90A, EUROCRYPT 2019, Lecture Notes in Computer Science 11477, Springer, 2019"
    locator: the robustness analysis of Hash_DRBG in the random oracle model and the discussion of state compromise during long requests
  - paper: doi:10.6028/NIST.SP.800-90B
    title: Meltem Sönmez Turan, Elaine Barker, John Kelsey, Kerry A. McKay, Mary L. Baish and Mike Boyle, NIST Special Publication 800-90B, Recommendation for the Entropy Sources Used for Random Bit Generation, January 2018
    locator: the entropy sources that supply the entropy input
---

Hash_DRBG is one of the three deterministic random bit generators approved in NIST SP 800-90A. It keeps two secret numbers of $\mathit{seedlen}$ bits (440 for SHA-1 and SHA-256, 888 for SHA-384 and SHA-512): a value $V$ that changes on every request and a constant $C$ fixed at each seeding. A request for output returns $\mathrm{Hash}(V), \mathrm{Hash}(V+1), \ldots$, truncated to the requested length, and then moves $V$ forward to $V + \mathrm{Hash}(\texttt{03} \| V) + C + c$, where $c$ counts requests. Seeding and reseeding pass the [entropy input](/entropy-source/) through a hash-based derivation function. Its security rests on the hash function behaving like a random function, and it has no known weaknesses when used as specified.

## In plain words

Think of a secret counter. To produce random-looking bytes, hash the counter, then hash the counter plus one, and so on, and glue the results together. Nobody who does not know the counter can predict the hashes. After each request, jump the counter to a new secret place computed with a one-way hash, so that someone who later steals the counter cannot step back to the old place and recompute what was handed out before.

Fresh entropy is mixed in at the start and whenever the generator is reseeded, by hashing it together with the old state.

## The problem

Turn a short secret seed with enough [min-entropy](/min-entropy/) into a long stream of pseudorandom bits for keys, nonces and other secrets, with the requirements of a [CSPRNG](/cryptographically-secure-prng/): the output must be indistinguishable from uniform, compromise of the current state must not reveal earlier outputs (backtracking resistance), and reseeding with fresh entropy must restore security after a compromise (prediction resistance). The generator must work with any approved hash function and must be easy to validate against known answers.

In the notation of generators, the state is $s = (V, C, c)$, the transition is the update at the end of a request, and the output of a request of $m$ blocks is $g(s) = \mathrm{Hash}(V) \| \cdots \| \mathrm{Hash}(V + m - 1)$. The cost model counts hash compression calls, each a fixed number of word operations.

**Parameters (SP 800-90A Rev. 1, Table 2).** For SHA-1, SHA-224, SHA-512/224, SHA-256 and SHA-512/256, $\mathit{seedlen} = 440$; for SHA-384 and SHA-512, $\mathit{seedlen} = 888$. The security strength is 128 for SHA-1, 192 for SHA-224 and SHA-512/224, and 256 for the others. At most $2^{19}$ bits are returned per request, and the generator must be reseeded after at most $2^{48}$ requests.

## The algorithm

**Hash_df** (derivation function). To derive $\ell$ bits from a string $x$, concatenate $\mathrm{Hash}(\mathit{counter} \| \ell \| x)$ for $\mathit{counter} = 1, 2, \ldots$, with the counter as one byte and $\ell$ as a 32-bit integer, and keep the leftmost $\ell$ bits.

**Instantiate.** With entropy input $e$, a nonce $\nu$ and an optional personalization string $\pi$: $V \leftarrow \mathrm{Hash\_df}(e \| \nu \| \pi, \mathit{seedlen})$, $C \leftarrow \mathrm{Hash\_df}(\texttt{00} \| V, \mathit{seedlen})$, $c \leftarrow 1$.

**Reseed.** With fresh entropy $e$ and optional additional input $a$: $V \leftarrow \mathrm{Hash\_df}(\texttt{01} \| V \| e \| a, \mathit{seedlen})$, $C \leftarrow \mathrm{Hash\_df}(\texttt{00} \| V, \mathit{seedlen})$, $c \leftarrow 1$.

**Generate.** All additions are modulo $2^{\mathit{seedlen}}$, and $V$ is hashed as a $\mathit{seedlen}$-bit string.

```pseudo id=main
HASH-DRBG-GENERATE(V, C, c, n, a)      ▷ state (V, C, c); n output bits; optional additional input a
L1  if c > reseed_interval then return "reseed required"
L2  if a is not empty then w ← Hash(0x02 ‖ V ‖ a); V ← (V + w) mod 2^seedlen
L3  data ← V; W ← empty string
L4  while |W| < n
L5      W ← W ‖ Hash(data); data ← (data + 1) mod 2^seedlen
L6  H ← Hash(0x03 ‖ V)
L7  V ← (V + H + C + c) mod 2^seedlen
L8  c ← c + 1
L9  return the leftmost n bits of W, with the new state (V, C, c)
```

**Prediction resistance.** When the caller asks for prediction resistance, the generator first reseeds with fresh entropy and the additional input, and then runs the generate algorithm with empty additional input (SP 800-90A, Section 9.3.1).

The one-byte prefixes 00, 01, 02 and 03 separate the different uses of the hash function, so that no hash input in one role can equal a hash input in another.

## Example

SHA-256, entropy input $\texttt{00 01} \ldots \texttt{1f}$ (32 bytes), nonce $\texttt{20 21} \ldots \texttt{2f}$ (16 bytes), no personalization string. Instantiation gives a 55-byte $V$ beginning `b7fe6938cbd50598` and $C$ beginning `78722e72ef495f78`, with $c = 1$. The first request for 256 bits returns $\mathrm{Hash}(V)$:

`48f1bd755b6b0625155a440483340d86901795fb5f804e0e5e2720d8c1692912`

and moves $V$ to a value beginning `307097abbb1e6510` with $c = 2$. The second request returns

`27a3342a35d4bbb8e1dcd8ec0fc1a0d1a25cf906f0445d3b974dbddf4a3ba34e`.

**Known-answer tests.** The NIST CAVP vectors run instantiate, an optional reseed, and two generate calls, and publish the output of the second call. The tests check seven of them: SHA-1 and SHA-256 without reseeding, SHA-256 and SHA-512 with reseeding, each with and without personalization string and additional input, and one SHA-256 case with prediction resistance. For example, SHA-256 with entropy input `a65ad0f3…85e0fb`, nonce `8581f931…cbcc2e` and no other inputs returns 1024 bits beginning `d3e160c35b99f340`.

## Correctness

The generate algorithm returns $\mathrm{Hash}(V') \| \mathrm{Hash}(V' + 1) \| \cdots$ truncated to $n$ bits, where $V' = V$ or $V' = V + \mathrm{Hash}(\texttt{02} \| V \| a)$, and the new state is $V'' = V' + \mathrm{Hash}(\texttt{03} \| V') + C + c$. The proof page shows this, and two structural facts used by the security arguments:

- **No repeated hash input within a request.** The values $V', V'+1, \ldots, V'+m-1$ are distinct modulo $2^{\mathit{seedlen}}$ because $m \le 2^{19} < 2^{\mathit{seedlen}}$.
- **Domain separation.** Output blocks hash a string of exactly $\mathit{seedlen}$ bits, while the update and the additional-input step hash strings that are longer by at least 8 bits, so no output block reuses the input of an update hash.

**Security (cited).** If the hash function is modelled as a random oracle, Hash_DRBG meets the robustness notion of Dodis et al. as analysed by Woodage and Shumow (2019), with the caveat on long requests in Pitfalls. Intuitively: without knowledge of $V'$, every output block is the hash of an unknown $\mathit{seedlen}$-bit value; and the update adds $\mathrm{Hash}(\texttt{03} \| V')$, so recovering $V'$ from $V''$ requires inverting that relation. No reduction to a standard-model assumption on the hash function is known.

## Complexity

A request for $m$ output blocks (an output block has 160 to 512 bits, depending on the hash) costs $m$ hash calls for the output, one for the update, and one more if additional input is given, so $\Theta(m)$ hash calls and $\Theta(m)$ word operations for a fixed hash function. Each hash input of $\mathit{seedlen}$ bits fits in one compression call: 55 bytes plus 9 bytes of padding is one 64-byte SHA-256 block, and 111 bytes plus 17 bytes is one 128-byte SHA-512 block. The additions modulo $2^{\mathit{seedlen}}$ cost $O(1)$ words each. Instantiation and reseeding cost $O(1 + |e| / B)$ compression calls for an input of $|e|$ bits and block size $B$. The state is two $\mathit{seedlen}$-bit values and a counter. In practice, Hash_DRBG with SHA-256 produces output at roughly the speed of SHA-256, a few cycles per byte with hardware SHA instructions.

## Properties

- **Approved by NIST** for all security strengths up to 256 bits, with the parameter limits above.
- **Backtracking resistance between requests**, from the one-way update.
- **Prediction resistance** on request, by reseeding before generating.
- **Simple and fixed-length.** Only additions of large integers and hash calls; no keyed primitive is needed.
- **Fully deterministic** given the inputs, which is what makes known-answer validation possible.

## Variants and improvements

- **[HMAC_DRBG](/hmac-drbg/)** uses HMAC with a key that is replaced on every request; it has a cleaner security analysis under PRF assumptions on HMAC (Hirose 2008) and is the more common choice of the two hash-based generators, for example in deterministic ECDSA (RFC 6979).
- **[CTR_DRBG](/ctr-drbg/)** uses a block cipher, usually AES, in counter mode and is the fastest of the three on hardware with AES instructions.
- **With and without derivation.** Hash_DRBG always uses Hash_df; CTR_DRBG can omit its derivation function when full-entropy input is available.
- **Other hash functions.** SP 800-90A Rev. 1 lists SHA-1 and the SHA-2 family; NIST has since also allowed SHA-3 based instances through the general rule that approved hash functions may be used.

## When to use it

Use it when a NIST-approved deterministic generator is required (FIPS 140 validated modules) and a hash function is the primitive already available, for example in constrained devices without AES hardware. For general software, the operating system generator (getrandom, BCryptGenRandom) is the right interface; it is often built from one of these DRBGs or from [ChaCha20](/chacha20/).

## Pitfalls

- **Entropy is the real requirement.** The DRBG adds none. Its output is no harder to guess than its entropy input; a seed with 32 bits of min-entropy gives 32-bit security whatever the hash.
- **Compromise during a long request.** The output blocks of one request are hashes of consecutive counter values. An attacker who captures $V'$ in the middle of a request can recompute the whole request, including the blocks returned before the capture; backtracking resistance only covers earlier requests. Keep requests short when this matters.
- **Reusing the nonce and entropy.** Instantiating two generators with the same inputs gives the same output stream; virtual machine snapshots and forked processes reproduce the state unless the generator is reseeded or forked state is detected.
- **Bit-level details.** The counter byte, the 32-bit length field in Hash_df, the byte order of $V$ and the modular additions must all match the standard; known-answer tests catch errors that statistical tests never would.
- **Reseed counter.** Implementations that never check the counter, or that let it wrap, violate the specification's limits.

## Implementations

## History

Hash_DRBG was specified by Elaine Barker and John Kelsey in the first version of NIST SP 800-90 (June 2006), together with HMAC_DRBG, CTR_DRBG and Dual_EC_DRBG; it descends from earlier hash-based generators in ANSI X9.82 drafts. SP 800-90A (January 2012) and Revision 1 (June 2015) kept it, while Revision 1 removed Dual_EC_DRBG. Security analyses followed later than standardization: Kan (2007) reviewed the assumptions of the four generators, and Woodage and Shumow (2019) gave the first analysis of Hash_DRBG and HMAC_DRBG in a model with state compromise and reseeding.

## References
