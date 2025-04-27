#!/usr/bin/env node
// backend/scripts/addKey.js
const fs = require("fs");

const key = process.env.MDB_PRO_KEY;
if (!key) {
  console.error("MDB_PRO_KEY is not set. Aborting.");
  process.exit(1);
}

function replaceApiKey(filePath) {
  const content = fs.readFileSync(filePath, "utf8");
  const replaced = content.replace(
    /git\+https:\/\/oauth2:\[api-key-redacted\]@git\.mdbootstrap\.com/g,
    `git+https://oauth2:${key}@git.mdbootstrap.com`
  );
  fs.writeFileSync(filePath, replaced, "utf8");
  console.log(`Added MDB_PRO_KEY to ${filePath}`);
}

["package.json", "package-lock.json"].forEach(replaceApiKey);
