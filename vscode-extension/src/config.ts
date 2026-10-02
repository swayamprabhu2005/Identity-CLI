import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import * as vscode from 'vscode';

export interface IdentityPreferences {
  defaultLocation: string;
  defaultFields: string[];
  defaultQuantity: number;
  defaultFormat: string;
  folderName: string;
  setupCompleted: boolean;
}

export function getSharedConfigPath(): string {
  const envConfig = process.env.IDENTITY_CONFIG_DIR;
  if (envConfig) {
    return path.join(envConfig, 'config.json');
  }

  if (process.platform === 'win32') {
    const appData = process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming');
    return path.join(appData, 'IdentityCLI', 'config.json');
  }

  const xdgConfig = process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config');
  return path.join(xdgConfig, 'identity-cli', 'config.json');
}

export function readSharedConfig(): Partial<IdentityPreferences> {
  const configPath = getSharedConfigPath();
  if (!fs.existsSync(configPath)) {
    return {};
  }
  try {
    const raw = fs.readFileSync(configPath, 'utf8');
    const data = JSON.parse(raw);
    return {
      defaultLocation: data.default_location || '',
      defaultFields: data.default_fields || ['name', 'email', 'password'],
      defaultQuantity: data.default_quantity || 1,
      defaultFormat: data.default_format || 'terminal',
      folderName: data.folder_name || 'generated-names',
      setupCompleted: Boolean(data.setup_completed),
    };
  } catch {
    return {};
  }
}

export function saveSharedConfig(prefs: IdentityPreferences): void {
  const configPath = getSharedConfigPath();
  const dir = path.dirname(configPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  let existing: Record<string, any> = {};
  if (fs.existsSync(configPath)) {
    try {
      existing = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    } catch {
      existing = {};
    }
  }

  existing.default_location = prefs.defaultLocation;
  existing.default_fields = prefs.defaultFields;
  existing.default_quantity = prefs.defaultQuantity;
  existing.default_format = prefs.defaultFormat;
  existing.folder_name = prefs.folderName;
  existing.setup_completed = prefs.setupCompleted;

  fs.writeFileSync(configPath, JSON.stringify(existing, null, 2), 'utf8');
}

export function getPreferences(): IdentityPreferences {
  const shared = readSharedConfig();
  const vscodeConfig = vscode.workspace.getConfiguration('identityGenerator');

  return {
    defaultLocation: shared.defaultLocation || vscodeConfig.get<string>('defaultLocation') || path.join(os.homedir(), 'IdentityData'),
    defaultFields: shared.defaultFields || vscodeConfig.get<string[]>('defaultFields') || ['name', 'email', 'password'],
    defaultQuantity: shared.defaultQuantity || vscodeConfig.get<number>('defaultQuantity') || 1,
    defaultFormat: shared.defaultFormat || vscodeConfig.get<string>('defaultFormat') || 'terminal',
    folderName: shared.folderName || vscodeConfig.get<string>('folderName') || 'generated-names',
    setupCompleted: shared.setupCompleted ?? false,
  };
}

export async function persistPreferences(prefs: IdentityPreferences): Promise<void> {
  // 1. Save to shared config.json for CLI
  saveSharedConfig(prefs);

  // 2. Save to VS Code configuration
  const vscodeConfig = vscode.workspace.getConfiguration('identityGenerator');
  await vscodeConfig.update('defaultLocation', prefs.defaultLocation, vscode.ConfigurationTarget.Global);
  await vscodeConfig.update('defaultFields', prefs.defaultFields, vscode.ConfigurationTarget.Global);
  await vscodeConfig.update('defaultQuantity', prefs.defaultQuantity, vscode.ConfigurationTarget.Global);
  await vscodeConfig.update('defaultFormat', prefs.defaultFormat, vscode.ConfigurationTarget.Global);
  await vscodeConfig.update('folderName', prefs.folderName, vscode.ConfigurationTarget.Global);
}
