# %%
from flask import Flask, request, jsonify
import requests
import json
import os
from metaphor_python import Metaphor
from data import get_information




# %%
app = Flask(__name__)
@app.route('/job_search', methods=['POST'])
def job_search():
    data = request.get_json()
    # conecting to the metaphor API
    metaphor_api_key = os.environ.get('Metaphor_API_Key')
    metaphor = Metaphor(metaphor_api_key)
    # Check if the required fields are present in the request JSON
    if 'query' not in data:
        return jsonify({'error': 'Missing required field'}), 400

    # initiaing the search
    response = metaphor.search(
        data["query"],
        num_results=1,
        use_autoprompt=True,
        include_domains=["linkedin.com"],
        type = "keyword"
    )

    #right now we return only 1 result using the search
    overall = []
    for content in response.get_contents().contents:
        res = get_information(content.url)
        overall.extend(res)

    return jsonify(overall)


# %%
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)


