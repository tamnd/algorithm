---
tag: 3NN434
kind: algorithm
slug: prediction-by-partial-matching
name: Prediction by partial matching
aliases:
- PPM
area: compression-and-coding/entropy-coding
level: advanced
summary: Predicts each symbol from the longest context seen before and escapes to shorter contexts when the symbol is new there, coding symbols and escapes with an arithmetic coder.
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of symbols, k: the maximum order, m: the alphabet size}
  time: {worst: O(n k m), average: O(n k m), best: Θ(n k)}
  space: {extra: O(n k)}
properties: {deterministic: true, online: true, recursive: false, comparison: false}
history:
  year: 1984
  people: [John G. Cleary, Ian H. Witten]
  note: Cleary and Witten introduced PPM with the escape methods A and B. Moffat's PPMC (1990) and Shkarin's PPMd (2002) made it practical.
prereqs: [context-modeling, arithmetic-coding]
see_also: [adaptive-modeling, context-mixing, context-tree-weighting, burrows-wheeler-transform, suffix-tree, lzma, deflate]
sources:
  - paper: doi:10.1109/TCOM.1984.1096090
    title: John G. Cleary and Ian H. Witten, Data compression using adaptive coding and partial string matching, IEEE Transactions on Communications 32(4), 396-402, 1984
    locator: the method of partial string matching, the escape mechanism, the exclusion of symbols, and the methods A and B
  - paper: doi:10.1109/26.61469
    title: Alistair Moffat, Implementing the PPM data compression scheme, IEEE Transactions on Communications 38(11), 1917-1921, 1990
    locator: the escape method C, the data structure and the limit on memory
  - paper: doi:10.1109/DCC.1995.515495
    title: John G. Cleary, W. J. Teahan and Ian H. Witten, Unbounded length contexts for PPM, Data Compression Conference, 52-61, 1995
    locator: PPM* and its use of deterministic contexts of unbounded length
  - paper: doi:10.1109/DCC.2002.999958
    title: Dmitry Shkarin, PPM, one step to practicality, Data Compression Conference, 202-211, 2002
    locator: information inheritance and secondary escape estimation in PPMII, the basis of PPMd
  - book: isbn:9780139119910
    title: Timothy C. Bell, John G. Cleary and Ian H. Witten, Text Compression, Prentice Hall, 1990
    locator: the chapters on finite-context models, escapes and exclusion
---

Prediction by partial matching (PPM) is an adaptive [context model](/context-modeling/) for text and other data, coded with an [arithmetic coder](/arithmetic-coding/). To code a symbol, PPM looks at the longest context of up to $k$ preceding symbols that it has seen before. If the symbol has followed that context, PPM codes it with a probability from the counts of that context. If not, it codes an *escape* and tries the context one symbol shorter, down to an order-0 model and then a fixed uniform model. So PPM uses long contexts where they have data and short ones elsewhere, which answers the trade-off between prediction and dilution of context modeling. With exclusion and good escape estimates, PPM was the best practical text compressor from the late 1980s until [context mixing](/context-mixing/), and PPMd is still in common use.

## In plain words

To guess the next letter, PPM first looks at the last few letters, say "the", and checks what has followed "the" before. If the next letter is one of those, it is coded cheaply. If it is something new after "the", the coder sends a short "escape" signal and tries again with the shorter "he", then "e", then no context at all, and as a last step it picks among all letters equally.

Each escape costs bits, so the coder learns how often new letters appear in each context. When it falls back to a shorter context, it leaves out the letters it has just ruled out, since the letter cannot be one of them. Both the coder and the decoder keep the same tallies, so the decoder can follow the same steps.

## The problem

The input is a sequence $x_1 \ldots x_n$ over an alphabet of $m$ symbols, read once. The output is a bit string from which the decoder, knowing $n$, gets the sequence back. The goal is a code length close to $n H_k$, the empirical entropy of order $k$, with no model sent and no knowledge of the source.

## The algorithm

PPMC uses escape method C: in a context where the symbols not excluded have total count $n_C$ and $q$ distinct values, a symbol with count $c$ gets $c/(n_C + q)$ and the escape gets $q/(n_C + q)$.

