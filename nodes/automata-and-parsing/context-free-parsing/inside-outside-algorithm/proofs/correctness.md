---
title: The inside-outside algorithm computes the expected rule counts, and its update never lowers the likelihood
proves: [correctness]
status: full
---

**Notation.** $G = (V, \Sigma, P, S)$ is in Chomsky normal form: every rule is $A \to B C$ with $B, C \in V$, or $A \to a$ with $a \in \Sigma$, or $S \to \varepsilon$, and in the last case $S$ is on no right side. $\theta(r) \ge 0$ is the probability of rule $r$. For a sentence $w = a_1 \cdots a_n$, $T(w)$ is the set of parse trees of $w$ from $S$, and $P_\theta(t) = \prod_r \theta(r)^{f_r(t)}$, where $f_r(t)$ is the number of uses of $r$ in $t$. $Z(w) = \sum_{t \in T(w)} P_\theta(t)$. A node of a tree is labeled by $(A, i, j)$ when it has the nonterminal $A$ and its yield is $a_{i+1} \cdots a_j$. For $n \ge 1$, $T_A(i, j)$ is the set of trees with root $A$ and yield $a_{i+1} \cdots a_j$, and $\beta(A, i, j)$, $\alpha(A, i, j)$ are the values that the algorithm computes at lines L4, L5 and L7 to L9.

**Fact 1 (spans).** For $n \ge 1$, no tree of $T(w)$ uses $S \to \varepsilon$, since $S$ is on no right side and the root has a nonempty yield. Every node has a nonempty yield, so the two children of a binary node have nonempty yields that split the span of the node: $i < k < j$. Hence a proper descendant of a node has a strictly shorter span. Two nodes with the same span cannot be nested, and two nodes that are not nested have disjoint spans, so a tree has at most one node with a given span $(i, j)$.

**Lemma 1 (inside).** For $n \ge 1$ and $0 \le i < j \le n$, $\beta(A, i, j) = \sum_{t \in T_A(i, j)} P_\theta(t)$.

*Proof.* By induction on $j - i$. If $j = i + 1$, a tree in $T_A(i, i + 1)$ is a single rule $A \to a_{i+1}$, since a binary rule would need a span of length at least 2. Line L4 sums $\theta(A \to a_{i+1})$. If $j - i \ge 2$, the root uses a binary rule $A \to B C$ and splits at a unique $k$ with $i < k < j$, and the tree is determined by the rule, $k$, a tree of $T_B(i, k)$ and a tree of $T_C(k, j)$. Its probability is the product of $\theta(A \to B C)$ and the probabilities of the two subtrees. Summing over all choices, and using the induction for the shorter spans, gives the sum at line L5, which runs after all shorter spans are final. $\square$

**Outside trees.** For $n \ge 1$, an **outside tree** for $(A, i, j)$ is a tree with root $S$ and yield $a_1 \cdots a_i\, A\, a_{j+1} \cdots a_n$, in which exactly one leaf, the **hole**, is the nonterminal $A$. Its probability is the product of $\theta$ over its rules. Let $O(A, i, j)$ be the set of outside trees.

**Lemma 2 (outside).** For $n \ge 1$, $\alpha(A, i, j) = \sum_{u \in O(A, i, j)} P_\theta(u)$.

*Proof.* By induction on $n - (j - i)$. For $(i, j) = (0, n)$, the hole spans the whole sentence. If it is not the root, its parent spans more than $n$ symbols, which is impossible by the argument of Fact 1. So the only outside tree is the hole alone, as root, with $A = S$ and probability 1, which is line L7. For a shorter span, the hole is not the root, and its parent is a binary node $(D, i', j')$ with a rule $D \to X Y$. Either the hole is the left child, so $A = X$, $i' = i$, $j' > j$, and the right child is a complete tree of $T_Y(j, j')$; or it is the right child, so $A = Y$, $j' = j$, $i' < i$, and the left child is a tree of $T_X(i', i)$. Cutting the tree at the parent gives an outside tree for $(D, i', j')$ with a longer span. This is a bijection between $O(A, i, j)$ and the triples of a parent rule and position, an outside tree of the parent, and a sibling tree. The probability is the product of the parts. By the induction for the longer span and Lemma 1 for the sibling, the sum is the total that line L9 adds to $\alpha(A, i, j)$. Line L8 processes spans by decreasing length, so $\alpha(D, i', j')$ is final when it is used. $\square$

**Lemma 3 (node marginals).** For $n \ge 1$, $\sum \{P_\theta(t) : t \in T(w)$ has a node $(A, i, j)\} = \alpha(A, i, j)\, \beta(A, i, j)$.

*Proof.* By Fact 1, a tree has at most one node with the span $(i, j)$. Cutting a tree at its node $(A, i, j)$ gives an outside tree of $O(A, i, j)$ and an inside tree of $T_A(i, j)$, and putting the inside tree into the hole is the inverse. The probability of the tree is the product of the two. Lemma 1 and Lemma 2 give the result. $\square$

