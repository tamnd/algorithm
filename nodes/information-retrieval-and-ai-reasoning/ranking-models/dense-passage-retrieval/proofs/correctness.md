---
title: The gradient of the in-batch negative loss, its bounds, and exact inner-product top-k
proves: [correctness]
status: full
---

A batch has $B$ question vectors $q_1, \ldots, q_B$ and $m \ge B$ passage vectors $c_1, \ldots, c_m$ in $\mathbb R^d$. For $i \le B$, $c_i$ is the positive passage of question $i$, and every other $c_k$ is a negative for it: the positives of the other questions, and any extra negatives such as one BM25 hard negative per question. The vectors are the outputs of the two encoders, which this proof treats as given. Let $S_{ik} = q_i \cdot c_k$ and

$$p_{ik} = \frac{e^{S_{ik}}}{\sum_{l=1}^{m} e^{S_{il}}}, \qquad L = \frac{1}{B} \sum_{i=1}^{B} -\log p_{ii}.$$

This is the negative log-likelihood of Karpukhin et al. (2020), Equation (2), with the in-batch negatives of their Section 3.2.

**Lemma 1 (gradient).**

$$\frac{\partial L}{\partial q_i} = \frac{1}{B} \sum_{k=1}^{m} (p_{ik} - [k = i])\, c_k, \qquad \frac{\partial L}{\partial c_k} = \frac{1}{B} \sum_{i=1}^{B} (p_{ik} - [k = i])\, q_i.$$

*Proof.* $-\log p_{ii} = -S_{ii} + \log \sum_l e^{S_{il}}$, so $\partial(-\log p_{ii}) / \partial S_{ik} = p_{ik} - [k = i]$, and $S_{ik}$ does not enter any other row. Since $\partial S_{ik} / \partial q_i = c_k$ and $\partial S_{ik} / \partial c_k = q_i$, the chain rule gives both sums. $\square$

Lines L1 to L3 of the code compute $S$, the rows of log-probabilities and $L$, and lines L4 and L5 accumulate the coefficient $(p_{ik} - [k = i])/B$ times the other vector. One batch costs $O(B m d)$ time for $S$ and the same for the gradients. With a matrix library the two gradients are $G C$ and $G^\top Q$, where $G$ is the matrix of the coefficients.

A passage $c_k$ that is not a positive ($k > B$) gets $\partial L / \partial c_k = \frac{1}{B} \sum_i p_{ik} q_i$, a pull away from every question in proportion to how much probability it takes. The positive $c_i$ gets the push $-\frac{1}{B}(1 - p_{ii}) q_i$ toward its question, plus the pulls from the other questions that score it.

**Lemma 2 (bounds).** $L > 0$. If all scores of row $i$ are equal, its term is $\log m$. The term of row $i$ tends to 0 exactly when $S_{ii} - S_{ik} \to \infty$ for every $k \ne i$.

*Proof.* $p_{ii} < 1$ because every $e^{S_{ik}} > 0$, so $-\log p_{ii} > 0$. Equal scores give $p_{ii} = 1/m$. The term is $\log(1 + \sum_{k \ne i} e^{S_{ik} - S_{ii}})$, which tends to 0 exactly when each exponent tends to $-\infty$. $\square$

So each question of a batch with $B$ questions and no extra negatives is trained against $B - 1$ negatives at no extra encoding cost, since the other positives are already encoded. With one hard negative per question, $m = 2B$ and each question has $2B - 1$ negatives.

**Lemma 3 (exact top-k).** Line L7 returns the $k$ passages with the largest $q \cdot c$, and among equal scores the smaller ids, in that order.

*Proof.* Sorting by the key $(-q \cdot c_p, p)$ orders the passages by score, highest first, and then by id. The keys are distinct, because the ids are, so the first $k$ entries are the $k$ smallest keys. $\square$

Exact search is the reference that approximate indexes such as [HNSW](/hnsw/) approximate. It costs $O(N d)$ per query for $N$ passages, plus the sort.

**What is outside the proof.** Nothing here says that training makes relevant passages nearest neighbors on new questions. The encoders, their training data and their retrieval accuracy are outside the code, and the accuracy figures of the paper are measurements.

The tests in `impl/python/test_dense_passage_retrieval.py` check Lemma 1 by central finite differences in every coordinate of $q$ and $c$ on random batches, the loss against a direct sum, Lemma 2, that a small step against the gradient lowers the loss, Lemma 3 with ties against a brute force, and the worked example of the page.
