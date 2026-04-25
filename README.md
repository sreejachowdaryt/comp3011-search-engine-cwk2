# COMP3011 Search Engine - Coursework 2

A command-line search engine that crawls, indexes, and searches the quotes.toscrape.com website. Built with Python as part of the COMP3011 Web Services and Web Data module at the University of Leeds.

---

## Project Overview

This tool works in three stages:

1. **Crawl** - visits every page of quotes.toscrape.com automatically
2. **Index** - builds an inverted index storing each word's frequency, position, and TF-IDF score across all pages
3. **Search** - lets the user find pages containing one or more search terms, ranked by relevance

---

## Project Structure

```bash
comp3011-search-engine-cwk2/
├── src/
│   ├── crawler.py      # Web crawler with 6-second politeness window
│   ├── indexer.py      # Inverted index builder with TF-IDF scoring
│   ├── search.py       # Query processing and ranked retrieval
│   └── main.py         # Command-line interface
├── tests/
│   ├── test_crawler.py
│   ├── test_indexer.py
│   ├── test_search.py
│   └── test_main.py
├── data/
│   └── index.json      # Pre-built index file
├── requirements.txt
└── README.md
```

---

## Dependencies 

- Python 3.12+
- requests
- beautifulsoup4
- pytest
- pytest-cov

---

## Installation 

