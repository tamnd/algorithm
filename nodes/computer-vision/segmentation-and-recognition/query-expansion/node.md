---
tag: 9CQ57K
kind: technique
slug: query-expansion
name: Average query expansion
aliases:
- visual query expansion
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Average the representation of the query with those of top verified results and search again, which recalls views the first query missed."
prereqs: [spatial-verification, bag-of-visual-words, pseudo-relevance-feedback]
see_also: [rocchio-algorithm, relevance-feedback, stemming, image-retrieval, vlad, mean-average-precision, visual-place-recognition, vocabulary-tree]
sources:
  - paper: doi:10.1109/ICCV.2007.4408891
    title: "Ondrej Chum, James Philbin, Josef Sivic, Michael Isard and Andrew Zisserman, Total recall: automatic query expansion with a generative feature model for object retrieval, ICCV 2007"
    locator: "The query expansion methods (baseline, transitive closure, average, recursive average, multiple image resolution), the verification rule of more than 20 inliers, and the results in Table 2"
  - paper: doi:10.1109/CVPR.2012.6248018
    title: "Relja Arandjelovic and Andrew Zisserman, Three things everyone should know to improve object retrieval, CVPR 2012, 2911-2918"
    locator: "Discriminative query expansion with a linear SVM trained on the verified results, and database-side augmentation"
  - paper: doi:10.1109/TPAMI.2018.2846566
    title: "Filip Radenovic, Giorgos Tolias and Ondrej Chum, Fine-tuning CNN image retrieval with no human annotation, IEEE Transactions on Pattern Analysis and Machine Intelligence 41(7), 2019, 1655-1668"
    locator: "Alpha query expansion: the weighted average of the top global descriptors with weights given by the similarity raised to the power alpha"
  - book: isbn:9780521865715
    title: "Christopher D. Manning, Prabhakar Raghavan and Hinrich Schutze, Introduction to Information Retrieval, Cambridge University Press, 2008"
    locator: "Chapter 9, Relevance feedback and query expansion (the Rocchio algorithm, pseudo relevance feedback and global methods of query expansion)"
---

In text search, query expansion adds terms to a query so that it also finds documents that use other words for the same thing: synonyms from a thesaurus, word forms from [stemming](/stemming/), or terms of the top results, as in the [Rocchio algorithm](/rocchio-algorithm/) and [pseudo relevance feedback](/pseudo-relevance-feedback/). Average query expansion is the visual form of this idea (Chum et al. 2007). Search with the query image, check the top results with [spatial verification](/spatial-verification/), and keep those that pass. Map their features into the frame of the query, average their [bag of visual words](/bag-of-visual-words/) vectors with the query vector, and search again with the average. The verified results show the object from other views and under other light, so the new query also finds images that share few words with the original one. The gain is a benchmark result, not a theorem.

## In plain words

A photo of a building shows only one side, at one time of day. Many other photos of the same building share few details with it. The first search finds the photos that look most like the query. Some of them are clearly the same building, because their details line up with the query when the image is moved and stretched.

These sure results show the building a bit differently, so they contain details that the query lacks. Mix them with the query into a richer query and search again. The second search reaches photos that the first one missed.

## When it applies

- The search has a high precision at the top: the first few verified results are almost always correct. Spatial verification gives this for rigid objects such as buildings.
- The queries have many relevant images in the database, as for landmarks. With one relevant image, there is nothing to add.
- Representations can be averaged: bag of words histograms, [VLAD](/vlad/) vectors or other global descriptors.
- A second search is affordable. The cost is about one more query.

## The template

```pseudo id=main
AVERAGE-QE(q, m, R, t_min)               ▷ q: the query region of an image
L1  L ← the ranked list of SEARCH(the vector d_0 of q)
L2  V ← the images among the top R of L with at least t_min inliers, with their maps T_i
L3  if V is empty then return L
L4  keep the first m images of V, in the order of L
L5  for each kept image d_i do
L6      d_i ← the vector of the inlier features of d_i mapped into q by T_i, inside the query region
L7  d_avg ← (d_0 + d_1 + ... + d_m) / (m + 1)
L8  return the ranked list of SEARCH(d_avg), verified again
```

