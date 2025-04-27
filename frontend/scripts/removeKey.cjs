#!/usr/bin/env node
// backend/scripts/removeKey.js
const fs = require("fs");

const key = process.env.MDB_PRO_KEY;
if (!key) {
    console.error("MDB_PRO_KEY is not set. Aborting.");
    process.exit(1);
}

function removeApiKey(filePath) {
    const content = fs.readFileSync(filePath, "utf8");
    // We build a dynamic regexp in case the key changes
    const keyRegex = new RegExp(`git\\+https:\\/\\/oauth2:${key}@git\\.mdbootstrap\\.com`, "g");
    const replaced = content.replace(
        keyRegex,
        "git+https://oauth2:[api-key-redacted]@git.mdbootstrap.com"
    );
    fs.writeFileSync(filePath, replaced, "utf8");
    console.log(`Removed MDB_PRO_KEY from ${filePath}`);
}

["package.json", "package-lock.json"].forEach(removeApiKey);
