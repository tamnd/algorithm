---
title: Class hierarchy analysis computes the least closed call graph, and it is sound for well-typed programs
proves: [correctness, termination, complexity]
status: full
---

**Setting.** The program has a finite set of classes with a parent function; $C \le D$ means that $C$ is $D$ or below it. Each method name $m$ has a class $\mathrm{decl}(m)$ that defines it, and $\mathrm{LOOKUP}(C, m)$ is the definition of $m$ in the nearest class at or above $C$ that has one. Each variable $y$ of a method body has a declared class $\mathrm{decl}(y)$. A call site $s$: `x = y.m(z)` has the target set $T(s) = \{\mathrm{LOOKUP}(C, m) : C \le \mathrm{decl}(y)\}$. A pair $(R, E)$ is *closed* if $main \in R$ and, for every site $s$ in a method of $R$ and every $T \in T(s)$, $(s, T) \in E$ and $T \in R$.

The program is *well typed*: `x = new C()` has $C \le \mathrm{decl}(x)$; `x = y` has $\mathrm{decl}(y) \le \mathrm{decl}(x)$; a load `x = y.f` and a store `y.f = z` have $\mathrm{decl}(y) \le \mathrm{decl}(f)$ for the class that declares $f$, $\mathrm{type}(f) \le \mathrm{decl}(x)$ for the load and $\mathrm{decl}(z) \le \mathrm{type}(f)$ for the store; a call `x = y.m(z)` has $\mathrm{decl}(y) \le \mathrm{decl}(m)$, $\mathrm{decl}(z) \le \mathrm{ptype}(m)$ and $\mathrm{rtype}(m) \le \mathrm{decl}(x)$; in the body of the definition of $m$ in class $C$, $\mathrm{decl}(this) = C$, $\mathrm{decl}(p) = \mathrm{ptype}(m)$ and $\mathrm{decl}(ret) = \mathrm{rtype}(m)$. The program has no reflection, no native code that calls back and no classes loaded at run time: every call of a run is the execution of a call site of the text.

**Lemma 1 (LOOKUP stops).** For a site `y.m(z)` and $C \le \mathrm{decl}(y)$, the loop of line L10 stops at a class that defines $m$.

*Proof.* $C \le \mathrm{decl}(y) \le \mathrm{decl}(m)$, so $\mathrm{decl}(m)$ is on the path from $C$ to the root, and it defines $m$. The loop stops at the first class on this path that defines $m$, at the latest at $\mathrm{decl}(m)$. $\square$

**Lemma 2 (termination and the invariant).** The loop of line L2 runs at most $|\Pi|$ times, where $\Pi$ is the set of methods. At each test of line L2: (a) every method is in $W$ at most once, and $W \subseteq R$; (b) for every method $M \in R \setminus W$, every site $s$ of $M$ and every $T \in T(s)$, $(s, T) \in E$ and $T \in R$.

*Proof.* A method enters $W$ only in line L1 or line L8, and line L8 adds it to $R$ at the same time, only if it was not in $R$. Methods never leave $R$. So each method enters $W$ at most once, and the loop runs at most $|\Pi|$ times. This gives (a). For (b): at the start, $R \setminus W = \emptyset$. A method $M$ leaves $W$ in line L3, and lines L4 to L8 add $(s, T)$ to $E$ and $T$ to $R$ for every site $s$ of $M$ and every $T \in T(s)$, by Lemma 1. Sets only grow, so (b) stays true for the methods that left $W$ before. $\square$

**Lemma 3 (every fact is forced).** Let $(R^*, E^*)$ be any closed pair. At all times, $R \subseteq R^*$ and $E \subseteq E^*$.

*Proof.* At the start, $R = \{main\} \subseteq R^*$ and $E = \emptyset$. Line L7 adds $(s, T)$ for a site $s$ of a method $M$ taken from $W \subseteq R \subseteq R^*$ and a $T \in T(s)$, so $(s, T) \in E^*$ and $T \in R^*$ because $(R^*, E^*)$ is closed. Line L8 adds the same $T$ to $R$. $\square$

**Theorem 1 (least closed pair).** The algorithm stops and returns the least closed pair.

*Proof.* It stops by Lemma 2. At the end $W$ is empty, so by Lemma 2(b) the pair $(R, E)$ is closed. By Lemma 3 it is inside every closed pair. The intersection of all closed pairs is closed (each rule instance holds in each of them), so a least closed pair exists, and $(R, E)$ is it. $\square$

**Lemma 4 (type safety).** In every run of a well-typed program, at every moment, every variable $v$ of a live frame holds null or an object of a class $C \le \mathrm{decl}(v)$, and every field $f$ of every object holds null or an object of a class $C \le \mathrm{type}(f)$.

*Proof.* By induction over the steps of the run. At the start, all variables and fields hold null. `x = new C()` stores an object of class $C \le \mathrm{decl}(x)$. `x = y` stores the value of $y$, of a class $C \le \mathrm{decl}(y) \le \mathrm{decl}(x)$. A load stores a field value, of a class $C \le \mathrm{type}(f) \le \mathrm{decl}(x)$. A store puts a value of class $C \le \mathrm{decl}(z) \le \mathrm{type}(f)$ in a field. A call `x = y.m(z)` on a receiver of class $C' \le \mathrm{decl}(y)$ runs the body of $\mathrm{LOOKUP}(C', m)$, defined in a class $C$ with $C' \le C$; it binds `this` to the receiver, of class $C' \le C = \mathrm{decl}(this)$, and `p` to a value of class at most $\mathrm{decl}(z) \le \mathrm{ptype}(m)$. The return stores the value of `ret`, of a class at most $\mathrm{rtype}(m) \le \mathrm{decl}(x)$, in $x$. $\square$

**Theorem 2 (soundness).** In every run, every method that the run enters is in $R$, and for every execution of a site $s$ that enters a method $T$, $(s, T) \in E$.

*Proof.* By induction over the calls of the run, in the order in which they happen. The run starts in $main \in R$. Take a call at site $s$: `x = y.m(z)` in a frame of method $M$. That frame was entered earlier, so $M \in R$ by the induction hypothesis. The receiver is an object of a class $C \le \mathrm{decl}(y)$ by Lemma 4 (a null receiver makes no call). The method that runs is $T = \mathrm{LOOKUP}(C, m) \in T(s)$. Since $(R, E)$ is closed by Theorem 1, $(s, T) \in E$ and $T \in R$. $\square$

**Theorem 3 (cost).** With a dispatch table and the sets of classes below each class built first, the algorithm takes $O(n + S K)$ time after the table, where $n$ is the size of the program, $S$ the number of sites and $K$ the number of classes. The table takes $O(K M)$ time for $M$ method names when it is filled from the root down.

*Proof.* By Lemma 2, each method is taken from $W$ once, so lines L3 and L4 read each body once, in $O(n)$ in total. For each site, line L5 visits at most $K$ classes, and lines L6 to L8 take $O(1)$ each with the table and with hashing or direct indexing for $R$ and $E$. That is $O(S K)$. The table: for each name $m$, visit the classes below $\mathrm{decl}(m)$ from the top; the entry of a class is its own definition of $m$ if it has one, and else the entry of its parent. Each of the at most $K M$ entries takes $O(1)$. The sets of classes below each class have $O(K h)$ elements in total for a tree of height $h$, and the program reads one of them per site. $\blacksquare$
