// Verify the assetUrl guard: kie/remote URLs must never reach an <img>.
global.window = {};
require('../renderer/api.js');
const { assetUrl } = global.window.api;
let pass = 0, fail = 0;
function reject(input, why) {
  try { assetUrl(input); console.log('FAIL (allowed) ' + why); fail++; }
  catch (e) { console.log('ok   rejected  ' + why); pass++; }
}
function allow(input, expectPrefix, why) {
  try {
    const u = assetUrl(input, 'V1');
    if (u.startsWith(expectPrefix) && u.includes('v=V1')) { console.log('ok   allowed   ' + why + ' -> ' + u); pass++; }
    else { console.log('FAIL wrong url ' + why + ' -> ' + u); fail++; }
  } catch (e) { console.log('FAIL (threw)   ' + why + ': ' + e.message); fail++; }
}
reject('https://tempfile.aiquickdraw.com/s/abc.png?token=xyz', 'kie signed CDN url');
reject('http://cdn.kie.ai/out/f1.png',                          'plain http remote');
reject('//cdn.kie.ai/out/f1.png',                               'protocol-relative remote');
reject('HTTPS://CDN.KIE.AI/F.PNG',                              'uppercase scheme');
reject('data:image/png;base64,iVBORw0KG',                        'data uri');
allow('beat01.png',        '/outputs/beat01.png',        'bare local filename');
allow('/beat01.png',       '/outputs/beat01.png',        'leading-slash local path');
allow('frames/beat01.png', '/outputs/frames/beat01.png', 'nested local path');
console.log(assetUrl('') === '' ? 'ok   empty -> empty string' : 'FAIL empty');
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
