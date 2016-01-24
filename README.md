# Wikipedia Search Engine

## Libraries Required

* python-stemmer
* python-unidecode
* nltk stopwords corpus

## Run

* ./commands

- To change wiki dump change the path inside commands file

## Description

-This project generates a sorted indexer for the dump specified. It is optimized by converting the number into hexadecimal format. It can further be optimized by compressing text by bz.compresser. Given a dump, it will output a file which will contain terms and its posting list. 

- Posting list contains the count of that term in title, body, infobox, references, external links and categories.



