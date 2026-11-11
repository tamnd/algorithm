---
tag: 0WC6B8
kind: theorem
slug: merkle-damgard-theorem
name: Merkle-Damgard theorem
aliases:
- Merkle-Damgard collision resistance preservation
area: cryptography/hash-functions
level: advanced
summary: With length padding (MD strengthening), every collision of the iterated hash gives a collision of its compression function, found in linear time. The reduction loses nothing.
prereqs: [merkle-damgard-construction, collision-resistance]
see_also: [compression-function, davies-meyer-construction, length-extension-attack, multicollision-attack, second-preimage-finding, ideal-cipher-model, md5, sha-2]
sources:
  - paper: "Ralph C. Merkle, One way hash functions and DES, Advances in Cryptology, CRYPTO 1989, LNCS 435, Springer, 1990"
    locator: the meta-method and the argument that a collision of the hash gives a collision of the fixed-size function
  - paper: "Ivan B. Damgård, A design principle for hash functions, Advances in Cryptology, CRYPTO 1989, LNCS 435, Springer, 1990"
    locator: the theorem that a collision-free function family on fixed-size inputs gives one on inputs of any length
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 9, Section 9.3.2, Fact 9.24, Algorithm 9.25 with the proof sketch after it, Algorithm 9.26 and Remark 9.32
  - paper: "John Black, Phillip Rogaway and Thomas Shrimpton, Black-box analysis of the block-cipher-based hash-function constructions from PGV, Advances in Cryptology, CRYPTO 2002, LNCS 2442, Springer, 2002"
    locator: full version of May 31, 2002, Definition 2.2, Lemma 3.2 (Merkle-Damgard in the black-box model, proof in Appendix C.1), Lemma 6.2 and Theorem 4.1
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 6, Section 6.2, the Merkle-Damgard transform and the proof of its collision resistance
  - paper: "Xiaoyun Wang and Hongbo Yu, How to break MD5 and other hash functions, Advances in Cryptology, EUROCRYPT 2005, LNCS 3494, Springer, 2005"
    locator: the two-block collision attack, a near-collision after the first block and a collision after the second
  - url: "https://www.mscs.dal.ca/~selinger/md5collision/"
    title: Peter Selinger, MD5 Collision Demo, 2006
    locator: the two 128-byte messages with the MD5 digest 79054025255fb1a26e4bc422aef54eb4
  - paper: "Elena Andreeva, Gregory Neven, Bart Preneel and Thomas Shrimpton, Seven-property-preserving iterated hashing, ROX, Advances in Cryptology, ASIACRYPT 2007, LNCS 4833, Springer, 2007"
    locator: which security properties of the compression function each iteration preserves
---

The Merkle-Damgard theorem says that the [Merkle-Damgard construction](/merkle-damgard-construction/) preserves collision resistance: if the [compression function](/compression-function/) $f$ is collision resistant, then so is the hash function built by iterating $f$ over a message padded with its length. The proof is a reduction that, given two different messages with the same hash, walks the two chains backward from the end and stops at the first place where the inputs of $f$ differ but the outputs agree. That place is a collision of $f$. Merkle and Damgard proved it independently at CRYPTO 1989. It is the reason that MD5, SHA-1 and SHA-2 were designed as a compression function plus a standard iteration, and the reason that attacks on these hashes are attacks on their compression functions.

**Notation.** $f : \{0,1\}^n \times \{0,1\}^b \to \{0,1\}^n$ is the compression function and $IV \in \{0,1\}^n$ a fixed initial value. $\mathrm{pad}$ maps a message $M$ to a sequence of $b$-bit blocks $m_1, \ldots, m_\ell$. For blocks $m_1, \ldots, m_\ell$, the chain is $h_0 = IV$ and $h_i = f(h_{i-1}, m_i)$, and $H(M) = h_\ell$ for the blocks of $\mathrm{pad}(M)$. A **collision** of $f$ is a pair of inputs $(h, m) \ne (h', m')$ with $f(h, m) = f(h', m')$; both the chaining values and the blocks are free. $t_f$ is the time of one call of $f$.

## Statement

**Theorem (Merkle 1989, Damgard 1989).** Let $\mathrm{pad}$ have these three properties for all messages $M$, $M'$:

1. (injective) if $M \ne M'$, then $\mathrm{pad}(M) \ne \mathrm{pad}(M')$;
2. (same length, same number of blocks) if $|M| = |M'|$, then $\mathrm{pad}(M)$ and $\mathrm{pad}(M')$ have the same number of blocks;
3. (length in the last block) if $|M| \ne |M'|$, then the last blocks of $\mathrm{pad}(M)$ and $\mathrm{pad}(M')$ differ.

