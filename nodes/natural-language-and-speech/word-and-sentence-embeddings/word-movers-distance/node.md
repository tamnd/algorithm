---
tag: ZXZK9R
kind: algorithm
slug: word-movers-distance
name: Word mover's distance
aliases:
- WMD
area: natural-language-and-speech/word-and-sentence-embeddings
level: advanced
summary: The distance between two documents as the minimum cost to move the word embeddings of one to those of the other, an earth mover's distance.
model: real-ram
complexity:
  vars: {p: the number of distinct words in the two documents, d: the dimension of the word vectors}
  time: {exact: "O(p^3 log p)", wcd: "O(d p)", rwmd: "O(d p^2)"}
  space: {extra: "O(p^2)"}
properties: {deterministic: true, exact: true, online: false, recursive: false, supervised: false}
history:
  year: 2015
  people: [Matt J. Kusner, Yu Sun, Nicholas I. Kolkin, Kilian Q. Weinberger]
  note: Kusner, Sun, Kolkin and Weinberger applied the earth mover's distance to the bags of words of two documents with word2vec vectors as the ground space, and gave two cheap lower bounds that make nearest-neighbor search practical.
prereqs: [word-embedding, min-cost-flow-problem]
see_also: [hungarian-algorithm, assignment-problem, network-simplex, bellman-ford, k-nearest-neighbors, metric-space, bertscore, sentence-embedding]
sources:
  - paper: "Matt J. Kusner, Yu Sun, Nicholas I. Kolkin and Kilian Q. Weinberger, From word embeddings to document distances, Proceedings of the 32nd International Conference on Machine Learning, PMLR 37, 2015, pages 957 to 966"
    title: Kusner et al. 2015
    locator: the definitions of the nBOW, the travel cost and the linear program, the word centroid distance and the relaxed WMD, the prefetch and prune search, and the Obama example
  - paper: "Yossi Rubner, Carlo Tomasi and Leonidas J. Guibas, A metric for distributions with applications to image databases, ICCV 1998"
    title: Rubner, Tomasi and Guibas 1998
    locator: the earth mover's distance, and the proof that it is a metric when the ground distance is a metric
  - paper: "Ofir Pele and Michael Werman, Fast and robust earth mover's distances, ICCV 2009"
    title: Pele and Werman 2009
    locator: the fast solver whose running time Kusner et al. quote for WMD
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, theory, algorithms and applications, Prentice Hall, 1993
    locator: chapter 9, the negative cycle optimality condition and the successive shortest path algorithm
---

The word mover's distance (WMD) measures how far apart two documents are as the least total distance that the words of one document must travel in a [word embedding](/word-embedding/) to become the words of the other. Each document is a normalized bag of words, a probability distribution over its distinct words, and the cost of moving a unit of weight from one word to another is the Euclidean distance of their vectors. WMD is the earth mover's distance between the two distributions, so it is the optimum of a transportation problem, a special case of the [minimum cost flow problem](/min-cost-flow-problem/). The distance itself is exact; how well it predicts what people judge as similar documents is a measurement.

## In plain words

Think of each document as a set of piles of sand, one pile for each word, with more sand for words that occur more often. Every word has a place in space, given by its vector, and words with similar meanings are close. To turn the first document into the second, move all the sand from the piles of the first to the piles of the second. Moving sand far costs more than moving it near. WMD is the cheapest way to move it all.

"Obama speaks to the media in Illinois" and "The President greets the press in Chicago" share no word except "the" and "in", which are removed. But Obama is close to President, speaks to greets, media to press and Illinois to Chicago, so the sand moves only short distances and the two sentences come out close.

## The problem

Let a document have the distinct words $w_1, \ldots, w_m$ (after the stop words and the words without a vector are removed) with the counts $c_i$. Its normalized bag of words (nBOW) is $d_i = c_i / \sum_k c_k$. The second document has the nBOW $d'_1, \ldots, d'_n$ over its words $w'_j$. With the word vectors $x_i$ and $x'_j$, the travel cost is $c(i, j) = \|x_i - x'_j\|_2$. Then

