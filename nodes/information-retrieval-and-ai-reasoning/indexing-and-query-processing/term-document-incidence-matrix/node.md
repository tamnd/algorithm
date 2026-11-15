---
tag: Q35WK6
kind: definition
slug: term-document-incidence-matrix
name: Term-document incidence matrix
aliases:
- term-document matrix
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: intro
summary: A 0-1 matrix with a row for each term and a column for each document, set where the term occurs in the document.
prereqs: [bit-vector]
see_also: [posting-list, inverted-index, boolean-retrieval-model, posting-list-intersection, bitmap-index, sparse-matrix, vector-space-model, latent-semantic-analysis]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 1, Section 1.1 (the term-document incidence matrix, Boolean queries as bitwise operations on its rows, and the size of the matrix for a large collection)
  - book: isbn:9781558605701
    title: Ian H. Witten, Alistair Moffat and Timothy C. Bell, Managing Gigabytes, second edition, Morgan Kaufmann, 1999
    locator: Chapter 3 (indexing, with bitmaps and inverted files as two ways to store the same term-document relation)
---

The term-document incidence matrix of a collection is the 0-1 matrix with one row for each term and one column for each document, whose entry is 1 exactly when the term occurs in the document. Each row is a [bit vector](/bit-vector/) that gives the set of documents of a term, so a Boolean query is a bitwise expression over rows. The matrix is the model behind the [Boolean retrieval model](/boolean-retrieval-model/). For a real collection it is almost all zeros, so engines store each row as a [posting list](/posting-list/) of its 1 positions, which is an [inverted index](/inverted-index/).

## Definition

Let $D = (d_1, \ldots, d_N)$ be a collection of $N$ documents, each a sequence of terms, and let $V = (t_1, \ldots, t_M)$ be its vocabulary: the $M$ distinct terms that occur in at least one document, after the same tokenization for all documents. The **term-document incidence matrix** is the matrix $A \in \{0, 1\}^{M \times N}$ with

$$A_{ij} = \begin{cases} 1 & \text{if } t_i \text{ occurs in } d_j, \\ 0 & \text{otherwise,} \end{cases} \qquad 1 \le i \le M,\ 1 \le j \le N.$$

The row $A_{i\cdot}$ is the incidence vector of term $t_i$, and the number of 1s in it is the document frequency $\mathrm{df}_{t_i}$. The column $A_{\cdot j}$ is the set of terms of $d_j$, with no count and no order. The number of 1s in $A$ is the number of postings $\sum_i \mathrm{df}_{t_i}$, which is at most the number of tokens.

A Boolean query maps to bit operations on rows: $t \text{ AND } u$ is $A_{t\cdot} \wedge A_{u\cdot}$, $t \text{ OR } u$ is $A_{t\cdot} \vee A_{u\cdot}$, and NOT $t$ is the complement $\neg A_{t\cdot}$, with all operations bitwise over the $N$ columns. The documents that match are the columns with a 1 in the result.

## Examples and non-examples

**A toy collection.** The toy collection of the information retrieval pages has $N = 8$ short documents and $M = 50$ terms, so $A$ has $400$ entries. Exactly $74$ of them are 1, so $18.5\%$ of the matrix is set. Five rows, with the columns $d_1$ to $d_8$ from left to right:

| term | $d_1$ | $d_2$ | $d_3$ | $d_4$ | $d_5$ | $d_6$ | $d_7$ | $d_8$ |
|---|---|---|---|---|---|---|---|---|
| sorted | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 |
| array | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| search | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| posting | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 |
| list | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |

The query sorted AND array AND NOT search is the bitwise expression $11010001 \wedge 11000001 \wedge \neg 10000010 = 11010001 \wedge 11000001 \wedge 01111101 = 01000001$. The 1s are in columns 2 and 8, so the answer is $\{d_2, d_8\}$. Document $d_1$ holds all three terms, and the NOT removes it. The query sorted OR search gives $11010011$, the documents $\{1, 2, 4, 7, 8\}$.

The row of "sorted" has a 1 in column 2 although $d_2$ ("merge sort merges two sorted runs into one sorted array") holds the term twice. The matrix records only that the term occurs, not how often.

**A large collection.** Manning, Raghavan and Schuetze take a collection of one million documents with 500,000 distinct terms. The matrix has $5 \times 10^{11}$ entries. With about 1000 tokens in each document, at most $10^9$ entries are 1, so at least $99.8\%$ of the entries are 0. Such a matrix is never stored in full. Its rows are kept as sorted lists of the column numbers of their 1s, which are the posting lists.

**Non-example: the term-document count matrix.** The matrix with entry $\mathrm{tf}_{t,d}$, the number of times $t$ occurs in $d$, is not an incidence matrix: its entry for "sorted" and $d_2$ is 2. The weighted matrix with tf-idf entries of the [vector space model](/vector-space-model/), and the matrix that [latent semantic analysis](/latent-semantic-analysis/) factors, are not 0-1 either. The name "term-document matrix" often means one of these weighted matrices.

**Non-example: a phrase.** The incidence matrix cannot answer the [phrase query](/phrase-query/) "list sorted". The rows of "list" and "sorted" have a common 1 only in column 4, but $d_4$ is "a posting list is a sorted list of document ids", where "list" is never right before "sorted". The matrix has lost the order of the words; a [positional index](/positional-index/) keeps it.

## Related definitions

- **Posting list.** The [posting list](/posting-list/) of $t_i$ is the sorted list of the column numbers $j$ with $A_{ij} = 1$, the sparse form of row $i$. Its length is $\mathrm{df}_{t_i}$.
- **Inverted index.** The set of all rows in posting list form, with a dictionary from terms to rows, is an [inverted index](/inverted-index/). The columns in sparse form are a forward index.
- **Document-term matrix.** The transpose $A^{\mathsf T}$, with documents as rows, is the same relation in the other orientation.
- **Bitmap index.** A database [bitmap index](/bitmap-index/) is the same idea for the values of a column of a table: one bit vector for each value.
- **Sparse matrix.** Posting lists are the compressed sparse row form of $A$ as a [sparse matrix](/sparse-matrix/).
- **Posting list intersection.** The AND of two rows, computed on their sparse forms, is the [posting list intersection](/posting-list-intersection/) problem.

## References
