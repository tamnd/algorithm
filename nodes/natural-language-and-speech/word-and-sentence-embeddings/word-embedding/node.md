---
tag: 9HSMWP
kind: definition
slug: word-embedding
name: Word embedding
aliases:
- word vector
- distributed word representation
area: natural-language-and-speech/word-and-sentence-embeddings
level: intro
summary: "A map from each word of a vocabulary to a dense real vector, usually of 50 to a few hundred dimensions, fit from text so that words used alike lie close together."
prereqs: [embedding, distributional-hypothesis]
see_also: [skip-gram-model, glove, word-context-matrix, latent-semantic-analysis, cosine-similarity, word-analogy, contextual-word-embedding, subword-information-embeddings]
sources:
  - paper: "Yoshua Bengio, Réjean Ducharme, Pascal Vincent and Christian Jauvin, A neural probabilistic language model, Journal of Machine Learning Research 3, 2003, pages 1137 to 1155"
    title: Bengio, Ducharme, Vincent and Jauvin 2003
    locator: the shared table C of word feature vectors, learned with the language model
  - paper: "Ronan Collobert, Jason Weston, Léon Bottou, Michael Karlen, Koray Kavukcuoglu and Pavel Kuksa, Natural language processing (almost) from scratch, Journal of Machine Learning Research 12, 2011, pages 2493 to 2537"
    title: Collobert, Weston, Bottou, Karlen, Kavukcuoglu and Kuksa 2011
    locator: the lookup table layer and word vectors trained on unlabeled text and reused across tagging tasks
  - paper: "Tomas Mikolov, Kai Chen, Greg Corrado and Jeffrey Dean, Efficient estimation of word representations in vector space, ICLR 2013 workshop track, arXiv:1301.3781"
    title: Mikolov, Chen, Corrado and Dean 2013
    locator: "Sections 3 and 4 (the CBOW and skip-gram models, and the test set of 8869 semantic and 10675 syntactic analogy questions)"
  - paper: "Peter D. Turney and Patrick Pantel, From frequency to meaning: vector space models of semantics, Journal of Artificial Intelligence Research 37, 2010, pages 141 to 188"
    title: Turney and Pantel 2010
    locator: the word-context matrix, weighting by PMI and smoothing by truncated SVD
---

## Definition

Let $V$ be a finite vocabulary of word types and $d$ a positive integer, the **dimension**. A **word embedding** is a map $E : V \to \mathbb{R}^d$. It is stored as a $|V| \times d$ real matrix whose row $w$ is the **word vector** $\vec w = E(w)$. Reading a vector is a table lookup; in matrix form, $\vec w = e_w^\top E$, where $e_w$ is the one-hot vector of $w$. This is the [embedding](/embedding/) lookup table of machine learning, applied to words.

The term carries two conditions that the bare map does not. First, $d$ is much smaller than $|V|$: typical values are 50 to 300 for vocabularies of $10^5$ to $10^6$ words, so the vectors are **dense** (most entries nonzero) rather than sparse. Second, the vectors are **fit from text**, by a model or a factorization that follows the [distributional hypothesis](/distributional-hypothesis/): words that occur in similar contexts should get similar vectors. Similarity of two words is then measured by the [cosine similarity](/cosine-similarity/)

$$\cos(\vec u, \vec v) = \frac{\vec u \cdot \vec v}{\lVert \vec u \rVert\, \lVert \vec v \rVert},$$

or by the dot product, or by the Euclidean distance after each vector is scaled to unit length.

A word embedding gives one vector per **type**. Every occurrence of "bank" gets the same vector, whatever its sense. A method that gives one vector per **token**, as a function of the sentence, makes a [contextual word embedding](/contextual-word-embedding/).

Many methods learn two tables: word vectors $\vec w$ and context vectors $\vec c$, and the model only sees the dot products $\vec w \cdot \vec c$. The [skip-gram model](/skip-gram-model/) keeps the word table. [GloVe](/glove/) uses the sum $\vec w + \vec c$ of the two vectors of each word. Such a pair of tables is not unique: for any invertible $d \times d$ matrix $A$, the tables $W A$ and $C A^{-\top}$ give the same dot products. Cosines between word vectors survive only the orthogonal choices of $A$. So an embedding is fixed at most up to a rotation or a reflection of the space, and two embeddings trained apart, for example in two languages, need a map between them before their vectors can be compared (see [cross-lingual embedding mapping](/cross-lingual-embedding-mapping/)).

