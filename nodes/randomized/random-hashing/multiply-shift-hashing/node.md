---
tag: Z4W792
kind: definition
slug: multiply-shift-hashing
name: Multiply-shift hashing
aliases:
- Dietzfelbinger multiply-shift
- multiply-add-shift
- multiply-shift family
- pair-multiply-shift
area: randomized/random-hashing
level: advanced
summary: Fast 2-universal family computing (a*x) shifted right, using one multiplication and a shift per key.
prereqs: [universal-hash-family, pairwise-independence, word-ram]
see_also: [multiplicative-hashing, universal-hashing, dot-product-hashing, k-independent-hashing, tabulation-hashing, universal-hashing-expected-chain-length]
sources:
  - paper: doi:10.1006/jagm.1997.0873
    title: Martin Dietzfelbinger, Torben Hagerup, Jyrki Katajainen and Martti Penttonen, A reliable randomized algorithm for the closest-pair problem, Journal of Algorithms 25(1), 19 to 51, 1997
    locator: the multiplicative class of hash functions and the lemma that two keys collide with probability at most 2/m
  - paper: doi:10.1007/3-540-60922-9_46
    title: Martin Dietzfelbinger, Universal hashing and k-wise independent random variables via integer arithmetic without primes, STACS 96, Lecture Notes in Computer Science 1046, 1996
    locator: the strongly universal multiply-add-shift class with a product of w + l - 1 bits
  - paper: doi:10.48550/arXiv.1504.06804
    title: Mikkel Thorup, High speed hashing for integers and strings, lecture notes, arXiv 1504.06804, 2015
    locator: Section 2.3 (multiply-shift and its 2/m bound), Section 3.3 (strongly universal multiply-shift), Section 3.4 (vector multiply-shift) and Section 3.5 (pair-multiply-shift)
---

Multiply-shift hashing is the family of hash functions $h_a(x) = (a x \bmod 2^w) \gg (w - \ell)$ on $w$-bit keys, with a random odd $w$-bit multiplier $a$: multiply in one machine word and keep the top $\ell$ bits of the low word, for a table of $m = 2^\ell$ slots. It needs no prime, no division and no table, just one multiplication and one shift. Dietzfelbinger, Hagerup, Katajainen and Penttonen (1997) proved that two distinct keys collide with probability at most $2/m$, so the family is 2-approximately universal, and all the expected bounds of [universal hashing](/universal-hashing/) hold with a factor of at most 2. Adding a random $b$ and taking the product in a word of $\bar w \ge w + \ell - 1$ bits gives multiply-add-shift, which is [pairwise independent](/pairwise-independence/) (Dietzfelbinger 1996). This page states the family and its guarantees as a randomized object. The page [multiplicative hashing](/multiplicative-hashing/) treats the same formula as a practical technique with a fixed or random multiplier, including Fibonacci hashing.

## Definition

Let $w \ge \ell \ge 1$ be integers, and let keys be integers in $\{0, \ldots, 2^w - 1\}$. Write $x \gg s$ for $\lfloor x / 2^s \rfloor$.

**Multiply-shift.** For an odd $a \in \{1, 3, \ldots, 2^w - 1\}$,
$$h_a(x) = \big((a \cdot x) \bmod 2^w\big) \gg (w - \ell) \in \{0, \ldots, 2^\ell - 1\}.$$
The *multiply-shift family* is $\{h_a : a \text{ odd}\}$, with $2^{w-1}$ functions, and $a$ is drawn uniformly. In C on unsigned $w$-bit words this is `(a*x) >> (w-l)`, since the product wraps modulo $2^w$.

**Multiply-add-shift.** Let $\bar w \ge w + \ell - 1$, and let $a, b$ be uniform in $\{0, \ldots, 2^{\bar w} - 1\}$. Then
$$h_{a,b}(x) = \big((a x + b) \bmod 2^{\bar w}\big) \gg (\bar w - \ell).$$
For 32-bit keys and $\ell \le 32$, the choice $\bar w = 64$ fits one 64-bit word.

**Vector and pair-multiply-shift.** For keys $x = (x_0, \ldots, x_{d-1})$ of $d$ words of $w$ bits, with $a_0, \ldots, a_{d-1}, b$ uniform in $\{0, \ldots, 2^{\bar w} - 1\}$ and $\bar w \ge w + \ell - 1$, vector multiply-shift is
$$h(x) = \Big(\big(\textstyle\sum_i a_i x_i + b\big) \bmod 2^{\bar w}\Big) \gg (\bar w - \ell).$$
For even $d$, pair-multiply-shift replaces the sum by $\sum_{i < d/2} (a_{2i} + x_{2i+1})(a_{2i+1} + x_{2i})$, which uses half as many multiplications. Thorup credits this trick to the UMAC paper of Black, Halevi, Krawczyk, Krovetz and Rogaway (1999).

**Theorem (Dietzfelbinger, Hagerup, Katajainen and Penttonen 1997).** For all keys $x \ne y$ in $\{0, \ldots, 2^w - 1\}$, $\Pr_a[h_a(x) = h_a(y)] \le 2/2^\ell = 2/m$.

*Proof.* Write $x - y = 2^r z$ with $z$ odd and $0 \le r < w$; we may take $x > y$. Let $A = ax \bmod 2^w$, $B = ay \bmod 2^w$ and $D = (A - B) \bmod 2^w = a 2^r z \bmod 2^w$.

