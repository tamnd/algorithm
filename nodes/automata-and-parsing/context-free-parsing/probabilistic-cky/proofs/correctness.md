---
title: Probabilistic CKY returns the largest probability of a parse tree and a tree that has it, and it stops
proves: [correctness, termination]
status: full
---

We use the notation of the [context-free grammar](/context-free-grammar/) page and the pseudocode PROBABILISTIC-CKY of the page. The grammar $G = (V, \Sigma, P, S)$ is in Chomsky normal form: each production is $A \to BC$ with $B, C \in V$, $A \to a$ with $a \in \Sigma$, or $S \to \varepsilon$ with $S$ on no right side. Each production $r$ has a weight $q(r) \ge 0$; the proof does not use that the weights of a nonterminal sum to 1. The input is $w = a_1 \cdots a_n$, and $w_{i,j} = a_i \cdots a_j$.

For a parse tree $t$, $P(t)$ is the product of $q(r)$ over the nodes of $t$, each node counted with the production it uses. For $1 \le i \le j \le n$ and $A \in V$, let $\mathcal{T}(A, i, j)$ be the set of parse trees with root $A$ and yield $w_{i,j}$, and

$$\mu(A, i, j) = \max \{ P(t) : t \in \mathcal{T}(A, i, j) \},$$

with $\mu(A, i, j) = 0$ when the set is empty. The set is finite: in Chomsky normal form a tree with yield of length $\ell \ge 1$ has exactly $2\ell - 1$ internal nodes, so there are finitely many such trees, and the maximum exists. The table entry $\pi[i, j, A]$ starts at 0, as in the pseudocode.

## Lemma 1: the structure of the trees

A tree in $\mathcal{T}(A, i, i)$ is the single node $A$ with the leaf $a_i$, using $A \to a_i$. For $i < j$, a tree $t \in \mathcal{T}(A, i, j)$ has a root production $A \to BC$ and two subtrees $t_1 \in \mathcal{T}(B, i, k)$ and $t_2 \in \mathcal{T}(C, k + 1, j)$ for a unique $k$ with $i \le k < j$, and

$$P(t) = q(A \to BC) \cdot P(t_1) \cdot P(t_2).$$

Conversely, any such $A \to BC$, $k$, $t_1$ and $t_2$ give a tree in $\mathcal{T}(A, i, j)$ with this probability.

*Proof.* This is the structure part of Lemmas 1 and 2 of the [CYK correctness proof](/cyk-algorithm/): a node labeled with a nonterminal other than an empty $S$ yields a nonempty string, the root of a tree with a yield of length 1 must use $A \to a$, and the root of a longer one must use $A \to BC$, whose two children yield a nonempty prefix and a nonempty suffix. The product formula is the definition of $P(t)$, split at the root. $\square$

## Lemma 2: the recurrence

$\mu(A, i, i) = q(A \to a_i)$ if $A \to a_i \in P$ and 0 otherwise. For $i < j$,

$$\mu(A, i, j) = \max_{i \le k < j}\ \max_{A \to BC \in P}\ q(A \to BC) \cdot \mu(B, i, k) \cdot \mu(C, k + 1, j),$$

where the maximum of an empty set is 0.

*Proof.* The first part is Lemma 1 for $i = j$. For $i < j$, by Lemma 1 the trees of $\mathcal{T}(A, i, j)$ are the combinations of a split $k$, a production $A \to BC$, and independent choices of $t_1$ and $t_2$. Since all factors are nonnegative, the product $q \cdot P(t_1) \cdot P(t_2)$ is nondecreasing in each of $P(t_1)$ and $P(t_2)$, so for fixed $k$ and $A \to BC$ its maximum is reached with $P(t_1) = \mu(B, i, k)$ and $P(t_2) = \mu(C, k + 1, j)$. If one of the two sets of subtrees is empty, no tree arises from this $k$ and production, and the corresponding factor $\mu = 0$ makes the term 0, which does not change a maximum of nonnegative numbers. Taking the maximum over $k$ and the productions gives the formula. $\square$

This is the [principle of optimality](/principle-of-optimality/): a best tree is built from best subtrees. It needs the monotonicity of the product, which is why weights must be nonnegative.

## Lemma 3: the table holds the recurrence

When line L11 is reached, $\pi[i, j, A] = \mu(A, i, j)$ for all $1 \le i \le j \le n$ and $A \in V$. Moreover, if $\mu(A, i, j) > 0$, then $back[i, j, A]$ is set and is either $a_i$ (for $i = j$) or a triple $(k, B, C)$ with $A \to BC \in P$, $i \le k < j$ and

