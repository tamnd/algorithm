---
title: LYNDON-ARRAY computes the longest Lyndon word at each index
proves: [correctness, termination]
status: full
---

**Notation.** $s = s[0..n-1]$ is a word over a totally ordered alphabet, with 0-based indices. Words are compared in lexicographic order, where a proper prefix is smaller, and $s[i..]$ is the suffix that starts at $i$. The array $rank$ is the inverse suffix array: $rank[i] < rank[j]$ if and only if $s[i..] < s[j..]$, and all ranks are distinct. For $0 \le i < n$, $\mathrm{nss}(i)$ is the least $j > i$ with $rank[j] < rank[i]$, or $n$ if there is none. We use two results from the [Lyndon factorization](/lyndon-factorization/) and [Chen-Fox-Lyndon theorem](/lyndon-schutzenberger-theorem/) pages: (1) the first factor of the Lyndon factorization of a nonempty word is its longest Lyndon prefix; (2) the start indices of the factors of a word $w$ are exactly the indices $i$ such that $w[i..] < w[j..]$ for every $j < i$.

**Lemma 1.** For each $i$, the longest Lyndon word that starts at $i$ has length $\mathrm{nss}(i) - i$.

*Proof.* Let $w = s[i..n-1]$. A Lyndon word starting at $i$ is a Lyndon prefix of $w$, so by (1) the longest one is the first factor of the factorization of $w$, and its length is the start of the second factor (or $|w|$ if there is one factor). The suffixes of $w$ are $w[d..] = s[i+d..]$, compared as suffixes of $s$. By (2), the second factor of $w$ starts at the least $d \ge 1$ such that $w[d..] < w[e..]$ for all $e < d$. Let $d^*$ be the least $d \ge 1$ with $w[d..] < w[0..]$, or $|w|$ if there is none. For $1 \le e < d^*$, $w[e..] > w[0..]$, so the minimum of $w[0..], \ldots, w[e-1..]$ is $w[0..]$ for each $e \le d^*$. Hence an index $1 \le e < d^*$ is not a factor start, because $w[e..] > w[0..]$, and $d^*$ is a factor start if $d^* < |w|$, because $w[d^*..]$ is smaller than the minimum $w[0..]$. So the second factor starts at $d^*$, and $i + d^* = \mathrm{nss}(i)$. If $d^* = |w|$, then $w$ has one factor, of length $n - i = \mathrm{nss}(i) - i$. $\square$

**Stack invariant.** At the start of the iteration of line L3 for $i$ (and, for $i = -1$, at the end of the loop), the stack $S$ holds exactly the set
$$ T_i = \{\, j : i < j < n \text{ and } rank[j] < rank[j'] \text{ for every } j' \text{ with } i < j' < j \,\}, $$
ordered with the smallest index on top. For $j < j'$ both in $T_i$, the definition with $j'$ gives $rank[j'] < rank[j]$, so the ranks decrease from the top down. Also $\lambda[i'] = \mathrm{nss}(i') - i'$ for every $i' > i$.

*Initialization.* For $i = n - 1$, $T_{n-1}$ is empty, and so is the stack.

*Maintenance.* First, $\mathrm{nss}(i) \in T_i$ when $\mathrm{nss}(i) < n$: every $j'$ strictly between $i$ and $\mathrm{nss}(i)$ has $rank[j'] > rank[i] > rank[\mathrm{nss}(i)]$. Lines L4 and L5 pop the elements of rank larger than $rank[i]$. Since ranks decrease from the top down, these form a top segment of the stack, and the pops stop at the first element with a smaller rank, or at the empty stack. Each element $j$ of $T_i$ with $j < \mathrm{nss}(i)$ has $rank[j] > rank[i]$, by the choice of $\mathrm{nss}(i)$, and is popped; $\mathrm{nss}(i)$ itself has a smaller rank and stops the pops. So after the pops the top is $\mathrm{nss}(i)$, or the stack is empty and $\mathrm{nss}(i) = n$. Lines L6 and L7 set $\lambda[i] = \mathrm{nss}(i) - i$. After line L8, the stack holds $i$ on top of the elements of $T_i$ with rank smaller than $rank[i]$. This set is $T_{i-1}$: an index $j > i$ is in $T_{i-1}$ exactly when it is in $T_i$ and $rank[j] < rank[i]$, and $i$ is in $T_{i-1}$ with nothing between. The smallest index, $i$, is on top.

*Termination.* The loop runs $n$ times; each pop removes an element pushed once, so there are at most $n$ pops in total.

**Conclusion for LYNDON-ARRAY.** At the end, $\lambda[i] = \mathrm{nss}(i) - i$ for every $i$, which by Lemma 1 is the length of the longest Lyndon word that starts at $i$.

**FACTORS.** By (1), the first factor of the factorization of $s[i..]$ is $s[i..i+\lambda[i]-1]$. If $s[i..] = \ell_1 \ell_2 \cdots \ell_k$ is the factorization, then $\ell_2 \cdots \ell_k$ is a nonincreasing product of Lyndon words, so by uniqueness it is the factorization of $s[i + \lambda[i]..]$. By induction on $n - i$, lines L12 and L13 list the start indices of all the factors, and the loop stops because $\lambda[i] \ge 1$. $\blacksquare$
