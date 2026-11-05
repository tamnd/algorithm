---
tag: 7FR9JQ
kind: problem
slug: regex-minimization
name: Regex minimization
aliases:
- minimal regular expression problem
area: automata-and-parsing/regular-expressions
level: research
summary: Find a shortest regular expression equivalent to a given one, which is PSPACE-hard.
prereqs: [regular-expression, regex-equivalence, regex-universality, pspace]
see_also: [regex-equivalence, nfa-minimization, dfa-minimization, state-elimination, dfa-to-regex-conversion, kleene-algebra, star-height-problem, regex-equivalence-pspace-completeness]
sources:
  - paper: "Albert R. Meyer and Larry J. Stockmeyer, The equivalence problem for regular expressions with squaring requires exponential space, 13th Annual Symposium on Switching and Automata Theory (1972)"
    locator: pp. 125 to 129 (minimizing regular expressions and NFAs is PSPACE-complete)
  - paper: doi:10.1137/0222067
    title: Tao Jiang and Bala Ravikumar, Minimal NFA problems are hard, SIAM Journal on Computing 22(6) (1993)
    locator: pp. 1117 to 1141 (minimization stays PSPACE-complete when the language is given by a DFA)
  - paper: doi:10.1016/j.jcss.2006.11.002
    title: Gregor Gramlich and Georg Schnitger, Minimizing NFA's and regular expressions, Journal of Computer and System Sciences 73(6) (2007)
    locator: pp. 908 to 923; conference version STACS 2005, LNCS 3404, pp. 399 to 411 (no approximation within o(m) unless P = PSPACE, Theorem 4; the unary case, Theorem 3; regular expressions from DFAs under cryptographic assumptions, Theorem 1)
  - paper: doi:10.1016/S0022-0000(76)80034-7
    title: Andrzej Ehrenfeucht and Paul Zeiger, Complexity measures for regular expressions, Journal of Computer and System Sciences 12(2) (1976)
    locator: pp. 134 to 146 (DFAs with n states whose shortest regular expressions have length exponential in n)
  - paper: "Larry J. Stockmeyer and Albert R. Meyer, Word problems requiring exponential time, Fifth Annual ACM Symposium on Theory of Computing (STOC 1973)"
    locator: pp. 1 to 9 (inequivalence of regular expressions over a one-letter alphabet is NP-complete)
---

Regex minimization is the problem of finding, for a given [regular expression](/regular-expression/), a shortest expression that denotes the same language. Unlike [DFA minimization](/dfa-minimization/), which is fast and has a unique answer, it is PSPACE-complete in its decision form (Meyer and Stockmeyer, 1972), it stays PSPACE-complete when the language is given by a DFA (Jiang and Ravikumar, 1993), and no polynomial algorithm can even approximate the minimum size within a factor $o(m)$ unless P = PSPACE (Gramlich and Schnitger, 2005). Shortest expressions are also not unique. In practice expressions are shortened by algebraic rewriting and by careful conversion from automata, with no guarantee of optimality.

## In plain words

Many patterns describe the same set of strings, and some are much longer than they need to be. "Any mix of a's and b's that contains an a, or only b's" is just "any mix of a's and b's". Minimization asks for the shortest pattern with exactly the same meaning.

For machines that read one letter at a time there is a fast method that always finds the smallest machine, and it is unique. For patterns there is nothing like it. Even checking that a short pattern means the same as a long one is a very hard problem, and finding the shortest pattern is at least as hard. Even coming close to the shortest size is hard.

So tools simplify patterns with rules that are always safe, such as "a star of a star is just a star", and accept that the result may not be the shortest.

## Definition

The expressions use the syntax of the [regular expression](/regular-expression/) page: symbols of $\Sigma$, $\varepsilon$, $\emptyset$, union $\mid$, concatenation and star $^*$. The *size* $\lvert r \rvert$ of an expression is the number of symbols, constants and operators in it, its length in reverse Polish notation; so $(a \mid b)^*$ has size 4. Other measures are the total length with parentheses and the *alphabetic width*, the number of symbol occurrences. The hardness results hold for all of them.

