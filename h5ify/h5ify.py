import h5py

def load(file):
    with open(file, 'r') as h:
        return _recursive_load(h, {})

def save(file, dic, mode = 'a', **kwargs):
    with open(file, mode) as h:
        _recursive_save(h, dic)

def _open(file, mode = None):
    return h5py.File(file, mode) if type(file) is str else file

def _recursive_load(h, d):
    attrs = dict(h.attrs)
    if len(attrs) > 0:
        d['attrs'] = attrs
    for key, val in h.items():
        if isinstance(val, h5py.Group):
            d[key] = {}
            recursive(val, d[key])
        elif isinstance(val, h5py.Dataset):
            d[key] = val[()]
    return d

def _recursive_save(h, d):
    for key, val in d.items():
        if key == 'attrs':
            h.attrs.update(d[key])
        elif isinstance(val, dict):
            h.create_group(key)
            recursive(h[key], val)
        else:
            h.create_dataset(key, data = val, **kwargs)
