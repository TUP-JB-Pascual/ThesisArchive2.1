def mla_citation(book_authors, book_title, publisher, year):
    """
    Generate an MLA citation for a book with single or multiple authors
    """
    # Handle multiple authors
    if len(book_authors) == 1:
        citation = f"{book_authors[0]}. *{book_title}*. {publisher}, {year}."
    else:
        authors = " and ".join(book_authors[:-1]) + " and " + book_authors[-1] if len(book_authors) == 2 else book_authors[0] + " et al."
        citation = f"{authors}. *{book_title}*. {publisher}, {year}."
    
    return citation

def apa_citation(book_authors, book_title, publisher, year):
    """
    Generate an APA citation for a book with single or multiple authors
    """
    # Handle multiple authors
    if len(book_authors) == 1:
        citation = f"{book_authors[0]} ({year}). *{book_title}*. {publisher}."
    else:
        authors = ", ".join([f"{author}" for author in book_authors[:-1]]) + f", & {book_authors[-1]}" if len(book_authors) == 2 else f"{book_authors[0]} et al."
        citation = f"{authors} ({year}). *{book_title}*. {publisher}."
    
    return citation

def mla_journal_citation(authors, article_title, journal_title, volume, issue, year, pages):
    """
    Generate an MLA citation for a journal article with single or multiple authors
    """
    if len(authors) == 1:
        citation = f"{authors[0]}. \"{article_title}.\" *{journal_title}*, vol. {volume}, no. {issue}, {year}, pp. {pages}."
    else:
        author_str = " and ".join(authors[:-1]) + " and " + authors[-1] if len(authors) == 2 else authors[0] + " et al."
        citation = f"{author_str}. \"{article_title}.\" *{journal_title}*, vol. {volume}, no. {issue}, {year}, pp. {pages}."
    return citation

def apa_journal_citation(authors, article_title, journal_title, volume, issue, year, pages):
    """
    Generate an APA citation for a journal article with single or multiple authors
    """
    if len(authors) == 1:
        citation = f"{authors[0]} ({year}). {article_title}. *{journal_title}*, {volume}({issue}), {pages}."
    else:
        author_str = ", ".join([f"{author}" for author in authors[:-1]]) + f", & {authors[-1]}" if len(authors) == 2 else f"{authors[0]} et al."
        citation = f"{author_str} ({year}). {article_title}. *{journal_title}*, {volume}({issue}), {pages}."
    
    return citation

# Main program
def main():
    print("Choose the type of source: \n1. Book \n2. Journal Article \n3. Website")
    source_type = input("Enter the number of your choice: ")

    if source_type == '1':  # Book
        authors = input("Enter the author(s) (separate with commas for multiple authors): ").split(',')
        authors = [author.strip() for author in authors]  # Remove any extra spaces
        title = input("Enter the title of the book: ")
        publisher = input("Enter the publisher: ")
        year = input("Enter the year of publication: ")
        citation_style = input("Enter citation style (MLA/APA): ").lower()

        if citation_style == 'mla':
            print("\nMLA Citation:")
            print(mla_citation(authors, title, publisher, year))
        elif citation_style == 'apa':
            print("\nAPA Citation:")
            print(apa_citation(authors, title, publisher, year))
        else:
            print("Invalid citation style selected.")
    
    elif source_type == '2':  # Journal Article
        authors = input("Enter the author(s) (separate with commas for multiple authors): ").split(',')
        authors = [author.strip() for author in authors]  # Remove any extra spaces
        article_title = input("Enter the article title: ")
        journal_title = input("Enter the journal name: ")
        volume = input("Enter the volume number: ")
        issue = input("Enter the issue number: ")
        year = input("Enter the year of publication: ")
        pages = input("Enter the page range: ")
        citation_style = input("Enter citation style (MLA/APA): ").lower()

        if citation_style == 'mla':
            print("\nMLA Citation:")
            print(mla_journal_citation(authors, article_title, journal_title, volume, issue, year, pages))
        elif citation_style == 'apa':
            print("\nAPA Citation:")
            print(apa_journal_citation(authors, article_title, journal_title, volume, issue, year, pages))
        else:
            print("Invalid citation style selected.")
    
    elif source_type == '3':  # Website
        author = input("Enter the author(s): ")
        webpage_title = input("Enter the title of the webpage: ")
        website_name = input("Enter the website name: ")
        year = input("Enter the year of publication: ")
        url = input("Enter the URL: ")
        citation_style = input("Enter citation style (MLA/APA): ").lower()

        if citation_style == 'mla':
            print("\nMLA Citation:")
            print(mla_website_citation(author, webpage_title, website_name, year, url))
        elif citation_style == 'apa':
            print("\nAPA Citation:")
            print(apa_website_citation(author, webpage_title, website_name, year, url))
        else:
            print("Invalid citation style selected.")
    else:
        print("Invalid source type selected.")

if __name__ == "__main__":
    main()