**Input.** A regular expression $r$ of size $m$ over $\Sigma$.

**Output.** An expression $s$ with $L(s) = L(r)$ and $\lvert s \rvert$ as small as possible.

**Decision version.** Given $r$ and a number $k$, is there an expression $s$ with $\lvert s \rvert \le k$ and $L(s) = L(r)$?

## Variants

- **From an automaton.** The language is given by a DFA or an NFA instead of an expression. From a DFA the input can be exponentially larger than a shortest expression, but the problem is still PSPACE-complete (Jiang and Ravikumar, 1993, as reported by Gramlich and Schnitger).
- **To an automaton.** Find a smallest NFA for an expression or an automaton ([NFA minimization](/nfa-minimization/)), with the same hardness.
- **Approximation.** Find an expression at most a factor $c$ larger than the shortest.
- **One letter.** Over $\Sigma = \{a\}$, equivalence is coNP-complete (Stockmeyer and Meyer, 1973), so the decision version is in $\Sigma_2^p$; Gramlich and Schnitger showed that a polynomial algorithm cannot output an expression within a factor $m^{1 - \delta}$ of the minimum unless P = NP.
- **Other measures.** Minimize the [star height](/star-height-problem/), the nesting depth of stars, instead of the size. That problem is decidable but far harder to analyze.
- **Practical syntax.** With character classes, $r^+$, $r?$ and bounded repetition, sizes change, but the hardness proofs carry over. Backreferences go beyond regular languages and are outside this problem.

## Examples

Over $\{a, b\}$ a script listed every expression of size at most 11, kept one shortest expression for each language, identified by its minimal DFA, and so found the exact minima below. It also confirmed each equivalence by comparing automata.

| expression | size | shortest equivalent | size |
|---|---|---|---|
| $(a \mid b)^* a (a \mid b)^* \mid b^*$ | 14 | $(a \mid b)^*$ | 4 |
| $(a^* b^*)^*$ | 6 | $(a \mid b)^*$ | 4 |
| $(aa)^* \mid a (aa)^*$ | 11 | $a^*$ | 2 |
| $b^* (a b^* a b^*)^*$ | 13 | $(b \mid a b^* a)^*$ | 9 |
| $\varepsilon \mid a \mid aa$ | 7 | $\varepsilon \mid a (\varepsilon \mid a)$, or $(\varepsilon \mid a)(\varepsilon \mid a)$ | 7 |
| $(ab)^* a$ | 6 | itself, or $a (ba)^*$ | 6 |
| $(a \mid b)^* abb$ | 10 | itself | 10 |

- **No unique minimum.** $(ab)^* a$ and $a (ba)^*$ are both shortest for the same language, and so are $\varepsilon \mid a(\varepsilon \mid a)$ and $(\varepsilon \mid a)(\varepsilon \mid a)$. By contrast, the minimal DFA is unique up to renaming of states.
- **Even number of $a$s.** The usual expression $b^* (a b^* a b^*)^*$ is not shortest: $(b \mid a b^* a)^*$ is, with size 9 against 13, and no expression of size at most 8 denotes this language.
- **DFA size is a poor guide.** $(a \mid b)^* abb$ has a minimal DFA with 4 states and a shortest expression of size 10, while $(b \mid a b^* a)^*$ has 2 states and size 9. In the other direction, there are DFAs with $n$ states whose shortest expressions have size exponential in $n$ (Ehrenfeucht and Zeiger, 1976).

## Known algorithms

