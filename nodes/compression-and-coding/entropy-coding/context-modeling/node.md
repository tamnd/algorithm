---
tag: SDA0PS
kind: concept
slug: context-modeling
name: Context modeling
aliases:
- context-based coding
area: compression-and-coding/entropy-coding
level: advanced
summary: Predict each symbol from the symbols just before it by keeping one adaptive model per context. Longer contexts predict better but learn more slowly.
prereqs: [adaptive-modeling]
see_also: [prediction-by-partial-matching, context-tree-weighting, context-mixing, cabac, conditional-entropy, entropy-rate, markov-chain, burrows-wheeler-transform]
sources:
  - paper: doi:10.1109/TIT.1981.1056282
    title: Jorma Rissanen and Glen G. Langdon, Universal modeling and coding, IEEE Transactions on Information Theory 27(1), 12-23, 1981
    locator: the split of a compressor into a model and a coder, and the models with finite contexts
  - book: isbn:9780139119910
    title: Timothy C. Bell, John G. Cleary and Ian H. Witten, Text Compression, Prentice Hall, 1990
    locator: the chapters on finite-context models, blending and escapes
  - paper: doi:10.1109/TCOM.1984.1096090
    title: John G. Cleary and Ian H. Witten, Data compression using adaptive coding and partial string matching, IEEE Transactions on Communications 32(4), 396-402, 1984
    locator: the blending of contexts of different orders with escapes
  - paper: doi:10.1109/18.382012
    title: Frans M. J. Willems, Yuri M. Shtarkov and Tjalling J. Tjalkens, The context-tree weighting method, basic properties, IEEE Transactions on Information Theory 41(3), 653-664, 1995
    locator: tree sources and the weighting of all context trees up to a depth
  - paper: "Giovanni Manzini, An analysis of the Burrows-Wheeler transform, Journal of the ACM 48(3), 407-430, 2001"
    locator: the definition of the empirical entropy of order k of a string
---

Context modeling predicts each symbol of a sequence from the symbols just before it, its *context*. A model of order $k$ keeps a separate [adaptive model](/adaptive-modeling/) for each string of $k$ symbols, and to code the next symbol it uses the model of the $k$ symbols just coded. The decoder knows these symbols too, so it picks the same model. In English text, the letter after "q" is almost always "u", and an order-1 model learns this, while an order-0 model gives "u" its average rate everywhere. Context modeling is the modeling half of the split of a compressor into a model and a coder, set out by Rissanen and Langdon (1981). With an [arithmetic coder](/arithmetic-coding/) as the coder, the compression depends only on how well the contexts predict.

## In plain words

To guess the next letter, look at the letters just before it. After "th" the next letter is likely "e"; after "q" it is almost always "u". A context model keeps a separate tally of next letters for each short run of letters that has come before, and uses the tally of the current run to guess.

Longer runs give sharper guesses, but there are many more of them, and each tally fills up slowly. A tally that has seen only a few cases guesses badly. So a model that looks back too far spends most of its time learning. Good compressors look back a long way when the tally there has seen enough, and fall back to a shorter run when it has not.

## The idea

**Order-$k$ models.** Write $x_1 \ldots x_n$ for the sequence over an alphabet of $\sigma$ symbols. An order-$k$ model gives symbol $x_i$ the probability $P(x_i \mid x_{i-k} \ldots x_{i-1})$, taken from the counts of the symbols that have followed this context so far. Near the start, where fewer than $k$ symbols precede, it uses the shorter context. The code length is $\sum_i \lg(1/P(x_i \mid \text{context}))$. If the source is a [Markov chain](/markov-chain/) of order $k$, the order-$k$ model learns its transition probabilities, and the length per symbol tends to the [entropy rate](/entropy-rate/) of the source, the [conditional entropy](/conditional-entropy/) of a symbol given the $k$ before it.

**Empirical entropy.** For a given sequence, the best order-$k$ model chosen after seeing the whole sequence gives the length $n H_k$, where $H_k$ is the empirical entropy of order $k$: the average over the contexts $w$ of the order-0 entropy of the symbols that follow $w$, weighted by the number of times $w$ occurs. $H_0 \ge H_1 \ge H_2 \ge \cdots$, because a longer context can only split the counts further. Bounds of the form $n H_k + o(n)$ are the standard yardstick for compressors and for compressed data structures, for example those built on the [Burrows-Wheeler transform](/burrows-wheeler-transform/).

