---
tag: 5RV91M
kind: technique
slug: multiplicative-hashing
name: Multiplicative hashing
aliases:
- Fibonacci hashing
- division method
- multiplication method
- multiply-shift hashing
area: data-structures/hashing
level: intro
summary: Hash by multiplying the key by a constant and taking high-order bits.
prereqs: [hash-function, word-ram]
see_also: [multiply-shift-hashing, division-method, universal-hash-family, universal-hashing, hash-table, tabulation-hashing, randomized-closest-pair, modular-inverse]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), the multiplicative scheme, Fibonacci hashing and the theorem on the points {θ}, {2θ}, ..., {nθ}
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.3 (Hash functions), the multiplication method and the multiply-shift method
  - paper: doi:10.1006/jagm.1997.0873
    title: Martin Dietzfelbinger, Torben Hagerup, Jyrki Katajainen and Martti Penttonen, A reliable randomized algorithm for the closest-pair problem, Journal of Algorithms 25(1), 1997
    locator: pages 19 to 51 (the multiplicative class of hash functions and its collision bound)
  - url: https://arxiv.org/abs/1504.06804
    title: Mikkel Thorup, High speed hashing for integers and strings, lecture notes, arXiv:1504.06804
    locator: the sections on multiply-shift and on strongly universal multiply-add-shift
  - url: https://github.com/torvalds/linux/blob/master/include/linux/hash.h
    title: Linux kernel source, include/linux/hash.h
    locator: GOLDEN_RATIO_32, GOLDEN_RATIO_64 and hash_32
---

Multiplicative hashing maps a key $k$ to one of $m = 2^\ell$ slots by multiplying it by a constant $a$ and keeping the top $\ell$ bits of the low word of the product: $h(k) = (a k \bmod 2^w) \gg (w - \ell)$ on a machine with $w$-bit words. It costs one multiplication and one shift, with no division, which makes it one of the fastest [hash functions](/hash-function/) for integer keys on the [word RAM](/word-ram/). With a fixed odd constant close to $2^w/\varphi$, where $\varphi$ is the golden ratio, it is Knuth's Fibonacci hashing. With $a$ drawn at random among the odd numbers it is the multiply-shift scheme of Dietzfelbinger, Hagerup, Katajainen and Penttonen, in which two distinct keys collide with probability at most $2/m$.

## In plain words

Multiply the key by a large fixed number, in the way a computer multiplies: the result wraps around and keeps only one word. Then keep the leftmost few bits of that word as the slot number.

The left bits of the product depend on every bit of the key, so keys that differ only a little end up far apart. The right bits of the product depend only on the right bits of the key, so they are a bad choice of slot.

The fixed number matters. A number based on the golden ratio spreads keys that come in a regular pattern, such as 16, 32, 48, almost evenly over the table. If the program picks the number at random among the odd numbers, then any two keys share a slot with a small chance, whatever keys the user supplies.

## When it applies

- The keys are integers of at most one word, or they are first reduced to one word, for example by a string hash.
- The table size is a power of two, so the slot is a group of bits and needs no division.
- Speed of the hash matters more than strong guarantees: one multiplication is cheaper than the division of the [division method](/division-method/).
- The keys have regular patterns, such as arithmetic progressions or keys that differ only in their high bits, which defeat a hash that keeps low bits.
- With a random multiplier: the analysis needs only a bound on the collision probability of each pair of keys, as for chaining in [universal hashing](/universal-hashing/).

## The template

```pseudo id=main
MULT-HASH(k)                    ▷ k: an unsigned w-bit key; the table has m = 2^ℓ slots, 1 ≤ ℓ ≤ w
L1  a ← the multiplier           ▷ hole: a fixed odd constant, or a random odd number drawn once
L2  t ← (a · k) mod 2^w          ▷ the low word of the product; free with unsigned wraparound
L3  return t ≫ (w − ℓ)           ▷ the top ℓ bits of t, a slot in {0, ..., m − 1}
```

