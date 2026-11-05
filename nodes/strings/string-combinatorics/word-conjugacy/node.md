---
tag: S1ZH38
kind: definition
slug: word-conjugacy
name: Conjugacy of words
aliases:
- rotation equivalence
- cyclic shift
area: strings/string-combinatorics
level: intro
summary: Two words are conjugate if one is a rotation of the other, i.e. uv and vu.
prereqs: [alphabet, equivalence-relation]
see_also: [necklace, primitive-word, primitive-root-of-a-word, word-conjugacy-testing, minimal-rotation, lyndon-word, circular-pattern-matching, burrows-wheeler-transform]
sources:
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 1, Words (D. Perrin), the section on conjugacy (conjugate words, the equation uz = zv, and the classes of conjugate words)
  - book: isbn:9780521865722
    title: Jeffrey Shallit, A Second Course in Formal Languages and Automata Theory, Cambridge University Press, 2009
    locator: Chapter 2, Combinatorics on words (conjugates and the commutation of words)
  - book: isbn:9780521823326
    title: Jean-Paul Allouche and Jeffrey Shallit, Automatic Sequences, Cambridge University Press, 2003
    locator: Chapter 1, Stringology (conjugates, powers and primitive words)
---

Two words $u$ and $v$ are conjugate when one is a rotation of the other: $u = xy$ and $v = yx$ for some words $x$ and $y$. Conjugacy is an [equivalence relation](/equivalence-relation/) on the words of each length, and its classes are the [necklaces](/necklace/). The class of a word of length $n$ has exactly $d$ elements, where $d$ is the length of its [primitive root](/primitive-root-of-a-word/), so a [primitive word](/primitive-word/) has $n$ distinct conjugates.

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/); only equality of letters is used, so no order is needed. Indices are 0-based, and $u[i..j]$ includes both ends.

**Conjugate words.** Words $u, v \in \Sigma^*$ are *conjugate*, written $u \sim v$, if there are words $x, y \in \Sigma^*$ with
$$ u = xy \quad \text{and} \quad v = yx. $$
Conjugate words have the same length. The choice $x = \varepsilon$ shows $u \sim u$.

**Rotations.** For $u$ of length $n \ge 1$ and $0 \le i \le n - 1$, the *rotation* (or *cyclic shift*) of $u$ by $i$ is
$$ \mathrm{rot}_i(u) = u[i..n-1]\,u[0..i-1], \qquad \mathrm{rot}_i(u)[t] = u[(t + i) \bmod n]. $$
With $x = u[0..i-1]$ and $y = u[i..n-1]$, the conjugates of $u$ are exactly its $n$ rotations $\mathrm{rot}_0(u), \ldots, \mathrm{rot}_{n-1}(u)$, some of which may be equal.

**Conjugacy is an equivalence relation.** Reflexivity was shown above, and symmetry is clear from the definition (swap the roles of $x$ and $y$). For transitivity, the formula for the letters gives $\mathrm{rot}_j(\mathrm{rot}_i(u))[t] = u[(t + i + j) \bmod n]$, so $\mathrm{rot}_j \circ \mathrm{rot}_i = \mathrm{rot}_{(i + j) \bmod n}$. A rotation of a rotation of $u$ is therefore a rotation of $u$.

**The equation $uz = zv$.** Two words $u$ and $v$ are conjugate if and only if $uz = zv$ for some word $z$.

*Proof.* If $u = xy$ and $v = yx$, take $z = x$: then $uz = xyx = zv$. Conversely, let $uz = zv$, and use induction on $|z|$. If $u = \varepsilon$, then $|v| = 0$ and $u = v$. Otherwise, if $|z| < |u|$, then $z$ is a prefix of $uz$ of length less than $|u|$, so $u = zy$ for a word $y$; then $zyz = zv$ gives $v = yz$, and $u = zy \sim yz = v$. If $|z| \ge |u|$, then $u$ is a prefix of $zv = uz$ of length at most $|z|$, so $z = uz'$; then $uuz' = uz'v$ gives $uz' = z'v$ with $|z'| = |z| - |u| < |z|$, and the induction hypothesis applies. $\square$

