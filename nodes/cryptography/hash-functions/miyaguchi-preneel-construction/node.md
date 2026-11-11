---
tag: A2T8E9
kind: technique
slug: miyaguchi-preneel-construction
name: Matyas-Meyer-Oseas and Miyaguchi-Preneel constructions
aliases:
- Miyaguchi-Preneel
- Matyas-Meyer-Oseas
area: cryptography/hash-functions
level: advanced
summary: "Compression functions keyed by the chaining value: MMO is E_g(h)(m) XOR m, and Miyaguchi-Preneel also XORs in h. Secure in the ideal cipher model; Whirlpool uses Miyaguchi-Preneel."
prereqs: [davies-meyer-construction, block-cipher]
see_also: [compression-function, merkle-damgard-construction, whirlpool, ideal-cipher-model, key-schedule, advanced-encryption-standard, merkle-damgard-theorem, sha-2]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 9, Algorithms 9.41 and 9.43, Remarks 9.44 and 9.45, the maps g and g~ of MDC-2 (Section 9.4.1 (ii)), Section 9.7.4 and Example 9.103, and the notes to Section 9.4
  - paper: "Bart Preneel, René Govaerts and Joos Vandewalle, Hash functions based on block ciphers, a synthetic approach, Advances in Cryptology, CRYPTO 1993, LNCS 773, Springer, 1994"
    locator: the 12 secure schemes, among them Matyas-Meyer-Oseas and Miyaguchi-Preneel
  - paper: "John Black, Phillip Rogaway and Thomas Shrimpton, Black-box analysis of the block-cipher-based hash-function constructions from PGV, Advances in Cryptology, CRYPTO 2002, LNCS 2442, Springer, 2002"
    locator: full version of May 31, 2002, Figure 1 (rows f1 and f3, PGV schemes 6 and 14), Lemma 3.3 and its proof for f1, Theorems 3.1, 5.1 and 6.1
  - paper: "Stephen M. Matyas, Carl H. Meyer and Jonathan Oseas, Generating strong one-way functions with cryptographic algorithm, IBM Technical Disclosure Bulletin 27(10A), 1985"
    locator: the scheme E_g(H)(x) XOR x, published with the Davies-Meyer scheme
  - paper: "Shoji Miyaguchi, Kazuo Ohta and Masahiko Iwata, 128-bit hash function (N-Hash), NTT Review 2(6), 1990"
    locator: the scheme with the chaining value fed forward as well, found independently of Preneel
  - paper: "Paulo S. L. M. Barreto and Vincent Rijmen, The Whirlpool hashing function, submission to NESSIE, 2000, revised 2003"
    locator: the compression function H_i = W[H_(i-1)](m_i) XOR H_(i-1) XOR m_i
---

The Matyas-Meyer-Oseas (MMO) and Miyaguchi-Preneel (MP) constructions make a [compression function](/compression-function/) from a [block cipher](/block-cipher/) $E$ by keying the cipher with the chaining value and encrypting the message block:

$$\text{MMO: } f(h, m) = E_{g(h)}(m) \oplus m, \qquad \text{MP: } f(h, m) = E_{g(h)}(m) \oplus m \oplus h.$$

Here $g$ maps an $n$-bit chaining value to a key of the cipher. MP is MMO with the chaining value fed forward too. Both are the dual of [Davies-Meyer](/davies-meyer-construction/), which keys the cipher with the message block, and both are among the 12 schemes that Preneel, Govaerts and Vandewalle (1993) regarded as secure. In the [ideal cipher model](/ideal-cipher-model/) both have the same collision bound $q(q+1)/2^n$ as Davies-Meyer (Black, Rogaway and Shrimpton 2002). Unlike Davies-Meyer, they have no fixed points that are easy to find. [Whirlpool](/whirlpool/) is a Miyaguchi-Preneel hash over a dedicated 512-bit cipher.

**Notation.** $E : \{0,1\}^\kappa \times \{0,1\}^n \to \{0,1\}^n$ is a block cipher with $\kappa$-bit keys and $n$-bit blocks. $g : \{0,1\}^n \to \{0,1\}^\kappa$ maps chaining values to keys. $h$ is the chaining value, $m$ an $n$-bit message block, and $q$ the number of queries to $E$ and $E^{-1}$. The toy numbers come from the code of this page, which uses a 16-bit toy cipher with 16-bit keys and $g$ the identity. The toy cipher is only a permutation; it is not a real cipher.

## In plain words

The state picks the key, and the message is the text that gets encrypted. If the output were only the ciphertext, anyone who knows the state could decrypt to find a message for any target. So the message is XORed onto the ciphertext (MMO), and in MP the state is XORed on as well. The extra XOR of MP means that two different states can never give the same output for the same block, even when the map $g$ from states to keys throws away some bits.

## When it applies

