---
title: Valiant's merge computes the stable merge
proves: [correctness]
status: full
---

Let $C$ be the stable merge of the sorted lists $A[0 \ldots m-1]$ and $B[0 \ldots n-1]$: an item $a$ of $A$ comes before an item $b$ of $B$ if and only if $b < a$ is false, and items of one list keep their order. So $A[i]$ is at position $i + \#\{j : B[j] < A[i]\}$ and $B[j]$ at position $j + \#\{i : \text{not } B[j] < A[i]\}$, which is $j$ plus the number of items of $A$ at most $B[j]$. A pair $(i, j)$ is a *split* if the first $i + j$ items of $C$ are $A[0 \ldots i-1]$ and $B[0 \ldots j-1]$.

We prove by induction on $m + n$ that VALIANT-MERGE writes $C$, where a call on parts of $A$ and $B$ writes into $C$ starting at a given position.

## Lemma 1. Lines L1 and L2

*Proof.* Line L1 copies the only non-empty list. Line L2 compares every pair, so for every item it knows the number of items of the other list before it, and the position formulas above give its place. $\square$

## Lemma 2. Each sample gets its rank

On lines L4 and L5, each A-sample learns the number of items of $B$ less than it, and each B-sample the number of items of $A$ at most it.

*Proof.* Let $a$ be an A-sample, and let $k$ be the number of B-samples $b$ with $b < a$, from round 1. B-samples are at the indices $t - 1, 2t - 1, \ldots$, and $B$ is sorted, so the items $B[0 \ldots kt - 1]$ are all less than $a$ (each is at most the $k$-th B-sample, which is less than $a$), and the items from index $(k+1)t - 1$ on are not less than $a$, if that index exists. The items in between are $B[kt \ldots \min((k+1)t - 1, n) - 1]$, at most $t - 1$ of them, and round 2 compares $a$ with each. So the rank of $a$ is $kt$ plus the number of those items less than $a$. For a B-sample the same argument holds with "at most" in place of "less than", since "not $b < a$" means $a \le b$. $\square$

## Lemma 3. The samples give a chain of splits

Each sample at index $i$ of $A$ with rank $j$ gives a split $(i, j)$, and $A[i]$ is at position $i + j$. The same holds for B-samples. Splits with $i + j \le i' + j'$ have $i \le i'$ and $j \le j'$, and different splits have different sums.

*Proof.* The items before $A[i]$ in $C$ are $A[0 \ldots i-1]$ and the items of $B$ less than $A[i]$, which are $B[0 \ldots j-1]$, so $(i, j)$ is a split. The same argument works for B-samples. For the chain property, the first $i + j$ items are a prefix of the first $i' + j'$ items, and two splits with equal sums describe the same set. $\square$

## Lemma 4. The pieces

Let $(i, j)$ and $(i', j')$ be splits next to each other in the sorted list of line L7. The positions $i + j, \ldots, i' + j' - 1$ of $C$ hold the stable merge of $A[i \ldots i'-1]$ and $B[j \ldots j'-1]$. If $(i, j)$ comes from an A-sample, the first of these items is $A[i]$, and if it comes from a B-sample, it is $B[j]$. Each piece, after removing that item, has at most $s - 1$ items of $A$ and at most $t - 1$ items of $B$.

*Proof.* The first part follows from Lemma 3 as in a merge by splits: the items between the two prefixes are the two parts, in the order of $C$. By Lemma 3 the sample that gives the split $(i, j)$ is at position $i + j$, the first position of the piece. If the remaining part of $A$ had $s$ or more items, it would contain an index $i''$ with $i < i'' < i'$ that is an A-sample index, because A-sample indices are $s$ apart. Its split would lie strictly between the two splits, by Lemma 3, which contradicts that they are next to each other. The same holds for $B$. $\square$

## Theorem

VALIANT-MERGE writes the stable merge of $A$ and $B$ into $C$.

*Proof.* By induction on $m + n$. If line L1 or L2 applies, use Lemma 1. Otherwise $m n > m + n$, so $m, n \ge 2$ and $s, t \ge 2$, and there is at least one sample in each list. By Lemmas 2 and 3, line L6 writes each sample to its position in $C$. By Lemma 4 the remaining positions split into pieces, each the stable merge of two parts with fewer items than $m + n$, which line L8 writes correctly by the induction hypothesis. The pieces and the samples cover all positions of $C$ once. $\square$
