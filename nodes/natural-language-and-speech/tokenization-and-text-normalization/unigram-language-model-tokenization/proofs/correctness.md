---
title: The unigram lattice recursions give the best segmentation, the total probability and the expected counts, and an EM step never lowers the likelihood
proves: [correctness, termination]
status: full
---

Notation. A model is a map $p$ from a finite set of pieces (nonempty strings) to probabilities with $\sum_w p(w) = 1$. All logs are natural logs. A word $x$ has $n$ characters, and positions are fenceposts $0, 1, \ldots, n$: the piece $x[i{:}j]$ covers the characters after position $i$ up to position $j$. A segmentation of $x$ is a list of pieces whose concatenation is $x$; its probability is $P(s) = \prod_{w \in s} p(w)$, with one factor per use, and $P(x) = \sum_s P(s)$. The lattice has the positions as nodes and an edge $i \to j$ of weight $p(x[i{:}j])$ for each piece $x[i{:}j]$ of the model. A segmentation is a path from $0$ to $n$, and its probability is the product of the edge weights.

**Lemma 1 (paths).** The map from segmentations of $x$ to paths $0 \to n$ in the lattice is a bijection that keeps the probability.

*Proof.* A segmentation $w_1 \cdots w_r$ fixes the cut positions $0 = c_0 < c_1 < \cdots < c_r = n$ with $w_k = x[c_{k-1}{:}c_k]$, and each $w_k$ is a piece, so each step is an edge. Conversely a path $c_0, \ldots, c_r$ gives the pieces $x[c_{k-1}{:}c_k]$, which join to $x$. The two maps are inverse, and both products have the same factors. $\square$

**Theorem 1 (Viterbi).** In the VITERBI semiring (log probabilities, plus = max, times = +), line V6 gives $\mathrm{best}[j] = \max_s \log P(s)$ over the segmentations $s$ of $x[{:}j]$, and VITERBI returns a segmentation of $x$ of the largest probability, or reports that none exists.

*Proof.* By induction on $j$. For $j = 0$ the only segmentation is empty, with log probability $0$ (line V2). For $j > 0$, the last piece of a segmentation of $x[{:}j]$ is some $x[i{:}j]$ in the model, and the rest is a segmentation of $x[{:}i]$; the log probability is the sum of the two parts. Lines V4 to V6 take the max over $i$ of $\mathrm{best}[i] + \log p(x[i{:}j])$, which by the induction hypothesis is the max over all segmentations. The pointer $\mathrm{back}[j]$ keeps an $i$ that reaches the max, so lines V7 and V8 rebuild a best segmentation. If no segmentation exists, $\mathrm{best}[n]$ stays at the semiring zero, $-\infty$. $\square$

**Theorem 2 (forward and backward).** In the LOG semiring (plus = log-add, times = +), $\alpha[j] = \log \sum_s P(s)$ over the segmentations of $x[{:}j]$, and $\beta[i] = \log \sum_s P(s)$ over the segmentations of $x[i{:}]$. So $\alpha[n] = \beta[0] = \log P(x)$.

*Proof.* The same induction as for Theorem 1, with the sum in place of the max: the segmentations of $x[{:}j]$ split, without overlap, by their last piece, and the probability factors into the last piece times the rest. The LOG semiring computes the log of these sums. The argument for $\beta$ runs from the right end. $\square$

**Theorem 3 (expected counts).** For each piece $w$, EXPECTED-COUNTS returns $E[c_w] = \sum_s P(s \mid x)\, c_w(s)$, where $c_w(s)$ is the number of uses of $w$ in $s$ and $P(s \mid x) = P(s) / P(x)$.

*Proof.* Write $c_w(s)$ as the number of edges $i \to j$ on the path of $s$ with $x[i{:}j] = w$. Swap the two sums: $E[c_w] = \sum_{(i, j) : x[i{:}j] = w} \sum_{s \ni (i, j)} P(s) / P(x)$. A path through the edge $i \to j$ is a path $0 \to i$, then the edge, then a path $j \to n$, and these choices are free, so the inner sum is $\exp(\alpha[i]) \, p(w) \, \exp(\beta[j])$ by Theorem 2. The code adds $\exp(\alpha[i] + \log p(w) + \beta[j] - \alpha[n])$ over these edges. $\square$

**Theorem 4 (EM).** Let $L(p) = \sum_x f_x \log P_p(x)$ for a corpus with word counts $f_x$, and let $p'$ be the model of EM-STEP. Then $L(p') \ge L(p)$.

*Proof.* This is the EM inequality for the hidden segmentation. Let $Q(q) = \sum_x f_x \sum_s P_p(s \mid x) \log P_q(s)$. For each word, Jensen's inequality on the concave log gives $\log P_q(x) - \log P_p(x) = \log \sum_s P_p(s \mid x) \frac{P_q(s)}{P_p(s)} \ge \sum_s P_p(s \mid x) \log \frac{P_q(s)}{P_p(s)}$, so $L(q) - L(p) \ge Q(q) - Q(p)$. Now $Q(q) = \sum_w C_w \log q(w)$ with $C_w = \sum_x f_x E_p[c_w]$, by Theorem 3. Over the probability vectors $q$ on the pieces, $\sum_w C_w \log q(w)$ is largest at $q(w) = C_w / \sum_v C_v$ (Gibbs' inequality), which is what lines E1 to E6 compute. So $Q(p') \ge Q(p)$ and $L(p') \ge L(p)$. A piece with $C_w = 0$ gets $q(w) = 0$, that is $-\infty$ in log space. $\square$

**Theorem 5 (termination of TRAIN).** TRAIN stops, and its result has at most $\max(T, A)$ pieces, where $T$ is the target size and $A$ is the number of characters of the corpus, and it holds every character of the corpus.

*Proof.* The seed holds every character (SEED-VOCABULARY adds them first), and lines T5 and T10 never remove a character: FLOOR-CHARACTERS removes only pieces of probability $0$ that are not single characters. If the loop does not stop at line T6, the model has more than $T$ pieces and at least one piece of length 2 or more. Line T8 sets the new size to $\max(T, \lfloor \eta N \rfloor)$, which is less than the current size $N$ because $N > T$ and $\eta < 1$, and lines T9 and T10 keep at most that many pieces. So the size drops at every round, and the loop stops after at most $N_0$ rounds for a seed of $N_0$ pieces. At the stop, either the size is at most $T$ or only characters are left. $\square$

The pruning rule itself, keeping the pieces whose removal lowers the likelihood the most, is a heuristic: it does not find the vocabulary of size $T$ of the largest likelihood, and the page does not claim that it does.
