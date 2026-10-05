FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

# GC520 2D stack support: DRM backend pixman-renderer, GBM/dmabuf scanout
# under pixman, KMS plane dmabuf format advertisement, and cursor plane
# support. Ported from Buildroot's Weston 10.0.5 patches to this recipe's
# Weston 13.0.1; two of the original four fixes are no longer needed
# (superseded by upstream refactors between 10.0.5 and 13.0.1) - see each
# patch's own commit message for details.
SRC_URI += " \
    file://0002-drm-pixman-advertise-linux-dmabuf-and-kms-plane-formats.patch \
    file://0003-state-propose-planes-only-no-buffer-skip-dual-client.patch \
    file://0005-drm-backend-cursor-plane-gbm-pixman.patch \
    "

# shell-kiosk/shell-ivi are load-bearing for this BSP (used by
# weston-kiosk.ini/weston-ivi.ini in the weston-init bbappend)
