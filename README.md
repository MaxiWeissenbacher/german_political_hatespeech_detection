# Offensive Language and Hate Speech Identification in a Political Discourse Using German politicians as a Case Study

This is the repository for my Masterthesis about Hatespeech Detection in a Politial Discourse in Germany.
The link/pdf to the thesis will be added soon.

## Folder - BertTopic:

- This folder consists of a topic plot over time. This plot was used to determine which time frames should be scraped.


## Folder - Creating Annotation Dataset:

- Consists of Notebooks on how the annotation datasets got created.
- "schimpf.ipynb" with the swear word approach
- "sentiment_approach.ipynb" with the sentiment approach


## Folder - Creating Annotation Webapp:

- Consists with the implementation of the Annotation Webapp, developed with Streamlit


## Folder - Data Scraping:

- Consists of notebooks on how the Twitter API V2 with Research access was used to scrape the Twitter data.
- "Bundestagsabgeordnete.ipynb": Scraping all MPs and their Social Media account names from "https://www.bundestag.de/abgeordnete"
- "Scraping.ipynb": Scraping of tweets from MPs
- "Mentions_Scraping.ipynb": Scraping of tweets where a MP gets mentioned
- "Data_Concat.ipynb": Putting all datasets from the scraping proccess together into one dataframe
- "retrieve_tweets.ipynb": Reproducing the dataset. Fetch all the Tweets contents with the Tweet ID.


## Folder - Datasets:

- Consits of datasets which were usesd for annotation, training or data analysis
- Datasets are only published with "tweet_id" insteaf of all contents to not hurt Twitter policies
- "annotation_dataseet_tweet_id": The annotated dataset of 1.250 Tweets
- "model_predictions_dataset_tweet_id": The whole Mentions Dataset with the model predictions
- "scraped_twitter_names.csv" & "twitter_usernames_extracted.csv": Scraped usernames from all MPs with an active Twitter Account


## Folder - Model Building:

- Folder with all notebooks which were used for the model building steps
- "Traditional.ipynb": Implementing a traditional machine learning model (SVM)
- "LazyPredict.ipynb": Implementing various traditional machine learning models at once
- "LSTM.ipynb": Implementation of a Pytorch LSTM model
- "Trainer.ipynb": Implementation of Huggingface Trainer with Pytorch datasets (BERT, Electra, RoBERTa models)
- "Hyperparameter_search.ipynb": Hyperparameter optimization for transformer models
- "Ensembling.ipynb": Implementation of the Ensemble approach
- "Ensembling_Germeval_Hasoc.ipynb": Implementation of the Ensemble approach and testing on the Germeval and Hasoc Test Dataset
- "Prediction.ipynb": Applying model to all tweets and predict their label
- "eval_metrics.ipynb": Notebook with functions for evaluation
- "model_overview.ipynb": Notebook to compare the performance of the different models

## Folder - Data Analysis:
- Consists of all Notebooks used for the Data Analysis as well of all plots that have been created
