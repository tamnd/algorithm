---
tag: X0R4VW
kind: model
slug: markov-algorithm
name: Markov algorithm
aliases:
- normal algorithm
- Markov normal algorithm
area: automata-and-parsing/term-rewriting
level: core
summary: A string rewriting model of computation with ordered rules applied to the leftmost match.
prereqs: [string-rewriting-system, turing-machine]
see_also: [post-canonical-system, combinatory-logic, word-problem, church-turing-thesis, halting-problem, universal-turing-machine, aho-corasick, term-rewriting-system]
sources:
  - url: https://www.mathnet.ru/tm1178
    title: Andrei A. Markov, Teoriya algorifmov (Theory of algorithms), Trudy Matematicheskogo Instituta imeni V. A. Steklova 42, Izdatel'stvo Akademii Nauk SSSR, 1954
    locator: pp. 3 to 375 (normal algorithms, their composition, the normalization principle, and the unsolvability results)
  - book: isbn:9781482237726
    title: Elliott Mendelson, Introduction to Mathematical Logic, sixth edition, CRC Press, 2015
    locator: Section 5.5.2, Markov Algorithms, p. 362 onward (definition of normal algorithms, examples, and their equivalence with Turing computability)
  - book: isbn:9789027727732
    title: Andrei A. Markov and Nikolai M. Nagorny, The Theory of Algorithms, Kluwer, 1988
    locator: the English translation of the 1984 monograph, the chapters on normal algorithms and their composition
---

A **Markov algorithm**, or normal algorithm, is a model of computation that works on a single string. Its program is an ordered list of rules $P \to Q$, each one replacing a substring. At each step the machine takes the first rule in the list whose left side occurs in the current string, and replaces the leftmost occurrence. It stops when a rule marked as final has been used, or when no rule applies. Andrei A. Markov defined it around 1950 and proposed it, in his normalization principle, as a definition of what an algorithm is on strings. It computes the same functions as [Turing machines](/turing-machine/), and it is a deterministic strategy for a [string rewriting system](/string-rewriting-system/).

## The machine

We use the notation of the term rewriting pages: rules $l \to r$, and $\to^*$ for the reflexive transitive closure. Strings are words over a finite alphabet; $\varepsilon$ is the empty word and $uv$ is concatenation.

**Program.** Fix an alphabet $A$ for the input and the output, and an extended alphabet $B \supseteq A$, whose extra letters serve as markers. A **scheme** is a finite list of rules

$$P_1 \to Q_1,\quad P_2 \to Q_2,\quad \ldots,\quad P_m \to Q_m$$

with $P_i, Q_i \in B^*$. Each rule is **simple**, written $P \to Q$, or **final**, written $P \to .Q$. A left side may be the empty word, which occurs at the start of every string.

**Step.** Let $w$ be the current word.

1. Find the smallest $i$ such that $P_i$ is a substring of $w$. If there is none, stop: $w$ is the result.
2. Write $w = x P_i y$ with $x$ as short as possible, the leftmost occurrence, and replace $w$ by $x Q_i y$.
3. If rule $i$ is final, stop: the new word is the result. Else go to 1.

The machine is deterministic: each word has at most one next word. A computation from $w$ either stops with a result, or runs forever. The algorithm computes the partial function that maps $w \in A^*$ to the result, when the computation stops and the result is in $A^*$.

**Examples.** Each example was run step by step.

- *Unary addition.* With the one rule $+ \to \varepsilon$, the word $|| + |||$ becomes $|||||$ in one step, and then no rule applies.
- *Binary to unary.* The scheme $|0 \to 0||$, $1 \to 0|$, $0 \to \varepsilon$ turns a binary numeral into a unary one. On $101$ it takes 8 steps: $101$, $0|01$, $00||1$, $00||0|$, $00|0|||$, $000|||||$, $00|||||$, $0|||||$, $|||||$. The first rule doubles the marks that a $0$ passes, so a $1$ that has $k$ digits after it is worth $2^k$ marks.
- *Doubling a unary number*, with the marker $a$: the scheme $a| \to ||a$, $a \to .\varepsilon$, $\varepsilon \to a$. On $|||$ it takes 5 steps: $|||$, $a|||$, $||a||$, $||||a|$, $||||||a$, $||||||$. The last rule puts the marker at the front, the first rule moves it right and doubles each mark it passes, and the final rule removes it and stops. The order of the rules matters: if $\varepsilon \to a$ came first, it would apply forever.

