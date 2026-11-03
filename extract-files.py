#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from pathlib import Path

namespace_imports = [
    'device/oppo/CPH2185',
]

module = ExtractUtilsModule(
    'CPH2185',
    'oppo',
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()

    android_root = Path(__file__).resolve().parents[3]
    vendor_makefile = android_root / 'vendor/oppo/CPH2185/CPH2185-vendor.mk'
    if vendor_makefile.exists():
        lines = vendor_makefile.read_text().splitlines()
        lines = [line for line in lines if not any(
            apk in line for apk in (
                'SoterService/SoterService.apk',
                'EmCamera/EmCamera.apk',
            )
        )]
        contents = '\n'.join(lines).rstrip()
        if 'PRODUCT_PACKAGES += SoterService EmCamera' not in contents:
            contents += '\n\nPRODUCT_PACKAGES += SoterService EmCamera'
        vendor_makefile.write_text(contents + '\n')
