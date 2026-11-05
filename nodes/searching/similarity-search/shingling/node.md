---
tag: 8V1VY4
kind: technique
slug: shingling
name: Shingling
aliases:
- k-shingles
- q-grams for documents
area: searching/similarity-search
level: intro
summary: Represents a document as the set of its contiguous k-grams so that set similarity measures resemblance.
prereqs: [jaccard-similarity]
see_also: [minhash, simhash, set-similarity-join, rabin-fingerprint, q-gram-lemma, prefix-filtering, locality-sensitive-hashing]
sources:
  - paper: doi:10.1109/SEQUEN.1997.666900
    title: Andrei Z. Broder, On the resemblance and containment of documents, Compression and Complexity of Sequences (SEQUENCES 1997)
    locator: pages 21 to 29 (the w-shingling of a document, resemblance and containment as set ratios, and their estimate by random permutations)
  - paper: doi:10.1016/S0169-7552(97)00031-7
    title: Andrei Z. Broder, Steven C. Glassman, Mark S. Manasse and Geoffrey Zweig, Syntactic clustering of the Web, Computer Networks and ISDN Systems 29(8-13), 1997
    locator: pages 1157 to 1166 (word shingles of the pages of a Web crawl, sketches of shingle fingerprints, and the clustering of near-duplicate pages)
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 3, Section 3.2, Shingling of Documents (k-shingles, the choice of k, hashing shingles, and shingles built from words)
---

Shingling turns a document into the set of its *shingles*, the contiguous substrings of a fixed length $w$, so that the similarity of two documents becomes the [Jaccard similarity](/jaccard-similarity/) of two sets. Broder introduced it for the detection of near-duplicate Web pages. The set loses the order of the shingles but keeps most local order, and a single edit changes only a few shingles. Shingling is the first step before [MinHash](/minhash/), [SimHash](/simhash/) and [set similarity joins](/set-similarity-join/).

## In plain words

Two copies of a news story often differ in a few words, a date or an advertisement. To see that they are nearly the same, cut each text into short overlapping pieces: the first five letters, then letters two to six, then letters three to seven, and so on. Each piece is a shingle. Put the pieces of each text into a bag and remove repeats.

Now compare the two bags. Count the pieces that are in both, and divide by the number of different pieces in the two bags together. Equal texts give one. Texts that share long passages give a value close to one. A change of one word only changes the few pieces that cover that word, so the value drops only a little. Texts on different topics share almost no pieces and give a value close to zero.

## When it applies

- The objects are sequences: text, source code, DNA, logs, or sequences of words or tokens.
- Two objects count as similar when they share long common passages, not only the same vocabulary.
- The similarity must survive small edits, reorderings of paragraphs and inserted or deleted blocks.
- The next step works on sets: an exact [Jaccard similarity](/jaccard-similarity/), a [MinHash](/minhash/) signature, an inverted index, or a [set similarity join](/set-similarity-join/).

## The template

Let a document be a sequence $T = t_1 t_2 \cdots t_n$ of tokens: characters, or words after a normalization. For $w \ge 1$, the **$w$-shingling** of $T$ is the set

$$S_w(T) = \{\, t_i t_{i+1} \cdots t_{i+w-1} : 1 \le i \le n - w + 1 \,\}.$$

It has at most $n - w + 1$ elements, and it is empty when $n < w$. Broder defines the **resemblance** $r_w(A, B) = J(S_w(A), S_w(B))$ and the **containment** $c_w(A, B) = |S_w(A) \cap S_w(B)| / |S_w(A)|$, which is close to 1 when $A$ is roughly a part of $B$.

```pseudo id=main
SHINGLE(T, w)                              ▷ T is a document, w the shingle length
L1  T ← NORMALIZE(T)                        ▷ hole: case, spaces, punctuation, stop words
L2  t ← TOKENIZE(T)                         ▷ hole: characters or words
L3  S ← ∅
L4  for i ← 1 to |t| − w + 1 do
L5      g ← t[i .. i + w − 1]
L6      S ← S ∪ {FINGERPRINT(g)}             ▷ hole: identity, or a hash to 32 or 64 bits
L7  return S

RESEMBLANCE(A, B, w)
L8  SA ← SHINGLE(A, w), SB ← SHINGLE(B, w)
L9  return |SA ∩ SB| / |SA ∪ SB|
```

Line L1 removes differences that should not count, such as upper and lower case or runs of spaces. Line L2 picks the token. Characters suit short texts and texts without clear words; words suit long texts and give fewer shingles. Line L6 can store the shingle itself, but most systems store a fingerprint of 32 or 64 bits, for example a [Rabin fingerprint](/rabin-fingerprint/), which can be updated in $O(1)$ time per window as in [Rabin-Karp](/rabin-karp/). Two different shingles then collide with a small probability, and this makes the resemblance slightly too high. With a hash table for $S$, SHINGLE takes $O(nw)$ time with explicit substrings and $O(n)$ expected time with a rolling fingerprint.

**Lemma (edits change few shingles).** Let $B$ come from $A$ by one substitution, insertion or deletion of a token. Then $|S_w(A) \mathbin{\triangle} S_w(B)| \le 2w$. So $e$ edits change at most $2we$ elements of the shingle set.

