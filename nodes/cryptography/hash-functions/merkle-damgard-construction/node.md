---
tag: FVJZV5
kind: technique
slug: merkle-damgard-construction
name: Merkle-Damgard construction
aliases:
- MD construction
- Merkle-Damgard transform
area: cryptography/hash-functions
level: core
summary: Builds a hash for messages of any length by padding with the length (MD strengthening) and iterating a compression function from a fixed IV. Used by MD5, SHA-1 and SHA-2.
prereqs: [compression-function, collision-resistance]
see_also: [merkle-damgard-theorem, davies-meyer-construction, length-extension-attack, multicollision-attack, second-preimage-finding, indifferentiability-framework, sponge-construction, hmac]
sources:
  - paper: "Ralph C. Merkle, One way hash functions and DES, Advances in Cryptology, CRYPTO 1989, LNCS 435, Springer, 1990"
    locator: the iteration of a fixed-size function built from DES, with the message length in the last block
  - paper: "Ivan B. Damgård, A design principle for hash functions, Advances in Cryptology, CRYPTO 1989, LNCS 435, Springer, 1990"
    locator: the theorem that a collision-free function on fixed-size inputs gives a collision-free function on inputs of any length
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 9, Section 9.3.1 (equation 9.1), Section 9.3.2 (Fact 9.24, Algorithms 9.25 and 9.26), Section 9.3.3 (Padding Methods 1 and 2, Remarks 9.31 and 9.32), Fact 9.37 and Example 9.96
  - paper: doi:10.6028/NIST.FIPS.180-4
    title: NIST, FIPS 180-4, Secure Hash Standard (SHS), August 2015
    locator: Section 5.1 (padding the message), Section 5.2 (parsing into blocks) and Section 5.3 (the initial hash values)
  - paper: "Antoine Joux, Multicollisions in iterated hash functions, application to cascaded constructions, Advances in Cryptology, CRYPTO 2004, LNCS 3152, Springer, 2004"
    locator: 2^k messages with one digest for the cost of k birthday searches, and the attack on the concatenation of two hashes
  - paper: "John Kelsey and Bruce Schneier, Second preimages on n-bit hash functions for much less than 2^n work, Advances in Cryptology, EUROCRYPT 2005, LNCS 3494, Springer, 2005"
    locator: expandable messages and the second preimage of a message of 2^k blocks in about k 2^(n/2+1) + 2^(n-k+1) work
  - paper: "John Kelsey and Tadayoshi Kohno, Herding hash functions and the Nostradamus attack, Advances in Cryptology, EUROCRYPT 2006, LNCS 4004, Springer, 2006"
    locator: the diamond structure and the herding attack
  - paper: "Jean-Sébastien Coron, Yevgeniy Dodis, Cécile Malinaud and Prashant Puniya, Merkle-Damgård revisited, how to construct a hash function, Advances in Cryptology, CRYPTO 2005, LNCS 3621, Springer, 2005"
    locator: plain MD is not indifferentiable from a random oracle; prefix-free MD, chop MD, NMAC and HMAC constructions are
  - paper: "Stefan Lucks, A failure-friendly design principle for hash functions, Advances in Cryptology, ASIACRYPT 2005, LNCS 3788, Springer, 2005"
    locator: the wide-pipe design, with a chaining value larger than the output
  - url: "https://eprint.iacr.org/2007/278"
    title: Eli Biham and Orr Dunkelman, A framework for iterative hash functions, HAIFA, Cryptology ePrint Archive, Report 2007/278
    locator: the counter of hashed bits and the salt as inputs of the compression function
---

The Merkle-Damgard construction turns a [compression function](/compression-function/) $f$, which hashes inputs of one fixed size, into a hash function for messages of any length. It pads the message so that its length is a multiple of the block size and so that the last block holds the message length (MD strengthening). Then it runs $f$ once per block, from a fixed initial value $IV$, and outputs the last chaining value. Merkle and Damgard each published it at CRYPTO 1989, and both proved the key fact: if $f$ is collision resistant, so is the hash (the [Merkle-Damgard theorem](/merkle-damgard-theorem/)). MD4, [MD5](/md5/), SHA-1, [SHA-2](/sha-2/), RIPEMD-160, Whirlpool and Tiger are all built this way. It has known generic weaknesses that a random function does not have, and SHA-3 uses the [sponge construction](/sponge-construction/) instead.

