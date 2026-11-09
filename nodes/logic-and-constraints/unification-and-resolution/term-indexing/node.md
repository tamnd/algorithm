---
tag: AFH7NE
kind: concept
slug: term-indexing
name: Term indexing
aliases:
- term index
- clause indexing
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Data structures that retrieve, from a large set of terms or clauses, those that unify with, match, are instances of, or subsume a query.
prereqs: [term, term-matching, unification-problem]
see_also: [discrimination-tree, substitution-tree, trie, subsumption, demodulation, superposition, warren-abstract-machine, inverted-index]
sources:
  - book: isbn:9780444508133
    title: I. V. Ramakrishnan, R. Sekar and A. Voronkov, Term Indexing, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume II, Chapter 26, pages 1853 to 1964 (retrieval conditions, perfect and imperfect filtering, discrimination trees, path indexing, substitution trees, code trees, and their use in provers)
  - paper: "Peter Graf, Term Indexing, Lecture Notes in Artificial Intelligence 1053, Springer, 1996"
    locator: the survey of indexing techniques, the retrieval tasks for generalizations, instances and unifiable terms, and the comparison of discrimination trees, path indexing and substitution trees
  - paper: "W. McCune, Experiments with discrimination-tree indexing and path indexing for term retrieval, Journal of Automated Reasoning 9(2), 1992, pages 147 to 167"
    locator: the description of discrimination trees and path indexing as used in Otter, and the measurements for each retrieval task
  - paper: "M. E. Stickel, The path-indexing method for indexing terms, Technical Note 473, SRI International, 1989"
    locator: the definition of path indexing and its retrieval operations
  - paper: "P. Graf, Substitution tree indexing, Rewriting Techniques and Applications (RTA 1995), Lecture Notes in Computer Science 914, Springer, 1995"
    locator: the definition of substitution trees, their insertion by common generalization, and retrieval
  - paper: "S. Schulz, Simple and efficient clause subsumption with feature vector indexing, in M. P. Bonacina and M. E. Stickel (editors), Automated Reasoning and Mathematics, Lecture Notes in Computer Science 7788, Springer, 2013, pages 45 to 67"
    locator: the definition of subsumption-compatible features, the feature vector trie, and its use for forward and backward subsumption in the E prover
  - paper: "S. Schulz, Fingerprint indexing for paramodulation and rewriting, International Joint Conference on Automated Reasoning (IJCAR 2012), Lecture Notes in Computer Science 7364, Springer, 2012"
    locator: the definition of term fingerprints, their compatibility test for unification and matching, and the fingerprint index
---

**Term indexing** is the family of data structures that store a large set of [terms](/term/) or clauses and retrieve, for a query term, those that stand in a given relation to it: unifiable with it, more general than it, instances of it, variants of it, or, for clauses, related by [subsumption](/subsumption/). Theorem provers spend most of their time on such retrievals, because each new clause must be compared with many thousands of stored ones. An index is **perfect** when it returns exactly the answers, and it is a **filter** (imperfect) when it returns a superset of candidates that must then be checked with [unification](/unification-problem/) or [matching](/term-matching/). The main techniques are [discrimination trees](/discrimination-tree/), path indexing, [substitution trees](/substitution-tree/), code trees and, for clauses, feature vector indexing.

## In plain words

A prover keeps a big library of patterns. Again and again it gets a new pattern and asks which stored patterns fit it in some way: which ones can be made equal to it, which ones cover it, which ones it covers. Checking every stored pattern each time is far too slow when the library holds a hundred thousand patterns.

An index sorts the library in advance, so that most patterns that cannot fit are skipped without being looked at. One kind of index is like a dictionary tree: patterns are spelled out symbol by symbol, and shared beginnings are stored once. Another kind lists, for each place and symbol, which patterns have that symbol at that place. Some indexes return exactly the right patterns. Others return a short list of likely candidates, which are then checked one by one.

## The idea

Notation: $S$ is the indexed set, $t$ is the query, and $\sigma$ is a substitution. The variables of $S$ and of $t$ are kept apart, as in [standardization apart](/standardization-apart/).

