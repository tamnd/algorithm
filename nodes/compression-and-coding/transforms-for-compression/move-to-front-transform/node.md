---
tag: HBY4JR
kind: algorithm
slug: move-to-front-transform
name: Move-to-front transform
aliases:
- MTF transform
- move-to-front coding
- book stack transform
area: compression-and-coding/transforms-for-compression
level: core
summary: Replace each symbol by its index in a list of the alphabet, then move it to the front. Symbols used recently get small numbers, so local repetition becomes many zeros.
model: word-ram
complexity:
  vars: {n: the length of the input, σ: the size of the alphabet, S: the sum of the output values}
  time: {worst: Θ(n σ), output_sensitive: O(n + S), with_tree: "O(n log(n + σ))"}
  space: {extra: Θ(σ)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1980
  people: [Boris Ryabko, Jon Bentley, Daniel Sleator, Robert Tarjan, Victor Wei, Peter Elias]
  note: Ryabko described the book stack code in 1980. Bentley, Sleator, Tarjan and Wei published the move-to-front compression scheme in 1986, and Elias studied recency rank coding in 1987.
prereqs: [self-organizing-list, lossless-compression]
see_also: [move-to-front-heuristic, list-update-problem, burrows-wheeler-transform, locality-recoding, run-length-encoding, elias-delta-coding, huffman-coding, adaptive-modeling]
sources:
  - paper: doi:10.1145/5684.5688
    title: Jon Louis Bentley, Daniel D. Sleator, Robert E. Tarjan and Victor K. Wei, A locally adaptive data compression scheme, Communications of the ACM 29(4), 1986
    locator: pages 320 to 330 (the move-to-front scheme, and bounds on its output length in terms of the frequencies of the symbols)
  - paper: doi:10.1109/TIT.1987.1057262
    title: Peter Elias, Interval and recency rank source coding, two on-line adaptive variable-length schemes, IEEE Transactions on Information Theory 33(1), 1987
    locator: pages 3 to 10 (recency rank coding, which is the move-to-front transform, and interval coding)
  - paper: "Michael Burrows and David J. Wheeler, A block-sorting lossless data compression algorithm, SRC Research Report 124, Digital Equipment Corporation, Palo Alto, California, 1994"
    title: Burrows and Wheeler 1994
    locator: Section 3 (move-to-front coding of the output of the transform)
  - book: isbn:9781848829022
    title: David Salomon and Giovanni Motta, Handbook of Data Compression, 5th edition, Springer, 2010
    locator: Chapter 1, Basic Techniques, the section on move-to-front coding (section number not checked)
---

The move-to-front transform (MTF) replaces each symbol of a sequence by its current index in a list of the alphabet, and then moves that symbol to the front of the list. A symbol that was used a short time ago is near the front, so it gets a small number, and a run of equal symbols becomes one number followed by zeros. The decoder keeps the same list and undoes each step, so the transform is lossless. MTF does not compress by itself; it turns local repetition into a skewed distribution of small integers that an entropy coder such as [Huffman coding](/huffman-coding/) compresses well. It is the second stage of the classic [Burrows-Wheeler](/burrows-wheeler-transform/) compressor.

## In plain words

Keep all possible symbols in a row, like books in a stack. To send a symbol, say how far down the stack it is, then take it out and put it on top. If you send the same symbol again soon, it is still near the top, so the number is small. If you send it many times in a row, every number after the first is zero.

The receiver keeps its own stack in the same order. It reads a number, takes the book at that place, writes down its name, and puts it on top. Both stacks change in the same way, so the receiver always gets the right symbol back.

The numbers are not shorter than the symbols. They are just more often small, which a later coder can use.

## The problem

**Input.** A sequence $X = X[0 \ldots n-1]$ over an alphabet $\Sigma$ of $\sigma$ symbols, and an initial order $A[0 \ldots \sigma-1]$ of $\Sigma$ that the encoder and the decoder agree on (for bytes, usually $0, 1, \ldots, 255$).

**Output.** A sequence $Y[0 \ldots n-1]$ of integers in $\{0, \ldots, \sigma - 1\}$, where $Y[i]$ is the *recency rank* of $X[i]$: the index of $X[i]$ in the list, which equals the number of distinct symbols used since the last use of $X[i]$ (with the initial order seen as an earlier use of the symbols, $A[0]$ last).

## The algorithm

```pseudo id=main
MTF-ENCODE(X[0 .. n − 1], A[0 .. σ − 1])        ▷ the list starts as a copy of A
L1  for i ← 0 to n − 1 do
L2      r ← the index of X[i] in the list
L3      Y[i] ← r
L4      move the symbol at index r to the front of the list
L5  return Y
```

The decoder is the same loop with line L2 read the other way:

```pseudo id=decode
MTF-DECODE(Y[0 .. n − 1], A[0 .. σ − 1])        ▷ the list starts as a copy of A
D1  for i ← 0 to n − 1 do
D2      X[i] ← the symbol at index Y[i] of the list
D3      move the symbol at index Y[i] to the front of the list
D4  return X
```

With the list in an array, line L2 is a linear scan and line L4 shifts $r$ entries one place, so both cost $O(r + 1)$.

## Example

Encode `bananaaa` with the initial list $a, b, c, \ldots, z$.

| symbol | index | list after the move (first four) |
|---|---|---|
| b | 1 | b a c d |
| a | 1 | a b c d |
| n | 13 | n a b c |
| a | 1 | a n b c |
| n | 1 | n a b c |
| a | 1 | a n b c |
| a | 0 | a n b c |
| a | 0 | a n b c |

The output is $1, 1, 13, 1, 1, 1, 0, 0$. The alternation of `a` and `n` gives ones, and the final run of `a` gives zeros.

**After the BWT.** The [BWT](/burrows-wheeler-transform/) of `abracadabra` is $\texttt{ard\$rcaaaabb}$. With the initial list $\$, a, b, c, d, r$, MTF gives $1, 5, 5, 3, 2, 5, 4, 0, 0, 0, 5, 0$: the run `aaaa` becomes $4, 0, 0, 0$. MTF on the text `abracadabra$` itself, with the same list, gives $1, 2, 5, 2, 4, 1, 5, 1, 4, 4, 2, 5$, with no zero. On longer texts the effect is larger, because the BWT output has long runs.

## Correctness

The decoder inverts the encoder because both keep the same list. Invariant: before step $i$, the decoder's list equals the encoder's list. It holds at the start, since both lists are copies of $A$. At step $i$ the encoder outputs the index $r$ of $X[i]$, so the decoder's symbol at index $r$ is $X[i]$, and both lists then make the same move. The output is the recency rank: the list is always ordered by the time of the last use, with the most recent first, so the symbols in front of $X[i]$ are exactly the distinct symbols used after the last use of $X[i]$. The full proof is below, together with the proof of the bound that follows.

**Length bound.** Let $H_0$ be the empirical entropy of order 0 of $X$, and code each output $r$ with the [Elias delta code](/elias-delta-coding/) of $r + 1$, which has at most $f(r+1)$ bits with $f(x) = 1 + \log_2 x + 2 \log_2(1 + \log_2 x)$. Then the total length is at most

$$n\,\bigl(1 + H_0 + 2 \log_2(1 + H_0)\bigr) + \sigma f(\sigma) \text{ bits}.$$

The reason: between two uses of a symbol $x$ that are $g$ positions apart, at most $g - 1$ distinct symbols occur, so the rank is less than $g$; the gaps of $x$ add up to at most $n$, and $f$ is concave, so Jensen's inequality gives $n_x f(n / n_x)$ for the $n_x$ uses of $x$. Bentley, Sleator, Tarjan and Wei prove a bound of this form in 1986. MTF can do much better than $H_0$: on $a^{100} b^{100} c^{100}$, $H_0 = \log_2 3$ bits per symbol, but MTF outputs only two nonzero values after the first.

## Complexity

- **Array list.** Each step costs $O(r + 1)$ for the output $r$, so the total is $O(n + \sum_i Y[i])$, and $\Theta(n \sigma)$ in the worst case, for example when the input cycles through all $\sigma$ symbols. For bytes, $\sigma = 256$, and the inputs after a BWT have mostly small ranks, so a plain array is the usual choice.
- **A tree over time.** Mark, for each symbol, the time of its last use in a Fenwick tree over the times $0 \ldots n + \sigma - 1$. The rank of $X[i]$ is the number of marks after its last use, one prefix sum. Each step makes one query and two updates, so the time is $O(n \log(n + \sigma))$, which helps when $\sigma$ is large.
- **Space.** $\Theta(\sigma)$ for the list.

## Properties

- **Online and lossless.** Each output depends only on the earlier inputs, and the decoder works symbol by symbol.
- **Locally adaptive.** The cost of a symbol depends on the time since its last use, not on its overall frequency. A symbol that is frequent in one part of the input and absent in another is cheap in the part where it is frequent.
- **Runs become zeros.** A run of $k$ copies of a symbol gives one rank followed by $k - 1$ zeros, so MTF is often followed by a [run-length](/run-length-encoding/) step for the zeros.
- **Related to list update.** The same rule, as the [move-to-front heuristic](/move-to-front-heuristic/) of a [self-organizing list](/self-organizing-list/), is a strategy for the [list update problem](/list-update-problem/), where the cost of an access is its position. Here the position is the output.

## Variants and improvements

- **Moves that are not to the front.** MTF-1 and MTF-2 of Balkenhol, Kurtz and Shtarkov (DCC 1999) move a symbol to index 1 in some cases instead of to index 0, so one symbol that occurs once does not push the current run symbol away.
- **Ordering by counts.** Weighted frequency count and similar second-step methods (surveyed by Deorowicz, 2002) order the list by recent counts instead of by the last use.
- **Inversion frequencies and distance coding.** Inversion frequencies (Arnavut and Magliveras, DCC 1997) code, for each symbol in turn, the number of larger symbols between its uses. Interval coding (Elias, 1987) codes the gap itself. Both are alternatives to MTF after the BWT; see [recoding for locality](/locality-recoding/).
- **bzip2.** bzip2 applies MTF to the BWT output, then codes the runs of zeros with two symbols (RUNA and RUNB), and then applies Huffman coding.

## When to use it

Use MTF after a transform that makes runs or local repetition, chiefly the BWT, and before an entropy coder. Do not use it on data that has no locality: on a random sequence the ranks are as random as the input, and the transform only costs time. Do not use it alone as a compressor, since its output has the same length as its input.

## Pitfalls

- **Different initial lists.** The encoder and the decoder must start from the same list. A difference in one place changes every later symbol.
- **Index from 0 or from 1.** The output for the front symbol is 0 here. Codes for positive integers, such as Elias codes, need $r + 1$.
- **Updating before the output.** Line L3 must use the index from before the move. If the move comes first, every output is 0.
- **Large alphabets.** With $\sigma$ in the thousands and little locality, the array list makes each step slow; use the tree method.
- **Expecting compression from MTF alone.** The output has $n$ values of $\lceil \log_2 \sigma \rceil$ bits each; the gain comes only from the coder after it.

## Implementations

## History

Ryabko published the idea as the "book stack" code in 1980, in Problems of Information Transmission. Bentley, Sleator, Tarjan and Wei published the move-to-front compression scheme independently in Communications of the ACM in 1986, with bounds on its output in terms of the symbol frequencies. Elias (1987) studied the same recency rank code together with interval coding. Burrows and Wheeler (1994) used MTF as the second stage of their block-sorting compressor, and bzip2 (1996) made the combination widely used.

## References
