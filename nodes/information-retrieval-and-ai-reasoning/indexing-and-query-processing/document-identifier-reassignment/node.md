---
tag: EDK0VS
kind: problem
slug: document-identifier-reassignment
name: Document identifier reassignment
aliases:
- docid reordering
- document reordering for compression
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: advanced
summary: Renumber the documents of a collection so that the gaps in the posting lists are small and the index compresses best.
prereqs: [postings-gap-encoding]
see_also: [recursive-graph-bisection-reordering, traveling-salesman-problem, minhash, graph-partitioning-problem, np-hard, webgraph-compression, partitioned-elias-fano, inverted-index]
sources:
  - paper: doi:10.1109/DCC.2002.999972
    title: Daniel Blandford and Guy Blelloch, Index compression through document reordering, Proceedings of the Data Compression Conference (DCC 2002), pages 342 to 351
    locator: the statement of the reordering problem for gap-coded indexes, and the reordering by recursive clustering of a document similarity graph
  - paper: "Wann-Yun Shieh, Tien-Fu Chen, Jean Jyh-Jiun Shann and Chung-Ping Chung, Inverted file compression through document identifier reassignment, Information Processing and Management 39(1), 2003, pages 117 to 131"
    title: Inverted file compression through document identifier reassignment
    locator: the model of reassignment as a traveling salesman tour that maximizes the similarity of consecutive documents
  - paper: "Fabrizio Silvestri, Sorting out the document identifier assignment problem, Advances in Information Retrieval, 29th European Conference on IR Research (ECIR 2007), Lecture Notes in Computer Science 4425"
    title: Sorting out the document identifier assignment problem
    locator: the assignment of ids in the lexicographic order of the URLs, and its comparison with the clustering methods
  - paper: doi:10.1145/2939672.2939862
    title: Laxman Dhulipala, Igor Kabiljo, Brian Karrer, Giuseppe Ottaviano, Sergey Pupyrev and Alon Shalita, Compressing graphs and indexes with recursive graph bisection, KDD 2016
    locator: the log-gap objective on the term-document graph, the proof that its minimization is NP-hard, and the comparison of orders on Gov2 and ClueWeb09
---

Document identifier reassignment asks for a new numbering of the documents of a collection that makes the [inverted index](/inverted-index/) as small as possible. With [postings gap encoding](/postings-gap-encoding/), each posting list is stored as the gaps between its ids, and a small gap takes few bits. So the order of the documents decides the size: if documents that share terms get close ids, the gaps of many lists shrink at the same time. The problem is to choose that order. This page states the problem and surveys the ways to attack it. One of them, [recursive graph bisection](/recursive-graph-bisection-reordering/), has its own page with the algorithm, and the codes for the gaps are on the page for gap encoding.

## In plain words

A search engine gives each document a number, and for each word it keeps the list of numbers of the documents with that word. It stores each list as the steps from one number to the next, and small steps are cheap to store. The numbers can be given out in any order. If documents about the same topic get numbers next to each other, the words of that topic have lists with small steps. The problem is to find the order of documents that makes all the lists together as cheap as possible. Finding the very best order is too hard for large collections, so real systems use good orders found by fast methods.

## Definition

The input is a collection of $n$ documents, each given as its set of terms, and a cost $\text{cost}(g)$ for a gap $g \ge 1$. A numbering is a permutation $\pi$ that gives document $v$ the id $\pi(v) \in \{1, \ldots, n\}$. For a term $t$ in the documents $D_t$, let $p_1 < p_2 < \cdots < p_k$ be the ids $\pi(D_t)$ in order, with $p_0 = 0$. The cost of $\pi$ is

$$\text{C}(\pi) = \sum_t \sum_{i=1}^{k} \text{cost}(p_i - p_{i-1}).$$

The goal is a numbering of least cost. The usual choices of the gap cost are the bit length $\lfloor \lg g \rfloor + 1$, the log-gap $\lg g$, and the true length of $g$ in a given code such as [Elias gamma coding](/elias-gamma-coding/). Equivalently, the input is the bipartite graph between terms and documents, and the output is an order of the document side.

## Variants

