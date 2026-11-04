---
tag: 1K7PH7
kind: theorem
slug: avl-height-theorem
name: AVL height bound
aliases:
- AVL height theorem
area: data-structures/balanced-trees
level: core
summary: An AVL tree with n nodes has height at most about 1.44 log2(n), since the minimum node count at height h is a Fibonacci-like recurrence.
prereqs: [avl-tree, fibonacci-numbers, induction]
see_also: [red-black-height-theorem, height-balanced-tree, balance-factor, binet-formula, wavl-tree, balanced-binary-search-tree]
sources:
  - paper: "G. M. Adelson-Velsky and E. M. Landis, An algorithm for the organization of information, Doklady Akademii Nauk SSSR 146, 1962 (English translation in Soviet Mathematics Doklady 3, 1962)"
    locator: the bound on the height through the minimal trees
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.3, Balanced Trees, Theorem A (the height of a balanced tree with N internal nodes lies between lg(N + 1) and 1.4405 lg(N + 2) − 0.3277) and the Fibonacci trees
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 13 problems, AVL trees (prove that an AVL tree with n nodes has height O(lg n))
---

An [AVL tree](/avl-tree/) with $n$ nodes has height less than $\log_\varphi(n + 2) - 0.3277$, which is about $1.4405 \lg(n + 2) - 0.3277$, where $\varphi = (1 + \sqrt 5)/2$ is the golden ratio. The reason is that the fewest nodes an AVL tree of height $h$ can have is $F_{h+2} - 1$, where $F_k$ is the $k$-th [Fibonacci number](/fibonacci-numbers/): the smallest tree of height $h$ has a smallest subtree of height $h - 1$ and a smallest subtree of height $h - 2$, so the counts follow the Fibonacci recurrence. The bound is Theorem A of Knuth, Section 6.2.3, and it is tight: the Fibonacci trees reach it.

## Statement

The height $h(t)$ of a binary tree is the number of nodes on a longest path from the root down, with $h(\text{nil}) = 0$. A binary tree is *AVL* (or height-balanced) when, at each node, the heights of the two subtrees differ by at most 1. Let $F_0 = 0$, $F_1 = 1$ and $F_{k} = F_{k-1} + F_{k-2}$, and let $\varphi = (1 + \sqrt 5)/2 \approx 1.618$.

**Theorem.** Let $N(h)$ be the least number of nodes of an AVL tree of height $h$. Then

1. **(Minimum size.)** $N(h) = F_{h+2} - 1$ for all $h \ge 0$.
2. **(Simple bound.)** An AVL tree with $n$ nodes has height $h \le \log_\varphi(n + 1) < 1.4405 \lg(n + 1)$.
3. **(Sharp bound.)** It has height $h < \log_\varphi(n + 2) + \log_\varphi \sqrt 5 - 2 < 1.4405 \lg(n + 2) - 0.3277$.

Every binary tree with $n$ nodes also has height at least $\lg(n + 1)$, so an AVL tree has height between $\lg(n + 1)$ and about $1.44 \lg n$.

## In plain words

Ask how few nodes a tree of a given height can have if it must stay balanced. The thinnest such tree has a thinnest tree one level shorter on one side, and a thinnest tree two levels shorter on the other side, since the two sides may differ by one level and not more. So the smallest count for each height is the two counts before it added together, plus one for the root. These are the Fibonacci numbers, minus one. They grow by a factor of about 1.618 at each step. So with a given number of nodes, the height can grow only as fast as the number of times you can divide by 1.618, which is about 1.44 times the base-2 log.

## Proof

**Lemma 1.** $F_{k} \ge \varphi^{k-2}$ for all $k \ge 1$.

*Proof.* By induction on $k$. $F_1 = 1 \ge \varphi^{-1}$ and $F_2 = 1 = \varphi^0$. For $k \ge 3$, $\varphi^2 = \varphi + 1$ gives $F_k = F_{k-1} + F_{k-2} \ge \varphi^{k-3} + \varphi^{k-4} = \varphi^{k-4}(\varphi + 1) = \varphi^{k-2}$. $\square$

**Part 1, lower bound.** We show that an AVL tree of height $h$ has at least $F_{h+2} - 1$ nodes, by induction on $h$. For $h = 0$ the tree is nil, with $0 = F_2 - 1$ nodes. For $h = 1$ it is one node, and $1 = F_3 - 1$. Let $h \ge 2$. The root has subtrees of heights $a$ and $b$ with $\max(a, b) = h - 1$ and $|a - b| \le 1$, so one has height $h - 1$ and the other height $h - 1$ or $h - 2$. Both are AVL. By the induction hypothesis, and since $F$ is nondecreasing, they have at least $F_{h+1} - 1$ and $F_h - 1$ nodes. So the tree has at least
$$1 + (F_{h+1} - 1) + (F_h - 1) = F_{h+2} - 1$$
nodes.