```pseudo id=main
PPM-ENCODE(x_1 … x_n, k)
L1  for i ← 1 to n do
L2      E ← ∅, o ← min(k, i − 1)
L3      while o ≥ 0 do
L4          C ← the counts in the context x_{i−o} … x_{i−1}, without the symbols in E
L5          if C is empty then o ← o − 1, and go on with the next pass
L6          n_C ← the sum of C, q ← the number of symbols in C
L7          if x_i ∈ C then code x_i with probability C[x_i] / (n_C + q), and leave the loop
L8          code an escape with probability q / (n_C + q)
L9          E ← E ∪ (the symbols of C), o ← o − 1
L10     if o < 0 then code x_i with probability 1 / (m − |E|)
L11     add 1 to the count of x_i in the contexts of orders max(o, 0) to min(k, i − 1);
        halve the counts of a context, rounded up, when its total gets too large

PPM-DECODE(code, n, k)
L12 for i ← 1 to n do
L13     E ← ∅, o ← min(k, i − 1)
L14     while o ≥ 0 do: build C as in L4 to L6, skip it if empty; decode a target in n_C + q; if it is a symbol of C, output it and leave the loop; else E ← E ∪ C, o ← o − 1
L15     if o < 0 then decode a rank among the symbols not in E and output that symbol
L16     update the counts as in L11
```

**Exclusion.** When PPM escapes from a context, the symbol is none of the symbols of that context. Line L9 removes them from the counts of all shorter contexts for this symbol, so their probability goes to the symbols that are still possible. This *full exclusion* costs time but saves a few percent of the output on text.

**Update exclusion.** Line L11 adds the symbol only to the context where it was found and to the longer ones, not to the shorter ones. The counts of a short context then reflect the symbols that the longer contexts could not predict, which is what the short context is used for.

**Escape methods.** Method A gives the escape a count of 1, method B counts a symbol only from its second occurrence, method C gives the escape a count of $q$, and method D (Howard) counts each symbol as $c - \tfrac12$ and the escape as $q/2$. See [adaptive modeling](/adaptive-modeling/) for the formulas. Method C and D are better than A and B on text, because the number of distinct symbols seen in a context is a good guide to how often a new one appears.

## Example

Code `abracadabra` with $k = 2$ over the byte alphabet, $m = 256$. The events for each symbol are:

| symbol | context used | events and probabilities |
|---|---|---|
| a | none | order $-1$: $1/256$ |
| b | a (empty) | escape from order 0: $1/2$, order $-1$: $1/255$ |
| r | ab, b (empty) | escape from order 0: $2/4$, order $-1$: $1/254$ |
| a | br, r (empty) | order 0: $1/6$ |
| c | ra (empty) | escape from a: $1/2$, escape from order 0: $2/5$, order $-1$: $1/253$ |
| a | ac, c (empty) | order 0: $2/9$ |
| d | ca (empty) | escape from a: $1/2$, escape from order 0: $2/6$, order $-1$: $1/252$ |
| a | ad, d (empty) | order 0: $3/12$ |
| b | da (empty) | order 1, context a: $1/6$ |
| r | ab | order 2: $1/2$ |
| a | br | order 2: $1/2$ |

At the c, the context a has seen only b, so PPM escapes with $1/(1+1)$ and excludes b. The order-0 table then has a with count 2 and r with count 1, so $n_C = 3$, $q = 2$ and the escape is $2/5$. At the order $-1$ model, a, b and r are excluded, so c gets $1/253$. At the second b, the context a has seen b, c and d once each, so b gets $1/(3 + 3)$. The last two symbols are found in order-2 contexts with probability $\tfrac12$ each. The sum of the information is 58.2 bits, and the implementation writes 8 bytes.

## Correctness

