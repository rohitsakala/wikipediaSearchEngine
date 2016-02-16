# Wikipedia Search Engine

## Run

* bash commands
* python query.py

type the query and press enter and see the top most 10 documents calculated using tf-idf.

# Query Example

* sachin
* t:sachin b:cricket ( t - title , b - body )

- Results are shown in less than 1 second.
- To change wiki dump change the path inside commands file.

## Description

-This project generates a sorted indexer for the dump specified. It is optimized by compression techniques. Given a dump, it will create the inverted index file in Index/ folder, create a tree of indexers in Split/ folder for the inverted index and tree in Title/ for title-docID mappings file. Inverted index and title mapping file can be found in Index/ folder. 

- Posting list contains the count of that term in title, body, infobox, references, external links and categories.

- T - Title
- X - body
- I - Infobox
- C - Categories
- L - External Links
- R - References

## Email

rohitsakala@gmail.com


