---
tag: BBQNVE
kind: abstract-type
slug: static-sequence
name: Static indexable sequence
aliases:
- indexable sequence
area: data-structures/succinct-structures
level: advanced
summary: An immutable sequence over an alphabet supporting access, rank and select for each symbol.
prereqs: [rank-select-problem]
see_also: [wavelet-tree, wavelet-matrix, rank-select-dictionary, fm-index, burrows-wheeler-transform, range-kth-smallest-query, compressed-data-structure, document-listing]
sources:
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 6 (Sequences), Sections 6.1 (Using Permutations) and 6.2 (Wavelet Trees)
  - paper: doi:10.1145/1109557.1109599
    title: Alexander Golynski, J. Ian Munro and S. Srinivasa Rao, Rank/select operations on large alphabets, a tool for text indexing, Seventeenth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 2006), 368-373
    locator: the representation of a sequence in n lg σ + o(n lg σ) bits with select in O(1) time and access and rank in O(lg lg σ) time
  - paper: doi:10.1145/2629339
    title: Djamal Belazzougui and Gonzalo Navarro, Optimal lower and upper bounds for representing sequences, ACM Transactions on Algorithms 11(4), Article 31, 2015
    locator: the lower bound Ω(lg(lg σ / lg w)) for rank and the matching compressed representation
---

A static indexable sequence is an abstract data type that holds a fixed string $S[0 \ldots n-1]$ over an alphabet $\Sigma = \{0, \ldots, \sigma - 1\}$ and answers three queries: `access(i)`, the symbol $S[i]$; `rank(c, i)`, the number of occurrences of $c$ in $S[0 \ldots i-1]$; and `select(c, j)`, the position of the $j$-th occurrence of $c$. It is the [rank and select problem](/rank-select-problem/) lifted from bits to symbols. Solutions range from $\sigma$ bit vectors, with $O(1)$ time and about $\sigma n$ bits, to the [wavelet tree](/wavelet-tree/) and the [wavelet matrix](/wavelet-matrix/), with $O(\lg \sigma)$ time and $n \lg \sigma + o(n \lg \sigma)$ bits. The [FM-index](/fm-index/) is a static sequence on the [Burrows-Wheeler transform](/burrows-wheeler-transform/) of a text.

## In plain words

Think of a long string of letters that will never change. You want to ask three kinds of questions about it. What is the letter at a given place? How many times does a given letter appear before a given place? Where is the tenth appearance of a given letter?

For a string of only two letters, 0 and 1, these are the questions that rank and select answer on a row of bits. For a larger alphabet, you could keep one row of bits for each letter, but that takes much more space than the string. The data types on this page answer the same questions using about the same space as the string itself, or less if the string is compressible.

## Operations

Let $S[0 \ldots n-1]$ be a string over $\Sigma = \{0, \ldots, \sigma-1\}$, and let $n_c$ be the number of occurrences of $c$ in $S$. Positions are 0-based.

| operation | signature | what it does |
|---|---|---|
| `build` | $S \to$ structure | builds the structure for $S$ |
| `access(i)` | $0 \le i < n$ | returns $S[i]$ |
| `rank(c, i)` | $c \in \Sigma$, $0 \le i \le n$ | returns $|\{p < i : S[p] = c\}|$ |
| `select(c, j)` | $c \in \Sigma$, $1 \le j \le n_c$ | returns the $p$ with $S[p] = c$ and $\text{rank}(c, p) = j - 1$ |
| `length()` | | returns $n$ |

Many structures for this type also answer range queries on the sequence seen as a grid of points $(i, S[i])$: counting the positions $i \in [l, r)$ with $S[i] \in [a, b)$, the $k$-th smallest symbol in $S[l \ldots r-1]$ (the [range k-th smallest query](/range-kth-smallest-query/)), and listing the distinct symbols of a range, which is the core of [document listing](/document-listing/). These are extensions; the type itself has only access, rank and select.

**Example.** Take $S = $ abracadabra, $n = 11$, over $\{a, b, c, d, r\}$. The $a$s are at $0, 3, 5, 7, 10$, the $b$s at $1, 8$, the $r$s at $2, 9$, the $c$ at 4 and the $d$ at 6. Then `access(4)` $= c$, `rank(a, 7)` $= 3$, `select(a, 4)` $= 7$, `rank(b, 9)` $= 2$ and `select(r, 2)` $= 9$.

## Laws

For every $S$, every symbol $c$, every $0 \le i \le n$ and every $1 \le j \le n_c$:

