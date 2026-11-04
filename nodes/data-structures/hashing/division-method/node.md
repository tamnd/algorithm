---
tag: A1WGV6
kind: technique
slug: division-method
name: Division method
aliases:
- division hashing
- modular hashing
area: data-structures/hashing
level: intro
summary: Hash by taking the key modulo a table size, usually a prime not close to a power of two.
prereqs: [hash-function, hash-collision]
see_also: [multiplicative-hashing, universal-hashing, polynomial-rolling-hash, hash-table, double-hashing, prime-number, horner-rule]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.3 (Hash functions), the division method
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), the discussion of the division method and the choice of the modulus
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4 (Hash tables), modular hashing for integers and for strings with Horner's method
---

The division method is a [hash function](/hash-function/) for integer keys: it maps a key $k$ to the slot $h(k) = k \bmod m$ of a table with $m$ slots. It costs one division, and it uses all the bits of the key only when $m$ has no small relation to the base of the number system. So the standard advice is to choose $m$ prime and not close to a power of two. It is the oldest and simplest hash function, and it is the last step of many others, such as the [polynomial rolling hash](/polynomial-rolling-hash/) and [universal hashing](/universal-hashing/).

## In plain words

To put a number in one of a fixed set of boxes, divide it by the number of boxes and keep the remainder. The remainder is the box. Each box gets an equal share of all possible numbers.

The danger is the number of boxes. With 100 boxes, the remainder is the last two digits of the number, and the other digits do not matter at all. If many keys end in the same digits, such as prices that end in 99, they all fall in the same box. A number of boxes that is a prime, far from a round number such as a power of ten or a power of two, makes each digit of the key change the box. For text, read the characters as the digits of a large number, and take the remainder step by step, so the number never gets too large.

## When it applies

- The keys are integers, or can be turned into integers without loss, such as strings read as numbers in some base.
- The table size can be chosen freely, so it can be a prime. A table that must have a power-of-two size (for fast masking, as in many open-addressing tables) needs another method, such as the [multiplicative method](/multiplicative-hashing/).
- The keys are not chosen by an adversary. A fixed $m$ is known, so an attacker can pick keys that are all congruent modulo $m$. For that case, use [universal hashing](/universal-hashing/), which applies the division method to a random affine image of the key.
- A division instruction is cheap enough. On some processors a division is many times slower than a multiplication; with a fixed $m$, a compiler can replace it by a multiplication and a shift.

## The template

```pseudo id=main
DIVISION-HASH(k, m)                           ▷ m ≥ 1, chosen once for the table
L1  x ← TO-INTEGER(k)                          ▷ hole: the key as a non-negative integer
L2  return x mod m

STRING-DIVISION-HASH(s, m, r)                 ▷ s = s[0 .. L − 1], radix r
L3  x ← 0
L4  for i ← 0 to L − 1 do
L5      x ← (x · r + CODE(s[i])) mod m         ▷ hole: CODE maps a character to 0 .. r − 1
L6  return x

CHOOSE-MODULUS(N)                             ▷ about N slots are wanted
L7  m ← a prime near N that is not near a power of 2 or of 10
L8  return m
```

Line L1 is the hole for the conversion of the key. For a signed integer, use a non-negative representative: in a language where the remainder of a negative number is negative, write $((x \bmod m) + m) \bmod m$. Line L2 is the whole method. Its value is in $\{0, \ldots, m - 1\}$, and each slot receives $\lfloor |U|/m \rfloor$ or $\lceil |U|/m \rceil$ keys of a universe $U = \{0, \ldots, |U| - 1\}$.

