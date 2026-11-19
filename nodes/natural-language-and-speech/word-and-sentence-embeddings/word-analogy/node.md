---
tag: CX78YB
kind: problem
slug: word-analogy
name: Word analogy
aliases:
- vector offset method
- parallelogram model of analogy
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: Solve a is to b as c is to what, by the word whose vector is closest to b - a + c, a common test of word embeddings.
prereqs: [word-embedding, cosine-similarity]
see_also: [skip-gram-model, glove, sgns-implicit-factorization-theorem, k-nearest-neighbor-search, hubness, cross-lingual-embedding-mapping, hard-debiasing, word-embedding-association-test]
sources:
  - paper: "Tomas Mikolov, Wen-tau Yih and Geoffrey Zweig, Linguistic regularities in continuous space word representations, Proceedings of NAACL-HLT 2013, pages 746 to 751"
    title: Mikolov, Yih and Zweig 2013
    locator: the vector offset method, the answer as the word of highest cosine similarity to b - a + c, and the test of syntactic and semantic analogies
  - paper: "Tomas Mikolov, Kai Chen, Greg Corrado and Jeffrey Dean, Efficient estimation of word representations in vector space, ICLR 2013 workshop track, arXiv:1301.3781"
    title: Mikolov, Chen, Corrado and Dean 2013
    locator: "Section 4.1 (the semantic-syntactic word relationship test set, 8869 semantic and 10675 syntactic questions, scored by exact match of the nearest word)"
  - paper: "Omer Levy and Yoav Goldberg, Linguistic regularities in sparse and explicit word representations, Proceedings of CoNLL 2014, pages 171 to 180"
    title: Levy and Goldberg 2014
    locator: "the rewriting of the vector offset objective as a sum of three cosine similarities (3CosAdd), and the multiplicative objective 3CosMul"
  - paper: "Tal Linzen, Issues in evaluating semantic spaces using word analogies, Proceedings of the 1st Workshop on Evaluating Vector Space Representations for NLP (RepEval 2016), pages 13 to 18"
    title: Linzen 2016
    locator: the effect of excluding the three query words from the candidates, and baselines that ignore part of the question
  - paper: "Jeffrey Pennington, Richard Socher and Christopher D. Manning, GloVe: Global vectors for word representation, Proceedings of EMNLP 2014, pages 1532 to 1543"
    title: Pennington, Socher and Manning 2014
    locator: "Section 4.1 (the word analogy task with 19,544 questions, and the use of 3CosAdd)"
---

The word analogy problem asks for the missing word of a proportion "$a$ is to $b$ as $c$ is to ?", such as "man is to woman as king is to ?" (queen) or "walk is to walked as swim is to ?" (swam). Mikolov, Yih and Zweig (2013) observed that [word embeddings](/word-embedding/) often encode such relations as a nearly constant offset between vectors, $\vec b - \vec a \approx \vec d - \vec c$, and answered the question with the word whose vector has the highest [cosine similarity](/cosine-similarity/) to $\vec b - \vec a + \vec c$. This vector offset method, later called 3CosAdd, and the analogy test sets of Mikolov et al. became a standard measure of the quality of word vectors. Solving one question is a [nearest neighbour search](/k-nearest-neighbor-search/) over the vocabulary after a little vector arithmetic, $O(|V| d)$ time by brute force. The answer depends on details that are easy to miss, above all whether the three question words are allowed as answers.

## In plain words

An analogy question gives three words and asks for a fourth: "man is to woman as king is to what?" A person answers "queen".

Word vectors can answer many such questions with simple arithmetic. Take the vector of "king", take away "man" and add "woman". The point you get is often close to the vector of "queen". The idea is that the step from "man" to "woman" is about the same as the step from "king" to "queen".

To answer, compare the point with the vector of every word and pick the closest one. The three words of the question must usually be left out, because the point is often closest to "king" itself. The share of questions answered correctly is a common score for word vectors.

## Definition

**Input.** A vocabulary $V$ with a vector $\vec x_w \in \mathbb{R}^d$ for each word, usually scaled to unit length, and a question $(a, b, c)$ of three words of $V$, read "$a$ is to $b$ as $c$ is to ?".

**Output.** A word $d^* \in V$. Under the vector offset method (3CosAdd),

$$d^* = \arg\max_{x \in V \setminus \{a, b, c\}} \cos(\vec x_x, \vec x_b - \vec x_a + \vec x_c).$$

For unit vectors this is the same as $\arg\max_x \big(\cos(x, b) - \cos(x, a) + \cos(x, c)\big)$, because the norm of $\vec x_b - \vec x_a + \vec x_c$ is the same for every candidate.

**Evaluation.** A test set is a list of questions with a gold answer $d$. The score is the accuracy, the fraction of questions with $d^* = d$. Mikolov, Chen, Corrado and Dean count only an exact match as correct, so a synonym of the gold word is an error.