- **Exhaustive search.** List expressions in order of size and test each for [equivalence](/regex-equivalence/) with $r$. Listing by size with one representative per language, as in the script above, is valid because every subexpression of a shortest expression is itself shortest for its language. The number of languages grows exponentially with the size: the script found 16,576 distinct languages among the expressions of size at most 11 over two letters. This is practical only for small expressions.
- **Algebraic simplification.** Rewrite with sound laws, such as $r \mid r = r$, $\emptyset r = \emptyset$, $\varepsilon r = r$, $(r^*)^* = r^*$, $r^* r^* = r^*$, $\varepsilon \mid r r^* = r^*$ and $(r^* s^*)^* = (r \mid s)^*$, which are theorems of [Kleene algebra](/kleene-algebra/). Each step is cheap and keeps the language, but rewriting gets stuck in local minima and does not reach a shortest expression in general; by the bounds below, no polynomial method can unless P = PSPACE.
- **Through automata.** Convert to a minimal DFA, or a small NFA, and back to an expression by [state elimination](/state-elimination/) ([DFA to regex conversion](/dfa-to-regex-conversion/)). The order in which states are eliminated changes the result a great deal, and heuristics choose an order that keeps the expressions short; the output is not minimal in general.
- **Polynomial space.** For the decision version, guess $s$ of size at most $k$ one symbol at a time and test $L(s) = L(r)$ in polynomial space; if $k \ge m$ the answer is yes, with $s = r$.

## Bounds

- **PSPACE-complete.** The decision version is in PSPACE by the last algorithm and Savitch's theorem. It is PSPACE-hard because [universality](/regex-universality/) is: Gramlich and Schnitger build, from a deterministic machine that runs for at least $2^n$ steps on inputs of length $n$ before it accepts, expressions $r_w$ of size $O(n)$ whose language is $\Sigma^*$ if the machine rejects $w$, and $\Sigma^*$ minus the single string $x$ that encodes its accepting computation otherwise. In the first case $(a \mid b)^*$, of size 4, is equivalent. In the second, an expression of size $s$ has a [Glushkov automaton](/glushkov-automaton/) with at most $s + 1$ states and so a DFA with at most $2^{s + 1}$ states, while $\Sigma^*$ minus one string of length $N$ needs $N + 2$ states, which forces $s \ge \log_2 (N + 2) - 1$, at least about $n$.
- **No good approximation.** The same gap, a constant against $\Omega(m)$, shows that no polynomial algorithm approximates the minimum size within a factor $o(m)$ unless P = PSPACE (Gramlich and Schnitger, Theorem 4), over every alphabet with at least two letters.
- **From a DFA.** PSPACE-complete (Jiang and Ravikumar, 1993). Under a cryptographic assumption, polynomial algorithms cannot find expressions much shorter than the DFA even when expressions of polylogarithmic size exist (Gramlich and Schnitger, Theorem 1).
- **Expression size from a DFA.** Some DFAs with $n$ states need expressions of size $2^{\Omega(n)}$ (Ehrenfeucht and Zeiger, 1976), and state elimination always gives size $2^{O(n)}$ times a polynomial in $\lvert \Sigma \rvert$.

## Reductions

- **From universality.** As in the bounds: $r$ is universal if and only if it has an equivalent expression of size 4 over $\{a, b\}$, for the expressions $r_w$ of the construction, whose languages are either $\Sigma^*$ or have only large expressions.
- **Universality from the optimization version.** An algorithm that outputs a shortest expression decides universality over $\{a, b\}$: $r$ is universal if and only if the output is $(a \mid b)^*$ or $(b \mid a)^*$, since a script confirmed that these are the only expressions of size at most 4 for $\Sigma^*$.
- **To equivalence.** The decision version is an existential search over candidate expressions, each followed by an equivalence test.

## Applications

- **Readable output.** Tools that convert automata to expressions, learn expressions from examples or generate them from grammars simplify the result before showing it to people, since state elimination produces long expressions.
- **Faster matching.** Shorter expressions give smaller automata and fewer states for [Thompson's simulation](/thompson-nfa-simulation/) and backtracking engines, and simplifying $(a^* b^*)^*$ to $(a \mid b)^*$ also removes an exponential worst case for backtracking: Python takes about 4 seconds to reject $a^{24}$ against $(a^* b^*)^* c$ and no measurable time against $(a \mid b)^* c$ ([ReDoS](/redos/)).
- **Normal forms in derivative engines.** Engines that build [derivatives](/regex-derivative/) keep their expressions small with simplification laws; without them the number of states is not even finite.
- **Descriptional complexity.** The size of the shortest expression is a measure of how complex a regular language is, and comparing it with the sizes of minimal DFAs and NFAs is a central topic of [state complexity](/state-complexity/).

## References