## What it counts

The cost of a computation is the number of steps, and its space is the largest length of a word in it. A step is not a constant-time operation on a real machine: finding the first applicable rule and its leftmost occurrence costs $O(|w| \sum_i |P_i|)$ time by direct search, or $O(|w| + \sum_i |P_i|)$ with an [Aho-Corasick](/aho-corasick/) automaton built once for the left sides, and the replacement costs $O(|w|)$ on an array. So $t$ steps on words of length at most $s$ cost $O(t s)$ time on a RAM, for a fixed scheme.

Compared with a Turing machine, one step can do more: a rule may change a substring of any fixed length, and the machine finds the place to work by search instead of by moving a head. The simulation in the next section shows that the step counts of the two models agree up to a constant factor in one direction.

## Relation to other models

**String rewriting.** A scheme without final rules is a [string rewriting system](/string-rewriting-system/) (a semi-Thue system) with a fixed strategy: rule priority by position in the list, and the leftmost occurrence. Every step of the Markov algorithm is a step of the string rewriting system, but not conversely. A string rewriting system is in turn a [term rewriting system](/term-rewriting-system/) over unary symbols, so a Markov algorithm is a deterministic strategy for a special case of term rewriting. [Combinatory logic](/combinatory-logic/) is the analogous model on terms.

**Turing machines.** A normal algorithm can simulate a Turing machine step by step. Code a configuration with tape $u a v$, state $q$ and the head on $a$ as the word $L\,u\,q\,a\,v\,E$, where $q$ is a letter, and $L$ and $E$ mark the ends of the tape. For a move $\delta(q, a) = (p, b, R)$ use the rule $q a \to b p$, and also $q E \to b p E$ if $a$ is the blank $\sqcup$. For a move $\delta(q, a) = (p, b, L)$ use the rules $c q a \to p c b$ for each tape letter $c$, and $L q a \to L p \sqcup b$ for the left end; if $a$ is the blank, also add $c q E \to p c b E$ and $L q E \to L p \sqcup b E$, for a head on the right end. A halting state $h$ gets the final rule $h \to .h$. The word has exactly one state letter, and exactly one rule matches around it, so the order of the rules does not matter here, and each step of the machine is exactly one step of the algorithm. For a machine that adds 1 to a binary number, scanning right and then carrying left, this scheme reproduces the run on every input of up to 6 bits, with one more step for the final rule. Conversely, a Turing machine can find the first applicable rule and the leftmost occurrence by scanning, and do the replacement by shifting the tape.

**Post canonical systems and other models.** Markov algorithms are close to Post's [canonical systems](/post-canonical-system/), which also rewrite strings, but nondeterministically. Normal algorithms, Turing machines, the λ-calculus and partial recursive functions all define the same class of computable functions, which is the content of the [Church-Turing thesis](/church-turing-thesis/). Markov's normalization principle is his own form of the thesis: every algorithm on words is fully equivalent to a normal algorithm.

**Programming languages.** The pattern-directed language Refal, designed by Valentin Turchin, grew from the idea of ordered rewrite rules over strings.

## Known results in the model

**Equivalence with Turing machines.** A partial function on words is computable by a normal algorithm if and only if it is Turing computable. One direction is the simulation above, which also shows that each Turing machine step costs one Markov step. The other direction is the simulation by scanning. Markov's book develops the theory directly in terms of normal algorithms, and Mendelson (Section 5.5.2) proves the equivalence.

**Composition.** Normal algorithms are closed under composition, branching on a condition, and repetition, and Markov builds complex algorithms from simple ones with these constructions. The usual technique is to rename the letters of each part apart and to use marker letters to pass control from one scheme to the next.

**Universal algorithm.** There is a normal algorithm that, given the code of a scheme and a word, computes what the scheme computes on the word, as a [universal Turing machine](/universal-turing-machine/) does.

**Undecidability.** Whether a normal algorithm stops on a given word is undecidable, by the simulation and the undecidability of the [halting problem](/halting-problem/). Markov (1947) and Post (1947), independently, proved that the [word problem](/word-problem/) for finitely presented semigroups is undecidable, by reductions of this kind.

**Determinism and confluence.** A normal algorithm is deterministic, so its result is unique by construction, whatever the underlying string rewriting system is. The fixed strategy is what makes the result well defined; the string rewriting system itself may be non-confluent, as in the doubling example, where $\varepsilon \to a$ can apply at any time.

## References
