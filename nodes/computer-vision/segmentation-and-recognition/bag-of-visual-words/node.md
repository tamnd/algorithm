---
tag: YRDC42
kind: model
slug: bag-of-visual-words
name: Bag of visual words
aliases:
- bag of features
- Video Google model
area: computer-vision/segmentation-and-recognition
level: core
summary: "Quantize local descriptors to a vocabulary of k-means centers and represent an image by its histogram of visual words, searched with an inverted file."
history:
  year: 2003
  people: [Josef Sivic, Andrew Zisserman, Gabriella Csurka, Christopher Dance]
  note: "Sivic and Zisserman (Video Google, ICCV 2003) built the model for object retrieval in films, with k-means words, tf-idf weights, a stop list and an inverted file. Csurka et al. (2004) used the same histogram for image categorization with a classifier."
prereqs: [k-means, tf-idf, feature-descriptor]
see_also: [image-retrieval, inverted-index, vocabulary-tree, vlad, fisher-vector, spatial-pyramid-matching, spatial-verification, vector-space-model]
sources:
  - paper: doi:10.1109/ICCV.2003.1238663
    title: "Josef Sivic and Andrew Zisserman, Video Google: a text retrieval approach to object matching in videos, Ninth IEEE International Conference on Computer Vision (ICCV 2003), vol. 2, 1470-1477"
    locator: "Section 3 (the vocabulary by k-means, about 6k Shape Adapted and 10k Maximally Stable clusters), Section 4 (tf-idf weights and ranking by the normalized scalar product), Section 6.1 (stop list)"
  - paper: doi:10.1109/CVPR.2007.383172
    title: "James Philbin, Ondrej Chum, Michael Isard, Josef Sivic and Andrew Zisserman, Object retrieval with large vocabularies and fast spatial matching, CVPR 2007"
    locator: "Section 2 (the Oxford buildings data set and the tf-idf baseline), Section 3 (approximate k-means for vocabularies of up to 1M words)"
  - paper: doi:10.1109/CVPR.2006.68
    title: "Svetlana Lazebnik, Cordelia Schmid and Jean Ponce, Beyond bags of features: spatial pyramid matching for recognizing natural scene categories, CVPR 2006, vol. 2, 2169-2178"
    locator: "Section 3.1 (histogram intersection; level 0 of the pyramid is the bag of words)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.1, Instance recognition, and Section 6.2, Image classification"
  - book: isbn:9780521865715
    title: "Christopher D. Manning, Prabhakar Raghavan and Hinrich Schutze, Introduction to Information Retrieval, Cambridge University Press, 2008"
    locator: "Chapter 6, Scoring, term weighting and the vector space model"
---

The bag of visual words model represents an image by how often each entry of a fixed vocabulary of local appearances occurs in it, and it forgets where in the image these appearances are. Each local [feature descriptor](/feature-descriptor/) is replaced by the index of its nearest center from a [k-means](/k-means/) clustering, so an image becomes a sparse histogram over $K$ visual words. With [tf-idf](/tf-idf/) weights and an [inverted index](/inverted-index/), a large image collection is then searched like a text collection. This page is the representation and its score; the task it serves is [image retrieval](/image-retrieval/), and the [vocabulary tree](/vocabulary-tree/), [VLAD](/vlad/) and the [Fisher vector](/fisher-vector/) are later ways to build or replace the histogram.

## The machine

**Vocabulary.** Take a training set of local descriptors in $\mathbb{R}^D$ (for example SIFT, $D = 128$). Run [k-means](/k-means/) on them to get $K$ centers $c_1, \ldots, c_K$. Each center is a *visual word*. The vocabulary is built once and is then fixed.

**Quantizer.** A descriptor $x$ goes to its nearest center,
$$q(x) = \arg\min_{k} \lVert x - c_k \rVert_2,$$
with ties broken by the smaller index. The cells $\{x : q(x) = k\}$ are the Voronoi cells of the centers.

**Image vector.** An image $d$ with descriptors $x_1, \ldots, x_{n_d}$ becomes the count vector $h_d \in \mathbb{N}^K$, $h_d(k) = \lvert \{ j : q(x_j) = k \} \rvert$. The positions of the features are not part of the vector. That is the "bag".

**Weights.** For a database of $N$ images, let $N_k$ be the number of images that contain word $k$ at least once. The tf-idf weight of word $k$ in image $d$ is
$$t_d(k) = \frac{h_d(k)}{n_d} \, \log \frac{N}{N_k}.$$
This is the form of Sivic and Zisserman (Section 4), who write the denominator of the idf as the number of occurrences of the word in the database; most later systems use the document frequency $N_k$, as here. A *stop list* removes the most frequent words, and Video Google also removes the rarest ones (the top 5 percent and the bottom 10 percent of words on their data, Section 6.1). Both are tuned choices.

**Score.** A query image $q$ is scored against image $d$ by the cosine of the angle between the weighted vectors,
$$s(q, d) = \frac{\langle t_q, t_d \rangle}{\lVert t_q \rVert_2 \, \lVert t_d \rVert_2},$$
and the database is ranked by decreasing $s$. For unit vectors this ranking is the same as ranking by increasing Euclidean distance, because $\lVert a - b \rVert^2 = 2 - 2 \langle a, b \rangle$. Other scores are in use: the $L_1$ distance of $L_1$ normalized vectors (the [vocabulary tree](/vocabulary-tree/)), and histogram intersection $\sum_k \min(h_q(k), h_d(k))$ for classification ([spatial pyramid matching](/spatial-pyramid-matching/)).