**Part 1, upper bound.** The *Fibonacci tree* $\Phi_h$ is defined by $\Phi_0 = \text{nil}$, $\Phi_1$ = one node, and $\Phi_h$ = a root with left subtree $\Phi_{h-1}$ and right subtree $\Phi_{h-2}$. By induction, $\Phi_h$ has height $h$, it is AVL (the root's subtrees have heights $h - 1$ and $h - 2$, and the subtrees are AVL), and its number of nodes $s_h$ satisfies $s_0 = 0$, $s_1 = 1$ and $s_h = 1 + s_{h-1} + s_{h-2}$. Then $s_h + 1 = (s_{h-1} + 1) + (s_{h-2} + 1)$, with $s_0 + 1 = 1 = F_2$ and $s_1 + 1 = 2 = F_3$, so $s_h + 1 = F_{h+2}$. Hence $N(h) \le F_{h+2} - 1$, and with the lower bound, $N(h) = F_{h+2} - 1$.

**Part 2.** Let an AVL tree have $n$ nodes and height $h$. By part 1 and Lemma 1, $n \ge N(h) = F_{h+2} - 1 \ge \varphi^h - 1$. So $\varphi^h \le n + 1$ and $h \le \log_\varphi(n + 1) = \lg(n + 1)/\lg \varphi$. Since $\lg \varphi > 0.6942$, $1/\lg \varphi < 1.4405$.

**Part 3.** By [Binet's formula](/binet-formula/), $F_k = (\varphi^k - \psi^k)/\sqrt 5$ with $\psi = (1 - \sqrt 5)/2$, and $|\psi| < 1$, so $F_k > \varphi^k/\sqrt 5 - 1/\sqrt 5 > \varphi^k / \sqrt 5 - 1$. Then $n + 2 \ge F_{h+2} + 1 > \varphi^{h+2}/\sqrt 5$, so
$$h < \log_\varphi(n + 2) + \log_\varphi \sqrt 5 - 2.$$
Numerically, $\log_\varphi \sqrt 5 = \ln \sqrt 5 / \ln \varphi \approx 1.6723$, so the constant is about $-0.3277$, and $\log_\varphi x = \lg x / \lg \varphi < 1.4405 \lg x$ for $x > 1$. $\blacksquare$

## Consequences

- **Logarithmic operations.** Search, insertion and deletion in an AVL tree walk one path and do $O(1)$ work per level, so they take $O(\log n)$ time in the worst case.
- **Shallower than red-black trees.** An AVL tree has height at most about $1.44 \lg n$, while a [red-black tree](/red-black-height-theorem/) can have height near $2 \lg n$. So AVL trees search a little faster in the worst case. Every AVL tree can be colored as a red-black tree, so the AVL trees are a subclass in this sense.
- **Height in a small field.** A node needs only its [balance factor](/balance-factor/), two bits, or a height of $O(\log \log n)$ bits.
- **WAVL trees.** A [WAVL tree](/wavl-tree/) with no deletions is an AVL tree, so it has this height bound; with deletions, its height stays below $2 \lg n$.

## Tightness

The bound in part 1 is exact, and the Fibonacci trees reach it: $\Phi_h$ is an AVL tree with $F_{h+2} - 1$ nodes and height $h$. For $h = 1, 2, \ldots, 7$, the minimum sizes are $1, 2, 4, 7, 12, 20, 33$. For $n = F_{h+2} - 1$, the height is $h > \log_\varphi(n + 1) - 2$, using $F_k \le \varphi^{k-1}$. So the constant $1/\lg \varphi \approx 1.4404$ in front of $\lg n$ cannot be lowered.

The lower bound $\lg(n + 1)$ is reached by perfect binary trees, which are AVL. Random insertions give AVL trees whose average search cost is close to $\lg n$, which is far from the worst case; the exact average is still not known in closed form.

## History

Adelson-Velsky and Landis (1962) introduced the trees and showed that the height is $O(\log n)$ through the minimal trees. Knuth's Volume 3 (1973) gives the sharp form as Theorem A of Section 6.2.3, with the Fibonacci trees as the extreme case. CLRS gives the $O(\lg n)$ height of AVL trees as part of a problem in its chapter on red-black trees.

## References
