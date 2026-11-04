---
tag: 35X045
kind: technique
slug: tabulation-hashing
name: Tabulation hashing
aliases:
- Zobrist-style tabulation
- simple tabulation hashing
area: data-structures/hashing
level: research
summary: Hash by XORing lookup-table entries indexed by each character of the key.
prereqs: [universal-hash-family, hash-function, linear-independence]
see_also: [zobrist-hashing, k-wise-independent-hashing, universal-hashing, linear-probing, cuckoo-hashing, minhash, multiplicative-hashing, ams-sketch]
sources:
  - paper: doi:10.1145/2220357.2220361
    title: Mihai Patrascu and Mikkel Thorup, The power of simple tabulation hashing, Journal of the ACM 59(3), 2012 (conference version at STOC 2011)
    locator: Article 14, pages 14:1 to 14:50; Section 1 (the results on linear probing, Theorem 1 on concentration, Theorem 2 on cuckoo hashing, Theorem 3 on min-wise hashing)
  - paper: "Albert L. Zobrist, A new hashing method with application for game playing, Technical Report 88, Computer Sciences Department, University of Wisconsin, Madison, 1970 (reprinted in ICCA Journal 13(2), 1990, pages 69 to 73)"
    locator: the whole report (random codes for each piece on each square, combined by exclusive or)
  - paper: doi:10.1016/0022-0000(79)90044-8
    title: J. Lawrence Carter and Mark N. Wegman, Universal classes of hash functions, Journal of Computer and System Sciences 18(2), 1979
    locator: pages 143 to 154
  - paper: doi:10.1137/100800774
    title: Mikkel Thorup and Yin Zhang, Tabulation-based 5-independent hashing with applications to linear probing and second moment estimation, SIAM Journal on Computing 41(2), 2012
    locator: pages 293 to 331
  - paper: doi:10.1145/3068772
    title: Mikkel Thorup, Fast and powerful hashing using tabulation, Communications of the ACM 60(7), 2017
    locator: the whole survey (simple, twisted, double and mixed tabulation)
  - paper: doi:10.1137/070702278
    title: Anna Pagh, Rasmus Pagh and Milan Ruzic, Linear probing with constant independence, SIAM Journal on Computing 39(3), 2009
    locator: pages 1107 to 1120
---

Simple tabulation hashing views a key as $c$ characters $x = (x_0, \dots, x_{c-1})$ of $q$ bits each, keeps $c$ tables $T_0, \dots, T_{c-1}$ of $2^q$ random $r$-bit words, and returns $h(x) = T_0[x_0] \oplus T_1[x_1] \oplus \dots \oplus T_{c-1}[x_{c-1}]$, where $\oplus$ is the bitwise exclusive or. It costs $c$ table lookups and $c - 1$ XORs, with no multiplication. The family is 3-wise independent but not 4-wise independent, so it is [strongly universal](/universal-hash-family/). Patrascu and Thorup proved in 2011 that it still gives many guarantees of a fully random function, among them expected constant time for [linear probing](/linear-probing/) and a high success probability for [cuckoo hashing](/cuckoo-hashing/).

## In plain words

Cut the key into a few small pieces, for example a 32-bit number into four bytes. For each piece position, keep a table with one random number for each possible byte value. These tables are filled once, at random, when the program starts.

To hash a key, look up each byte in the table of its position, and combine the four random numbers with exclusive or. Exclusive or is a bit operation that flips the bits of one number where the other number has a one.

Two different keys differ in at least one byte, so at least one of their four random numbers is different, and this makes the results look unrelated. The tables are small, so they stay in the fast memory of the processor, and the hash needs only a few lookups.

## When it applies

- The keys have a fixed length of a few bytes, such as 32-bit or 64-bit integers, or they are first reduced to such a length.
- The analysis needs more than [universality](/universal-hashing/): long runs of keys in linear probing, the random graph of cuckoo hashing, the minimum of many hash values in [MinHash](/minhash/), or concentration of the load of a bucket.
- Multiplication is slow, or a hash of several words would need many multiplications, while a few kilobytes of tables fit in the [cache](/cache/).
- The key changes one character at a time, as a board position changes one square at a time, so the hash can be updated with two XORs. This is [Zobrist hashing](/zobrist-hashing/).