**Index.** An [inverted index](/inverted-index/) stores, for each word $k$, the list of pairs $(d, h_d(k))$ with $h_d(k) > 0$. A query reads only the lists of the words it contains and adds the products $t_q(k) \, t_d(k)$ into one accumulator per image. Images that share no word with the query keep the score 0 and are never touched.

## What it counts

The model predicts that two images show the same object when many of their local features fall into the same Voronoi cells, with rare cells counted more. The plain count has an exact meaning: $\langle h_q, h_d \rangle = \sum_k h_q(k) \, h_d(k)$ is the number of pairs (query feature, database feature) that have the same word. Histogram intersection counts the pairs of a one-to-one matching within words instead. So the bag of words is a fast stand-in for [feature matching](/feature-matching/), where "the same word" replaces "nearest neighbor within a ratio test".

The fit of the vocabulary minimizes the k-means quantization error $\sum_x \lVert x - c_{q(x)} \rVert^2$ over the training descriptors. This is not the retrieval quality. A vocabulary with a lower error does not always give a better ranking, and $K$ is chosen by measuring retrieval on a ground truth set, as in both Video Google and Philbin et al.

**Worked example.** Take $K = 4$ words and $N = 3$ images with counts $h_1 = (2, 1, 0, 0)$, $h_2 = (0, 1, 1, 0)$, $h_3 = (1, 0, 0, 3)$. The document frequencies are $N_k = (2, 2, 1, 1)$, so $\log(N / N_k) = (0.4055, 0.4055, 1.0986, 1.0986)$. A query with counts $(1, 1, 0, 0)$ has $t_q = (0.2027, 0.2027, 0, 0)$. The weighted vectors of the images are $t_1 = (0.2703, 0.1352, 0, 0)$, $t_2 = (0, 0.2027, 0.5493, 0)$ and $t_3 = (0.1014, 0, 0, 0.8240)$. The cosine scores are 0.9487, 0.2448 and 0.0863. Without weights they are 0.9487, 0.5000 and 0.2236: the rare word 3 of image 2 and the rare word 4 of image 3 are not in the query, and the idf makes them pull those images further away. The inverted lists are word 1: $(1, 2), (3, 1)$; word 2: $(1, 1), (2, 1)$; word 3: $(2, 1)$; word 4: $(3, 3)$. The query reads the lists of words 1 and 2, that is 4 postings. The count $\langle h_q, h_1 \rangle = 3$ is the number of same-word pairs: the query feature of word 1 pairs with two features of image 1, and the query feature of word 2 pairs with one.

## Relation to other models

- **Text retrieval.** The model is the [vector space model](/vector-space-model/) of text with words replaced by Voronoi cells of descriptors. Tf-idf, stop lists, [cosine similarity](/cosine-similarity/) and inverted files carry over without change. Text words come with the language, but visual words come from a clustering, so their number and their boundaries are free parameters.
- **Larger vocabularies.** The [vocabulary tree](/vocabulary-tree/) of Nister and Stewenius (2006) and the approximate k-means of Philbin et al. (2007) make $K$ of the order of $10^6$ affordable. The quantizer then costs much less than $K D$ per descriptor, at the price of an approximate nearest center.
- **Richer statistics per word.** [VLAD](/vlad/) keeps, for each word, the sum of the residuals $x - c_k$, and the [Fisher vector](/fisher-vector/) keeps first and second order statistics under a Gaussian mixture. Both give dense vectors of size $K D$ or $2 K D$ with a small $K$, where the bag of words gives a sparse vector with a large $K$.
- **Layout.** [Spatial pyramid matching](/spatial-pyramid-matching/) adds coarse positions by counting words in grid cells. [Spatial verification](/spatial-verification/) checks the geometry of the matched features after the bag of words ranking.
- **Classification.** Csurka et al. (2004) feed the histogram to a naive Bayes model or a [support vector machine](/support-vector-machine/). Here the histogram is a feature vector, and no inverted file is used.

## Known results in the model

- **Exact facts.** The inner product of count vectors equals the number of same-word pairs, and histogram intersection equals the size of a largest one-to-one matching that pairs only features with the same word (in each word, $\min(a, b)$ pairs is the most that can be formed). The inverted index returns the same scores as a full scan over all $N$ images, because the terms it skips are products with a zero factor.
- **Query cost.** With the index, a query costs one quantization per query feature plus the total length of the posting lists of its words. Without the index it costs $O(N K)$ for dense vectors. A stop list exists mostly to cut the long posting lists of frequent words. The saving depends on the word statistics, so it is a measured property, not a bound.
- **Quantization loses information.** Two descriptors close to a cell boundary can get different words, and two far apart descriptors in one large cell get the same word. Larger $K$ reduces the second error and increases the first. Soft assignment to several near words is one fix.
- **Benchmark results.** On the Oxford buildings set (5,062 images, 55 queries, mean average precision), Philbin et al. (CVPR 2007, Section 3) report 0.618 for a 1M-word vocabulary built with approximate k-means against 0.439 for the best hierarchical vocabulary they tried, and a lower value for 20K words. Video Google used about 6,000 and 10,000 words for its two region types, chosen on a ground truth set of film frames. These numbers depend on the descriptors, the data and the version of the benchmark.
- **No spatial information.** Two images with the same features in a different layout get the same vector. This is the reason for [spatial verification](/spatial-verification/) in retrieval and for [spatial pyramid matching](/spatial-pyramid-matching/) in classification.

## References
