---
tag: JQQZ9A
kind: problem
slug: protein-fold-recognition
name: Protein fold recognition
aliases:
- Fold assignment
area: biology/structure-prediction
level: advanced
summary: Given a query sequence and a library of known structures, find the folds the query is likely to share, with an alignment, when no close homolog of known structure exists.
prereqs: [comparative-modeling, profile-hmm]
see_also: [protein-threading, i-tasser, sequence-profile-alignment, hmmer, position-specific-scoring-matrix, structure-alignment, protein-structure-prediction, alphafold]
sources:
  - paper: doi:10.1126/science.1853201
    title: James U. Bowie, Roland Luthy and David Eisenberg, A method to identify protein sequences that fold into a known three-dimensional structure, Science 253(5016), 1991, 164-170
    locator: the 3D profile method and its use to find sequences that fit a known fold
  - paper: doi:10.1038/358086a0
    title: David T. Jones, William R. Taylor and Janet M. Thornton, A new approach to protein fold recognition, Nature 358(6381), 1992, 86-89
    locator: fold recognition by threading through a library of folds
  - paper: doi:10.1006/jmbi.1999.2583
    title: David T. Jones, GenTHREADER, an efficient and reliable protein fold recognition method for genomic sequences, Journal of Molecular Biology 287(4), 1999, 797-815
    locator: the combination of sequence profile alignment, pair and solvation potentials, and a neural network that gives a confidence for each match
  - paper: doi:10.1093/bioinformatics/bti125
    title: Johannes Soding, Protein homology detection by HMM-HMM comparison, Bioinformatics 21(7), 2005, 951-960
    locator: the alignment of a profile HMM of the query with profile HMMs of the templates (HHsearch, the method of HHpred)
  - paper: doi:10.1093/protein/7.9.1059
    title: Richard H. Lathrop, The protein threading problem with sequence amino acid interaction preferences is NP-complete, Protein Engineering 7(9), 1994, 1059-1068
    locator: the NP-completeness of threading with variable-length loops and pairwise interactions
  - paper: doi:10.1093/protein/12.2.85
    title: Burkhard Rost, Twilight zone of protein sequence alignments, Protein Engineering 12(2), 1999, 85-94
    locator: the range of sequence identity where pairwise alignment no longer tells homologs apart
  - paper: doi:10.1093/nar/gkm251
    title: Sitao Wu and Yang Zhang, LOMETS, a local meta-threading-server for protein structure prediction, Nucleic Acids Research 35(10), 2007, 3375-3382
    locator: the combination of several threading programs in one meta-server
---

Protein fold recognition is the problem of finding, for a protein sequence with no close homolog of known structure, the known structures whose fold it shares. The answer is a ranked list of templates from a library such as the Protein Data Bank, each with an alignment of the query to the template and a measure of confidence. It exists because the number of folds is much smaller than the number of protein families: two proteins can share a fold even when their sequences have drifted into the twilight zone, where a sequence alignment alone no longer shows the relation (Rost 1999). A recognized template is the start of a [comparative model](/comparative-modeling/).

## In plain words

Many proteins whose letters look unrelated still fold into the same shape. Fold recognition tries to find that shared shape. We have a library of shapes we already know. For a new sequence, we ask each shape in the library: how well could this sequence sit in you?

To answer, a program lines up the new sequence with each shape and gives the fit a score. It looks at more than the letters: for example whether water-fearing letters land inside the shape, and whether the predicted helices and strands of the new sequence match those of the shape. The shapes with the best scores are the answer, together with a number that says how sure the program is.

## Definition

**Input.** A query sequence $a$ of length $n$, and a library $\mathcal{L}$ of template structures, each with its sequence and coordinates. Often the input also includes a [multiple sequence alignment](/multiple-sequence-alignment/) of homologs of the query, from which a profile is built.

**Output.** A ranked list of templates $T \in \mathcal{L}$, each with

- a score $\sigma(a, T)$, or better a calibrated confidence such as an E-value or a probability that $a$ and $T$ share a fold,
- an alignment of $a$ to $T$, which maps residues of the query to residues of the template.

**Correctness.** The ground truth is a fold classification of the structures, for example the fold or superfamily level of SCOP or CATH, or the structural similarity of the true structure of the query to the template, measured with [TM-score](/tm-score/) after a [structure alignment](/structure-alignment/). A method is judged by how often its top hits are correct at a fixed rate of false positives, and by the quality of its alignments. The query structure is unknown when the method runs, so the problem is a prediction problem.

