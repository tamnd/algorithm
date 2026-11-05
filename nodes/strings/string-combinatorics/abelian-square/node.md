---
tag: PC21W6
kind: definition
slug: abelian-square
name: Abelian square
aliases:
- Abelian-equivalent square
area: strings/string-combinatorics
level: core
summary: A word uv where u and v are nonempty and Abelian equivalent.
prereqs: [abelian-equivalence, square]
see_also: [keranen-theorem, square-free-word, abelian-complexity, cube, avoidability, thue-theorem, parikh-vector, sliding-window]
sources:
  - paper: doi:10.1007/3-540-55719-9_62
    title: Veikko Keränen, Abelian squares are avoidable on 4 letters, Automata, Languages and Programming (ICALP 1992), Lecture Notes in Computer Science 623, 1992, 41-52
    locator: the introduction (the history of the problem) and the 85-uniform morphism on four letters
  - paper: "F. Michel Dekking, Strongly non-repetitive sequences and progression-free sets, Journal of Combinatorial Theory, Series A 27(2), 1979, 181-185"
    title: F. Michel Dekking, Strongly non-repetitive sequences and progression-free sets
    locator: the ternary word without Abelian cubes, the binary word without Abelian fourth powers
  - paper: "Peter A. B. Pleasants, Non-repetitive sequences, Proceedings of the Cambridge Philosophical Society 68(2), 1970, 267-274"
    title: Peter A. B. Pleasants, Non-repetitive sequences
    locator: the infinite word over five letters without Abelian squares
---

An Abelian square is a nonempty word $uv$ in which $v$ is a rearrangement of $u$: the two halves have the same length and the same number of each letter, as in `abba` or `abcacb`. It is the Abelian analogue of a [square](/square/) $uu$, with equality of the halves replaced by [Abelian equivalence](/abelian-equivalence/). Abelian squares are harder to avoid than squares: every word of length 8 over three letters contains one, and the existence of an infinite word over four letters without them, asked by Erdős, was settled by [Keränen's theorem](/keranen-theorem/) in 1992.

## Definition

Let $\Sigma$ be a finite [alphabet](/alphabet/); only equality of letters is used. Indices are 0-based. For $w \in \Sigma^*$, $\Psi(w)$ is its [Parikh vector](/parikh-vector/), the vector of the counts $|w|_a$.

**Abelian square.** A word $w$ is an Abelian square if $w = uv$ with $u, v \in \Sigma^+$ and $\Psi(u) = \Psi(v)$. Since $\Psi$ gives the length, $|u| = |v|$, so $|w|$ is even and $u = w[0..m-1]$, $v = w[m..2m-1]$ with $m = |w|/2$. The number $m$ is the period of the Abelian square, in the Abelian sense.

**Abelian-square-free.** A finite or infinite word is Abelian-square-free if no factor is an Abelian square, that is, if there are no $i \ge 0$ and $m \ge 1$ with
$$ \Psi(w[i..i+m-1]) = \Psi(w[i+m..i+2m-1]). $$

**Abelian $k$-th power.** More generally, $u_1 u_2 \cdots u_k$ with nonempty, pairwise Abelian equivalent $u_j$ is an Abelian $k$-th power; $k = 2$ is the Abelian square and $k = 3$ the Abelian cube.

### Basic facts

1. **Each square is an Abelian square,** since $u = v$ implies $\Psi(u) = \Psi(v)$. So an Abelian-square-free word is [square-free](/square-free-word/). The converse fails: `abcacb` is an Abelian square, and the word `abcacb` contains no square.
2. **Each factor $aa$ is an Abelian square.** So in an Abelian-square-free word, adjacent letters differ.
3. **Two letters.** The only binary Abelian-square-free words of length 3 are `aba` and `bab`, and there are none of length 4. *Proof.* Adjacent letters differ, so a binary word of length 4 without the factors $aa$ and $bb$ is `abab` or `baba`, and both are Abelian squares (even squares). $\square$
4. **Three letters.** The longest ternary Abelian-square-free words have length 7. The numbers of them for lengths 0 to 8 are 1, 3, 6, 12, 18, 30, 30, 18, 0. An example of length 7 is `abacaba`. These numbers come from a search of all extensions, one letter at a time, with a test of every suffix of even length.
5. **Four letters.** The numbers for lengths 1 to 14 are 4, 12, 36, 96, 264, 648, 1584, 3576, 7872, 15360, 29184, 51120, 90384, 158448. They keep growing, and Keränen proved that an infinite Abelian-square-free word over four letters exists.
6. **Testing.** All Abelian square factors of a word of length $n$ can be found in $O(n^2)$ time on an integer alphabet of size $\sigma = O(n)$: for each half-length $m$, slide two adjacent windows of length $m$ over the word and keep the number of letters whose counts in the two windows differ. Each slide changes at most four counts, so it updates this number in $O(1)$ time.

## Examples and non-examples

**Abelian squares.**

- `abba`: $\Psi($`ab`$) = \Psi($`ba`$) = (1, 1)$.
- `abcacb`: the halves `abc` and `acb` are permutations of each other, and the whole word is square-free.
- `aabbab` is not an Abelian square, since `aab` and `bab` have the vectors $(2, 1)$ and $(1, 2)$; but its factor `abba`, at the indices 1 to 4, is one.
- Each square, such as `abab` or `aa`.

**Non-examples.**

- `aba`: odd length.
- `aabb`: the halves `aa` and `bb` have different counts. It contains the Abelian squares `aa` and `bb`.
- `abacaba` contains no Abelian square: its factors of even length are `ab`, `ba`, `ac`, `ca` (length 2), `abac`, `baca`, `acab`, `caba` (length 4) and `abacab`, `bacaba` (length 6), and in each the two halves have different vectors.
- $\varepsilon$ is excluded: $u$ must be nonempty.

## Related definitions

- **[Square](/square/).** A word $uu$; the Abelian square weakens the equality $u = v$ to $\Psi(u) = \Psi(v)$.
- **[Abelian equivalence](/abelian-equivalence/) and [Parikh vector](/parikh-vector/).** The relation and the map that define the notion.
- **[Keränen's theorem](/keranen-theorem/).** An infinite Abelian-square-free word over four letters exists. Pleasants had done five letters in 1970, and fact 4 shows that three letters are not enough.
- **Abelian cubes and fourth powers.** Dekking (1979) gave an infinite ternary word without Abelian cubes and an infinite binary word without Abelian fourth powers. Both are optimal: Abelian squares cannot be avoided on three letters by fact 4, and every binary word of length 10 contains an Abelian cube, while some binary words of length 9 do not.
- **[Avoidability](/avoidability/).** The general question whether an infinite word can avoid all instances of a pattern; Abelian squares are its commutative case.
- **[Abelian complexity](/abelian-complexity/).** The number of distinct Parikh vectors of factors of each length.

## References
