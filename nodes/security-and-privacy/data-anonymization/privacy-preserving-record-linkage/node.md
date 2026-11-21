---
tag: KHENH3
kind: algorithm
slug: privacy-preserving-record-linkage
name: Privacy-preserving record linkage with Bloom filters
aliases:
- Bloom filter record linkage
- PPRL
area: security-and-privacy/data-anonymization
level: advanced
summary: Encodes the q-grams of each identifier into a keyed Bloom filter and links records across parties by the Dice similarity of the filters.
model: word-ram
complexity:
  vars: {n: the records of the first party, r: the records of the second party, l: the longest identifier, q: the q-gram length, k: the number of hash functions, m: the filter length in bits, w: the word size}
  time: {worst: O((n + r) l (q + k) + n r m / w)}
  space: {extra: O((n + r) m / w)}
history:
  year: 2009
  people: [Rainer Schnell, Tobias Bachteler, Joerg Reiher]
  note: "Schnell, Bachteler and Reiher proposed Bloom filters of q-grams with keyed hash functions for linkage of medical records in 2009. Later work found attacks on the encoding and proposed hardening methods."
prereqs: [bloom-filter, hmac, entity-resolution]
see_also: [fellegi-sunter-model, pseudonymization, jaccard-similarity, minhash, edit-distance, private-set-intersection, secure-multiparty-computation, linkage-attack]
sources:
  - paper: doi:10.1186/1472-6947-9-41
    title: "Rainer Schnell, Tobias Bachteler and Joerg Reiher, Privacy-preserving record linkage using Bloom filters, BMC Medical Informatics and Decision Making 9, article 41, 2009"
    locator: "the encoding of padded bigrams into a Bloom filter by double hashing with HMAC-SHA1 and HMAC-MD5, the Dice coefficient of filters, the worked example with 2 hash functions and 30 bits, and the evaluation on simulated and real data"
  - paper: doi:10.1016/j.is.2012.11.005
    title: "Dinusha Vatsalan, Peter Christen and Vassilios S. Verykios, A taxonomy of privacy-preserving record linkage techniques, Information Systems 38(6), 2013"
    locator: "pp. 946 to 969, the parties, the adversary models and the classes of PPRL techniques"
  - paper: doi:10.29012/jpc.764
    title: "Anushka Vidanage, Thilina Ranbaduge, Peter Christen and Rainer Schnell, A taxonomy of attacks on privacy-preserving record linkage, Journal of Privacy and Confidentiality 12(1), 2022"
    locator: the classes of published attacks on PPRL encodings and the conditions they need
  - paper: doi:10.1145/362686.362692
    title: "Burton H. Bloom, Space/time trade-offs in hash coding with allowable errors, Communications of the ACM 13(7), 1970"
    locator: "pp. 422 to 426, the Bloom filter"
  - paper: doi:10.1002/rsa.20208
    title: "Adam Kirsch and Michael Mitzenmacher, Less hashing, same performance, building a better Bloom filter, Random Structures and Algorithms 33(2), 2008"
    locator: "pp. 187 to 218, bit positions by double hashing g_i = h_1 + i h_2 and its false positive rate"
---

Two data owners, such as a hospital and a cancer registry, want to find the records that belong to the same person, but they may not share names or birth dates. Exact pseudonyms do not work, because names are often misspelled and one wrong letter changes a keyed hash completely. The method of Schnell, Bachteler and Reiher (2009) encodes each identifier as a [Bloom filter](/bloom-filter/): it splits the identifier into q-grams, such as the bigrams of a name, and sets $k$ bits of an $m$-bit vector for each q-gram, at positions from [HMAC](/hmac/) under keys that only the data owners know. Similar names share most q-grams, so their filters share most bits. A third party, the linkage unit, receives only the filters and compares every pair by the Dice coefficient $2 |a \wedge b| / (|a| + |b|)$. It reports the pairs at or above a threshold. The method is fast and tolerant of errors. It is not secure in a cryptographic sense: the encoding is deterministic, and published attacks recover q-grams from the filters through their frequencies.

## In plain words

Two offices each have a list of people. They want to know which people are on both lists, but neither may show its names. Names are also typed with mistakes, so "Smith" and "Smyth" should still match.

Each office cuts every name into pairs of letters. For each pair, a secret rule that both offices share picks a few boxes in a long row, and the office ticks them. It sends only the rows of ticks to a third office. Names that look alike have most letter pairs in common, so their rows have most ticks in the same boxes. The third office counts the shared ticks for every pair of rows and reports the pairs that share enough. It never sees a name, and without the secret rule it cannot directly check a guessed name. But the ticks still carry patterns, so the rows must be protected too.

## The problem

