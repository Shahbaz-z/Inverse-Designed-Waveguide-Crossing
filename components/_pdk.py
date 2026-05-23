"""Activate GDSFactory generic PDK once (required for cross sections in v9+)."""

import gdsfactory as gf

_pdk_active = False


def ensure_generic_pdk() -> None:
    global _pdk_active
    if _pdk_active:
        return
    try:
        gf.get_active_pdk()
    except ValueError:
        gf.gpdk.PDK.activate()
    _pdk_active = True
