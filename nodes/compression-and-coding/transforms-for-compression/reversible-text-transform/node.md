---
tag: 3C2Q9R
kind: problem
slug: reversible-text-transform
name: Reversible text transform
aliases:
- invertible string permutation
area: compression-and-coding/transforms-for-compression
level: core
summary: Change a text, before compression, by an invertible map that the compressor handles better, such as a permutation like the BWT or a recoding of capitals and words.
prereqs: [lossless-compression]
see_also: [burrows-wheeler-transform, bijective-burrows-wheeler-transform, move-to-front-transform, static-dictionary-compression, brotli, byte-pair-encoding, prediction-by-partial-matching, kolmogorov-complexity]
sources:
  - paper: "Holger Kruse and Amar Mukherjee, Preprocessing text to improve compression ratios, Proceedings of the Data Compression Conference (DCC 1998), IEEE, 1998"
    title: Kruse and Mukherjee, Preprocessing text to improve compression ratios
    locator: page 556 (star encoding of the words of a text with a shared dictionary)
  - paper: "Fauzia S. Awan and Amar Mukherjee, LIPT: a lossless text transform to improve compression, Proceedings of the International Conference on Information Technology: Coding and Computing (ITCC 2001), IEEE, Las Vegas, April 2001"
    title: Awan and Mukherjee, LIPT
    locator: pages 452 to 460 (the length index preserving transform)
  - paper: "Przemysław Skibiński, Szymon Grabowski and Sebastian Deorowicz, Revisiting dictionary-based compression, Software: Practice and Experience 35(15), 2005"
    title: Skibiński, Grabowski and Deorowicz, Revisiting dictionary-based compression
    locator: the word replacement transform and its capital conversion and other text preprocessing steps (exact pages not checked)
  - paper: "RFC 7932, J. Alakuijala and Z. Szabadka, Brotli Compressed Data Format, IETF, July 2016"
    title: RFC 7932, Brotli Compressed Data Format
    locator: Appendix B (the transforms of the words of the static dictionary, which include upper case first and upper case all)
---

A reversible text transform is an invertible map that is applied to a text before a general compressor, and undone after the decompressor, so that the compressor sees data it models better. The transform does not compress by itself; it moves structure to where the compressor can see it. There are two kinds. A *permutation* keeps the symbols and changes their order: the [Burrows-Wheeler transform](/burrows-wheeler-transform/) groups symbols by their context, and its [bijective variant](/bijective-burrows-wheeler-transform/) does so with no extra data. A *recoding* changes the symbols: capital conversion writes `The` as a flag and `the`, and dictionary transforms replace frequent words by short codes. The second kind was studied as text preprocessing in the late 1990s and 2000s (star encoding, LIPT, the word replacement transform), and a form of it is built into the static dictionary of Brotli.

## In plain words

A compressor learns patterns from the text it reads. Sometimes the same pattern hides behind small changes, and the compressor learns it twice. "The" at the start of a sentence and "the" inside one are the same word, but to a compressor they are different strings.

A reversible transform rewrites the text so that such patterns become plain to see, and it keeps enough marks to undo the change exactly. For example, write "The" as a mark for "capital" followed by "the". Now there is only one form of the word to learn.

Another kind of transform does not change any symbol but puts them in a new order, so that equal symbols come together. Both kinds must be exactly reversible, since not one character of the text may be lost.

## Definition

**Input.** A text $x \in \Sigma^*$ and a target compressor $C$.

**Output.** A map $\tau : \Sigma^* \to \Gamma^*$ with an inverse $\tau^{-1}$, both fast to compute, such that $|C(\tau(x))|$ is smaller than $|C(x)|$ for the texts of interest. The full compressor is $x \mapsto C(\tau(x))$, and the decompressor is $y \mapsto \tau^{-1}(C^{-1}(y))$.

The map must be one to one on all of $\Sigma^*$, including texts that hold the special characters the transform uses as flags. A transform that is a *permutation* has $\Gamma = \Sigma$ (plus perhaps a sentinel or an index) and $\tau(x)$ is a reordering of $x$.

## Variants

- **Permutations.** The BWT needs a sentinel or a start index; the bijective BWT needs neither and is a bijection of $\Sigma^n$.
- **Case and spacing.** Capital conversion, and similar transforms for end-of-line codes or for spaces before words.
- **Dictionary transforms.** A dictionary of words, fixed or sent with the data, maps each known word to a short code. In star encoding, the codes are strings of `*` with a few letters, of the same length as the word. In LIPT, the code holds the length of the word and its index among the words of that length. The word replacement transform of Skibiński, Grabowski and Deorowicz uses short byte codes and adds capital conversion.
- **Transforms for other data.** Filters for machine code turn the relative addresses of x86 call instructions into absolute ones, so that calls to the same function look the same; the xz format applies such filters before its main compressor.