**Retrieval tasks.** For a query $t$, find the $s \in S$ such that

| task | condition | typical use |
|---|---|---|
| unifiable terms | $s\sigma = t\sigma$ for some $\sigma$ | [resolution](/binary-resolution/), [superposition](/superposition/), [paramodulation](/paramodulation/) |
| generalizations | $s\sigma = t$ | forward [demodulation](/demodulation/): find rewrite rules whose left side matches $t$; forward subsumption |
| instances | $s = t\sigma$ | backward demodulation and backward subsumption |
| variants | $s = t\rho$ for a renaming $\rho$ | detecting duplicate terms and clauses |

Retrieval of generalizations and of instances are matching problems, which are easier than unification, and provers often use different indexes for different tasks.

**Perfect indexes and filters.** A perfect index returns exactly the $s \in S$ with the condition. A filter returns a candidate set that contains all answers and possibly more, and each candidate is then tested. Most filters lose precision in the same place: they treat every variable as an anonymous wildcard, so they ignore that two occurrences of one variable must take the same value.

**Main techniques.**

- **Top symbol hashing.** A [hash table](/hash-table/) from the top symbol and arity to the terms. It is a very coarse filter, and it is the idea behind first-argument indexing of clauses in Prolog systems that follow the [Warren abstract machine](/warren-abstract-machine/).
- **[Discrimination trees](/discrimination-tree/).** Each term is written as the sequence of its symbols in preorder, with each variable replaced by a wildcard $*$, and the sequences are stored in a [trie](/trie/). Retrieval walks the trie with the query and lets a wildcard in the trie skip a whole subterm of the query, or a variable of the query skip a whole subterm stored in the trie. With wildcards, the tree is a filter for all tasks. **Perfect discrimination trees** keep the variable names in the trie and check consistent bindings during the walk, and they are perfect for the retrieval of generalizations. The E prover uses them for rewriting.
- **Path indexing** (Stickel 1989). For each term $s$ and each position $p$ of $s$, the index records the pair of the path to $p$ (the symbols and argument numbers on the way) and the symbol at $p$. A table maps each such path to the set of terms with that path. A query is answered by intersecting and joining these sets. Variables become wildcards, so path indexing is a filter. It is cheap to update, and it is good for instance retrieval with large sets.
- **[Substitution trees](/substitution-tree/)** (Graf 1995). Each node stores a substitution, and each stored term is the composition of the substitutions along a path from the root to a leaf. Inner nodes hold common generalizations of the terms below them, built with the same steps as [Plotkin's lgg algorithm](/plotkin-lgg/). The variables are kept, so substitution trees are perfect for all four tasks. They are compact, but insertion and deletion are more complex.
- **Code trees** (Voronkov). The indexed terms are compiled into a tree of instructions for an abstract machine that performs the matching. They are perfect for the retrieval of generalizations and are used for forward subsumption in Vampire.
- **Feature vector indexing** (Schulz 2013). A clause-level index for subsumption. Each clause $C$ gets a vector of numbers, such as the number of positive literals, the number of negative literals, and the number of occurrences and the maximal depth of each function symbol in each kind of literal. The features are chosen so that if $C$ subsumes $D$, then $f(C) \le f(D)$ in each coordinate. The vectors are stored in a trie, and a query finds all vectors that are componentwise smaller (forward subsumption) or larger (backward subsumption). It is a filter: the candidates are then tested by a full subsumption check, which is NP-complete in general. The E prover uses it for both directions of subsumption.
- **Fingerprint indexing** (Schulz 2012). Each term gets a short vector that records the symbols at a few fixed positions, or that the position is a variable or is missing. Two fingerprints that are incompatible show that the terms cannot unify or match. It is a filter with a very small cost.

| technique | level | tasks | perfect? |
|---|---|---|---|
| top symbol hashing | term or clause | all | filter |
| discrimination tree with wildcards | term | all | filter |
| perfect discrimination tree | term | generalizations | perfect |
| path indexing | term | all, best for instances | filter |
| substitution tree | term | all | perfect |
| code tree | term and clause | generalizations, forward subsumption | perfect |
| feature vector indexing | clause | forward and backward subsumption | filter |
| fingerprint indexing | term | unification and matching | filter |

## Examples

**A discrimination tree.** Let $S = \{f(a, x), f(y, b), f(g(z), b), g(a)\}$. The preorder strings, with each variable as $*$, are

- $f\ a\ *$
- $f\ *\ b$
- $f\ g\ *\ b$
- $g\ a$

and the trie shares the prefix $f$ of the first three. For the query $f(a, b)$:

- *Unifiable terms.* The walk reads $f$, then $a$. In the trie, the branch $a$ fits, and so does the wildcard $*$, but the branch $g$ does not. It returns $f(a, x)$ and $f(y, b)$, which are exactly the unifiable terms.
- *Generalizations.* The same two terms match $f(a, b)$: $f(a, x)$ with $x \mapsto b$, and $f(y, b)$ with $y \mapsto a$.

For the query $f(u, u)$, a query variable skips any subterm, so all three $f$-terms are candidates. But $f(g(z), b)$ does not unify with $f(u, u)$, because $u$ would have to be both $g(z)$ and $b$. The tree returns it because the wildcards forget that the two occurrences of $u$ are one variable. This is the typical loss of a filter.

**Path indexing.** For the same set, the path lists include the following:

| path and symbol | terms |
|---|---|
| root is $f$ | $f(a, x)$, $f(y, b)$, $f(g(z), b)$ |
| argument 1 of $f$ is $a$ | $f(a, x)$ |
| argument 1 of $f$ is $g$ | $f(g(z), b)$ |
| argument 2 of $f$ is $b$ | $f(y, b)$, $f(g(z), b)$ |
| root is $g$ | $g(a)$ |

An instance of the query $f(v, b)$ must have root $f$ and the symbol $b$ as argument 2, so the index intersects these two lists and gets $f(y, b)$ and $f(g(z), b)$. Both are instances. For the query $f(v, v)$, the only non-variable path is the root, so all three $f$-terms are candidates. None of them is an instance, because an instance of $f(v, v)$ has two equal arguments. The index cannot see this, so the candidates are tested with matching.

**Feature vectors.** Take the features (number of positive literals, number of negative literals, occurrences of $Q$ in positive literals, occurrences of $Q$ in negative literals). For $C = \{P(x)\}$ and $D = \{P(a), \neg Q(b)\}$, $f(C) = (1, 0, 0, 0)$ and $f(D) = (1, 1, 0, 1)$. As $f(C) \le f(D)$, $C$ is a candidate to subsume $D$, and the full test confirms it with $x \mapsto a$. The clause $E = \{Q(x)\}$ has $f(E) = (1, 0, 1, 0)$, and its third coordinate is larger than that of $f(D)$, so $E$ is excluded without a full test. Here subsumption is taken on multisets of literals, as in the E prover: $C\sigma$ must be a sub-multiset of $D$, so that counts of literals can only grow.

## Where it is used

- **Saturation provers.** Provers based on resolution and [superposition](/superposition/), such as Otter, SPASS, Vampire and E, use several indexes at once: one for the unification partners of inferences, one for forward and backward demodulation, and one for forward and backward subsumption. McCune's experiments with Otter compared discrimination trees and path indexing for these tasks.
- **Logic programming.** Prolog systems select the clauses that can match a call with indexing on the first argument or on several arguments, which avoids creating choice points for clauses that cannot match. See the [Warren abstract machine](/warren-abstract-machine/).
- **Term rewriting engines.** Rewriting with many rules retrieves the rules whose left side matches a subterm, which is a retrieval of generalizations. Discrimination trees and automata built from the left sides serve this purpose.
- **Tabling and memoization.** Tabled logic programming stores calls and answers in tries of terms and looks up variants and instances.
- **Type checkers and proof assistants.** Instance resolution for type classes and lemma search retrieve stored patterns that match a goal, often with discrimination trees.

## References