Lines L3 to L6 hash a string as the number $x = \sum_{i} \mathrm{CODE}(s[i]) \, r^{L-1-i}$ in base $r$, by [Horner's rule](/horner-rule/), and reduce modulo $m$ after each step. The loop keeps the invariant $x = (\sum_{j < i} \mathrm{CODE}(s[j]) \, r^{i-1-j}) \bmod m$, because $(a \bmod m) \cdot r + c \equiv a r + c \pmod m$. So it returns the same value as line L2 applied to the whole number, while each intermediate value stays below $m r$.

**Why the modulus matters.** Let the keys be the multiples $d, 2d, 3d, \ldots$ of some step $d$. Then the slots that they reach are exactly the multiples of $g = \gcd(d, m)$, and there are $m/g$ of them. *Proof.* If $g$ divides $m$ and $d$, it divides $jd \bmod m = jd - qm$, so each slot is a multiple of $g$. Conversely, by Bézout there are integers $a, b$ with $ad + bm = g$, so the key $ad$ (with $a$ taken modulo $m/g$ to make it positive) lands on slot $g$, and its multiples reach every multiple of $g$. $\square$ So a modulus with many small factors wastes slots on keys with a regular step, and a prime $m$ that does not divide $d$ uses every slot.

**Why a power of the radix is bad.** If $m = r^p$ and the key is written in base $r$, then $k \bmod m$ is the last $p$ digits of $k$, and the other digits are ignored. If $m = r^p - 1$, then $r^p \equiv 1 \pmod m$, so $k \bmod m$ is the sum of the blocks of $p$ digits of $k$, modulo $m$. Then any two strings with the same blocks in a different order collide. Knuth's general rule in Section 6.4 is to avoid each $m$ that divides $r^j \pm a$ for small $j$ and $a$.

## Classic examples

- **Chained [hash table](/hash-table/).** CLRS and Sedgewick and Wayne use $h(k) = k \bmod m$ with a prime $m$ as the first hash function for a table with [separate chaining](/separate-chaining/).
- **[Double hashing](/double-hashing/).** The standard pair is $h_1(k) = k \bmod m$ and $h_2(k) = 1 + (k \bmod m')$ with $m$ prime and $m' = m - 1$ or $m - 2$, so that the step is never 0 and is coprime to $m$.
- **[Polynomial rolling hash](/polynomial-rolling-hash/) and [Rabin-Karp](/rabin-karp/).** Lines L3 to L6 with a large prime $m$ give the fingerprint of a string, and the update for a sliding window is also a computation modulo $m$.
- **[Universal hashing](/universal-hashing/).** The Carter and Wegman family $h_{a,b}(k) = ((a k + b) \bmod p) \bmod m$, with a prime $p$ larger than each key and random $a \ne 0$ and $b$, applies the division method twice. The random $a$ and $b$ remove the weakness against chosen keys.

## Variations

- **Modulus a power of two.** $k \bmod 2^p$ is the mask $k \wedge (2^p - 1)$, which is faster than a division. It is safe only after a mixing step that makes the low bits depend on all bits of the key, as in Java's `HashMap`, which XORs the high half of the hash code into the low half.
- **Fast reduction for a fixed modulus.** For a fixed $m$, compilers replace $x \bmod m$ by a multiplication with a precomputed inverse and a shift, the [division by a constant](/division-by-constant/) technique.
- **Mersenne prime modulus.** For $p = 2^{61} - 1$, the reduction of a 122-bit product needs only shifts and additions, because $2^{61} \equiv 1 \pmod p$. Fast universal hashing uses this prime.
- **Multiplicative method.** The [multiplicative method](/multiplicative-hashing/) $h(k) = \lfloor m \cdot (k A \bmod 1) \rfloor$ works with any $m$, including a power of two.

## Pitfalls

- **A round modulus.** With $m = 100$ or $m = 2^{10}$, only the last digits or bits of the key matter. The ten keys $8, 16, \ldots, 80$ reach only 2 slots modulo 16, 3 slots modulo 12 and 5 slots modulo 10, but 10 slots modulo 13.
- **$m = 2^p - 1$ for strings in radix $2^p$.** With $m = 255$ and each character a byte, the strings `stop`, `pots`, `tops` and `spot` all hash to 199, because each one is the sum of its bytes modulo 255. With the prime $m = 251$, they hash to 121, 151, 129 and 25.
- **Negative keys.** In C, Java and Go, `-7 % 10` is $-7$, which is not a valid slot. Write `((k % m) + m) % m`, or reduce an unsigned value. Python's `%` already returns a value in $\{0, \ldots, m - 1\}$ for $m > 0$.
- **Overflow in the string loop.** Line L5 computes $x \cdot r + c$ with $x < m$. With 64-bit words, $m \cdot r$ must stay below $2^{64}$, so a modulus near $2^{61}$ needs a 128-bit product.
- **Changing $m$ without rehashing.** The slot $k \bmod m$ depends on $m$. When the table grows, each key must be hashed again for the new $m$.
- **Chosen keys.** A fixed $m$ is public. An attacker can send keys $k, k + m, k + 2m, \ldots$ that all land in one slot, an [algorithmic complexity attack](/algorithmic-complexity-attack/).

## Exercises

1. Show that for keys $k = c + j d$ with $j = 0, 1, \ldots$, the slots $k \bmod m$ form a set of size $m / \gcd(d, m)$.
2. Let $m = 2^p - 1$ and let a string be read as a number in base $2^p$. Show that two strings that are permutations of each other have the same hash value.
3. Write lines L3 to L6 for $m = 2^{61} - 1$ with 64-bit words, and show how to reduce a product of two numbers below $m$ with shifts and additions only.

## References
