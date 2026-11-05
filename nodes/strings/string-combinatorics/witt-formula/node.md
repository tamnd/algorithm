---
tag: J4GBHE
kind: theorem
slug: witt-formula
name: Witt formula
aliases:
- necklace polynomial formula
- Lyndon word counting formula
area: strings/string-combinatorics
level: advanced
summary: Counts Lyndon words of length n over k letters via Möbius inversion.
prereqs: [lyndon-word, mobius-inversion-formula]
see_also: [primitive-word, necklace, necklace-counting, lyndon-factorization, fkm-algorithm, de-bruijn-sequence, irreducible-polynomial, fermat-little-theorem]
sources:
  - paper: "Ernst Witt, Treue Darstellung Liescher Ringe, Journal für die reine und angewandte Mathematik 177, 1937, 152-160"
    locator: the formula for the dimension of the homogeneous components of a free Lie algebra
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 5, Lyndon words (D. Perrin), the factorization theorem and the enumeration of Lyndon words, and Chapter 1, primitive words and conjugacy
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1, Generating all n-tuples (prime strings, their number and the necklace count)
  - paper: "Kuo-Tsai Chen, Ralph H. Fox and Roger C. Lyndon, Free differential calculus IV. The quotient groups of the lower central series, Annals of Mathematics 68(1), 1958, 81-95"
    locator: the unique factorization of every word into a nonincreasing product of standard (Lyndon) words
---

The Witt formula counts the [Lyndon words](/lyndon-word/) of length $n$ over an ordered alphabet of $k$ letters: there are $L_k(n) = \frac{1}{n} \sum_{d \mid n} \mu(d)\,k^{n/d}$ of them, where $\mu$ is the Möbius function. It follows from two facts: every word is a power of a unique [primitive word](/primitive-word/), and every primitive word of length $d$ has exactly $d$ rotations, one of which is a Lyndon word. The same number is the dimension of the degree-$n$ part of the free Lie algebra on $k$ generators, as Witt showed in 1937, and the number of monic irreducible polynomials of degree $n$ over a field with $k$ elements when $k$ is a prime power.

## Statement

Let $\Sigma$ be an alphabet of $k \ge 1$ letters with a total order; words are indexed from 0. For a word $w$ of length $n$ and $0 \le i < n$, the rotation $\mathrm{rot}_i(w) = w[i..n-1]\,w[0..i-1]$. A nonempty word is *primitive* if it is not $u^e$ for any word $u$ and $e \ge 2$, and it is a *Lyndon word* if it is strictly smaller in [lexicographic order](/lexicographic-order/) than each of its proper rotations $\mathrm{rot}_i(w)$, $0 < i < n$. Let $P_k(n)$ and $L_k(n)$ be the numbers of primitive words and of Lyndon words of length $n$, and $\mu$ the [Möbius function](/mobius-function/).

**Theorem (Witt formula).** For all $k \ge 1$ and $n \ge 1$,
$$ k^n = \sum_{d \mid n} d\,L_k(d), \qquad P_k(n) = n\,L_k(n) = \sum_{d \mid n} \mu(d)\,k^{n/d}, \qquad L_k(n) = \frac{1}{n} \sum_{d \mid n} \mu(d)\,k^{n/d}. $$
Moreover the number of [necklaces](/necklace/) of length $n$, the classes of words under rotation, is
$$ N_k(n) = \sum_{d \mid n} L_k(d) = \frac{1}{n} \sum_{d \mid n} \varphi(d)\,k^{n/d}, $$
with $\varphi$ the [Euler totient](/euler-totient/).

## In plain words

Take all strings of a fixed length over a few letters and arrange each one on a ring. Some rings look the same after a turn because the string is a smaller block repeated; the others look different after every turn, and among their turned versions exactly one comes first in dictionary order. Those first ones are the Lyndon words. So to count them, count the strings that are not repetitions of a smaller block and divide by the length, since each ring of such a string contains that many different strings. The strings that are repetitions are counted with the help of shorter lengths, and an alternating sum over the divisors of the length removes them exactly. The same count appears in algebra, for irreducible polynomials over finite fields and for free Lie algebras.

## Proof

