import hashlib
import yaml

class CheckedItemContract(object):
    def __init__(self, checked_items=[]):
        assert isinstance(checked_items, list)

        for ci in checked_items: 
            assert isinstance(ci, CheckedItem)

        self._items = {}

        for ci in checked_items:
            self.add_item(ci)
    
    def verify(self, verbose=False):
        statuses = []
        
        for ci in self._items.values():
            is_ok = ci.verify()
            statuses.append(is_ok)
            if verbose:
                print('%s : %s' % (ci.fp, is_ok))
    
        return all(statuses)

    def as_dict(self):
        return {k: ci.hash for k, ci in self._items.items()}

    @classmethod
    def from_filepaths(cls, fps):
        '''
        Generates checked items and populates their hash
        '''
        checked_items = [CheckedItem(fp)for fp in fps]
        for ci in checked_items:
            ci.populate_hash()
        return cls(checked_items=checked_items)

    @classmethod
    def from_dict(cls, d):
        contract = cls()
        for fp, h in d.items():
            contract.add_item(CheckedItem(fp, h))
        return contract

    def to_yaml(self, fp):
        d = self.as_dict()
        with open(fp, 'w') as out:
            yaml.dump(d, out)

    @classmethod
    def from_yaml(cls, fp):
        with open(fp, 'r') as f:
            d = yaml.safe_load(f)
        return cls.from_dict(d)

    def add_item(self, item):
        self[item.fp] = item

    def __setitem__(self, fp, ci):
        assert fp not in self._items
        assert isinstance(ci, CheckedItem)
        self._items[fp] = ci

    def __getitem__(self, fp):
        assert fp in self._items
        return self._items[fp]

    def __repr__(self):
        return str(self.as_dict())

class CheckedItem(object):
    def __init__(self, fp, checksum=None):
        self.fp = fp
        self.hash = checksum
    
    def verify(self):
        assert self.is_hashed()
        return self._calc_hash(self.fp) == self.hash

    def populate_hash(self):
        assert self.fp is not None
        assert not self.is_hashed()
        self.hash = self._calc_hash(self.fp)

    @staticmethod
    def _calc_hash(fp):
        with open(fp, 'rb') as f:
            hexhash = hashlib.md5(f.read()).hexdigest()
        return hexhash
    
    def as_dict(self):
        return dict(path=self.fp, hash=self.hash)
    
    def __repr__(self):
        return str(self.as_dict())
    
    def is_hashed(self):
        return self.hash is not None