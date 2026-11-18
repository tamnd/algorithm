---
title: The parallel hash join returns the bag join and sends each tuple at most once
proves: [correctness, termination, communication]
status: full
---

We use the line numbers of the pseudocode on the page. The inputs are bags. $R$ is the bag union of its parts $R_0, \dots, R_{p-1}$, and $S$ is the bag union of $S_0, \dots, S_{p-1}$. The routing key $K$ is a nonempty set of attributes that $R$ and $S$ have in common, and $J$ is the set of all common attributes, so $K \subseteq J$. The output $R \bowtie S$ is the bag in which the tuple $r \cdot s$ (the tuple $r$ extended by the attributes of $s$ outside $J$) has as many copies as there are pairs of occurrences $(r, s)$ with $r[J] = s[J]$ and no NULL in $r[J]$. We treat each stored copy of a tuple as a distinct occurrence. The hash function $h$ is any function from key values to the integers. It need not be injective or uniform.

**Lemma 1 (routing).** After lines L1 to L3, every occurrence of $R$ and of $S$ is at exactly one node. An occurrence $r$ is at node $h(r[K]) \bmod p$, and an occurrence $s$ is at node $h(s[K]) \bmod p$.

*Proof.* Lines L1 and L2 visit each node $i$ once and each occurrence of $R_i$ once, and send it to one node. The parts $R_i$ together hold each occurrence of $R$ exactly once, so each occurrence of $R$ is sent once. Nothing is sent twice or dropped, because the simulation does not lose messages. The same holds for $S$ by line L3. The target node is the value that the line computes. $\square$

**Lemma 2 (co-location).** If $r[J] = s[J]$, then $r$ and $s$ are at the same node after line L3.

*Proof.* $K \subseteq J$, so $r[J] = s[J]$ gives $r[K] = s[K]$. Then $h(r[K]) \bmod p = h(s[K]) \bmod p$, because $h$ is a function. By Lemma 1 both occurrences are at that node. $\square$

**Theorem 1 (correctness).** The bag that line L8 returns is $R \bowtie S$.

*Proof.* Fix a node $j$, and let $R'_j$ and $S'_j$ be the occurrences that it holds after line L3. Lines L6 and L7 are the hash join of the page [hash join](/hash-join/) on $R'_j$ and $S'_j$ with the key $J$: line L6 puts each occurrence of $R'_j$ whose key has no NULL into the bucket of its key, once, and line L7 meets each occurrence $s$ of $S'_j$ once and outputs $r \cdot s$ for each occurrence $r$ in the bucket of $s[J]$. A NULL in $s[J]$ finds no bucket, because no key in the table has a NULL. So node $j$ outputs one copy of $r \cdot s$ for each pair $(r, s)$ in $R'_j \times S'_j$ with $r[J] = s[J]$ and no NULL in $r[J]$. This is the bag $R'_j \bowtie S'_j$.

Now take any matching pair $(r, s)$ of $R \times S$. By Lemma 2, both are at one node $j$, so the pair appears in $R'_j \bowtie S'_j$. By Lemma 1, each occurrence is at only one node, so the pair appears at no other node. Pairs that do not match appear nowhere. So the bag union of the local outputs, which line L8 returns, has exactly one copy of $r \cdot s$ for each matching pair. That is $R \bowtie S$. $\square$

**Theorem 2 (termination).** The algorithm stops after $O(n + z)$ steps of work in total, where $n = |R| + |S|$ counts occurrences and $z = |R \bowtie S|$, if each insert and each lookup of a bucket takes $O(1)$ steps plus the length of the bucket that it scans.

*Proof.* Lines L1 to L3 do one send per occurrence: $n$ sends. Line L6 does $|R'_j|$ inserts at node $j$, and these add up to $|R|$ over all nodes by Lemma 1. Line L7 does $|S'_j|$ lookups, which add up to $|S|$. The work of the lookups beyond $O(1)$ each is the number of matching pairs they output, which adds up to $z$ by Theorem 1, plus the tuples with other keys in the same bucket. With a table that keeps one bucket per distinct key, as the implementation does, there are no such tuples. Every loop runs over a finite bag, so the algorithm stops. $\square$

**Theorem 3 (network cost).** The algorithm uses one round of communication. It sends exactly the occurrences $t$ of $R$ and $S$ whose home node $i$ differs from $h(t[K]) \bmod p$, so at most $n$ tuples, and at most $p(p - 1)$ messages if the tuples from node $i$ to node $j$ go in one message.

*Proof.* By Lemma 1, each occurrence is sent once, from its home node to its target node, and only the sends between different nodes use the network. All sends happen in lines L1 to L3, before any node starts line L4, so they form one round. The messages are the ordered pairs $(i, j)$ with $i \ne j$ that carry at least one tuple, and there are $p(p - 1)$ such pairs. $\square$

**Theorem 4 (expected balance).** Suppose that $h$ maps the distinct key values to nodes independently and uniformly at random, and that the placement of the parts does not depend on $h$. Then each node holds $n/p$ occurrences in expectation after line L3. If the home node of each occurrence is also independent of its key and uniform, the expected number of tuples sent is $n(p - 1)/p$.

*Proof.* An occurrence goes to node $j$ with probability $1/p$, so by linearity of expectation node $j$ receives $n/p$ occurrences in expectation. An occurrence stays at home when its target equals its home node, which happens with probability $1/p$ under the second assumption. So it is sent with probability $(p - 1)/p$, and the expected number of sent tuples is $n(p - 1)/p$. $\square$

**Theorem 5 (skew bound).** Let $v$ be a value of $K$, and let $m_R$ and $m_S$ be the numbers of occurrences of $R$ and $S$ with key $v$. Whatever $h$ is, one node holds at least $m_R + m_S$ occurrences after line L3, and if the tuples with key $v$ also agree on $J$, that node outputs at least $m_R m_S$ tuples.

*Proof.* All these occurrences have the same value $v$ of $K$, so by Lemma 1 they go to the same node $h(v) \bmod p$. If they also agree on $J$, every pair of an $R$ occurrence and an $S$ occurrence among them matches, and by the proof of Theorem 1 the node outputs each such pair. $\square$

Theorem 4 says that the expected load is balanced. It does not bound the largest load. Theorem 5 shows that no choice of $h$ helps when one key value is frequent: the time of the slowest node is at least proportional to $m_R + m_S$, so with $m_R + m_S \ge n/2$ the speed-up over one node is at most about 2, whatever $p$ is.