**Notation.** $f : \{0,1\}^n \times \{0,1\}^b \to \{0,1\}^n$ is the compression function, with an $n$-bit chaining value and a $b$-bit block. In the code the block has $B = b/8$ bytes and the length field has $\lambda$ bytes. $M$ is the message, of $|M|$ bytes. $[x]_\lambda$ is $x$ as a $\lambda$-byte integer. $\mathrm{MD}^f$ is the hash function the construction gives. All the numbers in the examples come from the code of this page, run on its toy compression function with $n = 16$, $B = 2$ and $\lambda = 2$.

## In plain words

You have a machine that takes a state of $n$ bits and one block of $b$ bits and returns a new state of $n$ bits. You want to hash a long message. Cut the message into blocks. Start from a fixed state. Feed the blocks to the machine one at a time, each time with the state that the last call returned. The final state is the hash. Two details make this safe. First, the last block must be filled in a way that cannot be confused with a message that really ends in those bits, so you add a 1 bit and then zeros. Second, the message length goes into the last block, so that two messages of different lengths always end with different blocks.

## When it applies

- **You have a good compression function and want a hash.** The construction needs nothing from $f$ except fixed sizes. It processes the message in one pass with constant memory, so it works on streams and in small devices.
- **You need collision resistance.** The [Merkle-Damgard theorem](/merkle-damgard-theorem/) reduces collisions of $\mathrm{MD}^f$ to collisions of $f$. This is the property that the construction was made for.
- **Not as a random oracle or a MAC.** $\mathrm{MD}^f$ is not indifferentiable from a random oracle even when $f$ is ideal. $\mathrm{Hash}(K \| M)$ is not a secure MAC because of length extension. Use [HMAC](/hmac/), a truncated output, or a sponge.
- **Not where generic attacks are cheap enough to matter.** For a digest of $n$ bits, multicollisions, herding and long-message second preimages cost far less than for a random function. With $n = 256$ these attacks are still out of reach, but they rule out shorter outputs for long-term use.

## The template

```pseudo id=main
MD-PAD(len)                                ▷ len = |M| in bytes; B block bytes, λ length bytes
L1  z ← (−(len + 1 + λ)) mod B             ▷ number of zero bytes, 0 ≤ z < B
L2  return 0x80 ‖ 0^z ‖ [8·len]_λ          ▷ a 1 bit, zero bits, then the length in bits

MD^f(M)
L3  P ← M ‖ MD-PAD(|M|)                    ▷ |P| is a multiple of B
L4  h ← IV
L5  for i ← 1 to |P|/B do
L6      h ← f(h, P_i)                      ▷ P_i is the i-th block of B bytes
L7  return h
```

The holes of the template are $f$, the $IV$, the block size, the length field (size and byte order), and an optional output transform $g$ applied to the result of L7, for example truncation. HAC writes the whole model as $H_0 = IV$, $H_i = f(H_{i-1}, x_i)$, $h(x) = g(H_t)$ (equation 9.1).

**MD strengthening.** Line L2 is HAC's Padding Method 2 (a 1 bit, then zeros) with the bit length in the last $\lambda$ bytes. This is the form of MD5 ($B = 64$, $\lambda = 8$, little-endian), SHA-1 and SHA-256 ($B = 64$, $\lambda = 8$, big-endian), and SHA-512 ($B = 128$, $\lambda = 16$). It has three properties, and the security proof needs all of them:

1. **Injective.** The original message is all bytes before the last `80` byte that is followed only by zeros and the length field. So $M \ne M'$ gives $P \ne P'$.
2. **Whole blocks.** $|M| + 1 + z + \lambda \equiv 0 \pmod B$ by the choice of $z$.
3. **Suffix-free.** If $|M| \ne |M'|$, the last blocks of $P$ and $P'$ differ, because they hold different lengths. So no padded message is a tail of another one. Merkle's own version (HAC Algorithm 9.25) puts the length in a separate extra block; the effect is the same.

Padding without the length, as in HAC Padding Method 2 alone, is still injective but not suffix-free, and the reduction of the theorem then fails. The [Merkle-Damgard theorem](/merkle-damgard-theorem/) page shows this failure in code with a compression function that has a fixed point.

