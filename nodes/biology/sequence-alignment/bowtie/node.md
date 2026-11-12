---
tag: 1P62H4
kind: algorithm
slug: bowtie
name: Bowtie
aliases:
- Bowtie2
- Bowtie 1
area: biology/sequence-alignment
level: advanced
summary: A short-read mapper that searches an FM-index of the genome, backtracks to allow a few mismatches, and uses a second index of the reversed genome to keep the backtracking small.
solves: [read-mapping]
model: word-ram
complexity:
  vars: {n: the length of the genome, m: the length of the read, k: the number of mismatches allowed, o: the number of hits}
  time: {worst: O(3^k m^(k+1) + o)}
  space: {extra: O(n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2009
  people: [Ben Langmead, Cole Trapnell, Mihai Pop, Steven L. Salzberg]
  note: Bowtie mapped short reads to the human genome with an FM-index small enough for a desktop computer; Bowtie 2 (2012) added gapped alignment.
prereqs: [fm-index, read-mapping]
see_also: [bwa, burrows-wheeler-transform, k-mismatch-problem, minimap2, seed-and-extend, pigeonhole-filtering, approximate-string-matching, generic-backtracking-algorithm]
sources:
  - paper: doi:10.1186/gb-2009-10-3-r25
    title: Ben Langmead, Cole Trapnell, Mihai Pop and Steven L. Salzberg, Ultrafast and memory-efficient alignment of short DNA sequences to the human genome, Genome Biology 10(3), 2009
    locator: article R25, Methods (Burrows-Wheeler indexing, Searching for inexact alignments, Excessive backtracking, Phased Maq-like search) and Results
  - paper: doi:10.1038/nmeth.1923
    title: Ben Langmead and Steven L. Salzberg, Fast gapped-read alignment with Bowtie 2, Nature Methods 9(4), 2012
    locator: pages 357 to 359, seed extraction from the read, FM-index lookup of the seeds and SIMD dynamic programming
  - paper: doi:10.1109/SFCS.2000.892127
    title: Paolo Ferragina and Giovanni Manzini, Opportunistic data structures with applications, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS), 2000
    locator: pages 390 to 398, the FM-index and backward search
  - paper: doi:10.1101/gr.078212.108
    title: Heng Li, Jue Ruan and Richard Durbin, Mapping short DNA sequencing reads and calling variants using mapping quality scores, Genome Research 18(11), 2008
    locator: pages 1851 to 1858, the alignment policy with mismatches in the seed and quality values that Bowtie's Maq-like mode follows
---

Bowtie is a short-read mapper from 2009 by Langmead, Trapnell, Pop and Salzberg. It stores the genome as an [FM-index](/fm-index/), which for the human genome fits in about 1.3 GB of memory, and finds each read by backward search, one letter at a time from the right end. To allow mismatches it *backtracks*: when the search fails or may miss a better hit, it goes back to an earlier letter and tries a substitution. Unbounded backtracking can explode, so Bowtie adds *double indexing*: a second FM-index of the reversed genome, the *mirror index*, lets every search start with the half of the read that must match exactly. Bowtie is a heuristic: by default its search is greedy, it limits the number of backtracks, and it does not promise the best alignment. Bowtie 2 (2012) is a different program that adds gaps.

## In plain words

An FM-index lets you look up a word in a genome by reading the word backwards, from its last letter to its first. Each step keeps the set of genome places that still match what you have read so far. If the set becomes empty, the word does not occur.

A read from a sequencing machine can have a wrong letter. So when the set becomes empty, Bowtie steps back and tries another letter at some earlier position. This is fast when the wrong letter is near the start of the search, and slow when it is near the end, because then many short dead ends get explored. Bowtie's trick is a second index of the genome written backwards. With it, Bowtie can also search a read from its first letter forwards, so it can always begin with the half of the read that has no wrong letter.

## The problem

**Input.** A genome $R$ of length $n$ over $\{A, C, G, T\}$, reads of length $m$ with a quality value per base, and a policy: the number $k$ of mismatches allowed, at most 3 in Bowtie, either in the whole read or in a seed of the first $L$ bases.

**Output.** For each read, one or more places where the read or its reverse complement matches $R$ with at most $k$ mismatches, with no gaps. By default Bowtie reports one valid hit, not necessarily the best one; with the option for the best hit it reports a hit with the fewest mismatches, at a cost in speed.

This is the [k-mismatch problem](/k-mismatch-problem/) for many short patterns against one indexed text, in the setting of [read mapping](/read-mapping/).

## The algorithm

**Backward search.** The FM-index keeps the [Burrows-Wheeler transform](/burrows-wheeler-transform/) $B$ of $R\$$, the array $C[a]$ (the number of letters smaller than $a$) and rank queries $\mathrm{Occ}(a, i)$ (the number of $a$ in $B[0 \ldots i-1]$). If $[sp, ep)$ is the interval of suffix array rows whose suffixes start with a string $u$, then the rows that start with $au$ are

$$[\,C[a] + \mathrm{Occ}(a, sp),\ C[a] + \mathrm{Occ}(a, ep)\,).$$

Each step takes $O(1)$ time, so an exact read takes $m$ steps. See the [FM-index](/fm-index/) page for the details and the proof.

**Backtracking.** To allow up to $k$ substitutions, the search is a depth-first search over the read from right to left. At position $i$ it tries the read letter, and, if fewer than $k$ substitutions are used and position $i$ is allowed to change, the three other letters. A branch dies when its interval becomes empty.

**Double indexing for one mismatch.** Split the read $P$ into a left half $P_L$ and a right half $P_R$. A hit with at most one mismatch has an exact copy of $P_L$ or of $P_R$. Phase 1 uses the forward index, matches $P_R$ first with no substitution, and allows the mismatch only in $P_L$. Phase 2 uses the mirror index, the FM-index of $R$ reversed (not complemented), on the reversed read $\overleftarrow{P}$. Its backward search reads $P$ from left to right, so it matches $P_L$ first with no substitution and allows the mismatch only in $P_R$. In both phases the first half of the search is exact, so branches do not start until the interval is already small.

```pseudo id=main
BACKTRACK(I, P, k, lo, hi)                ▷ index I, read P[0 .. m − 1], substitutions only in [lo, hi)
L1  S ← stack with (m, [0, n + 1), 0)
L2  while S is not empty do pop (i, [sp, ep), z)
L3      if i = 0 then report the rows [sp, ep) with z mismatches; continue
L4      for each letter b in {A, C, G, T} do
L5          if b ≠ P[i − 1] and (z = k or i − 1 ∉ [lo, hi)) then skip b
L6          if b ≠ P[i − 1] and the backtrack limit is reached then skip b
L7          [sp', ep') ← [C[b] + Occ(b, sp), C[b] + Occ(b, ep))
L8          if sp' < ep' then push (i − 1, [sp', ep'), z + [b ≠ P[i − 1]])

BOWTIE-ONE-MISMATCH(P)                    ▷ h = ⌊m/2⌋: P_L = P[0 .. h − 1], P_R = P[h .. m − 1]
L9  H ← positions of BACKTRACK(forward index, P, 1, 0, h)
L10 for each row of BACKTRACK(mirror index, reverse of P, 1, 0, m − h) do
L11     add n − SA_mirror[row] − m to H     ▷ start in R of the hit found in reverse(R)
L12 return H
```

Bowtie runs this for the read and for its reverse complement. The real program adds three things. It is *quality-aware*: among the positions where it may substitute, it tries first the ones with low base quality. It is *greedy and randomized*: it goes depth first, takes the first valid hit, and breaks ties at random. And it limits *excessive backtracking*: after a fixed number of backtracks (125 by default) it gives up on a branch. In the Maq-like mode, mismatches are bounded in a seed of the first $L = 28$ bases, which are split into two halves of 14, and the search runs in phases over the two indexes so that each phase starts from a half that has few or no mismatches.

## Example

Let $R = \texttt{GATTACAGATTGCA}$ ($n = 14$) and the read $P = \texttt{GATTAC}$, with at most one mismatch. The answer is two hits on the forward strand: position 0 with no mismatch, and position 7, where $R[7 \ldots 12] = \texttt{GATTGC}$ differs from $P$ at read position 4. The reverse complement GTAATC has no hit.

Split $P$ into $P_L = \texttt{GAT}$ and $P_R = \texttt{TAC}$. The mismatch of the second hit lies in $P_R$.

- *Phase 1* (forward index) matches C, A, T of $P_R$ exactly. The interval holds only the suffix that starts at position 3 (TAC…). It then reads $P_L$ with one substitution allowed and finds position 0. Position 7 is not found here, because its copy of $P_R$ is TGC.
- *Phase 2* (mirror index of $\overleftarrow{R} = \texttt{ACGTTAGACATTAG}$) searches $\overleftarrow{P} = \texttt{CATTAG}$ backwards: first G, A, T, which is $P_L$ read from left to right, with no substitution, then $P_R$ with one substitution allowed. It finds CATTAG at mirror position 8 and CGTTAG at mirror position 1. Line L11 turns these into $14 - 8 - 6 = 0$ and $14 - 1 - 6 = 7$.

The union is $\{0, 7\}$. On this example the implementation makes 50 backward-search steps for plain backtracking and 35 for double indexing, counting both strands. On 30 reads of 30 bases with one mismatch each, taken from a random genome of 3,000 bases, the averages are about 238 and 99 steps.

## Correctness

**Backtracking.** BACKTRACK reports exactly the occurrences of strings that differ from $P$ in at most $k$ positions, all in $[lo, hi)$, provided no limit cuts the search. The search tree has one node for each such string suffix whose interval is non-empty; the backward-search step is correct by the FM-index invariant, so a node's interval holds the rows of the suffixes that start with its string, and a leaf at $i = 0$ holds the occurrences of the whole string.

**Double indexing.** Let a hit at position $s$ have at most one mismatch. If the mismatch is in $P_L$ or there is none, then $P_R$ matches exactly, and phase 1 finds $s$. If it is in $P_R$, then $P_L$ matches exactly. The string $R[s \ldots s+m-1]$ reversed occurs in $\overleftarrow{R}$ at $n - s - m$, and it differs from $\overleftarrow{P}$ only in the first $m - h$ positions, which phase 2 allows to change; so phase 2 finds row $n - s - m$, and line L11 gives back $s$. Every reported position is a real hit with at most one mismatch, by the correctness of BACKTRACK. The proofs file has the details.

**Heuristics.** With the backtrack limit, the greedy order and the first-hit rule, Bowtie can miss hits and can report a hit that is not the best. The Bowtie paper states this, and offers a slower mode that finds the best hit.

## Complexity

| step | time | space |
|---|---|---|
| build the two indexes | $O(n \log n)$ with a typical suffix sorting, $O(n)$ with a linear one | $O(n)$ words while building |
| exact read | $O(m)$ | $O(1)$ |
| up to $k$ mismatches, plain backtracking | $O(3^k m^{k+1})$ worst case, plus $O(o)$ to list the hits | $O(km)$ stack |
| one mismatch, double indexing | $O(m^2)$ worst case, much less on average | $O(m)$ |

The worst case of backtracking counts all strings within Hamming distance $k$ of $P$: $\sum_{z \le k} \binom{m}{z} 3^z$ of them, each with up to $m$ steps. In practice most branches die after a few steps, because a random string of length $\ell$ occurs in the genome only if $4^\ell$ is not much more than $n$. The double index helps because the exact half shrinks the interval to a few rows before any branch starts; in phase 1 of the example the interval holds one row when the substitutions begin. The index takes about $2n$ bits for the BWT of DNA plus the rank tables and a sample of the suffix array, for each of the two indexes; Bowtie reported about 1.3 GB of memory for the human genome.

## Properties

- **Heuristic.** It reports valid hits, but by default not all of them and not the best one.
- **No gaps.** Bowtie allows only mismatches; reads with insertions or deletions are missed or reported with extra mismatches.
- **Randomized.** Ties between equal hits, such as reads from repeats, are broken at random, which is why the property list marks it as not deterministic.
- **Memory-efficient.** The index is a compressed self-index; the genome itself is not stored separately.

## Variants and improvements

- **Best hit mode.** The search continues until it can prove that no hit with fewer mismatches exists, which Bowtie reports as 2 to 3 times slower.
- **More mismatches.** For two or three mismatches the read is split into more parts and the phases cover the cases of where the mismatches lie, as in [pigeonhole filtering](/pigeonhole-filtering/).
- **[BWA](/bwa/).** BWA-backtrack, published in the same year, also searches an FM-index with backtracking, but it allows gaps and prunes with a lower bound on the differences left, computed with the index of the reversed genome.
- **Bowtie 2.** Bowtie 2 extracts short seeds from the read, looks them up exactly in the FM-index, and extends them with SIMD dynamic programming, so it allows gaps and local alignment. It is the variant in common use.
- **Bidirectional indexes.** Later methods keep a forward and a reversed index in sync, so that a search can grow a match in both directions; this generalizes the two phases of double indexing.

## When to use it

Bowtie fits short reads with few mismatches and no indels, such as the 25 to 50 base reads it was built for, when speed and memory matter more than finding every hit. For longer reads, reads with indels, or reads of varying quality, use Bowtie 2, [BWA](/bwa/)-MEM or [minimap2](/minimap2/).

## Pitfalls

- **Indels.** A read with a 1-base deletion looks like many mismatches after the deletion point and is often not mapped.
- **Default reporting.** One valid hit is not the best hit. For variant calling use the best-hit mode or a mapper that reports a mapping quality.
- **Mirror index direction.** The mirror index is of the reversed genome, not of the reverse complement. Using the reverse complement there finds hits on the wrong strand and at wrong positions.
- **Off by one in the mirror positions.** A hit at mirror position $p$ of a read of length $m$ starts at $n - p - m$ in the forward genome, not at $n - p$.

## Implementations

## History

Burrows and Wheeler described their transform in 1994, and Ferragina and Manzini built the FM-index on it in 2000. In 2008 and 2009, as second-generation sequencers produced millions of reads of 25 to 50 bases, several groups turned the FM-index into a read mapper. Bowtie (Langmead, Trapnell, Pop and Salzberg, 2009) introduced the mirror index and quality-aware backtracking and reported mapping more than 25 million reads per hour to the human genome on one CPU; BWA (Li and Durbin, 2009) and SOAP2 appeared the same year. Bowtie 2 (Langmead and Salzberg, 2012) replaced the ungapped search with seed lookups and dynamic programming.

## References
