do_image_nand[depends] = "virtual/trusted-firmware-a:do_deploy \
                          ${@bb.utils.contains('MACHINE_FEATURES', 'optee', 'virtual/optee-os:do_deploy', '',d)} \
                          virtual/kernel:do_deploy \
                          virtual/bootloader:do_deploy \
                          python3-nuwriter-native:do_install \
                          jq-native:do_populate_sysroot \
                          mtd-utils-native:do_populate_sysroot \
                          m4proj:do_deploy \
                         "

do_image_spinand[depends] = "virtual/trusted-firmware-a:do_deploy \
                             ${@bb.utils.contains('MACHINE_FEATURES', 'optee', 'virtual/optee-os:do_deploy', '',d)} \
                             virtual/kernel:do_deploy \
                             virtual/bootloader:do_deploy \
                             python3-nuwriter-native:do_install \
                             jq-native:do_populate_sysroot \
                             mtd-utils-native:do_populate_sysroot \
                             m4proj:do_deploy \
                             ${@bb.utils.contains('IMAGE_FSTYPES', 'nand', '${IMAGE_BASENAME}:do_image_nand', '', d)} \
                            "

do_image_spinor[depends] = "virtual/trusted-firmware-a:do_deploy \
                             ${@bb.utils.contains('MACHINE_FEATURES', 'optee', 'virtual/optee-os:do_deploy', '',d)} \
                             virtual/kernel:do_deploy \
                             virtual/bootloader:do_deploy \
                             python3-nuwriter-native:do_install \
                             jq-native:do_populate_sysroot \
                             mtd-utils-native:do_populate_sysroot \
                             m4proj:do_deploy \
                             ${@bb.utils.contains('IMAGE_FSTYPES', 'nand', '${IMAGE_BASENAME}:do_image_nand', '', d)} \
                             ${@bb.utils.contains('IMAGE_FSTYPES', 'spinand', '${IMAGE_BASENAME}:do_image_spinand', '', d)} \
                            "

do_image_sdcard[depends] = "parted-native:do_populate_sysroot \
                            virtual/trusted-firmware-a:do_deploy \
                            ${@bb.utils.contains('MACHINE_FEATURES', 'optee', 'virtual/optee-os:do_deploy', '',d)} \
                            virtual/kernel:do_deploy \
                            virtual/bootloader:do_deploy \
                            python3-nuwriter-native:do_install \
                            jq-native:do_populate_sysroot \
                            m4proj:do_deploy \
                            ${@bb.utils.contains('IMAGE_FSTYPES', 'nand', '${IMAGE_BASENAME}:do_image_nand', '', d)} \
                            ${@bb.utils.contains('IMAGE_FSTYPES', 'spinand', '${IMAGE_BASENAME}:do_image_spinand', '', d)} \
                            ${@bb.utils.contains('IMAGE_FSTYPES', 'spinor', '${IMAGE_BASENAME}:do_image_spinor', '', d)} \
                           "
