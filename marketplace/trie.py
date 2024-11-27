# Definiert die Klasse Trie. class is used to look for all words that start with a given prefix.

class TrieNode:
    """A node in the Trie structure.

   Attributes:
       children: A dictionary mapping character to TrieNode.
       _is_end_of_word: A boolean indicating if the node represents the end of a word.
   """

    # *** CONSTRUCTORS ***
    def __init__(self):
        """Initializes a TrieNode with an empty children dictionary and end-of-word flag set to False."""
        self.children = {}
        self._is_end_of_word = False

    # *** PUBLIC SET methods ***

    def set_is_end_of_word(self):
        """
        Sets member variable _is_end_of_word to True
        """
        self._is_end_of_word = True

    # *** PUBLIC methods to return class properties ***

    def is_end_of_word(self):
        return self._is_end_of_word


class Trie:
    """A Trie data structure for storing strings.

    Attributes:
        _root (TrieNode): The root node of the Trie.
    """

    # *** CONSTRUCTORS ***
    def __init__(self):
        """Initializes a Trie with a root TrieNode."""
        self._root = TrieNode()

    # *** PUBLIC methods ***

    def insert(self, word):
        """Inserts a word into the Trie. Goes through each character of the given word. if a character is not yet
        a child node, then add a new TrieNode for this character and go to this child node. the node representing the
        last character of the word is marked by setting _is_end_of_word to True.

        Args:
            word (str): The word to be inserted into the Trie.
        """
        word = word.lower()
        node = self._root
        for char in word:           # for each character of the word
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.set_is_end_of_word()

    # *** PUBLIC GET methods ***

    def search(self, prefix):
        """Searches for all words in the Trie that start with the given prefix. Calls _ind_words with the node that is
        the last node of the prefix

        Args:
            prefix (str): The prefix to search for in the Trie.

        Returns:
            list: A list of words that start with the given prefix.
        """
        prefix = prefix.lower()
        node = self._root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return Trie._find_words(node, prefix)

    # *** PRIVATE methods ***

    @staticmethod
    def _find_words(node, prefix):
        """Recursively finds all words starting from the given node.

        Args:
            node (TrieNode): The node to start the search from.
            prefix (str): The current prefix formed from the root to this node.

        Returns:
            list: A list of words found from this node.
        """
        words = []
        if node.is_end_of_word():
            words.append(prefix)
        for char, next_node in node.children.items():
            words.extend(Trie._find_words(next_node, prefix + char))
        return words
