# Website Report Demo

Public version of the work I did building a website report at Sunbound during the summer of 2022. Due to the private nature of the underlying SQL database, as well as my desire to highlight parts of the report that I was the primary contributor to, numerous modifications were made in compiling this repository. 

## Modification

When making changes putting this repository together, my general philosophy was as follows:
* Removing files that I was not the primary (>90%) contributor to
* Removing files that could not be decoupled from SQL without completely cannibalizing the code
* Perserving the original structure and functionality of the report as much as possible
* Protecting Sunbound's data by thououghly randomizing all underlying numbers and writing them to static files to circumvent SQL

As a result of the randomization, numbers may not sum evenly across different parts of the report. 

## General Overview

The goal of this project is to understand how traffic flows through the Sunbound website.

## Usage

### Running

From the top level directory `python website-report.py`.

Running the script with no arguments will write the "main" report to `static/file.html`

Command line flags have been removed from this version of the report, as there is no way to write to S3. 

## Files
`website-report.py` — Processes flags that control how report is generated, behavior described above. 

`app/main.py` — Performs preliminary data processing, segmenting hits, unique users and form submissions by category and landing page. Invokes functions from `modules/*` in main() to write specific portions of the website. 

`app/modules/blog.py` — Tracks performance of recent blog posts. User specifys how many posts (default is 5), displays views and unique users for the top posts in the last month. 

`app/modules/transformations.py` — Unused in this version. Transforms data from initial SQL query. Categorizes all hits as seo, info, lead, legal, or job. Merges the initial ad campaign with all of a users traffic.

`app/modules/form_attrition.py` — Tracks form attrition, displayed in the form attrition section of the website. Displays starters and submitters for all Sunbound forms. 

`app/modules/graph_detail.py` — Transforms results into format suitable for d3 graphing in area_graphs.js, intiializes and formats `app/templates/_graph_detail.html`

`app/modules/header.py` — Creates header section of website, get timestamp of most recent row in data and the current timestamp, formats the html section. 

`app/modules/queries.py` — Methods for formatting query templates and querying the Sunbound Big Query database. 

`app/modules/top_graphs.py` — Writes top section of website, containing topline hits, users, and forms data from the past 2 weeks. Formats data for d3 to draw graphs of each of the categories. 

`app/modules/utils.py` — Contains variety of \<5 line helper functions that are invoked multiple times. 

`app/sql_queries/campaigns.json` - contains list of campaigns normally calculated in `app/modules/transformations.py`

`app/sql_queries/*_results.json` - contains the randomized results dictionaries normally calculated in `app/modules/transformations.py`

`app/sql_queries/blog_data.json` - contains the randomized data normally calculated in `app/modules/blog.py`

`app/sql_queries/top_stats.csv` — Static, randomized results from top_stats.sql query, report configured to read from this file to circumvent the private SQL database.

`app/templates/index.html` — Main HTML template, other templates written to it using Jinja after being formatted in Python.

`app/templates/*` — Template files correspond to their similarly named .py file in modules. Each contains the HTML template for its respective portion of the website. 

`static/main.css` — CSS file for the page, needs to be written to S3.

`static/main.js` — Contains the JavaScript functions that convert the timestamps displayed on the top of the page into human readable format: "Month DD at HH:MM" needs to be written to S3.

`static/graphs.js` — Draws the line charts at the top of the page. 

`static/area_graphs.js` — Draws the area-graphs in the middle of the page.

### Outputs

`static/index.html`, a .html webpage containing the final report

## Installation

### Environment

- Create a virtual environment `python -m venv venv`
- Activate it, then install requirements `pip install -r requirements.txt`

## Development

### Testing

Run unit tests with `python -m unittest -v` 
* Removed all tests that depended on SQL queries or pre-processed data
* Added new tests for static data

### Style/Linting

Use the [flake8](https://flake8.pycqa.org/en/latest/#) python linter. The flake8 styleguide is [here](https://flake8.pycqa.org/en/latest/internal/writing-code.html).

Sunbound's styleguide has only one conflict with the above, which is we prefer 2 tab spaces. Further information on configuration is available [here](https://flake8.pycqa.org/en/latest/user/configuration.html#)

invocation is simply `flake8` in the root directory. Further invocation options are found [here](https://flake8.pycqa.org/en/latest/user/invocation.html)

### Documenting

Follow [google style docstring conventions](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) for module level functions

### Reflection

Reflecting on my work in this project, I initially attempted to use a single SQL query to get all of the data I would need to compile the report. As a result, I ended up doing a lot more work in Python than is ideal. Looking back, if I could do this project over I would use more targeted queries for each of the sections, which would have reduced the processing that had to be done in Python. Many of the less than ideal style choices made later on were a direct result of this early strategic misstep.

### Resources

I'd like to thank Python How for their CSS template, which I used as the basis for my own in this project. Additionally, I'd like to thank Shahpar Khan for his guide on how to use d3. I modified his guide for the d3 graphs. Finally, I want to credit Louise Moxy for the guide on area graphs in d3. 
