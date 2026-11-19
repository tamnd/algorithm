---
tag: 2GJA5E
kind: technique
slug: hclg-decoding-graph
name: HCLG decoding graph
aliases:
- WFST decoding graph
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Compose HMM, context, lexicon and grammar transducers into one optimized WFST that maps HMM states to words for search.
prereqs: [pronunciation-lexicon, n-gram-language-model, hidden-markov-model, triphone-model, weighted-transducer-composition, weighted-determinization, weight-pushing]
see_also: [finite-state-transducer, weighted-automaton, time-synchronous-beam-search, token-passing, word-lattice, hopcroft-minimization, determinization-blowup-lower-bound, katz-backoff]
sources:
  - paper: doi:10.1006/csla.2001.0184
    title: Mehryar Mohri, Fernando Pereira and Michael Riley, Weighted finite-state transducers in speech recognition, Computer Speech and Language 16(1), 2002, pages 69 to 88
    locator: the construction of the recognition transducer from the HMM, context, lexicon and grammar transducers by composition, determinization, minimization and weight pushing, with auxiliary symbols
  - url: https://kaldi-asr.org/doc/graph.html
    title: Kaldi documentation, Decoding graph construction in Kaldi
    locator: the formula HCLG = asl(min(rds(det(H' o min(det(C o min(det(L o G)))))))), the disambiguation symbols #1, #2 and #0, and the aim to keep the graph stochastic instead of pushing weights
  - book: isbn:9781467303668
    title: Daniel Povey, Arnab Ghoshal, Gilles Boulianne and others, The Kaldi speech recognition toolkit, IEEE Workshop on Automatic Speech Recognition and Understanding (ASRU), 2011
    locator: the overview of the toolkit and its decoding with weighted finite-state transducers built with OpenFst
  - url: https://aclanthology.org/J97-2003/
    title: Mehryar Mohri, Finite-state transducers in language and speech processing, Computational Linguistics 23(2), 1997, pages 269 to 311
    locator: the determinization of transducers and weighted automata, and the condition under which it terminates
---

The HCLG graph is the search network of a WFST speech recognizer. It is one weighted transducer, built offline as the composition $H \circ C \circ L \circ G$ of four models. $G$ is the grammar or n-gram language model, an acceptor over words. $L$ is the pronunciation lexicon, which maps phone sequences to words. $C$ maps context-dependent phones, such as triphones, to phones. $H$ maps HMM states to context-dependent phones. The result maps sequences of HMM states to word sequences, with the language model cost and the transition costs on its arcs. Built naively, the composition is far too large and too nondeterministic to search. The construction therefore [determinizes](/weighted-determinization/) and minimizes after each [composition](/weighted-transducer-composition/), and can [push the weights](/weight-pushing/) toward the start. Auxiliary symbols #1, #2, ... make the lexicon determinizable. A decoder then runs [time-synchronous beam search](/time-synchronous-beam-search/) or [token passing](/token-passing/) on the graph, with acoustic scores from the HMM states.

## In plain words

A recognizer needs four kinds of knowledge: which HMM states make up each sound, how sounds change with their neighbors, how each word is pronounced, and which word sequences are likely. Each kind can be written as a machine that reads one kind of symbol and writes another.

If you plug the four machines into each other ahead of time, you get one big machine that reads HMM states and writes words. The decoder then needs only that one machine. To keep it small, words that start with the same sounds share the start of their path, and words that end alike share the end. The language model costs are moved as early as possible, so that the decoder can drop bad paths soon.

## When it applies

- The models can be written as weighted finite-state machines: an n-gram or other finite-state language model, a lexicon with a finite list of pronunciations, a context model of finite width, and HMMs.
- The graph can be built offline, and memory allows it. For very large language models, a smaller $G$ is used in the graph and the large one later, by [lattice rescoring](/lattice-rescoring/) or by composition on the fly.
- The costs live in the tropical semiring: the cost of a path is the sum of its arc costs, the costs are negative log probabilities, and the decoder takes the minimum. Determinization and minimization then keep the best cost of every word sequence.

## The template

The cost convention is used throughout: a cost is $-\log p$, and a smaller cost is better.

1. **Build $G$.** An n-gram model becomes a weighted acceptor with one state per history. The back-off arcs of a [Katz](/katz-backoff/) or similar model are $\varepsilon$ arcs. Kaldi replaces their $\varepsilon$ by the symbol #0, so that they are not removed as epsilons during determinization.
2. **Build $L$ with disambiguation symbols.** $L$ reads phones and writes words, with one path per pronunciation and a loop back to the start after each word. Determinization needs every input string to have one output, and it needs the output to be known after a bounded delay. Two cases break this. *Homophones*, such as "red" and "read" in the past tense, have the same phone string with two outputs. A pronunciation that is a *prefix* of another one leaves the decoder unable to tell where the word ends. So each such pronunciation gets a distinct symbol #1, #2, ... at its end. $L$ also passes #0 through, with a self-loop.
3. **Combine $L$ and $G$:** $LG = \min(\det(L \circ G))$. After determinization, the words that start with the same phones share one path until the phones differ, so the lexicon becomes a prefix tree with the language model costs pushed toward the root. Minimization then shares the common suffixes.
4. **Add the context:** $CLG = \min(\det(C \circ LG))$. $C$ passes the disambiguation symbols through.
5. **Add the HMMs:** compose with $H'$, which is $H$ without the self-loops of the HMM states, determinize, replace the disambiguation symbols by $\varepsilon$, minimize, and add the self-loops back. Kaldi writes this as $HCLG = \mathrm{asl}(\min(\mathrm{rds}(\det(H' \circ \min(\det(C \circ \min(\det(L \circ G))))))))$.
6. **Push the weights.** Mohri, Pereira and Riley 2002 push the weights of the network so that costs appear as early as possible, which helps pruning. Kaldi does not push. Instead it uses operations that keep the graph stochastic if $G$ was stochastic, so that the costs are already well placed.

