# MA35D1 BSP Recipe CVE Reports — numaker-som-ma35d16a81 (Yocto 5.0)

This report package presents recipe-level CVE scan results from the MA35D1 BSP
`core-image-minimal` build. It covers target software, boot components, and
native and cross-build tools for which Yocto produced a CVE report. Start at the
searchable [report index](./index.html) to review scan results, see the evidence
behind each triage category, and identify findings that need follow-up.

This is a standalone report snapshot. The HTML pages work offline; external
advisory links require network access. The results describe scanned recipes,
not the set of packages installed in the rootfs or whether a vulnerability is
reachable in the delivered image.

## Files

| File | Description |
|---|---|
| [`index.html`](./index.html) | Recipe index with aggregate counts, search, and a filter for recipes that still have entries under investigation. |
| `<recipe>.html` (for example, [`glibc.html`](./glibc.html)) | The recipe's CVE entries, the original Yocto scan status and notes, and the HTML triage category and reason. |
| `<recipe>.openvex.json` (for example, [`glibc.openvex.json`](./glibc.openvex.json)) | OpenVEX v0.2.0 with one statement per reported CVE; classifications match the recipe's HTML report. |

The snapshot covers **245 recipe HTML reports** and **19,768 recipe/CVE
entries**. The **119 recipes with CVE entries** also have an OpenVEX document.
The other **126 recipes** have HTML reports only: their Yocto reports list no
CVEs, and the [OpenVEX schema](https://github.com/openvex/spec/blob/main/openvex_json_schema.json)
requires at least one statement. A missing OpenVEX file does not mean
`not_affected`.

## Scan evidence and scope

The primary inputs were Yocto `cve-check` reports
(`build/tmp-glibc/deploy/cve/*_cve.json`). That directory can contain results
retained from different scan runs. A `log.do_cve_check` task log was used only
when a unique, completed task had a byte-for-byte matching `cve.json`. This
distinguishes version-range exclusions from recorded recipe fixes when Yocto
labels both `Patched`.

The OpenVEX identifiers use `pkg:generic/yocto/…` and include the recipe version,
layer, and SHA-256 of the source report. The hash identifies the scan report,
not the built artifact. The documents are for recipe triage, not image-level
product assessments.

## Classification

The HTML and recipe OpenVEX use the same four [OpenVEX status labels](https://github.com/openvex/spec/blob/main/OPENVEX-SPEC.md#status-labels)
for automated recipe-level triage. The original Yocto status remains visible
and can be filtered separately. Counts are recipe/CVE pairs, not unique CVE IDs.

| Triage status | Entries in this snapshot | Basis |
|---|---:|---|
| Not Affected | 18,727 | An explicit Yocto exclusion note (CPE, configuration, or platform), or a matching task log that records a version-range exclusion. |
| Affected | 954 | Yocto reports `Unpatched`; treated as potentially affected pending validation. |
| Fixed | 69 | Yocto records a fixed version or backport, or the matching task log records a recipe patch or fix metadata. |
| Under Investigation | 18 | The available JSON and task log do not justify a final classification. |

### Example: BusyBox 1.36.1 and CVE-2022-48174

The [BusyBox HTML report](./busybox.html) and [BusyBox OpenVEX](./busybox.openvex.json)
show CVE-2022-48174 as `affected` at recipe scope. The NVD summary says
“before 1.35,” but the [structured NVD record](https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2022-48174)
has `versionEndIncluding: 1.36.1`. Yocto used that range, matched the scanned
version, and reported `Unpatched`. The build enabled `ash` (`CONFIG_ASH=y`),
and its patch log did not show a corresponding fix. This supports retaining
the recipe-level finding; it does not establish network reachability in the
delivered image.

## Why 18 entries remain Under Investigation

All 18 entries are reported as `Ignored` by Yocto and span 11 recipes.
`Ignored` indicates how Yocto handles the finding; it does not mean the issue
is fixed or that the delivered product is unaffected.

| Yocto reason | Entries | Why it remains under investigation |
|---|---:|---|
| `disputed` | 12 | The vulnerability determination is disputed. That disagreement alone does not establish whether the delivered product is affected. |
| `upstream-wontfix` | 5 | Upstream does not plan to fix the issue. This is not evidence that the affected code is absent or that the product is unaffected. |
| `ignored` | 1 | The generic ignore reason does not provide enough evidence to determine product impact. |

For example, the [CVE-2019-1010025 record](https://www.cve.org/CVERecord?id=CVE-2019-1010025)
records the upstream view that an ASLR bypass alone is not a vulnerability.
The [glibc report](./glibc.html) shows that the issue is disputed; it does not
establish that this product is unaffected.

OpenVEX does not prescribe a mapping from `Ignored` or `disputed` to
`not_affected`. The [statement fields](https://github.com/openvex/spec/blob/main/OPENVEX-SPEC.md#statement-fields)
require a `not_affected` statement to include a `justification` or an
`impact_statement` explaining why the specific product is unaffected. For
example, if review confirms that the delivered build excludes the vulnerable
code, `vulnerable_code_not_present` may apply. Until there is enough evidence
for a product-specific decision, keep the entry `under_investigation`.

To find these entries, select **Has Under Investigation entries** in
[the index](./index.html), open a recipe, and select **Under Investigation**
in its VEX triage filter. Each row shows the triage reason and the original
Yocto note. These notes explain the current status; they do not close the
product assessment.