Then there is an algorithm EXTRACT that, given $M \ne M'$ with $H(M) = H(M')$, outputs a collision of $f$, with at most $\ell + \ell'$ calls of $f$, where $\ell$ and $\ell'$ are the numbers of blocks of $\mathrm{pad}(M)$ and $\mathrm{pad}(M')$.

**Corollary (concrete security).** For every adversary $\mathcal{A}$ that finds a collision of $H$ with probability $\varepsilon$ in time $t$, using messages of at most $L$ blocks, the adversary $\mathcal{B}$ that runs $\mathcal{A}$ and then EXTRACT finds a collision of $f$ with probability at least $\varepsilon$ in time $t + 2L \cdot t_f + O(L)$. So if $f$ is collision resistant, $H$ is.

MD strengthening (a 1 bit, zeros, and the bit length in the last block, as in MD5, SHA-1 and SHA-2) has all three properties for messages shorter than $2^{8\lambda}$ bits, where $\lambda$ is the size of the length field in bytes. HAC states the theorem as Fact 9.24, and Black, Rogaway and Shrimpton (2002) state it for a compression function that calls an ideal cipher as Lemma 3.2: $\mathrm{Adv}^{\mathrm{coll}}_H(q) \le \mathrm{Adv}^{\mathrm{comp}}_f(q)$.

## In plain words

Suppose two different messages give the same hash. Line up their chains of chaining values from the end. The last values are equal, because they are the hash. Look at the last call of $f$ on each side. If the two calls had different inputs, you have found two different inputs of $f$ with the same output: a collision of $f$. If the inputs were the same, then the chaining values before them are also equal, and you step back one block on both sides and repeat. You cannot step back forever. If the messages have different lengths, the very last blocks already differ, because they hold the lengths. If they have the same length, then stepping back through every block would mean that all blocks are equal, so the messages would be equal. Either way, you find a collision of $f$ somewhere on the way.

## Proof

The reduction is the procedure EXTRACT below. Lines L1 to L4 compute the chain of the construction, and lines L5 to L12 walk back.

```pseudo id=main
CHAIN(f, IV, m_1 … m_ℓ)
L1  h_0 ← IV
L2  for i ← 1 to ℓ do
L3      h_i ← f(h_{i−1}, m_i)
L4  return (h_0, …, h_ℓ)

EXTRACT(M, M')                          ▷ M ≠ M' and H(M) = H(M')
L5  m ← pad(M); m' ← pad(M')            ▷ ℓ and ℓ' blocks
L6  h ← CHAIN(f, IV, m); h' ← CHAIN(f, IV, m')
L7  i ← ℓ; j ← ℓ'
L8  loop
L9      x ← (h_{i−1}, m_i); y ← (h'_{j−1}, m'_j)
L10     if x ≠ y then
L11         return (x, y)               ▷ f(x) = h_i = h'_j = f(y)
L12     i ← i − 1; j ← j − 1
```

**Lemma 1 (invariant).** Each time line L9 runs, $i \ge 1$, $j \ge 1$ and $h_i = h'_j$.

*Proof.* At the first run, $i = \ell$ and $j = \ell'$, and $h_\ell = H(M) = H(M') = h'_{\ell'}$ by assumption. Suppose the invariant holds at some run of L9 and the loop does not return. Then $x = y$, that is $h_{i-1} = h'_{j-1}$ and $m_i = m'_j$, and line L12 sets $i \leftarrow i - 1$ and $j \leftarrow j - 1$, so $h_i = h'_j$ holds for the new values. It remains to show $i, j \ge 1$ at the next run, which is Lemma 2. $\square$

**Lemma 2 (termination).** The loop returns at a run of L9 with $i \ge 1$ and $j \ge 1$, after at most $\min(\ell, \ell')$ runs.

*Proof.* There are two cases.

*Case $|M| \ne |M'|$.* By property 3, $m_\ell \ne m'_{\ell'}$. So at the first run, $x \ne y$, and the loop returns at once with $i = \ell \ge 1$ and $j = \ell' \ge 1$.

*Case $|M| = |M'|$.* By property 2, $\ell = \ell'$, so $i = j$ at every run. Suppose the loop does not return in the runs with $i = \ell, \ell - 1, \ldots, 1$. Then $m_i = m'_i$ for all $i$, so $\mathrm{pad}(M) = \mathrm{pad}(M')$, and property 1 gives $M = M'$, a contradiction. So it returns at some run with $1 \le i = j \le \ell$. $\square$

**Lemma 3 (output).** The pair $(x, y)$ returned by line L11 is a collision of $f$.

*Proof.* By line L10, $x \ne y$. By Lemma 1, $f(x) = f(h_{i-1}, m_i) = h_i = h'_j = f(h'_{j-1}, m'_j) = f(y)$, where the outer equalities are line L3. $\square$

*Proof of the theorem.* Lemmas 2 and 3. Line L6 makes $\ell + \ell'$ calls of $f$, and the loop makes none, only at most $\min(\ell, \ell')$ comparisons. $\square$

