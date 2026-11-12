---
tag: 9BK48N
kind: technique
slug: seed-and-extend
name: Seed and extend
aliases:
- seed and extend heuristic
- seed-and-extend alignment
area: biology/sequence-alignment
level: core
summary: Find short exact or near-exact matches (seeds) with an index, then grow each seed into a local alignment. Fast, but it misses alignments that contain no seed.
prereqs: [local-alignment, kmer, pigeonhole-filtering]
see_also: [blast, fasta-algorithm, spaced-seed, kmer-index, high-scoring-segment-pair, x-drop-extension, seed-chaining, q-gram-lemma]
sources:
  - paper: doi:10.1016/S0022-2836(05)80360-2
    title: Stephen F. Altschul, Warren Gish, Webb Miller, Eugene W. Myers and David J. Lipman, Basic local alignment search tool, Journal of Molecular Biology 215(3), 1990
    locator: pages 403 to 410, Methods (word hits from a neighborhood list, extension of each hit with a drop-off, and the trade of speed against the chance to miss a segment pair)
  - paper: doi:10.1073/pnas.85.8.2444
    title: William R. Pearson and David J. Lipman, Improved tools for biological sequence comparison, PNAS 85(8), 1988
    locator: pages 2444 to 2448 (ktup lookup, diagonal regions and the optimized score in a band)
  - paper: doi:10.1093/bioinformatics/18.3.440
    title: Bin Ma, John Tromp and Ming Li, PatternHunter, faster and more sensitive homology search, Bioinformatics 18(3), 2002
    locator: pages 440 to 445 (the sensitivity of a seed as the probability to hit a region of given length and similarity, and spaced seeds)
  - paper: doi:10.1101/gr.229202
    title: W. James Kent, BLAT, the BLAST-like alignment tool, Genome Research 12(4), 2002
    locator: pages 656 to 664 (an index of the database instead of the query, and the hit statistics of exact and near-exact seeds)
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Chapter 9, Combinatorial Pattern Matching (filtering for approximate matching and BLAST)
---

Seed and extend is a heuristic technique that finds [local alignments](/local-alignment/) fast in two steps. First it finds *seeds*, short matches between the query and the database that an index can look up, such as shared [k-mers](/kmer/). Then it *extends* each seed into a full alignment, with work only near the seed. It is fast because random seed hits are rare, and it is not exact: an alignment that contains no seed is never found.

## In plain words

To find a sentence in a big library that is like your own sentence, you do not compare your sentence with every page. You first look up the rare words of your sentence in the index at the back of each book. Each place where a word is found is a *seed*. Then you go to that page and read around the word to see if the whole sentence is similar. That is the *extension*.

Most pages share no rare word with you, so you never read them. This saves most of the work. The risk is a similar sentence that has no word exactly like yours, for example because each word has one typo. The index does not find it, and you miss it. Longer seeds give fewer false starts but more misses. Shorter seeds give fewer misses but more false starts, and the search gets slow.

## When it applies

The technique fits a search for local similarity in a large text, when three things are true:

- **Seeds are common in true matches.** The alignments you want are long or similar enough that most of them contain a seed. The sensitivity table in the template shows how fast this fails as the identity drops.
- **Seeds are rare in random matches.** For a uniform random text over an alphabet of size $\sigma$, the expected number of chance hits of exact $k$-mers is $m N / \sigma^k$ for a query of length $m$ and a database of $N$ letters. This must be small next to $mN$, the work of a full [Smith-Waterman](/smith-waterman/) search.
- **The extension is local.** One seed fixes a diagonal, and the alignment stays near it. A band or an X-drop rule keeps the extension cost small.

It does not apply when you need every alignment above a score with a guarantee. Then use Smith-Waterman (exact, $O(mN)$ time), or a *lossless* seed design, where a lemma proves that each alignment of the class contains a seed.

## The template

