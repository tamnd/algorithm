---
title: IA-Select is greedy on a monotone submodular objective, so it is a (1 - 1/e) approximation
proves: [correctness]
status: full
---

Let $C$ be a finite set of categories (intents) with $P(c \mid q) \ge 0$ and $\sum_c P(c \mid q) = 1$, and let $D$ be a finite set of documents with values $V(d \mid q, c) \in [0, 1]$, taken as $0$ when $c$ is not a category of $d$. Write $P(c)$ and $V(d, c)$ for short. For $S \subseteq D$ define

$$f(S) = P(S \mid q) = \sum_{c \in C} P(c) \Big(1 - \prod_{d \in S} \big(1 - V(d, c)\big)\Big),$$

the objective of Agrawal et al. (Equation 1 of their paper). The task is to find $S$ with $|S| = k$ that maximizes $f$.

**Lemma 1 (invariant).** Before each pass of the loop of line L3, with $S$ the set of documents chosen so far, $U(c) = P(c) \prod_{d \in S} (1 - V(d, c))$ for every $c$.

*Proof.* Line L1 sets $U(c) = P(c)$, the empty product. Lines L7 and L8 multiply $U(c)$ by $1 - V(b, c)$ for the new document $b$ and each category of $b$; for the other categories the factor would be $1$. $\square$

So $U(c)$ is the probability that the intent is $c$ and no chosen document satisfies it. It is not a conditional probability: in the example of the paper, $0.7$ becomes $0.35$ and is not renormalized.

**Lemma 2 (the gain is the marginal gain).** Line L5 computes $g(d) = f(S \cup \{d\}) - f(S)$.

*Proof.* For each $c$, adding $d$ multiplies the product of $f$ by $1 - V(d, c)$, so the term of $c$ grows by $P(c) \prod_{d' \in S} (1 - V(d', c)) \cdot V(d, c) = U(c) V(d, c)$ by Lemma 1. Summing over the categories of $d$ gives line L5. $\square$

**Lemma 3 (the objective).** $f(\emptyset) = 0$, $f$ is monotone, and $f$ is submodular: for $A \subseteq B \subseteq D$ and $d \notin B$, $f(A \cup \{d\}) - f(A) \ge f(B \cup \{d\}) - f(B) \ge 0$.

*Proof.* The empty product is $1$, so $f(\emptyset) = 0$. By Lemma 2 the marginal gain at $S$ is $\sum_c P(c) V(d, c) \prod_{d' \in S} (1 - V(d', c))$. Every factor lies in $[0, 1]$, so the gain is at least $0$, and each product over $B$ is the product over $A$ times more factors in $[0, 1]$, so it is no larger. $\square$

Agrawal et al. state the theorem of Nemhauser, Wolsey and Fisher (their Theorem 2) for "a submodular set function". The guarantee needs more: the function must also be monotone with $f(\emptyset) = 0$. Lemma 3 shows that $f$ has both properties, so the conclusion holds here.

**Theorem 4 (approximation).** If $|D| \ge k$, the set $G$ that IA-Select returns satisfies $f(G) \ge \big(1 - (1 - 1/k)^k\big) f(O) \ge (1 - 1/e)\, f(O)$ for every $O \subseteq D$ with $|O| = k$. If $|D| < k$, it returns $D$, which is optimal.

*Proof.* The scan of lines L4 to L6 keeps a document with the largest value of line L5, so by Lemma 2 each pick $b_{i+1}$ maximizes the marginal gain over the remaining documents, whatever the tie rule. Let $G_i$ be the first $i$ picks and $O = \{o_1, \ldots, o_k\}$. By monotonicity and submodularity (Lemma 3),

$$f(O) \le f(G_i \cup O) \le f(G_i) + \sum_{j=1}^{k} \big(f(G_i \cup \{o_j\}) - f(G_i)\big) \le f(G_i) + k\, \big(f(G_{i+1}) - f(G_i)\big),$$

