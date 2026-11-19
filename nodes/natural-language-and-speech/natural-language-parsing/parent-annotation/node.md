---
tag: SJCKA7
kind: technique
slug: parent-annotation
name: Parent annotation
aliases:
- vertical Markovization
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: "Split each nonterminal of the treebank trees by the label of its parent, so a PCFG sees more context. Klein and Manning measured F1 rising from 72.62 to 76.81."
history:
  year: 1998
  people: [Mark Johnson]
  note: "Johnson showed that the independence assumptions of a treebank PCFG depend on the tree representation, and that copying the parent label onto each node improves the parser. Klein and Manning generalized the idea in 2003."
prereqs: [probabilistic-context-free-grammar, treebank]
see_also: [latent-variable-pcfg, lexicalized-pcfg, head-rules, probabilistic-cky, parseval-measures, constituency-parsing, hidden-markov-model, smoothing]
sources:
  - paper: "Mark Johnson, PCFG Models of Linguistic Tree Representations, Computational Linguistics 24(4), 1998"
    title: "Mark Johnson, PCFG Models of Linguistic Tree Representations"
    locator: "pp. 613-632; the effect of the tree representation on a treebank PCFG, and the parent transform"
  - paper: doi:10.3115/1075096.1075150
    title: "Dan Klein and Christopher D. Manning, Accurate Unlexicalized Parsing, ACL 2003"
    locator: pp. 423-430; the orders of ancestor and sibling context and the F1 and grammar sizes of their Figure 2
  - paper: "Eugene Charniak, Tree-bank Grammars, Proceedings of AAAI-96"
    title: "Eugene Charniak, Tree-bank Grammars"
    locator: the plain treebank PCFG that parent annotation improves on
---

Parent annotation is a tree transform for treebank grammars. Before the rules of a [probabilistic context-free grammar](/probabilistic-context-free-grammar/) are read off a [treebank](/treebank/), each phrasal label is renamed to carry the label of its parent: an NP under S becomes NP^S, and an NP under VP becomes NP^VP. The grammar read off the new trees can give the two kinds of noun phrase different expansions, which a plain PCFG cannot do, because it chooses the expansion of a node from its label alone. After parsing, the parent part of every label is removed again. Mark Johnson studied the transform in 1998. In the measurements of Klein and Manning (2003) on the Penn Treebank, it raised the F1 of a plain treebank PCFG from 72.62 to 76.81, while the number of rules grew from 9657 to 14666. It is a heuristic: it adds context in a fixed way, and [latent-variable PCFGs](/latent-variable-pcfg/) learn such splits from the data instead.

## In plain words

A plain treebank grammar decides how to build a phrase by looking only at the name of the phrase, for example "noun phrase". But a noun phrase at the start of a sentence, the subject, is often just a pronoun such as "she", while a noun phrase after a verb, the object, is more often a full phrase such as "the cat". The plain grammar cannot see this difference, because both are just noun phrases.

Parent annotation gives the grammar this missing piece of context. Each phrase name gets the name of the phrase above it, so "noun phrase under a sentence" and "noun phrase under a verb phrase" become two different names with their own statistics. The parser works as before with the larger grammar, and at the end the extra part of each name is cut off.

## When it applies

The transform applies to any grammar that is read off a treebank by relative frequency and parsed with a chart parser such as [probabilistic CKY](/probabilistic-cky/). It helps when the expansion of a node depends on where the node is, which is common in natural language. Klein and Manning report that in the Penn Treebank a subject NP is 8.7 times more likely than an object NP to expand as just a pronoun.

A small example shows the effect. Take a treebank of four trees:

- (S (NP (PRP she)) (VP (VBD saw) (NP (DT the) (NN cat))))
- (S (NP (PRP he)) (VP (VBD fed) (NP (DT the) (NN dog))))
- (S (NP (DT the) (NN dog)) (VP (VBD saw) (NP (PRP her))))
- (S (NP (PRP they)) (VP (VBD left)))

Of the seven NP nodes, four expand as PRP, so the plain grammar has $q(NP \to PRP) = 4/7$ and $q(NP \to DT\ NN) = 3/7$. After annotation, the four subject nodes are NP^S, and the rule NP^S → PRP has probability 3/4. The three object nodes are NP^VP, and the rule NP^VP → PRP has probability 1/3. The plain grammar gives the trees of *she saw the cat* and *the cat saw her* the same probability $3/392$, because the two trees use the same multiset of rules. The annotated grammar gives them $1/64$ and $1/384$, a factor of 6 in favour of the pronoun subject. The numbers are exact fractions computed by the tests.

The transform does not apply in the same way to parsers that do not read rules off trees, such as [span-based neural parsers](/span-based-constituency-parsing/), whose encoder already sees the whole sentence.

## The template

The transform is a walk over the tree with an explicit stack. Each stack entry is a node of the input tree, the original label of its parent, and the list that receives its copy. The default leaves the part-of-speech tags unchanged.

