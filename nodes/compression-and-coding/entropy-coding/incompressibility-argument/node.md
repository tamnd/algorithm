---
tag: DZF65X
kind: theorem
slug: incompressibility-argument
name: Incompressibility argument
aliases:
- counting argument for compression
area: compression-and-coding/entropy-coding
level: intro
summary: No lossless compressor shortens every input; fewer than 2^(1-c) of the n-bit strings shrink by c bits. With Kolmogorov complexity this proves lower bounds by the incompressibility method.
prereqs: [pigeonhole-principle]
see_also: [incompressibility-method, kolmogorov-complexity, counting-argument, information-theoretic-bound, comparison-sort-lower-bound, lossless-compression, source-coding-theorem, kraft-inequality]
sources:
  - book: isbn:9783030112974
    title: Ming Li and Paul Vitanyi, An Introduction to Kolmogorov Complexity and Its Applications, fourth edition, Springer, 2019
    locator: Chapter 2 (the count of incompressible strings) and Chapter 6 (The incompressibility method)
  - url: https://arxiv.org/abs/0905.4452
    title: Paul Vitanyi, Analysis of sorting algorithms by Kolmogorov complexity (a survey), arXiv 0905.4452, 2009
    locator: Section 2 (the average-case analysis of Bubblesort by incompressibility) and Lemma 1 (most strings are incompressible relative to any fixed side information)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 14 (Kolmogorov complexity, and the bound on the number of strings with low complexity)
---

The incompressibility argument is the simple count that limits every lossless compressor: there are $2^n$ binary strings of length $n$ but only $2^n - 1$ strings that are shorter, so no one-to-one map can shorten them all. More strongly, fewer than a $2^{1-c}$ fraction of the strings of length $n$ can be shortened by $c$ bits or more. So no compressor works on all data, random data does not compress, and applying a compressor again to its own output cannot keep gaining. The same count, applied to the shortest programs that print a string ([Kolmogorov complexity](/kolmogorov-complexity/)), gives the [incompressibility method](/incompressibility-method/): a way to prove lower bounds by showing that a bad case for an algorithm would give a short description of a string that has none.

## Statement

Notation. Strings are binary. $\{0, 1\}^n$ is the set of the $2^n$ strings of length $n$, and $\{0, 1\}^{<n}$ is the set of the $2^n - 1$ strings of length less than $n$, the empty string included. A *lossless compressor* is a one-to-one map $f : \{0, 1\}^* \to \{0, 1\}^*$ (one-to-one is exactly what lets a decompressor recover the input). The model is the worst case: there is no probability law on the inputs. In part (d), $C(x)$ is the plain Kolmogorov complexity of $x$, the length of a shortest program for a fixed universal machine that prints $x$, and $C(x \mid y)$ is the same when the program also gets $y$.

**Theorem.**

- **(a)** For every $n \ge 0$ and every one-to-one $f$, some $x \in \{0, 1\}^n$ has $|f(x)| \ge n$.
- **(b)** For $1 \le c \le n$, at most $2^{n - c + 1} - 1$ strings $x \in \{0, 1\}^n$ have $|f(x)| \le n - c$, that is, a fraction less than $2^{1 - c}$. The bound is reached by some $f$.
- **(c)** If the images $f(x)$, for $x \in \{0, 1\}^n$, form a prefix-free set (as when outputs are concatenated without lengths), then at most $2^{n - c}$ of the strings $x \in \{0, 1\}^n$ have $|f(x)| \le n - c$, a fraction at most $2^{-c}$.
- **(d) Incompressible strings.** For every $n$, every $c \ge 0$ and every string $y$, at least $2^n - 2^{n - c} + 1$ strings $x \in \{0, 1\}^n$ have $C(x \mid y) \ge n - c$. In particular, some $x \in \{0, 1\}^n$ has $C(x \mid y) \ge n$.

## In plain words