*Proof of the corollary.* $\mathcal{B}$ runs $\mathcal{A}$. If $\mathcal{A}$ outputs $M \ne M'$ with $H(M) = H(M')$, which happens with probability $\varepsilon$, then $\mathcal{B}$ runs EXTRACT, which by the theorem always outputs a collision of $f$. The added time is at most $2L$ calls of $f$ and $O(L)$ comparisons. $\square$

**Where each property is used.** Property 1 is used only in the case of equal lengths, to rule out that all blocks agree. Property 2 keeps $i = j$ in that case. Property 3 handles different lengths. Without property 3, the walk for messages of different lengths can reach $i = 0$ while $j \ge 1$, with $IV = h_0 = h'_j = f(h'_{j-1}, m'_j)$. This is not a collision but a preimage of $IV$ under $f$. That is why Definition 2.2 of Black, Rogaway and Shrimpton counts an input with $f(h, m) = IV$ as a success: with that clause, the theorem holds for padding without the length. The example in the Tightness section shows that the clause is needed.

**The code.** The implementation of this page computes the chain with lines L1 to L4 and runs EXTRACT with lines L5 to L12, on a toy 16-bit Davies-Meyer function, truncated to 10 or 8 bits so that a birthday search finds hash collisions at once. Its padding is Merkle's form (HAC Algorithm 9.25): the byte `80`, zeros to a whole block, and one extra block with the length.

## Consequences

### A worked reduction on a toy function

With $f$ truncated to 10 bits and $IV = \texttt{155}$, a birthday search finds the 4-byte messages $M = $ `00000000` and $M' = $ `00000024` with the same hash. Their padded forms and chains are:

| | $m_1$ | $m_2$ | $m_3$ | $m_4$ (length) | $h_0$ | $h_1$ | $h_2$ | $h_3$ | $h_4$ |
|---|---|---|---|---|---|---|---|---|---|
| $M$ | `0000` | `0000` | `8000` | `0004` | `155` | `3a2` | `078` | `37c` | `3ef` |
| $M'$ | `0000` | `0024` | `8000` | `0004` | `155` | `3a2` | `11f` | `37c` | `3ef` |

EXTRACT starts at $i = j = 4$. The inputs $(h_3, m_4) = (\texttt{37c}, \texttt{0004})$ agree on both sides, so it steps back. At $i = j = 3$ the inputs are $(\texttt{078}, \texttt{8000})$ and $(\texttt{11f}, \texttt{8000})$. They differ, and both give $\texttt{37c}$. This is a collision of $f$ with the same block and different chaining values: a free-start collision, which the theorem counts as a collision. The tests repeat this for five starting values and for messages of different lengths, where the collision is always at the length block.

### Real hash collisions contain compression collisions

Apply EXTRACT to the MD5 collision of Wang and Yu (2005), in the form published by Selinger: two 128-byte messages $M = M_0 \| M_1$ and $M' = M_0' \| M_1'$ with the digest `79054025255fb1a26e4bc422aef54eb4`. Both pad to three blocks, and the third (padding) block is the same, so the walk steps back to block 2. The chaining values after block 1 are

| | $A$ | $B$ | $C$ | $D$ |
|---|---|---|---|---|
| $h_1$ for $M$ | `52589324` | `3093d7ca` | `2a06dc54` | `20c5be06` |
| $h_1'$ for $M'$ | `d2589324` | `b293d7ca` | `ac06dc54` | `a2c5be06` |
| $h_1' - h_1$ modulo $2^{32}$ | `80000000` | `82000000` | `82000000` | `82000000` |

So EXTRACT returns $((h_1, M_1), (h_1', M_1'))$: two different chaining values and two different blocks with the same output $h_2 = $ `8d5e7019 61804e08 715d6b58 6324c015`. This is the structure of the attack: block 1 gives a near-collision with a chosen difference, and block 2 cancels it. Every collision attack on an MD hash must produce such a collision of $f$; the theorem says there is no other way. The SHAttered collision of SHA-1 has the same two-block shape (see [SHA-1](/sha-1/)).

