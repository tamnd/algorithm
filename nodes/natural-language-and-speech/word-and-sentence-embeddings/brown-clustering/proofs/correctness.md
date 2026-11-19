---
title: Each Brown merge is the merge that keeps the most average mutual information
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The corpus has $V$ word types. The bigrams are the adjacent token pairs inside each sentence, $n(u, w)$ is the number of times the pair $(u, w)$ occurs, and $B = \sum_{u, w} n(u, w)$. All logs are natural.

**Notation.** A partition $\pi$ of the vocabulary into classes gives the class counts $n_\pi(l, m) = \sum_{u \in l} \sum_{w \in m} n(u, w)$. Let $p(l, m) = n_\pi(l, m) / B$, $p_L(l) = \sum_m p(l, m)$ and $p_R(m) = \sum_l p(l, m)$. Let

$$ q(l, m) = p(l, m) \log \frac{p(l, m)}{p_L(l)\, p_R(m)} \quad (\log = \ln), $$

with $q(l, m) = 0$ when $p(l, m) = 0$. If $p(l, m) > 0$, then $p_L(l) \ge p(l, m) > 0$ and $p_R(m) > 0$, so $q$ is well defined. The average mutual information of $\pi$ is $I(\pi) = \sum_{l, m} q(l, m)$, and for a class $i$ let $s(i) = \sum_l q(l, i) + \sum_m q(i, m) - q(i, i)$, the sum of $q$ over row $i$ and column $i$, with the cell $(i, i)$ counted once.

**Lemma 1 (the merge formula, equation 15 of Brown et al.).** Let $i \ne j$ be two classes of $\pi$ with $k$ classes, and let $\pi'$ be $\pi$ with $i$ and $j$ replaced by their union $i + j$. Then

