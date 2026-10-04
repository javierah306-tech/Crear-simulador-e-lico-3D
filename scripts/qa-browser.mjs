import { createRequire } from 'node:module';
import { mkdir, writeFile } from 'node:fs/promises';
const require = createRequire(
  'C:/Users/javie/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/package.json',
);
const { chromium } = require('playwright');
await mkdir('tmp/qa', { recursive: true });
const browser = await chromium.launch({
  channel: 'msedge',
  headless: true,
  args: ['--enable-webgl', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
});
const page = await browser.newPage({
  viewport: { width: 1440, height: 1050 },
  deviceScaleFactor: 1,
});
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => {
  if (m.type() === 'error') errors.push(m.text());
});
await page.goto('http://127.0.0.1:5173/', { waitUntil: 'networkidle' });
await page.waitForTimeout(3000);
await page.screenshot({ path: 'tmp/qa/desktop.png', fullPage: true });
await page.getByRole('button', { name: 'Vista interior', exact: true }).click();
await page.waitForTimeout(1600);
await page.screenshot({ path: 'tmp/qa/interior.png', fullPage: true });
const canvas = page.locator('canvas');
const imageA = await canvas.screenshot();
await page.waitForTimeout(700);
const imageB = await canvas.screenshot();
if (imageA.equals(imageB)) throw Error('El rotor no anima.');
await page.getByRole('button', { name: 'Pausar animación', exact: true }).click();
await page.waitForTimeout(400);
const box = await canvas.boundingBox();
await page.mouse.click(box.x + box.width * 0.44, box.y + box.height * 0.53);
await page.getByRole('region', { name: /Información de/ }).waitFor({ timeout: 5000 });
await page.getByRole('button', { name: 'Cerrar componente' }).click();
await page.getByRole('button', { name: 'Reanudar animación', exact: true }).click();
await page.getByRole('button', { name: 'Generador', exact: true }).click();
await page.waitForTimeout(1000);
await page.screenshot({ path: 'tmp/qa/selected.png', fullPage: true });
await page.getByRole('button', { name: 'Cerrar componente' }).click();
await page.getByRole('button', { name: 'Separar componentes' }).click();
await page.waitForTimeout(1000);
await page.screenshot({ path: 'tmp/qa/exploded.png', fullPage: true });
await page.getByRole('button', { name: 'Ficha técnica', exact: true }).click();
await page.getByText('Supuestos de la simulación', { exact: true }).click();
await page.screenshot({ path: 'tmp/qa/sheet.png', fullPage: true });
await page.getByRole('button', { name: 'Cerrar ficha técnica' }).click();
await page.getByRole('button', { name: 'Catálogo técnico', exact: true }).click();
await page.screenshot({ path: 'tmp/qa/catalog.png', fullPage: true });
const rows = await page.locator('tbody tr').count();
if (rows !== 9) throw Error('Se esperaban nueve filas de catálogo.');
await page.getByRole('button', { name: 'Ver modelo', exact: true }).nth(3).click();
await page.waitForTimeout(1800);
await page.getByRole('button', { name: 'Vista interior', exact: true }).click();
await page.waitForTimeout(1500);
await page.screenshot({ path: 'tmp/qa/geared.png', fullPage: true });
await page.setViewportSize({ width: 390, height: 844 });
await page.waitForTimeout(1000);
await page.screenshot({ path: 'tmp/qa/mobile.png', fullPage: true });
if (await page.evaluate(() => document.documentElement.scrollWidth > innerWidth))
  throw Error('Desbordamiento horizontal en móvil.');
if (await page.locator('input[type=range]').count())
  throw Error('Se encontraron controles de viento no solicitados.');
await page.setViewportSize({ width: 1440, height: 1050 });
const cards = page.locator('.model-card');
for (let i = 0; i < 9; i++) {
  await cards.nth(i).click();
  await page.getByRole('button', { name: 'Vista exterior', exact: true }).click();
  await page.waitForTimeout(500);
  await page.getByRole('button', { name: 'Vista interior', exact: true }).click();
  await page.waitForTimeout(600);
  if (await page.getByText('No se pudo cargar la vista 3D', { exact: true }).count())
    throw Error('Error de GLB en modelo ' + i);
}
await cards.first().click();
await page.getByRole('button', { name: 'Vista exterior', exact: true }).click();
await writeFile(
  'tmp/qa/results.json',
  JSON.stringify({ errors, rows, viewport: '390×844,1440×1050' }, null, 2),
);
await browser.close();
if (errors.length) throw Error(errors.join('\n'));
console.log('QA inicial OK: exterior, interior, selección, explosión, ficha, catálogo y móvil.');