- **The cost of a given code.** The cost is the number of bits of the gaps under a fixed code, such as variable-byte or Simple-9. The best order can differ from code to code, because each code rounds the gap sizes in its own way.
- **Log-gap.** The cost $\lg g$ is a code-free model of the size. Dhulipala and others use it as the objective of their method.
- **Weighted terms.** Each term can be weighted, for example by how often queries read its list, so that the order favors the lists that are read most.
- **Online assignment.** Documents arrive over time, and each new one must get an id when it arrives, without renumbering the old ones.
- **Graphs.** The same question for the adjacency lists of a graph asks for an order of the vertices that makes [web graph compression](/webgraph-compression/) work best.

## Examples

Take four documents $A = \{x\}$, $B = \{y\}$, $C = \{x\}$ and $D = \{y\}$, with the bit length as the gap cost.

| order | list of $x$ | gaps | list of $y$ | gaps | bits |
|---|---|---|---|---|---|
| $A, B, C, D$ | 1, 3 | 1, 2 | 2, 4 | 2, 2 | $1 + 2 + 2 + 2 = 7$ |
| $A, C, B, D$ | 1, 2 | 1, 1 | 3, 4 | 3, 1 | $1 + 1 + 2 + 1 = 5$ |

Grouping the two documents of each term saves 2 bits, and no order gives less than 5. The list that does not hold id 1 starts at id 2 or more, which costs at least 2 bits, and each of the other three gaps costs at least 1 bit.

The toy collection of the information retrieval pages has 8 documents. Its input order costs 169 bits under the bit length cost. A search over all $8! = 40320$ orders finds a least cost of 148 bits. On this small collection, recursive graph bisection gives 178, so a fast method can do worse than doing nothing.

## Known algorithms

| method | idea | source |
|---|---|---|
| Clustering | build a similarity graph of the documents and order it by recursive clustering, so that a cluster gets a run of ids | Blandford and Blelloch, 2002 |
| Traveling salesman tour | find a path through the documents of large total similarity, with a [traveling salesman](/traveling-salesman-problem/) heuristic, and number along the path | Shieh and others, 2003 |
| URL order | sort the web pages by their URLs, so that pages of one site and one directory get close ids | Silvestri, 2007 |
| MinHash order | sort the documents by [MinHash](/minhash/) signatures, so that documents with similar term sets come close | a common baseline in later work |
| [Recursive graph bisection](/recursive-graph-bisection-reordering/) | split the documents in halves again and again, and swap documents between the halves to lower the log-gap cost | Dhulipala and others, 2016 |

None of these has a bound on its cost against the best order. They are compared by measuring index sizes on large collections. On web collections, URL order is cheap and strong, and recursive graph bisection gave smaller indexes than the other orders in the experiments of its authors.

## Bounds

- **Hardness.** Dhulipala and others show that minimizing the log-gap cost is [NP-hard](/np-hard/). So no exact method that is fast on large collections is known.
- **Every order is fairly good on long lists.** For any numbering, the $k$ gaps of a term add up to at most $n$, so by the concavity of the logarithm the term costs at most $k \lg(n/k)$ log-gap bits. A term in most documents is cheap in every order.
- **A lower bound for every order.** Each gap is at least 1, so under the bit length cost every term costs at least one bit for each of its documents, and the total is at least the number of document-term pairs.

## Reductions

- **To a tour.** If the gain is measured only between documents with consecutive ids, the problem becomes the search for a path of largest total similarity through all documents, a form of the [traveling salesman problem](/traveling-salesman-problem/). Shieh and others solve this model with tour heuristics. It is a model, not an exact reduction, because a gap can also span many ids.
- **To bisection.** Fixing which half of the ids each document gets is a balanced cut of the bipartite graph, close to the [graph partitioning problem](/graph-partitioning-problem/) but with the log-gap cost in place of the number of cut edges. Recursive bisection repeats this cut in each half.

## Applications

- **Index size.** A better order shrinks the posting lists under every gap code, and also under list codes such as [partitioned Elias-Fano](/partitioned-elias-fano/) that gain from dense runs of ids.
- **Query speed.** Smaller lists take less time to read and to decode, and clusters of ids help skips and block-based pruning.
- **Graph compression.** Orders of the vertices that put neighbors close make the adjacency lists of social and web graphs smaller.

## References
