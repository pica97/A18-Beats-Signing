# A18 v2.0 R7 — Public Shortcut Signing Channel Handoff

Authorization:
`A18-v2.0-R7-PUBLIC-SHORTCUT-SIGNING-CHANNEL-01 = AUTHORIZED`

Target public repository:
`pica97/A18-Beats-Signing`

Purpose:
- Public, no-secrets signing/distribution channel only.
- Generate A18 Bridge R2 from deterministic source.
- Sign with Apple's official macOS `shortcuts sign --mode anyone`.
- Publish the signed `.shortcut` file and SHA-256.
- No LightCube workspace, private A18 source, tokens, credentials, Apple IDs, Spotify secrets, or private project artifacts.

Source prepared in private A18 repo:
- `tools/shortcuts/build_a18_bridge_r2.py`
- `.github/workflows/build-a18-bridge-r2.yml`
- `r7-field-probe/A18-BRIDGE-R2-GENERATION.md`

Target Shortcut behavior:
- FOCUS: Clipboard=PAUSE -> run existing A18 Bridge -> Speak Text "Modo focus activo" -> Clipboard=RESUME -> run existing A18 Bridge -> exit.
- DEPORTE: Speak Text "Modo deporte activo" while media remains active -> exit.
- Other core tokens delegate to existing A18 Bridge.

Security:
- The current A18 Bridge remains untouched.
- R2 is installed separately until physical PASS.
- Apple import confirmation remains mandatory.