**The hole.** Line L1 is done once, when the table is created, not at each call. Knuth's choice is $a = \lfloor 2^w/\varphi \rfloor$ rounded to an odd number; for $w = 32$ this is $a = 2654435769$, and for $w = 64$ it is $11400714819323198485$. The multiply-shift choice is a uniform odd number in $\{1, 3, \dots, 2^w - 1\}$.

**Why the top bits.** Bit $i$ of $a k \bmod 2^w$ depends only on bits $0$ to $i$ of $k$ and of $a$, because a carry moves only to the left. So the low $\ell$ bits of the product depend only on the low $\ell$ bits of the key, and the top bits depend on all of them. Line L3 keeps the top bits.

**The real-number form.** Let $A = a/2^w$, a number in $(0, 1)$. Then $(a k \bmod 2^w)/2^w$ is the fractional part $\{kA\}$, so line L3 returns $\lfloor m \{kA\} \rfloor$. This is the multiplication method of CLRS and Knuth: multiply by a constant $A$ in $(0, 1)$, keep the fraction, scale it to $m$ slots. The integer form computes it exactly, in one word.

### A worked example

Take $w = 32$, $\ell = 14$ (so $m = 16384$), $a = 2654435769$ and $k = 123456$. The full product is $k a = 76300 \cdot 2^{32} + 17612864$, so line L2 gives $t = 17612864$, and line L3 gives $17612864 \gg 18 = 67$. The real-number form with $A = (\sqrt{5} - 1)/2$ and $m = 10000$ maps the same key to $\lfloor 10000 \{123456 A\} \rfloor = 41$.

With the same $a$ and 16 slots ($\ell = 4$), the keys $1, 2, \dots, 8$ go to the slots $9, 3, 13, 7, 1, 11, 5, 15$, and the keys $16, 32, \dots, 128$ go to the slots $14, 12, 10, 8, 7, 5, 3, 1$. Both sets get eight different slots. The division method $k \bmod 16$ sends all of $16, 32, \dots, 128$ to slot 0.

### The golden ratio

Knuth explains the choice of $A = 1/\varphi = (\sqrt{5} - 1)/2$ with a theorem on the points $\{\theta\}, \{2\theta\}, \dots, \{n\theta\}$ for an irrational $\theta$ (TAOCP Volume 3, Section 6.4). These $n$ points cut the interval $[0, 1)$ into $n + 1$ parts with at most three different lengths, and the point $\{(n+1)\theta\}$ falls into one of the longest parts. For $\theta = 1/\varphi$, each new point cuts a longest part in the golden ratio, so the parts stay close to equal. For $n = 10$ the 11 parts have the three lengths $0.0557$, $0.0902$ and $0.1459$, and for $n = 20$ the 21 parts have only the two lengths $0.0344$ and $0.0557$. Keys in an arithmetic progression $k, k + d, k + 2d, \dots$ have the fractions $\{kA\} + i\{dA\}$, so they are spread in the same way.

### The multiply-shift bound

**Theorem (Dietzfelbinger, Hagerup, Katajainen and Penttonen).** Let $1 \le \ell \le w$, let $m = 2^\ell$, let $h_a(k) = (a k \bmod 2^w) \gg (w - \ell)$, and let $a$ be uniform over the $2^{w-1}$ odd numbers in $\{1, \dots, 2^w - 1\}$. Then for each two keys $x \ne y$ in $\{0, \dots, 2^w - 1\}$,

$$\Pr[h_a(x) = h_a(y)] \le \frac{2}{m}.$$

*Proof.* Let $z = (x - y) \bmod 2^w$. Then $z \ne 0$, so $z = z' 2^r$ with $z'$ odd and $0 \le r < w$. Let $d = a z \bmod 2^w$, which equals $(a x - a y) \bmod 2^w$.