**Step 1: unique primitive roots.** Every nonempty word $w$ is $u^{n/d}$ for exactly one primitive word $u$, of length $d \mid n$. *Existence:* let $d$ be the least length of a word $u$ with $w = u^{n/|u|}$; if $u = v^e$ with $e \ge 2$ then $w$ is a power of the shorter $v$, so $u$ is primitive. *Uniqueness:* let $w = u^a = v^b$ with $u, v$ primitive. If $a = 1$ then $w = u$ is primitive, so $b = 1$ and $u = v$; likewise if $b = 1$. Otherwise $n \ge 2\max(|u|, |v|) \ge |u| + |v|$, so $w$ has periods $|u|$ and $|v|$ and length at least $|u| + |v| - \gcd(|u|, |v|)$, and by the [Fine-Wilf theorem](/fine-and-wilf-theorem/) it has period $g = \gcd(|u|, |v|)$, which divides $|u|$, so $u$ is a power of its prefix of length $g$ and primitivity gives $|u| = g$; likewise $|v| = g$, and $u = v$ as both are prefixes of $w$. Counting the words of length $n$ by the length of their root gives
$$ k^n = \sum_{d \mid n} P_k(d). \tag{1} $$

**Step 2: a primitive word has $d$ distinct rotations.** Let $u$ have length $d$. The set $S = \{ i \in \mathbb{Z}_d : \mathrm{rot}_i(u) = u \}$ is a subgroup of $\mathbb{Z}_d$, because $\mathrm{rot}_i \circ \mathrm{rot}_j = \mathrm{rot}_{i+j \bmod d}$. So $S$ is generated by some $g \mid d$, and $u[t] = u[t + g \bmod d]$ for all $t$, that is, $u = (u[0..g-1])^{d/g}$. If $u$ is primitive then $g = d$ and $S = \{0\}$. Then $\mathrm{rot}_i(u) = \mathrm{rot}_j(u)$ implies $\mathrm{rot}_{i-j}(u) = u$, so $i = j$, and the $d$ rotations are distinct. Every rotation of a primitive word is primitive, since $\mathrm{rot}_i(u) = v^e$ would give $u = \mathrm{rot}_{d-i}(v^e) = (\mathrm{rot}_{(d-i) \bmod |v|}(v))^e$.

**Step 3: each class of primitive words contains one Lyndon word.** The rotations of a primitive word $u$ of length $d$ form a class of $d$ distinct primitive words, closed under rotation. Its least element $\ell$ is strictly smaller than its $d - 1$ proper rotations, which are the other elements of the class, so $\ell$ is a Lyndon word; any other element $\mathrm{rot}_i(\ell)$ has the smaller rotation $\ell$ and is not. Conversely, a Lyndon word $w$ is primitive, since $w = v^e$ with $e \ge 2$ gives $\mathrm{rot}_{|v|}(w) = w$, which is not strictly larger than $w$. So the primitive words of length $d$ split into $L_k(d)$ classes of $d$ words each, and
$$ P_k(d) = d\,L_k(d). \tag{2} $$

**Step 4: Möbius inversion.** Combining (1) and (2), $k^n = \sum_{d \mid n} d\,L_k(d)$. The [Möbius inversion formula](/mobius-inversion-formula/) states that $f(n) = \sum_{d \mid n} g(d)$ for all $n \ge 1$ if and only if $g(n) = \sum_{d \mid n} \mu(d)\,f(n/d)$ for all $n \ge 1$. With $f(n) = k^n$ and $g(n) = n\,L_k(n) = P_k(n)$ this gives $n\,L_k(n) = \sum_{d \mid n} \mu(d)\,k^{n/d}$.

**Step 5: necklaces.** A class of words of length $n$ under rotation is the class of $u^{n/d}$ for a primitive $u$ of length $d \mid n$, and two such powers are rotations of each other exactly when their roots are, by Step 1 applied to the rotated word. Each class of primitive words of length $d$ holds one Lyndon word by Step 3, so $N_k(n) = \sum_{d \mid n} L_k(d)$. Substituting the formula for $L_k(d)$, writing $d = e m$ and using $\sum_{e \mid N} \mu(e)/e = \varphi(N)/N$,
$$ \sum_{d \mid n} \frac{1}{d} \sum_{e \mid d} \mu(e)\,k^{d/e} = \sum_{m \mid n} \frac{k^m}{m} \sum_{e \mid n/m} \frac{\mu(e)}{e} = \sum_{m \mid n} \frac{k^m}{m} \cdot \frac{\varphi(n/m)}{n/m} = \frac{1}{n} \sum_{m \mid n} \varphi(n/m)\,k^m . \qquad \blacksquare $$

**Checks.** By exhaustive enumeration, the numbers of Lyndon words, primitive words and necklaces agree with the formulas for $k = 1$ and $k = 2$ up to $n = 14$ and for $k = 3$ up to $n = 10$; the product identity below was checked up to $t^{20}$ for $k = 2, 3, 4$, and the divisibility by $n$ for $n < 40$ and all integers $-20 \le k \le 20$.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $L_2(n)$ | 2 | 1 | 2 | 3 | 6 | 9 | 18 | 30 | 56 | 99 | 186 | 335 |
| $L_3(n)$ | 3 | 3 | 8 | 18 | 48 | 116 | 312 | 810 | 2184 | 5880 | 16104 | 44220 |

