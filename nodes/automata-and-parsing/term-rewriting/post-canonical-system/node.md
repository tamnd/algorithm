---
tag: V2JJ42
kind: model
slug: post-canonical-system
name: Post canonical system
aliases:
- Post production system
- Post system
- Post normal system
- tag system
area: automata-and-parsing/term-rewriting
level: advanced
summary: A string-rewriting model of computation equivalent to Turing machines.
prereqs: [string-rewriting-system, turing-machine]
see_also: [markov-algorithm, undecidability-of-word-problem, post-correspondence-problem, recursively-enumerable-language, church-turing-thesis, context-free-grammar, word-problem]
sources:
  - paper: doi:10.2307/2371809
    title: Emil L. Post, Formal reductions of the general combinatorial decision problem, American Journal of Mathematics 65(2) (1943)
    locator: pp. 197 to 215 (canonical systems, the normal form theorem, and the generated sets as recursively enumerable sets)
  - paper: doi:10.2307/1970290
    title: Marvin L. Minsky, Recursive unsolvability of Post's problem of Tag and other topics in theory of Turing machines, Annals of Mathematics 74(3) (1961)
    locator: pp. 437 to 455 (tag systems can simulate Turing machines, so their halting problem is undecidable)
  - paper: doi:10.1145/321203.321206
    title: John Cocke and Marvin Minsky, Universality of tag systems with P = 2, Journal of the ACM 11(1) (1964)
    locator: pp. 15 to 20
  - paper: doi:10.1109/FOCS.2006.58
    title: Damien Woods and Turlough Neary, On the time complexity of 2-tag systems and small universal Turing machines, 47th IEEE Symposium on Foundations of Computer Science (FOCS 2006)
    locator: pp. 439 to 448 (2-tag systems simulate Turing machines in polynomial time)
  - paper: doi:10.1016/j.tcs.2007.10.020
    title: Liesbeth De Mol, Tag systems and Collatz-like functions, Theoretical Computer Science 390(1) (2008)
    locator: pp. 92 to 101
---

A **Post canonical system** generates a set of strings from a finite set of axioms by productions that cut a string into pieces and reassemble them, possibly with new letters added. Emil Post published the model in 1943 and showed that the sets it generates are exactly the recursively enumerable sets, so it has the power of Turing machines. Its special cases are the normal systems, with productions $g P \to P h$, the tag systems, which read the front of a word and append to its end, and the semi-Thue systems behind the [word problem](/word-problem/) and the [Post correspondence problem](/post-correspondence-problem/).

## The machine

We use the notation of the term rewriting pages, specialized to strings as on the [string rewriting system](/string-rewriting-system/) page: an alphabet $A$, words $A^*$ with empty word $\lambda$, rules $l \to r$, and $\to^*$ for the reflexive transitive closure. A **canonical system** has:

- a finite alphabet $A$, and a subset $T \subseteq A$ of terminal letters (the others are auxiliary);
- a finite set of **axioms**, words in $A^*$;
- a finite set of **productions** $g_0 P_1 g_1 P_2 \cdots P_m g_m \to h_0 P_{i_1} h_1 \cdots P_{i_k} h_k$, where the $g_j, h_j \in A^*$ are fixed words, the $P_i$ are string variables that range over $A^*$, and every variable on the right occurs on the left.

**A step.** A word $w$ yields $w'$ if $w$ matches the left side under some assignment of words to the variables, and $w'$ is the right side under the same assignment. A variable that occurs twice on the left must take the same value at both places. A word $w$ may match a left side in several ways, and each match gives a step.

**Generated set.** The words derivable from the axioms by finitely many steps are the **theorems** of the system; the **language** of the system is the set of theorems in $T^*$. Post's general form also allows productions with several premises, $\alpha_1, \ldots, \alpha_s \to \beta$, which yield $\beta$ when all $\alpha_j$ are theorems under one assignment; single premises suffice, by the normal form theorem below.

**Special cases.**

