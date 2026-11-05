---
title: SAM-EXTEND keeps the end-position classes, transitions and suffix links
proves: [correctness]
status: full
---

Let $S = S[0 \ldots n-1]$. For a string $x$, $endpos_S(x) = \{\, e : 0 \le e < n,\ S[e - |x| + 1 \ldots e] = x \,\}$ for $x \ne \varepsilon$, and $endpos_S(\varepsilon) = \{-1, 0, \ldots, n-1\}$. Write $x \equiv_S y$ if $endpos_S(x) = endpos_S(y) \ne \emptyset$; the classes are the substrings of $S$ grouped by $endpos$.

**Lemma 1.** For substrings $x, y$ with $|x| \le |y|$: if $x$ is a suffix of $y$ then $endpos(y) \subseteq endpos(x)$; otherwise $endpos(x) \cap endpos(y) = \emptyset$. *Proof.* If $e$ is in both, then $x$ and $y$ both end at $e$, so the shorter is a suffix of the longer. $\square$

**Lemma 2 (classes are suffix intervals).** A class $C \ne [\varepsilon]$ has a longest string $long(C)$, and $C$ is the set of suffixes of $long(C)$ with lengths in an interval $[minlen(C), |long(C)|]$. *Proof.* By Lemma 1, all members of $C$ are suffixes of the longest one. If $x$ and $z$ are in $C$ and $y$ is a suffix of $z$ longer than $x$, then $endpos(z) \subseteq endpos(y) \subseteq endpos(x) = endpos(z)$ by Lemma 1, so $y \in C$. $\square$

Define $link(C)$ as the class of the suffix of $long(C)$ of length $minlen(C) - 1$; by Lemma 2 it is the class of the longest suffix of the strings of $C$ that is not in $C$, and $len(link(C)) = minlen(C) - 1$.

**Lemma 3 (transitions are well defined).** If $x \equiv y$ and $xc$ is a substring, then $yc$ is a substring and $xc \equiv yc$, since $endpos(xc) = \{\, e + 1 : e \in endpos(x),\ S[e+1] = c \,\}$. $\square$

So the automaton with one state per class, transitions $[x] \xrightarrow{c} [xc]$, and accepting states the classes that contain a suffix of $S$ is deterministic and accepts exactly the suffixes of $S$ (reading $x$ from the initial state $[\varepsilon]$ succeeds exactly when $x$ is a substring, and ends in $[x]$). It is minimal: two substrings $x \not\equiv y$ have, say, $e \in endpos(x) \setminus endpos(y)$, and then $x \cdot S[e+1 \ldots n-1]$ is a suffix of $S$ while $y \cdot S[e+1 \ldots n-1]$ is not, so the states are distinguishable (Myhill-Nerode), and all non-substrings go to one dead state that is not stored.

**The claim.** After each call, the stored states, with $len$, $link$ and $next$, are exactly the classes of the current text with $len(v) = |long(v)|$, $link$ as defined, and transitions as in Lemma 3; and $last$ is the class of the whole text. This holds for $S = \varepsilon$: one class $\{\varepsilon\}$, no transitions.

**One step.** Assume the claim for $S$, of length $n$, and let $S' = Sc$. For each substring $x$ of $S'$,

