import requests
import config
import collections
import json

from typing import List
from collections import UserDict



GRAPHQL_URL = "https://api.github.com/graphql"
REPO_ISSUES_QUERY = """
{{
  repository(owner: "{owner}", name: "{name}") {{
    databaseId
    primaryLanguage {{
      name
    }}
    issues(first: 100, labels: {labels}, after: {endCursor}, states:OPEN){{
      nodes{{
        title
        url
      }}
      pageInfo{{
        hasNextPage
        endCursor
      }}
    }}
  }}
}}
"""


class GraphQLQuery(object):
    query_base = ""
    json = ""
    headers = {'Authorization': 'token %s' % config.TOKEN}

    def __init__(self, **kwargs):
        self.json = requests.post(GRAPHQL_URL, json={"query": self.query_base.format_map(kwargs).replace("'", "\"")},
                                  headers=self.headers).json()["data"]
        # self.data = namedtuple('Field', self.json.keys())(*self.json.values())
        self.data = tupperware(self.json)
        # print(self.data)

    # def _convert(self, dictionary):
    #     return namedtuple('Field', dictionary.keys())(**dictionary)


class RepoIssuesQuery(GraphQLQuery):
    query_base = REPO_ISSUES_QUERY

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.issues = type('', (), {})()  # https://stackoverflow.com/questions/2280334/shortest-way-of-creating-an-object-with-arbitrary-attributes-in-python
    #     self.issues.nodes = self.json["repository"]["issues"]["nodes"]
    #     self.issues.pageInfo = self.json["repository"]["issues"]["pageInfo"]
    #     self.repo = type('', (), {})()
    #     self.repo.id = self.json["repository"]["databaseId"]
    #     self.repo.language = self.json["repository"]["primaryLanguage"]["name"]


def get_issues(name: str, owner: str, labels: List[str], endCursor: str = None):
    if endCursor is not None:
        endCursor = "\"" + endCursor + "\""
    else:
        endCursor = "null"
    headers = {'Authorization': 'token %s' % config.TOKEN}
    generated_query = REPO_ISSUES_QUERY.format_map(locals()).replace("'", "\"")
    query_results = requests.post(GRAPHQL_URL, json={"query": generated_query}, headers=headers).json()["data"]
    return query_results

def tupperware(mapping):
    """ From https://gist.github.com/hangtwenty/5960435.
    Convert mappings to 'tupperwares' recursively.
    Lets you use dicts like they're JavaScript Object Literals (~=JSON)...
    It recursively turns mappings (dictionaries) into namedtuples.
    Thus, you can cheaply create an object whose attributes are accessible
    by dotted notation (all the way down).
    Use cases:
        * Fake objects (useful for dependency injection when you're making
         fakes/stubs that are simpler than proper mocks)
        * Storing data (like fixtures) in a structured way, in Python code
        (data whose initial definition reads nicely like JSON). You could do
        this with dictionaries, but namedtuples are immutable, and their
        dotted notation can be clearer in some contexts.
    .. doctest::
        >>> t = tupperware({
        ...     'foo': 'bar',
        ...     'baz': {'qux': 'quux'},
        ...     'tito': {
        ...             'tata': 'tutu',
        ...             'totoro': 'tots',
        ...             'frobnicator': ['this', 'is', 'not', 'a', 'mapping']
        ...     }
        ... })
        >>> t # doctest: +ELLIPSIS
        Tupperware(tito=Tupperware(...), foo='bar', baz=Tupperware(qux='quux'))
        >>> t.tito # doctest: +ELLIPSIS
        Tupperware(frobnicator=[...], tata='tutu', totoro='tots')
        >>> t.tito.tata
        'tutu'
        >>> t.tito.frobnicator
        ['this', 'is', 'not', 'a', 'mapping']
        >>> t.foo
        'bar'
        >>> t.baz.qux
        'quux'
    Args:
        mapping: An object that might be a mapping. If it's a mapping, convert
        it (and all of its contents that are mappings) to namedtuples
        (called 'Tupperwares').
    Returns:
        A tupperware (a namedtuple (of namedtuples (of namedtuples (...)))).
        If argument is not a mapping, it just returns it (this enables the
        recursion).
    """

    if (isinstance(mapping, collections.Mapping) and
            not isinstance(mapping, ProtectedDict)):
        for key, value in mapping.items():
            mapping[key] = tupperware(value)
        return namedtuple_from_mapping(mapping)
    return mapping


def namedtuple_from_mapping(mapping, name="Tupperware"):
    this_namedtuple_maker = collections.namedtuple(name, mapping.keys())
    return this_namedtuple_maker(**mapping)


class ProtectedDict(UserDict):
    """ A class that exists just to tell `tupperware` not to eat it.
    `tupperware` eats all dicts you give it, recursively; but what if you
    actually want a dictionary in there? This will stop it. Just do
    ProtectedDict({...}) or ProtectedDict(kwarg=foo).
    """


def tupperware_from_kwargs(**kwargs):
    return tupperware(kwargs)


if __name__ == "__main__":
    r = RepoIssuesQuery(name="ansible", owner="ansible", labels=["docs"], endCursor="null")
    for i in r.data.repository.issues.nodes:
        print(i)
    print(r.data.repository.issues.pageInfo.hasNextPage)
