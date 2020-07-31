#!/usr/bin/env node

const fs = require('fs');
const merge = require('package-merge');
const dst = fs.readFileSync(__dirname + '/../package.json');
const src = fs.readFileSync(__dirname + '/../_handler.json');

// Create a new `package.json`
fs.writeFileSync(__dirname + '/../package.json', merge(dst, src));
