# -*- coding: utf-8 -*-

from .state import FlowState


class FlowEngine:

    def __init__(self):
        self.steps = {}

    def register(self, step):
        self.steps[step.code] = step

    def execute(self, state):

        while not state.finished and not state.cancelled:

            step = self.steps.get(state.step)

            if not step:
                state.add_error(f"Unknown step: {state.step}")
                state.cancel()
                break

            step.execute(state)

        return state
