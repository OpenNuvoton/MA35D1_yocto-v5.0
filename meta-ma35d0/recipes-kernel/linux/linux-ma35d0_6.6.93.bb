# Copyright 2025 Nuvoton
# Released under the MIT license (see COPYING.MIT for the terms)

SUMMARY = "Linux Kernel provided and supported by Nuvoton"
DESCRIPTION = "Linux Kernel provided and supported by Nuvoton MA35D0"

inherit kernel
PACKAGE_WRITE_DEPS += "cross-localedef-native qemuwrapper-cross"
LICENSE = "GPL-2.0-only"
LIC_FILES_CHKSUM = "file://COPYING;md5=6bc538ed5bd9a7fc9398086aedcd7e46"

# We need to pass it as param since kernel might support more then one
# machine, with different entry points
MA35D0_KERNEL_LOADADDR = "0x80080000"
KERNEL_EXTRA_ARGS += "LOADADDR=${MA35D0_KERNEL_LOADADDR}"

KERNEL_SRC ?= "git://github.com/OpenNuvoton/MA35D1_linux-6.6.y.git;branch=master;protocol=https"
SRC_URI = "${KERNEL_SRC}"
SRCREV = "${KERNEL_SRCREV}"

SRCBRANCH = "6.6.93"
LOCALVERSION = "-${SRCBRANCH}"

SRC_URI += " \
    file://optee.config \
    file://dts-reserve \
    file://ampipi.sh \
    file://cfg80211.config \
    "
PV = "${SRCBRANCH}+git${SRCPV}"
S = "${WORKDIR}/git"
B = "${WORKDIR}/build"

SRC_URI += "${@bb.utils.contains('DISTRO_FEATURES', 'rt-patch', ' file://patch-6.6.93-rt55.patch', '', d)}"

DEFAULT_PREFERENCE = "1"
DEPENDS += "util-linux-native libyaml-native openssl-native"
# =========================================================================
# Kernel
# =========================================================================
KERNEL_IMAGETYPE = "Image"

do_deploy:append() {
    for dtbf in ${KERNEL_DEVICETREE}; do
        dtb=`normalize_dtb "$dtbf"`
        dtb_ext=${dtb##*.}
        dtb_base_name=`basename $dtb .$dtb_ext`
	ln -sf $dtb_base_name.dtb ${DEPLOYDIR}/Image.dtb
    done
}

do_configure:prepend() {
    bbnote "Copying defconfig"
    cp ${S}/arch/${ARCH}/configs/${KERNEL_DEFCONFIG} ${WORKDIR}/defconfig
    cat ${WORKDIR}/cfg80211.config >> ${WORKDIR}/defconfig

    if [ "${TFA_LOAD_SCP}" = "yes" ]; then        
        if [ "${TFA_SCP_M4}" = "no" ]; then
            for dtbf in ${KERNEL_DEVICETREE}; do
	        dt=$(echo $dtbf | sed 's/\.dtb/\.dts/')
                if [ "${TFA_SCP_IPI}" = "yes" ]; then
                    ${WORKDIR}/ampipi.sh ${S}/arch/${ARCH}/boot/dts/nuvoton/${TFA_PLATFORM}.dtsi
                fi
                ${WORKDIR}/dts-reserve ${S}/arch/${ARCH}/boot/dts/${dt} ${TFA_SCP_BASE} ${TFA_SCP_LEN}
            done
        fi
    fi

    if ${@bb.utils.contains('MACHINE_FEATURES', 'optee', 'true', 'false', d)}; then
        cat ${WORKDIR}/optee.config >> ${WORKDIR}/defconfig
    fi
}

correct_buildpaths() {
    FILES=" \
    ${B}/drivers/video/logo/logo_linux_clut224.c \
    ${B}/drivers/tty/vt/consolemap_deftbl.c \
    ${B}/lib/oid_registry_data.c \
    "
    for f in $FILES; do
        if [ -e $f ]; then
            sed -i "s|${TMPDIR}||g" $f
        fi
    done
}

do_install:append() {
    correct_buildpaths
}

COMPATIBLE_MACHINE = "(ma35d0)"