## The template

```pseudo id=main
TABULATION-SETUP(c, q, r)                  ▷ c tables of 2^q entries, each an r-bit word
L1  for i ← 0 to c − 1 do
L2      for α ← 0 to 2^q − 1 do
L3          T_i[α] ← an independent uniform r-bit word    ▷ hole: the source of random bits

TAB-HASH(x)                                ▷ x = (x_0, ..., x_{c−1}), each x_i in {0, ..., 2^q − 1}
L4  v ← 0
L5  for i ← 0 to c − 1 do
L6      v ← v ⊕ T_i[x_i]                    ▷ one lookup in the table of position i
L7  return v                                ▷ an r-bit hash value
```

**The holes.** The parameters are a choice of speed against space. For 32-bit keys, $q = 8$ and $c = 4$ give four tables of 256 entries; with $r = 32$ this is 4 KB. For 64-bit keys, $c = 8$ tables of 256 entries, or $c = 4$ tables of $2^{16}$ entries. Line L3 needs good random bits, from the system source or from a good [pseudorandom generator](/pseudorandom-number-generator/) seeded from it. For a table with $m = 2^\ell \le 2^r$ slots, use $\ell$ bits of $v$; each fixed set of output bits of a simple tabulation function is again a simple tabulation function, with narrower entries.

**What is random.** The key is fixed and the tables are random. Each statement below is over the random choice of the $c \cdot 2^q$ entries, for keys that are fixed in advance.

### A worked example

Take 4-bit keys with $c = 2$ characters of $q = 2$ bits: $x = 4x_1 + x_0$, with the high character $x_1$ and the low character $x_0$. Take $r = 4$ and the tables

| $\alpha$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| $T_1[\alpha]$ | 1010 | 0100 | 1100 | 0001 |
| $T_0[\alpha]$ | 0010 | 0011 | 1011 | 0001 |

The key $6 = 0110$ has $x_1 = 1$ and $x_0 = 2$, so $h(6) = 0100 \oplus 1011 = 1111 = 15$. The 16 keys $0, 1, \dots, 15$ get the values $8, 9, 1, 11, 6, 7, 15, 5, 14, 15, 7, 13, 3, 2, 10, 0$. Look at the four keys 0, 1, 4 and 5, which form a rectangle: two choices of $x_1$ times two choices of $x_0$. Their values are $8, 9, 6, 7$, and $8 \oplus 9 \oplus 6 \oplus 7 = 0$. This is true for every choice of the tables, because each of the entries $T_1[0], T_1[1], T_0[0], T_0[1]$ occurs exactly twice in the four sums. So the value of the fourth key is fixed by the other three.

### Independence: exactly three

Write $N = c \cdot 2^q$ for the number of table entries, and call a pair $(i, \alpha)$ a *position character*. The key $x$ uses the $c$ position characters $(i, x_i)$. Let $v_x \in \mathrm{GF}(2)^N$ be the indicator vector of these $c$ position characters. For a set $K$ of keys, a nonempty subset $K' \subseteq K$ is *dependent* when $\sum_{x \in K'} v_x = 0$ over $\mathrm{GF}(2)$, that is, when each position character is used an even number of times by the keys of $K'$.

**Lemma (Thorup and Zhang).** For distinct keys $x^1, \dots, x^k$, the values $h(x^1), \dots, h(x^k)$ are independent and uniform on $\{0, \dots, 2^r - 1\}$ if and only if the vectors $v_{x^1}, \dots, v_{x^k}$ are [linearly independent](/linear-independence/) over $\mathrm{GF}(2)$.