**Levels of difficulty.** At the family level the query and the template are clear homologs. At the superfamily level they are distant homologs with low identity. At the fold level they share the arrangement of secondary structures but may not share an ancestor. Detection becomes harder at each level.

## Variants

- **Template detection.** Only the ranking of templates matters, for example to annotate a genome with folds.
- **Template alignment.** The alignment must also be accurate, because a model is built from it. A correct fold with a shifted alignment gives a poor model.
- **Domain-level recognition.** A long query has several domains, which may match different templates. The problem then includes the split into domains.
- **Novel fold.** The query has no template in the library. A good method should report low confidence for all templates, and the structure must come from template-free methods such as [ab initio folding](/ab-initio-protein-folding/).

## Examples

**Raw scores are not comparable.** Suppose a threading method gives a query the raw energies $-60$, $-40$ and $-25$ against templates B, A and C, with lower being better. For each template we also thread 1000 shuffled versions of the query, which keep its composition but destroy its order, and record the mean $\mu$ and the standard deviation $s$ of their energies:

| template | raw energy | shuffled $\mu$ | shuffled $s$ | $z = (E - \mu) / s$ |
|---|---|---|---|---|
| A | $-40$ | $-30$ | 5 | $-2.0$ |
| B | $-60$ | $-55$ | 10 | $-0.5$ |
| C | $-25$ | $-12$ | 4 | $-3.25$ |

By raw energy, template B ranks first. But B is a large template on which every sequence scores well; the real query is only half a standard deviation better than random. By $z$-score, C ranks first: the query fits C much better than its shuffled versions do. The numbers here are a toy, but the effect is the reason why fold recognition programs normalize their scores.

**Sequence identity is not enough.** A pair of proteins with 15% identity over 100 aligned residues can be true structural relatives or unrelated. The fraction of identical residues alone does not decide, so methods add profiles, predicted secondary structure and structural terms.

## Known algorithms

- **Profile search.** Build a profile of the query from its homologs and search the sequences of the library with it: PSI-BLAST with a [position-specific scoring matrix](/position-specific-scoring-matrix/), or [HMMER](/hmmer/) with a [profile HMM](/profile-hmm/). Each comparison is a dynamic program in $O(nm)$ time for a template of length $m$.
- **[Protein threading](/protein-threading/).** Fit the query to the core of each template and score the fit with environment and pair potentials (Bowie, Luthy and Eisenberg 1991; Jones, Taylor and Thornton 1992).
- **GenTHREADER** (Jones 1999). Align the query profile to each template, score the alignment with pair and solvation potentials, and feed these scores and the alignment length to a neural network that outputs a confidence for each template.
- **HMM-HMM comparison.** HHsearch, the method behind the HHpred server, builds a profile HMM for the query and for each template, with predicted and known secondary structure, and aligns the two HMMs (Soding 2005). The paper reports that it finds more remote homologs than profile-sequence search.
- **Meta-servers.** LOMETS (Wu and Zhang 2007) runs several threading programs and combines their top hits; [I-TASSER](/i-tasser/) starts from such hits.
- **Deep learning.** Predicted contacts and distances help to score alignments to templates, and end-to-end predictors such as [AlphaFold](/alphafold/) can use or ignore templates.

## Bounds

- **Threading with pair terms is NP-complete** (Lathrop 1994): finding the best alignment of a query to one template, with variable loop lengths and a pairwise contact energy, has no known polynomial algorithm. Exact methods use branch and bound or integer programming.
- **Profile alignment is polynomial.** Without pair terms, aligning a query of length $n$ to a template of length $m$ is a dynamic program in $O(nm)$ time, so scanning a library with total length $M$ costs $O(nM)$.
- **No method is complete.** Two proteins can share a fold by convergence, without a sequence signal. For such pairs no sequence-based method can be expected to find the relation, so recall at the fold level stays below one.

## Reductions

- **To protein threading.** Fold recognition over a library reduces to one threading problem per template, then a ranking of the normalized scores.
- **To profile-profile alignment.** In the HMM-HMM view, each template is a profile, and the problem becomes a library search with [profile alignment](/sequence-profile-alignment/).
- **To comparative modeling.** The output alignment to the best template is the input of [comparative modeling](/comparative-modeling/).

## Applications

- **Structure prediction.** Template-based modeling starts with fold recognition when the identity to the best template is low.
- **Function prediction.** A recognized fold suggests a function, a binding site or a catalytic mechanism, for example for proteins of unknown function in a new genome.
- **Evolution.** Fold-level matches link families that sequence search cannot connect, and so help to classify proteins into superfamilies.

## References
