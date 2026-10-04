import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
const executable =
  process.env.BLENDER_PATH || 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe';
if (!existsSync(executable)) throw Error('Configura BLENDER_PATH con la ruta a Blender.');
const result = spawnSync(executable, ['--background', '--python', 'scripts/create_models.py'], {
  stdio: 'inherit',
});
process.exit(result.status ?? 1);