Party $A$ holds records $a_1, \ldots, a_n$ and party $B$ holds records $b_1, \ldots, b_r$, each with an identifier such as a name. The goal is the set of pairs $(i, j)$ that refer to the same person, with errors in the identifiers allowed. A linkage unit $C$ does the comparison. The usual adversary model, as in the taxonomy of Vatsalan, Christen and Verykios (2013), is honest-but-curious: $C$ follows the protocol but tries to learn identifiers from what it receives. $A$ and $B$ share the keys $K_1, K_2$ and the parameters, and $C$ does not know the keys.

The output is a list of candidate pairs with their similarity. Deciding which candidates are true matches is the usual record linkage problem of [entity resolution](/entity-resolution/), for example with the [Fellegi-Sunter model](/fellegi-sunter-model/) on several fields. The threshold $\theta$, the filter length $m$ and the number of hash functions $k$ are chosen by the users. Schnell et al. use 30 bits and 2 hash functions in their worked example and fix no threshold.

## The algorithm

Lines L1 to L5 run at each data owner, on its own records. Lines L6 to L10 run at the linkage unit, which sees only the filters.

```pseudo id=main
PPRL-LINK(A, B, K1, K2, k, m, q, theta)
L1  for each record x of A and of B, at its owner, compute F_x as follows
L2      G ← the q-grams of NORMALIZE(x), padded with q - 1 blanks on each side
L3      F_x ← m zero bits
L4      for each g in G and each i in 0 .. k - 1 do
L5          set bit (h1(g) + i · h2(g)) mod m of F_x, where h1 = HMAC-SHA1 under K1 and h2 = HMAC-MD5 under K2
L6  M ← an empty list
L7  for each pair (a, b) in A × B do
L8      s ← 2 |F_a ∧ F_b| / (|F_a| + |F_b|)
L9      if s ≥ theta then append (a, b, s) to M
L10 return M
```

Line L5 is double hashing. Kirsch and Mitzenmacher (2008) showed that, for set membership, it has the same asymptotic false positive rate as $k$ independent hash functions. The pad at line L2 marks the first and last letters, so the bigram "_s" says that a name starts with "s".

## Example

Take $q = 2$, $k = 2$, $m = 30$, the made-up keys `demo-key-1` and `demo-key-2`, and the names smith, smyth and jones. The bigrams and their positions are:

| name | bigrams and bit positions | bits set |
|---|---|---|
| smith | _s: 15, 4; sm: 12, 12; mi: 18, 0; it: 9, 4; th: 5, 20; h_: 8, 20 | 0, 4, 5, 8, 9, 12, 15, 18, 20 |
| smyth | _s: 15, 4; sm: 12, 12; my: 7, 22; yt: 11, 19; th: 5, 20; h_: 8, 20 | 4, 5, 7, 8, 11, 12, 15, 19, 20, 22 |
| jones | _j: 26, 4; jo: 23, 22; on: 14, 16; ne: 6, 9; es: 9, 28; s_: 21, 9 | 4, 6, 9, 14, 16, 21, 22, 23, 26, 28 |

- smith and smyth share 4 of their 6 bigrams each, so the Dice coefficient of the bigram sets is $8 / 12 = 2/3$. Their filters have 9 and 10 bits and share 6, so the Dice coefficient of the filters is $12 / 19 \approx 0.63$.
- smith and jones share no bigram, but their filters share bits 4 and 9 by collision, and their Dice coefficient is $4 / 19 \approx 0.21$. smyth and jones share bits 4 and 22 and get $4 / 20 = 1/5$.
- With $\theta = 3/5$, the linkage of smith and jones against smyth and Jones returns (smith, smyth) with $12/19$ and (jones, Jones) with 1, because the normalization at line L2 changes "Jones" to lower case.
- With $m = 1000$ and $k = 15$, the same keys give $61/89 \approx 0.69$ for smith and smyth and $22/177 \approx 0.12$ for smith and jones. A longer filter has fewer collisions.

The bigram "sm" sets one bit only, because its $h_2$ is a multiple of 30. Bits 4 and 20 are each set by two bigrams of smith. The test file checks all these values.

## Correctness

The filter of an identifier is the union of the positions of its q-grams, so it depends only on the set of q-grams. Equal normalized identifiers give equal filters with Dice coefficient 1. Every q-gram that two identifiers share contributes the same bits to both filters, so shared q-grams always give shared bits. Collisions can add more shared bits, so the Dice coefficient of the filters is an estimate of the Dice coefficient of the q-gram sets, never below what the shared q-grams give. The linkage loop compares each pair once and returns exactly the pairs at or above $\theta$. If the keyed hash functions are pseudorandom, a party without the keys cannot compute the filter of a guessed name. The full proof is in proofs/correctness.md.

## Complexity

Let $n$ and $r$ be the numbers of records, $l$ the length of the longest identifier, $q$ the q-gram length, $k$ the number of hash functions, $m$ the filter length and $w$ the word size of the [word RAM](/word-ram/).