1. *The distribution of $d$.* We have $d = 2^r \cdot (a z' \bmod 2^{w-r})$. When $a$ is uniform over the odd numbers below $2^w$, the residue $a \bmod 2^{w-r}$ is uniform over the odd residues below $2^{w-r}$, because each odd residue has exactly $2^r$ odd preimages. Multiplication by the odd number $z'$ is a bijection on the odd residues modulo $2^{w-r}$, since $z'$ has an inverse. So $a z' \bmod 2^{w-r}$ is uniform over the odd residues, and $d = 2^r + 2^{r+1} u$ with $u$ uniform in $\{0, \dots, 2^{w-r-1} - 1\}$.
2. *A collision needs a small $d$.* Let $s = w - \ell$, $X = a x \bmod 2^w$ and $Y = a y \bmod 2^w$. If $X \gg s = Y \gg s$, then $|X - Y| < 2^s$, so $d = (X - Y) \bmod 2^w$ is in $\{1, \dots, 2^s - 1\}$ or in $\{2^w - 2^s + 1, \dots, 2^w - 1\}$ (and $d \ne 0$ because bit $r$ of $d$ is 1).
3. *Case $r \ge s$.* Then $d$ is a multiple of $2^r \ge 2^s$, and $d \le 2^w - 2^r \le 2^w - 2^s$. So $d$ is in neither range, and the probability of a collision is 0.
4. *Case $r < s$.* The condition $d < 2^s$ means $2^r(1 + 2u) < 2^s$, that is, $u < 2^{s-r-1} - 1/2$, which holds for exactly $2^{s-r-1}$ values of $u$. The map $d \mapsto 2^w - d$ sends the values of the form $2^r \cdot \text{odd}$ to values of the same form, so exactly $2^{s-r-1}$ values of $u$ also give $d > 2^w - 2^s$. So at most $2^{s-r}$ of the $2^{w-r-1}$ equally likely values of $u$ give a collision, and the probability is at most $2^{s-r}/2^{w-r-1} = 2^{s - w + 1} = 2/m$. $\square$

The factor 2 is reached. For $w = 8$ and $\ell = 3$, the keys 1 and 9 collide for 32 of the 128 odd multipliers, with probability $1/4 = 2/m$, so the family is 2-approximately universal but not [universal](/universal-hash-family/). Each bound of universal hashing then holds with an extra factor 2.

## Classic examples

- **[Hash tables](/hash-table/) with a power-of-two size.** A table that doubles its size keeps $m = 2^\ell$, and line L3 with a larger $\ell$ gives the new slot. The Linux kernel hashes a 32-bit value into $2^{\text{bits}}$ slots by `hash_32`, which multiplies by `GOLDEN_RATIO_32` $= 1640531527$ and shifts right by $32 - \text{bits}$. This constant is $2^{32} - 2654435769$, the negative of Knuth's multiplier modulo $2^{32}$.
- **[Separate chaining](/separate-chaining/) with a random multiplier.** Multiply-shift with a random odd $a$ gives expected chain length at most $1 + 2\alpha$ for each key of the table, by the chaining bound of [universal hashing](/universal-hashing/) with the factor 2.
- **[Randomized closest pair](/randomized-closest-pair/).** Dietzfelbinger, Hagerup, Katajainen and Penttonen introduced the multiply-shift class for the grid hashing of a linear-time closest-pair algorithm, where they needed a family that is fast and has a proven collision bound.
- **[Multiply-shift hashing](/multiply-shift-hashing/)** has its own page with the variants for long keys.

## Variations

- **Multiply-add-shift.** With a second random number $b$ and a product in a word of $\bar{w} \ge w + \ell - 1$ bits, $h_{a,b}(k) = ((a k + b) \bmod 2^{\bar{w}}) \gg (\bar{w} - \ell)$ is strongly universal. Thorup's notes give the proof. The usual setting is $w = 32$ and $\bar{w} = 64$.
- **Vectors and strings.** For a key of several words $x_0, \dots, x_{r-1}$, the pair-multiply-shift of Thorup's notes multiplies pairs of words with random multipliers, adds the products in a double word, and keeps the top bits. It needs about one multiplication for each two words.
- **The division method.** The [division method](/division-method/) $h(k) = k \bmod m$ uses a prime $m$ not close to a power of two. It needs a division, or a precomputed reciprocal, and it is weak on keys that differ by multiples of $m$.
- **Floating point.** The real-number form $\lfloor m \{kA\} \rfloor$ is the textbook definition. It is exact only when the product $kA$ is computed with enough bits; the integer form avoids the question.
- **Mixing first.** Some libraries apply a fixed bit-mixing step (shifts and XORs, or a few rounds of multiply and shift) to the key before the slot is taken from the low bits. This is a different design, which takes the slot from the bits that are cheap to mask.

## Pitfalls

- **Keeping the low bits.** Writing line L3 as $t \bmod 2^\ell$ makes the slot depend only on the low $\ell$ bits of $k$. All keys that agree in their low $\ell$ bits then collide, such as all multiples of $2^\ell$. Keep the top bits: $t \gg (w - \ell)$.
- **An even multiplier.** If $a = 2^s a'$ with $s \ge 1$, then $a k \bmod 2^w$ ignores the top $s$ bits of $k$, so keys that differ only in those bits always collide. For $w = 32$, $\ell = 4$ and $a = 2654435768$, the keys 5 and $5 + 2^{31}$ both go to slot 1. Choose $a$ odd in line L1.
- **A fixed multiplier and a hostile user.** For a fixed odd $a$, the keys $k_i = i \cdot a^{-1} \bmod 2^w$ for $i = 0, 1, \dots, 2^{w - \ell} - 1$ give $a k_i \bmod 2^w = i < 2^{w-\ell}$, so they all go to slot 0. With Knuth's 32-bit multiplier, $a^{-1} \bmod 2^{32} = 340573321$, and the keys $0, 340573321, 681146642, \dots$ fill slot 0 of a table of 1024 slots with $2^{22}$ keys. The [modular inverse](/modular-inverse/) is cheap to compute, so a fixed multiplier gives no protection against an [algorithmic complexity attack](/algorithmic-complexity-attack/). Draw $a$ at random when the input can be hostile.
- **Shift by the full width.** For $m = 1$, line L3 shifts by $w$ bits. In C this is undefined behaviour for a $w$-bit type. Treat $\ell = 0$ as a special case.
- **No wraparound in the language.** In Python and in other languages with big integers, line L2 needs an explicit mask: `t = (a * k) & ((1 << w) - 1)`. In Java, use `>>>`, not `>>`, so that the shift does not copy the sign bit.
- **The real-number form in doubles.** A 64-bit floating-point number has 53 bits of mantissa. For keys near $2^{64}$, the product $kA$ in floating point has lost all the bits of its fraction, so $\{kA\}$ is rounding noise. Use the integer form.
- **Multiply-shift for linear probing.** The bound is on pairs of keys only. It does not give the guarantees that [linear probing](/linear-probing/) needs; use a family with more independence there, such as [tabulation hashing](/tabulation-hashing/).

## Exercises

1. Prove that bit $i$ of $a k \bmod 2^w$ depends only on bits $0$ to $i$ of $a$ and of $k$.
2. Show that $\lfloor m \{k a / 2^w\} \rfloor = (a k \bmod 2^w) \gg (w - \ell)$ for $m = 2^\ell$ and integers $a, k \ge 0$.
3. For $w = 8$ and $\ell = 3$, show that no pair of distinct keys collides under every odd $a$, and find all pairs that collide under no odd $a$. Use the proof of the multiply-shift bound to explain the answer.
4. Show that the multiply-shift family is not strongly universal: find a key whose slot is the same for every $a$.
5. For a fixed odd multiplier $a$ and $m = 2^\ell$, prove that each slot receives exactly $2^{w - \ell}$ of the $2^w$ keys.

## References
