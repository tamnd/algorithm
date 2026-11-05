---
tag: 2CTT9C
kind: definition
slug: bracelet
name: Bracelet
aliases:
- free necklace
- turn-necklace
area: strings/string-combinatorics
level: core
summary: A necklace equivalence class that also identifies reflections of the word.
prereqs: [necklace]
see_also: [necklace-counting, burnside-lemma, polya-enumeration-theorem, fkm-algorithm, booth-algorithm, necklace-enumeration, palindrome, lyndon-word]
sources:
  - paper: doi:10.1215/ijm/1255631587
    title: Edgar N. Gilbert and John Riordan, Symmetry types of periodic sequences, Illinois Journal of Mathematics 5(4), 1961, 657-665
    locator: the counts of periodic sequences up to rotation and up to rotation and reversal
  - paper: doi:10.1137/S0097539700377037
    title: Joe Sawada, Generating bracelets in constant amortized time, SIAM Journal on Computing 31(1), 2001, 259-268
    locator: the definition of bracelets as the least representatives under rotation and reversal, and their generation in constant amortized time
  - url: "https://oeis.org/A000029"
    locator: OEIS A000029, the number of binary bracelets of length n (necklaces of n beads in 2 colors, allowing turning over), with the formula
  - url: "https://oeis.org/A027671"
    locator: OEIS A027671, the number of ternary bracelets of length n
---

A bracelet is a class of words that are equal up to rotation and reversal, like beads on a loop of string that can be turned around and also flipped over. It is a coarser class than a [necklace](/necklace/), which allows only rotation: `001011` and `001101` are different necklaces but the same bracelet, since each is a rotation of the reverse of the other. As with necklaces, a bracelet is represented by its lexicographically least member, and the number of bracelets follows from [Burnside's lemma](/burnside-lemma/) with the dihedral group.

## Definition

Let $\Sigma$ be a finite totally ordered [alphabet](/alphabet/) of $k$ letters; the order is used only to pick representatives. Indices are 0-based. For $w = w[0..n-1]$, the rotation by $i$ is $\rho^i(w) = w[i..n-1]\,w[0..i-1]$, and the reversal is $w^R = w[n-1]\,w[n-2] \cdots w[0]$.

**Bracelet.** Words $u, v \in \Sigma^n$ are equivalent as bracelets if $v = \rho^i(u)$ or $v = \rho^i(u^R)$ for some $i$. The classes are the orbits of the dihedral group $D_n$, of order $2n$ for $n \ge 3$, acting on the positions $0, \ldots, n - 1$ placed around a circle; a bracelet is such a class.

**Representative.** The bracelet of $w$ is represented by the least word in its class. A word $w$ is a bracelet representative, often itself called a bracelet, if it is a necklace (least among its rotations) and $w \le \rho^i(w^R)$ for every $i$. It can be tested in $O(n)$ time: compute the least rotation of $w$ and of $w^R$, for instance with [Booth's algorithm](/booth-algorithm/), and check that $w$ equals the first and is at most the second.

**Chiral and achiral.** A necklace is achiral, or symmetric, if its reversal is a rotation of it; then its bracelet is the same set as the necklace. Otherwise it is chiral, and its bracelet is the union of two necklaces, the necklace of $w$ and that of $w^R$.

### Basic facts

1. **Counting.** By Burnside's lemma, the number of bracelets of length $n \ge 1$ over $k$ letters is
$$ B_k(n) = \begin{cases} \frac{1}{2} N_k(n) + \frac{1}{2} k^{(n+1)/2} & n \text{ odd}, \\ \frac{1}{2} N_k(n) + \frac{k+1}{4} k^{n/2} & n \text{ even}, \end{cases} $$
where $N_k(n) = \frac{1}{n} \sum_{d \mid n} \varphi(d)\,k^{n/d}$ is the number of necklaces, as on the [necklace counting](/necklace-counting/) page. *Proof.* The rotations contribute $n N_k(n)$ fixed words in total, as in the necklace count. For odd $n$, each of the $n$ reflections fixes one position and pairs the other $n - 1$, so it fixes $k^{(n+1)/2}$ words. For even $n$, $n/2$ reflections fix two opposite positions and pair the rest, fixing $k^{n/2 + 1}$ words, and $n/2$ reflections pair all positions, fixing $k^{n/2}$ words. Dividing the total by $2n$ gives the formula. $\square$
2. **Chiral pairs.** Each chiral bracelet contains two necklaces and each achiral one contains one, so the number of chiral bracelets is $N_k(n) - B_k(n)$ and the number of achiral ones is $2B_k(n) - N_k(n)$.
3. **Small lengths.** For $n \le 2$ every necklace is achiral, so $B_k(n) = N_k(n)$. For $k = 2$ this still holds up to $n = 5$; the first binary chiral necklaces have length 6.
4. **Growth.** $B_k(n) \sim k^n / (2n)$, since the reflection terms are $O(k^{n/2 + 1})$.

## Examples and non-examples

**Counts.** For $n = 1, \ldots, 10$:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| binary necklaces $N_2(n)$ | 2 | 3 | 4 | 6 | 8 | 14 | 20 | 36 | 60 | 108 |
| binary bracelets $B_2(n)$ | 2 | 3 | 4 | 6 | 8 | 13 | 18 | 30 | 46 | 78 |

For three letters and $n = 1, \ldots, 7$ the bracelets number 3, 6, 10, 21, 39, 92, 198, against 3, 6, 11, 24, 51, 130, 315 necklaces.

**Bracelets that are one necklace.**

- `0011`: its reversal `1100` is a rotation of it.
- `0101`, `000`, and every word over one letter.
- `0010`, whose least rotation is `0001`; its reversal `0100` is also a rotation of `0001`.

**Bracelets with two necklaces.**

- `001011` and `001101`, binary, length 6: the reversal of `001011` is `110100`, whose least rotation is `001101`. This is the only binary chiral pair of length 6, so $B_2(6) = 14 - 1 = 13$.
- `012` and `021` over three letters: the reversal of `012` is `210`, a rotation of `021`. So $B_3(3) = 11 - 1 = 10$.
- In length 7, the binary chiral pairs are `0001011` with `0001101`, and `0010111` with `0011101`.

**Non-examples.**

- `001101` is a necklace but not a bracelet representative, because the rotation `001011` of its reversal is smaller.
- `abc` and `acb` are different necklaces, but the same bracelet, so treating them as different bracelets is the error of forgetting reflections.

## Related definitions

- **[Necklace](/necklace/).** The class under rotation only, the orbit of the cyclic group; each bracelet is one necklace or the union of two.
- **[Lyndon word](/lyndon-word/).** An aperiodic necklace representative. The bracelets whose representative is a Lyndon word are sometimes called Lyndon bracelets.
- **[Necklace counting](/necklace-counting/) and the [Pólya enumeration theorem](/polya-enumeration-theorem/).** The general method to count orbits under a group; for bracelets the group is dihedral, and Pólya's theorem also counts bracelets with a given number of each letter.
- **Generation.** Sawada's algorithm lists the bracelet representatives in constant amortized time, by running the necklace generation of the [FKM algorithm](/fkm-algorithm/) style and rejecting, cheaply, the necklaces that are larger than a rotation of their reversal. See [necklace enumeration](/necklace-enumeration/).
- **[Palindrome](/palindrome/).** A word is achiral, that is, its reversal is one of its rotations, exactly when it is a product $pq$ of two palindromes, one of which may be empty. For example `001011` is not such a product, while `0010` $=$ `0` $\cdot$ `010`.

## References
