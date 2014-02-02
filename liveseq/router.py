#!/usr/bin/env python3

class Router:
    """
    A router that holds a set of outputs and routes data
    to them according to a simple addressing scheme. Supported
    are also splitting and transforms.
    """
    def __init__(self):
        self.outputs = {}
        self.splits = {}
        self.transforms = {}

    def write(self, identifier, data):
        """
        Write data to an identifier and do what is meant for that identifier,
        either write to output, split to new identifiers or transform.

        @identifier string
        @data any type suitable for the intended output object
        """
        transform = self.transforms.get(identifier)
        if not transform is None:
            data = transform(data)
        splits = self.splits.get(identifier)
        if not splits is None:
            for split in splits:
                self.push(split, data)
            return
        output = self.outputs.get(identifier)
        if output is None:
            print("Output '%s' not defined!" % identifier)
            return
        print("Writing %s to %s" % (str(data), identifier))
        output.write(data)

    def add(self, output, identifier=None):
        """
        Add an output object to the routing table
        @output output object with a write method
        @identifier string (override internal identifier)
        """
        identifier = identifier or output.identifier
        self.outputs[identifier] = output
        if hasattr(output, "router"):
            output.router = self

    def add_splitter(self, identifier, targets):
        """
        Add a splitter rule for a transformer
        @identifier string
        @targets enumerable list of targets
        """
        self.splits[identifier] = targets

    def add_transform(self, identifier, transform):
        """
        Add a transform function to the routing table
        @identifier string
        @transform function taking and returning data
        """
        self.transforms[identifier] = transform

