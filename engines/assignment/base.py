# -*- coding: utf-8 -*-

class BaseAssignmentStrategy:

    code = None

    def __init__(self, env):
        self.env = env

    def execute(self, assignments):
        raise NotImplementedError()
