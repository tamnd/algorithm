---
tag: XBE1Y5
kind: theorem
slug: church-theorem
name: Church's theorem
aliases:
- undecidability of first-order logic
area: complexity/computability
level: advanced
summary: "No algorithm decides whether a sentence of first-order logic is valid. Validity is computably enumerable, so it is semi-decidable but not decidable (Church and Turing, 1936)."
prereqs: [post-correspondence-problem, halting-problem, recursively-enumerable-language]
see_also: [entscheidungsproblem, post-correspondence-problem, godel-incompleteness-theorem, halting-problem, first-order-theorem-proving, herbrand-theorem, presburger-arithmetic, tarski-decidability-theorem]
sources:
  - paper: doi:10.2307/2269326
    title: Alonzo Church, A note on the Entscheidungsproblem, Journal of Symbolic Logic 1(1) (1936), with a correction in Journal of Symbolic Logic 1(3) (1936), pp. 101 to 102
    locator: pp. 40 to 41
  - paper: doi:10.1112/plms/s2-42.1.230
    title: Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society (2) 42 (1936)
    locator: pp. 230 to 265, Section 11, Application to the Entscheidungsproblem
  - paper: doi:10.1007/BF01696781
    title: Kurt Gödel, Die Vollständigkeit der Axiome des logischen Funktionenkalküls, Monatshefte für Mathematik und Physik 37 (1930)
    locator: pp. 349 to 360 (the completeness theorem)
  - book: isbn:9780521543101
    title: Michael Huth and Mark Ryan, Logic in Computer Science, Modelling and Reasoning about Systems, second edition, Cambridge University Press, 2004
    locator: Section 2.5, Undecidability of predicate logic (the reduction from the Post correspondence problem)
  - paper: doi:10.1073/pnas.48.3.365
    title: A. S. Kahr, Edward F. Moore and Hao Wang, Entscheidungsproblem reduced to the AEA case, Proceedings of the National Academy of Sciences 48(3) (1962)
    locator: pp. 365 to 377
  - book: isbn:9783540570738
    title: Egon Börger, Erich Grädel and Yuri Gurevich, The Classical Decision Problem, Perspectives in Mathematical Logic, Springer, 1997
    locator: the chapters Reductions and Undecidable Standard Classes for Pure Predicate Logic
---

Church's theorem says that there is no algorithm that decides, for every sentence of first-order logic, whether the sentence is valid, that is, true in every structure. Alonzo Church proved it in 1936, and Alan Turing proved it independently a few months later with his machines. Together they gave the negative answer to Hilbert's [Entscheidungsproblem](/entscheidungsproblem/). The theorem has a positive half: by Gödel's completeness theorem the valid sentences are exactly the provable ones, so a program that lists all proofs finds every valid sentence. Validity is therefore computably enumerable (c.e.) but not decidable. The proof below reduces the [Post correspondence problem](/post-correspondence-problem/) to validity.

## Statement

Fix a first-order vocabulary that contains one constant symbol, two unary function symbols and one binary relation symbol. For larger vocabularies the result follows at once.

**Theorem (Church 1936, Turing 1936).** The set of valid first-order sentences over this vocabulary is c.e. and complete for the c.e. sets under many-one reductions. In particular it is undecidable. Equivalently, the set of satisfiable sentences is undecidable, and it is not c.e.

The two forms are equivalent because a sentence $\varphi$ is valid if and only if $\neg \varphi$ is not satisfiable.

## In plain words

First-order logic is the usual language of mathematics: "for all", "there exists", "and", "or", "not", and names for objects, functions and relations. A sentence is valid if it is true no matter what the names stand for.

Hilbert hoped for a machine that could read any such sentence and say whether it is valid. Church and Turing showed that no such machine exists.

The trouble is that sentences can describe computations. For any puzzle of matching tiles, there is a sentence that is valid exactly when the puzzle has a solution. A machine that judged all sentences would solve all such puzzles, and no machine can.

What remains possible is a search. If a sentence is valid, there is a proof of it, and a program that tries all proofs will find one. If the sentence is not valid, the search can run forever.

## Proof

*Validity is c.e.* By Gödel's completeness theorem (1930), a sentence is valid if and only if it has a proof in a standard proof system. Proofs are finite strings and checking a proof is decidable, so a program that lists all strings and checks each one halts exactly on the valid sentences.

*Hardness.* The reduction is Floyd's, as given by Huth and Ryan. Let $(s_1, t_1), \ldots, (s_k, t_k)$ be an instance of PCP over the alphabet $\{0, 1\}$, which is undecidable. Use a constant $e$, unary function symbols $f_0$ and $f_1$, and a binary relation symbol $P$. For a word $u = b_1 b_2 \cdots b_m$ over $\{0, 1\}$, write
$$f_u(x) = f_{b_m}(\cdots f_{b_2}(f_{b_1}(x)) \cdots),$$
with $f_u(x) = x$ for the empty word. So $f_u$ appends the letters of $u$ in order. Let $\varphi$ be the sentence $(\varphi_1 \wedge \varphi_2) \to \varphi_3$, where
$$\varphi_1 = \bigwedge_{i=1}^{k} P\big(f_{s_i}(e),\, f_{t_i}(e)\big),$$
$$\varphi_2 = \forall v\, \forall w\, \Big( P(v, w) \to \bigwedge_{i=1}^{k} P\big(f_{s_i}(v),\, f_{t_i}(w)\big) \Big),$$
$$\varphi_3 = \exists z\, P(z, z).$$
The map from the instance to $\varphi$ is computable. We show that $\varphi$ is valid if and only if the instance has a match.

