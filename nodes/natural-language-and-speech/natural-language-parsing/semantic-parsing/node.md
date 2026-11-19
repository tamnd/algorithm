---
tag: PZ76MD
kind: problem
slug: semantic-parsing
name: Semantic parsing
aliases:
- natural language to logical form
area: natural-language-and-speech/natural-language-parsing
level: core
summary: Map a sentence to a formal meaning representation, such as a logical form, a database query or a program, that can be executed.
prereqs: [lambda-calculus, structured-prediction]
see_also: [combinatory-categorial-grammar, abstract-meaning-representation, smatch, semantic-role-labeling, encoder-decoder-model, grammar-constrained-decoding, synchronous-context-free-grammar, program-synthesis]
sources:
  - paper: "John M. Zelle and Raymond J. Mooney, Learning to parse database queries using inductive logic programming, Proceedings of AAAI-96, Volume 2, 1050-1055, 1996"
    title: "John M. Zelle and Raymond J. Mooney, Learning to parse database queries using inductive logic programming"
    locator: "the CHILL system, the GeoQuery questions with Prolog queries, and the learned control rules for a shift-reduce parser"
  - paper: "Luke S. Zettlemoyer and Michael Collins, Learning to map sentences to logical form: structured classification with probabilistic categorial grammars, UAI 2005, 658-666"
    title: "Luke S. Zettlemoyer and Michael Collins, Learning to map sentences to logical form"
    locator: "the task definition with lambda-calculus logical forms, the CCG lexicon learned by GENLEX, and the log-linear model over derivations"
  - paper: "Laura Banarescu, Claire Bonial, Shu Cai, Madalina Georgescu, Kira Griffitt, Ulf Hermjakob, Kevin Knight, Philipp Koehn, Martha Palmer and Nathan Schneider, Abstract Meaning Representation for Sembanking, Proceedings of the 7th Linguistic Annotation Workshop and Interoperability with Discourse, 2013, 178-186"
    title: "Laura Banarescu et al., Abstract Meaning Representation for Sembanking"
    locator: "AMR as a broad-coverage target for semantic parsing"
  - paper: doi:10.1162/coli_a_00324
    title: "Marco Kuhlmann, Giorgio Satta and Peter Jonsson, On the complexity of CCG parsing, Computational Linguistics 44(3), 447-482, 2018"
    locator: "the complexity of universal recognition for CCG"
---

Semantic parsing maps a sentence to a formal representation of its meaning, such as a logical form in the [lambda calculus](/lambda-calculus/), a database query or a program, which a machine can execute or reason with. It differs from syntactic parsing, whose output is a tree over the words, and from [semantic role labeling](/semantic-role-labeling/), whose output is labeled spans: the output of semantic parsing is an expression of another language, with its own symbols and structure, and need not mention the words at all. Broad-coverage semantic parsing into [abstract meaning representation](/abstract-meaning-representation/) graphs is the same problem with a graph as the target, evaluated with [Smatch](/smatch/).

## In plain words

A person asks a database "which states border Texas?". The database does not understand English, but it can run a query. A semantic parser turns the question into that query. The query must be exactly right: a small mistake gives a wrong answer, not a slightly worse one.

The hard part is that the same request can be worded in many ways, and the words do not line up one to one with the parts of the query. A parser learns this mapping from examples, either pairs of sentences and queries, or pairs of questions and their answers.

## Definition

**Input.** A sentence $w = w_1 \cdots w_n$ of $n$ words, and often a context: a database schema, a knowledge base, or the state of a program or a robot.

**Output.** An expression $z$ of a formal meaning representation language $\mathcal{L}$, such as a typed lambda calculus over the predicates of a database, Prolog, SQL, a domain-specific language, general-purpose code, or AMR graphs.

**Question.** Find $z$ whose meaning is the meaning of $w$. In the learned setting, a model gives a score $s(w, z)$, and the parser outputs $\hat z = \arg\max_{z \in \mathcal{L}} s(w, z)$, often limited to expressions that are well typed or that run without error in the context. This is a case of [structured prediction](/structured-prediction/) with an output space that is infinite and recursive.

**Supervision.** In the fully supervised setting the training data are pairs $(w, z)$. In the weakly supervised setting they are pairs of a sentence and the result $y$ of executing the correct expression, its denotation, and the parser must find expressions that give $y$; many wrong expressions give the right answer by accident.

**Evaluation.** Exact match of $z$ with the gold expression after normalization; execution or denotation accuracy, the share of sentences whose predicted expression gives the gold result; and for graphs, the [Smatch](/smatch/) score.

## Variants

- **Database queries.** The target is SQL or a query in logic over a fixed database. Questions about geography in the GeoQuery data of Zelle and Mooney (1996) are the classic small benchmark. Later benchmarks ask for SQL over many databases with schemas not seen in training.
- **Questions over knowledge bases.** The target is a query over a large graph of facts, with many predicates, so lexical coverage is the main difficulty.
- **Broad-coverage meaning graphs.** The target is an [AMR](/abstract-meaning-representation/) or a similar graph for any sentence, with no execution, evaluated by graph matching.
- **Code generation.** The target is a program in a general-purpose language, judged by tests. It overlaps with [program synthesis](/program-synthesis/) from specifications in natural language.
- **Instructions and dialogue.** The target is a sequence of actions for a robot or an agent, or a query that depends on earlier turns of a conversation.