- **You have a block cipher with a key as long as the block.** Then $g$ can be the identity, as in Whirlpool ($\kappa = n = 512$) or AES-128 ($\kappa = n = 128$). Each call hashes $n$ message bits, so the rate is 1.
- **The key is shorter or has bad values.** Then $g$ must squeeze the chaining value into a key and avoid weak keys. HAC describes the maps of MDC-2 for DES: delete every eighth bit to get 56 bits, and set bits 2 and 3 to 10 for $g$ (to 01 for the second map $\tilde g$). All weak and semi-weak DES keys have bit 2 equal to bit 3, so they never occur, and the complementation property of DES is also blocked (HAC Example 9.103).
- **Keys from the chaining value are an advantage.** In Davies-Meyer the attacker chooses every key, since the key is the message. Here the key is a chaining value, which the attacker controls only through the hash itself. This makes related-key and weak-key properties of the cipher harder to use.
- **Rekeying must be cheap.** The key changes with every block, as in Davies-Meyer. Whirlpool pays for this: its key schedule is the cipher itself, so each block costs two runs of the round function.

## The template

```pseudo id=main
MP(h, m)                                  ▷ h: n-bit chaining value, m: n-bit block
L1  k ← g(h)                              ▷ map the chaining value to a key
L2  c ← E_k(m)                            ▷ the message block is the plaintext
L3  return c ⊕ m ⊕ h                      ▷ MMO returns c ⊕ m only

ITERATE(f, IV, m_1 … m_t)                 ▷ the Merkle-Damgard chain
L4  h ← IV
L5  for i ← 1 to t
L6      h ← f(h, m_i)
L7  return h
```

Lines L1 and L2 are the same in both schemes. MMO stops at $c \oplus m$; MP adds $h$ on line L3. The message must be padded with [MD strengthening](/merkle-damgard-construction/) before line L4, and the [Merkle-Damgard theorem](/merkle-damgard-theorem/) then turns collision resistance of $f$ into collision resistance of the hash.

### The map g

When $\kappa = n$ and the cipher has no weak keys, $g$ is the identity; Whirlpool uses the identity. Otherwise $g$ must be chosen with care:

- If $g$ is not injective, two chaining values $h \ne h'$ with $g(h) = g(h')$ give the same key. MMO then has $f(h, m) = f(h', m)$ for every $m$, a collision for free. MP has $f(h, m) \oplus f(h', m) = h \oplus h' \ne 0$, so MP keeps them apart.
- If $\kappa < n$, $g$ cannot be injective, and MMO loses $n - \kappa$ bits of the chaining value at every step. For DES ($n = 64$, $\kappa = 56$) this is part of why the double-length schemes MDC-2 and MDC-4 were built around MMO.
- $g$ should keep out weak keys, for which $E_k$ is an involution and two equal blocks give a fixed point.

### Collision resistance in the ideal cipher model

**Theorem (Black, Rogaway and Shrimpton 2002, Lemma 3.3, functions $f_1$ and $f_3$).** Let $g$ be the identity, let $E$ be an ideal cipher with $n$-bit blocks, and fix $h_0$. An adversary that makes $q$ queries to $E$ and $E^{-1}$ finds a collision of MMO or of MP, or an input that maps to $h_0$, with probability at most $q(q+1)/2^n$.

*Proof for MP.* As in the Davies-Meyer proof, assume no repeated or redundant queries. Query $i$ fixes a triple $(k_i, m_i, c_i)$ with $E_{k_i}(m_i) = c_i$, and so the value $z_i = c_i \oplus m_i \oplus k_i = f(k_i, m_i)$. Different inputs $(h, m)$ give different triples. For a forward query, $c_i$ is uniform over at least $2^n - (i - 1)$ values, and $z_i$ is a bijective image of $c_i$. For a backward query, $m_i$ is uniform over at least $2^n - (i - 1)$ values, and $z_i = c_i \oplus k_i \oplus m_i$ is a bijective image of $m_i$. So $z_i$ hits one of the at most $i$ values $h_0, z_1, \ldots, z_{i-1}$ with probability at most $i/(2^n - i)$, and the sum over $i$ is at most $q(q+1)/2^n$. For MMO, drop $k_i$ from $z_i$; nothing else changes. $\square$

BRS Theorem 3.1 carries the bound to the iterated hash. For inversion, BRS Theorem 6.1 gives $2q/2^n$. BRS Figure 1 gives the lower bounds $0.039(q-1)(q-3)/2^n$ for collisions (the attack of BRS Theorem 5.1) and $0.4q/2^n$ for inversion, for both schemes. So all three schemes need about $2^{n/2}$ queries for a collision and $2^n$ for a preimage.

## Classic examples

### The toy cipher in numbers

With the 16-bit toy cipher and $g$ the identity:

- **One call.** For $h = \texttt{0123}$ and $m = \texttt{BEEF}$: $c = E_h(m) = \texttt{1940}$. MMO gives $\texttt{1940} \oplus \texttt{BEEF} = \texttt{A7AF}$ and MP gives $\texttt{A7AF} \oplus \texttt{0123} = \texttt{A68C}$.
- **A two-block chain.** From $IV = \texttt{0000}$ with the blocks $\texttt{6162}$ and $\texttt{6380}$ ("abc" padded): MP gives $\texttt{9950}$ and then $\texttt{ABB2}$; MMO gives $\texttt{9950}$ and then $\texttt{32E2}$. The first values agree because $h = 0$.
- **A lossy g.** With $g$ that forces bit 0 to 1 and bit 1 to 0, the chaining values $\texttt{1230}$ and $\texttt{1233}$ both give the key $\texttt{1231}$. For $m = 0$, MMO gives $\texttt{B769}$ for both, a collision; MP gives $\texttt{A559}$ and $\texttt{A55A}$, which differ by $\texttt{1230} \oplus \texttt{1233} = \texttt{0003}$.
- **Birthday collisions.** From $h = \texttt{0000}$, MP collides on the blocks $\texttt{003E}$ and $\texttt{0172}$ (value $\texttt{28C0}$) after 371 queries; from $\texttt{1111}$, on $\texttt{0015}$ and $\texttt{0074}$ (value $\texttt{2E1C}$) after 117 queries. The bound $q(q+1)/2^{16}$ passes $1/2$ at $q = 181$.

### Fixed points are not free

For MP, $f(h, m) = h$ means $E_{g(h)}(m) = m$: $m$ is a fixed point of the permutation $E_{g(h)}$. A random permutation has on average one fixed point, and no shortcut is known to find it, so the attacker must search about $2^n$ blocks. In the toy cipher, an exhaustive search finds one fixed point for $h = \texttt{0001}$ (the block $\texttt{6B04}$) and none for $\texttt{0BAD}$ and $\texttt{C0DE}$; over 64 keys it finds 59 fixed points, close to the expected 64. For MMO, $f(h, m) = h$ means $E_{g(h)}(m) = m \oplus h$, again with no shortcut. Compare Davies-Meyer, where one decryption gives a fixed point for any block. This is why Dean's long-message attack, in its original form, does not apply here (the Kelsey and Schneier form with multicollisions still does).

### Whirlpool

Whirlpool (Barreto and Rijmen 2000, in ISO/IEC 10118-3) uses MP with the 512-bit cipher W, $g$ the identity, and MD strengthening with a 256-bit length:

$$H_i = W_{H_{i-1}}(m_i) \oplus H_{i-1} \oplus m_i.$$

W is an AES-like cipher on an $8 \times 8$ byte state with 10 rounds, and its key schedule is W's own round function with round constants. See [Whirlpool](/whirlpool/) for the full algorithm and the ISO test vectors.

### MDC-2

MDC-2 (HAC Algorithm 9.46) runs two MMO calls per 64-bit block with DES, one keyed through $g$ and one through $\tilde g$, and swaps the right halves of the two outputs. It gives a 128-bit hash from a 64-bit cipher.

## Variations

- **Davies-Meyer.** $f(h, m) = E_m(h) \oplus h$, the dual scheme with the message as key. The block can be as long as the key, but fixed points are free. MD5, SHA-1 and SHA-2 use it.
- **The other group-1 schemes.** BRS group 1 has 12 schemes with the same bound; MMO is $f_1$, MP is $f_3$ and DM is $f_5$. HAC notes that they are the linear transformations of MMO and MP by the six invertible $2 \times 2$ binary matrices on $(m, h)$.
- **Hirose and other double-block-length schemes.** These give $2n$-bit outputs from an $n$-bit cipher for a cipher with a $2n$-bit key.

## Pitfalls

- **A lossy g breaks MMO.** If two chaining values share a key, MMO collides on them for every block. MP does not, but its proof also assumes $g$ is injective.
- **Weak keys and complementation.** HAC Example 9.103: with DES, force key bits 2 and 3 to 10 or 01 so that the weak keys and the complementation property never occur.
- **Small blocks.** The output is $n$ bits, the cipher block size. With a 128-bit block, collisions cost $2^{64}$. Whirlpool uses a 512-bit block for this reason.
- **Slow key schedules.** The key changes with every block. A cipher with an expensive key setup makes a slow hash.
- **The ideal cipher model is a heuristic.** Real ciphers have structure. The bound says nothing about attacks that use the internals of $E$, such as the rebound attacks on reduced Whirlpool.
- **For study only.** The code of this page uses a 16-bit toy cipher with no security, and it is not constant time.

## Exercises

1. Show that $f(h, m) = E_{g(h)}(m)$, with no feed-forward, is not preimage resistant: for any target $y$ and any $h$, give a block $m$ with $f(h, m) = y$.
2. Let $g(h) = h \wedge \texttt{FFFC}$ in the toy cipher. Count the chaining values that MMO cannot tell apart, and give a collision of the iterated MMO hash on two-block messages.
3. Prove the MMO case of the theorem in full, writing out the forward and backward query cases.
4. For each of DM, MMO and MP, write the equation that a fixed point $f(h, m) = h$ must satisfy, and say which of them can be solved with one call to $E$ or $E^{-1}$.

## References
