---
title: The XOR metric orders nodes in blocks, and the Kademlia node lookup finds the k closest nodes in O(log n) rounds
proves: [correctness]
status: full
---

We use the notation of the page. Identifiers are $b$-bit integers ($b = 160$ in the paper), and $d(x, y) = x \oplus y$. For a node $x$ and $0 \le i < b$, the *range* $B_i(x)$ is the set of live nodes $y$ with $2^i \le d(x, y) < 2^{i+1}$; bucket $i$ of $x$ holds contacts from $B_i(x)$. Line numbers refer to the pseudocode on the page. $N$ is the set of live nodes, $t$ is the target, and $T$ is the set of the $k$ nodes of $N$ closest to $t$ (all of $N$ if $|N| \le k$).

## 1. The XOR metric

**Lemma 1.** $d$ is a metric, and it is unidirectional: for each $x$ and each $\Delta$, exactly one $y$ has $d(x, y) = \Delta$.

*Proof.* $d(x, x) = 0$, $d(x, y) > 0$ for $x \ne y$, and $d(x, y) = d(y, x)$ follow from the properties of $\oplus$. For the triangle inequality, $d(x, y) \oplus d(y, z) = x \oplus z = d(x, z)$, and $a \oplus c \le a + c$ for non-negative integers $a, c$, because $\oplus$ is addition without carries. The only $y$ with $x \oplus y = \Delta$ is $y = x \oplus \Delta$. $\square$

By unidirectionality, distinct nodes have distinct distances to $t$, so the order by distance to $t$ is a strict order. We call it the *$t$-order*.

**Lemma 2 (blocks).** Let $p$ be a bit string of length $\ell \le b$, and let $Y$ be the set of nodes whose top $\ell$ bits are $p$. Then $Y$ is consecutive in the $t$-order: a node outside $Y$ is closer to $t$ than all of $Y$ or farther than all of $Y$.

*Proof.* For $a \in Y$, the top $\ell$ bits of $d(a, t)$ are $V = p \oplus t'$, where $t'$ is the top $\ell$ bits of $t$. So $d(a, t)$ lies in the interval $[V \cdot 2^{b - \ell}, (V + 1) \cdot 2^{b - \ell})$. For $c \notin Y$, the top $\ell$ bits of $d(c, t)$ differ from $V$, so $d(c, t)$ lies below this interval or above it. $\square$

Each range $B_i(x)$ is such a set: its nodes share the top $b - i - 1$ bits of $x$ and have the other value at bit $i$. Two nodes of $B_i(x)$ are at distance less than $2^i$ from each other.

## 2. The bucket rule never evicts a live contact

**Claim 1.** UPDATE (lines L1 to L5) removes a contact from a bucket only at line L5, and only when that contact did not answer a ping. A bucket holds at most $k$ contacts, and they stay in the order of the time last seen.

*Proof.* Line L2 moves a contact to the tail and line L3 appends one below the limit $k$. Line L4 keeps the head, moves it to the tail, and drops the new contact. Line L5 runs only when the head did not answer. In each case the tail is the contact seen last. $\square$

## 3. With full buckets, the lookup returns the exact k closest nodes

We assume two things during the lookup. (A) No node fails, so every call of line L14 gets an answer, and line L15 never runs. (B) For every live node $x$ and every $i$, bucket $i$ of $x$ holds $\min(k, |B_i(x)|)$ nodes of $B_i(x)$. Under (A), UPDATE keeps (B): it moves a contact, adds one to a bucket that has fewer than $k$ contacts (which by (B) already holds all of its range), or keeps the live head.

Let $S$, $Q$ and $K$ be as in the pseudocode. Let $P$ be the set of nodes whose answer the lookup has merged into $S$: $u$, with the answer $A_u$ of line L6, and every queried node, with its answer $A_x$ from line L19. Under (A), nothing leaves $S$, so $A_x \subseteq S$ for every $x \in P$, and $P \subseteq S \subseteq N$.

The lookup ends: each round with $C \ne \emptyset$ adds a new node to $Q$, and there are finitely many nodes. It returns at line L11, when every node of $K$, the $k$ nodes of $S$ closest to $t$, is in $Q$. So $K \subseteq P$.

**Fact F.** If $y \in S \setminus K$, then $|K| = k$ and every node of $K$ is closer to $t$ than $y$. This is the definition of $K$.

**Claim 2.** Under (A) and (B), the lookup returns $T$, sorted by distance to $t$.

*Proof.* $K$ is sorted at line L9. Suppose $K \ne T$. Then some $y \in T$ is not in $K$: if $|N| \le k$ then $T = N \supseteq K$, and otherwise $|T| = k \ge |K|$.

*Step 1: $y \notin S$.* If $y \in S$, Fact F gives $k$ nodes of $K$ closer to $t$ than $y$. They are in $T$, because $y \in T$ and $T$ is a prefix of the $t$-order. With $y$, that is $k + 1$ nodes of $T$, which is not possible.

*Step 2.* Choose $x \in P$ with the smallest $d(x, y)$; $P$ contains $u$, and $x \ne y$ by Step 1. Let $i$ be the index with $y \in B_i(x)$, and $Y = B_i(x)$. Every node of $Y$ is at distance less than $2^i \le d(x, y)$ from $y$, so by the choice of $x$, no node of $Y$ is in $P$, and so no node of $Y$ is in $K$.

