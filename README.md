[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6108108.svg)](https://doi.org/10.5281/zenodo.6108108)

This repository collects the supplementary materials to the article titled "**Ontology Reuse: the Real Test of Ontological Design**", published in the proceedings of the SOMET 2022 conference, [Frontiers in Artificial Intelligence and Applications vol. 355](https://ebooks.iospress.nl/volumearticle/60841). A preprint version of the article can be accessed ([here](https://arxiv.org/abs/2205.02892)).

## How to run this?
The code in this repo consists of mostly Jupyter notebooks and SPARQL queries. For the former, you will need to set up a Python environment using the attached `requirements.txt` file. We used Python 3.9 on Linux. Running this on Windows will most likely fail.

In the subdirectories, additional `README.md` files explain the sequence in which the files should be run and how to set up the triple store. In our experiments, we used [Blazegraph](https://blazegraph.com/) due to its high performance on large KBs, but please do note that it is currently unmaintained. It may be possible to replicate the queries using other triple stores, e.g., Apache Jena.

## Directory structure
In the subdirectories you will find the code used to perform the analyses, as well as the results and (in some cases) suggested patches.

- `obo/` – analysis of [OBO Foundry](https://obofoundry.org/) ontologies
    - `obo/1_rare_props` – rarely used properties
    - `obo/2_prop_values` – properties with inconsistent value types
    - `obo/3_cross_refs` – cross-ontology references
    - `obo/summary` – summary of the identified issues
- `cso/` – analysis of the [Computer Science Ontology](https://cso.kmi.open.ac.uk/home)
    - `cso/1_synonym_structure` – CSO's structure transformation demonstrated in the paper
    - `cso/2_ext_ref_consistency` – externally-checked consistency of references to DBpedia
    - `cso/3_missing_refs` – missing references to corresponding KBs
    - `cso/4_refs_reasoning` – logically inconsistent external references
    - `cso/5_intra_ref_consistency` – intra-cluster inconsistencies in external references
    - `cso/6_conflation` – term conflation in clusters
    - `cso/summary` – summary of the identified issues

## Reproducibility
We attempted to describe the experiment well enough, so that interested researchers can reproduce them in the future. However, in case of any unclear documentation or other issues, we will be happy to help. Feel free to contact us, contact details are in the paper.

## License
The materials in this repository are licensed under the MIT License. You can cite this code using this DOI: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6108108.svg)](https://doi.org/10.5281/zenodo.6108108)


## Authors
Piotr Sowiński, Katarzyna Wasielewska-Michniewska, Maria Ganzha, Marcin Paprzycki
