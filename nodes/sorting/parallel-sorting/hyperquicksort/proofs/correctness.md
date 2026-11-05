---
title: Hyperquicksort sorts in processor order
proves: [correctness]
status: full
---

Let $p = 2^d$. For a processor number $q$ and $0 \le i < d$, write $q_i$ for bit $i$ of $q$. Call the rounds by their dimension $i$, which runs from $d - 1$ down to $0$. Let $H_i(q)$ be the subcube of dimension $i + 1$ that contains $q$: the processors whose numbers agree with $q$ on the bits above bit $i$.

## Lemma 1. Keys are kept and lists stay sorted

*Proof.* Line L1 sorts each list. In a round, a pair $q, q'$ splits its two sorted lists into four sorted parts, and lines L6 and L7 put each key into exactly one of the two merged lists. Merging two sorted lists gives a sorted list. Processors not in a pair with a pivot keep their lists. So after every round, the multiset of all keys is the input, and each list is sorted. $\square$

## Lemma 2. Keys stay inside the subcubes of later rounds

After round $i$, and in all later rounds, keys move only between processors that agree on bits $i$ and above.

*Proof.* In round $i' \le i$, keys move only between $q$ and $q + 2^{i'}$, which differ only in bit $i'$. If $i' < i$, they agree on bits $i$ and above. $\square$

## Lemma 3. Round i splits each subcube by its pivot

Let $x$ be the pivot of the subcube $H = H_i(q)$ in round $i$. After round $i$, every key on a processor of $H$ with bit $i$ equal to $0$ is at most $x$, and every key on a processor of $H$ with bit $i$ equal to $1$ is greater than $x$.

*Proof.* The processors of $H$ with bit $i$ equal to $0$ are paired with those with bit $i$ equal to $1$ by $q \mapsto q + 2^i$, and every processor of $H$ is in exactly one pair. By lines L6 and L7, after the round the lower processor of each pair holds exactly the keys at most $x$ of the pair, and the upper one holds exactly the keys greater than $x$. If no processor of $H$ has keys, there is nothing to show. $\square$

## Theorem. The output is sorted in processor order

At the end, each list is sorted, and for $q < q'$ every key on processor $q$ is at most every key on processor $q'$.

*Proof.* By Lemma 1 the lists are sorted and hold the input keys. Let $q < q'$ and let $i$ be the highest bit where they differ, so $q_i = 0$ and $q'_i = 1$, and both lie in the subcube $H = H_i(q)$. By Lemma 3, right after round $i$, the processors of $H$ with bit $i$ equal to $0$ hold only keys at most the pivot $x$ of $H$, and those with bit $i$ equal to $1$ hold only keys greater than $x$. By Lemma 2, all later moves are between processors that agree on bit $i$ and above, so the keys of the lower half of $H$ stay in the lower half, and the same for the upper half. So at the end, every key on $q$ is at most $x$, and every key on $q'$ is greater than $x$. $\square$