*Step 1: the law of $D$.* Multiplication by the odd number $z$ is a bijection on the odd residues modulo $2^{w-r}$, so as $a$ runs over the odd numbers, $az \bmod 2^{w-r}$ is uniform on the $2^{w-r-1}$ odd residues. Hence $D = 2^r o$, where $o$ is uniform on the odd numbers in $\{1, \ldots, 2^{w-r} - 1\}$.

*Step 2: a collision forces $D$ to be near 0.* If $h_a(x) = h_a(y)$, then $A$ and $B$ have the same top $\ell$ bits, so $|A - B| < 2^{w-\ell}$. Then $D = A - B$ or $D = 2^w + (A - B)$, so $D < 2^{w-\ell}$ or $D > 2^w - 2^{w-\ell}$.

*Step 3: count.* If $r \ge w - \ell$, then $2^r \le D \le 2^w - 2^r$, which meets neither range, and the probability is 0. If $r < w - \ell$, then $D < 2^{w-\ell}$ means $o < 2^{w-\ell-r}$, which holds for $2^{w-\ell-r-1}$ of the $2^{w-r-1}$ odd values: probability $2^{-\ell}$. By the symmetry $o \mapsto 2^{w-r} - o$ of the odd values, $D > 2^w - 2^{w-\ell}$ also has probability $2^{-\ell}$. So a collision has probability at most $2 \cdot 2^{-\ell} = 2/m$. $\blacksquare$

**Theorem (Dietzfelbinger 1996).** If $\bar w \ge w + \ell - 1$, multiply-add-shift is pairwise independent: for $x \ne y$ and all $s, t \in \{0, \ldots, 2^\ell - 1\}$, $\Pr_{a,b}[h_{a,b}(x) = s \wedge h_{a,b}(y) = t] = 2^{-2\ell}$. Thorup's notes prove the same for vector multiply-shift and leave pair-multiply-shift as an exercise.

## Examples and non-examples

**A trace.** Let $w = 8$, $\ell = 3$ and $a = 179$, in binary $10110011$. The key 1 gives $179 = 10110011_2$, top three bits $101_2 = 5$. The key 9 gives $9 \cdot 179 = 1611$, and $1611 \bmod 256 = 75 = 01001011_2$, top bits $010_2 = 2$. So $h_{179}(1) = 5$ and $h_{179}(9) = 2$.

**The factor 2 is reached.** Over all odd multipliers, the worst pair of keys collides with probability exactly $2/m$ in each case checked by enumeration: $1/2$ for $(w, \ell) = (4, 2)$ and $(5, 2)$, and $1/4$ for $(6, 3)$ and $(8, 3)$. For $w = 8$ and $\ell = 3$, the keys 1 and 9 collide for 32 of the 128 odd multipliers. So the family is not [universal](/universal-hash-family/) in the strict sense.

**Not uniform on single keys.** $h_a(0) = 0$ for every $a$, and $h_a(2^{w-1}) = 2^{\ell - 1}$ for every odd $a$, since $a 2^{w-1} \bmod 2^w = 2^{w-1}$. So plain multiply-shift is not 1-independent, let alone pairwise independent. Multiply-add-shift fixes this with $b$.

**The extra bits are needed.** By enumeration, multiply-add-shift is exactly pairwise independent for $(w, \ell, \bar w) = (2, 2, 3), (3, 2, 4), (3, 3, 5)$ and $(4, 2, 5)$, all with $\bar w = w + \ell - 1$. With one bit fewer, $(3, 2, 3)$ and $(3, 3, 4)$, it is not. The same check for keys of two $w$-bit words confirms vector multiply-shift and pair-multiply-shift for $(w, \ell, \bar w) = (2, 1, 2), (2, 2, 3), (2, 2, 4)$ and $(3, 2, 4)$, and shows both fail for $(2, 2, 2)$.

**An even multiplier.** If $a$ may be even, $a = 0$ maps all keys to slot 0, and $a = 2^{w-1}$ maps every even key to slot 0. The keys 0 and $2^{w-1}$ collide for every even $a$, so with probability $1/2$: for $w = 6$ and $\ell = 3$ that is twice the bound $2/m = 1/4$. Draw $a$ odd, for example as $2u + 1$.

**Low bits instead of high bits.** $(ax) \bmod 2^\ell$ depends only on the low $\ell$ bits of $x$, so the keys $x$ and $x + 2^\ell$ collide for every $a$. The shift must keep the high bits of the low word.

**The fixed golden-ratio multiplier.** Fibonacci hashing uses $a \approx 2^w/\varphi$. With $a$ fixed, there is no probability over $a$, and an input chosen for that $a$ can put all keys in one slot. The guarantee above is for a random odd $a$ only.

## Related definitions

- [Universal hash family](/universal-hash-family/). Multiply-shift is $2/m$-almost universal, which some authors call 2-approximately universal.
- [Pairwise independence](/pairwise-independence/). Multiply-add-shift and vector multiply-shift have it; plain multiply-shift does not.
- [Multiplicative hashing](/multiplicative-hashing/). The same formula as a hashing technique, with the fixed-multiplier variants and their history.
- [Dot-product hashing](/dot-product-hashing/). The prime-field version of vector hashing, exactly universal, but with a division per key.
- [Expected chain length under universal hashing](/universal-hashing-expected-chain-length/). With multiply-shift, the expected chain of a stored key is at most $1 + 2(n-1)/m$.
- [k-independent hashing](/k-independent-hashing/) and [tabulation hashing](/tabulation-hashing/). The next steps when pairs are not enough, for example for linear probing.

## References
