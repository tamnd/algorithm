---
title: Skip list operations keep the level lists sorted and return the right answers
proves: [correctness, invariant, termination]
status: full
---

Write $\mathcal{L}_i$ for the list obtained by following $forward[i]$ from the header, and $N_{\ge i}$ for the set of nodes with $\ell(x) \ge i$. The invariant is (S1) $\mathcal{L}_1$ is strictly increasing and contains each node; (S2) for each $i$, $\mathcal{L}_i$ is $N_{\ge i}$ in increasing key order; (S3) $S.level = \max(1, \max_x \ell(x))$ and $S.header.forward[i] = $ NIL for $i > S.level$. (S1) is (S2) for $i = 1$. Treat the header as a node with key $-\infty$ and level $M$.

**Lemma 1 (search).** Assume (S1) to (S3). When the loop of line L2 finishes level $i$ (after line L3 for that $i$), $x = update[i]$ is the last element of $\{\text{header}\} \cup \{y \in N_{\ge i} : y.key < k\}$ in key order.

*Proof.* By downward induction on $i$. Before level $S.level$, $x$ is the header, which is in every list. Before level $i < S.level$, $x$ is the node of the claim for $i + 1$, which is in $N_{\ge i+1} \subseteq N_{\ge i}$ (or is the header), so it is on $\mathcal{L}_i$ by (S2). Line L3 moves right along $\mathcal{L}_i$ while the next key is less than $k$. Since $\mathcal{L}_i$ is sorted, it stops at the last node of $\mathcal{L}_i$ with key $< k$, provided that $x$ starts at or before it, which holds because $x.key < k$. The walk ends because the list is finite. $\square$

**Search.** By Lemma 1 for $i = 1$ and (S1), $update[1]$ is the last node with key $< k$, so $x = update[1].forward[1]$ in line L4 is the first node with key $\ge k$, or NIL. Key $k$ is present if and only if this node exists and has key $k$, which is the test of line L5. The search writes no field of the structure.

**Insert.** If $k$ is present, line L7 changes one value and nothing else, so the invariant holds. Otherwise let $z$ be the new node with level $\lambda$. For $i \le \min(\lambda, S.level)$, $update[i]$ is the last node of $\mathcal{L}_i$ with key $< k$ by Lemma 1; for $S.level < i \le \lambda$, line L9 sets $update[i]$ to the header, which is the last element of $\mathcal{L}_i = (\text{header})$ since that list is empty by (S3). Lines L12 and L13 put $z$ between $update[i]$ and its old successor in $\mathcal{L}_i$, whose key is $> k$ (it is $\ge k$ by the choice of $update[i]$, and $k$ is absent). So $\mathcal{L}_i$ stays sorted and becomes $N_{\ge i} \cup \{z\}$ for $i \le \lambda$. For $i > \lambda$ the list does not change, and $z \notin N_{\ge i}$. So (S2) holds. Line L9 raises $S.level$ to $\lambda$ when needed, so (S3) holds.

**Delete.** If $k$ is absent, line L15 returns and nothing changes. Otherwise $x$ is the node with key $k$. For $i \le \ell(x)$, $x \in N_{\ge i}$ is on $\mathcal{L}_i$, and its predecessor there is the last node with key $< k$, that is $update[i]$ by Lemma 1, because $\ell(x) \le S.level$. Line L17 unlinks $x$ from $\mathcal{L}_i$. The lists for $i > \ell(x)$ do not hold $x$. So each $\mathcal{L}_i$ becomes $N_{\ge i} \setminus \{x\}$ in order, and (S2) holds. Line L18 lowers $S.level$ while the top list is empty, which restores (S3).

**Termination.** Each walk of line L3 moves along a finite list, the loops of lines L2, L11 and L16 have at most $M$ rounds, and the loop of line L18 lowers $S.level$, which is at least 1. $\blacksquare$
