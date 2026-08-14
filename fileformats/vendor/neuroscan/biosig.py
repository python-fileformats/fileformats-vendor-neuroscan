from fileformats.biosig import Eeg
from fileformats.core import validated_property
from fileformats.core.exceptions import FormatMismatchError
from fileformats.core.mixin import WithAdjacentFiles
from fileformats.generic import BinaryFile, File, UnicodeFile


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
    Neuroscan data

    Required files:
    - Main data file (.cdt)
    - Parameter file (.dpa) (data info)
    Optional files:
    - .cef (events)
    - .pom (sensor position)
    """

    ext = ".cdt"

    @validated_property
    def data_parameter_file(self) -> NeuroscanDataParameter:
        return NeuroscanDataParameter(self.select_by_ext(NeuroscanDataParameter))

    @validated_property
    def event_file(self) -> NeuroscanEvents | None:
        try:
            event_path = self.select_by_ext(NeuroscanEvents)
            return NeuroscanEvents(event_path)
        except FormatMismatchError:
            return None

    @validated_property
    def head_position_file(self) -> NeuroscanSensorPosition | None:
        try:
            return NeuroscanSensorPosition(self.select_by_ext(NeuroscanSensorPosition))
        except FormatMismatchError as e:
            if e.args[0].startswith("No matching files"):
                return None
            raise

    @validated_property
    def data_parameter_DPO_file(self) -> NeuroscanDataParameterDPO | None:
        try:
            return NeuroscanDataParameterDPO(
                self.select_by_ext(NeuroscanDataParameterDPO)
            )
        except FormatMismatchError as e:
            if e.args[0].startswith("No matching files"):
                return None
            raise
