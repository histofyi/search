from flask import Flask

import pandas as pd
from pandasql import sqldf


def create_app():
    app = Flask(__name__)
    app.tables = {}
    return app


app = create_app()


def load_core():
    core_df = pd.read_csv("data/core.csv", sep=",")
    return core_df



table_methods = {
    'core': load_core
}




@app.before_first_request
def load_data():
    """
    This is a function which loads the generated datasets which are used by the site.

    By loading them in here, we can reduce S3 calls and speed the app up significantly.
    """
    tables = ['core','authors','class_i_positions','class_i_peptide_positions']
    tables = ['core']
    for table in tables:
        app.tables[table] = table_methods[table]()




@app.route('/search/')
@app.route('/search')
def advanced_search_handler(api=False):
    empty_search = True
    core = app.tables['core']
    query = "select pdb_code from core where locus='hla-c' order by allele_slug,resolution"

    search_results = sqldf(query).to_dict()['pdb_code'].values()

    pdb_codes = [pdb_code for pdb_code in search_results]
    
    return pdb_codes