### Other consequences

- **Design.** A designer of an MD hash needs only a collision resistant $f$ of fixed size. For SHA-256, $f$ maps 768 bits to 256 bits; all the analysis of SHA-256 for collisions is analysis of this $f$.
- **Inversion.** The same walk proves the analog for one-wayness in the ideal cipher setting: Black, Rogaway and Shrimpton, Lemma 6.2, $\mathrm{Adv}^{\mathrm{inv}}_H(q) \le \mathrm{Adv}^{\mathrm{inv}}_f(q)$.
- **Common suffixes.** Since the collision is internal, $H(M \,\|\, S) = H(M' \,\|\, S)$ for every $S$ when $M$ and $M'$ have the same length and collide before the padding. This is how the MD5 and SHA-1 collisions are turned into colliding certificates and documents.
- **Multicollisions do not contradict the theorem.** Joux's $2^k$ colliding messages are built from $k$ collisions of $f$, so they cost $k$ birthday searches; the theorem says nothing about how many collisions of $H$ one collision of $f$ gives. See [multicollision attack](/multicollision-attack/).

## Tightness

**The reduction loses nothing.** The success probability of $\mathcal{B}$ equals that of $\mathcal{A}$, and the extra time is linear in the message length. So a collision of $H$ is exactly as hard as a collision of $f$ up to this cost, and the generic bound $2^{n/2}$ for $f$ carries over to $H$.

**The length in the last block is needed.** Take a collision resistant $f$ for which it is also hard to find $(h, m)$ with $f(h, m) = IV$, and fix a block $m^*$. Define $f'(IV, m^*) = IV$ and $f'(h, m) = f(h, m)$ for all other inputs. A collision of $f'$ is a collision of $f$ or an input $(h, m) \ne (IV, m^*)$ with $f(h, m) = IV$, so $f'$ is still collision resistant. But with padding that has only properties 1 and 2 (a 1 bit and zeros, no length), $M$ and $m^* \| M$ have the same hash for every $M$, because the extra first block maps $IV$ to $IV$. The test `test_padding_without_length_breaks_md` builds this with the 16-bit toy function: the block $m^* = \texttt{1234}$ gives the fixed point $IV = E_{m^*}^{-1}(0) = \texttt{6a0c}$ in Davies-Meyer form. The message `a` pads to `6180`, the message `12 34 61` pads to `1234 6180`, and both chains end at `8ecc`. With MD strengthening the last blocks are the lengths 1 and 3, and the hashes are `69a3` and `05e5`. In Davies-Meyer such fixed points are free for any block, which is why real hashes must encode the length. See [Davies-Meyer](/davies-meyer-construction/).

**The converse is false.** $H$ can be collision resistant while $f$ is not. A free-start collision of $f$ with chaining values that the iteration never reaches does not give a collision of $H$; den Boer and Bosselaers found one for MD5 in 1993, and Stevens, Karpman and Peyrin one for SHA-1 in 2016, years before the full collisions. Black, Rogaway and Shrimpton (Theorem 4.1) found 8 block-cipher schemes whose $f$ has easy collisions but whose iterated hash is provably collision resistant in the ideal cipher model. So the theorem gives a sufficient condition only.

**Other properties are not preserved.** The theorem is about collisions. Second preimage resistance at the level $2^n$ is not preserved: Kelsey and Schneier (2005) find second preimages of long messages in much less than $2^n$ work for any $f$ (see [second-preimage finding](/second-preimage-finding/)). Pseudorandomness and random-oracle behavior are not preserved either, because of [length extension](/length-extension-attack/). Andreeva, Neven, Preneel and Shrimpton (2007) list which of seven properties each common iteration preserves.

## History

Merkle and Damgard presented the construction and the theorem in two separate papers at CRYPTO 1989. Merkle's paper built fixed-size functions from DES and iterated them with the length in a final block. Damgard's paper proved the result for collision-free function families in a complexity-theoretic setting. HAC (1996) states it as Fact 9.24, with Algorithm 9.25 called Merkle's meta-method and the length block called MD-strengthening. Black, Rogaway and Shrimpton (2002) gave a concrete version in the ideal cipher model, with the extra clause for preimages of the initial value. Coron, Dodis, Malinaud and Puniya (2005) showed that the construction does not preserve random-oracle behavior, and proposed modified iterations that do (see [indifferentiability](/indifferentiability-framework/)).

## References
