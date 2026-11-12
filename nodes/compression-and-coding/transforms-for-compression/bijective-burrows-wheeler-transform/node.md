---
tag: R9BPTQ
kind: algorithm
slug: bijective-burrows-wheeler-transform
name: Bijective Burrows-Wheeler transform
aliases:
- bijective BWT
- BBWT
- BWTS
area: compression-and-coding/transforms-for-compression
level: research
summary: A Burrows-Wheeler transform with no sentinel and no index. It sorts the rotations of the Lyndon factors of the text in omega order, and every string has exactly one preimage.
model: word-ram
complexity:
  vars: {n: the length of the text}
  time: {worst: "O(n^2 log n)", linear_method: Θ(n)}
  space: {extra: "O(n^2)", linear_method: Θ(n)}
properties: {deterministic: true, recursive: false, online: false, comparison: true}
history:
  year: 2009
  people: [Joseph Yossi Gil, David A. Scott, Manfred Kufleitner]
  note: Gil and Scott described the transform in a preprint of 2009, put on arXiv in 2012. Kufleitner gave a proof and further variants at the Prague Stringology Conference 2009.
prereqs: [burrows-wheeler-transform, lyndon-factorization]
see_also: [inverse-burrows-wheeler-transform, lyndon-word, duval-algorithm, word-conjugacy, fine-and-wilf-theorem, primitive-word, minimal-rotation]
sources:
  - paper: "Joseph Yossi Gil and David A. Scott, A bijective string sorting transform, arXiv:1201.3077, 2012 (preprint of 2009)"
    title: Gil and Scott, A bijective string sorting transform
    locator: the definition by the Lyndon factorization and the order of infinite periodic words, and the inverse by the cycles of the permutation
  - paper: "Manfred Kufleitner, On bijective variants of the Burrows-Wheeler transform, Proceedings of the Prague Stringology Conference 2009, pages 65 to 79, arXiv:0908.0239"
    title: Kufleitner, On bijective variants of the Burrows-Wheeler transform
    locator: pages 65 to 79 (a proof that the transform is a bijection, with the omega order, and a new bijective variant of the sort transform of order k)
  - paper: doi:10.4230/OASIcs.Manzini.2
    title: Hideo Bannai, Dominik Köppl and Zsuzsanna Lipták, A Survey of the Bijective Burrows-Wheeler Transform, OASIcs volume 131, 2025
    locator: pages 2:1 to 2:26 (definitions, the inverse, the linear-time construction and open problems)
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge University Press, 1997
    locator: Chapter 5 (Lyndon words and the unique factorization theorem of Chen, Fox and Lyndon)
---

The bijective Burrows-Wheeler transform (BBWT) is a variant of the [Burrows-Wheeler transform](/burrows-wheeler-transform/) that is a bijection from $\Sigma^n$ to $\Sigma^n$. It cuts the text into its [Lyndon factors](/lyndon-factorization/), sorts all rotations of all factors in the $\omega$ order, the order of their infinite repetitions, and outputs the last symbol of each rotation. Unlike the BWT, it needs no sentinel and no start index, and every string is the transform of exactly one string. The inverse uses the same LF mapping as the [inverse BWT](/inverse-burrows-wheeler-transform/), but the permutation has one cycle for each factor. A linear-time construction is known; the version on this page sorts with a simple key and takes $O(n^2 \log n)$ time.

## In plain words

The usual transform needs extra data to undo it: an end marker or the number of the first line. This variant needs none.

First, cut the text into special pieces called Lyndon words. A Lyndon word comes first in sorted order among all its rotations, and each text has exactly one cut into such pieces with the pieces in falling order. Then take every rotation of every piece and sort them all together. To compare two rotations of different lengths, repeat each one forever and compare the endless strings. Output the last symbol of each rotation in this order.

To undo it, follow the same jumps as in the usual inverse. They now go around in several small loops, one for each piece. Read each loop, put the pieces back in falling order, and you have the text.

## The problem

**Input.** A string $T$ of length $n \ge 0$ over an ordered alphabet $\Sigma$.

**Output.** A string $\mathrm{BBWT}(T)$ of length $n$ that is a permutation of $T$, such that the map $T \mapsto \mathrm{BBWT}(T)$ is a bijection of $\Sigma^n$.