*Proof.* A substitution at position $i$ changes only the windows that contain position $i$; there are at most $w$ of them. Every other window of $A$ is a window of $B$ with the same content. So at most $w$ shingles of $A$ can be missing from $S_w(B)$, and at most $w$ shingles of $B$ can be missing from $S_w(A)$. An insertion between positions $i$ and $i+1$ destroys the at most $w - 1$ windows of $A$ that contain both $i$ and $i + 1$, and creates at most $w$ windows of $B$ that contain the new token; all other windows keep their content. A deletion is an insertion seen from $B$. In each case the symmetric difference has at most $2w$ elements. For $e$ edits, apply the triangle inequality of the symmetric difference, $|X \mathbin{\triangle} Z| \le |X \mathbin{\triangle} Y| + |Y \mathbin{\triangle} Z|$, $e - 1$ times. $\square$

The bound shows the trade-off in $w$. A small $w$ makes the sets robust to edits but lets unrelated documents share many shingles. A large $w$ makes shared shingles rare and meaningful, but each edit destroys more of them. Leskovec, Rajaraman and Ullman suggest $w = 5$ characters for short texts such as emails and $w = 9$ for long documents: with 27 symbols there are $27^5 = 14{,}348{,}907$ possible 5-shingles, more than the shingles of one email, so a random shingle is unlikely to occur by chance.

### Example

Let $A$ = "the cat sat on the mat" and $B$ = "the cat sat on a mat".

With words and $w = 2$, $S_2(A) = \{$the cat, cat sat, sat on, on the, the mat$\}$ and $S_2(B) = \{$the cat, cat sat, sat on, on a, a mat$\}$. They share 3 shingles out of 7, so $r_2(A, B) = 3/7 \approx 0.4286$. The single substitution of "the" by "a" changed $2 \times 2 = 4$ elements of the set, the most that the lemma allows.

| tokens | $w$ | $\lvert S_w(A) \rvert$ | $\lvert S_w(B) \rvert$ | shared | union | resemblance |
|---|---|---|---|---|---|---|
| words | 1 | 5 | 6 | 5 | 6 | 0.8333 |
| words | 2 | 5 | 5 | 3 | 7 | 0.4286 |
| words | 3 | 4 | 4 | 2 | 6 | 0.3333 |
| characters | 3 | 17 | 17 | 14 | 20 | 0.7 |
| characters | 4 | 18 | 17 | 13 | 22 | 0.5909 |
| characters | 5 | 18 | 16 | 11 | 23 | 0.4783 |

The word "the" occurs twice in $A$, so $A$ has 6 word positions but only 5 distinct 1-shingles: shingling builds a set, not a multiset. The text "mat on the sat cat the" has the same words as $A$, so its 1-shingle resemblance with $A$ is 1. Its 2-shingle resemblance with $A$ is $1/9 \approx 0.1111$: shingles with $w \ge 2$ see word order.

## Classic examples

- **Near-duplicate Web pages.** Broder, Glassman, Manasse and Zweig shingled the pages of a Web crawl by words, hashed the shingles, kept a small sketch of each page, and clustered pages of high resemblance.
- **[MinHash](/minhash/).** Shingle sets are large; MinHash compresses each one into a short signature whose agreement rate estimates the resemblance.
- **[Locality-sensitive hashing](/locality-sensitive-hashing/) for documents.** Bands of MinHash signatures of shingle sets find candidate pairs of similar documents without comparing all pairs.
- **[Set similarity join](/set-similarity-join/).** With each document as its shingle set, [prefix filtering](/prefix-filtering/) and [PPJoin](/ppjoin/) find all pairs above a Jaccard threshold.
- **[SimHash](/simhash/).** A weighted set of shingles or words becomes a 64-bit fingerprint whose Hamming distance reflects similarity.
- **Approximate string matching.** The [q-gram lemma](/q-gram-lemma/) uses the same count as the lemma above to filter strings by edit distance: strings within edit distance $e$ share many $q$-grams.

## Variations

- **Character or word shingles.** Words give shorter sets and ignore spacing; characters work for any language and catch changes inside words.
- **Multiset shingling.** Count each shingle with its multiplicity, and compare with the weighted Jaccard similarity.
- **Stop-word shingles.** For news pages, start a shingle at each stop word and take the next few words. This favors the article text over menus and advertisements, whose text has few stop words.
- **Sampling.** Keep only the shingles whose fingerprint is 0 modulo $m$, or the minimum fingerprint in each window of consecutive shingles (the minimizer or winnowing scheme). This shrinks the set and keeps a guarantee on long shared passages. See [minimizer](/minimizer/) for the same idea on DNA.
- **$k$-mers.** In bioinformatics the shingles of a DNA sequence are its $k$-mers, and tools compare genomes by MinHash of their $k$-mer sets.

## Pitfalls

- **Shingle length too small.** With $w = 1$ or 2 characters, almost all English texts share almost all shingles, and every pair looks similar. Choose $w$ so that a fixed shingle is rare in a random document of the collection.
- **No normalization.** Without line L1, a change in case, in line breaks or in HTML markup changes many shingles and hides true duplicates.
- **Multiset by accident.** Storing shingles in a list keeps repeats, and the ratio of the list sizes is no longer the Jaccard similarity. Use a set, as lines L3 and L6 do.
- **Short documents.** A document with fewer than $w$ tokens has no shingles at all, and the resemblance of two empty sets is undefined in the formula of line L9. Treat such documents apart, or pad them.
- **Too few fingerprint bits.** With 32-bit fingerprints and sets of millions of shingles, chance collisions are frequent; use 64 bits for large collections.

## Exercises

1. Show that $r_w(A, B) = 1$ does not imply $A = B$, with two different strings over the alphabet $\{a, b\}$ and $w = 2$. (Hint: "aab" and "aaab".)
2. Give two token sequences whose 1-shingle resemblance is 1 but whose 2-shingle resemblance is 0.
3. Prove that the containment $c_w(A, B)$ is 1 whenever $A$ is a contiguous part of $B$ with at least $w$ tokens.

## References
