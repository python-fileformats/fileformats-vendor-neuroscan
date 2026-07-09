from fileformats.core.mixin import WithAdjacentFiles
from fileformats.core.exceptions import FormatMismatchError
from fileformats.generic import File, BinaryFile, UnicodeFile

from fileformats.biosig import Eeg


class NeuroscanEvents(BinaryFile):
    """events"""
    ext = ".cef"

class NeuroscanSensorPosition(UnicodeFile):
    "eeg or meg sensor positions, mostly eeg"
    ext = ".pom"

class NeuroscanDataParameter(UnicodeFile):
    "data parameters, .dpa"
    ext = ".dpa"

class NeuroscanDataParameterDPO(File):
    "data parameters, .dpo"
    ext = ".dpo"


class Neuroscan(WithAdjacentFiles, Eeg, BinaryFile):
    """
    KIT/RIKEN (Ricon) MEG format (directory-based)
    Required files:
    - Main data file (.cdt)
    Optional files: .cef (events), .pom (sensor position), .dpa (data info)
    """

    ext = ".cdt"
    # alternate_exts = (".con",)

    marker_generic_names = ("marker.mrk", "markers.mrk", "kit.mrk")

    @property
    def event_file(self) -> NeuroscanEvents | None:
        try:
            event_path = self.select_by_ext(NeuroscanEvents)
            return NeuroscanEvents(event_path)
        except FormatMismatchError:
            pass
        for cand in self.marker_generic_names:
            event_path = self.parent / cand
            if event_path.exists():
                return NeuroscanEvents(event_path)
        return None

    @property
    def head_position_file(self) -> NeuroscanSensorPosition | None:
        try:
            return NeuroscanSensorPosition(self.select_by_ext(NeuroscanSensorPosition))
        except FormatMismatchError as e:
            if e.args[0].startswith("No matching files"):
                return None
            raise

    @property
    def data_parameter_file(self) -> NeuroscanDataParameter | None:
        try:
            return NeuroscanDataParameter(self.select_by_ext(NeuroscanDataParameter))
        except FormatMismatchError as e:
            if e.args[0].startswith("No matching files"):
                return None
            raise

    @property
    def data_parameter_DPO_file(self) -> NeuroscanDataParameterDPO | None:
        try:
            return NeuroscanDataParameterDPO(self.select_by_ext(NeuroscanDataParameterDPO))
        except FormatMismatchError as e:
            if e.args[0].startswith("No matching files"):
                return None
            raise