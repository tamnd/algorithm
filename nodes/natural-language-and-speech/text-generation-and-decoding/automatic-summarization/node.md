---
tag: 2YZFKS
kind: problem
slug: automatic-summarization
name: Automatic summarization
aliases:
- text summarization
- document summarization
area: natural-language-and-speech/text-generation-and-decoding
level: intro
summary: Produce a short text that keeps the main content of one or more documents, either by extracting sentences or by writing new ones.
prereqs: [sentence-boundary-detection, knapsack-problem]
see_also: [luhn-summarization, textrank, lexrank, pointer-generator-network, rouge, maximal-marginal-relevance, knapsack-dynamic-programming, submodular-function]
sources:
  - paper: doi:10.1007/978-3-540-71496-5_51
    title: Ryan McDonald, A Study of Global Inference Algorithms in Multi-document Summarization, ECIR 2007, Lecture Notes in Computer Science 4425, pages 557 to 564
    locator: "equation 1 (relevance minus redundancy under a length budget), Section 2.1 (NP-hardness by a reduction from three-dimensional matching), the greedy, knapsack dynamic programming and integer linear programming algorithms"
  - paper: doi:10.1561/1500000015
    title: Ani Nenkova and Kathleen McKeown, Automatic Summarization, Foundations and Trends in Information Retrieval 5(2-3), 2011, pages 103 to 233
    locator: the survey of extractive methods and of evaluation
  - paper: doi:10.1145/290941.291025
    title: Jaime Carbonell and Jade Goldstein, The use of MMR, diversity-based reranking for reordering documents and producing summaries, SIGIR 1998, pages 335 to 336
    locator: maximal marginal relevance for selecting summary sentences
---

Automatic summarization asks for a short text that keeps the main content of one document or of a set of documents. An extractive summarizer selects sentences of the input and puts them together; an abstractive summarizer writes new sentences. There is no single correct answer, so the problem is defined by a length budget and by an objective, and the result is judged against summaries written by people, with metrics such as [ROUGE](/rouge/) or by human readers. In its extractive form with a length budget, the problem is a knapsack problem when only relevance counts, and NP-hard when redundancy between sentences is also scored (McDonald 2007).

## In plain words

You have a long news story, or twenty stories about the same event, and room for 100 words. Which sentences should you keep? You want the sentences that carry the main facts, and you do not want two sentences that say the same thing. Long sentences use up the room quickly, so a long sentence must be worth its length.

A machine can do this by giving each sentence a score, then choosing the best set of sentences that fits. It can also write a new, shorter text, as a person would. The second way is harder, but it can merge facts from several sentences and drop the parts that do not matter.

## Definition

The input is a set of documents, split into sentences $s_1, \ldots, s_n$ with lengths $l_1, \ldots, l_n$ (in words or in bytes), and a budget $K$.

**Extractive summarization.** Choose a set $S \subseteq \{1, \ldots, n\}$ with $\sum_{i \in S} l_i \le K$ that maximizes an objective $f(S)$. The global objective of McDonald (2007, equation 1) is

$$f(S) = \sum_{i \in S} \mathrm{Rel}(i) - \sum_{i, j \in S,\ i < j} \mathrm{Red}(i, j),$$

where $\mathrm{Rel}(i) \ge 0$ is the relevance of sentence $i$ and $\mathrm{Red}(i, j) \ge 0$ is the redundancy of a pair. The output is the chosen sentences, usually in the order of the source.

**Abstractive summarization.** Produce any text of length at most $K$. The objective is implicit: a model is trained to give high probability to summaries written by people, and the output is decoded from it.

The scores $\mathrm{Rel}$ and $\mathrm{Red}$ are not given by the problem. They come from a method, for example word frequencies, centrality in a sentence graph or a trained model. So two parts must be kept apart: the scoring, which is a heuristic, and the selection under the budget, which is an exact optimization problem once the scores are fixed.

## Variants

- **Single-document or multi-document.** Many documents on one topic repeat the same facts, so redundancy matters more.
- **Generic or query-focused.** A query-focused summary answers a question or a topic statement, and relevance is measured against it.
- **Extractive, compressive or abstractive.** Compressive summarizers also delete words inside the chosen sentences.
- **Update summarization.** Summarize new documents for a reader who has read earlier ones, so the facts already known count as redundant.
- **Headline and title generation.** A budget of about ten words, which is close to abstractive sentence compression.
- **Indicative or informative.** An indicative summary tells what the document is about; an informative one can replace it.

## Examples