Take all the files of a given size. There are fewer smaller files than files of this size, so no program can make every file smaller without giving two files the same smaller form, and then it could not undo the change. Each extra bit we want to save halves the number of files that can be shrunk that much. So almost all files can be shrunk only a little, and a file of random bits is almost never shrunk at all. A compressor works on real data only because real data is not random: it has patterns, and the compressor bets on them. The same idea gives a way to prove that some tasks are hard on most inputs: if an algorithm were fast on a typical input, we could use its run to describe that input in fewer bits than any typical input needs.

## Proof

(a) The strings of length less than $n$ number $\sum_{m=0}^{n-1} 2^m = 2^n - 1$. If $|f(x)| < n$ for all $2^n$ strings $x \in \{0, 1\}^n$, then $f$ maps a set of $2^n$ elements into a set of $2^n - 1$ elements, and by the [pigeonhole principle](/pigeonhole-principle/) two inputs get the same output. That contradicts one-to-one. $\square$

(b) The strings of length at most $n - c$ number $2^{n - c + 1} - 1$. A one-to-one $f$ maps different inputs to different outputs, so at most that many inputs can have outputs of length at most $n - c$. To reach the bound, list $\{0, 1\}^n$ in any order and map the $i$-th string to the $i$-th string in the order of increasing length; this map is one-to-one on $\{0, 1\}^n$ and extends to a one-to-one map on all strings. $\square$

(c) A prefix-free set of binary strings has at most $2^m$ strings of length at most $m$: by the [Kraft inequality](/kraft-inequality/), $\sum 2^{-|w|} \le 1$, and each word of length at most $m$ adds at least $2^{-m}$. Take $m = n - c$. $\square$

(d) Fix $y$. Each $x$ with $C(x \mid y) < n - c$ has a program of length less than $n - c$, and different strings $x$ have different shortest programs, since a program prints only one string. There are at most $2^{n-c} - 1$ programs of length less than $n - c$, so at most $2^{n - c} - 1$ strings of length $n$ have $C(x \mid y) < n - c$. The rest, at least $2^n - 2^{n - c} + 1$, have $C(x \mid y) \ge n - c$. For $c = 0$ this is at least 1 string. $\square$

**The incompressibility method.** The [incompressibility method](/incompressibility-method/) page treats the method in general. In short, to prove that an algorithm $A$ needs many steps on most inputs:

1. Fix an input $x$ of length $n$ with $C(x \mid n, A) \ge n - c$. By (d), all but a $2^{-c}$ fraction of the inputs are like this.
2. Assume that $A$ runs fast on $x$.
3. Use the run of $A$ on $x$ to write a program that prints $x$, given $n$ and $A$, with fewer than $n - c$ bits.
4. This contradicts step 1. So $A$ is slow on all inputs except a $2^{-c}$ fraction, and slow on average.