- Encoding one identifier takes $O(l\, q)$ time for the q-grams and $O(l\, k)$ for the bit positions, counting one HMAC call as one step, so $O((n + r)\, l\, (q + k))$ in all.
- One Dice coefficient takes $O(m / w)$ word operations, with a population count per word. The full comparison of all pairs takes $O(n\, r\, m / w)$.
- The filters need $O((n + r)\, m / w)$ words.

The comparison of all pairs dominates for large files. In practice, blocking reduces it: only pairs that agree on a coarse key, or whose filters fall into the same bucket of a [MinHash](/minhash/) style index, are compared. Blocking can miss true matches, and its loss is a measured property.

## Properties

- **Error tolerance.** One wrong letter changes at most $q$ q-grams, so similar strings get similar filters. How the filter Dice tracks the q-gram Dice depends on $m$, $k$ and the length of the identifiers, and it is measured on data.
- **One-sided error from collisions.** Shared q-grams always give shared bits. Collisions only add shared bits, so the filter Dice is never lower than the part due to shared q-grams. This is a theorem.
- **No exact privacy guarantee.** The linkage unit cannot compute the filter of a guessed identifier without the keys. This is a theorem if HMAC is a pseudorandom function. It does not mean that the filters hide the identifiers: the encoding is deterministic, and the frequencies of bit patterns follow those of q-grams. The attacks on this are published, as the taxonomy of Vidanage, Ranbaduge, Christen and Schnell (2022) describes.
- **The linkage unit learns the similarity of every pair.** This is part of the output, and it is leaked by design.

## Variants and improvements

- **Record-level filters.** Encode several fields, such as first name, last name and birth date, into one filter, with a separate key or a different $k$ for each field. It gives one similarity per record, and as a heuristic it makes frequency analysis harder than one filter per field.
- **Hardening.** Later work adds random noise to the bits, balances the number of 1 bits between filters, or folds a filter onto itself by XOR. Each method trades linkage quality for resistance to some attacks; the taxonomy of attacks discusses which attack each one stops.
- **Other similarities.** The [Jaccard similarity](/jaccard-similarity/) $J = |a \wedge b| / |a \vee b|$ satisfies $J = D / (2 - D)$ for the Dice coefficient $D$, so it ranks the pairs in the same order. The [Hamming distance](/hamming-distance/) gives the same order only for filters with equal numbers of 1 bits.
- **Cryptographic protocols.** For exact matching on equal pseudonyms, [private set intersection](/private-set-intersection/) or [secure multiparty computation](/secure-multiparty-computation/) give proved security. Protocols for approximate matching with proved security usually cost much more than Bloom filter encodings.
- **Without a linkage unit.** In two-party variants, one data owner compares the filters. That party then holds both filters and the keys, so the protection is weaker.

## When to use it

Use Bloom filter linkage when two or more data owners must link records with typing errors, under a legal setting that forbids sharing identifiers with the linkage unit, and when the cost of a cryptographic protocol is too high for the size of the files. Use the [Fellegi-Sunter model](/fellegi-sunter-model/) or a classifier on the similarity of several fields to decide matches. Do not treat the filters as anonymous data. They need the same access control as pseudonymized identifiers, and the linkage unit must be trusted not to attack them. If exact matching on clean identifiers is enough, use keyed [pseudonymization](/pseudonymization/) or a set intersection protocol instead.

## Pitfalls

- **A filter that is too short at line L3.** With few bits, unrelated names share many bits by collision, as smith and jones do in the example with 30 bits, and the threshold must rise until true matches with errors fail it.
- **$h_2$ that is a multiple of $m$ at line L5.** All $k$ positions of that q-gram are then the same bit, as for "sm" in the example. This weakens the filter for that q-gram. A safer form maps $h_2$ to a value in $1, \ldots, m - 1$ first.
- **Missing normalization at line L2.** Case, spaces, accents and the order of name parts change the q-grams. Agree on one normalization for all parties.
- **One filter per field with the same key everywhere.** A filter of a single common field, such as a first name, repeats across many records, and its frequency then matches the frequency of the name in the population. Use record-level encodings, field-specific keys and hardening.
- **Reusing the keys across projects.** Filters from two projects with the same keys can be joined by anyone who holds both. Use new keys for each project.
- **Treating the threshold as a privacy parameter.** $\theta$ trades false matches against missed matches. It has no effect on privacy, and its value is a choice tested on data.

## Implementations

## History

Burton Bloom introduced the Bloom filter in 1970 for set membership with a small rate of false positives. Linkage on encrypted or hashed identifiers needs exact agreement of the identifiers. Schnell, Bachteler and Reiher (2009) proposed Bloom filters of bigrams with keyed double hashing, in the form of Kirsch and Mitzenmacher, to allow errors, and evaluated the linkage quality on simulated and real data. Vatsalan, Christen and Verykios (2013) placed the method in a taxonomy of PPRL techniques. Since then, several attacks on Bloom filter encodings and several hardening methods have been published, and Vidanage et al. (2022) gave a taxonomy of the attacks.

## References
