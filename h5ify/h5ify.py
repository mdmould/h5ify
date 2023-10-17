import h5py


def open(file, mode=None):

    return h5py.File(file, mode) if type(file) is str else file


def load(file):

    def recursive(h, d):

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

    with open(file, 'r') as h:
        return recursive(h, {})


def save(file, dic, *args, **kwargs):

    def recursive(h, d):

        for key, val in d.items():

            if key == 'attrs':
                h.attrs.update(d[key])

            elif isinstance(val, dict):
                h.create_group(key)
                recursive(h[key], val)

            else:
                h.create_dataset(key, *args, data=val, **kwargs)

    with open(file, 'a') as h:
        recursive(h, dic)

