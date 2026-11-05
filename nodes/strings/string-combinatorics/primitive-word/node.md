---
tag: RGZ821
kind: definition
slug: primitive-word
name: Primitive word
aliases:
- aperiodic word
- unbordered-root word
area: strings/string-combinatorics
level: intro
summary: A word that is not a proper power of another word.
prereqs: [string-period, word-conjugacy]
see_also: [primitive-root-of-a-word, lyndon-word, necklace, witt-formula, lyndon-schutzenberger-theorem, fine-and-wilf-theorem, mobius-inversion, square]
sources:
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 1, Words (D. Perrin), the section on conjugacy (primitive words, the uniqueness of the primitive root, and the number of primitive words)
  - book: isbn:9780521865722
    title: Jeffrey Shallit, A Second Course in Formal Languages and Automata Theory, Cambridge University Press, 2009
    locator: Chapter 2, Combinatorics on words (primitive words, the theorems of Lyndon and Schutzenberger, and the count of primitive words)
  - book: isbn:9780521823326
    title: Jean-Paul Allouche and Jeffrey Shallit, Automatic Sequences, Cambridge University Press, 2003
    locator: Chapter 1, Stringology (powers and primitive words)
---

A primitive word is a nonempty word that is not a power $u^k$ of another word with $k \ge 2$. Each nonempty word is a power of exactly one primitive word, its [primitive root](/primitive-root-of-a-word/), and a word is primitive if and only if it differs from all its other rotations. Over $k$ letters there are $\sum_{d \mid n} \mu(d)\, k^{n/d}$ primitive words of length $n$, and dividing this number by $n$ gives the count of [Lyndon words](/lyndon-word/), the [Witt formula](/witt-formula/).

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/) with $k = |\Sigma|$ letters; only equality of letters is used. Indices are 0-based.

**Primitive word.** A word $w \in \Sigma^+$ is *primitive* if $w = u^m$ with $u \in \Sigma^*$ and $m \ge 1$ implies $m = 1$. A nonempty word that is not primitive is a *proper power*, or *imprimitive*. The empty word is not primitive by convention, because $\varepsilon = \varepsilon^m$ for every $m$.

**In terms of periods.** For $w$ of length $n \ge 1$, the word is a proper power if and only if it has a [period](/string-period/) $p < n$ that divides $n$: if $w = u^m$ with $m \ge 2$, then $|u| = n/m$ is such a period, and conversely a period $p$ with $p \mid n$ gives $w = (w[0..p-1])^{n/p}$.

**Facts.** Let $w$ be a nonempty word of length $n$.

1. **Unique root.** There is exactly one primitive word $\rho$ with $w = \rho^m$ for some $m \ge 1$.
2. **Rotation test.** $w$ is primitive if and only if $w$ occurs in $ww$ only at the positions $0$ and $n$.
3. **Conjugates.** All conjugates of a primitive word are primitive, and a primitive word of length $n$ has exactly $n$ distinct conjugates.
4. **The count.** The number of primitive words of length $n$ over $k$ letters is
$$ \psi_k(n) = \sum_{d \mid n} \mu(d)\, k^{n/d}, $$
where $\mu$ is the [Möbius function](/mobius-function/).

*Proof of 1.* Existence: let $\rho$ be a shortest word with $w = \rho^m$ for some $m$. If $\rho = v^j$ with $j \ge 2$, then $w = v^{jm}$ with $|v| < |\rho|$, a contradiction, so $\rho$ is primitive. Uniqueness: let $w = u^a = v^b$ with $u$ and $v$ primitive and $|u| \le |v|$. If $b = 1$, then $v = w = u^a$, and $v$ primitive gives $a = 1$ and $u = v$. If $b \ge 2$, then also $a \ge 2$, so $|u| + |v| \le n/2 + n/2 = n$. Both $|u|$ and $|v|$ are periods of $w$, so by the [Fine and Wilf theorem](/fine-and-wilf-theorem/) $g = \gcd(|u|, |v|)$ is a period, and $g$ divides $n$. Then $u = (w[0..g-1])^{|u|/g}$, and $u$ primitive gives $|u| = g$. In the same way $|v| = g$, so $u = w[0..g-1] = v$. $\square$

