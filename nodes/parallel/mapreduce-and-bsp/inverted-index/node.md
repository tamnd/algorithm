---
tag: GZMPCF
kind: problem
slug: inverted-index
name: Inverted index construction
aliases:
- building an inverted index
- posting lists construction
- inverted indexing
area: parallel/mapreduce-and-bsp
level: core
summary: Build, for every term of a document collection, the sorted list of documents (and positions) that contain it, here as a MapReduce job.
prereqs: [mapreduce-model, word-count, secondary-sort]
see_also: [shuffle-phase, partitioner, variable-byte-encoding, elias-gamma-coding, golomb-coding, delta-encoding, document-listing, data-skew]
sources:
  - book: isbn:9781608453429
    title: Jimmy Lin and Chris Dyer, Data-Intensive Text Processing with MapReduce, Morgan and Claypool, 2010
    locator: Chapter 4, Sections 4.2 (inverted indexes), 4.3 (baseline implementation), 4.4 (revised implementation) and 4.5 (index compression, with 4.5.1 byte-aligned and word-aligned codes, 4.5.2 bit-aligned codes and 4.5.3 postings compression)
  - paper: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, 6th Symposium on Operating Systems Design and Implementation (OSDI), 2004"
    locator: Section 2.3 (the inverted index example, map emits word and document ID, reduce sorts the IDs) and Section 6.1 (large-scale indexing)
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 4 (index construction, including distributed indexing with MapReduce) and Chapter 5 (index compression)
---

Inverted index construction is the problem of computing, for each term of a document collection, its **posting list**: the documents that contain the term, in increasing document number, each with its term frequency and, for a positional index, the positions of the term. It is the main data structure of text search. In the [MapReduce model](/mapreduce-model/), Dean and Ghemawat give it as an example (Section 2.3): map emits (word, document id), and reduce sorts the ids. Lin and Dyer (Chapter 4) show that this baseline runs out of memory for frequent terms and fix it with the [value-to-key conversion](/secondary-sort/), which also lets the reducer compress the postings as it writes them.

## In plain words

The index at the back of a book lists, for each important word, the pages where it appears. A search engine needs the same thing for every word of millions of documents. To build it with many computers, each computer reads some documents and writes a note for each word it sees: the word, the document number, and where in the document the word is. The system sends all notes for the same word to one computer, which puts them in document order and stores the list. Common words have very long lists, so the computer must not hold a whole list in memory to sort it. The fix is to let the system sort the notes on the way. The lists are also stored in a compact form, by keeping only the jumps from one document number to the next.

## Definition

**Input.** Documents $d_0, d_1, \dots, d_{D-1}$, numbered $0$ to $D - 1$, each a sequence of terms. Let $N$ be the total number of tokens.

**Output.** For each term $t$ that occurs, the posting list

$$\text{post}(t) = \big[(d, \text{tf}(t, d), [p_1 < p_2 < \dots < p_{\text{tf}}]) : t \text{ occurs in } d\big],$$

sorted by increasing $d$, where $\text{tf}(t, d)$ is the number of occurrences of $t$ in $d$ and the $p_i$ are their positions. The **document frequency** $\text{df}(t)$ is the length of $\text{post}(t)$. Let $P = \sum_t \text{df}(t)$ be the number of postings, so $P \le N$.

**Cost model.** The [MapReduce model](/mapreduce-model/) with $M$ map tasks and $R$ reduce tasks: rounds, pairs and bytes in the [shuffle](/shuffle-phase/), the largest reducer input, and the memory of a reduce task. On one machine, time in the word RAM.

## Variants

- **Non-positional index.** Each posting is $(d, \text{tf})$ or only $d$. The output and the shuffle are smaller, and phrase queries are not possible.
- **Document-partitioned index.** Each machine builds a full index of its own documents and a query goes to all machines. This needs no shuffle at all, and each map task writes the index of its split.
- **Term-partitioned index.** Each machine holds the full posting lists of some terms. This is what the MapReduce job of this page builds, with the [partitioner](/partitioner/) deciding which terms go to which output file.
- **Compressed index.** The posting lists are stored as gaps between document numbers, coded with an integer code (Lin and Dyer, Section 4.5).

## Examples

Take three documents: $d_0$ = "the cat sat", $d_1$ = "the dog", $d_2$ = "the cat and the dog", with positions counted from 0.

| term | posting list |
|---|---|
| and | $(2, 1, [2])$ |
| cat | $(0, 1, [1]),\ (2, 1, [1])$ |
| dog | $(1, 1, [1]),\ (2, 1, [4])$ |
| sat | $(0, 1, [2])$ |
| the | $(0, 1, [0]),\ (1, 1, [0]),\ (2, 2, [0, 3])$ |

The baseline job sends one pair per token, 10 pairs. The value-to-key job sends one pair per posting, 9 pairs, since "the" occurs twice in $d_2$. The gaps of the document numbers of "the" are $1, 1, 1$ (counting from $-1$, so that every gap is at least 1). With a [variable-byte code](/variable-byte-encoding/), each number below 128 takes one byte, so the list of "the" (gap, frequency, position gaps for each posting) is the 10 numbers 1, 1, 1, 1, 1, 1, 1, 2, 1, 3 in 10 bytes.