*Proof.* Fix one output bit $b$ and let $t_b \in \mathrm{GF}(2)^N$ be the vector of bit $b$ of all $N$ entries; it is uniform, and the vectors $t_0, \dots, t_{r-1}$ are independent. Bit $b$ of $h(x)$ is the inner product $\langle v_x, t_b \rangle$ over $\mathrm{GF}(2)$, because XOR adds bits modulo 2. If the $v_{x^j}$ are linearly independent, the linear map $t \mapsto (\langle v_{x^1}, t \rangle, \dots, \langle v_{x^k}, t \rangle)$ from $\mathrm{GF}(2)^N$ to $\mathrm{GF}(2)^k$ has rank $k$, so it is onto, and each point of $\mathrm{GF}(2)^k$ has a preimage of the same size (a coset of the kernel). So bit $b$ of the $k$ values is uniform on $\mathrm{GF}(2)^k$. The $r$ bit positions are independent, so the $k$ values are uniform on $(\{0, \dots, 2^r - 1\})^k$. Conversely, if a nonempty subset $K'$ is dependent, then $\bigoplus_{x \in K'} h(x) = 0$ for every choice of the tables, an event of probability 1 instead of $2^{-r}$, so the values are not independent and uniform. $\square$

**Theorem.** Simple tabulation is 3-wise independent: for distinct keys $x, y, z$ and any values $u, v, w$, $\Pr[h(x) = u \wedge h(y) = v \wedge h(z) = w] = 2^{-3r}$, and the same holds for one or two keys. If $c \ge 2$ and $q \ge 1$, it is not 4-wise independent.

*Proof.* By the lemma, it suffices to show that no nonempty set of at most 3 distinct keys is dependent. Let $K'$ be dependent. At position 0, the $|K'|$ keys use characters whose multiplicities are all even, so $|K'|$ is even. So $|K'| \ne 1$ and $|K'| \ne 3$. If $|K'| = 2$, say $K' = \{x, y\}$, then at each position $i$ the character $x_i$ must be used twice, so $y_i = x_i$ for all $i$, and $x = y$, which is false. So each set of at most 3 distinct keys is independent. For the second claim, take characters $\alpha \ne \alpha'$ and $\beta \ne \beta'$, fix the characters at the positions 2 to $c - 1$, and take the four keys with $(x_0, x_1)$ in $\{\alpha, \alpha'\} \times \{\beta, \beta'\}$. Each of their position characters is used exactly twice, so the four keys are dependent and not independent. $\blacksquare$

For $c = 2$, $q = 2$ and $r = 1$, a check of all $2^8$ tables shows that each set of three keys gets uniform values, and that exactly 36 of the 1820 sets of four keys do not. These 36 sets are the $\binom{4}{2}^2$ rectangles.

### What simple tabulation does give

Patrascu and Thorup proved the following for a set of $n$ keys hashed by simple tabulation with a constant number $c$ of characters (Section 1 of their paper).

- **Linear probing.** In a table of $m = (1 + \varepsilon) n$ slots, the expected time per operation is $O(1/\varepsilon^2)$, the bound that Knuth proved for a fully random function. Low independence alone does not give this: Pagh, Pagh and Ruzic showed that some pairwise independent families give logarithmic expected time.
- **Concentration (Theorem 1).** With $m \ge n^{1 - 1/(2c)}$ bins, the number of keys in a bin has Chernoff-type tail bounds around its mean $n/m$, also for the bin of a query key.
- **Cuckoo hashing (Theorem 2).** Each set of $n$ keys can be placed in two tables of size $(1 + \varepsilon) n$ with probability $1 - O(n^{-1/3})$, and some sets fail with probability $\Omega(n^{-1/3})$. A fully random function fails with probability $\Theta(1/n)$.
- **Min-wise hashing (Theorem 3).** For a set $S$ of $n$ keys and a key $q \notin S$, $\Pr[h(q) < \min h(S)] = (1 \pm \varepsilon)/n$ with $\varepsilon = O(\lg^2 n / n^{1/c})$.

## Classic examples

- **[Zobrist hashing](/zobrist-hashing/).** Zobrist (1970) gave each pair (piece, square) of a board game a random code and hashed a position by the XOR of the codes of its pieces. This is tabulation with one position for each square and one character for each piece. A move from square $s$ to $s'$ updates the hash by $h \oplus T_s[p] \oplus T_{s'}[p]$, in constant time, which makes it the standard key of a chess [transposition table](/transposition-table/).
- **[Linear probing](/linear-probing/).** Simple tabulation gives the expected $O(1/\varepsilon^2)$ time of a random function, at the cost of a few lookups in small tables.
- **[Cuckoo hashing](/cuckoo-hashing/).** Two tabulation functions give a failure probability of $O(n^{-1/3})$, enough for a construction that rebuilds on failure.
- **[MinHash](/minhash/).** The min-wise bound above makes tabulation a fast choice for the estimate of the Jaccard similarity of two sets.
- **Chaining.** As a strongly universal family, it gives the bounds of [separate chaining](/separate-chaining/), and the concentration bound also limits the longest chain.

