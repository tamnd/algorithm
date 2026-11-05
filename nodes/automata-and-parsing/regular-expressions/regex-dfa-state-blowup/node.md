---
tag: FQY32P
kind: theorem
slug: regex-dfa-state-blowup
name: Exponential state blowup from regex to DFA
aliases:
- subset construction lower bound for regex
area: automata-and-parsing/regular-expressions
level: core
summary: The regex (a|b)*a(a|b)^(n-1) needs 2^n DFA states, so the conversion can be exponential.
prereqs: [regular-expression, deterministic-finite-automaton, myhill-nerode-relation]
see_also: [determinization-blowup-lower-bound, subset-construction, glushkov-automaton, lazy-dfa-construction, thompson-nfa-simulation, state-complexity, regex-to-nfa-conversion, brzozowski-derivatives]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 2.3.6, A Bad Case for the Subset Construction
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: pp. 114 to 125 (the subset construction and its upper bound of 2^n states)
  - paper: doi:10.1109/swat.1971.11
    title: Albert R. Meyer and Michael J. Fischer, Economy of description by automata, grammars, and formal systems, 12th Annual Symposium on Switching and Automata Theory (1971)
    locator: pp. 188 to 191
  - url: "https://arxiv.org/abs/2504.20555"
    title: Olga Martynova and Alexander Okhotin, From regular expressions to deterministic finite automata, 2^(n/2 + n^(1/2) (log n)^Θ(1)) states are necessary and sufficient, arXiv 2504.20555 (2025)
    locator: the abstract and the main theorems (upper and lower bounds in terms of the alphabetic width, and the earlier bounds 2^n and (5/4) 2^(n/2))
  - url: "https://swtch.com/~rsc/regexp/regexp1.html"
    title: Russ Cox, Regular Expression Matching Can Be Simple And Fast, 2007
    locator: section Caching the NFA to build a DFA (building only the DFA states that the input reaches)
---

## Statement

The expressions use the syntax of the [regular expression](/regular-expression/) page: union $\mid$, concatenation, star $^*$, $\varepsilon$ and $\emptyset$. The size of an expression is the number of nodes of its syntax tree, and its *alphabetic width* is the number of occurrences of symbols in it. DFAs are complete.

**Theorem.** For $n \ge 1$ let
$$r_n = (a \mid b)^* \, a \, \underbrace{(a \mid b) \cdots (a \mid b)}_{n - 1}$$
over $\Sigma = \{a, b\}$. Then:

1. $r_n$ has size $4n + 2$ and alphabetic width $2n + 1$, and $L(r_n)$ has an NFA with $n + 1$ states;
2. $L(r_n) = L_n = \{w \in \{a, b\}^* : |w| \ge n \text{ and the } n\text{-th symbol from the end of } w \text{ is } a\}$;
3. every DFA that accepts $L(r_n)$ has at least $2^n$ states, and the minimal DFA has exactly $2^n$.

**Corollary.** There are regular expressions of size $m$ for every $m = 4n + 2$ whose minimal DFA has $2^{(m - 2)/4}$ states. So every algorithm that converts regular expressions to DFAs takes time $2^{\Omega(m)}$ in the worst case, if only to write its output.

## In plain words

The pattern says: "the letter $n$ places before the end is an $a$". It is short, about four symbols for each unit of $n$. A machine that may guess can read the text, guess when it has reached that letter, and then count the remaining $n - 1$ letters.

A machine that cannot guess does not know where the end is until it gets there. So it must remember the last $n$ letters it has read, because any one of them could become the letter that matters. There are $2^n$ different strings of $n$ letters, and any two of them can be told apart by reading a few more letters. So the machine needs $2^n$ states, and the pattern of length about $4n$ becomes a machine of size $2^n$.

## Proof

**Part 1.** The subexpression $(a \mid b)^*$ has 4 nodes, the symbol $a$ has 1, and each of the $n - 1$ copies of $(a \mid b)$ has 3. The expression is the concatenation of $n + 1$ factors, which takes $n$ concatenation nodes. In total $4 + 1 + 3(n - 1) + n = 4n + 2$. The symbol occurrences are 2 in the star, 1 for the middle $a$, and 2 in each copy, $2n + 1$ in total. The NFA has states $0, 1, \ldots, n$, start 0, accepting state $n$, loops at 0 on $a$ and $b$, a move $0 \xrightarrow{a} 1$, and moves $i \xrightarrow{a} i + 1$ and $i \xrightarrow{b} i + 1$ for $1 \le i \le n - 1$; it reads $(a \mid b)^*$ in state 0, guesses the middle $a$, and then counts $n - 1$ more symbols.

**Part 2.** By the semantics of union, concatenation and star, $L(r_n)$ is the set of strings $u a v$ with $u \in \{a, b\}^*$ and $v \in \{a, b\}^{n-1}$. A string $w$ has this form if and only if $|w| \ge n$ and the symbol at position $|w| - n + 1$, which is the $n$-th from the end, is $a$: given such a $w$, take $u$ as the first $|w| - n$ symbols and $v$ as the last $n - 1$; conversely, in $u a v$ the $a$ is followed by exactly $n - 1$ symbols.