Line L2 is the step that makes the method work: only verified results are added. Line L6 is the back-projection of Chum et al.: each result contributes only the features that its transformation $T_i$ maps into the query region, so the background of the result does not enter the query. Chum et al. use $m < 50$ and count an image as verified when it has more than 20 inliers.

**Example.** Take raw counts over 4 words and the cosine score. The query is $d_0 = (1, 1, 0, 0)$, and the verified results are $(1, 1, 1, 0)$ and $(0, 1, 1, 0)$. Then $d_{\text{avg}} = (2, 3, 2, 0) / 3$. The image $e = (0, 0, 1, 0)$ shows a part of the object that the query does not show. Its cosine with $d_0$ is 0, and its cosine with $d_{\text{avg}}$ is $2 / \sqrt{17} = 0.485$. The image $f = (1, 0, 0, 1)$ shares one word with the query, and its cosine drops from $0.5$ to $2 / (\sqrt{17} \sqrt 2) = 0.343$. So $e$ moves above $f$ after the expansion.

## Classic examples

Chum et al. (2007) compared several strategies on Oxford 5K plus 100,000 images from Flickr (104,844 images), with mean average precision over the 55 queries (Table 2). That is a benchmark result.

| Method | What it adds | mAP |
|---|---|---|
| original query | nothing | 55.0 |
| query expansion baseline | the top 5 results, not verified | 52.9 |
| transitive closure | each verified result is a new query, until no new image passes | 63.5 |
| average query expansion | the average of the query and its verified results | 71.1 |
| recursive average | average expansion repeated, until more than 30 images are verified | 75.2 |
| multiple resolution | average expansion separately for verified results at larger, equal and smaller scale | 78.2 |

The baseline, which adds the top results without verification, lowers the score: pseudo relevance feedback needs a precise top of the list. The multiple resolution method splits the verified results into three bands of the relative scale, $(0, 4/5)$, $(2/3, 3/2)$ and $(5/4, \infty)$, and runs one expanded query for each band, so that zoomed in and zoomed out views give their own queries.

## Variations

- **Discriminative query expansion** (Arandjelovic and Zisserman 2012). Train a linear classifier (a [support vector machine](/support-vector-machine/)) with the verified results as positive examples and low ranked images as negative examples, then rank the database by its score. It costs about as much as the average and was better in their tests.
- **Database-side augmentation** (same paper). Before any query, replace each database vector by the average of itself and its verified neighbors in the database. The work moves offline.
- **Alpha query expansion** (Radenovic et al. 2019). For global descriptors from a network, average the top $n$ results with the weight $s_i^{\alpha}$, where $s_i$ is the similarity to the query. This needs no spatial verification, at the price of trusting the top results.
- **Text query expansion.** Thesaurus terms, stemming, and the terms of the top documents (Manning et al. 2008, Chapter 9). Here no geometric test exists, so the expansion relies on the precision of the first results.

## Pitfalls

- **Query drift.** One false positive in $V$ adds the features of another object to the query, and the second search returns more images of that object. Use a strict inlier threshold and verify again after the second search.
- **No verified results.** For hard queries, $V$ is empty and the expansion does nothing. The method helps most where the first search is already good.
- **Background in the average.** Without back-projection into the query region, each result adds its whole image, including the sky, the street and other buildings.
- **Repeated averaging without normalization.** Vectors of different lengths must be normalized before or after the average, or images with many features dominate it.
- **Evaluation leaks.** If the query image itself is in the database, it is always verified and added. That is harmless for the average, but it must not be counted as a retrieved result.

## Exercises

1. In the example, add idf weights for a database of 10 images in which the four words appear in 5, 8, 2 and 6 images. Compute the cosines of $e$ and $f$ with $d_0$ and with $d_{\text{avg}}$ again.
2. Show that if the verified results are copies of the query, $d_{\text{avg}} = d_0$, and the expansion changes nothing.
3. A false positive with 25 inliers enters $V$ with $m = 5$. Its vector has no word in common with $d_0$. By what factor does the weight of the query words in $d_{\text{avg}}$ drop?
4. Explain why the transitive closure in the table can reach images that average query expansion misses, and why it scores lower anyway.

## References