**Example: sorting by comparisons** (Li and Vitanyi, Chapter 6, where the method is used for sorting and many other problems; Vitanyi's survey, Section 2, applies it to Bubblesort in the same way). Let $A$ be a deterministic comparison sort and $\pi$ a permutation of $\{1, \ldots, n\}$. Write down the outcomes of the comparisons that $A$ makes on input $\pi$, one bit each; say there are $t(\pi)$ of them. Given $n$ and $A$, this bit string determines $\pi$: run $A$ and answer each comparison from the next bit. Two different permutations cannot give the same bits, because $A$ would then move their items in the same way and leave one of them unsorted. The decoder knows when $A$ stops, so it also knows where the bit string ends, and so the strings for different $\pi$ form a prefix-free set. By the argument of (c), at most $2^{m}$ permutations have $t(\pi) \le m$. Take $m = \log_2 n! - c$: all but a $2^{-c}$ fraction of the permutations need more than $\log_2 n! - c$ comparisons, and so the average is at least $\log_2 n! - O(1) = n \log_2 n - O(n)$. In the words of the method, a permutation $\pi$ with $K(\pi \mid n, A) \ge \log_2 n! - c$ (prefix complexity) needs $t(\pi) \ge \log_2 n! - c - O(1)$ comparisons, since the outcome bits plus a constant-size decoder describe it. This is the average-case form of the [comparison sort lower bound](/comparison-sort-lower-bound/).

## Consequences

- **No universal compressor.** Every lossless compressor makes some inputs longer, or at least not shorter. A practical format adds one flag bit and stores an input raw when compression does not help, so its worst-case growth is small, but never zero.
- **No repeated gain.** Running a compressor on its own output is again a one-to-one map, so the count applies again. Claims of a compressor that shrinks every file, or that shrinks any file down to a fixed size by repeated passes, are false by (a).
- **Random data does not compress.** If the input is uniform on $\{0, 1\}^n$, the mean output length of any lossless compressor whose outputs are prefix-free is at least $n$, by the [source coding theorem](/source-coding-theorem/) with $H = n$; by (b), only a small fraction of inputs shrink by more than a few bits.
- **Lower bounds by incompressibility.** Average-case lower bounds for sorting algorithms such as Bubblesort, Heapsort and Shellsort, and lower bounds in routing and in formal language theory, are proved this way (Li and Vitanyi, Chapter 6). The proofs work with one fixed incompressible input, so they avoid an explicit probability calculation.
- **Information-theoretic bounds.** The [information-theoretic bound](/information-theoretic-bound/) on data structures and the [counting argument](/counting-argument/) for circuits are the same count in other settings.

## Tightness

**Exhaustive check for small $n$.** The code on this page searches all partial one-to-one maps from $\{0, 1\}^n$ into $\{0, 1\}^{<n}$ by backtracking. It visits 2, 16 and 13700 partial maps for $n = 1, 2, 3$ and finds no complete one, as (a) predicts. It also enumerates every one-to-one map from $\{0, 1\}^n$ into the strings of length at most $n$, for $n = 1$ and $n = 2$, and checks the counts of (b) on each. The map that sends the strings in order to the shortest strings first reaches the bound of (b) exactly for every $c$.

**A real compressor on random bytes.** zlib at level 9 on random bytes (Python's `random` with seed 2):

| input bytes | output bytes |
|---|---|
| 0 | 8 |
| 1 | 9 |
| 100 | 111 |
| 1000 | 1011 |
| 10000 | 10011 |

Each output is longer than its input: zlib finds no pattern and stores the data in raw blocks, plus a header, block headers and a checksum. The same compressor turns 10000 zero bytes into 33 bytes. A compressor wins on some inputs only by losing on others.

**The constants.** Part (b) is exact, not only up to a constant: the greedy map reaches $2^{n-c+1} - 1$. For a prefix-free set of outputs, $2^{n-c}$ is reached by $\{0, 1\}^{n-c}$ itself. In part (d) the constant $c$ can be any number, but the fraction $2^{-c}$ of compressible strings does not depend on $n$; a statement like "$C(x) \ge n - c$" for a fixed $c$ thus holds for most, but never all, strings.

**What the count does not say.** It does not say which strings are compressible, and it cannot: $C(x)$ is not computable. It also does not bound compression under a model. A source with entropy $H$ per symbol is compressible to about $H$ bits per symbol, which is a statement about an average under a law, not about all strings.

## History

The counting argument is folklore and follows from the pigeonhole principle. Kolmogorov complexity was introduced by Solomonoff (1964), Kolmogorov (1965) and Chaitin (1966); from the start it was known that most strings are incompressible, by the count above. The use of incompressible inputs to prove lower bounds on algorithms grew from about 1980, for example in work by Paul, Seiferas and Simon on on-line computation, and Li and Vitanyi made it a general tool, the incompressibility method, in their book. The 4th edition (2019) treats it in Chapter 6.

## References
