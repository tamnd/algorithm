---
title: TLSF returns a block that fits, keeps its bitmaps exact, and runs in constant time
proves: [correctness, termination]
status: full
---

**Setting.** Fix $J \ge 0$ and a heap $[0, h)$ with $h \ge 2^J$. For a size $r \ge 2^J$ let $\phi(r) = (fl, sl)$ be the result of MAPPING-INSERT, and for a class $c = (fl, sl)$ with $0 \le sl < 2^J$ let $\text{low}(c) = 2^{fl} + sl \cdot 2^{fl - J}$. Order classes by $fl$ first and then by $sl$.

**Lemma 1 (classes).** For $r \ge 2^J$ with $\phi(r) = (fl, sl)$: $0 \le sl < 2^J$ and $\text{low}(\phi(r)) \le r < \text{low}(c')$, where $c'$ is the class just after $\phi(r)$. So the classes cut the sizes $r \ge 2^J$ into intervals, and $r \le r'$ implies $\phi(r) \le \phi(r')$.

*Proof.* Let $fl = \lfloor \lg r \rfloor \ge J$ and $d = fl - J \ge 0$. Then $2^J \le r \gg d < 2^{J + 1}$, so $sl = (r \gg d) - 2^J$ is in $[0, 2^J)$. Also $(r \gg d) \cdot 2^d \le r < (r \gg d + 1) \cdot 2^d$, that is, $\text{low}(fl, sl) \le r < 2^{fl} + (sl + 1) 2^d$. The right side is $\text{low}(fl, sl + 1)$ if $sl + 1 < 2^J$, and $2^{fl + 1} = \text{low}(fl + 1, 0)$ otherwise. The intervals $[\text{low}(c), \text{low}(c'))$ for consecutive classes are disjoint, follow each other in class order and cover all sizes $\ge 2^J$, so $\phi$ is monotone. $\square$

**Lemma 2 (MAPPING-SEARCH).** For $r \ge 2^J$, MAPPING-SEARCH$(r)$ returns the least class $c$ with $\text{low}(c) \ge r$.

*Proof.* Let $d = \lfloor \lg r \rfloor - J$ and $r' = r + 2^d - 1$, and let $c = \phi(r')$. If $\lfloor \lg r' \rfloor = \lfloor \lg r \rfloor$, the row of $c$ has classes of width $2^d$, and $\text{low}(c) = \lfloor r' / 2^d \rfloor 2^d = \lceil r / 2^d \rceil 2^d$, the least multiple of $2^d$ that is at least $r$. The class lower bounds in this row, and $2^{fl + 1}$, are exactly the multiples of $2^d$ from $2^{fl}$ to $2^{fl+1}$, so $c$ is the least class with $\text{low}(c) \ge r$. Otherwise $r' \ge 2^{fl + 1}$ with $fl = \lfloor \lg r \rfloor$, and $r' < 2^{fl + 1} + 2^d$ because $r < 2^{fl + 1}$, so $c = (fl + 1, 0)$ with $\text{low}(c) = 2^{fl + 1} \ge r$. Every class of row $fl$ has $\text{low} \le 2^{fl+1} - 2^d < r$, because $r > 2^{fl + 1} - 2^d$ in this case. So again $c$ is the least such class. $\square$

**Invariant (I).** A state is a list of blocks $[a_0, a_1), [a_1, a_2), \ldots$ with $a_0 = 0$ and the last end $h$, each with a size $a_{k+1} - a_k \ge 2^J$, a free flag and a pointer to the block before it. (I) says:

1. the blocks tile $[0, h)$, and the pointer of each block is the start of the block before it;
2. no two free blocks are next to each other;
3. each free block is in LIST$[\phi(\text{size})]$, each block in a list is free, and no block is in two lists;
4. bit $sl$ of SL$[fl]$ is 1 exactly when LIST$[fl][sl]$ is not empty, and bit $fl$ of FL is 1 exactly when SL$[fl] \ne 0$.

The start state, one free block of $h$ words in LIST$[\phi(h)]$ with its two bits set, satisfies (I). INSERT and the removal of line L9 keep (3) and (4): INSERT pushes the block on the list of its class and sets both bits; a removal unlinks the block from the list of its class, which is the list it is on by (3), and clears the SL bit only when that list becomes empty, and the FL bit only when the whole row becomes empty.

**Lemma 3 (FIND-SUITABLE-BLOCK).** Assume (I.3) and (I.4). For a class $c$, FIND-SUITABLE-BLOCK$(c)$ returns the head of the least nonempty list LIST$[c^*]$ with $c^* \ge c$, or FAIL when all lists at or above $c$ are empty.

*Proof.* Let $c = (fl, sl)$. By (I.4), the 1 bits of $m$ in line L3 are the nonempty classes $(fl, s)$ with $s \ge sl$, and FFS gives the least of them, if $m \ne 0$. If there is none, the 1 bits of $m$ in line L5 are the rows above $fl$ with a nonempty list. FFS gives the least such row $f$, and by (I.4) SL$[f] \ne 0$, so FFS(SL$[f]$) gives its least nonempty class. In class order this is the least nonempty class above row $fl$, and no nonempty class of row $fl$ is at or above $sl$. If $m = 0$ in line L5, no list at or above $c$ is nonempty. $\square$

**Lemma 4 (malloc).** Assume (I). TLSF-MALLOC$(n)$ either returns a block of at least $n$ words and keeps (I), or returns FAIL, and it returns FAIL only when every free block has fewer than $\text{low}(c)$ words, where $c$ is the class of line L8.

*Proof.* Line L8 sets $n_0 = \max(n, 2^J)$ and $c = $ MAPPING-SEARCH$(n_0)$, and it rounds the request to $n_1 = \text{low}(c) \ge n_0 \ge n$ by Lemma 2. If a free block $b$ has at least $\text{low}(c)$ words, then $\phi(\text{size}(b)) \ge c$ by Lemma 1, and by (I.3) $b$ is in a list at or above $c$. So by Lemma 3 FIND-SUITABLE-BLOCK does not fail. Conversely, when it returns a block $b$ from LIST$[c^*]$ with $c^* \ge c$, then size$(b) \ge \text{low}(c^*) \ge \text{low}(c) = n_1 \ge n$ by Lemma 1, and $b$ is free by (I.3). Line L9 removes $b$, which keeps (I.3) and (I.4). If the rest size$(b) - n_1$ is at least $2^J$, line L10 cuts $b$ into $[b, b + n_1)$ and a free block $[b + n_1, \text{end})$, sets the pointer of the new block and of the block after it, and inserts the new block. The new free block has the same neighbor after it as $b$ had. That neighbor is not free by (I.2), and the block before it is $b$, now used, so (I.2) holds. Line L11 marks $b$ used. All parts of (I) hold. $\square$

**Lemma 5 (free).** Assume (I) and let $b$ be a used block. After TLSF-FREE$(b)$, (I) holds, and the free words are those before the call plus the words of $b$.

*Proof.* By (I.2) each neighbor of $b$ that is free has no free neighbor other than $b$. Line L12 removes the block before $b$ from its list, if it is free, and joins the two into one block. Line L13 does the same with the block after. The pointers of the merged block and of the block after it are set as in the code, so (I.1) holds. The merged block has no free neighbor: a free block next to it would have been next to a free neighbor of $b$, against (I.2). Line L14 inserts it into the list of its class and sets its bits, so (I.3) and (I.4) hold. The merged block covers $b$ and the free neighbors, and no other block changes. $\square$

**Theorem.** For any sequence of calls in which `free` gets only used blocks, (I) holds after each call, every block that `malloc(n)` returns has at least $n$ words, `malloc` fails only when no free block has at least $\text{low}(\text{MAPPING-SEARCH}(\max(n, 2^J)))$ words, and when all blocks are freed the heap is one free block of $h$ words. Each call ends after $O(1)$ word operations.

*Proof.* (I) holds at the start and is kept by Lemmas 4 and 5. If all blocks are free, (I.1) and (I.2) leave a single block, which is $[0, h)$. No line of the pseudocode has a loop. Each call does a constant number of FLS and FFS steps, shifts, list operations and header updates, and each takes $O(1)$ time in the word RAM, so each call ends after $O(1)$ steps. $\blacksquare$
