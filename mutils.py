# pylint: disable=missing-docstring
import bson


class NSMatcher:
    def __init__(self, nss=()):
        self._exacts = set()
        self._prefixes = []
        self.extend(*nss)

    def extend(self, *nss):
        for ns in set(nss):
            ns = ns.strip()
            if ns == "":
                continue
            if ns.endswith("*"):
                self._prefixes.append(ns.rstrip("*"))
            else:
                self._exacts.add(ns)

    def __contains__(self, ns):
        if ns in self._exacts:
            return True
        for prefix in self._prefixes:
            if ns.startswith(prefix):
                return True
        return False


def doc_sort_key(doc: dict):
    _id = doc.get("_id")
    return _id if isinstance(_id, (bson.ObjectId, int, str)) else 0