$$q(A \to BC) \cdot \mu(B, i, k) \cdot \mu(C, k + 1, j) = \mu(A, i, j).$$

*Proof.* By induction on $\ell = j - i + 1$. For $\ell = 1$, line L3 sets $\pi[i, i, A] = q(A \to a_i)$ and the back pointer $a_i$ for every lexical production; if the same production is listed twice, the larger weight is kept. The entries of other nonterminals stay 0. Later iterations write only cells with $j > i$. So the claim holds by Lemma 2.

For $\ell \ge 2$, the cell $(i, j)$ is written only in the iteration of lines L5 to L10 with $\text{len} = \ell$ and this $i$. In that iteration, lines L7 to L9 go through every pair of a split $k$ and a production $A \to BC$ and compute $p = q(A \to BC) \cdot \pi[i, k, B] \cdot \pi[k + 1, j, C]$. The cells read have lengths $k - i + 1$ and $j - k$, both less than $\ell$, so by the induction hypothesis they hold $\mu(B, i, k)$ and $\mu(C, k + 1, j)$, and $p$ is the term of Lemma 2. Line L10 keeps a running maximum: after each step, $\pi[i, j, A]$ is the largest term seen so far, or 0, and when it changes, $back[i, j, A]$ is set to the triple of the term that set it. At the end of the iteration $\pi[i, j, A]$ is the maximum of all terms, which is $\mu(A, i, j)$ by Lemma 2. If $\mu(A, i, j) > 0$, the last change set the back pointer to a triple whose term equals the final value. $\square$

## Lemma 4: the tree from the back pointers

If $\mu(A, i, j) > 0$, following the back pointers from $(i, j, A)$ (the node $(i, j, A)$ with back pointer $(k, B, C)$ gets the children $(i, k, B)$ and $(k + 1, j, C)$, and a node $(i, i, A)$ gets the leaf $a_i$) gives a tree $t \in \mathcal{T}(A, i, j)$ with $P(t) = \mu(A, i, j)$.

*Proof.* By induction on $j - i$. For $i = j$ the tree is $A \to a_i$, with probability $q(A \to a_i) = \mu(A, i, i)$. For $i < j$, the triple $(k, B, C)$ of Lemma 3 has $q(A \to BC) \cdot \mu(B, i, k) \cdot \mu(C, k + 1, j) = \mu(A, i, j) > 0$, so both $\mu(B, i, k)$ and $\mu(C, k + 1, j)$ are positive. By induction, the two children give trees $t_1 \in \mathcal{T}(B, i, k)$ and $t_2 \in \mathcal{T}(C, k + 1, j)$ with these probabilities, and by Lemma 1 the combined tree is in $\mathcal{T}(A, i, j)$ with probability $q(A \to BC) \cdot \mu(B, i, k) \cdot \mu(C, k + 1, j) = \mu(A, i, j)$. The construction visits $2(j - i + 1) - 1$ nodes, so it stops. $\square$

## Theorem

PROBABILISTIC-CKY stops and returns $\mu(S, 1, n)$, the largest probability of a parse tree of $w$, together with a tree of that probability when it is positive.

*Proof.* For $n = 0$, the only tree with an empty yield in Chomsky normal form is the node $S$ with the production $S \to \varepsilon$, since every other node yields a nonempty string; line L1 returns its weight, or 0. For $n \ge 1$, Lemma 3 gives $\pi[1, n, S] = \mu(S, 1, n)$ and Lemma 4 gives the tree.

*Termination.* All loops are bounded: line L2 runs $n$ times, and lines L8 to L10 run once for each production and each triple $(\text{len}, i, k)$, of which there are $\binom{n + 1}{3}$. The tree construction visits $2n - 1$ nodes. $\square$

## Remarks

**The sum version.** Replacing the maximum of line L10 by a sum, and the back pointers by nothing, computes $\beta(A, i, j) = \sum_{t \in \mathcal{T}(A, i, j)} P(t)$, the inside probability. The proof is the same with Lemma 2 read with sums: the sum over the pairs $(t_1, t_2)$ of $q \cdot P(t_1) \cdot P(t_2)$ factors as $q \cdot \beta(B, i, k) \cdot \beta(C, k + 1, j)$ by distributivity. Both versions are instances of one algorithm over a semiring, (max, ·) and (+, ·).

**Log space.** Replacing each weight by its logarithm and the products by sums keeps every comparison of line L10, because the logarithm is increasing. Weights equal to 0 become $-\infty$ and can be dropped.

**Negative weights.** Lemma 2 fails for weights of mixed sign: a best tree may then use a subtree of smallest, not largest, value. The implementation rejects negative weights.
