---
tag: 3CNTQG
kind: technique
slug: product-quantization
name: Product quantization
aliases:
- PQ
area: searching/similarity-search
level: advanced
summary: Splits vectors into subvectors, quantizes each with its own codebook, and compares codes by table lookup.
prereqs: [vector-quantization, k-means, nearest-neighbor-search]
see_also: [vector-quantization, k-means, inverted-file-index, approximate-nearest-neighbor, maximum-inner-product-search, hnsw, diskann, euclidean-distance]
sources:
  - paper: doi:10.1109/TPAMI.2010.57
    title: Hervé Jégou, Matthijs Douze and Cordelia Schmid, Product quantization for nearest neighbor search, IEEE Transactions on Pattern Analysis and Machine Intelligence 33(1), 2011
    locator: pages 117 to 128 (Section 2, product quantizers; Section 3, symmetric and asymmetric distance computation and their error bounds; Section 4, the inverted file with residual encoding, IVFADC)
  - paper: doi:10.1109/18.720541
    title: Robert M. Gray and David L. Neuhoff, Quantization, IEEE Transactions on Information Theory 44(6), 1998
    locator: pages 2325 to 2383 (vector quantization, the Lloyd conditions, and product codes among the structured quantizers)
  - paper: "Tiezheng Ge, Kaiming He, Qifa Ke and Jian Sun, Optimized product quantization for approximate nearest neighbor search, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2013)"
    locator: pages 2946 to 2953 (a rotation of the space learned together with the codebooks to lower the quantization error)
---

Product quantization compresses vectors of $\mathbb{R}^d$ into short codes and estimates [Euclidean distances](/euclidean-distance/) between a query and the compressed vectors by table lookups. The space is split into $m$ blocks of $d/m$ coordinates, and each block gets its own codebook of $k^*$ centroids, found by [k-means](/k-means/). A vector is stored as the $m$ indices of the nearest centroid in each block: $m \log_2 k^*$ bits, 64 bits for the common choice $m = 8$, $k^* = 256$. The codes describe $(k^*)^m$ reconstruction points while the codebooks store only $k^* d$ numbers. At query time a table of $m k^*$ partial distances is computed once, and then each stored vector costs $m$ lookups and additions. The estimate is off by at most the quantization error $\|x - Q(x)\|$ of the stored vector. Jégou, Douze and Schmid introduced the method for nearest neighbor search in 2011.

## In plain words

Storing a billion long lists of numbers in memory is too costly. Product quantization stores each list as a few small labels instead.

Cut every list into, say, eight pieces. For each piece position, find 256 typical pieces in the data. Now describe each list by naming, for each of its eight pieces, the typical piece it is closest to. Eight names from 256 choices fit in eight bytes.

To find the stored lists closest to a query, cut the query into the same eight pieces, and for each piece position measure its distance to each of the 256 typical pieces once. That makes a small table. The distance from the query to a stored list is then about the sum of eight entries of the table, one per piece, which is very fast to add up.

## When it applies

- The vectors live in $\mathbb{R}^d$ with $d$ in the tens to the thousands, and the distance is the Euclidean distance or the inner product.
- There are too many vectors to keep at full precision in memory, or the scan must be faster than full distance computations.
- Approximate distances are acceptable, or the best few candidates can be re-ranked with the exact vectors kept on disk.
- A sample of the data is available to train the codebooks, and the data that comes later resembles it.

## The template

Write $x = (x^1, \ldots, x^m)$ with $x^j \in \mathbb{R}^{d/m}$ the $j$-th block of coordinates. A **product quantizer** is $Q(x) = (Q_1(x^1), \ldots, Q_m(x^m))$, where $Q_j$ maps a block to the nearest of its centroids $C_j[1], \ldots, C_j[k^*]$. Its code is the tuple of indices $(c_1(x), \ldots, c_m(x))$. Since the blocks use disjoint coordinates,

$$\|q - Q(x)\|^2 = \sum_{j=1}^{m} \|q^j - C_j[c_j(x)]\|^2.$$

