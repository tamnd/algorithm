---
tag: QKQX68
kind: technique
slug: reduced-error-pruning
name: Reduced-error pruning
aliases:
- REP
- reduced error pruning
- validation-set pruning of decision trees
area: machine-learning/supervised-learning
level: advanced
summary: "Prune a decision tree bottom-up on a held-out set: make a node a leaf when that does not add errors. One linear pass gives the smallest most-accurate pruning."
prereqs: [decision-tree, overfitting]
see_also: [cost-complexity-pruning, c4-5, id3, decision-tree-learning, cross-validation, tree-dynamic-programming, early-stopping]
sources:
  - paper: doi:10.1016/S0020-7373(87)80053-6
    title: J. R. Quinlan, Simplifying decision trees, International Journal of Man-Machine Studies 27(3), 1987
    locator: pages 221 to 234; the section on reduced error pruning (replace a subtree by its best leaf if that does not increase the errors on a separate test set, and no subtree of it has the same property)
  - paper: doi:10.1109/34.589207
    title: F. Esposito, D. Malerba and G. Semeraro, A comparative analysis of methods for pruning decision trees, IEEE Transactions on Pattern Analysis and Machine Intelligence 19(5), 1997
    locator: pages 476 to 491; the section on reduced error pruning (bottom-up, linear in the number of nodes, and it finds the smallest version of the most accurate subtree on the pruning set) and the experiments
  - book: isbn:9780070428072
    title: T. M. Mitchell, Machine Learning, McGraw-Hill, 1997
    locator: Section 3.7.1.1 (reduced error pruning with a validation set, and its accuracy curve) and Section 3.7.1 (avoiding overfitting the data)
---

Reduced-error pruning (REP) cuts back a [decision tree](/decision-tree/) with a separate *pruning set* $V$ of labeled cases that the tree did not see in training. Going from the leaves up, it makes a node a leaf, labeled with its majority training class, when that does not increase the number of errors on $V$. Quinlan (1987) proposed it. One bottom-up pass is linear in the tree size, and it returns the smallest pruned tree with the fewest errors on $V$ (Esposito, Malerba and Semeraro 1997).

## In plain words

A tree grown until its leaves are pure has learned the noise in its training data. To find the branches that help only on the training data, test the tree on data it has not seen. For each branch, ask: if this branch were one leaf that predicts its most common training class, would the tree make more mistakes on the held-out data? If not, cut it.

Work from the bottom up. Then each branch is judged in its best pruned form, not in its original form. On a tie, cut, because a smaller tree is easier to read and is less likely to overfit.

## When it applies

- You have a grown tree, and enough labeled data to hold some of it back. Mitchell (1997) suggests about one third of the data for the pruning set.
- Each node stores a label, the majority class of the training cases that reached it. Pruning only turns internal nodes into leaves; it does not change any test or label.
- The goal is a small tree that is accurate on new data. The method needs no parameter and no statistical assumption, unlike the pessimistic pruning of [C4.5](/c4-5/).
- It works for multiway trees such as those of [ID3](/id3/) as well as for binary ones. A case whose value has no branch stops at the node and takes its label.

## The template

```pseudo id=main
REDUCED-ERROR-PRUNE(T, V)
L1  route each case of V down T; wrong(t) ← its cases with class ≠ label(t)
L2  return PRUNE(root of T)
PRUNE(t)
L3  if t is a leaf then return wrong(t)
L4  sub ← Σ PRUNE(u) over the children u of t, plus the errors of the cases that stop at t
L5  if wrong(t) ≤ sub then make t a leaf; return wrong(t)
L6  return sub
```

$\mathrm{wrong}(t)$ is the number of errors that $t$ would make on $V$ as a leaf, and PRUNE returns the least number of errors on $V$ of any pruning of the branch at $t$. Both counts come from one pass of $V$ down the full tree: whether a case reaches $t$ does not depend on what is cut below $t$.

**The theorem.** Let $E^*(t)$ be the least number of errors on the cases that reach $t$, over all prunings of the branch at $t$. Then
$$E^*(t) = \min\Big(\mathrm{wrong}(t),\ \mathrm{stop}(t) + \sum_u E^*(u)\Big),$$
and the tree that PRUNE leaves has $E^*(\text{root})$ errors and is contained in every pruning with that many errors. So it is the unique smallest most-accurate pruning on $V$. Esposito, Malerba and Semeraro (1997) state this property. The proof is an induction on the height, and it is the same as for [cost-complexity pruning](/cost-complexity-pruning/) with $\alpha = 0$ and the training risk replaced by the errors on $V$. Ties must be pruned: a tie kept would give a larger tree with the same errors.

**Quinlan's statement.** Quinlan (1987) phrased the rule as a loop: replace a subtree by a leaf if that does not increase the errors on the test set and no subtree of it has the same property, until no subtree qualifies. This loop always ends at the same tree as the bottom-up pass; the proof shows why.

