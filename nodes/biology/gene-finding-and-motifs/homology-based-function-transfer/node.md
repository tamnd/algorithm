---
tag: 2Z97VR
kind: technique
slug: homology-based-function-transfer
name: Homology-based function transfer
aliases:
- annotation transfer by homology
area: biology/gene-finding-and-motifs
level: core
summary: Give a new gene the function of its best similar characterized gene, with thresholds of identity and coverage to limit error spread.
prereqs: [blast, e-value]
see_also: [genome-annotation, profile-hmm, hmmer, local-alignment, smith-waterman, substitution-matrix, multiple-sequence-alignment, comparative-gene-finding]
sources:
  - paper: doi:10.1371/journal.pcbi.1000605
    title: Alexandra M. Schnoes, Shoshana D. Brown, Igor Dodevski and Patricia C. Babbitt, Annotation error in public databases, misannotation of molecular function in enzyme superfamilies, PLoS Computational Biology 5(12), 2009
    locator: article e1000605; misannotation in UniProtKB/Swiss-Prot, GenBank NR, UniProtKB/TrEMBL and KEGG for 37 families of six enzyme superfamilies, and overprediction of function as the main cause
  - paper: doi:10.1038/nrg3174
    title: Mark Yandell and Daniel Ence, A beginner's guide to eukaryotic genome annotation, Nature Reviews Genetics 13(5), 2012
    locator: pp. 329 to 342; functional annotation as the last stage of a genome annotation pipeline
---

Homology-based function transfer gives a newly found gene the function of a similar gene whose function is already known, on the assumption that genes with a common ancestor usually keep the same function. It is the main way to assign functions in [genome annotation](/genome-annotation/), because only a small part of all known proteins has been studied in the laboratory. The technique is a heuristic: similarity is evidence of common ancestry, and common ancestry makes a common function likely, but not certain. Thresholds on the [E-value](/e-value/), the identity and the alignment coverage, and a preference for experimentally characterized sources, keep the error rate down; without them, wrong labels spread from one database entry to the next.

## In plain words

Most new genes have never been studied. But many of them look like a gene that someone has studied, in another species. If the two proteins are alike along most of their length, they very likely came from one ancestral gene, and very likely do the same job. So we copy the label of the known gene onto the new one. The risk is that the copy is wrong: the two genes may have changed their jobs after they separated, or the "known" label may itself be a copy of a copy that nobody checked. Good practice is to copy only from genes with real experimental evidence, only when the match is strong and covers both proteins almost fully, and to record where every label came from.

## When it applies

- **The query has a clear homolog.** A local alignment search ([BLAST](/blast/), or a [profile HMM](/profile-hmm/) search with [HMMER](/hmmer/) for distant relations) finds a hit with a small E-value. The E-value says that the similarity is unlikely by chance, which is evidence of common ancestry. It does not measure how close the functions are.
- **The match covers both proteins.** Many proteins are built from several domains. A hit on one shared domain says that the query has that domain, not that it has the whole function of the hit. Coverage of most of both sequences is the usual condition for transferring a full name.
- **The identity is high enough for the kind of label.** Broad labels (a domain, a fold, "kinase") survive at low identity. Specific labels (the exact substrate, the EC number to the last digit) need high identity. A common rule of thumb in annotation is that specific enzyme functions are reliable to transfer only well above 40 percent identity over the full length, and that below about 30 percent even the structural similarity becomes uncertain; the exact values depend on the protein family and on the study.
- **The source label has evidence.** A label from an experiment on the protein itself is a good source; a label that was itself assigned by similarity is not.

## The template

The query $q$ is a protein (or a gene that translates into one), and $D$ is a database of proteins with function labels and evidence codes.

```pseudo id=main
TRANSFER-FUNCTION(q, D, e_max, i_min, c_min)
L1  H ← the hits of q in D, found by a local alignment search or a profile HMM search
L2  keep the hits h with E(h) ≤ e_max, identity(h) ≥ i_min, and coverage of q and of the subject ≥ c_min
L3  keep the hits whose label comes from an experiment on that protein
L4  if no hit is left then
L5      return only the labels of the protein families and domains found in q, with their evidence
L6  h* ← the kept hit with the best score
L7  if q is not the best hit of h* when h* is searched back against the genome of q then
L8      mark the label as a possible paralog transfer
L9  return the label of h*, the hit, its scores and its evidence, as the record of the transfer
```

Lines L2 and L3 are the filters that prevent most errors. Line L5 is the fall-back: a protein with no close characterized homolog still gets the labels of its families, at the broad level that families support. Lines L7 and L8 apply a reciprocal best hit check: if the query and the hit are each other's best match between the two genomes, they are likely orthologs, which are more likely than paralogs to share a function.

The output is a label with a trail of evidence, not a bare label. The trail makes it possible to remove a label later when its source is corrected.

## Classic examples

**A filtered choice.** A query protein of 400 residues gives four hits:

| hit | identity | coverage (query, subject) | E-value | label | evidence |
|---|---|---|---|---|---|
| P1 | 92% | 98%, 97% | 1e-180 | uncharacterized protein | by similarity |
| P2 | 61% | 95%, 96% | 1e-120 | glucokinase | experiment |
| P3 | 45% | 40%, 35% | 1e-30 | hexokinase, with a second regulatory domain | experiment |
| P4 | 28% | 90%, 88% | 1e-8 | ATP-binding protein | by similarity |

With $e_{\max} = 10^{-10}$, $i_{\min} = 40$ percent and $c_{\min} = 80$ percent, line L2 keeps P1 and P2 (P3 fails on coverage and P4 on both the E-value and the identity). Line L3 removes P1, whose label is itself a transfer and says nothing. The query gets the label of P2, with P2 as its source. A rule that takes the best hit only would have chosen P1 and given the query no function; a rule that takes the best hit with a name would have chosen P1 or P3, and P3 describes a protein with a domain that the query does not have.

**Error spread.** Suppose that each transfer from an entry that was itself labeled by transfer is wrong with probability 0.1, independently. A label that has passed through three such steps is right with probability $0.9^3 = 0.729$. This is a toy model, but it shows why line L3 insists on experimental sources: errors in a chain multiply.

**Measured misannotation.** Schnoes, Brown, Dodevski and Babbitt (2009) checked 37 well-characterized families from six enzyme superfamilies in four databases. Swiss-Prot, which is curated, had misannotation levels near 0 percent for most families. GenBank NR, TrEMBL and KEGG had similar, much higher levels, between 5 and 63 percent on average across the six superfamilies, and for 10 of the 37 families the level was above 80 percent in at least one database. The level in NR grew from 1993 to 2005. Most errors were overpredictions: a label more specific than the evidence supports. These are measurements on the data of that study.

**Pipelines.** In [genome annotation](/genome-annotation/) pipelines, the predicted proteins are searched against curated protein sets and against protein family databases built from profile HMMs. The names come from the best close homologs, and the domains and Gene Ontology terms come from the families.

## Variations

- **Orthology first.** Build ortholog groups between many genomes, by reciprocal best hits or by tree-based methods, and transfer only within an ortholog group. This reduces the paralog errors of plain best hits.
- **Tree-based transfer.** Build a [multiple alignment](/multiple-sequence-alignment/) and a gene tree of the family, place the query in it, and transfer the label of its closest characterized relatives, with the duplication events taken into account.
- **Family and domain models.** Profile HMMs of protein families give labels at the family level, with thresholds set per family by its curators. They find distant homologs that a pairwise search misses, but they cannot tell apart subfamilies with different substrates unless the database has separate models for them.
- **Function terms with confidence.** Instead of one name, transfer a set of Gene Ontology terms, each with a score from the identity, the coverage and the number of agreeing hits.
- **Active-site checks.** For enzymes, check that the catalytic residues of the source are kept in the alignment. A protein that has lost them may have lost the activity, even at high identity.
- **Structure-based transfer.** Compare predicted structures instead of sequences. Structures stay similar longer than sequences, so this finds relations below the level that sequence search can see, with the same caveat that a common fold is not a common function.

## Pitfalls

- **Transferring from transfers.** A database entry labeled "by similarity" is not evidence. Following such entries turns one early error into many, as the measured misannotation levels show.
- **Partial matches.** A hit that covers one domain of a multi-domain protein does not carry the full function. Check the coverage of both sequences, not only of the query.
- **Paralogs.** After a gene duplication, one copy often takes a new function. The best hit in another genome may be the paralog with the other function. Reciprocal best hits and gene trees help.
- **Overprediction.** Give the most specific label that the evidence supports, not the most specific label in the source. "Kinase" is often right where "glucokinase" is not.
- **E-value is not function.** A very small E-value between long proteins can come from a shared domain alone, and the E-value depends on the size of the database. Use it to decide homology, then use identity, coverage and the domain structure to decide the label.
- **Low-complexity regions.** Regions such as long runs of one or two amino acids give strong but meaningless hits. Search tools mask them by default; do not turn the masking off.
- **No record of the source.** A label without its source cannot be checked or corrected when the source changes. Keep the hit, the scores and the version of the database.

## Exercises

1. In the table of the example, change the coverage of P3 to 85 and 83 percent. Which label does the template give, and is it the right one for the query? What extra check would catch the problem?
2. In the toy model of error spread, how many transfer steps can a label pass through before its probability of being right falls below one half, for an error rate of 0.1 per step?
3. Explain why a reciprocal best hit between two genomes can still be a pair of paralogs, using a gene that was lost in one genome after a duplication.
4. Two proteins of 300 residues share one domain of 100 residues with 70 percent identity and are unrelated elsewhere. Compute the identity and the coverage that a local alignment reports, and decide which labels can be transferred.
5. Design a score for a Gene Ontology term transferred from several hits that uses their identities, their coverages and their evidence codes, and say how it should behave when two hits disagree.

## References
