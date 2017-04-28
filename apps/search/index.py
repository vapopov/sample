import re
import typing
from collections import defaultdict


class DocumentAlreadyExistsException(Exception):
    """ Raised when document with this id is already added to storage """


class DocumentNotFoundException(Exception):
    """ Raised when document can't be found in storage """


class DocumentIndex:
    """
    Document storage for searchable documents
    Base criteria for task:
     > The service should be optimized for search speed and should be able
     > to handle thousands of documents without significant performance degradation.
    We can use Dict/DefaultDict as a memory storage with constant access level without dependency to storage size:
     - https://www.ics.uci.edu/~pattis/ICS-33/lectures/complexitypython.txt
    """

    _clear_pattern = re.compile('[\W_]+')

    def __init__(self):
        self._terms_storage = defaultdict(set)
        self._document_storage = {}

    def __iter__(self):
        return iter(self._document_storage.values())

    def __str__(self):
        return '<DocumentIndex: with({} documents)>'.format(len(self._document_storage))

    def _tokenize_text(self, text) -> typing.List[str]:
        """ Remove punctuations and return list of words in this text """
        raw_text = self._clear_pattern.sub(' ', text)
        return [term.lower() for term in raw_text.split()]

    def get(self, document_id):
        if document_id not in self._document_storage:
            raise DocumentNotFoundException('Document can\'t be found')
        return self._document_storage[document_id]

    def add(self, document_id: str, text: str):
        """ Add document to searchable storage """
        if document_id in self._document_storage:
            raise DocumentAlreadyExistsException('This id is already added to storage')

        for term in self._tokenize_text(text):
            self._terms_storage[term].add(document_id)

        self._document_storage[document_id] = text

    def remove(self, document_id: str):
        """ Remove document from storage and terms storage """
        if document_id not in self._document_storage:
            raise DocumentNotFoundException('Document can\'t be found')

        text = self._document_storage[document_id]
        for term in self._tokenize_text(text):
            if document_id in self._terms_storage[term]:
                self._terms_storage[term].remove(document_id)

        del self._document_storage[document_id]

    def get_document_ids_by_term(self, term: str) -> typing.Set[str]:
        return self._terms_storage[term]

    def get_documents_by_term(self, term: str) -> typing.List[str]:
        return [self._document_storage[document_id] for document_id in self._terms_storage[term]]


document_index = DocumentIndex()