Four sentences with relevance $(5, 4, 3, 3)$ and lengths $(10, 6, 5, 5)$, and a budget $K = 11$.

| choice | length | relevance |
|---|---|---|
| {1} | 10 | 5 |
| {2, 3} | 11 | 7 |
| {2, 4} | 11 | 7 |
| {3, 4} | 10 | 6 |

Taking the most relevant sentence first gives {1}, with relevance 5, and nothing else fits. The best set is {2, 3} or {2, 4}, with 7. Now say that sentences 2 and 3 report the same fact, with $\mathrm{Red}(2, 3) = 4$ and all other redundancies 0. Then $f(\{2, 3\}) = 3$, and the unique best set is {2, 4}, with $f = 7$. A selection that ignores redundancy cannot tell {2, 3} from {2, 4}.

An abstractive example: from the sentences "The council met on Friday." and "It voted to close the bridge for repairs.", a summarizer can write "On Friday the council voted to close the bridge." An extractive summarizer with a budget of eight words cannot produce this.

## Known algorithms

- **Scoring by word frequency.** [Luhn's method](/luhn-summarization/) (1958) scores a sentence by its clusters of frequent content words.
- **Graph centrality.** [TextRank](/textrank/) and [LexRank](/lexrank/) (2004) rank sentences by PageRank on a sentence similarity graph.
- **Greedy selection with a redundancy penalty.** [Maximal marginal relevance](/maximal-marginal-relevance/) (Carbonell and Goldstein 1998) adds, at each step, the sentence with the best balance of relevance and dissimilarity to the sentences already chosen. It is a heuristic for the global objective.
- **Knapsack dynamic programming.** Without redundancy, the [knapsack dynamic program](/knapsack-dynamic-programming/) finds the best set in $O(nK)$ time; McDonald (2007) uses it as one of his algorithms.
- **Integer linear programming.** McDonald (2007) solves the global objective exactly with an integer linear program, with a variable per sentence and per pair; it is exact but slow on large inputs. Later work scores concepts, such as bigrams, instead of pairs.
- **Submodular maximization.** Lin and Bilmes (2011) write the objective as a monotone [submodular function](/submodular-function/) of the chosen set, for which a greedy algorithm with a budget has a constant factor guarantee.
- **The lead baseline.** For news, the first sentences up to the budget are a strong baseline, often hard to beat on ROUGE.
- **Neural abstractive models.** Encoder-decoder models with attention, such as the [pointer-generator network](/pointer-generator-network/), and later pretrained transformers, generate the summary token by token.

## Bounds

- **NP-hardness of the global objective.** McDonald (2007, Section 2.1) proves that maximizing equation 1 under the budget is NP-hard, by a reduction from [three-dimensional matching](/three-dimensional-matching/). This is a theorem.
- **Pseudo-polynomial without redundancy.** With $\mathrm{Red} = 0$ the problem is the 0-1 [knapsack problem](/knapsack-problem/), NP-hard when the lengths are large binary numbers, and solved in $O(nK)$ time by dynamic programming. Since sentence lengths in words are at most the length $N$ of the input, $K \le N$ can be assumed, and the dynamic program takes $O(nN)$ time, polynomial in the input size.
- **Reading the input.** Every method must read the documents, so $\Omega(N)$ time is needed.
- **No ground truth.** Different people write different summaries of the same text, and the agreement between human summaries limits how well any system can score against them. This is a measurement, and the reason for evaluation with several references.

## Reductions

- **To knapsack.** Extractive selection with additive relevance and no redundancy is the 0-1 knapsack problem, with weights $l_i$, values $\mathrm{Rel}(i)$ and capacity $K$.
- **To integer linear programming.** The global objective becomes a [binary integer program](/binary-integer-programming/) with variables $x_i$ for sentences and $y_{ij}$ for pairs, with $y_{ij} \le x_i$, $y_{ij} \le x_j$ and $y_{ij} \ge x_i + x_j - 1$.
- **From three-dimensional matching.** McDonald (2007) reduces three-dimensional matching to the decision form of the global objective, which shows that the redundancy terms make the problem hard.
- **To maximum coverage.** If each sentence covers a set of concepts and the score is the total weight of the covered concepts, the problem is budgeted maximum coverage, a monotone submodular maximization.

## Applications

News digests and search result snippets, summaries of meetings, emails and medical records, abstracts of scientific papers, and summaries of reviews. Summarization is also a standard test of text generation models, usually on news data sets such as CNN and Daily Mail, with ROUGE as the main metric and human judgments for faithfulness, since a fluent summary can state facts that are not in the source.

## References
