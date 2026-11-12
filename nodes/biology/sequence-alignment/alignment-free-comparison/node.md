---
tag: VBAZRT
kind: concept
slug: alignment-free-comparison
name: Alignment-free sequence comparison
aliases:
- alignment-free methods
- alignment-free sequence distance
area: biology/sequence-alignment
level: advanced
summary: Compare sequences by the words of length k they contain, such as the D2 count of shared words or the Mash distance from a MinHash sketch, without any alignment.
prereqs: [kmer, jaccard-similarity]
see_also: [minhash, kmer-spectrum, spaced-seed, database-similarity-search, kmer-index, phylogenetic-tree, neighbor-joining, bloom-filter]
sources:
  - paper: "David C. Torney, Christian Burks, Dan Davison and Karl M. Sirotkin, Computation of d2, a measure of sequence dissimilarity, in Computers and DNA, SFI Studies in the Sciences of Complexity 7, Addison-Wesley, 1990, pages 109 to 125"
    title: Torney, Burks, Davison and Sirotkin 1990
    locator: the D2 statistic, the number of pairs of equal words of length k in two sequences
  - paper: doi:10.1186/s13059-016-0997-x
    title: Brian D. Ondov, Todd J. Treangen, Pall Melsted, Adam B. Mallonee, Nicholas H. Bergman, Sergey Koren and Adam M. Phillippy, Mash, fast genome and metagenome distance estimation using MinHash, Genome Biology 17, article 132, 2016
    locator: the Mash distance D = -(1/k) ln(2j/(1+j)) from the Jaccard index j of k-mer sets, the bottom sketch of size s, and the comparison of D with 1 minus ANI
  - paper: doi:10.1093/bioinformatics/btg005
    title: Susana Vinga and Jonas Almeida, Alignment-free sequence comparison, a review, Bioinformatics 19(4), 2003
    locator: pages 513 to 523 (word frequency vectors, distances between them, and the D2 family)
---

Alignment-free sequence comparison measures how similar two sequences are from the [k-mers](/kmer/) they contain, and does not compute an alignment. Each sequence becomes a vector of word counts or a set of words, and a distance between the vectors or sets stands in for the alignment score. The classic statistic is D2, the number of pairs of equal $k$-mers (Torney et al. 1990); the best-known modern tool is Mash (Ondov et al. 2016), which turns a [MinHash](/minhash/) estimate of the [Jaccard similarity](/jaccard-similarity/) of the two $k$-mer sets into an estimate of the mutation rate. Both run in time linear in the length of the sequences, so they scale to whole genomes and to databases of many thousands of genomes.

## In plain words

Instead of lining up two sequences letter by letter, cut each one into all of its short overlapping words, for example all words of 21 letters. Then ask how many words the two lists have in common.

Two copies of the same genome share all their words. Each mutation breaks the few words that cover it, so the more the sequences differ, the fewer words they share. Counting shared words is much faster than aligning, because it needs only one pass over each sequence and no table of all position pairs. The price is that you learn how close the sequences are, but not where they match or how the letters line up.

To compare very large collections, keep only a small sample of each word list, chosen in the same way for every sequence, and compare the samples.

## The idea

**The model.** Sequences $x$ and $y$ over an alphabet of size $\sigma$ have lengths $m$ and $n$. Fix a word length $k$. For each word $w$ of length $k$, $X_w$ is the number of positions $i$ with $x[i \ldots i+k-1] = w$, and $Y_w$ is the same for $y$. The *count vector* of $x$ has one entry for each of the $\sigma^k$ words; it has at most $m - k + 1$ nonzero entries. The *$k$-mer set* $A$ of $x$ is the set of words with $X_w > 0$, and $B$ is the set for $y$. For DNA, tools often count *canonical* $k$-mers, the smaller of a word and its reverse complement, so that the two strands give the same set.

**D2.** The D2 statistic is the number of pairs of positions whose words are equal:

$$D_2(x, y) = \left|\{(i, j) : x[i \ldots i+k-1] = y[j \ldots j+k-1]\}\right|.$$

*Claim.* $D_2(x, y) = \sum_w X_w Y_w$, the inner product of the count vectors.

*Proof.* Put each pair $(i, j)$ in the set into the class of its common word $w$. The classes are disjoint and cover the set. The class of $w$ is the set of pairs with $x[i \ldots i+k-1] = w$ and $y[j \ldots j+k-1] = w$, which is a product of a set of $X_w$ positions and a set of $Y_w$ positions, so it has $X_w Y_w$ elements. Sum over $w$. $\square$

So D2 needs one count table per sequence, not a comparison of all $(m - k + 1)(n - k + 1)$ pairs. With a [hash table](/hash-table/) of words and a rolling hash, the counts take $O(m + n)$ expected time in the word-RAM model, and the sum takes time linear in the number of distinct words. The squared Euclidean distance between the count vectors is $\sum_w X_w^2 + \sum_w Y_w^2 - 2 D_2$, so D2 is also the cross term of the most direct distance between the vectors. D2 grows with the lengths and with repeats, so it is used in standardized forms when sequences of different lengths or composition are compared.

