class CompilerReport:
    """
    Contains useful information about the compilation process.
    This is supposed to be used by Poulpi.
    """
    def __init__(self):
        self.warnings = []
        self.errors = []

    def reset(self):
        self.warnings = []
        self.errors = []

    def warning(self, warning):
        self.warnings.append(warning)

    def error(self, error):
        self.errors.append(error)

    def __repr__(self):
        return f"REPORT:\n{self.warnings}\n{self.errors}"


class Warning:
    def __init__(self, message, location_span):
        self.message = message
        self.location_span = location_span

    def __repr__(self):
        return f"WARNING: {self.message} at {self.location_span}"

class Error:
    pass
