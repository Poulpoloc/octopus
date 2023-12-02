class CompilerReport:
    """
    Contains useful information about the compilation process.
    This is supposed to be used by Poulpi.
    """
    warnings : list[Warning] = []
    errors = []
    def __init__(self):
        pass

    def reset(self):
        self.warnings = []
        self.errors = []

    def warning(self, warning:Warning):
        self.warnings.append(warning)

    def error(self, error):
        self.errors.append(error)

    def merge_span(self, spans):
        return min([i[0] for i in spans]), max([i[1] for i in spans])

    def __repr__(self):
        return f"REPORT:\n{self.warnings}\n{self.errors}"

class CRWarning:
    def __init__(self, message, location_span):
        self.message = message
        self.location_span = location_span

    def __repr__(self):
        return f"WARNING: {self.message} at {self.location_span}"

class CRError:
    def __init__(self, message, location_span):
        self.message = message
        self.location_span = location_span

    def __repr__(self):
        return f"ERROR: {self.message} at {self.location_span}"
