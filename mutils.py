# pylint: disable=missing-docstring
import bson

admin_collections = [
    "system.users",
    "system.roles",
    "system.version",
]

config_collections = [
    "shards",
    "databases",
    "collections",
    "chunks",
    "tags",
    "version",
]


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


def mtrim(src):
    dst = {
        "nss": {},
        "brief": {},
        "docs": {},
    }

    for key in src["nss"]:
        _, ns = key.split(":", 1)
        db, coll = ns.split(".", 1)
        if not _allowed(db, coll):
            continue

        dst["nss"][key] = src["nss"][key]
        if key in src["brief"]:
            dst["brief"][key] = src["brief"][key]

        if "docs" not in src:
            continue

        if key in src["docs"]:
            dst["docs"][key] = src["docs"][key]
            dst["docs"][key].sort(key=doc_sort_key)
        if not coll.startswith("system.") and f":{ns}" in src["docs"]:
            dst["docs"][f":{ns}"] = src["docs"][f":{ns}"]
            dst["docs"][key].sort(key=doc_sort_key)

    return dst


def _allowed(db_name, coll_name):
    match db_name:
        case "local":
            return False
        case "admin":
            return coll_name in admin_collections
        case "config":
            return coll_name in config_collections

    return (
        not coll_name.startswith("system.")
        or coll_name.startswith("system.buckets.")
        or coll_name in ("system.views", "system.js")
    )