## Examples and non-examples

**A toy embedding.** Take $d = 2$ and the vectors $\vec{\text{cat}} = (0.8, 0.6)$, $\vec{\text{dog}} = (0.6, 0.8)$ and $\vec{\text{car}} = (-0.6, 0.8)$, all of unit length. Then $\cos(\text{cat}, \text{dog}) = 0.48 + 0.48 = 0.96$, $\cos(\text{dog}, \text{car}) = -0.36 + 0.64 = 0.28$ and $\cos(\text{cat}, \text{car}) = -0.48 + 0.48 = 0$. In this space "cat" is close to "dog" and unrelated to "car". Rotate the plane by any angle and the three cosines do not change.

**Learned embeddings (examples).**

- The input vectors of the [skip-gram model](/skip-gram-model/) or of the [continuous bag-of-words model](/continuous-bag-of-words/), trained with [negative sampling](/negative-sampling/) or [hierarchical softmax](/hierarchical-softmax/).
- [GloVe](/glove/) vectors, fit by weighted least squares to log co-occurrence counts.
- The rows of $U_d \Sigma_d^{1/2}$ (or of $U_d$) from a truncated [singular value decomposition](/singular-value-decomposition/) of a [positive PMI](/positive-pointwise-mutual-information/) matrix, as in [latent semantic analysis](/latent-semantic-analysis/).
- [Subword information embeddings](/subword-information-embeddings/), where a word vector is a sum of character n-gram vectors, so that words never seen in training also get a vector.
- The lookup table of a neural language model, such as the [neural probabilistic language model](/neural-probabilistic-language-model/) of Bengio et al., learned together with the rest of the network.

**Non-examples.**

- **One-hot vectors.** $E(w) = e_w$ is a map into $\mathbb{R}^{|V|}$, but $d = |V|$, and the cosine of any two different words is 0. It says nothing about similarity.
- **Raw count rows.** The row of $w$ in a [word-context matrix](/word-context-matrix/) is a distributional vector, but it is sparse and has one dimension per context. It becomes a word embedding only after a reduction to a few hundred dense dimensions.
- **A random table.** Rows drawn at random and never fit to text form a map $V \to \mathbb{R}^d$, but their geometry does not follow any usage. This is the state of a table before training.
- **Contextual vectors.** The hidden states of [ELMo](/elmo/) or [BERT](/bert/) depend on the sentence, so the same word gets many vectors. They are contextual embeddings, not word embeddings in the sense above.
- **Cluster labels.** The bit strings of [Brown clustering](/brown-clustering/) group similar words, but a word belongs to one cluster path, and the strings are not points in $\mathbb{R}^d$ with a cosine.

## Related definitions

- **Word similarity.** The cosine of two word vectors, compared with human ratings of word pairs, is the usual intrinsic test of an embedding. [Word analogy](/word-analogy/) is another intrinsic test, and the use of the vectors as features in a downstream task is the extrinsic test.
- **Distributional vector.** Any vector that describes a word by its contexts, sparse or dense. The rows of a [word-context matrix](/word-context-matrix/) weighted by [PMI](/pointwise-mutual-information/) are distributional vectors; Turney and Pantel 2010 survey these vector space models. Word embeddings are the dense, low-dimensional kind.
- **Embedding of other objects.** The same idea gives a [sentence embedding](/sentence-embedding/), a [paragraph vector](/paragraph-vector/) for documents and a [node embedding](/node-embedding/) for the vertices of a graph. [DeepWalk](/deepwalk/) runs the skip-gram model on random walks.
- **Implicit factorization.** For skip-gram with negative sampling, the [SGNS factorization theorem](/sgns-implicit-factorization-theorem/) shows that the word and context tables factorize a shifted PMI matrix when the dimension is large enough. This links the neural and the count-based examples above.
- **Bias in embeddings.** Embeddings fit from text also encode the social associations of that text. The [word embedding association test](/word-embedding-association-test/) measures them and [hard debiasing](/hard-debiasing/) removes one direction of them.

## References
