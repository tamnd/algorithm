---
tag: MYQDY5
kind: technique
slug: davies-meyer-construction
name: Davies-Meyer construction
aliases:
- Davies-Meyer compression
area: cryptography/hash-functions
level: advanced
summary: The compression function f(h, m) = E_m(h) XOR h from a block cipher E keyed by the message block. Collision resistant in the ideal cipher model; the core of MD5, SHA-1 and SHA-2.
prereqs: [compression-function, block-cipher, ideal-cipher-model]
see_also: [miyaguchi-preneel-construction, merkle-damgard-construction, merkle-damgard-theorem, sha-2, sha-1, md5, second-preimage-finding, pseudorandom-permutation]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 9, Section 9.4.1 (Algorithm 9.42, Remarks 9.44 and 9.45), Section 9.7 (fixed points of compression functions) and Section 9.8 (the notes on the origin of the scheme)
  - paper: "Bart Preneel, René Govaerts and Joos Vandewalle, Hash functions based on block ciphers, a synthetic approach, Advances in Cryptology, CRYPTO 1993, LNCS 773, Springer, 1994"
    locator: the 64 schemes and the 12 secure ones, among them Davies-Meyer
  - paper: "John Black, Phillip Rogaway and Thomas Shrimpton, Black-box analysis of the block-cipher-based hash-function constructions from PGV, Advances in Cryptology, CRYPTO 2002, LNCS 2442, Springer, 2002"
    locator: full version of May 31, 2002, Figure 1 (row 5, PGV scheme 25), Lemma 3.3 with its proof, Theorem 3.1, Theorem 6.1, and the lower bounds 0.3q(q-1)/2^n and 0.6q/2^n
  - paper: "Robert S. Winternitz, A secure one-way hash function built from DES, IEEE Symposium on Security and Privacy, 1984"
    locator: the security of the Davies-Meyer scheme against inversion in a black-box model of DES
  - paper: "Drew Dean, Formal aspects of mobile code security, PhD thesis, Princeton University, 1999"
    locator: the second preimage attack on long messages with fixed points of the compression function
  - paper: "John Kelsey and Bruce Schneier, Second preimages on n-bit hash functions for much less than 2^n work, Advances in Cryptology, EUROCRYPT 2005, LNCS 3494, Springer, 2005"
    locator: expandable messages, from fixed points as in Dean's attack or from multicollisions for any compression function
  - paper: doi:10.6028/NIST.FIPS.180-4
    title: NIST, FIPS 180-4, Secure Hash Standard (SHS), August 2015
    locator: Section 6.1.2 step 4 and Section 6.2.2 step 4, the addition of the old hash value after the rounds
  - paper: "Helena Handschuh and David Naccache, SHACAL, submission to the NESSIE project, 2000"
    locator: the SHA-1 compression function without its feed-forward, used as a block cipher
---

The Davies-Meyer construction makes a [compression function](/compression-function/) from a [block cipher](/block-cipher/) $E$. The message block is the key, the chaining value is the plaintext, and the chaining value is added again to the ciphertext:

$$f(h, m) = E_m(h) \oplus h.$$

The last XOR is the feed-forward. Without it, $f$ could be run backward. Davies-Meyer is one of the 12 schemes that Preneel, Govaerts and Vandewalle (1993) regarded as secure, and Black, Rogaway and Shrimpton (2002) proved that in the [ideal cipher model](/ideal-cipher-model/) a collision needs about $2^{n/2}$ queries to the cipher. All of MD4, MD5, SHA-1 and SHA-2 have a compression function of this form, with a cipher designed for hashing and with word-wise addition in place of XOR. Its one structural quirk is that every block has a fixed point that costs one decryption, and this is why the [Merkle-Damgard construction](/merkle-damgard-construction/) must put the length in the last block.

**Notation.** $E : \{0,1\}^k \times \{0,1\}^n \to \{0,1\}^n$ is a block cipher with $k$-bit keys and $n$-bit blocks, $E_m$ is the permutation for the key $m$, and $E_m^{-1}$ its inverse. $h$ is the $n$-bit chaining value and $m$ the $k$-bit message block. $q$ is the number of queries an adversary makes to $E$ and $E^{-1}$. The toy numbers below come from the code of this page, which uses a 16-bit toy cipher with 16-bit keys. The toy cipher is a permutation and nothing more; it is not a real cipher.

