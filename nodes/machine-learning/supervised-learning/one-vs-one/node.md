---
tag: W9KQF9
kind: technique
slug: one-vs-one
name: One-vs-one
aliases:
- all-pairs
- pairwise classification
area: machine-learning/supervised-learning
level: intro
summary: "Reduce k-class classification to k(k-1)/2 binary problems, one per pair of classes, trained on those two classes only, and predict by majority vote."
prereqs: [multiclass-classification]
see_also: [multiclass-classification, one-vs-rest, error-correcting-output-codes, support-vector-machine, svm-training, hinge-loss, logistic-regression]
sources:
  - paper: "Chih-Wei Hsu and Chih-Jen Lin, A comparison of methods for multiclass support vector machines, IEEE Transactions on Neural Networks 13(2), 415-425, 2002"
    locator: the one-against-one method with the max-wins voting rule and a tie going to the smaller class index, and the comparison with one-against-all and DAGSVM
  - paper: "Trevor Hastie and Robert Tibshirani, Classification by pairwise coupling, Annals of Statistics 26(2), 451-471, 1998"
    locator: combining the pairwise probability estimates into one class probability vector
  - paper: "Ting-Fan Wu, Chih-Jen Lin and Ruby C. Weng, Probability estimates for multi-class classification by pairwise coupling, Journal of Machine Learning Research 5, 975-1005, 2004"
    locator: pairwise coupling methods for probability estimates from one-against-one classifiers
  - paper: "John C. Platt, Nello Cristianini and John Shawe-Taylor, Large margin DAGs for multiclass classification, Advances in Neural Information Processing Systems 12, 547-553, 2000"
    locator: the decision DAG that evaluates k - 1 of the pairwise classifiers
  - paper: "Erin L. Allwein, Robert E. Schapire and Yoram Singer, Reducing multiclass to binary: a unifying approach for margin classifiers, Journal of Machine Learning Research 1, 113-141, 2000"
    locator: all-pairs as a code matrix with entries in {-1, 0, +1}
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 4.1.2 (the one-versus-one majority vote leaves ambiguous regions)
---

One-vs-one (OvO, also all-pairs) reduces a $k$-class problem to $\binom{k}{2} = k(k - 1)/2$ binary problems, one for each pair of classes $i < j$. The classifier $f_{ij}$ is trained only on the examples of classes $i$ and $j$, and a new input gets one vote from each classifier; the class with the most votes wins. Ties in the vote need a rule: LIBSVM gives the tie to the class with the smaller index (Hsu and Lin 2002). Each binary problem is small and balanced when the classes are, so the total training time is often less than that of [one-vs-rest](/one-vs-rest/), though there are more classifiers to store and evaluate.

## In plain words

To decide among many classes, hold a round-robin tournament. For every pair of classes, train a judge that has seen only those two classes. Show a new example to all the judges; each one names one of its two classes. The class with the most wins is the answer.

Each judge has a small, easy job. But a judge for "cat or dog" must still give an answer when it sees a bird, and that answer is noise. And the tournament can end in a tie, so you need a rule for that.

## When it applies

- You have a binary learner whose cost grows faster than linearly in the number of examples, such as a kernel [SVM](/support-vector-machine/). Many small problems are then cheaper than $k$ big ones.
- $k$ is small to moderate. The number of classifiers grows as $k^2/2$: 45 for $k = 10$, 4950 for $k = 100$.
- The binary learner gives at least a sign. Real scores or probabilities allow better tie rules and pairwise coupling.

## The template

Classes are $0, \ldots, k - 1$. The holes are the binary learner `BINARY` and the tie rule in L8.

```pseudo id=main
ONE-VS-ONE-TRAIN(S, k, BINARY)
L1  for each pair (i, j) with 0 ≤ i < j < k do
L2      S_ij ← ((x_t, +1 if y_t = i else −1) : y_t ∈ {i, j})
L3      f_ij ← BINARY(S_ij)                       ▷ f_ij(x) > 0 means class i
L4  return all f_ij
ONE-VS-ONE-PREDICT(f, x)
L5  v ← (0, ..., 0)                               ▷ one counter per class
L6  for each pair (i, j) with i < j do
L7      if f_ij(x) > 0 then v_i ← v_i + 1 else v_j ← v_j + 1
L8  return the smallest c with v_c = max_m v_m      ▷ the LIBSVM tie rule
```

**The votes.** Each input casts exactly $\binom{k}{2}$ votes, so $\sum_c v_c = k(k - 1)/2$, and a class can get at most $k - 1$. A class with $k - 1$ votes beat every other class and is the unique winner. With $k = 3$ the vote vector is a permutation of $(2, 1, 0)$ or it is $(1, 1, 1)$; the second case is a cycle, $i$ beats $j$, $j$ beats $m$, $m$ beats $i$, and only the tie rule decides.

