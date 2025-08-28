# -*- coding: utf-8 -*-

"""Participant class"""

import logging
from os.path import join as opj

from dcm2bids.utils.utils import DEFAULT
from dcm2bids.version import __version__


class Acquisition(object):
    """ Class representing an acquisition

    Args:
        participant (Participant): A participant object
        dataType (str): A functional group of MRI data (ex: func, anat ...)
        modalityLabel (str): The modality of the acquisition
                (ex: T1w, T2w, bold ...)
        customLabels (str): Optional labels (ex: task-rest)
        srcSidecar (Sidecar): Optional sidecar object
    """

    def __init__(
        self,
        participant,
        dataType,
        modalityLabel,
        indexSidecar=None,
        customLabels="",
        srcSidecar=None,
        sidecarChanges=None,
        intendedFor=None,
        IntendedFor=None,
        **kwargs
    ):
        self.logger = logging.getLogger(__name__)

        self._modalityLabel = ""
        self._customLabels = ""
        self._intendedFor = None
        self._indexSidecar = None

        self.participant = participant
        self.dataType = dataType
        self.modalityLabel = modalityLabel
        self.customLabels = customLabels
        self.srcSidecar = srcSidecar

        if sidecarChanges is None:
            self.sidecarChanges = {}
        else:
            self.sidecarChanges = sidecarChanges

        if intendedFor is None:
            self.intendedFor = IntendedFor
        else:
            self.intendedFor = intendedFor

        self.dstFile = ''

    def __eq__(self, other):
        if not isinstance(other, Acquisition):
            return False
        return (self.participant == other.participant and
                self.dataType == other.dataType and
                self.modalityLabel == other.modalityLabel and
                self.customLabels == other.customLabels)

    @property
    def modalityLabel(self):
        """
        Returns:
            A string '_<modalityLabel>'
        """
        return self._modalityLabel

    @modalityLabel.setter
    def modalityLabel(self, modalityLabel):
        """ Prepend '_' if necessary"""
        self._modalityLabel = self.prepend(modalityLabel)

    @property
    def customLabels(self):
        """
        Returns:
            A string '_<customLabels>'
        """
        return self._customLabels

    @customLabels.setter
    def customLabels(self, customLabels):
        """ Prepend '_' if necessary"""
        self._customLabels = self.prepend(customLabels)

    @property
    def suffix(self):
        """ The suffix to build filenames

        Returns:
            A string '_<modalityLabel>' or '_<customLabels>_<modalityLabel>'
        """
        if self.customLabels.strip() == "":
            return self.modalityLabel
        else:
            return self.customLabels + self.modalityLabel

    @property
    def srcRoot(self):
        """
        Return:
            The sidecar source root to move
        """
        if self.srcSidecar:
            return self.srcSidecar.root
        else:
            return None

    @property
    def dstRoot(self):
        """
        Return:
            The destination root inside the BIDS structure
        """
        return opj(
            self.participant.directory,
            self.dataType,
            self.dstFile
        )

    @property
    def dstIntendedFor(self):
        """
        Return:
            The destination root inside the BIDS structure for intendedFor
        """
        return opj(
            self.participant.session,
            self.dataType,
            self.dstFile,
        )

    def setDstFile(self):
        """
        Return:
            The destination filename formatted following the v1.7.0 BIDS entity key table
            https://bids-specification.readthedocs.io/en/v1.7.0/99-appendices/04-entity-table.html
        """
        current_name = self.participant.prefix + self.suffix

        # Parse the current name to extract entities and suffix
        parts = current_name.split("_")
        entities = {}
        suffix_parts = []

        for part in parts:
            if "-" in part and len(part.split("-")) == 2:
                key, value = part.split("-", 1)
                entities[key] = value
            else:
                suffix_parts.append(part)

        # Build the filename with entities in BIDS order
        ordered_parts = []

        # Add entities in BIDS order
        for key in DEFAULT.entityTableKeys:
            if key in entities:
                ordered_parts.append(f"{key}-{entities[key]}")
                entities.pop(key)

        # Add any remaining non-standard entities
        for key, value in entities.items():
            ordered_parts.append(f"{key}-{value}")

        # Add the suffix (modality label)
        if suffix_parts:
            ordered_parts.extend(suffix_parts)

        self.dstFile = "_".join(ordered_parts)

    @property
    def intendedFor(self):
        return self._intendedFor

    @intendedFor.setter
    def intendedFor(self, value):
        if isinstance(value, list):
            self._intendedFor = value
        else:
            self._intendedFor = [value]

    @property
    def indexSidecar(self):
        """
        Returns:
            A int '_<indexSidecar>'
        """
        return self._indexSidecar

    @indexSidecar.setter
    def indexSidecar(self, value):
        """
        Returns:
            A int '_<indexSidecar>'
        """
        self._indexSidecar = value

    def dstSidecarData(self, descriptions, intendedForList):
        """
        """
        data = self.srcSidecar.origData
        data["Dcm2bidsVersion"] = __version__

        # intendedFor key
        if self.intendedFor != [None]:
            intendedValue = []

            for index in self.intendedFor:
                intendedValue = intendedValue + intendedForList[index]

            if len(intendedValue) == 1:
                data["IntendedFor"] = intendedValue[0]
            else:
                data["IntendedFor"] = intendedValue

        # sidecarChanges
        for key, value in self.sidecarChanges.items():
            data[key] = value

        return data

    @staticmethod
    def prepend(value, char="_"):
        """ Prepend `char` to `value` if necessary

        Args:
            value (str)
            char (str)
        """
        if value.strip() == "":
            return ""

        elif value.startswith(char):
            return value

        else:
            return char + value
