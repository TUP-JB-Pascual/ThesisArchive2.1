def mla_format(self):
    """Returns MLA formatted citation with multiple authors."""
    authors = [str(author) for author in self.authors.all()]
    if len(authors) > 1:
        authors = ", ".join(authors[:-1]) + " and " + authors[-1]
    else:
        authors = authors[0]
    return f"{authors}. {self.title}. {self.publisher}, {self.date_published}."
    
def apa_format(self):
    """Returns APA formatted citation with multiple authors."""
    authors = [f"{author.last_name}, {author.first_name[0]}." for author in self.authors.all()]
    if len(authors) > 1:
        authors = ", ".join(authors[:-1]) + " & " + authors[-1]
    else:
        authors = authors[0]
    return f"{authors} ({self.date_published}). {self.title}. {self.publisher}."