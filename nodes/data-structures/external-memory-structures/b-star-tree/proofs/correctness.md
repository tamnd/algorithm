---
title: Search, insert and delete keep the B*-tree properties and give the right answers
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, a capacity $C \ge 4$, $f = \lfloor (2C+1)/3 \rfloor$ and $R = 2f - 1$. The keys are distinct. The *entries* $e(x)$ of a node $x$ are its keys if $x$ is a leaf and its children if $x$ is internal. A tree is *valid* if (S1) to (S4) of the page hold, with (S2) in the form: for an internal node $x$ with separators $key[1..m]$, $key[0] = -\infty$, $key[m+1] = +\infty$, every key in the leaves below $x.c[i]$ lies in $[key[i], key[i+1])$, and the separators of each node are increasing.

**Two facts about $f$.** (a) $3f \le 2C + 1$, by the definition of $f$. (b) $f \ge 3$, because $C \ge 4$ gives $2C + 1 \ge 9$. By (S1) and (b), each internal node other than the root has at least 3 children. Also $f \le C$, since $3f \le 2C + 1 < 3C + 3$, and $R = 2f - 1 \ge f$.

**Lemma 1 (search).** In a valid tree, lines L1 to L5 reach the only leaf whose key range contains $k$, so SEARCH returns true exactly when $k$ is a key. The range query returns the keys of $[a, b]$ in order.

*Proof.* At each internal node, line L3 picks the child $i$ with $key[i] \le k < key[i+1]$, and by (S2) no other child can hold $k$. The loop goes one level down per step and stops at a leaf by (S3). The range query is the one of the B+ tree: every leaf to the left of the leaf of $a$ holds only keys below $a$, and by (S4) the $next$ links visit the leaves in key order. $\square$

**Lemma 2 (SHARE).** Let $x$ be an internal node, let $x.c[j], \ldots, x.c[j+g-1]$ be valid subtrees of one height that satisfy (S2) with respect to the separators of $x$, and let $t$ be their total number of entries, with $t \ge k$. After SHARE$(x, j, g, k)$:

1. the keys in the leaves below $x$ are the same, and the leaf chain is in key order;
2. the $g$ children are replaced by $k$ children of the same height, each with $\lfloor t/k \rfloor$ or $\lceil t/k \rceil$ entries, and $x$ gains $k - g$ children;
3. (S2) holds at $x$ and inside each new child, and all leaves keep their depth.

*Proof.* Leaves. Line L17 concatenates the keys of the $g$ leaves. They are in increasing order, since each leaf is sorted and, by (S2), each key of a leaf is below the separator that follows it in $x$, and each key of the next leaf is at least that separator. Line L18 cuts this sorted list into $k$ consecutive pieces of the stated sizes. Line L19 takes as the separator before each piece after the first its first key $s$. Every key of the piece to the left is $< s$ and every key of the piece is $\ge s$, and the outer bounds of the group, $x.key[j]$ and $x.key[j+g]$, do not change. So (S2) holds at $x$. Line L20 links the pieces in order and gives the last one the old $next$ link of the group, so the chain stays in key order.

Internal nodes. Line L17 forms the sequence $c_1, s_1, c_2, s_2, \ldots, s_{t-1}, c_t$ of the $t$ grandchildren of $x$ in the group and the separators between them: the separators of the group nodes and, between two group nodes, the separator of $x$ that divided them. By (S2) at $x$ and at the group nodes, every key below $c_p$ lies in $[s_{p-1}, s_p)$, with $s_0 = x.key[j]$ and $s_t = x.key[j+g]$. Line L18 cuts the sequence of children into $k$ consecutive pieces. A new node gets the children of its piece and the separators between them, and the separator $s_p$ between the last child of one piece and the first of the next goes up to $x$. Every grandchild keeps the same two separators as its bounds, one in its new parent or in $x$, so (S2) holds at every level. No grandchild moves to another depth.

In both cases the sizes are as in item 2. $\square$

**Lemma 3 (insert below a node).** Let the subtree of $x$ be valid except that $x$ may have any number of entries, and let $k$ be a key not in it. After INSERT-REC$(x, k)$, the subtree holds its old keys and $k$, satisfies (S2) to (S4), every node below $x$ other than $x$ has $f$ to $C$ entries, and $x$ has gained at most one entry.

*Proof.* By induction on the height of $x$. A leaf gains the one key $k$ in order (line L9). For an internal $x$, line L10 picks the child $c = x.c[i]$ whose range contains $k$, so the new key respects (S2) at $x$. By the hypothesis, after line L11 the child $c$ has between $f$ and $C + 1$ entries and the nodes below it are fine. If it has at most $C$, line L12 returns and $x$ has not changed its number of entries. Otherwise $e(c) = C + 1$. Each internal node other than the root has at least 3 children, and the root, being internal, has at least 2, so $c$ has a sibling next to it.

