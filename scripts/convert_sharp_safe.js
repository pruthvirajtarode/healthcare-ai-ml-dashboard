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

        console.log(`--- Processing ${file} ---`);

        try {
            if (!fs.existsSync(svgPath)) {
                console.error(`ERROR: File not found: ${svgPath}`);
                continue;
            }

            let svgContent = fs.readFileSync(svgPath, 'utf8');

            // Remove emojis as they often crash SVG renderers without specific fonts
            svgContent = svgContent.replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F1E6}-\u{1F1FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, '');

            // Ensure & is escaped correctly (only if not already part of an entity)
            // This is a simple fix for "no name" entity errors
            svgContent = svgContent.replace(/&(?!lt;|gt;|amp;|quot;|apos;)/g, '&amp;');

            console.log(`Sanitized size: ${svgContent.length} bytes`);

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