```pseudo id=main
TRAIN(X, m, k*)                             ▷ X is a training sample
L1  split every x in X into its m blocks x^1, ..., x^m of d/m coordinates
L2  for j ← 1 to m do C_j ← KMEANS({x^j : x ∈ X}, k*)          ▷ hole: k-means, or a rotation first

ENCODE(x)
L3  for j ← 1 to m do c_j ← the index of the centroid of C_j nearest to x^j
L4  return (c_1, ..., c_m)

SEARCH(q, codes, k)                         ▷ asymmetric distance computation, ADC
L5  for j ← 1 to m and i ← 1 to k* do T[j][i] ← ‖q^j − C_j[i]‖²
L6  for each stored code c do D(c) ← T[1][c_1] + ... + T[m][c_m]
L7  return the k codes with the smallest D        ▷ hole: re-rank them with exact vectors
```

Line L5 computes $m k^*$ block distances, $k^* d$ arithmetic operations in all, once per query. Line L6 then costs $m$ lookups per stored vector, against $d$ multiplications for an exact distance. The query is not quantized; only the stored vectors are. This is the *asymmetric* distance $\tilde d(q, x) = \|q - Q(x)\|$. The *symmetric* distance $\|Q(q) - Q(x)\|$ also quantizes the query, so that the tables can be precomputed between centroids, at the price of a larger error.

**Error bound.** For every $q$ and $x$, $|\tilde d(q, x) - \|q - x\|| \le \|x - Q(x)\|$, by the triangle inequality applied to $q$, $x$ and $Q(x)$. The symmetric distance satisfies $|\|Q(q) - Q(x)\| - \|q - x\|| \le \|x - Q(x)\| + \|q - Q(q)\|$ in the same way. These are exact bounds for each pair; they do not depend on the data distribution. In particular, if $x^*$ is the true nearest neighbor of $q$ and $x$ is the vector that SEARCH ranks first, then $\|q - x\| \le \|q - x^*\| + \|x - Q(x)\| + \|x^* - Q(x^*)\|$, so the answer is off by at most twice the largest quantization error.

**Why the product.** A single k-means quantizer with $2^{64}$ centroids would match 64-bit codes but cannot be trained or stored. The product of $m$ quantizers with $k^*$ centroids each has $(k^*)^m$ reconstruction points, $2^{64}$ for $m = 8$ and $k^* = 256$, and costs $k^* d$ numbers to store and $O(k^* d)$ operations to encode a vector.

### Example

Take $d = 4$ and $m = 2$ blocks of two coordinates, with $k^* = 2$ centroids per block, as if trained on a larger sample: $C_1 = \{(1, 1), (8, 8)\}$ and $C_2 = \{(6, 2), (1, 7)\}$. Each code is 2 bits.

| vector | $x$ | code | $Q(x)$ | $\lVert x - Q(x) \rVert$ | $\lVert q - x \rVert^2$ | ADC $\lVert q - Q(x) \rVert^2$ | SDC |
|---|---|---|---|---|---|---|---|
| a | (1, 2, 6, 1) | (1, 1) | (1, 1, 6, 2) | 1.4142 | 18 | 18 | 0 |
| b | (2, 1, 7, 2) | (1, 1) | (1, 1, 6, 2) | 1.4142 | 26 | 18 | 0 |
| c | (8, 9, 1, 7) | (2, 2) | (8, 8, 1, 7) | 1 | 111 | 98 | 148 |
| d | (9, 8, 2, 8) | (2, 2) | (8, 8, 1, 7) | 1.7321 | 121 | 98 | 148 |
| e | (0, 1, 1, 6) | (1, 2) | (1, 1, 1, 7) | 1.4142 | 22 | 28 | 50 |
| f | (8, 7, 6, 3) | (2, 1) | (8, 8, 6, 2) | 1.4142 | 78 | 88 | 98 |

