---
title: The choose or skip recursion visits each k-subset once, in lexicographic order, with 2N - 1 + 2C(n,k-1) calls
proves: [correctness]
status: full
---

Fix $0 \le k \le n$ and write $N = C(n, k)$. A *state* of a call CHOOSE$(i)$ is the pair of $i$ and the stack $P = a[1 \ldots m]$, an increasing list of elements of $\{1, \ldots, i-1\}$. Let $E(i, P)$ be the set of $k$-subsets $S$ of $[n]$ with $S \cap \{1, \ldots, i-1\} = P$, written as increasing lists. Each list in $E(i, P)$ is $P$ followed by an increasing list of $k - m$ elements of $\{i, \ldots, n\}$, so $|E(i, P)| = C(n - i + 1, k - m)$.

**Lemma 1.** CHOOSE$(i)$ with state $(i, P)$ visits each list of $E(i, P)$ exactly once, in increasing lexicographic order, and visits nothing else. When it returns, $m$ and $a[1 \ldots m]$ are as they were at the call.

*Proof.* By induction on $n + 1 - i$, which is at least $0$ in each call that passes line L3 or reaches line L2 with $m = k$. We treat the three exits of the call.

*Line L2.* If $m = k$, then $E(i, P) = \{P\}$, since no more elements can be added. Line L2 visits $P$ once and returns without a change.

*Line L3.* If $m < k$ and $n - i + 1 < k - m$, then fewer than $k - m$ elements are left, so $E(i, P)$ is empty, and the call returns without a visit or a change.

*Lines L4 to L7.* Otherwise $m < k$ and $n - i + 1 \ge k - m \ge 1$, so $i \le n$. Split $E(i, P)$ into the lists that contain $i$ and the lists that do not:
$$E(i, P) = E(i + 1, P \cdot i)\ \cup\ E(i + 1, P),$$
where $P \cdot i$ is $P$ with $i$ added at the end. The union is disjoint. Line L4 pushes $i$, so the call of line L5 has state $(i + 1, P \cdot i)$, and by the induction hypothesis it visits $E(i + 1, P \cdot i)$ in order, once each, and restores the stack. Line L6 pops $i$, so the call of line L7 has state $(i + 1, P)$, and it visits $E(i + 1, P)$ in order, once each, and restores the stack.

It remains to show that each list $u$ of the first part is smaller than each list $v$ of the second part. Both start with $P$. At position $m + 1$, $u$ has $i$, and $v$ has an element of $\{i + 1, \ldots, n\}$, since $v$ does not contain $i$. So $u_{m+1} < v_{m+1}$, and $u < v$. $\square$

**Theorem 1.** REC-COMBINATIONS$(n, k)$ visits each $k$-subset of $[n]$ exactly once, in lexicographic order.

*Proof.* Line L1 calls CHOOSE$(1)$ with the empty stack. $E(1, \emptyset)$ is the set of all $k$-subsets of $[n]$. Apply Lemma 1. $\blacksquare$

**Theorem 2 (calls).** For $k \ge 1$ the number of calls is $2N - 1 + 2C(n, k-1)$. For $k = 0$ it is $1$.

*Proof.* For $k = 0$ the first call visits the empty set at line L2 and returns. Let $k \ge 1$.

The calls form a rooted tree in which each call that reaches line L4 has exactly two children, and each other call is a leaf. In such a tree, the number of nodes is $2\ell - 1$, where $\ell$ is the number of leaves. The leaves are the calls that return at line L2 and the calls that return at line L3.

A call returns at line L2 exactly once for each visit, so there are $N$ such calls by Theorem 1.

Now count the calls that return at line L3. The root has state $(1, \emptyset)$, and $n \ge k$, so it passes line L3. A call of line L5 from a parent with state $(i, P)$ has state $(i + 1, P \cdot i)$, with $n - (i + 1) + 1 = n - i$ elements left and $k - m - 1$ needed. The parent passed line L3, so $n - i + 1 \ge k - m$, which gives $n - i \ge k - m - 1$. So a call of line L5 never returns at line L3. A call of line L7 has state $(i + 1, P)$, with $n - i$ elements left and $k - m$ needed, and it returns at line L3 exactly when $n - i < k - m$. With the parent condition $n - i + 1 \ge k - m$, this means $n - i + 1 = k - m$, that is, $i = n - k + m + 1$.

So the calls that return at line L3 correspond one to one to the calls that reach line L4 with $i = n - k + m + 1$ and $m < k$. Such a call has a stack $P$ that is an $m$-subset of $\{1, \ldots, n - k + m\}$. Each such $P$ does occur: by Lemma 1, the root visits each $k$-subset, and the $k$-subset $P \cup \{n - k + m + 1, \ldots, n\}$ is visited inside the call with state $(n - k + m + 1, P)$, which is therefore made, and which reaches line L4 because $m < k$ and $n - i + 1 = k - m$. There are $C(n - k + m, m)$ such states for each $m$, so the number of calls that return at line L3 is
$$\sum_{m=0}^{k-1} C(n - k + m, m) = C(n, k - 1),$$
by the hockey stick identity $\sum_{j=0}^{r} C(s + j, j) = C(s + r + 1, r)$ with $s = n - k$ and $r = k - 1$. Hence $\ell = N + C(n, k-1)$, and the tree has $2N + 2C(n, k-1) - 1$ nodes. $\blacksquare$

**Remark.** Each call does $O(1)$ work besides its calls, so the total time is $\Theta(N + C(n, k-1))$. Since $C(n, k-1) = N \cdot k / (n - k + 1)$, this is $\Theta(N \cdot n/(n - k + 1))$ for $n \ge 1$.
