---
title: A polymorphic inline cache returns the result of the full lookup
proves: [correctness]
status: full
---

We use the operations SEND, GLOBALLOOKUP and CHANGED with lines L1 to L11 from the page. A *class state* is the set of classes with their parent links and method tables. The parent links have no cycle: SETPARENT refuses a parent $P$ whose chain holds $D$, and a new class gets an existing class as parent, so following parent links from any class ends after finitely many steps. The *chain* of $K$ is the list $K, \mathit{parent}(K), \dots$ up to a class with no parent. $\mathrm{LOOKUP}(K, s)$ returns the method table entry for $s$ of the first class in the chain of $K$ that defines $s$, or the marker "not understood" if none does. We write $\mathrm{LOOKUP}_\Sigma$ when we need to name the class state $\Sigma$.

A run is a sequence of steps. Each step is a SEND at some site, or a change SETMETHOD, REMOVEMETHOD or SETPARENT of one class $D$, which first calls CHANGED($D$) and then changes $D$.

**Invariant $I$.** In the current class state $\Sigma$:

1. at each site with selector $s$ and bound $k$, the classes $K_i$ in $\mathit{entries}$ are distinct, $|\mathit{entries}| \le k$, and $m_i = \mathrm{LOOKUP}_\Sigma(K_i, s)$ for each pair;
2. if $\mathit{mega}$ is true, then $\mathit{entries}$ is empty;
3. each pair $((K, s), m)$ in the global cache satisfies $m = \mathrm{LOOKUP}_\Sigma(K, s)$.

Initially every site is empty with $\mathit{mega}$ false, and the global cache is empty, so $I$ holds.

**Lemma 1 (locality).** Let $\Sigma$ and $\Sigma'$ differ only in the parent link and the method table of one class $D$. If $D$ is not in the chain of $K$ in $\Sigma$, then the chain of $K$ is the same in $\Sigma$ and $\Sigma'$, and $\mathrm{LOOKUP}_\Sigma(K, s) = \mathrm{LOOKUP}_{\Sigma'}(K, s)$ for every selector $s$.

*Proof.* Let the chain of $K$ in $\Sigma$ be $C_0 = K, C_1, \dots, C_t$, where $C_t$ has no parent. By induction on $i$, the chain in $\Sigma'$ starts with $C_0, \dots, C_i$: for $i = 0$ both start with $K$; and if both start with $C_0, \dots, C_i$ with $i < t$, then $C_i \ne D$, so $\mathit{parent}(C_i)$ is the same in both states, and it is $C_{i+1}$. Also $C_t \ne D$, so $C_t$ has no parent in $\Sigma'$ either. So the chains are equal. LOOKUP reads only the method tables of $C_0, \dots, C_t$, which are equal in the two states because none of them is $D$. So the results are equal. $\square$

**Lemma 2 (send).** If $I$ holds before SEND(site, $K$) in class state $\Sigma$, then the send returns $\mathrm{LOOKUP}_\Sigma(K, s)$, and $I$ holds after it.

*Proof.* SEND does not change the class state. There are three cases.

Megamorphic (line L1). GLOBALLOOKUP returns the cached method for $(K, s)$ if there is one, which equals $\mathrm{LOOKUP}_\Sigma(K, s)$ by part 3 of $I$. Otherwise line L8 stores $\mathrm{LOOKUP}_\Sigma(K, s)$ and line L9 returns it, and the new pair satisfies part 3. Parts 1 and 2 are unchanged.

Hit (line L3). The loop returns $m_i$ for the first $i$ with $K_i = K$. By part 1, $m_i = \mathrm{LOOKUP}_\Sigma(K_i, s) = \mathrm{LOOKUP}_\Sigma(K, s)$. Nothing changes.

Miss (lines L4 to L7). The loop found no $i$ with $K_i = K$, so $K$ is not among the cached classes. Line L4 computes $m = \mathrm{LOOKUP}_\Sigma(K, s)$ and line L7 returns it. If $|\mathit{entries}| < k$, line L5 appends $(K, m)$: the classes stay distinct because $K$ was not in the list, the length is at most $k$, and the new pair satisfies the equation. Otherwise line L6 empties the list and sets $\mathit{mega}$, which satisfies parts 1 and 2. Part 3 is unchanged. $\square$

**Lemma 3 (change).** If $I$ holds in class state $\Sigma$, and a step changes the class $D$ to give $\Sigma'$, then $I$ holds in $\Sigma'$ after the step.

*Proof.* The step runs CHANGED($D$) in $\Sigma$ and then changes $D$. Line L10 empties the global cache, so part 3 holds in $\Sigma'$. Line L11 only removes pairs and does not touch $\mathit{mega}$, so the classes stay distinct, the length stays at most $k$, and part 2 still holds. Take a pair $(K_i, m_i)$ that is still in a list. Line L11 kept it, so $D$ is not in the chain of $K_i$ in $\Sigma$. By part 1 in $\Sigma$, $m_i = \mathrm{LOOKUP}_\Sigma(K_i, s)$, and by Lemma 1 this equals $\mathrm{LOOKUP}_{\Sigma'}(K_i, s)$. So part 1 holds in $\Sigma'$. $\square$

**Theorem 1 (correctness).** In every run, every SEND(site, $K$) returns $\mathrm{LOOKUP}(K, s)$ in the class state at the time of the send.

*Proof.* By induction on the steps of the run, $I$ holds before each step: it holds at the start, Lemma 2 keeps it over a send, and Lemma 3 keeps it over a change. Lemma 2 then gives the result of each send. $\square$

**Theorem 2 (state machine).** Let the state of a site be uninitialized, monomorphic or polymorphic when $\mathit{mega}$ is false and the list has 0, 1, or at least 2 entries, and megamorphic when $\mathit{mega}$ is true. Then in every run:

1. a hit and every step at another site leave the state and the entries of the site unchanged, except that a change of a class can remove entries;
2. a miss at a site that is not megamorphic with $j < k$ entries leads to $j + 1$ entries, and a miss with $j = k$ entries leads to the megamorphic state;
3. a change of a class leaves $\mathit{mega}$ unchanged and does not add entries;
4. once megamorphic, a site stays megamorphic.

In particular, in a run without changes, the states that a site goes through are a prefix of uninitialized, monomorphic, polymorphic, megamorphic, with polymorphic left out when $k = 1$. If the site sees exactly $j$ distinct classes and $j \le k$, it ends with $j$ entries after exactly $j$ misses. If it sees more than $k$ distinct classes, it ends megamorphic.

*Proof.* Parts 1 to 4 are read off lines L1 to L11: only lines L5 and L6 add entries or set $\mathit{mega}$, only line L11 removes entries, and no line clears $\mathit{mega}$. Without changes, the number of entries starts at 0, grows by 1 at each miss while it is below $k$, and the site turns megamorphic at the first miss with $k$ entries, so the sequence of states is as stated. With $k = 1$ the count goes from 1 directly to the megamorphic state. If the site sees exactly $j \le k$ distinct classes, the first send of each class misses, because by part 1 of $I$ the list holds only classes seen before, and every later send of it hits, because the class was added and nothing removes it. So there are $j$ misses and $j$ entries. If it sees more than $k$ distinct classes and is not megamorphic before the first send of the $(k+1)$-th class, then the list holds the $k$ earlier classes, and that send misses with $k$ entries and makes the site megamorphic. $\square$