**Part 3, lower bound.** Let $x \neq y$ be two strings of length $n$. They differ at some position $i$ with $1 \le i \le n$; by symmetry let $x_i = a$ and $y_i = b$. Let $z = b^{i - 1}$. The strings $xz$ and $yz$ have length $n + i - 1$, and the $n$-th symbol from the end of each is the symbol at position $i$. So $xz \in L_n$ and $yz \notin L_n$. Hence $x$ and $y$ are not equivalent under the [Myhill-Nerode relation](/myhill-nerode-relation/) of $L_n$: a DFA for $L_n$ must reach different states on $x$ and on $y$, since from a common state it would accept both $xz$ and $yz$ or neither. There are $2^n$ strings of length $n$, so every DFA for $L_n$ has at least $2^n$ states.

**Part 3, upper bound.** Let $D$ have the states $\{a, b\}^n$, the start state $b^n$, the move $x_1 x_2 \cdots x_n \xrightarrow{c} x_2 \cdots x_n c$ for each symbol $c$, and accept in the states with $x_1 = a$. By induction on $|w|$, the state after reading $w$ is the string of the last $n$ symbols of $b^n w$. If $|w| \ge n$, its first symbol is the $n$-th symbol from the end of $w$. If $|w| < n$, its first symbol is a padding $b$, and $w \notin L_n$ because it is too short. So $D$ accepts exactly $L_n$ with $2^n$ states. With the lower bound, the minimal DFA has exactly $2^n$ states. $\square$

**Corollary.** For $m = 4n + 2$ we get $n = (m - 2)/4$, and the minimal DFA of $r_n$ has $2^{(m - 2)/4}$ states. Any DFA for $L(r_n)$ has at least this many, so producing it takes at least this much time. $\square$

**Check by script.** For $n = 1, \ldots, 10$, a script built the [Glushkov automaton](/glushkov-automaton/) of $r_n$, applied the [subset construction](/subset-construction/), and minimized the result. The subset DFA had $2^n + 1$ reachable states and the minimal DFA had $2^n$: 2, 4, 8, $\ldots$, 1024.

## Consequences

- **Engines avoid building the full DFA.** A DFA matches in $O(n)$ time per text of length $n$, but building it can cost $2^{\Omega(m)}$. Engines such as RE2 and [grep](/grep/) build only the DFA states that the text reaches ([lazy DFA construction](/lazy-dfa-construction/)) and fall back to [Thompson's NFA simulation](/thompson-nfa-simulation/), which takes $O(m)$ time per symbol, when the cache fills up.
- **The pattern of the theorem in practice.** Patterns like `[ab]*a[ab]{20}` ask for the 21st character from the end, and a DFA for them has $2^{21}$ states. Patterns with bounded repetition after a free prefix are the usual cause of DFA cache trouble ([bounded repetition](/bounded-repetition/)).
- **Lexer generators.** Lexer generators build the DFA ahead of time. Token patterns rarely have the form of the theorem, so the DFA stays small in practice, but no worst-case guarantee exists.
- **Decision problems.** Testing [equivalence](/regex-equivalence/) or [universality](/regex-universality/) by building DFAs costs exponential time in the worst case. These problems are PSPACE-complete, so the exponential is not only a weakness of the method ([PSPACE-completeness of equivalence](/regex-equivalence-pspace-completeness/)).
- **Complement.** Complementing a regular expression through a DFA has the same blowup, which is why expressions with complement are much more succinct ([extended regular expressions](/extended-regular-expressions/)).

## Tightness

- **An upper bound in the alphabetic width.** Let $r$ have alphabetic width $k$. Its [Glushkov automaton](/glushkov-automaton/) has an initial state $0$ and one state for each of the $k$ positions, and every move goes into a position, never into $0$. So after at least one symbol the subset construction is in a subset of the $k$ positions, and the reachable subsets are $\{0\}$ and at most $2^k$ others: the DFA has at most $2^k + 1$ states. The family $r_n$, with $k = 2n + 1$, needs $2^n = 2^{(k - 1)/2}$, so the exponent is right up to a factor of 2.
- **The exact exponent.** Martynova and Okhotin (2025) closed most of this gap: the DFA for an expression of alphabetic width $k$ needs at most $2^{k/2 + O(\sqrt{k \ln k})}$ states, and some expressions over two letters need $2^{k/2 + \Omega(\sqrt{k / \ln k})}$. Before their work, the best bounds were $2^k$ and $\frac{5}{4} 2^{k/2}$.
- **In the size.** Since the alphabetic width is at most the size, the upper bound gives at most $2^m + 1$ states for size $m$, and the family $r_n$ gives $2^{(m - 2)/4}$.
- **One letter.** Over a one-letter alphabet the blowup is smaller: an NFA with $s$ states has a DFA with $e^{O(\sqrt{s \ln s})}$ states, so the two-letter alphabet in the theorem cannot be reduced to one letter with the same growth ([determinization blowup](/determinization-blowup-lower-bound/)).
- **NFAs do not blow up.** By contrast, every expression of size $m$ has an NFA with at most $2m$ states ([regex to NFA conversion](/regex-to-nfa-conversion/)), so the blowup is purely the price of determinism.

## History

Rabin and Scott (1959) introduced the subset construction, with its upper bound of $2^s$ states for an NFA with $s$ states. Meyer and Fischer (1971) studied how much more succinct one kind of description can be than another, and gave families of NFAs whose DFAs must be exponentially larger. The language of the "$n$-th symbol from the end" is the standard textbook example of the blowup, for instance in Section 2.3.6 of Hopcroft, Motwani and Ullman. Cox (2007) explained why practical engines built on automata construct the DFA lazily. Martynova and Okhotin (2025) determined the exponent of the worst case in terms of the alphabetic width up to lower-order terms.

## References