**The IV.** The $IV$ is a fixed public constant, part of the definition of the hash. The theorem needs no property of it. In practice it is a "nothing up my sleeve" value: MD5 uses the bytes `01 23 45 67 89 AB CD EF FE DC BA 98 76 54 32 10`, SHA-256 uses the first 32 bits of the fractional parts of the square roots of the first 8 primes. The truncated SHA-2 functions use a different $IV$ from the full ones, so that, for example, SHA-224 is not just a cut SHA-256.

**Cost.** $\mathrm{MD}^f$ calls $f$ exactly $\lceil (|M| + 1 + \lambda)/B \rceil$ times, so it takes $\Theta(|M|)$ time. It keeps one chaining value and one partial block, so it needs $\Theta(1)$ extra space as a stream. The work is sequential: block $i$ needs the result of block $i - 1$. A [Merkle tree](/merkle-tree/) or [tree hashing](/tree-hashing/) is the parallel alternative.

### Generic weaknesses

These hold for every compression function $f$, even an ideal one. Each one has its own page.

- **[Length extension](/length-extension-attack/).** The digest is the full state, so anyone who knows $\mathrm{MD}^f(M)$ and $|M|$ can compute $\mathrm{MD}^f(M \,\|\, \mathrm{pad}(M) \,\|\, S)$ for any $S$, without $M$.
- **[Multicollisions](/multicollision-attack/).** Joux (2004): $k$ successive block collisions, each found by a [birthday attack](/birthday-attack/), give $2^k$ messages with one digest for about $k \cdot 2^{n/2}$ work. For a random function, $2^k$ colliding messages cost much more. One result is that the concatenation of two MD hashes of $n$ bits is not much stronger than one.
- **Long-message second preimages ([second-preimage finding](/second-preimage-finding/)).** Dean (1999) and Kelsey and Schneier (2005): for a target of $2^k$ blocks, an attacker can find a second preimage in about $k \cdot 2^{n/2+1} + 2^{n-k+1}$ work, much less than $2^n$. MD strengthening does not stop it, because expandable messages fix the length.
- **Herding.** Kelsey and Kohno (2006): the attacker first commits to a digest and later, for a prefix it learns only then, finds a suffix that gives this digest, for about $2^{2n/3}$ work.
- **Not a random oracle.** Coron, Dodis, Malinaud and Puniya (2005) showed that plain MD is not indifferentiable from a random oracle, even with an ideal $f$; length extension is a distinguisher. See [indifferentiability](/indifferentiability-framework/).

## Classic examples

### SHA-256 padding

For $M = $ `abc` ($|M| = 3$, $B = 64$, $\lambda = 8$), line L1 gives $z = (-(3 + 1 + 8)) \bmod 64 = 52$. So $P$ is `616263`, `80`, 52 zero bytes and `0000000000000018` (24 bits), one block. A message of 55 bytes gets 9 bytes of padding and still fits in one block. A message of 56 bytes gets 72 bytes of padding and needs two blocks, because the `80` byte and the 8 length bytes do not fit in the last 8 bytes of the first block. The empty message gets one block of 64 bytes of padding. Each of the six SHA-2 functions follows this template exactly (see [SHA-2](/sha-2/)).

### A toy run

With the toy $f$ of the code, $IV = \texttt{2468}$, $B = 2$ and $\lambda = 2$, the message `abc` pads to `61 62 63 80 00 18`: here $z = (-(3 + 1 + 2)) \bmod 2 = 0$, and $\texttt{0018} = 24$ is the bit length. The three calls are:

| $i$ | $h$ before | block $P_i$ | $h$ after |
|---|---|---|---|
| 1 | `2468` | `6162` | `8887` |
| 2 | `8887` | `6380` | `a833` |
| 3 | `a833` | `0018` | `9da9` |

So $\mathrm{MD}^f(\texttt{abc}) = \texttt{9da9}$.

### Length extension in numbers

A server computes a tag as $\mathrm{MD}^f(K \,\|\, D)$ with the secret key $K = $ `key` and the data $D = $ `abc`. The tag is `b95a`. The padding of the 6-byte input is the glue $G = $ `80 00 00 30` ($\texttt{30} = 48$ bits). An attacker who knows the tag and the length 6, but not $K$, starts from $h = \texttt{b95a}$ as if 10 bytes were already hashed, and hashes the suffix `!` with the padding for a total length of 11 bytes. It gets `e834`. The server computes $\mathrm{MD}^f(K \,\|\, D \,\|\, G \,\|\, \texttt{!}) = \texttt{e834}$ for the data $D \,\|\, G \,\|\, \texttt{!}$, so the forged tag is valid. The test `test_length_extension` checks the same attack with a longer key and longer data.

