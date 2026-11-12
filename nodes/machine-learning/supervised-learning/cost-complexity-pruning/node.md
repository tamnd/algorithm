---
tag: V06HEB
kind: technique
slug: cost-complexity-pruning
name: Cost-complexity pruning
aliases:
- weakest link pruning
- minimal cost-complexity pruning
- CART pruning
area: machine-learning/supervised-learning
level: advanced
summary: "Prune a tree to minimize R(T) + alpha times its leaf count: the weakest-link steps give nested optimal subtrees, and cross-validation chooses alpha."
prereqs: [decision-tree, cross-validation]
see_also: [cart, reduced-error-pruning, c4-5, overfitting, tree-dynamic-programming, minimum-description-length, hyperparameter-tuning, decision-tree-learning]
sources:
  - book: isbn:9780412048418
    title: L. Breiman, J. H. Friedman, R. A. Olshen and C. J. Stone, Classification and Regression Trees, Wadsworth 1984, reprinted by Chapman and Hall/CRC
    locator: Chapter 3 (right-sized trees; minimal cost-complexity pruning, the smallest minimizing subtree and its uniqueness, the nested sequence by weakest-link cutting, cross-validation and the 1-SE rule) and Chapter 10 (optimal pruning)
  - book: isbn:9780387848570
    title: T. Hastie, R. Tibshirani and J. Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 9.2.2 (the cost-complexity criterion, weakest link pruning, the unique smallest subtree T_alpha, and the choice of alpha by five- or tenfold cross-validation)
  - paper: doi:10.1109/34.589207
    title: F. Esposito, D. Malerba and G. Semeraro, A comparative analysis of methods for pruning decision trees, IEEE Transactions on Pattern Analysis and Machine Intelligence 19(5), 1997
    locator: pages 476 to 491; cost-complexity pruning against the other methods, in theory and in experiments
---

Cost-complexity pruning cuts back a large [decision tree](/decision-tree/) by charging a price $\alpha \ge 0$ for each leaf. For each $\alpha$ it keeps the pruned subtree $T$ that minimizes
$$R_\alpha(T) = R(T) + \alpha\, |\tilde T|,$$
where $R(T)$ is the training risk (misclassified cases, or the sum of squared errors) and $|\tilde T|$ is the number of leaves. Breiman, Friedman, Olshen and Stone (1984, Chapter 3) proved that each $\alpha$ has a unique smallest minimizing subtree $T(\alpha)$, that these subtrees are nested as $\alpha$ grows, and that a simple *weakest-link* loop lists all of them. [Cross-validation](/cross-validation/) then picks $\alpha$. It is the pruning step of [CART](/cart/).

## In plain words

A tree grown until its leaves are pure fits the noise in the training data. Cutting off a branch makes more training errors but gives a simpler tree. Cost-complexity pruning puts a price on each leaf, so a branch stays only if the errors it saves are worth the leaves it uses.

If the price is zero, nothing is cut. As the price rises, the cheapest tree loses branches one at a time, and the branch to go next is the "weakest link": the one that saves the fewest errors per extra leaf. This gives a short list of trees, from the full tree down to the root alone. To pick one from the list, hold out part of the data, grow and prune on the rest, and see which price predicts best.

## When it applies

- You have a tree in which every node $t$ has a risk $R(t)$, its training risk as a leaf, and $R(t) \ge \sum_u R(u)$ over its children $u$. Resubstitution risks satisfy this: one constant for a whole node is never better than one constant for each child.
- The goal is a tree that predicts well on new data, and you have enough data to cross-validate.
- The criterion adds over leaves. Any additive leaf cost $R(t)$ works, such as misclassification cost with unequal costs, deviance, or squared error.
- It works for multiway trees as well as binary ones. The proofs need only that each internal node has at least two children.

## The template

Let $T_t$ be the branch at $t$, and for a pruned tree $T_k$, let $T_{k,t}$ be the branch at $t$ inside $T_k$.

