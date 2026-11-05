---
tag: GWRZNB
kind: algorithm
slug: fnv-hash
name: FNV hash
aliases:
- FNV-1a
- FNV-1
- Fowler-Noll-Vo hash
area: strings/string-hashing
level: intro
summary: A simple non-cryptographic byte-string hash that alternates XOR and multiplication by a fixed prime.
model: word-ram
complexity:
  vars: {n: the number of bytes of the input}
  time: {worst: Θ(n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1991
  people: [Glenn Fowler, Landon Curt Noll, Kiem-Phong Vo]
  note: Fowler and Vo sent the idea as reviewer comments to the IEEE POSIX P1003.2 committee in 1991, and Noll improved it in a later ballot round; RFC 9923 described it in 2026.
prereqs: [hash-function, hash-table]
see_also: [multiplicative-hashing, polynomial-rolling-hash, murmurhash, xxhash, siphash, avalanche-effect, anti-hash-tests, checksum]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc9923
    title: Landon Curt Noll, Kiem-Phong Vo, Donald E. Eastlake 3rd and Tony Hansen, The FNV Non-Cryptographic Hash Algorithm, RFC 9923, Informational (February 2026)
    locator: Section 1.4 (why FNV is not cryptographic), Section 2 (FNV-0, FNV-1 and FNV-1a), Sections 2.1 and 2.2 (the primes and the offset basis), Section 3 (XOR folding), Section 5 (the constants), Section 6.1 (inducing collisions) and Section 7 (history)
  - url: http://www.isthe.com/chongo/tech/comp/fnv/index.html
    title: Landon Curt Noll, FNV Hash (the web page of the FNV authors)
    locator: the description of FNV-1 and FNV-1a, the parameters for each size, and the history of the name
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.3, Hash functions (fixed hash functions against random families, and the multiplication method)
---

The FNV hash, named after Glenn Fowler, Landon Curt Noll and Kiem-Phong Vo, maps a byte string to a $w$-bit number with one XOR and one multiplication per byte. FNV-1a starts from a fixed value called the offset basis and, for each byte, XORs the byte into the state and multiplies the state by a fixed prime modulo $2^w$; FNV-1 does the two steps in the other order. It is short, fast on short keys, and used in many [hash tables](/hash-table/), compilers, routers and checksums. It has no key and no random choice, so it gives no bound on collisions: inputs chosen against it collide, and its low bits are weak unless the result is folded.

## In plain words

FNV reads a piece of data one byte at a time and keeps one number as its state. The state starts at a fixed value. For each byte, it mixes the byte into the low part of the number, then multiplies the number by a large fixed odd number and keeps only the last 32 or 64 binary digits. The final state is the hash.

The multiplication spreads the effect of each byte toward the high digits, so similar inputs usually get very different hashes. The method has no secret, so anyone can search for two inputs with the same hash and find them. FNV is good for spreading ordinary keys over a table, and not for protection against an attacker.

## The problem

Given a byte string $b = b[0] \cdots b[n-1]$ with $b[i] \in \{0, \ldots, 255\}$, compute a value $h(b) \in \{0, \ldots, 2^w - 1\}$ such that the same string always gives the same value, and distinct strings that occur in practice give distinct values most of the time. The alphabet is the 256 bytes; a text string is first encoded as bytes, for example in UTF-8. Indices are 0-based. The output width $w$ is 32, 64, 128, 256, 512 or 1024; this page uses 32 and 64. A hash table with $2^k$ buckets uses $k$ bits of the hash as the bucket index.

## The algorithm

Each width $w$ has a prime $P_w$ and an offset basis $O_w$ (RFC 9923, Section 5):

| $w$ | $P_w$ | $O_w$ |
|---|---|---|
| 32 | $16777619 = 2^{24} + 2^8 + \mathtt{0x93}$ | $2166136261 = \mathtt{0x811C9DC5}$ |
| 64 | $1099511628211 = 2^{40} + 2^8 + \mathtt{0xB3}$ | $14695981039346656037 = \mathtt{0xCBF29CE484222325}$ |

```pseudo id=main
FNV-1A(b[0 .. n−1], w)
L1  h ← O_w
L2  for i ← 0 to n − 1 do
L3      h ← h XOR b[i]
L4      h ← (h · P_w) mod 2^w
L5  return h
```

Line L3 changes only the low 8 bits of the state. Line L4 multiplies by $P_w$, which has few one bits: in machine arithmetic it is a single multiplication with the high part of the product thrown away. **FNV-1** swaps lines L3 and L4: it multiplies first and then XORs the byte. **FNV-0** is FNV-1 with the offset basis 0; it is obsolete, because a leading run of zero bytes leaves its state at 0. The offset basis is the FNV-0 hash of the 32-byte string `chongo <Landon Curt Noll> /\../\`, a mistyped copy of Noll's e-mail signature.

**The choice of the prime.** For $w = 2^s$ with $4 < s < 11$, the RFC takes $P_w$ as the smallest prime of the form $256^{\lfloor (5 + 2^s)/12 \rfloor} + 2^8 + b$ with $0 < b < 2^8$, four or five one bits in $b$, and one more condition modulo $2^{40} - 2^{24} - 1$. The rule is experimental: the RFC reports that such primes spread the hash values well, and gives no proof. What the analysis below uses is only that $P_w$ is odd.

**Other widths.** For a $k$-bit hash with $k$ not in the list, the RFC recommends XOR folding: compute the smallest FNV hash $t$ with more than $k$ bits, then take $(t \oplus (t \gg k)) \bmod 2^k$. A table index taken from the folded value depends on the high bits of $t$, which depend on all input bits.

## Example

The 32-bit FNV-1a hash of foobar, with every state written in hexadecimal:

| $i$ | $b[i]$ | after L3 | after L4 |
|---|---|---|---|
| | | | 0x811c9dc5 (L1) |
| 0 | f = 0x66 | 0x811c9da3 | 0xe30c2799 |
| 1 | o = 0x6f | 0xe30c27f6 | 0x6222e842 |
| 2 | o = 0x6f | 0x6222e82d | 0xa9f37ed7 |
| 3 | b = 0x62 | 0xa9f37eb5 | 0x3f5076ef |
| 4 | a = 0x61 | 0x3f50768e | 0x39aaa18a |
| 5 | r = 0x72 | 0x39aaa1f8 | 0xbf9cf968 |

The result 0xbf9cf968 is the test vector of RFC 9923 for foobar. The hash of the empty string is the offset basis 0x811c9dc5, and the 64-bit hash of foobar is 0x85944171f73967e8.

**Collisions.** The 32-bit FNV-1a hashes of costarring and liquid are both 0x5e4daa9d, and so are the hashes of declinate and macallums (0xe20e47d2). Because each step is a bijection on the state (see Properties), a collision survives any common suffix: altarage and zinke collide, and so do altarages and zinkes. Under FNV-1, creamwove and quists collide (0xc3e7b8c8), while their FNV-1a hashes differ.

**Weak low bits.** The bytes a = 0x61 and q = 0x71 agree in their low 4 bits. Since the low $k$ bits of the hash depend only on the low $k$ bits of the bytes, every string over {a, q} of a given length has the same low 4 bits. The 126 strings of lengths 1 to 6 over {a, q} fall into only 6 of the 16 buckets of a table indexed by the low 4 bits of the 32-bit FNV-1a hash, one bucket per length: 64 strings in bucket 11, 32 in bucket 8, 16 in bucket 9, 8 in bucket 2, 4 in bucket 7 and 2 in bucket 12. With XOR folding to 4 bits, the 64 strings of length 6 spread over the buckets, with at most 6 in one bucket.

## Correctness

FNV is a definition, so correctness means that the procedure computes the defined function and has the properties below. By induction on $i$, after $i$ passes of the loop $h$ equals the value of the recurrence $h_0 = O_w$, $h_{i+1} = ((h_i \oplus b[i]) \cdot P_w) \bmod 2^w$, so line L5 returns $h_n$. The structural properties all come from one fact: since $P_w$ is odd, it has an inverse modulo $2^w$, so for each byte $\beta$ the step $x \mapsto ((x \oplus \beta) P_w) \bmod 2^w$ is a bijection of $\{0, \ldots, 2^w - 1\}$. The full proofs are in the proof file below.

## Complexity

- **Time.** Lines L3 and L4 run once per byte, with one XOR and one multiplication of $w$-bit words: $\Theta(n)$ word operations in all. Every byte must be read, so no hash that depends on all bytes is faster in this model.
- **Space.** One $w$-bit word of state: $O(1)$.
- **In practice.** The multiplications form a chain, each waiting for the previous one, so FNV processes one byte per multiplication latency. Hashes that read 4 or 8 bytes per step, such as [MurmurHash](/murmurhash/) and [xxHash](/xxhash/), are several times faster on long inputs; on short keys such as identifiers, FNV is competitive.

## Properties

- **Deterministic and keyless.** The output depends only on the input. There is no random parameter, so no statement of the form "two fixed distinct strings collide with probability at most $\varepsilon$" holds; compare the [polynomial hash collision bound](/polynomial-hash-collision-bound/), which is a probability over a random base.
- **Not collision-free.** With $2^w$ values, any $2^w + 1$ distinct inputs contain a collision. If the outputs behave like random values, a collision is expected among about $\sqrt{\pi 2^w / 2}$ inputs, about 82 000 for $w = 32$ by the [birthday paradox](/birthday-paradox/); this is a heuristic, not a theorem about FNV.
- **Suffix extension.** Each step is a bijection of the state, so for every suffix $z$, $h(uz) = h(vz)$ if and only if $h(u) = h(v)$. One collision gives infinitely many.
- **Single-byte changes.** Two strings of the same length that differ in exactly one byte never collide, under FNV-1a and FNV-1.
- **Low bits.** Modulo $2^k$, XOR and multiplication depend only on the low $k$ bits of their operands. So $h \bmod 2^k$ depends only on $b[i] \bmod 2^k$ for all $i$. In particular bit 0 of the hash is bit 0 of $O_w$ XOR the parity of the number of odd bytes (RFC 9923, Section 1.4).
- **Sticky zero state.** If the state becomes 0, zero bytes keep it at 0, so the hash then ignores how many zero bytes follow.
- **Online.** The hash is computed in one pass with $O(1)$ state, and the hash of $uz$ follows from the state after $u$ and the bytes of $z$.

## Variants and improvements

- **FNV-1 and FNV-1a.** The two orders give different functions with the same cost. The RFC suggests FNV-1a for general use, because operational experience shows that it spreads short inputs better: in FNV-1a the last byte goes through a multiplication, while in FNV-1 it only changes the low 8 bits.
- **XOR folding.** $(t \oplus (t \gg k)) \bmod 2^k$ fixes the weak low bits for table sizes $2^k$. The RFC also suggests computing a hash of twice the needed width and folding it.
- **Wider hashes.** The RFC defines FNV for 128 to 1024 bits with larger primes. The weak low bits and the absence of a key remain.
- **A secret offset basis.** Starting from a secret random $O_w$ makes offline collision search harder, and RFC 9923, Section 6.1, says that this is adequate against an attacker who cannot observe collisions. It is not a keyed hash with a proven bound, and an attacker who can measure the time of the hash table can still collect colliding keys.
- **Mixing at the end.** Some libraries apply an extra mixing step to the final state, as in the finalizer of [MurmurHash](/murmurhash/), so that every output bit depends on every input bit.

## When to use it

Use FNV-1a for hash tables, symbol tables and caches whose keys are short strings that no attacker chooses, when simplicity matters more than speed on long inputs. Take the table index from the high bits or fold the hash; do not use the low bits of a raw FNV hash with a table of size $2^k$. For long inputs, use a hash that reads several bytes per step, such as [xxHash](/xxhash/). When keys may come from an attacker, as in a web server, use a keyed hash such as [SipHash](/siphash/) with a secret random key. For a probability bound on collisions, use a random member of a [universal hash family](/universal-hash-family/) or a polynomial hash with a random base. For integrity against tampering, use a [cryptographic hash function](/cryptographic-hash-function/).

## Pitfalls

- **Treating the hash as unique.** Two keys with equal FNV hashes are not known to be equal. A hash table must compare the keys; a cache or a database that uses the hash as the identity of the key will mix up colliding keys.
- **Low bits as the bucket index.** Keys whose bytes agree in their low bits, such as identifiers that differ only in the high bits of their characters, all fall into the buckets that their length chooses. Fold the hash or use a prime table size.
- **Confusing FNV-1 and FNV-1a.** The two give different values; a mismatch between a writer and a reader of stored hashes breaks lookups. The offset basis is also easy to mistype: the empty string must hash to the offset basis.
- **Arithmetic width.** In languages with unbounded integers, the product must be reduced modulo $2^w$ after each step, or the state grows without bound. Reducing only at the end gives the same value but costs time that grows with $n$.
- **Signed bytes.** In C, a plain `char` may be signed, and XOR with a negative value sets high bits of the state. Read the input as unsigned bytes.
- **Exposed hash tables.** With a known function, an attacker can compute many keys with one bucket offline and slow a table from $O(1)$ to $\Theta(n)$ time per operation: an [algorithmic complexity attack](/algorithmic-complexity-attack/).

## Implementations

## History

Glenn Fowler and Phong Vo sent the idea to the IEEE POSIX P1003.2 committee as reviewer comments in 1991, and Landon Curt Noll proposed an improvement in a later ballot round. People who tried the hash named it after the three authors in alphabetical order. The original version had offset basis 0 and is now called FNV-0; the nonzero offset basis came later, from a mistyped copy of Noll's e-mail signature, and FNV-1a, with the two steps in the other order, became the recommended form. RFC 9923, an informational RFC of February 2026 by Noll, Vo, Donald Eastlake and Tony Hansen, gives the constants for all sizes, reference C code and test vectors.

## References
