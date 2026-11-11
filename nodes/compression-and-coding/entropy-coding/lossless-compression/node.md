---
tag: DRHZ6Y
kind: problem
slug: lossless-compression
name: Lossless data compression
aliases:
- lossless coding
area: compression-and-coding/entropy-coding
level: intro
summary: Map data to a shorter bit string so that a decoder gets back the exact original, with a length close to the information content of the data.
prereqs: [shannon-entropy]
see_also: [source-coding-theorem, incompressibility-argument, arithmetic-coding, huffman-coding, dictionary-based-compression, burrows-wheeler-transform, kolmogorov-complexity, lossy-compression]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: Claude E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 379-423, 1948
    locator: the entropy of a source and the coding theorem for noiseless channels
  - paper: doi:10.1109/TIT.1981.1056282
    title: Jorma Rissanen and Glen G. Langdon, Universal modeling and coding, IEEE Transactions on Information Theory 27(1), 12-23, 1981
    locator: the split of a compressor into a model and a coder
  - paper: doi:10.1109/TIT.1984.1056936
    title: Jorma Rissanen, Universal coding, information, prediction, and estimation, IEEE Transactions on Information Theory 30(4), 629-636, 1984
    locator: the lower bound of about one half lg n bits for each parameter on the redundancy of universal codes
  - paper: doi:10.1145/76894.76896
    title: Timothy Bell, Ian H. Witten and John G. Cleary, Modeling for text compression, ACM Computing Surveys 21(4), 557-591, 1989
    locator: the survey of models for text and the Calgary corpus used to compare them
  - paper: doi:10.1109/DCC.1997.582019
    title: Ross Arnold and Timothy Bell, A corpus for the evaluation of lossless compression algorithms, Data Compression Conference, 201-210, 1997
    locator: the design of the Canterbury corpus
  - url: https://sun.aei.polsl.pl/~sdeor/index.php?page=silesia
    title: Sebastian Deorowicz, The Silesia corpus
    locator: the files of the Silesia corpus and their kinds
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, 2nd edition, Wiley, 2006
    locator: the chapters on data compression and on universal source coding
---

Lossless data compression asks for a way to write data as a shorter string of bits from which a decoder gets back the data exactly. No method can shrink every input, so the problem is to shrink the inputs that are likely or that have structure, by a model of the data. For a random source, the expected length of a code is at least the [entropy](/shannon-entropy/) of the source, and good methods come close to it. Rissanen and Langdon split every compressor into a *model*, which gives probabilities to what comes next, and a *coder*, which turns those probabilities into bits. Since arithmetic coding solves the coding part almost exactly, most of the work in the field is in the models.

## In plain words

A compressor takes a file and writes a shorter file. A decompressor takes the shorter file and gives back the first one, every bit the same. Text, program code and pictures with large plain areas have patterns, and a compressor uses the patterns to write them in fewer bits.

No compressor can make every file shorter. There are fewer short files than long ones, so some file must stay the same size or grow. Files of random bytes are of this kind: they have no pattern to use.

So each compressor makes a bet about what data are likely. One counts how often each letter appears, one looks for repeated pieces, and one predicts each letter from the letters before it. The better the bet fits the data, the shorter the output.

## Definition

Let $\Sigma$ be a finite alphabet. A *lossless code* is a pair of maps, an encoder $C : \Sigma^* \to \{0, 1\}^*$ and a decoder $D$, with $D(C(x)) = x$ for every input $x$. So $C$ must be one-to-one. The cost of $x$ is the length $|C(x)|$ in bits. There are three common ways to state the goal.

- **Known source.** The input is a random variable $X$ with a known distribution $P$. Minimize the expected length $\mathbb E\,|C(X)|$. When $C$ is a [prefix code](/prefix-code/), a code where no codeword starts another, the minimum is between $H(X)$ and $H(X) + 1$, and for long blocks from a stationary source the length per symbol tends to the [entropy rate](/entropy-rate/).
- **Universal coding.** The source is unknown but belongs to a class, such as the memoryless sources or the Markov sources of order $k$. Find one code whose expected length is close to the entropy for every source in the class. The excess is the *redundancy*.
- **Single sequences.** There is no source. Compare $|C(x)|$ with the best length that any model in a class gives to the same $x$, for example $n H_k(x)$, where $H_k$ is the empirical entropy of order $k$.

The ideal for a single sequence is its [Kolmogorov complexity](/kolmogorov-complexity/), the length of the shortest program that prints it. That ideal cannot be computed, which is why practical methods fix a class of models.

## Variants

- **Static or adaptive.** A *static* method reads the data twice: it builds a model, writes the model, and then codes the data with it. An *adaptive* method reads the data once, updates its model as it goes, and sends no model, since the decoder builds the same one.
- **Block or stream.** The input may be a block of known length or a stream with no end known in advance.
- **Symbol alphabets.** The data may be bits, bytes, words, or integers from an unbounded range; the last is the domain of [universal codes](/universal-code/) for integers.
- **Side information.** The decoder may know related data, such as an older version of the file, a shared dictionary, or a correlated source. The [Slepian-Wolf theorem](/slepian-wolf-theorem/) gives the limits when the encoders are separate.
- **Access and resources.** Some uses need to decode any part of the data alone, to search the compressed data, or to fit in little memory or time, at some cost in the length.

## Examples

The table below comes from the harness in the implementation. It generates 20000 bytes of each kind with seed 1948, compresses them with zlib at level 9, bz2 at level 9, lzma at preset 9, and an adaptive order-0 arithmetic coder, and checks that each output decodes to the input. All sizes are in bytes. *Source* is the information content of the data under the source that made it, $\sum -\lg p$ over the bytes, divided by 8. $nH_0$ is the empirical order-0 entropy, also in bytes.