**The model.** The query $q$ has length $m$ and the database $D$ has $N$ letters over an alphabet $\Sigma$ of size $\sigma$ (4 for DNA, 20 for proteins). A seed is a pair of positions $(i, j)$ where a word of $q$ at $i$ and a word of $D$ at $j$ match in a stated sense: an exact $k$-mer, a [spaced seed](/spaced-seed/), or a word pair with a [substitution matrix](/substitution-matrix/) score of at least $T$. The index is a [k-mer index](/kmer-index/) (a [hash table](/hash-table/) or a direct array of $\sigma^k$ lists), a [suffix array](/suffix-array/) or an [FM-index](/fm-index/). The extension scores alignments with a substitution matrix and a gap model. $S$ is the score cutoff.

```pseudo id=main
SEED-AND-EXTEND(q, D, S)
L1  build an index of the seeds of D, or of q
L2  for each seed hit (i, j) between q and D do
L3      if (i, j) lies inside an alignment already found on its diagonal then
L4          continue
L5      A ← EXTEND(q, D, i, j)            ▷ ungapped, then gapped, near (i, j)
L6      if score(A) ≥ S then report A
L7  remove duplicate and contained alignments
```

**Cost.** Let $h$ be the number of seed hits and $e$ the cost of one extension. The time is the index build, plus $O(m + h)$ for the lookups, plus $O(h e)$ for the extensions. For exact $k$-mers in a uniform random database, the expected number of chance hits is $m N \sigma^{-k}$, under the model that each of the $mN$ position pairs matches with probability $\sigma^{-k}$. The worst case has no such bound: a query AAAA$\cdots$ against a database AAAA$\cdots$ has $\Theta(mN)$ hits. So the speed is a property of typical inputs, not a worst-case guarantee.

**Sensitivity.** The sensitivity of a seed is the probability that a true alignment contains at least one seed hit. A common model is an ungapped alignment of length $L$ in which each position is a match with probability $p$, independently. The table gives this probability for a contiguous $k$-mer at $L = 64$, computed exactly by dynamic programming over the positions, and the expected number of chance hits for $m = 500$ and $N = 10^9$ DNA bases:

| $k$ | chance hits $mN/4^k$ | sensitivity at $p = 0.7$ | sensitivity at $p = 0.9$ |
|---|---|---|---|
| 8 | $7.6 \times 10^6$ | 0.7009 | 0.9996 |
| 11 | $1.2 \times 10^5$ | 0.3002 | 0.9824 |
| 14 | 1863 | 0.1054 | 0.9004 |
| 20 | 0.45 | 0.0113 | 0.5804 |
| 28 | $6.9 \times 10^{-6}$ | 0.0005 | 0.2378 |

Each step of $k$ divides the chance hits by 4, but the sensitivity at 70% identity falls fast. This trade is the central design choice of the technique.

**Lossless seeds.** Some seeds come with a proof. By the pigeonhole principle, an ungapped alignment of length $L$ with at most $e$ mismatches, cut into $e + 1$ pieces, has a piece with no mismatch, so an exact seed of length $\lfloor L/(e+1) \rfloor$ cannot miss it. A read of 100 bases with at most 4 mismatches always contains an exact match of 20 bases. See [pigeonhole filtering](/pigeonhole-filtering/). For [edit distance](/edit-distance/), the [q-gram lemma](/q-gram-lemma/) gives a count of shared $q$-grams that every match within distance $e$ must have; see [q-gram filtering](/q-gram-filtering/). Lossless seeds are used for read mapping with few errors. Protein homology search uses lossy seeds, because no short seed is present in all distant homologs.

## Classic examples

