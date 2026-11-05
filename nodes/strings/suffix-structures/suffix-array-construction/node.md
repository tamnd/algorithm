---
tag: JTQK8V
kind: problem
slug: suffix-array-construction
name: Suffix array construction
aliases:
- suffix sorting
area: strings/suffix-structures
level: core
summary: Sort all suffixes of a string, in time n log n or linear time.
prereqs: [suffix-array, sorting-problem]
see_also: [manber-myers-algorithm, sa-is, dc3-skew-algorithm, prefix-doubling, larsson-sadakane-algorithm, suffix-tree-construction, lcp-array-construction, burrows-wheeler-transform]
sources:
  - paper: doi:10.1145/1242471.1242472
    title: Simon J. Puglisi, W. F. Smyth and Andrew H. Turpin, A taxonomy of suffix array construction algorithms, ACM Computing Surveys 39(2), 2007
    locator: article 4; the classification into prefix doubling, recursive and induced copying methods, and the experiments
  - paper: doi:10.1137/0222058
    title: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5), 1993
    locator: pages 935 to 948; the O(N log N) sorting by doubling
  - paper: doi:10.1145/1217856.1217858
    title: Juha Kärkkäinen, Peter Sanders and Stefan Burkhardt, Linear work suffix array construction, Journal of the ACM 53(6), 2006
    locator: pages 918 to 936; the skew algorithm DC3 and the difference cover generalization
  - paper: doi:10.1109/TC.2010.188
    title: Ge Nong, Sen Zhang and Wai Hong Chan, Two efficient algorithms for linear time suffix array construction, IEEE Transactions on Computers 60(10), 2011
    locator: pages 1471 to 1484; SA-IS and SA-DS
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.5, Suffix arrays
---

Suffix array construction, or suffix sorting, is the problem of computing the [suffix array](/suffix-array/) of a string: the start positions of its [suffixes](/suffix/) in lexicographic order. Comparing whole suffixes is slow, because suffixes are long and overlap, and the problem is to use this overlap. Over a general ordered alphabet it needs and admits $\Theta(n \log n)$ comparisons; over an integer alphabet it is solvable in $\Theta(n)$ time by [SA-IS](/sa-is/) and [DC3](/dc3-skew-algorithm/). It is the first step of the [Burrows-Wheeler transform](/burrows-wheeler-transform/), of the [FM-index](/fm-index/), and of most text indexes in practice.

## In plain words

Take all endings of a text, from the whole text down to its last letter, and put them in dictionary order. The answer is the list of the places where the sorted endings start.

A plain sort works, but it is slow: the endings of a long text are long, and comparing two of them can read most of the text. The endings are not independent, though. Each ending is one letter followed by the next ending. So the order of the long endings follows from the order of shorter ones, and good algorithms use this to sort all endings with little more work than reading the text.

## Definition

**Input.** A string $S = S[0 \ldots n-1]$, $n \ge 0$, over an alphabet $\Sigma$ with a total order. Indices are 0-based. Three alphabet models are common:

- **general ordered alphabet:** symbols can only be compared, at unit cost;
- **integer alphabet:** $\Sigma \subseteq \{0, 1, \ldots, n^c\}$ for a constant $c$, so symbols can index arrays and be sorted by [radix sort](/radix-sort/) in $O(n)$ time;
- **constant alphabet:** $|\Sigma| = O(1)$, such as DNA or bytes.

**Output.** The permutation $SA$ of $\{0, \ldots, n-1\}$ with $S_{SA[0]} < S_{SA[1]} < \cdots < S_{SA[n-1]}$, where $S_i = S[i \ldots n-1]$ and $<$ is the [lexicographic order](/lexicographic-order/) in which a proper prefix is smaller. The output is unique because different suffixes are different strings.

Many programs instead sort the suffixes of $S\$$, with a [sentinel](/sentinel-character/) $\$$ smaller than all symbols. The output then is $n$ followed by the suffix array of $S$, so the two versions are equivalent.

## Variants

- **With the LCP array.** Output also $LCP[r]$, the length of the longest common prefix of the suffixes of ranks $r - 1$ and $r$. Some constructions produce it as a by-product; otherwise [LCP array construction](/lcp-array-construction/) computes it in $O(n)$ time from $S$ and $SA$.
- **Inverse suffix array.** Output $rank = SA^{-1}$, which [prefix doubling](/prefix-doubling/) produces directly.
- **Burrows-Wheeler transform.** Output only $BWT[r] = S\$[SA[r] - 1]$. This can be done in less working space than a full suffix array.
- **Circular suffix array.** Sort the rotations instead of the suffixes: the [circular suffix array](/circular-suffix-array/).
- **Generalized suffix array.** Sort the suffixes of a set of strings, each with its own end marker.
- **Sparse suffix sorting.** Sort only the suffixes that start at $b$ given positions, in less than $\Theta(n)$ space.
- **External memory and parallel construction.** Build arrays larger than the main memory, with the cost counted in block transfers, or on many processors. DC3 was designed to fit these models.

## Examples