**Lemma 4 (expected counts).** For a sentence with $Z(w) > 0$, the values that lines L3, L10 and L11 add for $w$ are $E_\theta[f_r \mid w] = \sum_{t \in T(w)} P_\theta(t) f_r(t) / Z(w)$ for every rule $r$, and $Z(w)$ at line L6 is the probability of $w$.

*Proof.* If $n = 0$, the only tree is $S \to \varepsilon$, used once, so line L3 is right. Let $n \ge 1$. By Lemma 1, line L6 computes $\beta(S, 0, n) = Z(w)$. For a binary rule $r = A \to B C$, $f_r(t)$ is the number of triples $i < k < j$ such that $t$ has a node $(A, i, j)$ that uses $r$ with split $k$, because a node has one span and one split. So
$$\sum_t P_\theta(t) f_r(t) = \sum_{i < k < j} \sum \{P_\theta(t) : t \text{ has a node } (A, i, j) \text{ that uses } r \text{ at } k\}.$$
As in Lemma 3, such trees correspond to an outside tree for $(A, i, j)$, a tree of $T_B(i, k)$ and a tree of $T_C(k, j)$, so the inner sum is $\alpha(A, i, j)\, \theta(r)\, \beta(B, i, k)\, \beta(C, k, j)$. Dividing by $Z(w)$ gives line L10. For $r = A \to a$, $f_r(t)$ is the number of positions $i$ with $a_{i+1} = a$ such that $t$ has the node $(A, i, i + 1)$ with this rule, and the same argument gives $\alpha(A, i, i + 1)\, \theta(r) / Z(w)$, which is line L11. $\square$

**Lemma 5 (the update maximizes the expected log probability).** Let $c(r)$ be the totals of line L1 to line L11 over the sentences with $Z(w) > 0$, and $Q(\theta') = \sum_r c(r) \log \theta'(r)$, with $0 \log 0 = 0$ and $c \log 0 = -\infty$ for $c > 0$. Among all $\theta'$ such that the rules of each nonterminal sum to 1, line L12 gives a maximizer of $Q$.

*Proof.* $Q$ is a sum over the nonterminals $A$ of $Q_A = \sum_{A \to \gamma} c(A \to \gamma) \log \theta'(A \to \gamma)$, and the constraints are separate for each $A$. If $C_A = \sum_\gamma c(A \to \gamma) = 0$, $Q_A = 0$ for every choice, and line L12 keeps $\theta$. If $C_A > 0$, let $\hat\theta(A \to \gamma) = c(A \to \gamma) / C_A$. For any $\theta'$ with $\theta'(A \to \gamma) > 0$ whenever $c(A \to \gamma) > 0$, the concavity of $\log$ (Jensen's inequality) gives
$$Q_A(\theta') - Q_A(\hat\theta) = C_A \sum_{c > 0} \hat\theta(A \to \gamma) \log \frac{\theta'(A \to \gamma)}{\hat\theta(A \to \gamma)} \le C_A \log \sum_{c > 0} \theta'(A \to \gamma) \le C_A \log 1 = 0.$$
Other $\theta'$ give $Q_A = -\infty$. So $\hat\theta$, which is line L12, is a maximizer. $\square$

**Theorem.** EM-STEP returns $\theta'$ with the rules of each nonterminal summing to 1 (for every nonterminal that has a rule with a positive expected count, and otherwise its old values), and $\prod_w Z_{\theta'}(w) \ge \prod_w Z_\theta(w)$, where both products run over the sentences of the corpus with $Z_\theta(w) > 0$.

*Proof.* The normalization is line L12. By Lemma 4, the totals are $c(r) = \sum_w E_\theta[f_r \mid w]$, summed over the sentences with $Z_\theta(w) > 0$. Fix such a $w$, and let $q(t) = P_\theta(t) / Z_\theta(w)$ for $t \in T(w)$, which is a probability distribution on the trees with $q(t) > 0$. For any $\theta'$, Jensen's inequality gives
$$\log Z_{\theta'}(w) \ge \log \sum_{q(t) > 0} P_{\theta'}(t) = \log \sum_{q(t) > 0} q(t) \frac{P_{\theta'}(t)}{q(t)} \ge \sum_t q(t) \log \frac{P_{\theta'}(t)}{q(t)},$$
with equality for $\theta' = \theta$, because then $P_\theta(t) / q(t) = Z_\theta(w)$ for every $t$. Subtracting the two cases,
$$\log Z_{\theta'}(w) - \log Z_\theta(w) \ge \sum_t q(t) \bigl(\log P_{\theta'}(t) - \log P_\theta(t)\bigr) = \sum_r E_\theta[f_r \mid w] \bigl(\log \theta'(r) - \log \theta(r)\bigr).$$
Summing over the sentences gives $\sum_w \log Z_{\theta'}(w) - \sum_w \log Z_\theta(w) \ge Q(\theta') - Q(\theta)$. $Q(\theta)$ is finite, because a rule with $c(r) > 0$ is used in a tree of positive probability, so $\theta(r) > 0$. By Lemma 5, $Q(\theta') \ge Q(\theta)$ for the $\theta'$ of line L12, which also satisfies the constraints of Lemma 5. So the sum of the logarithms does not decrease, and the products satisfy the claim. $\blacksquare$
