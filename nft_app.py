import streamlit as st
import pandas as pd
import numpy as np

# Load the data
nft_df = pd.read_csv('./Data/nft_data.csv', low_memory=False)
tweets_df = pd.read_csv('./Data/tweets.csv', low_memory=False)
google_trend_region_df = pd.read_csv('./Data/google_trend_per_region.csv')
google_trend_time_df = pd.read_csv('./Data/google_trend_over_time.csv')

# Calculate the difference between followers and friends "Followings"
nft_df['Profile: relative followers'] = nft_df['Twitter User Followers Count'] - nft_df['Twitter User Friends Count']

# Remove duplicates (keep one tweet per username per NFT)
tweets_df.drop_duplicates(subset=['Twitter Profile', 'Username'], inplace=True)

# Group, aggregate, and rename columns
grouped_tweets = tweets_df[['Twitter Profile', 'User Followers Count']].groupby(['Twitter Profile'])
tweets_followers_df = grouped_tweets.agg({'User Followers Count': ['count', 'sum', 'mean', 'median', 'max']})['User Followers Count']
tweets_followers_df.rename(columns={"count": "Tweets: count", "mean": "Tweets: average followers", "median": "Tweets: median followers", "max": "Tweets: max followers", "sum": "Tweets: cumulated followers"}, inplace=True)

# Merge profile and tweets information
merged_df = tweets_followers_df.merge(nft_df.set_index('Twitter Profile')['Profile: relative followers'], left_index=True, right_index=True, how='inner')

# Min-max normalization
merged_norm_df=(merged_df-merged_df.min())/(merged_df.max()-merged_df.min())

# Calculate "Exposure" indicator
merged_norm_df['Exposure score'] = merged_norm_df.sum(axis=1)

# Get the top NFT according to the "Exposure" indicator
top_nfts_norm_df = merged_norm_df.sort_values('Exposure score', ascending=False)

# Set the index names with numbers to keep the order in the bar plot that follows
top_nfts_norm_df['Twitter Profile'] = top_nfts_norm_df.index
top_nfts_norm_df.set_index(['{:0>2d} – '.format(i) for i in range(1, len(top_nfts_norm_df)+1)] + top_nfts_norm_df.index, inplace=True)

# Get the merged dataframe sorted by the "Exposure score"
top_merged_df = merged_df.loc[top_nfts_norm_df['Twitter Profile']]
top_merged_df.set_index(['{:0>2d} – '.format(i) for i in range(1, len(top_merged_df)+1)] + top_merged_df.index, inplace=True)

# Streamlit title and text
st.title('Ranking of upcoming NFT sales')

st.header("19th of November 2021")

# Plots 20 first NFTs
st.bar_chart(top_nfts_norm_df.drop(['Exposure score', 'Twitter Profile'], axis=1)[0:20])

# st.bar_chart(top_merged_df[ 'Tweets: max followers'][0:15]*1e-6)
# st.bar_chart(top_merged_df['Profile: relative followers'][0:20]*1e-3, height=300, width=5000)

# Show table
for i in range(1,21): # number of rows in your table! = 2   
    # Localize element in the dataframe
    nft_name = top_nfts_norm_df.index[i-1][5:]
    nft_local_df = nft_df.loc[nft_df['Twitter Profile'] == nft_name]
    top_nfts_local_df = top_nfts_norm_df.loc[top_nfts_norm_df['Twitter Profile'] == nft_name]

    # Extract information for each NFT
    twitter_url = '[Twitter](https://twitter.com/{0})'.format(nft_local_df['Twitter Profile'].values[0])
    website_url = '[Website](https://{0})'.format(nft_local_df['Website'].values[0])
    banner_url = nft_local_df['Twitter User Profile Banner Url'].values[0]
    description = nft_local_df['Description'].values[0]
    twitter_description = nft_local_df['Twitter User Description'].values[0]
    price = nft_local_df['Price ETH'].values[0]
    Exposure_score = top_nfts_local_df['Exposure score'].values[0]
    delta_twitter_followers = nft_local_df['Profile: relative followers'].values[0]

    # Print tilte and subtitle
    st.header(("{0}. {1}".format(i, nft_name).title()))
    st.subheader(description)

    # Print main metrics
    col = st.columns(3)
    if price > 0:
        col[0].metric('Price (ETH)', '{:.2f}'.format(price)) 
    else:
        col[0].metric('No price tag', '{:.2f}'.format(price))
    col[1].metric('Exposure Score', '{:.2f}'.format(Exposure_score))
    col[2].metric('Profile: relative followers', '{:,.0f}'.format(delta_twitter_followers))

    # Picture and links
    if type(banner_url) is str:
        st.image(banner_url)
    st.write(twitter_description)
    st.write(' :point_right: ', twitter_url)
    st.write(' :point_right: ', website_url)