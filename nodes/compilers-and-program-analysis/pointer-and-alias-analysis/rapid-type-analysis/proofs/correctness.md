---
title: Rapid type analysis computes the least closed call graph, it is sound for well-typed programs, and it is inside class hierarchy analysis
proves: [correctness, termination, complexity]
status: full
---

**Setting.** The program, $C \le D$, $\mathrm{decl}$, $\mathrm{LOOKUP}$ and *well typed* are as in the proof of [class hierarchy analysis](/class-hierarchy-analysis/). The program has no reflection, no native code and no classes loaded at run time: every object of a run comes from the execution of a statement `x = new C()` of the text, and every call of a run is the execution of a call site of the text. A triple $(R, I, E)$ of methods, classes and edges is *closed* if

1. $main \in R$;
2. for every method $M \in R$ and every statement `x = new C()` in $M$, $C \in I$;
3. for every method $M \in R$, every site $s$: `x = y.m(z)` in $M$ and every $C \in I$ with $C \le \mathrm{decl}(y)$, the edge $(s, \mathrm{LOOKUP}(C, m))$ is in $E$ and $\mathrm{LOOKUP}(C, m) \in R$.

$\mathrm{LOOKUP}(C, m)$ is defined in rule 3, because $C \le \mathrm{decl}(y) \le \mathrm{decl}(m)$ and $\mathrm{decl}(m)$ defines $m$.

**Lemma 1 (termination).** Each method enters $W$ at most once, so the loop of line L2 runs at most $|\Pi|$ times, for the set $\Pi$ of methods. Each class enters $I$ at most once, and each site enters $S$ at most once.

*Proof.* A method enters $W$ only in line L1 or line L14, and line L14 adds it to $R$ in the same step, only if it was not in $R$. Methods never leave $R$. A class enters $I$ in line L5 only if it is not in $I$. A site enters $S$ in line L9 when its method is taken from $W$, which happens once. $\square$

**Lemma 2 (the invariant).** At each test of line L2: (a) $W \subseteq R$; (b) $I$ is the set of classes $C$ such that some method of $R \setminus W$ has a statement `x = new C()`, and $S$ is the set of sites of the methods of $R \setminus W$; (c) for every site $s$: `x = y.m(z)` in $S$ and every $C \in I$ with $C \le \mathrm{decl}(y)$, $(s, \mathrm{LOOKUP}(C, m)) \in E$ and $\mathrm{LOOKUP}(C, m) \in R$.

*Proof.* At the start, $R \setminus W$, $I$ and $S$ are empty, so (b) and (c) hold, and $W = R = \{main\}$. Take one pass of the loop, with method $M$. Part (a) holds because line L14 adds a method to $R$ and to $W$ together. Lines L4 and L5 add the classes created in $M$ to $I$, and line L9 adds the sites of $M$ to $S$, while $M$ leaves $W$ in line L3. This gives (b). For (c), take a site $s$ in $S$ and a class $C$ in $I$ with $C \le \mathrm{decl}(y)$, after the pass. There are three cases. If both were there before the pass, (c) held before, and sets only grow. If $s$ was in $S$ before and $C$ entered $I$ in this pass, line L6 visited $s$ when $C$ entered, and line L7 added the edge. If $s$ entered $S$ in this pass, lines L4 to L7 ran before, so $C$ was in $I$ when line L10 ran for $s$, and line L11 added the edge. In each case, ADD put the target in $R$ (line L14). $\square$

**Lemma 3 (every fact is forced).** Let $(R^*, I^*, E^*)$ be any closed triple. At all times, $R \subseteq R^*$, $I \subseteq I^*$ and $E \subseteq E^*$.

