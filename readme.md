# France culture's Science en questions bibliography scraper
## Goal

The goal of this project is to scrape the bibliography made available each week on France Culture's Sciences en Questions podcast page.
The conversations on this podcast are often based on a book published by the weekly guest and I would like to have an easy access to the bibliography without having to access their website each time.

Some ideas about the output could be a list sent by mail each week with all the books available. It could be complemented by a summary found online.
Also, the book could be downloaded automatically and added on my cloud.

## Steps

[1] Use the *requests* library to scrape the data for each episode of the show.
[2] Two ways to go about it.
[x] Using Dictionaries.
[] Using DataFrames.

## Bugs

[x] Only one book per episode at the moment due to the dictionaries loops construction.

## Notes

[Interesting article regarding performance of constructing DataFrames in different ways (list of dicts vs incrementally building it)](https://stackoverflow.com/questions/10715965/create-a-pandas-dataframe-by-appending-one-row-at-a-time).