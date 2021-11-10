import streamlit as st
import pandas as pd
import numpy as np



import streamlit.components.v1 as components  # Import Streamlit

# Render the h1 block, contained in a frame of size 200x200.
components.html(
    """
    <script id="mcjs">!function(c,h,i,m,p){m=c.createElement(h),p=c.getElementsByTagName(h)[0],m.async=1,m.src=i,p.parentNode.insertBefore(m,p)}(document,"script","https://chimpstatic.com/mcjs-connected/js/users/caa5f8f8430da8ccdec49101c/b0fa7a23be31a6aba1cedf0f2.js");</script>
    """
)


# Streamlit title and text
st.title("NFT analysis")

st.write("What we do:")
st.write("- 1")
st.write("- 1")
st.write("- 1")

# Load the data
nft_df = pd.read_csv('./Data/nft_data.csv', low_memory=False)
tweets_df = pd.read_csv('./Data/tweets.csv', low_memory=False)
google_trend_region_df = pd.read_csv('./Data/google_trend_per_region.csv')
google_trend_time_df = pd.read_csv('./Data/google_trend_over_time.csv')

# First Section: Evaluate Twitter profiles for each NFT
st.subheader('Evaluate Twitter profiles for each NFT')

# Calculate the difference between followers and friends "Followings"
nft_df['Delta Twitter Followers'] = nft_df['Twitter User Followers Count'] - nft_df['Twitter User Friends Count']

# Sub-heading
st.subheader('Evaluate last tweets')

# Group and aggregate
tweets_followers_df = tweets_df[['Twitter Profile', 'User Followers Count']].groupby(['Twitter Profile']).agg({'User Followers Count': ['count', 'sum', 'mean', 'median', 'max']})['User Followers Count']

# Merge profile and tweets information
merged_df = tweets_followers_df.merge(nft_df.set_index('Twitter Profile')['Delta Twitter Followers'], left_index=True, right_index=True, how='inner')

# Min-max normalization
merged_norm_df=(merged_df-merged_df.min())/(merged_df.max()-merged_df.min())

# Calculate "hype" indicator
merged_norm_df['hype indicator'] = merged_norm_df.sum(axis=1)

# Get the top NFT according to the "hype" indicator
top_nfts_df = merged_norm_df.sort_values('hype indicator', ascending=False)

# Set the index names with numbers to keep the order in the bar plot that follows
top_nfts_df['Twitter Profile'] = top_nfts_df.index
top_nfts_df.set_index(['{:0>2d} – '.format(i) for i in range(1, len(top_nfts_df)+1)] + top_nfts_df.index, inplace=True)

# Plots
st.bar_chart(top_nfts_df.drop(['hype indicator', 'Twitter Profile'], axis=1)[0:20])
st.bar_chart(top_nfts_df['Delta Twitter Followers'][0:20])

## TITLE
st.title("Top NFT")

# Show table
for i in range(1,len(top_nfts_df)+1): # number of rows in your table! = 2   
    # Localize element in the dataframe
    nft_name = top_nfts_df.index[i-1][5:]
    nft_local_df = nft_df.loc[nft_df['Twitter Profile'] == nft_name]
    top_nfts_local_df = top_nfts_df.loc[top_nfts_df['Twitter Profile'] == nft_name]

    # Extract information for each NFT
    twitter_url = '[Twitter](https://twitter.com/{0})'.format(nft_local_df['Twitter Profile'].values[0])
    website_url = '[Website]({0})'.format(nft_local_df['Website'].values[0])
    banner_url = nft_local_df['Twitter User Profile Banner Url'].values[0]
    description = nft_local_df['Description'].values[0]
    twitter_description = nft_local_df['Twitter User Description'].values[0]
    price = nft_local_df['Price ETH'].values[0]
    hype_score = top_nfts_local_df['hype indicator'].values[0]
    delta_twitter_followers = nft_local_df['Delta Twitter Followers'].values[0]

    # Print tilte and subtitle
    st.header(("{0}. {1}".format(i, nft_name).title()))
    st.subheader(description)

    # Print main metrics
    col = st.columns(3)
    if price > 0:
        col[0].metric('Price (ETH)', '{:.2f}'.format(price)) 
    else:
        col[0].metric('No price tag', '{:.2f}'.format(price))
    col[1].metric('Hype Score', '{:.2f}'.format(hype_score))
    col[2].metric('Delta Twitter Followers', '{:,.0f}'.format(delta_twitter_followers))

    # Picture and links
    st.image(banner_url)
    st.write(twitter_description)
    st.write(' :point_right: ', twitter_url)
    st.write(' :point_right: ', website_url)



    
    



    


