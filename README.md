# h5ify

Save Python dictionaries to HDF5 files, and load HDF5 files into Python dictionaries.

The dictionary can be a nested dictionary of dictionaries, the terminal values of which are numbers, lists/tuples of numbers, arrays, etc. If the value of a key is not another dictionary, it is stored as a `Dataset` in the HDF5 file, otherwise it creates a new `Group`.

The `attrs` key can be used at each level of a nested dictionary to store metadata for the corresponding `Group` objects in `.attrs`. This currently cannot be used to store `.attrs` metadata for `Dataset` objects. The value for each `attrs` key must be a dictionary that is not nested.

## Install

`pip install h5ify`

## Examples

Make a small dictionary, then save it.
```
import h5ify

d = {'x': 1.0, 'y': 2, 'z': [1, 2, 3], 'attrs': {'info': 'README example'}}
h5ify.save('tmp.h5', d)
```

Load the saved dictionary.
```
dd = h5ify.load('tmp.h5')
print(dd)
```
```
{'attrs': {'info': 'README example'}, 'x': 1.0, 'y': 2, 'z': array([1, 2, 3])}
```
Note that lists/tuple are converted to numpy arrays by h5py.

You can use the usual h5py API to open the stored HDF5 file.
```
import h5py

with h5py.File('tmp.h5', 'r') as f:
    for key, val in f.items():
        print(key, val[()])
    for key, val in f.attrs.items():
        print(key, val)
```
```
x 1.0
y 2
z [1 2 3]
info README example
```

`h5ify` opens HDF5 files in `a` mode, meaning "Read/write if exists, create otherwise". You cannot save a dictionary with the same file name and `Dataset` keys.
```
h5ify.save('tmp.h5', d)
```
```
ValueError: Unable to synchronously create dataset (name already exists)
```

You can append values that are not yet saved to the same file, however.
```
h5ify.save('tmp.h5', {'w': 42})
print(h5ify.load('tmp.h5'))
```
```
{'attrs': {'info': 'README example'}, 'w': 42, 'x': 1.0, 'y': 2, 'z': array([1, 2, 3])}
```

Any additional arguments or keyword arguments to `h5ify.save` are passed to the `create_dataset` function in `h5py`.
```
h5ify.save('tmp.h5', {'comp': [100]}, compression = 'gzip', compression_opts = 9)
```

That should cover it. Let me know if you have questions!