| data | source | $nH_0$ | zlib | bz2 | lzma | order 0 |
|---|---|---|---|---|---|---|
| random bytes | 20000 | 19971 | 20016 | 20468 | 20060 | 20080 |
| skewed bytes, 5 values | 4175 | 4175 | 5521 | 5178 | 5312 | 4422 |
| order-2 Markov text | 3942 | 10141 | 7283 | 5639 | 6976 | 10379 |
| long runs, mean 200 | 166 | 9680 | 288 | 384 | 316 | 9919 |

The results follow the theory.

- **Random bytes.** No method shrinks them; each adds a header or a model cost.
- **Skewed bytes.** The bytes are independent, so a model of the byte frequencies is the right model. The order-0 coder is the best of the four, about 6% above the source, and the excess is the cost of learning 255 probabilities from scratch.
- **Markov text.** The order-0 coder cannot go below $nH_0$, while the methods that use context get well below it, bz2 most of all. None reaches the source, since none has a model of exactly this kind.
- **Long runs.** The order-0 coder sees about 4 bits of entropy per byte and cannot use the runs. The dictionary and transform coders write less than 2% of the input.
- **No method beats the source.** In every row, every size is above the source column. For any one-to-one code, the chance that the output is $c$ bits shorter than the information content is at most about $2^{-c}$ times the number of possible lengths.

## Known algorithms

The methods fall into three families.

- **Statistical methods** give each symbol a probability and code it with about $-\lg p$ bits. The coders are [Huffman coding](/huffman-coding/), [arithmetic coding](/arithmetic-coding/), [range coding](/range-coding/) and [asymmetric numeral systems](/asymmetric-numeral-systems/). The models range from fixed frequencies to [adaptive models](/adaptive-modeling/) and [context models](/context-modeling/), such as [PPM](/prediction-by-partial-matching/), [context tree weighting](/context-tree-weighting/) and [context mixing](/context-mixing/). [Enumerative coding](/enumerative-coding/) gives the index of the data in a set of the same type.
- **Dictionary methods** replace repeated strings by references to earlier copies or to entries of a dictionary. See [dictionary-based compression](/dictionary-based-compression/); the main members are LZ77, LZ78 and LZW, and the formats [Deflate](/deflate/), [LZMA](/lzma/) and [Zstandard](/zstandard/) combine them with an entropy coder.
- **Transform methods** change the data into a form that a simple model compresses well, and then code the result. The [Burrows-Wheeler transform](/burrows-wheeler-transform/) groups symbols with similar contexts, and it is followed by move-to-front and run-length coding; [predictive coding](/predictive-coding/) codes the difference from a prediction, as in lossless image and audio coders.

The families mix in practice. LZ77 parsing has a statistical side in the entropy coder of its output, and many context models are trained on the output of a transform.

## Bounds

- **No universal shrinking.** There are $2^n$ strings of $n$ bits but only $2^n - 1$ strings of fewer bits, so a one-to-one code cannot shorten all inputs of length $n$. More strongly, fewer than $2^{n-c+1}$ strings of length $n$ can be shortened by $c$ bits or more, a fraction below $2^{1-c}$. See the [incompressibility argument](/incompressibility-argument/).
- **Entropy.** For a prefix code and a source $X$, $\mathbb E\,|C(X)| \ge H(X)$, by the [Kraft inequality](/kraft-inequality/); the [source coding theorem](/source-coding-theorem/) shows that the rate of a stationary source can be reached, and not passed, by codes of long blocks.
- **Single outcomes.** For a prefix code, $\Pr[\,|C(X)| < -\lg P(X) - c\,] \le 2^{-c}$. So a code rarely beats the information content of the actual outcome by much.
- **Universal redundancy.** For a class of sources with $d$ parameters, every universal code has a redundancy of at least about $\tfrac{d}{2} \lg n$ bits on most sources of the class, and codes such as the KT mixture and context tree weighting reach this rate.

## Reductions

- **Prediction and compression are the same problem.** A predictor that gives the next symbol a probability $p$ becomes a compressor through arithmetic coding, with a length within 2 bits of $\sum -\lg p$. A compressor with lengths $|C(x)|$ defines a probability $2^{-|C(x)|}$ and so a predictor. Good compression and good prediction in the log loss are the same goal.
- **Compression and model selection.** The [minimum description length](/minimum-description-length/) principle chooses the model that gives the shortest total code for the model and the data.
- **Coding and modeling.** Through the model and coder split, any compression problem reduces to the estimation of conditional probabilities.

## Applications

- **Files and archives.** gzip and ZIP use Deflate, xz and 7z use LZMA, and Zstandard and Brotli are common in newer systems.
- **Media.** PNG uses Deflate after a filter that predicts each pixel; lossless audio coders use prediction and Rice codes; video standards code their syntax elements with [CABAC](/cabac/), a context-adaptive arithmetic coder.
- **Data systems.** Databases, column stores and search engines compress their pages and their lists of integers, often in a form that can be read without full decoding.
- **Networks and storage.** Web servers compress pages before sending them, and storage systems compress blocks to save space and bandwidth.
- **Genomics.** Sequencing data and reference genomes are stored with special models for DNA and quality scores.
- **Benchmarks.** Methods are compared on fixed sets of files. The Calgary corpus of Bell, Witten and Cleary (from 1987), the Canterbury corpus of Arnold and Bell (1997) and the Silesia corpus of Deorowicz (2003) are the best known for general data.

## References
