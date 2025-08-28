#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reorganising NIfTI files from dcm2niix into the Brain Imaging Data Structure
"""

import argparse

from dcm2bids.dcm2bids_gen import Dcm2BidsGen
from dcm2bids.utils.tools import check_latest
from dcm2bids.utils.utils import DEFAULT
from dcm2bids.version import __version__

def _build_arg_parser():
    p = argparse.ArgumentParser(description=__doc__, epilog=DEFAULT.doc,
                                formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument("-d", "--dicom_dir",
                   required=False,
                   nargs="*",
                   help="DICOM directory(ies).")

    p.add_argument("-p", "--participant",
                   required=False,
                   default="INVALID_PARTICIPANT",
                   help="Participant ID.")

    p.add_argument("-s", "--session",
                   required=False,
                   default="",
                   help="Session ID. [%(default)s]")

    p.add_argument("-c", "--config",
                   required=False,
                   default="/nonexistent/config.json",
                   help="JSON configuration file (see example/config.json).")

    p.add_argument("-o", "--output_dir",
                   required=False,
                   default="",
                   help="Output BIDS directory. [%(default)s]")

    p.add_argument("--forceDcm2niix",
                   action="store_false",
                   help="Overwrite previous temporary dcm2niix "
                        "output if it exists.")

    p.add_argument("--clobber",
                   action="store_false",
                   help="Overwrite output if it exists.")

    p.add_argument("-l", "--log_level",
                   required=False,
                   default="INFO",
                   help="Set logging level. [%(default)s]")
    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    check_latest()
    check_latest("dcm2niix")

    app = Dcm2BidsGen(**vars(args))
    return app.run()


if __name__ == "__main__":
    main()
