#!/usr/bin/env node

const fs = require('fs');
const dst = JSON.parse(
  fs.readFileSync(__dirname + '/../_package.json').toString()
);

delete dst.scripts;

fs.writeFileSync(__dirname + '/../package.json', JSON.stringify(dst, null, 2));
