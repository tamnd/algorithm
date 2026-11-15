---
title: A key range of the permuterm index holds exactly the terms with a given prefix and suffix, each once
proves: [correctness]
status: full
---

A term is a string, possibly empty, without the characters \$, \* and TOP, where TOP is a character that sorts after every character of a term and after \$. For a term $t$ let $s = t\$$; the rotations of $s$ are the $|t| + 1$ strings $\rho_i(t) = s[i..] \cdot s[..i)$ for $0 \le i \le |t|$. A query $q$ has no \$ and no TOP, and each \* in it stands for any string. Write $q = P_0 * P_1 * \cdots * P_r$ with pieces $P_i$ that contain no \*. A term $t$ *matches* $q$ if $t = P_0 S_1 P_1 \cdots S_r P_r$ for some strings $S_i$, and the answer over a vocabulary $V$ is $A(q) = \{t \in V : t \text{ matches } q\}$.

**Invariant (I).** The array $keys$ is strictly increasing and is the set $\{\rho_i(t) : t \in V, 0 \le i \le |t|\}$, and $owner[j]$ is the term $t$ with $keys[j]$ a rotation of $t\$$.

**Lemma 1 (a key names its term).** Each rotation of $t\$$ contains \$ exactly once, and the rotations $\rho_0(t), \ldots, \rho_{|t|}(t)$ are distinct. A string is a rotation of $t\$$ for at most one term $t$.

*Proof.* The string $t\$$ has one \$, and a rotation keeps the multiset of characters. In $\rho_i(t)$ the \$ is at position $|t| - i$, so different $i$ give different positions of \$ and different strings. If $\kappa$ is a rotation of $t\$$, then rotating $\kappa$ so that its \$ comes last gives $t\$$ back, so $\kappa$ determines $t$. $\square$

So $owner$ is well defined, and the number of keys is $\sum_{t \in V} (|t| + 1)$.

**Lemma 2.** The constructor makes (I) true, and INSERT and DELETE keep it.

*Proof.* The empty index has no keys and $V = \emptyset$. By Lemma 1, the key $t\$ = \rho_0(t)$ is in $keys$ if and only if $t \in V$, so line L9 tests membership correctly, and INSERT of a term of $V$ changes nothing. For $t \notin V$, Lemma 1 says that no rotation of $t\$$ is a key yet. Line L10 inserts each rotation at the place that binary search finds for it, with $t$ at the same place of $owner$, which keeps $keys$ strictly increasing and $owner$ aligned. At the end $keys$ is the set for $V \cup \{t\}$. DELETE of $t \in V$ finds each rotation of $t\$$ at the place that binary search gives, since it is present, and removes it with its owner; the keys of other terms stay. $\square$

**Lemma 3 (the prefix range).** If $keys$ is sorted, PREFIX-RANGE$(p)$ returns $[lo, hi)$ such that $keys[j]$ starts with $p$ if and only if $lo \le j < hi$.

*Proof.* Here $lo$ is the number of keys less than $p$, and $hi$ is the number of keys less than $p \cdot \mathrm{TOP}$. A key $\kappa$ that starts with $p$ is at least $p$, and it is less than $p \cdot \mathrm{TOP}$, because either $\kappa = p$ or the character of $\kappa$ after $p$ is less than TOP. A key $\kappa < p$ is less than $p \cdot \mathrm{TOP}$ too. A key $\kappa \ge p$ that does not start with $p$ is not a proper prefix of $p$, so it first differs from $p$ at a position $j < |p|$ with $\kappa[j] > p[j]$, and then $\kappa > p \cdot \mathrm{TOP}$. In sorted order the keys are therefore: those less than $p$, then those that start with $p$, then the others, and the second group is the range $[lo, hi)$. $\square$

**Lemma 4 (the rotated query).** Let $X$ and $Z$ be strings without \$. A term $t$ has a rotation of $t\$$ that starts with $Z\$X$ if and only if $t = X S Z$ for some string $S$, and then exactly one rotation of $t\$$ starts with $Z\$X$.

*Proof.* If $t = XSZ$, then $\rho_{|XS|}(t) = Z\$XS$ starts with $Z\$X$. Conversely, let a rotation $\kappa$ of $t\$$ start with $Z\$X$. Its only \$ is at position $|Z|$, and the rotation with \$ at that position is $\kappa = t[|t| - |Z|..] \cdot \$ \cdot t[..|t| - |Z|)$, which needs $|Z| \le |t|$. So $Z$ is the suffix of $t$ of length $|Z|$, and $X$ is a prefix of $t[..|t| - |Z|)$, which is $t = XSZ$ with $S$ the rest. Only one rotation has its \$ at position $|Z|$, so it is the only one that starts with $Z\$$. $\square$

**Theorem.** If (I) holds, WILDCARD$(q)$ returns $A(q)$ in increasing order, with no term twice.

*Proof.* If $q$ has no \*, then $A(q)$ is $\{q\}$ when $q \in V$ and empty otherwise, and line L1 returns this by the membership test of Lemma 2.

Let $q$ have at least one \*. Line L2 sets $X = P_0$, the part before the first \*, and $Z = P_r$, the part after the last \*. Line L3 forms $p = Z\$X$, and by Lemma 3 line L4 finds the keys that start with $p$. By Lemmas 1 and 4, their owners are the terms $t \in V$ with $t = XSZ$ for some $S$, each exactly once.

If $q$ has exactly one \*, then $q = X * Z$, and $t$ matches $q$ exactly when $t = XSZ$. So the owners of the range are $A(q)$, each once, and line L5 returns them sorted with no filter.

If $q$ has two or more stars, every $t$ that matches $q$ has the form $X S Z$ with $S = S_1 P_1 \cdots S_r$, so $A(q)$ is contained in the owners of the range, each once. Line L6 keeps the owners that pass MATCHES. That test is the same as on the k-gram index page, where it is proved to return true if and only if $t$ matches $q$. So line L6 returns exactly $A(q)$, sorted, with no repeats. $\blacksquare$
