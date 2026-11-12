---
tag: 3PGQMC
kind: data-structure
slug: kmer-index
name: k-mer index
aliases:
- k-mer table
- seed index
- k-mer lookup table
area: biology/sequence-alignment
level: core
summary: A table from each k-mer of a text to the sorted list of its start positions. It finds the exact seeds that read mappers and search tools extend into alignments.
model: word-ram
complexity:
  vars: {n: the length of the text, k: the k-mer length, s: the sampling step, o: the number of occurrences returned}
  time: {worst: O(k + o)}
  space: {extra: O(4^k + n/s)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [kmer, hash-table, counting-sort]
see_also: [minimizer, blat, seed-and-extend, spaced-seed, fm-index, suffix-array, kmer-counting, inverted-index]
sources:
  - paper: doi:10.1101/gr.229202
    title: W. James Kent, BLAT, the BLAST-like alignment tool, Genome Research 12(4), 2002
    locator: pages 656 to 664, Methods (the index of non-overlapping K-mers of the database and the exclusion of K-mers that occur too often)
  - paper: doi:10.1101/gr.194201
    title: Zemin Ning, Anthony J. Cox and James C. Mullikin, SSAHA, a fast search method for large DNA databases, Genome Research 11(10), 2001
    locator: pages 1725 to 1729, the hash table of non-overlapping k-tuples of the database and its position lists
  - paper: doi:10.1093/bioinformatics/bty191
    title: Heng Li, Minimap2, pairwise alignment for nucleotide sequences, Bioinformatics 34(18), 2018
    locator: pages 3094 to 3100, Section 2 (a hash table from minimizer hashes to lists of positions)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.2, Counting sort (the layout of the position array) and Chapter 11, Hash tables
---

A k-mer index of a text $T$ is a table that maps each [k-mer](/kmer/) $x$ to the sorted list of positions $p$ with $T[p \ldots p+k-1] = x$. It answers "where does this word of length $k$ occur?" in $O(k)$ time plus the size of the answer, and it is the seed finder of [seed-and-extend](/seed-and-extend/) tools such as [BLAT](/blat/), SSAHA and [minimap2](/minimap2/). For DNA and small $k$ the table is a direct-address array of $4^k$ buckets laid out as in a counting sort; for larger $k$ it is a [hash table](/hash-table/). It finds only exact k-mer matches, so it is a filter: the tool must still check each hit with an alignment, and a true alignment with no exact match of length $k$ is missed.

## In plain words

Think of the index at the back of a book. For each word, it lists the pages where the word appears. A k-mer index does the same for DNA. The "words" are all the short pieces of one fixed length, and the "pages" are the positions in the genome.

To build it, slide a window of that length along the genome. For each window, write its position in the list of the word it holds. To use it, cut a read into words of the same length and look each one up. Each position you get back is a place where the read may come from. A genome position that many words of the read point to, at the same shift, is a strong candidate.

## The abstract type

The structure is static: it is built once from a text $T$ of length $n$ over $\Sigma = \{A, C, G, T\}$, for a fixed $k \ge 1$ and a sampling step $s \ge 1$. It supports:

- `lookup(x)`: for a string $x$ of length $k$, the sorted list of the indexed positions $p$ with $T[p \ldots p+k-1] = x$. With $s = 1$ every position $0 \le p \le n-k$ is indexed. With $s > 1$ only the positions $p$ with $p \bmod s = 0$ are indexed.
- `count(x)`: the length of that list.
- `seed-hits(Q)`: for a query $Q$, all pairs $(q, p)$ with $Q[q \ldots q+k-1] = T[p \ldots p+k-1]$ and $p$ indexed. This is a lookup for each of the $|Q| - k + 1$ k-mers of $Q$.

A k-mer that holds a letter outside $\Sigma$, such as N, is not indexed. This is a dictionary from $\Sigma^k$ to position lists, the same idea as an [inverted index](/inverted-index/) of a document collection, with every k-mer of the text as a term.

## Representation

A k-mer $x = x_1 \cdots x_k$ has the integer code $c(x) = \sum_{i=1}^{k} v(x_i)\, 4^{k-i}$, with $v(A) = 0$, $v(C) = 1$, $v(G) = 2$, $v(T) = 3$. The code is the k-mer read as a base-4 number, so it takes $2k$ binary digits and lies in $[0, 4^k)$, and two k-mers have the same code exactly when they are equal.

The direct-address layout has two arrays:

- `pos[0 .. P-1]`, where $P$ is the number of indexed positions. It holds every indexed position once, grouped by code, in increasing code order.
- `off[0 .. 4^k]`, the bucket boundaries. The positions of code $c$ are `pos[off[c] .. off[c+1] - 1]`.

**Invariant.** For each code $c$, the slice `pos[off[c] .. off[c+1] - 1]` is the increasing list of the indexed positions $p$ with $c(T[p \ldots p+k-1]) = c$. In particular `off[0] = 0` and `off[4^k] = P`.

For large $k$, $4^k$ buckets do not fit in memory. Then `off` is replaced by a hash table from the codes that occur to their slices, which keeps the same `pos` array.

## Operations

The codes of consecutive k-mers come from one rolling update. If $c_p$ is the code of $T[p \ldots p+k-1]$, then

$$c_{p+1} = \bigl(4\,c_p \bmod 4^k\bigr) + v(T[p+k]),$$

which drops the first letter and appends the next one. In binary this is a shift left by 2, a mask to $2k$ digits and an OR, so all codes take $O(n)$ time.

```pseudo id=main
BUILD-KMER-INDEX(T, k, s)                 ▷ text T[0 .. n − 1], step s
L1  for c ← 0 to 4^k − 1 do cnt[c] ← 0
L2  for each indexed position p, in increasing order, with code c_p do
L3      cnt[c_p] ← cnt[c_p] + 1
L4  off[0] ← 0
L5  for c ← 0 to 4^k − 1 do off[c + 1] ← off[c] + cnt[c]
L6  next[c] ← off[c] for each c
L7  for each indexed position p, in increasing order, with code c_p do
L8      pos[next[c_p]] ← p
L9      next[c_p] ← next[c_p] + 1
L10 return (off, pos)
```

Lines L1 to L5 count the positions of each code and turn the counts into bucket starts by a prefix sum. Lines L6 to L9 fill each bucket from left to right. This is the distribution pass of [counting sort](/counting-sort/), with the k-mer code as the key and the position as the item. A position is indexed when $p \le n - k$, $p \bmod s = 0$ and the k-mer holds only A, C, G and T.

```pseudo id=lookup
LOOKUP(x)                                 ▷ |x| = k
L11 if x holds a letter outside {A, C, G, T} then return the empty list
L12 c ← c(x)
L13 return pos[off[c] .. off[c + 1] − 1]

SEED-HITS(Q)
L14 H ← empty list
L15 for each q from 0 to |Q| − k with Q[q .. q + k − 1] over {A, C, G, T} do
L16     for each p in LOOKUP(Q[q .. q + k − 1]) do append (q, p) to H
L17 return H
```

LOOKUP computes the code in $O(k)$ time and returns a slice. SEED-HITS uses the rolling update for the codes of $Q$, so it takes $O(|Q| + h)$ time for $h$ hits. A mapper then groups the hits by the *diagonal* $p - q$: the hits of one ungapped match all lie on one diagonal, and a gapped match gives hits on a few nearby diagonals.

## Example

Index $T = \texttt{ACGTACGTTACG}$, $n = 12$, with $k = 3$ and $s = 1$. The ten k-mers and their codes are:

| $p$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| k-mer | ACG | CGT | GTA | TAC | ACG | CGT | GTT | TTA | TAC | ACG |
| code | 6 | 27 | 44 | 49 | 6 | 27 | 47 | 60 | 49 | 6 |

Six of the 64 buckets are not empty. After line L5, `off[6] = 0`, `off[27] = 3`, `off[44] = 5`, `off[47] = 6`, `off[49] = 7`, `off[60] = 9` and `off[64] = 10`. Lines L7 to L9 fill the buckets in the order of $p$:

| bucket | ACG (6) | CGT (27) | GTA (44) | GTT (47) | TAC (49) | TTA (60) |
|---|---|---|---|---|---|---|
| slots | 0 to 2 | 3 to 4 | 5 | 6 | 7 to 8 | 9 |
| positions | 0, 4, 9 | 1, 5 | 2 | 6 | 3, 8 | 7 |

So `pos` $= [0, 4, 9, 1, 5, 2, 6, 3, 8, 7]$. The query $Q = \texttt{TTACGA}$ has the k-mers TTA, TAC, ACG and CGA. SEED-HITS returns $(0, 7)$, $(1, 3)$, $(1, 8)$, $(2, 0)$, $(2, 4)$ and $(2, 9)$; CGA has no hit. Three hits lie on the diagonal $p - q = 7$, and indeed $Q[0 \ldots 4] = \texttt{TTACG} = T[7 \ldots 11]$. The other hits are on diagonals 2 and $-2$, and are short chance matches.

## Correctness

LOOKUP is correct because the build keeps the invariant: each indexed position is written once, into the bucket of its code, and the buckets are filled in increasing order of position. The proof follows the [loop invariant](/loop-invariant/) of lines L7 to L9: before the step for position $p$, `next[c]` is `off[c]` plus the number of indexed positions before $p$ with code $c$, and those positions fill the first slots of bucket $c$ in increasing order. Since the code is a bijection between $\Sigma^k$ and $[0, 4^k)$, the bucket of $c(x)$ holds exactly the occurrences of $x$. The full proof, with the guarantee of the sampled index, is in the proofs file.

**Sampled index.** With $s = k$, as in BLAT and SSAHA, every exact match of length at least $2k - 1$ between a query and $T$ contains a whole indexed k-mer, so SEED-HITS finds it. A shorter exact match may be missed. With $s = 1$, every exact match of length at least $k$ is found.

## Complexity

All costs are worst case in the [word RAM](/word-ram/) with words of at least $2k$ binary digits.

| operation | time | notes |
|---|---|---|
| build, direct address | $O(n + 4^k)$ | two passes over $T$, one prefix sum over the buckets |
| build, hash table | $O(n)$ expected | with a hash table of the codes that occur |
| lookup | $O(k + o)$ | $o$ positions returned; $O(1 + o)$ when the code is known |
| seed hits of a query $Q$ | $O(\lvert Q \rvert + h)$ | $h$ hits in total |
| space | $4^k + 1 + P$ words | $P \le \lfloor (n-k)/s \rfloor + 1$ positions |

The build visits each position twice and each bucket twice. The space is dominated by `off` when $4^k > n$, so direct address is used up to about $4^k \approx n$, which is $k \approx 16$ for a human-sized genome of $3 \times 10^9$ bases. The number of hits $h$ is the cost that matters in practice: in a random text of length $n$ with uniform letters, a fixed k-mer has $(n-k+1)/4^k$ expected occurrences, but a repeat such as an Alu element gives a single k-mer millions of hits. Tools therefore drop the k-mers whose count is above a cut-off. BLAT excludes k-mers that occur too often, and SSAHA uses a cut-off on the number of positions.

## Variants

- **Non-overlapping k-mers.** Index only the positions $p$ with $p \bmod k = 0$. The index is $k$ times smaller, and exact matches of length $2k - 1$ or more are still found. [BLAT](/blat/) and SSAHA use this.
- **Minimizer index.** Index only the [minimizers](/minimizer/) of the text. The index keeps about $2/(w+1)$ of the positions, and any exact match of length $w + k - 1$ shares at least one indexed k-mer. [Minimap2](/minimap2/) uses this.
- **Spaced seeds.** Use a pattern of care and don't-care positions instead of $k$ consecutive letters, so that a seed tolerates mismatches at the don't-care positions. See [spaced seed](/spaced-seed/).
- **Canonical k-mers.** Store the smaller of the codes of a k-mer and of its reverse complement, so that one lookup finds hits on both strands.
- **Query index.** [BLAST](/blast/) and FASTA build the table for the query, not for the database, and scan the database through it. This needs no index of the database but scans the whole database for each query.
- **Full-text indexes.** A [suffix array](/suffix-array/) or an [FM-index](/fm-index/) answers lookups for every length, not only $k$, and finds maximal matches. They take more time per lookup and support variable-length seeds such as [maximal exact matches](/maximal-exact-match/).

## When to use it

Use a k-mer index when the seed length is fixed, the text is static, and lookups must be fast. With direct address it needs no comparisons and no pointer chasing, so it is fast in practice. Use the sampled or minimizer version when memory is tight. Use an [FM-index](/fm-index/) when seeds of many lengths are needed, or when the index of a large genome must fit in a few gigabytes; an index of every position needs at least one machine word per position.

## Pitfalls

- **Ambiguous letters.** A rolling code that maps N to some base invents k-mers that are not in the text. The rolling update must restart after each letter outside the alphabet, as the implementation does.
- **Off by one at the end.** The last k-mer starts at $n - k$, not at $n - k + 1$ or $n - 1$; line L2 must stop there.
- **Repeats.** Without a cut-off on the count, one k-mer from a repeat family can return a huge list and make one query take as long as a full scan. Mask such k-mers, and report that the search can then miss hits inside repeats.
- **Mixing strands.** The index of one strand finds only hits on that strand. Index both strands, use canonical k-mers, or also look up the reverse complement of the query.
- **Too small or too large $k$.** A small $k$ gives many random hits, about $n/4^k$ for each lookup. A large $k$ misses true matches in reads with errors: a read of length $L$ with $e$ errors spread out evenly may have no error-free piece of length $k$ once $k > L/(e+1)$.

## Implementations

## History

Tables of short words are an old tool of sequence comparison. FASTA and [BLAST](/blast/) build the table for the query and scan the database. For large DNA databases the table moved to the database side: SSAHA (Ning, Cox and Mullikin, 2001) and BLAT (Kent, 2002) hash the non-overlapping k-mers of the genome, so that the index of a human genome fits in the memory of one machine. Later mappers kept the idea with smaller samples, such as the minimizer index of minimap2 (Li, 2018).

## References
