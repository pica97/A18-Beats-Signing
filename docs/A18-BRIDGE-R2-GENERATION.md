# A18 Bridge R2 generated wrapper

Goal: eliminate manual block editing on the Owner's iPhone.

The generated Shortcut is named A18 Bridge R2. It does not mutate the already-proven A18 Bridge. It wraps it:

- FOCUS: Clipboard=PAUSE -> run A18 Bridge -> Speak Text -> Clipboard=RESUME -> run A18 Bridge -> exit.
- DEPORTE: Speak Text while media remains active -> exit.
- Every other token: delegate once to A18 Bridge.

The unsigned plist is generated deterministically by tools/shortcuts/build_a18_bridge_r2.py.
A macOS GitHub Actions job signs it with Apple's official shortcuts sign --mode anyone command.
The signed file is published to dist/A18-Bridge-R2.shortcut.

Apple still requires the user to confirm Add Shortcut when importing a signed Shortcut. Silent installation is not possible.


Signing channel initialized on public satellite repository.
