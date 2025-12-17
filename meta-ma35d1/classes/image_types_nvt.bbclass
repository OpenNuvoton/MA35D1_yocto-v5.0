inherit image_types
inherit image_nvt

DEPENDS = " python3-nuwriter-native gcc-arm-none-eabi-native"
include image_nvt.inc
NUWRITER_DIR="${RECIPE_SYSROOT_NATIVE}${datadir}/nuwriter"

nvt_generate_image() {
    if ${@bb.utils.contains('MACHINE_FEATURES', 'optee', 'true', 'false', d)}; then
        TFA_LOAD_OPTEE="yes"
    else
        TFA_LOAD_OPTEE="no"
    fi
    ${PYTHON} ${NTOOL} \
        --deploy_dir "${DEPLOY_DIR_IMAGE}" \
        --imgdeploy_dir "${IMGDEPLOYDIR}" \
        --image_name "${IMAGE_NAME}" \
        --image_basename "${IMAGE_BASENAME}" \
        --machine "${MACHINE}" \
        --secure_boot "${SECURE_BOOT}" \
        --aes_key "${AES_KEY}" \
        --ecdsa_key "${ECDSA_KEY}" \
        --tfa_load_m4 "${TFA_LOAD_M4}" \
        --tfa_m4_bin "${TFA_M4_BIN}" \
        --tfa_load_optee "${TFA_LOAD_OPTEE}" \
        --tfa_platform "${TFA_PLATFORM}" \
        --nuwriter_dir "${NUWRITER_DIR}" \
        --ubinize_args "${UBINIZE_ARGS}" \
        --sd_rootfs_size "${ROOTFS_SIZE}" \
        --image "$1"
}

IMAGE_CMD:sdcard() {
    nvt_generate_image "SD"
}

IMAGE_CMD:spinand() {
    nvt_generate_image "SPINAND"
}

IMAGE_CMD:nand() {
    nvt_generate_image "NAND"
}

IMAGE_CMD:spinor() {
    nvt_generate_image "SPINOR"
}



