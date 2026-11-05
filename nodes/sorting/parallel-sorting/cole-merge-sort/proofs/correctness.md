---
title: Cole's merge sort sorts in 3 lg n stages
proves: [correctness]
status: full
---

Let $n = 2^k$ and assume the keys are distinct (ties are broken by input index). For a node $v$ of height $h$, $L(v)$ is the sorted list of the $2^h$ keys at the leaves below $v$. Write $\mathrm{UP}_t(v)$ and $\mathrm{SUP}_t(v)$ for the lists after stage $t$, with $\mathrm{UP}_0(v) = [\text{key}]$ at a leaf and $\mathrm{UP}_0(v) = \emptyset$ at an inner node. A node is *full* at stage $t$ if $\mathrm{UP}_t(v) = L(v)$.

## Lemma 1. The lists are sorted subsets

For every $t$ and $v$, $\mathrm{SUP}_t(v)$ and $\mathrm{UP}_t(v)$ are sorted lists of distinct items of $L(v)$, provided that each stage computes $\mathrm{NEWUP}(u)$ as the sorted union of $\mathrm{SUP}_t(x)$ and $\mathrm{SUP}_t(y)$.

*Proof.* By induction on $t$. A sample of a sorted list of items of $L(v)$ is again one. The union of a list of items of $L(x)$ and one of items of $L(y)$ has distinct items, because $L(x)$ and $L(y)$ are disjoint, and its items are in $L(u)$. $\square$

## Lemma 2. Line L7 finds the rank

Let $e \in \mathrm{SUP}(x)$, let $r$ be the number of items of $\mathrm{UP}(u)$ less than $e$, and let $d = \mathrm{UP}(u)[r-1]$ and $f = \mathrm{UP}(u)[r]$, with $d = -\infty$ if $r = 0$ and $f = +\infty$ if $r = |\mathrm{UP}(u)|$. Let $\ell$ be the number of items of $\mathrm{SUP}(y)$ less than $d$. Then the rank of $e$ in $\mathrm{SUP}(y)$ is $\ell$ plus the number of items of $\mathrm{SUP}(y)$ in $[d, f)$ that are less than $e$.

*Proof.* We have $d < e \le f$. Items of $\mathrm{SUP}(y)$ less than $d$ are less than $e$. Items of $\mathrm{SUP}(y)$ that are at least $f$ are at least $e$, and none of them equals $e$, because $e$ is below $x$ and they are below $y$. So the items of $\mathrm{SUP}(y)$ less than $e$ are the $\ell$ items below $d$ and those in $[d, f)$ below $e$. $\square$

The lemma holds for any lists. The 3-cover property only bounds the number of items in $[d, f)$, which matters for the time and not for the result.

## Lemma 3. The merge is correct

Line L8 writes each item of $\mathrm{SUP}(x) \cup \mathrm{SUP}(y)$ to a distinct position, and the result is the sorted union.

*Proof.* For $e \in \mathrm{SUP}(x)$, the items of the union less than $e$ are the items of $\mathrm{SUP}(x)$ less than $e$ and those of $\mathrm{SUP}(y)$ less than $e$. Their number is the sum that line L8 uses, by Lemma 2, and the same holds for items of $\mathrm{SUP}(y)$. In a set of distinct items, the number of smaller items is the position in sorted order. $\square$

## Lemma 4. Size before a node is full

For a node $v$ of height $h \ge 1$ and $0 \le t \le 3h$, $|\mathrm{UP}_t(v)| \le 2^h \cdot 8^{t/3 - h}$. In particular $|\mathrm{UP}_t(v)| < 2^h$ for $t < 3h$, so $v$ is not full before stage $3h$.

*Proof.* By induction on $h$, with the claim for height $0$ read as: a leaf is full from stage $0$ on. Let $x$ and $y$ be the children of $v$, of height $h - 1$. Then $|\mathrm{UP}_t(v)| \le |\mathrm{SUP}_t(x)| + |\mathrm{SUP}_t(y)|$. We prove Lemmas 4 and 5 together by induction on $h$, so we may use that $x$ and $y$ become full at exactly stage $3h - 3$. For $t = 0$ the list is empty, so let $t \ge 1$.

*Case $t \le 3h - 3$.* The children are not full at stage $t - 1 < 3h - 3$, so their samples are every fourth item, and $|\mathrm{SUP}_t(x)| \le |\mathrm{UP}_{t-1}(x)|/4 \le 2^{h-1} \cdot 8^{(t-1)/3 - (h-1)}/4$. Since $8^{-1/3} \cdot 8 / 4 = 1$, twice this is $2^h \cdot 8^{t/3 - h}$.

*Case $t = 3h - 3 + a$ with $a \in \{1, 2, 3\}$.* The children became full at stage $3h - 3$, so their samples have $2^{h-1}/4$, $2^{h-1}/2$ and $2^{h-1}$ items for $a = 1, 2, 3$, at most, which is $2^{h-1} \cdot 2^{a - 3}$. Twice this is $2^h \cdot 2^{t - 3h} = 2^h \cdot 8^{t/3 - h}$. $\square$

## Lemma 5. A node of height h is full at stage 3h

*Proof.* By induction on $h$. Leaves are full at stage $0$. Let $v$ have height $h \ge 1$. Its children are full at stage $3h - 3$, so at stage $3h$ their samples are all of $L(x)$ and all of $L(y)$, and by Lemma 3, $\mathrm{UP}_{3h}(v) = L(x) \cup L(y)$ in sorted order, which is $L(v)$. By Lemma 4 it is not full earlier. After stage $3h$ the node keeps its list, and it sends samples only in stages $3h + 1$ to $3h + 3$. $\square$

## Theorem

After stage $3k$, $\mathrm{UP}(\text{root})$ is $L(\text{root})$, the input keys in sorted order.

*Proof.* The root has height $k$, so this is Lemma 5 for $h = k$. With ties broken by input index, equal keys keep their input order, and removing the padding keys, which are larger than all real keys and sit at the end, gives the sorted input. $\square$
