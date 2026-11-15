---
tag: 354WR4
kind: technique
slug: retrieval-augmented-generation
name: Retrieval-augmented generation
aliases:
- retrieval-augmented language model
area: information-retrieval-and-ai-reasoning/ranking-models
level: research
summary: Retrieves passages for an input and conditions a text generator on them, so the output can use knowledge outside the model weights.
prereqs: [dense-passage-retrieval]
see_also: [dual-encoder-retrieval, maximum-inner-product-search, hnsw, bm25, cross-encoder-reranking, reciprocal-rank-fusion, beam-search, colbert]
sources:
  - paper: "Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel and Douwe Kiela, Retrieval-augmented generation for knowledge-intensive NLP tasks, Advances in Neural Information Processing Systems 33 (NeurIPS 2020), arXiv:2005.11401"
    locator: pp. 9459-9474; the RAG-Sequence and RAG-Token models (the marginal over the top k retrieved documents), the retriever p(z|x) proportional to exp(d(z) . q(x)) with a DPR bi-encoder and a frozen document encoder, the BART-large generator, the Wikipedia index of 21M passages of 100 words with FAISS HNSW, Thorough and Fast decoding, Table 1 (measured exact match on open-domain question answering)
  - paper: doi:10.18653/v1/2020.emnlp-main.550
    title: Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen and Wen-tau Yih, Dense passage retrieval for open-domain question answering, Proceedings of EMNLP 2020
    locator: pp. 6769-6781 (the dual encoder retriever that RAG starts from)
---

Retrieval-augmented generation (RAG) answers an input $x$ in two steps: a retriever finds the top $k$ passages $z$ for $x$ in a large text collection, and a generator produces the output $y$ conditioned on $x$ and those passages. In the model of Lewis et al. (2020), the retriever is a [dense passage retrieval](/dense-passage-retrieval/) dual encoder with $p_\eta(z \mid x) \propto \exp(d(z)^\top q(x))$, and the output probability is a marginal over the retrieved passages, so the retriever's query encoder can be trained through the generator's likelihood without labels for which passage is right. The DPR page trains the retriever with known positive passages; this page is about using retrieval inside a generator: the exact marginal objectives, the gradient that reaches the retriever, and the ways the method fails. The generator, the encoders, and the factual accuracy of the outputs are outside this page.

## In plain words

A text generator only knows what it learned during training, and that knowledge goes out of date. Retrieval-augmented generation gives it a library. For each question, a search step finds a few passages that look useful. The generator reads the question together with each passage and writes the answer. Passages that the search step trusts more count more. When a passage helps the generator produce the right answer during training, the search step learns to trust passages like it more. To update what the system knows, we can change the library without retraining the generator.

## When it applies

The technique applies when:

- the task needs knowledge that a text collection holds, such as open-domain questions, fact checking or grounded dialogue;
- there is a retriever whose score for a passage is a function of the input and the passage, so that the top $k$ passages can be found quickly, usually by [maximum inner product search](/maximum-inner-product-search/) over precomputed passage vectors;
- the generator can take the input and one passage, or several passages, as its conditioning text;
- training pairs $(x, y)$ exist, but labels for which passage supports $y$ need not.

It does not make outputs correct: the generator can ignore the passages or misread them, and the retriever can return wrong ones.

## The template

Let $Z_k(x)$ be the top $k$ passages by retriever score $s(z) = d(z)^\top q(x)$, and $p_\eta(z \mid x) = e^{s(z)} / \sum_{z' \in Z_k(x)} e^{s(z')}$. The two models of Lewis et al. (2020) are

$$p_{\text{seq}}(y \mid x) = \sum_{z \in Z_k(x)} p_\eta(z \mid x) \prod_{i} p_\theta(y_i \mid x, z, y_{<i}),$$

$$p_{\text{tok}}(y \mid x) = \prod_{i} \sum_{z \in Z_k(x)} p_\eta(z \mid x)\, p_\theta(y_i \mid x, z, y_{<i}).$$

RAG-Sequence uses one passage for the whole output and mixes at the end; RAG-Token may draw each token from a different passage.

```pseudo id=main
RAG-TRAIN-STEP(x, y, k)
L1  u ← q(x)                                   -- query encoder, trained
L2  Z ← the k passages with the largest d(z) · u   -- passage vectors d(z) precomputed and frozen
L3  π(z) ← softmax over Z of d(z) · u
L4  for each z ∈ Z: a(z) ← Π_i p_θ(y_i | x, z, y_<i)   -- one generator pass per passage
L5  loss ← -log Σ_z π(z) a(z)                  -- RAG-Sequence; RAG-Token mixes inside the product
L6  back-propagate into p_θ and into q, not into d
```

At inference, RAG-Token can use ordinary [beam search](/beam-search/) over the mixed token distribution. RAG-Sequence does not factor over tokens; Lewis et al. (2020) decode with a beam for each passage and then score the hypotheses, either running extra passes for hypotheses missing from some beams (Thorough Decoding) or treating those as probability 0 (Fast Decoding).

**The gradient that reaches the retriever.** For RAG-Sequence, with $a(z) = p_\theta(y \mid x, z)$ and $p = \sum_z \pi(z) a(z)$,

$$\frac{\partial \log p}{\partial s(z)} = \frac{\pi(z)\, a(z)}{p} - \pi(z) = p(z \mid x, y) - p_\eta(z \mid x).$$