**Dilution against prediction.** A larger $k$ lowers $H_k$, but an adaptive model has to learn each context, and an order-$k$ model has up to $\sigma^k$ of them. By the bounds for [adaptive models](/adaptive-modeling/), each context that occurs $m$ times costs about $\tfrac{\sigma - 1}{2} \lg m$ bits more than its share of $n H_k$. The total length is therefore about
$$n H_k + \sum_{w} \tfrac{\sigma - 1}{2} \lg m_w,$$
which grows with $k$ once the contexts are too many for the data. The best fixed order grows only like $\log n / \log \sigma$. On short inputs a low order wins; on long ones a higher order wins. This trade-off is the central problem of context modeling, and the main methods answer it in different ways:

- **Blending and escapes.** [PPM](/prediction-by-partial-matching/) starts at the longest context that has been seen and escapes to shorter ones when the symbol is new there, so it uses a long context only where it has data.
- **Weighting.** [Context tree weighting](/context-tree-weighting/) takes a Bayesian mixture over all tree-shaped sets of contexts up to a depth $D$. Its length is within a known bound of the best such tree for the sequence.
- **Mixing.** [Context mixing](/context-mixing/) runs many models with different contexts and combines their predictions with weights that it learns online.
- **Selecting contexts by hand.** In images and video, the context is a small set of nearby values chosen by design. JBIG uses a template of 10 neighbor pixels, 1024 contexts, for a binary image, and [CABAC](/cabac/) gives each bin of a video syntax element a context chosen from the neighboring blocks. JPEG-LS quantizes local gradients into 365 contexts so that each context sees enough data.

**Tree sources.** A context need not have a fixed length. In a tree source the set of contexts is a suffix-free set of strings of different lengths, so that, for example, "after a 1 the next bit is random; after 00 it is 0; after 10 it is 1". Such a source has few parameters even when some contexts are long. PPM*, CTW and the algorithm Context of Rissanen (1983) all aim at such variable-length contexts, and a [suffix tree](/suffix-tree/) of the text so far stores all contexts at once.

## Examples

**Order 1 on alternating bits.** The sequence $0101\ldots01$ of length 1000 costs about 1000 bits under an order-0 model, because 0 and 1 are equally common. An order-1 model has two contexts, "after 0" and "after 1", and each sees only one value. With the KT estimator, each context costs about $\tfrac12 \lg 500 + 1$ bits, so the whole sequence costs under 20 bits.

**The right order on a Markov source.** The implementation draws a random Markov source of order 2 over 4 symbols, with an entropy rate of 1.225 bits per symbol, and codes samples with order-$k$ models using the KT estimator. In bits per symbol:

| $k$ | 0 | 1 | 2 | 3 | 4 | 6 | 8 |
|---|---|---|---|---|---|---|---|
| $n = 50000$, adaptive | 1.987 | 1.783 | 1.231 | 1.237 | 1.252 | 1.324 | 1.481 |
| $n = 50000$, $H_k$ | 1.986 | 1.781 | 1.225 | 1.223 | 1.219 | 1.184 | 1.066 |
| $n = 1000$, adaptive | 1.987 | 1.796 | 1.353 | 1.443 | 1.572 | 1.808 | 1.944 |
| $n = 1000$, $H_k$ | 1.973 | 1.749 | 1.217 | 1.167 | 1.077 | 0.707 | 0.304 |

Order 2 is best in both rows, and on 50000 symbols it is within 0.01 bits of the entropy rate. The empirical entropy $H_k$ keeps falling as $k$ grows, but for $k$ above 2 the drop is overfitting: at $n = 1000$ the order-8 model has few repeats of each context, $H_8$ is 0.30, and the adaptive coder pays 1.94 bits per symbol, almost as much as order 0.

## Where it is used

Context models are the basis of the strongest general-purpose compressors: PPM in PPMd and the RAR and 7-Zip formats, context mixing in PAQ and its successors, and CTW in research. LZMA codes its literals with a context of the previous byte and the position. The [Burrows-Wheeler transform](/burrows-wheeler-transform/) gathers the symbols that share a context, which is why bzip2 gets close to the compression of a context model with only simple coding after the transform. Image and video standards use contexts chosen by design: JBIG and JBIG2 for binary images, JPEG-LS for lossless images, and [CABAC](/cabac/) in H.264 and HEVC. The same idea, under the name of $n$-gram models, was the standard language model in speech recognition before neural models.

## References