$$ I(\pi') = I(\pi) - s(i) - s(j) + q(i, j) + q(j, i) + q'(i{+}j, i{+}j) + \sum_{l \ne i, j} \big[ q'(l, i{+}j) + q'(i{+}j, l) \big], $$

where $q'$ is $q$ computed in $\pi'$, that is, from the counts $n_{\pi'}(l, i{+}j) = n_\pi(l, i) + n_\pi(l, j)$, $n_{\pi'}(i{+}j, m) = n_\pi(i, m) + n_\pi(j, m)$, $n_{\pi'}(i{+}j, i{+}j)$ the sum of the four counts of $\{i, j\} \times \{i, j\}$, and the marginals $p_L'(i{+}j) = p_L(i) + p_L(j)$ and $p_R'(i{+}j) = p_R(i) + p_R(j)$.

*Proof.* Take a cell $(l, m)$ with $l, m \notin \{i, j\}$. Its count does not change. The row of $l$ in $\pi'$ has the same total as in $\pi$, because the merge only adds two cells of that row together, so $p_L'(l) = p_L(l)$. In the same way $p_R'(m) = p_R(m)$. So $q'(l, m) = q(l, m)$ for all these cells.

Let $R$ be the set of cells of $\pi$ in row $i$, row $j$, column $i$ or column $j$. The sum $s(i)$ covers row $i$ and column $i$, each cell once. The sum $s(j)$ covers row $j$ and column $j$. A cell is in both sets only if it is in row $i$ or column $i$ and also in row $j$ or column $j$. Rows $i$ and $j$ are disjoint, and so are columns $i$ and $j$, so the common cells are $(i, j)$ and $(j, i)$. Hence $\sum_{R} q = s(i) + s(j) - q(i, j) - q(j, i)$, and

$$ I(\pi) = \sum_{l, m \notin \{i, j\}} q(l, m) + s(i) + s(j) - q(i, j) - q(j, i). $$

The cells of $\pi'$ that are not of the form $(l, m)$ with $l, m \notin \{i, j\}$ are $(i{+}j, i{+}j)$ and, for each $l \ne i, j$, the cells $(l, i{+}j)$ and $(i{+}j, l)$. So

$$ I(\pi') = \sum_{l, m \notin \{i, j\}} q(l, m) + q'(i{+}j, i{+}j) + \sum_{l \ne i, j} \big[ q'(l, i{+}j) + q'(i{+}j, l) \big]. $$

Subtract the two equations to get the claim. $\square$

**Claim.** If $1 \le C$, BROWN-CLUSTERING stops, returns $\min(C, V)$ classes, and each merge it makes joins a pair $(i, j)$ of the current partition $\pi$ such that $I(\pi')$ is the largest over all pairs of classes of $\pi$. Ties go to the first pair in the order of line L6.

*Proof.* We use this invariant at the test of line L4.

> **(I)** The class list holds a partition $\pi_k$ of the vocabulary into $k$ classes, and the matrix $n$ is the $k \times k$ matrix $n_{\pi_k}$, with rows and columns in the order of the class list.

*Initialization.* Line L1 makes each word its own class, line L2 counts the word bigrams, which are the class bigrams of the partition into single words, and line L3 sets $k = V$. So (I) holds.

*Maintenance.* Assume (I) and $k > C$. Line L5 computes $p_L$, $p_R$, $q$, $s$ and $I(\pi_k)$ from $n = n_{\pi_k}$. For each pair $i < j$, line L7 evaluates the right side of Lemma 1: the terms $q'$ are computed from the merged counts and the merged marginals, exactly as the lemma defines them. So the value of line L7 is $I(\pi')$ for the partition $\pi'$ that merges $i$ and $j$. Line L8 keeps the first pair with the largest value, so the chosen pair maximizes $I(\pi')$ over all pairs. Line L9 adds row $j$ to row $i$ and then column $j$ to column $i$. After that, $n(i, m) = n_{\pi_k}(i, m) + n_{\pi_k}(j, m)$ for $m \ne i, j$, $n(l, i) = n_{\pi_k}(l, i) + n_{\pi_k}(l, j)$ for $l \ne i, j$, and $n(i, i)$ is the sum of the four counts of $\{i, j\} \times \{i, j\}$. Then line L9 deletes row and column $j$. The result is $n_{\pi'}$ with the merged class in place $i$, and the class list is changed in the same way. Line L10 sets $k \leftarrow k - 1$, so (I) holds for $\pi_{k-1} = \pi'$.

*Termination.* Each iteration lowers $k$ by 1. If $V \le C$ the loop does not run and the $V$ single classes are returned. Otherwise the loop stops when $k = C$, after $V - C$ merges, and line L11 returns $C$ classes. $\square$

**Corollary (likelihood).** Give the class bigram model $P(w \mid u) = P(c(w) \mid c(u))\, P(w \mid c(w))$ the relative frequency parameters $P(m \mid l) = p(l, m) / p_L(l)$ and $P(w \mid m) = p_R(w) / p_R(m)$, where $p_R(w)$ is the right marginal of the word $w$ in the word bigram matrix. Then the average log likelihood of the bigrams is

$$ \frac{1}{B} \sum_{u, w} n(u, w) \log P(w \mid u) = I(\pi) - H_R \quad (\log = \ln), $$

where $H_R = -\sum_w p_R(w) \log p_R(w)$ does not depend on $\pi$.

*Proof.* For a bigram $(u, w)$ with $n(u, w) > 0$, let $l = c(u)$ and $m = c(w)$. Then

$$ \log P(w \mid u) = \log \frac{p(l, m)}{p_L(l)} + \log \frac{p_R(w)}{p_R(m)} = \log \frac{p(l, m)}{p_L(l)\, p_R(m)} + \log p_R(w). $$

Multiply by $n(u, w) / B$ and sum over all pairs. The first term depends only on $(l, m)$, and the weights $n(u, w) / B$ with $u \in l$, $w \in m$ add up to $p(l, m)$, so the first term gives $I(\pi)$. In the second term the weights $n(u, w) / B$ with a fixed $w$ add up to $p_R(w)$, so it gives $\sum_w p_R(w) \log p_R(w) = -H_R$. $\square$

So among the partitions that one merge can reach, the merge of line L8 gives the class bigram model with the highest likelihood. This is a statement about one step. The greedy sequence of merges need not reach the partition into $C$ classes with the highest $I$; the page gives a corpus of one sentence where it does not. $\blacksquare$
