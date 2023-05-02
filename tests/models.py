# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0


def dummy_model(TBD_I: int) -> int:
    """model of dummy"""
    return TBD_I
    
def power_model(POWER_MODE: int) -> int:
    """model of power"""
    if POWER_MODE:
        return True
    else:
        return False