```pseudo id=main
COST-COMPLEXITY-PRUNE(T_max, data)
L1  T_1 ← T_max with each node t made a leaf when R(t) = R(T_t), bottom-up; α_1 ← 0; k ← 1
L2  while T_k has an internal node do
L3      for each internal node t of T_k: g(t) ← (R(t) − R(T_{k,t})) / (|leaves(T_{k,t})| − 1)
L4      α_{k+1} ← the least g(t)
L5      T_{k+1} ← T_k with every t of g(t) = α_{k+1} made a leaf; k ← k + 1
L6  for each fold v of V: grow T^(v) on the other folds and run L1 to L5 on it
L7  for each k: CV(k) ← the total loss, on the held-out folds, of T^(v)(α'_k), α'_k = sqrt(α_k α_{k+1})
L8  return T_k for the k of least CV(k)
```

The quantity $g(t)$ is the increase of the training risk per leaf removed, when the branch at $t$ is replaced by a leaf: $R_\alpha$ of the leaf and of the branch are equal exactly at $\alpha = g(t)$. The node of least $g$ is the weakest link. Several nodes can tie, and line L5 collapses all of them at once.

For one fixed $\alpha$, a [dynamic program on the tree](/tree-dynamic-programming/) finds $T(\alpha)$ directly:
$$C_\alpha(t) = \min\Big(R(t) + \alpha,\ \sum_{u \text{ child of } t} C_\alpha(u)\Big),$$
making $t$ a leaf when the first term is at most the second. This is linear in the tree size.

**The theorem.** For each $\alpha \ge 0$, the smallest minimizer $T(\alpha)$ of $R_\alpha$ over the pruned subtrees of $T_{\max}$ is unique and contained in every minimizer. If $\alpha \le \beta$ then $T(\beta) \subseteq T(\alpha)$. The loop produces $0 = \alpha_1 < \alpha_2 < \dots < \alpha_K$ and $T_1 \supset T_2 \supset \dots \supset T_K = \{\text{root}\}$ with $T(\alpha) = T_k$ for all $\alpha \in [\alpha_k, \alpha_{k+1})$. This is the result of Breiman et al. (1984, Chapter 3); ESL (Section 9.2.2) states it. The proof below uses the recursion for $C_\alpha$: an internal node has at least two children, and every subtree has at least one leaf, so the advantage of keeping a node, $\sum_u C_\alpha(u) - R(t) - \alpha$, can only grow with $\alpha$. Hence a node once cut stays cut.

**Cross-validation.** The $\alpha_k$ of the full tree are not the $\alpha_k$ of a fold tree, so line L7 evaluates each fold tree at the geometric mean $\alpha'_k$ of the interval $[\alpha_k, \alpha_{k+1})$, as Breiman et al. do. The *1-SE rule* picks the smallest $T_k$ whose CV loss is within one standard error of the least; it gives smaller trees and is the book's default.

**Cost.** Each step of lines L3 to L5 is one postorder pass, $O(|T|)$, and there are fewer than $|T|$ steps, so the sequence costs $O(|T|^2)$ in the worst case; often far fewer steps occur, since one step can cut many nodes. Lines L6 to L8 repeat the growing $V$ times.

## Classic examples

**A small tree.** Take a classification tree whose nodes carry their misclassification counts $R$. The root has $R = 10$ and two children: $A$ with $R = 4$, whose two leaves have $R = 1$ and $1$; and $B$ with $R = 5$, whose children are a leaf with $R = 2$ and a node $B_2$ with $R = 2$ whose leaves have $R = 0$ and $1$. The full tree $T_1$ has 5 leaves and $R = 5$; no node has $R(t) = R(T_t)$.

| node | $R(t)$ | $R(T_{1,t})$ | leaves | $g(t)$ in $T_1$ | $g(t)$ in $T_2$ |
|---|---|---|---|---|---|
| root | 10 | 5 | 5 | 5/4 | 3/2 |
| $A$ | 4 | 2 | 2 | 2 | 2 |
| $B$ | 5 | 3 | 3 | **1** | cut |
| $B_2$ | 2 | 1 | 2 | **1** | cut |