## In plain words

A block cipher scrambles a block under a key, but anyone who knows the key can unscramble it. A hash must not be reversible. Davies-Meyer uses the message block as the key, so the message picks which scrambling to apply to the current state. Then it XORs the old state into the result. To go backward from an output, you would need both the old state and the scrambled state, and they are tied together by the XOR, so knowing the key no longer helps. Because the message is the key, each block can be as long as the key, not as long as the cipher block.

## When it applies

- **You have a block cipher and need a hash.** Davies-Meyer gives an $n$-bit compression function with a $k$-bit block. Iterate it with Merkle-Damgard to hash messages of any length.
- **The cipher must be strong as a family of permutations.** The proof models $E$ as an ideal cipher: every key gives an independent random permutation. Weak keys, related-key properties or a complementation property can break the hash even if the cipher is fine for encryption.
- **The block size must be large.** Collisions of an $n$-bit compression function cost about $2^{n/2}$. With AES ($n = 128$) that is $2^{64}$, too little today. This is why SHA-256 uses its own cipher with a 256-bit block.
- **Rekeying must be cheap.** The key changes with every block, so a cipher with a slow key schedule makes a slow hash. The ciphers inside MD5 and SHA-2 have a very simple key schedule: the message expansion.

## The template

```pseudo id=main
DM(h, m)                                  ▷ h: n-bit chaining value, m: k-bit block
L1  y ← E_m(h)                            ▷ the message block is the key
L2  return y ⊕ h                          ▷ feed-forward of the chaining value

FIXED-POINT(m)                            ▷ an h with DM(h, m) = h
L3  return E_m^{-1}(0^n)
```

The holes are the cipher $E$ and the group operation of the feed-forward. MD4, MD5, SHA-1 and SHA-2 use word-wise addition modulo $2^{32}$ or $2^{64}$; FIPS 180-4 writes it as step 4 of the hash computation, $H_i^{(j)} = a + H_i^{(j-1)}$ and so on for each word. The rate is $k/n$ message bits per cipher call: 2 for SHA-256 ($k = 512$, $n = 256$), and $56/64$ for DES (HAC Remark 9.44). The cipher inside SHA-1 without the feed-forward was later proposed as a block cipher in its own right, SHACAL.

**Why the feed-forward.** Without line L2, $f(h, m) = E_m(h)$, and for any target $y$ and any block $m$, $h = E_m^{-1}(y)$ is a pseudo-preimage. With the key on the chaining value, $f(h, m) = E_h(m)$, the attacker picks $h$ and decrypts. The XOR ties the output to both the input and the result of the cipher, so neither direction of $E$ alone produces a chosen output.

**Line L3, fixed points.** $f(h, m) = h$ holds exactly when $E_m(h) \oplus h = h$, that is $E_m(h) = 0^n$. So $h = E_m^{-1}(0^n)$ is a fixed point, and every block $m$ has exactly one. For a random function, finding a fixed point takes about $2^n$ trials. This does not give a collision, because the attacker does not control $h$ in the iteration from the fixed $IV$. HAC (Section 9.7) lists fixed points as a certificational weakness of this kind.

### Collision resistance in the ideal cipher model

**Theorem (Black, Rogaway and Shrimpton 2002, Lemma 3.3).** Let $E$ be an ideal cipher with $n$-bit blocks, fix $h_0 \in \{0,1\}^n$, and let $\mathcal{A}$ make $q$ queries to $E$ and $E^{-1}$. The probability that $\mathcal{A}$ outputs $(h, m) \ne (h', m')$ with $f(h, m) = f(h', m')$, or $(h, m)$ with $f(h, m) = h_0$, is at most

$$\frac{q(q+1)}{2^n}.$$

*Proof.* Assume, as BRS do, that $\mathcal{A}$ never repeats a query, never asks $E^{-1}_m(y)$ after it learned $E_m(h) = y$ or the reverse, and has queried the inputs it outputs (this adds at most two queries). Query $i$ fixes one triple $(m_i, h_i, y_i)$ with $E_{m_i}(h_i) = y_i$; write $z_i = y_i \oplus h_i = f(h_i, m_i)$. Two different inputs $(h, m)$ have different triples, so a success means $z_i = z_j$ for some $i \ne j$, or $z_i = h_0$.

