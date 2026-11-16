---
tag: 6NGQQH
kind: problem
slug: post-correspondence-problem
name: Post correspondence problem
aliases: []
area: complexity/computability
level: core
summary: Given a finite list of dominoes, each with a top word and a bottom word, decide whether some sequence of them spells the same word on top and bottom. The problem is undecidable.
prereqs: [halting-problem, acceptance-problem, many-one-reducibility]
see_also: [acceptance-problem, undecidability, cfg-ambiguity-undecidable, cfl-intersection-undecidable, church-theorem, post-canonical-system, word-problem, posts-theorem]
sources:
  - paper: doi:10.1090/S0002-9904-1946-08555-9
    title: Emil L. Post, A variant of a recursively unsolvable problem, Bulletin of the American Mathematical Society 52(4) (1946)
    locator: pp. 264 to 268
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 5.2, A simple undecidable problem
  - title: Andrzej Ehrenfeucht, Juhani Karhumäki and Grzegorz Rozenberg, The (generalized) Post correspondence problem with lists consisting of two words is decidable, Theoretical Computer Science 21(2) (1982)
    locator: pp. 119 to 144
  - paper: doi:10.4230/LIPIcs.STACS.2015.649
    title: Turlough Neary, Undecidability in binary tag systems and the Post correspondence problem for five pairs of words, STACS 2015, LIPIcs 30
    locator: pp. 649 to 661
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A4, problem SR11, Bounded Post correspondence problem
  - title: Michael S. Paterson, Unsolvability in 3 x 3 matrices, Studies in Applied Mathematics 49(1) (1970)
    locator: pp. 105 to 107
---

The Post correspondence problem asks whether a finite set of dominoes can be laid in a row so that the top and the bottom spell the same word. Each domino carries a word on top and a word on the bottom, and each domino may be used any number of times. Emil Post defined the problem in 1946 and proved it [undecidable](/undecidability/). It is the usual starting point for undecidability proofs about grammars, logic and matrices, because it has no machines in it: only words and concatenation. A search through all sequences finds a match when one exists, so the problem is computably enumerable, but no algorithm can report "no match" for every instance that has none.

## In plain words

You have a few kinds of tiles. Each tile has a short word on its top half and a short word on its bottom half. You may use as many copies of each kind as you like. Put tiles side by side in a row. Can you make the top row and the bottom row read exactly the same?

For a given row you can check this fast. The hard part is to know whether some row works at all. Rows can be very long before they match, and there is no limit on how long you must try.

Post proved that no method answers this question for every set of tiles. The reason is that tiles can be designed so that a match must spell out the full run of a computer program that stops. Deciding whether a match exists would then decide whether that program stops.

## Definition

**Instance.** A finite list of pairs of nonempty words $(t_1, b_1), \ldots, (t_k, b_k)$ over a finite alphabet $\Sigma$. We draw the pair $(t_i, b_i)$ as the domino $[t_i / b_i]$.

**Question.** Is there a nonempty sequence of indices $i_1, i_2, \ldots, i_m$, with repeats allowed, such that
$$t_{i_1} t_{i_2} \cdots t_{i_m} = b_{i_1} b_{i_2} \cdots b_{i_m}?$$

Such a sequence is a *match* or *solution*. As a language, $\mathrm{PCP}$ is the set of codes of lists that have a match.

**Theorem (Post 1946).** $\mathrm{PCP}$ is computably enumerable (c.e.) and complete for the c.e. sets under many-one reductions. So it is undecidable, and the set of lists with no match is not c.e. This stays true over the alphabet $\{0, 1\}$.

The proof reduces the [acceptance problem](/acceptance-problem/) to PCP. A list of dominoes is built so that the bottom row always runs one configuration of the machine ahead of the top row, and the rows can only become equal after the machine enters its accepting state. The full proof is in [the proof of undecidability](proofs/main.md).

## Variants

- **Modified PCP (MPCP).** The match must start with the first domino. It is the middle step of the standard proof, and it is undecidable too.
- **Fixed number of pairs.** With $k = 1$ the problem is trivial, and with $k = 2$ it is decidable (Ehrenfeucht, Karhumäki and Rozenberg 1982). With $k = 5$ it is undecidable (Neary 2015, improving on earlier bounds of $7$). The cases $k = 3$ and $k = 4$ are open.
- **Unary alphabet.** Over a one-letter alphabet only the lengths count, and the problem is decidable; see Known algorithms.
- **Binary alphabet.** Over $\{0, 1\}$ the problem is still undecidable: code each letter as a binary block of fixed length.
- **Bounded PCP.** The instance also gives a number $K$ in unary, and the question is whether a match of at most $K$ dominoes exists. This version is NP-complete (Constable, Hunt and Sahni 1974, listed by Garey and Johnson as problem SR11). A guessed sequence is a short certificate.

