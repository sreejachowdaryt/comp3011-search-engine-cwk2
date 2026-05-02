# COMP3011 Search Engine - Coursework 2

A command-line search engine that crawls, indexes, and searches the quotes.toscrape.com website. Built with Python as part of the COMP3011 Web Services and Web Data module at the University of Leeds.

---

## Project Overview

This tool works in three stages:

1. **Crawl** — visits every page of quotes.toscrape.com automatically, extracting only meaningful content (quotes, authors, tags)
2. **Index** — builds an inverted index storing each word's frequency, position, and TF-IDF score across all pages
3. **Search** — lets the user find pages containing one or more search terms, ranked by relevance with advanced query processing

---

## Project Structure

```bash
comp3011-search-engine-cwk2/
├── src/
│   ├── crawler.py      # Web crawler with 6-second politeness window
│   ├── indexer.py      # Inverted index builder with TF-IDF scoring
│   ├── search.py       # Query processing and ranked retrieval
│   └── main.py         # Command-line interface with benchmarking
├── tests/
│   ├── test_crawler.py
│   ├── test_indexer.py
│   ├── test_search.py
│   └── test_main.py
├── data/
│   └── index.json      # Pre-built index file
├── .github/
│   └── workflows/
│       └── test.yml    # GitHub Actions CI pipeline
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
git clone https://github.com/sreejachowdaryt/comp3011-search-engine-cwk2.git
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

### Avaliable Commands (shell)


1. **build** - Crawls the website, builds the inverted index, and saves it to `data/index.json`.
Note: this takes approximately 5 minutes due to the mandatory 6-second politeness window between requests.

> build

2. **load** - Loads a previously built index from disk. This is used to avoid re-crawling.

> load

3. **print \<word\> [word2] [word3]...** — Displays the full index entry for one or more words sequentially, including frequency, positions, and TF-IDF score across all pages.

> print indifference (single word print)
print good friends (multi-word print)

4. **find \<query\>** — Searches the index for pages containing query terms, ranked by TF-IDF score. Supports AND/OR Boolean operators, spell suggestions, and related terms.

> find indiffernece (single word query)
find good friends (multi-word query)
find love OR hate (OR logic)
find good AND friends (AND logic)

5. **quit** - Exits the search tool.

> quit

---

## Advanced Query Features 

### Boolean Operators
Operators must be **uppercase** following Boolean query syntax convention (same as Google and Elasticsearch). Lowercase `or`/`and` are treated as regular search terms.

> find love OR hate  → OR logic: pages containing either word
find love AND hate → AND logic: pages containing both words
find good friends → AND logic: default behaviour
find love or hate → AND logic: searches for "love", "or", "hate"
find love and hate → AND logic: searches for "love", "and", "hate"

### Spell correction 
When a word is not found, the closest match is suggested using edit distance:

> find freinds
'freinds' not found in index. Did you mean 'friends'?

> find loev freinds
'loev' not found in index. Did you mean 'love'?
'freinds' not found in index. Did you mean 'friends'?

### Related Terms
After a successful search, related terms are suggested using PMI (Pointwise Mutual Information) scoring — words that appear disproportionately often on the same pages as your query:

> find books
Related terms: book, written, lives, write, reading
Found 61 page(s)...

### Query Benchmarking 
All commands display execution time (execution time has minor changes during every new execution/run):

> find love OR hate
Found 56 page(s) in 0.0117s

> print indifference
Query completed in 0.0022s

---

## Example Session

### Avaliable commands
Search Engine ready. Commands: build | load | print <word> | find <query> | quit               

### 1. load 
> load       
Index loaded from data/index.json (4253 words)
Load completed in 0.0695s

### 2. print 

Print for single word
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
    Query completed in 0.0067s          
> 

Print for multiple words
> print nonsense crazy
first prints nonsense and then prints for crazy

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
    Query completed in 0.0019s                  
> 

### 3. find 

For single word query
> find indifference  
  Related terms: opposite, art, ugliness, heresy, apathy

Found 11 page(s) in 0.0059s:
  1. https://quotes.toscrape.com/tag/indifference/page/1/  (score: 0.20337)
  2. https://quotes.toscrape.com/tag/opposite/page/1/  (score: 0.169475)
  3. https://quotes.toscrape.com/tag/apathy/page/1/  (score: 0.169475)
  4. https://quotes.toscrape.com/tag/activism/page/1/  (score: 0.169475) ...
> 

For multi-word query
> find good friends
  Search mode: AND (pages containing all of: good, friends)
  Related terms: mess, decide, stay, lovers, actually

Found 19 page(s) in 0.0317s:
  1. https://quotes.toscrape.com/tag/contentment/page/1/  (score: 0.381029)
  2. https://quotes.toscrape.com/tag/friends/page/1/  (score: 0.084782)
  3. https://quotes.toscrape.com/tag/friends/  (score: 0.084782)
  4. https://quotes.toscrape.com/tag/friendship/page/1/  (score: 0.07721) ...
> 

Find for OR Boolean Operator
> find love OR hate
  Search mode: OR (pages containing any of: love, hate)
  Related terms: mess, decide, stay, lovers, actually

Found 56 page(s) in 0.0089s:
  1. https://quotes.toscrape.com/tag/women/page/1/  (score: 0.156766)
  2. https://quotes.toscrape.com/tag/romantic/page/1/  (score: 0.156766) ...
>

Find for AND Boolean Operator
> find love AND hate 
  Search mode: AND (pages containing all of: love, hate)
  Related terms: mess, decide, stay, lovers, actually

Found 19 page(s) in 0.0076s:
  1. https://quotes.toscrape.com/tag/humor/page/2/  (score: 0.154899)
  2. https://quotes.toscrape.com/tag/hate/page/1/  (score: 0.142493) ...
>

### quit 
> quit                
Goodbye!

---

## Edge Cases

### 1. Index not loaded 
> print good       
No index loaded. Use 'build' or 'load' first.
> 

### 2. Unknown command
> search love        
Unknown command: 'search'. Try: build | load | print | find | quit
>

### 3. Empty queries 
> print         
Usage: print <word> [word2] [word3]...
>

> find        
Usage: find <query>
>

### 4. non-existent word in index
> print thisisnotaaword
'thisisnotaaword' not found in index.
  Query completed in 0.0066s
> 
 
> find thisisnotaword
'thisisnotaword' not found in index.
  Query completed in 0.0104s
>  

### 5. Case insensitivity 
All words lowercase 
> find crazy
  Related terms: horrible, question, low, oh, beholder          

Found 3 page(s) in 0.0051s:                
  1. https://quotes.toscrape.com/tag/humor/page/1/  (score: 0.016792)     
  2. https://quotes.toscrape.com/tag/humor/  (score: 0.016792)       
  3. https://quotes.toscrape.com/page/8/  (score: 0.015018)       
>

All words uppercase
> find CRAZY
  Related terms: horrible, question, low, oh, beholder

Found 3 page(s) in 0.0058s:                
  1. https://quotes.toscrape.com/tag/humor/page/1/  (score: 0.016792)      
  2. https://quotes.toscrape.com/tag/humor/  (score: 0.016792)       
  3. https://quotes.toscrape.com/page/8/  (score: 0.015018)        
>

Mix of uppercase and lowercase in the word   
> find CrAzY       
  Related terms: horrible, question, low, oh, beholder          

Found 3 page(s) in 0.0049s:         
  1. https://quotes.toscrape.com/tag/humor/page/1/  (score: 0.016792)     
  2. https://quotes.toscrape.com/tag/humor/  (score: 0.016792)         
  3. https://quotes.toscrape.com/page/8/  (score: 0.015018)          
> 

### 6. Boolean Operator Case Sensitivity
AND logic -> 0 (Default)              
> find best friends forever         
  Search mode: AND (pages containing all of: best, friends, forever)      
No pages found containing search terms.       
  Query completed in 0.0000s        
> 
This shows that there is no single page that contains all the 3 words using the AND logic therefore find returns "No page found contaning all search terms" but the words exists individually in the index. 

OR Operator
> find love or hate      
  Search mode: AND (pages containing all of: love, or, hate)         
  Related terms: loves, aren, either, twice, onto        

Found 5 page(s) in 0.0060s:                  
  1. https://quotes.toscrape.com/tag/love/  (score: 0.07312)        
  2. https://quotes.toscrape.com/tag/love/page/1/  (score: 0.07312) ...    
>

AND Operator
> find love and hate            
  Search mode: AND (pages containing all of: love, and, hate)       
  Related terms: mess, decide, stay, lovers, actually           

Found 18 page(s) in 0.0065s:           
  1. https://quotes.toscrape.com/tag/activism/page/1/  (score: 0.153193)    
  2. https://quotes.toscrape.com/tag/indifference/page/1/  (score: 0.153193) ...     
>

### 7. Query Suggestions
Spell Correction
> find freinds    
'freinds' not found in index. Did you mean 'friends'?      
  Query completed in 0.0168s             
> 

> find loev freinds                
'loev' not found in index. Did you mean 'love'?                  
'freinds' not found in index. Did you mean 'friends'?               
  Query completed in 0.0394s                    
>

Related Terms                 
> find books                
  Related terms: book, written, lives, write, reading                   

Found 61 page(s) in 0.0142s:                 
>

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

Each word maps to the pages it appears on storing frequency, word position, and a TF-IDF relevance score. This structure allows O(1) word lookup and efficient multi-word AND/OR queries.

### Meaningful Content Extraction
The crawler extracts only quote text, author names, and tags - not navigation, footers, or boilerplate HTML. This significantly improves index quality and related term relevance.

### TF-IDF Ranking
Results are ranked using TF-IDF (Term Frequency-Inverse Document Frequency):
- **TF** = how often the word appears in a page / total words in that page
- **IDF** = log(total pages / pages containing the word)

Words that are rare across the site but frequent on a specific page score highest, pushing the most relevant results to the top.

### Boolean Query Syntax
Uppercase OR/AND operators follow industry-standard Boolean query syntax used by Google and Elasticsearch. This design decision means lowercase "or"/"and" are treated as regular search terms, which is both intuitive and consistent with professional search engine conventions.

### Related Terms using PMI
Related terms are discovered using Pointwise Mutual Information (PMI) scoring: PMI score = P(word | matching pages) / P(word | all pages)

Words that appear disproportionately often on matching pages compared to the overall index score highly — this naturally surfaces thematically related words without requiring a manually maintained stop words list.

### Storage
The index is saved as JSON for human readability and easy inspection. It is loaded entirely into memory for O(1) word lookup during queries.

### Query Benchmarking
All commands display execution time, demonstrating the efficiency of the in-memory index. Typical query times are under 0.02 seconds for a 4,000+ word index.

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
| File | Tests | Coverage |
|---|---|---|
| crawler.py | 17 | 98% |
| indexer.py | 13 | 100% |
| search.py | 52 | 96% |
| main.py | 18 | 87% |
| **Total** | **100** | **94%** |

### Testing Strategy
- **Crawler tests** — mocked HTTP responses so tests run instantly without hitting the real website, tests for `extract_page_content` with structured HTML
- **Indexer tests** — verify frequency counts, positions, case insensitivity, and TF-IDF scores
- **Search tests** — cover AND/OR logic, spell corrections, related terms, empty queries, missing words, ranking order, and Boolean operator detection
- **Main tests** — simulate user input to test all CLI commands, benchmarking, and edge cases

### Continuous Integration
GitHub Actions automatically runs the full test suite on every push to main:
```yaml
# .github/workflows/test.yml
pytest tests/ --cov=src --cov-fail-under=90
```

---

## Politeness

The crawler observes a mandatory **6-second delay** between every HTTP request, as required by the assignment brief and for good web crawling practice.

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
- Explaining concepts such as inverted indices, TF-IDF scoring, and PMI
- Suggesting advanced features such as Boolean operators and related terms

### Critical Reflection
- **Where it helped:** GenAI significantly sped up boilerplate code writing and helped explain unfamiliar library APIs. Understanding TF-IDF and PMI concepts was made much faster through AI explanation.
- **Where it hindered:** The initial code assumed a flat project structure and missed the `__init__.py` files needed for Python package imports — this caused a `ModuleNotFoundError` that required manual debugging. AI also initially suggested a stop words list for related terms filtering which was brittle — I replaced this with a mathematically principled PMI approach.
- **Iterative improvement:** The related terms feature went through multiple iterations — co-occurrence counting → TF-IDF averaging → PMI scoring. Each iteration was motivated by observing real output and identifying weaknesses, not by AI suggestion.
- **Code quality:** Every line of AI-generated code was reviewed, tested, and understood before being included. The TF-IDF and PMI logic was verified manually against the formulas.
- **Learning impact:** Using GenAI helped accelerate development but I was still required to debug, adapt, justify every design decision, and demonstrate full understanding of the implementation.

### Declaration
I confirm that:
- All GenAI usage has been declared above
- I understand every line of code in this submission
- I can explain and justify all design decisions
- GenAI use complies with the University of Leeds academic integrity guidelines for this Green Category assessment

---