**Definitions.** A nonempty word $w$ is a [Lyndon word](/lyndon-word/) if it is strictly smaller than each of its proper rotations. By the theorem of Chen, Fox and Lyndon, each string $T$ has exactly one factorization $T = w_1 w_2 \cdots w_m$ into Lyndon words with $w_1 \ge w_2 \ge \cdots \ge w_m$ in lexicographic order. For a nonempty word $u$, $u^\omega = u u u \cdots$ is its infinite repetition. The $\omega$ order is $u \le_\omega v$ if and only if $u^\omega \le v^\omega$ in lexicographic order. On words of the same length it is the usual order; on words of different lengths it can differ from it: $\texttt{b} < \texttt{ba}$, but $\texttt{ba} <_\omega \texttt{b}$, because $\texttt{baba}\cdots < \texttt{bbbb}\cdots$.

## The algorithm

```pseudo id=main
BBWT(T[0 .. n − 1])
L1  w_1, …, w_m ← the Lyndon factors of T        ▷ Duval's algorithm, O(n)
L2  R ← an empty list
L3  for each factor w in w_1, …, w_m do
L4      for i ← 0 to |w| − 1 do append the rotation w[i ..] w[.. i − 1] to R
L5  sort R in ω order                             ▷ a multiset of n words
L6  L ← the last symbol of each word of R, in sorted order
L7  return L
```

