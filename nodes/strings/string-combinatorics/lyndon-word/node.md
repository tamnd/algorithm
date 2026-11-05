---
tag: G2TDTG
kind: definition
slug: lyndon-word
name: Lyndon word
aliases:
- Lyndon sequence
- Lyndon string
area: strings/string-combinatorics
level: intro
summary: A word strictly smaller in lexicographic order than all of its proper rotations.
prereqs: [primitive-word, lexicographic-order, border]
see_also: [lyndon-factorization, duval-algorithm, necklace, minimal-rotation, fkm-algorithm, witt-formula, lyndon-array, christoffel-word]
sources:
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 5, Factorizations of free monoids, Section 5.1 (Lyndon words, their characterizations, the standard factorization and the count)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.2.1.1, Generating all n-tuples (prime strings, which are Lyndon words, and Algorithm F)
  - paper: doi:10.2307/1970044
    title: Kuo-Tsai Chen, Ralph H. Fox and Roger C. Lyndon, Free differential calculus IV. The quotient groups of the lower central series, Annals of Mathematics 68(1), 1958, 81-95
    locator: the definition of standard sequences and the unique factorization of words
  - paper: doi:10.1016/0196-6774(83)90017-2
    title: Jean-Pierre Duval, Factorizing words over an ordered alphabet, Journal of Algorithms 4(4), 1983, 363-381
    locator: the characterization of Lyndon words by their suffixes and the definition of prefixes of Lyndon words (preprime words)
---