*Proof.* $\partial \pi(w) / \partial s(z) = \pi(w)([w = z] - \pi(z))$, so $\partial p / \partial s(z) = \sum_w a(w) \pi(w)([w = z] - \pi(z)) = \pi(z) a(z) - \pi(z) p$. Divide by $p$. $\square$

So the likelihood raises the score of a passage exactly when its posterior given the output, $p(z \mid x, y) \propto \pi(z) a(z)$, exceeds its prior from the retriever. This is how the retriever learns from $(x, y)$ pairs alone. The gradient reaches only the passages in $Z_k(x)$; a passage outside the top $k$ gets nothing, however useful it would be.

## Classic examples

Take $k = 2$ retrieved passages with scores $s = (2.0, 1.0)$, so $p_\eta(z \mid x) = (0.7311, 0.2689)$, and a two-token output whose generator probabilities are $(0.9, 0.2)$ given passage 1 and $(0.3, 0.8)$ given passage 2.

| quantity | passage 1 | passage 2 | total |
|---|---|---|---|
| $p_\eta(z \mid x)$ | 0.7311 | 0.2689 | 1 |
| $p_\theta(y \mid x, z)$ | 0.18 | 0.24 | |
| $p_\eta(z \mid x)\, p_\theta(y \mid x, z)$ | 0.1316 | 0.0645 | $p_{\text{seq}} = 0.1961$ |
| posterior $p(z \mid x, y)$ | 0.6709 | 0.3291 | 1 |
| $\partial \log p_{\text{seq}} / \partial s(z)$ | -0.0601 | 0.0601 | 0 |

RAG-Token mixes per token: $(0.7311 \cdot 0.9 + 0.2689 \cdot 0.3)(0.7311 \cdot 0.2 + 0.2689 \cdot 0.8) = 0.7386 \cdot 0.3614 = 0.2669$, higher than $p_{\text{seq}}$ here, because each token can come from the passage that supports it best. Passage 2 explains the output better than the retriever thought, so the gradient raises its score; a finite-difference check of $\log p_{\text{seq}}$ gives the same $\pm 0.0601$.

Systems built on the template:

- **RAG with DPR and BART.** Lewis et al. (2020) use the DPR retriever over 21 million Wikipedia passages of 100 words, a FAISS [HNSW](/hnsw/) index, $k$ of 5 or 10, and a BART-large generator of about 400 million parameters, and train the query encoder and the generator while the passage encoder and index stay fixed. Table 1 of the paper reports exact match on Natural Questions of 44.1 for RAG-Token and 44.5 for RAG-Sequence, as measurements.
- **Sparse or hybrid retrieval.** Replace the dense retriever by [BM25](/bm25/), or fuse both lists with [reciprocal rank fusion](/reciprocal-rank-fusion/). The marginal still needs a score per passage to form $p_\eta(z \mid x)$; a fixed retriever with no gradient also works, as plain retrieve-then-read.
- **Reranked context.** Retrieve many passages, rerank them with a [cross-encoder](/cross-encoder-reranking/), and give the generator the top few. The reranker is usually trained apart from the generator.
- **Late interaction retrieval.** Use [ColBERT](/colbert/) as the retriever for better recall on long or complex inputs, at the cost of a larger index.

## Variations

- **Concatenated context.** Put all $k$ passages into one long input instead of one generator pass per passage. This is common with large language models; the output no longer is an explicit marginal over passages, and the gradient formula above does not apply.
- **Joint pretraining of the retriever.** Train the retriever and a language model together from the start, with a periodically refreshed index, instead of starting from a DPR retriever.
- **Retrieval at every chunk.** Retrieve again during generation, conditioned on what has been written so far.
- **Updating the passage encoder.** Training $d(z)$ as well means re-encoding and re-indexing the collection, which Lewis et al. (2020) avoid by freezing it.
- **Index swaps.** Replacing the collection, for example with a newer snapshot, changes the knowledge available without retraining, as long as the passage encoder is the same.

## Pitfalls

- **Training the frozen side.** Line L6 must not update $d(z)$ unless the index is rebuilt; otherwise the stored vectors of line L2 no longer match the encoder, and retrieval uses stale scores.
- **Recall caps everything.** If the useful passage is not in the top $k$ of line L2, neither the generator nor the gradient can use it. Measure the recall of the retriever separately.
- **Softmax over the wrong set.** Line L3 normalizes over the $k$ retrieved passages. Normalizing over the whole collection is the true $p_\eta(z \mid x)$, but it cannot be computed cheaply, and mixing the two changes the gradient.
- **Grounding is not guaranteed.** A high likelihood can come from the generator's own knowledge rather than from the passage. Check whether the cited passage supports the output.
- **Costs grow with $k$.** Line L4 runs one generator pass per passage, so time and memory per example grow linearly in $k$.
- **Leaked test answers.** If the collection contains the test questions with their answers, measured accuracy reflects lookup, not reasoning.

## Exercises

1. For RAG-Token with two tokens, derive $\partial \log p_{\text{tok}} / \partial s(z)$ and check it in the example by finite differences.
2. Show that $p_{\text{seq}} = p_{\text{tok}}$ when every passage gives the same generator distribution, and also when $k = 1$.
3. Suppose $a(z)$ is the same for all retrieved passages. Show that the gradient of $\log p_{\text{seq}}$ in the retriever scores is 0, and explain what this means for learning a retriever from outputs that do not depend on the passage.

## References
