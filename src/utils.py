"""Module containing methods related to query generator."""


def get_query(created, pub_year):
    # To improve
    # Have the schema and generate the query according to the type
    # Right now, it is straightforward for range values
    # Make it flexible and configurable for any argument keys from the document
    created_start, created_end = created.split(":")
    pub_year_start, pub_year_end = map(int, pub_year.split(":"))
    query = f"_created:[{created_start} TO {created_end}] AND publication_year:[{pub_year_start} TO {pub_year_end}]"

    return query