Let $C_i$ be the event $z_i \in \{h_0, z_1, \ldots, z_{i-1}\}$, a set of at most $i$ values. For a forward query $E_{m_i}(h_i)$, the answer $y_i$ is uniform over the at least $2^n - (i - 1)$ values not yet used as outputs of $E_{m_i}$, so $z_i = y_i \oplus h_i$ is uniform over a set of the same size. For a backward query $E^{-1}_{m_i}(y_i)$, the answer $h_i$ is uniform over the unused inputs, and again $z_i$ is uniform over at least $2^n - (i - 1)$ values. So $\Pr[C_i] \le i/(2^n - i)$. If $q \ge 2^{n/2}$, the bound is at least 1 and there is nothing to prove; otherwise $2^n - q \ge 2^{n-1}$, and

$$\Pr\Bigl[\bigcup_{i=1}^{q} C_i\Bigr] \le \sum_{i=1}^{q} \frac{i}{2^n - i} \le \frac{1}{2^n - q} \cdot \frac{q(q+1)}{2} \le \frac{q(q+1)}{2^n}. \qquad \square$$

The proof uses only that $y \mapsto y \oplus h$ and $h \mapsto y \oplus h$ are bijections, so it holds unchanged for word-wise addition, the form of the MD4 family.

By the [Merkle-Damgard theorem](/merkle-damgard-theorem/) in its black-box form (BRS Lemma 3.2), the iterated Davies-Meyer hash has the same bound, $\mathrm{Adv}^{\mathrm{coll}}(q) \le q(q+1)/2^n$ (BRS Theorem 3.1). The $h_0$ clause is the reason that the bound holds even for padding without the length. For inversion of the iterated hash at a random point, BRS Theorem 6.1 gives $q/2^{n-1}$. Both bounds are tight up to a constant: BRS Figure 1 gives attacks with collision probability $0.3q(q-1)/2^n$ and inversion probability $0.6q/2^n$ for this scheme. Winternitz (1984) first studied the one-wayness of the scheme in a black-box model of DES.

What the theorem does not give: second preimage resistance at the level $2^n$ for long messages (see Fixed points below), and indistinguishability from a random function, which the free fixed points rule out.

## Classic examples

### The toy cipher in numbers

With the 16-bit toy cipher of the code:

- **One call.** For $h = \texttt{0123}$ and $m = \texttt{BEEF}$: $E_m(h) = \texttt{51B2}$, and $f(h, m) = \texttt{51B2} \oplus \texttt{0123} = \texttt{5091}$.
- **A fixed point.** For $m = \texttt{BEEF}$, line L3 gives $h = E_m^{-1}(0) = \texttt{83CB}$. Then $E_m(\texttt{83CB}) = \texttt{0000}$ and $f(\texttt{83CB}, \texttt{BEEF}) = \texttt{83CB}$. The test repeats the block five times and the chain does not move.
- **No feed-forward.** For the target $\texttt{0F0F}$ and $m = 7$, $h = E_7^{-1}(\texttt{0F0F}) = \texttt{0427}$ is a preimage of $E_m(h)$. With the feed-forward, $f(\texttt{0427}, 7) = \texttt{0B28}$, not the target.
- **Birthday collisions.** For $n = 16$ the bound $q(q+1)/2^{16}$ passes $1/2$ at $q = 181$ (it is 0.503). A search over blocks from the chaining value $\texttt{0000}$ finds $f(\texttt{0000}, \texttt{003B}) = f(\texttt{0000}, \texttt{00BC}) = \texttt{0305}$ after 189 queries. From $\texttt{1111}$, $\texttt{2222}$ and $\texttt{3333}$ it takes 217, 353 and 63 queries, around the bound as expected.

### A fixed point of SHA-256

SHA-256's compression function is $f(H, Y) = E_Y(H) + H$ word by word, where $E$ is 64 rounds that can be run backward (see [SHA-2](/sha-2/)). For the all-zero block $Y = 0^{512}$, running the rounds backward from the all-zero state gives

$$H^* = \texttt{f8c9259fa4f5d787b570afa9219166a63636fc5c30ac289155d0cc4ffcb4b03d},$$

