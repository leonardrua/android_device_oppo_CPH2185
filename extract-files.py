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
    vendor_fstab = android_root / 'vendor/oppo/CPH2185/proprietary/vendor/etc/fstab.mt6765'
    product_mount = 'product /product ext4 ro wait,logical,first_stage_mount'
    if vendor_fstab.exists():
        original_lines = vendor_fstab.read_text().splitlines()
        vendor_mount = next(
            (i for i, line in enumerate(original_lines)
             if line.startswith('vendor /vendor ')),
            None,
        )
        if vendor_mount is not None:
            fstab_lines = [
                line for line in original_lines
                if not line.startswith('oppo_product /oppo_product ')
            ]
            if product_mount not in fstab_lines:
                vendor_mount = next(
                    i for i, line in enumerate(fstab_lines)
                    if line.startswith('vendor /vendor ')
                )
                fstab_lines.insert(vendor_mount + 1, product_mount)
            if fstab_lines != original_lines:
                vendor_fstab.write_text('\n'.join(fstab_lines) + '\n')

    vendor_init = android_root / 'vendor/oppo/CPH2185/proprietary/vendor/etc/init/self-init.rc'
    if vendor_init.exists():
        original_contents = vendor_init.read_text()
        init_contents = original_contents.replace(
            '/dev/block/mapper/oppo_product', '/dev/block/mapper/product'
        )
        if init_contents != original_contents:
            vendor_init.write_text(init_contents)

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