- Line L14: a sibling $y$ next to $c$ has $f \le e(y) \le C - 1$. Then $t = e(c) + e(y)$ satisfies $C + 1 + f \le t \le 2C$. By Lemma 2 with $k = 2$, each new node has at most $\lceil 2C / 2 \rceil = C$ and at least $\lfloor (C + 1 + f)/2 \rfloor \ge f$ entries, because $C + 1 \ge f$. The number of children of $x$ does not change.
- Line L16: every sibling next to $c$ is full, and $y$ is one of them, so $t = 2C + 1$. By Lemma 2 with $k = 3$, each new node has at least $\lfloor (2C+1)/3 \rfloor = f$ entries and at most $\lceil (2C+1)/3 \rceil \le C$, since $2C + 1 \le 3C$. Now $x$ has one more child.

In both cases Lemma 2 gives (S2) to (S4). $\square$

**Theorem 1 (insert).** If $T$ is valid and $k$ is not a key, after BSTAR-INSERT$(T, k)$ the tree is valid and its keys are the old keys and $k$.

*Proof.* By Lemma 3 at the root, only the root can break (S1), and it has at most $R + 1$ entries. If it has at most $R$, the tree is valid: an internal root keeps at least 2 children, because no step removes a child. If it has $R + 1 = 2f$ entries, line L8 puts a new root above it and calls SHARE with $g = 1$ and $k = 2$. By Lemma 2 the two new children have $f$ entries each, which is between $f$ and $C$. The new root has 2 children, at most $R$ since $R \ge 3$, and all leaves are one level deeper, so (S3) holds. $\square$

**Lemma 4 (delete below a node).** Let the subtree of $x$ be valid except that $x$ may have any number of entries, and let $k$ be a key in it. After DELETE-REC$(x, k)$, the subtree holds its old keys without $k$, satisfies (S2) to (S4), every node below $x$ other than $x$ has $f$ to $C$ entries, and $x$ has lost at most one entry.

*Proof.* By induction on the height. A leaf loses $k$ (line L23). For internal $x$, line L24 picks the only child $c = x.c[i]$ that can hold $k$, by Lemma 1, and after line L25 $c$ has between $f - 1$ and $C$ entries by the hypothesis. If it has at least $f$, line L26 returns. Otherwise $e(c) = f - 1$.

- Line L27: a sibling $y$ next to $c$ has $e(y) \ge f + 1$. Then $2f \le t \le f - 1 + C$, and the two new nodes have at least $f$ and at most $\lceil (f - 1 + C)/2 \rceil \le C$ entries, since $f \le C$. The number of children of $x$ does not change.
- Line L28: $x$ has 2 children. By fact (b), $x$ is the root. The other child has exactly $f$ entries, since line L27 did not apply, so $t = 2f - 1 = R$. SHARE with $k = 1$ makes one child with $R$ entries, and $x$ loses one entry.
- Lines L29 and L30: $x$ has at least 3 children, so there is a group of three neighbouring children that contains $c$. Each sibling of $c$ next to it has exactly $f$ entries, since line L27 did not apply, and the third node has between $f$ and $C$. So $3f - 1 \le t \le (f - 1) + f + C$. If $t \le 2C$, the two new nodes have at most $C$ and at least $\lfloor (3f - 1)/2 \rfloor \ge f$ entries, because $3f - 1 \ge 2f$ when $f \ge 1$, and $x$ loses one child. If $t > 2C$, the three new nodes have at least $\lfloor (2C + 1)/3 \rfloor = f$ entries and at most $\lceil t/3 \rceil \le C$, because $t \le 2f - 1 + C \le 3C$; the number of children of $x$ does not change.

Lemma 2 gives (S2) to (S4) in each case. $\square$

**Theorem 2 (delete).** If $T$ is valid and $k$ is a key, after BSTAR-DELETE$(T, k)$ the tree is valid and its keys are the old keys without $k$.

*Proof.* By Lemma 4 at the root, every node other than the root satisfies (S1), and the root has lost at most one entry, so it has at most $R$. If the root is internal and now has one child, which happens only through line L28, that child has exactly $R$ entries and line L22 makes it the root. All leaves move one level up, so (S3) holds, and the new root has at most $R$ entries, and at least 2 children if it is internal, since $R = 2f - 1 \ge 2$. Otherwise the root keeps at least 2 children. $\square$

**Termination.** INSERT-REC and DELETE-REC go one level down per call, and SEARCH one level per loop step, so each operation makes at most $h + 1$ calls, where $h$ is the height. Each SHARE does work linear in the size of its group. The range query visits each leaf at most once, because the $next$ links go strictly to the right. $\blacksquare$