**A larger run.** Take 500 documents of 200 tokens each, with terms drawn from a Zipf law with exponent 1 over 5,000 terms, $M = 10$ and $R = 8$. There are $N = 100{,}000$ tokens and $P = 63{,}867$ postings over 4,855 distinct terms. The most frequent term occurs in all 500 documents, 11,212 times.

| | baseline | value-to-key |
|---|---|---|
| pairs sent | 100,000 | 63,867 |
| largest reducer input (pairs) | 21,032 | 8,403 |
| largest buffer in a reducer | all values of one term | one posting |

Stored with 4-byte integers (document number, frequency and each position), the index takes 910,936 bytes. With gaps and a variable-byte code, it takes 252,835 bytes. The 63,867 document gaps alone take 67,860 bytes in variable-byte and 407,797 bits (about 6.4 bits per gap) in the [Elias gamma code](/elias-gamma-coding/).

## Known algorithms

**One machine.** Read the documents in increasing order of $d$ and append each posting to the list of its term in a hash table. The lists come out sorted without a sort, so the time is $O(N)$ expected. When the index does not fit in memory, build sorted partial indexes of blocks of documents and merge them, as in [external merge sort](/external-merge-sort/). Manning, Raghavan and Schuetze (Chapter 4) describe a blocked sort-based method and a single-pass in-memory method.

**MapReduce baseline (Dean and Ghemawat, Section 2.3; Lin and Dyer, Section 4.3).** Map reads a document $d$ and emits $(t, (d, p))$ for each token, or $(t, (d, \text{tf}))$ once per distinct term. The [shuffle](/shuffle-phase/) groups by term. Reduce buffers all values of $t$, sorts them by $d$, and writes the list. The values of a key arrive in no fixed order, so the sort is needed, and it needs memory for $\text{df}(t)$ postings. For a frequent term, $\text{df}(t)$ is close to $D$, which can be far more than the memory of one task.

**MapReduce with value-to-key conversion (Lin and Dyer, Section 4.4).** Map emits one pair $((t, d), (\text{tf}, [p_1, \dots]))$ for each term and document. The partitioner uses only $t$, and the sort is by $(t, d)$, so all postings of $t$ reach one reduce task and arrive in increasing $d$, see [secondary sort](/secondary-sort/). Reduce writes each posting as it arrives, as a gap from the previous $d$, and needs $O(1)$ memory besides the output buffer.

**Compression (Lin and Dyer, Section 4.5).** Store the [differences](/delta-encoding/) $d_i - d_{i-1}$ (d-gaps) instead of the numbers, since the gaps of a frequent term are small. Code them with a byte-aligned code such as the [variable-byte code](/variable-byte-encoding/), or with a bit-aligned code: the [Elias gamma code](/elias-gamma-coding/) uses $2\lfloor \log_2 g \rfloor + 1$ bits for a gap $g \ge 1$, and a [Golomb code](/golomb-coding/) with a parameter proportional to $D/\text{df}(t)$ suits the gaps of a term whose documents are spread at random. The Golomb parameter needs $\text{df}(t)$ before the first posting, which Lin and Dyer (Section 4.5.3) obtain with the order inversion pattern: the mappers also emit partial counts under a special key $(t, *)$ that sorts before every document.

## Bounds

- **One machine.** Any algorithm reads the $N$ tokens and writes the $P$ postings and their $N$ positions, so $\Omega(N)$ time is needed, and the hash table method reaches $O(N)$ expected time.
- **Rounds.** One round suffices, as both MapReduce algorithms show.
- **Communication.** Every posting of $t$ is in the output of the task that owns $t$, so the shuffle carries all postings and positions, $\Omega(P + N)$ numbers for a positional index. The baseline sends $N$ pairs and the value-to-key job sends $P$ pairs, with the same numbers in total.
- **Largest reducer input.** The task that owns the most frequent term receives at least $\max_t \text{df}(t)$ postings, which is up to $D$. This is [data skew](/data-skew/) that no partitioner on whole terms can remove. A document-partitioned index avoids it.
- **Reducer memory.** $\Theta(\max_t \text{df}(t))$ for the baseline and $O(1)$ for value-to-key conversion.

## Reductions

- [Word count](/word-count/) is the special case that keeps only $\sum_d \text{tf}(t, d)$ for each term, so its plan is the same with a [combiner](/combiner/) in place of the list.
- Building a posting list is a group-by-term followed by a sort by document, so it reduces to sorting the pairs $(t, d)$, which is what the [shuffle](/shuffle-phase/) does.
- [Document listing](/document-listing/) answers, for a pattern, the set of documents that contain it. For a single term, it is the posting list.

## Applications

- Web search and enterprise search, where the index is rebuilt in batches. Dean and Ghemawat (Section 6.1) report that Google's indexing system was rewritten as a sequence of MapReduce jobs.
- Phrase and proximity queries, which need the positions.
- The first step of computing term weights such as tf-idf, which need $\text{tf}(t, d)$ and $\text{df}(t)$.

## References