- **FASTA** (Lipman and Pearson 1985, Pearson and Lipman 1988). Seeds are exact matches of length ktup, found with a lookup table of the query. Hits are grouped by diagonal, the best regions are joined, and a [banded](/banded-smith-waterman/) Smith-Waterman gives the final score. See [FASTA](/fasta-algorithm/).
- **BLAST** (Altschul et al. 1990). Seeds are word pairs of length $w$ with a score of at least $T$, from a neighborhood list of the query. Each hit is extended without gaps by [X-drop extension](/x-drop-extension/) to a [high-scoring segment pair](/high-scoring-segment-pair/). Gapped BLAST (1997) adds the two-hit rule and gapped extension. See [BLAST](/blast/).
- **PatternHunter** (Ma, Tromp and Li 2002). The same frame with a [spaced seed](/spaced-seed/), which hits more true alignments for the same number of chance hits.
- **BLAT** (Kent 2002). It indexes the non-overlapping $k$-mers of the database instead of the query, and keeps the index in memory. See [BLAT](/blat/).
- **Read mappers.** [BWA](/bwa/) uses [maximal exact matches](/maximal-exact-match/) from an FM-index as seeds. [Bowtie](/bowtie/) starts from exact seeds with an FM-index. [minimap2](/minimap2/) uses [minimizers](/minimizer/) and then [chains](/seed-chaining/) the seeds before it extends them.

## Variations

- **The kind of seed.** Exact $k$-mers, word pairs that score at least $T$ (neighborhood words), spaced seeds, sets of several spaced seeds, maximal exact matches, and minimizers that sample the $k$-mers.
- **More than one hit.** The two-hit rule of Gapped BLAST extends only when two hits lie on one diagonal within a distance $A$. Chaining joins many seeds that are consistent in order before any extension. Both cut the number of extensions.
- **The extension.** Ungapped X-drop, then gapped X-drop; a banded DP around the seed diagonal; or a full DP in a window that the chain defines.
- **What to index.** Index the query and scan the database (BLAST, FASTA), or index the database and scan the query (BLAT, read mappers). The second costs memory once, and is better when many queries hit one database.

## Pitfalls

- **Low-complexity sequence.** Repeats such as AAAA$\cdots$ or CACACA$\cdots$ give a flood of hits and meaningless HSPs. Search tools mask such regions in the query (for example with the DUST filter for DNA and SEG for proteins) before the seed step.
- **One alignment, many seeds.** A long alignment contains many seeds. Without line L3, each one starts its own extension, the work grows with the length of the match, and the output has many copies.
- **Treating the result as exact.** A seed-and-extend search can miss a significant alignment that Smith-Waterman finds. The [BLAST](/blast/) page shows one: a DNA pair with a mismatch at every eighth position has no shared 11-mer, so seeding finds nothing, but the ungapped score is 42.
- **Too short a seed.** The table shows that $k = 8$ gives millions of chance hits for one query against $10^9$ bases. The extension step then does almost all the work of a full search.
- **The extension decides too.** A seed can be found but its extension can stop too early, by the X-drop rule or the band edge. Both steps can lose a match.
- **Sensitivity models are models.** The table assumes independent matches. Real alignments have gaps and runs of conserved positions, so real sensitivity differs.

## Exercises

1. For $\sigma = 20$, $m = 300$ and $N = 10^8$, find the least $k$ for which the expected number of chance exact $k$-mer hits is below 1000.
2. Prove that an ungapped alignment of length $L$ with at most $e$ mismatches contains an exact match of length $\lfloor L/(e+1) \rfloor$. Give an example with $L = 10$ and $e = 2$ where it contains no exact match of length 4.
3. Write the dynamic program that computes the probability that a random 0/1 string of length $L$ with $P(1) = p$ contains a run of $k$ ones. Check the value 0.3002 for $k = 11$, $L = 64$ and $p = 0.7$.
4. Show an input where the seed step of FASTA with ktup $= 2$ finds no hit but Smith-Waterman finds an alignment with a positive score. (Hint: alternate the letters.)
5. Give an example where the skip of line L3 loses a segment pair with a higher score than the one reported, even when the extension finds the best segment pair through its seed. (Hint: put a deep drop between two seeds on one diagonal.)

## References
