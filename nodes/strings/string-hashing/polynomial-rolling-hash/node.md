---
tag: C4WFX1
kind: technique
slug: polynomial-rolling-hash
name: Polynomial rolling hash
aliases:
- rolling hash
- polynomial string hash
- Horner-style string hash
area: strings/string-hashing
level: core
summary: Hash a string as a polynomial in a base modulo a prime, and update the hash of a sliding window in O(1).
prereqs: [hash-function, horner-rule, prime-number, sliding-window]
see_also: [polynomial-hash-collision-bound, rabin-karp, substring-equality-queries, dynamic-polynomial-hashing, anti-hash-tests, rabin-fingerprint, universal-string-hashing, mersenne-prime]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.2, The Rabin-Karp algorithm (Horner's rule for the pattern value, the window update in constant time, and the exercises of the section)
  - paper: doi:10.1147/rd.312.0249
    title: Richard M. Karp and Michael O. Rabin, Efficient randomized pattern-matching algorithms, IBM Journal of Research and Development 31(2) (1987), 249-260
    locator: the fingerprint functions that can be updated when the window moves by one character
  - url: https://ioinformatics.org/journal/INFOL119.pdf
    title: Jakub Pachocki and Jakub Radoszewski, Where to use and how not to use polynomial string hashing, Olympiads in Informatics 7 (2013), 90-100
    locator: Section 2 (the hash of a string, prefix hashes and the substring formula, the choice of the modulus, and the attack on the modulus 2^64)
  - url: https://arxiv.org/abs/1504.06804
    title: Mikkel Thorup, High speed hashing for integers and strings, lecture notes (arXiv 1504.06804)
    locator: Section 5.3, Hashing variable length strings (Horner's rule with the coefficients in reverse order, and arithmetic modulo the Mersenne prime 2^89 - 1)
---

A polynomial rolling hash maps a string $x_0 x_1 \cdots x_{\ell-1}$ to the value $\sum_i c(x_i)\, r^{\ell-1-i} \bmod p$, where $c$ gives each character an integer code, $p$ is a [prime](/prime-number/) and $r$ is a base. Two algebraic identities make it useful: the hash of a window can be updated in $O(1)$ time when the window moves by one character, and after $O(n)$ preprocessing the hash of any substring is a difference of two prefix hashes. With $r$ chosen at random after the input is fixed, two different strings of length at most $n$ get the same hash with probability at most $(n-1)/p$, by the [collision bound](/polynomial-hash-collision-bound/). The technique is the base of [Rabin-Karp](/rabin-karp/) and of [substring equality queries](/substring-equality-queries/).

## In plain words

Give each letter a number, for example a is 1, b is 2 and c is 3. Then read a word as a number written in a large base: with base 10, the word abc becomes 123. Keep only the remainder after division by a fixed large prime, so the number stays small.

When a window slides one letter to the right over a text, you do not have to read the whole window again. Take away the value of the letter that leaves, shift what remains by one place, and add the letter that comes in. This is a few arithmetic steps, whatever the length of the window.

Two equal words always get equal numbers. Two different words can get equal numbers by bad luck. If the base is picked at random, this bad luck is rare, but it is never impossible.

## When it applies

- **Many comparisons of strings or substrings.** The hash replaces a comparison of $\ell$ characters by a comparison of two numbers. The cost of the hash is paid once per string, or once per text for all its substrings.
- **Windows of fixed length.** A scan that looks at every window of length $\ell$ of a text of length $n$ computes all $n - \ell + 1$ hashes in $O(n)$ time, while hashing each window from scratch takes $O(n\ell)$.
- **Substrings at arbitrary positions.** After prefix hashes and powers of $r$ are stored, the hash of $T[i \ldots j-1]$ takes $O(1)$ time. This is the step that turns many string problems into binary searches over lengths.
- **A small error is acceptable, or a check follows.** The answer "equal" can be wrong with small probability. The technique fits when a wrong answer is rare enough for the use, or when each "equal" is verified, as in Rabin-Karp.
- **The input does not depend on the base.** The probability bound assumes that the strings are fixed before $r$ is drawn. An adversary who knows $r$ and $p$, or who can learn them from the program's behavior, can build collisions (see [anti-hash tests](/anti-hash-tests/)).

## The template

**Conventions.** Characters are integers given by a code $c : \Sigma \to \{1, \ldots, p - 1\}$ that is one-to-one; the codes start at 1, not 0, for the reason in the pitfalls. Indices are 0-based, and $T[i \ldots j-1]$ is the substring of length $j - i$ that starts at $i$; it is empty when $j = i$. Windows of a text overlap: the window at $s$ and the window at $s + 1$ share $\ell - 1$ characters. All arithmetic is modulo $p$, with results in $\{0, \ldots, p-1\}$.

**Definition.** For a string $x$ of length $\ell$, $h(x) = \sum_{i=0}^{\ell-1} c(x_i)\, r^{\ell-1-i} \bmod p$. The first character has the highest power, so [Horner's rule](/horner-rule/) computes $h$ from left to right: $h \leftarrow h \cdot r + c(x_i)$. The empty string has hash $0$.

```pseudo id=main
ALL-WINDOW-HASHES(T[0 .. n-1], ℓ)              ▷ the hash of every window of length ℓ
L1  r ← a uniform random element of {0, ..., p − 1}   ▷ hole: the base, drawn after T is fixed
L2  if ℓ = 0 then emit (s, 0) for s = 0, ..., n; return
L3  if ℓ > n then return
L4  R ← r^(ℓ−1) mod p                           ▷ the weight of the first window character
L5  h ← 0
L6  for i ← 0 to ℓ − 1 do h ← (h · r + c(T[i])) mod p    ▷ hole: the code c
L7  emit (0, h)
L8  for s ← 1 to n − ℓ do
L9      h ← ((h − c(T[s − 1]) · R) · r + c(T[s + ℓ − 1])) mod p
L10     emit (s, h)

PREFIX-HASHES(T[0 .. n-1])                      ▷ for hashes of arbitrary substrings
L11 H[0] ← 0; W[0] ← 1
L12 for i ← 0 to n − 1 do
L13     H[i + 1] ← (H[i] · r + c(T[i])) mod p
L14     W[i + 1] ← W[i] · r mod p

SUBSTRING-HASH(i, j)                            ▷ the hash of T[i .. j−1], for 0 ≤ i ≤ j ≤ n
L15 return (H[j] − H[i] · W[j − i]) mod p
```

The holes are the prime $p$, the base $r$ and the code $c$. The use of the hashes, in place of each "emit", is a further hole: compare with a pattern hash, insert into a hash table, or compare two substrings.

**Why the window update is right.** Write $h_s = \sum_{t=0}^{\ell-1} c(T[s+t])\, r^{\ell-1-t}$ for the hash of the window at $s$. Its first term is $c(T[s])\, r^{\ell-1} = c(T[s]) R$. Then

$$(h_s - c(T[s]) R)\, r + c(T[s+\ell]) = \sum_{t=1}^{\ell-1} c(T[s+t])\, r^{\ell-t} + c(T[s+\ell]) = \sum_{t=0}^{\ell-1} c(T[s+1+t])\, r^{\ell-1-t} = h_{s+1},$$

by the change of index $t \to t + 1$. All steps are ring operations, so they hold modulo $p$. Line L9 applies this with $s - 1$ in place of $s$.

**Why the substring formula is right.** By induction on $j$, line L13 gives $H[j] = h(T[0 \ldots j-1])$, and line L14 gives $W[k] = r^k$. Split the sum for $H[j]$ at $i$:

$$H[j] = \sum_{t=0}^{j-1} c(T[t])\, r^{j-1-t} = r^{j-i} \sum_{t=0}^{i-1} c(T[t])\, r^{i-1-t} + \sum_{t=i}^{j-1} c(T[t])\, r^{j-1-t} = W[j-i]\, H[i] + h(T[i \ldots j-1]).$$

So line L15 returns $h(T[i \ldots j-1])$.

**Cost.** ALL-WINDOW-HASHES does $O(\ell)$ operations for the first window, with $R$ computed by [fast exponentiation](/modular-exponentiation/) or by $\ell - 1$ multiplications, and $O(1)$ for each later window: $O(n)$ in total. PREFIX-HASHES takes $O(n)$ time and $2(n + 1)$ stored values, and each SUBSTRING-HASH takes $O(1)$ time. An operation means one multiplication modulo $p$; it is $O(1)$ on the [word RAM](/word-ram/) when $p$ fits in a word.

**Choosing the modulus and the base.**

- *A prime modulus.* The collision bound $(n - 1)/p$ for two fixed distinct strings of length at most $n$ needs $p$ prime, $r$ uniform in $\{0, \ldots, p-1\}$, and the strings fixed before $r$ is drawn. For $q$ comparisons the union bound gives $q(n-1)/p$, which must be small, not only the bound for one comparison.
- *The Mersenne prime $2^{61} - 1$.* A product of two residues is below $2^{122}$ and fits in 128 bits. Since $2^{61} \equiv 1$, a value $v$ reduces as $(v \bmod 2^{61}) + \lfloor v / 2^{61} \rfloor$, then by at most two subtractions of $p$. Both parts are a mask and a shift. With $n = q = 10^6$, the union bound is about $4.3 \times 10^{-7}$. See [Mersenne prime](/mersenne-prime/) and [modular multiplication](/modular-multiplication/).
- *Two primes near $10^9$.* With 64-bit integers and no 128-bit product, use two primes $p_1, p_2$ below $2^{31}$ with independent bases $r_1, r_2$, and treat the pair of hashes as the hash. For a fixed pair of strings the two collision events are independent, so the bound is $\frac{n-1}{p_1} \cdot \frac{n-1}{p_2}$.
- *Not $2^{64}$.* Arithmetic with natural overflow modulo $2^{64}$ is fast but has no such bound: $\mathbb{Z}/2^{64}$ is not a field. Strings of length 2048 built from the [Thue-Morse word](/thue-morse-word/) collide for every odd base, and every even base fails on short strings (see [anti-hash tests](/anti-hash-tests/)).

**Example.** Take $p = 101$, $r = 10$ and the codes $c(\mathrm{a}) = 1$, $c(\mathrm{b}) = 2$, $c(\mathrm{c}) = 3$, so the hash of a short string is its decimal reading modulo 101. For $T = $ abcab and $\ell = 3$, $R = 10^2 = 100$.

| step | window | computation | hash |
|---|---|---|---|
| L6 | $T[0..2]$ = abc | $123 \bmod 101$ | 22 |
| L9, $s = 1$ | $T[1..3]$ = bca | $(22 - 1 \cdot 100) \cdot 10 + 1 = -779 \equiv 29$ | 29 |
| L9, $s = 2$ | $T[2..4]$ = cab | $(29 - 2 \cdot 100) \cdot 10 + 2 = -1708 \equiv 9$ | 9 |

The direct values agree: $231 \bmod 101 = 29$ and $312 \bmod 101 = 9$. The intermediate value is negative, so the final reduction must return a residue in $\{0, \ldots, 100\}$.

For PREFIX-HASHES on the same text, $H = [0, 1, 12, 22, 19, 91]$ and $W = [1, 10, 100, 91, 1, 10]$. The hash of $T[2 \ldots 4]$ = cab is $H[5] - H[2]\, W[3] = 91 - 12 \cdot 91 = -1001 \equiv 9$, the same value as the window. The hash of $T[3 \ldots 4]$ = ab is $H[5] - H[3]\, W[2] = 91 - 2200 \equiv 12$, which is the decimal value 12. Here $W[4] = 1$ because $10^4 = 10000 = 99 \cdot 101 + 1$: the base has order 4 modulo 101, so a base that is fixed in advance can give many collisions for patterns chosen with that knowledge.

## Classic examples

- [Rabin-Karp](/rabin-karp/): compare the pattern hash with all window hashes, and verify each hash match.
- [Karp-Rabin with many patterns](/karp-rabin-multiple-patterns/): look up each window hash in a table of pattern hashes, for patterns of one length.
- [Substring equality queries](/substring-equality-queries/): test $T[i \ldots i+\ell-1] = T[j \ldots j+\ell-1]$ in $O(1)$ time after $O(n)$ preprocessing.
- [Longest common extension](/longest-common-extension-query/) by [binary search](/binary-search/) on the length, with substring hashes as the test, in $O(\log n)$ time per query; the same test compares two suffixes, which gives a simple [suffix array](/suffix-array/) construction in $O(n \log^2 n)$ time.
- [Longest repeated substring](/longest-repeated-substring/) and [longest common substring](/longest-common-substring/): binary search on the length $\ell$, and for each $\ell$ put all window hashes in a hash table.
- [Longest palindromic substring](/longest-palindromic-substring/): compare the hash of a substring with the hash of the same range in the reversed string.
- [String equality testing](/string-equality-testing/) between two machines: send one hash instead of the whole string.

## Variations

- **Lowest power first.** Some texts define $h(x) = \sum_i c(x_i)\, r^i$. Prefix sums are then direct, but comparing two substrings at different positions needs a multiplication by a power of $r$ on one side, or a division by $r^i$, which needs the [modular inverse](/modular-inverse/) of $r$ and fails for $r = 0$. The form on this page avoids division.
- **Several hashes.** Use $t$ independent bases, modulo the same prime or different primes. For one pair of strings the collision bound becomes $((n-1)/p)^t$.
- **Point updates.** Store the terms $c(T[i])\, r^{n-1-i}$ in a [Fenwick tree](/fenwick-tree/) or a [segment tree](/segment-tree/), so that a character can change in $O(\log n)$ time: [dynamic polynomial hashing](/dynamic-polynomial-hashing/).
- **Two dimensions.** Hash each row of a matrix window with a base $r_1$, then hash the column of row hashes with a second base $r_2$. The window hash slides in both directions with the same identities.
- **Polynomials over GF(2).** The [Rabin fingerprint](/rabin-fingerprint/) reads a bit string as a polynomial over the field with two elements and takes the residue modulo a random irreducible polynomial. The update uses XOR and shifts and has no carries.
- **Hash tables of strings.** To index a table of size $M$, reduce the hash further, for example by a [universal hash](/universal-string-hashing/) from $\{0, \ldots, p-1\}$ to $\{0, \ldots, M-1\}$. The fixed-key hashes [FNV](/fnv-hash/) and [MurmurHash](/murmurhash/) are faster but give no collision bound for strings fixed in advance.

## Pitfalls

- **Code 0 for a character.** If $c(\mathrm{a}) = 0$, then $h(\mathrm{b}) = h(\mathrm{ab}) = h(\mathrm{aab})$ for every base, because a leading zero coefficient adds nothing. Strings of different lengths then collide with certainty. Use codes from 1, or compare lengths first. For bytes, use the byte value plus 1.
- **Codes equal modulo $p$.** The codes must be distinct modulo $p$, so the alphabet must have fewer than $p$ characters. For Unicode text with a small prime, encode as bytes or use a larger prime.
- **Negative remainders.** In C, C++, Java and Go, the remainder of a negative number is negative. Lines L9 and L15 subtract, so add $p$ (or a multiple of $p$) before the last reduction. Python's `%` already returns a value in $\{0, \ldots, p-1\}$.
- **Overflow.** With $p$ near $10^9$, a product of two residues fits in 64 bits, but $h \cdot r + c$ must not first overflow a 32-bit type. With $p = 2^{61} - 1$, the product needs 128 bits. In line L9, reduce $c(T[s-1]) R$ before the subtraction.
- **A fixed base or a known modulus.** A base written in the source, such as 31 or 131, gives no probability bound at all: the strings are no longer chosen independently of $r$. In contests with hacks and in servers that hash user input, draw $r$ at run time from a good random source.
- **Modulus $2^{64}$.** See the template: the Thue-Morse strings collide for every odd base.
- **The base 0 or 1.** With $r = 0$, the hash is the code of the last character; with $r = 1$, it is the sum of the codes, so all anagrams collide. These bases are among the $p$ values in the bound, so a uniform $r$ picks them only with probability $2/p$. Excluding them changes the bound to $(n-1)/(p-2)$.
- **One comparison versus many.** The bound $(n-1)/p$ is for one pair. A program that makes $q$ comparisons needs $q(n-1)/p$ to be small, and a program that needs all of $N$ hashes to be distinct needs $p$ much larger than $N^2$, by the [birthday paradox](/birthday-paradox/). The prime $10^9 + 7$ is not enough for $10^5$ distinct strings.
- **Equal hashes are not equal strings.** A matcher that reports every hash match without a check is a [Monte Carlo](/monte-carlo-algorithm/) algorithm. Verify each match when the answer must be exact.

## Exercises

1. Working modulo $q = 11$ with the decimal digits as codes 0 to 9 and base 10, how many windows of the text 3141592653589793 have the same hash as the pattern 26, and how many of them are spurious hits? *Answer:* the windows 15, 59, 92 and 26, at positions 3 to 6, all have value $4 \bmod 11$; the first three are spurious. (This is an exercise in CLRS, Section 32.2, with the digits read as numbers.)
2. Show that if $c(\mathrm{a}) = 0$, the strings $\mathrm{a}^k \mathrm{b}$ for $k = 0, 1, 2, \ldots$ all have the same hash for every base and every modulus.
3. Give the window update for the form $h(x) = \sum_i c(x_i)\, r^i$, and state when it needs $r^{-1}$.
4. For $p = 101$, find all bases $r$ for which the strings $1\,0\,0\,0\,0$ and $0\,0\,0\,0\,1$ (as code sequences) collide. *Answer:* the $r$ with $r^4 = 1$, which are $1$, $10$, $91$ and $100$.
5. Prove that the pair of hashes modulo two different primes $p_1, p_2$, with independent uniform bases, gives collision probability at most $\frac{(n-1)^2}{p_1 p_2}$ for two fixed distinct strings of length at most $n$.

## References