Each event is a valid event of the arithmetic coder: in a context that is not skipped, the candidates and the escape have positive probabilities that sum to 1, and the symbol is never excluded, because a symbol is excluded only after an escape from a context that does not contain it. The decoder starts each symbol with the same tables and the same empty exclusion set, sees the same contexts because it has output the same symbols, and makes the same choices to skip; so it asks the arithmetic decoder for events with the same totals and gets back the same outcomes. The update depends only on what both sides know. The full proof is in [the correctness proof](#proof-correctness).

## Complexity

Model: [word RAM](/word-ram/).

- **Time.** For each symbol, PPM visits at most $k + 2$ contexts and scans the symbols of each. With a trie of contexts and lists of symbols, a symbol costs $O(k m)$ in the worst case and $O(k)$ when it is found in the longest context with few symbols. The implementation uses a dictionary of contexts and sorts the candidates, which adds a logarithmic factor.
- **Space.** Each symbol adds at most $k + 1$ counts, so the tables have $O(n k)$ entries. Real implementations bound the memory and restart or prune the model when it is full, as Moffat (1990) describes.
- **Code length.** The proof shows that the output is within $2$ bits plus less than $10^{-4}$ bits per event of the sum of $\lg(1/p)$ over the events. On 20000 symbols of a random order-2 Markov text over 8 letters, with an entropy rate of 2.16 bits per symbol, the implementation writes 3.00 bits per symbol with $k = 0$, 2.30 with $k = 2$ and 2.45 with $k = 3$; zlib at level 9 writes 3.01.

## Properties

- **Adaptive and one-pass.** No model is sent; the decoder rebuilds it.
- **Symmetric.** The decoder does the same work as the encoder, unlike LZ77 coders such as [Deflate](/deflate/), whose decoders are much faster.
- **Order matters.** A larger $k$ helps on long, repetitive data and hurts on short or random data, where most contexts are new and every symbol pays for escapes.

## Variants and improvements

- **PPMA, PPMB, PPMC, PPMD.** The same scheme with escape methods A to D.
- **PPM\*.** Cleary, Teahan and Witten (1995) allow contexts of any length. PPM\* uses the shortest *deterministic* context, one that has been followed by only one symbol, and the longest context otherwise, with the contexts kept in a trie of the text.
- **SEE.** Secondary escape estimation predicts the escape probability from a small set of features of the context, such as its order and its number of symbols, with an adaptive table, in place of a fixed formula. It appears in Bloom's PPMZ and in PPMd.
- **PPMd (PPMII).** Shkarin's PPM with information inheritance gives a new context the statistics of its shorter parent, which makes high orders learn fast, and uses SEE. PPMd is the PPM coder of the RAR format and of the 7z and ZIP formats.
- **Binary PPM and mixing.** Later coders break symbols into bits and combine the predictions of all orders with [context mixing](/context-mixing/) in place of escapes.

## When to use it

Use PPM for text and similar data when compression matters more than speed and the decoder can be as slow as the encoder. PPMd at order 4 to 8 compresses text better than LZ77 coders such as [LZMA](/lzma/) at a similar speed, but it decodes much more slowly than they do. For data with long repeats far apart, a dictionary coder finds them more cheaply. For the best ratio, context mixing compressors beat PPM at a much higher cost in time.

## Pitfalls

- **Zero totals.** All symbols of a context may be excluded. Such a context must be skipped with no escape coded; coding an escape with probability 1 wastes nothing but breaks a coder that expects a total above zero.
- **The order $-1$ model.** It must leave out the excluded symbols, or it gives them probability that can never be used.
- **Count overflow.** The totals must stay within the precision of the arithmetic coder. Halve the counts of a context when its total gets too large.
- **Memory.** The number of contexts grows with the input. A real implementation needs a memory limit and a policy for when it is reached.

## Implementations

## History

Cleary and Witten introduced PPM in 1984, with the escape methods A and B and the exclusion of symbols. Moffat's 1990 implementation, PPMC, added method C, a compact data structure and a bound on memory, and it set the standard for text compression. Howard's thesis of 1993 gave method D. In 1995 Cleary, Teahan and Witten removed the bound on the order with PPM\*. Charles Bloom's PPMZ added secondary escape estimation, and in 2002 Shkarin published PPMII, the algorithm of the PPMd program, which made PPM fast and strong enough for general archivers.

## References