- $\alpha_2 = 1$: $B$ and $B_2$ tie, and both are cut. $T_2$ has the leaves of $A$ and the leaf $B$: 3 leaves, $R = 7$.
- In $T_2$ the root has $g = (10 - 7)/(3 - 1) = 3/2 < 2$, so $\alpha_3 = 3/2$ and $T_3$ is the root alone.

The node $A$ is never cut by itself: for $\alpha \ge 3/2$, cutting the whole tree beats keeping $A$. Check at $\alpha = 1.2$: the full tree costs $5 + 6 = 11$, $T_2$ costs $7 + 3.6 = 10.6$, the root costs $11.2$, and $T_2$ with $A$ cut costs $9 + 2.4 = 11.4$. So $T(1.2) = T_2$, as the theorem says.

**CART.** [CART](/cart/) grows a maximal tree by Gini or squared-error decrease and prunes it by this technique, with 10-fold cross-validation; its page works the sequence for a six-point regression.

**A step function with noise.** On 120 points $x \in [0, 1]$ with $y = 10\,[x > 0.5]$ plus small integer noise, the maximal least-squares tree has more than 50 leaves. Five-fold cross-validation over its sequence picks the tree with 2 leaves, which splits near $x = 0.5$. The tests of the implementation check this.

## Variations

- **The 1-SE rule** instead of the minimum of the CV loss.
- **A held-out pruning set** instead of cross-validation: pick $T_k$ of least error on the held-out data. With a held-out set, [reduced-error pruning](/reduced-error-pruning/) is an alternative that does not restrict the answer to the sequence.
- **Other complexity terms.** Any penalty $\alpha \cdot \text{size}$ works with the same DP, for example counting all nodes. A penalty that is not linear in the size loses the nesting.
- **Pessimistic pruning** in [C4.5](/c4-5/) needs no held-out data, but it has no such optimality theorem.
- **Minimum description length pruning** charges bits for the tree and the exceptions, an additive cost of the same form ([MDL](/minimum-description-length/)).
- **Libraries.** scikit-learn exposes the sequence through `cost_complexity_pruning_path` and the parameter `ccp_alpha`; rpart in R uses the complexity parameter `cp`, which is $\alpha$ scaled by the risk of the root.

## Pitfalls

- **Using the training risk to choose $\alpha$.** $R(T_k)$ always falls as the tree grows, so it picks $T_1$. Choose $\alpha$ on data the tree did not see.
- **Comparing $\alpha$ across trees.** The values $\alpha_k$ depend on the tree. Evaluate the fold trees at representative values such as $\sqrt{\alpha_k \alpha_{k+1}}$, not at the index $k$.
- **Floating ties.** Two nodes with equal $g(t)$ must be cut in the same step. With floating point they can differ in the last bit, which adds a spurious step. Use exact arithmetic or a tolerance.
- **The weakest link is not always the smallest branch.** In the example, the whole tree goes before the branch $A$. Do not prune by looping over nodes in a fixed order; recompute $g$ after each step.
- **Gini for growing, misclassification for pruning.** CART grows classification trees by Gini but prunes them by the misclassification cost. Pruning by the Gini of the leaves gives a different sequence.

## Exercises

1. Show that $g(t) \ge 0$ for every internal node when the risks satisfy $R(t) \ge \sum_u R(u)$.
2. Give a tree where two nodes, neither an ancestor of the other, tie for the weakest link, and check that the theorem still holds when both are cut together.
3. Show that the sequence has at most $|\tilde T_{\max}|$ trees.
4. Find a tree and an $\alpha$ at which two different pruned subtrees both minimize $R_\alpha$, and check that the smaller one is contained in the larger one.
5. Show that the trees in the sequence correspond exactly to the vertices of the lower convex hull of the points $(|\tilde T|, \min R(T))$, where the minimum is over pruned subtrees with that many leaves.

## References