**Jaccard and Mash.** The Jaccard index of the $k$-mer sets is $j = |A \cap B| / |A \cup B|$. Mash relates it to a mutation rate under a simple model: $y$ comes from $x$ by independent substitutions at a rate $d$ per site, and the two sets have about the same size $N$ with no chance sharing. A $k$-mer survives with probability $(1 - d)^k \approx e^{-kd}$, so about $sN$ words are shared, with $s = e^{-kd}$, and the union has $2N - sN$ words. So $j = s / (2 - s)$. Solving for $s = 2j / (1 + j)$ gives the *Mash distance*

$$D = -\frac{1}{k} \ln \frac{2j}{1 + j}.$$

$D$ is 0 when $j = 1$ and has no finite value when $j = 0$. Ondov et al. found that $D$ tracks $1 - \text{ANI}$, where ANI is the average nucleotide identity of the aligned parts of two genomes, for closely related genomes.

**Sketches.** Mash does not store the whole set. It hashes each $k$-mer (with MurmurHash3) and keeps the $s$ smallest hash values, the *bottom-$s$ sketch*. For two sketches it takes the $s$ smallest values of their union and counts how many are in both; the fraction is an estimate of $j$ whose error shrinks like $1/\sqrt{s}$. The defaults are $k = 21$ and $s = 1000$. A sketch of a genome of $m$ bases takes $O(m \log s)$ time to build and $O(s)$ space, and two sketches are compared in $O(s)$ time, whatever the size of the genomes. See [MinHash](/minhash/) for why the estimate is unbiased.

**Choosing $k$.** If $k$ is small, unrelated sequences share many words by chance: a sequence of length $m$ has about $m$ words out of $\sigma^k$ possible ones, so chance sharing is common when $\sigma^k$ is not much larger than $m$. If $k$ is large, each mutation breaks $k$ words, and $j$ falls to 0 for distant sequences, where $D$ is no longer useful. For bacterial genomes over DNA, $k = 21$ keeps chance sharing small, and the table below shows how fast $j$ falls as the divergence grows.

## Examples

**D2 by hand.** Let $x = \texttt{ACGTACGTTA}$, $y = \texttt{TACGTTACGA}$ and $k = 3$. The counts are:

| word | ACG | CGA | CGT | GTA | GTT | TAC | TTA |
|---|---|---|---|---|---|---|---|
| $X_w$ | 2 | 0 | 2 | 1 | 1 | 1 | 1 |
| $Y_w$ | 2 | 1 | 1 | 0 | 1 | 2 | 1 |

So $D_2 = 2 \cdot 2 + 2 \cdot 1 + 1 \cdot 1 + 1 \cdot 2 + 1 \cdot 1 = 10$, and a direct count of the 64 position pairs also finds 10 equal pairs. Both count vectors have $\sum X_w^2 = \sum Y_w^2 = 12$, so the squared Euclidean distance is $12 + 12 - 20 = 4$. The sets have 5 shared words out of 7 in the union, so $j = 5/7 = 0.714$ and the Mash formula with $k = 3$ gives $D = 0.0608$.

**The model, forward and back.** With $k = 21$, the model gives these Jaccard values, and the Mash formula recovers $d$ from each one exactly:

| rate $d$ | $j = e^{-kd} / (2 - e^{-kd})$ | $D$ |
|---|---|---|
| 0.01 | 0.6815 | 0.01 |
| 0.05 | 0.2121 | 0.05 |
| 0.10 | 0.0652 | 0.10 |

So at a divergence of 10%, only about 6.5% of the union is shared at $k = 21$, and a sketch of 1000 hashes sees about 65 shared values.

**A simulation.** A random genome of 20,000 bases with uniform letters (seed 1) was copied with independent substitutions, and the exact $j$ of the two sets of 21-mers was computed. At $d = 0.01$, $j = 0.6456$ and $D = 0.0115$. At $d = 0.05$, $j = 0.2207$ and $D = 0.0484$. The estimate is close to the true rate, with an error from the random choice of mutated sites and from the approximation $(1 - d)^k \approx e^{-kd}$.

## Where it is used

- **Genome distance at scale.** Mash and similar tools compare a new genome against sketches of all genomes in a reference collection in seconds, to find its nearest relatives or to cluster a collection, which would take far longer with [database similarity search](/database-similarity-search/) by alignment.
- **Phylogeny.** A matrix of Mash or other word distances goes into a distance method such as [neighbor joining](/neighbor-joining/) to build a [phylogenetic tree](/phylogenetic-tree/) without a multiple alignment.
- **Read classification.** Tools that assign sequencing reads to taxa by exact $k$-mer lookup in a [k-mer index](/kmer-index/) are alignment-free in the same sense.
- **Screening and filtering.** Sketches and [Bloom filters](/bloom-filter/) of $k$-mer sets decide fast whether a sample contains a given genome, before any alignment is run.
- **Diverged sequences.** Counting [spaced words](/spaced-seed/) instead of contiguous $k$-mers lets a mismatch break fewer words, which extends the range of divergence where the distance is useful.

The limits come from the model. Word methods give a number, not an alignment, so they cannot show which positions match. They assume that differences are spread out; rearrangements, large insertions and repeats change $j$ in ways the substitution model does not describe. For distant protein sequences, alignment with a [substitution matrix](/substitution-matrix/) is still more sensitive.

## References
