# Youtube Channel Surf

 Simple Streamlit dashboard created using Official Youtube API and Spacy NLP similarity to search for similar youtube channels you might enjoy, using a youtube link as input.

## Pre-requisites:

1. Set-up Youtube project to obtain personal API Key. See [official documentation](https://developers.google.com/youtube/registering_an_application) for details 
* Note: Take note of daily API call quota limits (see [official limits](https://developers.google.com/youtube/v3/determine_quota_cost) for details). 

2. Activate virtual environment in the directory of choice and install the necessary libraries outlined in requirements.txt and the required NLP pipeline for spacy dependecy. 

   ```python
   pip install -r requirements.txt
   python -m spacy download en_core_web_lg
   ```
## Usage:

1. Activate your virtual environment of choice and run the streamlit script dashboard.py

   ```python
   streamlit run dashboard.py
   ```
2. The Dashboard would be running on local host (Port: 8501) by default. Open the web browser and enter the corresponding localhost address (http://127.0.0.1:8501/) to view the Dashboard.

3. To start using the dashboard, fill the following fields before selecting the 'Submit' button:

    * API Key: Obtain in Pre-requisite step 1
    * Search Input: Youtube input link (Example: https://www.youtube.com/watch?v=a1b2c3d4e5f)
    * Max Search Results: Maximum number of results to be returned
    * Similarity Filter Threshold: Channels with similarity score of input threshold or higher will be returned after search. (Higher threshold corresponds to more similar channels returned)

![dashboard-overview](/readme_img/dashboard-overview.png)