- **Semi-Thue system.** A rule $l \to r$ is the production $P\, l\, Q \to P\, r\, Q$: replace one occurrence of $l$ anywhere.
- **Normal system.** Every production has the form $g P \to P h$: remove the prefix $g$ and append $h$.
- **Tag system.** A deletion number $d \ge 1$ and a word $w_a$ for each letter $a$. If $|w| \ge d$ and $w$ starts with $a$, remove the first $d$ letters and append $w_a$; a word shorter than $d$ halts. This is a normal system that is deterministic: each word has at most one successor.

## What it counts

- **Derivability**, the set of theorems or the language: the main question for canonical and normal systems, which are nondeterministic generators like grammars.
- **Steps**, the number of productions applied in a derivation, which plays the role of time. For deterministic systems such as tag systems, each word has a unique run, and time is its length until it halts.
- **Word length**, which plays the role of space. A tag system keeps its whole memory in one word used as a queue.

## Relation to other models

- **Turing machines.** A configuration of a Turing machine is a word, and each transition is a semi-Thue rule, as in the proof of the [undecidability of the word problem](/undecidability-of-word-problem/). Conversely, a Turing machine can enumerate all derivations of a canonical system. So the languages of canonical systems are exactly the [recursively enumerable languages](/recursively-enumerable-language/), one more piece of evidence for the [Church-Turing thesis](/church-turing-thesis/).
- **Grammars.** An unrestricted (type 0) grammar is a semi-Thue system with a start symbol, terminal letters, and the generated terminal words as its language. A [context-free grammar](/context-free-grammar/) is the case where each left side is one nonterminal.
- **Markov algorithms.** A [Markov algorithm](/markov-algorithm/) is a semi-Thue system made deterministic by an order on the rules and a fixed leftmost position.
- **Queue machines.** A tag system is a machine with one queue: read and remove from the front, write at the back. Rotating the whole word through the queue simulates a tape.

## Known results in the model

- **Normal form theorem** (Post, 1943). For every canonical system there is a normal system over a larger alphabet whose theorems over the original alphabet are exactly the theorems of the given system. The idea is to rotate the word: a normal production can read only the front, so the word is cycled letter by letter, with markers, until the part to be rewritten reaches the front.
- **Power.** The sets of words generated by canonical systems, and by normal systems with auxiliary letters, are exactly the recursively enumerable sets (Post, 1943). Derivability in a canonical system is therefore undecidable in general, and there is a fixed normal system with an undecidable set of theorems.
- **Tag systems are universal.** Minsky (1961) proved that tag systems can simulate Turing machines, so their halting problem is undecidable, and Cocke and Minsky (1964) showed that deletion number $d = 2$ suffices. The simulation of Cocke and Minsky is exponentially slow; Woods and Neary (2006) gave a simulation of Turing machines by 2-tag systems in polynomial time, which also makes several small universal Turing machines efficient.
- **Tag systems and arithmetic.** Tag systems can compute number-theoretic maps on unary words. The 2-tag system $a \to bc$, $b \to a$, $c \to aaa$ maps $a^n$ to $a^{n/2}$ for even $n$ and to $a^{(3n+1)/2}$ for odd $n$, the next word that consists only of $a$'s, which is the Collatz map. A program checked this for $2 \le n < 60$. On $a^3$ the run is $aaa \to abc \to cbc \to caaa \to aaaaa$. So the question whether this tag system halts from every $a^n$ is a form of the Collatz problem; De Mol (2008) studies this link.
- **Post's tag problem.** Post's own example has $d = 3$, $0 \to 00$ and $1 \to 1101$. From $10010$ it gives $101101$, $1011101$, $11011101$, $111011101, \ldots$. Post asked whether its behaviour on every initial word is decidable; Minsky's paper of 1961 takes its title from this problem.

**Examples of generated languages.** The system with axioms $\lambda, a, b$ and productions $P \to a P a$, $P \to b P b$ generates the palindromes over $\{a, b\}$. The system with the one axiom $abc$ and the one production $a P b Q c \to a a P b b Q c c$ generates $\{a^n b^n c^n : n \ge 1\}$, a language that is not context-free: each match of the left side to $a^n b^n c^n$ gives $a^{n+1} b^{n+1} c^{n+1}$, whichever $b$ the pattern uses. Both claims were checked by a program up to length 9 and 18.

## References
