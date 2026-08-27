const { readFileSync, writeFileSync } = require('fs');

const xml = readFileSync('atom.xml', 'utf-8');
const entries = [...xml.matchAll(/<entry\b[\s\S]*?<\/entry>/g)].slice(0, 5);
// ponytail: regex over fast-xml-parser; atom's <content type="html"> is HTML-escaped so nested tags can't collide. Upgrade if feed source ever changes format.
const posts = entries.map((m) => {
    const e = m[0];
    const title = e.match(/<title>([\s\S]*?)<\/title>/)[1];
    const date = e.match(/<updated>([\s\S]*?)<\/updated>/)[1].split('T')[0];
    const url = e.match(/<link rel="alternate"[^>]*href="([^"]+)"/)[1];
    return `-   ${date} [${title}](${url}?utm_source=GitHubProfile)`;
});

let readme = readFileSync('README.md', 'utf-8');
readme = readme.replace(/(?<=<!--START_SECTION:blog-posts-->\n)[\s\S]*(?=\n<!--END_SECTION:blog-posts-->)/, posts.join('\n'));
writeFileSync('README.md', readme);