**Cost.** With $n_c$ examples in class $c$, classifier $f_{ij}$ trains on $n_i + n_j$ examples, and every example is used in $k - 1$ problems, so the total size of all the training sets is $(k - 1)n$. If the binary learner costs $T(m) = c\, m^2$ and the classes are balanced, OvO costs $\binom{k}{2} c\, (2n/k)^2 = 2c\,\frac{k - 1}{k}\, n^2 < 2 c n^2$, against $k c n^2$ for one-vs-rest. Prediction evaluates all $\binom{k}{2}$ classifiers.

**As a code matrix.** In the scheme of Allwein, Schapire and Singer (2000), all-pairs is the $k \times \binom{k}{2}$ matrix whose column for $(i, j)$ has $+1$ in row $i$, $-1$ in row $j$ and $0$ elsewhere; a 0 means "this classifier does not train on this class". With their distance, in which a column with a 0 in either row counts $\frac12$, two rows are at distance $\rho = (\ell + 1)/2$ for $\ell = \binom{k}{2}$ columns, so $\ell / \rho < 2$ in their training error bound (see [error-correcting output codes](/error-correcting-output-codes/)), while for one-vs-rest it is $k/2$.

## Classic examples

- Multiclass [support vector machines](/support-vector-machine/) in LIBSVM, with [SVM training](/svm-training/) on each pair (Hsu and Lin 2002).
- Pairwise [logistic regression](/logistic-regression/) followed by pairwise coupling, which gives class probabilities (Hastie and Tibshirani 1998).
- Pairwise [linear discriminants](/linear-discriminant-analysis/) for problems where one class sits between two others, so that no linear "class against the rest" rule exists.
- Round-robin rule learning, which learns one rule set per pair of classes.

## Variations

- **Tie rules.** The smallest index (LIBSVM), a random class, or the class with the largest sum of scores in its favor, $\sum_{j} f_{cj}(x)$ with $f_{jc} = -f_{cj}$.
- **Decision DAG (DDAG).** Keep a list of candidate classes, test the first against the last with $f_{ij}$, and drop the loser; after $k - 1$ tests one class remains (Platt, Cristianini and Shawe-Taylor 2000). It is faster to evaluate. If the pairwise results are consistent with one total order, it returns the same class as the vote; in a cycle the answer depends on the order of the list.
- **Pairwise coupling.** Use probability outputs $r_{ij}(x) \approx P(y = i \mid y \in \{i, j\}, x)$ and find a distribution $p$ with $p_i / (p_i + p_j) \approx r_{ij}$ (Hastie and Tibshirani 1998; Wu, Lin and Weng 2004). This replaces the vote with a probability vector.
- **Weighted votes.** Each classifier votes with its confidence, for example $r_{ij}$ for class $i$ and $1 - r_{ij}$ for class $j$.

## Pitfalls

- **Incompetent classifiers.** On an example of class $m$, the classifier $f_{ij}$ with $m \notin \{i, j\}$ never saw such data, and its vote is arbitrary. Of the $\binom{k}{2}$ votes, only $k - 1$ come from classifiers that involve the true class. The method works because the true class can still win all of its $k - 1$ duels, but the other votes add noise.
- **Cycles and ties.** For three classes, three pairwise rules that each look reasonable can form a cycle; Bishop (Section 4.1.2) shows the ambiguous region in input space. Report the tie rule, since it changes the results.
- **A tie rule by index is biased.** Giving every tie to the smaller index favors class 0. With many ties, use the summed scores or a random choice.
- **Too many models.** For large $k$ the $\binom{k}{2}$ classifiers dominate memory and prediction time; use one-vs-rest, an output code or a joint multiclass model.

## Exercises

1. Show that in the vote, a class with $k - 1$ votes is the unique winner, and that if the pairwise results agree with a total order of the classes, the vote and the DDAG both return its top class.
2. For $k = 3$ list all $2^3$ outcomes of the three pairwise classifiers, and show that exactly two of them give a three-way tie.
3. In the Allwein, Schapire and Singer distance, show that two rows of the all-pairs matrix are at distance $1 + (k - 2) + \frac12\binom{k - 2}{2}$, and that this equals $(\ell + 1)/2$ with $\ell = \binom{k}{2}$.
4. On a line with class 0 on $[0, 1)$, class 1 on $[1, 2)$ and class 2 on $[2, 3)$, give three threshold classifiers $f_{01}, f_{02}, f_{12}$ for which the vote is always correct, and explain why one-vs-rest with threshold classifiers cannot be.

## References
