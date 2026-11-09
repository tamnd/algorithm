---
tag: R0GV2G
kind: problem
slug: necklace-counting
name: Counting necklaces and bracelets
aliases:
- Necklace counting
- Pólya counting of necklaces
- bracelet counting
- counting necklaces
- counting Lyndon words
area: combinatorics/counting-algorithms
level: advanced
summary: Count the words of length n over k letters up to rotation (necklaces), up to rotation and reversal (bracelets), and the aperiodic necklaces (Lyndon words).
prereqs: [burnside-lemma, euler-totient, mobius-function, necklace]
see_also: [polya-enumeration-theorem, necklace-enumeration, lyndon-word, de-bruijn-sequence, irreducible-polynomial, mobius-inversion, cattell-necklace-generation, cyclic-group]
sources:
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 4.9, Phi and Mu (the number of necklaces with the totient function, and Möbius inversion)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1 (prime strings and necklaces, Algorithm F, and their counts)
  - book: isbn:9780521006019
    title: J. H. van Lint and R. M. Wilson, A Course in Combinatorics, second edition, Cambridge University Press, 2001
    locator: Chapter 37, Pólya theory of counting (necklaces under the cyclic and the dihedral group)
---

Necklace counting asks for the number of words of length $n$ over an alphabet of $k$ letters when two words are the same if one is a rotation of the other. The answer is $N_k(n) = \frac{1}{n} \sum_{d \mid n} \varphi(d) \, k^{n/d}$, by [Burnside's lemma](/burnside-lemma/) for the cyclic group. The same method counts bracelets, where turning the necklace over is also allowed, necklaces with a fixed number of beads of each color, and Lyndon words, the necklaces with no rotational symmetry, which also count the irreducible polynomials over a finite field.

## In plain words

You have beads in a few colors, and you put a fixed number of them on a closed string. Two necklaces are the same if you can slide the beads around the string to make one look like the other. A bracelet is a necklace that you may also flip over.

The question is how many different necklaces or bracelets there are. Listing all colorings and removing copies works for short strings only, because the number of colorings grows very fast. A short formula gives the answer: it adds a few terms, one for each number that divides the length. The same idea counts the necklaces that have no repeating pattern, and those are linked to the building blocks of codes and of finite fields.

## Definition

Notation: $n \ge 1$ is the length, $k \ge 1$ is the number of colors, $\Sigma$ is an alphabet with $|\Sigma| = k$, $\varphi$ is the [Euler totient](/euler-totient/) and $\mu$ is the [Möbius function](/mobius-function/).

Let the [cyclic group](/cyclic-group/) $C_n$ act on $\Sigma^n$ by rotation, $\rho(a_1 a_2 \cdots a_n) = a_2 \cdots a_n a_1$, and let the dihedral group $D_n$ of order $2n$ act by rotation and reversal. A *necklace* is an orbit of $C_n$, and a *bracelet* is an orbit of $D_n$. A word is *primitive* (aperiodic) if it is not $u^j$ for a word $u$ and an integer $j \ge 2$. A *Lyndon word* is a primitive word that is smallest in lexicographic order among its rotations; the Lyndon words of length $n$ are in bijection with the primitive necklaces of length $n$.

**Problem.** Given $n$ and $k$, compute

- $N_k(n)$, the number of necklaces,
- $B_k(n)$, the number of bracelets,
- $L_k(n)$, the number of Lyndon words (primitive necklaces),
- and, for a content vector $(n_1, \ldots, n_k)$ with $\sum_i n_i = n$, the number $N(n_1, \ldots, n_k)$ of necklaces with $n_i$ beads of color $i$.

The answers, for $n \ge 1$:

$$N_k(n) = \frac{1}{n} \sum_{d \mid n} \varphi(d) \, k^{n/d}, \qquad L_k(n) = \frac{1}{n} \sum_{d \mid n} \mu(d) \, k^{n/d},$$

$$B_k(n) = \begin{cases} \tfrac{1}{2} N_k(n) + \tfrac{1}{2} k^{(n+1)/2} & n \text{ odd}, \\ \tfrac{1}{2} N_k(n) + \tfrac{1}{4}(k+1) k^{n/2} & n \text{ even}, \end{cases} \qquad N(n_1, \ldots, n_k) = \frac{1}{n} \sum_{d \mid g} \varphi(d) \frac{(n/d)!}{(n_1/d)! \cdots (n_k/d)!},$$

where $g = \gcd(n_1, \ldots, n_k)$.

*Derivation.* The rotation $\rho^r$, for $0 \le r < n$, splits the positions into $\gcd(r, n)$ cycles of length $n / \gcd(r, n)$, so it fixes $k^{\gcd(r, n)}$ words. The number of $r$ with $n / \gcd(r, n) = d$ is $\varphi(d)$, for each divisor $d$ of $n$, because these are the $r = (n/d) s$ with $0 \le s < d$ and $\gcd(s, d) = 1$. Burnside's lemma gives $N_k(n)$. A word fixed by $\rho^r$ with content $(n_i)$ must use each color a multiple of $d = n/\gcd(r,n)$ times, one color per cycle, which gives the content formula. For bracelets, add the $n$ reflections. When $n$ is odd, each reflection fixes one position and pairs the rest, so it has $(n+1)/2$ cycles. When $n$ is even, $n/2$ reflections fix two positions ($n/2 + 1$ cycles) and $n/2$ fix none ($n/2$ cycles). Then $B_k(n) = \frac{1}{2n}(n N_k(n) + \text{the reflection terms})$. For Lyndon words, each word of length $n$ is $u^{n/d}$ for exactly one primitive word $u$ of length $d \mid n$, and the $d$ rotations of $u$ are distinct, so $k^n = \sum_{d \mid n} d \, L_k(d)$. [Möbius inversion](/mobius-inversion/) gives the formula for $L_k(n)$. Each necklace of length $n$ is the $(n/d)$-th power of a unique primitive necklace of length $d$, so $N_k(n) = \sum_{d \mid n} L_k(d)$.

## Variants

- **Necklaces versus bracelets.** The cyclic group gives necklaces (also called fixed necklaces), and the dihedral group gives bracelets (free necklaces). Some books say "necklace" for both, so check which group is meant.
- **Fixed content.** Count by the number of beads of each color, with the formula above or with the [Pólya enumeration theorem](/polya-enumeration-theorem/), which gives all contents at once as one polynomial.
- **Primitive necklaces.** Lyndon words count the necklaces whose $n$ rotations are all different.
- **Symmetries of the colors.** When the colors may also be permuted (for example, black and white swapped), the count needs de Bruijn's extension of Pólya's method.
- **Listing.** To list the necklaces rather than count them, use the [necklace enumeration](/necklace-enumeration/) algorithm of Fredricksen, Kessler and Maiorana, which takes constant amortized time per necklace.

## Examples

For two colors, $n = 1, \ldots, 12$:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| necklaces $N_2(n)$ (A000031) | 2 | 3 | 4 | 6 | 8 | 14 | 20 | 36 | 60 | 108 | 188 | 352 |
| bracelets $B_2(n)$ (A000029) | 2 | 3 | 4 | 6 | 8 | 13 | 18 | 30 | 46 | 78 | 126 | 224 |
| Lyndon words $L_2(n)$ (A001037) | 2 | 1 | 2 | 3 | 6 | 9 | 18 | 30 | 56 | 99 | 186 | 335 |

For three colors: $N_3(n) = 3, 6, 11, 24, 51, 130, 315, 834$ (A001867), $B_3(n) = 3, 6, 10, 21, 39, 92, 198, 498$ (A027671) and $L_3(n) = 3, 3, 8, 18, 48, 116, 312, 810$ (A027376), for $n = 1, \ldots, 8$.

**A worked case.** For $n = 6$ and $k = 2$, the divisors are 1, 2, 3, 6, with $\varphi = 1, 1, 2, 2$. So $N_2(6) = \frac{1}{6}(2^6 + 2^3 + 2 \cdot 2^2 + 2 \cdot 2^1) = \frac{84}{6} = 14$. With $\mu(1), \mu(2), \mu(3), \mu(6) = 1, -1, -1, 1$, $L_2(6) = \frac{1}{6}(64 - 8 - 4 + 2) = 9$. The 5 necklaces that are not primitive are 000000, 111111, 010101, 001001 and 011011. For bracelets, $B_2(6) = \frac{14}{2} + \frac{3 \cdot 8}{4} = 13$: the necklaces 001011 and 001101 are mirror images, and they form one bracelet.

**Fixed content.** With three black and three white beads, $g = 3$ and $N(3, 3) = \frac{1}{6}\left(\binom{6}{3} + \varphi(3) \cdot \frac{2!}{1!\,1!}\right) = \frac{20 + 4}{6} = 4$. With four of each, $N(4, 4) = 10$, and with two beads each of three colors, $N(2, 2, 2) = 16$.

**A non-example.** Dividing the number of words by the number of rotations, $2^6 / 6$, is not even an integer. It fails because the orbits do not all have size $n$: the orbit of 010101 has 2 words and the orbit of 000000 has 1.

## Known algorithms

- **The divisor-sum formulas.** Factor $n$, list its divisors, and evaluate the sums. With $\tau(n)$ divisors, this takes $O(\tau(n))$ operations on big integers of about $n \log_2 k$ binary digits, plus the time to factor $n$, which is small next to $n$ for every practical length. The bracelet and content counts cost the same up to a constant factor.
- **Pólya's polynomial.** For all contents at once, expand the cycle index of $C_n$ or $D_n$ at $x_d = y_1^d + \cdots + y_k^d$. The output has $\binom{n+k-1}{k-1}$ coefficients.
- **Listing and counting.** The [necklace enumeration](/necklace-enumeration/) algorithm lists the $N_k(n)$ necklaces, or only the Lyndon words, in lexicographic order in constant amortized time per necklace. Counting by listing is useful only to check the formulas for small $n$. [Cattell's generator](/cattell-necklace-generation/) lists the necklaces with a fixed content.

## Bounds

For all $n \ge 1$ and $k \ge 1$,

$$\frac{k^n}{n} \le N_k(n) \le \frac{k^n}{n} + k^{n/2}, \qquad \frac{k^n - 2k^{n/2}}{n} \le L_k(n) \le \frac{k^n}{n}.$$

*Proof.* In the sum for $N_k(n)$, the term $d = 1$ is $k^n$, and each other term is at most $\varphi(d) k^{n/2}$, because $n/d \le n/2$. Since $\sum_{d \mid n} \varphi(d) = n$, the other terms add up to at most $n k^{n/2}$, and dividing by $n$ gives the upper bound. All terms are at least 0, which gives the lower bound. For Lyndon words, $n L_k(n) \le k^n$ by the identity $k^n = \sum_{d \mid n} d L_k(d)$, and the words that are not primitive number at most $\sum_{j=1}^{\lfloor n/2 \rfloor} k^j \le 2k^{n/2}$ for $k \ge 2$, so $n L_k(n) \ge k^n - 2k^{n/2}$. $\square$

So $N_k(n) \sim L_k(n) \sim k^n / n$ and $B_k(n) \sim k^n / (2n)$ as $n \to \infty$ for fixed $k \ge 2$, since the reflection terms of $B_k(n)$ are $O(k^{n/2+1})$. The exact answer has about $n \log_2 k - \log_2 n$ binary digits, and an exact algorithm must write that many digits.

## Reductions

- **Irreducible polynomials.** For a prime power $q$, the number of monic [irreducible polynomials](/irreducible-polynomial/) of degree $n$ over the finite field $\mathbb{F}_q$ is $L_q(n)$. The proof uses the same identity $q^n = \sum_{d \mid n} d \, L_q(d)$, which counts the elements of $\mathbb{F}_{q^n}$ by the degree of their minimal polynomial. This is why OEIS A001037 has both names.
- **De Bruijn sequences.** The concatenation, in lexicographic order, of the Lyndon words whose length divides $n$ is a [de Bruijn sequence](/de-bruijn-sequence/) of order $n$. The length check is $\sum_{d \mid n} d \, L_k(d) = k^n$.
- **From the general orbit problem.** Necklace counting is the orbit-counting problem for the cyclic group, so any solution of the [Pólya](/polya-enumeration-theorem/) problem solves it.

## Applications

- The number of circular arrangements of colored items up to rotation, for example seatings at a round table or patterns on a rotating disk.
- The dimension of the homogeneous parts of a free Lie algebra (Witt's formula is $L_k(n)$).
- The analysis of the necklace generation algorithms, whose cost per object depends on $N_k(n) / k^n$.

## References