| $S$ | $SA$ |
|---|---|
| banana | 5 3 1 0 4 2 |
| mississippi | 10 7 4 1 0 9 8 6 3 5 2 |
| abracadabra | 10 7 0 3 5 8 1 4 6 9 2 |
| aaaaa | 4 3 2 1 0 |
| ababab | 4 2 0 5 3 1 |
| (the empty string) | (the empty array) |

For mississippi, the first four sorted suffixes are i, ippi, issippi and ississippi, at positions 10, 7, 4 and 1. With a sentinel, the array of $\texttt{mississippi\$}$ is $11$ followed by the row above, and the Burrows-Wheeler transform read from it is $\texttt{ipssm\$pissii}$.

The examples $\texttt{a}^n$ and $(\texttt{ab})^{n/2}$ are the hard cases for simple methods: two neighboring suffixes share a prefix of length up to $n - 2$, so a sort that compares suffixes symbol by symbol reads $\Theta(n)$ symbols for each comparison.

## Known algorithms

| algorithm | time | alphabet | notes |
|---|---|---|---|
| sort with full suffix comparisons | $O(n^2 \log n)$ worst | general | $O(n \log^2 n)$ expected on random texts; a test oracle |
| [Karp-Miller-Rosenberg](/karp-miller-rosenberg-algorithm/) naming | $O(n \log n)$ | general | the origin of doubling |
| [Prefix doubling](/prefix-doubling/) with a comparison sort | $O(n \log^2 n)$ | general | simple, the CLRS method |
| [Manber-Myers](/manber-myers-algorithm/) | $O(n \log n)$ | general | doubling with bucket sorts |
| [Larsson-Sadakane](/larsson-sadakane-algorithm/) | $O(n \log n)$ | general | doubling that skips sorted groups |
| [DC3 (skew)](/dc3-skew-algorithm/) | $O(n)$ | integer | recursion on two thirds of the suffixes |
| [SA-IS](/sa-is/) | $O(n)$ | integer | induced sorting, fast in practice |
| via a [suffix tree](/suffix-tree/) | $O(n)$ for a constant alphabet; $O(n)$ for an integer alphabet with [Farach's algorithm](/farach-algorithm/) | | a depth-first walk with children in order |

The linear-time algorithms DC3, the algorithm of Ko and Aluru and the algorithm of Kim, Sim, Park and Park appeared in 2003. SA-IS (2009) and programs based on induced sorting or induced copying, such as libdivsufsort, are among the fastest in practice. The survey of Puglisi, Smyth and Turpin compares the methods of that time.

## Bounds

- **Upper bound, integer alphabet.** $O(n)$ time in the worst case on a word RAM, by DC3 or SA-IS. This is optimal, since the output has $n$ entries.
- **Upper bound, general ordered alphabet.** $O(n \log n)$ comparisons and time: sort the symbols in $O(n \log n)$ time, replace them by their ranks in $\{0, \ldots, n-1\}$, and run a linear-time integer algorithm. Manber-Myers reaches the same bound directly.
- **Lower bound, general ordered alphabet.** $\Omega(n \log n)$ comparisons in the worst case, in the [comparison model](/comparison-model/). If the $n$ symbols are pairwise distinct, the order of the suffixes is the order of their first symbols, so the suffix array sorts the symbols, and [sorting](/sorting-problem/) $n$ distinct items needs $\lceil \lg n! \rceil$ comparisons.
- **Space.** The output takes $n$ words. Beyond the input and the output, SA-IS needs one bit for each symbol for the types, $O(\sigma)$ words for the bucket pointers of an alphabet of size $\sigma$, and space for the recursion, which Nong, Zhang and Chan keep inside the output array.

## Reductions

- **Sorting to suffix sorting.** As in the lower bound: $n$ distinct keys, written as a string, are sorted by its suffix array. The reduction costs $O(n)$.
- **Suffix sorting to suffix tree construction.** A depth-first walk of the [suffix tree](/suffix-tree/) of $S\$$ that visits children in the order of their first symbols lists the leaves in suffix array order, in $O(n)$ time.
- **Suffix tree construction to suffix sorting.** From $SA$ and the LCP array, a stack-based scan builds the suffix tree in $O(n)$ time. See [suffix tree from suffix array](/suffix-tree-from-suffix-array/). So the two problems have the same complexity up to $O(n)$.
- **Suffix sorting to string sorting.** Sorting the $n$ suffixes with a general [string sort](/string-sorting/) is correct, but the total length of the suffixes is $n(n+1)/2$, so this reduction is not efficient for repetitive texts.

## Applications

- **Text indexes.** The [suffix array](/suffix-array/), the [enhanced suffix array](/enhanced-suffix-array/), the [FM-index](/fm-index/) and the [compressed suffix array](/compressed-suffix-array/) all start from the suffix array.
- **Compression.** The [Burrows-Wheeler transform](/burrows-wheeler-transform/) of bzip2 is read off the suffix array, and [Lempel-Ziv factorization](/lempel-ziv-factorization/) can be computed from it.
- **Bioinformatics.** Read aligners index a reference genome with an FM-index built from its suffix array.
- **String problems.** With the LCP array, the [longest repeated substring](/longest-repeated-substring/), the [number of distinct substrings](/count-distinct-substrings/), [maximal repeats](/maximal-repeats/) and [shortest unique substrings](/shortest-unique-substring/) follow by linear scans.

## References
