import re
import requests
import pandas as pd
import numpy as np


def getUserId(apiKey:str, input:str, use_link=False):

    if apiKey is None:
        raise ValueError("API Key is not defined.")

    if use_link:
        # Search using video Id -> list: https://developers.google.com/youtube/v3/docs/videos/list
        vid_link_ls = re.findall(r'=(.*)', input)
        vid_id = vid_link_ls[0]
        endpoint = f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={vid_id}&key={apiKey}'
    else:    
        endpoint = f'https://www.googleapis.com/youtube/v3/channels?key={apiKey}&forUsername={input}&part=id'

    # Make a request
    content = requests.get(url = endpoint).json()

    return content['items'][0]['snippet']['channelId'] if use_link else content['items'][0]['id']


def getChannelInfo(apiKey:str, user_id:str):

    if apiKey is None:
        raise ValueError("API Key is not defined.")

    # List channel details
    # Docs: https://developers.google.com/youtube/v3/docs/channels/list
    endpoint = f'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&part=topicDetails&part=brandingSettings&part=contentOwnerDetails&id={user_id}&key={apiKey}'

    # Make a request
    content = requests.get(url = endpoint).json()

    # Try to get keywords if possible, else return description or wiki links tags as keywords
    keywords = ''
    try:
        keywords = keywords + content['items'][0]['brandingSettings']['channel']['keywords']
    except:
        try:
            keywords = keywords + content['items'][0]['snippet']['description']
        except:
            try:
                wiki_link_ls = ['items'][0]['topicDetails']['topicCategories']
                parse_ls = [re.findall(r'wiki\/(.*)', link) for link in wiki_link_ls]
                keywords = ' '.join(parse_ls)
            except:
                keywords = keywords + content['items'][0]['brandingSettings']['channel']['description']
    
    # Get channel statistics
    stats = content['items'][0]['statistics']

    return keywords, stats


def searchChannelInfo(apiKey:str, input:str, max_results=50, use_link=False):

    if apiKey is None:
        raise ValueError("API Key is not defined.")
    elif input is None or len(input) == 0:
        raise ValueError("Input is not defined.")

    if use_link:
        # Search using video Id -> list: https://developers.google.com/youtube/v3/docs/videos/list
        vid_link_ls = re.findall(r'=(.*)', input)
        vid_id = vid_link_ls[0]
        endpoint = f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&relatedToVideoId={vid_id}&type=video&key={apiKey}'
    else:
        # Operators: | (or), - (not), && (and)
        query_parse = input.replace('|','%7C').replace(' ','%20').replace('&','%26')
        endpoint = f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&q={query_parse}&type=channel&key={apiKey}'
    
    # Make a request
    content = requests.get(url = endpoint)

    return content.json()

def parseSearch(json):
    output = []

    for idx in range(len(json['items'])):

        item_dict = dict()
        try:
            item_dict['channelId'] = json['items'][idx]['snippet']['channelId']
            item_dict['title'] = json['items'][idx]['snippet']['title']
            item_dict['channelTitle'] = json['items'][idx]['snippet']['channelTitle']
            output.append(item_dict)
        except:
            continue

    return output

def parseKeywords(input:str, nlp):

    # Remove '\n' character
    input = input.replace('\n','')

    # Remove all punctuation
    input = re.sub(r'[^\w\s]', '', input)

    doc = nlp(input)
    output = []

    for token in doc:
        if token.is_stop == False: # Remove stops words, perform word stemming
            output.append(token.lemma_)

    return ' '.join(output)

def extractKeywords(search_list:list, apiKey:str, nlp):

    # unique list of channel ids
    unique_ids = list(set([item['channelId'] for item in search_list]))

    output_ls = []

    for id in unique_ids:
        keywords, stats = getChannelInfo(apiKey, id)
        for channel in search_list:
            if channel['channelId'] == id:
                channelTitle = channel['channelTitle']

        if len(keywords) == 0: # Ignore channels without any keywords (i.e. '')
            continue
        else:
            unique_channel_dict = dict()
            unique_channel_dict['id'] = id
            unique_channel_dict['channel'] = channelTitle
            unique_channel_dict['keywords'] = parseKeywords(keywords, nlp)
            # unique_channel_dict['stats'] = stats
            for key, value in stats.items():
                unique_channel_dict[key]=value
            output_ls.append(unique_channel_dict)

    return output_ls

def filterSearch(vid_url:str, extract_keywords_ls:list, apiKey:str, nlp, filter_percentile=0.75):

    input_id = getUserId(apiKey, vid_url, use_link=True)
    
    input_keywords, _ = getChannelInfo(apiKey, input_id)

    parsed_input_keywords = parseKeywords(input_keywords, nlp)

    base_doc = nlp(parsed_input_keywords)

    sim_score_ls = []

    for channel in extract_keywords_ls:
        if input_id == channel['id']:
            channel['sim_score'] = 0
        else:
            doc = nlp(channel['keywords'])
            sim_score = base_doc.similarity(doc)
            channel['sim_score'] = sim_score
            sim_score_ls.append(sim_score)

    arr = np.array(sim_score_ls)
    # creating a series
    ser = pd.Series(arr)
    # calculating quantile/percentile value
    quantile_value = ser.quantile(q=filter_percentile)
    
    return [channel for channel in extract_keywords_ls if channel['sim_score'] >= quantile_value]