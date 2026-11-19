---
title: "The mention-pair model: the training pairs have correct labels, the linkers follow their rules, and the output is a partition"
proves: [correctness]
status: full
---

Fix mentions $0, 1, \ldots, N - 1$ in document order (the numbering of the code), a gold chain $c(k)$ for each mention (or none), and a classifier that gives a probability $p(i, j)$ for each pair $i < j$. The threshold is $\theta = 0.5$. The line numbers refer to the pseudocode on the page. Whether the classifier is accurate is a measurement; what follows holds for any classifier.

## Claim 1: every training pair has the correct label

Line L1 takes, for a mention $j$ with an earlier mention of its chain, the closest one $i = \max\{k < j : c(k) = c(j)\}$. Line L2 labels $(i, j)$ positive, which is correct since $c(i) = c(j)$. It labels $(k, j)$ negative for each $i < k < j$. If such a $k$ had $c(k) = c(j)$, it would be an earlier mention of the chain closer to $j$ than $i$, against the choice of $i$. So every negative pair is in fact not coreferent. Each anaphoric mention gives exactly one positive pair, and a mention with no earlier chain mate gives no pair at all. In the variant of Ng and Cardie (2002), the positive antecedent of a non-pronominal anaphor can be farther away than the closest chain mate, so mentions of the same chain can lie between them; the code skips those, and the argument above applies to the rest.

## Claim 2: the gradient of the logistic loss

For a weight vector $w$ and pairs $(x, y)$ with $y \in \{0, 1\}$, the loss is $L(w) = \frac{1}{m} \sum (\log(1 + e^{z}) - y z) + \frac{\lambda}{2} |w|^2$ with $z = w \cdot x$ (natural log). The derivative of $\log(1 + e^{z}) - y z$ in $z$ is $\sigma(z) - y$, where $\sigma$ is the logistic function, and $\partial z / \partial w_k = x_k$. Hence $\nabla L = \frac{1}{m} \sum (\sigma(w \cdot x) - y) x + \lambda w$, which is what log_loss_grad returns. The code computes $\log(1 + e^{t})$ as $\max(t, 0) + \log(1 + e^{-|t|})$, which is the same value without overflow. The test file checks the gradient against central finite differences.

## Claim 3: the two linkers

Closest first (lines L4 to L6): for each $j$, the inner loop tries $i = j - 1, j - 2, \ldots, 0$ and stops at the first $i$ with $p(i, j) > \theta$. So the link is $\max\{i < j : p(i, j) > \theta\}$, or none if the set is empty, as in Soon et al. (2001, Section 2.5). Best first: the loop keeps the largest probability seen so far, starting from $\theta$, and replaces it only on a strictly larger value, scanning from the closest $i$. So the link is a maximizer of $p(i, j)$ over $\{i < j : p(i, j) > \theta\}$, and among equal maxima the closest one, since a later (farther) $i$ with the same value does not replace it. The test file checks both against these set definitions on random tables.

## Claim 4: the output is a partition

Each mention $j$ gets at most one link, to an earlier mention. A directed edge from each $j$ to its antecedent goes from a larger to a smaller index, so the edges form no cycle and the graph is a forest. Line L7 takes the connected components with a union-find structure ([disjoint-set](/disjoint-set/)): each union joins two components, and two mentions end with the same root exactly when a path of links joins them. The components are disjoint and cover all mentions, so the output is a partition of the mentions into entities. The test file compares the components with a graph search.

## Claim 5: the pairwise decisions need not be transitive

Coreference is an equivalence relation, but the classifier decides each pair alone. In the example of the page, $p(2, 3) = 0.52$ and $p(0, 3) = 0.8$ are above $\theta$, while $p(0, 2) = 0.2$ is below it. No partition agrees with all three decisions, because two of them put 0, 2 and 3 in one entity and the third separates 0 and 2. The clustering step resolves such conflicts: closest first and best first keep only one link per mention and then take the transitive closure, which can join two mentions the classifier called not coreferent. Finding the partition that agrees with the most weighted pairwise decisions is correlation clustering, which is NP-hard (Bansal, Blum and Chawla 2004); the linkers are greedy heuristics for it.