For example $L_2(6) = (2^6 - 2^3 - 2^2 + 2^1)/6 = 54/6 = 9$, and the nine binary Lyndon words of length 6 are `000001`, `000011`, `000101`, `000111`, `001011`, `001101`, `001111`, `010111`, `011111`.

## Consequences

- **Necklaces and aperiodic necklaces.** $L_k(n)$ is also the number of aperiodic necklaces, and $N_k(n) = \frac{1}{n} \sum_{d \mid n} \varphi(d)\,k^{n/d}$ is the formula used in [necklace counting](/necklace-counting/), which the [Burnside lemma](/burnside-lemma/) gives by another route.
- **Unique factorization.** By the Chen-Fox-Lyndon theorem every word is uniquely a nonincreasing product of Lyndon words, the [Lyndon factorization](/lyndon-factorization/). Counting words by their factorizations gives the identity
$$ \frac{1}{1 - k t} = \prod_{n \ge 1} \left( \frac{1}{1 - t^n} \right)^{L_k(n)}, $$
from which the Witt formula follows again by taking logarithms.
- **Irreducible polynomials.** For a prime power $q$, the number of monic irreducible polynomials of degree $n$ over the field with $q$ elements is $L_q(n)$, a count going back to Gauss; the identity $q^n = \sum_{d \mid n} d\,L_q(d)$ there counts the elements of the field of order $q^n$ by the degree of their minimal polynomial. See [irreducible polynomials](/irreducible-polynomial/).
- **Divisibility.** Since $L_k(n)$ is an integer, $n$ divides $\sum_{d \mid n} \mu(d)\,k^{n/d}$ for every $k \ge 1$, and so for every integer $k$, since the sum modulo $n$ depends only on $k$ modulo $n$. For a prime $n = p$ this is $p \mid k^p - k$, [Fermat's little theorem](/fermat-little-theorem/).
- **Generation and de Bruijn sequences.** The [FKM algorithm](/fkm-algorithm/) lists the Lyndon words of length dividing $n$ in lexicographic order; their concatenation is a [de Bruijn sequence](/de-bruijn-sequence/) of length $\sum_{d \mid n} d\,L_k(d) = k^n$, exactly the first identity.
- **Periodic points.** The full shift on $k$ symbols has $P_k(n) = n\,L_k(n)$ points of least period $n$, and $L_k(n)$ orbits of length $n$.
- **Free Lie algebras.** The degree-$n$ part of the free Lie algebra on $k$ generators has dimension $L_k(n)$, and the brackets of Lyndon words form a basis of it.

## Tightness

- **Size.** $L_k(n) \le k^n/n$, with equality only for $n = 1$. In the other direction, $n\,L_k(n) \ge k^n - \sum_{d \mid n,\, d < n} k^d \ge k^n - \sum_{j=1}^{\lfloor n/2 \rfloor} k^j$, so $L_k(n) = k^n/n + O(k^{n/2}/n)$ for $k \ge 2$. For a prime $n$ the middle bound is exact: $L_k(n) = (k^n - k)/n$.
- **One letter.** For $k = 1$, $L_1(1) = 1$ and $L_1(n) = \frac{1}{n} \sum_{d \mid n} \mu(d) = 0$ for $n \ge 2$: the only Lyndon word over one letter is the letter itself.
- **The order does not matter for the count.** Different total orders on $\Sigma$ give different sets of Lyndon words but the same number, since the count depends only on the classes of primitive words.
- **Bracelets.** If reflections are also allowed, the classes are no longer of equal size, and the count of [bracelets](/bracelet/) needs the full Burnside lemma rather than this formula.

## History

Gauss counted the irreducible polynomials of degree $n$ over a prime field with this formula in work published after his death. Moreau (1872) counted necklaces of beads in several colors. Witt (1937) proved that the dimensions of the homogeneous components of a free Lie algebra are $\frac{1}{n}\sum_{d \mid n} \mu(d)\,k^{n/d}$, which gives the formula its name. Lyndon (1954) introduced standard lexicographic sequences, now Lyndon words, and Chen, Fox and Lyndon (1958) proved the unique factorization of words into them. Metropolis and Rota (1983) called $M(k, n) = \frac{1}{n}\sum_{d \mid n} \mu(d)\,k^{n/d}$ the necklace polynomial.

## References