For the query $q = (2, 2, 2, 2)$, line L5 gives $T[1] = (2, 72)$, from $\|(2, 2) - (1, 1)\|^2 = 2$ and $\|(2, 2) - (8, 8)\|^2 = 72$, and $T[2] = (16, 26)$. Then $D(a) = T[1][1] + T[2][1] = 18$, $D(e) = 2 + 26 = 28$, and so on. ADC ranks $a$ and $b$ first, tied at 18, then $e$, $f$, and $c$ and $d$ tied. The true order is $a, e, b, f, c, d$. The true nearest neighbor $a$ is ranked first, and every estimate obeys the bound: for $b$, $|\sqrt{18} - \sqrt{26}| = 0.8564 \le 1.4142$. The query itself quantizes to the code $(1, 1)$, so the symmetric distance (SDC) gives 0 for both $a$ and $b$, coarser than ADC.

## Classic examples

- **IVFADC (Jégou et al.).** A coarse k-means quantizer with $k'$ cells sends each vector to an [inverted file](/inverted-file-index/) list; the residual $x - c(x)$ from its cell centroid is encoded by a product quantizer. A query visits the $w$ nearest cells and scans their lists with ADC on its own residuals. On collections of millions of vectors it answers in milliseconds with codes of 8 to 16 bytes per vector.
- **Re-ranking.** Search the compressed codes for a few hundred candidates and compute exact distances for those, reading the full vectors from disk. This is the usual pattern in large retrieval systems.
- **Graph indexes on compressed vectors.** [DiskANN](/diskann/) keeps product quantization codes in memory to guide the traversal of a graph stored on disk, and reads full vectors only to re-rank; [HNSW](/hnsw/) indexes are often combined with PQ codes to save memory.
- **[Maximum inner product search](/maximum-inner-product-search/).** The inner product also splits over blocks, $\langle q, Q(x) \rangle = \sum_j \langle q^j, C_j[c_j(x)] \rangle$, so the same tables, filled with inner products, score items for recommendation or retrieval.

## Variations

- **Optimized product quantization.** Rotate the space before splitting it, with an orthogonal matrix learned together with the codebooks, so that the blocks carry balanced variance and are less correlated. This lowers the quantization error at the same code length.
- **Additive and residual quantization.** Use $m$ codebooks over the full space and sum the chosen centroids, $Q(x) = \sum_j C_j[c_j]$. The error is lower than with blocks, but encoding becomes a hard search, and the distance needs cross terms between codebooks.
- **Fast scan.** With $k^* = 16$, each code is 4 bits and each table fits in a SIMD register, so the sums of line L6 run 16 or 32 at a time.
- **Anisotropic losses.** For inner product search, weight the error parallel to $x$ more than the error orthogonal to it, since only the first changes the ranking much; the codebooks are then trained with this loss instead of k-means.
- **Scalar quantization.** The case of one coordinate per block, with $k^*$ levels per coordinate. It is simple and fast, but needs more bits for the same error.

## Pitfalls

- **Unbalanced blocks.** If most of the variance sits in a few coordinates, contiguous blocks give some codebooks all the information and others none. Permute or rotate the coordinates first, as optimized PQ does.
- **Ties and coarse ranks.** Many stored vectors share a code, as $a$ and $b$ do above, and ADC cannot separate them. Re-rank the top candidates with exact distances when the order matters.
- **Training on unrepresentative data.** Codebooks learned on one distribution give large errors on another, and the error bound grows with $\|x - Q(x)\|$. Retrain when the data changes.
- **Quantizing the query.** The symmetric distance is simpler to precompute, but its error bound adds the query's error, and it ranks worse. Use ADC unless the queries are themselves stored codes.
- **Too many centroids.** The tables of line L5 cost $k^* d$ operations per query; with $k^* = 2^{16}$ this dominates the scan of small lists.

## Exercises

1. Prove the error bound $|\|q - Q(x)\| - \|q - x\|| \le \|x - Q(x)\|$, and show that it is tight by an example in $\mathbb{R}^1$.
2. Show that $\|q - Q(x)\|^2 = \sum_j \|q^j - Q_j(x^j)\|^2$ fails for additive quantization, and write the cross terms.
3. With $d = 128$, $m = 8$ and $k^* = 256$, count the operations of lines L5 and L6 for one query over $n = 10^6$ codes, and compare with the exact scan.
4. In the example, which single change to $C_2$ would make ADC rank $e$ before $b$?

## References