where the middle step adds the elements of $O$ one at a time and bounds each gain by its gain at $G_i$, and the last step uses that $b_{i+1}$ has the largest gain (a document of $O$ already in $G_i$ has gain $0$). So $f(O) - f(G_{i+1}) \le (1 - 1/k)(f(O) - f(G_i))$. From $f(G_0) = 0$, $f(O) - f(G_k) \le (1 - 1/k)^k f(O) \le e^{-1} f(O)$. If $|D| < k$, every set of at most $k$ documents is a subset of $D$, and $f(D)$ is the largest value by monotonicity. $\square$

The test file checks Theorem 4 against the optimum over all $k$-subsets on random instances.

**Theorem 5 (one category per document).** If every document has at most one category with a positive value, IA-Select is optimal for every $k$.

*Proof.* Group the documents by category, and inside category $c$ sort them by value, $v_{c,1} \ge v_{c,2} \ge \cdots$. Taking the $i$-th document of $c$ after the first $i - 1$ adds $h_{c,i} = P(c)\, v_{c,i} \prod_{l < i}(1 - v_{c,l})$, and $h_{c,i} \le h_{c,i-1}$ because $v_{c,i} \le v_{c,i-1}$ and $1 - v_{c,i-1} \le 1$. A set that takes $j_c$ documents from $c$ has the value $\sum_c P(c)(1 - \prod(1 - v))$ over its documents, which is at most $\sum_c \sum_{i \le j_c} h_{c,i}$, because the term of $c$ grows with each value and is symmetric, so the $j_c$ largest values of $c$ maximize it. So $f(O)$ is at most the sum of $k$ entries of the sequences $h_{c,\cdot}$, taken as prefixes, and since each sequence is non-increasing, at most the sum of the $k$ largest entries of all sequences together. IA-Select takes, inside each category, the documents in the order of their values, because the gain $U(c) V(d, c)$ has the same $U(c)$ for all documents of $c$. So at each step its gain is the largest head among the sequences, and $k$ steps of taking the largest head of non-increasing sequences give the $k$ largest entries. So $f(G)$ reaches the bound. $\square$

Agrawal et al. state this result as their Theorem 1 and Corollary 1.

**Lemma 6 (hardness).** Maximizing $f$ under $|S| = k$ is NP-hard.

*Proof.* Given an instance of [maximum coverage](/max-coverage/), with ground set $C$ and sets $D$, let $P(c) = 1/|C|$ and $V(d, c) = 1$ if $c \in d$ and $0$ otherwise. Then $f(S)$ is the fraction of $C$ covered by $S$, so an optimal $S$ for $f$ solves the coverage instance. $\square$

This is the reduction of Lemma 1 of Agrawal et al. With [max coverage inapproximability](/max-coverage-inapproximability/), no polynomial-time algorithm has a better constant than $1 - 1/e$ unless P = NP.

**Greedy is not always optimal.** Table 1 of the paper: $P(c_1) = P(c_2) = 0.5$, $V(d_1, \cdot) = (0.8, 0.8)$, $V(d_2, \cdot) = (1, 0)$, $V(d_3, \cdot) = (0, 1)$. The first pick is $d_1$ with gain $0.8$, against $0.5$ for the others. Then $U = (0.1, 0.1)$, both remaining documents gain $0.1$, and the tie rule gives $d_2$, so $f(\{d_1, d_2\}) = 0.9$, while $f(\{d_2, d_3\}) = 1$. Here $0.9 \ge (1 - 1/e) \cdot 1 \approx 0.632$, as Theorem 4 requires.

**Cost.** Let $n = |D|$, $m = |C|$ and $e = \sum_d |\{c : V(d, c) > 0\}| \le nm$. Each of the $k$ passes computes $n$ gains in $O(e)$ total time and updates at most $m$ values, so IA-Select runs in $O(n \log n + k e) = O(n \log n + nmk)$ time with $O(n + m)$ extra space.