and $f(H^*, 0^{512}) = H^*$ (checked with a forward run). This took one backward evaluation. Since $H^*$ is not reachable from the SHA-256 initial value in any known way, it does not threaten SHA-256 itself.

### Long-message second preimages with fixed points

Dean (1999) turned fixed points into an attack on the iterated hash, even with MD strengthening. Compute $2^{n/2}$ fixed points $(h_j, m_j)$ and $2^{n/2}$ chaining values reached from $IV$ by one random block, and find a match by the [birthday paradox](/birthday-paradox/). The result is a prefix that reaches some $h_j$, after which the block $m_j$ can be repeated any number of times without changing the chain: an expandable message that can take any length. To attack a target message of $2^k$ blocks, find one block that leads from $h_j$ to one of the $2^k$ chaining values of the target, at a cost of about $2^{n-k}$, and stretch the expandable part so that the length matches. The total is about $2^{n/2} + 2^{n-k}$ calls of $f$ up to small factors, far below $2^n$. Kelsey and Schneier (2005) built expandable messages from multicollisions instead, so the attack works for any compression function, not only for those with easy fixed points. See [second-preimage finding](/second-preimage-finding/).

## Variations

- **Matyas-Meyer-Oseas (MMO).** $f(h, m) = E_{g(h)}(m) \oplus m$: the roles are swapped, the chaining value is the key, through a map $g$ to the key space. HAC calls Davies-Meyer its dual (Remark 9.44). See [Miyaguchi-Preneel](/miyaguchi-preneel-construction/).
- **Miyaguchi-Preneel.** $f(h, m) = E_{g(h)}(m) \oplus m \oplus h$, MMO with the chaining value also fed forward. Whirlpool uses it.
- **The 12 secure schemes.** BRS group 1 has 12 schemes with the same bound $q(q+1)/2^n$, among them DM ($f_5$), MMO ($f_1$) and MP ($f_3$); 8 more are secure only when iterated.
- **Double-block-length schemes.** To get a $2n$-bit output from an $n$-bit cipher, run two linked Davies-Meyer calls per block. Tandem DM and Abreast DM (Lai and Massey 1992) and Hirose's scheme (2006) are of this kind, for ciphers with a $2n$-bit key such as AES-256.
- **Addition in place of XOR.** The MD4 family uses word-wise addition modulo $2^{32}$ or $2^{64}$. The proof above is the same.

## Pitfalls

- **Complementation and weak keys.** DES has $E_{\bar m}(\bar h) = \overline{E_m(h)}$, so Davies-Meyer over DES has $f(\bar h, \bar m) = \overline{E_m(h)} \oplus \bar h = f(h, m)$: a collision for free. A cipher that is fine for encryption can still fail the ideal cipher assumption.
- **Short blocks.** The output is only $n$ bits, the cipher block size. A 64-bit or 128-bit block cipher gives a hash with collisions in $2^{32}$ or $2^{64}$ work.
- **Fixed points need MD strengthening.** Without the length in the last block, a fixed point at the $IV$ gives collisions $M$ and $m \| M$ at once. The [Merkle-Damgard theorem](/merkle-damgard-theorem/) page shows this in code.
- **The feed-forward is not optional.** Dropping it, or feeding forward something the attacker can cancel, makes $f$ invertible.
- **The ideal cipher model is a heuristic.** The bound is a proof in a model in which each key gives an independent random permutation. Real ciphers are fixed algorithms, and related-key properties matter here because the attacker chooses the keys.
- **For study only.** The code of this page uses a 16-bit toy cipher with no security, and it is not constant time. Use SHA-256 or SHA-3 from a vetted library.

## Exercises

1. Show that the scheme $f(h, m) = E_m(h) \oplus m$ (feed-forward of the key) is not collision resistant: find a collision with two queries to $E^{-1}$. (Hint: fix the output and two keys.)
2. In the proof, why does a backward query give a uniform $z_i$? What changes if the adversary may query $E^{-1}$ only, or $E$ only?
3. For SHA-256, how many backward evaluations does it take to list $2^{20}$ fixed points? Why does this not help to find a collision?
4. Compute the BRS bound for $n = 128$ and $q = 2^{60}$, and the number of queries at which it reaches $1/2$.

## References
