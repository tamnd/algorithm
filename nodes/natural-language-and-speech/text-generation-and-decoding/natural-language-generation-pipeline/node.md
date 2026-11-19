---
tag: 72KQWJ
kind: concept
slug: natural-language-generation-pipeline
name: Natural language generation pipeline
aliases:
- Reiter-Dale pipeline
area: natural-language-and-speech/text-generation-and-decoding
level: core
summary: The classic split of data-to-text generation into document planning, microplanning with referring expressions, and surface realization.
history:
  year: 1997
  people: [Ehud Reiter, Robert Dale]
  note: Reiter described the pipeline in 1994 as the consensus of the systems built so far. Reiter and Dale set it out in a journal article in 1997 and in their book of 2000.
prereqs: []
see_also: [incremental-algorithm-referring-expressions, rhetorical-structure-theory, context-free-grammar, automatic-summarization, encoder-decoder-model, language-model]
sources:
  - paper: doi:10.1017/S1351324997001502
    title: Ehud Reiter and Robert Dale, Building applied natural language generation systems, Natural Language Engineering 3(1), 1997, pages 57 to 87
    locator: the basic tasks of an applied generation system and their grouping into an architecture
  - book: isbn:9780521620369
    title: Ehud Reiter and Robert Dale, Building Natural Language Generation Systems, Cambridge University Press, Studies in Natural Language Processing, 2000
    locator: "Chapter 3 (The Architecture of a Natural Language Generation System)"
  - paper: doi:10.1613/jair.5477
    title: Albert Gatt and Emiel Krahmer, Survey of the State of the Art in Natural Language Generation, Core tasks, applications and evaluation, Journal of Artificial Intelligence Research 61, 2018, pages 65 to 170
    locator: "Section 3.1 (modular approaches) and Figure 3 (the classical three-stage architecture, after Reiter and Dale 2000)"
---

The natural language generation pipeline is the classic architecture of systems that turn data into text, such as a weather forecast written from the numbers of a weather model. It splits the work into three stages that run one after the other: document planning decides what to say and in what order, microplanning decides how to say it in words and sentences, and surface realization produces the grammatical text. Ehud Reiter and Robert Dale made it the standard description of applied generation systems in 1997 and in their book of 2000. It is an engineering design, not a theorem: it describes how many working systems are built, and Gatt and Krahmer (2018) call it the "consensus" architecture of the field, while noting that it has been contested.

## In plain words

Think of how a meteorologist writes a forecast. First she decides which facts matter today: the rain in the afternoon matters, the exact humidity does not. She puts them in order, the most important first. That is document planning.

Then she decides how to say each fact. Should two facts share one sentence? Should she say "heavy rain" or "downpours"? Should she write "the front" or repeat "the cold front from the west"? That is microplanning.

Last, she writes the sentences with correct grammar, word endings and punctuation. That is surface realization.

A program can do the same in three modules. Each module has one job and passes its result to the next one.

## The idea

The input is non-linguistic data and a communicative goal, for example a table of forecast values and the goal "inform the public about tomorrow's weather". The output is text. The three stages and their tasks, as described by Reiter and Dale (2000) and by Gatt and Krahmer (2018):

1. **Document planning** (also text planning, or macroplanning).
   - *Content determination*: choose the messages, the units of information to say, from the data.
   - *Document structuring*: order and group the messages, and mark the relations between them, such as contrast or cause. The result is a document plan, a tree with messages at its leaves.
2. **Microplanning** (also sentence planning).
   - *Lexicalization*: choose the words and syntactic structures for each message.
   - *Aggregation*: combine messages into sentences, for example "rain in the north" and "rain in the east" into "rain in the north and east".
   - *Referring expression generation*: choose how to name each entity, with a pronoun, a name or a description such as "the small dog". The [incremental algorithm](/incremental-algorithm-referring-expressions/) of Dale and Reiter (1995) does this step.
   The result is a text specification: a structure of phrase specifications, which fix the content words and the syntax but not the word forms.
3. **Surface realization** (also linguistic realization).
   - *Linguistic realization*: apply the grammar of the language, with agreement, word order, inflection and function words.
   - *Structure realization*: map the document structure to paragraphs and to the markup of the output format.

The 1997 article lists six basic tasks: content determination, discourse planning, sentence aggregation, lexicalization, referring expression generation and linguistic realization. The book groups them into the three stages above.

The main design choice is the one way flow. A module never asks a later module for help, which makes each module simple to write, test and replace. The cost is that some decisions need information from later stages: whether a message fits in one sentence depends on the words chosen, and the words depend on the length limit. Systems that need such feedback use revision, planning over several stages at once, or overgeneration followed by ranking. Gatt and Krahmer (2018, Section 3) describe these alternatives, and also note that the psycholinguistic model of speaking of Levelt has a similar split into stages.

## Examples

A small data-to-text example, with one row of forecast data: maximum temperature 18 degrees, wind from the southwest at 15 to 20 knots, rain from 14:00 to 18:00.

| stage | result |
|---|---|
| content determination | messages: Rain(afternoon), Wind(SW, 15-20), Temp(max 18); humidity left out |
| document structuring | order: Rain, Wind, Temp; a Sequence relation joins Wind and Temp |
| lexicalization | Rain(afternoon) becomes "rain in the afternoon"; Wind becomes "southwest winds of 15 to 20 knots" |
| aggregation | Wind and Temp share one sentence joined by "with" |
| referring expressions | nothing to do here, since each entity is named once; a longer text would say "it" for a second mention of the rain |
| linguistic realization | "Rain is expected in the afternoon. Southwest winds of 15 to 20 knots, with a maximum of 18 degrees." |

Real systems of this kind include weather forecast generators, which write marine and public forecasts from numerical weather models, and systems that write reports of sports games, financial results and medical data. A separate realizer library, such as SimpleNLG or the realizers built on functional unification grammars, often does the last stage.

## Where it is used

- **Data-to-text systems** in industry, where the content and the wording must be controlled and checked, such as weather, finance, sports and health reports.
- **As a vocabulary.** Even neural systems are described in its terms. Content selection, planning and realization are the names of stages in many neural data-to-text models, and the tasks of the pipeline are the core tasks in surveys such as Gatt and Krahmer (2018).
- **Comparison with end-to-end models.** An [encoder-decoder model](/encoder-decoder-model/) or a large [language model](/language-model/) maps the data to text in one network, with no explicit stages. This removes the hand-written rules but makes it harder to control what is said, and such models can state facts that are not in the data.
- **Text to text generation.** [Automatic summarization](/automatic-summarization/) shares the content selection and realization problems, with a text as input instead of data.

## References