### Joux multicollision in numbers

Three birthday searches from $IV = \texttt{2468}$ find three block pairs with the same output:

| step | $h$ | block pair | both give |
|---|---|---|---|
| 1 | `2468` | `004f`, `00fc` | `e00c` |
| 2 | `e00c` | `00a4`, `0122` | `e4e6` |
| 3 | `e4e6` | `0040`, `0191` | `c5fe` |

Any choice of one block from each pair gives a 6-byte message with chaining value `c5fe` before the padding. All $2^3 = 8$ messages have the same length, so the padding block is the same, and all have the digest `68d1`. The test `test_joux_multicollision` builds $2^4 = 16$ such messages.

## Variations

- **MD strengthening off.** Plain padding (HAC Padding Method 1 or 2 without a length) breaks the proof and allows trivial pseudo-collisions by deletion of leading blocks (HAC Example 9.96). Do not use it.
- **Merkle's version.** HAC Algorithm 9.25 pads with zeros and adds the length as a separate final block, with $H_0 = 0^n$. The proof is the same.
- **Chop MD and truncation.** Output only part of the final chaining value, as SHA-224, SHA-384, SHA-512/224 and SHA-512/256 do. The hidden bits stop length extension, and Coron et al. (2005) proved chop MD indifferentiable from a random oracle if enough bits are cut.
- **Prefix-free MD and NMAC-style finalization.** Encode the message so that no encoding is a prefix of another, or apply an independent function to the last chaining value. Both are indifferentiable from a random oracle (Coron et al. 2005). [NMAC](/nmac/) and [HMAC](/hmac/) are of this type.
- **Wide pipe.** Lucks (2005): make the chaining value at least twice as long as the output. This blocks the multicollision and second preimage attacks above at the output size. SHA-512/256 is wide pipe in this sense.
- **HAIFA.** Biham and Dunkelman (2006): give $f$ the number of bits hashed so far and an optional salt as extra inputs. Each call then has a different function, which defeats fixed points and long-message attacks. [BLAKE2](/blake2/) uses a counter in this way.
- **Sponge.** Replace the compression function by a permutation and a hidden capacity part of the state. See [sponge construction](/sponge-construction/).

## Pitfalls

- **Bits and bytes.** The length field is the length in bits, $8|M|$, not in bytes. A byte length gives a different hash and fails every test vector.
- **The boundary case.** Test the message lengths $B - \lambda - 1$, $B - \lambda$ and $B$, which are 55, 56 and 64 bytes for SHA-256. The first gives one block, the other two give two.
- **Byte order.** MD4, MD5 and RIPEMD-160 store the length and the words little-endian, SHA-1 and SHA-2 big-endian. The template is the same; the vectors are not.
- **Hash of a secret prefix is not a MAC.** $\mathrm{MD}^f(K \,\|\, M)$ is open to length extension, as the example shows. Use HMAC.
- **"Collision resistant $f$" means the strong notion.** The theorem needs $f$ to be collision resistant with free chaining values. A free-start collision of $f$ leaves the hash unbroken but removes the proof; MD5 had one in 1993, long before its full collisions.
- **A collision resistant hash is not a random oracle.** The generic weaknesses above hold even with a perfect $f$. Proofs in the [random oracle model](/random-oracle-model/) do not carry over to $\mathrm{MD}^f$ without care.
- **The code is a toy.** The Python code of this page is for study only. Its 16-bit $f$ has no security, and the code is not constant time. Use SHA-256, SHA-512/256 or SHA-3 from a vetted library.

## Exercises

1. Show that the padding of L1 and L2 is suffix-free: if $|M| \ne |M'|$, the last blocks of the padded messages differ. What breaks if the length field holds $|M| \bmod 2^{8\lambda}$ and messages may be longer?
2. Take $f(h, m) = h \oplus m$ with $n = b$. Find two different messages of two blocks each with the same $\mathrm{MD}^f$ value. Which property of the theorem fails?
3. With a 16-bit $f$, how many calls does Joux's attack need to build $2^{10}$ messages with one digest? Compare with the cost of $2^{10}$-collisions of a random 16-bit function.
4. Explain why SHA-512/256 does not have length extension but SHA-512 does, with the same compression function.

## References