## Examples

**A question about geography.** "Which states border Texas?" maps to the lambda term $\lambda x.\, \mathit{state}(x) \wedge \mathit{borders}(x, \mathit{texas})$, whose denotation over the database is the set of states that border Texas. With a [CCG](/combinatory-categorial-grammar/) lexicon in the style of Zettlemoyer and Collins (2005), `states` $\vdash N : \lambda x.\,\mathit{state}(x)$, `border` $\vdash (S\backslash NP)/NP : \lambda y.\lambda x.\,\mathit{borders}(x, y)$, `Texas` $\vdash NP : \mathit{texas}$, and a category for `which` that combines a noun with a verb phrase, the derivation builds the term word by word.

**A database query.** "How many employees work in Paris?" maps to `SELECT COUNT(*) FROM employee WHERE city = 'Paris'`. A different but equivalent query, for example with an extra join that does not change the result, is right under execution accuracy and wrong under exact match.

**A meaning graph.** "The boy wants to go" maps to the AMR `(w / want-01 :ARG0 (b / boy) :ARG1 (g / go-01 :ARG0 b))`, where the boy is both the wanter and the goer.

## Known algorithms

- **Induced parsers with logic programming.** CHILL (Zelle and Mooney 1996) learned, by inductive [logic programming](/logic-programming/), control rules for a shift-reduce parser that builds Prolog queries, from GeoQuery pairs of questions and queries.
- **Grammar-based parsing with CCG.** Zettlemoyer and Collins (2005) induce a CCG lexicon whose entries carry lambda terms, from sentences paired with logical forms only, and train a log-linear model over derivations. Parsing is chart parsing with a beam: an item is a category with a lambda term over a span $(i, j)$, where spans are fenceposts and $(i, j)$ covers the words $i + 1$ to $j$. The meaning is read off the best derivation.
- **Synchronous grammars.** A [synchronous context-free grammar](/synchronous-context-free-grammar/) pairs rules for the sentence with rules for the meaning, so that parsing the sentence builds the meaning, as in syntax-based machine translation.
- **Sequence-to-sequence models.** An [encoder-decoder model](/encoder-decoder-model/) reads the sentence and writes the meaning representation as a sequence of tokens, often with a mechanism that copies names from the input. [Grammar-constrained decoding](/grammar-constrained-decoding/) restricts the output to well-formed expressions of $\mathcal{L}$, or the decoder writes the abstract syntax tree of the expression rule by rule.
- **Graph parsers for AMR.** Transition-based parsers build the graph with stack actions, graph-based parsers first find the concepts and then the best set of edges, and sequence-to-sequence parsers write a linearized graph.
- **Pretrained language models.** Large pretrained models fine-tuned on pairs, or prompted with examples by [in-context learning](/in-context-learning/), now give the strongest results on many benchmarks (measurement, varies by benchmark).

## Bounds

- **Parsing with a fixed grammar (theorem).** With a fixed CCG lexicon, recognition is polynomial in $n$; see [combinatory categorial grammar](/combinatory-categorial-grammar/). The meanings of all derivations can be exponentially many, so a parser keeps the best few per chart item.
- **Grammar as input (theorem).** If the lexicon is part of the input, CCG recognition is EXPTIME-complete, and NP-complete without empty categories (Kuhlmann, Satta and Jonsson 2018). Lexicon induction that reparses with large candidate lexicons pays for this in practice.
- **Equivalence of outputs (theorem).** Whether two queries of first-order logic give the same answer on every database is undecidable, and for conjunctive queries it is NP-complete, by [query containment](/query-containment-problem/) in both directions. This is why evaluation uses exact match, which is too strict, or execution on one database, which can accept wrong queries.
- **Graph evaluation (theorem).** Computing the Smatch score exactly is NP-hard; see [Smatch](/smatch/).

## Reductions

- **To structured prediction.** With a scoring function over derivations and a search procedure, semantic parsing is a [structured prediction](/structured-prediction/) problem, and learning methods for it apply, such as log-linear models and the [structured perceptron](/structured-perceptron/).
- **To translation.** A semantic parser translates from a natural language to a formal one, so methods of machine translation apply: synchronous grammars and encoder-decoder models.
- **From question answering.** Answering a question over a database or a knowledge base reduces to semantic parsing followed by execution. Weak supervision uses this direction backward: it trains the parser from answers.
- **Shallow versions.** [Semantic role labeling](/semantic-role-labeling/) finds the predicate-argument part of the meaning and leaves out quantifiers, entity types and the link to a database.

## Applications

- Natural language interfaces to databases and spreadsheets.
- Question answering over knowledge bases.
- Commands for robots, assistants and smart devices.
- Code generation from descriptions, and SQL generation for data analysis.
- Broad-coverage meaning graphs used in summarization, generation and machine translation research.

## References
