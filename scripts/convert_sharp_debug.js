const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const diagramsDir = 'c:\\Users\\pruth\\OneDrive\\Desktop\\HealthAI Pro\\healthcare-ml-project\\diagrams';
const svgFiles = [
    'use-case-diagram.svg',
    'class-diagram.svg',
    'sequence-diagram.svg',
    'system-architecture.svg'
];

async function convert() {
    for (const file of svgFiles) {
        const svgPath = path.join(diagramsDir, file);
        const pngPath = path.join(diagramsDir, file.replace('.svg', '.png'));

        console.log(`--- Converting ${file} ---`);

        try {
            if (!fs.existsSync(svgPath)) {
                console.error(`ERROR: File not found: ${svgPath}`);
                continue;
            }

            const svgContent = fs.readFileSync(svgPath, 'utf8');
            console.log(`File size: ${svgContent.length} bytes`);

            await sharp(Buffer.from(svgContent))
                .png()
                .toFile(pngPath);

            console.log(`SUCCESS: Saved to ${pngPath}`);
        } catch (err) {
            console.error(`FAILURE: Error converting ${file}:`, err.message);
        }
    }
}

convert();
