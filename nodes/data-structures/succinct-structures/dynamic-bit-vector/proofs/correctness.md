---
title: Correctness of the dynamic bit vector
proves: [correctness]
status: full
---

For a node $x$, let $S(x)$ be the concatenation of the chunks of its subtree in in-order, with $S(\text{nil})$ empty. The invariants are:

- **(I1)** $S(\text{root}) = B$;
- **(I2)** $\text{size}(x) = |S(x)|$ and $\text{ones}(x)$ is the number of 1s in $S(x)$, for every node $x$.

By the definition of in-order, $S(x) = S(\text{left}(x))\,\text{chunk}(x)\,S(\text{right}(x))$.

**RANK1.** Claim: at the start of each iteration, the answer equals $r$ plus the number of 1s in the first $i$ bits of $S(x)$, and $0 \le i \le |S(x)|$. Initially $x$ is the root, $r = 0$, and this is the definition of $\text{rank}_1(i)$ by (I1). Let $\ell = |S(\text{left}(x))|$, known from (I2). If $i < \ell$, the first $i$ bits of $S(x)$ are the first $i$ bits of $S(\text{left}(x))$, so moving left keeps the claim. If $\ell \le i \le \ell + |\text{chunk}(x)|$, the first $i$ bits are all of $S(\text{left}(x))$, with $\text{ones}(\text{left}(x))$ ones by (I2), and the first $i - \ell$ bits of the chunk; line L4 returns exactly this plus $r$. Otherwise the first $i$ bits contain all of $S(\text{left}(x))$ and the chunk, and then the first $i - \ell - |\text{chunk}(x)|$ bits of $S(\text{right}(x))$; line L5 adds the 1s of the first two parts to $r$ and moves right, keeping the claim. In this case $i > \ell + |\text{chunk}(x)|$, so the right subtree has at least one bit and is not nil. Each iteration moves one level down, so the loop ends, and it ends by line L4 because $i \le |S(x)|$ excludes reaching nil.

**SELECT1.** Claim: the answer is $\text{base}$ plus the position of the $j$-th 1 in $S(x)$, and $1 \le j \le \text{ones}(x)$. The three cases split $S(x)$ into the same three parts: the $j$-th 1 is in the left part if $j \le \text{ones}(\text{left}(x))$, in the chunk if $j$ is at most that plus the chunk's 1s, and otherwise in the right part, where it is the $(j - \text{ones}(\text{left}(x)) - c)$-th 1, with $c$ the chunk's 1s, and its position is shifted by $\ell + |\text{chunk}(x)|$. Line L10 returns the position in the chunk shifted by $\text{base} + \ell$.

**INSERT.** The search of line L12 is the walk of RANK1, which by the same argument stops at the node $x$ and offset $o$ such that position $i$ of $B$ is offset $o$ of $\text{chunk}(x)$, taking the last chunk with $o = |\text{chunk}|$ when $i = n$. Inserting $b$ at offset $o$ turns $B$ into $B[0..i-1]\, b\, B[i..n-1]$ by (I1), since the chunks before $x$ in in-order hold exactly the $i - o$ bits before it. The nodes whose $S$ contains $\text{chunk}(x)$ are exactly the ancestors of $x$ and $x$ itself, the path, and line L14 restores (I2) for them; other nodes are unchanged. If line L15 splits the chunk into $c_1 c_2$, keeping $c_1$ in $x$ and putting $c_2$ in a new node placed immediately after $x$ in in-order, the concatenation is unchanged, so (I1) holds, and the tree's insertion routine, here a split at the boundary after $c_1$ followed by two treap merges, recomputes the counts of every node it touches, so (I2) holds.

**DELETE.** Symmetric: removing the bit at offset $o$ of $\text{chunk}(x)$ removes $B[i]$, line L18 fixes the path, and removing an empty node does not change any concatenation. The removal splits the tree at the boundary where the empty chunk sits, which places it first in the right part, and removes the leftmost node of that part; the treap routines recompute the counts of the nodes they touch.

**Height.** The structure is a treap with independent random priorities over its chunks, so its expected height is $O(\lg m)$ for $m$ chunks, and all operations are $O(\lg n)$ expected plus the work inside one chunk. $\blacksquare$
