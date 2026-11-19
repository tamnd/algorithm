---
tag: TKNXEG
kind: algorithm
slug: retrofitting-word-vectors
name: Retrofitting
aliases:
- retrofitting word vectors to semantic lexicons
area: natural-language-and-speech/word-and-sentence-embeddings
level: advanced
summary: Post-process word vectors so that words linked in a lexicon such as WordNet move closer, by iterative updates that also keep each near its original.
model: real-ram
complexity:
  vars: {V: "the vocabulary size, the number of types", E: "the number of neighbour entries in the lexicon", d: "the dimension of the vectors", T: "the number of sweeps"}
  time: {worst: "O(T (V + E) d)"}
  space: {extra: "O(V d + E)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2015
  people: [Manaal Faruqui, Jesse Dodge, Sujay Kumar Jauhar, Chris Dyer, Eduard Hovy, Noah A. Smith]
  note: "Faruqui, Dodge, Jauhar, Dyer, Hovy and Smith proposed retrofitting at NAACL 2015 as a fast post-processing step that adds the relations of a semantic lexicon to any set of trained word vectors."
prereqs: [word-embedding, jacobi-method]
see_also: [gauss-seidel-method, diagonally-dominant-matrix, banach-fixed-point-theorem, laplacian-matrix, glove, skip-gram-model, word-sense-disambiguation, cosine-similarity]
sources:
  - paper: "Manaal Faruqui, Jesse Dodge, Sujay Kumar Jauhar, Chris Dyer, Eduard Hovy and Noah A. Smith, Retrofitting word vectors to semantic lexicons, Proceedings of NAACL-HLT 2015, pages 1606 to 1615, doi:10.3115/v1/N15-1184"
    title: Faruqui, Dodge, Jauhar, Dyer, Hovy and Smith 2015
    locator: "Section 2 (the objective Psi(Q), its convexity, the update of q_i, alpha_i = 1, beta_ij = 1/degree(i) and 10 iterations), the experiments with PPDB, WordNet and FrameNet as lexicons, and the released retrofit.py"
  - book: isbn:9781421407944
    title: "Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013"
    locator: the Jacobi and Gauss-Seidel iterations and their convergence for strictly diagonally dominant matrices
---

Retrofitting moves a set of trained word vectors so that words linked in a semantic lexicon, such as synonyms in WordNet or paraphrases in PPDB, get closer, while each vector stays near where it started. It needs no corpus and no retraining. Each word in turn is replaced by a weighted mean of its own original vector and the current vectors of its lexicon neighbours, and about 10 sweeps over the vocabulary are enough. Faruqui, Dodge, Jauhar, Dyer, Hovy and Smith (2015) proposed it. The sweep is a [Jacobi](/jacobi-method/) or [Gauss-Seidel](/gauss-seidel-method/) iteration for a strictly diagonally dominant linear system, so it converges to one fixed point from any start, with the error at least halved at every sweep under the default weights.

## In plain words

Word vectors learned from text put words close together when they appear in similar places. But "good" and "bad" appear in similar places too, and a dictionary of synonyms knows things that the text does not show.

Retrofitting uses such a dictionary to adjust the vectors after training. Each word is pulled toward the words listed as its synonyms, and also held back toward its original vector, so it does not lose what it learned from the text. The new vector of a word is a mix: half from its old self, half from the average of its listed neighbours.

Do this for every word, and repeat a few times. Words connected in the dictionary drift together, and the changes settle quickly. Words not in the dictionary stay as they were.

## The problem

The input is a vocabulary $V$ with original vectors $\hat{\vec q}_i \in \mathbb{R}^d$, a lexicon that gives a set $N(i)$ of neighbour words for each word $i$, positive weights $\alpha_i$ and $\beta_{ij}$, and a number of sweeps $T$. Only neighbours that are in $V$ count. Faruqui et al. define the objective

$$\Psi(Q) = \sum_{i} \Big(\alpha_i \|\vec q_i - \hat{\vec q}_i\|^2 + \sum_{j \in N(i)} \beta_{ij} \|\vec q_i - \vec q_j\|^2\Big)$$

and its coordinate update

$$\vec q_i \leftarrow \frac{\sum_{j \in N(i)} \beta_{ij} \vec q_j + \alpha_i \hat{\vec q}_i}{\sum_{j \in N(i)} \beta_{ij} + \alpha_i},$$

with $\alpha_i = 1$, $\beta_{ij} = 1/|N(i)|$ and 10 iterations. The output is the vectors after $T$ sweeps.

What the iteration computes is the fixed point of the update, the solution of the linear system

$$\Big(\alpha_i + \sum_{j \in N(i)} \beta_{ij}\Big) \vec q_i - \sum_{j \in N(i)} \beta_{ij} \vec q_j = \alpha_i \hat{\vec q}_i \quad \text{for every word } i \text{ with } N(i) \ne \emptyset.$$

This fixed point minimizes a quadratic objective only when the weights are symmetric. If the lexicon is symmetric, $\beta_{ij} = \beta_{ji}$, and each unordered edge $\{i, j\}$ is counted once in the second sum of $\Psi$, then the update is the exact minimizer of $\Psi$ in $\vec q_i$ and the fixed point is the minimizer of $\Psi$. With $\beta_{ij} = 1/|N(i)|$ the weights are not symmetric when the degrees differ, and the fixed point is then the solution of the system above, not a minimizer of $\Psi$.

## The algorithm

```pseudo id=main
RETROFIT(Q^, N, α, β, T)
L1  Q ← Q^                                       ▷ start at the original vectors
L2  for t ← 1 to T do
L3      for each word i with at least one neighbour in V do
L4          q_i ← (Σ_{j ∈ N(i)} β_ij q_j + α_i q^_i) / (Σ_{j ∈ N(i)} β_ij + α_i)
L5  return Q
```

Line L1 starts at the original vectors. Line L3 skips the words with no neighbour in the vocabulary, so they keep their vectors, and so do words outside the lexicon. Line L4 replaces $\vec q_i$ by a weighted mean of its original vector and the current vectors of its neighbours. With the default weights, the original vector has the weight 1 and the neighbours share the weight 1, so the new vector is half the original and half the mean of the neighbours. The released code writes each new vector at once, so the later words of the same sweep see it: a Gauss-Seidel sweep. Using only the vectors of the previous sweep gives a Jacobi sweep. Both converge to the same fixed point.

## Example

Take three words in a chain, a - b - c, with one-dimensional original vectors $\hat q = (0, 0, 4)$, $\alpha = 1$ and $\beta_{ij} = 1/|N(i)|$. The updates are $q_a \leftarrow (q_b + 0)/2$, $q_b \leftarrow (q_a/2 + q_c/2 + 0)/2$ and $q_c \leftarrow (q_b + 4)/2$. The fixed point is $(1/3, 2/3, 7/3)$.

| sweep | Jacobi $(q_a, q_b, q_c)$ | max error | Gauss-Seidel $(q_a, q_b, q_c)$ | max error |
|---|---|---|---|---|
| 0 | (0, 0, 4) | 1.6667 | (0, 0, 4) | 1.6667 |
| 1 | (0, 1, 2) | 0.3333 | (0, 1, 2.5) | 0.3333 |
| 2 | (0.5, 0.5, 2.5) | 0.1667 | (0.5, 0.75, 2.375) | 0.1667 |
| 3 | (0.25, 0.75, 2.25) | 0.0833 | (0.375, 0.6875, 2.3438) | 0.0417 |

In Gauss-Seidel sweep 1, $q_a = (0 + 0)/2 = 0$, then $q_b = (0/2 + 4/2)/2 = 1$ uses the new $q_a$, then $q_c = (1 + 4)/2 = 2.5$ uses the new $q_b$. The vector of c moves from 4 toward its neighbour, and a and b move toward c.

With the symmetric weights $\beta_{ij} = 1$ instead, the fixed point is $(0.5, 1, 2.5)$, which is the minimizer of $\Psi$ with each edge counted once. The two weightings give different answers.

## Correctness

Write the system as $A Q = D_\alpha \hat Q$ over the words with neighbours, where the neighbours without neighbours of their own are constants. Row $i$ of $A$ has the diagonal $\alpha_i + \sum_j \beta_{ij}$ and off-diagonal entries of total absolute value at most $\sum_j \beta_{ij}$, so $A$ is [strictly diagonally dominant](/diagonally-dominant-matrix/) by rows and the system has one solution. A Jacobi sweep maps the error $\vec e$ to a vector whose entries are weighted sums of the old entries with nonnegative weights summing to at most

$$\rho = \max_i \frac{\sum_j \beta_{ij}}{\alpha_i + \sum_j \beta_{ij}} < 1,$$

so $\|\vec e\|_\infty$ shrinks by the factor $\rho$ per sweep, and a Gauss-Seidel sweep shrinks it by at least the same factor. With the default weights $\rho = 1/2$. When the weights are symmetric and the edges are counted once, $\Psi$ is strictly convex and the fixed point is its unique minimizer. The full proof is in the proof file.

## Complexity

Line L4 for word $i$ costs $O((|N(i)| + 1) d)$, so a sweep costs $O((V + E) d)$, where $E = \sum_i |N(i)|$, and $T$ sweeps cost $O(T(V + E)d)$. The memory is the $V d$ numbers of the new vectors (the original vectors are kept), plus $O(E)$ for the neighbour lists. With $\rho = 1/2$, 10 sweeps reduce the max-norm error to at most $2^{-10} \approx 0.001$ of its start.

## Properties

- **Deterministic.** The result depends only on the input and the order of the words in a sweep, and the limit does not depend on the order.
- **Local.** A word moves only if it has a neighbour in the vocabulary, and the change spreads along the lexicon edges.
- **Linear.** The output is a linear function of the original vectors. Each coordinate of the vectors is solved by the same system, independently.
- **Not exact after $T$ sweeps.** The result approaches the fixed point geometrically. A direct solve of the sparse system gives the fixed point exactly.
- **Any vectors.** The input can come from [skip-gram](/skip-gram-model/), [GloVe](/glove/), an SVD of counts or any other method.

## Variants and improvements

- **Weights.** Faruqui et al. give each word's neighbours the total weight 1. Equal weights $\beta_{ij} = 1$ make the method minimize $\Psi$ exactly, and words with many neighbours then move more.
- **Direct solve.** The system is sparse and diagonally dominant, so conjugate gradients (for symmetric weights) or a sparse direct solver also work. The matrix of the symmetric case is $D_\alpha$ plus a weighted [graph Laplacian](/laplacian-matrix/) of the lexicon.
- **Relation types.** Later work gives different weights to synonyms, hypernyms and antonyms, or pushes antonyms apart.
- **Sense vectors.** The same idea applied to sense-level lexicons gives one vector per word sense, linking retrofitting to [word sense disambiguation](/word-sense-disambiguation/).

## When to use it

Use it when you have trained vectors and a reliable lexicon, and you want the vectors to reflect the lexicon relations, for example for word similarity or for tasks where synonyms should behave alike. It is fast, since each sweep is linear in the size of the vocabulary and the lexicon, and it needs no corpus. It does not help words outside the lexicon, and it can hurt when the lexicon relation is not the similarity you need: words linked as related in a broad lexicon are pulled together even when they are not substitutes.

## Pitfalls

- **Self loops.** A lexicon may list a word as its own neighbour. Line L4 must skip $j = i$; otherwise the word counts its own current vector as a neighbour, and the fixed point changes.
- **Neighbours outside the vocabulary.** Line L4 must use only neighbours that have vectors. Counting the others in $\sum_j \beta_{ij}$ with no vector to add shrinks the vector toward zero.
- **Reading the paper's update as exact minimization.** With $\beta_{ij} = 1/|N(i)|$ the weights are not symmetric, and the result is the fixed point of line L4, not the minimizer of $\Psi$. A test that checks the gradient of $\Psi$ at the result must use symmetric weights.
- **Overwriting $\hat Q$.** Line L4 needs the original vector $\hat{\vec q}_i$ in every sweep. If line L1 aliases $Q$ and $\hat Q$ instead of copying, each sweep pulls toward the current vector and the method drifts toward the mean of each connected group.

## Implementations

## History

Faruqui, Dodge, Jauhar, Dyer, Hovy and Smith presented retrofitting at NAACL 2015 and released a short Python script. They reported gains on word similarity and other lexical tasks for several kinds of vectors and three lexicons (PPDB, WordNet and FrameNet). The method became a common way to add lexical knowledge to word vectors, and later work extended it to antonyms and to other languages.

## References