*Proof of 2.* The factor of $ww$ of length $n$ at position $i$, for $0 \le i \le n$, is the rotation $\mathrm{rot}_{i \bmod n}(w)$. On the [conjugacy](/word-conjugacy/) page it is shown that the number of distinct rotations of $w$ is the length $d$ of its primitive root, and that $\mathrm{rot}_i(w) = w$ exactly when $d$ divides $i$. So $w$ occurs at some position $0 < i < n$ if and only if $d < n$, that is, if and only if $w$ is a proper power. $\square$

*Proof of 3.* If $w = \rho^m$, then $\mathrm{rot}_i(w) = (\mathrm{rot}_{i \bmod |\rho|}(\rho))^m$. So a conjugate of a proper power is a proper power, and since conjugacy is symmetric, a conjugate of a primitive word is primitive. The count $n$ is the class size $d = n$. $\square$

*Proof of 4.* By fact 1, each word of length $n$ is $\rho^{n/d}$ for exactly one primitive $\rho$ of a length $d$ that divides $n$, and each such $\rho$ gives one word. So $k^n = \sum_{d \mid n} \psi_k(d)$ for all $n \ge 1$. [Möbius inversion](/mobius-inversion/) of this identity gives the formula. $\square$

**Almost all words are primitive.** A proper power of length $n$ is determined by its root of some length $d \le n/2$, so there are at most $\sum_{d=1}^{\lfloor n/2 \rfloor} k^d < 2k^{\lfloor n/2 \rfloor}$ of them for $k \ge 2$. So $\psi_k(n) = k^n - O(k^{n/2})$, and the fraction of primitive words tends to 1.

## Examples and non-examples

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\psi_2(n)$ | 2 | 2 | 6 | 12 | 30 | 54 | 126 | 240 | 504 | 990 | 2046 | 4020 |
| $\psi_3(n)$ | 3 | 6 | 24 | 72 | 240 | 696 | 2184 | 6480 | 19656 | 58800 | 177144 | 530640 |

For example $\psi_2(6) = 2^6 - 2^3 - 2^2 + 2^1 = 54$: the $64$ binary words of length 6 minus the $10$ proper powers `aaaaaa`, `bbbbbb`, `ababab`, `bababa`, and the six squares $uu$ with $u \in \{$`aab`, `aba`, `baa`, `abb`, `bab`, `bba`$\}$.

- **Primitive:** `a`, `ab`, `aab`, `aabb`, `abaab`, `aba`. The word `aba` has the period 2, but 2 does not divide 3, so `aba` is not a power.
- **Not primitive:** `aa` $= a^2$, `abab` $= (ab)^2$, `abcabc` $= (abc)^2$, `abaaba` $= (aba)^2$. Each occurs in its own square at a middle position: `abab` occurs in `abababab` at position 2.
- **Not primitive by convention:** the empty word.
- **Primitive is not the same as unbordered.** `aba` is primitive and has the border `a`. An unbordered word is always primitive, because a power $u^m$ with $m \ge 2$ has the border $u^{m-1}$.
- **Square-free words are primitive.** A proper power $u^m$ with $m \ge 2$ starts with the [square](/square/) $uu$, so a square-free word is primitive. The converse fails: `aab` is primitive and has the square factor `aa`.

## Related definitions

- **Primitive root and exponent.** The word $\rho$ of fact 1 and the integer $m$; computing them is the problem [primitive root of a word](/primitive-root-of-a-word/).
- **Lyndon word.** A primitive word that is the least of its $n$ conjugates; see [Lyndon word](/lyndon-word/) and the [Witt formula](/witt-formula/) $\psi_k(n)/n$.
- **Necklace.** A class of conjugate words; the primitive classes are the aperiodic [necklaces](/necklace/).
- **Commuting words.** $uv = vu$ if and only if $u$ and $v$ are powers of the same word; see the [Lyndon-Schützenberger theorem](/lyndon-schutzenberger-theorem/).
- **Period.** The [period](/string-period/) of a primitive word need not equal its length; it does exactly when the word is unbordered.
- **Primitively rooted square.** A [square](/square/) $uu$ with $u$ primitive; these are the squares counted in the analysis of repetitions.

## References