Line L1 uses [Duval's algorithm](/duval-algorithm/). Line L5 compares two words $u$ and $v$ by the first $2n$ symbols of $u^\omega$ and $v^\omega$. This key is exact: by the [theorem of Fine and Wilf](/fine-and-wilf-theorem/), if $u^\omega$ and $v^\omega$ agree on their first $|u| + |v| - \gcd(|u|, |v|)$ symbols, then they are equal, and $|u| + |v| \le 2n$.

The inverse:

```pseudo id=inverse
INVERSE-BBWT(L[0 .. n − 1])
I1  LF[i] ← C[L[i]] + rank_{L[i]}(L, i) for each row i   ▷ as in the inverse BWT
I2  W ← an empty list; mark all rows as not visited
I3  for r ← 0 to n − 1 do
I4      if row r is not visited then
I5          read L[r], L[LF[r]], L[LF[LF[r]]], … until the cycle returns to r, and mark the rows
I6          append the reverse of the symbols read to W        ▷ this is one factor
I7  sort W in nonincreasing lexicographic order
I8  return the concatenation of the words of W
```

## Example

Take $T = \texttt{banana}$. Duval's algorithm gives the factors $\texttt{b} \ge \texttt{an} \ge \texttt{an} \ge \texttt{a}$. The six rotations are $\texttt{b}$, $\texttt{an}$, $\texttt{na}$, $\texttt{an}$, $\texttt{na}$, $\texttt{a}$. In $\omega$ order:

| row | rotation | infinite form | last symbol |
|---|---|---|---|
| 0 | a | aaaa… | a |
| 1 | an | anan… | n |
| 2 | an | anan… | n |
| 3 | b | bbbb… | b |
| 4 | na | nana… | a |
| 5 | na | nana… | a |

So $\mathrm{BBWT}(\texttt{banana}) = \texttt{annbaa}$. Compare $\mathrm{BWT}(\texttt{banana}) = \texttt{annb\$aa}$ with the sentinel, and $(\texttt{nnbaaa}, 3)$ with the index.

**Inverse.** For $L = \texttt{annbaa}$, $C[a] = 0$, $C[b] = 3$, $C[n] = 4$, and $\mathrm{LF} = (0, 4, 5, 3, 1, 2)$. The cycles in the order of their smallest row are $(0)$, $(1\ 4)$, $(2\ 5)$, $(3)$. Row 0 gives $\texttt{a}$. Row 1 reads $L[1] = \texttt{n}$, then $L[4] = \texttt{a}$, and the reverse is $\texttt{an}$. Row 2 gives $\texttt{an}$ in the same way, and row 3 gives $\texttt{b}$. In nonincreasing order the factors are $\texttt{b}, \texttt{an}, \texttt{an}, \texttt{a}$, and the text is $\texttt{banana}$.

**A second example.** $\texttt{abracadabra}$ has the factors $\texttt{abracad} \ge \texttt{abr} \ge \texttt{a}$. The 11 rotations in $\omega$ order are a, abr, abracad, acadabr, adabrac, bra, bracada, cadabra, dabraca, rab, racadab, so $\mathrm{BBWT}(\texttt{abracadabra}) = \texttt{ardrcaaaabb}$.

## Correctness

The proof has these steps. If $u$ and $v$ are primitive and $u^\omega = v^\omega$, then $u = v$, so rotations of different Lyndon factors are equal in $\omega$ order only when they are equal words. The first symbol moves to the end in the same way as in the BWT: $(a x)^\omega = a (x a)^\omega$, so the rows that end with a symbol $c$ map in order onto the rows that start with $c$, and $\mathrm{LF}$ maps the row of $x c$ to a row of $c x$. Each cycle of $\mathrm{LF}$ has the length of its factor, and the smallest row of a cycle holds the factor, since a Lyndon word is the smallest of its rotations. Reading the cycle gives the factor reversed. The sort of line I7 restores the order $w_1 \ge \cdots \ge w_m$, so the inverse returns $T$. A map from the finite set $\Sigma^n$ to itself with a left inverse is a bijection. The full proof is below.

## Complexity

- **As written.** Line L1 takes $O(n)$ time. Line L5 sorts $n$ keys of $2n$ symbols: $O(n \log n)$ comparisons of $O(n)$ time each, so $O(n^2 \log n)$ time, and $O(n^2)$ space if the keys are stored.
- **Linear time.** Bannai, Kärkkäinen, Köppl and Piątkowski (CPM 2021) build the BBWT in $O(n)$ time with an algorithm in the style of [SA-IS](/sa-is/).
- **Inverse.** Line I1 and the cycle walks take $\Theta(n)$ time with counting. The sort of the factors in line I7 takes $O(n \log n)$ time in the simple form.

## Properties

- **Bijective.** Each string of $\Sigma^n$ is the BBWT of exactly one string of $\Sigma^n$. For the BWT, most strings with one $\$$ are not valid inputs to the inverse; here all strings are.
- **A permutation of the text.** The rows are the $n$ rotations of the factors, and their last symbols are the $n$ symbols of $T$.
- **The same as the BWT on a Lyndon word.** If $T$ is a Lyndon word, it has one factor, the rotations have the same length, the $\omega$ order is the usual order, and $\mathrm{BBWT}(T)$ is the last column of the sorted rotations of $T$; the index is not needed because $T$ is the smallest rotation, row 0.
- **Context grouping.** Rotations that start with the same long prefix are near each other in $\omega$ order, as in the BWT, so the output has runs. The context of a symbol is now a rotation of its factor, not the rest of the text.
- **Rotations of the same text.** $\mathrm{BBWT}$ depends on the cut into factors, so unlike the BWT without a sentinel, two rotations of a text usually have different transforms.

## Variants and improvements

- **Extended BWT.** The extended BWT of Mantaci, Restivo, Rosone and Sciortino (2007) applies the same $\omega$ sort to the rotations of a multiset of words. The BBWT is the extended BWT of the multiset of the Lyndon factors.
- **A bijective sort transform.** The sort transform (ST) of order $k$ sorts the rotations only by their first $k$ symbols and breaks ties by position. Kufleitner (2009) gives a bijective variant of it, and relates the BBWT to the work of Gessel and Reutenauer (1993) and of Crochemore, Désarménien and Perrin (2005) on the same permutations.
- **Linear-time construction and indexing.** Bannai et al. (CPM 2021) construct the BBWT in linear time; the survey of Bannai, Köppl and Lipták (2025) covers the inverse, pattern search on the BBWT, and open problems.

## When to use it

Use the BBWT when the start index of the BWT is a cost, for example on many short blocks, or when a bijective transform is needed by design, for example in a bijective compression chain where every bit string must decode to some text. For general compression the gain over the BWT is small, and the BWT with a [suffix array](/suffix-array/) is simpler to build and has more tools.

## Pitfalls

- **Lexicographic order on words of different lengths.** Line L5 needs the $\omega$ order. The usual order puts $\texttt{b}$ before $\texttt{ba}$; the $\omega$ order puts $\texttt{ba}$ first. With the usual order the inverse fails.
- **A key that is too short.** A prefix of $u^\omega$ of length $\max(|u|, |v|)$ does not decide the order. Use at least $|u| + |v| - \gcd(|u|, |v|)$ symbols; $2n$ is safe.
- **Equal factors.** A text such as $\texttt{banana}$ has the factor $\texttt{an}$ twice, so $R$ holds equal words. The forward step is not affected, and the inverse finds two separate cycles of the same length.
- **The order of the factors in the inverse.** The cycles come out in the order of their smallest row. The text needs the factors in nonincreasing lexicographic order, so sort them.
- **Memory.** Keys of $2n$ symbols for $n$ words take $\Theta(n^2)$ space. Compare on the fly, or use the linear method, for large inputs.

## Implementations

## History

Gil and Scott wrote a preprint on a bijective string sorting transform in 2009 and put it on arXiv in 2012. Kufleitner (Prague Stringology Conference 2009) proved that the transform is bijective and gave further bijective variants. The Lyndon factorization that the transform uses is the theorem of Chen, Fox and Lyndon (1958), and Duval (1983) gave the linear-time algorithm for it. Bannai, Kärkkäinen, Köppl and Piątkowski gave a linear-time construction of the BBWT at CPM 2021, and Bannai, Köppl and Lipták surveyed the transform in 2025.

## References
