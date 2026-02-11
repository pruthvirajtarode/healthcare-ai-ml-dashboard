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

        console.log(`Converting ${svgPath} to ${pngPath}...`);

        try {
            await sharp(svgPath)
                .png()
                .toFile(pngPath);
            console.log(`Successfully converted ${file}`);
        } catch (err) {
            console.error(`Error converting ${file}:`, err);
        }
    }
}

convert();