## Examples

**A match of five dominoes.** Take the four dominoes
$$[b / ca],\quad [a / ab],\quad [ca / a],\quad [abc / c].$$
The sequence $2, 1, 3, 2, 4$ gives $a \cdot b \cdot ca \cdot a \cdot abc = abcaaabc$ on top and $ab \cdot ca \cdot a \cdot ab \cdot c = abcaaabc$ on the bottom. A breadth-first search over all sequences shows that no shorter match exists. This instance is from Sipser.

**Small matches.** For $[a / aa], [ab / b]$ the match $1, 2$ spells $aab$. For $[a / ab], [ba / a]$ the match $1, 2$ spells $aba$.

**No match.** For $[abc / ab], [ca / a], [acc / ba]$ every top is longer than its bottom, so every sequence gives a longer top than bottom, and there is no match.

**A long shortest match.** The four dominoes
$$[1000 / 0],\quad [01 / 0],\quad [1 / 101],\quad [00 / 001]$$
have a match, but the shortest one uses $206$ dominoes and spells a word of $412$ symbols. Small instances can hide long solutions, and this is the practical face of undecidability: there is no computable bound on the length of the shortest match in terms of the size of the instance, since such a bound would turn the search into a decision procedure.

## Known algorithms

- **Search by overhang.** After a prefix of a match, one row must be a prefix of the other. Keep only the *overhang*: which row is ahead, and the extra word it has. Start from the dominoes where one word is a prefix of the other, and extend by one domino at a time. A match is found when the overhang becomes empty. Breadth-first search over overhang states finds a shortest match, and it is a semi-decision procedure: it halts on every instance with a match.
- **Proofs of no match.** If the set of reachable overhangs is finite and none of them is empty, the search ends and proves that there is no match. Simple tests also help: a match must start with a domino in which one word is a prefix of the other, and end with one in which one word is a suffix of the other; if all tops are longer than their bottoms, or all shorter, there is no match.
- **Unary alphabet.** If $t_i = a^{p_i}$ and $b_i = a^{q_i}$, let $d_i = p_i - q_i$. A match exists if and only if some $d_i = 0$, or some $d_i > 0$ and some $d_j < 0$. In the second case use domino $i$ exactly $-d_j$ times and domino $j$ exactly $d_i$ times. This runs in linear time.
- **Bounded search.** Bounded PCP with $K$ in unary is in NP, and in practice it is attacked with SAT solvers or with the overhang search cut at depth $K$.

## Bounds

- **Undecidable** in general, with five or more pairs, and over two letters.
- **Semi-decidable.** The overhang search halts exactly on the instances with a match.
- **Complete.** Every c.e. set reduces to PCP by a many-one reduction, so PCP has the [Turing degree](/turing-degrees/) of the [halting problem](/halting-problem/).
- **Decidable cases.** Two pairs, a unary alphabet, and every instance where all tops are longer than their bottoms or all shorter.
- **Bounded version.** NP-complete, so a polynomial-time algorithm for it would give P = NP.

## Reductions

All reductions here are many-one reductions by total computable maps.

- **From A_TM to PCP.** Through MPCP, as in the proof. A computation history of the machine is spelled out, with the bottom row one step ahead.
- **To ambiguity of grammars.** For a list of dominoes, build a grammar with one part that derives top words followed by reversed index sequences, and one part that does the same for bottom words. It is ambiguous if and only if the list has a match. So [ambiguity of context-free grammars](/cfg-ambiguity-undecidable/) is undecidable.
- **To intersection of context-free languages.** The same two parts, as two separate grammars, have a common word if and only if the list has a match. So [emptiness of the intersection](/cfl-intersection-undecidable/) of two context-free languages is undecidable, and so is [equivalence of grammars](/cfg-equivalence-undecidable/).
- **To first-order validity.** Floyd's construction builds, from a list of dominoes, a first-order sentence that is valid if and only if the list has a match. This proves [Church's theorem](/church-theorem/).
- **To matrix mortality.** Paterson (1970) coded pairs of words as $3 \times 3$ integer matrices and showed that it is undecidable whether some product of matrices from a given finite set is the zero matrix.

## Applications

- **Formal languages.** Most undecidability results for context-free grammars go through PCP: ambiguity, equivalence and emptiness of intersection.
- **Logic.** The undecidability of first-order logic, in the form of [Church's theorem](/church-theorem/), has a short proof from PCP.
- **Matrix problems.** Mortality, and other questions about products of integer matrices, are undecidable by reductions from PCP.
- **Teaching.** PCP is often the first undecidable problem that has no machines in its statement, and so it shows that undecidability is not only about programs.

## References