*If the instance has a match $i_1, \ldots, i_n$.* Let $\mathcal{M}$ be any structure. If $\mathcal{M}$ does not satisfy $\varphi_1 \wedge \varphi_2$, it satisfies $\varphi$. Otherwise, for a word $u$ let $[u]$ be the element $f_u(e)$ of $\mathcal{M}$; then $f_{u'}([u]) = [u u']$ for all words $u, u'$. By $\varphi_1$, the pair $([s_{i_1}], [t_{i_1}])$ is in $P$. If $([s_{i_1} \cdots s_{i_j}], [t_{i_1} \cdots t_{i_j}])$ is in $P$, then by $\varphi_2$ with $i = i_{j+1}$, so is $([s_{i_1} \cdots s_{i_{j+1}}], [t_{i_1} \cdots t_{i_{j+1}}])$. By induction the pair for $j = n$ is in $P$. Its two words are equal, so its two elements are equal, and $z = [s_{i_1} \cdots s_{i_n}]$ satisfies $P(z, z)$. So $\mathcal{M}$ satisfies $\varphi_3$, and $\varphi$.

*If $\varphi$ is valid.* Let $\mathcal{M}$ be the structure whose elements are the words over $\{0, 1\}$, with $e$ the empty word, $f_0(u) = u0$, $f_1(u) = u1$, and
$$P = \{ (s_{i_1} \cdots s_{i_n},\ t_{i_1} \cdots t_{i_n}) : n \ge 1,\ 1 \le i_1, \ldots, i_n \le k \}.$$
In $\mathcal{M}$ the term $f_u(e)$ is the word $u$. The pairs with $n = 1$ give $\varphi_1$. If $(v, w)$ is in $P$, then appending one more index $i$ gives $(v s_i, w t_i)$ in $P$, which is $\varphi_2$. Since $\varphi$ is valid, $\mathcal{M}$ satisfies $\varphi_3$: some word $z$ has $(z, z)$ in $P$. That is, $s_{i_1} \cdots s_{i_n} = t_{i_1} \cdots t_{i_n}$ for some $n \ge 1$, which is a match.

So the map is a many-one reduction from PCP to validity. PCP is complete for the c.e. sets, so validity is too. A complete c.e. set is undecidable. Satisfiability is the complement of validity under the computable map $\varphi \mapsto \neg\varphi$, so it is undecidable, and it is not c.e., since then validity would be both c.e. and co-c.e., and so decidable. $\blacksquare$

## Consequences

- **The Entscheidungsproblem has no solution.** No algorithm decides validity, or satisfiability, of first-order sentences. See [Entscheidungsproblem](/entscheidungsproblem/).
- **Theorem provers cannot be complete deciders.** An [automated prover](/first-order-theorem-proving/) for first-order logic, such as one based on resolution and [Herbrand's theorem](/herbrand-theorem/), can be complete: it finds a proof of every valid sentence. By the theorem, it cannot also halt on every sentence that is not valid.
- **Undecidable theories.** A theory with finitely many axioms $A$ proves $\varphi$ exactly when $A \to \varphi$ is valid. So an undecidable theory with finitely many axioms gives another proof of the theorem, and this is the route Church took: every consistent theory that contains enough arithmetic is undecidable, and some such theories have finitely many axioms. This is closely linked to [Gödel's incompleteness theorem](/godel-incompleteness-theorem/).
- **Finite models.** Trakhtenbrot (1950) proved the version for finite structures: whether a sentence has a finite model is undecidable. Here the set of sentences with a finite model is c.e., and the set of sentences true in all finite structures is not c.e., so the completeness theorem has no finite analogue.

## Tightness

The theorem needs some expressive power, and many weaker fragments are decidable.

- **Monadic logic.** If every relation symbol is unary and there are no function symbols and no equality, validity is decidable. Such a sentence is satisfiable if and only if it has a model of size at most $2^r$, where $r$ is the number of relation symbols, so a finite search decides it.
- **Prefix classes.** For sentences in prenex form without function symbols, the class $\exists^* \forall^*$ (Bernays and Schönfinkel) and the class $\exists^* \forall \exists^*$ (Ackermann) have a decidable satisfiability problem. The class $\forall \exists \forall$ already has an undecidable satisfiability problem (Kahr, Moore and Wang 1962). The full classification is in Börger, Grädel and Gurevich.
- **Decidable theories.** Validity in a single structure can be decidable even when general validity is not. The theory of $(\mathbb{N}, +)$, [Presburger arithmetic](/presburger-arithmetic/), and the theory of the real numbers with $+$ and $\times$, by [Tarski's theorem](/tarski-decidability-theorem/), are decidable.
- **Vocabulary.** The function symbols in the proof can be replaced by relation symbols, and a single binary relation symbol is enough for undecidability. With only unary relation symbols the problem becomes the decidable monadic case above.

## History

Hilbert and Ackermann stated the Entscheidungsproblem in their 1928 textbook as a main problem of mathematical logic: find a procedure that decides whether a given first-order formula is valid. Gödel's completeness theorem of 1930 showed that validity equals provability, and so is semi-decidable. In 1936 Church defined effective calculability by the lambda calculus, proved that a problem about lambda terms is unsolvable, and in a two-page note in the first issue of the *Journal of Symbolic Logic* extended this to first-order logic. Turing, working on his own, defined his machines, proved that no machine decides whether a machine ever prints a given symbol, and in Section 11 of his paper coded this into first-order logic. The short proof through PCP came later, and Kahr, Moore and Wang used tilings to show that even the $\forall \exists \forall$ class is undecidable.

## References