**Why it is correct.** Composition gives exactly the relation $H \circ C \circ L \circ G$: a sequence of HMM states maps to a word sequence with the cost of the best way to explain it. Determinization and minimization in the tropical semiring keep, for every input string, its output and its smallest cost. So the optimized graph gives the same best cost to every pair of an HMM state sequence and a word sequence as the plain composition. The disambiguation symbols change the input alphabet, and removing them in step 5 maps the graph back to the original input. After that step the graph is no longer guaranteed to be deterministic, but it stays small.

**Cost.** Each composition takes time proportional to the number of states and arcs that it reaches, which is at most the product of the sizes of its arguments. Determinization can make a machine exponentially larger in the worst case ([determinization blowup](/determinization-blowup-lower-bound/)), but on speech models it usually makes the graph smaller, because it removes redundant paths. Minimization runs in $O(e \log n)$ time on a deterministic machine with $n$ states and $e$ arcs, as in [Hopcroft's algorithm](/hopcroft-minimization/).

## Classic examples

**A tiny $L \circ G$.** The lexicon has four words: "red" (r eh d), "read" (r eh d), "rat" (r ae t) and "at" (ae t). The grammar $G$ is a word loop with the unigram costs 1.2, 1.6, 0.9 and 2.3. In $L \circ G$ each word is a path from the start back to the start, with the word and its cost on the first arc.

- Without disambiguation symbols, $L \circ G$ has 8 states and 11 arcs. The phone string "r eh d" has two outputs, so the transducer is not functional and has no deterministic equivalent. Determinization never ends: in a run of the subset construction, the queue passed 200 states and kept growing, because the pending output "red" or "read" can never be written.
- With #1 after "red" and #2 after "read", $L \circ G$ has 10 states and 13 arcs. Determinization gives 6 states and 9 arcs:

| arc | input : output / cost |
|---|---|
| start to A | r : ε / 0.9 |
| A to B | eh : ε / 0.3 |
| B to C | d : ε / 0 |
| C to start | #1 : red / 0 |
| C to start | #2 : read / 0.4 |
| A to D | ae : rat / 0 |
| D to start | t : ε / 0 |
| start to E | ae : at / 2.3 |
| E to start | t : ε / 0 |

The three words that start with "r" share one arc, and its cost is the smallest of their costs, 0.9. After "r eh", the cost $\min(1.2, 1.6) - 0.9 = 0.3$ is paid, and "read" pays the last 0.4 at #2. Every word keeps its cost: "red" is $0.9 + 0.3 + 0 + 0 = 1.2$ and "read" is $0.9 + 0.3 + 0.4 = 1.6$. The output "rat" moves to the arc "ae" from A, the first point where the word is certain. Minimization then merges the states D and E, which both have one arc "t : ε / 0" back to the start, and the graph has 5 states and 8 arcs.

**Large-vocabulary graphs.** In a full system, $G$ is a pruned trigram or 4-gram model and $C$ uses triphones whose HMM states are tied by a [decision tree](/phonetic-decision-tree-state-tying/). The determinized lexicon gives the same sharing as the prefix tree of a dynamic decoder, but here it is built once, together with the language model costs.

## Variations

- **Order of the steps.** Mohri, Pereira and Riley 2002 determinize after each composition, so that every intermediate machine stays small. Composing all four models first and then determinizing is correct but uses much more memory.
- **Dynamic composition.** Some decoders keep $HCL$ and $G$ apart and compose them during the search. This allows a large $G$ and a change of language model without a rebuild.
- **Weight pushing or stochasticity.** Pushing in the log semiring makes the graph stochastic, which helps beam pruning. Kaldi aims for the same property by keeping each step stochastic.
- **Graphs for end-to-end models.** CTC models use a token topology $T$ in place of $H$ and $C$, and the graph is $T \circ L \circ G$ or $T \circ G$ with word pieces.
- **Lattice generation.** Decoders that run on HCLG write state-level lattices that are then determinized to word lattices ([word lattice](/word-lattice/)).

## Pitfalls

- **Missing disambiguation symbols.** Without them, determinization of $L \circ G$ does not terminate, or it runs out of memory, as in the example.
- **Back-off arcs as true epsilons.** A determinization that removes epsilons would remove the back-off arcs of $G$ too, and $G$ would then no longer be determinizable in a useful size. Use #0.
- **Forgetting to remove the symbols.** The graph that the decoder uses must have no #k on its input, or the decoder must treat them as $\varepsilon$.
- **The log semiring in determinization.** Determinization in the log semiring adds the probabilities of paths with the same input and output. That is a different model from the Viterbi decoder, which takes the best path. Use the tropical semiring for the graph, unless you want sums.
- **Size.** The graph grows with the number of n-grams in $G$ times the number of context-dependent variants of each phone. Prune $G$ first, or compose on the fly.
- **Scales.** The acoustic scale and the language model weight are applied in the decoder. If the graph is built with scaled costs, they must not be applied a second time.

## Exercises

1. Show that without #1 and #2, the transducer $L \circ G$ of the example maps the input "r eh d" to two outputs, and explain why the subset construction for transducers then creates a new state each time "r eh d" is read again.
2. Add the word "re" (r eh) to the example lexicon. Which pronunciations now need a disambiguation symbol, and why?
3. Check that every word in the determinized table keeps its cost from $G$. Then compute, for each state, the smallest cost of a path back to the start, and show that it is 0 for every state except the start, where it is 0.9. What does weight pushing change in the table?
4. Explain why the self-loops of the HMM states are left out of $H$ during the construction and added at the end.
5. Show that replacing the disambiguation symbols by $\varepsilon$ does not change the relation between HMM state sequences and word sequences, and give a small case where the result is no longer deterministic.

## References