A Lyndon word is a nonempty word over an ordered [alphabet](/alphabet/) that is strictly smaller, in [lexicographic order](/lexicographic-order/), than each of its proper rotations. Equivalently, it is a [primitive word](/primitive-word/) that is the least element of its conjugacy class, so each class of rotations of a primitive word has exactly one Lyndon word, which makes Lyndon words the canonical names of aperiodic [necklaces](/necklace/). Each word factors uniquely as a nonincreasing product of Lyndon words, the [Lyndon factorization](/lyndon-factorization/), which [Duval's algorithm](/duval-algorithm/) computes in linear time.

## Definition

Let $\Sigma$ be an alphabet with a total order $<$, extended to $\Sigma^*$ by the lexicographic order: $u < v$ if $u$ is a proper prefix of $v$, or $u = xay$ and $v = xbz$ with letters $a < b$. Indices are 0-based. For $w = w[0..n-1]$ and $0 \le i < n$, the rotation (conjugate) of $w$ by $i$ is $w[i..n-1]\,w[0..i-1]$; it is proper when $i \ne 0$.

**Lyndon word.** A word $w \in \Sigma^+$ is a Lyndon word if
$$ w < w[i..n-1]\,w[0..i-1] \qquad \text{for each } 1 \le i \le n - 1. $$

Each letter is a Lyndon word, since it has no proper rotation. The strict inequality is the point: a word equal to one of its proper rotations is a power $z^k$ with $k \ge 2$, so a Lyndon word is primitive. Knuth calls Lyndon words prime strings.

### Characterizations

For $w \in \Sigma^+$ with $|w| = n$, these statements are equivalent.

1. $w$ is a Lyndon word.
2. $w$ is primitive and $w = \min$ of its $n$ rotations.
3. $w < v$ for each proper nonempty suffix $v$ of $w$.
4. $|w| = 1$, or $w = uv$ with $u$ and $v$ Lyndon words and $u < v$.

*Proof that a Lyndon word is unbordered.* Suppose $w = xy = zx$ with $x \ne \varepsilon$ and $|x| < n$, so $|y| = |z| \ge 1$. The rotation $xz$ of $w = zx$ is proper, so $xy < xz$, which gives $y < z$. The rotation $yx$ of $w = xy$ is proper, so $zx < yx$; as $|z| = |y|$, this gives $z < y$. Both cannot hold. $\square$

*1 ⇔ 2.* If $w$ is Lyndon, its rotations are all different from $w$, so $w$ is primitive, and $w$ is the minimum. If $w$ is primitive, its $n$ rotations are pairwise different, so a minimum is strictly below all the others. $\square$

*1 ⇒ 3.* Let $w = uv$ with $u, v \ne \varepsilon$. If $v$ were a prefix of $w$, it would be a nonempty border, which the lemma excludes. So $w$ and $v$ differ at an index $j < |v|$. The rotation $vu$ starts with $v$, so $w$ and $vu$ also first differ at $j$, and $w < vu$ gives $w[j] < v[j]$, so $w < v$. $\square$

*3 ⇒ 1.* Let $w = uv$ with $u, v \ne \varepsilon$. Since $w < v$ and $v$ is shorter, $v$ is not a prefix of $w$ (a proper prefix is smaller). So $w$ and $v$ first differ at an index $j < |v|$ with $w[j] < v[j]$, and the same index shows $w < vu$. $\square$

*4 ⇒ 3 (the product of two Lyndon words).* Let $u < v$ be Lyndon words. First, $uv < v$: if $u$ is not a prefix of $v$, they first differ at an index $j < |u|$ with $u[j] < v[j]$; if $v = ut$ with $t \ne \varepsilon$, then $v < t$ by 3 for $v$, so $uv = u\,ut < u\,t = v$. Now take a proper suffix $s$ of $uv$. If $s$ is a proper suffix of $v$, then $uv < v < s$. If $s = v$, we just proved $uv < v$. If $s = u'v$ with $u'$ a proper nonempty suffix of $u$, then $u < u'$ and $u'$ is not a prefix of $u$ (no border), so they first differ at $j < |u'|$ with $u[j] < u'[j]$, and $uv < u'v$. $\square$

*1 ⇒ 4 (the standard factorization).* Let $|w| \ge 2$ and let $v$ be the smallest proper nonempty suffix of $w$, and $w = uv$. Each proper suffix of $v$ is a proper suffix of $w$, longer or shorter but different from $v$, so it is larger than $v$: $v$ is Lyndon by 3. Suppose a proper nonempty suffix $u'$ of $u$ has $u' \le u$. By 3 for $w$, $uv < u'v$. If $u'$ were not a prefix of $u$, then $u' < u$ would give $u'v < uv$; so $u = u't$ with $t \ne \varepsilon$. Then $u'tv < u'v$ gives $tv < v$, but $tv$ is a proper suffix of $w$, against the choice of $v$. So $u$ is Lyndon, and $u < w < v$ because $u$ is a proper prefix of $w$. $\square$

### Counting

Let $L_\sigma(n)$ be the number of Lyndon words of length $n$ over $\sigma$ letters. Then
$$ L_\sigma(n) = \frac{1}{n} \sum_{d \mid n} \mu(d)\, \sigma^{n/d}, $$
where $\mu$ is the [Möbius function](/mobius-function/). *Proof.* Each word of length $n$ is $z^{n/d}$ for a unique primitive $z$ of length $d \mid n$ (its [primitive root](/primitive-root-of-a-word/)), so $\sigma^n = \sum_{d \mid n} P(d)$, where $P(d)$ is the number of primitive words of length $d$. [Möbius inversion](/mobius-inversion/) gives $P(n) = \sum_{d \mid n} \mu(d) \sigma^{n/d}$. A primitive word of length $n$ has $n$ distinct rotations, all primitive, and by 2 exactly one of them is Lyndon. $\square$ This is [Witt's formula](/witt-formula/), and it also counts the aperiodic necklaces.

## Examples and non-examples

**Examples over $a < b$.**

- Length 1 to 5: `a`, `b`; `ab`; `aab`, `abb`; `aaab`, `aabb`, `abbb`; `aaaab`, `aaabb`, `aabab`, `aabbb`, `ababb`, `abbbb`.
- The counts $L_2(n)$ for $n = 1$ to $10$ are 2, 1, 2, 3, 6, 9, 18, 30, 56, 99. Over three letters, $L_3(n)$ for $n = 1$ to $7$ is 3, 3, 8, 18, 48, 116, 312.
- `aabab` is Lyndon. Its proper suffixes `abab`, `bab`, `ab`, `b` are all larger than it. Its smallest proper suffix is `ab`, so its standard factorization is `aab` $\cdot$ `ab`, with `aab` $<$ `ab`.
- Over $\{0, 1, 2\}$, `0102` and `012` are Lyndon. A [Christoffel word](/christoffel-word/) such as `aabab` is always Lyndon.

**Non-examples.**

- $\varepsilon$: the definition asks for a nonempty word.
- `ba`: the rotation `ab` is smaller. Its Lyndon conjugate is `ab`.
- `aba`: the rotation `aab` is smaller, and `a` is a border. The suffix `a` is smaller than `aba`.
- `abab`: it equals its rotation by 2, so it is not primitive. It is the least of its rotations, so it is a necklace but not a Lyndon word.
- `aabaab` $= ($`aab`$)^2$: a power of a Lyndon word, again a necklace and not Lyndon.
- Whether a word is Lyndon depends on the order: `ba` is Lyndon for the order $b < a$.

## Related definitions

- **[Necklace](/necklace/).** A word that is the least of its rotations, without the primitivity condition. The necklaces are exactly the powers $\ell^k$ of Lyndon words $\ell$.
- **Prenecklace (preprime word).** A prefix of some necklace. Each prenecklace is $\ell^k p$ with $\ell$ Lyndon, $k \ge 1$ and $p$ a proper prefix of $\ell$, the form that [Duval's algorithm](/duval-algorithm/) and the [FKM algorithm](/fkm-algorithm/) maintain.
- **[Lyndon factorization](/lyndon-factorization/).** Each word is uniquely $\ell_1 \ell_2 \cdots \ell_k$ with Lyndon words $\ell_1 \ge \ell_2 \ge \cdots \ge \ell_k$, by the [Chen-Fox-Lyndon theorem](/lyndon-schutzenberger-theorem/).
- **[Minimal rotation](/minimal-rotation/).** The least rotation of a word; for a primitive word it is its Lyndon conjugate. [Booth's algorithm](/booth-algorithm/) finds it in linear time.
- **[Lyndon array](/lyndon-array/).** For each position, the length of the longest Lyndon word that starts there.
- **[Witt's formula](/witt-formula/).** The count above, which is also the dimension of the homogeneous parts of the free Lie algebra.

## References