*Step 3.* By line L19, $A_x$ is the first $\min(k, \cdot)$ contacts of the table of $x$ in the $t$-order, and $A_x \subseteq S$, so $y \notin A_x$ by Step 1.

(a) If $y$ is a contact of $x$, then $A_x$ has $k$ nodes, all closer to $t$ than $y$, and all in $S$. So the $k$ nodes of $K$ are all closer to $t$ than $y$, and as in Step 1, $T$ would have $k + 1$ nodes.

(b) If $y$ is not a contact of $x$, then by (B) $|Y| > k$ and the table of $x$ holds a set $W \subseteq Y$ of $k$ nodes. If $A_x$ contains no node of $W$, then every node of $A_x$ comes before a node of $W$ in the $t$-order, and so, by Lemma 2, before all of $Y$, including $y$. Then $A_x$ is $k$ nodes closer than $y$, and (a) applies. If $A_x$ contains some $w \in W$, then $w \in S$ and $w \notin K$, so by Fact F every node of $K$ is closer to $t$ than $w$. $K$ is not a subset of $T$, because $K \subseteq T \setminus \{y\}$ would give $|K| < k$; take $z \in K \setminus T$. Then $d(y, t) < d(z, t) < d(w, t)$, with $y, w \in Y$ and $z \notin Y$. This contradicts Lemma 2. $\square$

## 4. With one contact per bucket, the lookup finds the closest node

Here we replace (B) by the invariant of Maymounkov and Mazières (2002, Section 3). (C) For every live node $x$ and every $i$ with $B_i(x) \ne \emptyset$, bucket $i$ of $x$ holds at least one node of $B_i(x)$. Let $y^*$ be the node of $N$ closest to $t$. For a node $c \ne y^*$, let $\lambda(c)$ be the index with $y^* \in B_\lambda(c)$. For $0 \le j \le b$, let $D_j$ be the set of nodes $x$ with $d(x, y^*) < 2^j$, the nodes that share the top $b - j$ bits of $y^*$.

**Fact G.** Each $D_j$ is a prefix of the $t$-order. By Lemma 2 it is consecutive, and it contains $y^*$, the first node of the order.

**Fact H.** If $c \in P$ and $c \ne y^*$, then $A_c$ contains a node $c'$ of $D_{\lambda(c)}$, closer to $t$ than $c$.

*Proof.* Let $i = \lambda(c)$. The range $B_i(c)$ is the set of nodes that share the top $b - i - 1$ bits of $c$ and differ from $c$ at bit $i$; these are the bits of $y^*$, so $B_i(c) = D_i$. By Fact G, all of $D_i$ comes before $c$ and before every other contact of $c$ that is not in $D_i$. By (C), bucket $i$ of $c$ is not empty, so the first contact of $c$ in the $t$-order, which is the first node of $A_c$, is in $D_i$. $\square$

**Claim 3.** Under (A) and (C), the first node returned is $y^*$. If $c_r$ is the node of $S$ closest to $t$ at the start of round $r$, and $c_r \ne y^*$, then $c_r$ is queried in round $r$, and $c_{r+1} = y^*$ or $\lambda(c_{r+1}) < \lambda(c_r)$. So $y^*$ is in $S$ after at most $b$ rounds.

*Proof.* At the end, the first node $c$ of $K$ is the node of $S$ closest to $t$, and $c \in P$. If $c \ne y^*$, Fact H puts a closer node in $S$, a contradiction. In round $r$, if $c_r \ne y^*$, then $c_r \notin P$ by the same argument, so it is not yet queried; it is the first node of $K$, so line L10 picks it. After the round, $A_{c_r} \subseteq S$, so $S$ has a node of $D_{\lambda(c_r)}$. By Fact G, the closest node of $S$ is then also in $D_{\lambda(c_r)}$, so it is $y^*$ or has $\lambda < \lambda(c_r)$. Since $0 \le \lambda < b$, this happens at most $b$ times. $\square$

**Claim 4.** If the $n$ live identifiers are independent and uniform, then $y^*$ is in $S$ after $O(\log n)$ rounds with high probability.

*Proof.* Let $j_0 = b - \lceil \log_2 n \rceil$. The rounds with $\lambda(c_r) \ge j_0$ number at most $b - j_0 = \lceil \log_2 n \rceil$, since $\lambda$ falls in each round. After that, each $c_r$ is in $D_{j_0}$, and the $c_r$ are distinct because $\lambda$ falls, so there are at most $|D_{j_0}|$ more rounds. $D_{j_0}$ is the set of nodes in one aligned block of $2^{j_0} \le 2^b / n$ identifiers. There are $2^{b - j_0} \ge n$ such blocks, and $n$ uniform identifiers put $O(\log n)$ nodes in the fullest block with high probability (the balls into bins bound). $\square$

Each round sends at most $\max(\alpha, k)$ FIND_NODE calls. The paper states the bound in a finer form: with $k$ contacts in each bucket, most operations take $\lceil \log n \rceil + c$ steps for a small constant $c$ (Maymounkov and Mazières 2002, Section 3).

## Scope

Claims 2 to 4 assume that no node fails during the lookup. When nodes fail, line L15 drops each node that does not answer and never adds it back, so the result holds only nodes that answered. Tables can then hold failed contacts and miss live ones, and the result can differ from $T$. The paper bounds this case with a probability argument: a contact stays in a bucket only if it has answered, and a node that has been up for a long time is likely to stay up (Section 2.2).
