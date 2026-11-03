# CVE information for the MA35 U-Boot (based on v2020.07)

# The recipe does not include poky's u-boot-common.inc, so set the same
# CVE_PRODUCT here; otherwise cve-check looks up the recipe name and
# finds no U-Boot CVEs.
CVE_PRODUCT = "u-boot:u-boot denx:u-boot"

# Not applicable to the MA35 defconfigs. If a product enables the
# related options, these CVEs must be re-evaluated.
CVE_STATUS[CVE-2022-30767] = "not-applicable-config: nfs_lookup_reply in net/nfs.c; CONFIG_CMD_NFS is disabled in all MA35 defconfigs"
CVE_STATUS[CVE-2026-29009] = "not-applicable-config: nfs_readlink_reply in net/nfs.c; CONFIG_CMD_NFS is disabled in all MA35 defconfigs"
CVE_STATUS[CVE-2022-34835] = "not-applicable-config: i2c md command in cmd/i2c.c; CONFIG_CMD_I2C is disabled in all MA35 defconfigs"
CVE_STATUS[CVE-2022-2347] = "not-applicable-config: USB DFU; CONFIG_DFU and CONFIG_CMD_DFU are disabled in all MA35 defconfigs"

# The vulnerable code does not exist in v2020.07.
CVE_STATUS[CVE-2026-29007] = "cpe-incorrect: tcp_rx_state_machine in net/tcp.c; v2020.07 has no TCP stack"
CVE_STATUS[CVE-2026-29008] = "cpe-incorrect: tcp_rx_state_machine in net/tcp.c; v2020.07 has no TCP stack"
CVE_STATUS[CVE-2024-57254] = "cpe-incorrect: squashfs support was added in v2020.10, not present in v2020.07"
CVE_STATUS[CVE-2024-57255] = "cpe-incorrect: squashfs support was added in v2020.10, not present in v2020.07"
CVE_STATUS[CVE-2024-57257] = "cpe-incorrect: squashfs support was added in v2020.10, not present in v2020.07"
CVE_STATUS[CVE-2024-57258] = "cpe-incorrect: squashfs support was added in v2020.10, not present in v2020.07"
CVE_STATUS[CVE-2024-57259] = "cpe-incorrect: squashfs support was added in v2020.10, not present in v2020.07"