**The size of a class.** Let $u$ have length $n \ge 1$ and let $\rho$ be its primitive root, so $u = \rho^{n/d}$ with $d = |\rho|$. Then $u$ has exactly $d$ distinct conjugates, and $\mathrm{rot}_i(u) = \mathrm{rot}_j(u)$ if and only if $i \equiv j \pmod d$.

*Proof.* Let $S = \{ i \in \{0, \ldots, n-1\} : \mathrm{rot}_i(u) = u \}$. By the composition rule, $S$ is a subgroup of the [cyclic group](/cyclic-group/) $\mathbb{Z}_n$, so $S$ is the set of multiples of the smallest positive $e \in S \cup \{n\}$, and $e$ divides $n$. The rule $u[t] = u[(t + e) \bmod n]$ for all $t$ gives $u = (u[0..e-1])^{n/e}$, so $d \le e$. Conversely, $u = \rho^{n/d}$ gives $\mathrm{rot}_d(u) = u$, so $e \le d$. So $e = d$. Finally $\mathrm{rot}_i(u) = \mathrm{rot}_j(u)$ if and only if $\mathrm{rot}_{(i - j) \bmod n}(u) = u$, that is, $i - j \in S$, so the number of distinct rotations is $n / |S| = n / (n/d) = d$. $\square$

## Examples and non-examples

| $u$ | its rotations $\mathrm{rot}_0, \ldots, \mathrm{rot}_{n-1}$ | distinct | primitive root |
| --- | --- | --- | --- |
| `abc` | abc, bca, cab | 3 | `abc` |
| `abaab` | abaab, baaba, aabab, ababa, babaa | 5 | `abaab` |
| `aabb` | aabb, abba, bbaa, baab | 4 | `aabb` |
| `abab` | abab, baba, abab, baba | 2 | `ab` |
| `abcabc` | abcabc, bcabca, cabcab, abcabc, bcabca, cabcab | 3 | `abc` |
| `aaaa` | aaaa (four times) | 1 | `a` |

- **A conjugate pair.** `abaab` $\sim$ `ababa`: take $x = $ `aba` and $y = $ `ab`, so $xy = $ `abaab` and $yx = $ `ababa`. With $z = x = $ `aba`, the equation $uz = zv$ reads `abaab` `aba` $=$ `aba` `ababa` $=$ `abaababa`.
- **Same letters, not conjugate.** `aabb` and `abab` have the same letters, each twice, but `abab` is not among the four rotations of `aabb`. Conjugate words have the same [Parikh vector](/parikh-vector/), and this example shows that the converse is false.
- **Not conjugate: a different order around the circle.** `abc` and `acb` have the same letters, but the rotations of `abc` are `abc`, `bca`, `cab`.
- **Reversal is not rotation.** `aab` and its reversal `baa` are conjugate, but `aabab` and its reversal `babaa` are also conjugate, while `abcd` and `dcba` are not. Classes under rotation and reversal together are [bracelets](/bracelet/).

## Related definitions

- **Necklace.** A conjugacy class, or its least element under a [lexicographic order](/lexicographic-order/); see [necklace](/necklace/).
- **Lyndon word.** A primitive word that is strictly smaller than all its other conjugates; see [Lyndon word](/lyndon-word/).
- **Primitive word and root.** The size of a class is the length of the [primitive root](/primitive-root-of-a-word/); a [primitive word](/primitive-word/) of length $n$ has $n$ conjugates.
- **Least rotation.** The [minimal rotation](/minimal-rotation/) problem asks for the least element of a class; it is a canonical name of a circular string.
- **Testing conjugacy.** [Conjugacy testing](/word-conjugacy-testing/) decides $u \sim v$ in linear time, as an occurrence of $v$ in $uu$.
- **The Burrows-Wheeler transform.** The [Burrows-Wheeler transform](/burrows-wheeler-transform/) sorts the $n$ rotations of a word, and two conjugate words have the same transform.
- **Conjugacy in groups.** In a free group, $g$ and $h$ are conjugate if $h = x^{-1} g x$. For cyclically reduced words, this is conjugacy of words in the sense of this page.

## References