$$endpos_{S'}(x) = endpos_S(x) \cup \{n\} \text{ if } x \text{ is a suffix of } S', \quad endpos_{S'}(x) = endpos_S(x) \text{ otherwise,}$$

with $endpos_S(x) = \emptyset$ when $x$ is not a substring of $S$. The suffixes of $S'$ are $\varepsilon$ and $yc$ for the suffixes $y$ of $S$. By the claim and Lemma 2, the suffixes of $S$ are the strings of the states on the link path $last = p_0, p_1 = link(p_0), \ldots, p_k = init$, with lengths decreasing along the path, and every length from $n$ down to 0 appears once.

*Line L1.* $cur$ will be the class of $S'$, with $len = n + 1$.

*Line L3.* Let $p_0, \ldots, p_{t-1}$ be the states without a transition on $c$. For $y$ in such a state, $yc$ is not a substring of $S$ (by Lemma 3 and the claim), so $endpos_{S'}(yc) = \{n\} = endpos_{S'}(S')$, and $yc$ belongs to the class of $cur$. Line L3 sets $next(p_i)[c] = cur$, which is right by Lemma 3.

*Line L4, case $p_t = $ NIL.* Then no $yc$ occurred in $S$, so $c$ does not occur in $S$; the class of $cur$ holds all nonempty suffixes of $S'$, its $minlen$ is 1, and its link is $init$. No old class changes: the only old strings whose $endpos$ changes are suffixes of $S'$, and only $\varepsilon$ is old among them, whose class is always $\{\varepsilon\}$.

*Otherwise,* let $p = p_t$, $q = next(p)[c]$, and $y_0 = long(p)$. The strings $yc$ for $y$ in $p$ are in $q$ (Lemma 3), and every shorter suffix $yc$ is a substring of $S$ (a suffix of $y_0 c$). So the class of $cur$ holds exactly the suffixes of $S'$ longer than $len(p) + 1$, its $minlen$ is $len(p) + 2$, and its link must be the class in $S'$ of $y_0 c$.

*Case $len(q) = len(p) + 1$ (line L5).* Then $long(q) = y_0 c$, a suffix of $S'$; by Lemma 2 every string of $q$ is a suffix of $y_0 c$ and so of $S'$, and they all gain $n$. So $q$ remains one class, unchanged in its strings, and $link(cur) = q$. Every other old class either consists of suffixes of $S'$ (those on the link path of $q$, whose strings are suffixes of $y_0 c$; they all gain $n$ and stay classes) or of non-suffixes (unchanged). Transitions out of old classes into $cur$ are exactly those set in line L3, since $xc'$ for an old $x$ lies in $cur$ only if it is a suffix of $S'$ longer than $len(p) + 1$, which means $c' = c$ and $x$ in $p_0, \ldots, p_{t-1}$.

*Case $len(q) > len(p) + 1$ (lines L6 to L8).* The strings of $q$ with length at most $len(p) + 1$ are suffixes of $y_0 c$, hence suffixes of $S'$, and gain $n$. The strings of $q$ with length greater than $len(p) + 1$ are not suffixes of $S'$: such a string $zc$, being in $q$, has $z$ in a state with a transition to $q$, and if $zc$ were a suffix of $S'$, $z$ would be a suffix of $S$ longer than $y_0$ with a transition on $c$, so it would be in one of $p_0, \ldots, p_{t-1}$, which have no such transition. So $q$ splits into $q_{short}$, the strings of lengths $minlen(q)$ to $len(p) + 1$, and $q_{long}$, the rest. The clone is $q_{short}$, with $len = len(p) + 1$ and the old link of $q$; $q$ becomes $q_{long}$, with $minlen = len(p) + 2$, so its link is the clone; and $link(cur)$ is the clone, the class of $y_0 c$. Both parts take the transitions of $q$ as they are after line L3, which line L6 copies: by Lemma 3 in $S'$, applied to each part, the extensions $wc'$ of the strings $w$ of one part lie in one class, and that class contains the old target of the transition of $q$ on $c'$ (an old class or $cur$); the only class that is split in this step is $q$ itself, and transitions into $q$ are handled next. An incoming transition $x \xrightarrow{c'} q$ must now go to the part that contains $xc'$. If $c' \ne c$ or $x$ is not a suffix of $S$, then $xc'$ is not a suffix of $S'$, so it is in $q_{long}$. If $c' = c$ and $x$ is a suffix of $S$, then $x$ is in one of $p_t, p_{t+1}, \ldots$, and $xc$ is in $q_{short}$ exactly when it goes to $q$: along the link path from $p_t$, the states whose transition on $c$ is $q$ form a prefix $p_t, \ldots, p_{s-1}$ (a shorter $x$ has $xc$ shorter, so once $xc$ falls below $minlen(q)$ it is in a class of the link path of $q$, never again in $q$). Line L7 redirects exactly these to the clone. All other old classes are unchanged in their strings, by the same argument as in the first case.

*Line L9.* $last = cur$, the class of $S'$.

So the claim holds for $S'$. Taking all states as accepting gives the substrings of $S$, and the accepting states of the suffix automaton are those on the link path of $last$, as stated in (A4). $\blacksquare$
