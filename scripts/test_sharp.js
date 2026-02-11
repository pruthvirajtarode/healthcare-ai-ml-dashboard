const sharp = require('sharp');
sharp(Buffer.from('<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect width="100" height="100" fill="red"/></svg>'))
    .png()
    .toFile('test.png')
    .then(() => console.log('success'))
    .catch(e => console.error(e));
