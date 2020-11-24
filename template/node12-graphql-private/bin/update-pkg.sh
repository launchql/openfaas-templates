#!/bin/bash

# only for development, when building the image via docker, the volume is NOT mounted.
# so this is to mitigate the issue where the 2nd npm install was not picking up the handler 
# created by the dev, and instead was npm installing the templated one with 0 deps

NPM_TOKEN=`cat $NPM_TOKEN_FILE`
echo //registry.npmjs.org/:_authToken=$NPM_TOKEN > /home/app/.npmrc
echo scripts-prepend-node-path=true >> /home/app/.npmrc

cp src/function/handler.json _handler.json 
node ./bin/merge.js
yarn install
rm /home/app/.npmrc
yarn build