```pseudo id=main
ANNOTATE(t)                                   ▷ t: a treebank tree; ^ does not occur in its labels
L1  stack ← [(root of t, ROOT, out)]
L2  while stack is not empty do
L3      pop (u, p, dest)
L4      if u is a preterminal then append a copy of u to dest;  continue
L5      append a new node with the label label(u)^p and an empty child list kids to dest
L6      for each child c of u, from right to left do push (c, label(u), kids)
L7  return the only node of out

STRIP(t)
L8  return a copy of t in which every label x is cut at its first ^
```

The whole method is then:

1. Annotate every training tree with ANNOTATE.
2. Read off the PCFG by relative frequency, $q(A \to \alpha) = \mathrm{count}(A \to \alpha) / \mathrm{count}(A)$, with $A$ an annotated label.
3. Parse a new sentence with the annotated grammar, from the start symbol S^ROOT.
4. Apply STRIP to the result and evaluate it with the [PARSEVAL measures](/parseval-measures/) against the plain gold tree.

The root has no parent, so it gets the marker ROOT. The root may have any number of children; the transform does not depend on it. STRIP undoes ANNOTATE exactly, and every tree that the annotated grammar builds strips to a tree that the plain grammar can also build. Both facts are theorems, proved in [the correctness proof](proofs/correctness.md). Whether the annotated grammar picks better trees is a measurement. ANNOTATE and STRIP each take time linear in the size of the tree.

## Classic examples

- **Johnson's treebank PCFG.** Johnson (1998) compared several tree representations for a PCFG read off the Penn Treebank and found that the parent transform improved on the plain [treebank](/treebank/) grammar, which Charniak (1996) had studied. His point was that the independence assumptions of a PCFG are a property of the tree representation, so changing the trees changes the model.
- **Unlexicalized parsing.** Klein and Manning (2003) annotated each node with its $v - 1$ nearest ancestors and kept only the last $h$ siblings in each rule. Their Figure 2 gives an F1 of 72.62 for the plain grammar ($v = 1$), 76.81 with the parent ($v = 2$), and 79.07 with the parent and grandparent and two siblings ($v = 3$, $h = 2$). They then added hand-made splits of single categories on top of this grammar.
- **Lexicalized models.** The head-driven models of Collins condition the head child and the dependents of a node on the label of the node itself, which is the parent of the children being generated. This is the same kind of context, built into the probability model instead of the labels. The heads come from [head rules](/head-rules/).
- **Learned splits.** [Latent-variable PCFGs](/latent-variable-pcfg/) replace the fixed parent split by subcategories learned with EM. Petrov et al. (2006) start from a binarized grammar without parent labels and let the splits find such context where the data supports it.
- **Sequence models.** A second-order [hidden Markov model](/hidden-markov-model/) for tagging conditions each tag on the two previous tags. It is the same move on a chain: enlarge the state so that the model sees more history, at the price of more parameters.

## Variations

- **Grandparent and higher orders.** Annotate each node with its two or more nearest ancestors, as in NP^VP^S. Each order adds context and multiplies the number of rules, so the gain shrinks once the counts become sparse.
- **Tags too.** Annotate the preterminals as well, so that a tag such as IN can tell a preposition under PP from a complementizer under SBAR. In the code this is the option tags=True.
- **Selective annotation.** Annotate only the categories where it helps, chosen on development data. This keeps the grammar smaller.
- **Sibling context.** Binarize the rules and keep only the last $h$ siblings in each intermediate symbol. This removes context from the right side of a rule, while parent annotation adds context from above. The two are usually tuned together.
- **Smoothing.** Interpolate the annotated estimate with the plain one, as in [smoothing](/smoothing/) for n-gram models, to give rules seen only in the plain treebank a nonzero probability.

## Pitfalls

- **Pushing the new label.** Writing line L6 as "push (c, label(u)^p, kids)" makes each label carry the whole chain of its ancestors, such as NP^VP^S^ROOT, which is a different and much sparser transform. The right line pushes the original label, "push (c, label(u), kids)".
- **Scoring annotated trees.** PARSEVAL compares labels as strings, so NP^S never matches NP in the gold tree. Apply STRIP before evaluation.
- **The separator.** Penn Treebank labels already contain - and =, as in NP-SBJ and NP=2. Using - as the separator makes STRIP cut off function tags as well, or cut at the wrong place. The code uses ^ and refuses labels that already contain it.
- **Function tags in the parent label.** If function tags are kept, the parent part becomes S-TPC instead of S and the counts split further. Remove function tags and empty elements before annotation, as usual for treebank PCFGs.
- **Sparse rules.** The annotated grammar has more rules, and each is seen fewer times. A rule that occurs under one parent but not under another gets probability 0 there, and a sentence can lose every parse. Smooth the annotated estimates, or back off to the plain grammar.

## Exercises

1. Show that a plain PCFG gives the same probability to a tree and to the tree in which the subject NP subtree and the object NP subtree are swapped. Use the example treebank to show that the parent-annotated grammar does not.
2. If the plain grammar has the nonterminal set $N$, show that the annotated grammar has at most $|N|(|N| + 1)$ nonterminals, and give a treebank where this bound is far from tight.
3. Prove that STRIP(ANNOTATE(t)) = t. Then show that the statement is false if a label of $t$ may contain the separator.
4. Write the grandparent version of ANNOTATE and compute, with exact fractions, the probability of *she saw the cat* under the grammar read off the example treebank.

## References
