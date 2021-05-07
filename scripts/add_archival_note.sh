#!/bin/bash -e

cd $1
find -type f -printf '%P\0' | xargs -0 -n 1 -I '{}' sed -i '/<header>/a \ \ \ \ <div id="archival_note">This page is historical. Follow <a href="https://dmnes.org/{}">this link</a> for the current version.<\/a><\/div>' "{}"

sed -i '/archival_note/s/https\?:\/\/dmnes.org\/index.html/https:\/\/dmnes.org\//' index.html
