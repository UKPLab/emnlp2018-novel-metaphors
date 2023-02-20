# Weeding out Conventionalized Metaphors: A Corpus of Novel Metaphor Annotations

Code and data for the EMNLP 2018 paper "Weeding out Conventionalized Metaphors: A Corpus of Novel Metaphor Annotations" by Erik-Lân Do Dinh, Hannah Wieland, and Iryna Gurevych. Paper PDF available at ACL Anthology: (to appear)

Please use the following citation:
```
@inproceedings{do-dinh-etal-2018-weeding,
   title = "Weeding out Conventionalized Metaphors: A Corpus of Novel Metaphor Annotations",
   author = "Do Dinh, Erik-L{\^a}n  and
     Wieland, Hannah  and
     Gurevych, Iryna",
   booktitle = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing",
   month = oct # "-" # nov,
   year = "2018",
   address = "Brussels, Belgium",
   publisher = "Association for Computational Linguistics",
   url = "https://aclanthology.org/D18-1171",
   doi = "10.18653/v1/D18-1171",
   pages = "1412--1424",
}
```

> **Abstract:** We encounter metaphors every day, but only a few jump out on us and make us stumble. However, little effort has been devoted to investigating more novel metaphors in comparison to general metaphor detection efforts. We attribute this gap primarily to the lack of larger datasets that distinguish between conventionalized, i.e., very common, and novel metaphors. The goal of this paper is to alleviate this situation by introducing a crowdsourced novel metaphor annotation layer for an existing metaphor corpus. Further, we analyze our corpus and investigate correlations between novelty and features that are typically used in metaphor detection, such as concreteness ratings and more semantic features like the \emph{Potential for Metaphoricity}. Finally, we present a baseline approach to assess novelty in metaphors based on our annotations.

Contact person: Erik-Lân Do Dinh, dodinh@ukp.informatik.tu-darmstadt.de
* UKP Lab: https://www.ukp.tu-darmstadt.de/
* TU Darmstadt: https://www.tu-darmstadt.de/

For code license information, see LICENSE.txt. This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication.
For data license information, see annotation/LICENSE.txt

## Project structure

* `annotation/` -- contains annotations and scripts to add them to the VU Amsterdam Metaphor Corpus.
* `baseline/` -- contains baseline BiLSTM implementation for novelty regression
* `correlation/` -- contains correlation data extraction and experiments

