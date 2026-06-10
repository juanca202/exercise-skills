const fs = require('fs');
const path = require('path');

const projectRoot = process.argv[2];
const packageJsonPath = path.join(projectRoot, 'package.json');

if (!fs.existsSync(packageJsonPath)) {
  console.error('package.json not found');
  process.exit(1);
}

const pkg = JSON.parse(
  fs.readFileSync(packageJsonPath, 'utf8')
);

console.log(`Project: ${pkg.name || 'Unknown'}`);
console.log(`Version: ${pkg.version || 'Unknown'}`);

const dependencies = Object.keys(pkg.dependencies || {});
const devDependencies = Object.keys(pkg.devDependencies || {});

console.log(`Dependencies: ${dependencies.length}`);
console.log(`Dev Dependencies: ${devDependencies.length}`);

if (dependencies.length) {
  console.log('\nMain dependencies:');
  dependencies.slice(0, 10).forEach(dep => {
    console.log(`- ${dep}`);
  });
}