## Variants

- **With or without exclusion.** The usual definition removes $a$, $b$ and $c$ from the candidates. Without the exclusion, the answer is often $c$ itself, since $\vec x_b - \vec x_a$ is short when $a$ and $b$ are similar. Linzen (2016) showed that this choice changes the reported accuracy a lot.
- **3CosMul.** Levy and Goldberg (2014) replace the sum of similarities by a product and a quotient, $\arg\max_x \cos(x, b)\cos(x, c) / (\cos(x, a) + \varepsilon)$, with each cosine shifted to $[0, 1]$ by $(\cos + 1)/2$ and $\varepsilon = 0.001$. This keeps one large similarity from dominating the others.
- **Restricted vocabulary.** Many evaluations search only the most frequent words, which removes rare words that are close to the target point by chance. The accuracy depends on this cut.
- **Semantic and syntactic questions.** The Google test set of Mikolov, Chen, Corrado and Dean has 8869 semantic questions (such as capitals and currencies) and 10675 syntactic questions (such as plurals and past tenses). Pennington, Socher and Manning report results on 19,544 questions from this set.
- **Ranking instead of top 1.** A softer score asks whether the gold word is among the $k$ best candidates.

## Examples

Take five words with unit vectors in the plane at the angles man $0°$, woman $10°$, king $50°$, queen $70°$ and prince $40°$. The question is "man is to woman as king is to ?". The target point is $\vec t = \vec x_{\text{king}} - \vec x_{\text{man}} + \vec x_{\text{woman}} = (0.6276, 0.9397)$, with norm $1.13$.

| word | cosine with $\vec t$ | 3CosMul score |
|---|---|---|
| man | 0.5554 | 0.8143 |
| woman | 0.6914 | 0.8889 |
| king | 0.9940 | 1.0737 |
| queen | 0.9714 | 1.0824 |
| prince | 0.9600 | 1.0474 |

Without exclusion, 3CosAdd returns king, the word of the question. With the three question words excluded, it returns queen, ahead of prince. 3CosMul (with $\varepsilon = 0.001$) also returns queen, and here it does so even without exclusion, since its score of king is lower than its score of queen.

## Known algorithms

- **Brute force.** Compute $\vec t = \vec x_b - \vec x_a + \vec x_c$ in $O(d)$, then the dot product of $\vec t$ with every unit word vector in $O(|V| d)$, and keep the best word that is not $a$, $b$ or $c$. For $Q$ questions at once, the dot products are one matrix product of a $Q \times d$ matrix by a $d \times |V|$ matrix.
- **3CosMul.** It needs the three similarities $\cos(x, a)$, $\cos(x, b)$ and $\cos(x, c)$ for every candidate, so three dot products per word, still $O(|V| d)$ per question. It is not a single nearest neighbour query.
- **Approximate search.** With an index built once, such as [locality-sensitive hashing](/locality-sensitive-hashing/) or [product quantization](/product-quantization/), 3CosAdd queries cost less than $O(|V| d)$ but can miss the exact best word.

## Bounds

The brute force method takes $O(|V| d)$ time and $O(|V|)$ extra space for the scores per question, or $O(1)$ extra space with a running maximum. Without an index or other preprocessing, every exact method must examine every candidate vector, because any vector it does not read could be the best one. With preprocessing, exact search in high dimension has no known method that is much faster than brute force in the worst case, which is why approximate indexes are used.

## Reductions

- **To nearest neighbour search.** 3CosAdd on unit vectors is a maximum cosine (or, after scaling, maximum dot product) query with the point $\vec t$. The exclusion of three words is handled by asking for the four best and dropping the question words.
- **From relation similarity.** The question "is $(c, d)$ in the same relation as $(a, b)$?" becomes a comparison of the offsets $\vec x_b - \vec x_a$ and $\vec x_d - \vec x_c$. Levy and Goldberg (2014) show that 3CosAdd can be written as a sum of word similarities, so it does not need the offsets themselves to be aligned.
- **Related to translation.** Word translation after [cross-lingual embedding mapping](/cross-lingual-embedding-mapping/) is the same kind of query, the nearest target word to a transformed source vector, and suffers from the same [hubness](/hubness/) effects.

## Applications

- **Evaluation of embeddings.** Analogy accuracy is a common intrinsic score for [skip-gram](/skip-gram-model/), [GloVe](/glove/) and other vectors, next to word similarity tests. It does not always predict how well the vectors do on other tasks.
- **Probing relations.** The offset between word pairs shows which relations, such as gender, tense, plural or country to capital, a space encodes in a regular way.
- **Bias analysis.** Analogies such as "man is to programmer as woman is to ?" expose social biases in embeddings, which motivated [hard debiasing](/hard-debiasing/) and tests such as the [WEAT](/word-embedding-association-test/).

## References