## Variations

- **Bitwise tabulation.** With $q = 1$, the key is a bit vector and $h(x)$ is the XOR of the entries for its bits. Up to the constant $\bigoplus_i T_i[0]$, this is a linear map over $\mathrm{GF}(2)$ given by a random matrix. Patrascu and Thorup trace tabulation back to Carter and Wegman (1977).
- **Twisted tabulation.** Patrascu and Thorup (2013) change one character of the key by a value from a table before the last lookup, which gives stronger concentration bounds with the same number of lookups and wider entries.
- **Double tabulation.** Thorup (2013) applies simple tabulation twice, the second time to the output of the first, and gets high independence, of order a power of the table size, with high probability.
- **5-independent tabulation.** Thorup and Zhang (2012) add lookups of derived characters to reach 5-wise independence with no multiplications. This is what the classic analyses of linear probing and of second-moment estimation in the [AMS sketch](/ams-sketch/) ask for.
- **Mixed tabulation.** Dahlgaard, Knudsen, Rotenberg and Thorup (2015) add derived characters to simple tabulation to get guarantees for statistics over $k$ partitions, such as one-permutation hashing. The survey of Thorup (2017) compares these schemes.

## Pitfalls

- **One table for all positions.** If line L6 uses the same table $T$ for each position, then $h(x)$ does not depend on the order of the characters: the keys $(\alpha, \beta)$ and $(\beta, \alpha)$ collide for every $T$. Use a separate table $T_i$ for each position $i$.
- **Assuming 4-wise independence.** An analysis that needs the fourth moment, such as the variance of the AMS estimate of the second frequency moment, does not hold as stated for simple tabulation, because rectangles of four keys are dependent. Use the 5-independent tabulation of Thorup and Zhang, or a polynomial of degree 3 or more modulo a prime.
- **Variable-length keys.** Padding a short string with zero characters makes "ab" and "ab" followed by a zero character the same key. Hash the length too, or reduce strings to a fixed length with a string hash first.
- **Weak random entries.** The proofs need independent uniform entries. A low-quality generator, or a seed that an attacker can guess, removes the guarantees. Fill the tables from a good source at start-up.
- **Tables that do not fit in cache.** With $q = 16$ and $c = 4$, the tables have $2^{18}$ entries, and each lookup can be a cache miss. Then tabulation can be slower than [multiplicative hashing](/multiplicative-hashing/). Measure on the target machine.
- **Too few characters for concentration.** The concentration bound needs $m \ge n^{1 - 1/(2c)}$ bins. With few bins and many keys this condition fails.

## Exercises

1. Show that for $c = 1$, simple tabulation is a fully random function on the $2^q$ keys.
2. Show that a set of keys is dependent only if its size is even, and give a dependent set of six keys for $c = 2$ and $q = 2$ that contains no dependent set of four keys.
3. Prove that simple tabulation is strongly universal directly, without the lemma: for $x \ne y$, choose a position where they differ and condition on all other entries.
4. In Zobrist hashing of chess positions, write the update of the hash for a capture, where a piece $p$ moves from $s$ to $s'$ and removes a piece $p'$ from $s'$.
5. For 64-bit keys, compare the space and the number of lookups of $c = 8, q = 8$ and of $c = 4, q = 16$, with 64-bit entries.

## References
