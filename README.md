## General Setup Instructions
Note that the following are descriptions of the scripts/code we ran to build our entire pipeline. To use and see the results of our pipeline, please access our service at: https://new-journal-theta.vercel.app/, or refer to this github repo to host locally: https://github.com/skylarrwang/new-journal-archive.

To replicate the construction of our pipeline, follow the instructions below:

First, setup your conda environment by running `pip install -r requirements.txt`.

Second, create a `.env` file and add API keys (or contact Alex and Skylar for access to Gemini / Supabase / Qdrant keys, if necessary). Here are the necessary key fields:

```Python
OPENAI_API_KEY=

QDRANT_API_KEY=
QDRANT_CLOUD_ID=
QDRANT_CLOUD_URL=

SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_PWD=

GEMINI_API_KEY=
```
## Detailed Pipeline Instructions
#### Downloading PDFs
`Issuu_downloader.py` is the script that we used to download all of the TNJ PDFs off of the ISSUU archive, but you won’t be able to run it yourself because you need the login information for ISSUU, which is private. Please contact Alex at (alex.moore@yale.edu) if interested in scraping ISSUU archive!

#### Processing PDFs and OCR
The `/pipeline/` folder contains the key processing scripts that convert the archive of PDFs into chunks. To test it, you can first run `process_magazine.py` on a PDF of TNJ (test PDFs can be found in `sample_data` folder). This will transcribe it into a .md file with lots of useful metadata extracted into headers. Next, you can run `process_transcription.py` on the .md file, which will get rid of advertisements in the text. Then, you can run `split_articles.py`, which will take the .md file and create a bunch of new files where each file corresponds to a single article in the .md file, including distinct files for the masthead (list of staff) and table of contents. Finally, run `split_into_chunks.py` on the directory of article files to divide each article into chunks and compile all of the resulting chunks into a single .json file. 

#### Pre-processing for meta-data organization
Other relevant processing scripts and data are in the `/other_preprocessing/` folder. The `all_links.csv` file contains links to each of the TNJ issue PDFs in a Google Drive folder, which we needed in order to embed the PDFs on the website. The extract_authors.py script scrapes the entire `all_article_chunks.json` for all of the author names, eliminates bad/useless names, and combines different versions of the same name into a single entity for better use in searching. Finally, `integrate_links.py` will take `all_links.csv` and put the correct issue link in the metadata for each chunk in `all_article_chunks.json`, based on the volume and issue number metadata contained in the chunk.

#### Accessing Chunks
The `all_article_chunks.json` contains the complete list of chunks with metadata.

#### Computing Vectors
We've already computed all the vectors for you and associated metadata, which are included in the json file called `all_article_chunks.json`. To recompute/replicate these computations, run the scripts in the notebook found in: `chunking/compute_embeddings.ipynb`

#### Vector Database Insertion + Querying
To insert items into the vector database, cd into `vectorDB` and run `python create_collection.py`
