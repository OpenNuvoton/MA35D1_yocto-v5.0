#@TYPE: Machine
#@NAME: ma35d1
#@DESCRIPTION: Configuration for all ma35d1 boards (EV, DK, ...)
#@NEEDED_BSPLAYERS: layers/meta-openembedded/meta-oe layers/meta-openembedded/meta-python

MACHINEOVERRIDES ?= "ma35d1"
# =========================================================================
# Chip architecture
# =========================================================================
DEFAULTTUNE_ma35d1 = "cortexa35-crypto"
include conf/machine/include/arm/armv8a/tune-cortexa35.inc

# =========================================================================
# Kernel
# =========================================================================
PREFERRED_PROVIDER_virtual/kernel = "linux-ma35d1"
PREFERRED_PROVIDER_kernel = "linux-ma35d1"

# Default Linux kernel version (weak default "?=").
# Each machine .conf (or local.conf) can override it with:
#   KERNEL_VERSION = "<version>"
#
# Supported values (must match a linux-ma35d1 recipe version):
#   - 6.6.93 : fixed release 6.6.93
#   - 6.12.y : 6.12 stable branch (latest 6.12.x)
#   - 6.18.y : 6.18 stable branch (latest 6.18.x)
KERNEL_VERSION ?= "6.18.y"

# =========================================================================
# u-boot
# =========================================================================
PREFERRED_PROVIDER_virtual/bootloader = "u-boot-ma35d1"
PREFERRED_PROVIDER_u-boot = "u-boot-ma35d1"
EXTRA_IMAGEDEPENDS += "virtual/bootloader"

UBOOT_ENTRYPOINT_ma35d1 = "0x80E00000"
# =========================================================================
# trusted-firmware-a
# =========================================================================
PREFERRED_PROVIDER_virtual/trusted-firmware-a = "tf-a-ma35d1"
EXTRA_IMAGEDEPENDS += "virtual/trusted-firmware-a"
TFA_PLATFORM ?= "ma35d1"
TFA_DTB ?= "ma35d1xx7"
# =========================================================================
# optee-os
# =========================================================================
PREFERRED_PROVIDER_virtual/optee-os = "optee-os-ma35d1"
EXTRA_IMAGEDEPENDS += "virtual/optee-os"
OPTEE_PLATFORM = "ma35"
OPTEE_PLATFORM_FLAVOR = "MA35D1"
# =========================================================================
# m4proj
# =========================================================================
EXTRA_IMAGEDEPENDS += "m4proj"
# =========================================================================
# nuwriter
# =========================================================================
EXTRA_IMAGEDEPENDS += "python3-nuwriter-native"
# =========================================================================
# fs
# =========================================================================
IMAGE_FSTYPES ?= " sdcard ext4 tar.bz2"
IMAGE_CLASSES = "image_types_nvt"


# Use the expected value of the ubifs filesystem's volume name in the kernel
UBI_VOLNAME ?= "rootfs"
# The biggest NANDs on current modules are 100MB.
# This sums up to 2048 LEBs available for the ubifs (-c)
MKUBIFS_ARGS ?= "-F -m 2048 -e 126976 -c 2800"
UBINIZE_ARGS ?= "-m 2048 -p 128KiB -s 2048 -O 2048"

# Block size for NAND, kb
NAND_BLKZ ?= "128"

# Block size for SPINAND, kb
SPINAND_BLKZ ?= "128"

# SD auto-resizes to Max on first boot,
# A specific disk must be selected
DISK_DRIVE ?= "mmcblk0"
DISK_NUM ?= "p1"

# Disable the serial console due to auto-serial-console
SERIAL_CONSOLES = "115200;ttyS0"

# we do not want to have getty running on tty1 as we run
# auto-serial-console there
USE_VT = "0"

# Free size for SD card, kb
SDCARD_FREE_SIZE ?="0"

# Image type
IMAGE_TYPEDEP:nand = "ubi"
IMAGE_TYPEDEP:spinand = "ubi"
IMAGE_TYPEDEP:spinor = "jffs2"
IMAGE_TYPEDEP:sdcard = "ext4"

# =========================================================================
# Anti-Rollback & A/B Boot
# =========================================================================
# "1" enables OTP anti-rollback (BL2/BL31 version counter) protection and
# dual-slot (A/B) signed-FIT kernel boot on sdcard/nand/spinand. Requires
# SECURE_BOOT = "yes" (enforced in image_types_nvt.bbclass / nvt_tool.py).
MA35_ANTI_ROLLBACK_AB_BOOT ?= "0"

# Anti-rollback version counters; bump on release to block older images.
# NOTE: OTP fuse bits can only be programmed (0->1), never reset.
MA35_ARB_LINUX_VER ?= "0"
MA35_ARB_BL2_VER ?= "0"
MA35_ARB_BL31_VER ?= "0"

# CONFIG_MTDPARTS_DEFAULT body (after "mtdparts=<dev>:") used when AB-boot
# is enabled, adding a redundant uboot/uboot-env/device-tree/kernel slot B.
MA35_UBOOT_MTDPARTS_AB ?= "3m(uboot),768k(uboot-env),256k(device-tree),24m(kernel),3m(uboot_b),768k(uboot-env_b),256k(device-tree_b),24m(kernel_b),100m(rootfs)"