$$\mathrm{WMD}(d, d') = \min_{T \ge 0} \sum_{i=1}^{m} \sum_{j=1}^{n} T_{ij}\, c(i, j) \quad \text{subject to} \quad \sum_j T_{ij} = d_i \ \text{for all } i, \quad \sum_i T_{ij} = d'_j \ \text{for all } j.$$

$T_{ij}$ is the amount of word $i$ that travels to word $j$. This linear program is the transportation problem: a minimum cost flow from the words of the first document to the words of the second on a complete bipartite network. The earth mover's distance has no page of its own here; WMD is its special case with word vectors as the ground space.

## The algorithm

The code solves the program exactly with successive shortest paths. The shares are rationals, so it scales them to integers first.

```pseudo id=main
WMD(doc1, doc2)
L1  d ← nBOW(doc1);  d' ← nBOW(doc2)
L2  c(i, j) ← ‖x_i - x'_j‖   for every word i of doc1 and j of doc2
L3  L ← lcm of the denominators of all d_i and d'_j;  a_i ← d_i L;  b_j ← d'_j L
L4  F ← 0
L5  while some supply a_i is not yet sent do
L6      P ← a cheapest path s → t in the residual network, by Bellman-Ford
L7      δ ← the bottleneck of P: the remaining supply, the remaining demand, or a reverse arc
L8      push δ along P
L9  return Σ_ij F_ij c(i, j) / L
```

The network has a source $s$ with an arc of capacity $a_i$ to each word $i$ of the first document, an arc of cost $c(i, j)$ and no capacity limit from each $i$ to each word $j$ of the second document, and an arc of capacity $b_j$ from $j$ to the sink $t$. The residual network also has the reverse arc $j \to i$ with cost $-c(i, j)$ wherever flow is on $i \to j$, which lets a later path undo an earlier choice. Negative arc costs are the reason for [Bellman-Ford](/bellman-ford/) in line L6; with node potentials, [Dijkstra's algorithm](/dijkstra/) works too.

**Lower bounds.** Two cheap bounds come with the method.

- **Word centroid distance (WCD).** $\|\sum_i d_i x_i - \sum_j d'_j x'_j\|_2$, the distance between the weighted means of the two documents. It costs $O(d p)$ time.
- **Relaxed WMD (RWMD).** Drop the column constraints: then each word moves all its weight to its nearest word in the other document, which gives $\ell_1 = \sum_i d_i \min_j c(i, j)$. Dropping the row constraints instead gives $\ell_2$. RWMD is $\max(\ell_1, \ell_2)$, at $O(d p^2)$ time.

**Prefetch and prune.** For the $k$ nearest documents of a query, sort the candidates by WCD, compute the exact WMD of the first $k$, and for each further candidate compute RWMD first. If RWMD is at least the current $k$-th distance, skip the exact computation.

## Example

Take the example of the paper with two dimensional vectors written for this page: Obama $(1, 0)$, President $(1.2, 0.1)$, speaks $(0, 1)$, greets $(0.2, 1.1)$, media $(-1, 0)$, press $(-1.1, -0.2)$, Illinois $(0, -1)$ and Chicago $(0.1, -1.3)$. The stop words "the", "to" and "in" are removed, so each document has four words with the share $1/4$. The travel costs are:

| | President | greets | press | Chicago |
| --- | --- | --- | --- | --- |
| Obama | 0.2236 | 1.3601 | 2.1095 | 1.5811 |
| speaks | 1.5000 | 0.2236 | 1.6279 | 2.3022 |
| media | 2.2023 | 1.6279 | 0.2236 | 1.7029 |
| Illinois | 1.6279 | 2.1095 | 1.3601 | 0.3162 |

The optimal flow sends each word to its partner on the diagonal, so $\mathrm{WMD} = (0.2236 + 0.2236 + 0.2236 + 0.3162)/4 = 0.2468$. Here every word's nearest word is its partner, so RWMD is also $0.2468$. The two centroids are $(0, 0)$ and $(0.1, -0.075)$, so WCD $= 0.125$, a weaker bound. With word2vec vectors trained on Google News, the paper gives $1.07$ for this pair of sentences.

With unequal lengths the weight splits. For "The President speaks", each of the two words gets $1/2$. The optimum sends Obama and Illinois to President, and speaks and media to speaks: $(0.2236 + 1.6279 + 0 + 1.4142)/4 = 0.8164$. Each word of the second document receives two quarters, as its share of $1/2$ requires.

## Correctness

The proof below shows that the algorithm returns the exact optimum. Scaling by $L$ turns the program into one with integer supplies and demands and does not change which $T$ is optimal. Successive shortest paths keep the invariant that the residual network has no negative cycle. The invariant holds at the start, since all costs are then at least 0. Augmenting along a shortest path keeps it, because every arc of the path has reduced cost 0 with the shortest path distances as potentials. A flow of full value with no negative residual cycle is a minimum cost flow (Ahuja, Magnanti and Orlin 1993, chapter 9). Every bottleneck is a positive integer, so the loop ends after at most $L$ rounds.

WCD is a lower bound by the triangle inequality: $\sum_i d_i x_i - \sum_j d'_j x'_j = \sum_{i,j} T_{ij}(x_i - x'_j)$ for any feasible $T$. RWMD is a lower bound because each of its two programs drops constraints. These bounds make the prefetch and prune search exact up to ties.

When both documents have $n$ distinct words with share $1/n$, the feasible set is the set of doubly stochastic matrices divided by $n$. By the Birkhoff-von Neumann theorem its vertices are the permutation matrices, so WMD is $1/n$ times the optimum of an [assignment problem](/assignment-problem/), which the [Hungarian algorithm](/hungarian-algorithm/) solves in $O(n^3)$ time. The tests check this against a brute force over all permutations.

WMD is a metric on nBOW distributions, because the earth mover's distance is a metric when the ground distance is one (Rubner, Tomasi and Guibas 1998). Two documents with the same nBOW are at distance 0, even when their word order differs.

## Complexity

The model is the [real-RAM](/real-ram/), with $p$ the number of distinct words in the two documents and $d$ the dimension of the vectors.

- **Costs.** Line L2 computes up to $p^2$ distances: $O(d p^2)$ time and $O(p^2)$ space.
- **Exact WMD.** Kusner et al. quote $O(p^3 \log p)$ as the best average time of the known solvers (Pele and Werman 2009). The code on this page is simpler: each round of Bellman-Ford costs $O(p^3)$ on the bipartite network, and there are at most $L$ rounds, where $L$ is at most the product of the two document lengths.
- **Bounds.** WCD costs $O(d p)$, or $O(d)$ per pair when the centroids are stored. RWMD costs $O(d p^2)$.
- **Search.** A nearest-neighbor search over $N$ documents computes $N$ WCDs, and RWMD and the exact WMD only for the documents that the bounds do not prune.

## Properties

- **No training.** WMD has no parameters beyond the word vectors and the stop list.
- **Metric.** It is symmetric, zero for equal nBOWs and satisfies the triangle inequality.
- **Bag of words.** Word order does not count. "Dog bites man" and "man bites dog" are at distance 0.
- **Sparse flow.** A vertex solution of the transportation problem has at most $m + n - 1$ nonzero entries, so most word pairs carry no flow.
- **Interpretable.** The flow $T$ shows which words match which.

## Variants and improvements

- **Supervised WMD.** Huang et al. 2016 learn a linear map of the word vectors and weights of the words from labeled documents, so that the distance fits the labels.
- **Entropic regularization.** Cuturi 2013 adds an entropy term to the transportation problem. Sinkhorn iterations then solve it with matrix scaling in roughly $O(p^2)$ per iteration, at the price of an approximate value.
- **Greedy matching.** Matching each word to its nearest word, which is one side of RWMD, is what [BERTScore](/bertscore/) does with contextual token vectors and cosine similarity.
- **Centroid only.** WCD alone is the distance between averaged word vectors, the simple [sentence embedding](/sentence-embedding/) baseline.

## When to use it

Use WMD to compare short texts that use different words for the same things, when good word vectors exist and the number of comparisons is small enough to afford a transportation problem for each. In the k-nearest-neighbor classification experiments of Kusner et al. on eight document data sets, WMD gave the lowest average error among the document distances they compared, such as bag of words, [tf-idf](/tf-idf/), BM25, LSI and LDA. That is a measurement on those data sets. For a large collection, compare sentence vectors with [nearest neighbor search](/nearest-neighbor-search/) first and use WMD, or RWMD, to rerank.

## Pitfalls

- **Stop words.** Without a stop list, "the", "of" and "in" take a large share of the weight and pull every pair of documents together. Remove them before line L1, as the paper does.
- **Words without vectors.** Removing them changes the nBOW. Report how many words were dropped, and handle a document with no remaining word as an error.
- **Vector length.** word2vec vectors are not unit length, and frequent words tend to have longer vectors. The Euclidean cost then mixes length and direction. Some implementations normalize the vectors first; say which form you use.
- **Floating point in the solver.** The residual network has negative arc costs, and rounding can make a zero-cost cycle look slightly negative. The code compares distances with a small tolerance, so Bellman-Ford does not loop on such cycles.
- **Ties in the pruned search.** The rule "skip when RWMD is at least the $k$-th distance" can drop a document whose WMD equals the $k$-th distance. Use a strict test if ties matter.
- **Long documents.** The cost grows about as $p^3$, so WMD is slow for long documents. Prune with the bounds, or use the entropic form.

## Implementations

The code takes the word vectors as given and implements the nBOW, an exact transportation solver by successive shortest paths on integer amounts, WCD, RWMD and the pruned nearest-neighbor search.

## History

The transportation problem goes back to Monge in 1781 and to Kantorovich and Hitchcock around 1940. Rubner, Tomasi and Guibas 1998 named the earth mover's distance and used it to compare color histograms for image retrieval. Kusner, Sun, Kolkin and Weinberger 2015 applied it to documents, with word2vec vectors as the ground space, and added the WCD and RWMD bounds for fast search. Later work learned the ground costs (Huang et al. 2016), replaced the exact solver with Sinkhorn iterations, and used contextual token vectors in place of word vectors.

## References