1. $\text{rank}(c, 0) = 0$ and $\text{rank}(c, n) = n_c$.
2. $\text{rank}(c, i+1) = \text{rank}(c, i) + [S[i] = c]$ for $i < n$, where $[\cdot]$ is 1 for true and 0 for false. Hence $\text{access}(i)$ is the unique $c$ with $\text{rank}(c, i+1) > \text{rank}(c, i)$.
3. $\sum_{c \in \Sigma} \text{rank}(c, i) = i$.
4. $S[\text{select}(c, j)] = c$ and $\text{rank}(c, \text{select}(c, j)) = j - 1$, so $\text{select}(c, j) < \text{select}(c, j+1)$.
5. $\text{select}(c, \text{rank}(c, i) + 1) \ge i$ when $\text{rank}(c, i) < n_c$, with equality exactly when $S[i] = c$.
6. For $\sigma = 2$, the type is the [rank and select problem](/rank-select-problem/) on a bit vector, with $\text{rank}_1(i) = \text{rank}(1, i)$.

In the example, law 3 at $i = 7$ reads $3 + 1 + 1 + 1 + 1 = 7$, for $a$, $b$, $c$, $d$ and $r$.

## Implementations

| implementation | space in bits | access | rank | select |
|---|---|---|---|---|
| plain array and a sorted list of positions for each symbol | $n \lg \sigma + n \lg n$ | $O(1)$ | $O(\lg n)$ | $O(1)$ |
| one [rank/select dictionary](/rank-select-dictionary/) for each symbol | $\sigma n + o(\sigma n)$ | $O(\sigma)$ | $O(1)$ | $O(1)$ |
| [wavelet tree](/wavelet-tree/) | $n \lceil \lg \sigma \rceil + o(n \lg \sigma) + O(\sigma \lg n)$ | $O(\lg \sigma)$ | $O(\lg \sigma)$ | $O(\lg \sigma)$ |
| [wavelet matrix](/wavelet-matrix/) | $n \lceil \lg \sigma \rceil + o(n \lg \sigma)$ | $O(\lg \sigma)$ | $O(\lg \sigma)$ | $O(\lg \sigma)$ |
| wavelet tree in Huffman shape, or with [RRR](/rrr-bitvector/) bit vectors | $n H_0(S) + o(n \lg \sigma)$ | $O(1 + H_0)$ average, $O(\lg \sigma)$ | same | same |
| Golynski, Munro and Rao | $n \lg \sigma + o(n \lg \sigma)$ | $O(\lg \lg \sigma)$ | $O(\lg \lg \sigma)$ | $O(1)$ |
| Belazzougui and Navarro | $n H_0(S) + o(n (H_0(S) + 1))$ | $O(1)$ | $O(\lg(\lg \sigma / \lg w))$ | any $\omega(1)$ |

The array with lists is the simple solution for small inputs. The $\sigma$ bit vectors are fast and fine for $\sigma$ up to a handful of symbols. The wavelet tree and the wavelet matrix are the general-purpose choices: they also answer the range extensions in $O(\lg \sigma)$ time. Golynski, Munro and Rao cut $S$ into chunks of $\sigma$ symbols and represent each chunk by a [permutation](/succinct-permutation/) of its positions sorted by symbol, which removes the $\lg \sigma$ factor from the time. Belazzougui and Navarro combine alphabet partitioning with these chunks to reach compressed space and optimal rank time. For $\sigma$ near $n$, the space $n \lg \sigma$ is about the size of an array of integers, and the wavelet matrix is usually the best in practice.

## Lower bounds

**Space.** There are $\sigma^n$ strings of length $n$, so a structure for all of them needs $n \lg \sigma$ bits for some string, by the [information-theoretic bound](/information-theoretic-bound/). For the strings with given counts $n_c$, there are $\binom{n}{n_0, n_1, \ldots}$ of them, and the bound is $\lg \binom{n}{n_0, n_1, \ldots} = n H_0(S) - O(\sigma \lg n)$ bits.

**Time.** Belazzougui and Navarro proved that, on the word RAM with words of $w$ bits and space $n \cdot w^{O(1)}$ bits, rank needs $\Omega(\lg(\lg \sigma / \lg w))$ time, and they matched it. So for $\sigma = w^{O(1)}$, rank takes $O(1)$ time, and for larger alphabets no representation of near-linear size can have constant-time rank. Access and select are not subject to this bound.

**Redundancy.** For $\sigma = 2$, the lower bounds on the redundancy of rank and select are those of the bit-vector case; see [Pătraşcu's lower bounds](/patrascu-succinct-lower-bound/).

## References
