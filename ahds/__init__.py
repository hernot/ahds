# -*- coding: utf-8 -*-
# ahds

# to use relative syntax make sure you have the package installed in a virtualenv in develop mode e.g. use
# pip install -e /path/to/folder/with/setup.py
# or
# python setup.py develop
from .core import Block
from .header import AmiraHeader
from .data_stream import set_data_stream


class AmiraFile(Block):
    """Main entry point for working with Amira files"""
    __slots__ = ('_fn', '_load_streams', '_meta' '_header', '_data_streams')

    def __init__(self, fn, load_streams=True, *args, **kwargs):
        """Initialise a new AmiraFile object given the Amira file.

        Passes additional args/kwargs to AmiraHeader class for initialisation of the reading process

        .. code:: python

            from ahds import AmiraFile
            af = AmiraFile('file.am')
            print(af)

        :param str fn: Amira file name
        :param bool load_streams: whether (default) or not to load data streams
        """
        super(AmiraFile, self).__init__(fn)
        self._fn = fn
        self._load_streams = load_streams
        # the header contains a lot of information relied on for reading streams
        self._header = AmiraHeader(fn, load_streams=load_streams, *args, **kwargs)
        # meta block
        super(AmiraFile, self).add_attr('meta', Block('meta'))
        self.meta.add_attr('file', self._fn)
        self.meta.add_attr('header length', len(self._header))
        self.meta.add_attr('data streams', self._header.data_stream_count)
        self.meta.add_attr('streams_loaded', self._load_streams)
        # header block
        super(AmiraFile, self).add_attr('header', self._header)
        # data streams block
        super(AmiraFile, self).add_attr(Block('data_streams'))
        if self._load_streams:
            self.read()

    def read(self):
        """Read the data streams if they are not read yet"""
        if self._header.filetype == "AmiraMesh":
            for ds in self._header._data_streams_block_list:
                ds.read()
                ds.add_attr('data', ds.get_data())
                self.data_streams.add_attr(ds)
        elif self._header.filetype == "HyperSurface":
            block = set_data_stream('Data', self._header)
            block.read()
            self.data_streams.add_attr(block)
        self._load_streams = self._header.load_streams = True

    def __repr__(self):
        return "AmiraFile('{}', read={})".format(self._fn, self._read)

    def __str__(self, prefix="", index=None):
        width = 140
        string = ""
        string += '*' * width + '\n'
        string += "AMIRA HEADER AND DATA STREAMS\n"
        string += "-" * width + "\n"
        string += super(AmiraFile, self).__str__(prefix=prefix, index=index)
        string += "*" * width
        return string


__all__ = ['AmiraFile', 'AmiraHeader']