## Examples

**Capital conversion.** The flags are CAP (the first letter is upper case, the rest lower case), UPPER (all of two or more letters are upper case), and ESC (the next character is a literal flag character). Each maximal run of ASCII letters is handled as one word. The text `The NASA team met THE Team.` becomes

`CAP the UPPER nasa team met UPPER the CAP team.`

and the words `The`, `THE` and `the` now all appear as `the`. A word in mixed case, such as `iPhone`, stays as it is.

**Dictionary transform.** With the dictionary $0{:}\ \texttt{the}$, $1{:}\ \texttt{team}$, a WORD flag followed by one index character replaces each word that is in the dictionary:

`CAP WORD 0 UPPER nasa WORD 1 met UPPER WORD 0 CAP WORD 1.`

The decoder first undoes the dictionary transform, then the capital conversion, and gets back the text exactly.

**Star encoding.** In the scheme of Kruse and Mukherjee, a word of length $k$ is replaced by a string of length $k$ made of `*` and a few letters, chosen from a dictionary that both sides share, so that the most frequent words of each length are mostly `*`. The transformed text has long stretches of `*`, which the compressor predicts well.

## Known algorithms

```pseudo id=main
CAP-ENCODE(x)
L1  out ← an empty string
L2  for each piece p of x, in order do          ▷ a maximal run of ASCII letters, or one other character
L3      if p is CAP, UPPER or ESC then append ESC and p to out
L4      else if |p| ≥ 2 and p is all upper case then append UPPER and lower(p) to out
L5      else if p[0] is upper case and p[1 ..] is lower case then append CAP and lower(p) to out
L6      else append p to out
L7  return out
```

The decoder reads the same pieces. After ESC it copies the next character; after CAP or UPPER it restores the case of the next word; any other piece it copies. The encoded word after a flag is the same maximal run as in the input, since changing the case keeps letters as letters, and the character after it is not a letter. So the decoder finds the same pieces, and the transform is one to one, also on texts that hold the flag characters. Both directions take linear time.

- **The Burrows-Wheeler transform** and its inverse, in $O(n)$ time with a [suffix array](/suffix-array/). It is the core of bzip2.
- **The bijective BWT**, in $O(n)$ time with the method of Bannai, Kärkkäinen, Köppl and Piątkowski (2021).
- **The [move-to-front transform](/move-to-front-transform/)**, a recoding that usually follows the BWT.
- **Star encoding** (Kruse and Mukherjee, 1998), **LIPT** (Awan and Mukherjee, 2001), and the **word replacement transform** (Skibiński, Grabowski and Deorowicz, 2005), all with a dictionary and linear-time encoding through a hash map.

## Bounds

- **No transform helps all texts.** The full map $x \mapsto C(\tau(x))$ is a lossless code, so by counting, it makes some inputs longer. A transform is chosen for a class of texts.
- **No gain in the limit of the best model.** If $\tau$ is computable and one to one, the Kolmogorov complexity can change by at most a constant: $K(x) \le K(\tau(x)) + c_\tau$, since a program for $\tau(x)$ followed by $\tau^{-1}$ gives $x$. A transform helps only a compressor whose model is weaker than the ideal one, which is every real compressor.
- **Permutations keep the order-0 entropy.** A permutation of $x$ has the same symbol counts, so a zero-order coder gains nothing from it; the gain comes from a coder that adapts to local statistics, such as MTF and an entropy coder after the BWT.

## Reductions

- **Text compression to compression of runs.** The BWT reduces the modeling of a text by its contexts to the coding of a string with long runs; see [run-length compression](/run-length-compression/).
- **Word-level modeling to symbol-level modeling.** A dictionary transform lets a compressor that models bytes, such as [PPM](/prediction-by-partial-matching/) or LZ77, see whole words as short units, which is close to giving it a word-level model.

## Applications

- **Preprocessing for text compressors.** Star encoding, LIPT and the word replacement transform were applied before bzip2, PPM and LZ-based compressors on English text.
- **Built into a format.** Brotli's static dictionary is used with a list of word transforms, which include upper case first and upper case all, so that one dictionary entry covers several forms of a word.
- **Executable compression.** The x86 call filter of xz and of other archivers is a reversible transform for machine code.
- **Block-sorting compressors.** bzip2 is a pipeline of reversible transforms (a run-length stage, the BWT, MTF, and a run-length code for zeros) followed by Huffman coding.

## References
