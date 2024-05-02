from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import plotly.graph_objects as go

headers = {'User-Agent': 'Chrome/41.0.2228.0'}

author_quotes_cnt = {}
quote_lengths = []
quote_tags = []
tag_counts = {}
for page_num in range(1, 11):
    url = f'http://quotes.toscrape.com/page/{page_num}/'
    req = Request(url, headers=headers)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')
    tags = soup.find_all('div', class_='tags')

    for author, quote, tag in zip(authors, quotes, tags):
        author_name = author.get_text()
        author_quotes_cnt[author_name] = author_quotes_cnt.get(author_name, 0) + 1
        quote_length = len(quote.get_text())
        quote_lengths.append(quote_length)

        for tag_ in tag.find_all('a'):    
            tag_name = tag_.get_text()  
            tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1     
            quote_tags.append(tag_name) 

print("----- Author Statistics -----")
most_quotes_author = max(author_quotes_cnt, key=author_quotes_cnt.get)
most_quotes_count = author_quotes_cnt[most_quotes_author]
least_quotes_author = min(author_quotes_cnt, key=author_quotes_cnt.get)
least_quotes_count = author_quotes_cnt[least_quotes_author]
print(f"Author with the most quotes: {most_quotes_author} ({most_quotes_count})")
print(f"Author with the least quotes: {least_quotes_author} ({least_quotes_count})")
print()

print("------ Quote Analysis ------")
average_length = sum(quote_lengths) / len(quote_lengths)
longest_quote = max(quote_lengths)
shortest_quote = min(quote_lengths)
print(f"Average length of quotes: {average_length:.2f}")
print(f"Longest quote length: {longest_quote}")
print(f"Shortest quote length: {shortest_quote}")
print()

print("------- Tag Analysis -------")
most_popular_tag = max(tag_counts, key=tag_counts.get)
total_tags_used = len(quote_tags)
print(f"Most popular tag: {most_popular_tag}")
print(f"Total number of tags used across all quotes: {total_tags_used}")




sorted_authors = sorted(author_quotes_cnt.items(), key=lambda x: x[1], reverse=True)
top_10_authors = [author for author, count in sorted_authors[:10]]
top_10_quotes = [count for author, count in sorted_authors[:10]]

fig1 = go.Figure(data=[go.Bar(
    x=top_10_authors,  
    y=top_10_quotes,
)])
fig1.update_layout(
    title="Quotes by Authors",
    xaxis_title="Authors",
    yaxis_title="Number of Quotes",
)

sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
top_10_tags = [tag for tag, count in sorted_tags[:10]]
top_10_cnt = [count for tag, count in sorted_tags[:10]]

fig2 = go.Figure(data=[go.Bar(
    x=top_10_tags,  
    y=top_10_cnt,
)])
fig2.update_layout(
    title="Most Popular Tags by Authors",
    xaxis_title="Tags",
    yaxis_title="Count",
)

fig1.show()
fig2.show()