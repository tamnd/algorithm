---
title: MINIMAL-ABSENT-WORDS reports each minimal absent word exactly once
proves: [correctness]
status: full
---

Let $y = y[0..n-1]$ be a string over the alphabet $\Sigma$, indexed from 0, and let $F$ be the set of its factors, including the empty word $\varepsilon$. For $x \in F$ let $E(x) = \{\, j : y[j - |x| + 1..j] = x \,\}$ be its set of end positions, with $E(\varepsilon) = \{-1, 0, \ldots, n-1\}$.

**The suffix automaton.** We use these properties of the automaton built at line L1, which hold for the standard online construction (Blumer and coauthors, 1985).

1. The states are the classes of the relation $E(x) = E(x')$ on $F$; state 0 is the class of $\varepsilon$, which contains only $\varepsilon$.
2. The words of a state $p$ are the suffixes of its longest word with lengths in $(\mathrm{len}[\mathrm{link}[p]], \mathrm{len}[p]]$, and for $p \ne 0$ the suffix of the longest word of $p$ of length $\mathrm{len}[\mathrm{link}[p]]$ is the longest word of $\mathrm{link}[p]$.
3. $\mathrm{next}[p][b]$ is defined if and only if $xb \in F$ for the words $x$ of $p$.
4. $\mathrm{end}[p] \in E(x)$ for the words $x$ of $p$.

Property 3 is well defined: whether $xb \in F$ depends only on $E(x)$, since $xb \in F$ if and only if some $j \in E(x)$ has $j + 1 \le n - 1$ and $y[j + 1] = b$. For property 4, a state created while reading $y[i]$ is the class of the prefix $y[0..i]$, so $i \in E(x)$ for its words. A clone of a state $q$ holds words whose set of end positions contains $E$ of the words of $q$, because they are suffixes of those words, so $\mathrm{end}[q]$ is a valid end position for the clone too. The end positions of a state never lose elements as the construction reads further letters, so property 4 holds at the end.

**Lemma 1 (one-letter words).** A letter $b$ is in $\mathrm{MAW}(y)$ if and only if $\mathrm{next}[0][b]$ is undefined.

*Proof.* The only proper factor of $b$ is $\varepsilon \in F$, so $b \in \mathrm{MAW}(y)$ if and only if $b \notin F$, which by property 3 for the state $0$ of $\varepsilon$ means that $\mathrm{next}[0][b]$ is undefined. $\square$

**Lemma 2 (longer words).** Let $w = a\,u\,b$ with letters $a, b$ and a word $u$. Then $w \in \mathrm{MAW}(y)$ if and only if there is a state $p \ne 0$ such that $au$ is the shortest word of $p$, $u$ is the longest word of $\mathrm{link}[p]$, $\mathrm{next}[\mathrm{link}[p]][b]$ is defined and $\mathrm{next}[p][b]$ is undefined.

*Proof.* Every proper factor of $w$ is a factor of $au$ or of $ub$, and $F$ is closed under taking factors, so $w \in \mathrm{MAW}(y)$ if and only if $au \in F$, $ub \in F$ and $aub \notin F$.

($\Leftarrow$) The word $au$ is a word of $p$, so it is in $F$; $\mathrm{next}[p][b]$ undefined gives $aub \notin F$ by property 3; $u$ is a word of $\mathrm{link}[p]$ and $\mathrm{next}[\mathrm{link}[p]][b]$ is defined, so $ub \in F$.

($\Rightarrow$) Let $p$ be the state of $au \in F$; $p \ne 0$ since $au \ne \varepsilon$. By property 3, $\mathrm{next}[p][b]$ is undefined because $aub \notin F$, while the state of $u$ has a transition by $b$ because $ub \in F$; so $u$ is not in $p$. By property 2, the words of $p$ are the suffixes of its longest word with lengths in $(\mathrm{len}[\mathrm{link}[p]], \mathrm{len}[p]]$. The word $au$ is one of them and $u$, its suffix of length $|au| - 1$, is not, so $|au| - 1 \le \mathrm{len}[\mathrm{link}[p]] < |au|$. Hence $|au| = \mathrm{len}[\mathrm{link}[p]] + 1$, $au$ is the shortest word of $p$, and $u$ is the suffix of the longest word of $p$ of length $\mathrm{len}[\mathrm{link}[p]]$, which by property 2 is the longest word of $\mathrm{link}[p]$. Then $\mathrm{next}[\mathrm{link}[p]][b]$ is defined since $ub \in F$. $\square$

**Claim.** The list $M$ returned at line L10 contains each word of $\mathrm{MAW}(y)$ exactly once and nothing else, where $(i, \ell, b)$ stands for $y[i..i+\ell-1]\,b$.

*Proof.* Lines L3 and L4 append $(0, 0, b)$, the word $b$, exactly for the letters $b \in \Sigma$ with $\mathrm{next}[0][b]$ undefined; by Lemma 1 these are the one-letter minimal absent words, each once.

Lines L5 to L9 consider each pair $(p, b)$ with $p \ne 0$ and $\mathrm{next}[\mathrm{link}[p]][b]$ defined exactly once, and append a triple exactly when $\mathrm{next}[p][b]$ is undefined. For such a pair, line L6 sets $\ell = \mathrm{len}[\mathrm{link}[p]] + 1$, the length of the shortest word $x_p$ of $p$ by property 2, and by property 4 $x_p = y[\mathrm{end}[p] - \ell + 1..\mathrm{end}[p]]$, so line L9 appends the word $x_p\,b$. Write $x_p = a\,u$ with $a$ a letter; then $u$, the suffix of $x_p$ of length $\mathrm{len}[\mathrm{link}[p]]$, is the longest word of $\mathrm{link}[p]$ by property 2. By Lemma 2 ($\Leftarrow$), $x_p\,b \in \mathrm{MAW}(y)$. By Lemma 2 ($\Rightarrow$), each word of $\mathrm{MAW}(y)$ of length at least 2 arises from some such pair $(p, b)$. Two different pairs give different words: if $p \ne p'$ then $x_p \ne x_{p'}$ because the states are disjoint classes, and the pair is recovered from the word as its prefix without the last letter and that letter. So each word of length at least 2 is appended exactly once. Words of length 1 and words of length at least 2 are different, which completes the proof. $\square$

**Cost.** By property 3, if $\mathrm{next}[p][b]$ is defined then $xb \in F$ for the words $x$ of $p$, hence $vb \in F$ for their suffixes $v$ in $\mathrm{link}[p]$, so $\mathrm{next}[\mathrm{link}[p]][b]$ is defined. Thus the loop of line L7 at state $p$ runs $|\mathrm{next}[p]| + z_p$ times, where $z_p$ is the number of words appended at $p$. Summed over all states this is at most the number of transitions plus $z$, and the automaton has $O(n)$ states and transitions. With hash maps each test takes $O(1)$ expected time, so after the construction the scan takes $O(n + \sigma + z)$ expected time, and the construction takes $O(n)$ expected time. ∎