**Cost.** Line L1 walks each of the $m$ cases down one path, in $O(m h)$ for a tree of depth $h$. PRUNE visits each node once, in $O(|T|)$. The total is $O(m h + |T|)$.

## Classic examples

**A worked tree.** The counts are the positive and negative pruning cases $(p, n)$ that reach each node, and a node labeled $+$ errs on its negative cases. The root, labeled $+$, has $(8, 6)$. Its child $A$, labeled $+$, has $(6, 2)$, with a leaf $A_1$ labeled $+$ with $(5, 0)$ and a node $A_2$ labeled $-$ with $(1, 2)$. $A_2$ has the leaves $A_{21}$, labeled $-$ with $(1, 2)$, and $A_{22}$, labeled $+$, which gets no case. The other child $B$, labeled $-$, has $(2, 4)$, with the leaves $B_1$, labeled $-$ with $(1, 3)$, and $B_2$, labeled $+$ with $(1, 1)$.

| node (postorder) | wrong | sub | decision | returns |
|---|---|---|---|---|
| $A_{21}$, $A_{22}$, $A_1$ | 1, 0, 0 | leaf | | 1, 0, 0 |
| $A_2$ | 1 | $1 + 0 = 1$ | tie: cut | 1 |
| $A$ | 2 | $0 + 1 = 1$ | keep | 1 |
| $B_1$, $B_2$ | 1, 1 | leaf | | 1, 1 |
| $B$ | 2 | $1 + 1 = 2$ | tie: cut | 2 |
| root | 6 | $1 + 2 = 3$ | keep | 3 |

The unpruned tree has 5 leaves and 3 errors on $V$. The pruned tree has 3 leaves, $A_1$, $A_2$ and $B$, and the same 3 errors. No pruning makes fewer errors, and every pruning with 3 errors contains this one. The tests check the example.

**ID3 on noisy data.** Draw five attributes with three values each, and set the class by the first attribute, with 20% of the labels replaced by a random class. An [ID3](/id3/) tree grown on 200 cases has 57 leaves. REP on 100 other cases leaves 3 leaves, one for each value of the first attribute. On 1000 fresh cases the errors drop from 208 to 91.

**The greedy variant can be worse.** Mitchell (1997) describes a best-first loop: cut the node whose removal most increases the accuracy on $V$, and stop when every removal would lower it. That loop is not optimal. In the tree of the proof, the root saves 3 errors and each of its two inner children saves 2, so the loop cuts the root first and ends with 3 errors, while the bottom-up pass cuts the two children and ends with 2.

## Variations

- **Pruning set by cross-validation.** [Cross-validation](/cross-validation/) cannot be used directly, as the pruned tree depends on the pruning set. Cost-complexity pruning uses it to pick one parameter instead.
- **Pruning rules instead of trees.** Quinlan's rule post-pruning in C4.5 turns each path into a rule and drops conditions. Incremental reduced-error pruning (IREP, Fürnkranz and Widmer 1994) and RIPPER (Cohen 1995) prune rules on a held-out set in the same spirit.
- **Other loss counts.** The pass works with any loss that adds over cases, such as costs for unequal errors or squared error on a regression tree: replace "errors" by that loss.
- **Without a pruning set.** [Cost-complexity pruning](/cost-complexity-pruning/) and the pessimistic pruning of [C4.5](/c4-5/) use only the training data.

## Pitfalls

- **Small pruning sets.** With few cases, many nodes get no case at all. Such a node has $\mathrm{wrong} = 0 = \mathrm{sub}$, so it is cut, and REP tends to prune too much (Esposito et al. 1997). Rare classes then vanish from the tree.
- **Less data for growing.** The cases in $V$ are not used to grow the tree. With a small data set, the loss in the grown tree can cost more than pruning gains.
- **Overfitting the pruning set.** The tree is chosen to fit $V$, so its error on $V$ is optimistic. Report the error on a third data set.
- **Judging a branch in its unpruned form.** Comparing $\mathrm{wrong}(t)$ with the errors of the full branch, top-down, cuts too much or too little. Use the errors of the best pruning of each branch, as PRUNE does.
- **Keeping ties.** The theorem needs a cut on a tie; with a strict test the tree is still most accurate on $V$, but not the smallest such tree.
- **Relabeling leaves on $V$.** The labels must come from the training cases. Using the majority class of $V$ at a node turns REP into a different, more optimistic method.

## Exercises

1. Show that a node that no case of $V$ reaches is always cut, and give a tree where this harms the accuracy on new data.
2. Modify PRUNE so that it keeps a node on a tie. Show that the result still has the fewest errors on $V$, and give a tree where it is larger than the REP tree.
3. Prove that $\mathrm{wrong}(t) \ge \sum_u \mathrm{wrong}(u)$ need not hold on $V$, unlike the training risk, and explain why REP does not need it.
4. Extend REP to costs: a case of class $j$ predicted as $k$ costs $c_{jk}$. Prove the theorem for this loss.
5. Run Mitchell's greedy loop on the worked tree of the examples. Does it reach the REP tree there? Then check the tree of the proof, where it does not.

## References
