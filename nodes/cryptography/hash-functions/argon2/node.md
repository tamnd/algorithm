---
tag: 3Y7XXB
kind: algorithm
slug: argon2
name: Argon2
aliases:
- Argon2id
- Argon2i
- Argon2d
area: cryptography/hash-functions
level: advanced
summary: "The winner of the Password Hashing Competition (RFC 9106). It fills m blocks of 1 KiB in p lanes over t passes. Argon2id, the recommended type, mixes fixed and password-dependent block reads."
model: word-ram
complexity:
  vars: {m: the memory in blocks of 1 KiB, t: the number of passes, p: the number of lanes}
  time: {worst: Θ(m t), average: Θ(m t), best: Θ(m t)}
  space: {extra: Θ(m)}
properties: {deterministic: true}
history:
  year: 2015
  people: [Alex Biryukov, Daniel Dinu, Dmitry Khovratovich]
  note: "Won the Password Hashing Competition in July 2015; version 1.3 is specified in RFC 9106 (2021)."
prereqs: [memory-hard-function, blake2, password-hashing]
see_also: [scrypt, bcrypt, pbkdf2, pebbling-lower-bound, time-memory-tradeoff, timing-attack, proof-of-work, hkdf]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc9106"
    title: Alex Biryukov, Daniel Dinu, Dmitry Khovratovich and Simon Josefsson, RFC 9106, Argon2 Memory-Hard Function for Password Hashing and Proof-of-Work Applications, September 2021
    locator: Section 3 (the algorithm, H', indexing, G and P), Section 4 (parameter choice), Section 5 (test vectors), Section 7 (security considerations and trade-off attacks)
  - url: "https://www.cryptolux.org/images/d/d0/Argon2ESP.pdf"
    title: Alex Biryukov, Daniel Dinu and Dmitry Khovratovich, Argon2, New generation of memory-hard functions for password hashing and other applications, IEEE EuroS&P 2016
    locator: the design rationale, the three types, and the trade-off analysis
  - paper: "Joël Alwen and Jeremiah Blocki, Efficiently computing data-independent memory-hard functions, CRYPTO 2016, LNCS 9815"
    locator: parallel attacks that lower the cumulative memory cost of every data-independent MHF, including Argon2i
  - paper: "Jeremiah Blocki and Samson Zhou, On the depth-robustness and cumulative pebbling cost of Argon2i, TCC 2017"
    locator: the cumulative pebbling cost of one-pass Argon2i, an attack with advantage O(m^0.233) and an upper bound O(m^0.25) on any attack (as summarized in RFC 9106, Section 7.2)
  - url: "https://www.password-hashing.net/"
    title: Password Hashing Competition
    locator: the list of finalists and the announcement of Argon2 as the winner in July 2015
  - url: "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"
    title: OWASP Password Storage Cheat Sheet
    locator: section Argon2id (m = 19 MiB, t = 2, p = 1 as a minimum)
---

Argon2 is the memory-hard password hash that won the Password Hashing Competition in 2015 and was published as RFC 9106 in 2021. It fills a large table of 1 KiB blocks, each computed from the block before it and one earlier block, and makes $t$ passes over the table. Its three types differ only in how the earlier block is chosen: *Argon2d* picks it from the data, which resists trade-off attacks but leaks through cache timing; *Argon2i* picks it from a fixed pseudorandom sequence, which does not leak but is easier to attack with less memory; and *Argon2id*, the recommended type, uses the Argon2i rule for the first half of the first pass and the Argon2d rule after that.

**Notation.** $P$ is the password, $S$ the salt, $K$ an optional secret key, $X$ optional associated data, $T$ the tag length in bytes, $m$ the memory in KiB, $t$ the number of passes, $p$ the number of lanes, and $y$ the type (0 for d, 1 for i, 2 for id). The memory is a matrix $B[i][j]$ of $m' = 4p \lfloor m / 4p \rfloor$ blocks with $p$ rows (lanes) and $q = m' / p$ columns, split into 4 *slices* of $q / 4$ columns; a slice in one lane is a *segment*. $H^x$ is BLAKE2b with an $x$-byte output, $H'$ the variable-length hash built from it, $G$ the compression function on two 1 KiB blocks, $\oplus$ xor, $\|$ concatenation, and LE32 a 4-byte little endian integer. Cost is counted in calls to $G$ and in KiB of memory. The security model is the parallel random oracle model, with $G$ or $H$ treated as random; see Correctness for which bounds are tight.

## In plain words

Argon2 is a big table that must be filled in order. Each new block mixes the block just before it with one older block. To compute the last block you need, sooner or later, almost every block in the table, so an attacker who wants to save memory must recompute missing blocks again and again.

The choice of the older block is the key design decision. If it depends on the password, the pattern of memory reads can leak the password to someone who watches the cache. If it is fixed in advance, an attacker knows which blocks he will need and can throw the others away early. Argon2id starts with the fixed rule, while a spy could learn the most, and then switches to the password rule.

## The problem

Given $(P, S, K, X)$ and costs $(m, t, p)$, compute a tag of $T$ bytes such that any evaluation, by the defender or by an attacker with custom hardware, costs about $m$ KiB of memory held for about $m t$ calls to $G$, with only a small gain from trading memory for time. Lanes let a defender with $p$ cores fill the memory $p$ times faster without lowering this cost.

## The algorithm

```pseudo id=main
ARGON2(P, S, K, X, T, m, t, p, y)                       ▷ RFC 9106, Section 3.2
L1  H_0 ← H^64(LE32(p) ‖ LE32(T) ‖ LE32(m) ‖ LE32(t) ‖ LE32(0x13) ‖ LE32(y) ‖ LE32(|P|) ‖ P ‖ LE32(|S|) ‖ S ‖ LE32(|K|) ‖ K ‖ LE32(|X|) ‖ X)
L2  for each lane i: B[i][0] ← H'^1024(H_0 ‖ LE32(0) ‖ LE32(i)); B[i][1] ← H'^1024(H_0 ‖ LE32(1) ‖ LE32(i))
    for pass r ← 0 to t − 1, slice s ← 0 to 3, each lane i, each column j of the segment (skip j < 2 in pass 0):
L3      (J_1, J_2) ← the first 64-bit word of B[i][j−1] (data dependent), or the next word of the address blocks G(0, G(0, Z ‖ counter)) (data independent)
L4      l ← J_2 mod p (l ← i in pass 0, slice 0); W ← the blocks allowed for reference; z ← the (|W| − 1 − ⌊|W| · ⌊J_1² / 2^32⌋ / 2^32⌋)-th block of W
L5      B[i][j] ← G(B[i][j−1], B[l][z]) if r = 0, else G(B[i][j−1], B[l][z]) ⊕ B[i][j]
L6  C ← B[0][q−1] ⊕ … ⊕ B[p−1][q−1]; return H'^T(C)

H'^T(A)                                                 ▷ Section 3.3
L7  if T ≤ 64 return H^T(LE32(T) ‖ A); else V_1 ← H^64(LE32(T) ‖ A), V_k ← H^64(V_(k−1)), output 32 bytes of each V_k, then H^(T−32r)(V_r)

G(X, Y)                                                 ▷ Sections 3.5 and 3.6
L8  R ← X ⊕ Y; apply P to each of the 8 rows of R, then to each of the 8 columns; return the result ⊕ R
```

**The reference set $W$ (line L4).** Within one slice, segments of different lanes can be computed in parallel, so a block may reference any block of the other three slices that is already computed, in any lane, but only blocks of its own lane in the current slice. The block just before it is excluded (it is already an input), and when the new block is the first of its segment, the last block of $W$ in another lane is also excluded. In passes after the first, $W$ starts just after the current slice and wraps around. The map from $J_1$ makes recent blocks more likely: it approximates $|W| (1 - J_1^2 / 2^{64})$ and counts from the end.

**The data-independent addresses (line L3).** For Argon2i, and for Argon2id in slices 0 and 1 of pass 0, the words come from address blocks $G(0, G(0, Z \| \mathrm{LE64}(c) \| 0^{968}))$, where $Z$ holds the pass, lane, slice, $m'$, $t$ and $y$, each as a 64-bit little endian word, and $c = 1, 2, \ldots$ counts the address blocks of the segment. One address block gives 128 words, so 128 references.

**$P$ and $GB$.** $P$ is one round of BLAKE2b without the message: it works on 16 words of 64 bits as a $4 \times 4$ matrix, with $GB$ on the four columns and then the four diagonals. $GB$ is the BLAKE2b $G$ with the rotations 32, 24, 16 and 63, except that each addition $a + b$ becomes $a + b + 2 \cdot \mathrm{lo}(a) \cdot \mathrm{lo}(b)$, where lo takes the low 32 bits. The products make a hardware circuit deeper, while CPUs compute them almost for free.

## Example

The RFC 9106 vectors use $P = $ 32 bytes `01`, $S = $ 16 bytes `02`, $K = $ 8 bytes `03`, $X = $ 12 bytes `04`, $m = 32$, $t = 3$, $p = 4$ and $T = 32$.

So $m' = 32$ blocks in 4 lanes of $q = 8$ columns, and each segment has 2 columns. In pass 0, slice 0 holds the columns 0 and 1, which line L2 fills, so line L5 first runs in slice 1. Take $B[0][2]$, the first block of lane 0 in slice 1. If $l = 0$, $W$ is $B[0][0]$ only, since $B[0][1]$ is the previous block. If $l \ne 0$, $W$ is the finished columns 0 and 1 of lane $l$ minus the last one, so again only column 0. Either way $B[0][2] = G(B[0][1], B[l][0])$. For Argon2id, slice 1 of pass 0 still uses the data-independent rule, so $l$ comes from the address block of (pass 0, lane 0, slice 1), not from the data. Slices 2 and 3 of pass 0 and all of passes 1 and 2 use the data-dependent rule.

The published values for Argon2id (RFC 9106, Section 5.3):

| value | Argon2id |
|---|---|
| $H_0$ (first 8 bytes) | `2889de487eb42ae5` |
| block 0, word 0, after pass 0 | `6b2e09f10671bd43` |
| block 31, word 127, after pass 2 | `0b012846a40f346a` |
| tag | `0d640df58d78766c08c037a34a8b53c9d01ef0452d75b65eb52520e96b01e659` |

Here block 0 is $B[0][0]$ and block 31 is $B[3][7]$, the last block of the last lane. The same inputs give the Argon2d tag `512b391b…` and the Argon2i tag `c814d9d1…`. The code gives these values, and the tests check all three types.

## Correctness

Argon2 is deterministic, so the claims to prove are about security. The proofs file has the full arguments.

**Output.** The tag is $H'$ of the xor of the last column, and every block depends on $H_0$, which hashes all inputs with their lengths. So the tag is a function of all inputs, and two inputs that differ in any field give different $H_0$ except with a BLAKE2b collision. RFC 9106, Section 7.1, states that collision and preimage resistance are those of BLAKE2b.

**Memory hardness.** Model the computation as a graph: one node per block, with edges from $B[i][j-1]$ and $B[l][z]$ to $B[i][j]$. Computing the tag with little memory is a pebbling of this graph, and the cumulative memory complexity (CMC) of the function is at least the cumulative pebbling cost of the graph times the block size, in the parallel random oracle model.

- **Argon2i** has a graph fixed in advance. Alwen and Blocki (2016) showed that every such graph on $n$ nodes can be pebbled with CMC $O(n^2 \log \log n / \log n)$, so no data-independent MHF reaches the full $n^2$. For one pass of Argon2i, RFC 9106, Section 7.2, cites a best attack with advantage $O(m^{0.233})$ and a proven upper bound $O(m^{0.25})$ on any attack (Blocki and Zhou, 2017). These two bounds are close, but not tight.
- **Argon2d** reads at places fixed by the data, as in [scrypt](/scrypt/). The best known trade-off attack on $t$ passes, the ranking attack, lowers the time-area product by a factor of only 1.33 (RFC 9106, Section 7.2).
- **Argon2id** inherits both: the best known attack on one pass gains about 2.1, and on $t$ passes 1.33 (RFC 9106, Section 7.2).

So there are proven lower bounds for the idealized function, but the practical numbers above come from the best known attacks, not from tight proofs.

## Complexity

Argon2 makes $t m' - 2p$ calls to $G$ in line L5 (the first two columns of pass 0 come from line L2), plus 2 calls per 128 blocks for the address blocks of the data-independent parts. Line L2 makes $2p$ blocks of 1024 bytes with $H'$, at 31 BLAKE2b calls each. Each $G$ applies $P$ 16 times, and each $P$ runs $GB$ 8 times, so one $G$ costs 128 $GB$ calls; a BLAKE2b compression costs 96 calls of its own $G$. Memory is $m'$ KiB. With $p$ cores, the $p$ segments of a slice run in parallel, so the wall time drops by up to a factor $p$ while the total work stays the same. The RFC vectors make $3 \cdot 32 - 8 = 88$ calls to $G$ in line L5; the OWASP minimum, $m = 19456$ and $t = 2$, makes about 39,000.

## Properties

- Memory hard, with separate cost parameters: $m$ sets memory and $t$ sets time.
- Argon2i and the first half of the first pass of Argon2id have memory reads that do not depend on the password.
- Argon2d and the rest of Argon2id read at places set by the data, so they leak the access pattern through caches.
- Lanes give parallelism to the defender; the 4 slices are the points where lanes synchronize.
- Deterministic, with an output of any length from 4 bytes up.
- Keyed: the optional secret $K$ acts as a pepper, and $X$ binds context data.

## Variants and improvements

- **Versions.** RFC 9106 is version 1.3 (0x13). In version 1.0 (0x10), the passes after the first overwrote blocks; version 1.3 xors the new block into the old one, as line L5 shows. Old stored hashes with `v=16` need the old rule.
- **Balloon hashing** (Boneh, Corrigan-Gibbs and Schechter, 2016) is a data-independent MHF with a proof of memory hardness against sequential attacks; [NIST SP 800-63B](/password-hashing/) lists it with PBKDF2.
- **Depth-robust graphs.** After the attacks on Argon2i, Alwen, Blocki and Pietrzak proposed data-independent MHFs built on depth-robust graphs, with near-optimal CMC $\Omega(n^2 / \log n)$.
- **yescrypt, Catena, Lyra2 and Makwa** were the other PHC finalists given special recognition; see [password hashing](/password-hashing/).
- **[scrypt](/scrypt/)** is the older data-dependent MHF; Argon2d is similar in spirit but separates time from memory and adds lanes.

## When to use it

Use Argon2id for new password storage and for keys derived from passwords. RFC 9106, Section 4, gives two defaults: $t = 1$, $p = 4$, $m = 2$ GiB first, and $t = 3$, $p = 4$, $m = 64$ MiB when memory is short, both with a 16-byte salt and a 32-byte tag. OWASP gives $m = 19$ MiB, $t = 2$, $p = 1$ as a minimum for web logins. Use Argon2d only when no attacker can observe timing on the same machine, as in proof-of-work. Use Argon2i only where a standard asks for it, with $t \ge 3$.

## Pitfalls

- **Memory is in KiB.** Passing a size in bytes or in MiB gives a cost 1024 times off. Also, $m'$ is rounded down to a multiple of $4p$.
- **Lanes do not add security.** $p$ changes the order of the computation and the tag, but not the total memory or work; set it to the number of cores the defender has.
- **Argon2i with few passes.** RFC 9106, Section 7.2, says that to prevent the trade-offs of Alwen and Blocki, the number of passes must exceed $\log_2$ of the memory size minus 26.
- **Side channels on Argon2d.** Its memory reads depend on the password, so cache timing can let an attacker test guesses without the full memory.
- **Denial of service.** A server must not let clients choose large parameters, and must limit concurrent hashes, because each one holds $m$ KiB.
- **Encoding.** Stored hashes use the PHC string format, such as `$argon2id$v=19$m=65536,t=3,p=4$` followed by the salt and hash in base64 without padding; compare the whole string in constant time.

## Implementations

The Python code is for study only. It is not constant time and must not protect real data. It is also far too slow for real parameters. Use the `argon2-cffi` package, libsodium (`crypto_pwhash`, whose default is Argon2id) or the reference C code `phc-winner-argon2` instead.

The module is self-contained. `blake2b` is an unkeyed BLAKE2b from RFC 7693, `h_prime` is line L7, and `compress` is $G$ (line L8) with `_gb` and `_permute`. `pre_hash` is line L1, and `argon2` runs lines L2 to L6 for all three types. The tests check, against RFC 9106, Section 5, the pre-hashing digest $H_0$, the first word of block 0 and the last word of block 31 after each of the three passes, and the tag, for Argon2d, Argon2i and Argon2id. They also check BLAKE2b against RFC 7693, Appendix A, and against `hashlib.blake2b` as a second check, the lengths of $H'$, that a changed password, salt, cost, type or secret changes the tag, that one changed bit changes about half the output bits, and that bad parameters are rejected. The standard library has no Argon2, so there is no second check of the whole function.

## History

The Password Hashing Competition ran from 2013 to 2015, with 24 submissions and 9 finalists. Biryukov, Dinu and Khovratovich of the University of Luxembourg submitted Argon2, and it won in July 2015. Version 1.3 changed the later passes from overwriting to xor. In 2016 Alwen and Blocki showed that every data-independent MHF, Argon2i included, allows parallel attacks that lower its cumulative memory cost, which strengthened the case for the hybrid Argon2id. The CFRG published Argon2 as RFC 9106 in September 2021, with Argon2id as the type every implementation must support.

## References
