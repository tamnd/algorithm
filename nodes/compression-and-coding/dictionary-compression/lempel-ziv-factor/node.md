---
tag: 2TX28T
kind: definition
slug: lempel-ziv-factor
name: Lempel-Ziv factor
aliases:
- LZ77 factor
- LZ phrase
area: compression-and-coding/dictionary-compression
level: intro
summary: "One phrase of the LZ factorization: the longest prefix of the rest of the string that also starts earlier, or one new symbol."
prereqs: [back-reference]
see_also: [lempel-ziv-factorization, longest-previous-factor, lempel-ziv-parsing, lz77, lz-end, string-attractor, lyndon-factorization, lempel-ziv-complexity]
sources:
  - paper: doi:10.1007/978-3-642-38905-4_19
    title: Juha Kärkkäinen, Dominik Kempa and Simon J. Puglisi, Linear time Lempel-Ziv factorization, simple, fast, small, CPM 2013, LNCS 7922
    locator: Section 2, Preliminaries (the factor as a pair of a previous position and a length, or a new letter; the example zzzzzipzip)
  - paper: doi:10.1016/j.ipl.2007.10.006
    title: Maxime Crochemore and Lucian Ilie, Computing Longest Previous Factor in linear time and applications, Information Processing Letters 106(2), 2008
    locator: the definition of the LPF array and the factorization read from it
  - paper: doi:10.1109/TIT.1976.1055501
    title: Abraham Lempel and Jacob Ziv, On the complexity of finite sequences, IEEE Transactions on Information Theory 22(1), 1976
    locator: pages 75 to 81 (copies from the earlier part of a sequence, which may extend into the part being produced)
---

A Lempel-Ziv factor is one phrase of the [Lempel-Ziv factorization](/lempel-ziv-factorization/) of a string. At a position $i$ it is the longest prefix of the rest of the string that also starts at some earlier position, where the earlier copy may run past $i$; if no such prefix exists, it is the single symbol at $i$, which then occurs for the first time. It is the unit that LZ77-type compressors write as a [back-reference](/back-reference/), and the number of factors, $z$, is a standard measure of repetition.

## Definition

Let $T = T[1..n]$ be a string over an alphabet $\Sigma$ with $\sigma$ symbols, and let $1 \le i \le n$.

**Longest previous factor.** The value

$$\mathrm{lpf}(i) = \max\{\, \ell \ge 0 : T[j..j+\ell-1] = T[i..i+\ell-1] \text{ for some } j < i \,\}$$

is the length of the longest prefix of $T[i..n]$ that also starts before $i$. The occurrence at $j$ may overlap the one at $i$ ($j + \ell - 1 \ge i$ is allowed). The array $\mathrm{lpf}[1..n]$ is the [longest previous factor](/longest-previous-factor/) array, and $\mathrm{lpf}(1) = 0$.

**Factor at $i$.** The Lempel-Ziv factor that starts at $i$ is

$$f(i) = T[i .. i + \max(1, \mathrm{lpf}(i)) - 1].$$

If $\mathrm{lpf}(i) \ge 1$, any $j < i$ that attains the maximum is a *source* of the factor, and the factor is written as the pair $(j, \mathrm{lpf}(i))$ or, with a distance, $(i - j, \mathrm{lpf}(i))$. If $\mathrm{lpf}(i) = 0$, the symbol $T[i]$ does not occur in $T[1..i-1]$, and the factor is written as that symbol.

**The factorization.** The factors of $T$ are $f_1 = f(1)$ and $f_{k+1} = f(1 + |f_1 \cdots f_k|)$ while that position is at most $n$. So $T = f_1 f_2 \cdots f_z$, where $z = z(T)$ is the number of factors. The word "factor" alone means any substring in combinatorics on words; a Lempel-Ziv factor is the particular substring that this greedy rule picks.

**Two facts that follow.** First, $\mathrm{lpf}(i+1) \ge \mathrm{lpf}(i) - 1$, since a copy of $T[i..i+\ell-1]$ that starts at $j$ gives a copy of $T[i+1..i+\ell-1]$ that starts at $j+1 < i+1$. Second, a factor $f_k$ that ends at position $e < n$ is maximal: $f_k T[e+1]$ does not start at any earlier position, or the rule would have taken it.

## Examples and non-examples

- In $T = abababab$ the factors are $a \mid b \mid ababab$. The third factor starts at 3, has source 1 and length 6, and overlaps its source: $T[1..6] = T[3..8]$.
- In $T = aaaaaaaa$ the factors are $a \mid aaaaaaa$: the factor at 2 has source 1 (distance 1) and length 7.
- In $T = abracadabra$ the factors are $a \mid b \mid r \mid a \mid c \mid a \mid d \mid abra$, so $z = 8$. The factor at 4 is $a$, with $\mathrm{lpf}(4) = 1$ and source 1; the factor at 8 is $abra$ with source 1.
- In $T = zzzzzipzip$ the factors are $z \mid zzzz \mid i \mid p \mid zip$, so $z = 5$. This is the example of Kärkkäinen, Kempa and Puglisi.
- *Non-example.* In $abracadabra$, the phrase $ac$ at position 4 is a phrase of the [LZ77](/lz77/) triple parse (a copy of $a$ plus the literal $c$), not a Lempel-Ziv factor: $ac$ does not occur earlier, so the factor at 4 is only $a$.
- *Non-example.* If the source must lie inside $T[1..i-1]$ (no self-reference), the phrase of $abababab$ at position 3 is $ab$, not $ababab$. That rule gives a different factorization, with 4 phrases here.
## Related definitions

- **LZ77 phrase.** In the [LZ77](/lz77/) triple parse, the phrase at $i$ is $T[i..i+\ell]$: the longest copy (in a window) followed by one literal symbol. It is one symbol longer than the copy part.
- **LZ78 phrase.** In [LZ78 parsing](/lz78-parsing/), the copy must be a whole earlier phrase, and one symbol follows.
- **LZ-End phrase.** In [LZ-End](/lz-end/), the source of the copy must end where an earlier phrase ends.
- **Lempel-Ziv parsing.** The family of all these parses is described on [Lempel-Ziv parsing](/lempel-ziv-parsing/).
- **String attractor.** The first positions of the Lempel-Ziv factors form a [string attractor](/string-attractor/), and so do the last positions: the leftmost occurrence of any substring cannot lie inside one copy factor, so it crosses a factor boundary or is a new symbol. So the smallest attractor has at most $z$ positions.
- **Lyndon factor.** A factor of the [Lyndon factorization](/lyndon-factorization/) is a Lyndon word, chosen by lexicographic order and not by repetition.
- **Lempel-Ziv complexity.** The phrase count of the 1976 parse, used as a complexity measure, is on [Lempel-Ziv complexity](/lempel-ziv-complexity/).

## References