**1. Clone the repository:**
```bash
git clone https://github.com/YOUR-USERNAME/comp3011-search-engine-cwk2.git
cd comp3011-search-engine-cwk2
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

---

## Usage

Run the search tool from the project root directory:

```bash
python -m src.main
```

### Available Commands (shell)


1. **build** - Crawls the website, builds the inverted index, and saves it to data/index.json.
Note: this takes approximately 5 minutes due to the mandatory 6-second politeness window between requests.

2. **load** - Loads a previously built index from disk. This is used to avoid re-crawling.

3. **print** - Displays the full index entry for a specific word, including frequency, positions, and TF-IDF score across all pages.

4. **find** - Searches the index for pages containing all query terms, ranked by TF-IDF score.

5. **quit** - Exits the search tool.

---

## Example Session

### Avaliable commands
Search Engine ready. Commands: build | load | print <word> | find <query> | quit               

### load commad
> load       
Index loaded from data/index.json (4295 words)

### print command

For single word print
> print nonsense 

Index entry for 'nonsense':         
  URL: https://quotes.toscrape.com/tag/life/page/1/         
    Frequency : 1          
    Positions : [490]          
    TF-IDF    : 0.006564        
  URL: https://quotes.toscrape.com/page/2/         
    Frequency : 1            
    Positions : [441]                    
    TF-IDF    : 0.005294                      
  URL: https://quotes.toscrape.com/tag/life/            
    Frequency : 1                
    Positions : [490]                    
    TF-IDF    : 0.006564                    
  URL: https://quotes.toscrape.com/tag/regrets/page/1/             
    Frequency : 1           
    Positions : [61]        
    TF-IDF    : 0.037583         
  URL: https://quotes.toscrape.com/tag/fantasy/page/1/       
    Frequency : 1        
    Positions : [12]         
    TF-IDF    : 0.06453         
  URL: https://quotes.toscrape.com/page/7/       
    Frequency : 1        
    Positions : [324]        
    TF-IDF    : 0.008124          
> 

For multi-word print 
> print nonsense crazy

Index entry for 'nonsense':                   
  URL: https://quotes.toscrape.com/tag/life/page/1/       
    Frequency : 1          
    Positions : [490]        
    TF-IDF    : 0.006564        
  URL: https://quotes.toscrape.com/page/2/        
    Frequency : 1        
    Positions : [441]       
    TF-IDF    : 0.005294             
  URL: https://quotes.toscrape.com/tag/life/      
    Frequency : 1          
    Positions : [490]         
    TF-IDF    : 0.006564          
  URL: https://quotes.toscrape.com/tag/regrets/page/1/        
    Frequency : 1         
    Positions : [61]         
    TF-IDF    : 0.037583         
  URL: https://quotes.toscrape.com/tag/fantasy/page/1/        
    Frequency : 1           
    Positions : [12]            
    TF-IDF    : 0.06453                    
  URL: https://quotes.toscrape.com/page/7/             
    Frequency : 1                
    Positions : [324]              
    TF-IDF    : 0.008124               

Index entry for 'crazy':                        
  URL: https://quotes.toscrape.com/tag/humor/page/1/         
    Frequency : 1        
    Positions : [172]           
    TF-IDF    : 0.01331         
  URL: https://quotes.toscrape.com/tag/humor/            
    Frequency : 1          
    Positions : [172]            
    TF-IDF    : 0.01331           
  URL: https://quotes.toscrape.com/page/8/               
    Frequency : 1           
    Positions : [37]              
    TF-IDF    : 0.012283          
> 

### find command

For single word query
> find indifference  

Found 11 page(s):
  1. https://quotes.toscrape.com/tag/indifference/page/1/  (score: 0.20337)
  2. https://quotes.toscrape.com/tag/opposite/page/1/  (score: 0.169475)
  3. https://quotes.toscrape.com/tag/apathy/page/1/  (score: 0.169475)
  4. https://quotes.toscrape.com/tag/activism/page/1/  (score: 0.169475)
  5. https://quotes.toscrape.com/tag/hate/page/1/  (score: 0.169475)
  6. https://quotes.toscrape.com/tag/philosophy/page/1/  (score: 0.126363)
  7. https://quotes.toscrape.com/tag/inspirational/  (score: 0.027972)
  8. https://quotes.toscrape.com/tag/inspirational/page/1/  (score: 0.027972)
  9. https://quotes.toscrape.com/page/2/  (score: 0.022299)
  10. https://quotes.toscrape.com/tag/love/page/1/  (score: 0.020261)
  11. https://quotes.toscrape.com/tag/love/  (score: 0.020261)
> 

For multi-word query
> find good friends

Found 34 page(s):
  1. https://quotes.toscrape.com/tag/contentment/page/1/  (score: 0.07584)
  2. https://quotes.toscrape.com/tag/good/page/1/  (score: 0.067315)
  3. https://quotes.toscrape.com/tag/aliteracy/page/1/  (score: 0.032755)
  4. https://quotes.toscrape.com/tag/friendship/page/1/  (score: 0.025149)
  5. https://quotes.toscrape.com/tag/friendship/  (score: 0.025149)
  6. https://quotes.toscrape.com/tag/classic/page/1/  (score: 0.025098)
  7. https://quotes.toscrape.com/tag/alcohol/page/1/  (score: 0.023568)
  8. https://quotes.toscrape.com/tag/friends/  (score: 0.023361)
  9. https://quotes.toscrape.com/tag/friends/page/1/  (score: 0.023361)
  10. https://quotes.toscrape.com/tag/integrity/page/1/  (score: 0.023007)
  11. https://quotes.toscrape.com/tag/music/page/1/  (score: 0.022214)
  12. https://quotes.toscrape.com/tag/books/  (score: 0.017473)
  13. https://quotes.toscrape.com/tag/books/page/1/  (score: 0.017473)
  14. https://quotes.toscrape.com/tag/attributed-no-source/page/1/  (score: 0.01624)
  15. https://quotes.toscrape.com/tag/life/  (score: 0.012896)
  16. https://quotes.toscrape.com/tag/life/page/1/  (score: 0.012896)
  17. https://quotes.toscrape.com/tag/writing/page/1/  (score: 0.012388)
  18. https://quotes.toscrape.com/tag/heartbreak/page/1/  (score: 0.011189)
  19. https://quotes.toscrape.com/tag/sisters/page/1/  (score: 0.011189)
  20. https://quotes.toscrape.com/page/2/  (score: 0.011113)
  21. https://quotes.toscrape.com/page/7/  (score: 0.008634)
  22. https://quotes.toscrape.com/page/6/  (score: 0.008084)
  23. https://quotes.toscrape.com/page/1/  (score: 0.00671)
  24. https://quotes.toscrape.com/  (score: 0.00671)
  25. https://quotes.toscrape.com/tag/humor/  (score: 0.006464)
  26. https://quotes.toscrape.com/tag/humor/page/1/  (score: 0.006464)
  27. https://quotes.toscrape.com/page/3/  (score: 0.005701)
  28. https://quotes.toscrape.com/tag/inspirational/page/1/  (score: 0.005541)
  29. https://quotes.toscrape.com/tag/inspirational/  (score: 0.005541)
  30. https://quotes.toscrape.com/page/9/  (score: 0.004918)
  31. https://quotes.toscrape.com/author/George-Eliot  (score: 0.004668)
  32. https://quotes.toscrape.com/tag/love/  (score: 0.004336)
  33. https://quotes.toscrape.com/tag/love/page/1/  (score: 0.004336)
  34. https://quotes.toscrape.com/author/J-K-Rowling  (score: 0.002876)
> 

### quit command
> quit
Goodbye!

---

## Edge Cases

### When index is not loaded 
> print good       
No index loaded. Use 'build' or 'load' first.
> 

### Unknown command
> search love        
Unknown command: 'search'. Try: build | load | print | find | quit
>

### Empty query for print 
> print         
Usage: print <word> [word2] [word3]...
>

### Empty query for find 
> find        
Usage: find <query>
>

### non-existent word print 
> print thisisnotaword         
'thisisnotaword' not found in index.
>

### non-existent word find 
> find thisisnotaword           
'thisisnotaword' not found in index.
> 

### Case insensitivity 
All words lowercase 
> find crazy

Found 3 page(s):
  1. https://quotes.toscrape.com/tag/humor/page/1/  (score: 0.01331)
  2. https://quotes.toscrape.com/tag/humor/  (score: 0.01331)
  3. https://quotes.toscrape.com/page/8/  (score: 0.012283)
> 

All words uppercase
> find CRAZY

Found 3 page(s):
  1. https://quotes.toscrape.com/tag/humor/page/1/  (score: 0.01331)
  2. https://quotes.toscrape.com/tag/humor/  (score: 0.01331)
  3. https://quotes.toscrape.com/page/8/  (score: 0.012283)
>

First word uppercase
> find Crazy

Found 3 page(s):
  1. https://quotes.toscrape.com/tag/humor/page/1/  (score: 0.01331)
  2. https://quotes.toscrape.com/tag/humor/  (score: 0.01331)
  3. https://quotes.toscrape.com/page/8/  (score: 0.012283)
> 

Mix of uppercase and lowercase in the word 
> find CrAzY

Found 3 page(s):
  1. https://quotes.toscrape.com/tag/humor/page/1/  (score: 0.01331)
  2. https://quotes.toscrape.com/tag/humor/  (score: 0.01331)
  3. https://quotes.toscrape.com/page/8/  (score: 0.012283)
> 

### AND logic -> 0
> find best friends forever          
No pages found containing all search terms.
> 

This shows that there is no single page that contains all the 3 words therefore find

--- 

## Architecture and Design Decisions 

### Inverted Index Structure
```json
{
  "word": {
    "https://example.com/page1": {
      "frequency": 3,
      "positions": [12, 47, 103],
      "tf_idf": 0.008633
    }
  }
}
```

Each word maps to the pages it appears on, with frequency, character positions, and a TF-IDF relevance score. This structure allows O(1) word lookup and efficient multi-word AND queries.

### TF-IDF Ranking
Results are ranked using TF-IDF (Term Frequency-Inverse Document Frequency):
- **TF** = how often the word appears in a page / total words in that page
- **IDF** = log(total pages / pages containing the word)

Words that are rare across the site but frequent on a specific page score highest, pushing the most relevant results to the top.

### Storage
The index is saved as JSON for human readability and easy inspection. It is loaded entirely into memory for fast query processing.

---

## Testing

Run the full test suite:
```bash
pytest tests/ -v
```

Run with coverage report:
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Test Coverage
| File | Coverage |
|---|---|
| crawler.py | 97% |
| indexer.py | 100% |
| search.py | 91% |
| main.py | 91% |
| **Total** | **94%** |

### Testing Strategy
- **Crawler tests** — use mocked HTTP responses so tests run instantly without hitting the real website
- **Indexer tests** — verify frequency counts, positions, case insensitivity, and TF-IDF scores
- **Search tests** — cover single/multi-word queries, empty queries, missing words, and ranking order
- **Main tests** — simulate user input to test all CLI commands and edge cases

---

## Politeness

The crawler observes a mandatory **6-second delay** between every HTTP request, as required by the assignment brief and good web crawling practice.

---

## Gen AI Declaration 
This project was completed with the assistance of Claude (claude.ai) as part of a Green Category assessment where GenAI use is permitted and encouraged.

### Tools Used
- **Claude (claude.ai)** — Used throughout the development process

### How GenAI Was Used
- Explaining Python libraries (BeautifulSoup API, requests, unittest.mock)
- Suggesting project structure and file organisation
- Writing boilerplate code for crawler, indexer, search, and CLI modules
- Helping design the test suite structure and suggesting edge cases to cover
- Debugging module import errors (missing `__init__.py` files)
- Explaining concepts such as inverted indices and TF-IDF scoring

### Critical Reflection
- **Where it helped:** GenAI significantly sped up boilerplate code writing and helped explain unfamiliar library APIs. Understanding the TF-IDF concept was made much faster through AI explanation.
- **Where it hindered:** The initial code provided by GenAI assumed a flat project structure and missed the `__init__.py` files needed for Python package imports — this caused a `ModuleNotFoundError` that required manual debugging and fixing.
- **Code quality:** Every line of AI-generated code was reviewed, tested, and understood before being included. The TF-IDF scoring logic was verified manually against the formula.
- **Learning impact:** Using GenAI helped accelerate development but I was still required to debug, adapt, justify every design decision, and demonstrate full understanding of the implementation.

### Declaration
I confirm that:
- All GenAI usage has been declared above
- I understand every line of code in this submission
- I can explain and justify all design decisions
- GenAI use complies with the University of Leeds academic integrity guidelines for this Green Category assessment

---