*Proof.* At the start, $R = \{main\} \subseteq R^*$ by rule 1, and $I$ and $E$ are empty. Line L5 adds a class created in a method $M \in R \subseteq R^*$, which is in $I^*$ by rule 2. Lines L7 and L11 call ADD with a site $s$ of a method of $R$, a class $C \in I$ with $C \le \mathrm{decl}(y)$ and $T = \mathrm{LOOKUP}(C, m)$. By the induction hypothesis the method is in $R^*$ and $C \in I^*$, so rule 3 gives $(s, T) \in E^*$ and $T \in R^*$. $\square$

**Theorem 1 (least closed triple).** The algorithm stops and returns $(R, E)$ of the least closed triple, and its $I$ is the $I$ of that triple.

*Proof.* It stops by Lemma 1. At the end $W$ is empty, so by Lemma 2 rule 2 holds (part (b)) and rule 3 holds (part (c), with $S$ the sites of all of $R$). Rule 1 holds from line L1. So $(R, I, E)$ is closed, and by Lemma 3 it is inside every closed triple. The intersection of all closed triples is closed, because each rule instance holds in each of them, so the least closed triple exists, and it is $(R, I, E)$. $\square$

**Lemma 4 (type safety).** In every run of a well-typed program, every variable of declared class $D$ and every field of type $D$ holds null or an object of a class $C \le D$.

*Proof.* This is Lemma 4 of the proof of class hierarchy analysis. It does not use any part of the analysis. $\square$

**Theorem 2 (soundness).** In every run, every object has a class in $I$, every method that the run enters is in $R$, and every call from a site $s$ to a method $T$ has $(s, T) \in E$.

*Proof.* By induction over the steps of the run. The run starts in $main \in R$. A step `x = new C()` runs in a frame of a method $M$ that the run entered, so $M \in R$ by the induction hypothesis, and $C \in I$ by rule 2. A call at site $s$: `x = y.m(z)` runs in a frame of a method $M \in R$. Its receiver is an object that an earlier step created, so its class $C$ is in $I$, and $C \le \mathrm{decl}(y)$ by Lemma 4. The method that runs is $T = \mathrm{LOOKUP}(C, m)$, so rule 3 gives $(s, T) \in E$ and $T \in R$. $\square$

**Theorem 3 (inside class hierarchy analysis).** Let $(R_C, E_C)$ be the result of class hierarchy analysis. Then $R \subseteq R_C$ and $E \subseteq E_C$.

*Proof.* Let $K$ be the set of all classes. The triple $(R_C, K, E_C)$ is closed. Rule 1 holds since $main \in R_C$. Rule 2 holds since $I = K$ contains every class. For rule 3, take a site $s$ of a method of $R_C$ and $C \le \mathrm{decl}(y)$. Then $\mathrm{LOOKUP}(C, m)$ is in the CHA target set of $s$, so the CHA closure rule puts the edge in $E_C$ and the target in $R_C$. By Theorem 1 the RTA result is inside every closed triple, so it is inside this one. $\square$

**Theorem 4 (cost).** After a dispatch table of $\mathrm{LOOKUP}$ and a subclass test in $O(1)$ are built, the algorithm runs in $O(n + S K)$ time, where $n$ is the size of the program, $S$ the number of sites and $K$ the number of classes.

*Proof.* By Lemma 1, each body is read once in lines L4 and L8, which costs $O(n)$ in total. Each pair of a site $s$ and a class $C$ is examined at most once: in line L6 if $s$ entered $S$ before $C$ entered $I$, and in line L10 otherwise. Each class enters $I$ once and each site enters $S$ once, so no pair is examined twice. Each examination is a subclass test, a table lookup and at most one ADD, all in $O(1)$ with hashing or direct indexing for $R$ and $E$. So lines L6, L7, L10 and L11 cost $O(S K)$ in total. The table takes $O(K M)$ time for $M$ method names, filled from the root down as in the proof of class hierarchy analysis, and a $K \times K$ bit matrix for the subclass test takes $O(K^2)$ time and space. A hash set of the classes below each class takes $O(K h)$ for a class tree of height $h$ and gives the same test in expected $O(1)$. $\blacksquare$
