# QR codes in the release edition

*A brief for the publisher, from the journalist, 19 October 2026. Book version reviewed: v2.0.0-rc2 (printed). Site version that published it: v0.2.39.*

**Read.** The article [Paper that talks both ways](../../../articles/paper-that-talks-both-ways.md); tasks 1 and 2 are yours.

**In one line.** Every link in the release edition becomes a small QR code printing a short address from `admin/content/qr/links.json` (`gen-z-developers.sgit.ai/q/<id>/`); the build writes the page behind each code and refuses a code without one; `admin/build/qr_codes.py` draws new codes (needs segno). About 15 mm printed is enough. The credits idea (a book buyer gets credits for the site's billing) is a note for later.
